#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-literature 的 P3 标准接入 wrapper。

P3 层要求 build_payload 签名 = build(env) / build(env, **kwargs)。
但 bug_report.build_report 是独立参数形态（skill, skill_version, ...）。
本文件做一次性适配：从 env 字典解包为 build_report 的命名参数。
"""

import bug_report as _br


def build_payload(env: dict) -> dict:
    """把 env 字典适配到 bug_report.build_report 的签名。"""
    # 直接透传（build_report 内部会 sanitize）
    return _br.build_report(
        skill=env.get("skill", "ct-literature"),
        skill_version=env.get("skill_version", "0.0.0"),
        test=env.get("test", "ctqa"),
        error_type=env.get("error_type", "error"),
        error_code=env.get("error_code", ""),
        engine_status=env.get("engine_status", ""),
        description=env.get("description", ""),
        locale=env.get("locale"),
        attempts=env.get("attempts", 1),
    )
