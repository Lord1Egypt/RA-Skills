#!/usr/bin/env python3
"""运势查询wrapper"""
import os
import sys

# 获取技能目录路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FORTUNE_MODULE = os.path.join(SCRIPT_DIR, "fortune_luck.py")

# 获取生日参数
birth = sys.argv[1] if len(sys.argv) > 1 else None

# 直接调用模块
sys.path.insert(0, SCRIPT_DIR)
try:
    from fortune_luck import FortuneCalculator
    
    calc = FortuneCalculator()
    
    if birth:
        # 直接调用计算
        result = calc.calculate(birth)
        print(result.to_text("detailed"))
    else:
        # 检查是否有保存的生日
        saved = calc.get_saved_birthday()
        if saved:
            result = calc.calculate()
            print(result.to_text("detailed"))
        else:
            print(calc.get_ask_birthday_prompt())
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()