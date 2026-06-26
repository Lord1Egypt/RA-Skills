#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
域名价值分析工具
Domain Value Analyzer

用法：python3 analyze_domain.py <domain>
"""

import sys
import re


# TLD 价值评级
TLD_RATINGS = {
    'com': {'score': 100, 'name': '.com', 'desc': '商业/通用，认知度最高'},
    'io': {'score': 70, 'name': '.io', 'desc': '科技/加密，创业公司青睐'},
    'co': {'score': 50, 'name': '.co', 'desc': '创业公司风格'},
    'xyz': {'score': 40, 'name': '.xyz', 'desc': 'Web3/加密常用'},
    'net': {'score': 40, 'name': '.net', 'desc': '网络服务'},
    'org': {'score': 40, 'name': '.org', 'desc': '非营利组织'},
    'link': {'score': 25, 'name': '.link', 'desc': '链接服务'},
    'cn': {'score': 30, 'name': '.cn', 'desc': '中国市场'},
    'ai': {'score': 65, 'name': '.ai', 'desc': 'AI/科技'},
    'app': {'score': 50, 'name': '.app', 'desc': '应用/小程序'},
    'dev': {'score': 55, 'name': '.dev', 'desc': '开发者工具'},
    'tech': {'score': 35, 'name': '.tech', 'desc': '科技行业'},
    'vip': {'score': 10, 'name': '.vip', 'desc': '灰产常用，价值低'},
    'top': {'score': 10, 'name': '.top', 'desc': '灰产常用，价值低'},
}

# 常见拼写错误检查
COMMON_MISSPELLINGS = {
    'gloabl': 'global',
    'goolge': 'google',
    'yahooo': 'yahoo',
    'microsft': 'microsoft',
    'amazn': 'amazon',
    'facebok': 'facebook',
    'twiter': 'twitter',
    'linkdin': 'linkedin',
    'instal': 'install',
    'securty': 'security',
    'privcy': 'privacy',
    'scurity': 'security',
}

# 行业风险评级
INDUSTRY_RISKS = {
    'crypto': {'risk': 'high', 'desc': '加密货币，监管不明朗'},
    'token': {'risk': 'high', 'desc': '代币相关，监管风险'},
    'bet': {'risk': 'high', 'desc': '博彩，法律风险'},
    'casino': {'risk': 'high', 'desc': '赌场，法律风险'},
    'loan': {'risk': 'medium', 'desc': '贷款，金融监管'},
    'finance': {'risk': 'medium', 'desc': '金融，合规要求高'},
    'health': {'risk': 'medium', 'desc': '医疗，广告限制'},
    'pharma': {'risk': 'medium', 'desc': '医药，严格监管'},
    'tech': {'risk': 'low', 'desc': '科技，低风险'},
    'ai': {'risk': 'low', 'desc': '人工智能，热门行业'},
    'shop': {'risk': 'low', 'desc': '电商，常规行业'},
    'game': {'risk': 'low', 'desc': '游戏，常规行业'},
}


def parse_domain(domain):
    """解析域名，返回主体和后缀"""
    domain = domain.lower().strip()
    # 移除协议
    domain = re.sub(r'^https?://', '', domain)
    # 移除路径
    domain = domain.split('/')[0]
    # 分割主体和后缀
    parts = domain.rsplit('.', 1)
    if len(parts) != 2:
        return None, None
    return parts[0], parts[1]


def check_length(name):
    """检查长度评分"""
    length = len(name)
    if length <= 6:
        return 5, f'{length}字符，极短稀缺'
    elif length <= 9:
        return 4, f'{length}字符，短小优质'
    elif length <= 12:
        return 3, f'{length}字符，中等长度'
    elif length <= 15:
        return 2, f'{length}字符，偏长'
    else:
        return 1, f'{length}字符，过长'


def check_spelling(name):
    """检查拼写错误"""
    issues = []
    for wrong, right in COMMON_MISSPELLINGS.items():
        if wrong in name:
            issues.append(f'"{wrong}" 应为 "{right}"')
    
    if issues:
        return 1, '发现拼写错误：' + '; '.join(issues)
    return 5, '拼写正确'


def check_tld(tld):
    """检查后缀评分"""
    tld = tld.lower()
    if tld in TLD_RATINGS:
        rating = TLD_RATINGS[tld]
        score = rating['score'] // 20  # 转换为 1-5 分
        return max(1, score), f"{rating['name']} - {rating['desc']}"
    return 2, f'.{tld} - 冷门后缀'


def check_industry(name):
    """检查行业风险"""
    name_lower = name.lower()
    for keyword, info in INDUSTRY_RISKS.items():
        if keyword in name_lower:
            score_map = {'low': 5, 'medium': 3, 'high': 2}
            return score_map[info['risk']], info['desc']
    return 5, '常规行业，无特殊风险'


def check_memorability(name):
    """检查记忆度"""
    # 检查是否包含数字
    has_digit = any(c.isdigit() for c in name)
    # 检查是否包含连字符
    has_hyphen = '-' in name
    # 检查音节数（简单估算）
    vowels = 'aeiou'
    syllables = sum(1 for c in name if c in vowels)
    
    issues = []
    score = 5
    
    if has_digit:
        score -= 1
        issues.append('包含数字')
    if has_hyphen:
        score -= 1
        issues.append('包含连字符')
    if syllables > 4:
        score -= 1
        issues.append(f'音节较多 ({syllables}个)')
    
    if issues:
        return max(1, score), '记忆度一般：' + '; '.join(issues)
    return 5, '易记顺口'


def check_meaning(name):
    """检查含义清晰度"""
    # 简单检查：是否由有意义的单词组成
    # 这里做基础检查，完整检查需要词典
    common_words = [
        'token', 'coin', 'chain', 'block', 'global', 'tech', 'ai',
        'smart', 'fast', 'easy', 'pro', 'hub', 'lab', 'box',
        'fab', 'app', 'web', 'net', 'soft', 'data', 'cloud',
        'pay', 'shop', 'buy', 'sell', 'trade', 'market', 'store',
    ]
    
    name_lower = name.lower()
    found_words = [w for w in common_words if w in name_lower]
    
    if len(found_words) >= 2:
        return 5, f'含义清晰，包含词根：{", ".join(found_words)}'
    elif len(found_words) == 1:
        return 4, f'含义较清晰，包含词根：{found_words[0]}'
    else:
        return 3, '含义一般，无明显词根'


def calculate_overall(scores):
    """计算综合评分"""
    weights = {
        'length': 0.20,
        'spelling': 0.20,
        'meaning': 0.20,
        'memorability': 0.15,
        'tld': 0.15,
        'industry': 0.10,
    }
    
    total = 0.0
    for key, value in scores.items():
        score = value[0] if isinstance(value, tuple) else value
        total += score * weights.get(key, 0.1)
    
    # 转换为 100 分制
    return round(total * 20)


def estimate_value(overall_score, tld):
    """估算价值范围"""
    if overall_score >= 90:
        return '10 万 -100 万+', '极品'
    elif overall_score >= 80:
        return '1 万 -10 万', '优质'
    elif overall_score >= 70:
        return '2000-1 万', '良好'
    elif overall_score >= 60:
        return '500-2000 元', '普通'
    elif overall_score >= 40:
        return '100-500 元', '一般'
    else:
        return '<100 元', '较差'


def analyze_domain(domain):
    """完整分析域名"""
    name, tld = parse_domain(domain)
    
    if not name or not tld:
        return {'error': '域名格式不正确'}
    
    # 各项评分
    scores = {
        'length': check_length(name),
        'spelling': check_spelling(name),
        'tld': check_tld(tld),
        'industry': check_industry(name),
        'memorability': check_memorability(name),
        'meaning': check_meaning(name),
    }
    
    # 综合评分
    overall = calculate_overall(scores)
    
    # 价值估算
    value_range, level = estimate_value(overall, tld)
    
    # 注册成本
    reg_cost = TLD_RATINGS.get(tld.lower(), {'score': 50})
    cost_range = '60-100 元' if tld.lower() == 'com' else '50-500 元'
    
    return {
        'domain': f'{name}.{tld}',
        'name': name,
        'tld': tld,
        'scores': scores,
        'overall': overall,
        'value_range': value_range,
        'level': level,
        'cost_range': cost_range,
    }


def print_report(result):
    """打印分析报告"""
    if 'error' in result:
        print(f"❌ 错误：{result['error']}")
        return
    
    print("\n" + "="*60)
    print(f"📊 域名价值分析报告")
    print("="*60)
    print(f"\n域名：{result['domain']}")
    
    print("\n### 📈 价值评分\n")
    print("| 维度 | 评分 | 说明 |")
    print("|------|------|------|")
    
    dimension_names = {
        'length': '长度',
        'spelling': '拼写',
        'tld': '后缀',
        'industry': '行业',
        'memorability': '记忆度',
        'meaning': '含义',
    }
    
    star_map = {5: '⭐⭐⭐⭐⭐', 4: '⭐⭐⭐⭐', 3: '⭐⭐⭐', 2: '⭐⭐', 1: '⭐'}
    
    for key, (score, desc) in result['scores'].items():
        name = dimension_names.get(key, key)
        stars = star_map.get(score, '⭐' * score)
        print(f"| {name} | {stars} | {desc} |")
    
    print(f"\n**综合评分：{star_map.get(result['overall']//20, '⭐'* (result['overall']//20))} ({result['overall']}/100)**")
    
    print("\n### 💰 价值评估\n")
    print(f"| 项目 | 数值 |")
    print(f"|------|------|")
    print(f"| 注册成本 | 约 {result['cost_range']}/年 |")
    print(f"| 潜在变现 | {result['value_range']} |")
    print(f"| 投资等级 | {result['level']} |")
    
    # 最终建议
    print("\n### 🎯 最终建议\n")
    if result['overall'] >= 70:
        print("✅ **值得注册**")
        print("\n理由：综合评分较高，具有投资价值。如是可注册状态，建议尽快拿下。")
    elif result['overall'] >= 50:
        print("⚠️ **谨慎考虑**")
        print("\n理由：中等评分，如有具体项目可使用，纯投资需谨慎。")
    else:
        print("❌ **不建议注册**")
        print("\n理由：评分较低，存在明显缺陷，建议寻找更好的域名。")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 analyze_domain.py <domain>")
        print("示例：python3 analyze_domain.py tokensfab.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    result = analyze_domain(domain)
    print_report(result)
