#!/usr/bin/env python3
"""
快递单号识别 v2.1
功能：根据单号识别快递公司，输出置信度和多候选
修复：去重逻辑
输出格式：JSON
"""

import json
import re
import sys

# 承运商识别规则库
CARRIERS = {
    '顺丰速运': {
        'prefixes': ['SF', 'sf'],
        'lengths': [12, 15],
        'patterns': [r'^13\d{9}$'],  # 手机号格式
        'confidence': 0.95
    },
    '极兔速递': {
        'prefixes': ['JT', 'jt', 'TG', 'tg'],
        'lengths': [12, 13],
        'patterns': [],
        'confidence': 0.95
    },
    '京东物流': {
        'prefixes': ['JD', 'jd', '16', '18', '36'],
        'lengths': [13, 15],
        'patterns': [],
        'confidence': 0.90
    },
    '圆通速递': {
        'prefixes': ['YT', 'yt', '88', '99', '66'],
        'lengths': [12, 13],
        'patterns': [],
        'confidence': 0.85
    },
    '中通快递': {
        'prefixes': ['ZT', 'zt', '78', '38', '01', '02'],
        'lengths': [12, 13],
        'patterns': [],
        'confidence': 0.85
    },
    '申通快递': {
        'prefixes': ['ST', 'st', '22'],
        'lengths': [12, 13],
        'patterns': [],
        'confidence': 0.85
    },
    '韵达速递': {
        'prefixes': ['YD', 'yd', '12', '10', '39', '30'],
        'lengths': [13],
        'patterns': [],
        'confidence': 0.85
    },
    '德邦物流': {
        'prefixes': ['DP', 'dp', 'TC', 'tc'],
        'lengths': [9, 10, 12],
        'patterns': [],
        'confidence': 0.90
    },
    '安能物流': {
        'prefixes': ['ANE', 'ane', '56', '52', '68'],
        'lengths': [10, 11, 12],
        'patterns': [],
        'confidence': 0.85
    },
    '跨越速运': {
        'prefixes': ['KY', 'ky'],
        'lengths': [12, 13],
        'patterns': [],
        'confidence': 0.95
    },
    '邮政快递': {
        'prefixes': ['YZ', 'yz', 'PG', 'pg', '98', '96'],
        'lengths': [13, 15],
        'patterns': [],
        'confidence': 0.80
    },
    '中铁快运': {
        'prefixes': ['KT', 'kt'],
        'lengths': [7, 8, 9, 10],
        'patterns': [],
        'confidence': 0.90
    }
}


def normalize_number(tracking_number):
    """标准化单号：去空格、转大写"""
    return tracking_number.strip().upper()


def identify_courier(tracking_number):
    """
    识别快递公司
    返回：{
        'candidates': [
            {'name': '顺丰速运', 'confidence': 0.95, 'reason': '前缀匹配'},
            ...
        ],
        'primary': '顺丰速运',
        'confidence_level': '高'
    }
    """
    number = normalize_number(tracking_number)
    candidates_dict = {}  # 用字典去重，key是公司名
    
    # 步骤一：前缀精确匹配
    for name, rules in CARRIERS.items():
        for prefix in rules['prefixes']:
            if number.startswith(prefix):
                # 只保留最高置信度
                if name not in candidates_dict or candidates_dict[name]['confidence'] < rules['confidence']:
                    candidates_dict[name] = {
                        'name': name,
                        'confidence': rules['confidence'],
                        'reason': f'前缀匹配:{prefix}',
                        'match_type': 'prefix'
                    }
    
    # 步骤二：长度匹配（只在没有前缀匹配时添加）
    if not candidates_dict:
        length = len(number)
        for name, rules in CARRIERS.items():
            if length in rules['lengths']:
                conf = rules['confidence'] * 0.7
                if name not in candidates_dict or candidates_dict[name]['confidence'] < conf:
                    candidates_dict[name] = {
                        'name': name,
                        'confidence': conf,
                        'reason': f'长度匹配:{length}位',
                        'match_type': 'length'
                    }
    
    # 转换为列表并按置信度排序
    results = list(candidates_dict.values())
    results.sort(key=lambda x: x['confidence'], reverse=True)
    
    # 取前3个候选
    candidates = results[:3]
    
    # 取最高置信度
    if candidates:
        primary = candidates[0]
        conf = primary['confidence']
        
        if conf >= 0.9:
            confidence_level = '高'
        elif conf >= 0.7:
            confidence_level = '中'
        else:
            confidence_level = '低'
    else:
        primary = None
        confidence_level = '无'
    
    return {
        'input': tracking_number,
        'normalized': number,
        'length': len(number),
        'candidates': candidates,
        'primary': primary['name'] if primary else None,
        'confidence_level': confidence_level,
        'success': len(candidates) > 0
    }


def format_text(result):
    """格式化输出为文本"""
    lines = []
    lines.append(f"单号：{result['input']}")
    lines.append(f"识别结果：{result['confidence_level']}置信度")
    lines.append("")
    
    if result['candidates']:
        lines.append("可能的公司：")
        for i, c in enumerate(result['candidates'], 1):
            conf_pct = int(c['confidence'] * 100)
            lines.append(f"{i}. {c['name']} ({conf_pct}%) - {c['reason']}")
    else:
        lines.append("无法识别快递公司")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        # 交互模式：测试几个样本
        print("测试样例：")
        print("-" * 40)
        
        test_numbers = [
            'SF1234567890',
            'JT12345678901', 
            'JD0012345678901',
            '781234567890',
            'YT1234567890',
            '123456789012'  # 纯数字，无前缀
        ]
        
        for num in test_numbers:
            result = identify_courier(num)
            print(format_text(result))
            print("-" * 40)
        sys.exit(0)
    
    tracking_number = sys.argv[1]
    result = identify_courier(tracking_number)
    
    # 输出格式
    if '--json' in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == '__main__':
    main()
