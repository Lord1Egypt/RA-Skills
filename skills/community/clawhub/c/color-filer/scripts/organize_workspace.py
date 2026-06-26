# -*- coding: utf-8 -*-
"""
Color-Filer 工作区整理脚本（增强版）

⚠️ 安全特性：
1. 默认 dry_run=True（仅预览，不修改文件）
2. 目标路径安全验证（拒绝系统目录）
3. 完整的操作预览（重命名、移动、创建）
4. 可选备份功能
5. 用户确认机制

🚀 新增功能：
1. 目录重命名 - 批量重命名目录
2. 文件归档 - 按规则移动文件到目标目录
3. 创建目录 - 批量创建缺失目录
4. 文件重命名 - 添加表情符号前缀
"""

import os
import sys
import shutil
import re
from datetime import datetime

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ==================== 安全配置 ====================

# 禁止处理的危险路径（Windows 和 Linux/Mac）
DANGEROUS_PATHS = [
    # Windows 系统目录
    r'C:\Windows',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\ProgramData',
    r'C:\Users\All Users',
    r'C:\Users\Default',
    r'C:\Users\Public',
    # Linux/Mac 系统目录
    '/root',
    '/bin',
    '/sbin',
    '/usr/bin',
    '/usr/sbin',
    '/usr/local/bin',
    '/System',
    '/etc',
    '/var',
]

# ==================== 表情符号配置 ====================

# 文件类型对应的表情符号
EXT_ICONS = {
    # 文档
    '.md': '📝',
    '.docx': '📝',
    '.txt': '📝',
    '.pdf': '📄',
    '.mmap': '🧠',
    '.pptx': '📽️',
    '.doc': '📄',
    '.ppt': '📽️',
    
    # 数据
    '.xlsx': '📊',
    '.csv': '📊',
    '.json': '📋',
    '.xml': '📋',
    '.ini': '⚙️',
    '.yaml': '⚙️',
    '.yml': '⚙️',
    '.toml': '⚙️',
    
    # 脚本
    '.sh': '🖥️',
    '.bat': '🖥️',
    '.cmd': '🖥️',
    '.py': '🖥️',
    '.js': '🖥️',
    '.ps1': '🖥️',
    
    # 配置
    '.conf': '⚙️',
    '.config': '⚙️',
    
    # 压缩包
    '.gz': '📦',
    '.zip': '📦',
    '.tar': '📦',
    '.rpm': '📦',
    '.7z': '📦',
    '.rar': '📦',
    
    # 图片
    '.png': '🖼️',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.gif': '🖼️',
    
    # 证书
    '.pem': '🔐',
    '.key': '🔐',
    '.crt': '🔐',
    '.cer': '🔐',
    
    # 其他
    '.client': '📄',
    '.server': '📄',
    '.92': '📄',
    '.repo': '📄',
    '.psk': '📄',
}

# ==================== 安全函数 ====================

def validate_target_path(target_path):
    """
    验证目标路径是否安全

    Returns:
        tuple: (is_safe, reason)
    """
    # 规范化路径
    target_path = os.path.abspath(target_path)

    # 检查是否在危险路径列表中
    for dangerous_path in DANGEROUS_PATHS:
        dangerous_path = os.path.abspath(dangerous_path)
        if target_path == dangerous_path or target_path.startswith(dangerous_path + os.sep):
            return False, f"禁止处理系统目录: {dangerous_path}"

    # 检查路径是否存在
    if not os.path.exists(target_path):
        return False, f"路径不存在: {target_path}"

    # 检查是否为目录
    if not os.path.isdir(target_path):
        return False, f"不是目录: {target_path}"

    return True, "路径安全"


def check_dry_run_warning(dry_run):
    """如果非 dry_run 模式，显示警告"""
    if not dry_run:
        print('\n' + '=' * 60)
        print('⚠️  警告：非预演模式（dry_run=False）')
        print('⚠️  将实际修改文件，建议先使用 --dry-run 测试')
        print('=' * 60 + '\n')
        return True
    return False


def create_backup(target_path):
    """创建目录备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'{os.path.basename(target_path)}_backup_{timestamp}'
    backup_path = os.path.join(os.path.dirname(target_path), backup_name)

    if os.path.exists(backup_path):
        print(f'⚠️  备份已存在: {backup_path}')
        return backup_path

    print(f'💾 创建备份: {backup_path}')
    try:
        shutil.copytree(target_path, backup_path)
        print(f'✅ 备份成功')
        return backup_path
    except Exception as e:
        print(f'❌ 备份失败: {e}')
        return None


def confirm_operation(dry_run, auto_confirm=False):
    """用户确认操作"""
    if dry_run:
        return True
    
    if auto_confirm:
        return True
    
    response = input('\n⚠️  确认执行以上操作？(y/n): ')
    return response.lower() == 'y'


# ==================== 核心功能函数 ====================

def has_emoji_prefix(filename):
    """检查文件是否已有表情符号前缀"""
    emoji_ranges = [
        (0x1F600, 0x1F64F),
        (0x1F300, 0x1F5FF),
        (0x1F680, 0x1F6FF),
        (0x1F900, 0x1F9FF),
        (0x2600, 0x26FF),
        (0x2700, 0x27BF),
    ]
    
    if not filename:
        return False
    
    first_char = filename[0]
    code_point = ord(first_char)
    
    for start, end in emoji_ranges:
        if start <= code_point <= end:
            return True
    
    return False


def get_file_icon(filename):
    """根据扩展名获取表情符号"""
    _, ext = os.path.splitext(filename)
    return EXT_ICONS.get(ext.lower(), '📄')


def rename_directories(target_path, dir_mappings, dry_run=True):
    """重命名目录"""
    mode_str = "[预演模式]" if dry_run else "[执行模式]"
    print(f'\n📁 {mode_str}重命名目录\n')
    print('=' * 60)

    success_count = 0
    failed_count = 0

    for old_name, new_name in dir_mappings.items():
        old_path = os.path.join(target_path, old_name)
        new_path = os.path.join(target_path, new_name)
        
        if not os.path.exists(old_path):
            print(f'⚠️  跳过（不存在）: {old_name}')
            failed_count += 1
            continue
        
        if os.path.exists(new_path):
            print(f'⚠️  跳过（目标已存在）: {old_name} → {new_name}')
            failed_count += 1
            continue
        
        if dry_run:
            print(f'[DRY] {old_name:30s} → {new_name}')
            success_count += 1
        else:
            try:
                os.rename(old_path, new_path)
                print(f'✅ {old_name:30s} → {new_name}')
                success_count += 1
            except Exception as e:
                print(f'❌ 失败: {old_name} → {new_name} | 错误: {e}')
                failed_count += 1

    print(f'\n📊 目录重命名统计:')
    print(f'  ✅ 成功: {success_count}')
    print(f'  ❌ 失败: {failed_count}')

    return success_count, failed_count


def create_directories(target_path, dir_names, dry_run=True):
    """创建目录"""
    mode_str = "[预演模式]" if dry_run else "[执行模式]"
    print(f'\n📁 {mode_str}创建目录\n')
    print('=' * 60)

    success_count = 0
    failed_count = 0

    for dir_name in dir_names:
        dir_path = os.path.join(target_path, dir_name)
        
        if os.path.exists(dir_path):
            print(f'⚠️  跳过（已存在）: {dir_name}')
            failed_count += 1
            continue
        
        if dry_run:
            print(f'[DRY] 创建: {dir_name}')
            success_count += 1
        else:
            try:
                os.makedirs(dir_path)
                print(f'✅ 创建: {dir_name}')
                success_count += 1
            except Exception as e:
                print(f'❌ 失败: {dir_name} | 错误: {e}')
                failed_count += 1

    print(f'\n📊 创建目录统计:')
    print(f'  ✅ 成功: {success_count}')
    print(f'  ❌ 失败: {failed_count}')

    return success_count, failed_count


def move_files(target_path, file_mappings, dry_run=True):
    """移动文件到目标目录"""
    mode_str = "[预演模式]" if dry_run else "[执行模式]"
    print(f'\n📄 {mode_str}移动文件\n')
    print('=' * 60)

    success_count = 0
    failed_count = 0

    for filename, target_dir in file_mappings.items():
        src_path = os.path.join(target_path, filename)
        dst_path = os.path.join(target_path, target_dir, filename)
        
        if not os.path.exists(src_path):
            print(f'⚠️  跳过（不存在）: {filename}')
            failed_count += 1
            continue
        
        if os.path.exists(dst_path):
            print(f'⚠️  跳过（目标已存在）: {filename} → {target_dir}')
            failed_count += 1
            continue
        
        if dry_run:
            print(f'[DRY] {filename:40s} → {target_dir}')
            success_count += 1
        else:
            try:
                shutil.move(src_path, dst_path)
                print(f'✅ {filename:40s} → {target_dir}')
                success_count += 1
            except Exception as e:
                print(f'❌ 失败: {filename} → {target_dir} | 错误: {e}')
                failed_count += 1

    print(f'\n📊 文件移动统计:')
    print(f'  ✅ 成功: {success_count}')
    print(f'  ❌ 失败: {failed_count}')

    return success_count, failed_count


def rename_files_recursive(target_path, dry_run=True):
    """递归重命名所有文件"""
    mode_str = "[预演模式]" if dry_run else "[执行模式]"
    print(f'\n📄 {mode_str}重命名文件\n')
    print('=' * 60)

    success_count = 0
    skipped_count = 0
    failed_count = 0

    for root, dirs, files in os.walk(target_path):
        if not files:
            continue
        
        dir_name = os.path.basename(root)
        
        for filename in sorted(files):
            # 跳过已有表情符号前缀的文件
            if has_emoji_prefix(filename):
                skipped_count += 1
                continue
            
            # 获取表情符号
            icon = get_file_icon(filename)
            new_filename = f"{icon}_01_{filename}"
            
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(root, new_filename)
            
            # 检查目标文件是否已存在
            if os.path.exists(dst_path):
                # 查找可用的序号
                for i in range(2, 100):
                    new_filename = f"{icon}_{i:02d}_{filename}"
                    dst_path = os.path.join(root, new_filename)
                    if not os.path.exists(dst_path):
                        break
            
            if dry_run:
                print(f'[DRY] {dir_name:30s} | {filename[:30]:30s} → {new_filename}')
                success_count += 1
            else:
                try:
                    os.rename(src_path, dst_path)
                    print(f'✅ {dir_name:30s} | {filename[:30]:30s} → {new_filename}')
                    success_count += 1
                except Exception as e:
                    print(f'❌ {dir_name:30s} | {filename[:30]:30s} | 错误: {e}')
                    failed_count += 1

    print(f'\n📊 文件重命名统计:')
    print(f'  ✅ 重命名: {success_count}')
    print(f'  ⏭️  跳过: {skipped_count}')
    print(f'  ❌ 失败: {failed_count}')

    return success_count, skipped_count, failed_count


# ==================== 命令行入口 ====================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Color-Filer: 工作区整理脚本（增强版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 预览整理（Dry-Run 模式，推荐）
  python organize_workspace.py "F:\\笔记" --dry-run

  # 执行实际整理（需先测试）
  python organize_workspace.py "F:\\笔记" --rename

  # 不创建备份
  python organize_workspace.py "F:\\笔记" --rename --no-backup

  # 使用 DocMD 配置
  python organize_workspace.py "F:\\AIcoding\\DocMD" --dry-run --config docmd
        """
    )
    parser.add_argument('target', help='目标目录路径')
    parser.add_argument('--dry-run', action='store_true', help='预演模式（默认），不实际修改文件')
    parser.add_argument('--rename', action='store_true', help='执行实际整理（需先测试）')
    parser.add_argument('--no-backup', action='store_true', help='不创建备份')
    parser.add_argument('--config', default=None, help='配置文件名（不含.py后缀），如 docmd')
    parser.add_argument('--yes', '-y', action='store_true', help='自动确认，跳过用户确认提示')

    args = parser.parse_args()

    # 添加 no_backup 属性（如果未指定，默认为 False）
    if not hasattr(args, 'no_backup'):
        args.no_backup = False

    args = parser.parse_args()

    # 默认 dry_run=True
    dry_run = not args.rename

    # 分析目录
    print(f'\n📂 分析目录: {args.target}')
    print('=' * 60)

    # 安全验证
    is_safe, reason = validate_target_path(args.target)
    if not is_safe:
        print(f'❌ 安全检查失败: {reason}')
        print('❌ 操作已取消')
        sys.exit(1)

    print(f'✅ 安全检查通过: {reason}\n')

    # 统计信息
    total_files = 0
    total_dirs = 0

    for root, dirs, files in os.walk(args.target):
        total_files += len(files)
        total_dirs += len(dirs)

    print(f'📊 文件总数: {total_files}')
    print(f'📁 目录总数: {total_dirs}')

    # 检测未使用表情符号的文件
    untagged_count = 0
    for root, dirs, files in os.walk(args.target):
        for f in files:
            if not has_emoji_prefix(f):
                untagged_count += 1

    print(f'⚠️  未使用表情符号的文件: {untagged_count} 个\n')

    # 显示非 dry_run 警告
    check_dry_run_warning(dry_run)

    # 显示操作预览
    print('📋 操作预览:')
    print('  1. 重命名目录（如需要）')
    print('  2. 创建缺失目录（如需要）')
    print('  3. 移动根目录散文件（如需要）')
    print('  4. 递归重命名文件（添加表情符号前缀）')

    # 用户确认
    auto_confirm = getattr(args, 'yes', False)
    if not confirm_operation(dry_run, auto_confirm=auto_confirm):
        print('\n❌ 用户取消操作')
        sys.exit(0)

    # 执行整理
    print('\n🚀 开始整理...\n')

    total_success = 0
    total_failed = 0

    # 创建备份（仅在非 dry_run 模式且未禁用备份时）
    backup_path = None
    if not dry_run and not args.no_backup:
        print('\n💾 创建备份中...\n')
        backup_path = create_backup(args.target)
        if not backup_path:
            print('\n❌ 备份失败，操作已取消')
            sys.exit(1)
        print()
    elif not dry_run and args.no_backup:
        print('\n⚠️  警告：已禁用备份，直接执行整理操作\n')

    # 加载配置文件（如果指定）
    DIR_MAPPINGS = {}
    FILE_MAPPINGS = {}
    DIRS_TO_CREATE = []

    if args.config:
        config_file = os.path.join(os.path.dirname(__file__), f'{args.config}_config.py')
        if os.path.exists(config_file):
            print(f'📋 加载配置: {args.config}_config.py\n')
            exec(open(config_file, encoding='utf-8').read(), globals())
        else:
            print(f'⚠️  配置文件不存在: {config_file}')
            print('⚠️  跳过目录重命名和文件归档步骤\n')

    # 重命名目录（如果有配置）
    if DIR_MAPPINGS:
        success, failed = rename_directories(args.target, DIR_MAPPINGS, dry_run)
        total_success += success
        total_failed += failed

    # 创建目录（如果有配置）
    if DIRS_TO_CREATE:
        success, failed = create_directories(args.target, DIRS_TO_CREATE, dry_run)
        total_success += success
        total_failed += failed

    # 移动文件（如果有配置）
    if FILE_MAPPINGS:
        success, failed = move_files(args.target, FILE_MAPPINGS, dry_run)
        total_success += success
        total_failed += failed

    # 重命名文件
    success, skipped, failed = rename_files_recursive(args.target, dry_run)
    total_success += success
    total_failed += failed

    # 输出总计
    print('\n' + '=' * 60)
    print('📊 整理完成统计:')
    print(f'  ✅ 成功: {total_success}')
    print(f'  ❌ 失败: {total_failed}')

    if dry_run:
        print('\n💡 提示: 当前为预演模式，未实际修改文件')
        print('💡 如需执行实际整理，请设置 dry_run=False 并重新运行')
