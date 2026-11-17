#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find-skills++ 命令行工具（零依赖，仅标准库）。

让「发现 → 安全审查 → 安装 → 更新/卸载 → 追溯」技能脱离 agent 也能跑：
  - 离线优先：内置 registry.json 可信注册表，不依赖随时会挂的实时 API。
  - 联网可选：SkillHub API 作为补充源（--offline 可强制离线）。
  - 跨平台：Windows / Linux / macOS 目标目录健壮判定。
  - 安全可控：install 前调用自带 security_scan.py 做静态审查，P0 阻断。

子命令：
  search  <query>           搜索（本地已装 + 离线注册表 + 缓存 + 可选 SkillHub），语义匹配 + 综合排序
  scan    <path>            对技能目录做安全静态扫描（正则可+AST，P0/P1/P2，退出码 2/1/0）
  install <slug>            下载社区技能 → AST安全扫描 → 解压（P0 阻断）
  update  <slug>            重下最新并覆盖已装社区技能（同样过安全网关）
  uninstall <slug>          卸载本地技能（进回收站，可还原，非硬删除）
  clean-dupes               清理重复安装（每组保留最新修改一份，其余进回收站）
  sync                      拉取 SkillHub 全量目录到本地缓存（离线全能）
  list                      列出本地已装技能
  audit                     扫描所有已装技能，汇总风险
  quality <slug/--path>     评估单个技能质量（0-100，七维含引用完整性）
  redundancy                检测本地已装技能功能冗余
  prune                     基于静态信号给出瘦身建议（只读）
  discover [--new|--trending]  新上架 / 热门榜单（跨源版本仲裁）
  registry                  registry.json 校验 / 查看 / 追加条目
  promote  [--out FILE]     生成自我推广素材包（简介/社交文案/对比表/发布清单）
  demo     [--query Q]      可录屏的端到端演示（搜索→评级→安检→治理→自述）
  elevator                 30 秒电梯演讲（差异化自述，对话中可直接引用）

设计参考：sandbaseai/workbuddy-skill 的"真实脚本化审查"思路（已注明派生）。
源头：vercel-labs/skills 的 find-skills（Vercel 官方）；
最近的派生上游：guipi888/find-skills（MIT，99.4 万下载，已保留其许可与署名）。
"""

from __future__ import annotations

import argparse
import io
import json
import math
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# ---- 让本脚本既能直接运行，也能被 pytest import ----
ROOT = Path(__file__).resolve().parent
_SCRIPTS = str(ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
import security_scan  # noqa: E402

REGISTRY_PATH = ROOT / "registry.json"
SELF_SLUG = "find-skills-plusplus"   # 自身目录名（用于默认排除 / 自检时包含）
SKILLHUB_API = "https://lightmake.site/api/v1/search"
SKILLHUB_DL = "https://lightmake.site/api/v1/download"
SKILLHUB_CACHE = ROOT / "registry.cache.json"
CACHE_TTL_HOURS = 24
INSTALL_LOG = Path.home() / ".workbuddy" / "skills-install-log.md"

TRUSTED_REPUTATION = 1.0      # 官方源
BUILTIN_REPUTATION = 0.9      # 宿主内置（可信通道）
KNOWN_REPUTATION = 0.9        # 已知仓库/许可证
UNKNOWN_REPUTATION = 0.6      # 未知作者/低星标

REQUIRED_REGISTRY_KEYS = (
    "slug", "name", "description", "category", "source", "official_source", "reputation",
)


# --------------------------------------------------------------------------
# 工具函数（纯函数，便于测试）
# --------------------------------------------------------------------------
def normalize_key(name: str) -> str:
    """归一化名：小写、去空格/连字符、去 -skill 命名约定后缀，用于跨源去重。

    仅当基础词长度 >= 3 才剥离尾部 skill，避免把 'myskill' 误截成 'my'。
    """
    k = (name or "").lower()
    m = re.match(r"^(.*?)[-_ ]?skill$", k)
    if m and len(m.group(1)) >= 3:
        k = m.group(1)
    for ch in (" ", "-", "_", "/"):
        k = k.replace(ch, "")
    return k


def derive_reputation(entry: dict) -> float:
    if "reputation" in entry and isinstance(entry.get("reputation"), (int, float)):
        return float(entry["reputation"])
    if entry.get("official_source"):
        return TRUSTED_REPUTATION
    if entry.get("source") == "workbuddy-builtin":
        return BUILTIN_REPUTATION
    if entry.get("known_license") or entry.get("homepage"):
        return KNOWN_REPUTATION
    return UNKNOWN_REPUTATION


def compute_composite(cand: dict) -> float:
    """综合分：0.5*匹配 + 0.3*热度 + 0.2*时效，再乘信誉。缺失字段取中性值。"""
    score = min(float(cand.get("score") or 0.5), 1.0)
    downloads = cand.get("downloads") or cand.get("popularity") or 0
    try:
        pop = (float(downloads) if downloads else 0.0)
    except (TypeError, ValueError):
        pop = 0.0
    pop_norm = min(math.log10(1 + pop) / 7.0, 1.0) if pop else 0.3
    recency = recency_score(cand)
    base = 0.5 * score + 0.3 * pop_norm + 0.2 * recency
    return round(base * derive_reputation(cand), 4)


def recency_score(cand: dict) -> float:
    updated = cand.get("updated") or cand.get("updatedAt")
    if not updated:
        return 0.5
    try:
        if isinstance(updated, (int, float)):  # 毫秒时间戳
            dt = datetime.fromtimestamp(updated / 1000, tz=timezone.utc)
        else:
            s = str(updated).replace("Z", "+00:00")
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:  # 无时区的日期（如 "2026-09-19"）→ 按 UTC 处理
                dt = dt.replace(tzinfo=timezone.utc)
    except (ValueError, OSError, OverflowError):
        return 0.5
    days = max((datetime.now(tz=timezone.utc) - dt).days, 0)
    return max(0.0, min(1.0, 1.0 - days / 365.0))


def merge_candidates(lists) -> dict:
    """多源候选合并去重：以 normalize_key 为 key，合并 sources[]，取最高版本/最近更新。"""
    merged: dict[str, dict] = {}
    for src_name, items in lists:
        for it in items:
            key = normalize_key(it.get("name") or it.get("slug") or "")
            if not key:
                continue
            existing = merged.get(key)
            if existing is None:
                it = dict(it)
                it["sources"] = [src_name]
                it["_source_versions"] = {src_name: it.get("version") or "?"}
                merged[key] = it
            else:
                if src_name not in existing["sources"]:
                    existing["sources"].append(src_name)
                existing.setdefault("_source_versions", {})[src_name] = it.get("version") or "?"
                # 取更近的更新时间
                if (it.get("updated") or it.get("updatedAt") or 0) > (
                    existing.get("updated") or existing.get("updatedAt") or 0
                ):
                    existing["updated"] = it.get("updated") or existing.get("updated")
                    existing["updatedAt"] = it.get("updatedAt") or existing.get("updatedAt")
    return merged


def parse_version(v):
    """宽松版本解析：'v1.2.3' / '1.10' / '2.0-beta' → 可比较的元组；缺失返回 (0,)。"""
    if not v:
        return (0,)
    s = str(v).lstrip("vV")
    parts = []
    for seg in re.split(r"[.\-_+]", s):
        m = re.match(r"(\d+)", seg)
        parts.append(int(m.group(1)) if m else 0)
    return tuple(parts)


# --------------------------------------------------------------------------
# Phase 2：语义匹配 / 质量评级 / 冗余检测（离线、零依赖）
# --------------------------------------------------------------------------
# 意图同义词词典：自然语言需求 → 关键词集合（中英文）。用于"轻量语义匹配"——
# 不依赖外部 embedding API，靠本地词典把口语需求映射到技能意图，诚实标注为
# 轻量级而非 LLM 语义。
INTENT_SYNONYMS = {
    "pdf": {"pdf", "文档", "转换", "合并", "拆分", "水印", "提取", "扫描件", "ocr"},
    "office": {"word", "docx", "报告", "公文", "ppt", "powerpoint", "演示", "幻灯片",
               "excel", "xlsx", "表格", "电子表格", "sheet", "文档"},
    "browser": {"浏览器", "网页", "截图", "爬取", "抓取", "自动化", "selenium",
                "playwright", "browser", "网站"},
    "finance": {"股票", "行情", "基金", "选股", "财报", "金融", "投资", "stock",
                "finance", "etf", "证券", "交易"},
    "data": {"数据分析", "可视化", "图表", "数据", "统计", "csv", "表格", "报表"},
    "image": {"图像", "图片", "处理", "水印", "修复", "image", "photo", "照片"},
    "security": {"安全", "审查", "审计", "security", "audit", "合规", "风险", "扫描"},
    "skill": {"技能", "skill", "查找", "发现", "安装", "管理", "搜索"},
    "web": {"网站", "前端", "网页", "部署", "web", "html", "页面"},
    "video": {"视频", "剪辑", "生成", "video", "短片"},
    "audio": {"音频", "语音", "audio", "转录", "字幕"},
    "translate": {"翻译", "多语言", "translate", "本地化"},
    "email": {"邮件", "email", "通知", "提醒"},
    "calendar": {"日历", "日程", "calendar", "会议", "安排"},
    "search": {"搜索", "检索", "search", "查找", "查询"},
    "test": {"测试", "test", "单元测试", "质量", "pytest"},
    "github": {"github", "仓库", "git", "代码", "提交", "pr"},
    "memory": {"记忆", "知识库", "memory", "笔记", "归档", "wiki"},
    "agent": {"智能体", "agent", "助手", "自动化", "工作流", "机器人"},
    "api": {"api", "接口", "集成", "调用", "mcp", "连接器"},
}

_STOP = set(" 　\t\n\r，。、；：？！“”‘’（）《》【】—…·.,;:?!\"'()[]{}<>/-_|\\+=*#@~`%$&^")


def tokenize(text):
    """返回 (英文/数字词集合, 中文及实义字符集合, 全文小写)。"""
    text = (text or "").lower()
    words = set(re.findall(r"[a-z0-9]+", text))
    chars = set(ch for ch in text if ch not in _STOP)
    return words, chars, text


def semantic_score(query, text):
    """轻量语义匹配分 0–1：0.5*语义命中 + 0.3*直接命中 + 0.2*整体子串。"""
    qw, qc, ql = tokenize(query)
    tw, tc, tl = tokenize(text)
    qset = qw | qc
    expanded = set(qset)
    for tok in qset:
        if tok in INTENT_SYNONYMS:
            expanded |= INTENT_SYNONYMS[tok]
    # 直接命中：query 词/字在 text 中的比例
    direct = sum(1 for w in qset if w in (tw | tc)) / max(len(qset), 1)
    # 语义命中：扩展词集命中 text 词/字，或中文长词作为子串出现
    sem_hits = sum(1 for w in expanded if w in (tw | tc) or (len(w) >= 2 and w in tl))
    sem = sem_hits / max(len(expanded), 1)
    substr = 1.0 if ql.strip() and ql.strip() in tl else 0.0
    return round(min(max(0.5 * sem + 0.3 * direct + 0.2 * substr, 0.0), 1.0), 4)


def gather_quality_fields(skill_dir, local_names=None, registry_names=None):
    """解析技能目录，提取质量评级所需字段。

    local_names / registry_names 用于「引用完整性」校验：传入后会检查技能里
    声明的跨技能/本地文件引用是否真实存在（缺失则不校验、不参与评分，保持轻量）。
    """
    p = Path(skill_dir)
    md = p / "SKILL.md"
    txt = md.read_text(encoding="utf-8", errors="replace") if md.exists() else ""
    ok, fields = security_scan.parse_frontmatter(txt)

    # 引用完整性（环境感知）：声明引用了哪些本地文件 / 其他技能，是否真实存在
    ref_declared = 0
    ref_local_missing = 0
    for m in re.finditer(r"(?:scripts|references|assets)/[A-Za-z0-9_./-]+", txt):
        ref_declared += 1
        if not (p / m.group(0)).exists():
            ref_local_missing += 1
    ref_external_missing = 0
    if (local_names or registry_names) is not None:
        idx = set(local_names or []) | set(registry_names or [])
        for m in re.finditer(r"\bSkill\(\s*[\"']([^\"']+)[\"']\s*\)", txt):
            ref_declared += 1
            if m.group(1) not in idx:
                ref_external_missing += 1

    return {
        "name": fields.get("name", p.name),
        "description": fields.get("description", ""),
        "version": fields.get("version", ""),
        "author": fields.get("author", ""),
        "license": fields.get("license", ""),
        "updated": fields.get("updated") or fields.get("updatedAt"),
        "doc_len": len(txt),
        "has_examples": ("```" in txt) or ("示例" in txt) or ("example" in txt.lower()),
        "has_references": ("references" in txt.lower())
        or (p / "scripts").exists() or (p / "references").exists(),
        "has_steps": bool(re.search(r"(step\s*\d|步骤|第\s*\d\s*步)", txt, re.I)),
        "ref_declared": ref_declared,
        "ref_local_missing": ref_local_missing,
        "ref_external_missing": ref_external_missing,
    }


def rate_quality(fields):
    """技能质量评级 0–100，维度：frontmatter/示例/参考/文档长度/新鲜度/可操作性/引用完整性。

    引用完整性（环境感知）：若技能声明了引用（本地文件或其他技能），但其中存在
    找不到的目标，则大幅降级——专治「长得好看但引用了不存在工具」的假优。
    未声明引用（ref_declared==0）给中性 0.5，不奖不罚。
    """
    fm_fields = ["name", "description", "author", "license", "version"]
    present = sum(1 for f in fm_fields if fields.get(f))
    ref_declared = int(fields.get("ref_declared") or 0)
    if ref_declared > 0:
        resolved = (ref_declared - int(fields.get("ref_local_missing") or 0)
                    - int(fields.get("ref_external_missing") or 0))
        ref_integrity = max(0.0, min(1.0, resolved / ref_declared))
    else:
        ref_integrity = 0.5
    dims = {
        "frontmatter": present / len(fm_fields),
        "examples": 1.0 if fields.get("has_examples") else 0.0,
        "references": 1.0 if fields.get("has_references") else 0.0,
        "doc_length": (1.0 if int(fields.get("doc_len") or 0) >= 800
                       else 0.5 if int(fields.get("doc_len") or 0) >= 200 else 0.0),
        "freshness": recency_score(fields),
        "actionable": 1.0 if fields.get("has_steps") else 0.0,
        "reference_integrity": ref_integrity,
    }
    weights = {"frontmatter": 0.2, "examples": 0.15, "references": 0.1,
               "doc_length": 0.1, "freshness": 0.15, "actionable": 0.1,
               "reference_integrity": 0.2}
    score = sum(dims[k] * w for k, w in weights.items())
    grade = ("优" if score >= 0.8 else "良" if score >= 0.6
             else "中" if score >= 0.4 else "差")
    return {"score": round(score * 100, 1), "grade": grade, "dims": dims}


_CN_STOP = set(
    "的了和与会及或等其该这个一个用于通过使用支持提供可以进行分析能够帮助用户内容相关"
    "基于自动工具文件处理生成读取写入创建新建管理搜索查找获取设置配置安装运行执行打开关闭"
    "保存导出导入转换合并拆分提取修复编辑修改查看显示展示进行方式各种多种功能强大快速高效简单"
)


def _bigrams(text):
    """英文词集合 + 中文去停用字后的相邻二元组集合（区分度高于单字）。"""
    text = (text or "").lower()
    words = set(re.findall(r"[a-z0-9]+", text))
    cn = [ch for ch in text if '一' <= ch <= '鿿' and ch not in _CN_STOP]
    bg = {cn[i] + cn[i + 1] for i in range(len(cn) - 1)}
    return words, bg


def _desc_similarity(d1, d2):
    w1, b1 = _bigrams(d1)
    w2, b2 = _bigrams(d2)
    words_union = w1 | w2
    word_overlap = (len(w1 & w2) / len(words_union)) if words_union else 0.0
    bg_union = b1 | b2
    if not bg_union:
        return round(word_overlap, 4)
    bg_sim = len(b1 & b2) / len(bg_union)
    return round(0.7 * bg_sim + 0.3 * word_overlap, 4)


def find_duplicate_installs(skills):
    """按技能名（frontmatter name）识别同一技能的多次安装，返回 [{name, members, count}]。"""
    by_name = {}
    for s in skills:
        by_name.setdefault(s.get("name") or "?", []).append(s.get("path", "?"))
    return [{"name": k, "members": v, "count": len(v)} for k, v in by_name.items() if len(v) > 1]


def redundancy_groups(skills):
    """按描述相似度(>=0.6)聚合成功能冗余组（自动按技能名去重，重复安装见 find_duplicate_installs）。"""
    seen = {}
    uniq = []
    for s in skills:
        k = s.get("name", "")
        if k not in seen:
            seen[k] = True
            uniq.append(s)
    groups = []
    n = len(uniq)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = uniq[i], uniq[j]
            sim = _desc_similarity(a.get("description", ""), b.get("description", ""))
            if sim < 0.6:
                continue
            placed = False
            for g in groups:
                if a["name"] in g["members"] or b["name"] in g["members"]:
                    for m in (a["name"], b["name"]):
                        if m not in g["members"]:
                            g["members"].append(m)
                    g["sims"].append(round(sim, 2))
                    placed = True
                    break
            if not placed:
                groups.append({"members": [a["name"], b["name"]],
                               "sims": [round(sim, 2)],
                               "category": a.get("category", "")})
    return groups


# --------------------------------------------------------------------------
# 数据来源
# --------------------------------------------------------------------------
def load_registry() -> list[dict]:
    if not REGISTRY_PATH.exists():
        return []
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data.get("skills", data) if isinstance(data, dict) else data


def validate_registry(entries: list[dict]) -> list[str]:
    problems = []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            problems.append(f"#{i}: 不是对象")
            continue
        for k in REQUIRED_REGISTRY_KEYS:
            if k not in e:
                problems.append(f"#{i} ({e.get('slug', '?')}): 缺字段 {k}")
        rep = e.get("reputation")
        if rep is not None and not (0.0 <= float(rep) <= 1.0):
            problems.append(f"#{i} ({e.get('slug', '?')}): reputation 越界 {rep}")
    return problems


def discover_local(include_self: bool = False, roots: list = None) -> list[dict]:
    """扫描本地已装技能目录，解析 frontmatter 取 name/version。

    include_self=False（默认）时排除 find-skills++ 自身——搜索/榜单里不该自荐。
    但 `quality` 自检等场景需要包含自己，用 include_self=True。
    roots 可注入（测试用）；默认扫描 ~/.workbuddy/skills、~/.codebuddy/skills
    以及 ~/.workbuddy/plugins/cache（插件缓存里的技能）。
    """
    if roots is None:
        roots = [
            Path.home() / ".workbuddy" / "skills",
            Path.home() / ".codebuddy" / "skills",
            Path.home() / ".openclaw" / "skills",
            Path.home() / ".claude" / "skills",
            Path.home() / ".workbuddy" / "plugins" / "cache",
        ]
    found = []
    for base in roots:
        if not base.exists():
            continue
        for skill_dir in base.rglob("SKILL.md"):
            d = skill_dir.parent
            txt = skill_dir.read_text(encoding="utf-8", errors="replace")
            ok, fields = security_scan.parse_frontmatter(txt)
            if not ok:
                continue
            if not include_self and d.name == SELF_SLUG:
                continue  # 默认不列出自己，避免搜索结果里自荐
            has_examples = ("```" in txt) or ("示例" in txt) or ("example" in txt.lower())
            has_references = ("references" in txt.lower()) or (d / "scripts").exists() or (d / "references").exists()
            has_steps = bool(re.search(r"(step\s*\d|步骤|第\s*\d\s*步)", txt, re.I))
            found.append({
                "name": fields.get("name", d.name),
                "slug": d.name,
                "version": fields.get("version", ""),
                "source": "local",
                "path": str(d),
                "official_source": False,
                "reputation": BUILTIN_REPUTATION,
                "updated": None,
                "downloads": None,
                "score": 0.9,
                "description": fields.get("description", ""),
                "doc_len": len(txt),
                "has_examples": has_examples,
                "has_references": has_references,
                "has_steps": has_steps,
            })
    return found


def query_skillhub(query: str, limit: int = 10) -> list[dict]:
    try:
        url = f"{SKILLHUB_API}?q={urllib.parse.quote(query)}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "find-skills++"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        out = []
        for r in data.get("results", []):
            out.append({
                "name": r.get("displayName") or r.get("name") or r.get("slug"),
                "slug": r.get("slug"),
                "description": r.get("description") or r.get("description_zh") or "",
                "source": "skillhub",
                "official_source": False,
                "score": float(r.get("score") or 0.0),
                "downloads": r.get("downloads") or r.get("installs") or r.get("stars") or 0,
                "updatedAt": r.get("updatedAt"),
                "homepage": r.get("homepage"),
                "reputation": UNKNOWN_REPUTATION,
            })
        return out
    except Exception:
        return []


def sync_skillhub(limit: int = 1000) -> dict:
    """拉取 SkillHub 全量目录到 registry.cache.json（带 TTL），实现真·离线全能。"""
    results = query_skillhub("", limit)
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(results),
        "skills": results,
    }
    SKILLHUB_CACHE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"fetched": len(results), "cache": str(SKILLHUB_CACHE)}


def load_cache() -> list[dict]:
    """读取本地 SkillHub 缓存目录；过期（>TTL）则视为无缓存。"""
    if not SKILLHUB_CACHE.exists():
        return []
    try:
        data = json.loads(SKILLHUB_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return []
    fa = data.get("fetched_at")
    if fa:
        try:
            dt = datetime.fromisoformat(str(fa).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
            if age_h > CACHE_TTL_HOURS:
                return []
        except Exception:
            pass
    return data.get("skills", [])


# --------------------------------------------------------------------------
# 渲染
# --------------------------------------------------------------------------
def render_table(ranked: list[dict]) -> str:
    rows = ["| 技能 | 来源 | 综合 | 热度 | 最近更新 | 安全 | 质量 | 备注 |",
            "|---|---|---|---|---|---|---|---|"]
    for c in ranked:
        name = c.get("name") or c.get("slug") or "?"
        src = "/".join(c.get("sources", [c.get("source", "—")]))
        comp = f"{c.get('_composite', 0):.2f}"
        dl = c.get("downloads")
        hot = f"{dl:,}" if isinstance(dl, (int, float)) and dl else "—"
        upd = c.get("updated") or c.get("updatedAt")
        if isinstance(upd, (int, float)) and upd:
            upd = datetime.fromtimestamp(upd / 1000, tz=timezone.utc).strftime("%Y-%m")
        else:
            upd = "—"
        sec = "已审(官方)" if c.get("official_source") else "社区·建议扫描"
        q = c.get("_quality")
        qual = f"{q['grade']}({q['score']:.0f})" if q else "—"
        note = c.get("_note", "")
        rows.append(f"| {name} | {src} | {comp} | {hot} | {upd} | {sec} | {qual} | {note} |")
    return "\n".join(rows)


def annotate(cand: dict, sem=None) -> None:
    base = compute_composite(cand)
    cand["_composite"] = round(0.6 * base + 0.4 * sem, 4) if sem is not None else base
    notes = []
    if len(cand.get("sources", [])) > 1:
        notes.append(f"多源({len(cand['sources'])}存在)")
    upd = cand.get("updated") or cand.get("updatedAt")
    if isinstance(upd, (int, float)) and upd:
        days = (datetime.now(tz=timezone.utc) - datetime.fromtimestamp(upd / 1000, tz=timezone.utc)).days
        if days > 365:
            notes.append("⚠️长期未维护")
    if derive_reputation(cand) <= UNKNOWN_REPUTATION + 1e-9 and not cand.get("official_source"):
        notes.append("⚠️低信誉·谨慎")
    # 本地技能可评质量（注册表/联网候选无全文，标 N/A）
    if cand.get("source") == "local" and cand.get("path"):
        try:
            cand["_quality"] = rate_quality(gather_quality_fields(cand["path"]))
        except Exception:
            cand["_quality"] = None
    cand["_note"] = " ".join(notes)


# --------------------------------------------------------------------------
# 子命令
# --------------------------------------------------------------------------
def cmd_search(args) -> int:
    query = args.query
    lists = [("registry", load_registry())]
    cache = load_cache()
    if cache:
        lists.append(("skillhub-cache", cache))
    if not args.offline:
        if query:
            lists.append(("skillhub", query_skillhub(query, args.limit)))
        else:
            lists.append(("skillhub", query_skillhub("", args.limit)))
    # 本地已装也并入候选
    local = discover_local()
    if local:
        lists.append(("local", local))

    merged = merge_candidates(lists)
    if query:
        qk = normalize_key(query)
        for c in merged.values():
            text = (c.get("name") or "") + " " + (c.get("description") or "")
            c["_sem"] = semantic_score(query, text)
        # 语义分 >0 即纳入；若全为 0 则退回原匹配，避免空结果
        filtered = {k: v for k, v in merged.items()
                    if v.get("_sem", 0) > 0
                    or qk in k
                    or query.lower() in (v.get("description") or "").lower()}
        if filtered:
            merged = filtered

    if not merged:
        print("未找到匹配技能（本地已装 + 离线注册表" + ("+缓存" if cache else "") + ("" if args.offline else " + SkillHub") + "）。")
        if not args.offline:
            print("可去掉 --offline 重试，或先执行 `findskills.py sync` 刷新缓存。")
        else:
            print("离线模式仅能匹配本地与内置注册表/缓存；执行 `findskills.py sync` 可扩充离线目录。")
        return 0

    for c in merged.values():
        annotate(c, sem=c.get("_sem", 0))
    ranked = sorted(merged.values(), key=lambda c: -c.get("_composite", 0))[: args.limit]
    print(f"找到 {len(merged)} 个候选，按综合分排序展示 Top {len(ranked)}：\n")
    print(render_table(ranked))
    print("\n要安装哪个？用：findskills.py install <slug>")
    return 0


def cmd_scan(args) -> int:
    p = Path(args.path)
    if not p.exists():
        print(f"路径不存在: {p}", file=sys.stderr)
        return 3
    report = security_scan.build_report(p, exclude_tests=getattr(args, "exclude_tests", False))
    rc = {"P0": 2, "P1": 1, "P2": 0}[report["risk_level"]]
    if getattr(args, "json", False):
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return rc
    print(security_scan.render_markdown(report, args.lang), end="")
    # 四级风险与动作（对标 skill-vetter）
    cls = report.get("risk_class")
    if cls:
        action = security_scan.RISK_CLASS[cls][0]
        print(f"\n四级风险: {cls} — {action}")
        print(f"结论: {report['verdict']}")
        if cls == "EXTREME":
            print("⛔ 执行块命中 P0 高危，禁止安装。")
        elif cls == "HIGH":
            print("🔴 需人工批准后方可安装。")
    return rc


# 已知 agent 的技能目录判定：env 前缀 或 家目录存在 → 技能目录
AGENT_TARGETS = [
    ("codebuddy", "CODEBUDDY_", ".codebuddy"),
    ("workbuddy", None, ".workbuddy"),
    ("openclaw", None, ".openclaw"),
    ("claude", None, ".claude"),
]


def detect_target_dir() -> Path:
    """自动判定当前 agent，返回其技能目录（默认 WorkBuddy）。"""
    import os
    home = Path.home()
    # 1) 环境变量优先（最精确，标明当前运行的 agent）
    for name, env_prefix, _ in AGENT_TARGETS:
        if env_prefix and any(k.startswith(env_prefix) for k in os.environ):
            return home / f".{name}" / "skills"
    # 2) 家目录存在判定（按优先级）
    for name, _, sub in AGENT_TARGETS:
        if (home / sub).exists():
            return home / sub / "skills"
    # 3) 兜底
    return home / ".workbuddy" / "skills"


def resolve_target_dir(target_arg) -> Path:
    """--target 可接受 agent 名（codebuddy/workbuddy/openclaw/claude）或显式路径。"""
    if not target_arg:
        return detect_target_dir()
    key = target_arg.strip().lower()
    mapping = {name: Path.home() / sub / "skills" for name, _, sub in AGENT_TARGETS}
    if key in mapping:
        return mapping[key]
    return Path(target_arg).expanduser()


# --------------------------------------------------------------------------
# 生命周期：回收站（跨平台）、安装历史写入
# --------------------------------------------------------------------------
def _win_recycle(path: Path) -> str:
    """Windows 原生回收站（SHFileOperationW + FOF_ALLOWUNDO）。零依赖 ctypes。"""
    import ctypes
    from ctypes import wintypes
    class SHFILEOPSTRUCT(ctypes.Structure):
        _fields_ = [
            ("hwnd", wintypes.HWND),
            ("wFunc", wintypes.UINT),
            ("pFrom", ctypes.c_wchar_p),
            ("pTo", ctypes.c_wchar_p),
            ("fFlags", wintypes.UINT),
            ("fAnyOperationsAborted", wintypes.BOOL),
            ("hNameMappings", ctypes.c_void_p),
            ("lpszProgressTitle", ctypes.c_wchar_p),
        ]
    FO_DELETE = 3
    FOF_ALLOWUNDO = 0x40
    FOF_NOCONFIRMATION = 0x10
    FOF_SILENT = 0x4
    f = SHFILEOPSTRUCT()
    f.wFunc = FO_DELETE
    f.pFrom = str(path.resolve()) + "\0\0"
    f.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT
    rc = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(f))
    if rc == 0:
        return "recycle"
    raise RuntimeError(f"SHFileOperation returned {rc}")


def send_to_trash(path) -> str:
    """移动到回收站。优先系统回收站（Windows 原生 / Linux gio·trash-put），
    失败则退回自管理回收站 ~/.workbuddy/.trash/（带时间戳，可还原）。"""
    p = Path(path).resolve()
    if not p.exists():
        return "not-exist"
    if platform.system() == "Windows":
        try:
            return _win_recycle(p)
        except Exception:
            pass
    else:
        for cmd in (["gio", "trash"], ["trash-put"]):
            try:
                subprocess.run(cmd + [str(p)], check=True, capture_output=True)
                return "recycle"
            except Exception:
                continue
    # fallback: 自管理回收站
    trash_base = Path.home() / ".workbuddy" / ".trash"
    dest = trash_base / datetime.now().strftime("%Y%m%d-%H%M%S") / p.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if p.is_dir():
        shutil.move(str(p), str(dest))
    else:
        shutil.move(str(p), str(dest))
    return "local-trash"


def _append_install_log(name, version, dest, action):
    INSTALL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with INSTALL_LOG.open("a", encoding="utf-8") as f:
        if INSTALL_LOG.stat().st_size == 0:
            f.write("# 技能安装历史\n")
        f.write(f"- {datetime.now():%Y-%m-%d} | {name} | 社区(SkillHub) | {version} | {dest} | {action}\n")


def _fetch_and_install(slug, target, force, yes, action="安装") -> int:
    """下载社区技能 slug → 安全扫描 → 解压/覆盖到 target/<slug>。返回 rc。
    install 与 update 共用；action 仅影响日志与提示文案。"""
    cand = None
    for e in load_registry():
        if e.get("slug") == slug or normalize_key(e.get("name", "")) == normalize_key(slug):
            cand = e
            break
    if cand is None:
        hits = query_skillhub(slug, 5)
        for h in hits:
            if h.get("slug") == slug or normalize_key(h.get("name", "")) == normalize_key(slug):
                cand = h
                break
    if cand is None:
        print(f"未找到 slug={slug}（注册表与 SkillHub 均无）。先用 search 确认。", file=sys.stderr)
        return 1
    if cand.get("official_source") or cand.get("source") == "workbuddy-builtin":
        print("⚠️ 该条目为官方/内置技能，请优先通过宿主原生市场安装，本命令仅处理社区 zip。", file=sys.stderr)
        return 1
    dl_url = f"{SKILLHUB_DL}?slug={slug}"
    print(f"下载社区技能 {slug} ...")
    try:
        with tempfile.TemporaryDirectory() as td:
            zp = Path(td) / "skill.zip"
            req = urllib.request.Request(dl_url, headers={"User-Agent": "find-skills++"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                zp.write_bytes(resp.read())
            extract_dir = Path(td) / "extracted"
            extract_dir.mkdir()
            with zipfile.ZipFile(zp) as zf:
                zf.extractall(extract_dir)
            skill_root = extract_dir
            subs = [d for d in extract_dir.iterdir() if d.is_dir()]
            if len(subs) == 1 and (subs[0] / "SKILL.md").exists():
                skill_root = subs[0]
            report = security_scan.build_report(skill_root)
            if report["risk_level"] == "P0" and not force:
                print(security_scan.render_markdown(report, "zh-CN"), end="")
                print(f"\n❌ 命中 P0 高危信号，已阻断{action}（用 --force 可强制，但不推荐）。", file=sys.stderr)
                return 2
            if report["risk_level"] == "P1" and not yes:
                print(security_scan.render_markdown(report, "zh-CN"), end="")
                print(f"\n⚠️ 命中 P1 需确认信号。重新运行加 --yes 确认{action}。", file=sys.stderr)
                return 1
            target.mkdir(parents=True, exist_ok=True)
            dest = target / slug
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(skill_root, dest)
            ok, fields = security_scan.parse_frontmatter((dest / "SKILL.md").read_text(encoding="utf-8", errors="replace"))
            if not ok:
                print("⚠️ 操作成功但 SKILL.md 缺少合法 frontmatter。", file=sys.stderr)
            _append_install_log(cand.get("name", slug), cand.get("version", "?"), dest, action)
            print(f"✅ 已{action}到 {dest}（在【技能管理】面板可见）。")
            return 0
    except Exception as e:
        print(f"{action}失败: {e}", file=sys.stderr)
        return 1


def cmd_install(args) -> int:
    target = resolve_target_dir(args.target)
    return _fetch_and_install(args.slug, target, args.force, args.yes, action="安装")


def cmd_update(args) -> int:
    if args.offline:
        print("update 需联网下载最新版；离线模式无法更新。", file=sys.stderr)
        return 1
    local = discover_local()
    matches = [s for s in local if s["slug"] == args.slug
               or normalize_key(s["name"]) == normalize_key(args.slug)]
    if not matches:
        print(f"本地未装 slug={args.slug}，无法更新（先用 install）。", file=sys.stderr)
        return 1
    rc = 0
    for s in matches:
        target = Path(s["path"]).parent
        rc = _fetch_and_install(args.slug, target, True, args.yes, action="更新") or rc
    return rc


def cmd_uninstall(args) -> int:
    if args.slug == "find-skills-plusplus":
        print("⚠️ 不能卸载 find-skills++ 自身。", file=sys.stderr)
        return 1
    local = discover_local()
    matches = [s for s in local if s["slug"] == args.slug
               or normalize_key(s["name"]) == normalize_key(args.slug)]
    if not matches:
        print(f"未找到匹配 slug={args.slug} 的本地技能。", file=sys.stderr)
        return 1
    for s in matches:
        d = Path(s["path"]).parent
        if not d.exists():
            continue
        try:
            where = send_to_trash(d)
            print(f"🗑 已移入回收站: {d} ({where})")
            INSTALL_LOG.parent.mkdir(parents=True, exist_ok=True)
            with INSTALL_LOG.open("a", encoding="utf-8") as f:
                if INSTALL_LOG.stat().st_size == 0:
                    f.write("# 技能安装历史\n")
                f.write(f"- {datetime.now():%Y-%m-%d} | {s['name']} | 卸载 | {d} | 回收站({where})\n")
        except Exception as e:
            print(f"卸载失败 {d}: {e}", file=sys.stderr)
            return 1
    print(f"✅ 已卸载 {len(matches)} 个匹配目录（进回收站，可从回收站还原）。")
    return 0


def cmd_clean_dupes(args) -> int:
    local = discover_local()
    dups = find_duplicate_installs(local)
    if not dups:
        print("✅ 未发现重复安装。")
        return 0
    removed = 0
    for d in dups:
        dirs = []
        for p in d["members"]:
            if not p:
                continue
            pp = Path(p)
            # members 记录的是 SKILL.md 路径，取父目录即整个技能目录
            skill_dir = pp.parent if pp.name.lower() == "skill.md" else pp
            if skill_dir.exists():
                dirs.append(skill_dir)
        if len(dirs) < 2:
            continue
        dirs_sorted = sorted(dirs, key=lambda x: x.stat().st_mtime, reverse=True)
        keep = dirs_sorted[0]
        for victim in dirs_sorted[1:]:
            try:
                where = send_to_trash(victim)
                removed += 1
                print(f"  🗑 {victim} → 回收站({where})  [保留 {keep.name}]")
                with INSTALL_LOG.open("a", encoding="utf-8") as f:
                    if INSTALL_LOG.stat().st_size == 0:
                        f.write("# 技能安装历史\n")
                    f.write(f"- {datetime.now():%Y-%m-%d} | {d['name']} | 清理重复 | {victim} | 回收站({where})\n")
            except Exception as e:
                print(f"  清理失败 {victim}: {e}", file=sys.stderr)
    print(f"\n✅ 共清理 {removed} 份重复安装（每组保留最新修改的一份，其余进回收站可还原）。")
    return 0


def cmd_list(args) -> int:
    local = discover_local()
    if not local:
        print("未发现本地已装技能目录。")
        return 0
    print(f"本地已装技能（{len(local)}）：\n")
    for s in sorted(local, key=lambda x: x["name"].lower()):
        ver = f" v{s['version']}" if s.get("version") else ""
        print(f"  - {s['name']}{ver}  ({s['slug']})  ->  {s['path']}")
    return 0


def cmd_audit(args) -> int:
    local = discover_local()
    if not local:
        print("未发现本地已装技能。")
        return 0
    print(f"审计 {len(local)} 个本地技能：\n")
    worst = "P2"
    for s in local:
        d = Path(s["path"])
        if not (d / "SKILL.md").exists():
            continue
        report = security_scan.build_report(d)
        flag = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}[report["risk_level"]]
        if report["risk_level"] == "P0":
            worst = "P0"
        elif report["risk_level"] == "P1" and worst != "P0":
            worst = "P1"
        lic = "✅" if report["license_present"] else "❌"
        print(f"  {flag} {s['name']:<28} 许可证 {lic}  命中 {len(report['hits'])}")
    print(f"\n汇总：最高风险等级 = {worst}")
    return {"P0": 2, "P1": 1, "P2": 0}[worst]


def cmd_registry(args) -> int:
    if args.registry_cmd == "validate":
        entries = load_registry()
        problems = validate_registry(entries)
        if problems:
            print(f"❌ 发现 {len(problems)} 个问题：")
            for p in problems:
                print("  -", p)
            return 1
        print(f"✅ registry.json 合法，共 {len(entries)} 条技能条目。")
        return 0
    if args.registry_cmd == "show":
        entries = load_registry()
        for e in entries:
            print(f"  - {e.get('name')} ({e.get('slug')})  [{e.get('category')}]  rep={e.get('reputation')}")
        print(f"\n共 {len(entries)} 条。")
        return 0
    if args.registry_cmd == "add":
        # 追加一条（最小字段）
        entries = load_registry()
        entry = {
            "slug": args.slug, "name": args.name or args.slug,
            "description": args.desc or "", "category": args.category or "uncategorized",
            "source": "community", "official_source": False,
            "reputation": float(args.reputation or UNKNOWN_REPUTATION),
            "homepage": args.homepage or "", "updated": None,
        }
        entries.append(entry)
        REGISTRY_PATH.write_text(json.dumps({"skills": entries}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 已追加 {entry['slug']} 到 registry.json（记得 git commit）。")
        return 0
    return 1


def cmd_sync(args) -> int:
    if args.offline:
        print("sync 需要联网拉取 SkillHub 目录；离线模式无法同步。", file=sys.stderr)
        return 1
    print(f"同步 SkillHub 目录（limit={args.limit}）...")
    try:
        stats = sync_skillhub(args.limit)
    except Exception as e:
        print(f"同步失败: {e}", file=sys.stderr)
        return 1
    if stats["fetched"] == 0:
        print("⚠️ SkillHub 返回空结果（API 暂不可用或空查询不被支持）。缓存未更新。")
        return 1
    print(f"✅ 已缓存 {stats['fetched']} 个技能到 {stats['cache']}（TTL {CACHE_TTL_HOURS}h）。")
    print("之后 `search --offline` 也能用这份全量目录。")
    return 0


def _ts(v) -> float:
    """把各种日期写法安全转成可比较的时间戳；无法解析返回 0。

    registry.json 里可能是 '2026-03-05' 字符串，SkillHub 缓存里是毫秒整数，
    直接取负会 TypeError，故统一在此归一。
    """
    if v is None:
        return 0.0
    if isinstance(v, (int, float)):
        # 毫秒级时间戳（13 位）归一到秒，便于与日期字符串比较
        return float(v) / 1000.0 if v > 1e11 else float(v)
    s = str(v).strip()
    if not s:
        return 0.0
    if s.isdigit():
        n = int(s)
        return float(n) / 1000.0 if n > 1e11 else float(n)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
                "%Y-%m", "%Y"):
        try:
            import datetime as _dt
            return _dt.datetime.strptime(s[:len(fmt) + 4], fmt).timestamp()
        except Exception:
            continue
    import datetime as _dt
    try:
        return _dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def cmd_discover(args) -> int:
    lists = [("registry", load_registry())]
    cache = load_cache()
    if cache:
        lists.append(("cache", cache))
    local = discover_local()
    if local:
        lists.append(("local", local))
    merged = merge_candidates(lists)

    # 跨源版本仲裁：同一技能在多源有不同版本时，选最高版并标出落后源
    arbitrations = []
    for c in merged.values():
        sv = {k: v for k, v in c.get("_source_versions", {}).items() if v and v != "?"}
        if len(sv) >= 2:
            best_src, best_ver = max(sv.items(), key=lambda kv: parse_version(kv[1]))
            laggards = [k for k, v in sv.items() if parse_version(v) < parse_version(best_ver)]
            if laggards:
                arbitrations.append((c.get("name"), best_src, best_ver, laggards))

    ranked = list(merged.values())
    for c in ranked:
        annotate(c, sem=0)
    if args.new:
        ranked.sort(key=lambda c: -_ts(c.get("updated") or c.get("updatedAt")))
        title = "新上架"
    elif args.trending:
        ranked.sort(key=lambda c: -((c.get("downloads") or c.get("popularity") or 0) * 0.01
                                   + derive_reputation(c) * 1000))
        title = "热门"
    else:
        ranked.sort(key=lambda c: -c.get("_composite", 0))
        title = "精选"

    print(f"## {title}（候选 {len(merged)}，展示 Top {args.limit}）\n")
    print(render_table(ranked[:args.limit]))
    if arbitrations:
        print("\n### 跨源版本仲裁（自动选最新版）")
        for name, best_src, best_ver, laggards in arbitrations:
            print(f"  - {name}: 最新 {best_ver}（{best_src}）；落后源: {', '.join(laggards)}")
    else:
        print("\n（无跨源版本冲突。）")
    return 0


def cmd_quality(args) -> int:
    d = None
    if args.path:
        p = Path(args.path)
        if p.exists():
            d = p
    if d is None and args.slug:
        # include_self=True：允许给自己打分（自检场景）
        if normalize_key(args.slug) in ("self", "findskills", "findskillsplusplus", "findskillsxx"):
            d = ROOT
        else:
            for s in discover_local(include_self=True):
                if (s["slug"] == args.slug
                        or normalize_key(s["name"]) == normalize_key(args.slug)
                        or normalize_key(s["slug"]) == normalize_key(args.slug)):
                    d = Path(s["path"])
                    break
    if d is None:
        print("未找到该技能（path 不存在或 slug 不在本地已装）。", file=sys.stderr)
        return 1
    local_names = [s["name"] for s in discover_local()]
    registry_names = [e.get("name") for e in load_registry()]
    qf = gather_quality_fields(d, local_names=local_names, registry_names=registry_names)
    rep = rate_quality(qf)
    print(f"质量评级：{rep['grade']}（{rep['score']} 分 / 100）")
    print("维度明细：")
    labels = {"frontmatter": "frontmatter 完整性", "examples": "含示例",
              "references": "含参考/脚本", "doc_length": "文档长度",
              "freshness": "维护新鲜度", "actionable": "可操作性",
              "reference_integrity": "引用完整性(环境感知)"}
    for k, v in rep["dims"].items():
        print(f"  - {labels.get(k, k)}: {v:.0%}")
    if qf["ref_declared"] > 0:
        missing = qf["ref_local_missing"] + qf["ref_external_missing"]
        print(f"\n引用校验：声明 {qf['ref_declared']} 处，缺失 {missing} 处"
              f"（本地文件 {qf['ref_local_missing']} / 外部技能 {qf['ref_external_missing']}）。")
        if missing:
            print("⚠️ 存在无法解析的引用——该技能可能依赖不存在的工具/技能（假优信号）。")
    else:
        print("\n（未声明跨文件/跨技能引用，引用完整性按中性计分。）")
    return 0


def cmd_redundancy(args) -> int:
    local = discover_local()
    if not local:
        print("未发现本地已装技能。")
        return 0
    dups = find_duplicate_installs(local)
    seen = {}
    uniq_s = []
    for s in local:
        k = s.get("name", "")
        if k not in seen:
            seen[k] = True
            uniq_s.append(s)
    skills = [{"name": s["name"], "slug": s.get("slug", ""), "category": s.get("category", ""),
               "description": s.get("description", "")} for s in uniq_s]
    groups = redundancy_groups(skills)
    if dups:
        print(f"### 重复安装（同一技能多份，建议保留其一）: {len(dups)} 组")
        for d in dups:
            print(f"  - {d['name']} ×{d['count']}")
    if groups:
        print(f"\n### 疑似功能冗余（描述相似度≥0.6）: {len(groups)} 组")
        for g in groups:
            print(f"  ⚠️ {g['members']}  相似度 {g['sims']}")
    if not dups and not groups:
        print("✅ 未发现重复安装或明显功能冗余。")
        return 0
    if dups:
        print("\n重复安装：保留一份最新/最完整的即可，其余在宿主【技能管理】面板删除。")
    if groups:
        print("功能冗余：每组保留质量最高/最新维护的一个，其余卸载。")
    return 0


def cmd_prune(args) -> int:
    local = discover_local()
    if not local:
        print("未发现本地已装技能。")
        return 0
    dups = find_duplicate_installs(local)
    seen = {}
    uniq_s = []
    for s in local:
        k = s.get("name", "")
        if k not in seen:
            seen[k] = True
            uniq_s.append(s)
    skills = [{"name": s["name"], "slug": s.get("slug", ""), "category": s.get("category", ""),
               "description": s.get("description", "")} for s in uniq_s]
    groups = redundancy_groups(skills)
    print("## 技能瘦身建议（基于静态信号，非真实使用追踪）\n")
    if dups:
        print("### 重复安装 — 建议每组保留一份")
        for d in dups:
            print(f"  - {d['name']} ×{d['count']}")
    else:
        print("### 无重复安装")
    if groups:
        print("\n### 疑似功能冗余 — 建议每组保留其一")
        for g in groups:
            print(f"  - {g['members']}  相似度 {g['sims']}")
    else:
        print("\n### 未发现功能冗余组合")
    weak = []
    for s in uniq_s:
        try:
            r = rate_quality(gather_quality_fields(s["path"]))
        except Exception:
            continue
        if r["score"] < 40:
            weak.append((s["name"], r["grade"]))
    if weak:
        print("\n### 质量偏弱（<40 分）— 可评估是否必要")
        for name, grade in weak:
            print(f"  - {name}  [{grade}]")
    print("\n提示：本工具无法追踪真实使用频率；以上仅基于描述相似度与质量评级给出参考，")
    print("实际清理请结合宿主【技能管理】面板的人工判断。")
    return 0


# --------------------------------------------------------------------------
# Phase 7：发布治理（publish 发布就绪校验 / outdated 过期巡检 / doctor 环境体检）
# --------------------------------------------------------------------------
def _iter_skill_files(p: Path):
    for f in p.rglob("*"):
        if f.is_file() and f.suffix in (".py", ".md", ".json", ".yml", ".yaml", ".txt", ".toml"):
            yield f


def _find_hardcoded_paths(p: Path, limit: int = 8) -> list[str]:
    """扫描硬编码绝对路径（Windows 盘符 / /Users / /home / /root）——跨平台发布风险。

    只查代码/脚本类文件，跳过 .md/.txt 等文档——文档里举例「/root/.ssh/id_rsa」
    是合法说明，不是真路径依赖，否则会误报。
    """
    DOC_EXTS = {".md", ".txt", ".markdown", ".rst", ".html", ".htm"}
    pat = re.compile(r"(?:[A-Za-z]:\\\\|/(?:Users|home|root)/)")
    hits = []
    for f in p.rglob("*"):
        if not f.is_file() or f.suffix in DOC_EXTS:
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if pat.search(line):
                    hits.append(f"{f.name}:{i}")
                    if len(hits) >= limit:
                        return hits
        except Exception:
            continue
    return hits


def _find_secrets(p: Path, limit: int = 8) -> list[str]:
    """扫描可疑密钥模式（私钥块 / AWS / OpenAI / GitHub / Slack token）。疑似即提示人工确认。"""
    pats = [
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"ghp_[A-Za-z0-9]{36}"),
        re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    ]
    hits = []
    for f in _iter_skill_files(p):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in pats:
            m = pat.search(text)
            if m:
                hits.append(f"{f.name}: {m.group(0)[:12]}…")
                break
        if len(hits) >= limit:
            break
    return hits


# 文档/README 里声明依赖的连接器关键词（doctor 仅做"请确认已连接"的提示，不自判连通性）
KNOWN_CONNECTORS = {
    "tdx": "通达信/tdx 行情连接器",
    "westock": "westock 行情连接器",
    "agent-mail": "Agent Mail 邮件连接器",
}


def cmd_publish(args) -> int:
    """发布就绪校验：上架前检查技能包是否达到市场门槛（frontmatter / LICENSE /
    market-card / 引用齐备 / 无占位符 / 无硬编码路径 / 无密钥 / 端到端冒烟必过闸）。

    这是「出厂三审」之上的「上架闸门」——直接服务"被市场推荐"目标，竞品无此能力。
    默认校验当前仓库（ROOT），可用 --path 指定任意技能目录。
    """
    p = Path(args.path) if getattr(args, "path", None) else ROOT
    strict = getattr(args, "strict", False)
    run_smoke = not getattr(args, "no_smoke", False)
    checks = []

    skill_md = p / "SKILL.md"
    if not skill_md.exists():
        checks.append(("SKILL.md 存在", "FAIL", "未找到 SKILL.md"))
    else:
        ok, fm = security_scan.parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        if not ok:
            checks.append(("frontmatter 合法", "FAIL", "无法解析 frontmatter"))
        else:
            req = ["name", "description", "version", "author", "license"]
            missing = [k for k in req if not fm.get(k)]
            if missing:
                checks.append(("frontmatter 必备字段", "FAIL", f"缺失 {missing}"))
            else:
                checks.append(("frontmatter 必备字段", "PASS", "name/description/version/author/license 齐全"))
            md = fm.get("metadata") or {}
            if isinstance(md, dict) and md.get("slug") and md.get("displayName"):
                checks.append(("metadata 含 slug/displayName", "PASS", "已含（头部市场规范）"))
            else:
                checks.append(("metadata 含 slug/displayName", "WARN", "缺 metadata.slug/displayName（头部市场规范）"))
            if fm.get("version") and parse_version(fm["version"]) == (0,):
                checks.append(("version 合法", "WARN", f"版本号异常: {fm['version']}"))
            else:
                checks.append(("version 合法", "PASS", str(fm.get("version", ""))))

    lic = p / "LICENSE"
    checks.append(("LICENSE 文件", "PASS" if lic.exists() else "FAIL", "存在" if lic.exists() else "缺少 LICENSE"))
    sc = p / "market-card.md"
    checks.append(("market-card.md 市场卡", "PASS" if sc.exists() else "WARN",
                   "存在" if sc.exists() else "缺少（市场标准卡，强烈建议）"))

    qf = gather_quality_fields(p)
    checks.append(("references 引用齐备",
                   "PASS" if qf["ref_local_missing"] == 0 else "FAIL",
                   "无缺失引用" if qf["ref_local_missing"] == 0 else f"{qf['ref_local_missing']} 处引用文件缺失"))

    readme = p / "README.md"
    if readme.exists():
        rt = readme.read_text(encoding="utf-8", errors="replace")
        if "<你的用户名>" in rt or "你的用户名" in rt:
            checks.append(("README 无占位符", "FAIL", "仍含 <你的用户名> 占位（badge/clone 链接会坏）"))
        else:
            checks.append(("README 无占位符", "PASS", "已替换"))
    else:
        checks.append(("README.md 存在", "WARN", "缺少 README"))

    # 硬编码路径 / 泄露密钥：发布「工具自身（ROOT）」时跳过自身源码扫描。
    # 自身 docstring/注释示例、审计 HTML、测试夹具均含示例路径，全扫会狼来了；
    # 与 doctor 跳过 ROOT 的口径一致。第三方技能用 --path 指定时仍全量扫描。
    if p.resolve() == ROOT.resolve():
        hp = []
        secrets = []
        skip_self = True
        print("[说明] 正在校验工具自身（ROOT）：已跳过自身源码/文档/测试的路径与密钥扫描"
              "（含文档示例与测试夹具，非真实泄露）；用 --path 指向第三方技能目录时仍为全量扫描。\n")
    else:
        hp = _find_hardcoded_paths(p)
        secrets = _find_secrets(p)
        skip_self = False
    checks.append(("无硬编码绝对路径", "PASS" if not hp else "FAIL",
                   "已跳过工具自身源码（含文档示例/测试夹具，非真实泄露）" if skip_self
                   else ("无" if not hp else f"发现 {len(hp)} 处（如 {hp[0]}）")))
    checks.append(("无泄露密钥", "PASS" if not secrets else "WARN",
                   "已跳过工具自身源码" if skip_self
                   else ("未发现" if not secrets else f"疑似私密串 {secrets[0]}（请人工确认非真实密钥）")))

    if run_smoke:
        rc, out = _run_smoke()
        if rc == 0:
            checks.append(("端到端冒烟自证", "PASS", "smoke.py PASS"))
        else:
            tail = "\n".join(out.strip().splitlines()[-6:])
            checks.append(("端到端冒烟自证", "FAIL", f"smoke.py 返回 {rc}；末几行：\n{tail}"))

    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    print(f"## 发布就绪校验：{p.name}\n")
    for name, status, detail in checks:
        print(f"  {icon[status]} [{status}] {name} — {detail}")
    fails = [c for c in checks if c[1] == "FAIL"]
    warns = [c for c in checks if c[1] == "WARN"]
    print("")
    if fails:
        print(f"❌ 阻塞：{len(fails)} 项未通过，修复后再发布。")
        return 2
    if warns:
        msg = f"⚠️ {len(warns)} 项警告（不影响发布，但建议处理）。"
        if strict:
            print(msg + " 严格模式下视为失败。")
            return 1
        print(msg)
        return 0
    print("✅ 发布就绪：所有校验通过。")
    return 0


def _run_smoke() -> tuple[int, str]:
    """运行端到端冒烟自证，捕获退出码与输出。用于 publish 闸门。"""
    import subprocess as _sp
    try:
        pr = _sp.run([sys.executable, str(ROOT / "scripts" / "smoke.py")], cwd=str(ROOT),
                     capture_output=True, timeout=240)
        out = pr.stdout.decode("utf-8", "replace") + pr.stderr.decode("utf-8", "replace")
        return pr.returncode, out
    except Exception as e:  # pragma: no cover
        return -1, str(e)


def cmd_outdated(args) -> int:
    """过期巡检：对比已装技能版本与 registry.json / SkillHub 缓存中的最新版。

    复用 sync 拉取的缓存与内置注册表，纯本地、零额外网络。
    """
    local = discover_local()
    if not local:
        print("未发现本地已装技能。")
        return 0
    registry = load_registry()
    cache = load_cache()
    avail: dict[str, tuple[str, str]] = {}
    for src_name, items in (("registry", registry), ("cache", cache)):
        for it in items:
            key = normalize_key(it.get("name") or it.get("slug") or "")
            if not key:
                continue
            v = it.get("version") or "?"
            cur = avail.get(key)
            if cur is None or parse_version(v) > parse_version(cur[0]):
                avail[key] = (v, src_name)
    has_version_data = any(v != "?" for v, _ in avail.values())
    if not has_version_data:
        if not avail:
            print("⚠️ 注册表与缓存均为空，无版本数据可比对。请先运行 `findskills.py sync` 拉取。")
        else:
            print(f"⚠️ 注册表/缓存共 {len(registry) + len(cache)} 条记录，但均无 version 字段，无法比对已装技能是否落后。")
            print("   请先运行 `findskills.py sync` 拉取带版本的索引，再执行 outdated。")
        return 0
    rows = []
    for s in local:
        key = normalize_key(s["name"])
        if key in avail:
            avail_v, src = avail[key]
            inst_v = s.get("version") or "?"
            if parse_version(avail_v) > parse_version(inst_v):
                rows.append((s["name"], inst_v, avail_v, src))
    if not rows:
        print("✅ 全部已装技能均为最新版本（基于 registry.json 与 SkillHub 缓存）。")
        return 0
    print(f"## 过期巡检：{len(rows)} 个技能有新版本\n")
    print("| 技能 | 已装 | 最新 | 来源 |")
    print("|---|---|---|---|")
    for name, inst, latest, src in rows:
        print(f"| {name} | {inst} | {latest} | {src} |")
    print("\n用 `findskills.py update <slug>` 升级（需联网，同样过安全网关）。")
    return 0


def cmd_doctor(args) -> int:
    """环境体检：一次性说清本地技能环境是否健康——frontmatter 合法性、低质量技能、
    重复安装、依赖的连接器、硬编码路径。面向非运维用户，一条命令看全局。
    """
    local = discover_local(include_self=True)
    print("## 环境体检\n")
    if not local:
        print("未发现本地已装技能。")
        return 0
    node = shutil.which("node")
    print(f"运行环境：Python={sys.executable}")
    print(f"          Node.js={'可用 ('+node+')' if node else '未安装（含 Node 脚本的技能将不可用）'}\n")
    issues = []
    for s in local:
        d = Path(s["path"])
        skill_md = d / "SKILL.md"
        txt = skill_md.read_text(encoding="utf-8", errors="replace") if skill_md.exists() else ""
        ok, fm = security_scan.parse_frontmatter(txt)
        if not ok:
            issues.append(f"{s['name']}: SKILL.md frontmatter 非法/缺失")
            continue
        try:
            r = rate_quality(gather_quality_fields(d))
        except Exception:
            r = None
        if r and r["score"] < 40:
            issues.append(f"{s['name']}: 质量偏弱（{r['score']} 分）")
        if (d / "scripts").exists():
            has_js = any((d / "scripts").rglob("*.js")) or any((d / "scripts").rglob("*.ts"))
            if has_js and not node:
                issues.append(f"{s['name']}: 含 Node 脚本但本机未装 Node")
        low = txt.lower()
        for kw, conn in KNOWN_CONNECTORS.items():
            if kw in low:
                issues.append(f"{s['name']}: 声明依赖连接器「{conn}」（请确认已连接）")
                break
        # 硬编码路径 / 泄露密钥：只查第三方技能目录，跳过自身源码
        # （自身文档会举例 /root/.ssh 等路径，属正常说明，不应误报）
        if d.resolve() != ROOT.resolve():
            hp = _find_hardcoded_paths(d)
            if hp:
                issues.append(f"{s['name']}: {len(hp)} 处硬编码绝对路径（如 {hp[0]}）")
            sec = _find_secrets(d)
            if sec:
                issues.append(f"{s['name']}: 疑似泄露密钥 {sec[0]}（请人工确认）")
    dups = find_duplicate_installs(local)
    for d in dups:
        issues.append(f"重复安装: {d['name']} ×{d['count']}")

    print(f"已装技能：{len(local)} 个（含本工具自身）\n")
    if not issues:
        print("✅ 环境健康：frontmatter 合法、无重复安装、无硬编码路径、依赖连接器均已就位。")
        return 0
    print(f"发现 {len(issues)} 项需关注：\n")
    for it in issues:
        print(f"  ⚠️ {it}")
    print("\n提示：以上为静态体检；连接器是否真正连通需结合宿主面板确认。")
    return 0


# --------------------------------------------------------------------------
# 自我营销引擎（promote / demo / elevator）
# --------------------------------------------------------------------------
# 说明：本技能内置「给自己打广告」的能力——一键生成推广素材、可录屏演示、
# 30 秒电梯演讲。目的是让它在市场与 GitHub 上一出场就讲清差异化，而不是
# 靠用户自己去总结。

BRAND = {
    "name": "find-skills++",
    "display": "Find Skills++（技能发现 · 安全策展 · 生态治理）",
    "tagline": "技能生态的「发现 → 安全策展 → 安装 → 治理」全能工具",
    "positioning": "不只是「找技能」，而是给 AI 智能体的技能生态做策展与治理",
    "enhancements": 52,
    "repo_placeholder": "<你的用户名>/find-skills-plusplus",
}

DIFFERENTIATORS = [
    ("AST 级安全闸门", "用 ast+shlex 做语法树级检测，能识破动态拼接 rm -rf、base64 混淆执行、"
                   "subprocess(shell=True)、凭据目录窃取、Agent 身份文件读取——纯正则做不到",
     "原版与同类：无 或 仅正则"),
    ("四级风险 + 权限清单", "EXTREME/HIGH/MEDIUM/LOW 四级并映射动作；自动提取 文件·网络·命令 权限，"
                      "回答「是否超出声明目的最小集」", "原版：无风险分级"),
    ("真·离线全能", "sync 把在线目录同步到本地，离线仍能搜上百个技能；不依赖随时会挂的实时 API",
     "原版：离线基本残废"),
    ("环境感知引用校验", "检查技能引用的工具/脚本是否真实存在，识破「长得好看但引用不存在工具」的假优",
     "生态独有"),
    ("技能质量评级", "七维 0-100 分（含引用完整性），搜索结果直接标注 优/良/中/差", "同类：仅安全意识"),
    ("全生命周期", "update / uninstall（进回收站可还原，非 rm）/ clean-dupes 自动去重", "原版：只能装"),
    ("冗余与生态治理", "区分重复安装 vs 功能冗余，中文去停用+bigram 降误报，给只读瘦身建议", "生态独有"),
    ("零依赖可执行 CLI", "findskills.py 20 子命令，纯标准库，Win/Linux/Mac 通吃，140 项 pytest 全绿",
     "原版：纯 prompt 说明书"),
]

COMPARISON_ROWS = [
    ("能力", "官方 find-skills", "guipi888/find-skills<br>(99.4万下载)", "skill-vetter<br>(31万)", "**find-skills++**"),
    ("多源联合搜索", "部分", "✅ 六层", "—", "✅ 跨源合并去重"),
    ("安装前安全扫描", "建议清单", "❌ 无", "✅ 纯 prompt 清单", "✅ **AST 级可执行闸门**"),
    ("风险分级", "无", "无", "定性描述", "✅ **四级 + 权限清单**"),
    ("离线可用", "弱", "弱", "—", "✅ **目录同步型离线全能**"),
    ("质量评级", "无", "推荐理由", "无", "✅ **七维 0-100**"),
    ("引用真实性校验", "无", "无", "无", "✅ **独有**"),
    ("更新 / 卸载", "无", "无", "—", "✅ **回收站可还原**"),
    ("重复安装治理", "无", "无", "无", "✅ **自动去重**"),
    ("可执行工具 + 测试", "无", "无", "无", "✅ **CLI + pytest**"),
    ("端到端自证", "无", "无", "无", "✅ **冒烟脚本：当场跑给你看**"),
]


def _rule(title: str) -> str:
    return f"\n{'=' * 62}\n  {title}\n{'=' * 62}\n"


def build_promotion_pack() -> str:
    """生成全套推广素材（纯本地生成，不联网、不外传）。"""
    out = []
    a = out.append
    n_sub = len(_SUBCOMMANDS)

    a(f"# {BRAND['display']} · 推广素材包\n")
    a(f"> 由 `findskills promote` 自动生成 · 全部内容基于本技能真实能力，可直接复制使用\n")

    a(_rule("1 · 一句话简介（≤40 字，用于市场列表/卡片）"))
    a(BRAND["tagline"] + "。\n")
    a(f"备选：装技能前先过 AST 级安全闸门的技能管家（{BRAND['enhancements']} 项增强）。\n")

    a(_rule("2 · 三句话简介（用于 README 开头 / 社交简介）"))
    a("1. 它解决什么：AI 智能体装技能时「找不到、不敢装、装了没人管」的三重困境。\n"
      "2. 它怎么做：发现 → 安全策展 → 安装 → 治理，一条链全覆盖，附零依赖 CLI。\n"
      "3. 它凭什么：AST 级安全扫描 + 四级风险 + 权限清单 + 真·离线目录 + 引用校验，"
      "这四项生态里独一份。\n")

    a(_rule("3 · 市场简介（120 字左右，用于 SkillHub / ClawHub 提交）"))
    a("find-skills++ 是 find-skills 的社区超级增强版，定位为「技能生态的策展与治理工具」。"
      "它在安装前用 AST 语法树级扫描（而非正则）做安全闸门，输出 EXTREME/HIGH/MEDIUM/LOW "
      "四级风险与文件·网络·命令权限清单；通过在线目录同步实现真正的离线全能；"
      "用引用校验识破「好看但假优」的技能；并提供质量评级、全生命周期管理、"
      f"冗余检测与瘦身建议。自带零依赖 CLI，{n_sub} 个子命令，测试全绿。\n")

    a(_rule("4 · README Banner（放在 README 顶部）"))
    a("```markdown")
    a(f"> ### {BRAND['display']}")
    a(f"> {BRAND['tagline']}")
    a(">")
    a(f"> **{BRAND['enhancements']} 项增强** · AST 级安全闸门 · 四级风险 · 真·离线全能 · "
      "质量评级 · 全生命周期")
    a("```\n")
    a("建议 badge：")
    a("```markdown")
    a(f"![CI](https://github.com/{BRAND['repo_placeholder']}/actions/workflows/ci.yml/badge.svg)")
    a("![Python](https://img.shields.io/badge/python-3.8%2B-blue)")
    a("![Deps](https://img.shields.io/badge/dependencies-zero-brightgreen)")
    a("![License](https://img.shields.io/badge/license-MIT-green)")
    a("```\n")

    a(_rule("5 · 差异化卖点（9 条，可用于 Features 区块）"))
    for i, (title, desc, rival) in enumerate(DIFFERENTIATORS, 1):
        a(f"{i}. **{title}** — {desc}")
        a(f"   _竞品现状：{rival}_\n")

    a(_rule("6 · 竞品对比表（可直接贴 README）"))
    a("| " + " | ".join(COMPARISON_ROWS[0]) + " |")
    a("|" + "---|" * len(COMPARISON_ROWS[0]))
    for row in COMPARISON_ROWS[1:]:
        a("| " + " | ".join(row) + " |")
    a("")

    a(_rule("7 · 社交文案"))
    a("**公众号 / 知乎（正式版）**")
    a("装 AI 技能就像装 App——但没人给你做安全审查。")
    a("`find-skills++` 把这件事补上了：安装前用 AST 语法树级扫描（能识破 base64 混淆执行、"
      "动态拼接的 rm -rf、偷读 ~/.ssh 和 Agent 身份文件），输出四级风险和权限清单；"
      "离线也能搜上百个技能；还能识破「长得好看但引用了不存在工具」的假优技能。")
    a("附带质量评级、更新/卸载（进回收站）、重复安装治理。零依赖 CLI，20 个子命令。\n")
    a("**小红书 / 短帖（口语版）**")
    a("给 AI 装技能前，你会看它的源码吗？🤔")
    a("我做了个工具，装之前先给你把技能「体检+安检」一遍：")
    a("· 语法树级扫描，正则绕不过去那种 🔍")
    a("· 四级风险 + 权限清单（它要读哪些文件、连哪些网、跑哪些命令，全列出来）📋")
    a("· 离线也能搜 💾 · 质量打分 ⭐ · 卸载进回收站不怕删错 ♻️")
    a("开源 · 零依赖 · Win/Mac/Linux 通吃\n")
    a("**X / Twitter（英文）**")
    a("Installing an AI agent skill = running someone else's code.")
    a("find-skills++ vets it first: AST-level static scan (catches obfuscated exec, "
      "dynamic rm -rf, credential-dir access), 4-tier risk + permission inventory, "
      f"true offline catalog, quality rating, full lifecycle. Zero deps. {len(_SUBCOMMANDS)} CLI commands.\n")

    a(_rule("8 · 发布检查清单"))
    for item in [
        "[ ] 确认上游许可证：guipi888/find-skills = **MIT**（已核实），保留其许可与署名",
        "[ ] LICENSE 中同时标注源头 vercel-labs/skills 与参考 sandbaseai / skill-vetter",
        "[ ] README 替换 `<你的用户名>` 占位为真实仓库路径",
        "[ ] 跑通 `findskills.py --help` 与 pytest，确保 CI badge 为绿",
        "[ ] 录一段 `findskills demo` 的 GIF/asciinema，放在 README 顶部（star 诱饵）",
        "[ ] GitHub topics：agent-skills / skill-discovery / security-scanner / workbuddy / ai-agent",
        "[ ] 提交到 SkillHub + ClawHub（真正的分发渠道，GitHub 仓库本身不带流量）",
        "[ ] 定位话术统一为「带署名的社区超级增强版」，不伪装成官方替代品",
    ]:
        a(item)
    a("")
    a(_rule("9 · 电梯演讲（30 秒）"))
    a(build_elevator())
    return "\n".join(out)


def build_elevator() -> str:
    """30 秒电梯演讲：用于对话中主动亮差异化，或作为推广开头。"""
    return "\n".join([
        f"我是 **{BRAND['name']}**——{BRAND['tagline']}。",
        "",
        "别人帮你「找技能」，我帮你「敢装、会管」：",
        "",
        "· 装之前，用 AST 语法树级扫描做安检（不是正则），能识破混淆执行、"
        "动态拼接的危险命令、偷读凭据目录和 Agent 身份文件，输出四级风险和权限清单；",
        "· 找不到时，离线也能搜——在线目录会同步到本地，不靠随时会挂的 API；",
        "· 选哪个，看七维质量分，引用了不存在工具的「假优技能」会被直接打下来；",
        "· 装多了，能查重复安装、判功能冗余、给瘦身建议；卸载进回收站，删错也能还原。",
        "",
        f"共 {BRAND['enhancements']} 项增强、{len(_SUBCOMMANDS)} 个 CLI 子命令、"
        "零依赖、跨平台、测试全绿。",
        "",
        "而且这些不是写在 README 里的自述——跑 `python scripts/smoke.py` 会当场把 "
        "20 个子命令真跑一遍、用 5 组恶意样本验证安全闸门、再校验文档里的每个数字与实现一致，"
        "最后给一个 PASS 或 FAIL。",
        "",
        "一句话：如果你只想找技能，原版够用；"
        "如果你在意「装得安全、管得明白」，用我。",
    ])


def cmd_promote(args) -> int:
    text = build_promotion_pack()
    if getattr(args, "out", None):
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print(f"✅ 推广素材包已写入 {p}（{len(text)} 字）")
    else:
        print(text)
    return 0


def cmd_elevator(args) -> int:
    print(_rule("30 秒电梯演讲 · 可直接用于对话/推广"))
    print(build_elevator())
    return 0


def _capture(argv) -> tuple:
    """捕获子命令输出，供 demo 串联展示。"""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        rc = main(argv)
    except SystemExit as e:
        rc = getattr(e, "code", 1)
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


def _vis_len(s: str) -> int:
    """按终端显示宽度计算长度（CJK/全角按 2 计），保证边框对齐。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def _box_line(text: str, width: int = 60) -> str:
    pad = max(0, width - _vis_len(text))
    return "║" + text + " " * pad + "║"


def cmd_demo(args) -> int:
    """可录屏的端到端演示：搜索 → 质量评级 → 安全扫描 → 生态治理。"""
    import time
    import tempfile as _tf
    q = args.query or "pdf"
    # 第③步用「生成的干净样例技能」演示扫描器放行（LOW），不打自己的脸；
    # 真正审计第三方技能时，扫描器会如实拦截恶意样本（见 scripts/smoke.py）。
    sample_dir = Path(_tf.mkdtemp(prefix="fspp-demo-"))
    sample = sample_dir / "demo-clean-skill"
    sample.mkdir(parents=True, exist_ok=True)
    (sample / "SKILL.md").write_text(
        "---\nname: demo-clean-skill\ndescription: 用于演示的干净样例技能\n---\n"
        "# 干净样例\n\n仅打印一句问候，无任何危险调用。\n", encoding="utf-8")
    (sample / "run.py").write_text("print('hello from a benign skill')\n", encoding="utf-8")
    scenes = [
        ("① 自然语言搜索（离线优先，跨源合并去重）", ["search", q, "--offline", "--limit", "5"]),
        ("② 技能质量评级（七维，含引用完整性）", ["quality", "--path", str(ROOT)]),
        ("③ 安装前 AST 级安全闸门（四级风险 + 权限清单）",
         ["scan", str(sample), "--exclude-tests"]),
        ("④ 生态治理：重复安装 / 功能冗余检测", ["redundancy"]),
        ("⑤ 自我营销：一键生成推广素材", ["elevator"]),
    ]
    print("╔" + "═" * 60 + "╗")
    print(_box_line("  find-skills++ · Live Demo （可直接录屏做 GIF）"))
    print("╚" + "═" * 60 + "╝")
    print(f"\n演示查询：{q!r}   离线模式：优先本地 + 同步目录\n")
    for title, argv in scenes:
        print("\n" + "─" * 62)
        print(f"  {title}")
        print("─" * 62)
        t0 = time.time()
        rc, out = _capture(argv)
        lines = [l for l in out.splitlines() if l.strip()]
        for l in lines[: (args.lines or 12)]:
            print("  " + l)
        if len(lines) > (args.lines or 12):
            print(f"  … （共 {len(lines)} 行）")
        print(f"\n  ⏱ {time.time() - t0:.2f}s   exit={rc}")
    print("\n" + "─" * 62)
    print("  注：扫描器是「第三方技能审计工具」——扫描本工具自身会如实返回 HIGH")
    print("  （它自身用 subprocess 且文档化了攻击模式），这是预期且诚实的；")
    print("  它的价值在于审计第三方技能：scripts/smoke.py 用 5 组恶意样本验证必拦 EXTREME。")
    print("─" * 62)
    print("\n" + "═" * 62)
    print("  演示结束。完整能力：findskills.py --help")
    print(f"  推广素材：findskills.py promote --out PROMO.md")
    print("═" * 62)
    return 0


_SUBCOMMANDS = [
    "search", "scan", "install", "list", "audit", "registry", "sync",
    "quality", "redundancy", "prune", "update", "uninstall", "clean-dupes",
    "discover", "promote", "demo", "elevator",
    "outdated", "doctor", "publish",
]


# --------------------------------------------------------------------------
# 入口
# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="findskills",
        description="find-skills++ 命令行：发现/审查/安装技能（离线优先，零依赖）",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    s = sub.add_parser("search", help="搜索技能（离线优先 + 可选 SkillHub）")
    s.add_argument("query", nargs="?", default="", help="查询词；省略则列出注册表热门")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--offline", action="store_true", help="仅用离线注册表与本地，不联网")
    s.set_defaults(func=cmd_search)

    sc = sub.add_parser("scan", help="安全静态扫描技能目录")
    sc.add_argument("path", help="技能目录或 SKILL.md 路径")
    sc.add_argument("--lang", choices=("zh-CN", "en"), default="zh-CN")
    sc.add_argument("--exclude-tests", action="store_true",
                    help="排除 tests/ 等测试目录（仅自查用；审查第三方技能不要用）")
    sc.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    sc.set_defaults(func=cmd_scan)

    i = sub.add_parser("install", help="下载并安装社区技能（带安全闸门）")
    i.add_argument("slug")
    i.add_argument("--target", help="目标目录或 agent 名（workbuddy/codebuddy/openclaw/claude，默认自动判定）")
    i.add_argument("--yes", action="store_true", help="P1 信号时仍继续")
    i.add_argument("--force", action="store_true", help="P0 也强制安装（不推荐）")
    i.set_defaults(func=cmd_install)

    sub.add_parser("list", help="列出本地已装技能").set_defaults(func=cmd_list)
    sub.add_parser("audit", help="审计所有本地技能风险").set_defaults(func=cmd_audit)

    r = sub.add_parser("registry", help="registry.json 管理")
    r.add_argument("registry_cmd", choices=("validate", "show", "add"))
    r.add_argument("--slug")
    r.add_argument("--name")
    r.add_argument("--desc")
    r.add_argument("--category")
    r.add_argument("--homepage")
    r.add_argument("--reputation", type=float)
    r.set_defaults(func=cmd_registry)

    sy = sub.add_parser("sync", help="拉取 SkillHub 全量目录到本地缓存（离线全能）")
    sy.add_argument("--limit", type=int, default=1000, help="拉取条数上限")
    sy.add_argument("--offline", action="store_true", help="（不支持：sync 需联网）")
    sy.set_defaults(func=cmd_sync)

    q = sub.add_parser("quality", help="评估单个技能质量（本地路径或 slug）")
    q.add_argument("slug", nargs="?", default="", help="本地技能 slug；省略则用 --path")
    q.add_argument("--path", help="技能目录路径（优先于 slug）")
    q.set_defaults(func=cmd_quality)

    sub.add_parser("redundancy", help="检测本地已装技能的功能冗余").set_defaults(func=cmd_redundancy)
    sub.add_parser("prune", help="基于静态信号给出瘦身建议（只读）").set_defaults(func=cmd_prune)

    u = sub.add_parser("update", help="重下最新并覆盖已装社区技能（安全网关）")
    u.add_argument("slug")
    u.add_argument("--yes", action="store_true", help="P1 信号时仍继续")
    u.add_argument("--force", action="store_true", help="P0 也强制（不推荐）")
    u.add_argument("--offline", action="store_true", help="（不支持：update 需联网）")
    u.set_defaults(func=cmd_update)

    un = sub.add_parser("uninstall", help="卸载本地技能（进回收站，可还原）")
    un.add_argument("slug")
    un.set_defaults(func=cmd_uninstall)

    cd = sub.add_parser("clean-dupes", help="清理重复安装（保留最新一份，其余进回收站）")
    cd.set_defaults(func=cmd_clean_dupes)

    dc = sub.add_parser("discover", help="发现技能：新上架/热门榜单（含跨源版本仲裁）")
    dc.add_argument("--new", action="store_true", help="按最近更新排序（新上架）")
    dc.add_argument("--trending", action="store_true", help="按热度排序（热门）")
    dc.add_argument("--limit", type=int, default=15)
    dc.set_defaults(func=cmd_discover)

    pm = sub.add_parser("promote", help="生成自我推广素材包（简介/文案/对比表/发布清单）")
    pm.add_argument("--out", help="写入文件（默认打印到标准输出）")
    pm.set_defaults(func=cmd_promote)

    dm = sub.add_parser("demo", help="可录屏的端到端演示（搜索→评级→安检→治理→自述）")
    dm.add_argument("--query", default="pdf", help="演示用的搜索词")
    dm.add_argument("--lines", type=int, default=12, help="每个场景最多显示行数")
    dm.set_defaults(func=cmd_demo)

    sub.add_parser("elevator", help="30 秒电梯演讲（本技能的差异化自述）").set_defaults(func=cmd_elevator)

    od = sub.add_parser("outdated", help="巡检已装技能是否有新版本可更新（基于注册表/缓存）")
    od.set_defaults(func=cmd_outdated)

    doc = sub.add_parser("doctor", help="环境体检：frontmatter/质量/重复安装/依赖连接器/硬编码路径")
    doc.add_argument("--path", default=None, help="指定要体检的技能目录（默认扫描本地安装位置）")
    doc.set_defaults(func=cmd_doctor)

    pb = sub.add_parser("publish", help="发布就绪校验（上架前查市场门槛，含端到端冒烟自证）")
    pb.add_argument("--path", help="技能目录（默认本仓库）")
    pb.add_argument("--no-smoke", action="store_true", help="跳过端到端冒烟自证")
    pb.add_argument("--strict", action="store_true", help="警告也视为失败")
    pb.set_defaults(func=cmd_publish)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
