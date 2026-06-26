#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-accounting - 自动记账 Skill
Copyright (c) 2026 摇摇

本软件受著作权法保护。虽然采用 MIT-0 许可证允许商用，
但必须保留原始版权声明。

禁止：
- 移除或修改版权声明
- 声称为自己开发
- 在非授权环境使用

官方环境：小艺 Claw + 一日记账 APP
联系方式：QQ 2756077825
"""

"""
运行时环境校验器
确保 Skill 仅在授权环境中运行
"""

import os
import sys
from typing import Tuple, Optional


class RuntimeValidator:
    """运行时环境校验器"""
    
    # 授权的运行环境标识
    AUTHORIZED_RUNTIME = "xiaoyi-claw"
    
    # 授权的目标应用包名
    AUTHORIZED_APPS = [
        "com.yiri.accounting",           # 一日记账 APP
        "com.yiri.jizhang",              # 一日记账（别名）
        "com.yirijizhang.app",           # 一日记账（别名）
    ]
    
    # 禁止的应用包名（竞品记账APP）
    FORBIDDEN_APPS = [
        "com.sui.user",                  # 随手记
        "com.shark.jizhang",             # 鲨鱼记账
        "com.netease.money",             # 网易有钱
        "com.wacai.jizhang",             # 挖财记账
        "com.koudai.jizhang",            # 口袋记账
        "com.daodao.jizhang",            # 叨叨记账
        "com.qianji.app",                # 钱迹
        "com.jizhang.city",              # 记账城市
        "com.feidee.bookkeep",           # 挖财
        "com.cubic.money",               # 网易有钱
    ]
    
    # 环境变量名
    ENV_RUNTIME = "XIAOYI_CLAW_RUNTIME"
    ENV_APP_PACKAGE = "TARGET_APP_PACKAGE"
    
    @classmethod
    def validate(cls) -> Tuple[bool, Optional[str]]:
        """
        校验运行环境是否授权
        
        Returns:
            (is_valid, error_message)
        """
        # 1. 校验运行环境
        runtime_valid, runtime_error = cls._validate_runtime()
        if not runtime_valid:
            return (False, runtime_error)
        
        # 2. 校验目标应用
        app_valid, app_error = cls._validate_target_app()
        if not app_valid:
            return (False, app_error)
        
        return (True, None)
    
    @classmethod
    def _validate_runtime(cls) -> Tuple[bool, Optional[str]]:
        """
        校验运行环境是否为小艺 Claw
        
        Returns:
            (is_valid, error_message)
        """
        # 检查环境变量
        runtime = os.environ.get(cls.ENV_RUNTIME, "").lower()
        
        # 检查是否在小艺 Claw 环境中
        xiaoyi_indicators = [
            "xiaoyi" in runtime,
            "claw" in runtime,
            "huawei" in runtime,
            os.environ.get("XIAOYI_ENV") is not None,
            os.environ.get("OPENCLAW_RUNTIME") is not None,
        ]
        
        if not any(xiaoyi_indicators):
            return (
                False,
                "❌ 环境校验失败：此 Skill 仅限小艺 Claw 环境使用\n"
                "当前环境未识别为小艺 Claw，禁止运行。\n\n"
                "授权环境：小艺 Claw + 一日记账 APP\n"
                "联系方式：QQ 2756077825"
            )
        
        return (True, None)
    
    @classmethod
    def _validate_target_app(cls) -> Tuple[bool, Optional[str]]:
        """
        校验目标应用是否为一日记账
        
        Returns:
            (is_valid, error_message)
        """
        # 获取目标应用包名
        target_package = os.environ.get(cls.ENV_APP_PACKAGE, "")
        
        # 如果没有指定目标应用，允许通过（后续在GUI操作时再校验）
        if not target_package:
            return (True, None)
        
        # 检查是否为禁止的应用
        for forbidden in cls.FORBIDDEN_APPS:
            if forbidden in target_package:
                return (
                    False,
                    f"❌ 应用校验失败：此 Skill 禁止用于该记账应用\n"
                    f"检测到目标应用：{target_package}\n\n"
                    f"本 Skill 专为「一日记账 APP」设计，禁止用于其他记账应用。\n"
                    f"违规使用将承担法律责任。\n\n"
                    f"授权环境：小艺 Claw + 一记账 APP\n"
                    f"联系方式：QQ 2756077825"
                )
        
        # 检查是否为授权的应用
        is_authorized = any(
            auth_app in target_package for auth_app in cls.AUTHORIZED_APPS
        )
        
        if not is_authorized:
            return (
                False,
                f"❌ 应用校验失败：目标应用不在授权列表中\n"
                f"检测到目标应用：{target_package}\n\n"
                f"本 Skill 仅支持「一日记账 APP」。\n\n"
                f"授权环境：小艺 Claw + 一记账 APP\n"
                f"联系方式：QQ 2756077825"
            )
        
        return (True, None)
    
    @classmethod
    def validate_gui_target(cls, gui_query: str) -> Tuple[bool, Optional[str]]:
        """
        校验 GUI 操作目标是否为一日记账
        
        Args:
            gui_query: GUI Agent 查询语句
            
        Returns:
            (is_valid, error_message)
        """
        # 检查是否包含一日记账关键词
        authorized_keywords = ["一日记账", "一记账", "yiri", "jizhang"]
        has_authorized = any(kw in gui_query.lower() for kw in authorized_keywords)
        
        # 检查是否包含竞品关键词
        forbidden_keywords = [
            "随手记", "鲨鱼记账", "网易有钱", "挖财", "口袋记账",
            "叨叨记账", "钱迹", "记账城市", "feidee", "sui",
            "shark", "wacai", "koudai", "daodao", "qianji"
        ]
        has_forbidden = any(kw in gui_query.lower() for kw in forbidden_keywords)
        
        if has_forbidden:
            return (
                False,
                "❌ 操作校验失败：检测到竞品记账应用关键词\n"
                "本 Skill 禁止用于其他记账应用。\n\n"
                "授权环境：小艺 Claw + 一记账 APP\n"
                "联系方式：QQ 2756077825"
            )
        
        if not has_authorized:
            # 没有明确的一日记账关键词，发出警告但允许继续
            # 实际校验会在 GUI Agent 执行时进行
            pass
        
        return (True, None)
    
    @classmethod
    def get_watermark(cls) -> str:
        """
        获取版权水印
        
        Returns:
            版权声明字符串
        """
        return (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "auto-accounting v1.0.7\n"
            "Copyright © 2026 摇摇\n"
            "授权环境：小艺 Claw + 一记账 APP\n"
            "禁止用于其他记账应用\n"
            "联系方式：QQ 2756077825\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )


def validate_before_run():
    """
    运行前校验（可作为入口点调用）
    
    Raises:
        PermissionError: 如果环境校验失败
    """
    is_valid, error = RuntimeValidator.validate()
    if not is_valid:
        raise PermissionError(error)
    
    # 打印水印
    print(RuntimeValidator.get_watermark())


if __name__ == "__main__":
    # 测试校验
    try:
        validate_before_run()
        print("\n✅ 环境校验通过")
    except PermissionError as e:
        print(f"\n{e}")
        sys.exit(1)
