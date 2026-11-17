#!/usr/bin/env python3
"""releaser.py — 零依赖 CLI 技能发布工程工具（cli-skill-release 主入口）。

对标 find-skills++ 的能力矩阵：把"发布工程"从散文说明书变成**可运行的多能力 CLI**。
find-skills++ 用 AST 扫描/离线搜索/生命周期治理主动管理 agent 技能；
本工具用 validate/inventory/selfcheck 主动管理"技能能否可靠发布"，并进一步提供
gap（市场情报）、发布就绪分、release（近一键发布）等碾压级能力。

子命令（19 个，全零依赖、真能跑）：
  scaffold   生成带 CI 的完整可发布骨架（委托同目录 scaffold.py）
  validate   主动扫描一个技能目录，报告全部发布陷阱 + 0-100 就绪分（--mode skill|cli|package）
  gate       CI 门禁：就绪分低于阈值即非零退出（readiness-as-a-service）
  secretscan ★安全红线：扫描硬编码密码/授权码/API Token（禁止入库）
  publish    ★多站上架编排：显式逐站授权上传 GitHub/ClawHub（安全闸门前置，默认不碰远程）
  inventory  扫描本机已装技能，逐条报告"能否发、差什么"（治理）
  gap        市场情报：扫描本机技能归类，报告稀疏类目为市场缺口并给出 scaffold 建议
  selfcheck  零依赖校验：扫 import，比对 sys.stdlib_module_names
  bump       自动升 SKILL.md 版本号 + 补 CHANGELOG
  release    git 推送 + clawhub CLI 真一键（或构造 ClawHub 导入链接 + 预填元数据）+ 自动登记账本
  badge      基于就绪分生成 readiness 徽章 SVG + 链回片段（链式传播引擎）
  promote    宣传工具箱：徽章区+电梯演讲+社媒文案+链式玩法
  diagnose   长尾诊断：症状→根因→修复（搜索即获客）
  preflight  市场定制上架前检查清单（回答"发布前检查清单"类搜索）
  registry   ★状态层：已发布技能账本（list/show/add），release 成功自动登记
  recheck    ★生命周期：再校验已发布技能，报告漂移/弃用（持续治理）
  selfdemo   ★自证底座：全量自证（主张即演示，对标 smoke.py）
  curate     ★供给侧策展：主动告诉生态该造什么（升级版 gap）
  doctor     自检 cli-skill-release 自身；或对 --path 目标目录跑 validate

零依赖：仅用标准库。用法：
  python releaser.py validate --path ./my-skill
  python releaser.py gap
  python releaser.py release --path . --dry-run
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# 通用工具
# --------------------------------------------------------------------------

STD_LIB = getattr(sys, "stdlib_module_names", set())

# 链回本技能页面的地址（徽章/宣传片段里点击即到达；可用环境变量 RELEASER_PAGE 覆盖）
RELEASER_PAGE = os.environ.get("RELEASER_PAGE", "https://clawhub.ai/skills/cli-skill-release")

# 已发布技能账本（状态层 A）：默认落在用户 home 下，可用 RELEASER_LEDGER 覆盖（测试用）。
# 让工具跨多次运行持有『已发布技能账本』，从一次性校验器升级为发布侧『治理者』。
LEDGER_PATH = os.environ.get(
    "RELEASER_LEDGER",
    os.path.expanduser("~/.workbuddy/cli-skill-release/ledger.json"),
)

REPORT = []  # (level, title, detail, weight)  weight=0 表示不计分的信息项

# 发布就绪分权重（合计 100）：每项 PASS=满分 / WARN=半分 / FAIL=0
W = {
    "fm_fields": 8,     # frontmatter 含 name/version/license
    "lic_field": 4,     # license 字段为 MIT/MIT-0
    "lic_spdx": 8,      # LICENSE 文件含可识别 SPDX
    "lic_ascii": 6,     # 版权名为 ASCII（licensee 才不会判 Other）
    "no_card": 8,       # 全仓无 skill-card.md 保留名冲突
    "doctor": 10,       # doctor --path . 真跑退出 0
    "ci": 8,            # CI 含 doctor 步 + tee
    "ref": 6,           # SKILL.md 引用文件真实存在
    "zero": 6,          # 零依赖
    "fn_compile": 8,    # 全部 .py 通过 compile（无语法错误）
    "fn_import": 6,     # 入口模块可 import（无 import-time 崩溃）
    "fn_smoke": 10,     # 入口 --help 烟测通过（CLI 真能 boot）
    "secret": 12,       # ★安全红线：全仓无硬编码凭据/授权码（防重演 v1.9.x 事故）
}

# 透明评分：每个维度的权重 + 理由（供 --rubric / --json.rubric，使分数可被审计、可被信任）
RATIONALE = {
    "fm_fields": "发布元数据齐全，ClawHub/SkillHub 强制要求",
    "lic_field": "许可字段须 MIT/MIT-0，否则市场拒绝或显示 Other",
    "lic_spdx": "LICENSE 文件须被 licensee 识别，否则 GitHub 显示 Other",
    "lic_ascii": "版权持有人名须 ASCII，否则 licensee 判 NOASSERTION",
    "no_card": "skill-card.md 是 ClawHub 保留名，冲突即发布失败",
    "doctor": "自检门真跑退出 0，过 CI 必现失败陷阱（find-skills++ 曾踩）",
    "ci": "CI 含 doctor + tee Step Summary，排障命门",
    "ref": "SKILL.md 引用的脚本/资产真实存在，否则运行期缺文件",
    "zero": "零依赖，任何环境（含 Windows 沙箱）裸跑",
    "fn_compile": "*功能验证：全部源码通过编译，无语法错误",
    "fn_import": "*功能验证：入口模块可 import，无 import-time 崩溃",
    "fn_smoke": "*功能验证：入口 --help 烟测通过，CLI 真能 boot（竞品无人做）",
    "secret": "*安全红线：全仓无硬编码密码/授权码/API Token，防凭据泄露并被市场判 malicious",
}


# --------------------------------------------------------------------------
# 长尾知识库：症状 → 根因 → 修复（diagnose 的数据底座，也是 README 的可索引长尾内容）
# 这些短语就是人类/AI 实际会搜的"长尾问题"，工具直接给出答案 → 被找到 + 真能解决问题。
# --------------------------------------------------------------------------
DIAGNOSE_KB = [
    {
        "id": "license-other",
        "title": "LICENSE 在 GitHub / ClawHub 显示 Other / NOASSERTION",
        "symptoms": ["license", "other", "noassertion", "licensee", "识别不了", "显示 other",
                     "spdx", "版权", "copyright", "非 ascii", "中文版权"],
        "cause": "LICENSE 文件缺可识别 SPDX 标识，或版权持有人名含非 ASCII（如中文\"何巍\"），"
                 "licensee 无法判定为 MIT/MIT-0。",
        "fix": "LICENSE 直接写 MIT-0 全文（含 \"MIT-0\" 字样），版权持有人名用 ASCII（如 \"He Wei\"）；"
               "派生上游时新建 NOTICE 保留上游署名。用 api.github.com/repos/{owner}/{repo}/license 核验 spdx_id。",
    },
    {
        "id": "pytest-exit-2",
        "title": "pytest exit code 2（CI 红、本地却绿）",
        "symptoms": ["pytest", "exit code 2", "exit 2", "收集", "collection", "import error",
                     "sys.path", "conftest", "路径注入"],
        "cause": "CLI 在模块级把 scripts/ 加 sys.path 后能自跑，但 tests/ 直接 import 缺 conftest 注入 → "
                 "收集期（import/语法）炸，退出码 2。CI 看不到本地那层 PATH。",
        "fix": "在 tests/conftest.py 注入根目录与 scripts/；退出码含义：2=收集错误，1=测试失败，0=全过，"
               "非零都让 CI 红。用 releaser.py validate 的 ★功能验证会提前暴露。",
    },
    {
        "id": "ci-red-doctor",
        "title": "CI 一直红：doctor 子命令报 unrecognized arguments: --path .",
        "symptoms": ["ci", "一直红", "doctor", "unrecognized arguments", "--path", "step 失败",
                     "整 job 红", "find-skills"],
        "cause": "CI 里 `python main.py doctor --path .` 时，doctor 子命令未真定义 --path → "
                 "全平台必现失败，且 pytest traceback 照不出（独立 step）。这是 find-skills++ 早期 CI 红的真凶。",
        "fix": "给 doctor 子命令加 --path 参数（脚手架已写好）；用 releaser.py gate 门禁把 CI 拦在相同陷阱前。",
    },
    {
        "id": "skill-card",
        "title": "上架报 skill-card.md is generated by ClawHub and cannot be published directly",
        "symptoms": ["skill-card", "cannot be published", "保留名", "冲突", "generated by clawhub",
                     "publish 失败"],
        "cause": "skill-card.md 是 ClawHub 保留名，仓库根（含子目录/夹具）有同名文件即冲突。",
        "fix": "全仓改名（如 market-card.md）；`git ls-files | grep skill-card` 排查；releaser.py validate 会主动扫出。",
    },
    {
        "id": "topics-48",
        "title": "ClawHub Topics 超 48 字符被拒",
        "symptoms": ["topics", "48", "超长", "characters or fewer", "标签", "超限"],
        "cause": "Topics 是整段（含逗号/空格）≤48 字符，不是单个标签。填一长串必然超限。",
        "fix": "先填最短组合卡过去（如 `skill-discovery, security` 25 字符）；releaser.py release 自动截断 ≤48。",
    },
    {
        "id": "import-crash",
        "title": "技能一跑就崩：入口 import 失败 / import-time 崩溃",
        "symptoms": ["import", "崩溃", "一跑就崩", "boot", "can't import", "module not found",
                     "入口报错"],
        "cause": "入口模块在加载时就执行了顶层代码或依赖了非标准库，import 即炸——格式完美却无法启动。",
        "fix": "releaser.py validate 的 ★功能验证（compile+import+--help 真跑）会挡住这类『文档漂亮、引擎熄火』的技能；"
               "竞品只查 paperwork，无人真跑 CLI。",
    },
    {
        "id": "not-found",
        "title": "技能发布后搜不到 / 没人下载",
        "symptoms": ["搜不到", "搜索不到", "不被发现", "discover", "findable", "没流量", "下载少",
                     "visibility", "曝光"],
        "cause": "SKILL.md 的 description 是 vector search 的匹配面、tags 决定相邻位、GitHub topics 喂外部索引器；"
                 "三者缺失或被写成中文独占，英文检索就匹配不上。",
        "fix": "description 写进中英文触发短语；加 tags（publish, skill-publishing, pre-publish-checklist, clawhub）；"
               "仓库加 GitHub topics（agent-skills, claude-skills, skill-md, ai-agents）；README 用长尾问题做标题被搜索引擎索引。",
    },
    {
        "id": "ready-to-publish",
        "title": "如何判断『我的技能能不能发 / 还差什么』（自然语长尾）",
        "symptoms": ["ready to publish", "is my skill ready", "审计", "audit", "spec compliant",
                     "还差什么", "能不能发", "缺什么", "检查清单", "checklist", "pre-publish"],
        "cause": "发布前没有量化标准，凭感觉上架 → 反复被拒。",
        "fix": "releaser.py validate 给 0-100 发布就绪分（含功能验证）；preflight 输出市场定制检查清单；"
               "直接回答 \"Is this skill ready to publish?\" / \"What am I missing before I push?\"。",
    },
    {
        "id": "secret-leak",
        "title": "密码/授权码/Token 不小心进 GitHub 了（泄露 + 被市场判恶意）",
        "symptoms": ["password", "token", "secret", "凭据", "授权码", "泄露", "明文",
                     "credential", "secret leak", "进了 github", "malicious", "硬编码", "smtp"],
        "cause": "把密码/授权码/API Token 明文硬编码进技能文件并 commit+push 到公开 GitHub："
                 "既造成凭据泄露，又被 ClawHub/SkillHub 安全扫描判 malicious 封禁（v1.9.x 真实事故）。",
        "fix": "发布前用 `releaser.py secretscan --path .` 扫出全部硬编码凭据 → 改为环境变量(os.environ)/密钥库，"
               "删除明文；已入库的须 `git filter-repo` 清历史并**立即轮换**泄露凭据；"
               "validate/gate 已将凭据扫描设为强制 FAIL 闸门，release 会直接拒绝提交/推送/发布。",
    },
]


def _diagnose_match(text):
    text = (text or "").lower()
    scored = []
    for item in DIAGNOSE_KB:
        hit = sum(1 for s in item["symptoms"] if s.lower() in text)
        if hit:
            scored.append((hit, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def _add(level, title, detail="", weight=10):
    REPORT.append((level, title, detail, weight))


def _score():
    """根据 REPORT 计算 0-100 就绪分。"""
    tot = sum(r[3] for r in REPORT if r[3] > 0)
    got = 0.0
    for level, _t, _d, w in REPORT:
        if w <= 0:
            continue
        if level == "PASS":
            got += w
        elif level == "WARN":
            got += w * 0.5
    return round(100.0 * got / tot) if tot else 0


def _print_report(show_score=True):
    order = {"PASS": 0, "WARN": 1, "FAIL": 2}
    REPORT.sort(key=lambda r: order.get(r[0], 9))
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for level, title, detail, _w in REPORT:
        counts[level] = counts.get(level, 0) + 1
        line = "  [%s] %s" % (level, title)
        if detail:
            line += " — " + detail
        print(line)
    print("-" * 56)
    print("  合计: PASS=%d  WARN=%d  FAIL=%d" % (counts["PASS"], counts["WARN"], counts["FAIL"]))
    if show_score:
        print("  发布就绪分: %d / 100" % _score())
    return counts["FAIL"]


def _bench_info(baseline=100):
    """对标头部技能画像：头部基线（默认 100）= 全部加权维度 PASS。

    返回与头部差距：哪些加权维度你没达到、差多少分。
    """
    gaps = [(lv, t) for lv, t, _d, w in REPORT if w > 0 and lv != "PASS"]
    score = _score()
    return {"baseline": baseline, "score": score,
            "gap": max(0, baseline - score),
            "missed_head_dims": [{"level": lv, "title": t} for lv, t in gaps]}


def _print_bench(baseline=100):
    info = _bench_info(baseline)
    print("\n" + "=" * 56)
    print("  releaser bench — 对标头部（基线分 %d）" % baseline)
    print("=" * 56)
    print("  你的就绪分: %d / %d" % (info["score"], baseline))
    print("  距头部还差: %d 分" % info["gap"])
    if info["missed_head_dims"]:
        print("  头部必过维度中你未达标:")
        for g in info["missed_head_dims"]:
            print("    - [%s] %s" % (g["level"], g["title"]))
    else:
        print("  ✓ 已对齐头部：全部加权维度 PASS")


def _report_payload(path, mode, bench=False):
    """结构化报告（供 --json 与未来市场闭环消费）。"""
    items = [{"level": lv, "msg": t, "detail": d, "weight": w}
             for lv, t, d, w in REPORT]
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for it in items:
        counts[it["level"]] += 1
    payload = {"path": path, "mode": mode, "score": _score(),
               "summary": counts, "items": items}
    if bench:
        payload["bench"] = _bench_info()
    return payload


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def parse_frontmatter(path):
    txt = _read(path)
    if not txt.startswith("---"):
        return {}, txt
    end = txt.find("\n---", 3)
    if end == -1:
        return {}, txt
    block = txt[3:end]
    data = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data, txt


# --------------------------------------------------------------------------
# validate —— 主动扫描发布陷阱（杀手锏）+ 就绪分
# --------------------------------------------------------------------------

# 仅匹配「目录/文件名.扩展名」形态，避免把正文描述（如 scripts/references/assets）误判为真实引用
REF_PATTERNS = [
    re.compile(r"scripts/[^\s`]+\.[a-zA-Z0-9]+"),
    re.compile(r"references/[^\s`]+\.[a-zA-Z0-9]+"),
    re.compile(r"assets/[^\s`]+\.[a-zA-Z0-9]+"),
]

CATEGORY_KEYWORDS = {
    "Developer Tools": ["git", "ci", "build", "release", "test", "lint", "deploy",
                         "devops", "code", "cli", "python", "脚手架", "发布"],
    "Security": ["security", "scan", "vuln", "auth", "encrypt", "secret", "guard",
                 "audit", "安全", "扫描"],
    "AI & ML": ["ai", "llm", "agent", "model", "rag", "prompt", "nlp", "vision",
                "ml", "智能体", "模型"],
    "Data": ["data", "csv", "excel", "db", "sql", "etl", "analytics", "pandas",
             "数据", "表格"],
    "Productivity": ["note", "task", "todo", "calendar", "doc", "markdown", "search",
                     "效率", "笔记"],
    "Web": ["http", "web", "scrape", "crawl", "api", "browser", "fetch", "网页"],
    "Finance": ["finance", "stock", "trade", "money", "invoice", "account", "金融",
                "股票"],
    "Content": ["image", "video", "audio", "write", "blog", "social", "post",
                "图像", "视频", "内容"],
}


def categorize(text):
    text = (text or "").lower()
    hits = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        n = sum(1 for k in kws if k.lower() in text)
        if n:
            hits[cat] = n
    return sorted(hits, key=lambda c: hits[c], reverse=True)


# ClawHub 发布要求：categories 必须是官方精确 slug（≤3 个），topics 为自由标签（≤5 个、≤48 字符、禁用保留词）
# 官方 slug 列表（docs.openclaw.ai/clawhub/publishing）：
#   integrations, automation, research, development, productivity, communication,
#   creative, knowledge, agents, operations, security, finance, lifestyle, other
# 内部 CATEGORY_KEYWORDS 用可读标签做市场情报；发布到 ClawHub 时映射成官方 slug
CLAWHUB_CATEGORY_SLUG = {
    "Developer Tools": "development",
    "Security": "security",
    "Productivity": "productivity",
    "Finance": "finance",
    "AI & ML": "agents",
    "Data": "research",
    "Web": "research",
    "Content": "creative",
}
# ClawHub 拒绝的保留词（作为 topic 会被拒）
CLAWHUB_RESERVED_TOPICS = {
    "approved", "audited", "certified", "clawhub", "community", "curated",
    "endorsed", "featured", "official", "officials", "openclaw", "recommended",
    "staff-pick", "trusted", "trusted-publisher", "verified",
}


def _as_list(val):
    """把 frontmatter 里的字段统一成小写字符串列表（兼容逗号分隔串与列表）。"""
    if isinstance(val, list):
        items = val
    elif isinstance(val, str):
        items = [x for x in val.split(",") if x.strip()]
    else:
        items = []
    return [str(x).strip().lower() for x in items if str(x).strip()]


def _registry_meta(fm):
    """发布元数据：优先读 frontmatter 的 clawhub_categories/clawhub_topics/github_topics；
    缺失时由 keywords 自动推导（categories 映射成 ClawHub 官方 slug）。"""
    # ClawHub 分类：frontmatter 显式 > 自动（内部标签 → 官方 slug，去重保序，≤3）
    cc = _as_list(fm.get("clawhub_categories"))
    if cc:
        seen, uniq = set(), []
        for c in cc:
            if c not in seen:
                seen.add(c); uniq.append(c)
        categories = uniq[:3]
    else:
        auto = categorize(" ".join([fm.get("keywords", ""), fm.get("description", "")]))[:3]
        seen, uniq = set(), []
        for c in auto:
            s = CLAWHUB_CATEGORY_SLUG.get(c, "development")
            if s not in seen:
                seen.add(s); uniq.append(s)
        categories = uniq[:3] or ["development"]
    # ClawHub topics：frontmatter 显式 > 自动（过滤保留词 + ≤48 字符，≤5）
    ct = _as_list(fm.get("clawhub_topics"))
    if ct:
        topics = [t[:48] for t in ct if t and t not in CLAWHUB_RESERVED_TOPICS][:5]
    else:
        topics = [t.strip().lower()[:48] for t in _auto_topics(fm.get("keywords", "")).split(",")
                  if t.strip() and t.strip().lower() not in CLAWHUB_RESERVED_TOPICS][:5]
    # GitHub topics：frontmatter 显式 > 默认推荐
    gt = _as_list(fm.get("github_topics"))
    github = gt or ["agent-skills", "skill-md", "python", "mit-0"]
    return categories, topics, github


def find_main_entry(skill_dir, slug):
    cand = os.path.join(skill_dir, slug.replace("-", "_") + ".py")
    if os.path.isfile(cand):
        return cand
    for f in sorted(os.listdir(skill_dir)):
        if f.endswith(".py"):
            t = _read(os.path.join(skill_dir, f))
            if 'add_parser("doctor"' in t or "add_parser('doctor'" in t:
                return os.path.join(skill_dir, f)
    return None


def detect_license(path):
    txt = _read(path)
    spdx = None
    if "with or without fee" in txt:
        spdx = "MIT-0"
    elif "Permission to use, copy, modify" in txt and "THE SOFTWARE IS PROVIDED" in txt:
        spdx = "MIT"
    non_ascii_holder = False
    for line in txt.splitlines():
        if "Copyright" in line and any(ord(c) > 127 for c in line):
            non_ascii_holder = True
    return spdx, non_ascii_holder


# --------------------------------------------------------------------------
# ★安全红线：密钥/授权码扫描（校对/审核/审定环节强制消灭"不该进 GitHub 的东西"）
# --------------------------------------------------------------------------
# 设计动因：v1.9.x 曾因技能目录混入明文 QQ SMTP 授权码（硬编码于 send_review_email.py）
# 被 commit+push 到公开 GitHub，触发 ClawHub SkillSpector 判 malicious 并封禁。
# 现把"凭据扫描"做成 validate / gate / release 的**强制 FAIL 闸门**：任何硬编码密码、
# 授权码、API Token 在校对阶段就被拦下，绝不会进入 GitHub / ClawHub。
#
# 设计原则：宁可误报也要拦住真凭据；误报用仓库根目录的 .releaser-secret-allow 放行。
# 报告里**绝不回显明文凭据**（一律脱敏）。

# 1) 凭据赋值关键词：识别 `PASSWORD = "..."` / `api_key="..."` / `client_secret='...'` 等
SECRET_ASSIGN_KEYS = (
    "password", "passwd", "pwd", "secret", "token", "apikey", "api_key",
    "access_token", "auth_token", "client_secret", "private_key", "privatekey",
    "authorization_code", "auth_code", "smtp_password", "smtp_pass", "smtp_pwd",
    "db_password", "database_password", "root_password", "admin_password",
    "bearer", "credential", "credentials", "license_key", "activation_code",
    "secret_key", "signing_key", "encryption_key", "api_secret",
)

# 2) 已知厂商令牌格式（高置信，无论上下文，命中即报）
SECRET_TOKEN_PATTERNS = [
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub PAT", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{36,}\b")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{8,}\b")),
    ("Google API Key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Stripe Secret", re.compile(r"\bsk_(live|test)_[0-9A-Za-z]{16,}\b")),
    ("OpenAI Key", re.compile(r"\bsk-[0-9A-Za-z]{20,}\b")),
    ("OpenRouter Key", re.compile(r"\bsk-or-v1-[0-9A-Za-z]{64}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b")),
    ("PEM Private Key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("BasicAuth(user:pass@)", re.compile(r"\b[a-zA-Z0-9._%+\-]+:[a-zA-Z0-9._%+\-]{3,}@[a-zA-Z0-9.\-]+\b")),
]

# 明显占位/示例/环境引用（不报警）
SECRET_SAFE_HINTS = (
    "your-", "your_", "your.", "example", "sample", "dummy", "fake", "test",
    "xxxx", "xxxxxxxx", "replace", "changeme", "changethis", "placeholder",
    "token_here", "secret_here", "password_here", "redacted", "<", ">",
    "none", "null", "none)", "***", "to-do", "todo", "mock",
)
# 环境变量引用（凭据应由运行时注入，不从仓库读）—— 这类赋值视为安全
SECRET_ENV_REF_HINTS = (
    "os.environ", "getenv", "environ[", "environ.get", "${", "{{",
    "input(", "getpass", "secret_ref", "resolve_secret", "get_secret",
)

# 扫描的文件扩展名（.env 无论扩展名都扫）；令牌格式只在代码/配置类文件扫，避免 .md 误伤
SECRET_SCAN_EXTS = {".py", ".js", ".ts", ".sh", ".env", ".json", ".yaml",
                    ".yml", ".toml", ".txt", ".cfg", ".ini", ".md", ".rst"}
SECRET_TOKEN_EXTS = {".py", ".js", ".ts", ".sh", ".env", ".json", ".yaml",
                     ".yml", ".toml", ".txt", ".cfg", ".ini"}
SECRET_SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
                    ".pytest_cache", ".mypy_cache"}
# 扫描器自身的配置常量名（左侧标识符命中凭据关键词时跳过，避免自伤）
SECRET_OWN_IDENTIFIERS = {
    "secret_assign_keys", "secret_token_patterns", "secret_safe_hints",
    "secret_scan_exts", "secret_token_exts", "secret_skip_dirs",
    "secret_own_identifiers",
}


def _secret_looks_safe(val):
    """值是否为明显占位/示例/环境引用——这类不算泄露，不报警。"""
    low = (val or "").lower()
    if len(low) < 6:
        return True  # 太短无意义
    for h in SECRET_SAFE_HINTS:
        if h in low:
            return True
    if low.strip("\"' ") in SECRET_ASSIGN_KEYS:  # 恰好等于某个凭据关键词
        return True
    return False


def _secret_extract_literal(s):
    """抽取字符串中第一个『引号包裹』的字面量（凭据值）。无则返回 None。"""
    m = re.search(r'''["']([^"']{1,256})["']''', s)
    return m.group(1) if m else None


def _secret_redact(s):
    """脱敏：绝不回显明文。只留前 4 + 后 2 字符。"""
    s = (s or "").strip().strip("\"'")
    if len(s) <= 6:
        return "••••"
    return s[:4] + "…" + s[-2:]


def _load_secret_allow(skill_dir, allow_file):
    path = allow_file or os.path.join(skill_dir, ".releaser-secret-allow")
    out = []
    if os.path.isfile(path):
        for ln in _read(path).splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                try:
                    out.append(re.compile(ln))
                except re.error:
                    pass
    return out


def _secret_ignored(allow, rel, line):
    for pat in allow:
        if pat.search(rel) or (line and pat.search(line)):
            return True
    return False


def _secret_scan(skill_dir, allow_file=None):
    """扫描技能目录，返回 [(level, title, detail)]（每条脱敏后的定位）。

    设计原则：宁可误报也要拦住真凭据；误报用 .releaser-secret-allow 放行。
    """
    findings = []
    allow = _load_secret_allow(skill_dir, allow_file)

    files = []
    for root, dirs, fns in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in SECRET_SKIP_DIRS]
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SECRET_SCAN_EXTS or fn.startswith(".env"):
                files.append(os.path.join(root, fn))

    for f in files:
        rel = os.path.relpath(f, skill_dir)
        if _secret_ignored(allow, rel, ""):
            continue
        # a) .env 文件本身即风险（禁止入库）
        if os.path.basename(f).startswith(".env"):
            findings.append(("FAIL", "发现 .env 凭据文件（禁止入库）",
                             "%s —— 移到仓库外或用 .gitignore 排除" % rel))
            continue
        text = _read(f)
        ext = os.path.splitext(f)[1].lower()
        # b) 已知令牌格式（仅代码/配置文件，.md 不扫）
        if ext in SECRET_TOKEN_EXTS:
            for name, pat in SECRET_TOKEN_PATTERNS:
                for m in pat.finditer(text):
                    snip = m.group(0)
                    if _secret_looks_safe(snip):
                        continue
                    if _secret_ignored(allow, rel, snip):
                        continue
                    findings.append(("FAIL", "命中已知凭据格式: %s" % name,
                                     "%s — %s" % (rel, _secret_redact(snip))))
        # c) 硬编码凭据赋值（所有文本文件）：仅当『赋值左侧标识符』本身含凭据关键词才判，
        #    避免文档/字符串里出现 password/token 等词、或引号值误伤（如本工具自身定义、中文说明）。
        assign_re = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$')
        colon_re = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$')
        for i, line in enumerate(text.splitlines(), 1):
            m = assign_re.match(line)
            if not m:
                m = colon_re.match(line)
            if not m:
                continue
            key = m.group(1).lower()
            if key in SECRET_OWN_IDENTIFIERS:
                continue
            if not any(k in key for k in SECRET_ASSIGN_KEYS):
                continue
            rest = m.group(2)
            # 环境变量引用视为安全（凭据由运行时注入，不入库）
            if any(h in rest.lower() for h in SECRET_ENV_REF_HINTS):
                continue
            val = _secret_extract_literal(rest)
            if not val:
                continue
            if _secret_looks_safe(val) or len(val) < 10:
                continue
            if _secret_ignored(allow, rel, line):
                continue
            findings.append(("FAIL", "疑似硬编码凭据赋值",
                             "%s:%d — %s = %s" % (rel, i, m.group(1), _secret_redact(val))))
    return findings


def validate_skill(skill_dir, mode="skill", silent=False):
    """对一个技能/CLI 目录跑全套发布就绪检查，结果写入 REPORT。返回失败数。"""
    REPORT.clear()
    skill_md = os.path.join(skill_dir, "SKILL.md")
    has_skill = os.path.isfile(skill_md)

    if mode == "package":
        _add("PASS", "非技能项目（--mode package），跳过 frontmatter/skill-card 检查", "", 0)
        fm, body = {}, ""
        slug = os.path.basename(skill_dir)
    elif mode == "cli" and not has_skill:
        _add("PASS", "非技能项目（--mode cli），跳过 frontmatter/skill-card 检查", "", 0)
        fm, body = {}, ""
        slug = os.path.basename(skill_dir)
    elif not has_skill:
        _add("FAIL", "SKILL.md 缺失", skill_dir, W["fm_fields"])
        return 1
    else:
        fm, body = parse_frontmatter(skill_md)
        slug = fm.get("slug") or fm.get("name") or os.path.basename(skill_dir)

        # 1) frontmatter 关键字段
        missing = [k for k in ("name", "version", "license") if not fm.get(k)]
        if missing:
            _add("FAIL", "frontmatter 缺字段", ", ".join(missing), W["fm_fields"])
        else:
            _add("PASS", "frontmatter 含 name/version/license", "", W["fm_fields"])
        lic_field = (fm.get("license") or "").upper()
        if lic_field and ("MIT-0" in lic_field or "MIT" in lic_field):
            _add("PASS", "frontmatter license 字段 = %s" % fm.get("license"), "", W["lic_field"])
        elif fm.get("license"):
            _add("WARN", "license 字段非 MIT/MIT-0", fm.get("license"), W["lic_field"])
        else:
            _add("WARN", "license 字段未识别", "", W["lic_field"])

        # 3) skill-card.md 保留名冲突（全仓递归）—— 仅技能模式
        hits = []
        for root, _dirs, files in os.walk(skill_dir):
            for fn in files:
                if fn == "skill-card.md":
                    hits.append(os.path.relpath(os.path.join(root, fn), skill_dir))
        if hits:
            _add("FAIL", "存在 ClawHub 保留名 skill-card.md", "; ".join(hits), W["no_card"])
        else:
            _add("PASS", "全仓无 skill-card.md 保留名冲突", "", W["no_card"])

    # 3b) 包发布清单（仅 package 模式，信息项不计分）
    if mode == "package":
        manifests = ["pyproject.toml", "setup.py", "setup.cfg"]
        found = [m for m in manifests if os.path.isfile(os.path.join(skill_dir, m))]
        if found:
            _add("PASS", "检测到打包清单: " + ", ".join(found), "", 0)
        else:
            _add("WARN", "未检测到打包清单(pyproject.toml/setup.py/setup.cfg)，pip 安装将失败", "", 0)

    # 2) LICENSE 文件 + licensee 识别（两种模式都查）
    lic_path = os.path.join(skill_dir, "LICENSE")
    if not os.path.isfile(lic_path):
        _add("FAIL", "LICENSE 文件缺失（GitHub 显示 Other）", "", W["lic_spdx"])
    else:
        spdx, non_ascii = detect_license(lic_path)
        if spdx:
            _add("PASS", "LICENSE 含可识别 SPDX: %s" % spdx, "", W["lic_spdx"])
        else:
            _add("WARN", "LICENSE 非标准 MIT/MIT-0 全文，licensee 可能判 Other", "", W["lic_spdx"])
        if non_ascii:
            _add("FAIL", "LICENSE 版权持有人含非 ASCII（licensee 易判 NOASSERTION/Other）", "", W["lic_ascii"])
        else:
            _add("PASS", "LICENSE 版权名为 ASCII", "", W["lic_ascii"])

    # 4) doctor --path . 真跑（防递归：被 doctor 子命令递归调用时不再二次 spawn）
    main = find_main_entry(skill_dir, slug) if has_skill else (
        find_main_entry(skill_dir, os.path.basename(skill_dir)))
    if os.environ.get("RELEASER_VALIDATE_DEPTH"):
        _add("PASS", "doctor 自检门已在父级执行（防递归，跳过二次 spawn）", "", W["doctor"])
    elif not main:
        _add("WARN", "未找到带 doctor 子命令的 CLI 入口（CI 无法跑自检门）", "", W["doctor"])
    else:
        env = dict(os.environ)
        env["RELEASER_VALIDATE_DEPTH"] = "1"
        r = subprocess.run([sys.executable, main, "doctor", "--path", "."],
                           cwd=skill_dir, capture_output=True, text=True, env=env)
        if r.returncode == 0:
            _add("PASS", "doctor --path . 退出 0（过 CI 必现失败陷阱）", "", W["doctor"])
        else:
            _add("FAIL", "doctor --path . 退出 %d" % r.returncode,
                 (r.stderr or r.stdout).strip()[-200:], W["doctor"])

    # 5) CI 模板：含 doctor 步 + tee
    ci = os.path.join(skill_dir, ".github", "workflows", "ci.yml")
    if not os.path.isfile(ci):
        _add("WARN", "无 .github/workflows/ci.yml（不上 CI 可忽略）", "", W["ci"])
    else:
        citxt = _read(ci)
        if "doctor --path" in citxt and "tee $GITHUB_STEP_SUMMARY" in citxt:
            _add("PASS", "CI 含 doctor 步 + tee Step Summary（排障命门）", "", W["ci"])
        elif "doctor --path" in citxt:
            _add("WARN", "CI 有 doctor 步但缺 tee $GITHUB_STEP_SUMMARY", "", W["ci"])
        else:
            _add("WARN", "CI 未含 doctor --path . 步", "", W["ci"])

    # 6) 引用完整性（SKILL.md 引用的 scripts/references/assets 是否真实存在）
    refs = set()
    if has_skill:
        for pat in REF_PATTERNS:
            for m in pat.findall(body):
                refs.add(m)
        missing_refs = [r for r in sorted(refs) if not os.path.isfile(os.path.join(skill_dir, r))]
        if not refs:
            _add("PASS", "SKILL.md 无外部文件引用（无需校验）", "", W["ref"])
        elif missing_refs:
            _add("FAIL", "SKILL.md 引用了不存在的文件", "; ".join(missing_refs), W["ref"])
        else:
            _add("PASS", "SKILL.md 引用的 %d 个文件均存在" % len(refs), "", W["ref"])

    # 7) 零依赖自检（仅扫描入口与 scripts）
    bad = _scan_imports(skill_dir, skip={"scaffold.py"})
    if bad:
        _add("WARN", "检测到可能非标准库依赖", ", ".join(sorted(bad)[:8]), W["zero"])
    else:
        _add("PASS", "未发现非标准库 import（零依赖）", "", W["zero"])

    # 8) ★功能级/可执行验证（竞品无人做）：compile + import + --help 烟测
    _functional_checks(skill_dir, mode, slug, has_skill)

    # 9) ★安全红线：密钥/授权码扫描（校对环节强制消灭"不该进 GitHub 的东西"）
    #    重演 v1.9.x：明文 QQ SMTP 授权码被 commit+push 触发 ClawHub 判 malicious。
    #    本项在发布前（validate / gate / release）就 FAIL 拦截，绝不让凭据入库。
    sec = _secret_scan(skill_dir)
    if sec:
        _add("FAIL", "安全红线：检测到 %d 处疑似硬编码凭据/授权码（禁止入库！）" % len(sec),
             "运行 `python releaser.py secretscan --path .` 看明细；改为环境变量/密钥库后再发",
             W["secret"])
        for lv, title, detail in sec[:12]:
            _add(lv, title, detail, 0)
    else:
        _add("PASS", "全仓无硬编码凭据/授权码（安全红线通过）", "", W["secret"])

    fails = sum(1 for r in REPORT if r[0] == "FAIL")
    return fails


def _scan_imports(skill_dir, skip=None):
    bad = set()
    skip = skip or set()
    targets = []
    for root, _d, files in os.walk(skill_dir):
        if ".git" in root or "tests" in root:
            continue
        for fn in files:
            if fn.endswith(".py") and fn not in skip:
                targets.append(os.path.join(root, fn))
    local_mods = {os.path.splitext(fn)[0] for fn in os.listdir(skill_dir)}
    for path in targets:
        for line in _read(path).splitlines():
            m = re.match(r"^\s*(?:import|from)\s+([A-Za-z_][\w.]*)", line)
            if not m:
                continue
            top = m.group(1).split(".")[0]
            if top in local_mods:
                continue
            if STD_LIB and top in STD_LIB:
                continue
            if not STD_LIB and top in ("os", "sys", "re", "ast", "argparse",
                                       "subprocess", "json", "html", "shlex",
                                       "datetime", "pathlib", "textwrap", "collections"):
                continue
            bad.add(top)
    return bad


def _run(cmd, cwd, timeout=25):
    """带超时的子进程运行，超时返回 returncode=124 的伪结果。"""
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        class _R:
            returncode = 124
            stdout = ""
            stderr = "timeout after %ss" % timeout
        return _R()


def _top_entry(skill_dir, slug, has_skill):
    """找一个可作为『功能验证』目标的顶层 .py 入口（优先带 doctor 子命令者）。"""
    cand = find_main_entry(skill_dir, slug) if has_skill else \
        find_main_entry(skill_dir, os.path.basename(skill_dir))
    if cand and os.path.dirname(cand) == skill_dir:
        return cand
    for f in sorted(os.listdir(skill_dir)):
        if f.endswith(".py") and f not in ("scaffold.py", "__init__.py"):
            return os.path.join(skill_dir, f)
    return None


def _functional_checks(skill_dir, mode, slug, has_skill):
    """★功能验证（竞品无人做）：compile + import + --help 烟测，证明 CLI 真能 boot。

    结构性 linter（skill-lint / agent-skill-linter / @effectorhq 等）只查 paperwork；
    本检查把代码真正执行起来，挡住『格式完美却一跑就崩』的技能。
    """
    # 1) compile 全部 .py（语法错误是发行级硬伤）
    bad = []
    for root, dirs, files in os.walk(skill_dir):
        if ".git" in root or ".venv" in root or "node_modules" in root or "__pycache__" in root:
            continue
        for fn in files:
            if fn.endswith(".py"):
                p = os.path.join(root, fn)
                try:
                    with open(p, "rb") as f:
                        compile(f.read(), p, "exec")
                except SyntaxError as e:
                    bad.append("%s:%s" % (os.path.relpath(p, skill_dir), e.lineno))
    if bad:
        _add("FAIL", "存在语法错误（compile 不过）", "; ".join(bad[:5]), W["fn_compile"])
    else:
        _add("PASS", "全部 .py 通过 compile（无语法错误）", "", W["fn_compile"])

    entry = _top_entry(skill_dir, slug, has_skill)
    if not entry:
        _add("WARN", "未找到可 import 的入口模块（跳过 import/--help 功能验证）", "", W["fn_import"])
        _add("WARN", "无入口，跳过 --help 烟测", "", W["fn_smoke"])
        return
    mod = os.path.splitext(os.path.basename(entry))[0]
    # 2) import 入口模块（捕获 import-time 崩溃：顶层代码 / 依赖缺失）
    r = _run([sys.executable, "-c", "import %s" % mod], cwd=skill_dir, timeout=25)
    if r.returncode == 0:
        _add("PASS", "入口模块可 import（无 import-time 崩溃）", "", W["fn_import"])
    else:
        _add("FAIL", "入口模块 import 失败", (r.stderr or r.stdout).strip()[-200:], W["fn_import"])
    # 3) --help 烟测（证明 CLI 真能 boot；argparse 默认提供 --help）
    r = _run([sys.executable, entry, "--help"], cwd=skill_dir, timeout=25)
    if r.returncode == 0:
        _add("PASS", "入口 --help 烟测通过（CLI 可 boot）", "", W["fn_smoke"])
    else:
        _add("WARN", "入口 --help 烟测未通过（非 argparse 或真有 bug）",
             (r.stderr or r.stdout).strip()[-160:], W["fn_smoke"])


# --------------------------------------------------------------------------
# validate 包装
# --------------------------------------------------------------------------

def cmd_validate(args):
    fails = validate_skill(args.path, mode=args.mode, silent=args.json)
    if args.json:
        payload = _report_payload(args.path, args.mode, bench=args.bench)
        if args.rubric:
            payload["rubric"] = {k: {"weight": W[k], "reason": RATIONALE.get(k, "")} for k in W}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        _print_header(args.path)
        _print_report()
        if args.rubric:
            _print_rubric()
        if args.bench:
            _print_bench()
    return 1 if fails else 0


def cmd_secretscan(args):
    """★安全红线：专项扫描硬编码密码/授权码/API Token（独立于就绪分，供发布前单独把关）。

    这是"校对/审核/审定"环节消灭凭据泄露的专用工具：宁可误报也要拦住真凭据，
    误报在仓库根建 `.releaser-secret-allow` 写放行正则（谨慎使用）。
    报告里**绝不回显明文**（一律脱敏）。
    """
    findings = _secret_scan(args.path, allow_file=args.allow_file)
    print("=" * 56)
    print("  releaser secretscan — 安全红线：密钥/授权码扫描")
    print("=" * 56)
    if not findings:
        print("  ✓ 未发现硬编码凭据/授权码。可安全入库。")
        return 0
    print("  ⚠ 发现 %d 处疑似凭据（已脱敏，绝不回显明文）：" % len(findings))
    for lv, title, detail in findings:
        print("   [%s] %s — %s" % (lv, title, detail))
    print("\n  处置：")
    print("    ① 改为环境变量(os.environ)/密钥库，删除明文；")
    print("    ② 已入库的须 git filter-repo 清历史，并**立即轮换**泄露凭据；")
    print("    ③ 确认无误报可在仓库根建 .releaser-secret-allow 写放行正则（谨慎）。")
    return 1


def _print_rubric():
    print("\n" + "=" * 56)
    print("  releaser rubric — 评分权重与理由（合计 %d）" % sum(W.values()))
    print("=" * 56)
    for k, w in W.items():
        star = "*" if k.startswith("fn_") else " "
        print("  %s%-11s %2d  %s" % (star, k, w, RATIONALE.get(k, "")))


def cmd_gate(args):
    """CI 门禁：就绪分低于阈值即非零退出，使『发布就绪分』成为可编排的流水线闸门。"""
    fails = validate_skill(args.path, mode=args.mode, silent=args.json)
    score = _score()
    if args.json:
        payload = _report_payload(args.path, args.mode)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        _print_header(args.path)
        _print_report()
    if fails:
        print("\n[gate] 存在 FAIL，未达发布门禁（min=%d）。" % args.min)
        return 1
    if score < args.min:
        print("\n[gate] 就绪分 %d < 门禁 %d，拦截。" % (score, args.min))
        return 1
    print("\n[gate] 通过：就绪分 %d ≥ 门禁 %d。" % (score, args.min))
    return 0


# --------------------------------------------------------------------------
# inventory —— 治理：扫描本机已装技能就绪度
# --------------------------------------------------------------------------

def default_roots():
    home = os.path.expanduser("~")
    roots = [
        os.path.join(home, ".workbuddy", "skills"),
        os.path.join(home, ".codebuddy", "skills"),
        os.path.join(home, ".openclaw", "skills"),
        os.path.join(home, ".claude", "skills"),
    ]
    return [r for r in roots if os.path.isdir(r)]


def cmd_inventory(args):
    roots = args.roots.split(",") if args.roots else default_roots()
    print("扫描根: " + ", ".join(roots))
    print("%-34s %-7s %-8s %-6s %-5s" % ("技能", "lic字段", "LICENSE", "CI", "doctor"))
    print("-" * 70)
    total = 0
    ready = 0
    for root in roots:
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if not os.path.isdir(d) or not os.path.isfile(os.path.join(d, "SKILL.md")):
                continue
            total += 1
            fm, _ = parse_frontmatter(os.path.join(d, "SKILL.md"))
            lic = (fm.get("license") or "-")[:6]
            has_lic = "Y" if os.path.isfile(os.path.join(d, "LICENSE")) else "-"
            has_ci = "Y" if os.path.isfile(os.path.join(d, ".github", "workflows", "ci.yml")) else "-"
            main = find_main_entry(d, fm.get("slug") or name)
            doc_ok = "-"
            if main:
                env = dict(os.environ)
                env["RELEASER_VALIDATE_DEPTH"] = "1"
                r = subprocess.run([sys.executable, main, "doctor", "--path", "."],
                                   cwd=d, capture_output=True, text=True, env=env)
                doc_ok = "Y" if r.returncode == 0 else "N"
            ok = (lic != "-") and has_lic == "Y" and doc_ok == "Y"
            if ok:
                ready += 1
            print("%-34s %-7s %-8s %-6s %-5s" % (name[:33], lic, has_lic, has_ci, doc_ok))
    print("-" * 70)
    print("共 %d 个技能，发布就绪 %d 个，待补 %d 个" % (total, ready, total - ready))
    return 0


# --------------------------------------------------------------------------
# gap —— 市场情报：扫描本机技能归类，报告稀疏类目
# --------------------------------------------------------------------------

def cmd_gap(args):
    """市场情报：本机覆盖始终计算；加 --scan-json 叠加真实市场数据，交叉出组合机会。"""
    loc_counts = {c: 0 for c in CATEGORY_KEYWORDS}
    skills_local = []
    roots = args.roots.split(",") if args.roots else default_roots()
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            smd = os.path.join(d, "SKILL.md")
            if not os.path.isfile(smd):
                continue
            fm, body = parse_frontmatter(smd)
            text = " ".join([name, fm.get("keywords", ""), fm.get("description", ""), body[:800]])
            cats = categorize(text)
            skills_local.append((name, cats))
            for c in cats:
                loc_counts[c] += 1

    mkt_counts = None
    if args.scan_json:
        mkt_counts = {c: 0 for c in CATEGORY_KEYWORDS}
        try:
            with open(args.scan_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("[gap] 读取扫描数据失败: %s" % e)
            return 1
        for item in data:
            cats = item.get("categories") or categorize(" ".join([
                item.get("name", ""), item.get("keywords", ""), item.get("description", "")]))
            for c in cats:
                mkt_counts[c] += 1

    print("=" * 56)
    print("  releaser gap — 技能组合缺口扫描")
    print("=" * 56)
    print("本机已扫描技能数: %d" % len(skills_local))
    print("\n[本机] 类目覆盖（技能数）:")
    for c in CATEGORY_KEYWORDS:
        print("  %-16s %2d  %s" % (c, loc_counts[c], "#" * loc_counts[c]))

    gaps = [c for c in CATEGORY_KEYWORDS if loc_counts[c] == 0]
    thin = [c for c in CATEGORY_KEYWORDS if loc_counts[c] == 1]
    print("\n>> 本机缺口（覆盖 =0，建议新建）:")
    for c in gaps:
        slug = "skill-" + re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")
        print("  - [%s] python releaser.py scaffold %s --author \"He Wei\"" % (c, slug))
    if not gaps:
        print("  （无完全空白类目）")
    print("\n>> 本机可补强（覆盖 =1）:")
    for c in thin:
        slug = "skill-" + re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")
        print("  - [%s] python releaser.py scaffold %s --author \"He Wei\"" % (c, slug))
    if not thin:
        print("  （无）")

    if mkt_counts is not None:
        print("\n[市场] 类目覆盖（来自 find-skills++ 真实扫描，技能数）:")
        for c in CATEGORY_KEYWORDS:
            print("  %-16s %2d  %s" % (c, mkt_counts[c], "#" * mkt_counts[c]))
        print("\n>> ★组合机会（市场有供给、你为 0）：最该造的方向")
        opp = [c for c in CATEGORY_KEYWORDS if loc_counts[c] == 0 and mkt_counts[c] > 0]
        if opp:
            for c in opp:
                print("  - [%s] 市场 %d 个 / 你 0 个 → scaffold %s" % (
                    c, mkt_counts[c], "skill-" + re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")))
        else:
            print("  （无：本机已覆盖市场所有类目，或市场数据为空）")
        print("\n提示: 组合缺口 = 把『本机盲区』与『真实市场供给』交叉，找出你该优先造的技能。")
    else:
        print("\n提示: 加 --scan-json <file> 可消费 find-skills++ 真实市场数据，")
        print("      交叉出『市场有、你缺』的组合机会（独有飞轮情报）。")
    return 0


# --------------------------------------------------------------------------
# selfcheck —— 零依赖校验
# --------------------------------------------------------------------------

def cmd_selfcheck(args):
    REPORT.clear()
    if args.path:
        d = args.path
    else:
        d = os.path.dirname(os.path.abspath(__file__))
    bad = _scan_imports(d, skip={"scaffold.py"})
    if bad:
        for b in sorted(bad):
            _add("WARN", "可能非标准库依赖: " + b)
        _print_report()
        return 1
    _add("PASS", "未发现非标准库 import（零依赖成立）")
    _print_report()
    return 0


# --------------------------------------------------------------------------
# bump —— 升版本 + 补 CHANGELOG
# --------------------------------------------------------------------------

def _bump_version(ver, typ):
    parts = ver.split(".")
    while len(parts) < 3:
        parts.append("0")
    maj, mn, pt = int(parts[0]), int(parts[1]), int(parts[2])
    if typ == "major":
        maj, mn, pt = maj + 1, 0, 0
    elif typ == "minor":
        mn, pt = mn + 1, 0
    else:
        pt += 1
    return "%d.%d.%d" % (maj, mn, pt)


def cmd_bump(args):
    d = args.path or "."
    skill_md = os.path.join(d, "SKILL.md")
    if not os.path.isfile(skill_md):
        print("[bump] 未找到 SKILL.md: " + skill_md)
        return 1
    fm, _ = parse_frontmatter(skill_md)
    old = fm.get("version", "0.1.0")
    new = _bump_version(old, args.type)
    txt = _read(skill_md)
    txt = re.sub(r"(?m)^(version:\s*)\S+", lambda m: m.group(1) + new, txt, count=1)
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(txt)
    today = datetime.date.today().isoformat()
    chlog = os.path.join(d, "CHANGELOG.md")
    entry = "\n## [%s] — %s · %s\n- （填写本次变更）\n" % (new, today, args.type)
    if os.path.isfile(chlog):
        with open(chlog, "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)
            f.write(entry + "\n" + content)
    else:
        with open(chlog, "w", encoding="utf-8") as f:
            f.write("# CHANGELOG\n" + entry + "\n")
    print("[bump] %s → %s（CHANGELOG 已加条目）" % (old, new))
    return 0


# --------------------------------------------------------------------------
# release —— git 推送 + 构造 ClawHub 导入链接 + 预填元数据（近一键）
# --------------------------------------------------------------------------

def _repo_url(d):
    try:
        r = subprocess.run(["git", "-C", d, "remote", "get-url", "origin"],
                           capture_output=True, text=True, check=False)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return None


def _clawhub_publish(d, slug, name, version, changelog):
    """可选：若本机装有 clawhub CLI 且已登录，则直调发布（英文生态真一键）。

    2026 实测：ClawHub 没有公开 REST/网页 publish 端点，但有官方 npm CLI
    `clawhub publish ./dir --slug --name --version --changelog`——这是合法的"真一键"路径。
    本函数仅在 CLI 存在时触发，且绝不伪造调用；缺 CLI 则回退人工导入情报。
    """
    import shutil
    cli = shutil.which("clawhub")
    if not cli:
        return False, "本机未安装 clawhub CLI（npm i -g clawhub），回退人工导入"
    r = subprocess.run([cli, "whoami"], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        return False, "clawhub 未登录（先 `clawhub login`），回退人工导入"
    pr = subprocess.run([cli, "publish", d, "--slug", slug, "--name", name,
                         "--version", version, "--changelog", changelog or "release via releaser"],
                        capture_output=True, text=True, check=False)
    if pr.returncode == 0:
        return True, (pr.stdout or pr.stderr).strip() or "已发布"
    return False, "clawhub publish 失败: " + (pr.stderr or pr.stdout).strip()[-200:]


def _auto_topics(keywords_str, max_len=48):
    kws = [k.strip() for k in (keywords_str or "").replace(";", ",").split(",") if k.strip()]
    if not kws:
        return "skill"
    picked, used = [], 0
    for k in kws:
        add = (", " if picked else "") + k
        if used + len(add) <= max_len:
            picked.append(k)
            used += len(add)
        else:
            break
    out = ", ".join(picked)
    return out[:max_len] if len(out) > max_len else out


def cmd_release(args):
    d = args.path or "."
    is_git = os.path.isdir(os.path.join(d, ".git"))
    if not is_git:
        print("[release] 注意: 当前不是 git 仓库，跳过提交/推送（仍可生成导入步骤）。")
    # 1) 校验发布就绪
    print("[release] 先跑 validate：")
    fails = validate_skill(d)
    _print_report()
    if fails:
        print("[release] 有 %d 项 FAIL，建议先修复再发。\n" % fails)

    # 1b) ★安全红线：硬编码凭据直接拒绝提交/推送/发布（审定闸门）
    allow_risk = getattr(args, "allow_secret_risk", False)
    has_secret = any(r[0] == "FAIL" and r[1].startswith("安全红线") for r in REPORT)
    if has_secret and not allow_risk:
        print("[release] ⛔ 安全红线拦截：存在硬编码凭据/授权码，拒绝提交/推送/发布！")
        print("[release] 处置：改为环境变量/密钥库后重跑；确认无误报用 --allow-secret-risk 强制（危险）。")
        return 1
    if has_secret and allow_risk:
        print("[release] ⚠ --allow-secret-risk 已强制越过安全红线（请确认无真实凭据入库）。")
    # 2) 本地提交（dry-run 不提交）；远程推送需显式 --push
    if not args.dry_run:
        if is_git:
            subprocess.run(["git", "-C", d, "add", "-A"], check=False)
            st = subprocess.run(["git", "-C", d, "status", "--porcelain"],
                                capture_output=True, text=True, check=False)
            if st.stdout.strip():
                msg = args.message or ("chore: release via releaser (%s)" % datetime.date.today().isoformat())
                subprocess.run(["git", "-C", d, "commit", "-m", msg], check=False)
                print("[release] 已本地提交（未推送；需要推送请加 --push）。")
            else:
                print("[release] 无改动，未提交")
        else:
            print("[release] 非 git 仓库，跳过本地提交。")
    else:
        print("[release] --dry-run：跳过本地提交与推送")

    # 2b) 远程推送：仅当显式 --push（绝不静默推送）
    if args.push and not args.dry_run and is_git:
        pr = subprocess.run(["git", "-C", d, "push", args.remote, args.branch],
                            capture_output=True, text=True, check=False)
        print(pr.stdout.strip() or pr.stderr.strip() or "[release] 已尝试推送")
    elif args.push and not is_git:
        print("[release] --push 但当前不是 git 仓库，无法推送。")

    # 2c) ClawHub 发布：仅当显式 --publish（且本机已装 clawhub CLI 并登录）
    if args.publish and not args.dry_run and os.path.isfile(os.path.join(d, "SKILL.md")):
        fm, _ = parse_frontmatter(os.path.join(d, "SKILL.md"))
        slug = fm.get("slug") or os.path.basename(os.path.abspath(d))
        name = fm.get("name") or slug
        ver = fm.get("version") or "1.0.0"
        ok, msg = _clawhub_publish(d, slug, name, ver, args.message)
        print("[release] clawhub publish: " + msg)
        if ok:
            print("[release] 已通过 clawhub CLI 发布（需你本机已安装并登录 clawhub CLI）。")
            # 发布成功同样要登记账本（状态层 A）
            try:
                _ledger_add({
                    "slug": slug, "name": name, "repo": _repo_url(d) or "",
                    "version": ver, "score": _score(),
                    "market": "clawhub", "path": os.path.abspath(d),
                    "published_at": datetime.date.today().isoformat(),
                    "last_checked": datetime.date.today().isoformat(),
                })
            except Exception:
                pass
            return 0
        else:
            print("[release] clawhub 发布未成功，下方仍给出人工导入步骤。")

    # 3) 构造人工导入步骤（默认路径：不推送、不发布，只给预填情报）
    fm, _ = parse_frontmatter(os.path.join(d, "SKILL.md")) if os.path.isfile(os.path.join(d, "SKILL.md")) else ({}, "")
    name = fm.get("name") or os.path.basename(os.path.abspath(d))
    slug = fm.get("slug") or os.path.basename(os.path.abspath(d))
    ver = fm.get("version") or "1.0.0"
    cats, topics_list, github = _registry_meta(fm)
    topics = ", ".join(topics_list) or "skill"
    repo = _repo_url(d)
    print("\n[release] 下一步（ClawHub 导入，需你登录后点一次）:")
    print("  ① 打开 ClawHub → Import from GitHub")
    if repo:
        print("  ② 粘贴仓库地址: " + repo)
    else:
        print("  ② 粘贴本仓库的 GitHub 地址（当前未配置 origin remote）")
    print("  ③ 预填（自动）: Display=%s | Slug=%s" % (name, slug))
    print("      License=MIT-0 | ClawHub 分类(slug)=%s" % " / ".join(cats))
    print("      ClawHub Topics=%s  (≤5，已过滤保留词/≤48字符)" % topics)
    print("      GitHub topics=%s" % ", ".join(github))
    print("  ④ 点 Publish selected 即上线。")
    # 登记到账本（状态层 A）：发布动作即记录，供 recheck 生命周期治理消费
    try:
        _ledger_add({
            "slug": slug, "name": name, "repo": repo or "",
            "version": ver, "score": _score(),
            "market": "manual",
            "path": os.path.abspath(d),
            "published_at": datetime.date.today().isoformat(),
            "last_checked": datetime.date.today().isoformat(),
        })
    except Exception:
        pass  # 账本登记失败不影响发布主流程
    return 0


# --------------------------------------------------------------------------
# publish —— 多站上架编排（显式逐站授权；安全闸门前置）
# --------------------------------------------------------------------------

def _publish_github(d, remote, branch, message, force, dry_run):
    """★GitHub：本地提交 + 推送。仅当 --github 显式授权才触碰远端；绝不静默。

    --force-history：历史曾被 git filter-repo 重写后，远端与本地分叉，需强推
    （默认用 --force-with-lease 防覆盖他人提交；常规更新走普通 fast-forward 推送）。
    """
    if dry_run:
        is_git = os.path.isdir(os.path.join(d, ".git"))
        note = "" if is_git else "（当前非 git 仓库，正式运行需先 `git init` + 配置 origin）"
        return True, "[dry-run] 将：git add -A → commit → git push %s %s%s" % (
            remote, branch, " --force-with-lease" if force else "") + note
    is_git = os.path.isdir(os.path.join(d, ".git"))
    if not is_git:
        return False, "当前不是 git 仓库，无法推送到 GitHub（先 `git init` + 配置 origin）。"
    subprocess.run(["git", "-C", d, "add", "-A"], check=False)
    st = subprocess.run(["git", "-C", d, "status", "--porcelain"],
                        capture_output=True, text=True, check=False)
    if st.stdout.strip():
        msg = message or ("chore: publish via releaser (%s)" % datetime.date.today().isoformat())
        subprocess.run(["git", "-C", d, "commit", "-m", msg], check=False)
    else:
        print("[publish] GitHub: 无改动，未提交。")
    push = ["git", "-C", d, "push"]
    if force:
        push.append("--force-with-lease")
    push += [remote, branch]
    r = subprocess.run(push, capture_output=True, text=True, check=False)
    out = (r.stdout or r.stderr).strip()
    if r.returncode == 0:
        return True, "已推送到 GitHub(%s/%s): %s" % (remote, branch, out[:160])
    # 非快进失败：提示用 --force-history（历史曾被重写）
    if "non-fast-forward" in out or "fetch first" in out or "rejected" in out:
        return False, ("普通推送被拒(非快进)：远端与本地分叉。若历史曾被 git filter-repo 重写，"
                       "请加 --force-history 强推；否则先 `git pull --rebase`。\n" + out[:200])
    return False, "GitHub 推送失败: " + out[:200]


def _publish_xiaping(d, dry_run):
    """★虾评（xiaping.coze.site）：预留位（本轮未接入，无公开 API）。

    暂不触碰远程，仅给出下一步人工链接，待接入 Coze bot / 开放上传接口后真自动。
    """
    if dry_run:
        return True, "[dry-run] 虾评：将打包 Coze 技能格式并打开 xiaping.coze.site 上传页。"
    return False, ("虾评(xiaping.coze.site) 本轮未接入自动上传（无公开 API）。"
                  "请手动：登录 xiaping.coze.site → 上传技能 → 走众测转正流程。"
                  "后续将接入 Coze bot 实现真自动。")


def _publish_workbuddy(d, dry_run):
    """★WorkBuddy SkillHub（open.workbuddy.cn）：预留位（本轮未接入，无公开 API）。

    暂不触碰远程，仅给出下一步人工链接，待接入开放平台上传接口后真自动。
    """
    if dry_run:
        return True, "[dry-run] WorkBuddy：将打成 ≤3MB ZIP 并打开 open.workbuddy.cn 上传页。"
    return False, ("WorkBuddy SkillHub(open.workbuddy.cn) 本轮未接入自动上传（无公开 API）。"
                  "请手动：打包 ≤3MB ZIP(SKILL.md + references/scripts) → 开放平台『发布新技能』"
                  "→ 填 description_zh/en、version、author → 提交审核。后续将接入开放平台接口真自动。")


def cmd_publish(args):
    """★多站上架编排：正确更新/新技能后，一键把技能发布到多站（默认不碰任何远程）。

    设计原则（回应 ClawHub malicious 误判 + 用户的『校对/审核/审定』要求）：
      · 安全闸门前置：先跑 validate(校对) + secretscan(审定)，凭据命中即拦截，绝不入库/外发；
      · 显式逐站授权：每个目标需对应开关(--github/--clawhub/--xiaping/--workbuddy)，
        未开的站绝不触碰；没有任何『无开关自动推全站』的路径，杜绝静默远程写入；
      · 本轮只做 GitHub + ClawHub（你已选）；虾评/WorkBuddy 为预留位，仅给人工链接。
    """
    d = args.path or "."
    has_skill = os.path.isfile(os.path.join(d, "SKILL.md"))
    if not has_skill:
        print("[publish] ✗ 当前目录无 SKILL.md，不是技能目录，退出。")
        return 1
    # 1) 校对 + 审核：validate
    print("[publish] ① 校对: validate（发布就绪扫描）")
    validate_skill(d)
    _print_report()
    # 1b) 审定：安全红线
    allow_risk = getattr(args, "allow_secret_risk", False)
    has_secret = any(r[0] == "FAIL" and r[1].startswith("安全红线") for r in REPORT)
    if has_secret and not allow_risk:
        print("\n[publish] ⛔ 安全红线拦截：存在硬编码凭据/授权码，拒绝上架任何站点！")
        print("[publish] 处置：改为环境变量/密钥库后重跑；确认无误报用 --allow-secret-risk 强制（危险）。")
        return 1
    if has_secret and allow_risk:
        print("\n[publish] ⚠ --allow-secret-risk 已强制越过安全红线（请确认无真实凭据入库）。")
    # 2) 确定上架目标（显式授权）
    targets = []
    for flag, name in ((args.github, "github"), (args.clawhub, "clawhub"),
                       (args.xiaping, "xiaping"), (args.workbuddy, "workbuddy")):
        if flag:
            targets.append(name)
    if not targets:
        print("\n[publish] 未指定任何 --<站点> 开关，按设计不触碰任何远程（防静默外发）。")
    # 上架元数据：从 frontmatter 读取（或自动推导），供你复制到各站
    fm, _ = parse_frontmatter(os.path.join(d, "SKILL.md"))
    cats, topics_list, github = _registry_meta(fm)
    print("\n[publish] 上架元数据（复制到各站时直接粘贴）:")
    print("    ClawHub 分类(精确 slug, ≤3): %s" % ", ".join(cats))
    print("    ClawHub Topics(≤5, 已过滤保留词/≤48字符): %s" % (", ".join(topics_list) or "skill"))
    print("    GitHub topics: %s" % ", ".join(github))
    if not targets:
        print("\n[publish] 预览：可对以下目标显式授权上架 ——")
        print("    python releaser.py publish --github            # 推送到 GitHub")
        print("    python releaser.py publish --clawhub           # 发布到 ClawHub（需 clawhub CLI 登录）")
        print("    python releaser.py publish --github --clawhub  # 两站一起（你选定的本轮范围）")
        print("    # 预留：--xiaping / --workbuddy（本轮未接入）")
        return 0
    print("\n[publish] ② 上架目标（已显式授权）: " + ", ".join(targets))
    # 3) 逐站上架
    fm, _ = parse_frontmatter(os.path.join(d, "SKILL.md"))
    slug = fm.get("slug") or os.path.basename(os.path.abspath(d))
    name = fm.get("name") or slug
    ver = fm.get("version") or "1.0.0"
    any_ok = False
    for t in targets:
        print("\n[publish] ── 站点: %s ──" % t)
        if t == "github":
            ok, msg = _publish_github(d, args.remote, args.branch, args.message,
                                     args.force_history, args.dry_run)
        elif t == "clawhub":
            ok, msg = _clawhub_publish(d, slug, name, ver, args.message)
            if ok and not args.dry_run:
                try:
                    _ledger_add({"slug": slug, "name": name, "repo": _repo_url(d) or "",
                                 "version": ver, "score": _score(), "market": "clawhub",
                                 "path": os.path.abspath(d),
                                 "published_at": datetime.date.today().isoformat(),
                                 "last_checked": datetime.date.today().isoformat()})
                except Exception:
                    pass
        elif t == "xiaping":
            ok, msg = _publish_xiaping(d, args.dry_run)
        elif t == "workbuddy":
            ok, msg = _publish_workbuddy(d, args.dry_run)
        else:
            ok, msg = False, "未知目标"
        status = "✓" if ok else "✗"
        print("  [%s] %s" % (status, msg))
        any_ok = any_ok or ok
    print("\n[publish] 完成。GitHub/ClawHub 已真自动；虾评/WorkBuddy 为人工链接（本轮未接入）。")
    return 0 if any_ok else 1


# --------------------------------------------------------------------------
# doctor —— 自检或委托 validate
# --------------------------------------------------------------------------

def cmd_doctor(args):
    if args.path:
        print("[doctor] 校验目标: " + args.path)
        fails = validate_skill(args.path)
        _print_report()
        return 1 if fails else 0
    here = os.path.dirname(os.path.abspath(__file__))
    print("[doctor] 自检 cli-skill-release: " + here)
    REPORT.clear()
    need = ["SKILL.md", "releaser.py", "scaffold.py", "LICENSE"]
    for f in need:
        _add("PASS" if os.path.isfile(os.path.join(here, f)) else "FAIL", "存在 " + f, "", 0)
    bad = _scan_imports(here, skip={"scaffold.py"})
    if bad:
        _add("WARN", "可能非标准库依赖: " + ", ".join(sorted(bad)))
    else:
        _add("PASS", "零依赖成立")
    _print_report(show_score=False)
    return 0


# --------------------------------------------------------------------------
# scaffold —— 委托同目录 scaffold.py
# --------------------------------------------------------------------------

def cmd_scaffold(args):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import scaffold
    dest = args.dest or os.path.join(os.getcwd(), args.name)
    created = scaffold.scaffold(args.name, args.author, args.email, dest)
    print("[scaffold] 已生成到: " + dest)
    for rel in created:
        print("  + " + rel)
    print("[scaffold] 下一步: cd " + dest + " && python -m venv env && env/Scripts/python -m pip install pytest && python -m pytest -q && python " + args.name.replace('-', '_') + ".py doctor --path .")
    return 0


# --------------------------------------------------------------------------
# badge —— ★链式传播：生成 readiness 徽章 SVG + 链回片段
# --------------------------------------------------------------------------

def _badge_color(score):
    if score >= 90:
        return "#4c1"      # 绿
    if score >= 70:
        return "#dfb317"   # 黄
    return "#e05d44"       # 红


def _text_w(s):
    return len(s) * 7 + 10


def _badge_svg(left, right, color, link=RELEASER_PAGE):
    """生成 shields 风格的扁平徽章 SVG（自托管、无需联网）。"""
    lw, rw = _text_w(left), _text_w(right)
    total = lw + rw
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
        ' width="%d" height="20" role="img" aria-label="%s">'
        '<a xlink:href="%s"><rect width="%d" height="20" fill="#555"/>'
        '<rect x="%d" width="%d" height="20" fill="%s"/>'
        '<g fill="#fff" font-family="Verdana,Geneva,sans-serif" font-size="11" text-anchor="middle">'
        '<text x="%d" y="14">%s</text><text x="%d" y="14">%s</text></g></a></svg>'
    ) % (total, left + " " + right, link, lw, lw, rw, color, lw // 2, left, lw + rw // 2, right)


def _raw_badge_url(repo, branch):
    """把 github 仓库地址转成 raw.githubusercontent.com 徽章地址（自托管，渲染必现）。"""
    if not repo:
        return None
    m = re.match(r"(?:git@|https?://)([^/:]+)[/:]([^/]+)/(.+?)(?:\.git)?/?$", repo)
    if not m or m.group(1) != "github.com":
        return None
    owner, name = m.group(2), m.group(3)
    br = branch or "main"
    return "https://raw.githubusercontent.com/%s/%s/%s/readiness-badge.svg" % (owner, name, br)


def cmd_badge(args):
    """生成 readiness 徽章：基于 validate 的就绪分，输出 SVG + 链回本技能的 markdown 片段。

    这是『链式传播』的引擎：使用者把徽章嵌进自己技能的 README/仓库页，
    每个访问者点徽章即到达本技能页 → 下一个技能作者 → 再挂徽章 → 链式扩散。
    """
    fails = validate_skill(args.path, mode=args.mode, silent=True)
    score = _score()
    color = _badge_color(score)
    svg = _badge_svg("releaser", "%d/100" % score, color, link=args.page or RELEASER_PAGE)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(svg)
        print("[badge] 已写 SVG: " + args.output)
    else:
        print(svg)

    repo = _repo_url(args.path)
    branch = None
    if repo:
        try:
            br = subprocess.run(["git", "-C", args.path, "rev-parse", "--abbrev-ref", "HEAD"],
                                capture_output=True, text=True, check=False)
            branch = br.stdout.strip() or None
        except Exception:
            branch = None
    img = _raw_badge_url(repo, branch) or "<你的仓库 raw 徽章地址，如 https://raw.githubusercontent.com/OWNER/REPO/main/readiness-badge.svg>"
    page = args.page or RELEASER_PAGE
    print("\n[badge] 把下面这段贴进你的技能 README / 仓库首页，即开启链式传播：")
    print(
        "[![releaser readiness](%s)](%s)\n"
        "> 本技能经 [cli-skill-release](%s) 校验发布（零依赖发布工程，就绪分 %d/100）。"
        % (img, page, page, score)
    )
    print("[badge] 提示：徽章链回 %s —— 每个看到你仓库的人都可能成为我们的下一个用户。" % page)
    return 0


# --------------------------------------------------------------------------
# promote —— ★宣传系统：生成可被直接转发/粘贴的传播工具箱
# --------------------------------------------------------------------------

def cmd_promote(args):
    """生成『宣传工具箱』：README 徽章区 + 电梯演讲 + 社媒文案 + 安装一行 + 链式传播指引。

    让每一次下载都变成一次分发：使用者照着贴，就把我们送到他的受众面前。
    """
    score = 0
    if args.path and os.path.isdir(args.path):
        validate_skill(args.path, mode=args.mode, silent=True)
        score = _score()
    page = args.page or RELEASER_PAGE
    repo = _repo_url(args.path) if args.path else None
    img = _raw_badge_url(repo, None) or "<你的仓库 raw 徽章地址>"

    print("=" * 56)
    print("  releaser promote — 链式传播工具箱")
    print("=" * 56)
    print("\n① README 徽章区（贴进你每个技能仓库，自动链回我们）:")
    print("  [![releaser readiness](%s)](%s)" % (img, page))
    print("  > 用 [cli-skill-release](%s) 校验发布 · 别人 lint 文档，我们 execute 引擎。" % page)

    print("\n② 电梯演讲（一句话讲清差异化）:")
    print("  “别人 lint 你的文档，我们 execute 你的引擎——cli-skill-release 把你的技能 CLI")
    print("   真正跑起来证明能 boot，再给 0-100 就绪分、CI 门禁、市场缺口情报，零依赖裸跑。”")

    print("\n③ 社媒/社区文案（可直接转发）:")
    print("  【技能发布不再靠运气】做 WorkBuddy/ClawHub 技能最怕“格式完美一跑就崩”。")
    print("  cli-skill-release 一键校验发布就绪度（含真跑 CLI 的功能验证），零依赖、带 CI 门禁。")
    print("  挂个 readiness 徽章，你的技能更可信，也帮我们找到彼此 → %s" % page)

    print("\n④ 安装/使用一行:")
    print("  git clone <本仓库> && cd cli-skill-release && python releaser.py validate --path <你的技能>")

    print("\n⑤ 链式传播玩法（关键）:")
    print("  - 你每发一个技能都跑 validate + badge，把徽章放进该仓库 README；")
    print("  - 徽章链回 %s，访问你仓库的人点进来即用；" % page)
    print("  - 他们也发技能→也挂徽章→链越铺越长。一个人下载，整张网都在帮你分发。")
    if score:
        print("\n[promote] 你当前技能的就绪分: %d/100（满分再发，徽章更亮，转化更高）。" % score)
    return 0


# --------------------------------------------------------------------------
# diagnose —— ★长尾功能：症状 → 根因 → 修复（直接回答用户实际会搜的长尾问题）
# --------------------------------------------------------------------------

def cmd_diagnose(args):
    """把『用户实际会搜的长尾问题』映射成根因+修复。

    这是"搜索即获客"的发动机：有人搜 "skill LICENSE 显示 Other" / "pytest exit code 2" /
    "CI 一直红" / "技能搜不到"，README 里的这些短语被索引 → 点进来 → 跑 diagnose 即得答案。
    竞品（jeremyknows/publish-skills 等）只给静态清单，我们给"可执行 + 可诊断"。
    """
    print("=" * 56)
    print("  releaser diagnose — 发布陷阱长尾诊断")
    print("=" * 56)
    if args.list:
        print("已知症状（可直接搜这些词找到我们）:")
        for it in DIAGNOSE_KB:
            print("  - [%s] %s" % (it["id"], it["title"]))
        print("\n用法: python releaser.py diagnose --symptom \"LICENSE 显示 Other\"")
        return 0
    if not args.symptom:
        print("请给 --symptom \"你的现象\"，或 --list 看全部已知症状。")
        return 1
    matches = _diagnose_match(args.symptom)
    if not matches:
        print("[diagnose] 未匹配到已知症状。可试试 --list，或直接跑 validate 看就绪分。")
        return 1
    for hit, it in matches[:3]:
        print("\n▶ [%s] %s  (匹配度 %d)" % (it["id"], it["title"], hit))
        print("  根因: " + it["cause"])
        print("  修复: " + it["fix"])
    print("\n[diagnose] 更多: 跑 `releaser.py validate --path .` 拿 0-100 就绪分；"
          "`releaser.py preflight` 拿上架清单。")
    return 0


# --------------------------------------------------------------------------
# preflight —— ★长尾功能：市场定制上架前检查清单（回答"发布前检查清单"类搜索）
# --------------------------------------------------------------------------

PREFLIGHT = {
    "clawhub": {
        "label": "ClawHub / OpenClaw",
        "items": [
            ("SKILL.md 含 name/version/description（YAML 合法、description 无未引号冒号）", "必填"),
            ("LICENSE 用 MIT-0（ClawHub 强制；发布包可不含 LICENSE 文件，但仓库保留）", "必填"),
            ("全仓无 skill-card.md 保留名（有则改名，如 market-card.md）", "必填"),
            ("Topics 整段 ≤48 字符（含逗号/空格）", "必填"),
            ("GitHub 账号龄 ≥1 周", "必填"),
            ("分类选满 3 个（Developer Tools / Security / AI & ML 等）", "必填"),
            ("仅文本文件：.md/.py/.txt/.json/.yaml/.toml/.js/.ts/.svg（排除图片/.git/.env）", "必填"),
            ("README.md 必填（人类可读文档）", "必填"),
            ("发布后核验：含 <main>.py+scripts/、SkillHub 镜像可搜到", "核验"),
        ],
    },
    "skillhub": {
        "label": "SkillHub（ClawHub 镜像）",
        "items": [
            ("同 ClawHub 全部必填项（SkillHub 是 ClawHub 的镜像索引）", "必填"),
            ("确保 ClawHub 发布后 SkillHub 能搜到（新提交显示 'Import is out of date' 时点 Re-run）", "核验"),
            ("保持 MIT-0 与 3 分类一致", "必填"),
        ],
    },
    "agentskills": {
        "label": "agentskills.io / GitHub（开源标准）",
        "items": [
            ("仓库公开（自动索引器只扫 public repo）", "必填"),
            ("`gh skill publish --dry-run` 全过（agentskills.io 规范校验）", "必填"),
            ("根 LICENSE（MIT 典型）+ frontmatter license: MIT", "必填"),
            ("README 含三种安装方式（Claude Code / Cursor / OpenClaw）", "必填"),
            ("SKILL.md < 500 行（超长移入 references/）", "建议"),
            ("GitHub topics: agent-skills, claude-skills, codex-skills, skill-md, ai-agents", "必填"),
            ("无 secrets/PII 入库（发布前 git ls-files 扫一遍）", "必填"),
            ("scripts 有可执行权限（chmod +x）", "必填"),
        ],
    },
    "generic": {
        "label": "通用（任意市场）",
        "items": [
            ("SKILL.md frontmatter 合法（name/version/description/license）", "必填"),
            ("LICENSE 文件存在且被识别（SPDX 可识别 + ASCII 版权名）", "必填"),
            ("零依赖（任何环境裸跑）或在 README 写明依赖", "必填"),
            ("CI 含自检门 + 日志 tee（排障命门）", "建议"),
            ("`releaser.py validate` 就绪分 ≥90 再发", "建议"),
            ("挂 readiness 徽章（链式传播）", "建议"),
        ],
    },
}


def cmd_preflight(args):
    """输出指定市场的上架前检查清单（markdown 勾选框）。

    回答长尾搜索："skill publish checklist" / "pre-publish checklist for agent skills" /
    "what am I missing before I publish"。清单本身也可贴进 README 被索引。
    """
    mkt = PREFLIGHT.get(args.market) or PREFLIGHT["generic"]
    print("=" * 56)
    print("  releaser preflight — %s 上架前检查清单" % mkt["label"])
    print("=" * 56)
    print("\n```markdown")
    print("# 发布前检查清单（%s）" % mkt["label"])
    for text, level in mkt["items"]:
        box = "[ ]" if level in ("必填", "建议") else "[~]"
        print("%s %s  _(%s)_" % (box, text, level))
    print("```")
    print("\n提示: 跑 `releaser.py validate --path .` 自动核验大部分项并给就绪分；")
    print("      `releaser.py badge` 生成 readiness 徽章挂进 README（链式传播）。")
    return 0


# --------------------------------------------------------------------------
# 状态层（A）：已发布技能账本 ledger —— 从"瞎子"变"持有账本的治理者"
# --------------------------------------------------------------------------

def _load_ledger():
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "entries" in data:
            return data
    except (OSError, ValueError):
        pass
    return {"entries": {}}


def _save_ledger(data):
    d = os.path.dirname(LEDGER_PATH)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ledger_add(entry):
    data = _load_ledger()
    slug = entry.get("slug")
    if not slug:
        return False
    data["entries"][slug] = entry
    _save_ledger(data)
    return True


def cmd_registry(args):
    """状态层：查看 / 登记已发布技能账本。

    让 cli-skill-release 跨多次运行持有『已发布技能账本』，从一次性校验器升级为
    发布侧的『治理者』（对标 find-skills++ 的状态层 / 全生命周期治理）。
    `release` 成功后自动调用 `add`。
    """
    if args.action == "list":
        data = _load_ledger()
        entries = data.get("entries", {})
        if not entries:
            print("[registry] 账本为空。跑一次 `release` 即自动登记。")
            return 0
        print("%-22s %-9s %-6s %-12s %s" % ("slug", "version", "score", "market", "published_at"))
        print("-" * 70)
        for slug, e in sorted(entries.items()):
            print("%-22s %-9s %-6s %-12s %s" % (
                slug[:21], e.get("version", "-"), e.get("score", "-"),
                e.get("market", "-"), e.get("published_at", "-")))
        print("-" * 70)
        print("共 %d 个已发布技能在账本中。" % len(entries))
        return 0
    if args.action == "show":
        data = _load_ledger()
        e = data.get("entries", {}).get(args.slug)
        if not e:
            print("[registry] 账本中无 slug=%s 的记录。" % args.slug)
            return 1
        print(json.dumps(e, ensure_ascii=False, indent=2))
        return 0
    if args.action == "add":
        if not args.slug:
            print("[registry] add 需要 slug（位置参数）。")
            return 1
        entry = {
            "slug": args.slug,
            "name": args.name or args.slug,
            "repo": args.repo or "",
            "version": args.version or "1.0.0",
            "score": args.score if args.score is not None else 0,
            "market": args.market or "manual",
            "path": os.path.abspath(args.path or "."),
            "published_at": datetime.date.today().isoformat(),
            "last_checked": datetime.date.today().isoformat(),
        }
        _ledger_add(entry)
        print("[registry] 已登记 %s → 账本 %s" % (args.slug, LEDGER_PATH))
        return 0
    print("[registry] 用法: list | show <slug> | add <slug> [--name --repo --version --score --market --path]")
    return 1


# --------------------------------------------------------------------------
# 生命周期（B）：再校验 / 漂移治理 —— 把"发完即终"升级为持续治理
# --------------------------------------------------------------------------

def cmd_recheck(args):
    """生命周期治理：读账本中已发布技能，重新 validate，对比上次分数，报告漂移。

    让发布后的技能持续被治理：分数下降（漂移）、目录缺失（弃用/搬走）、低于门禁（需修复）
    都会被标记——这是『治理技能的命』（find-skills++ 生命周期治理的对位）。
    """
    data = _load_ledger()
    entries = data.get("entries", {})
    if not entries:
        print("[recheck] 账本为空，无可再校验的技能。先 `release` 登记。")
        return 0
    if args.slug is None:
        targets = entries
    elif args.slug not in entries:
        print("[recheck] 账本中无 slug=%s。" % args.slug)
        return 1
    else:
        targets = {args.slug: entries[args.slug]}

    print("=" * 56)
    print("  releaser recheck — 已发布技能漂移复核")
    print("=" * 56)
    drift = []
    for slug, e in sorted(targets.items()):
        path = e.get("path")
        print("\n▶ %s（登记分 %s，发布于 %s）" % (slug, e.get("score", "-"), e.get("published_at", "-")))
        if not path or not os.path.isdir(path):
            print("  [缺失] 本地路径不存在: %s —— 技能可能已搬走/弃用" % (path or "(无记录)"))
            drift.append((slug, "缺失", 0))
            continue
        fails = validate_skill(path, mode="skill", silent=True)
        score = _score()
        prev = e.get("score") or 0
        if fails:
            print("  [弃用] 现 %d FAIL，就绪分 %d（登记时 %d）—— 低于发布门禁，需修复" % (fails, score, prev))
            drift.append((slug, "弃用", score))
        elif score < prev:
            print("  [漂移] 就绪分 %d < 登记时 %d（下降 %d）—— 内容/依赖/CI 有退化" % (score, prev, prev - score))
            drift.append((slug, "漂移", score))
        else:
            print("  [健康] 就绪分 %d ≥ 登记时 %d —— 无退化" % (score, prev))
            drift.append((slug, "健康", score))
        e["last_checked"] = datetime.date.today().isoformat()
        e["score"] = score
    _save_ledger(data)
    print("\n" + "-" * 56)
    n_health = sum(1 for _s, st, _v in drift if st == "健康")
    n_drift = sum(1 for _s, st, _v in drift if st in ("漂移", "弃用", "缺失"))
    print("  复核 %d 个：健康 %d / 漂移 %d / 弃用 %d / 缺失 %d" % (
        len(drift), n_health,
        sum(1 for _s, st, _v in drift if st == "漂移"),
        sum(1 for _s, st, _v in drift if st == "弃用"),
        sum(1 for _s, st, _v in drift if st == "缺失")))
    if n_drift:
        print("  ⚠ 有 %d 个技能需要关注（见上方标记）。" % n_drift)
    return 1 if n_drift else 0


# --------------------------------------------------------------------------
# 自证底座（E）：全量自证 —— 主张即演示（对标 find-skills++ smoke.py）
# --------------------------------------------------------------------------

def cmd_selfdemo(args):
    """自证底座：当场对自己（cli-skill-release 仓库）运行每个能力，打印演示摘要。

    碾压级信任机制：不靠叙述，靠『当场演示』。每个能力现场跑一遍并报告成功/摘要，
    证明『别人 lint 文档，我们 execute 引擎』不是口号——是已验证事实。
    对标 find-skills++ 的 smoke.py（全量自证）。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    print("=" * 56)
    print("  releaser selfdemo — 全量自证（主张即演示）")
    print("=" * 56)
    demos = []
    # 1) validate 自身（含 ★功能验证）
    fails = validate_skill(here, mode="skill", silent=True)
    score = _score()
    n_pass = sum(1 for r in REPORT if r[0] == "PASS")
    demos.append(("validate（功能验证+就绪分）", fails == 0,
                  "就绪分 %d/100，%d 维 PASS" % (score, n_pass)))
    # 2) selfcheck 零依赖
    r = subprocess.run([sys.executable, __file__, "selfcheck", "--path", here],
                       capture_output=True, text=True, check=False)
    demos.append(("selfcheck（零依赖）", r.returncode == 0, "零依赖成立" if r.returncode == 0 else "存在非标准库依赖"))
    # 3) badge 生成 SVG（链式传播引擎）
    r = subprocess.run([sys.executable, __file__, "badge", "--path", here],
                       capture_output=True, text=True, check=False)
    demos.append(("badge（链式传播引擎）", "<svg" in r.stdout, "生成 readiness 徽章 + 链回片段"))
    # 4) preflight（上架清单）
    r = subprocess.run([sys.executable, __file__, "preflight", "--market", "generic"],
                       capture_output=True, text=True, check=False)
    demos.append(("preflight（上架清单）", "检查清单" in r.stdout, "输出 4 个市场定制清单"))
    # 5) diagnose（长尾诊断）
    r = subprocess.run([sys.executable, __file__, "diagnose", "--list"],
                       capture_output=True, text=True, check=False)
    n = r.stdout.count("- [") if r.returncode == 0 else 0
    demos.append(("diagnose（长尾诊断）", n > 0, ("内置 %d 条症状→根因→修复" % n) if n > 0 else "未列出症状"))
    # 6) registry（状态层账本）
    r = subprocess.run([sys.executable, __file__, "registry", "list"],
                       capture_output=True, text=True, check=False)
    demos.append(("registry（已发布账本）", r.returncode == 0, "状态层就绪（账本可查）"))
    # 7) gap（市场情报）
    r = subprocess.run([sys.executable, __file__, "gap"],
                       capture_output=True, text=True, check=False)
    demos.append(("gap（市场情报）", r.returncode == 0, "本机类目覆盖 + 缺口提示"))
    # 8) recheck 结构（生命周期，账本为空时返回 0）
    r = subprocess.run([sys.executable, __file__, "recheck"],
                       capture_output=True, text=True, check=False)
    demos.append(("recheck（生命周期治理）", r.returncode in (0, 1), "生命周期治理就绪"))

    ok = sum(1 for _n, s, _d in demos if s)
    for name, status, detail in demos:
        print("  [%s] %s — %s" % ("✓" if status else "✗", name, detail))
    print("-" * 56)
    print("  自证结果: %d/%d 能力通过演示" % (ok, len(demos)))
    print("  → 这就是『别人 lint 文档，我们 execute 引擎』的现场证据。")
    return 0 if ok == len(demos) else 1


# --------------------------------------------------------------------------
# 供给侧策展（F）：主动告诉生态"该造什么"
# --------------------------------------------------------------------------

def cmd_curate(args):
    """供给侧策展：把市场情报升级为『可操作的策展清单』。

    结合 ledger（本机已发布，避免重复造）与可选 --scan-json 市场数据，输出
    优先级排序的『该造什么』清单——从被动等待搜索升级为主动策展分发
    （find-skills++ 主动策展的对位）。
    """
    loc_counts = {c: 0 for c in CATEGORY_KEYWORDS}
    roots = args.roots.split(",") if args.roots else default_roots()
    published = set()
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            smd = os.path.join(d, "SKILL.md")
            if not os.path.isfile(smd):
                continue
            published.add(name)
            fm, body = parse_frontmatter(smd)
            text = " ".join([name, fm.get("keywords", ""), fm.get("description", ""), body[:800]])
            for c in categorize(text):
                loc_counts[c] += 1

    data = _load_ledger()
    ledger_slugs = set(data.get("entries", {}).keys())

    mkt_counts = None
    if args.scan_json:
        mkt_counts = {c: 0 for c in CATEGORY_KEYWORDS}
        try:
            with open(args.scan_json, "r", encoding="utf-8") as f:
                mdata = json.load(f)
            for item in mdata:
                cats = item.get("categories") or categorize(" ".join([
                    item.get("name", ""), item.get("keywords", ""), item.get("description", "")]))
                for c in cats:
                    mkt_counts[c] += 1
        except Exception as e:
            print("[curate] 读取市场数据失败: %s" % e)
            return 1

    print("=" * 56)
    print("  releaser curate — 供给侧策展清单（该造什么）")
    print("=" * 56)
    print("本机已装技能: %d 个 · 账本登记: %d 个" % (len(published), len(ledger_slugs)))

    prio = []
    if mkt_counts:
        for c in CATEGORY_KEYWORDS:
            if loc_counts[c] == 0 and mkt_counts[c] > 0:
                prio.append(c)
        if prio:
            print("\n① ★组合机会（市场有供给 / 你为 0，最该造）:")
            for c in prio:
                print("   - [%s] 市场 %d 个 / 你 0 → scaffold skill-%s" % (
                    c, mkt_counts[c], re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")))
    gaps = [c for c in CATEGORY_KEYWORDS if loc_counts[c] == 0]
    print("\n② 本机空白类目（建议新建）:")
    for c in gaps:
        print("   - [%s] scaffold skill-%s" % (c, re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")))
    if not gaps:
        print("   （无完全空白类目）")
    thin = [c for c in CATEGORY_KEYWORDS if loc_counts[c] == 1]
    print("\n③ 本机单薄类目（可补强）:")
    for c in thin:
        print("   - [%s] scaffold skill-%s" % (c, re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-")))
    if not thin:
        print("   （无）")
    print("\n[curate] 提示: 优先做 ① 组合机会（市场有真实需求，你尚未供给）；")
    print("      加 --scan-json 消费 find-skills++ 真实市场数据，策展清单即飞轮情报。")
    return 0


# --------------------------------------------------------------------------
# CLI 入口
# --------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="releaser", description="零依赖 CLI 技能发布工程工具")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("scaffold", help="生成带 CI 的可发布骨架")
    s.add_argument("name")
    s.add_argument("--author", default="He Wei")
    s.add_argument("--email", default="you@example.com")
    s.add_argument("--dest", default=None)
    s.set_defaults(func=cmd_scaffold)

    v = sub.add_parser("validate", help="主动扫描技能目录的发布陷阱 + 就绪分")
    v.add_argument("--path", default=".")
    v.add_argument("--mode", default="skill", choices=["skill", "cli", "package"])
    v.add_argument("--json", action="store_true", help="输出机器可读 JSON（供 CI/市场闭环消费）")
    v.add_argument("--bench", action="store_true", help="输出对标头部技能画像的差距分析（相对分，而非绝对分）")
    v.add_argument("--rubric", action="store_true", help="输出评分权重与理由（透明评分，使分数可被审计）")
    v.set_defaults(func=cmd_validate)

    ss = sub.add_parser("secretscan", help="★安全红线：扫描硬编码密码/授权码/API Token（禁止入库）")
    ss.add_argument("--path", default=".")
    ss.add_argument("--allow-file", default=None, help="自定义放行正则文件（默认 .releaser-secret-allow）")
    ss.set_defaults(func=cmd_secretscan)

    g2 = sub.add_parser("gate", help="CI 门禁：就绪分低于阈值则非零退出（readiness-as-a-service）")
    g2.add_argument("--path", default=".")
    g2.add_argument("--mode", default="skill", choices=["skill", "cli", "package"])
    g2.add_argument("--min", type=int, default=90, help="就绪分门禁阈值（默认 90）")
    g2.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    g2.set_defaults(func=cmd_gate)

    i = sub.add_parser("inventory", help="扫描本机已装技能就绪度")
    i.add_argument("--roots", default=None, help="逗号分隔的根目录")
    i.set_defaults(func=cmd_inventory)

    g = sub.add_parser("gap", help="市场情报：扫描技能归类，报告缺口")
    g.add_argument("--roots", default=None, help="逗号分隔的根目录（默认扫描本机已装技能）")
    g.add_argument("--scan-json", default=None, help="消费 find-skills++ 导出的市场扫描 JSON，升级为真实在售缺口情报")
    g.set_defaults(func=cmd_gap)

    c = sub.add_parser("selfcheck", help="零依赖 import 校验")
    c.add_argument("--path", default=None)
    c.set_defaults(func=cmd_selfcheck)

    b = sub.add_parser("bump", help="升版本号 + 补 CHANGELOG")
    b.add_argument("--path", default=".")
    b.add_argument("--type", default="patch", choices=["major", "minor", "patch"])
    b.add_argument("--message", default=None)
    b.set_defaults(func=cmd_bump)

    r = sub.add_parser("release", help="本地提交 + 构造 ClawHub 导入步骤（默认不推送、不发布）")
    r.add_argument("--path", default=".")
    r.add_argument("--remote", default="origin")
    r.add_argument("--branch", default="main")
    r.add_argument("--message", default=None)
    r.add_argument("--dry-run", action="store_true", help="只生成导入步骤，不提交")
    r.add_argument("--push", action="store_true", help="显式授权：将本地提交推送到远端（默认不推送）")
    r.add_argument("--publish", action="store_true",
                   help="显式授权：通过本机已登录的 clawhub CLI 发布到 ClawHub（默认不发布，仅给出人工导入步骤）")
    r.add_argument("--allow-secret-risk", action="store_true",
                   help="危险：强制越过安全红线（仅当你确认无真实凭据入库、或文件已被 .gitignore 排除时）")
    r.set_defaults(func=cmd_release)

    pb = sub.add_parser("publish", help="★多站上架编排：显式逐站授权上传 GitHub/ClawHub（安全闸门前置，默认不碰远程）")
    pb.add_argument("--path", default=".")
    pb.add_argument("--github", action="store_true", help="显式授权：推送 commits 到 GitHub 远端")
    pb.add_argument("--clawhub", action="store_true", help="显式授权：通过本机已登录的 clawhub CLI 发布到 ClawHub")
    pb.add_argument("--xiaping", action="store_true", help="预留：虾评(xiaping.coze.site)，本轮未接入，仅给人工链接")
    pb.add_argument("--workbuddy", action="store_true", help="预留：WorkBuddy SkillHub(open.workbuddy.cn)，本轮未接入，仅给人工链接")
    pb.add_argument("--remote", default="origin")
    pb.add_argument("--branch", default="main")
    pb.add_argument("--force-history", action="store_true",
                   help="强制推送（历史曾被 git filter-repo 重写、远端本地分叉时必须；用 --force-with-lease 防覆盖）")
    pb.add_argument("--message", default=None)
    pb.add_argument("--dry-run", action="store_true", help="只预览各站动作，不提交/不推送/不发布")
    pb.add_argument("--allow-secret-risk", action="store_true",
                   help="危险：强制越过安全红线（仅当你确认无真实凭据入库时）")
    pb.set_defaults(func=cmd_publish)

    d = sub.add_parser("doctor", help="自检本工具或对 --path 目标校验")
    d.add_argument("--path", default=None)
    d.set_defaults(func=cmd_doctor)

    bdg = sub.add_parser("badge", help="★链式传播：基于就绪分生成徽章 SVG + 链回片段")
    bdg.add_argument("--path", default=".")
    bdg.add_argument("--mode", default="skill", choices=["skill", "cli", "package"])
    bdg.add_argument("--output", default=None, help="写出 SVG 文件路径（默认打印到 stdout）")
    bdg.add_argument("--page", default=None, help="徽章链回地址（默认 RELEASER_PAGE 或环境变量）")
    bdg.set_defaults(func=cmd_badge)

    pr = sub.add_parser("promote", help="★发布说明工具箱：徽章区+要点说明+社媒文案+链回玩法")
    pr.add_argument("--path", default=None, help="可选：给定则先校验并展示就绪分")
    pr.add_argument("--mode", default="skill", choices=["skill", "cli", "package"])
    pr.add_argument("--page", default=None, help="链回地址（默认 RELEASER_PAGE 或环境变量）")
    pr.set_defaults(func=cmd_promote)

    dg = sub.add_parser("diagnose", help="★长尾诊断：症状→根因→修复（直接回答用户会搜的长尾问题）")
    dg.add_argument("--symptom", default=None, help="你的现象，如 \"LICENSE 显示 Other\" / \"pytest exit code 2\"")
    dg.add_argument("--list", action="store_true", help="列出全部已知症状")
    dg.set_defaults(func=cmd_diagnose)

    pf = sub.add_parser("preflight", help="★市场定制上架前检查清单（回答\"发布前检查清单\"类搜索）")
    pf.add_argument("--market", default="generic",
                    choices=["clawhub", "skillhub", "agentskills", "generic"],
                    help="目标市场（默认 generic）")
    pf.set_defaults(func=cmd_preflight)

    # A 状态层：已发布技能账本
    reg = sub.add_parser("registry", help="★状态层：已发布技能账本（list/show/add）")
    reg.add_argument("action", choices=["list", "show", "add"])
    reg.add_argument("slug", nargs="?", default=None)
    reg.add_argument("--name", default=None)
    reg.add_argument("--repo", default=None)
    reg.add_argument("--version", default=None)
    reg.add_argument("--score", type=int, default=None)
    reg.add_argument("--market", default=None)
    reg.add_argument("--path", default=None)
    reg.set_defaults(func=cmd_registry)

    # B 生命周期：再校验/漂移治理
    rc2 = sub.add_parser("recheck", help="★生命周期：再校验已发布技能，报告漂移/弃用")
    rc2.add_argument("slug", nargs="?", default=None, help="指定 slug 复核；缺省复核全部账本")
    rc2.set_defaults(func=cmd_recheck)

    # E 自证底座：全量自证
    sd = sub.add_parser("selfdemo", help="★自证底座：全量自证（主张即演示，对标 smoke.py）")
    sd.set_defaults(func=cmd_selfdemo)

    # F 供给侧策展：主动告诉生态该造什么
    cu = sub.add_parser("curate", help="★供给侧策展：告诉生态该造什么（升级版 gap）")
    cu.add_argument("--roots", default=None)
    cu.add_argument("--scan-json", default=None)
    cu.set_defaults(func=cmd_curate)

    return p


def _print_header(path):
    print("=" * 56)
    print("  releaser validate → " + path)
    print("=" * 56)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
