#!/usr/bin/env python3
"""
ISV 通用层

提供多 ISV Provider 插件式架构：
- base.py: ISV Provider 基类 + 全局注册表
- providers/: 各 ISV 实现（每个 ISV 一个目录，包含独立的 cli.py 和业务脚本）
"""
