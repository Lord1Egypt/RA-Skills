#!/usr/bin/env python3
"""
快递查询主脚本 v3.2
功能：按快递公司设置优先查询平台，一级查不到自动用二级
"""

import sys
import json
import re
from datetime import datetime, timedelta

# 导入识别模块
from identify import identify_courier


# 按快递公司设置优先查询平台
# 优先级策略：
# 1. 官方小程序/APP（最准，但可能需要验证）
# 2. 官网查询页（通常需要验证）
# 3. 聚合平台（有验证码保护）
# 4. 搜索引擎（兜底）

QUERY_STRATEGY = {
    '顺丰速运': {
        'priority': 1,
        'name': '顺丰速运',
        'level1': [
            '顺丰小程序',
            '顺丰APP'
        ],
        'level2': [
            'https://www.sf-express.com/sfweb/xbmm/query',
            'https://www.sf-express.com/tracking'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu=',
            'https://www.kdniao.com/?'
        ],
        'level4': [
            '百度搜索:顺丰快递 单号'
        ]
    },
    '中通快递': {
        'priority': 1,
        'name': '中通快递',
        'level1': [
            '中通小程序',
            '中通APP'
        ],
        'level2': [
            'https://www.zto.com/search',
            'https://www.zto.com/express/search'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu=',
            'https://www.zto.com/'
        ],
        'level4': [
            '百度搜索:中通快递 单号'
        ]
    },
    '圆通速递': {
        'priority': 1,
        'name': '圆通速递',
        'level1': [
            '圆通小程序',
            '圆通APP'
        ],
        'level2': [
            'https://www.yto.net.cn/express/track',
            'https://www.yto.net.cn/'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:圆通快递 单号'
        ]
    },
    '韵达速递': {
        'priority': 1,
        'name': '韵达速递',
        'level1': [
            '韵达小程序',
            '韵达APP'
        ],
        'level2': [
            'https://www.yundaex.com/www/track/trace',
            'https://www.yundaex.com/'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:韵达快递 单号'
        ]
    },
    '申通快递': {
        'priority': 1,
        'name': '申通快递',
        'level1': [
            '申通小程序',
            '申通APP'
        ],
        'level2': [
            'https://www.sto.cn/search',
            'https://www.sto.cn/'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:申通快递 单号'
        ]
    },
    '极兔速递': {
        'priority': 1,
        'name': '极兔速递',
        'level1': [
            '极兔小程序',
            '极兔APP'
        ],
        'level2': [
            'https://www.jtexpress.com.cn/track',
            'https://www.jtexpress.com.cn/'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:极兔快递 单号'
        ]
    },
    '京东物流': {
        'priority': 1,
        'name': '京东物流',
        'level1': [
            '京东小程序',
            '京东APP'
        ],
        'level2': [
            'https://www.jd.com/track',
            'https://m.jd.com/trace'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:京东快递 单号'
        ]
    },
    '邮政快递': {
        'priority': 1,
        'name': '邮政快递',
        'level1': [
            '邮政小程序',
            'EMS APP'
        ],
        'level2': [
            'https://www.ems.com.cn/query',
            'https://www.ems.com.cn/'
        ],
        'level3': [
            'https://www.kuaidi100.com/?nu='
        ],
        'level4': [
            '百度搜索:EMS快递 单号'
        ]
    }
}


def get_query_urls(tracking_number, courier):
    """
    根据快递公司获取分级查询URL
    """
    # 默认策略
    default_strategy = {
        'level1': ['官方小程序/APP'],
        'level2': [
            f'https://www.kuaidi100.com/?nu={tracking_number}'
        ],
        'level3': [
            f'https://www.kdniao.com/?nu={tracking_number}',
            f'https://www.ickd.cn/?nu={tracking_number}'
        ],
        'level4': [f'百度搜索:快递 {tracking_number}']
    }
    
    # 如果有特定策略，用特定策略
    if courier in QUERY_STRATEGY:
        strategy = QUERY_STRATEGY[courier]
        urls = {
            'level1': strategy.get('level1', []),
            'level2': [u.format(tracking_number) if '{}' in u else u + tracking_number for u in strategy.get('level2', [])],
            'level3': [u.format(tracking_number) if '{}' in u else u + tracking_number for u in strategy.get('level3', [])],
            'level4': [u.format(tracking_number) if '{}' in u else u for u in strategy.get('level4', [])]
        }
    else:
        urls = default_strategy
    
    return urls


def format_query_plan(tracking_number, courier, urls):
    """格式化查询方案"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"快递查询方案 - {courier}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"单号：{tracking_number}")
    lines.append("")
    
    lines.append("【一级方案】官方渠道（最准确）")
    if urls['level1']:
        for item in urls['level1']:
            lines.append(f"  - {item}")
    else:
        lines.append("  无")
    lines.append("")
    
    lines.append("【二级方案】官网查询")
    if urls['level2']:
        for url in urls['level2']:
            lines.append(f"  - {url}")
    else:
        lines.append("  无")
    lines.append("")
    
    lines.append("【三级方案】聚合平台")
    if urls['level3']:
        for url in urls['level3']:
            lines.append(f"  - {url}")
    else:
        lines.append("  无")
    lines.append("")
    
    lines.append("【四级方案】搜索引擎（兜底）")
    if urls['level4']:
        for item in urls['level4']:
            lines.append(f"  - {item}")
    else:
        lines.append("  无")
    lines.append("")
    
    lines.append("查询建议：")
    lines.append("1. 优先用【一级方案】小程序/APP，通常最准确")
    lines.append("2. 【二级】官网查询可能需要手机号验证")
    lines.append("3. 【三级】聚合平台也可能需要验证")
    lines.append("4. 【四级】搜索是兜底方案")
    lines.append("")
    lines.append("如果遇到验证，请告诉我：")
    lines.append("- 需要手机号后四位")
    lines.append("- 需要登录")
    lines.append("- 需要图形验证码")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法：python query.py <单号>")
        print("示例：python query.py SF1234567890")
        print("")
        print("功能：按快递公司设置优先查询平台，一级查不到用二级")
        sys.exit(1)
    
    tracking_number = sys.argv[1]
    
    # 识别快递公司
    result = identify_courier(tracking_number)
    courier = result['primary'] if result['success'] else '未知'
    confidence = int(result['candidates'][0]['confidence'] * 100) if result['candidates'] else 0
    
    print(f"识别：{courier} (置信度:{confidence}%)")
    print("")
    
    # 获取查询方案
    urls = get_query_urls(tracking_number, courier)
    
    # 输出查询方案
    print(format_query_plan(tracking_number, courier, urls))


if __name__ == '__main__':
    main()
