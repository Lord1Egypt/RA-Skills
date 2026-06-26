"""
WorkBuddy 自动化任务去重守护脚本（通用版）
=============================================
功能：扫描 WorkBuddy 自动化数据库，检测并清理重复的自动化任务
策略：按名称分组，同一名称只保留最新创建的，其余自动删除

适用平台：Windows / macOS / Linux
依赖：Python 3.6+（仅使用标准库，无需安装额外包）

使用方式：
  1. 检查模式（只看不动）：  python automation_dedup_guard.py --dry-run
  2. 执行模式（自动清理）：  python automation_dedup_guard.py
  3. 指定数据库路径：        python automation_dedup_guard.py --db /custom/path/automations.db
"""

import sqlite3
import sys
import os
from datetime import datetime
from collections import defaultdict

# ============================================================================
# 数据库路径自动检测
# ============================================================================

def find_db_path():
    """
    自动查找 WorkBuddy 自动化数据库文件。
    搜索顺序：
      1. 命令行 --db 参数指定的路径
      2. 环境变量 WORKBUDDY_DB_PATH
      3. 默认路径：
         - Windows: %APPDATA%/WorkBuddy/automations/automations.db
         - macOS:   ~/Library/Application Support/WorkBuddy/automations/automations.db
         - Linux:   ~/.config/WorkBuddy/automations/automations.db
    """
    # 1. 命令行参数
    if '--db' in sys.argv:
        idx = sys.argv.index('--db')
        if idx + 1 < len(sys.argv):
            path = sys.argv[idx + 1]
            if os.path.isfile(path):
                return os.path.abspath(path)
            print(f"[ERROR] 指定的数据库文件不存在: {path}")
            sys.exit(1)

    # 2. 环境变量
    env_path = os.environ.get('WORKBUDDY_DB_PATH')
    if env_path and os.path.isfile(env_path):
        return os.path.abspath(env_path)

    # 3. 默认路径（按操作系统）
    home = os.path.expanduser('~')

    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA', os.path.join(home, 'AppData', 'Roaming'))
        default = os.path.join(appdata, 'WorkBuddy', 'automations', 'automations.db')
    elif sys.platform == 'darwin':
        default = os.path.join(home, 'Library', 'Application Support',
                               'WorkBuddy', 'automations', 'automations.db')
    else:
        default = os.path.join(home, '.config', 'WorkBuddy', 'automations', 'automations.db')

    if os.path.isfile(default):
        return default

    print(f"[ERROR] 未找到 WorkBuddy 自动化数据库")
    print(f"  尝试的路径: {default}")
    print(f"  请使用 --db 参数手动指定路径")
    print(f"  示例: python {sys.argv[0]} --db /your/path/automations.db")
    sys.exit(1)


def parse_args():
    """解析命令行参数"""
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    return dry_run, verbose


# ============================================================================
# 核心逻辑
# ============================================================================

def get_all_automations(conn):
    """获取所有自动化任务"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, status, created_at
        FROM automations
        ORDER BY created_at ASC
    """)
    return cursor.fetchall()


def detect_duplicates(automations):
    """
    按名称分组，检测重复任务。
    返回: {name: {keep: {...}, duplicates: [...], count: N}, ...}
    """
    groups = defaultdict(list)
    for row in automations:
        aid, name, status, created_at = row
        groups[name].append({
            'id': aid,
            'status': status,
            'created_at': created_at
        })

    duplicates = {}
    for name, items in groups.items():
        if len(items) > 1:
            # 按创建时间倒序，最新的保留
            items_sorted = sorted(items, key=lambda x: x['created_at'], reverse=True)
            keep = items_sorted[0]
            dups = items_sorted[1:]
            duplicates[name] = {
                'keep': keep,
                'duplicates': dups,
                'count': len(items)
            }

    return duplicates


def cleanup_duplicates(conn, duplicates, dry_run=True):
    """删除重复任务（同时清理关联的运行记录）"""
    cursor = conn.cursor()
    results = []
    total_runs_removed = 0

    for name, info in duplicates.items():
        for dup in info['duplicates']:
            did = dup['id']
            if dry_run:
                results.append({
                    'id': did,
                    'name': name,
                    'runs': '?',
                    'dry_run': True
                })
            else:
                # 先删除关联的运行记录
                cursor.execute("DELETE FROM automation_runs WHERE automation_id = ?", (did,))
                runs_removed = cursor.rowcount
                total_runs_removed += runs_removed
                # 再删除任务本身
                cursor.execute("DELETE FROM automations WHERE id = ?", (did,))
                if cursor.rowcount > 0:
                    results.append({
                        'id': did,
                        'name': name,
                        'runs': runs_removed,
                        'dry_run': False
                    })

    if not dry_run:
        conn.commit()

    return results, total_runs_removed


# ============================================================================
# 报告输出
# ============================================================================

def print_report(automations, duplicates, cleanup_results, total_runs_removed, dry_run):
    """输出结构化报告"""
    total = len(automations)
    deleted_count = len(cleanup_results)
    remaining = total - deleted_count
    mode_tag = "[检查模式]" if dry_run else "[执行模式]"

    print()
    print("=" * 60)
    print(f"  WorkBuddy 自动化任务去重检查 {mode_tag}")
    print("=" * 60)
    print(f"  时间:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  当前任务总数: {total}")
    print("-" * 60)

    if not duplicates:
        print()
        print("  [OK] 未发现重复任务，一切正常。")
        print("=" * 60)
        return

    print(f"  [!] 发现 {len(duplicates)} 组重复任务:")
    print()

    for name, info in duplicates.items():
        print(f"  {'─' * 50}")
        print(f"  {name} (共 {info['count']} 个)")
        print(f"    [保留] {info['keep']['id']}")
        for dup in info['duplicates']:
            print(f"    [重复] {dup['id']}  <- 将删除")
        print()

    print(f"  {'─' * 50}")
    print(f"  操作结果:")

    if dry_run:
        print(f"    (检查模式，以下为模拟操作，未实际删除)")
    for r in cleanup_results:
        tag = "将删除" if r['dry_run'] else "已删除"
        print(f"    {tag}: {r['id']} ('{r['name']}')  - {r['runs']} 条运行记录")

    print()
    print(f"  统计: 删除 {deleted_count} 个重复任务" +
          (f"，清除 {total_runs_removed} 条运行记录" if not dry_run else ""))
    print(f"  剩余: {remaining} 个任务")
    print("=" * 60)


# ============================================================================
# 主函数
# ============================================================================

def main():
    db_path = find_db_path()
    dry_run, verbose = parse_args()

    if verbose:
        print(f"[DEBUG] 数据库路径: {db_path}")
        print(f"[DEBUG] 模式: {'dry-run' if dry_run else 'execute'}")

    conn = sqlite3.connect(db_path)

    # 1. 获取所有任务
    automations = get_all_automations(conn)

    # 2. 检测重复
    duplicates = detect_duplicates(automations)

    # 3. 执行清理
    cleanup_results, total_runs_removed = cleanup_duplicates(
        conn, duplicates, dry_run=dry_run
    )

    # 4. 输出报告
    print_report(automations, duplicates, cleanup_results, total_runs_removed, dry_run)

    # 退出码：有重复返回 1（方便自动化任务检测），无重复返回 0
    conn.close()
    sys.exit(1 if duplicates else 0)


if __name__ == '__main__':
    main()
