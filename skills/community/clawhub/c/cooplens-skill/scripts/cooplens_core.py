#!/usr/bin/env python3
"""Local helper checks and converters for CoopLens.

The script intentionally uses only the Python standard library. It performs
local candidate lookup, report-policy checks, simple source-link checks and
Markdown-to-mobile-HTML rendering. It does not perform hidden network activity
except when the user explicitly runs link-check on a report containing URLs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
import os
import re
import sys
import tempfile
import textwrap
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Iterable
try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - fallback for older Python runtimes
    ZoneInfo = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "project_major_index.json"
RANKINGS_PATH = ROOT / "data" / "rankings_local_compact.json"
DISCLAIMER = "重要声明：CoopLens Skill 产出的内容由 AI 生成，真实性需要使用者自行核实，不代表任何官方意见，不能作为任何决策依据或参考。"

HTML_GENERATOR_NAME = "CoopLensStaticHTML"
HTML_GENERATOR_META = f'<meta name="generator" content="{HTML_GENERATOR_NAME}">'
ASCII_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,80}$")
SAFE_EXTERNAL_HREF_PATTERN = re.compile(r"^https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]+$")
BAD_HREF_TRAILING = "。．，,；;：:、！!？?）)]】}》>"
HTML_REBUILD_MAX_ATTEMPTS = 6
HTML_VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
HTML_REQUIRED_NESTING = ["html", "head", "body", "main"]

REQUIRED_FILES = [
    "SKILL.md",
    "license.txt",
    "agents/openai.yaml",
    "data/project_major_index.json",
    "data/rankings_local_compact.json",
    "data/rankings_semantic.md",
    "prompts/report_modules.md",
    "references/core_workflow.md",
    "references/source_methods.md",
    "references/live_rank_estimation.md",
    "references/rank_estimation_workflow.md",
    "references/rank_statistical_estimation.md",
    "references/cscse_authentication.md",
    "references/overseas_living_cost.md",
    "references/parent_manual_distilled.md",
    "references/recommendation_rubric.md",
    "references/public_platform_discussion.md",
    "references/schema.md",
    "scripts/cooplens_core.py",
]

FORBIDDEN_TREE_NAMES = {
    "imports",
    "mcp",
    "app",
    "runtime_indexes",
    "generated_reports",
    "local_knowledge_sources",
    "__pycache__",
}

WX = "微" + "信"
XHS = "小" + "红" + "书"
ZH = "知" + "乎"
TB = "贴" + "吧"
WB = "微" + "博"
DY = "抖" + "音"
BILI = "B" + "站"
FORBIDDEN_PUBLIC_REPORT_TERMS = [
    WX,
    WX + "公众",
    "mp." + "wei" + "xin" + ".qq.com",
    XHS,
    "Xiao" + "hong" + "shu",
    ZH,
    TB,
    WB,
    DY,
    BILI,
    "来源" + "平台",
    "平台" + "名",
    "检索" + "平台",
    "来源分组",
    "渠道" + "类别",
    "渠道" + "状态",
    "账号名",
    "用户名",
    "用户说",
    "网友说",
    "某网友",
    "某博主",
    "帖子标题",
    "原帖",
    "原文评论",
    "截图",
    "头像",
    "主页",
    "个人主页",
    "handle",
]

BLANKET_SOURCE_CLAIMS = [
    "所有数据均来自公开可访问页面",
    "所有信息均来自公开渠道",
    "全部数据已核实",
    "所有数据都有官方来源",
    "所有数据均已核验",
    "均来自公开可查",
    "本报告" + "所有数据",
    "所有" + "数字结论",
    "权威" + "渠道",
    "官方" + "来源链接",
    "均来自" + "各高校官方网站",
]

BLANKET_SOURCE_CLAIM_PATTERNS = [
    re.compile(r"数据来源说明[:：][^\n。]{0,160}(所有|全部|均来自|权威渠道|官方来源|可验证|已核验)"),
    re.compile(r"(本报告|本文|本分析)[^\n。]{0,40}(所有|全部)[^\n。]{0,40}(数据|信息|数字结论)[^\n。]{0,80}(来自|附有|已核验|可验证|官方|权威)"),
    re.compile(r"所有(数据|信息|数字结论)[^\n。]{0,80}(来自|附有|已核验|可验证|官方|权威)"),
]

DOCUMENT_EXPORT_TERMS = ["P" + "DF", "p" + "df"]
OLD_PRODUCT_TERMS = ["1"+".0"+".12", "1"+".0"+".13", "修改"+"日志", "change"+"log", "rel"+"ease note", "旧"+"包", "升"+"级"+"说明"]
OLD_STARTUP_EXAMPLE = "南京" + "师范" + "大学" + " + " + "麦" + "考" + "瑞" + "大学" + " + " + "计算机科学与技术" + " + " + "江苏"
OLD_RANK_STARTUP_EXAMPLE = "4，广东，物理类，约3" + "万位，港中深理工实验班今年能不能冲"
OLD_RANK_STARTUP_EXAMPLE_1500 = "4，广东，物理类，约15" + "00位，港中深理工实验班今年能不能冲"
OLD_RANK_STARTUP_EXAMPLE_1200 = "4，广东，物理类，约12" + "00位，港中深理工实验班今年能不能冲"
REQUIRED_MOBILE_STARTUP_SUFFIX = "必须确保生成的静态页面能在手机上正常显示"
REQUIRED_STARTUP_LINES = [
    "你可以这样发：1，香港中文大学(深圳)+理工实验班+广东，必须确保生成的静态页面能在手机上正常显示",
    "你可以这样发：2，项目A vs 项目B vs 项目C，所在省份/分数或位次，必须确保生成的静态页面能在手机上正常显示",
    "你可以这样发：3，浙江，物理类，约2.5万位，计算机或人工智能方向，预算约10万每年，必须确保生成的静态页面能在手机上正常显示",
    "你可以这样发：4，广东，物理类，约 1200 位，港中深理科实验班今年能不能冲，必须确保生成的静态页面能在手机上正常显示",
]
REQUIRED_STARTUP_FALLBACK_COMMAND = "如果生成页面失败，请输入如此命令：基于 markdown 文件，生成用户友好的美观的适合手机阅读的静态页面，不能添加新的内容或图片，需要严格按照 markdown 文件的内容生成。"

PLATFORM_ARTIFACT_NAME_TERMS = [
    "豆" + "包",
    "在" + "线" + "工具",
    "网" + "页",
    "web" + "page",
    "browser",
    "internet",
    "search" + "tool",
    "online" + "tool",
    "tool" + "output",
    "chat" + "report",
]
GENERIC_ARTIFACT_STEMS = {"report", "analysis", "output", "result", "index", "page", "html", "markdown", "cooplens"}

OLD_CONVERSATION_STARTERS = [
    "对比" + "南京" + "师范" + "大学" + "麦" + "考" + "瑞" + "项目" + "和" + "杭州" + "电子" + "科技" + "大学" + "圣" + "光" + "机" + "项目",
    "江西" + "理科" + "2" + "万" + "位次" + "计算机" + "方向" + "预算" + "10" + "万" + "年" + "有哪些" + "中外" + "合作" + "项目" + "可选",
]

URL_PATTERN = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]+")
MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
NUMERIC_PATTERN = re.compile(
    r"(?<![\w/])约?\d+(?:\.\d+)?(?:[-–—~至]\d+(?:\.\d+)?)?\s*(?:分|位|名|人|个|项|所|年|万元|元|%|％|万|亿|次|门|学分|/年)?"
)

RANK_REASONING_FIELDS = ["输入数据", "招生批次", "院校专业组", "基线选择", "差值样本", "调整项", "计算过程", "置信度", "推翻条件"]
BATCH_DISTINCTION_TRIGGER_TERMS = ["招生计划", "招生人数", "计划数", "分数线", "投档线", "专业线", "最低分", "最低位次", "批次控制线", "线差", "位差", "位次预估", "冲/稳/保", "候选排序"]
BATCH_DISTINCTION_GROUPS = {
    "admission batch field": ["招生批次", "批次"],
    "major group field": ["院校专业组", "专业组"],
    "plan type field": ["计划类型", "普通计划", "中外合作单列", "综合评价", "专项计划"],
    "same-batch comparison boundary": ["同招生批次", "同批次", "批次口径", "口径一致"],
    "multiple-batch separation": ["不同批次不得合并", "分批次", "不同批次", "多批次", "拆成多条", "批次未核到"],
}
CURRENT_ADMISSION_STATUS_TRIGGER_TERMS = ["招生计划", "招生简章", "招生章程", "专业目录", "候选", "位次预估", "冲/稳/保", "推荐", "排序", "中外合作"]
CURRENT_ADMISSION_STATUS_GROUPS = {
    "admission status module": ["当年是否招生", "招生状态", "是否仍招生", "是否继续招生", "当年是否招生核验"],
    "current-year plan/catalog": ["当年招生计划", "今年招生计划", "current-year招生计划", "当年专业目录", "省级专业目录", "目标省专业目录", "省考试院专业目录"],
    "school or regulator source": ["学校官网", "本科招生网", "招生办", "教育部中外合作办学监管工作信息平台", "CRS", "教育部官网", "教育部"],
    "explicit status label": ["继续招生", "仍在招生", "当年招生", "正常招生", "未在当年招生计划中", "当年停招", "停招", "暂停招生", "未核到当年招生", "待学校书面确认"],
    "decision effect": ["进入位次预估", "不进入位次预估", "不做本年位次估计", "不参与排序", "仅关注/待核验", "暂不建议填报"],
    "manual confirmation": ["人工确认", "打开链接", "核对", "书面确认"],
}
CURRENT_ADMISSION_STOP_TERMS = ["未在当年招生计划中", "当年停招", "停招", "暂停招生", "不招生", "停止招生", "未核到当年招生"]
CURRENT_ADMISSION_STOP_HANDLING_TERMS = ["不进入位次预估", "不做本年位次估计", "不参与排序", "仅关注/待核验", "暂不建议填报", "不建议填报"]


CRITICAL_DATA_TERMS = [
    "招生人数", "招生计划人数", "招生计划", "计划数", "计划人数",
    "分数线", "投档线", "录取线", "最低分", "专业线", "最低位次",
    "分位数", "排位", "位次", "升学率", "深造率", "出国率", "境外升学率",
    "就业率", "毕业去向落实率", "去向落实率", "保研率", "推免率", "保研", "推免",
]
CRITICAL_DATA_UNKNOWN_TERMS = [
    "未知", "未核到", "未找到", "无法确认", "未公开", "无公开", "待学校书面确认",
    "未核到可打开且内容对应", "不写数字", "没有可验证来源", "验证不了",
]
CRITICAL_VALUE_PATTERN = re.compile(
    r"(?P<approx>约)?\d[\d,]*(?:\.\d+)?(?:\s*[万千亿])?(?:\s*[-–—~至]\s*(?:约)?\d[\d,]*(?:\.\d+)?(?:\s*[万千亿])?)?\s*(?:人|名|分|位|%|％)"
)
CRITICAL_SOURCE_KEYWORDS = {
    "招生": ["招生计划", "计划数", "计划人数", "招生人数", "专业目录", "招生专业"],
    "分数": ["分数线", "投档线", "录取线", "最低分", "最低位次", "位次", "一分一段"],
    "位次": ["位次", "最低位次", "排位", "分位", "一分一段", "投档"],
    "升学": ["升学", "深造", "出国", "就业质量", "毕业去向", "质量报告"],
    "出国": ["出国", "境外升学", "海外升学", "毕业去向", "质量报告"],
    "就业": ["就业率", "毕业去向落实率", "就业质量", "毕业去向", "质量报告"],
    "保研": ["保研", "推免", "推荐免试", "免试攻读", "名额", "办法"],
}
PERSONALIZATION_GROUPS = {
    "家庭预算/费用压力": ["家庭", "预算", "费用", "四年总投入", "学费"],
    "出国偏好": ["出国", "境外", "海外", "不愿出国", "愿意出国"],
    "未来路径": ["未来路径", "保研", "考研", "就业", "考公", "国企", "海外硕士"],
    "学习承受度": ["英语", "GPA", "毕业压力", "学习压力", "全英文"],
}

CSCSE_GROUPS = {
    "module": ["留服认证路径与风险", "留服认证", "中留服", "教育部留学服务中心"],
    "authentication object": ["认证对象", "外方学位", "境外文凭", "学位名称"],
    "authentication path": ["认证路径", "学历学位认证", "服务大厅", "申请材料", "认证流程"],
    "mode and overseas record": ["项目模式", "4+0", "2+2", "3+1", "境外学习记录", "出入境记录"],
    "plan status and domestic backup": ["计划内", "计划外", "国内学籍", "国内毕业证", "国内学位证", "学信网"],
    "result boundary": ["认证结果预期", "传统海归", "留学生待遇", "不能承诺", "以正式认证结果为准"],
    "risk and questions": ["风险等级", "待核验", "书面确认", "家长书面提问", "近三届"],
}

CSCSE_FORBIDDEN_CLAIMS = ["保证认证", "一定能认证", "包认证", "等同海归", "必然认证", "100%认证"]

RANK_WORKFLOW_TERMS = {
    "rank chapter": ["位次预估：统计、分析与预测", "位次预估"],
    "rank conclusion first": ["位次预估结论先行", "参考区间", "冲/稳/保"],
    "rank disclaimer": ["位次预估重要声明", DISCLAIMER],
    "statistics first": ["可验证数据统计", "先统计", "数据统计"],
    "analysis second": ["位差与线差分析", "再分析", "绝对位差", "相对位差", "线差"],
    "prediction third": ["本年位次估计", "再预测", "参考区间", "门槛偏高", "门槛偏宽"],
    "manual confirmation": ["人工确认", "人工核对", "打开链接核对"],
    "quality grade": ["质量等级", "A级", "B级", "C级", "D级"],
    "source links": ["http://", "https://", "来源链接"],
    "batch separation": ["招生批次", "院校专业组", "同招生批次", "批次未核到", "不同批次不得合并", "分批次"],
}

RECOMMENDATION_SPLIT_TERMS = {
    "personal fit rating": ["个性化推荐度评价（学生/家庭适配）"],
    "project strength rating": ["项目综合实力推荐度评价（项目综合实力角度）"],
    "student/family basis": ["学生情况", "学生分数", "位次", "家庭预算", "出国偏好", "未来路径", "英语", "GPA", "城市", "校区"],
    "project basis": ["项目综合实力", "监管身份", "证书", "留服", "外方", "专业", "费用", "毕业成果", "风险"],
    "conflict": ["两者冲突", "冲突说明", "项目综合实力强", "但不适合", "项目综合实力一般", "适配"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def result(ok: bool, errors: list[str] | None = None, warnings: list[str] | None = None, **extra: Any) -> int:
    payload: dict[str, Any] = {"ok": ok}
    if errors:
        payload["errors"] = errors
    if warnings:
        payload["warnings"] = warnings
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def normalize(s: str) -> str:
    return re.sub(r"\s+", "", str(s).lower())


def iter_text_files() -> Iterable[Path]:
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".py", ".json"}:
            yield p


def cmd_runtime_date(args: argparse.Namespace) -> int:
    tz = ZoneInfo("Asia/Tokyo") if ZoneInfo else dt.timezone(dt.timedelta(hours=9), name="Asia/Tokyo")
    now = dt.datetime.now(tz)
    timezone_label = "Asia/Tokyo"
    payload = {
        "current_date": now.strftime("%Y-%m-%d"),
        "current_year": now.year,
        "timezone": timezone_label,
        "checked_at": now.isoformat(timespec="seconds"),
        "date_source_tool": "local_system_datetime_asia_tokyo",
        "display_line": f"检索执行日期：{now.year}年{now.month:02d}月{now.day:02d}日（时区：{timezone_label}；通过工具获取）",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for p in ROOT.rglob("*"):
        if p.name in FORBIDDEN_TREE_NAMES:
            errors.append(f"forbidden path present: {p.relative_to(ROOT)}")

    for rel in ["SKILL.md", "references/core_workflow.md", "prompts/report_modules.md"]:
        text = read_text(ROOT / rel) if (ROOT / rel).exists() else ""
        for line in REQUIRED_STARTUP_LINES:
            if line not in text:
                errors.append(f"required clean startup line missing in {rel}: {line}")
        if REQUIRED_STARTUP_FALLBACK_COMMAND not in text:
            errors.append(f"startup fallback command missing in {rel}")
        if OLD_STARTUP_EXAMPLE in text:
            errors.append(f"old startup example present in {rel}")
        if OLD_RANK_STARTUP_EXAMPLE in text or OLD_RANK_STARTUP_EXAMPLE_1500 in text or OLD_RANK_STARTUP_EXAMPLE_1200 in text:
            errors.append(f"old rank-estimation startup example present in {rel}")
        for startup_line in re.findall(r"你可以这样发：[^\n]+", text):
            if REQUIRED_MOBILE_STARTUP_SUFFIX not in startup_line:
                errors.append(f"startup line lacks mobile-static-page suffix in {rel}: {startup_line}")
        normalized_text = normalize(text)
        for starter in OLD_CONVERSATION_STARTERS:
            if normalize(starter) in normalized_text:
                errors.append(f"old conversation starter present in {rel}")

    for p in iter_text_files():
        rel = str(p.relative_to(ROOT))
        text = read_text(p)
        if rel.startswith("data/"):
            scan_text = text.replace("QS World University Rankings", "QS World University Rankings")
        else:
            scan_text = text
        for term in OLD_PRODUCT_TERMS:
            if term.lower() in scan_text.lower():
                errors.append(f"old product/log residue `{term}` in {rel}")
        if any(term in scan_text for term in DOCUMENT_EXPORT_TERMS):
            errors.append(f"document-export residue found in {rel}")

    try:
        idx = load_json(INDEX_PATH)
        if "rows" not in idx or not isinstance(idx["rows"], list):
            errors.append("project_major_index.json must contain rows list")
    except Exception as exc:
        errors.append(f"project_major_index.json invalid: {exc}")

    try:
        ranks = load_json(RANKINGS_PATH)
        if not isinstance(ranks, dict):
            errors.append("rankings_local_compact.json must be an object")
    except Exception as exc:
        errors.append(f"rankings_local_compact.json invalid: {exc}")

    required_text_terms = {
        "references/rank_estimation_workflow.md": ["先统计", "再分析", "再预测", "人工确认", "黑底红字", "计算过程", "不得另写位次预估专用声明", "招生批次拆分规则", "批次未核到", "当年是否招生核验", "停招"],
        "references/rank_statistical_estimation.md": ["先统计", "再分析", "再预测", "人工确认", "批次口径先行", "不同批次"],
        "references/recommendation_rubric.md": ["个性化推荐度评价（学生/家庭适配）", "项目综合实力推荐度评价（项目综合实力角度）"],
        "prompts/report_modules.md": ["critical-data-source-check", "pure-report-file-check", "strict-final-delivery-check", "个性化推荐度评价（学生/家庭适配）", "项目综合实力推荐度评价（项目综合实力角度）", "位次预估：统计、分析与预测", "位次预估结论先行", "safe-html-build", "html-syntax-check", "HTML 语法校验", "HTML 渲染失败原因", "function3-delivery-gate-check", "黑底红字", "最重要建议", "附录：重要声明与人工确认提醒", "交付文件下载链接", "下载链接", "不得给 ZIP/压缩包", "招生批次与专业组展示模板", "同一项目多批次时不得合并", "当年是否招生核验展示模板", "未在当年招生计划中"],
        "references/source_methods.md": ["QS World University Rankings 2027", "人工确认", "Overseas-city living-cost", "招生批次与专业组口径规则", "批次未核到", "不同招生批次", "当年是否招生入场闸门", "未在当年招生计划中", "关键数据硬闸门", "招生人数、分数线、分位数、升学率、出国率、就业率、保研率"],
        "references/schema.md": ["strict-final-delivery-check", "pure-report-file-check", "critical-data-source-check", "exactly_two_report_download_targets", "ZIP 下载", "critical_data_source_gate"],
        "references/overseas_living_cost.md": ["境外城市生活成本", "外方大学所在城市", "年度预算差额", "人工确认"],
        "references/core_workflow.md": ["strict-final-delivery-check", "pure-report-file-check", "critical-data-source-check", "HTML 结果缺失处理", "function3-delivery-gate-check", "最终交付闸门", "html-syntax-check", "不通过就重新生成", "基于 markdown 文件", "重要声明硬规则", "最重要建议", "附录：重要声明与人工确认提醒", "交付文件下载链接", "下载链接", "压缩包", "重做", "招生批次口径锁定", "不同批次不得合并", "当年是否招生入场闸门", "当年停招", "找不到就写未知"],
        "SKILL.md": ["1.0.15", "strict-final-delivery-check", "pure-report-file-check", "critical-data-source-check", "function3-delivery-gate-check", "`.html`", "html-syntax-check", "不通过就重新生成", "Strict important-statement policy", "附录：重要声明与人工确认提醒", "交付文件下载链接", "下载链接", "ZIP/archive", "pure Markdown", "招生批次严格区分规则", "批次未核到", "不得把招生人数", "当年是否招生入场闸门", "未在当年招生计划中", "关键数据硬闸门", "找不到就写未知"],
    }
    for rel, terms in required_text_terms.items():
        f = ROOT / rel
        body = read_text(f) if f.exists() else ""
        for term in terms:
            if term not in body:
                errors.append(f"required policy term `{term}` missing in {rel}")

    strict_delivery_good = """### 交付文件下载链接

- 静态网页（HTML）下载链接：[下载/打开 广东港中深理科试验班位次预估报告.html](sandbox:/mnt/data/广东港中深理科试验班位次预估报告.html)
- Markdown 文件下载链接：[下载 广东港中深理科试验班位次预估报告.md](sandbox:/mnt/data/广东港中深理科试验班位次预估报告.md)
"""
    good_delivery_errors = strict_pure_html_md_delivery_errors(strict_delivery_good)
    if good_delivery_errors:
        errors.append("strict-final-delivery self-test should pass pure .html/.md links: " + "; ".join(good_delivery_errors[:3]))
    strict_delivery_bad_cases = {
        "zip_only": """### 交付文件下载链接

- 报告压缩包下载链接：[下载 report.zip](sandbox:/mnt/data/report.zip)
""",
        "zip_plus_files": """### 交付文件下载链接

- 静态网页（HTML）下载链接：[下载/打开 report.html](sandbox:/mnt/data/report.html)
- Markdown 文件下载链接：[下载 report.md](sandbox:/mnt/data/report.md)
- 打包下载链接：[下载 report.zip](sandbox:/mnt/data/report.zip)
""",
        "html_inside_zip": """### 交付文件下载链接

- 静态网页（HTML）下载链接：[下载 report.html.zip](sandbox:/mnt/data/report.html.zip)
- Markdown 文件下载链接：[下载 report.md](sandbox:/mnt/data/report.md)
""",
    }
    critical_good = """招生人数：[约6人](https://example.edu/plan)；招生批次：本科批；院校专业组：201
最低分/最低位次：[约650分/约1200位](https://example.edu/score)
就业率：未知（未核到可打开且内容对应的来源链接）
保研率：未知（学校未公开项目口径，待学校书面确认）
"""
    if critical_data_source_errors(critical_good):
        errors.append("critical-data-source self-test should pass source-linked approx values and unknown fields: " + "; ".join(critical_data_source_errors(critical_good)[:3]))
    critical_bad = """招生人数：6人；来源：https://example.edu/plan
分数线：650分；最低位次：1200位
就业率：95%
保研率：约10%
"""
    if not critical_data_source_errors(critical_bad):
        errors.append("critical-data-source self-test failed to reject missing 约/source-linked critical data")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        good_html = tmp / "report.html"
        good_md = tmp / "report.md"
        good_html.write_text("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'></head><body><main>ok</main></body></html>", encoding="utf-8")
        good_md.write_text("# 报告\n\n正文", encoding="utf-8")
        if pure_target_file_errors(str(good_html), "html") or pure_target_file_errors(str(good_md), "md"):
            errors.append("pure-report-file self-test should pass true .html and .md files")
        zipped_html = tmp / "浙江物理类2.5万位计算机AI方向中外合作项目分析报告（HTML）.zip"
        with zipfile.ZipFile(zipped_html, "w") as zf:
            zf.writestr("浙江物理类2.5万位计算机AI方向中外合作项目分析报告（HTML）", "<!doctype html><html><body>looks like html but packaged</body></html>")
        if not pure_target_file_errors(str(zipped_html), "html"):
            errors.append("pure-report-file self-test failed to reject ZIP container whose content looks like HTML")

    return result(not errors, errors, warnings, required_files=len(REQUIRED_FILES))


def row_search_text(row: dict[str, Any]) -> str:
    parts = [
        row.get("canonical_project_or_institution_name", ""),
        row.get("chinese_partner", ""),
        row.get("foreign_partner", ""),
        row.get("country_region", ""),
        row.get("province_of_chinese_partner_or_entity", ""),
        row.get("project_level", ""),
    ]
    major = row.get("major_or_category") or {}
    if isinstance(major, dict):
        parts.extend([major.get("name", ""), major.get("major_group", ""), major.get("industry_group", "")])
    admissions = row.get("admissions") or {}
    if isinstance(admissions, dict):
        parts.extend([admissions.get("admission_plan_text_excerpt_from_local_index", ""), admissions.get("study_mode_text", "")])
    return " ".join(map(str, parts))


def score_text(query: str, target: str) -> int:
    q_norm = normalize(query)
    t_norm = normalize(target)
    score = 0
    for token in re.split(r"[\s+，,;；/]+", query):
        token = token.strip()
        if not token:
            continue
        n = normalize(token)
        if n and n in t_norm:
            score += max(2, len(n))
    if q_norm and q_norm in t_norm:
        score += 20
    return score


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    major = row.get("major_or_category") or {}
    admissions = row.get("admissions") or {}
    rankings = row.get("rankings") or {}
    qs = rankings.get("foreign_qs_world_university_2027") if isinstance(rankings, dict) else {}
    softke = rankings.get("softke_chinese_school_2026") if isinstance(rankings, dict) else {}
    return {
        "name": row.get("canonical_project_or_institution_name"),
        "chinese_partner": row.get("chinese_partner"),
        "foreign_partner": row.get("foreign_partner"),
        "province": row.get("province_of_chinese_partner_or_entity"),
        "major": major.get("name") if isinstance(major, dict) else major,
        "project_level": row.get("project_level"),
        "start_year": row.get("start_year"),
        "recommendation_eligible": row.get("recommendation_eligible"),
        "local_admission_status": admissions.get("current_year_admission_status") if isinstance(admissions, dict) else None,
        "local_tuition_text": admissions.get("tuition_domestic_rmb_per_year_text") if isinstance(admissions, dict) else None,
        "local_certificate_status": (admissions.get("certificates") or {}).get("certificate_verification_status") if isinstance(admissions, dict) and isinstance(admissions.get("certificates"), dict) else None,
        "foreign_qs_rank_local_hint": qs.get("rank") if isinstance(qs, dict) else None,
        "softke_chinese_school_rank_local_hint": softke.get("rank") if isinstance(softke, dict) else None,
        "warning": "local index is only a discovery hint; verify through current official sources before user-facing analysis",
    }


def cmd_query(args: argparse.Namespace) -> int:
    idx = load_json(INDEX_PATH)
    rows = idx.get("rows", [])
    hits = []
    for row in rows:
        s = score_text(args.query, row_search_text(row))
        if s > 0:
            hits.append((s, row))
    hits.sort(key=lambda x: x[0], reverse=True)
    payload = [dict(score=s, **compact_row(row)) for s, row in hits[: args.top]]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def flatten(obj: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


def cmd_rank_query(args: argparse.Namespace) -> int:
    data = load_json(RANKINGS_PATH)
    q = normalize(args.query)
    records: list[tuple[int, str, dict[str, Any]]] = []
    for path, value in flatten(data):
        if isinstance(value, str) and q and q in normalize(value):
            container_path = path.rsplit(".", 1)[0]
            score = len(q) + 5
            records.append((score, container_path, {"path": path, "value": value}))
    records.sort(key=lambda x: x[0], reverse=True)
    print(json.dumps([r[2] for r in records[: args.top]], ensure_ascii=False, indent=2))
    return 0



def safe_filename_slug(text: str, max_len: int = 56) -> str:
    """Create a compact task-derived filename stem.

    Chinese characters are retained; whitespace and punctuation are normalized.
    Generic platform/tool words are removed so artifacts are named for the
    actual analysis task rather than the execution environment.
    """
    text = re.sub(r"<[^>]+>", "", str(text or ""))
    for term in PLATFORM_ARTIFACT_NAME_TERMS:
        text = text.replace(term, "")
    text = re.sub(r"[\\/:*?\"<>|]+", "-", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text).strip("-_. ")
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "", text)
    if not text or text.lower() in GENERIC_ARTIFACT_STEMS:
        text = "cooplens-分析报告"
    return text[:max_len].strip("-_. ") or "cooplens-分析报告"


def clean_report_title(raw: str) -> str:
    """Return a display-safe report title without Markdown heading syntax.

    The broken HTML samples showed `<title>## 目录</title>` and a hero H1
    of `## 目录`.  Mobile skill containers can treat that as a malformed page.
    Titles therefore must be task-derived, visible, and not copied from the TOC.
    """
    s = html.unescape(re.sub(r"<[^>]+>", "", str(raw or ""))).strip()
    s = re.sub(r"^#{1,6}\s*", "", s).strip()
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[`*_]+", "", s)
    s = re.sub(r"\s+", " ", s).strip(" -—_:：。.")
    return s[:80].strip()


def report_title_is_bad(raw: str) -> bool:
    raw_s = str(raw or "").strip()
    clean = clean_report_title(raw_s)
    n = normalize(clean)
    if not clean:
        return True
    if raw_s.startswith("#"):
        return True
    if n in {"目录", "正文", "重要声明", "检索执行日期", "cooplensreport", "cooplens报告", "报告", "分析报告"}:
        return True
    if n.startswith("目录") and len(n) <= 8:
        return True
    return False


def title_from_filename(path_or_name: str) -> str:
    stem = Path(str(path_or_name or "")).stem
    stem = re.sub(r"（?HTML版）?", "", stem, flags=re.I)
    stem = re.sub(r"[-_]+", " · ", stem)
    return clean_report_title(stem)


def title_from_markdown(md: str, fallback: str | None = None) -> str:
    for line in md.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            candidate = m.group(1).strip()
            if not report_title_is_bad(candidate):
                return clean_report_title(candidate)
    fb = title_from_filename(fallback or "")
    if not report_title_is_bad(fb):
        return fb
    for line in md.splitlines():
        line = line.strip()
        if not line or line.startswith("重要声明") or line.startswith("检索执行日期"):
            continue
        if re.match(r"^##\s*目录\s*$", line):
            continue
        if re.match(r"^[-*+]\s+\[", line):
            continue
        candidate = clean_report_title(line)
        if not report_title_is_bad(candidate):
            return candidate
    return "中外合作办学分析报告"


def artifact_name_is_bad(name: str) -> bool:
    stem = Path(name).stem.strip().lower()
    normalized = normalize(stem)
    if not stem or stem in GENERIC_ARTIFACT_STEMS or len(stem) <= 2:
        return True
    for term in PLATFORM_ARTIFACT_NAME_TERMS:
        if normalize(term) and normalize(term) in normalized:
            return True
    return False


def safe_output_path(requested: Path, markdown_title: str, suffix: str) -> Path:
    if artifact_name_is_bad(requested.name):
        return requested.with_name(safe_filename_slug(markdown_title) + suffix)
    return requested.with_suffix(suffix)


def visible_text_from_html(src: str) -> str:
    src = re.sub(r"<style[\s\S]*?</style>", " ", src, flags=re.I)
    src = re.sub(r"<script[\s\S]*?</script>", " ", src, flags=re.I)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(re.sub(r"\s+", " ", src))


def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def check_disclaimer_and_date(text: str) -> list[str]:
    errors = []
    if first_non_empty_line(text) != DISCLAIMER:
        errors.append("fixed disclaimer must be the first non-empty line")
    if "检索执行日期：" not in text:
        errors.append("runtime date line missing")
    return errors


def check_no_public_terms(text: str) -> list[str]:
    errors = []
    for term in FORBIDDEN_PUBLIC_REPORT_TERMS:
        if term and term in text:
            errors.append(f"public-discussion report exposes forbidden term: {term}")
    return errors


def check_no_blanket_claims(text: str) -> list[str]:
    errors = [f"blanket source claim not allowed: {term}" for term in BLANKET_SOURCE_CLAIMS if term in text]
    for pattern in BLANKET_SOURCE_CLAIM_PATTERNS:
        for m in pattern.finditer(text):
            snippet = re.sub(r"\s+", " ", m.group(0)).strip()[:120]
            errors.append(f"blanket source claim not allowed: {snippet}")
    return errors


def text_without_code_literals(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`]*`", " ", text)
    return text


def check_strict_important_statement(text: str) -> list[str]:
    scan = text_without_code_literals(text)
    errors: list[str] = []
    if "重要申明" in scan:
        errors.append("use `重要声明` exactly; `重要申明` is not allowed")
    for m in re.finditer(r"重要声明[:：][^。\n]*(?:。)?", scan):
        statement = m.group(0).strip()
        if statement != DISCLAIMER:
            errors.append(f"custom important statement is not allowed; use the fixed statement exactly: {statement}")
    return errors


def check_appendix_important_statement(text: str) -> list[str]:
    errors: list[str] = []
    if "附录：重要声明" not in text and "附录：重要声明与人工确认提醒" not in text:
        errors.append("full report missing appendix important statement section: ## 附录：重要声明与人工确认提醒")
    appendix_pos = max(text.rfind("附录：重要声明"), text.rfind("附录：重要声明与人工确认提醒"))
    if appendix_pos != -1 and DISCLAIMER not in text[appendix_pos:]:
        errors.append("appendix important statement section must repeat the fixed statement exactly")
    return errors


def check_function3_structure(text: str) -> list[str]:
    triggered = any(t in text for t in ["候选", "按省份", "同分段", "可选项目", "项目可选", "找项目"])
    errors: list[str] = []
    if not triggered:
        return errors
    toc = text.find("## 目录")
    if toc == -1:
        errors.append("Function 3 report must place ## 目录 before analysis sections")
    important_terms = ["最重要建议", "先看这里", "优先候选", "备选候选", "观察候选", "慎选候选"]
    first_advice_positions = [text.find(t) for t in important_terms if text.find(t) != -1]
    first_advice = min(first_advice_positions) if first_advice_positions else -1
    if first_advice == -1:
        errors.append("Function 3 report missing the most-important advice block before explanatory sections")
    if toc != -1 and first_advice != -1 and toc > first_advice:
        errors.append("Function 3 report must show the table of contents before the advice/analysis section")
    explanation_markers = ["最新官方材料核验", "可验证数据统计", "统计口径", "位差与线差分析", "参考来源与核验说明", "人工确认清单"]
    explanation_positions = [text.find(t) for t in explanation_markers if text.find(t) != -1]
    if first_advice != -1 and explanation_positions and min(explanation_positions) < first_advice:
        errors.append("Function 3 explanatory/source/method sections must come after the most-important advice")
    return errors


def check_no_doc_export_terms(text: str) -> list[str]:
    errors = []
    for term in DOCUMENT_EXPORT_TERMS:
        if term in text:
            errors.append("document-export wording is not part of the default workflow")
    return errors



def _line_has_unknown_marker(line: str) -> bool:
    return any(term in line for term in CRITICAL_DATA_UNKNOWN_TERMS)


def _line_has_source_link(line: str) -> bool:
    return bool(MD_LINK_PATTERN.search(line) or URL_PATTERN.search(line) or "filecite" in line or "cite" in line)


def _critical_label_for_line(line: str) -> str | None:
    for term in CRITICAL_DATA_TERMS:
        if term in line:
            return term
    return None


def _link_text_spans(text: str) -> list[tuple[int, int]]:
    return [(m.start(1), m.end(1)) for m in MD_LINK_PATTERN.finditer(text)]


def _inside_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos <= b for a, b in spans)


def critical_data_source_errors(text: str) -> list[str]:
    """Hard gate for critical admissions/outcome data.

    Admissions plan counts, score/rank lines and graduate-outcome rates are
    decision-critical. The model must not fill them from memory or estimate
    them without a source that opens and supports the value. In visible output,
    use `约` before each important numeric value and place a source hyperlink
    on the same line; if verification fails, write unknown instead.
    """
    errors: list[str] = []
    spans = _link_text_spans(text)
    offset = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        start_offset = offset
        offset += len(line) + 1
        label = _critical_label_for_line(line)
        if not label:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#") and not re.search(r"[:：]", stripped):
            continue
        values = list(CRITICAL_VALUE_PATTERN.finditer(line))
        has_unknown = _line_has_unknown_marker(line)
        has_link = _line_has_source_link(line)
        if values:
            if not has_link:
                errors.append(f"line {lineno}: critical data `{label}` has numeric value but no source hyperlink on the same line; write unknown if no verified source: {stripped[:160]}")
            for m in values:
                value = m.group(0).strip()
                if not value.startswith("约"):
                    errors.append(f"line {lineno}: critical numeric value must be prefixed with `约`: {value}")
                # Prefer the number itself to be linked. If it is not, allow a source link on the same line but flag it as weaker.
                if not _inside_spans(start_offset + m.start(), spans) and not has_link:
                    errors.append(f"line {lineno}: critical numeric value should be linked or accompanied by a same-line source link: {value}")
        else:
            # A critical-data label with no value must say unknown/未核到 instead of leaving the field vague.
            if re.search(r"[:：]", stripped) and not has_unknown and not has_link:
                errors.append(f"line {lineno}: critical data field `{label}` must provide source-linked data or explicitly write unknown/未核到: {stripped[:160]}")
    return list(dict.fromkeys(errors))


def critical_evidence_items(text: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        label = _critical_label_for_line(line)
        if not label or _line_has_unknown_marker(line):
            continue
        values = [m.group(0).strip() for m in CRITICAL_VALUE_PATTERN.finditer(line)]
        if not values:
            continue
        urls = [u for _label, u in MD_LINK_PATTERN.findall(line)]
        urls.extend(URL_PATTERN.findall(line))
        urls = list(dict.fromkeys(u.strip().rstrip(BAD_HREF_TRAILING) for u in urls if u.strip().startswith(("http://", "https://"))))
        items.append({"line": lineno, "label": label, "values": values, "urls": urls, "text": line.strip()})
    return items


def _critical_keyword_bucket(label: str, line: str) -> str:
    if any(t in label or t in line for t in ["招生", "计划"]):
        return "招生"
    if any(t in label or t in line for t in ["分数", "投档", "录取", "最低分"]):
        return "分数"
    if any(t in label or t in line for t in ["位次", "分位", "排位"]):
        return "位次"
    if any(t in label or t in line for t in ["升学", "深造"]):
        return "升学"
    if "出国" in label or "出国" in line or "境外" in line:
        return "出国"
    if "就业" in label or "去向" in line:
        return "就业"
    if "保研" in label or "推免" in label or "推免" in line:
        return "保研"
    return "招生"


def _digits_only(s: str) -> str:
    return re.sub(r"\D", "", s)


def fetch_url_text(url: str, *, timeout: float = 10.0, max_bytes: int = 300_000) -> tuple[bool, str, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CoopLens critical-source evidence check"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", None) or resp.getcode())
            ctype = (resp.headers.get("content-type") or "").lower()
            data = resp.read(max_bytes)
        if status < 200 or status >= 400:
            return False, "", f"status {status}"
        if any(t in ctype for t in ["zip", "rar", "7z", "octet-stream"]):
            return False, "", f"not inspectable text/html source: {ctype}"
        text = data.decode("utf-8", errors="ignore")
        text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(re.sub(r"\s+", " ", text))
        if not text.strip():
            return False, "", f"empty or non-text source: {ctype}"
        return True, text, ""
    except Exception as exc:
        return False, "", str(exc)[:200]


def critical_source_evidence_errors(text: str, *, timeout: float = 10.0, max_lines: int = 80) -> list[str]:
    """Network-assisted check: linked critical-data source must contain matching evidence.

    This is intentionally strict. If no opened link contains both a relevant
    keyword and a recognizable value, the report should replace the value with
    `未知（未核到可打开且内容对应的来源链接）` rather than guessing.
    """
    errors: list[str] = []
    cache: dict[str, tuple[bool, str, str]] = {}
    for item in critical_evidence_items(text)[:max_lines]:
        if not item["urls"]:
            errors.append(f"line {item['line']}: no URL to verify critical data: {item['text'][:160]}")
            continue
        bucket = _critical_keyword_bucket(str(item["label"]), str(item["text"]))
        keywords = CRITICAL_SOURCE_KEYWORDS.get(bucket, [])
        wanted_digits = [_digits_only(v) for v in item["values"]]
        wanted_digits = [d for d in wanted_digits if len(d) >= 1]
        supported = False
        fetch_notes: list[str] = []
        for url in item["urls"][:3]:
            if url not in cache:
                cache[url] = fetch_url_text(url, timeout=timeout)
            ok, body, note = cache[url]
            if not ok:
                fetch_notes.append(f"{url} => {note}")
                continue
            body_digits = _digits_only(body)
            has_keyword = any(k in body for k in keywords)
            has_value = not wanted_digits or any(d in body_digits for d in wanted_digits)
            if has_keyword and has_value:
                supported = True
                break
            fetch_notes.append(f"{url} => opened but did not contain expected keyword/value")
        if not supported:
            errors.append(f"line {item['line']}: linked source did not verify critical data; replace with unknown unless an opened source contains the value. Details: {'; '.join(fetch_notes[:3])}")
    return errors


def check_batch_distinction_text(text: str) -> list[str]:
    """Ensure admission plan/score/rank analysis keeps batch口径 separate.

    The same project can have different batches, professional groups or plan
    types. When a report uses plan counts, score lines or rank references, it
    must show batch-level fields and avoid merging different口径 values.
    """
    triggered = any(term in text for term in BATCH_DISTINCTION_TRIGGER_TERMS)
    if not triggered:
        return []
    errors: list[str] = []
    for name, terms in BATCH_DISTINCTION_GROUPS.items():
        if not any(term in text for term in terms):
            errors.append(f"batch distinction missing: {name}")
    if any(term in text for term in ["合并招生人数", "合并计划", "平均分数线", "取最低位次"]) and not any(term in text for term in ["不得", "不能", "不允许", "禁止"]):
        errors.append("batch distinction risk: report appears to merge or average batch-specific data without forbidding it")
    return errors


def check_current_admission_status_text(text: str) -> list[str]:
    """Ensure reports first confirm whether the exact project recruits this year.

    Regulatory identity/approval is not equivalent to current-year enrollment.
    If a project is stopped, suspended, absent from current-year plan/catalog or
    unresolved, it must not be used in rank formulas or hard candidate ranking.
    """
    triggered = any(term in text for term in CURRENT_ADMISSION_STATUS_TRIGGER_TERMS)
    if not triggered:
        return []
    errors: list[str] = []
    for name, terms in CURRENT_ADMISSION_STATUS_GROUPS.items():
        if not any(term in text for term in terms):
            errors.append(f"current-year admission status gate missing: {name}")
    has_stop_or_unknown = any(term in text for term in CURRENT_ADMISSION_STOP_TERMS)
    if has_stop_or_unknown and not any(term in text for term in CURRENT_ADMISSION_STOP_HANDLING_TERMS):
        errors.append("current-year admission status gate missing stop/unknown handling: stopped or unconfirmed projects must not enter rank formulas or hard ranking")
    if any(term in text for term in ["CRS", "教育部中外合作办学监管工作信息平台", "监管记录"]) and any(term in text for term in ["继续招生", "当年招生", "仍在招生"]):
        if not any(term in text for term in ["学校官网", "本科招生网", "招生办", "当年招生计划", "当年专业目录", "省级专业目录"]):
            errors.append("CRS/regulator identity alone cannot support current-year recruiting; include school/provincial current-year admission evidence")
    return errors


ARTIFACT_LINK_RE = re.compile(r"(?:sandbox:/[^)\s]+|[A-Za-z0-9_./\-\u4e00-\u9fff]+)\.(?:md|html|json)", re.I)
ARCHIVE_ARTIFACT_LINK_RE = re.compile(r"(?:sandbox:/[^)\s]+|[A-Za-z0-9_./\-\u4e00-\u9fff]+)\.(?:zip|rar|7z|tgz|tar\.gz)", re.I)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ARCHIVE_TOKEN_RE = re.compile(r"(?i)(?:\.zip|\.rar|\.7z|\.tgz|\.tar\.gz|\bzip\b|\brar\b|\b7z\b|\btgz\b|压缩包|打包下载|打包文件|打包合集|合集下载|文件夹下载|archive package|archive link|compressed bundle|folder link)")
ARCHIVE_DELIVERY_TERMS = ["zip", ".zip", "rar", ".rar", "7z", ".7z", "tgz", ".tgz", "tar.gz", ".tar.gz", "压缩包", "打包下载", "打包文件", "打包合集", "合集下载", "文件夹下载", "archive package", "archive link", "compressed bundle", "folder link"]

def artifact_links_by_suffix(text: str, suffix: str) -> list[str]:
    suffix = suffix.lower().lstrip('.')
    links: list[str] = []
    for m in ARTIFACT_LINK_RE.finditer(text):
        value = m.group(0).strip()
        if value.lower().endswith('.' + suffix):
            links.append(value)
    return links

def final_answer_has_artifact(text: str, suffix: str) -> bool:
    return bool(artifact_links_by_suffix(text, suffix))

def archive_artifact_links(text: str) -> list[str]:
    return [m.group(0).strip() for m in ARCHIVE_ARTIFACT_LINK_RE.finditer(text)]

def archive_delivery_violations(text: str) -> list[str]:
    """Return ZIP/archive/bundle delivery violations in a final answer.

    Function outputs must link the individual pure .html and .md files.
    A downloadable archive is not an acceptable substitute, even when it
    contains those files. The term check is limited to delivery/download
    lines to avoid punishing explanatory policy text elsewhere.
    """
    violations = archive_artifact_links(text)
    lowered_terms = [t.lower() for t in ARCHIVE_DELIVERY_TERMS]
    for line in text.splitlines():
        low = line.lower()
        is_delivery_line = any(term in line for term in ["交付文件下载链接", "下载链接", "下载", "交付"]) or "download" in low
        if not is_delivery_line:
            continue
        if any(term in low for term in lowered_terms):
            violations.append(line.strip()[:180])
    return list(dict.fromkeys(violations))

DOWNLOAD_LABEL_TERMS = ["下载", "download"]

def artifact_download_links_by_suffix(text: str, suffix: str) -> list[str]:
    """Return artifact links whose visible line clearly presents them as downloads.

    The final answer must not merely mention a filename or say a file was
    generated. A user should see an explicit download-link line for each
    generated deliverable. This intentionally accepts platform-specific link
    formats as long as the same line contains 下载/download and a .md/.html link.
    """
    suffix = suffix.lower().lstrip('.')
    links: list[str] = []
    for line in text.splitlines():
        if not any(term.lower() in line.lower() for term in DOWNLOAD_LABEL_TERMS):
            continue
        links.extend(artifact_links_by_suffix(line, suffix))
    return links

def final_answer_has_download_artifact(text: str, suffix: str) -> bool:
    return bool(artifact_download_links_by_suffix(text, suffix))

def markdown_link_targets(line: str) -> list[str]:
    return [target.strip() for _label, target in MARKDOWN_LINK_RE.findall(line)]

def _target_without_fragment_or_query(target: str) -> str:
    return target.strip().split("#", 1)[0].split("?", 1)[0]

def is_pure_file_target(target: str, suffix: str) -> bool:
    """Return True only for a direct standalone .html/.md file target.

    This deliberately rejects archives, generated bundles, folders and links
    where the visible text implies ZIP/download packaging. The skill report
    delivery must be two single files, not a ZIP containing the files.
    """
    suffix = suffix.lower().lstrip(".")
    clean = _target_without_fragment_or_query(target).lower()
    if ARCHIVE_TOKEN_RE.search(target):
        return False
    return clean.endswith("." + suffix)


def local_path_from_target(target: str) -> Path | None:
    clean = _target_without_fragment_or_query(target).strip()
    if clean.startswith("sandbox:"):
        clean = clean[len("sandbox:"):]
    if clean.startswith("file://"):
        clean = clean[len("file://"):]
    if clean.startswith("/"):
        return Path(clean)
    if re.match(r"^[A-Za-z]:[\\/]", clean):
        return Path(clean)
    # Relative artifact paths are checked relative to the current working directory.
    if not re.match(r"^[a-z]+://", clean, flags=re.I):
        return Path(clean)
    return None


def path_has_archive_magic(path: Path) -> bool:
    try:
        if zipfile.is_zipfile(path):
            return True
        head = path.read_bytes()[:8]
    except Exception:
        return False
    return head.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08", b"Rar!", b"7z\xbc\xaf\x27\x1c", b"\x1f\x8b"))


def pure_target_file_errors(target: str, suffix: str) -> list[str]:
    suffix = suffix.lower().lstrip(".")
    errors: list[str] = []
    path = local_path_from_target(target)
    if path is None:
        return errors
    if not path.exists():
        errors.append(f"delivery target does not exist locally and cannot be verified as a pure .{suffix} file: {target}")
        return errors
    clean_name = path.name.lower()
    if ARCHIVE_TOKEN_RE.search(str(target)) or clean_name.endswith((".zip", ".rar", ".7z", ".tgz", ".tar.gz")):
        errors.append(f"delivery target is an archive/package, not a pure .{suffix} file: {target}")
    if path.suffix.lower() != "." + suffix:
        errors.append(f"delivery target must have literal .{suffix} filename suffix; got `{path.name}` from {target}")
    if path_has_archive_magic(path):
        errors.append(f"delivery target has archive/ZIP magic bytes; it is not a pure .{suffix} file: {target}")
        return errors
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        errors.append(f"delivery target cannot be read as UTF-8 text: {target}: {exc}")
        return errors
    low = text[:5000].lower()
    if suffix == "html":
        if "<!doctype html" not in low or "<html" not in low or "</html>" not in text.lower():
            errors.append(f"HTML delivery target is not a complete standalone HTML document: {target}")
    elif suffix == "md":
        if "<!doctype html" in low or "<html" in low:
            errors.append(f"Markdown delivery target appears to be HTML content, not pure Markdown: {target}")
    return errors


def delivered_file_target_errors(text: str) -> list[str]:
    errors: list[str] = []
    html_targets = pure_download_targets_by_suffix(text, "html")
    md_targets = pure_download_targets_by_suffix(text, "md")
    for target in html_targets:
        errors.extend(pure_target_file_errors(target, "html"))
    for target in md_targets:
        errors.extend(pure_target_file_errors(target, "md"))
    return errors


def pure_download_targets_by_suffix(text: str, suffix: str) -> list[str]:
    suffix = suffix.lower().lstrip(".")
    targets: list[str] = []
    for line in text.splitlines():
        if not any(term.lower() in line.lower() for term in DOWNLOAD_LABEL_TERMS):
            continue
        line_targets = markdown_link_targets(line)
        if line_targets:
            for target in line_targets:
                if is_pure_file_target(target, suffix):
                    targets.append(target)
            continue
        # Accept a raw sandbox/path link only when there is no Markdown link
        # on the same line and the line clearly says 下载/download.
        for raw in artifact_links_by_suffix(line, suffix):
            if is_pure_file_target(raw, suffix):
                targets.append(raw)
    return list(dict.fromkeys(targets))

def strict_pure_html_md_delivery_errors(text: str, *, check_local_files: bool = False) -> list[str]:
    """Hard final-answer gate for Function 1/2/3/4 report delivery.

    A passing final answer must expose exactly the two report artifacts as
    direct, user-clickable single-file downloads: one .html and one .md.
    Any ZIP/archive/bundle wording or link is a failure, even when the archive
    allegedly contains the HTML/Markdown.
    """
    errors: list[str] = []
    archive_violations = archive_delivery_violations(text)
    for bad in archive_violations:
        errors.append(f"ZIP/archive/bundle delivery is forbidden; deliver two direct single-file links only: {bad}")

    for line in text.splitlines():
        low = line.lower()
        if any(term in line for term in ["下载", "交付", "链接"]) or "download" in low:
            if ARCHIVE_TOKEN_RE.search(line):
                errors.append(f"delivery/download line mentions ZIP/archive/bundle and must be regenerated: {line.strip()[:180]}")

    if "交付文件下载链接" not in text:
        errors.append("missing visible `交付文件下载链接` block")

    html_label_lines = [line for line in text.splitlines() if "静态网页" in line and "HTML" in line and "下载链接" in line]
    md_label_lines = [line for line in text.splitlines() if "Markdown" in line and "下载链接" in line]
    if not html_label_lines:
        errors.append("missing required line label: 静态网页（HTML）下载链接")
    if not md_label_lines:
        errors.append("missing required line label: Markdown 文件下载链接")

    html_targets = pure_download_targets_by_suffix("\n".join(html_label_lines), "html")
    md_targets = pure_download_targets_by_suffix("\n".join(md_label_lines), "md")
    if len(html_targets) != 1:
        errors.append(f"HTML delivery must contain exactly one direct pure .html download target; found {len(html_targets)}")
    if len(md_targets) != 1:
        errors.append(f"Markdown delivery must contain exactly one direct pure .md download target; found {len(md_targets)}")
    if check_local_files:
        for target in html_targets:
            errors.extend(pure_target_file_errors(target, "html"))
        for target in md_targets:
            errors.extend(pure_target_file_errors(target, "md"))

    delivery_block_text = ""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "交付文件下载链接" in line:
            delivery_block_text = "\n".join(lines[i:])
            break
    if delivery_block_text:
        all_delivery_targets = []
        for line in delivery_block_text.splitlines():
            all_delivery_targets.extend(markdown_link_targets(line))
        non_report_targets = [t for t in all_delivery_targets if not (is_pure_file_target(t, "html") or is_pure_file_target(t, "md"))]
        if non_report_targets:
            errors.append("delivery block may only contain pure .html and .md single-file links; other targets found: " + ", ".join(non_report_targets[:4]))

    return list(dict.fromkeys(errors))

def explicit_html_failure(text: str) -> bool:
    failure_terms = ["HTML 渲染失败", "HTML 生成失败", "HTML 语法校验失败", "静态页面生成失败", "错误报告", "html_audit", "audit.json"]
    return any(term in text for term in failure_terms)

def html_artifact_delivery_errors(text: str, *, allow_explicit_failure: bool = False, check_local_files: bool = False) -> list[str]:
    errors: list[str] = []
    errors.extend(strict_pure_html_md_delivery_errors(text, check_local_files=check_local_files))
    archive_violations = archive_delivery_violations(text)
    for bad in archive_violations:
        errors.append(f"archive/ZIP delivery link is forbidden; provide direct pure .html and .md file download links instead: {bad}")
    has_md = final_answer_has_artifact(text, "md")
    has_html = final_answer_has_artifact(text, "html")
    has_md_download = final_answer_has_download_artifact(text, "md")
    has_html_download = final_answer_has_download_artifact(text, "html")
    has_audit = final_answer_has_artifact(text, "json") or "html_audit" in text or "错误报告" in text
    if not has_md:
        errors.append("Markdown download link is missing; final answer must include a direct task-named pure .md report file download link, not a ZIP/archive")
    elif not has_md_download:
        errors.append("Markdown artifact is mentioned but not presented as a visible download link; the .md link line must contain 下载")
    if not has_html:
        if allow_explicit_failure and explicit_html_failure(text) and has_audit:
            return errors
        errors.append("static HTML download link is missing; final answer must include a direct task-named pure .html file download link, not a ZIP/archive")
    elif not has_html_download:
        errors.append("static HTML artifact is mentioned but not presented as a visible download link; the .html link line must contain 下载")
    if has_md and has_html and "交付文件下载链接" not in text:
        errors.append("final answer must include a visible `交付文件下载链接` block with only direct .html and .md file download links")
    return errors


def heading_slug(text: str) -> str:
    """Return a WebView-safe ASCII id for a heading.

    Some mobile skill containers fail or refuse section navigation when ids
    contain Chinese text, punctuation, emoji, spaces, or very long strings.
    Use a short stable hash instead of visible heading text; the visible text
    remains unchanged in the rendered page and TOC.
    """
    clean = re.sub(r"<[^>]+>", "", str(text))
    clean = html.unescape(clean)
    clean = re.sub(r"\s+", " ", clean).strip() or "section"
    digest = hashlib.sha1(clean.encode("utf-8")).hexdigest()[:10]
    return f"sec-{digest}"


def unique_heading_slug(title: str, counts: dict[str, int]) -> str:
    base = heading_slug(title) or "section"
    counts[base] = counts.get(base, 0) + 1
    if counts[base] == 1:
        return base
    return f"{base}-{counts[base]}"


def normalize_internal_anchor(href: str) -> str:
    """Normalize Markdown TOC anchors to current ASCII heading ids."""
    if not href.startswith("#"):
        return href
    raw = html.unescape(href[1:].strip()).lstrip("#")
    if ASCII_ID_PATTERN.fullmatch(raw):
        return "#" + raw
    return "#" + heading_slug(raw)


def sanitize_external_href(raw: str) -> str:
    """Return a WebView-safe http(s) href or an empty string.

    The renderer intentionally strips common full-width closing punctuation and
    any accidental Chinese text captured from malformed Markdown links, e.g.
    `https://example.cn/）申请认证`.  If a URL cannot be made ASCII-safe, it is
    withheld rather than producing a broken HTML artifact.
    """
    href = html.unescape(str(raw)).strip().strip('"\'')
    # Stop at the first non-ASCII character; official/source URLs in reports
    # should be punycode or percent-encoded before becoming href attributes.
    href = re.split(r"[^\x21-\x7e]", href, maxsplit=1)[0]
    href = href.rstrip(BAD_HREF_TRAILING)
    if SAFE_EXTERNAL_HREF_PATTERN.fullmatch(href):
        return href
    return ""


def heading_ids_for_markdown(md: str) -> list[tuple[int, str, str]]:
    counts: dict[str, int] = {}
    out: list[tuple[int, str, str]] = []
    for level, title, _ in extract_headings(md):
        out.append((level, title, unique_heading_slug(title, counts)))
    return out


def build_clean_toc(md: str) -> str:
    entries = []
    for level, title, slug in heading_ids_for_markdown(md):
        if level == 2 and title != "目录":
            entries.append(f"- [{title}](#{slug})")
    if not entries:
        return f"## 目录\n\n- [正文](#{heading_slug('正文')})"
    return "## 目录\n\n" + "\n".join(entries)


def repair_markdown_toc(md: str) -> str:
    """Replace or insert a canonical H2 table of contents for static HTML rendering."""
    lines = md.splitlines()
    toc = build_clean_toc(md).splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+目录\s*$", line.strip()):
            start = i
            break
    if start is not None:
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if re.match(r"^##\s+", lines[j]):
                end = j
                break
        return "\n".join(lines[:start] + toc + [""] + lines[end:]) + "\n"

    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
        if line.startswith("检索执行日期："):
            insert_at = i + 1
    return "\n".join(lines[:insert_at] + [""] + toc + [""] + lines[insert_at:]) + "\n"


def ensure_static_markdown_shape(md: str, title: str) -> str:
    """Normalize Markdown before static HTML rendering.

    A passing mobile artifact must have a visible task-derived hero title, a
    canonical TOC, and horizontal rules instead of visible `---` paragraphs.
    If the Markdown lacks an H1 or accidentally uses the TOC as its title, the
    renderer injects/replaces the H1 with a clean task title.
    """
    text = md.strip() + "\n"
    clean_title = clean_report_title(title)
    if report_title_is_bad(clean_title):
        clean_title = title_from_markdown(md)
    lines = text.splitlines()
    h1_index = None
    for i, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            h1_index = i
            break
    if h1_index is None:
        text = f"# {clean_title}\n\n" + text
    else:
        current = re.sub(r"^#\s+", "", lines[h1_index]).strip()
        if report_title_is_bad(current):
            lines[h1_index] = f"# {clean_title}"
            text = "\n".join(lines) + "\n"
    text = re.sub(r"(?m)^\s*---\s*$", "\n---HR---\n", text)
    text = repair_markdown_toc(text)
    return text


def extract_headings(md: str) -> list[tuple[int, str, str]]:
    out = []
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            out.append((level, title, heading_slug(title)))
    return out


def cmd_markdown_toc_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = check_disclaimer_and_date(text)
    if "## 目录" not in text:
        errors.append("Markdown report must contain `## 目录`")
    toc_pos = text.find("## 目录")
    first_analysis = min([p for p in [text.find("## 一、"), text.find("## 一,"), text.find("## 一 ")] if p != -1] or [10**9])
    if toc_pos == -1 or toc_pos > first_analysis:
        errors.append("table of contents must appear before the first analysis section")
    headings = extract_headings(text)
    h2_slugs = [slug for level, title, slug in headings if level == 2 and title != "目录"]
    toc_links = re.findall(r"\]\(#([^)]+)\)", text)
    if len(h2_slugs) >= 4 and not any(slug in toc_links for slug in h2_slugs[:3]):
        errors.append("TOC links should point to report headings")
    return result(not errors, errors, headings=len(headings), toc_links=len(toc_links))


def inline_md_to_html(s: str) -> str:
    """Render the small Markdown subset used inside report paragraphs.

    The converter keeps the HTML self-contained and safe: only http(s) source
    links and in-page TOC anchors are emitted as anchors; everything else is
    escaped. Raw Markdown links should not leak into the static page.
    """
    code_spans: list[str] = []
    link_spans: list[str] = []

    def save_code(m: re.Match[str]) -> str:
        code_spans.append(html.escape(m.group(1)))
        return f"\u0000CODE{len(code_spans)-1}\u0000"

    def save_link(m: re.Match[str]) -> str:
        label = html.escape(m.group(1).strip())
        href_raw = m.group(2).strip()
        if href_raw.startswith("#"):
            href = normalize_internal_anchor(href_raw)
        elif href_raw.startswith("http://") or href_raw.startswith("https://"):
            href = sanitize_external_href(href_raw)
        else:
            href = ""
        if not href:
            return label
        link_spans.append(f'<a href="{html.escape(href, quote=True)}">{label}</a>')
        return f"\u0000LINK{len(link_spans)-1}\u0000"

    s = re.sub(r"`([^`]+)`", save_code, s)
    s = re.sub(r"\[([^\]]+)\]\(((?:https?://|#)[^\s)]+)\)", save_link, s)
    s = html.escape(s)

    def auto_link(m: re.Match[str]) -> str:
        url_visible = m.group(0)
        href = sanitize_external_href(url_visible)
        if not href:
            return html.escape(url_visible)
        safe_visible = html.escape(href)
        link_spans.append(f'<a href="{html.escape(href, quote=True)}">{safe_visible}</a>')
        return f"\u0000LINK{len(link_spans)-1}\u0000"

    s = URL_PATTERN.sub(auto_link, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    for i, link in enumerate(link_spans):
        s = s.replace(f"\u0000LINK{i}\u0000", link)
    for i, code in enumerate(code_spans):
        s = s.replace(f"\u0000CODE{i}\u0000", f"<code>{code}</code>")
    return s



def section_class_for_title(title: str) -> str:
    title = str(title)
    if "结论" in title:
        return "card card-conclusion"
    if "目录" in title:
        return "card toc"
    if "位次" in title or "分数" in title or "投档" in title:
        return "card card-rank"
    if "留服" in title or "认证" in title or "证书" in title:
        return "card card-auth"
    if "费用" in title or "生活成本" in title or "预算" in title:
        return "card card-cost"
    if "公开讨论" in title or "担忧" in title or "核验" in title:
        return "card card-discussion"
    if "家长" in title or "确认" in title or "问题" in title:
        return "card card-questions"
    if "来源" in title or "核验说明" in title:
        return "card card-sources"
    if "毕业" in title or "就业" in title or "升学" in title:
        return "card card-outcomes"
    return "card"


def paragraph_class_for_line(line: str) -> str:
    if line.startswith(DISCLAIMER) or "位次预估重要声明" in line:
        return ' class="notice"'
    if line.startswith("检索执行日期："):
        return ' class="meta"'
    if any(term in line for term in ["计算过程", "公式链", "基线位次", "样本位差", "情景调整"]):
        return ' class="rank-calc"'
    if any(term in line for term in ["项目综合实力推荐度评价", "个性化推荐度评价", "最终动作", "参考区间", "冲/稳/保判断"]):
        return ' class="highlight"'
    return ""

def markdown_to_body(md: str) -> str:
    """Convert CoopLens Markdown into valid mobile-first HTML body markup.

    The converter keeps the page readable in mobile WebViews by avoiding
    unclosed or deeply nested card containers.  Intro paragraphs, the TOC and
    each H2 section become explicit blocks; H3-H6 headings stay inside the
    current H2 card.
    """
    lines = md.splitlines()
    html_lines: list[str] = []
    in_ul = False
    in_ol = False
    in_code = False
    code_buf: list[str] = []
    in_table = False
    table_rows: list[list[str]] = []
    block_open = False
    block_tag = "section"
    slug_counts: dict[str, int] = {}

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    def open_block(css_class: str = "card", tag: str = "section", aria_label: str | None = None) -> None:
        nonlocal block_open, block_tag
        if block_open:
            return
        attrs = f' class="{css_class}"'
        if aria_label:
            attrs += f' aria-label="{html.escape(aria_label, quote=True)}"'
        html_lines.append(f"<{tag}{attrs}>")
        block_open = True
        block_tag = tag

    def close_block() -> None:
        nonlocal block_open, block_tag
        if block_open:
            html_lines.append(f"</{block_tag}>")
            block_open = False
            block_tag = "section"

    def ensure_intro_block() -> None:
        if not block_open:
            open_block("card intro")

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        ensure_intro_block()
        html_lines.append('<div class="table-wrap" role="region" aria-label="可横向滚动表格"><table>')
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            html_lines.append("<tr>" + "".join(f"<{tag}>{inline_md_to_html(cell.strip())}</{tag}>" for cell in row) + "</tr>")
        html_lines.append("</table></div>")
        in_table = False
        table_rows = []

    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("```"):
            flush_table()
            close_lists()
            ensure_intro_block()
            if not in_code:
                in_code = True
                code_buf = []
            else:
                html_lines.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                in_code = False
            continue
        if in_code:
            code_buf.append(line)
            continue

        if not line.strip():
            flush_table()
            close_lists()
            continue

        if line.strip() == "---HR---":
            flush_table()
            close_lists()
            ensure_intro_block()
            html_lines.append("<hr>")
            continue

        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                in_table = True
                continue
            in_table = True
            table_rows.append(cells)
            continue
        else:
            flush_table()

        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            close_lists()
            level = len(m.group(1))
            title = m.group(2).strip()
            slug = unique_heading_slug(title, slug_counts)
            if level == 1:
                close_block()
                html_lines.append(f'<header class="hero"><h1 id="{slug}">{inline_md_to_html(title)}</h1></header>')
            elif level == 2:
                close_block()
                if title == "目录":
                    open_block("card toc", tag="nav", aria_label="目录")
                    html_lines.append(f'<h2 id="{slug}" class="toc-heading">{inline_md_to_html(title)}</h2>')
                else:
                    open_block(section_class_for_title(title))
                    html_lines.append(f'<h2 id="{slug}">{inline_md_to_html(title)}</h2>')
            else:
                ensure_intro_block()
                html_lines.append(f'<h{level} id="{slug}">{inline_md_to_html(title)}</h{level}>')
            continue

        if re.match(r"^[-*+]\s+", line):
            ensure_intro_block()
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append("<li>" + inline_md_to_html(re.sub(r"^[-*+]\s+", "", line)) + "</li>")
            continue

        if re.match(r"^\d+[.)、]\s+", line):
            ensure_intro_block()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append("<li>" + inline_md_to_html(re.sub(r"^\d+[.)、]\s+", "", line)) + "</li>")
            continue

        if line.startswith(">"):
            ensure_intro_block()
            close_lists()
            html_lines.append("<blockquote>" + inline_md_to_html(line.lstrip("> ")) + "</blockquote>")
            continue

        ensure_intro_block()
        close_lists()
        html_lines.append("<p" + paragraph_class_for_line(line) + ">" + inline_md_to_html(line) + "</p>")

    flush_table()
    close_lists()
    if in_code:
        ensure_intro_block()
        html_lines.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    close_block()
    return "\n".join(html_lines)


def static_html_document(md: str, title: str = "中外合作办学分析报告") -> str:
    title = clean_report_title(title)
    if report_title_is_bad(title):
        title = title_from_markdown(md)
    md = ensure_static_markdown_shape(md, title)
    body = markdown_to_body(md)
    css = """
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior:smooth; }
:root {
  color-scheme: light;
  --bg:#f8fafc; --card:#ffffff; --text:#0f172a; --muted:#475569; --line:#e2e8f0;
  --blue:#2563eb; --violet:#7c3aed; --orange:#f97316; --green:#16a34a; --rose:#e11d48;
  --soft-blue:#eef2ff; --soft-orange:#fff7ed; --soft-green:#ecfdf5; --soft-rose:#fff1f2;
  --shadow:0 12px 34px rgba(15,23,42,.10);
}
body { margin:0; background:linear-gradient(180deg,#e0e7ff 0,#f8fafc 240px); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif; line-height:1.75; }
main { width:100%; max-width:920px; margin:0 auto; padding:14px; }
.hero, .card { overflow-wrap:anywhere; word-break:break-word; }
.hero { color:#fff; border-radius:24px; padding:22px 18px; margin:14px 0 16px; background:linear-gradient(135deg,#1d4ed8 0%,#7c3aed 58%,#db2777 100%); box-shadow:var(--shadow); }
.hero h1 { color:#fff; }
.card { position:relative; background:rgba(255,255,255,.96); border:1px solid var(--line); border-radius:20px; padding:16px; margin:14px 0; box-shadow:var(--shadow); }
.card::before { content:""; position:absolute; inset:0 auto 0 0; width:6px; border-radius:20px 0 0 20px; background:var(--blue); }
.card-conclusion { background:linear-gradient(180deg,#eef2ff,#fff); border-color:#c7d2fe; }
.card-rank { background:linear-gradient(180deg,#fff7ed,#fff); border-color:#fed7aa; }
.card-rank::before { background:var(--orange); }
.card-auth { background:linear-gradient(180deg,#ecfdf5,#fff); border-color:#bbf7d0; }
.card-auth::before { background:var(--green); }
.card-cost { background:linear-gradient(180deg,#f0fdfa,#fff); border-color:#99f6e4; }
.card-cost::before { background:#0d9488; }
.card-discussion { background:linear-gradient(180deg,#fff1f2,#fff); border-color:#fecdd3; }
.card-discussion::before { background:var(--rose); }
.card-questions { background:linear-gradient(180deg,#fefce8,#fff); border-color:#fde68a; }
.card-questions::before { background:#ca8a04; }
.card-sources { background:linear-gradient(180deg,#f8fafc,#fff); border-color:#cbd5e1; }
.card-sources::before { background:#64748b; }
.card-outcomes { background:linear-gradient(180deg,#f5f3ff,#fff); border-color:#ddd6fe; }
.card-outcomes::before { background:var(--violet); }
.toc { background:rgba(255,255,255,.9); border-color:#c7d2fe; }
.toc::before { background:linear-gradient(180deg,#2563eb,#7c3aed); }
h1 { font-size:1.58rem; line-height:1.28; margin:0; letter-spacing:-.02em; }
h2 { font-size:1.24rem; line-height:1.35; margin:0 0 12px; scroll-margin-top:14px; }
h3 { font-size:1.08rem; line-height:1.4; margin:16px 0 8px; scroll-margin-top:14px; }
h4, h5, h6 { font-size:1rem; line-height:1.4; margin:14px 0 8px; scroll-margin-top:14px; }
p { margin:10px 0; }
p, li, blockquote, td, th { font-size:1rem; overflow-wrap:anywhere; word-break:break-word; }
.meta { color:#334155; font-size:.94rem; background:#f1f5f9; border:1px solid #e2e8f0; border-radius:14px; padding:10px 12px; }
.notice { color:#7c2d12; background:#fff7ed; border:1px solid #fed7aa; border-left:5px solid var(--orange); border-radius:14px; padding:11px 12px; font-weight:600; }
.highlight { background:#eef2ff; border:1px solid #c7d2fe; border-radius:14px; padding:10px 12px; font-weight:650; }
ul, ol { padding-left:1.35rem; margin:10px 0; }
li + li { margin-top:6px; }
a { color:#1d4ed8; text-decoration-thickness:1px; text-underline-offset:3px; overflow-wrap:anywhere; word-break:break-all; }
a:focus, a:hover { background:#dbeafe; border-radius:8px; }
.toc a { display:block; min-height:44px; padding:10px 12px; margin:8px 0; border-radius:14px; background:linear-gradient(90deg,#eef2ff,#f8fafc); border:1px solid #dbeafe; text-decoration:none; font-weight:650; }
blockquote { margin:12px 0; padding:11px 13px; border-left:5px solid var(--blue); background:#eff6ff; border-radius:12px; color:var(--muted); }
code { background:#f1f5f9; border-radius:7px; padding:1px 5px; }
pre { background:#0f172a; color:#e5e7eb; padding:14px; border-radius:16px; overflow:auto; white-space:pre-wrap; }
.rank-calc, .card-rank pre { background:#050505; color:#ff2d2d; border:1px solid #7f1d1d; border-left:6px solid #ef4444; border-radius:16px; padding:12px 13px; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace; font-weight:700; }
.rank-calc code, .card-rank pre code { background:transparent; color:#ff2d2d; padding:0; }
.table-wrap { width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch; margin:12px 0; border-radius:14px; border:1px solid var(--line); }
table { width:100%; border-collapse:collapse; min-width:520px; background:#fff; }
th, td { border:1px solid var(--line); padding:10px; vertical-align:top; }
th { background:#f1f5f9; text-align:left; }
hr { border:0; border-top:1px dashed #cbd5e1; margin:16px 0; }
@media (min-width:760px) { main { padding:28px; } .hero, .card { padding:24px; } h1 { font-size:1.95rem; } h2 { font-size:1.36rem; } }
@media print { body { background:#fff; } .hero, .card { box-shadow:none; break-inside:avoid; } }
"""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="format-detection" content="telephone=no">
  <meta name="color-scheme" content="light">
  {HTML_GENERATOR_META}
  <title>{html.escape(title)}</title>
  <style>
{css}
  </style>
</head>
<body>
  <main>
{body}
  </main>
</body>
</html>
"""

def cmd_markdown_to_html(args: argparse.Namespace) -> int:
    md_path = Path(args.report)
    md = read_text(md_path)
    requested = Path(args.out) if args.out else md_path.with_suffix(".html")
    fallback_title = title_from_filename(requested.name) or title_from_filename(md_path.name)
    title = args.title or title_from_markdown(md, fallback=fallback_title)
    if report_title_is_bad(title):
        title = title_from_markdown(md, fallback=fallback_title)
    out = safe_output_path(requested, title, ".html")
    out.write_text(static_html_document(md, title), encoding="utf-8")
    print(json.dumps({"ok": True, "html": str(out), "title": clean_report_title(title)}, ensure_ascii=False, indent=2))
    return 0



class StrictHTMLSyntaxParser(HTMLParser):
    """Small standard-library HTML stack checker for WebView-safe reports.

    HTMLParser is forgiving, so this class adds a deterministic stack for the
    subset of HTML emitted by CoopLensStaticHTML. It catches the cases that
    caused mobile parse failures: missing closing tags, unexpected end tags,
    duplicated document shells, or head/body/main order mistakes.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.starts: dict[str, int] = {}
        self.ends: dict[str, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        self.starts[t] = self.starts.get(t, 0) + 1
        if t not in HTML_VOID_TAGS:
            self.stack.append(t)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        self.starts[t] = self.starts.get(t, 0) + 1
        self.ends[t] = self.ends.get(t, 0) + 1

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        self.ends[t] = self.ends.get(t, 0) + 1
        if t in HTML_VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing tag </{t}> with empty stack")
            return
        if self.stack[-1] == t:
            self.stack.pop()
            return
        if t in self.stack:
            expected = self.stack[-1]
            self.errors.append(f"misnested closing tag </{t}>; expected </{expected}> before it")
            while self.stack and self.stack[-1] != t:
                self.stack.pop()
            if self.stack and self.stack[-1] == t:
                self.stack.pop()
            return
        self.errors.append(f"unexpected closing tag </{t}>; no matching start tag")


def html_syntax_errors(text: str) -> list[str]:
    errors: list[str] = []
    parser = StrictHTMLSyntaxParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:
        errors.append(f"HTML parser failed: {exc}")
        return errors
    errors.extend(parser.errors)
    if parser.stack:
        errors.append("unclosed HTML tags: " + " > ".join(parser.stack[-8:]))
    for tag in ["html", "head", "body", "main"]:
        if parser.starts.get(tag, 0) != 1:
            errors.append(f"HTML syntax requires exactly one <{tag}> tag, found {parser.starts.get(tag, 0)}")
        if parser.ends.get(tag, 0) != 1:
            errors.append(f"HTML syntax requires exactly one </{tag}> tag, found {parser.ends.get(tag, 0)}")
    # The generated report must be a normal document, not a fragment whose
    # parts were accidentally concatenated in a wrong order.
    ordered_terms = ["<html", "<head", "</head>", "<body", "<main", "</main>", "</body>", "</html>"]
    low = text.lower()
    cursor = -1
    for term in ordered_terms:
        pos = low.find(term)
        if pos == -1:
            continue
        if pos < cursor:
            errors.append(f"HTML document order is invalid near {term}")
            break
        cursor = pos
    if low.count("<!doctype html") != 1:
        errors.append(f"HTML syntax requires exactly one <!doctype html>, found {low.count('<!doctype html')}")
    return errors

def html_report_errors(text: str) -> list[str]:
    low = text.lower()
    errors: list[str] = []
    errors.extend(html_syntax_errors(text))
    required = ["<!doctype html", "<html", "</html>", "<head", "</head>", "<meta charset", "viewport", "format-detection", "<style", "</style>", "<body", "</body>", "<main", "</main>"]
    for term in required:
        if term not in low:
            errors.append(f"static HTML missing required item: {term}")
    if HTML_GENERATOR_META.lower() not in low:
        errors.append("static HTML was not produced by the current safe renderer; rebuild from Markdown with safe-html-build")
    if '<header class="hero"' not in low or "<h1" not in low:
        errors.append("static HTML missing visible hero title; add an H1 title before rendering")
    title_match = re.search(r"<title>([\s\S]*?)</title>", text, flags=re.I)
    browser_title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))).strip() if title_match else ""
    if not title_match:
        errors.append("static HTML missing browser <title>")
    elif report_title_is_bad(browser_title):
        errors.append(f"static HTML has invalid browser title, usually caused by using the TOC as title: {browser_title!r}")
    if "<title>cooplens report</title>" in low:
        errors.append("static HTML has generic browser title; use a task-derived report title")
    h1_texts = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"<h1\b[^>]*>([\s\S]*?)</h1>", text, flags=re.I)]
    if not h1_texts:
        errors.append("static HTML missing visible H1 hero title")
    else:
        for h1 in h1_texts:
            if report_title_is_bad(h1):
                errors.append(f"static HTML has invalid hero title, usually caused by missing task H1 before the TOC: {h1!r}")
    if re.search(r"CoopLens\s+Skill\s+v?\d", text, flags=re.I):
        errors.append("static HTML exposes internal version/generator wording in visible content")
    if re.search(r"<p[^>]*>\s*---\s*</p>", text):
        errors.append("static HTML contains visible Markdown separator paragraphs; render separators as <hr>")
    visible = visible_text_from_html(text)
    if DISCLAIMER not in visible:
        errors.append("static HTML missing visible fixed important statement")
    errors.extend(check_strict_important_statement(visible))
    errors.extend(check_no_blanket_claims(visible))
    if "附录" in visible or "报告" in visible:
        if "附录：重要声明" not in visible and "附录 重要声明" not in visible:
            errors.append("static HTML missing appendix important statement section")
    if "位次预估" in visible and "位次预估重要声明" not in visible:
        errors.append("static HTML rank section missing visible rank-estimation important statement heading")
    if "目录" in visible and '<a href="#' not in low:
        errors.append("static HTML TOC does not contain clickable internal anchors")
    for css_term in ["linear-gradient", "card-rank", "card-auth", "card-conclusion", "notice", "toc a", "rank-calc", "#ff2d2d"]:
        if css_term not in low:
            errors.append(f"mobile/color CSS missing: {css_term}")
    paired_tags = ["main", "section", "article", "nav", "ul", "ol", "table", "tr", "td", "th", "blockquote", "pre", "code"]
    for tag in paired_tags:
        opens = len(re.findall(fr"<{tag}(?:\s|>|/)", low))
        closes = low.count(f"</{tag}>")
        if opens != closes:
            errors.append(f"static HTML has unbalanced <{tag}> tags: open={opens}, close={closes}")
    if re.search(r"\[[^\]]+\]\((?:https?://|#)[^)]+\)", text):
        errors.append("static HTML still contains unrendered Markdown links")
    if "&amp;amp;" in low:
        errors.append("static HTML contains double-escaped URL/entity text: &amp;amp;")
    forbidden = ["<script", "javascript:", "cdn.", "bootstrap", "tailwind", "jquery", "<iframe", "<canvas", "<img", "background-image", "onload=", "onclick="]
    for term in forbidden:
        if term in low:
            errors.append(f"static HTML contains forbidden item: {term}")
    for css_term in ["overflow-wrap", "word-break", "max-width", "line-height", "@media", "-webkit-text-size-adjust"]:
        if css_term not in low:
            errors.append(f"mobile CSS missing: {css_term}")
    if re.search(r"\[[^\]]+\]\((?:#|https?://)", text):
        errors.append("raw Markdown link syntax remains visible in static HTML")
    for tag in ["html", "body", "main", "section", "nav"]:
        opens = len(re.findall(fr"<{tag}(?:\s|>|/)", low))
        closes = len(re.findall(fr"</{tag}>", low))
        if opens != closes:
            errors.append(f"HTML tag mismatch for <{tag}>: opens={opens}, closes={closes}")
    if re.search(r"(?m)^#{1,6}\s+", text):
        errors.append("raw Markdown heading marker appears in HTML; Markdown was not fully rendered")

    ids = re.findall(r'\bid=["\']([^"\']+)["\']', text)
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in ids:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    for item in sorted(duplicates):
        errors.append(f"duplicate HTML id breaks section navigation: {item}")
    for item in ids:
        if not ASCII_ID_PATTERN.fullmatch(item):
            errors.append(f"HTML id is not mobile-WebView-safe ASCII: {item}")
    for href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']', text, flags=re.I):
        if href.startswith("#"):
            anchor = href[1:]
            if not ASCII_ID_PATTERN.fullmatch(anchor):
                errors.append(f"internal href is not mobile-WebView-safe ASCII: {href}")
            if anchor not in seen:
                errors.append(f"TOC/internal anchor target missing: {href}")
        elif href.startswith("http://") or href.startswith("https://"):
            if not SAFE_EXTERNAL_HREF_PATTERN.fullmatch(href) or href.rstrip(BAD_HREF_TRAILING) != href:
                errors.append(f"external href is malformed or WebView-unsafe: {href}")
        else:
            errors.append(f"href uses unsupported scheme or malformed value: {href}")

    errors.extend(check_no_public_terms(text))
    errors.extend(check_no_doc_export_terms(text))
    return errors


def html_consistency_errors(markdown: str, html_text: str) -> list[str]:
    visible = visible_text_from_html(html_text)
    errors: list[str] = []
    for level, title, _slug in extract_headings(markdown):
        if level == 1 and report_title_is_bad(title):
            # safe-html-build replaces bad H1 values such as `## 目录` with a
            # task-derived title, so the original broken title should not be
            # required to appear in the final page.
            continue
        if title and title not in visible:
            errors.append(f"heading missing from HTML: {title}")
    for phrase in [DISCLAIMER, "检索执行日期", "参考来源与核验说明"]:
        if phrase in markdown and phrase not in visible:
            errors.append(f"key phrase missing from HTML: {phrase}")
    if len(visible) < max(100, len(re.sub(r"[#*`\[\]()\-]", "", markdown)) * 0.45):
        errors.append("HTML visible text is unexpectedly short compared with Markdown")
    return errors


def repair_markdown_for_html_attempt(md: str, title: str, errors: list[str], attempt_no: int) -> str:
    """Deterministically repair common Markdown causes of HTML parse failures."""
    repaired = ensure_static_markdown_shape(md, title)
    repaired = repair_markdown_toc(repaired)
    if any("title" in e.lower() or "hero" in e.lower() or "H1" in e for e in errors):
        clean = clean_report_title(title) or title_from_markdown(repaired)
        lines = repaired.splitlines()
        replaced = False
        for i, line in enumerate(lines):
            if re.match(r"^#\s+", line):
                lines[i] = f"# {clean}"
                replaced = True
                break
        if not replaced:
            lines.insert(0, f"# {clean}")
        repaired = "\n".join(lines) + "\n"
    if any("raw Markdown" in e or "Markdown heading" in e for e in errors):
        # Remove accidental fenced metadata or stray heading markers inside normal lines.
        repaired = re.sub(r"(?m)^(?!#{1,6}\s)(\s*)#{1,6}\s+", r"\1", repaired)
    if any("href" in e or "link" in e or "URL" in e for e in errors):
        repaired = re.sub(r"\]\((https?://[^)\s]+)[^\x00-\x7F)]+\)", r"](\1)", repaired)
    if attempt_no >= 2:
        repaired = re.sub(r"(?m)^\s*---+\s*$", "---HR---", repaired)
    if attempt_no >= 3:
        # Rebuild TOC after all other changes, because duplicate or changed headings
        # are the most common source of navigation mismatches in function 3 pages.
        repaired = repair_markdown_toc(repaired)
    if attempt_no >= 4:
        # Last deterministic cleanup: collapse excessive blank lines and strip HTML fragments.
        repaired = re.sub(r"<\/?(?:html|head|body|main|section|nav|script|style)[^>]*>", "", repaired, flags=re.I)
        repaired = re.sub(r"\n{3,}", "\n\n", repaired)
    return repaired


def build_static_html_with_gate(md: str, title: str, max_attempts: int = HTML_REBUILD_MAX_ATTEMPTS) -> tuple[str, list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    candidate_md = md
    last_html = ""
    last_errors: list[str] = []
    seen_signatures: set[str] = set()
    for attempt_no in range(1, max(1, max_attempts) + 1):
        label = "original_markdown" if attempt_no == 1 else f"auto_rebuild_attempt_{attempt_no}"
        html_text = static_html_document(candidate_md, title)
        errors = html_report_errors(html_text) + html_consistency_errors(candidate_md, html_text)
        last_html = html_text
        last_errors = errors
        attempts.append({"attempt": label, "ok": not errors, "errors": errors})
        if not errors:
            return html_text, attempts
        signature = hashlib.sha1((candidate_md + "\n" + "\n".join(errors)).encode("utf-8", errors="ignore")).hexdigest()
        if signature in seen_signatures and attempt_no >= 2:
            break
        seen_signatures.add(signature)
        candidate_md = repair_markdown_for_html_attempt(candidate_md, title, errors, attempt_no)
    if attempts and attempts[-1].get("errors") != last_errors:
        attempts.append({"attempt": "stopped_without_pass", "ok": False, "errors": last_errors})
    return last_html, attempts


def cmd_html_report_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.html))
    errors = html_report_errors(text)
    return result(not errors, errors)


def cmd_html_syntax_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.html))
    errors = html_syntax_errors(text)
    return result(not errors, errors)



def cmd_html_important_statement_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.html))
    visible = visible_text_from_html(text)
    errors: list[str] = []
    if DISCLAIMER not in visible:
        errors.append("fixed important statement is not visible in HTML")
    errors.extend(check_strict_important_statement(visible))
    errors.extend(check_no_blanket_claims(visible))
    if "位次预估" in visible and "位次预估重要声明" not in visible:
        errors.append("rank-estimation important statement heading is not visible in HTML")
    if "目录" in visible and '<a href="#' not in text.lower():
        errors.append("HTML table of contents lacks clickable section anchors")
    return result(not errors, errors)


def cmd_html_consistency_check(args: argparse.Namespace) -> int:
    md = read_text(Path(args.markdown))
    ht = read_text(Path(args.html))
    errors = html_consistency_errors(md, ht)
    return result(not errors, errors)


def cmd_safe_html_build(args: argparse.Namespace) -> int:
    md_path = Path(args.report)
    md = read_text(md_path)
    requested = Path(args.out) if args.out else md_path.with_suffix(".html")
    fallback_title = title_from_filename(requested.name) or title_from_filename(md_path.name)
    title = args.title or title_from_markdown(md, fallback=fallback_title)
    if report_title_is_bad(title):
        title = title_from_markdown(md, fallback=fallback_title)
    out = safe_output_path(requested, title, ".html")
    html_text, attempts = build_static_html_with_gate(md, title)
    final_errors = attempts[-1]["errors"] if attempts else ["html build did not run"]
    if final_errors:
        failed_out = out.with_suffix(".failed.html")
        failed_out.write_text(html_text, encoding="utf-8")
        if args.error_out:
            Path(args.error_out).write_text(json.dumps({"ok": False, "attempts": attempts, "failed_html": str(failed_out)}, ensure_ascii=False, indent=2), encoding="utf-8")
        return result(False, final_errors, attempts=attempts, failed_html=str(failed_out), instruction=f"HTML 语法校验/渲染闸门未通过；已自动重建 {len(attempts)} 次。反馈失败原因后，继续修正 Markdown 并再次运行 safe-html-build，直到 html-syntax-check、html-report-check、html-render-gate-check 全部通过；不要交付失败 HTML。")
    out.write_text(html_text, encoding="utf-8")
    if args.error_out:
        Path(args.error_out).write_text(json.dumps({"ok": True, "attempts": attempts, "html": str(out)}, ensure_ascii=False, indent=2), encoding="utf-8")
    return result(True, [], html=str(out), title=clean_report_title(title), regenerated=any(a["attempt"] != "original_markdown" and a["ok"] for a in attempts), attempts=attempts)


def cmd_html_render_gate_check(args: argparse.Namespace) -> int:
    md = read_text(Path(args.markdown))
    ht = read_text(Path(args.html))
    errors = html_report_errors(ht) + html_consistency_errors(md, ht)
    if any(t in md for t in ["候选", "按省份", "同分段", "可选项目", "找项目"]):
        # Function 3 pages are long and card-heavy; require all internal TOC links to resolve.
        ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', ht))
        hrefs = re.findall(r'<a\b[^>]*\bhref=["\']#([^"\']+)["\']', ht, flags=re.I)
        if hrefs and not all(h in ids for h in hrefs):
            errors.append("Function 3 HTML navigation has unresolved TOC/internal anchors")
    return result(not errors, errors)



def cmd_report_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(check_disclaimer_and_date(text))
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_appendix_important_statement(text))
    errors.extend(check_function3_structure(text))
    errors.extend(check_no_public_terms(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_no_doc_export_terms(text))
    errors.extend(check_current_admission_status_text(text))
    errors.extend(check_batch_distinction_text(text))
    errors.extend(critical_data_source_errors(text))
    if "## 目录" not in text:
        errors.append("Markdown report missing table of contents")
    if not any(section in text for section in ["结论先行", "最重要建议"]):
        errors.append("required section missing: 结论先行 or 最重要建议")
    for section in ["最新官方材料核验", "位次预估", "留服认证路径与风险", "毕业成果", "公开讨论", "家长应向学校确认的问题", "参考来源与核验说明"]:
        if section not in text:
            errors.append(f"required section missing: {section}")
    if not any(t in text for t in ["家庭画像", "家庭", "预算压力", "出国偏好"]):
        errors.append("required personalized family-fit section missing")
    # Inline check equivalents for recommendation split and rank workflow.
    if any(t in text for t in ["推荐", "优先", "备选", "观察", "慎选", "适合", "不适合"]):
        for name, terms in RECOMMENDATION_SPLIT_TERMS.items():
            if not any(t in text for t in terms):
                errors.append(f"recommendation split missing: {name}")
        for exact_label in ["个性化推荐度评价（学生/家庭适配）", "项目综合实力推荐度评价（项目综合实力角度）"]:
            if exact_label not in text:
                errors.append(f"required recommendation label missing: {exact_label}")
    if any(t in text for t in ["位次", "分数线", "投档线", "预测", "估计", "估算"]):
        for name, terms in RANK_WORKFLOW_TERMS.items():
            if not any(t in text for t in terms):
                errors.append(f"rank workflow missing: {name}")
    cscse_result = check_cscse_authentication_text(text)
    errors.extend(cscse_result)
    errors.extend(check_overseas_living_cost_text(text))
    if any(t in text for t in ["本年", "今年", "预测", "估计", "估算"]) and any(t in text for t in ["位次", "排位", "分数线", "投档线"]):
        for field in RANK_REASONING_FIELDS:
            if field not in text:
                errors.append(f"required rank reasoning field missing: {field}")
    if not any(term in text for term in ["优先候选", "备选候选", "观察候选", "慎选候选", "暂不建议", "总体排序"]):
        errors.append("report must provide a non-neutral conclusion or grouping")
    if not any(term in text for term in ["推翻", "反转", "会被", "如果", "若", "除非"]):
        warnings.append("reversal condition not obvious")
    return result(not errors, errors, warnings)


def cmd_numeric_link_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    linked_spans = [(m.start(1), m.end(1)) for m in MD_LINK_PATTERN.finditer(text)]
    errors: list[str] = []
    annotations: list[tuple[int, str]] = []
    for m in NUMERIC_PATTERN.finditer(text):
        value = m.group(0).strip()
        if not value or len(value) < 2:
            continue
        context = text[max(0, m.start()-20):m.end()+20]
        if not any(k in context for k in ["分", "位", "排名", "率", "学费", "费用", "计划", "人数", "万元", "%", "名", "QS", "软科", "位次"]):
            continue
        inside_link = any(a <= m.start() <= b for a, b in linked_spans)
        if not inside_link and not ("cite" in context or "来源" in context):
            errors.append(f"numeric value may lack direct source link: {value}")
            annotations.append((m.end(), "【未满足：数字未直接链接来源】"))
    if args.annotate_out:
        annotated = text
        offset = 0
        for pos, mark in annotations:
            annotated = annotated[:pos+offset] + mark + annotated[pos+offset:]
            offset += len(mark)
        Path(args.annotate_out).write_text(annotated, encoding="utf-8")
    return result(not errors, errors, checked_numbers=len(errors) + len(linked_spans))



def cmd_critical_data_source_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = critical_data_source_errors(text)
    items = critical_evidence_items(text)
    return result(not errors, errors, checked_critical_lines=len(items))


def cmd_critical_source_evidence_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = critical_data_source_errors(text)
    if not errors:
        errors.extend(critical_source_evidence_errors(text, timeout=args.timeout, max_lines=args.max_lines))
    return result(not errors, errors)


def cmd_pure_report_file_check(args: argparse.Namespace) -> int:
    errors: list[str] = []
    errors.extend(pure_target_file_errors(str(args.html), "html"))
    errors.extend(pure_target_file_errors(str(args.markdown), "md"))
    return result(not errors, errors, html=str(args.html), markdown=str(args.markdown))


def cmd_consolidated_source_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors: list[str] = []
    if "参考来源与核验说明" not in text:
        errors.append("final consolidated source section missing")
    if not URL_PATTERN.search(text) and not MD_LINK_PATTERN.search(text) and "filecite" not in text and "cite" not in text:
        errors.append("no clickable/cited source detected")
    if len(re.findall(r"(?:数据来源|来源链接|原文链接)[:：]", text)) > 6:
        errors.append("too many repeated per-module source labels; consolidate sources at the end")
    return result(not errors, errors)


def cmd_official_latest_source_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    groups = {
        "runtime date": ["检索执行日期"],
        "current admissions": ["招生简章", "招生章程", "招生计划", "专业目录"],
        "current admission status gate": ["当年是否招生", "招生状态", "继续招生", "未在当年招生计划中", "停招", "暂停招生"],
        "score line": ["分数线", "投档线", "录取线", "位次", "一分一段"],
        "official authority": ["官方", "权威", "教育考试院", "省考试院", "CRS", "教育部", "本科招生网"],
        "latest/current wording": ["当前年份", "最新", "最近完成", "今年", "当年"],
        "batch/major group": ["招生批次", "院校专业组", "专业组", "批次控制线"],
    }
    errors = [name for name, terms in groups.items() if not any(t in text for t in terms)]
    return result(not errors, [f"latest official-source bundle missing: {name}" for name in errors])


def cmd_function3_deep_analysis_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["候选", "按省份", "同分段", "可选项目", "项目可选", "找项目"])
    errors: list[str] = []
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_function3_structure(text))
    if triggered:
        groups = {
            "candidate cards": ["候选项目卡片", "候选卡", "项目卡片"],
            "advantages": ["核心优势", "优势", "亮点"],
            "disadvantages": ["主要缺点", "缺点", "风险", "短板"],
            "possible rank": ["预测可能位次", "参考区间", "冲/稳/保", "位次预估"],
            "current admission status": ["当年是否招生", "招生状态", "继续招生", "未在当年招生计划中", "停招", "暂停招生"],
            "batch口径": ["招生批次", "院校专业组", "同批次", "批次未核到"],
            "graduate study": ["升学", "出国/境申硕", "考研", "保研", "推免"],
            "employment": ["就业", "知名企业", "重点行业", "就业去向"],
            "budget/cost": ["家庭预算", "年度预算", "四年总投入", "预算差额", "费用"],
            "certificate/cscse": ["证书", "留服", "CSCSE", "学籍", "计划内"],
            "recommendation split": ["项目综合实力推荐度评价（项目综合实力角度）", "个性化推荐度评价（学生/家庭适配）"],
            "watchlist boundary": ["仅关注/待核验", "不参与排序", "证据不足", "未核到"],
        }
        for name, terms in groups.items():
            if not any(t in text for t in terms):
                errors.append(f"Function 3 deep analysis missing: {name}")
    return result(not errors, errors, triggered=triggered)


def cmd_personalized_input_use_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered_budget = "预算" in text or "每年" in text or "年度" in text
    triggered_rank = "位次" in text or "排名" in text or "排位" in text
    errors: list[str] = []
    if triggered_rank:
        for term in ["安全边际", "差距", "冲/稳/保"]:
            if term not in text:
                errors.append(f"rank input not concretely used: {term}")
    if triggered_budget:
        for term in ["年度预算", "四年总投入", "预算差额", "预算压力"]:
            if term not in text:
                errors.append(f"budget input not concretely used: {term}")
    return result(not errors, errors, triggered_rank=triggered_rank, triggered_budget=triggered_budget)


def cmd_overseas_living_cost_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = check_overseas_living_cost_text(text)
    return result(not errors, errors, triggered=bool(errors) or any(t in text for t in ["境外阶段", "海外阶段", "出国阶段", "境外学习", "海外学习", "必须出国", "需要出国", "明确出国", "愿意出国", "2+2", "3+1", "1+3", "外方大学所在城市"]))


def cmd_artifact_filename_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors: list[str] = []
    names = set(re.findall(r"[\w\-.\u4e00-\u9fff ]+\.(?:md|html)", text, flags=re.I))
    for name in names:
        clean = name.strip()
        if artifact_name_is_bad(clean):
            errors.append(f"artifact filename is generic or platform-derived: {clean}")
    if not names and any(t in text for t in ["Markdown", "HTML", "静态页面"]):
        errors.append("artifact delivery mentioned but no .md/.html filename found")
    return result(not errors, errors, checked=len(names))


def cmd_live_rank_estimation_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    groups = {
        "runtime/current": ["检索执行日期", "当前年份", "实时"],
        "official plan": ["招生计划", "专业目录", "省考试院", "教育考试院", "本科招生网"],
        "current admission status gate": ["当年是否招生", "招生状态", "继续招生", "未在当年招生计划中", "停招", "暂停招生"],
        "latest completed line": ["最近完成", "最新完成", "分数线", "投档线", "位次"],
        "one-score-one-rank": ["一分一段", "位次转换"],
        "comparison basis": ["同校普通", "同省同档", "普通招生基线", "位次差样本"],
        "batch separation": ["招生批次", "院校专业组", "同招生批次", "批次未核到", "不同批次"],
    }
    errors = [f"rank-estimation evidence missing: {name}" for name, terms in groups.items() if not any(t in text for t in terms)]
    errors.extend(check_current_admission_status_text(text))
    errors.extend(check_batch_distinction_text(text))
    errors.extend(critical_data_source_errors(text))
    return result(not errors, errors)


def cmd_function3_estimation_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    is_new = any(t in text for t in ["新项目", "首次招生", "首招", "新获批", "无历史线", "暂无历史线", "没有历史线"])
    errors: list[str] = []
    required = ["B普通招生基线", "A同省同档", "门槛偏高", "中性", "门槛偏宽", "公式", "样本", "不是今年录取预测"]
    if is_new:
        for term in required:
            if term not in text:
                errors.append(f"new/no-history estimation missing: {term}")
    if "仅关注/待核验，不参与排序" in text and not any(t in text for t in ["缺少", "未核到", "证据不足", "待核验"]):
        errors.append("watchlist item must state the missing evidence")
    errors.extend(check_current_admission_status_text(text))
    errors.extend(check_batch_distinction_text(text))
    errors.extend(critical_data_source_errors(text))
    if args.annotate_out:
        annotated = text
        if errors:
            annotated += "\n\n" + "\n".join(f"【未满足：{e}】" for e in errors)
        Path(args.annotate_out).write_text(annotated, encoding="utf-8")
    return result(not errors, errors, new_or_no_history_detected=is_new)


def cmd_rank_reasoning_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["本年", "今年", "预测", "估计", "估算"]) and any(t in text for t in ["位次", "排位", "分数线", "投档线"])
    errors: list[str] = []
    if triggered:
        for term in RANK_REASONING_FIELDS:
            if term not in text:
                errors.append(f"rank reasoning missing: {term}")
        if not re.search(r"[=＝+＋\-−]", text):
            errors.append("rank reasoning missing: formula or arithmetic")
        if not any(t in text for t in ["强", "中", "弱", "弱参照", "中等置信", "低置信"]):
            errors.append("rank reasoning missing: confidence strength")
        if not any(t in text for t in ["如果", "若", "调整", "推翻", "降为", "反转"]):
            errors.append("rank reasoning missing: reversal/adjustment condition")
        errors.extend(check_batch_distinction_text(text))
        errors.extend(critical_data_source_errors(text))
    return result(not errors, errors, triggered=triggered)


def cmd_personalization_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["适合", "不适合", "建议", "优先", "备选", "观察", "慎选"])
    errors: list[str] = []
    if triggered:
        for name, terms in PERSONALIZATION_GROUPS.items():
            if not any(t in text for t in terms):
                errors.append(f"personalized advice missing: {name}")
        if not any(t in text for t in ["未提供", "三情景", "如果", "若", "按"]):
            errors.append("personalized advice missing: scenario handling for missing family data")
    return result(not errors, errors, triggered=triggered)



def cmd_rank_workflow_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["位次", "分数线", "投档线", "冲", "稳", "保", "预测", "估计", "估算"])
    errors: list[str] = []
    if triggered:
        for name, terms in RANK_WORKFLOW_TERMS.items():
            if not any(t in text for t in terms):
                errors.append(f"rank workflow missing: {name}")
        order_terms = ["位次预估结论先行", "可验证数据统计", "位差与线差分析", "本年位次估计"]
        positions = [text.find(t) for t in order_terms]
        if all(pos != -1 for pos in positions) and positions != sorted(positions):
            errors.append("rank workflow order must be conclusion -> statistics -> analysis -> prediction")
        if any(t in text for t in ["新项目", "首次招生", "首招", "无历史线", "暂无历史线"]):
            for term in ["门槛偏高", "中性", "门槛偏宽"]:
                if term not in text:
                    errors.append(f"new/no-history scenario missing: {term}")
        errors.extend(check_batch_distinction_text(text))
        errors.extend(critical_data_source_errors(text))
    return result(not errors, errors, triggered=triggered)


def cmd_manual_source_confirmation_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["位次", "分数线", "投档线", "QS", "排名", "学费", "招生计划"])
    errors: list[str] = []
    if triggered:
        for term in ["人工确认", "打开链接", "年份", "省份", "科类", "招生批次", "专业组", "计划类型", "数值"]:
            if term not in text:
                errors.append(f"manual source confirmation missing: {term}")
        if not (URL_PATTERN.search(text) or MD_LINK_PATTERN.search(text) or "cite" in text):
            errors.append("manual confirmation requires clickable/cited sources")
        if "质量等级" not in text and not any(t in text for t in ["A级", "B级", "C级", "D级"]):
            errors.append("data quality grade missing")
        errors.extend(check_current_admission_status_text(text))
        errors.extend(check_batch_distinction_text(text))
        errors.extend(critical_data_source_errors(text))
    return result(not errors, errors, triggered=triggered)


def cmd_batch_distinction_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = check_batch_distinction_text(text)
    triggered = any(term in text for term in BATCH_DISTINCTION_TRIGGER_TERMS)
    return result(not errors, errors, triggered=triggered)


def cmd_current_admission_status_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = check_current_admission_status_text(text)
    triggered = any(term in text for term in CURRENT_ADMISSION_STATUS_TRIGGER_TERMS)
    return result(not errors, errors, triggered=triggered)


def cmd_qs_latest_ranking_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = "QS" in text or "TopUniversities" in text or "世界大学排名" in text
    errors: list[str] = []
    if triggered:
        if "QS World University Rankings 2027" not in text and "QS官方最新" not in text and "TopUniversities" not in text:
            errors.append("QS ranking mention must identify the runtime latest official QS edition")
        if "2026" in text and "QS" in text and "2027" not in text:
            errors.append("QS 2026 appears without acknowledging newer official 2027 edition")
        if not any(t in text for t in ["topuniversities.com", "QS官方", "TopUniversities", "官方榜单"]):
            errors.append("QS ranking must be linked or explicitly tied to official QS/TopUniversities source")
        if not any(t in text for t in ["背景", "不能替代", "不等于", "排名只是"]):
            errors.append("QS ranking boundary missing: ranking must not substitute for project quality/admission value")
    return result(not errors, errors, triggered=triggered)


def cmd_recommendation_split_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    triggered = any(t in text for t in ["推荐", "优先", "备选", "观察", "慎选", "适合", "不适合"])
    errors: list[str] = []
    if triggered:
        for name, terms in RECOMMENDATION_SPLIT_TERMS.items():
            if not any(t in text for t in terms):
                errors.append(f"recommendation split missing: {name}")
        if not any(t in text for t in ["强", "较强", "中等", "偏弱", "高风险"]):
            errors.append("project-strength rating level missing")
        if not any(t in text for t in ["高度适合", "边界适合", "不太适合", "不适合", "适合"]):
            errors.append("personal-fit rating level missing")
    return result(not errors, errors, triggered=triggered)

def cmd_public_platform_search_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = []
    errors.extend(check_no_public_terms(text))
    groups = {
        "public discussion": ["公开讨论", "公开口碑", "网络讨论"],
        "neutral search terms": ["中性检索词", "检索词"],
        "themes": ["正面主题", "负面担忧", "反驳", "澄清", "信号强弱"],
        "fact boundary": ["不作为官方事实", "不能证明", "需要官方确认", "书面确认"],
    }
    for name, terms in groups.items():
        if not any(t in text for t in terms):
            errors.append(f"public-discussion module missing: {name}")
    return result(not errors, errors)


def cmd_negative_consultation_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    groups = {
        "negative concern": ["负面担忧", "质疑", "担忧", "争议"],
        "official answer path": ["官方", "权威", "教育考试院", "学校官网", "本科招生网", "政府", "教育主管部门"],
        "school consultation": ["向学校", "招生办", "学院", "教务", "就业", "国际", "书面确认", "邮件"],
        "decision impact": ["对判断的影响", "会把", "降为", "推翻", "权重"],
    }
    errors = [f"negative-concern handling missing: {name}" for name, terms in groups.items() if not any(t in text for t in terms)]
    return result(not errors, errors)


def cmd_graduate_outcomes_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    groups = {
        "outcome module": ["毕业成果", "培养成果", "已有毕业生"],
        "scope label": ["项目级", "学院/机构级", "学校级", "暂无本项目毕业生公开成果", "未核到"],
        "selective study or employer": ["世界知名大学", "世界名校", "知名企业", "重点行业", "深造", "就业"],
        "research/awards": ["一作", "第一作者", "高水平论文", "科研", "竞赛", "专利", "奖学金", "成果"],
        "privacy": ["不列姓名", "不透露姓名", "不展示姓名", "不含姓名", "不写姓名"],
    }
    errors = [f"graduate-outcomes module missing: {name}" for name, terms in groups.items() if not any(t in text for t in terms)]
    return result(not errors, errors)



def check_overseas_living_cost_text(text: str) -> list[str]:
    triggered = any(t in text for t in ["境外阶段", "海外阶段", "出国阶段", "境外学习", "海外学习", "必须出国", "需要出国", "明确出国", "愿意出国", "2+2", "3+1", "1+3", "外方大学所在城市"])
    errors: list[str] = []
    if not triggered:
        return errors
    groups = {
        "city": ["外方大学所在城市", "所在城市", "校区"],
        "living cost module": ["境外城市生活成本", "生活成本", "生活费", "cost of living"],
        "cost components": ["住宿", "租金", "餐饮", "交通", "保险", "医疗", "签证", "教材"],
        "currency/exchange": ["汇率", "币种", "人民币", "CNY"],
        "budget gap": ["年度预算差额", "预算差额", "家庭年度预算", "预算压力"],
        "sources/manual": ["来源链接", "http://", "https://", "人工确认", "打开链接"],
    }
    for name, terms in groups.items():
        if not any(t in text for t in terms):
            errors.append(f"overseas living-cost analysis missing: {name}")
    return errors


def check_cscse_authentication_text(text: str) -> list[str]:
    triggered = any(t in text for t in ["外方学位", "境外", "出国", "4+0", "2+2", "3+1", "留服", "学历学位认证", "教育部留学服务中心", "证书"])
    errors: list[str] = []
    if not triggered:
        return errors
    for term in CSCSE_FORBIDDEN_CLAIMS:
        if term in text:
            errors.append(f"CSCSE authentication overpromise detected: {term}")
    for name, terms in CSCSE_GROUPS.items():
        if not any(t in text for t in terms):
            errors.append(f"CSCSE authentication module missing: {name}")
    if not any(t in text for t in ["教育部留学服务中心", "CSCSE", "中国留学网", "国家政务服务平台"]):
        errors.append("CSCSE authentication module must name the official CSCSE source target")
    if not any(t in text for t in ["CRS", "中外合作办学监管", "招生章程", "学校官网", "学校书面答复"]):
        errors.append("CSCSE authentication module must connect CSCSE with CRS/school certificate evidence")
    return errors


def cmd_cscse_authentication_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = check_cscse_authentication_text(text)
    return result(not errors, errors)


def cmd_parent_questions_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    groups = {
        "question section": ["家长应向学校确认的问题", "需要问学校", "提问清单"],
        "certificates": ["证书", "学籍", "学信网", "毕业证", "学位证", "留服认证", "教育部留学服务中心"],
        "cost/pressure": ["费用", "学费", "总投入", "延毕", "挂科", "GPA", "语言"],
        "resources/transfer": ["校区", "资源", "住宿", "转专业", "调剂"],
        "future path": ["就业", "保研", "推免", "考研", "出国", "升学", "留学生待遇", "传统海归"],
        "written confirmation": ["书面", "邮件", "官方确认", "招生章程", "培养方案"],
    }
    errors = [f"parent-question coverage missing: {name}" for name, terms in groups.items() if not any(t in text for t in terms)]
    return result(not errors, errors)


def cmd_postgraduate_recommendation_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = []
    if not any(t in text for t in ["保研", "推免"]):
        errors.append("postgraduate recommendation / 推免 discussion missing")
    if any(t in text for t in ["保研", "推免"]) and not any(t in text for t in ["官方", "推免办法", "名额", "学院", "未核到"]):
        errors.append("推免/保研 discussion lacks evidence boundary")
    return result(not errors, errors)


def cmd_function2_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    errors = []
    for term in ["结论先行", "总体排序", "专业与行业前景", "毕业成果", "公开讨论", "家长应向学校确认的问题"]:
        if term not in text:
            errors.append(f"Function 2 report missing: {term}")
    if not any(term in text for term in ["优先候选", "备选候选", "观察候选", "慎选候选"]):
        errors.append("Function 2 must group projects into useful recommendation buckets")
    if "|" in text and any(term in text for term in ["学校", "项目", "学费", "位次", "证书"]):
        errors.append("Function 2 should avoid dense wide Markdown tables; use cards or narrow lists")
    return result(not errors, errors)


def cmd_html_delivery_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors = check_disclaimer_and_date(text)
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(html_artifact_delivery_errors(text, allow_explicit_failure=False, check_local_files=True))
    errors.extend(check_no_doc_export_terms(text))
    if any(term in text for term in ["HTML 已生成", "静态页面已生成", "HTML 报告"]) and not final_answer_has_artifact(text, "html"):
        errors.append("final answer claims HTML/static page delivery but contains no .html download link")
    return result(not errors, errors, md_links=artifact_links_by_suffix(text, "md"), html_links=artifact_links_by_suffix(text, "html"), md_download_links=artifact_download_links_by_suffix(text, "md"), html_download_links=artifact_download_links_by_suffix(text, "html"))


def cmd_completion_gate_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors = check_disclaimer_and_date(text)
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_public_terms(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_no_doc_export_terms(text))
    errors.extend(html_artifact_delivery_errors(text, allow_explicit_failure=False, check_local_files=True))
    return result(not errors, errors, md_links=artifact_links_by_suffix(text, "md"), html_links=artifact_links_by_suffix(text, "html"), md_download_links=artifact_download_links_by_suffix(text, "md"), html_download_links=artifact_download_links_by_suffix(text, "html"))


def cmd_final_product_audit_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors = []
    errors.extend(check_disclaimer_and_date(text))
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_public_terms(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_no_doc_export_terms(text))
    for name in set(re.findall(r"[\w\-.\u4e00-\u9fff ]+\.(?:md|html)", text, flags=re.I)):
        if artifact_name_is_bad(name.strip()):
            errors.append(f"artifact filename is generic or platform-derived: {name.strip()}")
    if any(term in text for term in ["各有优劣", "看个人情况", "都可以考虑"]):
        errors.append("low-information neutral conclusion detected")
    return result(not errors, errors)


def cmd_function3_delivery_gate_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors = check_disclaimer_and_date(text)
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_no_doc_export_terms(text))
    errors.extend(check_no_public_terms(text))
    errors.extend(html_artifact_delivery_errors(text, allow_explicit_failure=False, check_local_files=True))
    if "功能3" in text or "功能 3" in text or "候选" in text or "按省份" in text:
        if not final_answer_has_artifact(text, "html"):
            errors.append("Function 3 final answer omitted the HTML artifact; keep regenerating until a passing .html file is produced")
    if final_answer_has_artifact(text, "html") and not any(term in text for term in ["html-render-gate-check", "safe-html-build", "HTML 校验", "静态页面校验", "已通过"]):
        errors.append("Function 3 final answer should state that safe-html-build/html-syntax-check/html-report-check/html-render-gate-check passed before linking the HTML")
    return result(not errors, errors, md_links=artifact_links_by_suffix(text, "md"), html_links=artifact_links_by_suffix(text, "html"), md_download_links=artifact_download_links_by_suffix(text, "md"), html_download_links=artifact_download_links_by_suffix(text, "html"))


def cmd_strict_final_delivery_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.final_answer))
    errors = []
    errors.extend(check_disclaimer_and_date(text))
    errors.extend(check_strict_important_statement(text))
    errors.extend(check_no_public_terms(text))
    errors.extend(check_no_blanket_claims(text))
    errors.extend(check_no_doc_export_terms(text))
    errors.extend(strict_pure_html_md_delivery_errors(text, check_local_files=True))
    return result(
        not errors,
        errors,
        html_download_targets=pure_download_targets_by_suffix(text, "html"),
        markdown_download_targets=pure_download_targets_by_suffix(text, "md"),
        archive_links=archive_artifact_links(text),
    )


def cmd_artifact_delivery_check(args: argparse.Namespace) -> int:
    return cmd_completion_gate_check(args)


def cmd_link_check(args: argparse.Namespace) -> int:
    text = read_text(Path(args.report))
    urls = list(dict.fromkeys(URL_PATTERN.findall(text)))[: args.max_urls]
    results = []
    errors = []
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CoopLens local link check"})
            with urllib.request.urlopen(req, timeout=args.timeout) as resp:
                status = getattr(resp, "status", None) or resp.getcode()
                ctype = resp.headers.get("content-type", "")
                results.append({"url": url, "ok": 200 <= int(status) < 400, "status": status, "content_type": ctype[:80]})
                if not (200 <= int(status) < 400):
                    errors.append(f"URL returned status {status}: {url}")
        except Exception as exc:
            results.append({"url": url, "ok": False, "error": str(exc)[:200]})
            errors.append(f"URL failed: {url}")
    return result(not errors, errors, checked=len(urls), results=results)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CoopLens local helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("runtime-date").set_defaults(func=cmd_runtime_date)
    sub.add_parser("validate").set_defaults(func=cmd_validate)

    q = sub.add_parser("query")
    q.add_argument("--query", required=True)
    q.add_argument("--top", type=int, default=8)
    q.set_defaults(func=cmd_query)

    rq = sub.add_parser("rank-query")
    rq.add_argument("--query", required=True)
    rq.add_argument("--top", type=int, default=8)
    rq.set_defaults(func=cmd_rank_query)

    mt = sub.add_parser("markdown-toc-check")
    mt.add_argument("report")
    mt.set_defaults(func=cmd_markdown_toc_check)

    mh = sub.add_parser("markdown-to-html")
    mh.add_argument("report")
    mh.add_argument("--out")
    mh.add_argument("--title")
    mh.set_defaults(func=cmd_markdown_to_html)

    sh = sub.add_parser("safe-html-build")
    sh.add_argument("report")
    sh.add_argument("--out")
    sh.add_argument("--title")
    sh.add_argument("--error-out")
    sh.set_defaults(func=cmd_safe_html_build)

    hrg = sub.add_parser("html-render-gate-check")
    hrg.add_argument("markdown")
    hrg.add_argument("html")
    hrg.set_defaults(func=cmd_html_render_gate_check)

    hc = sub.add_parser("html-report-check")
    hc.add_argument("html")
    hc.set_defaults(func=cmd_html_report_check)

    hs = sub.add_parser("html-syntax-check")
    hs.add_argument("html")
    hs.set_defaults(func=cmd_html_syntax_check)

    hi = sub.add_parser("html-important-statement-check")
    hi.add_argument("html")
    hi.set_defaults(func=cmd_html_important_statement_check)

    hcc = sub.add_parser("html-consistency-check")
    hcc.add_argument("markdown")
    hcc.add_argument("html")
    hcc.set_defaults(func=cmd_html_consistency_check)

    hd = sub.add_parser("html-delivery-check")
    hd.add_argument("final_answer")
    hd.set_defaults(func=cmd_html_delivery_check)

    sfd = sub.add_parser("strict-final-delivery-check")
    sfd.add_argument("final_answer")
    sfd.set_defaults(func=cmd_strict_final_delivery_check)

    prf = sub.add_parser("pure-report-file-check")
    prf.add_argument("html")
    prf.add_argument("markdown")
    prf.set_defaults(func=cmd_pure_report_file_check)

    cds = sub.add_parser("critical-data-source-check")
    cds.add_argument("report")
    cds.set_defaults(func=cmd_critical_data_source_check)

    cse = sub.add_parser("critical-source-evidence-check")
    cse.add_argument("report")
    cse.add_argument("--timeout", type=float, default=10.0)
    cse.add_argument("--max-lines", type=int, default=80)
    cse.set_defaults(func=cmd_critical_source_evidence_check)

    f3dg = sub.add_parser("function3-delivery-gate-check")
    f3dg.add_argument("final_answer")
    f3dg.set_defaults(func=cmd_function3_delivery_gate_check)

    rc = sub.add_parser("report-check")
    rc.add_argument("report")
    rc.set_defaults(func=cmd_report_check)

    nl = sub.add_parser("numeric-link-check")
    nl.add_argument("report")
    nl.add_argument("--annotate-out")
    nl.set_defaults(func=cmd_numeric_link_check)

    cs = sub.add_parser("consolidated-source-check")
    cs.add_argument("report")
    cs.set_defaults(func=cmd_consolidated_source_check)

    ol = sub.add_parser("official-latest-source-check")
    ol.add_argument("report")
    ol.set_defaults(func=cmd_official_latest_source_check)

    f2 = sub.add_parser("function2-check")
    f2.add_argument("report")
    f2.set_defaults(func=cmd_function2_check)

    f3 = sub.add_parser("function3-estimation-check")
    f3.add_argument("report")
    f3.add_argument("--annotate-out")
    f3.set_defaults(func=cmd_function3_estimation_check)

    f3d = sub.add_parser("function3-deep-analysis-check")
    f3d.add_argument("report")
    f3d.set_defaults(func=cmd_function3_deep_analysis_check)

    piu = sub.add_parser("personalized-input-use-check")
    piu.add_argument("report")
    piu.set_defaults(func=cmd_personalized_input_use_check)

    olc = sub.add_parser("overseas-living-cost-check")
    olc.add_argument("report")
    olc.set_defaults(func=cmd_overseas_living_cost_check)

    afc = sub.add_parser("artifact-filename-check")
    afc.add_argument("final_answer")
    afc.set_defaults(func=cmd_artifact_filename_check)

    lr = sub.add_parser("live-rank-estimation-check")
    lr.add_argument("report")
    lr.set_defaults(func=cmd_live_rank_estimation_check)

    rr = sub.add_parser("rank-reasoning-check")
    rr.add_argument("report")
    rr.set_defaults(func=cmd_rank_reasoning_check)

    ps = sub.add_parser("personalization-check")
    ps.add_argument("report")
    ps.set_defaults(func=cmd_personalization_check)

    rw = sub.add_parser("rank-workflow-check")
    rw.add_argument("report")
    rw.set_defaults(func=cmd_rank_workflow_check)

    rwe = sub.add_parser("rank-estimation-workflow-check")
    rwe.add_argument("report")
    rwe.set_defaults(func=cmd_rank_workflow_check)

    ms = sub.add_parser("manual-source-confirmation-check")
    ms.add_argument("report")
    ms.set_defaults(func=cmd_manual_source_confirmation_check)

    bd = sub.add_parser("batch-distinction-check")
    bd.add_argument("report")
    bd.set_defaults(func=cmd_batch_distinction_check)

    cas = sub.add_parser("current-admission-status-check")
    cas.add_argument("report")
    cas.set_defaults(func=cmd_current_admission_status_check)

    qs = sub.add_parser("qs-latest-ranking-check")
    qs.add_argument("report")
    qs.set_defaults(func=cmd_qs_latest_ranking_check)

    rs = sub.add_parser("recommendation-split-check")
    rs.add_argument("report")
    rs.set_defaults(func=cmd_recommendation_split_check)

    rr2 = sub.add_parser("recommendation-rating-check")
    rr2.add_argument("report")
    rr2.set_defaults(func=cmd_recommendation_split_check)

    pp = sub.add_parser("public-platform-search-check")
    pp.add_argument("report")
    pp.set_defaults(func=cmd_public_platform_search_check)

    nc = sub.add_parser("negative-consultation-check")
    nc.add_argument("report")
    nc.set_defaults(func=cmd_negative_consultation_check)

    go = sub.add_parser("graduate-outcomes-check")
    go.add_argument("report")
    go.set_defaults(func=cmd_graduate_outcomes_check)

    ca = sub.add_parser("cscse-authentication-check")
    ca.add_argument("report")
    ca.set_defaults(func=cmd_cscse_authentication_check)

    pq = sub.add_parser("parent-questions-check")
    pq.add_argument("report")
    pq.set_defaults(func=cmd_parent_questions_check)

    pr = sub.add_parser("postgraduate-recommendation-check")
    pr.add_argument("report")
    pr.set_defaults(func=cmd_postgraduate_recommendation_check)

    cg = sub.add_parser("completion-gate-check")
    cg.add_argument("final_answer")
    cg.set_defaults(func=cmd_completion_gate_check)

    fa = sub.add_parser("final-product-audit-check")
    fa.add_argument("final_answer")
    fa.set_defaults(func=cmd_final_product_audit_check)

    ad = sub.add_parser("artifact-delivery-check")
    ad.add_argument("final_answer")
    ad.set_defaults(func=cmd_artifact_delivery_check)

    lc = sub.add_parser("link-check")
    lc.add_argument("report")
    lc.add_argument("--max-urls", type=int, default=20)
    lc.add_argument("--timeout", type=int, default=8)
    lc.set_defaults(func=cmd_link_check)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
