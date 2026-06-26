#!/usr/bin/env python3
"""
ISV Providers 自动注册。

导入本包时会自动加载并注册所有 ISV Provider。
新增 ISV 时只需在本目录下新建 provider 目录，包含 cli.py 和 SKILL.md，
并在 base.py 中注册即可自动被发现。
"""

from scripts.isv.providers.zhangfei import provider  # noqa: F401
