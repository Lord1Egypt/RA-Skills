#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对 all_tasks.jsonl 中的任务做多维度分类，输出分类结果与统计报告（环境无关版）。

分类规则从 config/project_rules.json 读取；无配置时用通用规则。
运行：python classify_tasks.py
输出：$OUTPUT_DIR/tasks_classified.jsonl + task_analysis_report.md
"""
import os, sys, json, re, collections
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import out_dir, month_of, load_jsonl, installed_agents, norm_agent

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = out_dir()
IN = os.path.join(OUT_DIR, "all_tasks.jsonl")
OUT_JSON = os.path.join(OUT_DIR, "tasks_classified.jsonl")
OUT_MD = os.path.join(OUT_DIR, "task_analysis_report.md")
def _config_path():
    env = os.environ.get("WORKLOG_CONFIG", "")
    if env and os.path.isfile(env):
        return env
    for p in ("config/local/project_rules.local.json", "config/project_rules.json"):
        fp = os.path.join(BASE, *p.split("/"))
        if os.path.isfile(fp):
            return fp
    return os.path.join(BASE, "config", "project_rules.json")


CONFIG = _config_path()

# ---------- 通用兜底规则（同事无配置文件时也能用）----------
DEFAULT_PROJECT_RULES = [
    ("AI工具/方法论", [r"\bskill\b", r"\bagent\b", r"\bmcp\b", r"copilot", r"cursor", r"claude", r"codex", r"\bdsh\b", r"openai"]),
    ("前端/UI", [r"前端", r"vue", r"react", r"页面", r"界面", r"原型", r"html", r"css"]),
    ("后端/服务", [r"后端", r"接口", r"\bapi\b", r"spring", r"java", r"微服务", r"feign"]),
    ("数据/数据库", [r"数据库", r"mysql", r"redis", r"postgres", r"\bsql\b"]),
    ("运维/部署", [r"部署", r"安装", r"升级", r"docker", r"k8s", r"镜像", r"linux", r"wsl"]),
    ("文档/报告", [r"文档", r"报告", r"方案", r"周报", r"readme"]),
]

DEFAULT_TYPE_RULES = [
    ("代码审查/Review", [r"\breview\b", r"审查", r"code.?review", r"代码检查", r"审核"]),
    ("Bug修复/问题定位", [r"\bbug\b", r"修复", r"定位", r"排查", r"解决.*问题", r"报错", r"异常", r"错误"]),
    ("性能优化/容量", [r"性能", r"容量", r"并发", r"压测", r"优化", r"慢查询"]),
    ("开发实现/编码", [r"实现", r"开发", r"编写", r"写一个", r"新增", r"改造", r"重构"]),
    ("测试验证", [r"测试", r"验证", r"回归", r"验收", r"用例"]),
    ("部署/环境/运维", [r"部署", r"安装", r"升级", r"环境", r"配置", r"docker", r"wsl", r"服务器"]),
    ("文档/规范/报告", [r"文档", r"报告", r"方案", r"周报", r"汇报", r"总结", r"规范", r"readme"]),
    ("AI工具使用/提示词", [r"提示词", r"\bprompt\b", r"\bskill\b", r"\bagent\b", r"模型", r"\bai\b", r"llm"]),
    ("咨询/问答/调研", [r"咨询", r"怎么", r"如何", r"为什么", r"是什么", r"调研", r"了解", r"解释", r"看下", r"查下", r"学习"]),
    ("前端/UI", [r"前端", r"vue", r"页面", r"菜单", r"界面", r"原型", r"html", r"css"]),
    ("Agent评估/测试任务", [r"transcript start", r"assessing", r"you are implementing task", r"task \d+ of the", r"verify todo"]),
    ("版本控制/提交", [r"\bgit\b", r"提交", r"commit", r"分支", r"worktree"]),
]

DEFAULT_SKILL_TAGS = [
    ("AI编程助手", [r"claude", r"codex", r"copilot", r"cursor", r"qoder", r"trae", r"\bdsh\b"]),
    ("Skill/技能体系", [r"\bskill\b", r"技能", r"skills"]),
    ("多智能体/Subagent", [r"subagent", r"子代理", r"多智能体", r"agent.?team"]),
    ("MCP/工具链", [r"\bmcp\b", r"codegraph", r"lsp", r"工具链"]),
    ("自动化/定时任务", [r"automation", r"自动化", r"定时", r"cron"]),
    ("提示词工程", [r"提示词", r"\bprompt\b", r"system.?prompt"]),
    ("文档生成", [r"生成.*文档", r"写.*报告", r"\bdocx\b"]),
]


def normalize_rules(raw, fallback):
    """把配置里的规则转成 (name, patterns) 数组；兼容对象与数组两种写法。"""
    if not raw:
        return fallback
    out = []
    for item in raw:
        if isinstance(item, dict) and "name" in item and "patterns" in item:
            out.append((item["name"], item["patterns"]))
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            out.append((item[0], item[1]))
    return out or fallback


def load_config():
    if os.path.isfile(CONFIG):
        try:
            d = json.load(open(CONFIG, encoding="utf-8"))
            return (normalize_rules(d.get("projects"), DEFAULT_PROJECT_RULES),
                    normalize_rules(d.get("work_types"), DEFAULT_TYPE_RULES),
                    normalize_rules(d.get("skill_tags"), DEFAULT_SKILL_TAGS))
        except Exception as e:
            print(f"配置读取失败，使用默认规则: {e}")
    return DEFAULT_PROJECT_RULES, DEFAULT_TYPE_RULES, DEFAULT_SKILL_TAGS


PROJECT_RULES, TYPE_RULES, SKILL_TAGS = load_config()


def classify(text, rules, multi=False):
    t = str(text or "").lower()
    hits = [name for name, pats in rules if any(re.search(p, t) for p in pats)]
    if multi:
        return hits
    return hits[0] if hits else "其他"


def project_from_cwd(cwd):
    """从工作目录末级目录名推断项目（通用兜底）。"""
    cwd = str(cwd or "").replace("\\", "/").rstrip("/")
    if not cwd:
        return ""
    leaf = os.path.basename(cwd)
    skip = {"home", "root", "workspace", "projects", "sessions", "src", "app", "test"}
    return leaf if leaf and leaf.lower() not in skip else ""


def main():
    rows = load_jsonl(IN)
    if not rows:
        print(f"无输入数据: {IN}")
        return
    out = []
    for r in rows:
        text = ((r.get("title") or "") + " " + (r.get("prompt") or "")).strip()
        cwd = r.get("cwd", "")
        rec = dict(r)
        rec["text"] = text[:500]
        rec["month"] = month_of(r.get("timestamp", ""))
        # 项目分类：文本优先 → cwd 路径 → cwd 末级目录名推断
        proj = classify(text, PROJECT_RULES)
        if proj == "其他" and cwd:
            proj = classify(cwd, PROJECT_RULES)
            if proj == "其他":
                leaf = project_from_cwd(cwd)
                if leaf:
                    proj = f"[路径推断] {leaf}"
        if not text.strip():
            proj = "未分类(无任务描述)"
        rec["project"] = proj
        rec["work_type"] = classify(text, TYPE_RULES)
        rec["ai_tags"] = classify(text, SKILL_TAGS, multi=True)
        out.append(rec)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total = len(out)
    lines = ["# AI Agent 会话任务分类报告", "",
             f"> 分析会话数：**{total}** 条 ｜ 数据源：`all_tasks.jsonl` ｜ 配置：`config/project_rules.json`", ""]

    def table(title, counter, top=None):
        s = [f"## {title}", "", "| 类别 | 数量 | 占比 |", "|---|---:|---:|"]
        items = counter.most_common(top) if top else counter.most_common()
        for k, v in items:
            s.append(f"| {k} | {v} | {v/total*100:.1f}% |")
        return s

    # ---- 核心发现（动态计算，无硬编码项目名）----
    valid = [r for r in out if r["project"] != "未分类(无任务描述)" and r.get("title")]
    no_desc = sum(1 for r in out if r["project"] == "未分类(无任务描述)")
    eval_cnt = sum(1 for r in out if r["work_type"] == "Agent评估/测试任务")
    top_proj = collections.Counter(r["project"] for r in out if r["project"] != "未分类(无任务描述)").most_common(3)
    top_type = collections.Counter(r["work_type"] for r in out).most_common(4)
    months = collections.Counter(r["month"] for r in out if r["month"] != "未知")
    peak_month, peak_cnt = months.most_common(1)[0] if months else ("未知", 0)
    quality = sum(1 for r in out if r["work_type"] in
                  ("代码审查/Review", "Bug修复/问题定位", "性能优化/容量", "测试验证"))
    lines += ["## 核心发现", "",
              f"1. **有效任务描述**：{len(valid)} / {total} 条会话有明确任务描述，{no_desc} 条无描述。",
              f"2. **高频项目（TOP3）**：" + ("、".join(f"{k}（{v}）" for k, v in top_proj) if top_proj else "无"),
              f"3. **工作类型集中在**：" + ("、".join(f"{k}（{v}）" for k, v in top_type) if top_type else "无"),
              f"4. **质量治理类**（审查+修复+性能+测试）{quality} 条，纯开发实现 {sum(1 for r in out if r['work_type']=='开发实现/编码')} 条。",
              f"5. **使用高峰**在 {peak_month}（{peak_cnt} 条）。{eval_cnt} 条为 Agent 自评估任务，不代表人工工作量，汇报时应剔除。", ""]

    # ---- 本机在用 Agent：只列实际产出过任务或 token 的，未安装/未使用不进报告 ----
    installed = installed_agents(OUT_DIR)
    token_rows_early = load_jsonl(os.path.join(OUT_DIR, "token_usage.jsonl"))
    token_by_agent = collections.Counter(norm_agent(r.get("agent")) for r in token_rows_early)
    task_by_agent = collections.Counter(norm_agent(r.get("agent")) for r in out)

    # 提取方式：从适配器清单判定（专用 / 兜底）
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from adapters.base import discover as _discover
        all_adapters = _discover()
        # 用「模块名」排除 generic/heuristic，避免继承 DeclarativeAdapter 的专用适配器误判
        l1_names = {norm_agent(a.name) for a in all_adapters
                    if type(a).__module__ not in ("adapters.generic", "adapters.heuristic")}
        l2_names = set()
        try:
            from adapters.generic import load_rules as _load_rules
            l2_names = {norm_agent(r.get("name")) for r in _load_rules()}
        except Exception:
            pass
        notes_by_agent = {}
        for a in all_adapters:
            n = a.note()
            if n:
                notes_by_agent[norm_agent(a.name)] = str(n)
    except Exception:
        l1_names, l2_names, notes_by_agent = set(), set(), {}

    if installed:
        lines += ["", f"## 本机在用 Agent（{len(installed)} 个）", "",
                  "> 仅统计本机实际产出过会话数据的 Agent；未安装或未产生数据的 Agent 不列入报告。", "",
                  "| Agent | 任务数 | Token 会话数 | 提取方式 | Token 状态 |",
                  "|---|---:|---:|---|---|"]
        for a in sorted(installed, key=lambda x: -(task_by_agent.get(x, 0) + token_by_agent.get(x, 0))):
            mode = "专用适配器" if a in l1_names or a in l2_names else "通用兜底/其他"
            tk = token_by_agent.get(a, 0)
            if tk:
                tstate = "✅ 已统计"
            elif a in notes_by_agent:
                tstate = "⚠️ " + notes_by_agent[a][:40]
            else:
                tstate = "⚠️ 无 token 数据"
            lines.append(f"| {a} | {task_by_agent.get(a,0):,} | {tk:,} | {mode} | {tstate} |")
        lines.append("")

    agents = collections.Counter(r["agent"] for r in out)
    lines += [""] + table("一、按 Agent 分布", agents)
    lines += [""] + table("二、按项目归属", collections.Counter(r["project"] for r in out))
    lines += [""] + table("三、按工作类型", collections.Counter(r["work_type"] for r in out))
    tagc = collections.Counter(t for r in out for t in r["ai_tags"])
    lines += [""] + table("四、按 AI 技能标签（多标签）", tagc)
    lines += [""] + table("五、按月份", collections.Counter(r["month"] for r in out))

    # 各项目代表任务
    lines += ["", "## 六、各项目代表性任务（每类取前 8 条）", ""]
    for proj, _ in collections.Counter(r["project"] for r in out).most_common():
        lines += [f"### {proj}", ""]
        rs = [r for r in out if r["project"] == proj and r["title"]]
        for r in rs[:8]:
            lines.append(f"- `{r['agent']}` {r['month']} {r['title'][:80]}")
        lines.append("")

    # Agent × 项目交叉表（动态列）
    cross = collections.Counter((r["agent"], r["project"]) for r in out
                                if r["project"] not in ("未分类(无任务描述)", "其他"))
    agents_order = list(agents.keys())
    if cross:
        projs = sorted(set(p for a, p in cross),
                       key=lambda p: -sum(v for (a, pp), v in cross.items() if pp == p))
        lines += ["", "## 七、Agent × 项目交叉分布（AI 落地全景）", "",
                  "| 项目 | " + " | ".join(agents_order) + " | 合计 |",
                  "|---|" + "---:|" * (len(agents_order) + 1)]
        for p in projs[:25]:
            vals = [cross.get((a, p), 0) for a in agents_order]
            lines.append(f"| {p} | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} |")

    # Token 章节（若已运行 stat_tokens.py）
    token_path = os.path.join(OUT_DIR, "token_usage.jsonl")
    if os.path.isfile(token_path):
        trows = [r for r in load_jsonl(token_path) if norm_agent(r.get("agent")) in installed]
        if trows:
            t_all = sum(r.get("total_tokens", 0) for r in trows)
            t_fresh = sum(r.get("fresh_tokens", r.get("total_tokens", 0)) for r in trows)
            L = ["", "## 八、Token 消耗统计", "",
                 f"> 共 {len(trows)} 个会话含 token 数据，合计处理 **{t_all:,}** token，非缓存口径 **{t_fresh:,}** token。",
                 "", "| Agent | 会话数 | 合计 token | 非缓存 token |", "|---|---:|---:|---:|"]
            for a in sorted(set(r["agent"] for r in trows)):
                rs = [r for r in trows if r["agent"] == a]
                L.append(f"| {a} | {len(rs):,} | {sum(r.get('total_tokens',0) for r in rs):,} | "
                         f"{sum(r.get('fresh_tokens',r.get('total_tokens',0)) for r in rs):,} |")
            L += ["", "> 注：缓存命中 token 属上下文复用、不等于真实消耗；详细口径见 `token_report.md`。"]
            lines += L

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"classified {total} -> {OUT_JSON}")
    print(f"report -> {OUT_MD}")
    print("项目分布:", collections.Counter(r["project"] for r in out).most_common(6))
    print("工作类型:", collections.Counter(r["work_type"] for r in out).most_common(6))


if __name__ == "__main__":
    main()
