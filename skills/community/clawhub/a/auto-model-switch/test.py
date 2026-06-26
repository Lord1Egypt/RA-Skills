#!/usr/bin/env python3
"""测试自动切换模型"""

import sys
sys.path.insert(0, '.')

from auto_model_switch import AutoModelSwitch


def test_basic():
    """基础测试"""
    print("=" * 50)
    print("测试自动切换模型")
    print("=" * 50)
    
    switcher = AutoModelSwitch()
    
    # 1. 获取状态
    print("\n1. 当前状态:")
    status = switcher.get_status()
    print(f"   模型: {status['model_name']}")
    print(f"   ID: {status['current_model']}")
    
    # 2. 模拟token使用
    print("\n2. 模拟token使用:")
    switcher.update_token_usage(switcher.current_model, 1000000)
    usage = switcher.check_token_usage()
    if usage:
        print(f"   已用: {usage['used']:,}")
        print(f"   限制: {usage['limit']:,}")
        print(f"   百分比: {usage['percentage']*100:.1f}%")
    
    # 3. 测试切换
    print("\n3. 测试切换:")
    success = switcher.switch_model("manual")
    print(f"   切换结果: {'成功' if success else '失败'}")
    print(f"   新模型: {switcher.current_model}")
    
    # 4. 最终状态
    print("\n4. 最终状态:")
    status = switcher.get_status()
    print(f"   模型: {status['model_name']}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    test_basic()
