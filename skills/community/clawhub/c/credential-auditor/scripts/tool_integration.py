#!/usr/bin/env python3
"""
第三方工具集成接口
集成Hydra、Medusa、Ncrack等专业工具
"""

import shutil
import argparse

class ToolIntegration:
    """第三方工具集成"""
    
    def __init__(self):
        self.available_tools = self._check_tools()
    
    def _check_tools(self):
        """检查工具安装状态"""
        tools = {
            'hydra': 'hydra',
            'medusa': 'medusa',
            'ncrack': 'ncrack',
            'nmap': 'nmap'
        }
        
        available = {}
        for name, command in tools.items():
            available[name] = shutil.which(command) is not None
        
        return available
    
    def check_tools(self):
        """显示工具安装状态"""
        print("\n第三方工具安装状态:")
        print("="*60)
        
        for tool, installed in self.available_tools.items():
            status = "✓ 已安装" if installed else "✗ 未安装"
            print(f"  {tool:15} {status}")
        
        print("\n安装建议:")
        if not self.available_tools['hydra']:
            print("  - Hydra: brew install hydra (macOS)")
            print("           sudo apt-get install hydra (Ubuntu)")
        
        if not self.available_tools['medusa']:
            print("  - Medusa: brew install medusa (macOS)")
            print("            sudo apt-get install medusa (Ubuntu)")


def main():
    parser = argparse.ArgumentParser(description="第三方工具集成接口")
    
    parser.add_argument('--check-tools', action='store_true', help='检查工具安装状态')
    
    args = parser.parse_args()
    
    integration = ToolIntegration()
    
    if args.check_tools:
        integration.check_tools()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
