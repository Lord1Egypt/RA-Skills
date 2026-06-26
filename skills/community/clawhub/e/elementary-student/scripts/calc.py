import re

def calculate(expression):
    """
    简单的计算器函数，处理加减乘除
    支持整数和简单表达式如: 5+3, 10-4, 6*7, 20/4
    """
    try:
        # 移除空格
        expression = expression.replace(" ", "")

        # 简单验证
        if not re.match(r'^[0-9]+[+\-*/][0-9]+$', expression):
            return None

        # 安全地计算（只支持简单四则运算）
        # 注意：eval 在这个场景下是安全的，因为我们已经验证了输入格式
        result = eval(expression)

        # 返回整数或浮点数
        if isinstance(result, float):
            if result.is_integer():
                return int(result)
            else:
                return round(result, 2)
        return result
    except:
        return None

def is_within_10(num1, num2):
    """判断两个数是否都在10以内（包含10）"""
    return 0 <= num1 <= 10 and 0 <= num2 <= 10

def is_simple_operation(expression):
    """判断是否是简单的个位数运算"""
    try:
        expression = expression.replace(" ", "")
        match = re.match(r'^([0-9]+)([+\-*/])([0-9]+)$', expression)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(3))
            return is_within_10(num1, num2)
        return False
    except:
        return False

