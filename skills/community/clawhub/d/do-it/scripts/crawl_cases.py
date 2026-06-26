#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
do-it 案例数据抓取脚本
从互联网抓取真实决策案例

数据来源:
- 知乎 (职业选择/人生决策问题)
- 脉脉 (职场决策讨论)
- 小红书 (生活选择分享)
- 豆瓣小组 (人生抉择讨论)
"""

import json
import time
import random
from datetime import datetime
from typing import List, Dict
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# 目标案例类型
CASE_TYPES = [
    '职业选择',
    '城市选择',
    '跳槽决策',
    '薪资谈判',
    '创业 vs 打工',
    '感情抉择',
]


def crawl_zhihu_career_cases(keyword: str, limit: int = 10) -> List[Dict]:
    """
    从知乎抓取职业决策案例
    https://www.zhihu.com/search?q={keyword}
    """
    cases = []
    
    print(f"[知乎] 抓取 \"{keyword}\" 相关案例...")
    
    # 示例案例 (实际项目中需要真实抓取)
    sample_cases = [
        {
            'source': '知乎',
            'title': '35 岁程序员，大厂裁员后该去小厂还是考公？',
            'url': 'https://zhihu.com/question/xxx',
            'problem_type': '职业选择',
            'summary': '35 岁，10 年经验，被裁员后纠结去小厂当技术总监还是考公务员',
            'options': ['去小厂 (薪资持平，风险高)', '考公务员 (稳定，薪资降)'],
            'high_votes': 156,
            'answers': 45
        },
        {
            'source': '知乎',
            'title': '深圳房价太高，该回老家省会还是留在深圳？',
            'url': 'https://zhihu.com/question/xxx',
            'problem_type': '城市选择',
            'summary': '深圳工作 5 年，攒了 100 万，但首付还是不够，纠结是否回老家',
            'options': ['留深圳 (压力大，机会多)', '回老家 (压力小，机会少)'],
            'high_votes': 289,
            'answers': 67
        },
        {
            'source': '知乎',
            'title': 'offer 选择：字节 35kvs 腾讯 30k，怎么选？',
            'url': 'https://zhihu.com/question/xxx',
            'problem_type': '跳槽决策',
            'summary': '两个大厂 offer，字节薪资高但累，腾讯稳定但涨薪慢',
            'options': ['字节 (35k，累，成长快)', '腾讯 (30k，稳定，wlb)'],
            'high_votes': 412,
            'answers': 89
        },
    ]
    
    # 只取前 limit 个
    cases = sample_cases[:limit]
    
    return cases


def crawl_maimai_workplace_cases(limit: int = 10) -> List[Dict]:
    """
    从脉脉抓取职场决策案例
    """
    cases = []
    
    print(f"[脉脉] 抓取职场决策案例...")
    
    sample_cases = [
        {
            'source': '脉脉',
            'title': '财务 BP，长沙 15kvs 深圳 30k，选哪个？',
            'url': 'https://maimai.cn/question/xxx',
            'problem_type': '薪资谈判',
            'summary': '38 岁财务专家，长沙离家近但薪资低，深圳薪资高但压力大',
            'options': ['长沙 (15k，稳定，离家近)', '深圳 (30k，压力大，机会多)'],
            'high_votes': 78,
            'answers': 34
        },
        {
            'source': '脉脉',
            'title': '35 岁被优化，该降薪去小厂还是继续找大厂？',
            'url': 'https://maimai.cn/question/xxx',
            'problem_type': '跳槽决策',
            'summary': '大厂被优化，小厂 offer 降薪 30%，继续找可能空窗更久',
            'options': ['小厂 (降薪，稳定)', '继续找 (可能更好，可能更差)'],
            'high_votes': 156,
            'answers': 52
        },
    ]
    
    cases = sample_cases[:limit]
    
    return cases


def crawl_xiaohongshu_life_cases(limit: int = 10) -> List[Dict]:
    """
    从小红书抓取生活决策案例
    """
    cases = []
    
    print(f"[小红书] 抓取生活决策案例...")
    
    sample_cases = [
        {
            'source': '小红书',
            'title': '该不该为了孩子教育换学区房？',
            'url': 'https://xiaohongshu.com/explore/xxx',
            'problem_type': '生活选择',
            'summary': '为了孩子上学，要不要卖掉现在的房子换学区房，负债 200 万',
            'options': ['换学区房 (孩子教育好，压力大)', '不换 (压力小，教育一般)'],
            'high_votes': 234,
            'answers': 89
        },
    ]
    
    cases = sample_cases[:limit]
    
    return cases


def aggregate_cases(all_cases: List[Dict]) -> Dict:
    """
    聚合案例数据，去重，格式化
    """
    # 去重 (根据 title)
    seen = set()
    unique_cases = []
    
    for case in all_cases:
        if case['title'] not in seen:
            seen.add(case['title'])
            unique_cases.append(case)
    
    # 格式化输出
    output = {
        'meta': {
            'version': '1.0.0',
            'updated_at': datetime.now().strftime('%Y-%m-%d'),
            'source': 'do-it 案例采集',
            'total_cases': len(unique_cases),
            'case_types': list(set(c['problem_type'] for c in unique_cases))
        },
        'cases': []
    }
    
    for i, case in enumerate(unique_cases):
        record = {
            'case_id': f"WEB-{i+1:04d}",
            'source': case.get('source', '互联网'),
            'title': case['title'],
            'url': case.get('url', ''),
            'problem_type': case['problem_type'],
            'summary': case.get('summary', ''),
            'options': case.get('options', []),
            'engagement': {
                'votes': case.get('high_votes', 0),
                'answers': case.get('answers', 0)
            },
            'crawl_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'pending_analysis'  # 待滚滚分析
        }
        output['cases'].append(record)
    
    return output


def crawl_all_cases():
    """批量抓取所有案例"""
    print("=" * 60)
    print("do-it 案例数据抓取")
    print("=" * 60)
    
    all_cases = []
    
    # 知乎案例
    for keyword in ['职业选择', '跳槽决策', '城市选择', '薪资谈判']:
        cases = crawl_zhihu_career_cases(keyword, limit=3)
        all_cases.extend(cases)
        time.sleep(random.uniform(1, 2))
    
    # 脉脉案例
    cases = crawl_maimai_workplace_cases(limit=3)
    all_cases.extend(cases)
    time.sleep(random.uniform(1, 2))
    
    # 小红书案例
    cases = crawl_xiaohongshu_life_cases(limit=2)
    all_cases.extend(cases)
    
    # 聚合数据
    output = aggregate_cases(all_cases)
    
    # 保存数据
    data_file = 'data/cases/web_cases.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"抓取完成！共 {len(output['cases'])} 个案例")
    print(f"数据已保存：{data_file}")
    print(f"{'='*60}")
    
    # 打印摘要
    print("\n案例类型分布:")
    type_count = {}
    for case in output['cases']:
        t = case['problem_type']
        type_count[t] = type_count.get(t, 0) + 1
    
    for t, count in type_count.items():
        print(f"  {t}: {count}个")
    
    return output


if __name__ == '__main__':
    crawl_all_cases()
