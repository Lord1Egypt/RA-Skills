#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云域名安全操作示例

演示如何正确使用需要二次确认的资金操作

⚠️ 安全规则：
所有涉及订单和资金操作的 API 调用，必须经过用户明确二次确认后才能执行！
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from aliyun_domain import AliyunDomainClient


def example_register_domain_with_confirmation():
    """示例：带确认流程的域名注册"""
    
    client = AliyunDomainClient()
    
    # 步骤 1：准备注册信息（不实际提交）
    print("=" * 80)
    print("步骤 1: 准备注册信息")
    print("=" * 80)
    
    prepare_result = client.prepare_domain_registration(
        domain_name="example.xyz",
        years=1,
        registrant_profile_id=24485442  # 使用已实名的模板
    )
    
    if not prepare_result.get('success'):
        print(f"❌ 准备失败：{prepare_result.get('message')}")
        return
    
    # 步骤 2：展示确认信息给用户
    print("\n" + prepare_result.get('confirmation_message'))
    
    # 步骤 3：等待用户确认（在实际应用中，这里等待用户输入）
    # user_input = input("\n请输入确认：").strip().lower()
    # if user_input not in ['确认', 'confirm', 'yes', 'ok', '是']:
    #     print("❌ 用户取消操作")
    #     return
    
    # 示例中直接模拟用户确认
    print("\n✅ 模拟用户已确认")
    
    # 步骤 4：执行注册（必须设置 confirmed=True）
    print("\n" + "=" * 80)
    print("步骤 4: 执行注册")
    print("=" * 80)
    
    try:
        result = client.register_domain(
            domain_name="example.xyz",
            years=1,
            registrant_profile_id=24485442,
            confirmed=True  # ⚠️ 必须设置为 True
        )
        
        print(f"✅ 注册成功！")
        print(f"任务编号：{result.get('TaskNo')}")
        print(f"请求 ID: {result.get('RequestId')}")
        
    except ValueError as e:
        print(f"❌ 安全拦截：{e}")
    except Exception as e:
        print(f"❌ 注册失败：{e}")


def example_renew_domain_with_confirmation():
    """示例：带确认流程的域名续费"""
    
    client = AliyunDomainClient()
    
    # 步骤 1：准备续费信息
    print("\n" + "=" * 80)
    print("步骤 1: 准备续费信息")
    print("=" * 80)
    
    prepare_result = client.prepare_domain_renewal(
        domain_name="shenyue.xyz",
        years=1
    )
    
    if not prepare_result.get('success'):
        print(f"❌ 准备失败：{prepare_result.get('message')}")
        return
    
    # 步骤 2：展示确认信息
    print("\n" + prepare_result.get('confirmation_message'))
    
    # 步骤 3：等待用户确认
    # user_input = input("\n请输入确认：").strip().lower()
    # if user_input not in ['确认', 'confirm', 'yes', 'ok', '是']:
    #     print("❌ 用户取消操作")
    #     return
    
    print("\n✅ 模拟用户已确认")
    
    # 步骤 4：执行续费
    print("\n" + "=" * 80)
    print("步骤 4: 执行续费")
    print("=" * 80)
    
    try:
        result = client.renew_domain(
            domain_name="shenyue.xyz",
            years=1,
            confirmed=True  # ⚠️ 必须设置为 True
        )
        
        print(f"✅ 续费成功！")
        print(f"任务编号：{result.get('TaskNo')}")
        
    except ValueError as e:
        print(f"❌ 安全拦截：{e}")
    except Exception as e:
        print(f"❌ 续费失败：{e}")


def example_without_confirmation_will_fail():
    """示例：未确认直接调用会被拦截"""
    
    client = AliyunDomainClient()
    
    print("\n" + "=" * 80)
    print("示例：未确认直接调用（会被拦截）")
    print("=" * 80)
    
    try:
        # ❌ 错误做法：未确认直接调用，且 confirmed=False（默认值）
        result = client.register_domain(
            domain_name="test.xyz",
            years=1,
            confirmed=False  # 或者不传这个参数
        )
        print(f"✅ 注册成功（这不应该发生）")
        
    except ValueError as e:
        print(f"✅ 安全机制生效，操作被拦截！")
        print(f"错误信息：{e}")
    except Exception as e:
        print(f"其他错误：{e}")


if __name__ == '__main__':
    print("🦐 阿里云域名安全操作示例")
    print("=" * 80)
    print()
    print("⚠️ 安全规则：")
    print("所有涉及订单和资金操作的 API 调用，必须经过用户明确二次确认后才能执行！")
    print()
    
    # 示例 1：带确认的域名注册
    example_register_domain_with_confirmation()
    
    # 示例 2：带确认的域名续费
    example_renew_domain_with_confirmation()
    
    # 示例 3：未确认会被拦截
    example_without_confirmation_will_fail()
    
    print("\n" + "=" * 80)
    print("示例结束")
    print("=" * 80)
