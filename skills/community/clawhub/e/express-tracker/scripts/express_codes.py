#!/usr/bin/env python3
"""
快递公司代码库
根据单号前缀自动识别快递公司
"""

# 快递公司代码映射
EXPRESS_CODES = {
    # 常见快递公司
    'yuantong': {
        'name': '圆通速递',
        'prefixes': ['YT'],
        'patterns': ['^YT']
    },
    'zhongtong': {
        'name': '中通快递',
        'prefixes': ['ZT'],
        'patterns': ['^ZT', '^731', '^751', '^761', '^771', '^781']
    },
    'shentong': {
        'name': '申通快递',
        'prefixes': ['ST'],
        'patterns': ['^ST', '^773', '^774', '^775', '^776']
    },
    'yunda': {
        'name': '韵达快递',
        'prefixes': ['YD'],
        'patterns': ['^YD', '^43', '^46', '^31']
    },
    'shunfeng': {
        'name': '顺丰速运',
        'prefixes': ['SF'],
        'patterns': ['^SF', '^90', '^92', '^93', '^94', '^95', '^96', '^97', '^98', '^99']
    },
    'jd': {
        'name': '京东物流',
        'prefixes': ['JD'],
        'patterns': ['^JD', '^JDV', '^JDD', '^JDK', '^JDL']
    },
    'ems': {
        'name': '邮政EMS',
        'prefixes': ['10', '11', '50'],
        'patterns': ['^10', '^11', '^50', '^98', '^97']
    },
    'jtexpress': {
        'name': '极兔速递',
        'prefixes': ['JT'],
        'patterns': ['^JT', '^50']
    },
    'deppon': {
        'name': '德邦快递',
        'prefixes': ['DPL', 'DPK'],
        'patterns': ['^DPL', '^DPK']
    },
    'youzhengguonei': {
        'name': '邮政包裹',
        'prefixes': ['96', '97', '98'],
        'patterns': ['^96', '^97', '^98', '^99']
    },
    'zhaijisong': {
        'name': '宅急送',
        'prefixes': ['ZJS'],
        'patterns': ['^ZJS']
    },
    'tiantian': {
        'name': '天天快递',
        'prefixes': ['TT'],
        'patterns': ['^TT', '^55', '^56', '^88']
    },
    'guotong': {
        'name': '国通快递',
        'prefixes': ['GT'],
        'patterns': ['^GT', '^20', '^21', '^22', '^23', '^24', '^25']
    },
    'kuaijiesudi': {
        'name': '快捷快递',
        'prefixes': ['KJ'],
        'patterns': ['^KJ', '^53']
    },
    'zhongyouwuliu': {
        'name': '中邮物流',
        'prefixes': ['CNPL'],
        'patterns': ['^CNPL', '^A']
    },
    'fengwang': {
        'name': '丰网速运',
        'prefixes': ['FW'],
        'patterns': ['^FW']
    },
    'yuantongkuaidi': {
        'name': '圆通快递',
        'prefixes': ['YT'],
        'patterns': ['^YT', '^D0', '^D1', '^D2', '^D3', '^D4', '^D5']
    }
}


def detect_express(nu: str) -> tuple:
    """
    根据快递单号自动识别快递公司

    Args:
        nu: 快递单号

    Returns:
        (com_code, com_name) 元组
        如果无法识别，返回 (None, None)
    """
    if not nu:
        return None, None

    nu = str(nu).strip().upper()

    # 优先匹配前缀
    for code, info in EXPRESS_CODES.items():
        for prefix in info['prefixes']:
            if nu.startswith(prefix):
                return code, info['name']

    # 匹配正则模式
    import re
    for code, info in EXPRESS_CODES.items():
        for pattern in info['patterns']:
            if re.match(pattern, nu):
                return code, info['name']

    return None, None


def get_express_name(com: str) -> str:
    """
    根据快递公司代码获取名称

    Args:
        com: 快递公司代码

    Returns:
        快递公司名称，如果未找到返回代码本身
    """
    if com in EXPRESS_CODES:
        return EXPRESS_CODES[com]['name']
    return com


def list_express_codes() -> dict:
    """
    获取所有快递公司代码列表

    Returns:
        快递公司代码字典
    """
    return {code: info['name'] for code, info in EXPRESS_CODES.items()}


if __name__ == '__main__':
    # 测试
    test_nus = [
        'YT2538259220416',
        'SF1234567890',
        'JD0123456789012',
        '731234567890',
        '9876543210'
    ]

    print("快递公司识别测试：\n")
    for nu in test_nus:
        code, name = detect_express(nu)
        print(f"单号: {nu}")
        print(f"  识别结果: {name or '无法识别'} ({code or 'unknown'})\n")
