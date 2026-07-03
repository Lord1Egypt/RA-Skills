#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数智财务 Keynote 直接生成脚本 (macOS AppleScript 版)
======================================================
作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

此脚本需要在 macOS 上运行，通过 AppleScript 直接控制 Keynote.app
生成数智财务 SAP 风格的演示文稿。

使用方法:
    python3 create_keynote_direct.py

依赖:
    - macOS 12.0+ (Monterey 及以上)
    - Keynote 12.0+
    - Python 3.10+
"""

import subprocess
import sys
import os

def run_applescript(script: str) -> str:
    """执行 AppleScript 并返回结果"""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"AppleScript 错误: {result.stderr}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("AppleScript 执行超时")
        return ""
    except Exception as e:
        print(f"执行错误: {e}")
        return ""

def create_digital_finance_keynote():
    """创建数智财务 SAP 风格 Keynote 演示文稿"""

    print("=" * 60)
    print(" 数智财务 Keynote 直接生成器 (AppleScript 版)")
    print(" 作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026")
    print("=" * 60)
    print()

    # 检查是否在 macOS 上运行
    if sys.platform != 'darwin':
        print("❌ 此脚本只能在 macOS 上运行")
        print("   当前系统: " + sys.platform)
        print()
        print("替代方案:")
        print("   1. 使用 generate_presentation.py 生成 PPTX")
        print("   2. 在 macOS Keynote 中打开 PPTX 并另存为 .key")
        return False

    # 检查 Keynote 是否安装
    check_keynote = '''
    tell application "System Events"
        return name of every application process contains "Keynote"
    end tell
    '''

    result = run_applescript(check_keynote)
    if "true" not in result.lower():
        print("正在启动 Keynote...")
        run_applescript('tell application "Keynote" to activate')
        import time
        time.sleep(3)

    print("创建演示文稿...")

    # 创建 Keynote 文档的 AppleScript
    create_script = '''
    tell application "Keynote"
        activate

        -- 创建新文档，使用深色主题
        set newDoc to make new document with properties {document theme:theme "Black"}

        -- 设置文档尺寸为超宽屏 (3200 x 1080)
        tell newDoc
            set width to 3200
            set height to 1080
        end tell

        -- 获取第一个幻灯片
        set slide1 to slide 1 of newDoc

        -- 设置封面标题
        tell slide1
            set title to "数智财务峰会"
            set body to "SAP 企业级超宽屏演示文稿\\n\\n作者: Wang Dongjie, CGMA/AICPA&CIMA\\n© 2026"
        end tell

        -- 添加议程幻灯片
        set slide2 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide2
            set title to "议程概览"
            set body to "• 数字化背景与挑战\\n• 技术演进路径\\n• 解决方案架构\\n• 实施成果展示\\n• 未来展望"
        end tell

        -- 添加数字化背景幻灯片
        set slide3 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide3
            set title to "数字化背景"
            set body to "传统财务困境:\\n• 数据孤岛严重\\n• 手工操作繁琐\\n• 决策滞后\\n\\n转型驱动因素:\\n• 实时数据需求\\n• 合规监管压力\\n• 效率提升目标"
        end tell

        -- 添加解决方案幻灯片
        set slide4 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide4
            set title to "数智财务解决方案"
            set body to "核心能力:\\n• 预算编制自动化\\n• 实时财务分析\\n• 智能报表生成\\n• 多维度数据可视化\\n• 移动端审批流程"
        end tell

        -- 添加成果幻灯片
        set slide5 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Top" of newDoc}
        tell slide5
            set title to "实施成果"
            set body to "效率提升:\\n• 报表生成时间: 从 3 天 → 30 分钟\\n• 预算编制周期: 从 2 周 → 3 天\\n• 数据准确率: 99.5%\\n\\n成本节约:\\n• 人力成本降低 40%\\n• IT 维护成本降低 30%"
        end tell

        -- 添加 Thank You 幻灯片
        set slide6 to make new slide at end of slides of newDoc with properties {base slide:base slide "Title - Center" of newDoc}
        tell slide6
            set title to "Thank You"
            set body to "数智财务演示 Skill\\n\\nWang Dongjie, CGMA/AICPA&CIMA\\n© 2026"
        end tell

        -- 保存文档
        set savePath to (path to desktop as text) & "数智财务峰会演示.key"
        save newDoc in file savePath

        return "✅ 演示文稿已创建并保存到桌面: " & savePath
    end tell
    '''

    result = run_applescript(create_script)

    if result:
        print(result)
        print()
        print("=" * 60)
        print(" 生成完成!")
        print("=" * 60)
        print()
        print("文件位置: ~/Desktop/数智财务峰会演示.key")
        print("幻灯片数量: 6 张")
        print("风格: Black 深色主题")
        print()
        return True
    else:
        print("❌ 创建失败，请检查 Keynote 权限")
        print()
        print("权限设置:")
        print("  系统设置 → 隐私与安全性 → 自动化")
        print("  允许 Python 控制 Keynote")
        return False

if __name__ == "__main__":
    create_digital_finance_keynote()