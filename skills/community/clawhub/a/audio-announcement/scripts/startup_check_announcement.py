#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Announcement Startup Check
在每次 /RESET 或 /NEW 后自动运行，确保播报功能正常
"""

import sys
import subprocess
from pathlib import Path

def check_announcement_setup():
    """检查播报功能是否就绪"""
    issues = []
    
    # 1. 检查 edge-tts 模块
    try:
        import edge_tts
    except ImportError:
        issues.append("edge-tts 未安装 (运行: py -3 -m pip install edge-tts)")
    
    # 2. 检查 pygame 模块 (可选但推荐)
    try:
        import pygame
    except ImportError:
        issues.append("pygame 未安装 (运行: py -3 -m pip install pygame) - 推荐使用 pygame 方案")
    
    # 3. 检查配置文件
    config_file = Path.home() / ".config" / "audio-announcement" / "config.json"
    if not config_file.exists():
        issues.append("配置文件不存在 (运行: audio-announce config)")
    
    # 4. 检查 audio_announcement 包是否可用
    try:
        import audio_announcement
    except ImportError:
        issues.append("audio-announcement 包未安装 (运行: pip install audio-announcement)")
    
    return issues

def main():
    print("[AUDIO] 语音播报系统自检...")
    
    issues = check_announcement_setup()
    
    if not issues:
        print("[OK] 所有检查通过！语音播报功能正常。")
        
        # 可选：运行简短的测试
        print("\n[TEST] 正在测试播报...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "audio_announcement.cli", "receive", "系统启动", "zh"],
                capture_output=True,
                timeout=15
            )
            if result.returncode == 0:
                print("[OK] 播报测试完成！")
                return 0
            else:
                print("[WARN] 播报测试失败，但依赖检查通过")
                return 0
        except Exception as e:
            print(f"[WARN] 测试异常: {e}")
            return 0
    else:
        print("[ERROR] 发现以下问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n[SUGGEST] 建议:")
        print("   1. 安装依赖: py -3 -m pip install edge-tts pygame audio-announcement")
        print("   2. 运行测试: audio-announce test")
        print("   3. 配置: audio-announce config async_default=true")
        return 1

if __name__ == "__main__":
    sys.exit(main())
