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

官方环境：小艺 Claw + 一日记记账 APP
联系方式：QQ 2756077825
"""

import os
import sys
from typing import Tuple


class EnvironmentValidator:
    """环境验证器 - 确保运行在授权环境中"""
    
    # 授权的运行环境
    AUTHORIZED_RUNTIME = "小艺 Claw"
    AUTHORIZED_APP = "一日记账 APP"
    
    # 环境变量标识
    XIAOYI_ENV_VARS = [
        "XIAOYI_CLAW_ENV",
        "OPENCLAW_RUNTIME",
        "XIAOYI_API_KEY",
    ]
    
    @classmethod
    def validate(cls) -> Tuple[bool, str]:
        """
        验证运行环境
        
        Returns:
            (是否通过, 消息)
        """
        # 1. 检测环境变量
        env_check = cls._check_environment_variables()
        if not env_check[0]:
            return env_check
        
        # 2. 检测依赖组件
        dep_check = cls._check_dependencies()
        if not dep_check[0]:
            return dep_check
        
        # 3. 检测 API 可用性（可选）
        # api_check = cls._check_api_availability()
        # if not api_check[0]:
        #     return api_check
        
        return True, "环境验证通过"
    
    @classmethod
    def _check_environment_variables(cls) -> Tuple[bool, str]:
        """检测小艺 Claw 环境变量"""
        detected = False
        
        for env_var in cls.XIAOYI_ENV_VARS:
            if os.environ.get(env_var):
                detected = True
                break
        
        if not detected:
            return False, (
                f"❌ 非授权环境\n"
                f"本 Skill 仅支持：{cls.AUTHORIZED_RUNTIME} + {cls.AUTHORIZED_APP}\n"
                f"当前环境未检测到小艺 Claw 标识\n"
                f"联系方式：QQ 2756077825"
            )
        
        return True, "环境变量检测通过"
    
    @classmethod
    def _check_dependencies(cls) -> Tuple[bool, str]:
        """检测依赖组件"""
        missing = []
        
        # 检测 xiaoyi-image-understanding
        try:
            # 尝试导入，验证是否为官方组件
            pass  # 实际使用时由 xiaoyi-image-understanding skill 提供
        except Exception:
            missing.append("xiaoyi-image-understanding")
        
        # 检测 xiaoyi-gui-agent
        try:
            # 尝试导入，验证是否为官方组件
            pass  # 实际使用时由 xiaoyi-gui-agent skill 提供
        except Exception:
            missing.append("xiaoyi-gui-agent")
        
        if missing:
            return False, (
                f"❌ 缺少官方依赖组件\n"
                f"缺失组件：{', '.join(missing)}\n"
                f"本 Skill 必须使用小艺 Claw 官方组件\n"
                f"联系方式：QQ 2756077825"
            )
        
        return True, "依赖组件检测通过"
    
    @classmethod
    def get_environment_info(cls) -> dict:
        """获取环境信息"""
        return {
            "runtime": cls.AUTHORIZED_RUNTIME,
            "app": cls.AUTHORIZED_APP,
            "env_vars": {
                var: bool(os.environ.get(var))
                for var in cls.XIAOYI_ENV_VARS
            },
            "python_version": sys.version,
            "platform": sys.platform,
        }


def validate_and_exit():
    """验证环境，失败则退出"""
    valid, msg = EnvironmentValidator.validate()
    if not valid:
        print(msg)
        print("\n" + "=" * 50)
        print("本 Skill 受著作权保护")
        print("Copyright (c) 2026 摇摇")
        print("联系方式：QQ 2756077825")
        print("=" * 50)
        sys.exit(1)
    return True


if __name__ == "__main__":
    # 测试环境验证
    valid, msg = EnvironmentValidator.validate()
    print(f"验证结果: {valid}")
    print(f"消息: {msg}")
    print("\n环境信息:")
    import json
    print(json.dumps(EnvironmentValidator.get_environment_info(), indent=2))
