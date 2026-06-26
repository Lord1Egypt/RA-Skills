#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
业务命令模板 - 请根据实际需求修改

用法：python3 scripts/cli.py example your_function --param1=value
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.example.service import your_function as _your_function


def your_function(param1: str = "", param2: str = ""):
    """执行 your_function 并输出标准 JSON"""
    try:
        if not param1:
            print_output(False, "❌ 缺少必填参数 param1", {})
            return

        result = _your_function(param1=param1, param2=param2 or None)
        print_output(True, "✅ 调用成功", result)
    except Exception as e:
        print_error(e)
