#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DFP-Skill Keynote MCP Server (v6.0)

Author: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

Model Context Protocol (MCP) Server for direct Keynote control on macOS.
Generates native .key files with professional features.

SAP Digital Finance Methodology (v6.0):
- 51年技术演进: ERP → HANA → Business AI (AI驱动端到端业务流程)
- Joule: SAP生成式AI数字助手 (真正了解您的业务)
- RPA: 93.75%效率提升案例 (供应商发票校验流程)
- ESG碳资产管理: 碳数据 → 碳资产 → 碳资本
- 数智财务四大能力: 利润/收入/资金/应收穿透分析

Keynote Professional Advantages (v5.0):
- Screen Adaptation: Ultra-wide 3:1 canvas, auto-fit to display
- Animation Effects: Magic Move, transitions, build animations
- Design Superiority: 40+ themes, master slides, smart layout
- Stability: Native AppleScript, error recovery, timeout protection
- Visual Rendering: Core Animation, Metal engine, Retina support
- Performance: Fast startup, smooth transitions, low memory
- Font Rendering: PingFang SC, SF Pro, Retina clarity
- Professional Presentation: Presenter mode, timer, MOV export

MCP Tools (35+):
- Document: keynote_create, keynote_create_valuation_report
- 数智财务: keynote_create_digital_finance_report (v6.0)
- ESG报告: keynote_create_esg_report (v6.0)
- RPA案例: keynote_create_rpa_case_report (v6.0)
- Animation: keynote_set_magic_move, keynote_set_transition
- Font: keynote_set_font, keynote_apply_font_style
- Presentation: keynote_start_presenter_mode, keynote_export

Usage:
    Configure MCP connection in claude_desktop_config.json
    Then call Keynote directly via AI

Dependencies:
    pip install "mcp[cli]"
"""

import sys
import json
import time
from pathlib import Path

# 添加包路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from keynote_tools import keynote_controller


# ============================================================================
# 尝试导入 FastMCP
# ============================================================================

try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


# ============================================================================
# 创建 MCP Server 实例
# ============================================================================

if MCP_AVAILABLE:
    mcp = FastMCP(
        "Keynote",
        instructions="""
        你是一个可以操作 macOS Keynote 的 AI 助手。
        你可以创建、编辑、播放和导出 Keynote 演示文稿。

        操作指南:
        1. 创建新文档使用 keynote_create
        2. 打开现有文档使用 keynote_open
        3. 添加幻灯片使用 keynote_add_slide
        4. 设置幻灯片标题使用 keynote_set_title
        5. 设置正文使用 keynote_set_body
        6. 查询信息使用 keynote_get_info 或 keynote_list_slides
        7. 控制演示播放使用 keynote_start_show / keynote_stop_show
        8. 导出使用 keynote_export

        注意事项:
        - 所有操作都针对当前激活的文档（front document）
        - 幻灯片编号从 1 开始
        - 操作前确保用户了解会打开/修改 Keynote
        - 创建多张幻灯片时，先创建文档，然后逐张添加
        - 所有路径可以使用 ~/ 表示用户目录
        """
    )
else:
    mcp = None  # 占位，用于非 macOS 环境测试


# ============================================================================
# 工具：环境与状态
# ============================================================================

if mcp:
    @mcp.tool()
    def keynote_check_status() -> str:
        """
        检查 Keynote 的运行状态。

        返回:
            当前平台信息、Keynote 是否安装/运行等状态信息
        """
        status = keynote_controller.get_keynote_status()
        result = "=== Keynote 状态 ===\n"
        for key, value in status.items():
            result += f"{key}: {value}\n"
        return result


# ============================================================================
# 工具：文档管理
# ============================================================================

    @mcp.tool()
    def keynote_create(title: str = "", theme: str = "") -> str:
        """
        创建一个新的 Keynote 演示文档。

        Args:
            title: 第一张（封面）幻灯片的标题，留空则使用默认
            theme: 主题名称，例如 "White"、"Black"、"Gradient"。
                   留空则使用默认主题。

        Returns:
            操作结果描述，包含幻灯片数量
        """
        try:
            result = keynote_controller.create_presentation(
                title=title or None,
                theme=theme or None
            )
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"创建失败: {e}"

    @mcp.tool()
    def keynote_open(file_path: str) -> str:
        """
        打开一个已有的 .key 文件。

        Args:
            file_path: .key 文件的完整路径，支持 ~/ 表示用户目录
                       例如: ~/Documents/发布会.key
                            /Users/name/Documents/demo.key

        Returns:
            文档信息，包括幻灯片数量等
        """
        try:
            result = keynote_controller.open_presentation(file_path)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"打开失败: {e}"

    @mcp.tool()
    def keynote_save(file_path: str = "") -> str:
        """
        保存当前文档。

        Args:
            file_path: 另存为新路径（可选，留空则原地保存）

        Returns:
            保存结果
        """
        try:
            result = keynote_controller.save_presentation(
                file_path=file_path or None
            )
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"保存失败: {e}"

    @mcp.tool()
    def keynote_close(save: bool = True) -> str:
        """
        关闭当前文档。

        Args:
            save: 是否保存后关闭（默认 True）

        Returns:
            关闭操作结果
        """
        try:
            result = keynote_controller.close_presentation(save=save)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"关闭失败: {e}"


# ============================================================================
# 工具：幻灯片操作
# ============================================================================

    @mcp.tool()
    def keynote_add_slide(title: str = "", body: str = "",
                         position: int = 0) -> str:
        """
        添加新幻灯片到当前文档。

        Args:
            title: 幻灯片标题（可选）
            body: 正文内容（可选）
            position: 插入位置，1-based（0 或留空表示在末尾添加）

        Returns:
            新幻灯片编号和当前总数
        """
        try:
            pos = position if position > 0 else None
            result = keynote_controller.add_slide(
                title=title or None,
                body=body or None,
                position=pos
            )
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"添加幻灯片失败: {e}"

    @mcp.tool()
    def keynote_delete_slide(slide_number: int) -> str:
        """
        删除指定幻灯片。

        Args:
            slide_number: 要删除的幻灯片编号，从 1 开始

        Returns:
            删除结果和剩余幻灯片数量
        """
        try:
            result = keynote_controller.delete_slide(slide_number)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"删除失败: {e}"

    @mcp.tool()
    def keynote_list_slides() -> str:
        """
        列出当前文档的所有幻灯片。

        返回:
            所有幻灯片的编号和标题列表
        """
        try:
            result = keynote_controller.list_all_slides()
            output = f"=== 共 {result['total_slides']} 张幻灯片 ===\n\n"
            for slide in result["slides"]:
                output += f"[{slide['slide_number']:>2d}] {slide['title']}\n"
            return output
        except Exception as e:
            return f"获取幻灯片列表失败: {e}"

    @mcp.tool()
    def keynote_duplicate_slide(slide_number: int) -> str:
        """
        复制指定幻灯片。

        Args:
            slide_number: 要复制的幻灯片编号

        Returns:
            复制结果
        """
        try:
            from keynote_tools import applescript
            applescript.duplicate_slide(slide_number)
            return f"已复制幻灯片 {slide_number}"
        except Exception as e:
            return f"复制失败: {e}"


# ============================================================================
# 工具：内容编辑
# ============================================================================

    @mcp.tool()
    def keynote_set_title(slide_number: int, text: str) -> str:
        """
        设置指定幻灯片的标题。

        Args:
            slide_number: 幻灯片编号，从 1 开始
            text: 标题文本

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_title(slide_number, text)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"设置标题失败: {e}"

    @mcp.tool()
    def keynote_set_body(slide_number: int, text: str) -> str:
        """
        设置指定幻灯片的正文内容。

        Args:
            slide_number: 幻灯片编号，从 1 开始
            text: 正文文本

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_body(slide_number, text)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"设置正文失败: {e}"

    @mcp.tool()
    def keynote_add_textbox(slide_number: int, text: str,
                           left: int = 100, top: int = 100,
                           width: int = 400, height: int = 100) -> str:
        """
        在幻灯片上添加一个自由文本框。

        Args:
            slide_number: 幻灯片编号
            text: 文本内容
            left: 距离左边的像素位置
            top: 距离顶部的像素位置
            width: 文本框宽度（像素）
            height: 文本框高度（像素）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.add_textbox(
                slide_number, text, left, top, width, height
            )
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"添加文本框失败: {e}"

    @mcp.tool()
    def keynote_add_image(slide_number: int, image_path: str,
                         left: int = 100, top: int = 100,
                         width: int = 400, height: int = 300) -> str:
        """
        在幻灯片上添加图片。

        Args:
            slide_number: 幻灯片编号
            image_path: 图片文件路径（支持 ~/）
            left: 距离左边的像素位置
            top: 距离顶部的像素位置
            width: 图片宽度（像素）
            height: 图片高度（像素）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.add_image(
                slide_number, image_path, left, top, width, height
            )
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"添加图片失败: {e}"


# ============================================================================
# 工具：演示控制
# ============================================================================

    @mcp.tool()
    def keynote_start_show() -> str:
        """
        开始播放当前演示文稿。
        """
        try:
            result = keynote_controller.start_show()
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"播放失败: {e}"

    @mcp.tool()
    def keynote_stop_show() -> str:
        """
        停止播放演示文稿。
        """
        try:
            result = keynote_controller.stop_show()
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"停止失败: {e}"

    @mcp.tool()
    def keynote_next_slide() -> str:
        """
        切换到下一张幻灯片。
        """
        try:
            result = keynote_controller.next_slide()
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"操作失败: {e}"

    @mcp.tool()
    def keynote_previous_slide() -> str:
        """
        切换到上一张幻灯片。
        """
        try:
            result = keynote_controller.previous_slide()
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"操作失败: {e}"

    @mcp.tool()
    def keynote_go_to_slide(slide_number: int) -> str:
        """
        跳转到指定幻灯片。

        Args:
            slide_number: 目标幻灯片编号
        """
        try:
            result = keynote_controller.go_to_slide(slide_number)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"跳转失败: {e}"


# ============================================================================
# 工具：查询与导出
# ============================================================================

    @mcp.tool()
    def keynote_get_info() -> str:
        """
        获取当前文档的基本信息（幻灯片数量等）。
        """
        try:
            result = keynote_controller.get_info()
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"获取信息失败: {e}"

    @mcp.tool()
    def keynote_get_slide_content(slide_number: int) -> str:
        """
        获取指定幻灯片的标题和正文内容。

        Args:
            slide_number: 幻灯片编号
        """
        try:
            result = keynote_controller.get_slide(slide_number)
            output = f"=== 幻灯片 {slide_number} ===\n"

            content = result.get("content", {})
            if "title" in content and content["title"]:
                output += f"\n标题:\n{content['title']}\n"
            if "body" in content and content["body"]:
                output += f"\n正文:\n{content['body']}\n"

            if output == f"=== 幻灯片 {slide_number} ===\n":
                output += "\n(此幻灯片可能没有文本内容或为空)"

            return output
        except Exception as e:
            return f"获取内容失败: {e}"

    @mcp.tool()
    def keynote_export(format_type: str, output_path: str) -> str:
        """
        导出当前文档为其他格式。

        Args:
            format_type: 导出格式，可选: "pdf"、"pptx"、"mov"、"html"
            output_path: 输出文件路径（支持 ~/）
                        例如: ~/Desktop/导出.pdf

        Returns:
            导出结果和文件路径
        """
        try:
            result = keynote_controller.export_document(format_type, output_path)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"导出失败: {e}"

    @mcp.tool()
    def keynote_list_themes() -> str:
        """
        列出 Keynote 中所有可用的主题名称。
        可在创建文档时作为 theme 参数使用。
        """
        try:
            result = keynote_controller.get_themes()
            if result.get("status") == "error":
                return f"获取主题列表失败: {result.get('error')}"

            themes = result.get("themes", [])
            output = f"=== 可用主题 (共 {len(themes)} 个) ===\n\n"
            for i, theme in enumerate(themes, 1):
                output += f"{i:>2d}. {theme}\n"
            return output
        except Exception as e:
            return f"获取主题失败: {e}"

    @mcp.tool()
    def keynote_list_masters() -> str:
        """
        列出当前文档的所有母版/幻灯片布局。
        """
        try:
            result = keynote_controller.get_masters()
            if result.get("status") == "error":
                return f"获取母版失败: {result.get('error')}"

            masters = result.get("master_slides", [])
            output = f"=== 母版/布局 (共 {len(masters)} 个) ===\n\n"
            for i, master in enumerate(masters, 1):
                output += f"{i:>2d}. {master}\n"
            return output
        except Exception as e:
            return f"获取母版失败: {e}"


# ============================================================================
# 工具：高级场景
# ============================================================================

    @mcp.tool()
    def keynote_create_launch_event(event_title: str, slide_titles: list[str]) -> str:
        """
        创建一个完整的发布会演示文稿（快速创建多张幻灯片）。

        Args:
            event_title: 发布会标题（封面幻灯片标题）
            slide_titles: 各幻灯片的标题列表，例如:
                          ["议程", "产品愿景", "核心亮点", "技术规格"]

        Returns:
            创建结果和幻灯片数量
        """
        try:
            # 准备幻灯片数据
            slides_data = [{"title": title, "body": ""} for title in slide_titles]

            result = keynote_controller.create_launch_event_presentation(
                event_title, slides_data
            )
            return (
                f"✓ {result['message']}\n"
                f"发布会: {result['event_title']}\n"
                f"总幻灯片: {result['total_slides']}\n"
                f"\n提示: 你可以后续使用 keynote_set_title 和 keynote_set_body"
                f"逐张完善内容。"
            )
        except Exception as e:
            return f"创建发布会失败: {e}"


# ============================================================================
# 工具：数智财务 SAP 风格 (v2.0 新增)
# ============================================================================

    @mcp.tool()
    def keynote_set_canvas_size(width: int, height: int) -> str:
        """
        设置当前文档的画布尺寸。

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
        try:
            result = keynote_controller.set_canvas_size(width, height)
            return keynote_controller.format_result(result)
        except Exception as e:
            return f"设置画布尺寸失败: {e}"

    @mcp.tool()
    def keynote_create_ultra_wide(title: str = "", theme: str = "Black") -> str:
        """
        创建超宽屏演示文稿（3:1 比例，3200×1080）。

        Args:
            title: 封面标题（可选）
            theme: 主题名称（默认 Black 深色主题）

        Returns:
            创建结果，包含画布尺寸信息
        """
        try:
            result = keynote_controller.create_ultra_wide_presentation(title, theme)
            return (
                f"✓ {result['message']}\n"
                f"标题: {result['title']}\n"
                f"主题: {result['theme']}\n"
                f"画布: {result['canvas_size']}\n"
                f"幻灯片: {result['slide_count']}"
            )
        except Exception as e:
            return f"创建超宽屏演示文稿失败: {e}"

    @mcp.tool()
    def keynote_add_kpi_slide(title: str, kpi_items: list[dict]) -> str:
        """
        添加 KPI 数字展示幻灯片。

        Args:
            title: 幻灯片标题
            kpi_items: KPI 数据列表，每项包含:
                       - number: 数字（如 "¥2.42"）
                       - label: 标签（如 "当前股价"）
                       - color: 颜色（可选："gold", "green", "red", "white"）

        示例:
            kpi_items = [
                {"number": "¥2.42", "label": "当前股价", "color": "gold"},
                {"number": "¥215亿", "label": "市值", "color": "gold"},
                {"number": "15.17x", "label": "PE(TTM)", "color": "cyan"}
            ]

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.add_kpi_slide(title, kpi_items)
            return (
                f"✓ {result['message']}\n"
                f"幻灯片编号: {result['slide_number']}\n"
                f"标题: {result['title']}\n"
                f"KPI 数量: {result['kpi_count']}"
            )
        except Exception as e:
            return f"添加 KPI 幻灯片失败: {e}"

    @mcp.tool()
    def keynote_create_digital_finance(title: str, slides_data: list[dict],
                                       save_path: str = "") -> str:
        """
        创建数智财务 SAP 风格演示文稿（一键生成完整演示）。

        Args:
            title: 演示文稿标题
            slides_data: 幻灯片数据列表，每项包含:
                         - slide_type: "cover", "kpi", "content", "card", "thank_you"
                         - title: 幻灯片标题
                         - content: 内容数据
            save_path: 保存路径（可选，如 ~/Desktop/演示.key）

        示例:
            slides_data = [
                {"slide_type": "kpi", "title": "核心指标",
                 "content": [{"number": "¥2.42", "label": "股价"}]},
                {"slide_type": "content", "title": "业务分析",
                 "content": "五大业务板块..."},
                {"slide_type": "thank_you", "title": "Thank You", "content": ""}
            ]

        Returns:
            创建结果
        """
        try:
            path = save_path if save_path else None
            result = keynote_controller.create_digital_finance_presentation(
                title, slides_data, path
            )
            return (
                f"✓ {result['message']}\n"
                f"标题: {result['title']}\n"
                f"幻灯片: {result['slide_count']}\n"
                f"画布: {result['canvas_size']}\n"
                f"保存路径: {result['save_path'] or '(未保存)'}"
            )
        except Exception as e:
            return f"创建数智财务演示文稿失败: {e}"

    @mcp.tool()
    def keynote_create_valuation_report(stock_code: str, company_name: str,
                                         kpi_data: dict, financial_data: dict,
                                         save_path: str = "") -> str:
        """
        创建上市公司估值报告演示文稿（13页标准结构）。

        Args:
            stock_code: 股票代码（如 "600170"）
            company_name: 公司名称
            kpi_data: 核心 KPI 数据字典，包含:
                       - price: 股价
                       - market_cap: 市值
                       - pe: PE(TTM)
                       - pb: PB
                       - ps: PS
                       - dividend_yield: 股息率
            financial_data: 财务数据字典，包含:
                            - revenue: 营收
                            - net_profit: 净利润
                            - roe: ROE
            save_path: 保存路径（可选）

        示例:
            kpi_data = {
                "price": "¥2.42",
                "market_cap": "¥215亿",
                "pe": "15.17x",
                "pb": "0.56x",
                "dividend_yield": "2.48%"
            }
            financial_data = {
                "revenue": "¥3002亿",
                "net_profit": "¥21.68亿",
                "roe": "5.21%"
            }

        Returns:
            创建结果
        """
        try:
            path = save_path if save_path else None
            result = keynote_controller.create_valuation_report(
                stock_code, company_name, kpi_data, financial_data, path
            )
            return (
                f"✓ {result['message']}\n"
                f"股票代码: {result['stock_code']}\n"
                f"公司名称: {result['company_name']}\n"
                f"幻灯片: {result['slide_count']} 页\n"
                f"画布: {result['canvas_size']}\n"
                f"保存路径: {result['save_path'] or '(未保存)'}"
            )
        except Exception as e:
            return f"创建估值报告失败: {e}"

    @mcp.tool()
    def keynote_get_canvas_info() -> str:
        """
        获取当前文档的画布尺寸信息。

        Returns:
            画布宽度和高度
        """
        try:
            result = keynote_controller.get_canvas_info()
            canvas = result.get("canvas", {})
            width = canvas.get("width", "未知")
            height = canvas.get("height", "未知")
            return f"画布尺寸: {width} × {height} 像素"
        except Exception as e:
            return f"获取画布信息失败: {e}"


# ============================================================================
# 工具：动画效果 (v3.0 新增)
# ============================================================================

    @mcp.tool()
    def keynote_set_transition(slide_number: int, transition_type: str = "fade") -> str:
        """
        设置幻灯片的过渡动画。

        Args:
            slide_number: 幻灯片编号
            transition_type: 过渡动画类型
                - "magic_move": 神奇移动（元素平滑过渡）⭐
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
        try:
            result = keynote_controller.set_transition(slide_number, transition_type)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置过渡动画失败: {e}"

    @mcp.tool()
    def keynote_set_magic_move(from_slide: int, to_slide: int) -> str:
        """
        设置 Magic Move 神奇移动效果。

        Magic Move 是 Keynote 最强大的动画效果，可以自动匹配两张幻灯片
        中的相同元素，并创建平滑的过渡动画。

        Args:
            from_slide: 起始幻灯片编号
            to_slide: 目标幻灯片编号

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_magic_move(from_slide, to_slide)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置 Magic Move 失败: {e}"

    @mcp.tool()
    def keynote_add_build_animation(slide_number: int, element_index: int,
                                     animation_type: str = "appear") -> str:
        """
        添加构建动画（元素进入动画）。

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

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.add_build_animation(
                slide_number, element_index, animation_type
            )
            return f"✓ {result['message']}"
        except Exception as e:
            return f"添加构建动画失败: {e}"

    @mcp.tool()
    def keynote_clear_animations(slide_number: int) -> str:
        """
        清除幻灯片上的所有动画效果。

        Args:
            slide_number: 幻灯片编号

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.clear_animations(slide_number)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"清除动画失败: {e}"

    @mcp.tool()
    def keynote_preview_animation(slide_number: int) -> str:
        """
        预览幻灯片的动画效果。

        Args:
            slide_number: 幻灯片编号

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.preview_animation(slide_number)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"预览动画失败: {e}"


# ============================================================================
# 工具：字体渲染 (v3.0 新增)
# ============================================================================

    @mcp.tool()
    def keynote_set_font(slide_number: int, element_index: int, font_name: str) -> str:
        """
        设置元素的字体。

        Args:
            slide_number: 幻灯片编号
            element_index: 元素索引
            font_name: 字体名称
                - "pingfang_bold": 苹方粗体（中文标题）
                - "pingfang_regular": 苹方常规（中文正文）
                - "sf_pro_heavy": SF Pro Heavy（英文标题）
                - "sf_pro_black": SF Pro Black（KPI数字）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_font(slide_number, element_index, font_name)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置字体失败: {e}"

    @mcp.tool()
    def keynote_set_font_size(slide_number: int, element_index: int, size: int) -> str:
        """
        设置元素的字号。

        Args:
            slide_number: 幻灯片编号
            element_index: 元素索引
            size: 字号（pt），推荐值：
                - 封面标题: 88-120pt
                - 章节标题: 48-64pt
                - 卡片标题: 28-36pt
                - 正文: 18-22pt
                - KPI数字: 60-120pt

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_font_size(slide_number, element_index, size)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置字号失败: {e}"

    @mcp.tool()
    def keynote_set_font_color(slide_number: int, element_index: int, color: str) -> str:
        """
        设置元素的字体颜色。

        Args:
            slide_number: 幻灯片编号
            element_index: 元素索引
            color: 颜色名称
                - "white": 白色（主文本）
                - "gold": 金色（KPI数字）
                - "green": 财务绿（正向数据）
                - "red": 红色（警示）
                - "cyan": 青色（科技蓝）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_font_color(slide_number, element_index, color)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置颜色失败: {e}"

    @mcp.tool()
    def keynote_apply_font_style(slide_number: int, element_index: int,
                                  style_name: str = "title") -> str:
        """
        应用预设字体样式（一键设置字体、字号、颜色）。

        Args:
            slide_number: 幻灯片编号
            element_index: 元素索引
            style_name: 样式名称
                - "title": 大标题样式（苹方粗体 88pt 白色）
                - "subtitle": 副标题样式（苹方常规 44pt 白色）
                - "kpi": KPI数字样式（SF Pro Black 72pt 金色）⭐
                - "card_title": 卡片标题样式（苹方粗体 28pt 白色）
                - "body": 正文样式（苹方常规 18pt 浅灰）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.apply_font_style(
                slide_number, element_index, style_name
            )
            return f"✓ {result['message']}"
        except Exception as e:
            return f"应用样式失败: {e}"


# ============================================================================
# 工具：屏幕适配 (v3.0 新增)
# ============================================================================

    @mcp.tool()
    def keynote_auto_fit_screen() -> str:
        """
        自动适配当前屏幕尺寸。

        获取当前主显示器的分辨率，并设置演示文稿画布尺寸。

        Returns:
            操作结果，包含屏幕信息
        """
        try:
            result = keynote_controller.auto_fit_screen()
            screen_info = result.get("screen_info", {})
            return (
                f"✓ {result['message']}\n"
                f"屏幕分辨率: {screen_info.get('resolution', '未知')}"
            )
        except Exception as e:
            return f"自动适配屏幕失败: {e}"

    @mcp.tool()
    def keynote_get_screen_info() -> str:
        """
        获取屏幕信息。

        Returns:
            屏幕分辨率信息
        """
        try:
            result = keynote_controller.get_screen_info()
            screen = result.get("screen", {})
            return (
                f"屏幕分辨率: {screen.get('resolution', '未知')}\n"
                f"宽度: {screen.get('width', '未知')} px\n"
                f"高度: {screen.get('height', '未知')} px"
            )
        except Exception as e:
            return f"获取屏幕信息失败: {e}"


# ============================================================================
# 工具：专业展示 (v3.0 新增)
# ============================================================================

    @mcp.tool()
    def keynote_start_presenter_mode() -> str:
        """
        启动演讲者模式。

        演讲者模式会显示：
        - 当前幻灯片（观众看到的）
        - 下一张预览
        - 演讲者备注
        - 计时器

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.start_presenter_mode()
            return f"✓ {result['message']}"
        except Exception as e:
            return f"启动演讲者模式失败: {e}"

    @mcp.tool()
    def keynote_set_timer(duration_minutes: int) -> str:
        """
        设置演示计时器。

        Args:
            duration_minutes: 演示时长（分钟）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_timer(duration_minutes)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置计时器失败: {e}"

    @mcp.tool()
    def keynote_set_auto_play(interval_seconds: float = 5.0) -> str:
        """
        设置自动播放。

        Args:
            interval_seconds: 每张幻灯片显示时间（秒）

        Returns:
            操作结果
        """
        try:
            result = keynote_controller.set_auto_play(interval_seconds)
            return f"✓ {result['message']}"
        except Exception as e:
            return f"设置自动播放失败: {e}"

    @mcp.tool()
    def keynote_get_performance_info() -> str:
        """
        获取 Keynote 性能信息。

        Returns:
            性能信息，包含幻灯片数量、画布尺寸、内存估算
        """
        try:
            result = keynote_controller.get_performance_info()
            perf = result.get("performance", {})
            return (
                f"幻灯片数量: {perf.get('slide_count', '未知')}\n"
                f"画布尺寸: {perf.get('canvas_width', '未知')} × {perf.get('canvas_height', '未知')}\n"
                f"预估内存: {perf.get('estimated_memory_mb', '未知')} MB\n"
                f"状态: {perf.get('status', '未知')}"
            )
        except Exception as e:
            return f"获取性能信息失败: {e}"


# ============================================================================
# 主函数：启动 MCP Server
# ============================================================================

def main():
    """
    启动 Keynote MCP Server
    """
    # 检查运行环境
    status = keynote_controller.get_keynote_status()

    # 如果 MCP SDK 不可用，给出友好提示
    if not MCP_AVAILABLE:
        print("⚠️  MCP SDK 未安装")
        print()
        print("请先安装依赖:")
        print("  pip install \"mcp[cli]\"")
        print()
        print("或者使用项目自带的安装脚本:")
        print("  ./install.sh")
        sys.exit(1)

    # 打印启动信息到 stderr（避免干扰 stdio 协议）
    print(
        f"Keynote MCP Server (v3.0) 已启动\n"
        f"作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026\n"
        f"平台: {status.get('platform', 'unknown')}\n"
        f"状态: {status.get('status', 'unknown')}\n"
        f"新增功能: 动画效果 / 字体渲染 / 屏幕适配 / 演讲者模式 / 专业展示\n"
        f"(通过 MCP stdio 协议运行，等待 AI 调用...)",
        file=sys.stderr
    )

    # 启动 MCP Server（阻塞，直到进程被停止）
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nServer 已停止", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server 运行错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
