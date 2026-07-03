#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本

本地测试 Keynote MCP Server 的功能（无需启动 MCP Server）

用法:
    python3 quickstart.py --test      # 基本测试
    python3 quickstart.py --demo      # 创建一个简单的演示（需要 macOS + Keynote）
    python3 quickstart.py --status    # 检查状态

这个脚本可以在任何平台运行，但实际操作需要在 macOS + Keynote 才能执行
"""

import sys
import json
import argparse
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from keynote_tools import keynote_controller, applescript


def test_imports():
    """测试模块导入"""
    print("[1/4] 测试模块导入...")
    try:
        from keynote_tools import keynote_controller, applescript
        print("   ✓ keynote_tools 导入成功")
        return True
    except Exception as e:
        print(f"   ✗ 导入失败: {e}")
        return False


def test_platform():
    """测试平台检测"""
    print("[2/4] 测试平台检测...")

    try:
        info = keynote_controller.get_keynote_status()
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"   ✗ 平台检测失败: {e}")
        return False


def test_utils():
    """测试工具函数"""
    print("[3/4] 测试字符串处理...")

    try:
        text = "这是测试文本"
        escaped = applescript.escape_applescript_string(text)
        print(f"   原始: {text}")
        print(f"   转义: {escaped}")
        return True
    except Exception as e:
        print(f"   ✗ 测试失败: {e}")
        return False


def test_mcp_import():
    """测试 MCP SDK 可用性"""
    print("[4/4] 测试 MCP SDK...")
    try:
        from mcp.server.fastmcp import FastMCP
        print("   ✓ MCP SDK (mcp.server.fastmcp.FastMCP) 可用")
        return True
    except ImportError:
        print("   ✗ MCP SDK 未安装")
        print("   安装命令: pip install \"mcp[cli]\"")
        return False


def run_demo():
    """运行简单的演示操作"""
    print("\n=== Keynote 操作演示 ===\n")

    if not applescript.is_macos():
        print("⚠️  非 macOS 平台，无法操作 Keynote")
        print("(此功能仅在 macOS + Keynote环境可用")
        return False

    print("提示: 此操作会打开 Keynote.app")
    confirm = input("是否继续? (y/n): ")
    if confirm.lower() != "y":
        print("已取消")
        return False

    try:
        # 创建演示文稿
        result = keynote_controller.create_presentation(
            title="演示文稿 - Keynote MCP Server 演示",
        )
        print(f"✓ {result['message']}")

        # 等待一下，让 Keynote 准备好
        import time
        time.sleep(1)

        # 添加几张幻灯片
        slides_to_add = [
            "第二张",
            "第三张",
            "第四张",
        ]
        for title in slides_to_add:
            result = keynote_controller.add_slide(title=title, body="演示内容")
            print(f"  已添加: {title}")
            time.sleep(0.3)

        # 获取信息
        info = keynote_controller.get_info()
        print(f"\n✓ 当前文档: {info['slide_count']} 张幻灯片")

        # 列出幻灯片
        slides = keynote_controller.list_all_slides()
        print("\n幻灯片列表:")
        for slide in slides["slides"]:
            print(f"  [{slide['slide_number']:>2d}] {slide['title']}")

        # 导出 PDF
        home = Path.home()
        export_path = str(home / "Desktop/keynote_mcp_demo.pdf")
        export = keynote_controller.export_document("pdf", export_path)
        print(f"\n✓ 已导出到: {export['output_path']}")

        print("\n演示完成!")
        print("Keynote 应该已打开并显示演示文稿")
        return True

    except Exception as e:
        print(f"\n✗ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_status():
    """显示详细状态信息"""
    print("\n=== Keynote MCP Server 状态报告 ===\n")

    status = keynote_controller.get_keynote_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    print()

    # 检查 MCP SDK
    try:
        from mcp.server.fastmcp import FastMCP
        print("✓ MCP SDK: 已安装")
        mcp_available = True
    except ImportError:
        print("✗ MCP SDK: 未安装")
        mcp_available = False

    # 检查配置文件
    config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    if config_path.exists():
        print(f"✓ Claude Desktop 配置: 已找到")
        print(f"  路径: {config_path}")

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            if 'mcpServers' in config and 'keynote' in config['mcpServers']:
                print("  ✓ keynote MCP Server 已配置")
            else:
                print("  ⚠ keynote MCP Server 未配置")
        except json.JSONDecodeError:
            print("  ✗ 配置文件格式错误")
    else:
        print(f"⚠  Claude Desktop 配置: 未找到")
        print(f"  预期路径: {config_path}")

    print()
    print("=== 建议操作 ===")
    if not mcp_available:
        print("1. 安装 MCP SDK: pip install \"mcp[cli]\"")
    print("2. 运行安装脚本: ./install.sh")
    print("3. 重启 Claude Desktop")


def main():
    parser = argparse.ArgumentParser(
        description="Keynote MCP Server - 快速测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 quickstart.py --test    # 运行所有测试
  python3 quickstart.py --demo      # 创建演示文稿 (macOS 专用)
  python3 quickstart.py --status   # 检查状态
"""
    )
    parser.add_argument('--test', action='store_true', help='运行所有测试')
    parser.add_argument('--demo', action='store_true', help='创建演示文稿')
    parser.add_argument('--status', action='store_true', help='检查系统状态')

    args = parser.parse_args()

    # 如果没有指定任何参数，默认为 --test
    if not args.test and not args.demo and not args.status:
        args.test = True

    print("╔══════════════════════════════════════╗")
    print("║   Keynote MCP Server - 快速测试   ║")
    print("╚══════════════════════════════════════╝")
    print()

    success = True

    if args.test:
        print("\n--- 测试模式 ---")
        success &= test_imports()
        success &= test_platform()
        success &= test_utils()
        success &= test_mcp_import()
        print()

    if args.demo:
        print("\n--- 演示模式 ---")
        success &= run_demo()
        print()

    if args.status:
        show_status()

    # 总结
    if success:
        print("\n✓ 所有检查通过")
        print("\n下一步:")
        print("  1. 运行 ./install.sh 完成安装")
        print("  2. 配置 Claude Desktop (见 install.sh)")
        print("  3. 在 Claude 中说: '检查 Keynote 状态'")
        return 0
    else:
        print("\n⚠ 部分检查失败，请检查上方的警告信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
