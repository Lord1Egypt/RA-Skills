#!/usr/bin/env python3
"""
CLI-Anything Wrapper for OpenClaw
让 OpenClaw 可以调用 CLI-Anything 控制各种软件
"""

import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

# CLI-Anything 仓库路径
CLI_ANYTHING_PATH = Path.home() / ".openclaw/workspace/CLI-Anything"

@dataclass
class AppInfo:
    """软件信息"""
    name: str
    desc: str
    category: str
    harness_path: str
    requires: List[str]
    test_count: int = 0

# 支持的软件列表
SUPPORTED_APPS: Dict[str, AppInfo] = {
    "gimp": AppInfo(
        name="gimp",
        desc="图像处理 - 编辑、滤镜、批处理",
        category="设计",
        harness_path="gimp/agent-harness",
        requires=["gimp"],
        test_count=107
    ),
    "blender": AppInfo(
        name="blender",
        desc="3D建模/渲染/动画",
        category="3D",
        harness_path="blender/agent-harness",
        requires=["blender"],
        test_count=208
    ),
    "inkscape": AppInfo(
        name="inkscape",
        desc="矢量图处理",
        category="设计",
        harness_path="inkscape/agent-harness",
        requires=["inkscape"],
        test_count=202
    ),
    "libreoffice": AppInfo(
        name="libreoffice",
        desc="文档处理 - Word/Excel/PPT转换",
        category="办公",
        harness_path="libreoffice/agent-harness",
        requires=["libreoffice"],
        test_count=158
    ),
    "audacity": AppInfo(
        name="audacity",
        desc="音频编辑处理",
        category="音视频",
        harness_path="audacity/agent-harness",
        requires=["audacity"],
        test_count=161
    ),
    "obs": AppInfo(
        name="obs",
        desc="直播控制 - 录制、推流",
        category="音视频",
        harness_path="obs-studio/agent-harness",
        requires=["obs-studio"],
        test_count=153
    ),
    "comfyui": AppInfo(
        name="comfyui",
        desc="AI绘画工作流",
        category="AI",
        harness_path="comfyui/agent-harness",
        requires=["comfyui"],
        test_count=70
    ),
    "ollama": AppInfo(
        name="ollama",
        desc="本地大模型管理",
        category="AI",
        harness_path="ollama/agent-harness",
        requires=["ollama"],
        test_count=98
    ),
    "kdenlive": AppInfo(
        name="kdenlive",
        desc="视频剪辑",
        category="音视频",
        harness_path="kdenlive/agent-harness",
        requires=["kdenlive"],
        test_count=155
    ),
    "mermaid": AppInfo(
        name="mermaid",
        desc="流程图/图表生成",
        category="办公",
        harness_path="mermaid/agent-harness",
        requires=["nodejs"],
        test_count=10
    ),
    "zotero": AppInfo(
        name="zotero",
        desc="文献管理",
        category="学术",
        harness_path="zotero/agent-harness",
        requires=["zotero"],
        test_count=21
    ),
}

class CLIAnythingWrapper:
    """CLI-Anything 包装器"""
    
    def __init__(self):
        self.cli_path = CLI_ANYTHING_PATH
        self.plugin_path = self.cli_path / "cli-anything-plugin"
        
    def check_installation(self) -> bool:
        """检查 CLI-Anything 是否安装"""
        if not self.cli_path.exists():
            print("❌ CLI-Anything 未安装")
            print(f"\n📥 安装命令：")
            print(f"   git clone https://github.com/HKUDS/CLI-Anything {self.cli_path}")
            print(f"   cd {self.cli_path}")
            print(f"   ./setup.sh")
            return False
        
        if not self.plugin_path.exists():
            print(f"⚠️  CLI-Anything 目录存在，但 plugin 不完整")
            return False
            
        print(f"✅ CLI-Anything 已安装: {self.cli_path}")
        return True
    
    def list_apps(self, category: Optional[str] = None):
        """列出所有支持的软件"""
        print("\n📦 CLI-Anything 支持的软件列表：\n")
        
        # 按分类分组
        categories: Dict[str, List[AppInfo]] = {}
        for app in SUPPORTED_APPS.values():
            cat = app.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(app)
        
        # 显示
        for cat, apps in sorted(categories.items()):
            if category and cat != category:
                continue
            print(f"\n【{cat}】")
            for app in sorted(apps, key=lambda x: x.name):
                # 检查 harness 是否存在
                harness_exists = (self.cli_path / app.harness_path).exists()
                status = "✅" if harness_exists else "⬜"
                print(f"  {status} {app.name:12} - {app.desc}")
                print(f"     📁 {app.harness_path} ({app.test_count} tests)")
        
        print(f"\n总计: {len(SUPPORTED_APPS)} 个软件")
        print(f"\n📂 CLI-Anything 路径: {self.cli_path}")
        
        # 检查 harness 统计
        existing = sum(1 for a in SUPPORTED_APPS.values() 
                      if (self.cli_path / a.harness_path).exists())
        print(f"📊 Harness 已下载: {existing}/{len(SUPPORTED_APPS)}")
    
    def check_app_available(self, app_name: str) -> tuple[bool, Optional[AppInfo]]:
        """检查软件是否可用"""
        if app_name not in SUPPORTED_APPS:
            return False, None
        
        app = SUPPORTED_APPS[app_name]
        harness_full_path = self.cli_path / app.harness_path
        
        if not harness_full_path.exists():
            print(f"❌ {app_name} 的 harness 未找到")
            print(f"   路径: {harness_full_path}")
            print(f"\n📥 尝试从 CLI-Anything 获取...")
            return False, app
        
        return True, app
    
    def run_app(self, app_name: str, args: str, dry_run: bool = False) -> int:
        """运行指定软件"""
        available, app = self.check_app_available(app_name)
        
        if not available:
            if app:
                print(f"\n💡 {app.name} 信息：")
                print(f"   描述: {app.desc}")
                print(f"   依赖: {', '.join(app.requires)}")
                print(f"\n请确保：")
                print(f"1. CLI-Anything 完整克隆: git clone --recursive")
                print(f"2. {app_name} 软件已安装: {', '.join(app.requires)}")
            return 1
        
        harness_path = self.cli_path / app.harness_path
        
        print(f"\n🚀 准备运行 {app_name}")
        print(f"📁 Harness: {harness_path}")
        print(f"📋 参数: {args or '(无)'}")
        print(f"📝 描述: {app.desc}")
        
        if dry_run:
            print(f"\n🏃 模拟运行模式 (dry-run)")
            print(f"   实际会执行: cd {harness_path} && ./cli-anything {args}")
            return 0
        
        # 检查 CLI 脚本是否存在
        cli_script = harness_path / "cli-anything"
        if not cli_script.exists():
            # 尝试找其他可执行文件
            candidates = list(harness_path.glob("*.py")) + list(harness_path.glob("*.sh"))
            if candidates:
                cli_script = candidates[0]
            else:
                print(f"❌ 未找到可执行脚本")
                print(f"   请检查 {harness_path} 内容")
                return 1
        
        # 执行
        print(f"\n▶️  执行: {cli_script} {args}")
        try:
            result = subprocess.run(
                [str(cli_script)] + (args.split() if args else []),
                cwd=harness_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.stdout:
                print(f"\n📤 输出:\n{result.stdout}")
            if result.stderr:
                print(f"\n⚠️  错误:\n{result.stderr}")
            
            if result.returncode == 0:
                print(f"\n✅ {app_name} 执行成功")
            else:
                print(f"\n❌ {app_name} 执行失败 (code: {result.returncode})")
            
            return result.returncode
            
        except subprocess.TimeoutExpired:
            print(f"\n⏱️  执行超时 (5分钟)")
            return 1
        except Exception as e:
            print(f"\n💥 执行出错: {e}")
            return 1
    
    def install_cli_anything(self):
        """安装 CLI-Anything"""
        print("📥 开始安装 CLI-Anything...")
        print(f"目标路径: {self.cli_path}")
        
        cmds = [
            f"git clone --recursive https://github.com/HKUDS/CLI-Anything {self.cli_path}",
            f"cd {self.cli_path} && ./setup.sh 2>/dev/null || pip install -e . 2>/dev/null || echo 'setup.sh 不存在，尝试手动安装'",
        ]
        
        for cmd in cmds:
            print(f"\n$ {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0 and "already exists" not in result.stderr:
                print(f"⚠️  命令可能失败: {result.stderr[:200]}")
        
        print("\n✅ 安装命令执行完成")
        print("请检查安装结果，或手动运行 setup.sh")
    
    def show_info(self):
        """显示详细信息"""
        print("\nℹ️  CLI-Anything Wrapper 信息\n")
        print(f"版本: 1.0.0")
        print(f"作者: OpenClaw")
        print(f"CLI-Anything 路径: {self.cli_path}")
        print(f"Plugin 路径: {self.plugin_path}")
        print(f"\n支持的软件: {len(SUPPORTED_APPS)} 个")
        print(f"\n文档:")
        print(f"  - CLI-Anything README: {self.cli_path}/README.md")
        print(f"  - Harness 方法: {self.plugin_path}/HARNESS.md")


def main():
    parser = argparse.ArgumentParser(
        description="CLI-Anything Wrapper for OpenClaw - 让 AI 控制任意软件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看支持的软件
  %(prog)s --list
  
  # 运行 GIMP 处理图片
  %(prog)s --app gimp --args "photo.jpg --filter blur"
  
  # 只显示设计类软件
  %(prog)s --list --category 设计
  
  # 模拟运行（不实际执行）
  %(prog)s --app blender --args "render.blend" --dry-run
  
  # 安装 CLI-Anything
  %(prog)s --install
        """
    )
    
    parser.add_argument("--list", "-l", action="store_true", 
                       help="列出支持的软件")
    parser.add_argument("--app", "-a", type=str,
                       help="软件名称 (如: gimp, blender)")
    parser.add_argument("--args", type=str, default="",
                       help="传递给软件的参数")
    parser.add_argument("--category", "-c", type=str,
                       help="按分类筛选 (如: 设计, AI, 办公)")
    parser.add_argument("--dry-run", "-n", action="store_true",
                       help="模拟运行，不实际执行")
    parser.add_argument("--install", action="store_true",
                       help="安装 CLI-Anything")
    parser.add_argument("--info", "-i", action="store_true",
                       help="显示详细信息")
    parser.add_argument("--json", "-j", action="store_true",
                       help="以 JSON 格式输出")
    
    args = parser.parse_args()
    
    wrapper = CLIAnythingWrapper()
    
    # 处理各种命令
    if args.info:
        wrapper.show_info()
        return 0
    
    if args.install:
        wrapper.install_cli_anything()
        return 0
    
    if args.list:
        if args.json:
            # JSON 输出
            apps_data = {
                name: asdict(info) 
                for name, info in SUPPORTED_APPS.items()
            }
            print(json.dumps(apps_data, ensure_ascii=False, indent=2))
        else:
            wrapper.list_apps(category=args.category)
        return 0
    
    if args.app:
        # 先检查 CLI-Anything 是否安装
        if not wrapper.check_installation():
            return 1
        return wrapper.run_app(args.app, args.args, dry_run=args.dry_run)
    
    # 默认显示帮助
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
