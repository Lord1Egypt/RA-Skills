#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计本机各 AI Agent 会话的 token 消耗（适配器架构）。

采集逻辑全部下放到 scripts/adapters/；本脚本只负责汇总、分类与报告。
新增 Agent token 统计只需在适配器里实现 collect_tokens()。

配置：
  - 项目分类规则：WORKLOG_CONFIG 环境变量 或 config/local/project_rules.local.json
    或 config/project_rules.json；均无则用内置规则。

输出：$OUTPUT_DIR/token_usage.jsonl + token_report.md
"""
import os, sys, json, collections, datetime, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import out_dir, month_of, installed_agents, norm_agent
from adapters.base import discover, load_noise_markers

OUT_DIR = out_dir()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _config_path():
    env = os.environ.get("WORKLOG_CONFIG", "")
    if env and os.path.isfile(env):
        return env
    for p in ("config/local/project_rules.local.json", "config/project_rules.json"):
        fp = os.path.join(ROOT, *p.split("/"))
        if os.path.isfile(fp):
            return fp
    return ""


CONFIG = _config_path()
BUILTIN_RULES = [
    ("AI工具/方法论", [r"\bskill\b", r"\bagent\b", r"\bmcp\b", r"copilot", r"cursor", r"claude", r"codex", r"\bdsh\b"]),
    ("前端/UI", [r"前端", r"vue", r"页面", r"原型", r"html", r"css"]),
    ("后端/服务", [r"后端", r"接口", r"api", r"spring", r"java", r"微服务"]),
    ("数据/数据库", [r"数据库", r"mysql", r"redis", r"postgres", r"sql"]),
    ("运维/部署", [r"部署", r"docker", r"k8s", r"镜像", r"linux", r"wsl"]),
    ("文档/报告", [r"文档", r"报告", r"方案", r"readme"]),
]


def load_rules():
    if CONFIG:
        try:
            d = json.load(open(CONFIG, encoding="utf-8"))
            raw = d.get("projects") or []
            out = []
            for item in raw:
                if isinstance(item, dict) and "name" in item and "patterns" in item:
                    out.append((item["name"], item["patterns"]))
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    out.append((item[0], item[1]))
            return out or BUILTIN_RULES
        except Exception:
            pass
    return BUILTIN_RULES


PROJECT_RULES = load_rules()

# 各 Agent 的 token 采集口径说明（仅在报告里实际出现该 Agent 时输出）。
# key 为 norm_agent() 归一后的名称；未在下方登记的 Agent 只显示通用说明。
AGENT_TOKEN_NOTES = {
    "claudecode": "`message.usage`，按 `message.id` 去重（同一消息重复写入）。",
    "codex": "`token_count` 事件累计值取最后一条；cached 已含在 input 内，非缓存 = (input − cached) + output。",
    "workbuddy": "`session_usage.used`（上下文窗口占用量），会话级快照、非逐轮精确累计。",
    "dsh": "zstd 流式解压后 `assistant/chunk` 的 usage 逐条累加（需 zstandard）。",
    "qoder": "字段存在则取，字段全 0 时不伪造 token。",
    "opencode": "字段存在则取，字段全 0 时不伪造 token。",
}


def project_of(cwd, title=""):
    text = (str(cwd or "") + " " + str(title or "")).lower()
    for name, pats in PROJECT_RULES:
        if any(re.search(p, text) for p in pats):
            return name
    cwd = str(cwd or "").replace("\\", "/").rstrip("/")
    if cwd:
        leaf = os.path.basename(cwd)
        if leaf and leaf not in ("home", "root", "workspace", "projects", "sessions"):
            return f"[路径] {leaf}"
    return "其他"


def agg(rows, key):
    d = collections.defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    for r in rows:
        x = d[r.get(key, "未知")]
        x[0] += 1
        x[1] += r.get("input_tokens", 0)
        x[2] += r.get("output_tokens", 0)
        x[3] += r.get("cache_tokens", 0)
        x[4] += r.get("reasoning_tokens", 0)
        x[5] += r.get("total_tokens", 0)
    return d


def fmt(n):
    if n >= 1e8:
        return f"{n/1e8:.2f}亿"
    if n >= 1e4:
        return f"{n/1e4:.1f}万"
    return f"{n:,}"


def report(rows, adapter_notes=None):
    total_all = sum(r["total_tokens"] for r in rows)
    total_fresh = sum(r.get("fresh_tokens", r["total_tokens"]) for r in rows)
    L = ["# Token 消耗统计报告", "",
         f"> 统计时间：{datetime.datetime.now():%Y-%m-%d %H:%M}　|　会话数：**{len(rows)}**　|　合计 token：**{fmt(total_all)}**（其中非缓存 token 约 **{fmt(total_fresh)}**）",
         "",
         "> ⚠️ **口径提示**：缓存命中 token 是上下文复用、不等于真实消耗。汇报「用量」建议用 **非缓存 token** 口径，更经得起追问。",
         ""]
    if adapter_notes:
        L += ["## 未纳入统计的 Agent", "",
              "> 以下 Agent 已识别但当前环境无 token 数据或缺少 zstd 依赖，**未计入**统计，不代表未使用：", ""]
        for agent, note in adapter_notes:
            L.append(f"- **{agent}**：{note}")
        L.append("")
    for title, key in [("一、按 Agent", "agent"), ("二、按项目", "project"), ("三、按月份", "month")]:
        if key == "project":
            for r in rows:
                r["project"] = project_of(r.get("cwd", ""), r.get("title", ""))
        if key == "month":
            for r in rows:
                r["month"] = month_of(r.get("timestamp"))
        d = agg(rows, key)
        freshd = collections.defaultdict(int)
        for r in rows:
            freshd[r.get(key, "未知")] += r.get("fresh_tokens", r["total_tokens"])
        L += [f"## {title}", "",
              "| 类别 | 会话数 | 输入 | 输出 | 缓存命中 | 合计 token | 非缓存 token |",
              "|---|---:|---:|---:|---:|---:|---:|"]
        for k, v in sorted(d.items(), key=lambda x: -x[1][5]):
            L.append(f"| {k} | {v[0]:,} | {fmt(v[1])} | {fmt(v[2])} | {fmt(v[3])} | {fmt(v[5])} | **{fmt(freshd[k])}** |")
        L.append("")
    md = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if r.get("model"):
            md[r["model"]][0] += 1
            md[r["model"]][1] += r["total_tokens"]
    L += ["## 四、按模型（有模型名的会话）", "", "| 模型 | 会话数 | 合计 token |", "|---|---:|---:|"]
    for k, v in sorted(md.items(), key=lambda x: -x[1][1])[:20]:
        L.append(f"| {k} | {v[0]:,} | {fmt(v[1])} |")
    L += ["", "## 五、Token 消耗 Top 15 会话", "", "| Agent | 项目 | 时间 | 合计 token | 任务标题 |", "|---|---|---|---:|---|"]
    for r in sorted(rows, key=lambda x: -x["total_tokens"])[:15]:
        t = (r.get("title") or "(无标题)").replace("|", "／")[:60]
        L.append(f"| {r['agent']} | {r.get('project', '-')} | {str(r.get('timestamp', ''))[:10]} | {fmt(r['total_tokens'])} | {t} |")
    L += ["", "## 六、口径说明", "",
          "- 各 Agent 的 token 采集口径由对应适配器实现，详见 `scripts/adapters/*.py`。"]
    # 只列本机实际产生数据的 Agent 口径，未安装的不出现
    used = sorted({norm_agent(r.get("agent")) for r in rows})
    for a in used:
        note = AGENT_TOKEN_NOTES.get(a.lower())
        if note:
            L.append(f"- **{a}**：{note}")
    L += ["- token ≠ 费用；不同模型单价差异大，费用需按厂商定价另行换算。", ""]
    return "\n".join(L)


def main():
    adapters = discover()
    rows = []
    notes = []
    for a in adapters:
        try:
            got = a.collect_tokens() or []
        except Exception as e:
            print(f"{a.name} FAILED: {str(e)[:120]}")
            got = []
        n = sum(r.get("total_tokens", 0) for r in got)
        print(f"{a.name}: {len(got)} 会话, {fmt(n)} tokens")
        rows += got
        note = a.note()
        if note and not got:
            notes.append((a.name, note))
    # 「未纳入统计」只列本机实际在用的 Agent：未安装/未产生数据的不提。
    # installed 取任务侧快照 + 本轮 token 采集结果（token_usage.jsonl 此刻尚未刷新）。
    installed = installed_agents(OUT_DIR) | {norm_agent(r.get("agent")) for r in rows}
    notes = [(a, n) for a, n in notes if norm_agent(a) in installed]

    with open(os.path.join(OUT_DIR, "token_usage.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT_DIR, "token_report.md"), "w", encoding="utf-8") as f:
        f.write(report(rows, notes))
    print(f"总计: {len(rows)} 会话, {fmt(sum(r['total_tokens'] for r in rows))} tokens")


if __name__ == "__main__":
    main()
