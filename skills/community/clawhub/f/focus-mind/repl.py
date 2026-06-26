#!/usr/bin/env python3
"""
FocusMind 交互式 REPL
提供交互式界面来使用 FocusMind
"""

import sys
import os
import readline
from typing import Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from focusmind import (
    FocusMind,
    analyze_context_health,
    generate_summary,
    extract_goals,
    need_cleanup,
    format_health_report,
    format_summary_markdown,
    format_goals_markdown
)


class FocusMindREPL:
    """交互式 REPL"""
    
    def __init__(self):
        self.fm = FocusMind()
        self.context = ""
        self.commands = {
            "help": self.cmd_help,
            "health": self.cmd_health,
            "summarize": self.cmd_summarize,
            "goals": self.cmd_goals,
            "all": self.cmd_all,
            "add": self.cmd_add,
            "clear": self.cmd_clear,
            "load": self.cmd_load,
            "save": self.cmd_save,
            "quit": self.cmd_quit,
            "exit": self.cmd_quit,
        }
    
    def cmd_help(self, args):
        """显示帮助"""
        print("""
╔══════════════════════════════════════╗
║       FocusMind 交互式命令           ║
╠══════════════════════════════════════╣
║ help         - 显示帮助              ║
║ health       - 检查健康度            ║
║ summarize    - 生成摘要              ║
║ goals       - 提取目标               ║
║ all          - 完整分析              ║
║ add <text>   - 添加上下文            ║
║ clear        - 清除上下文            ║
║ load <file>  - 加载文件              ║
║ save <file> - 保存上下文            ║
║ quit/exit   - 退出                  ║
╚══════════════════════════════════════╝
        """)
    
    def cmd_health(self, args):
        """健康度检查"""
        if not self.context:
            print("❌ 上下文为空，请先添加内容 (add <text>)")
            return
        
        health = analyze_context_health(self.context)
        print(format_health_report(health))
    
    def cmd_summarize(self, args):
        """生成摘要"""
        if not self.context:
            print("❌ 上下文为空，请先添加内容")
            return
        
        # 解析风格参数
        style = "structured"
        if args:
            style = args[0]
        
        summary = generate_summary(self.context, style=style)
        print(format_summary_markdown(summary))
    
    def cmd_goals(self, args):
        """提取目标"""
        if not self.context:
            print("❌ 上下文为空，请先添加内容")
            return
        
        goals = extract_goals(self.context)
        print(format_goals_markdown(goals))
    
    def cmd_all(self, args):
        """完整分析"""
        if not self.context:
            print("❌ 上下文为空，请先添加内容")
            return
        
        report = self.fm.format_report(self.context)
        print(report)
    
    def cmd_add(self, args):
        """添加上下文"""
        if not args:
            print("❌ 请输入要添加的内容")
            return
        
        text = " ".join(args)
        self.context += " " + text
        print(f"✓ 已添加 {len(text)} 字符")
        print(f"  当前上下文长度: {len(self.context)} 字符")
    
    def cmd_clear(self, args):
        """清除上下文"""
        self.context = ""
        print("✓ 上下文已清除")
    
    def cmd_load(self, args):
        """加载文件"""
        if not args:
            print("❌ 请指定文件名")
            return
        
        filepath = args[0]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.context = f.read()
            print(f"✓ 已加载 {len(self.context)} 字符")
        except Exception as e:
            print(f"❌ 加载失败: {e}")
    
    def cmd_save(self, args):
        """保存上下文"""
        if not self.context:
            print("❌ 上下文为空")
            return
        
        if not args:
            print("❌ 请指定文件名")
            return
        
        filepath = args[0]
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.context)
            print(f"✓ 已保存到 {filepath}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def cmd_quit(self, args):
        """退出"""
        print("👋 再见!")
        return True
    
    def run(self):
        """运行 REPL"""
        print("""
╔══════════════════════════════════════╗
║     FocusMind 交互式模式            ║
║  输入 'help' 查看可用命令            ║
║  输入 'quit' 退出                    ║
╚══════════════════════════════════════╝
        """)
        
        while True:
            try:
                line = input("focus-mind> ").strip()
                if not line:
                    continue
                
                parts = line.split()
                cmd = parts[0].lower()
                args = parts[1:]
                
                if cmd in self.commands:
                    should_quit = self.commands[cmd](args)
                    if should_quit:
                        break
                else:
                    print(f"❌ 未知命令: {cmd}")
                    print("  输入 'help' 查看可用命令")
            
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


def main():
    repl = FocusMindREPL()
    repl.run()


if __name__ == "__main__":
    main()
