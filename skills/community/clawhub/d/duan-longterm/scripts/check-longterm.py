#!/usr/bin/env python3
"""
长期检查器 - 基于段永平的"10 年持有"思维

无需外部数据，评估是否值得长期持有
"""

import sys
import os
from datetime import datetime


# 长期持有检查清单
HOLD_CHECKLIST = [
    {
        'category': '商业模式',
        'questions': [
            '这个生意 10 年后还会存在吗？',
            '这个生意的护城河会变宽还是变窄？',
            '这个生意是否需要持续大量资本投入？',
        ],
    },
    {
        'category': '管理层',
        'questions': [
            '管理层是否诚信？',
            '管理层是否以股东利益为导向？',
            '管理层是否专注于主业？',
        ],
    },
    {
        'category': '财务健康',
        'questions': [
            '公司是否有持续的自由现金流？',
            '公司负债率是否合理？',
            'ROE 是否持续高于 15%？',
        ],
    },
    {
        'category': '估值',
        'questions': [
            '当前价格是否低于内在价值？',
            '是否有足够的安全边际？',
            '如果股市关闭 5 年，是否还愿意持有？',
        ],
    },
]


def evaluate_category(category: dict, user_answers: list = None) -> dict:
    """
    评估类别
    
    Args:
        category: 类别字典
        user_answers: 用户回答
    
    Returns:
        评估结果
    """
    result = {
        'category': category['category'],
        'score': 0,
        'max_score': len(category['questions']) * 5,
        'questions': [],
    }
    
    for i, question in enumerate(category['questions']):
        q_result = {
            'question': question,
            'score': 3,  # 默认中等
        }
        
        # 如果有用户回答，根据回答评分
        if user_answers and i < len(user_answers):
            ans = user_answers[i]
            if '是' in ans or '会' in ans or '愿意' in ans:
                q_result['score'] = 5
            elif '否' in ans or '不会' in ans or '不愿意' in ans:
                q_result['score'] = 1
        
        result['questions'].append(q_result)
        result['score'] += q_result['score']
    
    return result


def longterm_check(company_name: str, user_answers: dict = None) -> dict:
    """
    长期持有检查
    
    Args:
        company_name: 公司名称
        user_answers: 用户回答字典
    
    Returns:
        检查结果字典
    """
    result = {
        'company': company_name,
        'timestamp': datetime.now().isoformat(),
        'framework': '段永平 10 年持有思维',
    }
    
    # 评估各类别
    result['categories'] = {}
    total_score = 0
    max_score = 0
    
    for category in HOLD_CHECKLIST:
        cat_key = category['category']
        answers = user_answers.get(cat_key, []) if user_answers else None
        result['categories'][cat_key] = evaluate_category(category, answers)
        total_score += result['categories'][cat_key]['score']
        max_score += result['categories'][cat_key]['max_score']
    
    # 综合评分
    result['total_score'] = total_score
    result['max_score'] = max_score
    result['percentage'] = (total_score / max_score * 100) if max_score > 0 else 0
    
    # 持有建议
    if result['percentage'] >= 80:
        result['recommendation'] = '强烈推荐持有（符合长期标准）'
        result['action'] = '买入并持有 10 年+'
    elif result['percentage'] >= 60:
        result['recommendation'] = '可以持有（基本符合标准）'
        result['action'] = '持有，持续观察'
    elif result['percentage'] >= 40:
        result['recommendation'] = '谨慎持有（部分不符合）'
        result['action'] = '减仓或观望'
    else:
        result['recommendation'] = '不建议持有（不符合长期标准）'
        result['action'] = '卖出或回避'
    
    return result


def print_check(result: dict) -> None:
    """打印检查结果"""
    print("="*60)
    print(f"⏰ 长期检查器：{result['company']}")
    print("="*60)
    
    print(f"\n📋 检查框架")
    print(f"   {result['framework']}")
    
    print(f"\n📊 分类评估")
    for cat_key, cat_data in result['categories'].items():
        score_pct = cat_data['score'] / cat_data['max_score'] * 100
        score_icon = '⭐' * int(score_pct / 20)
        print(f"\n   {cat_data['category']} ({cat_data['score']}/{cat_data['max_score']}分) {score_icon}")
        for q in cat_data['questions']:
            q_icon = '✅' if q['score'] >= 4 else '➡️' if q['score'] >= 3 else '❌'
            print(f"     {q_icon} {q['question']}")
    
    print(f"\n📈 综合评分")
    print(f"   总分：{result['total_score']}/{result['max_score']} ({result['percentage']:.1f}%)")
    
    print(f"\n💡 持有建议")
    print(f"   {result['recommendation']}")
    print(f"   行动：{result['action']}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 诚实回答每个问题")
    print(f"   2. 基于事实而非印象")
    print(f"   3. 假设持有 10 年，是否安心？")
    print(f"   4. 如果答案不确定，选择"否"")


def main():
    """主函数"""
    company_name = sys.argv[1] if len(sys.argv) > 1 else '目标公司'
    
    result = longterm_check(company_name)
    print_check(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
