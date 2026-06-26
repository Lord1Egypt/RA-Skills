# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 主入口

使用流程:
1. 用户登录，保存cookie
2. 询问用户是否登录成功
3. 询问用户小说名
4. 询问用户上传的章节目录文件在哪
5. 发布章节（自动截取正文内容）
"""

import sys
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Optional

# 导入各模块
from login import login, logout, check_login_detail
from works import get_works, get_work
from publisher import publish_chapter, publish_batch, Chapter
from browser import get_browser


# 中文数字到阿拉伯数字的映射
CN_NUM_MAP = {
    '零': 0, '〇': 0,
    '一': 1, '壹': 1,
    '二': 2, '贰': 2,
    '三': 3, '叁': 3,
    '四': 4, '肆': 4,
    '五': 5, '伍': 5,
    '六': 6, '陆': 6,
    '七': 7, '柒': 7,
    '八': 8, '捌': 8,
    '九': 9, '玖': 9,
    '十': 10, '拾': 10,
    '百': 100, '佰': 100,
    '千': 1000, '仟': 1000,
    '万': 10000, '萬': 10000,
}


def cn_to_arabic(cn_num: str) -> int:
    """
    将中文数字转换为阿拉伯数字
    
    支持：
    - 简单数字：一、二、三、十、十一、二十...
    - 复合数字：二十一、三十五、一百二十三...
    
    Args:
        cn_num: 中文数字字符串
        
    Returns:
        int: 阿拉伯数字
    """
    if not cn_num:
        return 0
    
    # 如果已经是数字，直接返回
    if cn_num.isdigit():
        return int(cn_num)
    
    # 简单处理：单个中文数字
    if cn_num in CN_NUM_MAP and CN_NUM_MAP[cn_num] < 10:
        return CN_NUM_MAP[cn_num]
    
    # 处理"十"、"十一"到"十九"
    if cn_num == '十':
        return 10
    if cn_num.startswith('十') and len(cn_num) == 2:
        # 十一、十二...十九
        return 10 + CN_NUM_MAP.get(cn_num[1], 0)
    if cn_num.endswith('十') and len(cn_num) == 2:
        # 二十、三十...九十
        return CN_NUM_MAP.get(cn_num[0], 0) * 10
    
    # 处理"二十一"到"九十九"
    if '十' in cn_num and len(cn_num) >= 3:
        parts = cn_num.split('十')
        tens = CN_NUM_MAP.get(parts[0], 1) if parts[0] else 10
        ones = CN_NUM_MAP.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return tens * 10 + ones
    
    # 处理百、千、万级别的数字（简单实现）
    result = 0
    temp = 0
    
    for char in cn_num:
        if char in CN_NUM_MAP:
            num = CN_NUM_MAP[char]
            if num >= 10:
                if temp == 0:
                    temp = 1
                result += temp * num
                temp = 0
            else:
                temp = num
    
    result += temp
    return result


def convert_chapter_title(title: str) -> str:
    """
    转换章节标题中的中文数字为阿拉伯数字
    
    Examples:
        "第一章 重生" -> "第1章 重生"
        "第十二章 暗影" -> "第12章 暗影"
        "第二十三章 决战" -> "第23章 决战"
        "第一百章 终章" -> "第100章 终章"
    
    Args:
        title: 原标题
        
    Returns:
        str: 转换后的标题
    """
    # 匹配中文数字格式的章节标题
    # 支持格式：第一章、第二十三章、第一百章等
    pattern = r'第\s*([零〇一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬]+)\s*章'
    
    match = re.search(pattern, title)
    if match:
        cn_num = match.group(1)
        arabic_num = cn_to_arabic(cn_num)
        # 替换标题中的中文数字
        new_title = re.sub(pattern, f'第{arabic_num}章', title)
        return new_title
    
    return title


def detect_template_type(md_content: str) -> str:
    """
    检测章节文件的模板类型
    
    Returns:
        str: "detailed" (详细版) 或 "simple" (简洁版)
    """
    lines = md_content.split('\n')
    
    # 检测是否有 --- 分隔符（详细版模板的特征）
    has_separator = any(line.strip() == '---' for line in lines)
    
    # 检测是否有 > 引用块（元数据或钩子）
    has_quote_block = any(line.strip().startswith('>') for line in lines)
    
    # 如果有分隔符或引用块，认为是详细版模板
    if has_separator or has_quote_block:
        return "detailed"
    
    return "simple"


def extract_content_simple(md_content: str) -> Dict[str, str]:
    """
    从简洁版 Markdown 文件中提取内容
    
    输入格式（模板B - 简洁版）:
    # 第一章 重生
    
    正文内容...
    
    Returns:
        dict: {"title": "章节标题", "content": "正文内容"}
    """
    result = {"title": "", "content": ""}
    
    lines = md_content.split('\n')
    
    # 1. 提取标题（第一个 # 开头的行）
    title_found = False
    content_start = 0
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if not title_found and stripped_line.startswith('# '):
            full_title = stripped_line.replace('# ', '').strip()
            # 转换中文数字为阿拉伯数字（"第一章" → "第1章")
            full_title = convert_chapter_title(full_title)
            # 处理标题格式：去掉章节号前导零（"第05章" → "第5章"）
            full_title = re.sub(r'第\s*0(\d+)\s*章', r'第 \1 章', full_title)
            result["title"] = full_title
            # 同时提取纯标题（去掉"第X章"前缀）
            pure_title = re.sub(r'第\s*\d+\s*章\s*', '', full_title).strip()
            result["pure_title"] = pure_title
            title_found = True
            content_start = i + 1  # 正文从标题下一行开始
            break
    
    # 2. 提取正文内容（标题之后的所有内容）
    content_lines = lines[content_start:]
    
    # 3. 清理正文内容
    # 去掉开头和结尾的空行
    while content_lines and content_lines[0].strip() == '':
        content_lines.pop(0)
    while content_lines and content_lines[-1].strip() == '':
        content_lines.pop()
    
    result["content"] = '\n'.join(content_lines)
    
    return result


def extract_content_detailed(md_content: str) -> Dict[str, str]:
    """
    从详细版 Markdown 文件中提取内容
    
    输入格式（模板A - 详细版）:
    # 第05章 灵契学院
    
    > **本章概要**：...
    > **本章爽点**：...
    ...
    
    ---
    
    正文内容（可能包含多个 --- 场景分隔）...
    
    ---
    
    > **章末钩子**：...
    > **下章预告**：...
    
    Returns:
        dict: {"title": "章节标题", "content": "正文内容"}
    """
    result = {"title": "", "content": ""}
    
    lines = md_content.split('\n')
    
    # 1. 提取标题（第一个 # 开头的行，支持带缩进的标题行）
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            full_title = stripped_line.replace('# ', '').strip()
            # 转换中文数字为阿拉伯数字（"第一章" → "第1章")
            full_title = convert_chapter_title(full_title)
            # 处理标题格式：去掉章节号前导零（"第05章" → "第5章"）
            full_title = re.sub(r'第\s*0(\d+)\s*章', r'第 \1 章', full_title)
            result["title"] = full_title
            # 同时提取纯标题（去掉"第X章"前缀）
            pure_title = re.sub(r'第\s*\d+\s*章\s*', '', full_title).strip()
            result["pure_title"] = pure_title
            break
    
    # 2. 找到正文开始位置
    # 正文开始于第一个 --- 之后（元数据块结束）
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            content_start = i + 1  # --- 之后的第一行
            break
    
    # 3. 找到正文结束位置
    # 正文结束于最后一段 > 开头的引用块之前（章末钩子）
    # 从文件末尾往回找，找到第一个非空、非 > 的行之后出现的连续 > 行
    content_end = len(lines)
    
    # 从末尾往回扫描，找到钩子块的起始位置
    in_hook = False
    hook_start = len(lines)
    
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        
        if line == '':
            # 空行，继续往前找
            continue
        
        if line.startswith('>'):
            # 进入钩子区域
            in_hook = True
            hook_start = i
        else:
            # 遇到非空、非 > 的行，说明已经离开钩子区域
            if in_hook:
                # 钩子区域结束，正文到此为止
                content_end = i + 1
                break
            else:
                # 还没遇到钩子，继续往前找
                continue
    
    # 4. 提取正文内容
    content_lines = lines[content_start:content_end]
    
    # 5. 清理正文内容
    # 去掉开头和结尾的空行和分隔符
    while content_lines and content_lines[0].strip() in ['', '---']:
        content_lines.pop(0)
    while content_lines and content_lines[-1].strip() in ['', '---']:
        content_lines.pop()
    
    result["content"] = '\n'.join(content_lines)
    
    return result


def extract_content(md_content: str) -> Dict[str, str]:
    """
    从 Markdown 文件中截取正文内容
    
    自动检测模板类型并使用对应的解析方法：
    - 模板A（详细版）：带元数据块（概要、爽点）和章末钩子
    - 模板B（简洁版）：只有标题和正文
    
    Returns:
        dict: {"title": "章节标题", "content": "正文内容"}
    """
    template_type = detect_template_type(md_content)
    
    if template_type == "simple":
        return extract_content_simple(md_content)
    else:
        return extract_content_detailed(md_content)


def load_chapters_from_directory(directory_path: str) -> List[Dict[str, str]]:
    """
    从目录加载所有章节文件
    
    Args:
        directory_path: 章节文件目录路径
    
    Returns:
        List[Dict]: 章节列表，每项包含 title 和 content
    """
    chapters = []
    dir_path = Path(directory_path)
    
    if not dir_path.exists():
        print(f"[错误] 目录不存在: {directory_path}")
        return chapters
    
    # 获取所有 .md 文件，按文件名排序
    md_files = sorted(dir_path.glob('*.md'))
    
    if not md_files:
        print(f"[提示] 目录中没有找到 .md 文件: {directory_path}")
        return chapters
    
    print(f"[加载] 找到 {len(md_files)} 个章节文件")
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            chapter = extract_content(content)
            
            if chapter["title"] and chapter["content"]:
                chapters.append(chapter)
                print(f"  - {chapter['title']} ({len(chapter['content'])} 字)")
            else:
                print(f"  - 跳过 {md_file.name}（无法提取标题或内容）")
        except Exception as e:
            print(f"  - 错误 {md_file.name}: {e}")
    
    return chapters


def load_chapters_from_file(file_path: str) -> List[Dict[str, str]]:
    """
    从单个文件或 JSON 列表文件加载章节
    
    Args:
        file_path: 文件路径（.md 或 .json）
    
    Returns:
        List[Dict]: 章节列表
    """
    chapters = []
    path = Path(file_path)
    
    if not path.exists():
        print(f"[错误] 文件不存在: {file_path}")
        return chapters
    
    if path.suffix == '.md':
        # 单个 Markdown 文件
        content = path.read_text(encoding='utf-8')
        chapter = extract_content(content)
        if chapter["title"] and chapter["content"]:
            chapters.append(chapter)
        else:
            print(f"[错误] 无法从文件提取章节内容")
    
    elif path.suffix == '.json':
        # JSON 格式的章节列表
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for item in data:
                    if "title" in item and "content" in item:
                        chapters.append(item)
            elif isinstance(data, dict):
                if "title" in data and "content" in data:
                    chapters.append(data)
            
            print(f"[加载] 从 JSON 加载 {len(chapters)} 个章节")
        except Exception as e:
            print(f"[错误] JSON 解析失败: {e}")
    
    else:
        # 其他格式，尝试作为纯文本处理
        content = path.read_text(encoding='utf-8')
        # 使用文件名作为标题
        title = path.stem
        chapters.append({"title": title, "content": content})
    
    return chapters


def interactive_flow():
    """
    交互式发布流程
    
    流程:
    1. 用户登录，保存cookie
    2. 询问用户是否登录成功
    3. 询问用户小说名
    4. 询问用户上传的章节目录文件在哪
    5. 发布章节
    """
    
    print("\n" + "="*60)
    print("📚 番茄小说自动发布系统")
    print("="*60 + "\n")
    
    # ===== 步骤1: 登录 =====
    print("【步骤1】登录番茄小说")
    print("-"*40)
    
    # 先检查是否已登录
    login_status = check_login_detail()
    
    if login_status.get("logged_in"):
        print(f"[OK] 已登录: {login_status.get('message')}")
        print()
        
        # 询问是否需要重新登录
        relogin = input("是否需要重新登录？(y/N): ").strip().lower()
        if relogin == 'y':
            logout()
            print("已退出登录，开始重新登录...")
            login_result = login()
        else:
            login_result = {"success": True, "message": "使用现有登录状态"}
    else:
        print("⚠ 未登录或登录已过期")
        print()
        print("正在打开登录页面...")
        login_result = login()
    
    print()
    
    # ===== 步骤2: 确认登录成功 =====
    print("【步骤2】确认登录状态")
    print("-"*40)
    
    if login_result.get("success"):
        print(f"[OK] 登录成功: {login_result.get('message')}")
        
        # 询问用户确认
        confirm = input("请确认浏览器显示已登录，是否继续？(Y/n): ").strip().lower()
        if confirm == 'n':
            print("用户取消操作，退出程序")
            return
    else:
        print(f"✗ 登录失败: {login_result.get('message')}")
        retry = input("是否重新尝试登录？(Y/n): ").strip().lower()
        if retry != 'n':
            login_result = login()
            if not login_result.get("success"):
                print("登录仍然失败，请检查网络或账号问题")
                return
        else:
            return
    
    print()
    
    # ===== 步骤3: 获取作品列表，选择小说 =====
    print("【步骤3】选择小说作品")
    print("-"*40)
    
    # 获取作品列表
    print("正在获取作品列表...")
    works_result = get_works()
    
    if not works_result.get("success"):
        print(f"✗ 获取作品列表失败: {works_result.get('message')}")
        # 让用户手动输入作品名
        work_name = input("请输入小说名称: ").strip()
        if not work_name:
            print("未输入小说名称，退出程序")
            return
    else:
        works = works_result.get("works", [])
        if not works:
            print("未找到任何作品")
            work_name = input("请输入小说名称: ").strip()
            if not work_name:
                print("未输入小说名称，退出程序")
                return
        else:
            print(f"\n找到 {len(works)} 部作品:")
            for i, work in enumerate(works, 1):
                print(f"  {i}. {work['title']} ({work.get('status', '未知状态')})")
            
            print()
            choice = input("请选择作品（输入序号）或直接输入作品名: ").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(works):
                    work_name = works[idx]['title']
                else:
                    print("序号无效")
                    work_name = input("请输入小说名称: ").strip()
            else:
                work_name = choice
            
            if not work_name:
                print("未指定作品名称，退出程序")
                return
    
    print(f"\n[OK] 已选择作品: {work_name}")
    print()
    
    # ===== 步骤4: 输入章节文件路径 =====
    print("【步骤4】指定章节文件")
    print("-"*40)
    
    print("请提供章节文件位置:")
    print("  - 可以是单个 .md 文件")
    print("  - 可以是包含多个 .md 文件的目录")
    print("  - 可以是 .json 格式的章节列表文件")
    print()
    
    file_path = input("请输入章节文件或目录路径: ").strip()
    
    # 处理路径（支持拖拽的路径可能带引号）
    file_path = file_path.strip('"').strip("'")
    
    if not file_path:
        print("未输入文件路径，退出程序")
        return
    
    # 检查路径是否存在
    path = Path(file_path)
    if not path.exists():
        print(f"✗ 路径不存在: {file_path}")
        return
    
    # 判断是目录还是文件
    if path.is_dir():
        print(f"\n加载目录: {file_path}")
        chapters = load_chapters_from_directory(file_path)
    else:
        print(f"\n加载文件: {file_path}")
        chapters = load_chapters_from_file(file_path)
    
    if not chapters:
        print("未加载到任何章节，退出程序")
        return
    
    print(f"\n[OK] 已加载 {len(chapters)} 个章节")
    print()
    
    # ===== 步骤5: 确认并发布 =====
    print("【步骤5】选择发布模式")
    print("-"*40)
    
    print("待发布章节列表:")
    for i, ch in enumerate(chapters, 1):
        print(f"  {i}. {ch['title']} ({len(ch['content'])} 字)")
    
    print()
    print("请选择发布模式:")
    print("  1. 直接发布 (publish) - 确认内容无误，直接发布")
    print("  2. 存入草稿箱 (draft) - 内容待完善，先保存草稿")
    print()
    
    mode_input = input("请输入模式编号 (1/2，默认1): ").strip()
    mode = "draft" if mode_input == "2" else "publish"
    mode_desc = "存入草稿箱" if mode == "draft" else "直接发布"
    
    print(f"\n[OK] 已选择: {mode_desc}")
    
    confirm_publish = input(f"确认{mode_desc}以上章节？(Y/n): ").strip().lower()
    
    if confirm_publish == 'n':
        print("用户取消操作，退出程序")
        return
    
    # 询问发布间隔
    print()
    interval_input = input("章节发布间隔（秒，默认5）: ").strip()
    interval = int(interval_input) if interval_input.isdigit() else 5
    
    print()
    print("="*60)
    print(f"开始{mode_desc}...")
    print("="*60 + "\n")
    
    # 执行批量发布
    chapter_objs = [
        Chapter(title=ch["title"], content=ch["content"])
        for ch in chapters
    ]
    
    results = publish_batch(work_name, chapter_objs, interval, mode=mode)
    
    # 显示发布结果
    print()
    print("="*60)
    print(f"{mode_desc}完成")
    print("="*60)
    
    success_count = sum(1 for r in results if r.get("success"))
    fail_count = len(results) - success_count
    
    print(f"\n{mode_desc}统计:")
    print(f"  [OK] 成功: {success_count} 章")
    print(f"  ✗ 失败: {fail_count} 章")
    
    if fail_count > 0:
        print("\n失败章节:")
        for r in results:
            if not r.get("success"):
                print(f"  - {r.get('chapter_title', '未知')}: {r.get('message')}")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        command = sys.argv[1]
        
        if command == "login":
            result = login()
            if result["success"]:
                print("\n[OK] 登录成功")
            else:
                print(f"\n✗ {result['message']}")
        
        elif command == "logout":
            logout()
            print("[OK] 已退出登录")
        
        elif command == "works":
            result = get_works()
            if result["success"]:
                for work in result["works"]:
                    print(f"  - {work['title']}")
            else:
                print(f"✗ {result['message']}")
        
        elif command == "publish":
            # 简化发布命令
            interactive_flow()
        
        elif command == "batch":
            interactive_flow()
        
        elif command == "status":
            result = check_login_detail()
            print(f"登录状态: {result}")
        
        else:
            print(f"未知命令: {command}")
            print("可用命令: login, logout, works, publish, batch, status")
    
    else:
        # 无参数时进入交互流程
        interactive_flow()


if __name__ == "__main__":
    main()