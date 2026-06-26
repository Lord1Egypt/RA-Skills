#!/usr/bin/env python3
"""
龙虾 API 代理日志查看器 🦞
日志路径: /Users/xm_plus/.openclaw/workspace/company/api-logs/YYYY-MM-DD.jsonl

用法:
  python3 log_viewer.py              # 查看今日摘要列表
  python3 log_viewer.py --last 5     # 最后 5 条
  python3 log_viewer.py --id 3       # 第 3 条详情
  python3 log_viewer.py --stats      # 今日统计
  python3 log_viewer.py --search 飞书 # 搜索关键词
  python3 log_viewer.py --errors     # 只看失败请求
  python3 log_viewer.py --date 2026-03-09  # 指定日期
  python3 log_viewer.py --full       # 不截断文本
  python3 log_viewer.py --feishu     # 同时生成飞书文档
  python3 log_viewer.py --id 3 --feishu   # 查看详情并生成飞书文档

设计说明：
  --feishu 为显式可选标志，而非默认行为。原因：
  1. 飞书文档创建需要网络请求，有额外延迟；
  2. 用户快速查看终端时不需要额外的文档开销；
  3. 明确意图，避免频繁创建大量同类文档。
"""

import json
import argparse
import subprocess
import tempfile
import os
from datetime import datetime
from pathlib import Path

# ─── 配置 ────────────────────────────────────────────────────
LOG_DIR      = Path("/Users/xm_plus/.openclaw/workspace/company/api-logs")
FEISHU_WRITE = Path("/Users/xm_plus/.openclaw/workspace/company/feishu_write.py")

# ─── ANSI 颜色 ───────────────────────────────────────────────
R      = "\033[0m"
GRAY   = "\033[90m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
WHITE  = "\033[97m"
BLUE   = "\033[94m"

SEP = GRAY + "─" * 62 + R


# ═══════════════════════════ 工具函数 ════════════════════════

def cut(text, n=80):
    t = str(text).replace("\n", " ").strip()
    return t if len(t) <= n else t[:n] + "…"

def status_color(code):
    return (GREEN if code == 200 else RED) + str(code) + R

def fmt_ms(ms):
    return f"{ms/1000:.1f}s" if ms >= 1000 else f"{ms:.0f}ms"

def extract_text(content):
    if not content:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if not isinstance(item, dict):
                parts.append(str(item))
                continue
            t = item.get("type", "")
            if t == "text":
                parts.append(item.get("text", ""))
            elif t == "tool_use":
                parts.append(f"[tool_call: {item.get('name','?')}]")
            elif t == "tool_result":
                inner = extract_text(item.get("content", ""))
                parts.append(f"[tool_result: {inner[:60]}]")
        return "\n".join(parts)
    return str(content)

def last_user_text(msgs):
    for m in reversed(msgs):
        if m.get("role") == "user":
            return extract_text(m.get("content", ""))
    return ""

def asst_reply(entry):
    for key in ("response_body_parsed", "response_body"):
        rb = entry.get(key)
        if isinstance(rb, dict):
            c = rb.get("content", [])
            if c:
                return extract_text(c)
    return ""

def usage(entry):
    for key in ("response_body_parsed", "response_body"):
        rb = entry.get(key)
        if isinstance(rb, dict):
            u = rb.get("usage")
            if u:
                return {"in": u.get("input_tokens", 0), "out": u.get("output_tokens", 0)}
    return {"in": 0, "out": 0}

def model_short(entry):
    rb = entry.get("request_body")
    if isinstance(rb, dict):
        m = rb.get("model", "")
        return m.split("/")[-1] if m else "?"
    return "?"

def model_full(entry):
    rb = entry.get("request_body")
    return rb.get("model", "?") if isinstance(rb, dict) else "?"

def messages(entry):
    rb = entry.get("request_body")
    return rb.get("messages", []) if isinstance(rb, dict) else []

def system_prompt(entry):
    rb = entry.get("request_body")
    return rb.get("system", "") if isinstance(rb, dict) else ""

def parse_ts(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.now()

def is_api(entry):
    rb = entry.get("request_body")
    return isinstance(rb, dict) and "messages" in rb


# ═══════════════════════ 日志加载 & 过滤 ═════════════════════

def load(date_str):
    f = LOG_DIR / f"{date_str}.jsonl"
    if not f.exists():
        print(f"{RED}日志文件不存在: {f}{R}")
        return []
    entries = []
    with open(f, encoding="utf-8") as fp:
        for i, line in enumerate(fp, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"{GRAY}[第{i}行解析失败: {e}]{R}")
    return entries

def filter_api(entries, args):
    res = [e for e in entries if is_api(e)]
    if args.errors:
        res = [e for e in res if e.get("response_status", 0) != 200]
    if args.search:
        kw = args.search.lower()
        matched = []
        for e in res:
            msgs = messages(e)
            all_text = " ".join(extract_text(m.get("content", "")) for m in msgs)
            if (kw in all_text.lower()
                    or kw in asst_reply(e).lower()
                    or kw in system_prompt(e).lower()):
                matched.append(e)
        res = matched
    if args.last:
        res = res[-args.last:]
    return res


# ═══════════════════════ 飞书文档生成 ════════════════════════

def call_feishu_write(title, md_content, timeout=120):
    """调用 feishu_write.py 创建飞书文档，返回链接或 None，最多重试3次"""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False,
        prefix="/tmp/lobster_log_", encoding="utf-8"
    )
    tmp.write(md_content)
    tmp.close()

    link = None
    for attempt in range(1, 4):
        try:
            result = subprocess.run(
                ["python3", str(FEISHU_WRITE), title, tmp.name],
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0:
                link = result.stdout.strip()
                break
            else:
                print(f"{RED}飞书文档创建失败（第{attempt}次）: {result.stderr[:200]}{R}")
        except subprocess.TimeoutExpired:
            print(f"{RED}飞书写入超时（第{attempt}次/{timeout}s），正在重试...{R}")
        except Exception as ex:
            print(f"{RED}飞书写入异常（第{attempt}次）: {ex}{R}")

    try:
        os.unlink(tmp.name)
    except Exception:
        pass
    return link


# 单次飞书文档写入建议不超过此行数（约 300 条调用），超出则截断摘要
FEISHU_MAX_ENTRIES = 300


def build_stats_section(api_entries):
    """生成统计区块（Markdown 字符串，不含标题）"""
    total   = len(api_entries)
    errors  = sum(1 for e in api_entries if e.get("response_status", 0) != 200)
    tot_in  = sum(usage(e)["in"]  for e in api_entries)
    tot_out = sum(usage(e)["out"] for e in api_entries)
    durs    = [e["duration_ms"] for e in api_entries if "duration_ms" in e]
    avg_ms  = sum(durs) / len(durs) if durs else 0
    max_ms  = max(durs) if durs else 0
    model_cnt = {}
    for e in api_entries:
        m = model_short(e)
        model_cnt[m] = model_cnt.get(m, 0) + 1
    model_str = " / ".join(
        f"{m}（{cnt}次）"
        for m, cnt in sorted(model_cnt.items(), key=lambda x: -x[1])
    )
    lines = []
    lines.append(f"- 总调用：{total}次 | 成功：{total - errors} | 失败：{errors}")
    lines.append(f"- Input tokens：{tot_in:,} | Output tokens：{tot_out:,} | 合计：{tot_in + tot_out:,}")
    lines.append(f"- 平均响应：{fmt_ms(avg_ms)} | 最慢：{fmt_ms(max_ms)}")
    lines.append(f"- 模型：{model_str or '—'}")
    return "\n".join(lines)


def build_list_md(api_entries, date_str):
    """生成日志列表页的 Markdown（飞书文档正文）
    超过 FEISHU_MAX_ENTRIES 条时，只写统计 + 前 FEISHU_MAX_ENTRIES 条明细并注明截断。
    """
    truncated = len(api_entries) > FEISHU_MAX_ENTRIES
    show_entries = api_entries[:FEISHU_MAX_ENTRIES] if truncated else api_entries

    lines = []
    lines.append("## 📊 统计")
    lines.append(build_stats_section(api_entries))
    lines.append("")

    if truncated:
        lines.append(f"> ⚠️ 本日共 {len(api_entries)} 条调用，文档仅展示前 {FEISHU_MAX_ENTRIES} 条明细。")
        lines.append("")

    lines.append("## 📋 调用列表")

    for i, e in enumerate(show_entries, 1):
        ts  = parse_ts(e.get("timestamp", ""))
        st  = e.get("response_status", 0)
        dur = e.get("duration_ms", 0)
        u   = usage(e)
        ms  = messages(e)

        lines.append(f"### #{i} [{ts.strftime('%H:%M:%S')}] {st} | {fmt_ms(dur)} | {model_short(e)}")
        lines.append(f"- **Tokens**: in:{u['in']} out:{u['out']}")

        lu = last_user_text(ms)
        if lu:
            lines.append(f"- **User**: {cut(lu, 100)}")

        rep = asst_reply(e)
        if rep:
            lines.append(f"- **Asst**: {cut(rep, 100)}")

        lines.append("")

    return "\n".join(lines)


def build_detail_md(entry, idx, date_str):
    """生成单条详情的 Markdown（飞书文档正文）"""
    ts   = parse_ts(entry.get("timestamp", ""))
    st   = entry.get("response_status", 0)
    dur  = entry.get("duration_ms", 0)
    u    = usage(entry)
    msgs = messages(entry)
    sys_ = system_prompt(entry)
    rep  = asst_reply(entry)

    st_str = f"{st} OK" if st == 200 else f"{st} Error"

    lines = []
    lines.append("## 基本信息")
    lines.append(f"- 时间：{ts.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 状态：{st_str}")
    lines.append(f"- 耗时：{fmt_ms(dur)}")
    lines.append(f"- 模型：{model_full(entry)}")
    lines.append(f"- Tokens：input {u['in']:,} / output {u['out']:,}")
    lines.append(f"- 流式：{'是' if entry.get('streaming') else '否'}")
    lines.append("")

    if sys_:
        lines.append("## System Prompt")
        lines.append("")
        for para in sys_.split("\n"):
            lines.append(para)
        lines.append("")

    if msgs:
        lines.append("## 对话记录")
        lines.append("")
        for m in msgs:
            role = m.get("role", "?")
            txt  = extract_text(m.get("content", ""))
            if role == "user":
                lines.append("### User")
            elif role == "assistant":
                lines.append("### Assistant")
            else:
                lines.append(f"### {role}")
            lines.append("")
            for para in txt.split("\n"):
                lines.append(para)
            lines.append("")

    # 如果 msgs 里没有 assistant 角色，单独展示最终回复
    if rep and not any(m.get("role") == "assistant" for m in msgs):
        lines.append("## Assistant 最终回复")
        lines.append("")
        for para in rep.split("\n"):
            lines.append(para)
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════ 输出模式 ════════════════════════

def show_list(entries, full=False, feishu=False, date_str=None):
    """摘要列表模式"""
    if not entries:
        print(f"\n{GRAY}  没有找到匹配的日志条目{R}\n")
        return
    print()
    for i, e in enumerate(entries, 1):
        ts  = parse_ts(e.get("timestamp", ""))
        st  = e.get("response_status", 0)
        dur = e.get("duration_ms", 0)
        u   = usage(e)
        ms  = messages(e)

        print(
            f"{GRAY}[{ts.strftime('%H:%M:%S')}]{R} "
            f"{BOLD}#{i:<3}{R}"
            f"{status_color(st)} | "
            f"{GRAY}{fmt_ms(dur):<7}{R}| "
            f"{CYAN}{model_short(e)}{R} | "
            f"{YELLOW}in:{u['in']} out:{u['out']} tokens{R}"
        )

        sum_len = 999999 if full else 50
        lu = last_user_text(ms)
        if lu:
            print(f"  {GRAY}User摘要:{R} {cut(lu, sum_len)}")

        rep = asst_reply(e)
        if rep:
            print(f"  {GRAY}Asst摘要:{R} {cut(rep, sum_len)}")
        print(SEP)
    print()
    if feishu and date_str:
        print(f"{CYAN}正在生成飞书文档...{R}")
        md = build_list_md(entries, date_str)
        title = f"API调用日志 {date_str}"
        link = call_feishu_write(title, md)
        if link: print(f"{GREEN}飞书文档已创建: {link}{R}")
        else:    print(f"{RED}飞书文档创建失败{R}")


def show_detail(entries, id_str, full=False, feishu=False):
    entry = None
    idx   = None
    if id_str.isdigit():
        idx = int(id_str) - 1
        if 0 <= idx < len(entries): entry = entries[idx]
        else:
            print(f"{RED}序号 {id_str} 超出范围 共 {len(entries)} 条{R}"); return
    else:
        for i, e in enumerate(entries):
            if e.get("request_id", "").startswith(id_str):
                entry = e; idx = i; break
        if entry is None:
            print(f"{RED}找不到 request_id: {id_str}{R}"); return

    lim  = 999999 if full else 500
    ts   = parse_ts(entry.get("timestamp", ""))
    st   = entry.get("response_status", 0)
    dur  = entry.get("duration_ms", 0)
    u    = usage(entry)
    msgs = messages(entry)
    sys_ = system_prompt(entry)
    rep  = asst_reply(entry)

    print()
    print(BOLD + "=" * 64 + R)
    print(f"  {BOLD}Time :{R}  {GRAY}{ts.strftime('%Y-%m-%d %H:%M:%S')}{R}")
    print(f"  {BOLD}ID   :{R}  {GRAY}{entry.get('request_id','?')}{R}")
    print(f"  {BOLD}Status:{R} {status_color(st)}")
    print(f"  {BOLD}Dur  :{R}  {GRAY}{fmt_ms(dur)}{R}")
    print(f"  {BOLD}Model:{R}  {CYAN}{model_full(entry)}{R}")
    print(f"  {BOLD}Stream:{R} {GRAY}{'yes' if entry.get('streaming') else 'no'}{R}")
    print(f"  {BOLD}Path :{R}  {GRAY}{entry.get('path','?')}{R}")
    print(BOLD + "=" * 64 + R)

    if sys_:
        print(f"\n{BOLD}{BLUE}System Prompt{R}")
        print(GRAY + "-" * 40 + R)
        print(sys_ if full else cut(sys_, lim))

    if msgs:
        print(f"\n{BOLD}{BLUE}Messages ({len(msgs)}){R}")
        print(GRAY + "-" * 40 + R)
        for m in msgs:
            role = m.get("role", "?")
            txt  = extract_text(m.get("content", ""))
            if role == "user":        label = f"{WHITE}{BOLD}  [User]{R}"
            elif role == "assistant": label = f"{CYAN}{BOLD}  [Asst]{R}"
            else:                     label = f"{GRAY}{BOLD}  [{role}]{R}"
            print(f"\n{label}")
            print(txt if full else cut(txt, lim))

    if rep:
        print(f"\n{BOLD}{BLUE}Assistant Reply{R}")
        print(GRAY + "-" * 40 + R)
        print(rep if full else cut(rep, lim))

    print(f"\n{BOLD}{BLUE}Token Usage{R}")
    print(GRAY + "-" * 40 + R)
    print(f"  {YELLOW}Input: {R} {u['in']:,}")
    print(f"  {YELLOW}Output:{R} {u['out']:,}")
    print(f"  {YELLOW}Total: {R} {u['in'] + u['out']:,}")
    print()
    print(BOLD + "=" * 64 + R)
    print()

    if feishu:
        print(f"{CYAN}正在生成飞书详情文档...{R}")
        real_idx = (idx + 1) if idx is not None else 0
        date_str = ts.strftime("%Y-%m-%d")
        time_str = ts.strftime("%H:%M")
        md = build_detail_md(entry, real_idx, date_str)
        title = f"API调用详情 #{real_idx} {date_str} {time_str}"
        link = call_feishu_write(title, md)
        if link: print(f"{GREEN}飞书文档已创建: {link}{R}")
        else:    print(f"{RED}飞书文档创建失败{R}")


def show_stats(all_entries, date_str, feishu=False):
    api    = [e for e in all_entries if is_api(e)]
    total  = len(api)
    errors = sum(1 for e in api if e.get("response_status", 0) != 200)
    tot_in  = sum(usage(e)["in"]  for e in api)
    tot_out = sum(usage(e)["out"] for e in api)
    durs   = [e["duration_ms"] for e in api if "duration_ms" in e]
    avg_ms = sum(durs) / len(durs) if durs else 0
    max_ms = max(durs) if durs else 0
    model_cnt = {}
    for e in api:
        m = model_short(e)
        model_cnt[m] = model_cnt.get(m, 0) + 1
    print()
    print(BOLD + "=" * 52 + R)
    print(f"  {BOLD}API Stats -- {date_str}{R}")
    print(BOLD + "=" * 52 + R)
    print(f"  {BOLD}Total calls  :{R} {WHITE}{total}{R}")
    print(f"  {BOLD}Success (200):{R} {GREEN}{total - errors}{R}")
    print(f"  {BOLD}Failed       :{R} {(RED if errors else GREEN)}{errors}{R}")
    print(f"  {BOLD}Input tokens :{R} {YELLOW}{tot_in:,}{R}")
    print(f"  {BOLD}Output tokens:{R} {YELLOW}{tot_out:,}{R}")
    print(f"  {BOLD}Total tokens :{R} {YELLOW}{tot_in + tot_out:,}{R}")
    print(f"  {BOLD}Avg response :{R} {GRAY}{fmt_ms(avg_ms)}{R}")
    print(f"  {BOLD}Slowest      :{R} {GRAY}{fmt_ms(max_ms)}{R}")
    if model_cnt:
        print(f"\n  {BOLD}Models:{R}")
        for model, cnt in sorted(model_cnt.items(), key=lambda x: -x[1]):
            print(f"    {CYAN}{model}{R}: {cnt}")
    print(BOLD + "=" * 52 + R)
    print()

    if feishu:
        print(f"{CYAN}正在生成统计飞书文档...{R}")
        md = f"## 📊 统计\n\n{build_stats_section(api)}\n"
        title = f"API统计 {date_str}"
        link = call_feishu_write(title, md)
        if link: print(f"{GREEN}飞书文档已创建: {link}{R}")
        else:    print(f"{RED}飞书文档创建失败{R}")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(description="Lobster API Log Viewer")
    parser.add_argument("--date",   default=today)
    parser.add_argument("--last",   type=int)
    parser.add_argument("--id")
    parser.add_argument("--errors", action="store_true")
    parser.add_argument("--search")
    parser.add_argument("--stats",  action="store_true")
    parser.add_argument("--full",   action="store_true")
    parser.add_argument("--feishu", action="store_true",
                        help="generate Feishu doc")
    args = parser.parse_args()

    all_entries = load(args.date)
    if not all_entries and not args.stats:
        return

    if args.stats:
        show_stats(all_entries, args.date, feishu=args.feishu)
        return

    api_entries = filter_api(all_entries, args)

    if args.id:
        show_detail(api_entries, args.id, full=args.full, feishu=args.feishu)
        return

    show_list(api_entries, full=args.full, feishu=args.feishu, date_str=args.date)


if __name__ == "__main__":
    main()
