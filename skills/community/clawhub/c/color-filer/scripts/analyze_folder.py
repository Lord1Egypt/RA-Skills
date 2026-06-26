# -*- coding: utf-8 -*-
# 文件夹分析脚本 - 扫描并生成整理建议（优化版）

import os
import sys
import re
from datetime import datetime

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 基础表情符号
BASE_EMOJIS = {
    '🔴': '核心/警告',
    '🟠': '工具/配置',
    '🟡': '学习/记录',
    '🟢': '稳定/完成',
    '🔵': '开发/技术',
    '🟣': '高级/实验',
    '⚫': '历史/归档',
    '⚪': '通用/未分类',
}

# 扩展名图标（扩展版）
EXT_ICONS = {
    '.md': '📝',
    '.py': '💻',
    '.sh': '🖥️',
    '.pdf': '📄',
    '.xlsx': '📊',
    '.xls': '📊',
    '.csv': '📊',
    '.zip': '📦',
    '.tar': '📦',
    '.gz': '📦',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.svg': '🖼️',
    '.txt': '📜',
    '.json': '📋',
    '.xml': '📋',
    '.conf': '⚙️',
    '.ini': '⚙️',
    '.yaml': '⚙️',
    '.yml': '⚙️',
    '.toml': '⚙️',
    '.mmap': '🧠',
    '.pptx': '📽️',
    '.docx': '📝',
    '.mp4': '🎬',
    '.mp3': '🎵',
    '.wav': '🎵',
}


def extract_serial_number(name):
    """提取文件名中的序号"""
    # 匹配格式: XX-表情_XX_标题 或 XX-表情_标题
    match = re.match(r'^(\d+)[-–]', name)
    if match:
        return int(match.group(1))
    return None


def analyze_directory(target_path):
    """深度分析目录结构（优化版）"""
    print(f'\n📂 正在分析: {target_path}\n')
    print('=' * 70)

    if not os.path.exists(target_path):
        print(f'❌ 目录不存在: {target_path}')
        return

    # 收集信息
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'max_depth': 0,
        'extensions': {},
        'no_emoji_files': [],
        'duplicate_names': [],
        'very_long_names': [],
        'duplicate_serials': [],  # 新增：序号重复
        'root_dirs': [],  # 新增：根目录列表
        'empty_dirs': [],  # 新增：空目录
    }

    name_counts = {}
    dir_serials = {}  # 存储目录序号

    # 递归扫描
    def scan_dir(current_path, depth):
        nonlocal stats
        stats['max_depth'] = max(stats['max_depth'], depth)

        try:
            items = os.listdir(current_path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            # 统计名称重复
            name_counts[item] = name_counts.get(item, 0) + 1
            if name_counts[item] > 1:
                stats['duplicate_names'].append(item)

            # 检测过长文件名（>100字符）
            if len(item) > 100:
                stats['very_long_names'].append(item)

            # 提取目录序号（仅限根目录）
            if depth == 0 and os.path.isdir(full_path):
                stats['root_dirs'].append(item)
                serial = extract_serial_number(item)
                if serial is not None:
                    if serial in dir_serials:
                        dir_serials[serial].append(item)
                    else:
                        dir_serials[serial] = [item]

            # 检查目录是否为空
            if os.path.isdir(full_path):
                stats['total_dirs'] += 1
                try:
                    sub_items = os.listdir(full_path)
                    if len(sub_items) == 0:
                        stats['empty_dirs'].append(item)
                except PermissionError:
                    pass

                scan_dir(full_path, depth + 1)
                continue

            # 文件处理
            stats['total_files'] += 1
            ext = os.path.splitext(item)[1].lower()
            stats['extensions'][ext] = stats['extensions'].get(ext, 0) + 1

            # 检查文件名是否包含表情
            has_emoji = any(emoji in item for emoji in BASE_EMOJIS.keys())
            if not has_emoji and not item.startswith('.'):
                stats['no_emoji_files'].append(item)

    scan_dir(target_path, 0)

    # 收集序号重复的目录
    for serial, dirs in dir_serials.items():
        if len(dirs) > 1:
            stats['duplicate_serials'].append((serial, dirs))

    # 输出报告
    print('\n📊 目录结构统计:\n')
    print(f'  📁 总文件数: {stats["total_files"]:,}')
    print(f'  📂 总目录数: {stats["total_dirs"]:,}')
    print(f'  📏 最大深度: {stats["max_depth"]} 层\n')

    # 扩展名分布（Top 10）
    print('📋 文件类型分布 (Top 10):')
    for ext, count in sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True)[:10]:
        icon = EXT_ICONS.get(ext, '📄')
        ext_name = ext or '无扩展名'
        print(f'  {icon} {ext_name}: {count:,} 个')

    # 问题检测
    issues = []
    issue_details = {}

    if stats['no_emoji_files']:
        issues.append(f'⚠️  未使用表情符号的文件: {len(stats["no_emoji_files"])} 个')
        issue_details['no_emoji'] = len(stats['no_emoji_files'])

    if stats['duplicate_names']:
        unique_dups = len(set(stats['duplicate_names']))
        issues.append(f'⚠️  重复文件名: {unique_dups} 个')
        issue_details['duplicate_names'] = unique_dups

    if stats['very_long_names']:
        issues.append(f'⚠️  过长文件名(>100字符): {len(stats["very_long_names"])} 个')
        issue_details['long_names'] = len(stats['very_long_names'])

    if stats['duplicate_serials']:
        issues.append(f'⚠️  目录序号重复: {len(stats["duplicate_serials"])} 组')
        issue_details['duplicate_serials'] = stats['duplicate_serials']

    if stats['empty_dirs']:
        issues.append(f'⚠️  空目录: {len(stats["empty_dirs"])} 个')
        issue_details['empty_dirs'] = len(stats['empty_dirs'])

    if issues:
        print('\n⚠️  问题检测:')
        for issue in issues:
            print(f'  {issue}')

        # 详细信息
        if stats['duplicate_serials']:
            print('\n  序号重复详情:')
            for serial, dirs in stats['duplicate_serials']:
                dir_list = ', '.join(dirs)
                print(f'    序号 {serial:02d}: {dir_list}')

    # 整理建议
    print('\n💡 整理建议:\n')

    if stats['no_emoji_files']:
        print('  1. 为未分类文件添加表情符号和分类区前缀')
        print('     示例: `note.md` → `📝_01_note.md`')

    if stats['duplicate_serials']:
        print('  2. 修复目录序号重复问题，重新排序')
        print('     示例: `04-📊_01_Zabbix` → `04-📊_01_Zabbix`')
        print('              `04-🟢_01_高可用` → `05-🟢_01_高可用`')

    if stats['duplicate_names']:
        print('  3. 处理重复文件名，添加序号区分')
        print('     示例: `script.py` → `💻_01_script_01.py`')

    if stats['max_depth'] > 5:
        print(f'  4. 目录层级过深(当前{stats["max_depth"]}层)，建议扁平化整理')

    if stats['empty_dirs']:
        print(f'  5. 删除 {len(stats["empty_dirs"])} 个空目录以清理结构')

    # 生成详细报告
    report_dir = os.path.dirname(target_path)
    report_name = f'folder_analysis_{os.path.basename(target_path)}.md'
    report_path = os.path.join(report_dir, report_name)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f'# 📊 目录分析报告\n\n')
        f.write(f'> 📂 目录: `{target_path}`\n')
        f.write(f'> 🕐 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')

        f.write('## 📈 统计摘要\n\n')
        f.write(f'- 📁 总文件数: {stats["total_files"]:,}\n')
        f.write(f'- 📂 总目录数: {stats["total_dirs"]:,}\n')
        f.write(f'- 📏 最大深度: {stats["max_depth"]} 层\n\n')

        f.write('## 📋 文件类型分布\n\n')
        f.write('| 扩展名 | 数量 | 图标 |\n')
        f.write('|--------|------|------|\n')
        for ext, count in sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True):
            icon = EXT_ICONS.get(ext, '📄')
            ext_name = ext or '无扩展名'
            f.write(f'| {ext_name} | {count:,} | {icon} |\n')

        f.write('\n## 📂 根目录列表\n\n')
        for i, d in enumerate(sorted(stats['root_dirs'])):
            f.write(f'{i+1}. {d}\n')

        if issues:
            f.write('\n## ⚠️  发现的问题\n\n')
            if 'duplicate_serials' in issue_details:
                f.write('### 目录序号重复\n\n')
                for serial, dirs in issue_details['duplicate_serials']:
                    dir_list = ', '.join(dirs)
                    f.write(f'- 序号 **{serial:02d}**: {dir_list}\n')
                f.write('\n')

            f.write('### 其他问题\n\n')
            for issue in issues:
                f.write(f'- {issue}\n')

        f.write('\n## 💡 整理建议\n\n')
        f.write('1. **添加表情符号前缀** - 为未分类文件按类型添加对应的表情符号\n')
        f.write('2. **修复序号重复** - 重新排列目录序号，确保连续性\n')
        f.write('3. **处理重复文件** - 为重复文件名添加后缀区分\n')
        if stats['max_depth'] > 5:
            f.write('4. **扁平化结构** - 目录层级过深建议重新整理\n')
        if stats['empty_dirs']:
            f.write('5. **清理空目录** - 删除不需要的空目录\n')

        f.write('\n## 🎯 命名规范速查\n\n')
        f.write('### 表情符号分类\n\n')
        f.write('| 色系 | 表情 | 含义 | 适用场景 |\n')
        f.write('|------|------|------|----------|\n')
        f.write('| 🔴 红色 | 🔴🚨🔥❤️🧯 | 核心/警告 | 主入口、高危操作、高频脚本 |\n')
        f.write('| 🟠 橙色 | 🟠⚙️🛠️🧰🪛 | 工具/配置 | 通用工具、环境配置、批量处理 |\n')
        f.write('| 🟡 黄色 | 🟡✏️📝💡📒 | 学习/记录 | 教学示例、草稿、学习笔记 |\n')
        f.write('| 🟢 绿色 | 🟢✅🟩🌱🧩 | 稳定/完成 | 已验证版本、正式上线、模块组件 |\n')
        f.write('| 🔵 蓝色 | 🔵💻📚🔍🧠 | 开发/技术 | 编程脚本、技术文档、算法研究 |\n')
        f.write('| 🟣 紫色 | 🟣✨🧪🚀🧬 | 高级/实验 | 内部测试、优化技巧、创新探索 |\n')
        f.write('| ⚫⚪ 黑白 | ⚫⚪📦🗄️🧾 | 历史/归档 | 旧版归档、通用模板、存档文件 |\n\n')

        f.write('### 序号补零规则\n\n')
        f.write('- **≤ 99 个文件**: 2 位 (01, 02 ... 10, 11)\n')
        f.write('- **≤ 999 个文件**: 3 位 (001, 002 ... 010, 011)\n')
        f.write('- **超过 999**: 4 位 (0001, 0002 ... 1000)\n\n')

        f.write('### 命名格式\n\n')
        f.write('```\n')
        f.write('[表情][分类区][序号]_标题.扩展名\n')
        f.write('```\n\n')
        f.write('示例:\n')
        f.write('- `🚨 01_数据删除脚本.bat`\n')
        f.write('- `💻 02_系统监控工具.py`\n')
        f.write('- `📚 03_学习笔记.md`\n')

    print(f'\n📄 详细报告已生成: {report_path}')
    print('\n✅ 分析完成!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python analyze_folder.py <目录路径>')
        sys.exit(1)

    target_path = sys.argv[1]
    analyze_directory(target_path)
