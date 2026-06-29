"""
auto_link_vault.py — 自动为 vault 中没有双链的文件添加链接

规则引擎，0 token 消耗。
用法: python scripts/auto_link_vault.py [--dry-run]
"""
import re
from pathlib import Path

from shared_config import VAULT_DIR as VAULT

# 链接规则：根据文件路径模式决定添加什么链接
LINK_RULES = {
    # 日记文件
    r'01-日记/2026-\d{2}-\d{2}\.md': [
        '[[02-知识/系统配置]]',
        '[[04-教训/lessons]]',
    ],
    # 日记：任意文件
    r'01-日记/.+\.md': [
        '[[04-教训/lessons]]',
    ],
    # 知识文件
    r'02-知识/系统.*\.md': [
        '[[02-知识/系统总览]]',
        '[[02-知识/LM-Studio]]',
    ],
    r'02-知识/LM-Studio\.md': [
        '[[02-知识/系统配置]]',
        '[[02-知识/Worker能力]]',
    ],
    r'02-知识/Worker.*\.md': [
        '[[02-知识/LM-Studio]]',
        '[[02-知识/系统配置]]',
    ],
    # 教训文件
    r'04-教训/.*\.md': [
        '[[04-教训/lessons]]',
        '[[01-日记/2026-05-12]]',
    ],
    # 赛狐ERP 项目文件
    r'07-项目/赛狐ERP/模块/.*\.md': [
        '[[07-项目/赛狐ERP/README]]',
    ],
    r'07-项目/赛狐ERP/[^/]+\.md': [
        '[[07-项目/赛狐ERP/README]]',
    ],
    # 本地模型评估项目
    r'07-项目/01-本地模型评估/.*\.md': [
        '[[07-项目/01-本地模型评估/00-总览]]',
    ],
}

# 跳过的目录/文件
SKIP_PATTERNS = [
    r'\.obsidian',
    r'backup-\d{14}',
    r'05-存档',
    r'06-收件箱',
    r'00-索引',
]


def should_skip(filepath: Path) -> bool:
    rel = str(filepath.relative_to(VAULT))
    return any(re.search(p, rel) for p in SKIP_PATTERNS)


def has_links(content: str) -> bool:
    return bool(re.search(r'\[\[[^\]]+\]\]', content))


def get_link_line(filepath: Path) -> str | None:
    """根据文件路径 + 内容匹配规则，返回链接行。"""
    rel = str(filepath.relative_to(VAULT)).replace('\\', '/')

    # 路径规则（精确）
    for pattern, links in LINK_RULES.items():
        if re.match(pattern, rel):
            return '相关：' + ' | '.join(links)

    # 内容规则（关键词匹配）
    try:
        content = filepath.read_text(encoding='utf-8-sig')
    except Exception:
        return None

    content_lower = content.lower()
    content_links = []

    # 内容→链接映射
    CONTENT_RULES = {
        'gateway': '[[02-知识/系统配置]]',
        'api key': '[[02-知识/系统配置]]',
        '模型切换': '[[02-知识/系统总览]]',
        'deepseek': '[[02-知识/系统总览]]',
        'lm studio': '[[02-知识/LM-Studio]]',
        'qdrant': '[[02-知识/系统总览]]',
        '教训': '[[04-教训/lessons]]',
        '纠正': '[[04-教训/lessons]]',
        '偏好': '[[04-教训/lessons]]',
        '修复': '[[04-教训/lessons]]',
        'bug': '[[04-教训/lessons]]',
        '跨境': '[[02-知识/跨境洞察]]',
        'temu': '[[07-项目/赛狐ERP自动化]]',
        '赛狐': '[[07-项目/赛狐ERP自动化]]',
        'sellfox': '[[07-项目/赛狐ERP自动化]]',
        'agent': '[[02-知识/系统总览]]',
        'worker': '[[02-知识/Worker能力]]',
        'analyzer': '[[02-知识/系统总览]]',
        'cron': '[[02-知识/计划任务]]',
        'heartbeat': '[[02-知识/系统健康状态]]',
        '抗体': '[[02-知识/系统健康状态]]',
        'embed': '[[02-知识/LM-Studio]]',
        'prompt': '[[02-知识/系统总览]]',
        '记忆': '[[02-知识/记忆系统架构]]',
        'memory': '[[02-知识/记忆系统架构]]',
        '蒸馏': '[[02-知识/自我进化系统]]',
        '进化': '[[02-知识/自我进化系统]]',
        '脚本': '[[02-知识/脚本清单]]',
        '部署': '[[02-知识/部署总结]]',
        '日报': '[[03-日报/2026-05-20-跨境电商日报]]',
    }

    seen_targets = set()
    for keyword, link in CONTENT_RULES.items():
        if keyword in content_lower and link not in seen_targets:
            content_links.append(link)
            seen_targets.add(link)

    if content_links:
        return '相关：' + ' | '.join(content_links[:6])
    return None


def add_link_to_file(filepath: Path, link_line: str, dry_run: bool = False) -> bool:
    """在文件第一个标题后添加链接行。"""
    try:
        content = filepath.read_text(encoding='utf-8-sig')
        if has_links(content):
            return False

        lines = content.split('\n')
        new_lines = []
        link_added = False

        for line in lines:
            new_lines.append(line)
            if not link_added and line.startswith('# '):
                new_lines.append('')
                new_lines.append(link_line)
                new_lines.append('')
                link_added = True

        if link_added:
            if not dry_run:
                filepath.write_text('\n'.join(new_lines), encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f'  [ERROR] {e}')
        return False


# ── 断裂链接修复 ──

def scan_broken_links():
    """扫描所有文件中的断裂 wiki 链接"""
    broken = []
    all_files = {}
    # 建立文件名索引
    for f in VAULT.rglob("*.md"):
        all_files[f.name] = f
        all_files[f.stem] = f  # 同时索引不带扩展名的

    for f in VAULT.rglob("*.md"):
        if should_skip(f):
            continue
        try:
            content = f.read_text(encoding="utf-8-sig")
        except:
            continue
        refs = re.findall(r'\[\[([^\]]+)\]\]', content)
        for ref in refs:
            target = ref.split("|")[0].strip()
            if not target.endswith(".md"):
                target += ".md"
            # 尝试多种匹配方式
            filename = target.split("/")[-1] if "/" in target else target
            filename = filename.split("\\")[-1] if "\\" in filename else filename
            if filename not in all_files:
                broken.append({
                    "source": str(f.relative_to(VAULT)),
                    "link": ref,
                })
    return broken


def fix_broken_links(dry_run=True):
    """修复断裂链接：注释掉不存在的目标"""
    broken = scan_broken_links()
    if not broken:
        print("  无断裂链接")
        return 0

    # 按源文件分组
    by_source = {}
    for b in broken:
        by_source.setdefault(b["source"], []).append(b["link"])

    fixed = 0
    for source, links in by_source.items():
        fp = VAULT / source
        try:
            content = fp.read_text(encoding="utf-8-sig")
        except:
            continue
        new_content = content
        for link in links:
            # 注释掉断裂链接: [[broken]] → <!-- [[broken]] -->
            old = f"[[{link}]]"
            new = f"<!-- [[{link}]] (断裂，目标不存在) -->"
            new_content = new_content.replace(old, new)

        if new_content != content:
            if not dry_run:
                fp.write_text(new_content, encoding="utf-8")
            print(f"  [FIX] {source}: {len(links)} 个断裂链接已注释")
            fixed += len(links)

    return fixed


def main():
    import sys
    dry_run = '--dry-run' in sys.argv
    repair = '--repair' in sys.argv

    if repair:
        print(f'=== 断裂链接修复 {"DRY-RUN" if dry_run else "EXECUTE"} ===')
        fix_broken_links(dry_run=dry_run)
        return

    if dry_run:
        print('[DRY RUN] 不会实际修改文件\n')

    md_files = [f for f in VAULT.rglob('*.md') if not should_skip(f)]
    added = 0
    skipped = 0

    for f in sorted(md_files):
        rel = str(f.relative_to(VAULT))
        link_line = get_link_line(f)
        if not link_line:
            continue

        if add_link_to_file(f, link_line, dry_run):
            print(f'[ADD] {rel}')
            added += 1
        else:
            skipped += 1

    print(f'\n完成: {added} 添加, {skipped} 跳过')

# ── Health report ──
try:
    from system_health import task_report
    task_report("auto_link_vault", status="ok")
except Exception:
    pass


if __name__ == '__main__':
    main()
