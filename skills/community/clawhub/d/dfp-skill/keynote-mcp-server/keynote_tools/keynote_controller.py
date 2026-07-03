"""
keynote_tools/keynote_controller.py

Keynote 高层控制器

作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

提供更友好、更高级的 API，供 MCP Server 调用。
封装底层的 AppleScript 操作，提供：
    - 结构化的输入/输出
    - 错误处理与友好提示
    - 批量操作
    - 常见场景的快速方法

新增功能 (v2.0):
    - set_canvas_size() - 设置画布尺寸（含超宽屏）
    - create_ultra_wide_presentation() - 创建超宽屏演示文稿
    - add_kpi_slide() - 添加 KPI 数字展示幻灯片
    - create_digital_finance_presentation() - 创建数智财务风格演示
    - create_valuation_report() - 创建上市公司估值报告

依赖: keynote_tools.applescript（底层 AppleScript 执行）
"""

import os
import json
from typing import Optional, List, Dict, Any, Union

from . import applescript


# ============================================================================
# 异常处理
# ============================================================================

class KeynoteError(Exception):
    """Keynote 操作异常"""
    pass


class KeynoteNotAvailableError(KeynoteError):
    """Keynote 不可用（非 macOS / 未安装）"""
    pass


class KeynoteNotRunningError(KeynoteError):
    """Keynote 未运行"""
    pass


class AppleScriptError(KeynoteError):
    """AppleScript 执行错误"""
    pass


# ============================================================================
# 环境检测工具
# ============================================================================

def check_environment() -> Dict[str, Any]:
    """
    检查运行环境

    Returns:
        环境信息字典
    """
    info = applescript.get_system_info()
    return info


def ensure_keynote_ready() -> bool:
    """
    确保 Keynote 已准备好

    如果未运行则启动 Keynote。
    """
    if not applescript.is_macos():
        raise KeynoteNotAvailableError(
            "此 MCP Server 仅在 macOS 上运行。"
        )

    if not applescript.is_keynote_installed():
        raise KeynoteNotAvailableError(
            "未检测到 Keynote.app，请从 App Store 安装。"
        )

    if not applescript.is_keynote_running():
        try:
            applescript.activate_keynote()
            import time
            time.sleep(1)  # 等待 Keynote 启动
        except Exception as e:
            raise KeynoteNotAvailableError(
                f"启动 Keynote 失败: {e}"
            )

    return True


# ============================================================================
# 文档操作（高层 API）
# ============================================================================

def create_presentation(title: Optional[str] = None,
                       theme: Optional[str] = None) -> Dict[str, Any]:
    """
    创建新的 Keynote 演示文稿

    Args:
        title: 第一张幻灯片的标题（可选）
        theme: 主题名称（可选，例如 "White"、"Black"、"Gradient" 等）

    Returns:
        操作结果字典
    """
    ensure_keynote_ready()

    try:
        if theme:
            applescript.create_new_document_with_theme(theme)
        else:
            applescript.create_new_document()

        # 如果提供了标题，设置第一张幻灯片的标题
        if title:
            applescript.set_slide_title(1, title)

        return {
            "status": "success",
            "action": "create_presentation",
            "message": "新文档已创建",
            "theme": theme or "默认",
            "slide_count": applescript.get_slide_count()
        }
    except Exception as e:
        raise KeynoteError(f"创建演示文稿失败: {e}")


def open_presentation(file_path: str) -> Dict[str, Any]:
    """
    打开现有的 .key 文件

    Args:
        file_path: .key 文件路径（支持 ~/ 缩写）

    Returns:
        操作结果字典
    """
    ensure_keynote_ready()

    expanded_path = os.path.expanduser(file_path)
    if not os.path.exists(expanded_path):
        raise KeynoteError(f"文件不存在: {file_path}")

    try:
        applescript.open_document(expanded_path)
        import time
        time.sleep(0.5)

        slide_count = applescript.get_slide_count()
        doc_info = applescript.get_document_info()

        return {
            "status": "success",
            "action": "open_presentation",
            "file_path": expanded_path,
            "slide_count": slide_count,
            "info": doc_info
        }
    except Exception as e:
        raise KeynoteError(f"打开演示文稿失败: {e}")


def save_presentation(file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    保存当前演示文稿

    Args:
        file_path: 另存为路径（可选）。不提供则原地保存。

    Returns:
        操作结果字典
    """
    ensure_keynote_ready()

    try:
        if file_path:
            expanded = os.path.expanduser(file_path)
            applescript.save_document_as(expanded)
            message = f"已另存为: {expanded}"
        else:
            applescript.save_document()
            message = "已保存"

        return {
            "status": "success",
            "action": "save",
            "message": message
        }
    except Exception as e:
        raise KeynoteError(f"保存失败: {e}")


def close_presentation(save: bool = True) -> Dict[str, Any]:
    """
    关闭当前演示文稿

    Args:
        save: 是否保存后再关闭
    """
    ensure_keynote_ready()

    try:
        if save:
            applescript.close_document_saving()
        else:
            applescript.close_document()

        return {
            "status": "success",
            "action": "close",
            "saved": save,
            "message": "文档已关闭"
        }
    except Exception as e:
        raise KeynoteError(f"关闭失败: {e}")


# ============================================================================
# 幻灯片操作（高层 API）
# ============================================================================

def add_slide(title: Optional[str] = None,
              body: Optional[str] = None,
              position: Optional[int] = None) -> Dict[str, Any]:
    """
    添加新幻灯片

    Args:
        title: 幻灯片标题（可选）
        body: 正文内容（可选）
        position: 插入位置，1-based（默认末尾）

    Returns:
        操作结果，包含新幻灯片编号
    """
    ensure_keynote_ready()

    try:
        current_count = applescript.get_slide_count()

        if position is None or position > current_count:
            applescript.add_slide()
            new_position = current_count + 1
        else:
            applescript.add_slide(position)
            new_position = position + 1

        # 填入内容
        if title:
            applescript.set_slide_title(new_position, title)
        if body:
            applescript.set_slide_body(new_position, body)

        return {
            "status": "success",
            "action": "add_slide",
            "new_slide_number": new_position,
            "title": title or "(未设置标题)",
            "total_slides": applescript.get_slide_count()
        }
    except Exception as e:
        raise KeynoteError(f"添加幻灯片失败: {e}")


def delete_slide(slide_number: int) -> Dict[str, Any]:
    """删除指定幻灯片"""
    ensure_keynote_ready()

    try:
        applescript.delete_slide(slide_number)
        return {
            "status": "success",
            "action": "delete_slide",
            "slide_number": slide_number,
            "remaining_slides": applescript.get_slide_count()
        }
    except Exception as e:
        raise KeynoteError(f"删除幻灯片失败: {e}")


def list_all_slides() -> Dict[str, Any]:
    """
    列出所有幻灯片信息

    Returns:
        包含幻灯片列表的字典
    """
    ensure_keynote_ready()

    try:
        slide_count = applescript.get_slide_count()
        titles = applescript.get_slide_titles()

        slides = []
        for i in range(1, slide_count + 1):
            slides.append({
                "slide_number": i,
                "title": titles[i - 1] if i <= len(titles) else "(无标题)"
            })

        return {
            "status": "success",
            "action": "list_slides",
            "total_slides": slide_count,
            "slides": slides
        }
    except Exception as e:
        raise KeynoteError(f"获取幻灯片列表失败: {e}")


# ============================================================================
# 内容编辑（高层 API）
# ============================================================================

def set_title(slide_number: int, text: str) -> Dict[str, Any]:
    """设置幻灯片标题"""
    ensure_keynote_ready()

    try:
        applescript.set_slide_title(slide_number, text)
        return {
            "status": "success",
            "action": "set_title",
            "slide_number": slide_number,
            "title": text
        }
    except Exception as e:
        raise KeynoteError(f"设置标题失败: {e}")


def set_body(slide_number: int, text: str) -> Dict[str, Any]:
    """设置幻灯片正文"""
    ensure_keynote_ready()

    try:
        applescript.set_slide_body(slide_number, text)
        return {
            "status": "success",
            "action": "set_body",
            "slide_number": slide_number
        }
    except Exception as e:
        raise KeynoteError(f"设置正文失败: {e}")


def add_textbox(slide_number: int, text: str,
                left: int = 100, top: int = 100,
                width: int = 400, height: int = 100) -> Dict[str, Any]:
    """添加文本框到幻灯片"""
    ensure_keynote_ready()

    try:
        applescript.add_textbox(slide_number, text, left, top, width, height)
        return {
            "status": "success",
            "action": "add_textbox",
            "slide_number": slide_number,
            "text": text[:50] + "..." if len(text) > 50 else text,
            "position": {"left": left, "top": top},
            "size": {"width": width, "height": height}
        }
    except Exception as e:
        raise KeynoteError(f"添加文本框失败: {e}")


def add_image(slide_number: int, image_path: str,
              left: int = 100, top: int = 100,
              width: int = 400, height: int = 300) -> Dict[str, Any]:
    """添加图片到幻灯片"""
    ensure_keynote_ready()

    expanded = os.path.expanduser(image_path)
    if not os.path.exists(expanded):
        raise KeynoteError(f"图片不存在: {image_path}")

    try:
        applescript.add_image(slide_number, expanded, left, top, width, height)
        return {
            "status": "success",
            "action": "add_image",
            "slide_number": slide_number,
            "image_path": expanded,
            "position": {"left": left, "top": top},
            "size": {"width": width, "height": height}
        }
    except Exception as e:
        raise KeynoteError(f"添加图片失败: {e}")


# ============================================================================
# 演示控制（高层 API）
# ============================================================================

def start_show() -> Dict[str, Any]:
    """开始播放演示文稿"""
    ensure_keynote_ready()

    try:
        applescript.start_slideshow()
        return {
            "status": "success",
            "action": "start_show",
            "message": "开始播放"
        }
    except Exception as e:
        raise KeynoteError(f"播放失败: {e}")


def stop_show() -> Dict[str, Any]:
    """停止播放"""
    ensure_keynote_ready()

    try:
        applescript.stop_slideshow()
        return {
            "status": "success",
            "action": "stop_show",
            "message": "已停止"
        }
    except Exception as e:
        raise KeynoteError(f"停止播放失败: {e}")


def next_slide() -> Dict[str, Any]:
    """切换到下一张幻灯片"""
    ensure_keynote_ready()

    try:
        applescript.next_slide()
        return {
            "status": "success",
            "action": "next_slide",
            "message": "下一张"
        }
    except Exception as e:
        raise KeynoteError(f"切换幻灯片失败: {e}")


def previous_slide() -> Dict[str, Any]:
    """切换到上一张幻灯片"""
    ensure_keynote_ready()

    try:
        applescript.previous_slide()
        return {
            "status": "success",
            "action": "previous_slide",
            "message": "上一张"
        }
    except Exception as e:
        raise KeynoteError(f"切换幻灯片失败: {e}")


def go_to_slide(slide_number: int) -> Dict[str, Any]:
    """跳转到指定幻灯片"""
    ensure_keynote_ready()

    try:
        applescript.go_to_slide(slide_number)
        return {
            "status": "success",
            "action": "go_to_slide",
            "slide_number": slide_number
        }
    except Exception as e:
        raise KeynoteError(f"跳转失败: {e}")


# ============================================================================
# 查询与导出（高层 API）
# ============================================================================

def get_info() -> Dict[str, Any]:
    """获取当前文档信息"""
    ensure_keynote_ready()

    try:
        slide_count = applescript.get_slide_count()
        doc_info = applescript.get_document_info()

        return {
            "status": "success",
            "action": "get_info",
            "slide_count": slide_count,
            "document_info": doc_info,
            "keynote_running": True
        }
    except Exception as e:
        return {
            "status": "error",
            "action": "get_info",
            "error": str(e)
        }


def get_slide(slide_number: int) -> Dict[str, Any]:
    """获取指定幻灯片的完整内容"""
    ensure_keynote_ready()

    try:
        content = applescript.get_slide_content(slide_number)
        return {
            "status": "success",
            "action": "get_slide",
            "content": content
        }
    except Exception as e:
        raise KeynoteError(f"获取幻灯片内容失败: {e}")


def export_document(format_type: str, output_path: str) -> Dict[str, Any]:
    """
    导出文档

    Args:
        format_type: "pdf"、"pptx"、"mov"、"html"
        output_path: 输出文件路径
    """
    ensure_keynote_ready()

    fmt = format_type.lower()
    valid_formats = ["pdf", "pptx", "mov", "html"]
    if fmt not in valid_formats:
        raise KeynoteError(
            f"不支持的导出格式: {format_type}。可用: {', '.join(valid_formats)}"
        )

    expanded = os.path.expanduser(output_path)

    try:
        if fmt == "pdf":
            applescript.export_to_pdf(expanded)
        elif fmt == "pptx":
            applescript.export_to_pptx(expanded)
        elif fmt == "mov":
            applescript.export_to_movie(expanded)
        elif fmt == "html":
            applescript.export_to_html(expanded)

        return {
            "status": "success",
            "action": "export",
            "format": fmt,
            "output_path": expanded
        }
    except Exception as e:
        raise KeynoteError(f"导出失败: {e}")


# ============================================================================
# 列表查询工具
# ============================================================================

def get_themes() -> Dict[str, Any]:
    """获取可用主题列表"""
    if not applescript.is_macos():
        return {
            "status": "error",
            "action": "get_themes",
            "error": "非 macOS 平台"
        }

    try:
        themes = applescript.list_available_themes()
        return {
            "status": "success",
            "action": "get_themes",
            "themes": themes,
            "count": len(themes)
        }
    except Exception as e:
        return {
            "status": "error",
            "action": "get_themes",
            "error": str(e)
        }


def get_masters() -> Dict[str, Any]:
    """获取当前文档的母版/布局列表"""
    ensure_keynote_ready()

    try:
        masters = applescript.list_master_slides()
        return {
            "status": "success",
            "action": "get_masters",
            "master_slides": masters,
            "count": len(masters)
        }
    except Exception as e:
        return {
            "status": "error",
            "action": "get_masters",
            "error": str(e)
        }


# ============================================================================
# 高级：场景化批量操作
# ============================================================================

def create_launch_event_presentation(
    event_title: str,
    slides: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    创建一个完整的发布会演示文稿（场景化 API）

    Args:
        event_title: 发布会标题
        slides: 幻灯片列表，每项包含 title 和 body 字段

    示例:
        create_launch_event_presentation(
            "2026 春季新品发布",
            [
                {"title": "今日议程", "body": "产品愿景 / 核心亮点 / ..."},
                {"title": "产品愿景", "body": "..."},
                ...
            ]
        )
    """
    ensure_keynote_ready()

    try:
        # 创建新文档
        applescript.create_new_document()

        # 设置第一张为封面
        applescript.set_slide_title(1, event_title)
        applescript.set_slide_body(1, "发布会")

        # 添加其他幻灯片
        for i, slide_data in enumerate(slides, 2):
            title = slide_data.get("title", "")
            body = slide_data.get("body", "")

            applescript.add_slide()
            applescript.set_slide_title_and_body(i, title, body)

        slide_count = applescript.get_slide_count()

        return {
            "status": "success",
            "action": "create_launch_event",
            "event_title": event_title,
            "total_slides": slide_count,
            "message": f"已创建 {slide_count} 张幻灯片"
        }
    except Exception as e:
        raise KeynoteError(f"创建发布会演示文稿失败: {e}")


# ============================================================================
# 工具函数
# ============================================================================

def format_result(result: Dict[str, Any]) -> str:
    """
    将结果字典格式化为人类可读的字符串

    用于 MCP tool 返回值
    """
    lines = []
    for key, value in result.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {sub_value}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value[:20]:  # 限制列表长度
                if isinstance(item, dict):
                    lines.append(f"  - {json.dumps(item, ensure_ascii=False)}")
                else:
                    lines.append(f"  - {item}")
            if len(value) > 20:
                lines.append(f"  ... (共 {len(value)} 项)")
        else:
            lines.append(f"{key}: {value}")

    return "\n".join(lines)


def get_keynote_status() -> Dict[str, Any]:
    """获取 Keynote 的运行状态"""
    if not applescript.is_macos():
        return {
            "status": "unavailable",
            "platform": applescript.platform.system(),
            "message": "Keynote MCP Server 仅在 macOS 上工作"
        }

    return {
        "status": "ready" if applescript.is_keynote_running() else "not_running",
        "platform": "macOS",
        "version": applescript.platform.mac_ver()[0],
        "keynote_installed": applescript.is_keynote_installed(),
        "keynote_running": applescript.is_keynote_running()
    }


# ============================================================================
# 超宽屏与数智财务风格 (v2.0 新增)
# ============================================================================

def set_canvas_size(width: int, height: int) -> Dict[str, Any]:
    """
    设置当前文档的画布尺寸
    
    Args:
        width: 宽度（像素）
        height: 高度（像素）
    
    常用尺寸:
        - 标准 16:9: 1920 × 1080
        - 超宽屏 3:1: 3200 × 1080
        - 超宽屏 3.55:1: 3840 × 1080
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_canvas_size(width, height)
        return {
            "status": "success",
            "action": "set_canvas_size",
            "width": width,
            "height": height,
            "message": f"画布尺寸已设置为 {width} × {height}"
        }
    except Exception as e:
        raise KeynoteError(f"设置画布尺寸失败: {e}")


def create_ultra_wide_presentation(title: str = "",
                                   theme: str = "Black") -> Dict[str, Any]:
    """
    创建超宽屏演示文稿（3:1 比例，3200×1080）
    
    Args:
        title: 封面标题（可选）
        theme: 主题名称（默认 Black 深色主题）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.create_ultra_wide_document(theme)
        
        if title:
            applescript.set_slide_title(1, title)
        
        canvas = applescript.get_canvas_size()
        
        return {
            "status": "success",
            "action": "create_ultra_wide",
            "title": title or "(未设置标题)",
            "theme": theme,
            "canvas_size": canvas,
            "slide_count": applescript.get_slide_count(),
            "message": "超宽屏演示文稿已创建"
        }
    except Exception as e:
        raise KeynoteError(f"创建超宽屏演示文稿失败: {e}")


def add_kpi_slide(title: str, kpi_items: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    添加 KPI 数字展示幻灯片
    
    Args:
        title: 幻灯片标题
        kpi_items: KPI 数据列表，每项包含:
            - number: 数字（如 "¥2.42"）
            - label: 标签（如 "当前股价"）
            - color: 颜色（可选："gold", "green", "red", "white"）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        # 添加新幻灯片
        applescript.add_slide()
        slide_number = applescript.get_slide_count()
        
        # 设置标题
        applescript.set_slide_title(slide_number, title)
        
        # 添加 KPI 文本框
        for i, kpi in enumerate(kpi_items[:5]):
            number = kpi.get("number", "")
            label = kpi.get("label", "")
            color = kpi.get("color", "gold")
            
            applescript.add_kpi_textbox(
                slide_number, number, label,
                left=100 + i * 600, top=200,
                number_color=color
            )
        
        return {
            "status": "success",
            "action": "add_kpi_slide",
            "slide_number": slide_number,
            "title": title,
            "kpi_count": len(kpi_items),
            "message": f"已添加 KPI 幻灯片，包含 {len(kpi_items)} 个指标"
        }
    except Exception as e:
        raise KeynoteError(f"添加 KPI 幻灯片失败: {e}")


def create_digital_finance_presentation(
    title: str,
    slides_data: List[Dict[str, Any]],
    save_path: Optional[str] = None
) -> Dict[str, Any]:
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
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        result = applescript.create_digital_finance_presentation(
            title, slides_data, save_path
        )
        
        return {
            "status": "success",
            "action": "create_digital_finance",
            "title": title,
            "slide_count": applescript.get_slide_count(),
            "canvas_size": applescript.get_canvas_size(),
            "save_path": save_path,
            "message": result
        }
    except Exception as e:
        raise KeynoteError(f"创建数智财务演示文稿失败: {e}")


def create_valuation_report(
    stock_code: str,
    company_name: str,
    kpi_data: Dict[str, str],
    financial_data: Dict[str, str],
    save_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建上市公司估值报告演示文稿（13页标准结构）
    
    Args:
        stock_code: 股票代码（如 "600170"）
        company_name: 公司名称
        kpi_data: 核心 KPI 数据字典（price, market_cap, pe, pb, dividend_yield）
        financial_data: 财务数据字典（revenue, net_profit, roe）
        save_path: 保存路径（可选）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        result = applescript.create_valuation_report_presentation(
            stock_code, company_name, kpi_data, financial_data, save_path
        )
        
        return {
            "status": "success",
            "action": "create_valuation_report",
            "stock_code": stock_code,
            "company_name": company_name,
            "slide_count": applescript.get_slide_count(),
            "canvas_size": applescript.get_canvas_size(),
            "save_path": save_path,
            "message": result
        }
    except Exception as e:
        raise KeynoteError(f"创建估值报告失败: {e}")


def get_canvas_info() -> Dict[str, Any]:
    """获取当前文档画布信息"""
    ensure_keynote_ready()
    
    try:
        canvas = applescript.get_canvas_size()
        return {
            "status": "success",
            "action": "get_canvas_info",
            "canvas": canvas
        }
    except Exception as e:
        raise KeynoteError(f"获取画布信息失败: {e}")


# ============================================================================
# 动画效果控制 (v3.0 新增)
# ============================================================================

def set_transition(slide_number: int, transition_type: str = "fade") -> Dict[str, Any]:
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
    ensure_keynote_ready()
    
    try:
        applescript.set_transition(slide_number, transition_type)
        return {
            "status": "success",
            "action": "set_transition",
            "slide_number": slide_number,
            "transition_type": transition_type,
            "message": f"过渡动画 '{transition_type}' 已设置到幻灯片 {slide_number}"
        }
    except Exception as e:
        raise KeynoteError(f"设置过渡动画失败: {e}")


def set_magic_move(from_slide: int, to_slide: int) -> Dict[str, Any]:
    """
    设置 Magic Move 神奇移动效果
    
    Magic Move 是 Keynote 最强大的动画效果，可以自动匹配两张幻灯片
    中的相同元素，并创建平滑的过渡动画。
    
    Args:
        from_slide: 起始幻灯片编号
        to_slide: 目标幻灯片编号
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_magic_move(from_slide, to_slide)
        return {
            "status": "success",
            "action": "set_magic_move",
            "from_slide": from_slide,
            "to_slide": to_slide,
            "message": f"Magic Move 已设置，从幻灯片 {from_slide} 到 {to_slide}"
        }
    except Exception as e:
        raise KeynoteError(f"设置 Magic Move 失败: {e}")


def add_build_animation(slide_number: int, element_index: int,
                        animation_type: str = "appear") -> Dict[str, Any]:
    """
    添加构建动画（元素进入动画）
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        animation_type: 动画类型
            - "appear": 出现
            - "fade_in": 渐显
            - "fly_in": 飞入
            - "scale": 缩放
            - "pop": 弹出
            - "bounce": 弹跳
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.add_build_animation(slide_number, element_index, animation_type)
        return {
            "status": "success",
            "action": "add_build_animation",
            "slide_number": slide_number,
            "element_index": element_index,
            "animation_type": animation_type,
            "message": f"构建动画 '{animation_type}' 已添加到元素 {element_index}"
        }
    except Exception as e:
        raise KeynoteError(f"添加构建动画失败: {e}")


def clear_animations(slide_number: int) -> Dict[str, Any]:
    """
    清除幻灯片上的所有动画效果
    
    Args:
        slide_number: 幻灯片编号
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.clear_animations(slide_number)
        return {
            "status": "success",
            "action": "clear_animations",
            "slide_number": slide_number,
            "message": f"幻灯片 {slide_number} 的所有动画已清除"
        }
    except Exception as e:
        raise KeynoteError(f"清除动画失败: {e}")


def preview_animation(slide_number: int) -> Dict[str, Any]:
    """
    预览幻灯片的动画效果
    
    Args:
        slide_number: 幻灯片编号
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.preview_animation(slide_number)
        return {
            "status": "success",
            "action": "preview_animation",
            "slide_number": slide_number,
            "message": f"正在预览幻灯片 {slide_number} 的动画效果"
        }
    except Exception as e:
        raise KeynoteError(f"预览动画失败: {e}")


# ============================================================================
# 字体渲染控制 (v3.0 新增)
# ============================================================================

def set_font(slide_number: int, element_index: int, font_name: str) -> Dict[str, Any]:
    """
    设置元素的字体
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        font_name: 字体名称
            - "pingfang_bold": 苹方粗体
            - "pingfang_regular": 苹方常规
            - "sf_pro_heavy": SF Pro Heavy
            - "sf_pro_black": SF Pro Black
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_font(slide_number, element_index, font_name)
        return {
            "status": "success",
            "action": "set_font",
            "slide_number": slide_number,
            "element_index": element_index,
            "font_name": font_name,
            "message": f"字体 '{font_name}' 已应用到元素 {element_index}"
        }
    except Exception as e:
        raise KeynoteError(f"设置字体失败: {e}")


def set_font_size(slide_number: int, element_index: int, size: int) -> Dict[str, Any]:
    """
    设置元素的字号
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        size: 字号（pt）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_font_size(slide_number, element_index, size)
        return {
            "status": "success",
            "action": "set_font_size",
            "slide_number": slide_number,
            "element_index": element_index,
            "font_size": size,
            "message": f"字号 {size}pt 已应用到元素 {element_index}"
        }
    except Exception as e:
        raise KeynoteError(f"设置字号失败: {e}")


def set_font_color(slide_number: int, element_index: int, color: str) -> Dict[str, Any]:
    """
    设置元素的字体颜色
    
    Args:
        slide_number: 幻灯片编号
        element_index: 元素索引
        color: 颜色名称
            - "white": 白色
            - "gold": 金色
            - "green": 财务绿
            - "red": 红色
            - "cyan": 青色
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_font_color(slide_number, element_index, color)
        return {
            "status": "success",
            "action": "set_font_color",
            "slide_number": slide_number,
            "element_index": element_index,
            "font_color": color,
            "message": f"颜色 '{color}' 已应用到元素 {element_index}"
        }
    except Exception as e:
        raise KeynoteError(f"设置颜色失败: {e}")


def apply_font_style(slide_number: int, element_index: int,
                     style_name: str = "title") -> Dict[str, Any]:
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
    ensure_keynote_ready()
    
    try:
        applescript.apply_font_style(slide_number, element_index, style_name)
        return {
            "status": "success",
            "action": "apply_font_style",
            "slide_number": slide_number,
            "element_index": element_index,
            "style_name": style_name,
            "message": f"样式 '{style_name}' 已应用到元素 {element_index}"
        }
    except Exception as e:
        raise KeynoteError(f"应用样式失败: {e}")


# ============================================================================
# 屏幕适配控制 (v3.0 新增)
# ============================================================================

def auto_fit_screen() -> Dict[str, Any]:
    """
    自动适配当前屏幕尺寸
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        result = applescript.auto_fit_screen()
        screen_info = applescript.get_screen_info()
        return {
            "status": "success",
            "action": "auto_fit_screen",
            "screen_info": screen_info,
            "message": result
        }
    except Exception as e:
        raise KeynoteError(f"自动适配屏幕失败: {e}")


def get_screen_info() -> Dict[str, Any]:
    """
    获取屏幕信息
    
    Returns:
        屏幕信息
    """
    ensure_keynote_ready()
    
    try:
        screen_info = applescript.get_screen_info()
        return {
            "status": "success",
            "action": "get_screen_info",
            "screen": screen_info
        }
    except Exception as e:
        raise KeynoteError(f"获取屏幕信息失败: {e}")


# ============================================================================
# 专业展示控制 (v3.0 新增)
# ============================================================================

def start_presenter_mode() -> Dict[str, Any]:
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
    ensure_keynote_ready()
    
    try:
        applescript.start_presenter_mode()
        return {
            "status": "success",
            "action": "start_presenter_mode",
            "message": "演讲者模式已启动"
        }
    except Exception as e:
        raise KeynoteError(f"启动演讲者模式失败: {e}")


def set_timer(duration_minutes: int) -> Dict[str, Any]:
    """
    设置演示计时器
    
    Args:
        duration_minutes: 演示时长（分钟）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_timer(duration_minutes)
        return {
            "status": "success",
            "action": "set_timer",
            "duration_minutes": duration_minutes,
            "message": f"计时器已设置为 {duration_minutes} 分钟"
        }
    except Exception as e:
        raise KeynoteError(f"设置计时器失败: {e}")


def set_auto_play(interval_seconds: float = 5.0) -> Dict[str, Any]:
    """
    设置自动播放
    
    Args:
        interval_seconds: 每张幻灯片显示时间（秒）
    
    Returns:
        操作结果
    """
    ensure_keynote_ready()
    
    try:
        applescript.set_auto_play(interval_seconds)
        return {
            "status": "success",
            "action": "set_auto_play",
            "interval_seconds": interval_seconds,
            "message": f"自动播放已设置为 {interval_seconds} 秒/张"
        }
    except Exception as e:
        raise KeynoteError(f"设置自动播放失败: {e}")


def get_performance_info() -> Dict[str, Any]:
    """
    获取 Keynote 性能信息
    
    Returns:
        性能信息
    """
    ensure_keynote_ready()
    
    try:
        perf_info = applescript.get_performance_info()
        return {
            "status": "success",
            "action": "get_performance_info",
            "performance": perf_info
        }
    except Exception as e:
        raise KeynoteError(f"获取性能信息失败: {e}")


if __name__ == "__main__":
    # 简单的本地测试
    print("=== Keynote Controller 测试 (v3.0) ===")
    print("作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026\n")
    status = get_keynote_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    if status.get("status") == "ready" or status.get("status") == "not_running":
        print("\n注意: 仅在 macOS 上可以实际操作 Keynote")
        print("\n【v2.0 功能】")
        print("  - set_canvas_size(width, height)")
        print("  - create_ultra_wide_presentation()")
        print("  - add_kpi_slide()")
        print("  - create_digital_finance_presentation()")
        print("  - create_valuation_report()")
        print("\n【v3.0 新增功能】")
        print("  - set_transition() / set_magic_move() / add_build_animation()")
        print("  - set_font() / set_font_size() / set_font_color() / apply_font_style()")
        print("  - auto_fit_screen() / get_screen_info()")
        print("  - start_presenter_mode() / set_timer() / set_auto_play()")
        print("  - get_performance_info()")
