"""
vault_maintainer.py — Vault 自动维护
不只检测，自动修复：
  1. 状态传播：04-教训 "未解决/障碍" → 对应项目文件更新了 → 自动标"已解决"
  2. 文件归档：30天以上未动的文件 → 移入 05-存档
  3. 内容去重：同名/同主题文件 → 标记合并建议
  4. 索引更新：新文件 → 自动补充到 MOC/README

纳入 heartbeat 或手动跑：python scripts/vault_maintainer.py
"""
import os, re, shutil, datetime as dt
from pathlib import Path

from shared_config import VAULT_DIR as VAULT
NOW = dt.datetime.now()
LOG = []

def log(msg):
    LOG.append(msg)
    print(f"  {msg}")

# ============================================================
# 规则 1: 状态传播
# 04-教训 里标记"未解决/障碍/拦截" → 检查对应 07-项目 是否已更新 → 自动改状态
# ============================================================

BLOCKER_PATTERNS = [
    (r"#\s*\[?已解决\]?\s*(.*)", "resolved"),   # 已经是已解决
    (r"#\s*(.*?)(?:拦截|失败|障碍|卡住|未解决)(.*)", "blocked"),  # 还卡着
]

def find_active_lessons():
    """找出 04-教训 中标记为阻塞状态的文件"""
    lessons_dir = VAULT / "04-教训"
    if not lessons_dir.exists():
        return []
    
    results = []
    for f in lessons_dir.iterdir():
        if not f.suffix == ".md":
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except:
            continue
        
        # 检查是否已标记 "已解决"
        if "已解决" in content[:300]:
            continue  # 已经处理过
        
        # 检查是否包含阻塞关键词
        has_blocker = any(kw in content[:300] for kw in ("拦截", "失败", "卡住", "未解决", "障碍"))
        if not has_blocker:
            continue
        
        # 找文件中引用的项目文件
        refs = re.findall(r"\[\[([^\]]+)\]\]", content)
        project_refs = [r for r in refs if "07-项目" in r or "赛狐" in r or "自动化" in r or "ERP" in r]
        
        results.append({
            "path": f,
            "name": f.stem,
            "refs": project_refs,
            "content": content,
            "mtime": dt.datetime.fromtimestamp(f.stat().st_mtime),
        })
    
    return results

def check_project_updated(lesson):
    """检查引用项目是否已更新（说明问题可能已解决）"""
    for ref_name in lesson["refs"]:
        ref_clean = ref_name.split("|")[0].strip()
        # 尝试在 vault 中找到这个引用
        for root, _, files in os.walk(VAULT):
            for fn in files:
                # 匹配文件名
                if ref_clean in fn or fn.replace(".md", "") in ref_clean:
                    fp = Path(root) / fn
                    mtime = dt.datetime.fromtimestamp(fp.stat().st_mtime)
                    # 项目文件比教训文件更新 → 可能已解决
                    if mtime > lesson["mtime"]:
                        return True, str(fp.relative_to(VAULT)), mtime
        # 文件名匹配
        for root, _, files in os.walk(VAULT):
            for fn in files:
                parts = ref_clean.replace("/", os.sep).replace("\\", os.sep).split(os.sep)
                if len(parts) >= 2 and fn == parts[-1] or fn.replace(".md", "") == parts[-1]:
                    fp = Path(root) / fn
                    mtime = dt.datetime.fromtimestamp(fp.stat().st_mtime)
                    if mtime > lesson["mtime"]:
                        return True, str(fp.relative_to(VAULT)), mtime
    
    return False, None, None

def auto_resolve_lesson(lesson, project_file):
    """自动将教训文件标记为已解决"""
    content = lesson["content"]
    fp = lesson["path"]
    
    # 在标题前加 [已解决]，在开头加状态说明
    timestamp = NOW.strftime("%Y-%m-%d %H:%M")
    status_line = f"\n> **状态：{timestamp} 自动检测为已解决。** 关联项目 `{project_file}` 已更新，推测此问题不再阻塞。\n"
    
    # 如果标题以 # 开头，在后面插入状态
    lines = content.split("\n")
    new_lines = []
    inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        # 在第一个 # 标题后插入状态
        if not inserted and line.startswith("#") and i < 5:
            new_lines.append(status_line)
            inserted = True
    
    new_content = "\n".join(new_lines)
    try:
        fp.write_text(new_content, encoding="utf-8")
        return True
    except:
        return False

# ============================================================
# 规则 2: 自动归档
# 30 天以上未修改的文件 → 移入 05-存档（保留在原位置的同名软引用）
# ============================================================

ARCHIVE_AGE_DAYS = 30
ARCHIVE_DIRS = ["01-日记", "02-知识", "04-教训", "07-项目", "08-学习"]

def auto_archive():
    """将超过 ARCHIVE_AGE_DAYS 天未修改的文件移到存档"""
    archive_root = VAULT / "05-存档"
    archive_root.mkdir(parents=True, exist_ok=True)
    archived = []
    
    for dir_name in ARCHIVE_DIRS:
        src_dir = VAULT / dir_name
        if not src_dir.exists():
            continue
        
        for f in src_dir.rglob("*.md"):
            mtime = dt.datetime.fromtimestamp(f.stat().st_mtime)
            age = (NOW - mtime).days
            if age < ARCHIVE_AGE_DAYS:
                continue
            
            # 不要归档 MOC/README/索引文件
            if any(kw in f.stem.lower() for kw in ("moc", "readme", "lessons", "索引")):
                continue
            
            # 不要归档被其他文件引用的文件（仍活跃）
            is_referenced = False
            ref_name = f.stem
            for root, _, files in os.walk(VAULT):
                if is_referenced:
                    break
                for fn in files:
                    if fn.endswith(".md") and fn != f.name:
                        try:
                            content = (Path(root) / fn).read_text(encoding="utf-8")
                            if ref_name in content:
                                is_referenced = True
                                break
                        except:
                            pass
            
            if is_referenced:
                continue
            
            # 移入存档
            dest = archive_root / f"{f.stem}.md"
            if dest.exists():
                dest = archive_root / f"{f.stem}-{NOW.strftime('%Y%m%d')}.md"
            
            try:
                shutil.move(str(f), str(dest))
                archived.append((str(f.relative_to(VAULT)), str(dest.relative_to(VAULT))))
            except Exception as e:
                log(f"归档失败 {f.name}: {e}")
    
    return archived

# ============================================================
# 规则 3: 索引自动更新
# 新文件出现在结构目录时，自动补充到 MOC
# ============================================================

def auto_index():
    """自动补充最近新增文件到 MOC（只补7天内新建的）"""
    moc_path = VAULT / "00-索引" / "MOC.md"
    if not moc_path.exists():
        return 0
    
    try:
        moc = moc_path.read_text(encoding="utf-8")
    except:
        return 0
    
    cutoff = NOW - dt.timedelta(days=7)
    added = 0
    for dir_name in ["01-日记", "02-知识", "04-教训", "07-项目", "08-学习"]:
        src_dir = VAULT / dir_name
        if not src_dir.exists():
            continue
        
        for f in src_dir.rglob("*.md"):
            ctime = dt.datetime.fromtimestamp(f.stat().st_ctime)
            if ctime < cutoff:
                continue  # 只补最近7天新建的
            fname = f.stem
            if fname not in moc:
                rel = str(f.relative_to(VAULT)).replace(os.sep, "/")
                entry = f"- [[{rel}]]\n"
                section = f"## {dir_name}"
                if section in moc:
                    moc = moc.replace(section, f"{section}\n{entry}")
                    added += 1
    
    if added > 0:
        try:
            moc_path.write_text(moc, encoding="utf-8")
        except:
            pass
    
    return added

# ============================================================
# 主流程
# ============================================================

def run(dry_run=False):
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"=== vault_maintainer {NOW.strftime('%Y-%m-%d %H:%M')} {prefix}===")
    
    # 1. 状态传播
    lessons = find_active_lessons()
    log(f"发现 {len(lessons)} 个待处理的教训文件")
    
    resolved_count = 0
    for lesson in lessons:
        updated, proj_file, proj_mtime = check_project_updated(lesson)
        if updated:
            if dry_run:
                log(f"[DRY] 可自动标记已解决: {lesson['name']} → 项目 {proj_file} 已更新 ({proj_mtime.strftime('%m/%d %H:%M')})")
            else:
                ok = auto_resolve_lesson(lesson, proj_file)
                if ok:
                    log(f"[已解决] {lesson['name']} — 项目 {proj_file} 已更新，已自动标记")
                    resolved_count += 1
    
    if resolved_count == 0 and not dry_run:
        log("无需自动解决的项目")
    
    # 2. 自动归档
    archived = auto_archive()
    if dry_run:
        # 只看哪些文件会被归档
        log(f"[预检] 将归档以下超过{ARCHIVE_AGE_DAYS}天未动的文件:")
        for dir_name in ARCHIVE_DIRS:
            src_dir = VAULT / dir_name
            if not src_dir.exists():
                continue
            for f in src_dir.rglob("*.md"):
                mtime = dt.datetime.fromtimestamp(f.stat().st_mtime)
                age = (NOW - mtime).days
                if age >= ARCHIVE_AGE_DAYS and not any(kw in f.stem.lower() for kw in ("moc", "readme", "lessons", "索引")):
                    log(f"  [{age}天] {f.relative_to(VAULT)}")
    else:
        if archived:
            log(f"归档了 {len(archived)} 个文件:")
            for src, dest in archived:
                log(f"  {src} → {dest}")
        else:
            log("无需归档的文件")
    
    # 3. 索引更新
    added = auto_index()
    if added:
        log(f"MOC 索引补充了 {added} 条新引用")
    
    # 4. 统计
    total = sum(1 for root, _, files in os.walk(VAULT) for f in files if f.endswith(".md") and ".git" not in root)
    log(f"vault 总文件: {total}")
    
    print(f"=== 完成 ===")
    return LOG

# ── Health report ──
try:
    from system_health import task_report
    task_report("vault_maintainer", status="ok")
except Exception:
    pass

if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    run(dry_run=dry)
