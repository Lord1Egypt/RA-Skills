#!/usr/bin/env python3
"""
scan_skills.py — 技能自动扫描/分类/索引引擎 v1.0

功能：
  1. 递归扫描 skills/ 目录，提取 SKILL.md 元信息（name, description, tags, capabilities）
  2. 自动分类：按能力领域分组
  3. 输出索引 JSON，供 skill_match.py 和 skill_orchestrator.py 使用
  4. 支持增量扫描（缓存 mtime）

用法：
  python3 scripts/scan_skills.py                    # 完整扫描
  python3 scripts/scan_skills.py --refresh          # 强制重建索引
  python3 scripts/scan_skills.py --json             # 输出索引 JSON 到 stdout
  python3 scripts/scan_skills.py --stats            # 仅输出统计
"""

import json, os, re, sys, time, glob, pathlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# yaml is optional: use it when available, fallback to pure regex parsing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SKILLS_DIR = os.path.join(WORKSPACE, "skills")
CORE_SKILLS_DIR = os.path.expanduser("~/core_skills")
INDEX_PATH = os.path.join(WORKSPACE, ".state", ".skill_auto_index.json")
STATE_PATH = os.path.join(WORKSPACE, ".scan_skills_state.json")

# 已知技能分类（硬编码兜底分类，扫描不到时使用）
BACKUP_CATEGORIES = {
    "写作": {"keywords": ["写作", "文章", "文案", "内容创作", "copywriter", "humanizer", "writing"]},
    "工具": {"keywords": ["工具", "系统", "系统工具", "system", "office", "自动化", "automation", "git"]},
    "搜索": {"keywords": ["搜索", "search", "web", "fetch", "news", "paper"]},
    "媒体生成": {"keywords": ["图片", "视频", "音乐", "音频", "image", "video", "music", "gen"]},
    "数据分析": {"keywords": ["数据", "分析", "excel", "pdf", "doc", "convert"]},
    "安全": {"keywords": ["安全", "security", "guard", "validator", "opsec"]},
    "AI开发": {"keywords": ["agent", "skill", "plugin", "prd", "product", "design"]},
    "生活服务": {"keywords": ["天气", "日历", "备忘录", "note", "calendar", "todo", "task"]},
}


def load_state() -> Dict:
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"last_scan": "", "skill_count": 0, "cached_mtimes": {}}


def save_state(state: Dict):
    state["last_scan"] = datetime.now(BEIJING_TZ).isoformat()
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def try_parse_yaml_frontmatter(content: str) -> Optional[Dict]:
    """尝试从内容中提取 YAML frontmatter（SKILL.md 常用）"""
    content = content.strip()
    if not content.startswith("---"):
        return None
    # 找到第二个 ---
    second = content.find("---", 3)
    if second == -1:
        return None
    yaml_block = content[3:second].strip()
    if HAS_YAML:
        try:
            data = yaml.safe_load(yaml_block)
            return data if isinstance(data, dict) else None
        except:
            pass
    
    # fallback: 用正则提取 key: value
    result = {}
    for line in yaml_block.split("\n"):
        match = re.match(r'^(\w[\w.-]*)\s*:\s*(.+)$', line.strip())
        if match:
            key, val = match.group(1), match.group(2).strip()
            val = val.strip('"').strip("'")
            result[key] = val
    return result if result else None


def extract_skill_info(dirpath: str) -> Dict:
    """从技能目录提取信息"""
    info = {
        "name": os.path.basename(dirpath),
        "path": dirpath,
        "description": "",
        "tags": [],
        "capabilities": [],
        "has_skill_md": False,
        "mtime": 0,
        "file_count": 0,
    }
    
    skill_md_path = os.path.join(dirpath, "SKILL.md")
    if os.path.exists(skill_md_path):
        info["has_skill_md"] = True
        info["mtime"] = max(info["mtime"], os.path.getmtime(skill_md_path))
        try:
            with open(skill_md_path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            
            # 尝试解析 frontmatter
            fm = try_parse_yaml_frontmatter(content)
            if fm:
                info["name"] = fm.get("name", info["name"])
                info["description"] = fm.get("description", "")
                raw_tags = fm.get("tags", [])
                if isinstance(raw_tags, str):
                    raw_tags = [t.strip() for t in raw_tags.split(",")]
                info["tags"] = [t.lower() for t in raw_tags if t]
                
                # 从 metadata 中提取更多信息
                meta = fm.get("metadata", {})
                if isinstance(meta, dict) and "openclaw" in meta:
                    oc_meta = meta["openclaw"]
                    info["tags"].extend([t.lower() for t in oc_meta.get("tags", [])])
            
            # 从 content 提取 description heading 后面的内容
            if not info["description"]:
                desc_match = re.search(r'(?:^|\n)#+\s*(?:描述|功能|能力|Description|About)\s*\n+(.+?)(?:\n##|\Z)', content, re.DOTALL)
                if desc_match:
                    info["description"] = desc_match.group(1).strip()[:200]
            
            # 从 name/README 行提取
            if not info["description"]:
                name_match = re.search(r'description\s*[=:]\s*["\']?(.+?)["\']?$', content, re.MULTILINE)
                if name_match:
                    info["description"] = name_match.group(1).strip()[:200]
        except Exception as e:
            info["description"] = f"[parse error: {str(e)[:50]}]"
    
    # 计算目录文件数
    try:
        files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
        info["file_count"] = len(files)
    except: pass
    
    # 去重 tags
    info["tags"] = list(set(info["tags"]))
    
    return info


def classify_skill(info: Dict) -> Tuple[str, float]:
    """对单个技能分类，返回 (分类名, 置信度)"""
    name_lower = info["name"].lower()
    desc_lower = info["description"].lower()
    tags_lower = " ".join(info["tags"])
    combined = f"{name_lower} {desc_lower} {tags_lower}"

    best_cat = "其他"
    best_score = 0

    for cat_name, cat_info in BACKUP_CATEGORIES.items():
        score = 0
        for kw in cat_info["keywords"]:
            kw_lower = kw.lower()
            # name 匹配权重最高
            if kw_lower in name_lower:
                score += 3
            # tags 匹配
            if kw_lower in tags_lower:
                score += 2
            # description 匹配
            if kw_lower in desc_lower:
                score += 1
        if score > best_score:
            best_score = score
            best_cat = cat_name

    return best_cat, min(best_score / 3.0, 1.0)


def scan_skills(force_refresh: bool = False) -> Dict:
    """扫描所有 skill 目录"""
    state = load_state() if not force_refresh else {"last_scan": "", "skill_count": 0, "cached_mtimes": {}}
    cached_mtimes = state.get("cached_mtimes", {})

    skills = []
    categories = {}

    # 扫描 skills/ 目录
    scan_dirs = []
    if os.path.isdir(SKILLS_DIR):
        for d in sorted(os.listdir(SKILLS_DIR)):
            dp = os.path.join(SKILLS_DIR, d)
            if os.path.isdir(dp):
                scan_dirs.append(dp)
    if os.path.isdir(CORE_SKILLS_DIR):
        for d in sorted(os.listdir(CORE_SKILLS_DIR)):
            dp = os.path.join(CORE_SKILLS_DIR, d)
            if os.path.isdir(dp):
                scan_dirs.append(dp)

    changed_count = 0
    for dp in scan_dirs:
        info = extract_skill_info(dp)
        
        # 增量检测：mtime 没变就跳过
        cache_key = info["path"]
        cached_mtime = cached_mtimes.get(cache_key, 0)
        if not force_refresh and cached_mtime == info["mtime"]:
            continue

        # 分类
        cat_name, confidence = classify_skill(info)
        info["category"] = cat_name
        info["classification_confidence"] = round(confidence, 2)

        skills.append(info)
        changed_count += 1
        
        # 更新分类索引
        if cat_name not in categories:
            categories[cat_name] = {"name": cat_name, "keywords": [], "skills": []}
        categories[cat_name]["skills"].append(info["name"])
        
        # 更新 mtime 缓存
        cached_mtimes[cache_key] = info["mtime"]

    # 如果有未变化的技能，从之前的状态恢复
    if os.path.exists(INDEX_PATH) and not force_refresh:
        try:
            with open(INDEX_PATH, encoding="utf-8") as f:
                old_index = json.load(f)
            old_cats = old_index.get("categories", {})
            if isinstance(old_cats, list):
                old_cats = {c.get("name", ""): c for c in old_cats}
            for cat_name, cat_data in old_cats.items():
                if cat_name not in categories:
                    categories[cat_name] = cat_data
                else:
                    # 合并已知 skill 名
                    existing_names = set(s["name"] for s in skills)
                    for old_skill in cat_data.get("skills", []):
                        if old_skill not in existing_names:
                            categories[cat_name]["skills"].append(old_skill)
        except: pass

    # 写入索引
    result = {
        "version": "1.0",
        "scanned_at": datetime.now(BEIJING_TZ).isoformat(),
        "total_skills": len(skills),
        "categories": [v for v in categories.values()],
        "skills": skills,
    }

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # 更新状态
    state["cached_mtimes"] = cached_mtimes
    state["skill_count"] = len(skills)
    save_state(state)

    result["changed"] = changed_count
    return result


def scan_dir() -> Dict:
    """外部统一调用接口"""
    return scan_skills(force_refresh=False)


def run_stats(result: Dict) -> None:
    """输出统计信息"""
    print(f"📦 技能扫描报告")
    print(f"  技能总数: {result['total_skills']}")
    print(f"  分类数: {len(result['categories'])}")
    print(f"  本次变更: {result.get('changed', 0)} 个")
    print()
    for cat in result["categories"]:
        count = len(cat.get("skills", []))
        print(f"  {cat['name']}: {count} 个技能")
    print(f"\n  索引位置: {INDEX_PATH}")


if __name__ == "__main__":
    force = "--refresh" in sys.argv
    result = scan_skills(force_refresh=force)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif "--stats" in sys.argv or "-s" in sys.argv:
        run_stats(result)
    else:
        run_stats(result)
        print(f"\n✅ 扫描完成. 索引已保存到 .state/.skill_auto_index.json")
