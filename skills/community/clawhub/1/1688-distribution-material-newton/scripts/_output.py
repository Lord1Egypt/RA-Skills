#!/usr/bin/env python3
"""
统一输出工具 — 代理层

旧模块路径兼容：所有 import 转发到 scripts._sys._output
"""
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from scripts._sys._output import *
