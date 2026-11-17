#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 兄弟技能自动发现与能力匹配注册表（B 项实现）

设计目标（2026-09-29）：
  - 本地只读扫描技能根目录（默认 ~/.workbuddy/skills，env CT_SKILLS_DIR 可覆盖）下
    ct-* 目录 + tool_mapping.json tiers.registry 登记的非 ct- 前缀兄弟技能
    （meta-analysis / statsoft-cli / statdata-transfer）的 frontmatter
    （triggers/summary/description），构建「能力关键词 → 技能」映射注册表，
    替代 tool_mapping.json 中的硬编码 tiers.registry。
  - 注册表驱动 route_tool.py 的 suggest_footer：基于实际安装的技能动态生成
    「如需真实数据可调用...」软建议，避免建议未安装/不存在的技能。
  - 不修改 need_tool 的硬判定逻辑（TOOL_TRIGGERS / WEAK_TRIGGERS 不变），控制误报风险。

用法：
  python scripts/discover_siblings.py
        → 扫描 skills 目录，生成 sibling_registry.json（JSON 格式能力映射）
  python scripts/discover_siblings.py --pretty
        → 同上，输出格式化 JSON
  python scripts/discover_siblings.py --check
        → 检查注册表是否与 tool_mapping.json 的 tiers.registry 一致，报告差异
  python scripts/discover_siblings.py --ensure-fresh
        → 检查注册表是否新鲜（<24h），否则自动刷新（供调用链路惰性调用）

调用时机（三层保障）：
  1. 安装/卸载时：install_sibling.py 成功后立即调用 refresh() —— 注册表即时更新
  2. 调用时：suggest_footer() 先调 ensure_fresh(max_age_hours=24) —— 兜底过期注册表
  3. 手动：discover_siblings.py --force —— 按需重建

注册表格式（sibling_registry.json）：
  {
    "version": "2026-09-29",
    "skills": {
      "ct-registry": {
        "name": "ct-registry",
        "display_name": "Clinical Trial Registry Search / 临床试验注册检索专家",
        "version": "0.10.0",
        "summary": "跨源检索全球临床试验注册库...",
        "triggers": ["clinical trial registry search", ...],
        "tier": "A",
        "published": true,
        "installed": true,
        "install_path": "/home/.../ct-registry",
        "capabilities": ["registry_search", "competitor_landscape", ...],
        "trigger_keywords": ["注册", "检索", "竞品格局", ...]
      },
      ...
    },
    "capability_index": {
      "registry_search": ["ct-registry"],
      "competitor_landscape": ["ct-registry"],
      "safety_signal": ["ct-safety"],
      ...
    }
  }
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REGISTRY_PATH = SCRIPT_DIR / "sibling_registry.json"
TOOL_MAPPING_PATH = SCRIPT_DIR / "tool_mapping.json"

# 技能根目录
SKILLS_DIR = os.environ.get(
    "CT_SKILLS_DIR",
    str(Path.home() / ".workbuddy" / "skills"),
)

# frontmatter 解析：提取 triggers / summary / description / displayName / tier 等
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
YAML_LINE_RE = re.compile(r"^(\w[\w_]*):\s*(.*?)\s*$")
YAML_LIST_RE = re.compile(r"^-\s+(.*?)\s*$")


def _known_sibling_names() -> set:
    """tool_mapping.json tiers.registry 登记的非 ct- 前缀兄弟技能。

    2026-10-14：meta-analysis / statsoft-cli / statdata-transfer 是合法兄弟
    （tool_mapping tier=A）但目录名不带 ct- 前缀，被前缀过滤挡在注册表外
    （--check 报三条「未扫描到」）。此处从 tool_mapping 派生白名单而非硬编码，
    单一数据源；技能库里大量无关技能（clinical / drug-discovery-search 等）
    仍不进注册表。
    """
    try:
        mapping = json.loads(TOOL_MAPPING_PATH.read_text(encoding="utf-8"))
    except Exception:
        return set()
    tiers = mapping.get("tiers", {}).get("registry", {})
    return {
        name for name, info in tiers.items()
        if info.get("tier") != "meta" and not name.startswith("ct-")
    }


def _parse_frontmatter(text: str) -> dict:
    """简易 YAML frontmatter 解析（仅处理本项目 SKILL.md 的扁平结构）。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    body = m.group(1)
    fm = {}
    # 先提取 triggers 块（特殊处理列表）
    triggers_match = re.search(r"^triggers:\s*\n((?:^\s+-[^\n]+\n)+)", body, re.MULTILINE)
    if triggers_match:
        triggers = re.findall(r"^\s+-\s+(.+)$", triggers_match.group(1), re.MULTILINE)
        fm["triggers"] = [t.strip().strip('"').strip("'") for t in triggers]
    # 再处理其他字段
    for line in body.split("\n"):
        line = line.strip()
        if not line or line == "---":
            continue
        if line.startswith("triggers:"):
            continue
        m_line = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if m_line:
            key, val = m_line.group(1), m_line.group(2).strip().strip('"').strip("'")
            if val == "":
                fm[key] = []
            else:
                fm[key] = val
    return fm


def _scan_skill(skill_dir: Path, extra_siblings: set | None = None) -> dict | None:
    """扫描单个技能目录，提取 frontmatter 和能力信息。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    fm = _parse_frontmatter(text)
    if not fm:
        return None
    extra = extra_siblings or set()
    name = fm.get("name", skill_dir.name)
    # 只处理 ct-* 系列 + tool_mapping 登记的非 ct- 兄弟技能
    if (
        not name.startswith("ct-")
        and not skill_dir.name.startswith("ct-")
        and name not in extra
        and skill_dir.name not in extra
    ):
        return None
    # 跳过 ct-advisor 自身和元层技能
    if name in ("ct-advisor", "ct-base", "ct-update"):
        return None
    return {
        "name": name,
        "display_name": fm.get("displayName", name),
        "version": fm.get("version", "0.0.0"),
        "summary": fm.get("summary", ""),
        "triggers": fm.get("triggers", []),
        "tier": _resolve_tier(fm, name),
        "published": _resolve_published(fm, name),
        "installed": True,
        "install_path": str(skill_dir),
        "capabilities": _extract_capabilities(fm),
    }


def _resolve_tier(fm: dict, name: str) -> str:
    """从 frontmatter 或 tool_mapping.json 推断 tier。"""
    # 尝试从 metadata 推断
    metadata = fm.get("metadata", "")
    if isinstance(metadata, str) and "tier" in metadata.lower():
        m = re.search(r'tier["\s:=]+([AB])', metadata, re.I)
        if m:
            return m.group(1).upper()
    # 已知 tier 映射（fallback）
    tier_b = {"ct-protocol", "ct-ecrf", "ct-datacheck", "ct-statrev", "ct-sdtm",
              "ct-adam", "ct-analysis", "ct-tlf", "ct-csr", "ct-submission",
              "ct-eligibility", "ct-congress"}
    return "B" if name in tier_b else "A"


def _resolve_published(fm: dict, name: str) -> bool:
    """推断是否已发布（A 档默认已发布，B 档默认未发布）。"""
    # 有 GitHub 链接 + version 通常意味着已发布
    github = fm.get("metadata", "")
    if isinstance(github, str) and "github.com" in github:
        return True
    tier = _resolve_tier(fm, name)
    if tier == "B":
        return False
    # A 档检查是否有 published 字段
    return True


def _extract_capabilities(fm: dict) -> list[str]:
    """从 triggers + summary 提取能力关键词（用于能力→技能映射）。"""
    caps = set()
    triggers = fm.get("triggers", [])
    if isinstance(triggers, str):
        triggers = [triggers]
    summary = fm.get("summary", "") or ""
    description = fm.get("description", "") or ""
    text = " ".join(triggers) + " " + summary + " " + description
    text = text.lower()

    # 能力关键词映射
    cap_keywords = {
        "registry_search": ["registry", "注册", "登记", "clinicaltrials.gov", "竞品格局", "landscape", "pipeline"],
        "safety_signal": ["safety", "signal", "安全", "不良事件", "prr", "ror", "ebm", "faers", "药物警戒"],
        "literature_search": ["literature", "文献", "pubmed", "openalex", "系统综述", "meta"],
        "sample_size": ["sample", "样本量", "power", "效能", "检验效能", "估算"],
        "eligibility": ["eligibility", "入组", "受试者", "方案匹配"],
        "protocol_review": ["protocol", "方案", "审阅", "审查"],
        "data_quality": ["data quality", "质控", "datacheck", "数据核查"],
        "sdtm_mapping": ["sdtm", "标准数据", "域映射"],
        "adam_derivation": ["adam", "分析数据集", "推导"],
        "statistical_analysis": ["statistical", "统计分析", "假设检验"],
        "tlg_generation": ["tlg", "三线表", "table", "listing", "figure"],
        "csr_report": ["csr", "临床研究报告", "ich e3"],
        "submission": ["submission", "申报", "ectd", "ctd"],
        "synthetic_data": ["synthetic", "合成数据", "测试数据", "fixture"],
        "pipeline_intel": ["pipeline", "情报", "intelligence", "竞品"],
    }
    for cap, keywords in cap_keywords.items():
        if any(kw in text for kw in keywords):
            caps.add(cap)
    return sorted(caps)


def scan_all_skills() -> dict:
    """扫描 skills 目录，生成完整注册表。"""
    skills = {}
    skills_dir = Path(SKILLS_DIR)
    if not skills_dir.is_dir():
        print(f"Warning: skills dir not found: {SKILLS_DIR}", file=sys.stderr)
        return skills
    extra = _known_sibling_names()
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir() and (entry.name.startswith("ct-") or entry.name in extra):
            info = _scan_skill(entry, extra)
            if info:
                skills[info["name"]] = info
    return skills


def build_capability_index(skills: dict) -> dict:
    """构建能力→技能的反向索引。"""
    index = {}
    for name, info in skills.items():
        for cap in info.get("capabilities", []):
            if cap not in index:
                index[cap] = []
            index[cap].append(name)
    return index


def generate_registry(pretty: bool = False) -> dict:
    """生成完整注册表。"""
    skills = scan_all_skills()
    registry = {
        "version": "2026-09-29",
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "source_dir": SKILLS_DIR,
        "skills": skills,
        "capability_index": build_capability_index(skills),
    }
    return registry


def check_consistency(registry: dict) -> list[str]:
    """检查注册表与 tool_mapping.json tiers.registry 的一致性。"""
    issues = []
    try:
        mapping = json.loads(TOOL_MAPPING_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        issues.append(f"tool_mapping.json 读取失败: {e}")
        return issues
    tiers = mapping.get("tiers", {}).get("registry", {})
    registry_skills = registry.get("skills", {})

    # 检查 tool_mapping 中的技能是否在注册表中
    for name, tier_info in tiers.items():
        if name not in registry_skills:
            if tier_info.get("tier") != "meta":
                issues.append(f"tool_mapping 有 {name} (tier={tier_info.get('tier')})，但注册表未扫描到（可能未安装）")
        else:
            # 检查 tier 是否一致
            reg_tier = registry_skills[name].get("tier")
            map_tier = tier_info.get("tier")
            if reg_tier != map_tier:
                issues.append(f"tier 不一致: {name} registry={reg_tier} vs mapping={map_tier}")
    return issues


def refresh(force: bool = False) -> dict:
    """刷新注册表（返回新注册表）。安装器调用。"""
    registry = generate_registry()
    indent = 2 if not force else None
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=indent)
    return registry


def ensure_fresh(max_age_hours: int = 24) -> dict:
    """检查注册表是否新鲜，否则自动刷新。

    新鲜度判据：注册表文件 mtime 距今 < max_age_hours。
    仅安装时的立即刷新 + 24h 周期刷新，不逐次扫描 skills 目录。
    """
    reg_path = Path(REGISTRY_PATH)
    if reg_path.exists():
        now = __import__("time").time()
        age_hours = (now - reg_path.stat().st_mtime) / 3600
        if age_hours < max_age_hours:
            try:
                return json.loads(reg_path.read_text(encoding="utf-8"))
            except Exception:
                pass
    return refresh(force=False)


def main():
    ap = argparse.ArgumentParser(description="Discover ct-* siblings and build capability registry")
    ap.add_argument("--pretty", action="store_true", help="输出格式化 JSON")
    ap.add_argument("--check", action="store_true", help="检查与 tool_mapping.json 的一致性")
    ap.add_argument("--output", default=str(REGISTRY_PATH), help="输出路径")
    args = ap.parse_args()

    registry = generate_registry(pretty=args.pretty)

    if args.check:
        issues = check_consistency(registry)
        if issues:
            print("=== 一致性问题 ===")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("✓ 注册表与 tool_mapping.json tiers.registry 一致")
        return 0

    # 保存注册表
    indent = 2 if args.pretty else None
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=indent)

    print(f"Registry saved: {args.output}")
    print(f"  Skills: {len(registry['skills'])}")
    print(f"  Capabilities: {len(registry['capability_index'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
