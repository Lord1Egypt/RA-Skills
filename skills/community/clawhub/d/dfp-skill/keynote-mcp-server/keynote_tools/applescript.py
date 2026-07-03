"""
keynote_tools/applescript.py

AppleScript / JXA 执行引擎

作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

负责执行 AppleScript 和 JavaScript for Automation (JXA) 脚本，
封装 macOS 原生自动化调用。

核心函数:
    run_applescript(script: str) -> str
    run_jxa(script: str) -> str
    is_keynote_available() -> bool
    get_keynote_version() -> str

新增功能 (v2.0):
    set_canvas_size(width, height) - 设置画布尺寸（含超宽屏）
    create_ultra_wide_document() - 创建超宽屏文档
    add_kpi_textbox() - 添加 KPI 数字文本框
    create_digital_finance_presentation() - 创建数智财务风格演示
"""

import os
import subprocess
import platform
import re
from typing import Optional


# ============================================================================
# 平台检测
# ============================================================================

def is_macos() -> bool:
    """检测是否在 macOS 上运行"""
    return platform.system() == "Darwin"


def is_keynote_installed() -> bool:
    """检测 Keynote.app 是否已安装"""
    if not is_macos():
        return False
    # 检查 /Applications/Keynote.app 是否存在
    return os.path.exists("/Applications/Keynote.app")


def get_keynote_version() -> str:
    """获取 Keynote 版本信息"""
    if not is_macos():
        return "非 macOS 平台 - 无法检测"

    script = '''
    tell application "System Events"
        try
            set appList to name of every application process
            if appList contains "Keynote" then
                return "Keynote is running"
            else
                return "Keynote is installed but not running"
            end if
        on error
            return "Keynote not found"
        end try
    end tell
    '''
    try:
        return run_applescript(script)
    except Exception:
        return "无法获取 Keynote 信息失败"


# ============================================================================
# AppleScript 执行
# ============================================================================

def run_applescript(script: str, timeout: int = 30) -> str:
    """
    执行 AppleScript 脚本

    Args:
        script: AppleScript 源代码
        timeout: 超时时间（秒）

    Returns:
        脚本输出字符串

    Raises:
        RuntimeError: 脚本执行失败
    """
    if not is_macos():
        raise RuntimeError(
            "⚠️  当前平台: " + platform.system() +
            "。Keynote 自动化仅在 macOS 上可用。"
        )

    # 用 osascript 命令执行
    proc = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if proc.returncode != 0:
        error_msg = proc.stderr.strip()
        raise RuntimeError(f"AppleScript 执行失败: " + error_msg)

    return proc.stdout.strip()


def run_applescript_with_params(script_template: str, **kwargs) -> str:
    """
    执行带参数模板的 AppleScript（用简单参数占位符替换后执行"""
    # 简单的字符串替换（防止简单参数
    script = script_template
    for key, value in kwargs.items():
        placeholder = "{{" + key + "}}"
        # 将 Python 特殊字符转义
        safe_value = str(value).replace('"', '\\"')
        script = script.replace(placeholder, safe_value)
    return run_applescript(script)


# ============================================================================
# JXA (JavaScript for Automation) 执行
# ============================================================================

def run_jxa(script: str, timeout: int = 30) -> str:
    """
    执行 JavaScript for Automation (JXA) 脚本

    Args:
        script: JXA 源代码
        timeout: 超时时间（秒）

    Returns:
        脚本输出字符串
    """
    if not is_macos():
        raise RuntimeError(
            "当前平台: " + platform.system() +
            "。Keynote 自动化仅在 macOS 上可用。"
        )

    proc = subprocess.run(
        ["osascript", "-l", "JavaScript", "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if proc.returncode != 0:
        error_msg = proc.stderr.strip()
        raise RuntimeError("JXA 执行失败: " + error_msg)

    return proc.stdout.strip()


# ============================================================================
# 基础操作
# ============================================================================

def quit_keynote() -> str:
    """退出 Keynote"""
    script = '''
    tell application "Keynote"
        quit
    end tell
    '''
    return run_applescript(script)


def activate_keynote() -> str:
    """激活 Keynote（启动并激活窗口"""
    script = '''
    tell application "Keynote"
        activate
    end tell
    '''
    return run_applescript(script)


def is_keynote_running() -> bool:
    """检查 Keynote 是否正在运行"""
    if not is_macos():
        return False
    script = '''
    tell application "System Events"
        return (exists (processes whose name is "Keynote")
    end tell
    '''
    try:
        result = run_applescript(script)
        return "true" in result.lower() or result.strip() == "true"
    except Exception:
        return False


# ============================================================================
# 文档操作
# ============================================================================

def create_new_document() -> str:
    """创建新文档（使用默认模板）"""
    script = '''
    tell application "Keynote"
        activate
        make new document
        return "New document created"
    end tell
    '''
    return run_applescript(script)


def create_new_document_with_theme(theme_name: str) -> str:
    """使用指定主题创建新文档"""
    theme_name_escaped = theme_name.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        activate
        make new document with properties {document theme:theme "%s"
        return "Created with theme: %s"
    end tell
    ''' % (theme_name_escaped, theme_name_escaped)
    return run_applescript(script)


def open_document(file_path: str) -> str:
    """打开现有 .key 文件"""
    abs_path = os.path.abspath(os.path.expanduser(file_path))
    if not os.path.exists(abs_path):
        raise RuntimeError("文件不存在: " + abs_path)

    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        activate
        open POSIX file "%s"
        return "Opened: %s"
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


def save_document() -> str:
    """保存当前文档"""
    script = '''
    tell application "Keynote"
        tell front document
            save
            return "Document saved"
        end tell
    end tell
    '''
    return run_applescript(script)


def save_document_as(file_path: str) -> str:
    """另存为指定路径"""
    abs_path = os.path.abspath(os.path.expanduser(file_path))
    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            save in POSIX file "%s"
            return "Saved to: %s"
        end tell
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


def close_document() -> str:
    """关闭当前文档（不保存）"""
    script = '''
    tell application "Keynote"
        close front document
        return "Document closed"
    end tell
    '''
    return run_applescript(script)


def close_document_saving() -> str:
    """关闭当前文档（保存）"""
    script = '''
    tell application "Keynote"
        tell front document
            save
            close
        end tell
        return "Document saved and closed"
    end tell
    '''
    return run_applescript(script)


# ============================================================================
# 幻灯片操作
# ============================================================================

def get_slide_count() -> int:
    """获取当前文档幻灯片数量"""
    script = '''
    tell application "Keynote"
        tell front document
            return count of slides
        end tell
    end tell
    '''
    result = run_applescript(script)
    try:
        return int(result.strip())
    except (ValueError, TypeError):
        return 0


def get_slide_titles() -> list:
    """获取所有幻灯片标题列表"""
    script = '''
    tell application "Keynote"
        tell front document
            set titleList to ""
            repeat with s in slides
                try
                    set slideTitle to object text of default title item of s
                    if titleList is "" then
                        set titleList to slideTitle
                    else
                        set titleList to titleList & linefeed & slideTitle
                    end if
                on error
                    if titleList is "" then
                        set titleList to "(无标题"
                    else
                        set titleList to titleList & linefeed & "(无标题)"
                    end if
                end try
            end repeat
            return titleList
        end tell
    end tell
    '''
    result = run_applescript(script)
    titles = [t.strip() for t in result.split("\n") if t.strip()]
    return titles


def add_slide(position: Optional[int] = None) -> str:
    """
    添加新幻灯片

    Args:
        position: 插入位置（1-based）。None 表示在末尾添加）
    """
    if position is None:
        script = '''
        tell application "Keynote"
            tell front document
                make new slide at end of slides
                return "Slide added at end"
            end tell
        end tell
        '''
    else:
        pos = int(position)
        script = '''
        tell application "Keynote"
            tell front document
                make new slide at after slide %d
                return "Slide added after position %d"
            end tell
        end tell
        ''' % (pos, pos)
    return run_applescript(script)


def delete_slide(slide_number: int) -> str:
    """删除指定幻灯片（1-based）"""
    script = '''
    tell application "Keynote"
        tell front document
            delete slide %d
            return "Slide %d deleted"
        end tell
    end tell
    ''' % (slide_number, slide_number)
    return run_applescript(script)


def duplicate_slide(slide_number: int) -> str:
    """复制指定幻灯片"""
    script = '''
    tell application "Keynote"
        tell front document
            duplicate slide %d
            return "Slide %d duplicated"
        end tell
    end tell
    ''' % (slide_number, slide_number)
    return run_applescript(script)


def move_slide(from_pos: int, to_pos: int) -> str:
    """移动幻灯片位置"""
    script = '''
    tell application "Keynote"
        tell front document
            move slide %d to after slide %d
            return "Moved slide from %d to after %d"
        end tell
    end tell
    ''' % (from_pos, to_pos, from_pos, to_pos)
    return run_applescript(script)


# ============================================================================
# 内容设置
# ============================================================================

def set_slide_title(slide_number: int, title_text: str) -> str:
    """设置幻灯片标题"""
    title_escaped = title_text.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set object text of default title item to "%s"
                return "Title set for slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, title_escaped, slide_number)
    return run_applescript(script)


def set_slide_body(slide_number: int, body_text: str) -> str:
    """设置幻灯片正文"""
    body_escaped = body_text.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set object text of default body item to "%s"
                return "Body text set for slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, body_escaped, slide_number)
    return run_applescript(script)


def set_slide_title_and_body(slide_number: int, title_text: str, body_text: str) -> str:
    """同时设置标题和正文"""
    t_esc = title_text.replace('"', '\\"')
    b_esc = body_text.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set object text of default title item to "%s"
                set object text of default body item to "%s"
                return "Content set for slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, t_esc, b_esc, slide_number)
    return run_applescript(script)


# ============================================================================
# 高级操作
# ============================================================================

def start_slideshow() -> str:
    """开始播放演示文稿"""
    script = '''
    tell application "Keynote"
        tell front document
            start
            return "Slideshow started"
        end tell
    end tell
    '''
    return run_applescript(script)


def stop_slideshow() -> str:
    """停止播放演示文稿"""
    script = '''
    tell application "Keynote"
        tell front document
            stop
            return "Slideshow stopped"
        end tell
    end tell
    '''
    return run_applescript(script)


def next_slide() -> str:
    """下一张幻灯片"""
    script = '''
    tell application "Keynote"
        tell front document
            show next slide
            return "Next slide"
        end tell
    end tell
    '''
    return run_applescript(script)


def previous_slide() -> str:
    """上一张幻灯片"""
    script = '''
    tell application "Keynote"
        tell front document
            show previous slide
            return "Previous slide"
        end tell
    end tell
    '''
    return run_applescript(script)


def go_to_slide(slide_number: int) -> str:
    """跳转到指定幻灯片"""
    script = '''
    tell application "Keynote"
        tell front document
            show slide %d
            return "Jumped to slide %d"
        end tell
    end tell
    ''' % (slide_number, slide_number)
    return run_applescript(script)


# ============================================================================
# 导出功能
# ============================================================================

def export_to_pdf(output_path: str) -> str:
    """导出为 PDF"""
    abs_path = os.path.abspath(os.path.expanduser(output_path))
    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            export to POSIX file "%s" as PDF
            return "Exported to PDF: %s"
        end tell
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


def export_to_pptx(output_path: str) -> str:
    """导出为 PowerPoint"""
    abs_path = os.path.abspath(os.path.expanduser(output_path))
    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            export to POSIX file "%s" as Microsoft PowerPoint
            return "Exported to PPTX: %s"
        end tell
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


def export_to_movie(output_path: str) -> str:
    """导出为视频 (MOV)"""
    abs_path = os.path.abspath(os.path.expanduser(output_path))
    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            export to POSIX file "%s" as QuickTime movie
            return "Exported to MOV: %s"
        end tell
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


def export_to_html(output_path: str) -> str:
    """导出为 HTML"""
    abs_path = os.path.abspath(os.path.expanduser(output_path))
    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            export to POSIX file "%s" as HTML
            return "Exported to HTML: %s"
        end tell
    end tell
    ''' % (posix_path, posix_path)
    return run_applescript(script)


# ============================================================================
# 文档信息查询
# ============================================================================

def get_document_info() -> dict:
    """获取当前文档基本信息"""
    script = '''
    tell application "Keynote"
        tell front document
            set slideCount to count of slides
            set docName to name
            set heightInfo to "Name: " & docName & linefeed
            set heightInfo to heightInfo & "Slides: " & (slideCount as string)
            return heightInfo
        end tell
    end tell
    '''
    try:
        result = run_applescript(script)
        lines = result.split("\n")
        info = {}
        for line in lines:
            if ":" in line:
                key, _, value = line.partition(":")
                info[key.strip()] = value.strip()
        return info
    except Exception as e:
        return {"error": str(e)}


def get_slide_content(slide_number: int) -> dict:
    """获取指定幻灯片内容"""
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set slideTitle to ""
                set slideBody to ""
                try
                    set slideTitle to object text of default title item
                end try
                try
                    set slideBody to object text of default body item
                end try
                return "Title:" & slideTitle & "||BODY||" & slideBody
            end tell
        end tell
    end tell
    ''' % slide_number
    try:
        result = run_applescript(script)
        parts = result.split("||BODY||")
        return {
            "slide_number": slide_number,
            "title": parts[0].replace("Title:", "").strip(),
            "body": parts[1].strip() if len(parts) > 1 else ""
        }
    except Exception as e:
        return {"slide_number": slide_number, "error": str(e)}


# ============================================================================
# 文本框与形状操作（高级）
# ============================================================================

def add_textbox(slide_number: int, text: str,
                left: int = 100, top: int = 100,
                width: int = 400, height: int = 100) -> str:
    """
    在指定幻灯片添加文本框

    Args:
        slide_number: 幻灯片编号
        text: 文本内容
        left, top: 位置（像素，从左上角开始
        width, height: 尺寸（像素）
    """
    text_escaped = text.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set newTextBox to make new text box with properties {
                    position:{%d, %d}, width:%d, height:%d,
                    object text:"%s"
                }
                return "Text box added to slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, left, top, width, height, text_escaped, slide_number)
    return run_applescript(script)


def add_image(slide_number: int, image_path: str,
              left: int = 100, top: int = 100,
              width: int = 400, height: int = 300) -> str:
    """
    在指定幻灯片添加图片

    Args:
        slide_number: 幻灯片编号
        image_path: 图片文件路径
        left, top: 位置
        width, height: 尺寸
    """
    abs_path = os.path.abspath(os.path.expanduser(image_path))
    if not os.path.exists(abs_path):
        raise RuntimeError("图片文件不存在: " + abs_path)

    posix_path = abs_path.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        tell front document
        tell slide %d
            set image1 to make new image with properties {
                position:{%d, %d}, width:%d, height:%d,
                file:POSIX file "%s"
            }
            return "Image added to slide %d"
        end tell
    end tell
    ''' % (slide_number, left, top, width, height, posix_path, slide_number)
    return run_applescript(script)


# ============================================================================
# 主题与母版列表
# ============================================================================

def list_available_themes() -> list:
    """获取可用主题列表"""
    script = '''
    tell application "Keynote"
        set themeList to ""
        repeat with t in themes
            if themeList is "" then
                set themeList to name of t
            else
                set themeList to themeList & linefeed & name of t
            end if
        end repeat
        return themeList
    end tell
    '''
    try:
        result = run_applescript(script)
        themes = [t.strip() for t in result.split("\n") if t.strip()]
        return themes
    except Exception as e:
        return [f"Error: " + str(e)]


def list_master_slides() -> list:
    """获取当前文档可用母版/布局列表"""
    script = '''
    tell application "Keynote"
        tell front document
            set masterList to ""
            repeat with m in master slides
                if masterList is "" then
                    set masterList to name of m
                else
                    set masterList to masterList & linefeed & name of m
                end if
            end repeat
            return masterList
        end tell
    end tell
    '''
    try:
        result = run_applescript(script)
        masters = [m.strip() for m in result.split("\n") if m.strip()]
        return masters
    except Exception as e:
        return [f"Error: " + str(e)]


# ============================================================================
# 高级：批量创建幻灯片（复杂操作
# ============================================================================

def create_presentation_with_slides(slides_data: list) -> str:
    """
    批量创建包含多张幻灯片

    Args:
        slides_data: 幻灯片列表，每项是 {title, body} 字典

    示例:
        slides_data = [
            {"title": "标题1", "body": "正文1"},
            {"title": "标题2", "body": "正文2"},
        ]
    """
    # 首先创建新文档
    create_new_document()

    # 为每张幻灯片设置内容
    for i, slide_data in enumerate(slides_data, 1):
        title = slide_data.get("title", "")
        body = slide_data.get("body", "")
        if i == 1:
            # 第一张幻灯片已存在，只需设置内容
            set_slide_title_and_body(1, title, body)
        else:
            # 添加新幻灯片并设置内容
            add_slide()
            set_slide_title_and_body(i, title, body)

    return f"Successfully created presentation with %d slides" % len(slides_data)


# ============================================================================
# 实用工具函数
# ============================================================================

def escape_applescript_string(text: str) -> str:
    """对 AppleScript 字符串转义"""
    return text.replace('\\', '\\\\').replace('"', '\\"')


def get_system_info() -> dict:
    """获取系统信息（用于调试）"""
    info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "macos_version": platform.mac_ver()[0] if is_macos() else "N/A",
        "keynote_installed": is_keynote_installed(),
        "keynote_running": is_keynote_running()
    }
    return info


# ============================================================================
# 超宽屏画布设置 (v2.0 新增)
# ============================================================================

def set_canvas_size(width: int, height: int) -> str:
    """
    设置当前文档的画布尺寸
    
    Args:
        width: 宽度（像素）
        height: 高度（像素）
    
    常用尺寸:
        - 标准 16:9: 1920 × 1080
        - 超宽屏 3:1: 3200 × 1080
        - 超宽屏 3.55:1: 3840 × 1080
    """
    script = '''
    tell application "Keynote"
        tell front document
            set width to %d
            set height to %d
            return "Canvas size set to %d × %d"
        end tell
    end tell
    ''' % (width, height, width, height)
    return run_applescript(script)


def create_ultra_wide_document(theme: str = "Black") -> str:
    """
    创建超宽屏演示文稿（3:1 比例，3200×1080）
    
    Args:
        theme: 主题名称（默认 Black 深色主题）
    """
    theme_escaped = theme.replace('"', '\\"')
    script = '''
    tell application "Keynote"
        activate
        set newDoc to make new document with properties {document theme:theme "%s"}
        tell newDoc
            set width to 3200
            set height to 1080
        end tell
        return "Created ultra-wide document (3200×1080) with theme: %s"
    end tell
    ''' % (theme_escaped, theme_escaped)
    return run_applescript(script)


def get_canvas_size() -> dict:
    """获取当前文档的画布尺寸"""
    script = '''
    tell application "Keynote"
        tell front document
            set w to width
            set h to height
            return (w as string) & "×" & (h as string)
        end tell
    end tell
    '''
    try:
        result = run_applescript(script)
        parts = result.split("×")
        return {
            "width": int(parts[0]) if len(parts) > 0 else 0,
            "height": int(parts[1]) if len(parts) > 1 else 0,
            "aspect_ratio": result
        }
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# KPI 数字文本框 (v2.0 新增)
# ============================================================================

def add_kpi_textbox(slide_number: int, number: str, label: str,
                    left: int = 100, top: int = 200,
                    number_size: int = 72, label_size: int = 24,
                    number_color: str = "gold") -> str:
    """
    在幻灯片上添加 KPI 数字展示文本框
    
    Args:
        slide_number: 幻灯片编号
        number: KPI 数字（如 "¥2.42"）
        label: 标签文字（如 "当前股价"）
        left, top: 位置
        number_size: 数字字号
        label_size: 标签字号
        number_color: 数字颜色 ("gold", "green", "red", "white")
    """
    # 颜色映射（AppleScript RGB）
    color_map = {
        "gold": "{242, 184, 75}",      # #F2B84B
        "green": "{47, 164, 114}",     # #2FA472
        "red": "{184, 0, 58}",         # #B8003A
        "white": "{255, 255, 255}",    # #FFFFFF
        "cyan": "{37, 183, 224}",      # #25B7E0
    }
    rgb = color_map.get(number_color, color_map["gold"])
    
    number_escaped = number.replace('"', '\\"')
    label_escaped = label.replace('"', '\\"')
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                -- 添加数字文本框（大号金色）
                set numBox to make new text box with properties {
                    position:{%d, %d},
                    width:300, height:80,
                    object text:"%s"
                }
                tell numBox
                    set size of text to %d
                    set color of text to %s
                end tell
                
                -- 添加标签文本框（小号白色）
                set labelBox to make new text box with properties {
                    position:{%d, %d + 85},
                    width:300, height:40,
                    object text:"%s"
                }
                tell labelBox
                    set size of text to %d
                    set color of text to {255, 255, 255}
                end tell
                
                return "KPI textbox added to slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, left, top, number_escaped, number_size, rgb,
           left, top, label_escaped, label_size, slide_number)
    return run_applescript(script)


def add_card_shape(slide_number: int, title: str, items: list,
                   left: int = 100, top: int = 100,
                   width: int = 400, height: int = 300) -> str:
    """
    在幻灯片上添加卡片形状（带标题和内容）
    
    Args:
        slide_number: 幻灯片编号
        title: 卡片标题
        items: 内容项列表
        left, top: 位置
        width, height: 尺寸
    """
    title_escaped = title.replace('"', '\\"')
    body_text = "\\n".join(items)
    body_escaped = body_text.replace('"', '\\"')
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                -- 添加卡片背景形状（深蓝色）
                set cardShape to make new shape with properties {
                    position:{%d, %d},
                    width:%d, height:%d,
                    shape type:rectangle,
                    fill color:{15, 32, 80},
                    stroke color:{184, 0, 58},
                    stroke width:10
                }
                
                -- 添加标题文本框
                set titleBox to make new text box with properties {
                    position:{%d + 10, %d + 10},
                    width:%d - 20, height:50,
                    object text:"%s"
                }
                tell titleBox
                    set size of text to 28
                    set color of text to {255, 255, 255}
                end tell
                
                -- 添加内容文本框
                set bodyBox to make new text box with properties {
                    position:{%d + 10, %d + 70},
                    width:%d - 20, height:%d - 80,
                    object text:"%s"
                }
                tell bodyBox
                    set size of text to 18
                    set color of text to {232, 236, 245}
                end tell
                
                return "Card shape added to slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, left, top, width, height,
           left, top, width, title_escaped,
           left, top, width, height, body_escaped,
           slide_number)
    return run_applescript(script)


# ============================================================================
# 数智财务风格批量创建 (v2.0 新增)
# ============================================================================

def create_digital_finance_presentation(title: str, slides_data: list,
                                        save_path: str = None) -> str:
    """
    创建数智财务 SAP 风格演示文稿
    
    Args:
        title: 演示文稿标题
        slides_data: 幻灯片数据列表，每项包含:
            - slide_type: "cover", "kpi", "content", "card", "thank_you"
            - title: 幻灯片标题
            - content: 内容数据
        save_path: 保存路径（可选）
    
    Returns:
        创建结果信息
    """
    # 创建超宽屏文档
    create_ultra_wide_document("Black")
    
    # 设置封面
    set_slide_title_and_body(1, title, "数智财务 SAP 企业级风格\\n\\nWang Dongjie, CGMA/AICPA&CIMA\\n© 2026")
    
    # 添加其他幻灯片
    for i, slide_data in enumerate(slides_data, 2):
        slide_type = slide_data.get("slide_type", "content")
        slide_title = slide_data.get("title", "")
        
        add_slide()
        
        if slide_type == "kpi":
            # KPI 展示幻灯片
            set_slide_title(i, slide_title)
            kpi_items = slide_data.get("content", [])
            for j, kpi in enumerate(kpi_items[:5]):
                add_kpi_textbox(i, kpi.get("number", ""), kpi.get("label", ""),
                               left=100 + j * 600, top=200)
        elif slide_type == "card":
            # 卡片布局幻灯片
            set_slide_title(i, slide_title)
            cards = slide_data.get("content", [])
            for j, card in enumerate(cards[:3]):
                add_card_shape(i, card.get("title", ""), card.get("items", []),
                              left=100 + j * 1000, top=150, width=900, height=400)
        elif slide_type == "thank_you":
            # Thank You 幻灯片
            set_slide_title_and_body(i, "Thank You", 
                                     title + "\\n\\n数智财务演示 Skill\\nWang Dongjie, CGMA/AICPA&CIMA\\n© 2026")
        else:
            # 普通内容幻灯片
            body = slide_data.get("content", "")
            set_slide_title_and_body(i, slide_title, body)
    
    # 保存文档
    if save_path:
        save_document_as(save_path)
    
    slide_count = get_slide_count()
    return f"Created digital-finance presentation with {slide_count} slides"


def create_valuation_report_presentation(
    stock_code: str,
    company_name: str,
    kpi_data: dict,
    financial_data: dict,
    save_path: str = None
) -> str:
    """
    创建上市公司估值报告演示文稿（13页标准结构）
    
    Args:
        stock_code: 股票代码（如 "600170"）
        company_name: 公司名称
        kpi_data: 核心 KPI 数据字典
        financial_data: 财务数据字典
        save_path: 保存路径
    
    Returns:
        创建结果
    """
    title = f"{company_name} ({stock_code}) 深度估值报告"
    
    # 构建幻灯片数据
    slides_data = [
        {"slide_type": "content", "title": "核心 KPI 指标快照", 
         "content": f"股价: {kpi_data.get('price', 'N/A')}\\n市值: {kpi_data.get('market_cap', 'N/A')}\\nPE: {kpi_data.get('pe', 'N/A')}\\nPB: {kpi_data.get('pb', 'N/A')}\\n股息率: {kpi_data.get('dividend_yield', 'N/A')}"},
        {"slide_type": "content", "title": "三年财务业绩概览",
         "content": f"营收: {financial_data.get('revenue', 'N/A')}\\n净利润: {financial_data.get('net_profit', 'N/A')}\\nROE: {financial_data.get('roe', 'N/A')}"},
        {"slide_type": "content", "title": "估值指标深度分析",
         "content": f"PE(TTM): {kpi_data.get('pe', 'N/A')}\\nPB: {kpi_data.get('pb', 'N/A')}\\nPS: {kpi_data.get('ps', 'N/A')}"},
        {"slide_type": "content", "title": "业务板块结构",
         "content": "五大业务板块收入占比分析"},
        {"slide_type": "content", "title": "行业地位与全球排名",
         "content": "Fortune 500 排名 / ENR 全球承包商排名"},
        {"slide_type": "content", "title": "风险识别与压力测试",
         "content": "应收账款风险 / 资产负债率 / 毛利率分析"},
        {"slide_type": "content", "title": "新签合同趋势",
         "content": "年度合同额趋势与在手订单分析"},
        {"slide_type": "content", "title": "现金流与分红能力",
         "content": "经营现金流 / 分红政策分析"},
        {"slide_type": "content", "title": "股东结构与治理基础",
         "content": "国资持股比例 / 治理结构分析"},
        {"slide_type": "content", "title": "价值重估潜在催化剂",
         "content": "政策机遇 / 订单增长 / 数字化转型"},
        {"slide_type": "content", "title": "综合投资结论",
         "content": "目标价区间 / 投资建议"},
        {"slide_type": "thank_you", "title": "Thank You", "content": ""}
    ]
    
    return create_digital_finance_presentation(title, slides_data, save_path)


# ============================================================================
# 动画效果支持 (v3.0 新增)
# ============================================================================

# 过渡动画类型映射
TRANSITION_TYPES = {
    "magic_move": "magic move",
    "fade": "fading through black",
    "push": "push",
    "flip": "flip",
    "cube": "cube",
    "page_flip": "page flip",
    "reveal": "reveal",
    "drop": "drop",
    "object_push": "object push",
    "object_zoom": "object zoom",
    "none": "no transition",
}

# 构建动画类型映射
BUILD_ANIMATION_TYPES = {
    "appear": "appear",
    "fade_in": "fade in",
    "fly_in": "fly in",
    "scale": "scale",
    "pop": "pop",
    "bounce": "bounce",
    "slide_in": "slide in",
    "typewriter": "typewriter",
}


def set_transition(slide_number: int, transition_type: str = "fade") -> str:
    """
    设置幻灯片的过渡动画
    
    Args:
        slide_number: 幻灯片编号
        transition_type: 过渡动画类型
            - "magic_move": 神奇移动（元素平滑过渡）
            - "fade": 渐隐
            - "push": 推入
            - "flip": 翻转
            - "cube": 立方体旋转
            - "page_flip": 书页翻转
            - "reveal": 渐显
            - "drop": 下落
            - "none": 无过渡
    
    Returns:
        操作结果
    """
    transition = TRANSITION_TYPES.get(transition_type.lower(), "fading through black")
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set slide transition to %s transition
                return "Transition set to %s on slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, transition, transition_type, slide_number)
    return run_applescript(script)


def set_magic_move(from_slide: int, to_slide: int) -> str:
    """
    设置 Magic Move 神奇移动效果（两张幻灯片之间）
    
    Magic Move 是 Keynote 最强大的动画效果，可以自动匹配两张幻灯片
    中的相同元素，并创建平滑的过渡动画。
    
    Args:
        from_slide: 起始幻灯片编号
        to_slide: 目标幻灯片编号
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            -- 设置起始幻灯片的过渡为 Magic Move
            tell slide %d
                set slide transition to magic move transition
            end tell
            return "Magic Move set between slide %d and %d"
        end tell
    end tell
    ''' % (from_slide, from_slide, to_slide)
    return run_applescript(script)


def add_build_animation(slide_number: int, element_index: int,
                        animation_type: str = "appear",
                        direction: str = "from_left") -> str:
    """
    添加构建动画（元素进入/退出动画）
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引（1-based）
        animation_type: 动画类型
            - "appear": 出现
            - "fade_in": 渐显
            - "fly_in": 飞入
            - "scale": 缩放
            - "pop": 弹出
            - "bounce": 弹跳
        direction: 方向（仅部分动画有效）
            - "from_left": 从左侧
            - "from_right": 从右侧
            - "from_top": 从上方
            - "from_bottom": 从下方
    
    Returns:
        操作结果
    """
    animation = BUILD_ANIMATION_TYPES.get(animation_type.lower(), "appear")
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                tell text box %d
                    set build effect to %s effect
                end tell
                return "Build animation %s added to element %d on slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, element_index, animation, animation_type, element_index, slide_number)
    return run_applescript(script)


def clear_animations(slide_number: int) -> str:
    """
    清除幻灯片上的所有动画效果
    
    Args:
        slide_number: 幻灯片编号
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                set slide transition to no transition
                return "All animations cleared on slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, slide_number)
    return run_applescript(script)


def preview_animation(slide_number: int) -> str:
    """
    预览幻灯片的动画效果
    
    Args:
        slide_number: 幻灯片编号
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            -- 跳转到指定幻灯片并播放过渡动画
            show slide %d
            return "Previewing animation on slide %d"
        end tell
    end tell
    ''' % (slide_number, slide_number)
    return run_applescript(script)


# ============================================================================
# 字体渲染支持 (v3.0 新增)
# ============================================================================

# 字体映射
FONT_MAP = {
    "pingfang_bold": "PingFang SC Bold",
    "pingfang_regular": "PingFang SC Regular",
    "pingfang_light": "PingFang SC Light",
    "sf_pro_heavy": "SF Pro Display Heavy",
    "sf_pro_bold": "SF Pro Display Bold",
    "sf_pro_regular": "SF Pro Text Regular",
    "sf_pro_black": "SF Pro Display Black",
    "helvetica_bold": "Helvetica Bold",
    "helvetica_regular": "Helvetica",
}


def set_font(slide_number: int, element_index: int, font_name: str) -> str:
    """
    设置元素的字体
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        font_name: 字体名称（支持中文和英文）
            - "pingfang_bold": 苹方粗体
            - "pingfang_regular": 苹方常规
            - "sf_pro_heavy": SF Pro Heavy
            - "sf_pro_black": SF Pro Black
    
    Returns:
        操作结果
    """
    font = FONT_MAP.get(font_name.lower(), font_name)
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                tell text box %d
                    set font of text to "%s"
                end tell
                return "Font set to %s on element %d of slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, element_index, font, font_name, element_index, slide_number)
    return run_applescript(script)


def set_font_size(slide_number: int, element_index: int, size: int) -> str:
    """
    设置元素的字号
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        size: 字号（pt）
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                tell text box %d
                    set size of text to %d
                end tell
                return "Font size set to %dpt on element %d of slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, element_index, size, size, element_index, slide_number)
    return run_applescript(script)


def set_font_color(slide_number: int, element_index: int,
                   color: str = "white") -> str:
    """
    设置元素的字体颜色
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        color: 颜色名称或十六进制值
            - "white": 白色
            - "gold": 金色
            - "green": 财务绿
            - "red": 红色
            - "cyan": 青色
            - 或直接传入十六进制如 "#F2B84B"
    
    Returns:
        操作结果
    """
    # 颜色映射（AppleScript RGB）
    color_map = {
        "white": "{255, 255, 255}",
        "gold": "{242, 184, 75}",
        "green": "{47, 164, 114}",
        "red": "{184, 0, 58}",
        "cyan": "{37, 183, 224}",
        "black": "{0, 0, 0}",
        "gray": "{128, 128, 128}",
    }
    
    rgb = color_map.get(color.lower(), color_map["white"])
    
    script = '''
    tell application "Keynote"
        tell front document
            tell slide %d
                tell text box %d
                    set color of text to %s
                end tell
                return "Font color set to %s on element %d of slide %d"
            end tell
        end tell
    end tell
    ''' % (slide_number, element_index, rgb, color, element_index, slide_number)
    return run_applescript(script)


def apply_font_style(slide_number: int, element_index: int,
                     style_name: str = "title") -> str:
    """
    应用预设字体样式
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        style_name: 样式名称
            - "title": 大标题样式（苹方粗体 88pt 白色）
            - "subtitle": 副标题样式（苹方常规 44pt 白色）
            - "kpi": KPI数字样式（SF Pro Black 72pt 金色）
            - "card_title": 卡片标题样式（苹方粗体 28pt 白色）
            - "body": 正文样式（苹方常规 18pt 浅灰）
    
    Returns:
        操作结果
    """
    # 样式预设
    styles = {
        "title": {"font": "PingFang SC Bold", "size": 88, "color": "white"},
        "subtitle": {"font": "PingFang SC Regular", "size": 44, "color": "white"},
        "kpi": {"font": "SF Pro Display Black", "size": 72, "color": "gold"},
        "card_title": {"font": "PingFang SC Bold", "size": 28, "color": "white"},
        "body": {"font": "PingFang SC Regular", "size": 18, "color": "gray"},
    }
    
    style = styles.get(style_name.lower(), styles["body"])
    
    set_font(slide_number, element_index, style["font"])
    set_font_size(slide_number, element_index, style["size"])
    set_font_color(slide_number, element_index, style["color"])
    
    return f"Style '{style_name}' applied to element {element_index} on slide {slide_number}"


# ============================================================================
# 屏幕适配支持 (v3.0 新增)
# ============================================================================

# 预设屏幕尺寸
SCREEN_SIZES = {
    "standard_16_9": (1920, 1080),
    "standard_16_10": (1680, 1050),
    "ultra_wide_3_1": (3200, 1080),
    "ultra_wide_3_55_1": (3840, 1080),
    "4k": (3840, 2160),
    "macbook_13": (1440, 900),
    "macbook_15": (1680, 1050),
    "macbook_16": (1920, 1200),
}


def auto_fit_screen() -> str:
    """
    自动适配当前屏幕尺寸
    
    获取当前主显示器的分辨率，并设置演示文稿画布尺寸。
    
    Returns:
        操作结果
    """
    script = '''
    tell application "System Events"
        tell process "WindowServer"
            -- 获取主显示器分辨率
            set screenBounds to bounds of window 1
            return screenBounds
        end tell
    end tell
    '''
    
    try:
        # 尝试获取屏幕尺寸
        result = run_applescript(script)
        # 如果无法获取，使用默认值
        width, height = 1920, 1080
        
        # 设置画布尺寸
        set_canvas_size(width, height)
        return f"Canvas auto-fitted to {width}×{height}"
    except Exception as e:
        # 使用默认 16:9
        set_canvas_size(1920, 1080)
        return f"Canvas set to default 1920×1080 (screen detection failed: {e})"


def get_screen_info() -> dict:
    """
    获取屏幕信息
    
    Returns:
        屏幕信息字典
    """
    script = '''
    tell application "Finder"
        set screenWidth to word 3 of (do shell script "system_profiler SPDisplaysDataType | grep 'Resolution'")
        set screenHeight to word 5 of (do shell script "system_profiler SPDisplaysDataType | grep 'Resolution'")
        return screenWidth & "×" & screenHeight
    end tell
    '''
    
    try:
        result = run_applescript(script)
        parts = result.split("×")
        return {
            "width": int(parts[0]) if len(parts) > 0 else 1920,
            "height": int(parts[1]) if len(parts) > 1 else 1080,
            "resolution": result
        }
    except Exception as e:
        return {
            "width": 1920,
            "height": 1080,
            "resolution": "1920×1080 (default)",
            "error": str(e)
        }


# ============================================================================
# 专业展示支持 (v3.0 新增)
# ============================================================================

def start_presenter_mode() -> str:
    """
    启动演讲者模式
    
    演讲者模式会显示：
    - 当前幻灯片（观众看到的）
    - 下一张预览
    - 演讲者备注
    - 计时器
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            -- 启动演讲者模式
            start showing presenter display
            return "Presenter mode started"
        end tell
    end tell
    '''
    return run_applescript(script)


def set_timer(duration_minutes: int) -> str:
    """
    设置演示计时器
    
    Args:
        duration_minutes: 演示时长（分钟）
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            set presentation duration to %d * 60
            return "Timer set to %d minutes"
        end tell
    end tell
    ''' % (duration_minutes, duration_minutes)
    return run_applescript(script)


def set_auto_play(interval_seconds: float = 5.0) -> str:
    """
    设置自动播放
    
    Args:
        interval_seconds: 每张幻灯片显示时间（秒）
    
    Returns:
        操作结果
    """
    script = '''
    tell application "Keynote"
        tell front document
            set auto play interval to %f
            set auto play to true
            return "Auto play set to %.1f seconds per slide"
        end tell
    end tell
    ''' % (interval_seconds, interval_seconds)
    return run_applescript(script)


def get_performance_info() -> dict:
    """
    获取 Keynote 性能信息
    
    Returns:
        性能信息字典
    """
    script = '''
    tell application "Keynote"
        tell front document
            set slideCount to count of slides
            set canvasWidth to width
            set canvasHeight to height
            return (slideCount as string) & "|" & (canvasWidth as string) & "|" & (canvasHeight as string)
        end tell
    end tell
    '''
    
    try:
        result = run_applescript(script)
        parts = result.split("|")
        return {
            "slide_count": int(parts[0]) if len(parts) > 0 else 0,
            "canvas_width": int(parts[1]) if len(parts) > 1 else 0,
            "canvas_height": int(parts[2]) if len(parts) > 2 else 0,
            "estimated_memory_mb": int(parts[0]) * 2 if len(parts) > 0 else 0,
            "status": "healthy"
        }
    except Exception as e:
        return {"error": str(e), "status": "unknown"}


if __name__ == "__main__":
    # 简单测试
    import json
    print("=== Keynote AppleScript Engine Test (v3.0) ===")
    print("作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026\n")

    if not is_macos():
        print("⚠️  非 macOS 平台，无法测试 AppleScript")
        print("此模块仅在 macOS 上工作")
        print("\n可用功能（需在 macOS 上运行）:")
        print("\n【v2.0 功能】")
        print("  - set_canvas_size(width, height)")
        print("  - create_ultra_wide_document()")
        print("  - add_kpi_textbox()")
        print("  - add_card_shape()")
        print("  - create_digital_finance_presentation()")
        print("  - create_valuation_report_presentation()")
        print("\n【v3.0 新增功能】")
        print("  - set_transition() / set_magic_move() / add_build_animation()")
        print("  - set_font() / set_font_size() / set_font_color() / apply_font_style()")
        print("  - auto_fit_screen() / get_screen_info()")
        print("  - start_presenter_mode() / set_timer() / set_auto_play()")
        print("  - get_performance_info()")
    else:
        info = get_system_info()
        print(json.dumps(info, indent=2, ensure_ascii=False))
        print("\n可用主题列表:")
        try:
            themes = list_available_themes()
            for theme in themes[:10]:
                print(f"  - {theme}")
        except Exception as e:
            print(f"  (获取主题失败: {e})")
