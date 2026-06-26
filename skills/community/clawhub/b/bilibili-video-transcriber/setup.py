#!/usr/bin/env python3
"""
B站视频转录专家 - 安装脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """打印标题"""
    print("=" * 60)
    print("🎬 B站视频转录专家 - 安装程序")
    print("=" * 60)

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python版本过低: {sys.version}")
        print("   需要 Python 3.8 或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    return True

def check_ffmpeg():
    """检查FFmpeg"""
    print("🔍 检查FFmpeg...")
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # 提取版本信息
            lines = result.stdout.split('\n')
            version_line = lines[0] if lines else ""
            print(f"✅ FFmpeg: {version_line[:50]}...")
            return True
        else:
            print("❌ FFmpeg未正确安装")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg未安装")
        
        # 提供安装建议
        system = platform.system()
        if system == "Linux":
            print("   安装命令: sudo apt install ffmpeg")
        elif system == "Darwin":  # macOS
            print("   安装命令: brew install ffmpeg")
        elif system == "Windows":
            print("   请从 https://ffmpeg.org/download.html 下载安装")
        
        return False
    except Exception as e:
        print(f"❌ 检查FFmpeg失败: {e}")
        return False

def check_system_capability():
    """检查系统是否满足 faster-whisper 运行条件"""
    print("🔍 检查系统配置是否满足 faster-whisper 运行条件...")
    
    import psutil
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024 ** 3)
    
    has_cuda = False
    try:
        import torch
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"✅ 检测到 GPU: {gpu_name} ({gpu_memory:.1f} GB)")
    except Exception:
        pass
    
    if has_cuda:
        print(f"✅ 系统满足条件：有 GPU + {'%.1f'.format(memory_gb)}GB 内存")
        return True
    elif memory_gb >= 4:
        print(f"✅ 系统满足条件：有 {'%.1f'.format(memory_gb)}GB 内存（CPU 模式可用）")
        return True
    else:
        print(f"⚠️ 系统不满足 faster-whisper 条件（内存仅 {'%.1f'.format(memory_gb)}GB）")
        print("   将跳过 faster-whisper 安装，使用 Vosk 离线引擎替代")
        return False


def install_dependencies(skip_faster_whisper=False):
    """安装依赖，可选跳过 faster-whisper"""
    print("📦 安装Python依赖...")
    
    # 基础依赖（不包含 faster-whisper）
    base_dependencies = [
        "bilibili-api>=5.2.0",
        "requests>=2.28.0",
        "pydub>=0.25.1",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6"
    ]
    
    # faster-whisper 依赖列表
    faster_whisper_deps = ["faster-whisper>=0.10.0"]
    
    try:
        # 先安装基础依赖
        cmd = [sys.executable, "-m", "pip", "install"] + base_dependencies
        print(f"   安装基础依赖: {' '.join(base_dependencies[:3])}...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            print(f"❌ 基础依赖安装失败: {result.stderr[:200]}")
            return False
        print("✅ 基础依赖安装成功")
        
        # 根据条件决定是否安装 faster-whisper
        if skip_faster_whisper:
            print("⏭️ 跳过 faster-whisper 安装（系统配置不足）")
            print("   提示: 如需启用，请在高性能服务器上重新安装本技能")
        else:
            cmd = [sys.executable, "-m", "pip", "install"] + faster_whisper_deps
            print(f"   安装 faster-whisper...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode != 0:
                print(f"⚠️ faster-whisper 安装失败（非关键）: {result.stderr[:200]}")
                print("   将使用 Vosk 离线引擎作为替代")
            else:
                print("✅ faster-whisper 安装成功")
        
        return True
            
    except subprocess.TimeoutExpired:
        print("❌ 安装超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 安装依赖失败: {e}")
        return False

def create_config_files():
    """创建配置文件"""
    print("⚙️ 创建配置文件...")
    
    try:
        # 创建配置目录
        config_dir = Path.home() / ".config" / "bilibili_transcriber"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制配置文件
        current_dir = Path(__file__).parent
        config_file = current_dir / "config.yaml"
        
        if config_file.exists():
            import shutil
            shutil.copy2(config_file, config_dir / "config.yaml")
            print(f"✅ 配置文件已创建: {config_dir / 'config.yaml'}")
        else:
            print("⚠️ 未找到默认配置文件，将创建空配置")
            with open(config_dir / "config.yaml", 'w') as f:
                f.write("# B站视频转录专家配置文件\n")
        
        # 创建Cookie文件模板
        cookie_file = Path.home() / ".bilibili_cookie.txt"
        if not cookie_file.exists():
            with open(cookie_file, 'w') as f:
                f.write("# 请在此处粘贴B站Cookie\n")
                f.write("# 格式: SESSDATA=xxx; bili_jct=xxx; buvid3=xxx; DedeUserID=xxx\n")
            print(f"✅ Cookie文件模板已创建: {cookie_file}")
            print("   请编辑此文件并添加你的B站Cookie")
        else:
            print(f"✅ Cookie文件已存在: {cookie_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False

def setup_command_line():
    """设置命令行工具"""
    print("🔧 设置命令行工具...")
    
    try:
        current_dir = Path(__file__).parent
        cli_script = current_dir / "cli.py"
        
        # 检查脚本是否存在
        if not cli_script.exists():
            print("❌ 未找到命令行脚本")
            return False
        
        # 使脚本可执行
        if platform.system() != "Windows":
            os.chmod(cli_script, 0o755)
            print(f"✅ 脚本已设置为可执行: {cli_script}")
        
        # 创建符号链接或添加到PATH的建议
        system = platform.system()
        
        if system == "Linux" or system == "Darwin":
            # 建议创建符号链接
            bin_dir = Path.home() / ".local" / "bin"
            bin_dir.mkdir(parents=True, exist_ok=True)
            
            link_path = bin_dir / "bilibili-transcribe"
            
            try:
                if link_path.exists():
                    link_path.unlink()
                
                link_path.symlink_to(cli_script)
                print(f"✅ 创建符号链接: {link_path}")
                
                # 检查是否在PATH中
                path_str = os.environ.get('PATH', '')
                if str(bin_dir) not in path_str:
                    print(f"⚠️ 请将 {bin_dir} 添加到PATH环境变量")
                    print(f"   在 ~/.bashrc 或 ~/.zshrc 中添加:")
                    print(f'   export PATH="$HOME/.local/bin:$PATH"')
                
            except Exception as e:
                print(f"⚠️ 创建符号链接失败: {e}")
                print(f"   你可以手动创建链接或直接运行: python {cli_script}")
        
        elif system == "Windows":
            # Windows建议
            print("📝 Windows用户:")
            print(f"   1. 可以直接运行: python {cli_script}")
            print(f"   2. 或创建批处理文件 (.bat) 来运行")
        
        return True
        
    except Exception as e:
        print(f"❌ 设置命令行工具失败: {e}")
        return False

def create_example_files():
    """创建示例文件"""
    print("📝 创建示例文件...")
    
    try:
        current_dir = Path(__file__).parent
        examples_dir = current_dir / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        # 创建示例BV号列表
        bv_list = examples_dir / "bv_list.txt"
        with open(bv_list, 'w') as f:
            f.write("# B站视频BV号列表\n")
            f.write("# 每行一个BV号或视频URL\n")
            f.write("\n")
            f.write("# 示例视频（HermesAgent WebUI）\n")
            f.write("BV1txQGByERW\n")
            f.write("\n")
            f.write("# 可以添加更多视频\n")
            f.write("# https://www.bilibili.com/video/BV1xxxxxxx\n")
        
        print(f"✅ 示例文件已创建: {bv_list}")
        
        # 创建使用说明
        readme = examples_dir / "README.md"
        with open(readme, 'w') as f:
            f.write("# 使用示例\n")
            f.write("\n")
            f.write("## 基本使用\n")
            f.write("```bash\n")
            f.write("# 处理单个视频\n")
            f.write("bilibili-transcribe BV1txQGByERW\n")
            f.write("\n")
            f.write("# 批量处理\n")
            f.write("bilibili-transcribe --batch examples/bv_list.txt\n")
            f.write("```\n")
            f.write("\n")
            f.write("## 获取B站Cookie\n")
            f.write("1. 登录B站网页版\n")
            f.write("2. 按F12打开开发者工具\n")
            f.write("3. 进入Network标签页\n")
            f.write("4. 刷新页面\n")
            f.write("5. 找到任意请求，复制Request Headers中的Cookie\n")
            f.write("6. 粘贴到 ~/.bilibili_cookie.txt\n")
        
        print(f"✅ 使用说明已创建: {readme}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ 创建示例文件失败: {e}")
        return True  # 非关键错误

def run_tests():
    """运行测试"""
    print("🧪 运行基本测试...")
    
    try:
        # 测试导入模块
        import bilibili_transcriber
        from bilibili_transcriber import BilibiliTranscriber
        
        print("✅ 模块导入测试通过")
        
        # 测试配置读取
        import yaml
        config_file = Path(__file__).parent / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            print("✅ 配置文件读取测试通过")
        
        print("✅ 基本测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 导入测试失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def print_usage_instructions():
    """打印使用说明"""
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    
    print("\n📖 使用说明:")
    print("1. 编辑Cookie文件:")
    print(f"   nano ~/.bilibili_cookie.txt")
    print("   添加你的B站Cookie: SESSDATA=xxx; bili_jct=xxx; ...")
    
    print("\n2. 基本使用:")
    print("   # 处理单个视频")
    print("   bilibili-transcribe BV1txQGByERW")
    print("\n   # 查看帮助")
    print("   bilibili-transcribe --help")
    
    print("\n3. 批量处理:")
    print("   # 创建BV号列表文件")
    print("   echo 'BV1txQGByERW' > bv_list.txt")
    print("   echo 'BV1xxxxxxx' >> bv_list.txt")
    print("\n   # 批量处理")
    print("   bilibili-transcribe --batch bv_list.txt")
    
    print("\n4. 检查Cookie:")
    print("   bilibili-transcribe --check-cookie")
    
    print("\n5. 更新Cookie:")
    print('   bilibili-transcribe --update-cookie "SESSDATA=xxx; bili_jct=xxx"')
    
    print("\n🔧 高级功能:")
    print("   # 使用medium模型（更准确）")
    print("   bilibili-transcribe BV1txQGByERW --model medium")
    print("\n   # 输出JSON格式")
    print("   bilibili-transcribe BV1txQGByERW --format json")
    print("\n   # 保留音频文件")
    print("   bilibili-transcribe BV1txQGByERW --keep-audio")
    
    print("\n📁 输出目录:")
    print("   默认输出到: ./bilibili_transcripts/")
    print("   每个视频一个子目录，包含转录文件和音频文件")
    
    print("\n❓ 获取帮助:")
    print("   # 查看详细帮助")
    print("   bilibili-transcribe --help")
    print("\n   # 查看版本")
    print("   bilibili-transcribe --version")
    
    print("\n🐛 问题反馈:")
    print("   如果遇到问题，请检查日志文件:")
    print("   cat bilibili_transcriber.log")
    
    print("\n" + "=" * 60)

def main():
    """主安装函数"""
    print_header()
    
    # 检查前提条件
    if not check_python_version():
        sys.exit(1)
    
    if not check_ffmpeg():
        print("\n⚠️ FFmpeg未安装，部分功能可能受限")
        print("   是否继续安装？ (y/N): ", end='')
        choice = input().strip().lower()
        if choice != 'y':
            print("安装中止")
            sys.exit(1)
    
    # 安装步骤
    steps = [
        ("检查系统配置", check_system_capability),
        ("安装Python依赖", lambda: install_dependencies()),
        ("创建配置文件", create_config_files),
        ("设置命令行工具", setup_command_line),
        ("创建示例文件", create_example_files),
        ("运行基本测试", run_tests)
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n📋 步骤: {step_name}")
        if not step_func():
            print(f"❌ {step_name} 失败")
            success = False
            break
    
    if success:
        print_usage_instructions()
        print("\n✅ 安装成功完成！")
        sys.exit(0)
    else:
        print("\n❌ 安装失败，请检查错误信息")
        sys.exit(1)

if __name__ == '__main__':
    main()