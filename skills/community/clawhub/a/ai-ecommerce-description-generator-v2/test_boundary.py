#!/usr/bin/env python3
"""
边界异常测试 - AI电商商品描述生成器
测试空参数输入、超长文本输入、跨风格混合指令输入
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import AIEcommerceDescriptionGenerator

def test_empty_input():
    """测试空参数输入"""
    print("🧪 测试1：空参数输入")
    
    generator = AIEcommerceDescriptionGenerator()
    
    # 测试空商品名称
    try:
        result = generator.generate_descriptions("", "淘宝", "吸引人", 3)
        if not result or len(result) == 0:
            print("✅ 空商品名称测试通过：正确处理空输入")
        else:
            print("❌ 空商品名称测试失败：未正确处理空输入")
    except Exception as e:
        print(f"✅ 空商品名称测试通过：抛出异常 {e}")
    
    # 测试空平台
    try:
        result = generator.generate_descriptions("手机壳", "", "吸引人", 3)
        if not result or len(result) == 0:
            print("✅ 空平台测试通过：正确处理空输入")
        else:
            print("❌ 空平台测试失败：未正确处理空输入")
    except Exception as e:
        print(f"✅ 空平台测试通过：抛出异常 {e}")
    
    # 测试空风格
    try:
        result = generator.generate_descriptions("手机壳", "淘宝", "", 3)
        if result and len(result) > 0:
            print("✅ 空风格测试通过：使用默认风格")
        else:
            print("❌ 空风格测试失败：未使用默认风格")
    except Exception as e:
        print(f"❌ 空风格测试失败：抛出异常 {e}")

def test_long_text_input():
    """测试超长文本输入"""
    print("\n🧪 测试2：超长文本输入")
    
    generator = AIEcommerceDescriptionGenerator()
    
    # 测试超长商品名称
    long_product = "这是一个非常非常非常长的商品名称测试" * 10
    try:
        result = generator.generate_descriptions(long_product, "淘宝", "吸引人", 3)
        if result and len(result) > 0:
            # 检查描述长度是否合理
            total_length = sum(len(desc['description']) for desc in result)
            if total_length < 2000:
                print("✅ 超长商品名称测试通过：输出长度合理")
            else:
                print("❌ 超长商品名称测试失败：输出过长")
        else:
            print("❌ 超长商品名称测试失败：无输出")
    except Exception as e:
        print(f"❌ 超长商品名称测试失败：抛出异常 {e}")
    
    # 测试超长描述需求
    try:
        result = generator.generate_descriptions("手机壳", "淘宝", "吸引人", 100)
        if result and len(result) <= 10:  # 限制最大生成数量
            print("✅ 超长描述需求测试通过：限制生成数量")
        else:
            print("❌ 超长描述需求测试失败：未限制生成数量")
    except Exception as e:
        print(f"✅ 超长描述需求测试通过：抛出异常 {e}")

def test_mixed_style_input():
    """测试跨风格混合指令输入"""
    print("\n🧪 测试3：跨风格混合指令输入")
    
    generator = AIEcommerceDescriptionGenerator()
    
    # 测试混合风格指令
    try:
        result = generator.generate_descriptions("手机壳", "淘宝", "吸引人,专业", 3)
        if result and len(result) > 0:
            # 检查是否包含任一风格
            descriptions = [desc['description'] for desc in result]
            has_attractive = any("吸引人" in desc or "爆款" in desc for desc in descriptions)
            has_professional = any("专业" in desc or "高品质" in desc for desc in descriptions)
            
            if has_attractive or has_professional:
                print("✅ 混合风格指令测试通过：处理混合风格")
            else:
                print("❌ 混合风格指令测试失败：未识别风格")
        else:
            print("❌ 混合风格指令测试失败：无输出")
    except Exception as e:
        print(f"✅ 混合风格指令测试通过：抛出异常 {e}")
    
    # 测试无效风格
    try:
        result = generator.generate_descriptions("手机壳", "淘宝", "无效风格", 3)
        if result and len(result) > 0:
            print("✅ 无效风格测试通过：使用默认风格")
        else:
            print("❌ 无效风格测试失败：未使用默认风格")
    except Exception as e:
        print(f"✅ 无效风格测试通过：抛出异常 {e}")

def main():
    """主函数"""
    print("🚀 开始边界异常测试 - AI电商商品描述生成器")
    print("=" * 50)
    
    test_empty_input()
    test_long_text_input()
    test_mixed_style_input()
    
    print("\n" + "=" * 50)
    print("🎯 边界异常测试完成")

if __name__ == "__main__":
    main()