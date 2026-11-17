#!/usr/bin/env python3
"""v1.8: analyze_usage.py 新增多文件 fleet 批量模式 + cacheRead 异常值防护(input+cacheRead 远超窗口时剔除统计并在报告中明示,防聚合被污染)。

v1.7: analyze_usage.py 末轮构成新增工具 schema 利用率(加载未用/前缀聚合,区分「清工具输出」与「精简工具集」两类治理)。

v1.5: analyze_usage.py 支持 OpenClaw trajectory 格式。

设计依据(2026-10-27 实测本机 6 个 agents × 数百会话):
- OpenClaw trajectory 文件(*.trajectory.jsonl)每轮 run 产生 model.completed 事件,
  data.usage = {input, output, cacheRead, cacheWrite, reasoningTokens, totalTokens, cost{...}}
  (camelCase,CC 为 snake_case;cacheWrite 实测可为 null)
- 关键语义差异:trajectory 是 run-based —— 每轮 run 编译自己的上下文,input+cacheRead 是
  「本轮 run 的真实输入」,与上一轮 run 的值无关。run 间骤降 = 上下文重编译/新任务开始,
  ≠ compaction。因此:
  * 不适用跨 run 骤降检测(CC 的连续上下文语义);
  * context.compiled 事件暴露每轮 systemPrompt 字符数与 messages 数 —— 这是
    OpenClaw 侧更透明的上下文构成证据,予以统计;
  * 单 run 内 model.completed.usage 含 cachedTokens(部分 provider 拆分)时暂不深挖。
- 运行格式:trajectory 文件首行 traceSchema == "openclaw-trajectory"。
"""
import argparse
import json
import sys
from pathlib import Path


def _content_chars(content) -> int:
    """确定性字符计量: str 直接取长; list 取 text 部件长度,其余部件 JSON 序列化; 其他类型 JSON 序列化。"""
    if content is None:
        return 0
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        total = 0
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                total += len(part["text"])
            else:
                total += len(json.dumps(part, ensure_ascii=False))
        return total
    return len(json.dumps(content, ensure_ascii=False))


def _extract_cc_usage(obj: dict):
    """CC: assistant 行 message.usage{input_tokens,...} -> (total_in, output)"""
    if obj.get("type") != "assistant":
        return None
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return None
    u = msg.get("usage")
    if not isinstance(u, dict) or "input_tokens" not in u:
        return None
    total_in = (
        u.get("input_tokens", 0)
        + u.get("cache_read_input_tokens", 0)
        + u.get("cache_creation_input_tokens", 0)
    )
    return total_in, u.get("output_tokens", 0)


def _is_openclaw_trajectory(obj: dict, raw: str) -> bool:
    if obj.get("traceSchema") == "openclaw-trajectory":
        return True
    return '"openclaw-trajectory"' in raw[:4096] and obj.get("type") in (
        "session.started", "model.completed", "context.compiled", "prompt.submitted",
    )


def analyze_openclaw(path: Path, window: int, lines):
    """OpenClaw trajectory: run-based usage + context.compiled 统计"""
    trace = []              # (lineno, context_in, output)
    compiled = []           # (lineno, sys_chars, sys_original_chars, n_messages, images)
    last_composition = None  # 末轮(含消息的)context.compiled 构成快照
    completed = 0
    compaction_timeouts = 0
    unparsed = 0

    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            unparsed += 1
            continue
        t = obj.get("type")
        if t == "model.completed":
            completed += 1
            d = obj.get("data") or {}
            if d.get("timedOutDuringCompaction"):
                compaction_timeouts += 1
            u = d.get("usage")
            if isinstance(u, dict) and "input" in u:
                total_in = (u.get("input") or 0) + (u.get("cacheRead") or 0) + (u.get("cacheWrite") or 0)
                # 同一 usage 重复(流式分段)去重
                if trace and trace[-1][1] == total_in and trace[-1][2] == (u.get("output") or 0):
                    continue
                trace.append((lineno, total_in, u.get("output") or 0))
        elif t == "context.compiled":
            d = obj.get("data") or {}
            sp = d.get("systemPrompt")
            messages = d.get("messages") or []
            if isinstance(sp, dict):
                compiled.append((
                    lineno,
                    sp.get("truncated"), sp.get("originalChars"),
                    len(messages), d.get("imagesCount") or 0,
                ))
            elif isinstance(sp, str):
                compiled.append((lineno, False, len(sp), len(messages), d.get("imagesCount") or 0))
            # 构成快照: 只保留最后一个带消息的编译事件(最接近会话最终状态)
            if messages:
                roles = {}
                sized = []
                for m in messages:
                    if not isinstance(m, dict):
                        continue
                    role = m.get("role") or "unknown"
                    n = _content_chars(m.get("content"))
                    cell = roles.setdefault(role, {"count": 0, "chars": 0})
                    cell["count"] += 1
                    cell["chars"] += n
                    sized.append((n, role))
                sized.sort(key=lambda x: x[0], reverse=True)
                tools = d.get("tools") or []
                tools_chars = sum(len(json.dumps(t, ensure_ascii=False)) for t in tools if t is not None)
                if isinstance(sp, dict):
                    sp_trunc, sp_chars = bool(sp.get("truncated")), (sp.get("originalChars") or 0)
                elif isinstance(sp, str):
                    sp_trunc, sp_chars = False, len(sp)
                else:
                    sp_trunc, sp_chars = False, 0
                msgs_total = sum(c["chars"] for c in roles.values())
                # 工具 schema 利用率:编译进上下文的 tools 与实际调用过的工具名对比。
                # 调用证据取 toolResult 消息的 toolName 字段(有结果必有调用,比匹配
                # assistant 文本里的名字可靠);schema 字符按工具名前缀聚合,辅助判断
                # 「精简工具集」能省多少(如某类未用工具占 schema 大头)。
                tool_names = [t.get("name") for t in tools if isinstance(t, dict) and t.get("name")]
                used_names = {m.get("toolName") for m in messages if isinstance(m, dict) and m.get("role") == "toolResult" and m.get("toolName")}
                unused = [n for n in tool_names if n not in used_names]
                unused_chars = 0
                unused_by_prefix = {}
                for t in tools:
                    if isinstance(t, dict) and t.get("name") in set(unused):
                        n = len(json.dumps(t, ensure_ascii=False))
                        unused_chars += n
                        prefix = t["name"].split("_")[0] if "_" in t["name"] else t["name"]
                        cell = unused_by_prefix.setdefault(prefix, {"count": 0, "chars": 0})
                        cell["count"] += 1
                        cell["chars"] += n
                last_composition = {
                    "lineno": lineno,
                    "system_prompt_chars": sp_chars,
                    "system_prompt_truncated_in_trajectory": sp_trunc,
                    "tools_count": len(tools),
                    "tools_chars": tools_chars,
                    "tools_loaded_unused_count": len(unused),
                    "tools_loaded_unused_pct": round(len(unused) / len(tools) * 100, 1) if tools else None,
                    "tools_unused_chars": unused_chars,
                    "tools_unused_chars_pct": round(unused_chars / tools_chars * 100, 1) if tools_chars else None,
                    "tools_unused_by_prefix": dict(sorted(
                        unused_by_prefix.items(), key=lambda kv: kv[1]["chars"], reverse=True)),
                    "tools_used": sorted(used_names),
                    "messages_count": len(messages),
                    "messages_chars": msgs_total,
                    "messages_by_role": roles,
                    "grand_total_chars": sp_chars + tools_chars + msgs_total,
                    "top_messages": [{"role": r, "chars": n} for n, r in sized[:3]],
                }

    if not trace:
        return {
            "file": str(path), "format": "openclaw-trajectory", "error":
            "识别为 OpenClaw trajectory,但未找到 model.completed.usage 数据点。",
            "unparsed_lines": unparsed,
        }

    # v1.8 cacheRead 异常防护: 实测部分 provider 的 cacheRead 会跨会话累计而非
    # 本轮编译上下文(2026-11-11 本机 374 条 trajectory 实证: 254 条出现
    # input+cacheRead 高达 24M-38M 的不可能值;同期 context.compiled 消息字符
    # 折算仅 ≈19k tokens)。这类数据点保留在轨迹明细里,但剔除出统计值。
    plausible_limit = max(window * 8, 2_000_000)
    implausible = [(ln, v, o) for ln, v, o in trace if v > plausible_limit]
    plausible_trace = [(ln, v, o) for ln, v, o in trace if v <= plausible_limit]
    if plausible_trace:
        stat_trace = plausible_trace
    else:
        stat_trace = trace  # 全部异常时退回原始值,报告仍给出异常警告
    values = [v for _, v, _ in stat_trace]
    # run-based: 不做跨 run 骤降检测;改为单 run 视角的波动统计
    sys_trunc = [c for c in compiled if c[1]]
    peak = max(values)
    last_in = values[-1]
    result = {
        "file": str(path),
        "format": "openclaw-trajectory",
        "window": window,
        "semantics": "run-based",
        "data_points": len(trace),
        "implausible_points": len(implausible),
        "implausible_peak_tokens": max((v for _, v, _ in implausible), default=None),
        "model_completed_events": completed,
        "context_first_tokens": values[0],
        "context_last_tokens": last_in,
        "context_peak_tokens": peak,
        "context_mean_tokens": round(sum(values) / len(values)),
        "window_peak_pct": round(peak / window * 100, 1) if window else None,
        "window_last_pct": round(last_in / window * 100, 1) if window else None,
        "growth_last_minus_first": last_in - values[0],
        "context_compiled_events": len(compiled),
        "system_prompt_truncated_events": len(sys_trunc),
        "system_prompt_original_chars_max": max((c[2] or 0) for c in compiled) if compiled else None,
        "messages_per_run_max": max((c[3] for c in compiled), default=None),
        "images_per_run_max": max((c[4] for c in compiled), default=0) if compiled else None,
        "compaction_timeouts": compaction_timeouts,
        "unparsed_lines": unparsed,
    }
    if last_composition:
        result["composition"] = last_composition
    return result


def analyze_cc(path: Path, window: int, lines):
    trace = []
    usage_lines = 0
    assistant_lines = 0
    unparsed = 0

    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            unparsed += 1
            continue
        if obj.get("type") == "assistant":
            assistant_lines += 1
        u = _extract_cc_usage(obj)
        if u is None:
            continue
        usage_lines += 1
        if trace and trace[-1][1] == u[0] and trace[-1][2] == u[1]:
            continue
        trace.append((lineno, u[0], u[1]))

    if not trace:
        return {
            "file": str(path), "format": "unknown",
            "error": "未找到任何 message.usage 数据点。该文件可能不是 Claude Code 会话记录,"
                     "也不是 OpenClaw trajectory,请改用 analyze_session.py 走估算路线。",
            "assistant_lines": assistant_lines, "unparsed_lines": unparsed,
        }

    values = [v for _, v, _ in trace]
    peak = max(values)
    drops = []
    for k in range(1, len(trace)):
        prev_v, cur_v = trace[k - 1][1], trace[k][1]
        if prev_v > 0 and cur_v < prev_v * 0.8:
            drops.append({
                "line": trace[k][0], "from_tokens": prev_v, "to_tokens": cur_v,
                "drop_pct": round((prev_v - cur_v) / prev_v * 100, 1),
            })
    last_in = values[-1]
    return {
        "file": str(path), "format": "claude-code-usage", "window": window,
        "semantics": "continuous",
        "data_points": len(trace), "assistant_lines": assistant_lines,
        "usage_coverage_pct": round(len(trace) / assistant_lines * 100, 1) if assistant_lines else None,
        "context_first_tokens": values[0], "context_last_tokens": last_in,
        "context_peak_tokens": peak,
        "context_mean_tokens": round(sum(values) / len(values)),
        "window_peak_pct": round(peak / window * 100, 1) if window else None,
        "window_last_pct": round(last_in / window * 100, 1) if window else None,
        "compaction_drops": drops,
        "growth_last_minus_first": last_in - values[0],
        "unparsed_lines": unparsed,
    }


def analyze(path: Path, window: int):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # 严格检测:前 30 行中存在 traceSchema 字段形式的 trajectory 行。
    # 只匹配『traceSchema 键在行首附近且值 openclaw-trajectory』,防止 CC 会话
    # 在前 30 行回显该字符串(如 cat trajectory 文件)被误路由。
    is_oc = False
    for line in lines[:30]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("{\"traceSchema\"") and "openclaw-trajectory" in s[:120]:
            is_oc = True
            break
        if s.startswith("{") and "\"traceSchema\"" in s[:60] and "openclaw-trajectory" in s[:160]:
            is_oc = True
            break
    if is_oc:
        return analyze_openclaw(path, window, lines)
    return analyze_cc(path, window, lines)


def to_markdown(r: dict) -> str:
    if r.get("format") == "unknown":
        lines = ["# usage 轨迹分析(失败)", "",
                 f"- 文件:`{r['file']}`",
                 f"- {r['error']}",
                 f"- assistant 行数:{r.get('assistant_lines', 0)};未解析行:{r.get('unparsed_lines', 0)}"]
        return "\n".join(lines)

    if r.get("format") == "openclaw-trajectory":
        if r.get("error"):
            lines = ["# OpenClaw trajectory usage 轨迹分析(失败)", "",
                     f"- 文件:`{r['file']}`", f"- {r['error']}"]
            return "\n".join(lines)
        lines = ["# OpenClaw trajectory usage 轨迹分析(真实计量,run-based)", "",
                 f"- 文件:`{r['file']}`",
                 f"- 数据点:{r['data_points']}(model.completed 事件 {r['model_completed_events']} 个)",
                 f"- 单轮 run 上下文输入:首 {r['context_first_tokens']:,} → 末 {r['context_last_tokens']:,} tokens;"
                 f"峰值 {r['context_peak_tokens']:,}(窗口占用 {r['window_peak_pct']}%),均值 ≈{r['context_mean_tokens']:,}",
                 f"- context.compiled 事件:{r['context_compiled_events']} 个"
                 f"(systemPrompt 截断 {r['system_prompt_truncated_events']} 次,"
                 f"原始最长 {r['system_prompt_original_chars_max'] or 0:,} 字符;"
                 f"单轮最多 {r['messages_per_run_max']} 条消息 / {r['images_per_run_max']} 张图片)"]
        if r.get("implausible_points"):
            lines.append(
                f"- ⚠️ cacheRead 异常防护:{r['implausible_points']} 个数据点的 input+cacheRead "
                f"超过合理上限(窗口×8 且 ≥2M),疑似 provider 跨会话累计缓存而非本轮上下文,"
                f"已从统计中剔除(异常峰值 {r['implausible_peak_tokens']:,} tokens);"
                f"同一 run 的 context.compiled 字符折算是更可靠的规模证据")
        if r.get("compaction_timeouts"):
            lines.append(f"- ⚠️ 检测到 {r['compaction_timeouts']} 次 compaction 超时(timedOutDuringCompaction)")
        comp = r.get("composition")
        if comp:
            gt = comp["grand_total_chars"] or 1

            def pct(n):
                return round(n / gt * 100, 1)

            sp_note = "(轨迹存储截断,按 originalChars 计)" if comp["system_prompt_truncated_in_trajectory"] else ""
            lines.append(
                f"- 单轮上下文构成(第 {comp['lineno']} 行编译事件,字符口径): "
                f"系统提示 {comp['system_prompt_chars']:,} 字符({pct(comp['system_prompt_chars'])}%){sp_note} · "
                f"工具 schema {comp['tools_count']} 个 {comp['tools_chars']:,} 字符({pct(comp['tools_chars'])}%) · "
                f"对话消息 {comp['messages_count']} 条 {comp['messages_chars']:,} 字符({pct(comp['messages_chars'])}%)"
            )
            tops = " / ".join(f"{m['role']} {m['chars']:,}" for m in comp.get("top_messages", []))
            if tops:
                lines.append(f"  - 占字符最多的消息: {tops}(定位后可判断该轮被什么内容吃掉)")
            role_line = " · ".join(
                f"{role} {c['count']}条/{c['chars']:,}字符" for role, c in comp.get("messages_by_role", {}).items()
            )
            if role_line:
                lines.append(f"  - 按角色: {role_line}")
            if comp.get("tools_count"):
                used_str = ", ".join(comp.get("tools_used") or []) or "无"
                lines.append(
                    f"  - 工具 schema 利用率: 编译进上下文 {comp['tools_count']} 个工具,"
                    f"实际调用 {len(comp.get('tools_used') or [])} 个({used_str});"
                    f"{comp.get('tools_loaded_unused_count')} 个加载未用"
                    f"({comp.get('tools_loaded_unused_pct')}%),占 schema 字符 {comp.get('tools_unused_chars_pct')}%"
                )
                top_prefix = list((comp.get("tools_unused_by_prefix") or {}).items())[:3]
                if top_prefix:
                    detail = " / ".join(f"{p} {c['count']}个 {c['chars']:,}字符" for p, c in top_prefix)
                    lines.append(f"    未用 schema 集中在: {detail}(工具输出占比高 → 先清理大输出;加载未用占比高 → 先精简工具集)")
            lines.append("  - 注意: 构成为字符计量而非 token;若 trajectory 存储截断了超大字段,实际值只会更大。")
        lines += ["",
                  "**run-based 语义提醒**:OpenClaw trajectory 按轮(run)记录,每轮编译自己的上下文,"
                  "轮间数值下降是「上下文重编译/新任务」,不是 CC 那样的 compaction 骤降;"
                  "本脚本不做跨 run 骤降检测,也不应把轮间下降解读为压缩。"
                  "约束丢失审计请配合 audit_constraints.py(对 OpenClaw 会话自动降级为位置分析)。",
                  "",
                  "> 数据来自 model.completed.data.usage 官方计量字段(input + cacheRead + cacheWrite),"
                  "为真实值而非估算;重复 usage 已按变化点去重。"]
        return "\n".join(lines)

    # claude-code-usage
    lines = ["# Claude Code usage 轨迹分析(真实计量)", "",
             f"- 文件:`{r['file']}`",
             f"- 数据点:{r['data_points']}(assistant {r['assistant_lines']} 行,覆盖率 {r['usage_coverage_pct']}%)",
             f"- 上下文输入:首 {r['context_first_tokens']:,} → 末 {r['context_last_tokens']:,} tokens(增长 {r['growth_last_minus_first']:+,})",
             f"- 峰值 {r['context_peak_tokens']:,}(窗口占用 {r['window_peak_pct']}%),均值 ≈{r['context_mean_tokens']:,}"]
    if r["compaction_drops"]:
        lines += ["", "**疑似 Compaction 骤降点**(较前值下降 ≥20%):"]
        for d in r["compaction_drops"]:
            lines.append(f"- 第 {d['line']} 行:{d['from_tokens']:,} → {d['to_tokens']:,} tokens(降 {d['drop_pct']}%)")
    else:
        lines += ["", "未检测到上下文骤降点;若会话确实经历过压缩,该文件可能不含压缩边界,请结合 SKILL.md 人工核对。"]
    lines += ["",
              "> 数据来自 message.usage 官方计量字段(input + cache_read + cache_creation),为真实值而非估算;"
              "重复 usage 已按变化点去重。七类内容归组请配合 analyze_session.py 使用。"]
    return "\n".join(lines)


def build_fleet_summary(results: list) -> dict:
    """v1.8: 车队级聚合(中位数/极值),异常值防护后的统计才进入聚合。"""
    def stat(key):
        vals = sorted(r[key] for r in results if r.get(key) is not None)
        if not vals:
            return None
        return {
            "median": vals[len(vals) // 2],
            "min": vals[0],
            "max": vals[-1],
            "n": len(vals),
        }

    def comp_stat(key):
        vals = sorted(
            c[key]
            for r in results
            if (c := r.get("composition")) and c.get(key) is not None
        )
        if not vals:
            return None
        return {
            "median": vals[len(vals) // 2],
            "min": vals[0],
            "max": vals[-1],
            "n": len(vals),
        }

    return {
        "files_analyzed": len(results),
        "window_peak_pct": stat("window_peak_pct"),
        "context_last_tokens": stat("context_last_tokens"),
        "implausible_points_total": sum(r.get("implausible_points") or 0 for r in results),
        "tools_loaded_unused_pct": comp_stat("tools_loaded_unused_pct"),
        "tools_unused_chars_pct": comp_stat("tools_unused_chars_pct"),
        "messages_chars": comp_stat("messages_chars"),
        "system_prompt_chars": comp_stat("system_prompt_chars"),
        "tools_chars": comp_stat("tools_chars"),
    }


def fleet_lines(fleet: dict) -> list:
    """把 fleet 汇总对象转成可读行。"""
    def fmt(s):
        if not s:
            return "无数据"
        return f"中位 {s['median']:,} / 最小 {s['min']:,} / 最大 {s['max']:,}(n={s['n']})"

    lines = [
        f"# Fleet 汇总({fleet['files_analyzed']} 个文件)",
        "",
        f"- 分析文件数:{fleet['files_analyzed']}",
        f"- 窗口占用峰值%:{fmt(fleet['window_peak_pct'])}",
        f"- 末轮输入 tokens:{fmt(fleet['context_last_tokens'])}",
    ]
    if fleet["implausible_points_total"]:
        lines.append(
            f"- ⚠️ 剔除 cacheRead 异常数据点共 {fleet['implausible_points_total']} 个"
            "(已排除在统计外,详见各文件报告)")
    lines += [
        f"- 末轮构成·系统提示字符:{fmt(fleet['system_prompt_chars'])}",
        f"- 末轮构成·工具 schema 字符:{fmt(fleet['tools_chars'])}",
        f"- 末轮构成·对话消息字符:{fmt(fleet['messages_chars'])}",
        f"- 工具加载未用占比:{fmt(fleet['tools_loaded_unused_pct'])}",
        f"- 未用 schema 字符占比:{fmt(fleet['tools_unused_chars_pct'])}",
    ]
    return lines


def main():
    ap = argparse.ArgumentParser(description="会话 usage 真实上下文轨迹分析(Claude Code / OpenClaw trajectory)")
    ap.add_argument("file", nargs="+", help="会话 JSONL(CC: ~/.claude/projects/<proj>/<id>.jsonl;OpenClaw: *.trajectory.jsonl);v1.8 起支持多文件 fleet 汇总")
    ap.add_argument("--window", type=int, default=200000, help="上下文窗口大小(默认 200000)")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    args = ap.parse_args()
    window = max(args.window, 1)
    paths = [Path(f) for f in args.file]
    missing = [p for p in paths if not p.exists()]
    if missing:
        for p in missing:
            print(f"错误:文件不存在:{p}", file=sys.stderr)
        sys.exit(1)
    if len(paths) == 1:
        result = analyze(paths[0], window)
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else to_markdown(result))
        return
    # v1.8 fleet 批量模式: 逐文件分析 + 车队级汇总(单文件损坏不拖垮整体)
    results = []
    skipped = []
    for p in paths:
        try:
            r = analyze(p, window)
        except Exception as exc:
            skipped.append({"file": str(p), "error": f"analyze failed: {exc}"})
            continue
        if r.get("error"):
            skipped.append({"file": str(p), "error": r["error"]})
            continue
        results.append(r)
    if not results:
        print("所有文件都无法解析出 usage 数据点。", file=sys.stderr)
        sys.exit(1)
    fleet = build_fleet_summary(results)
    if args.json:
        print(json.dumps({"results": results, "skipped": skipped, "fleet": fleet},
                         ensure_ascii=False, indent=2))
        return
    for r in results:
        print(to_markdown(r))
        print()
    if skipped:
        print(f"## 跳过 {len(skipped)} 个文件(无 usage 数据点或解析失败)\n")
        for s in skipped:
            print(f"- `{s['file']}`: {s['error']}")
        print()
    print("\n".join(fleet_lines(fleet)))


if __name__ == "__main__":
    main()
