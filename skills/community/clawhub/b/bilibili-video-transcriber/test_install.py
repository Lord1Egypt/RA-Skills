#!/usr/bin/env python3
"""
安装后测试脚本
"""

import sys
import os
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        import bilibili_transcriber
        from bilibili_transcriber import BilibiliTranscriber, ProcessingResult
        
        print("✅ bilibili_transcriber 导入成功")
        
        # 测试依赖
        import requests
        import yaml
        from faster_whisper import WhisperModel
        from bilibili_api import video, Credential
        
        print("✅ 所有依赖导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_config():
    """测试配置文件"""
    print("\n🔍 测试配置文件...")
    
    try:
        config_path = Path(__file__).parent / "config.yaml"
        
        if config_path.exists():
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            print("✅ 配置文件读取成功")
            print(f"   模型: {config.get('model', {}).get('name', '未设置')}")
            print(f"   语言: {config.get('model', {}).get('language', '未设置')}")
            return True
        else:
            print("❌ 配置文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def test_cli():
    """测试命令行工具"""
    print("\n🔍 测试命令行工具...")
    
    try:
        cli_path = Path(__file__).parent / "cli.py"
        
        if cli_path.exists():
            # 检查文件是否可执行
            if os.access(cli_path, os.X_OK):
                print("✅ CLI脚本可执行")
            else:
                print("⚠️ CLI脚本不可执行，尝试修复...")
                os.chmod(cli_path, 0o755)
                print("✅ CLI脚本权限已修复")
            
            # 测试帮助命令
            import subprocess
            result = subprocess.run(
                [sys.executable, str(cli_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ CLI帮助命令测试成功")
                return True
            else:
                print("❌ CLI帮助命令测试失败")
                print(f"   错误: {result.stderr[:100]}")
                return False
        else:
            print("❌ CLI脚本不存在")
            return False
            
    except Exception as e:
        print(f"❌ CLI测试失败: {e}")
        return False

def test_cookie():
    """测试Cookie文件"""
    print("\n🔍 测试Cookie文件...")
    
    try:
        # 检查默认Cookie文件
        cookie_path = Path.home() / ".bilibili_cookie.txt"
        
        if cookie_path.exists():
            with open(cookie_path, 'r') as f:
                content = f.read().strip()
            
            if content and not content.startswith("#"):
                print("✅ Cookie文件存在且包含内容")
                return True
            else:
                print("⚠️ Cookie文件存在但可能为空或只有注释")
                print("   请编辑 ~/.bilibili_cookie.txt 并添加你的B站Cookie")
                return False
        else:
            print("⚠️ Cookie文件不存在")
            print("   请运行: python setup.py 创建Cookie文件模板")
            return False
            
    except Exception as e:
        print(f"❌ Cookie测试失败: {e}")
        return False

def test_ffmpeg():
    """测试FFmpeg"""
    print("\n🔍 测试FFmpeg...")
    
    try:
        import subprocess
        
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ FFmpeg可用")
            return True
        else:
            print("❌ FFmpeg不可用")
            print("   请安装FFmpeg: https://ffmpeg.org/download.html")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg未安装")
        print("   请安装FFmpeg: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"❌ FFmpeg测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 B站视频转录专家 - 安装测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置文件", test_config),
        ("命令行工具", test_cli),
        ("Cookie文件", test_cookie),
        ("FFmpeg", test_ffmpeg)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 打印结果
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
        if not success:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 所有测试通过！")
        print("\n📖 下一步:")
        print("1. 编辑Cookie文件: nano ~/.bilibili_cookie.txt")
        print("2. 添加你的B站Cookie")
        print("3. 测试转录: bilibili-transcribe BV1txQGByERW")
    else:
        print("\n⚠️ 部分测试失败")
        print("\n🔧 修复建议:")
        print("1. 运行安装脚本: python setup.py")
        print("2. 安装FFmpeg")
        print("3. 检查Python依赖: pip install -r requirements.txt")
    
    print("\n" + "=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())