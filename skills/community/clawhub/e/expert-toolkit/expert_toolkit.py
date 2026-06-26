#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专家工具箱 - Expert Toolkit
入口文件，OpenClaw调用入口
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from expert_toolkit import ExpertLibrary, parse_input, handle_command, handle_auto_match

def run(user_input: str) -> str:
    """Skill主入口，OpenClaw调用这个函数"""
    library = ExpertLibrary()
    
    if library.count_total() == 0:
        return "❌ 未找到专家角色，请确保已经将角色存入 `knowledge/agency-orchestrator/roles/` 目录。"
    
    command, args, is_auto = parse_input(user_input)
    
    if is_auto:
        return handle_auto_match(args, library)
    else:
        return handle_command(command, args, library)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        print(run(user_input))
    else:
        print("Usage: python expert_toolkit.py '<command> <args>'")
