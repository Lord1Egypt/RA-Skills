#!/usr/bin/env python3
"""
上下文优化器安装和测试脚本
"""

import os
import sys
import subprocess

def check_prerequisites():
    """检查前提条件"""
    print("🔍 检查系统环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python版本过低: {sys.version}")
        print("   需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查工作空间目录
    workspace_path = os.path.expanduser("~/.openclaw/workspace")
    if not os.path.exists(workspace_path):
        print(f"❌ OpenClaw工作空间不存在: {workspace_path}")
        print("   请先安装和配置OpenClaw")
        return False
    
    print(f"✅ OpenClaw工作空间: {workspace_path}")
    
    # 检查必要文件
    required_files = ["AGENTS.md", "SOUL.md"]
    missing_files = []
    
    for filename in required_files:
        filepath = os.path.join(workspace_path, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
    
    if missing_files:
        print(f"⚠️  缺少文件: {', '.join(missing_files)}")
        print("   优化器仍可工作，但功能可能受限")
    else:
        print("✅ 必要文件存在")
    
    return True

def install_optimizer():
    """安装优化器"""
    print("\n📦 安装上下文优化器...")
    
    # 获取当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查是否已在技能目录
    skills_dir = os.path.expanduser("~/.openclaw/skills")
    target_dir = os.path.join(skills_dir, "context-optimizer")
    
    if current_dir == target_dir:
        print("✅ 优化器已在正确位置")
        return True
    
    # 复制文件到技能目录
    try:
        import shutil
        
        # 创建目标目录
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制所有文件
        for filename in os.listdir(current_dir):
            if filename.endswith(('.py', '.md')):
                src = os.path.join(current_dir, filename)
                dst = os.path.join(target_dir, filename)
                shutil.copy2(src, dst)
                print(f"  复制: {filename}")
        
        print(f"✅ 优化器安装完成: {target_dir}")
        return True
        
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False

def test_optimizer():
    """测试优化器功能"""
    print("\n🧪 测试优化器功能...")
    
    workspace_path = os.path.expanduser("~/.openclaw/workspace")
    optimizer_script = os.path.join(workspace_path, "context_optimizer.py")
    
    # 如果脚本不在工作空间，从技能目录复制
    if not os.path.exists(optimizer_script):
        skills_dir = os.path.expanduser("~/.openclaw/skills/context-optimizer")
        source_script = os.path.join(skills_dir, "context_optimizer.py")
        
        if os.path.exists(source_script):
            import shutil
            shutil.copy2(source_script, optimizer_script)
            print(f"✅ 复制优化器脚本到工作空间")
        else:
            print("❌ 找不到优化器脚本")
            return False
    
    # 测试分析功能
    print("1. 测试分析功能...")
    try:
        result = subprocess.run(
            [sys.executable, optimizer_script, "analyze"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 分析功能正常")
            
            # 保存报告
            report_file = os.path.join(workspace_path, "initial_analysis_report.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"   报告已保存: {report_file}")
            
            return True
        else:
            print(f"❌ 分析失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 分析超时")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def create_sample_config():
    """创建示例配置"""
    print("\n⚙️  创建示例配置...")
    
    config_content = {
        "optimization_strategy": "balanced",
        "target_reduction": 60,
        "preserve_format": True,
        "backup_original": True,
        "auto_approve": False,
        "skill_extraction": {
            "min_complexity": 3,
            "reuse_potential": "high",
            "template_library": True,
            "auto_test": True
        },
        "automation": {
            "schedule": "weekly",
            "report_delivery": True,
            "rollback_enabled": True
        }
    }
    
    config_file = os.path.expanduser("~/.openclaw/workspace/context_optimizer_config.json")
    
    import json
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_content, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 配置创建完成: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 配置创建失败: {e}")
        return False

def setup_cron_job():
    """设置定期优化任务"""
    print("\n⏰ 设置定期优化任务...")
    
    try:
        # 检查openclaw命令是否可用
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print("⚠️  openclaw命令不可用，跳过cron设置")
            return False
        
        # 创建cron任务
        cron_command = (
            'openclaw cron add '
            '--name "weekly-context-optimization" '
            '--cron "0 2 * * 1" '
            '--message "执行每周上下文优化: 分析工作空间，优化文件，提取新Skill" '
            '--description "每周一凌晨2点自动优化上下文"'
        )
        
        print(f"   执行命令: {cron_command}")
        print("   请手动执行以上命令创建cron任务")
        
        # 提供手动执行说明
        print("\n💡 手动设置说明:")
        print("1. 复制上面的openclaw cron add命令")
        print("2. 在终端中执行")
        print("3. 使用 'openclaw cron list' 验证任务")
        
        return True
        
    except Exception as e:
        print(f"❌ cron设置检查失败: {e}")
        return False

def main():
    """主安装流程"""
    print("=" * 60)
    print("🔄 上下文优化器安装向导")
    print("=" * 60)
    
    # 步骤1: 检查环境
    if not check_prerequisites():
        print("\n❌ 环境检查失败，请解决问题后重试")
        return 1
    
    # 步骤2: 安装优化器
    if not install_optimizer():
        print("\n❌ 安装失败")
        return 1
    
    # 步骤3: 创建配置
    if not create_sample_config():
        print("\n⚠️  配置创建失败，但优化器仍可工作")
    
    # 步骤4: 测试功能
    if not test_optimizer():
        print("\n⚠️  测试失败，但优化器可能仍可工作")
    
    # 步骤5: 设置自动化
    setup_cron_job()
    
    print("\n" + "=" * 60)
    print("🎉 安装完成!")
    print("=" * 60)
    
    print("\n📋 下一步:")
    print("1. 查看初始分析报告: initial_analysis_report.md")
    print("2. 尝试优化文件: python context_optimizer.py optimize all")
    print("3. 提取Skill示例: python context_optimizer.py extract-skill test-skill")
    print("4. 调整配置: 编辑context_optimizer_config.json")
    
    print("\n📚 更多信息:")
    print("- 查看SKILL.md了解完整功能")
    print("- 查看EXAMPLES.md获取使用示例")
    print("- 运行 'python context_optimizer.py --help' 查看命令帮助")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())