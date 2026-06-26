#!/usr/bin/env python3
"""
Claw Ethics Checker - 测试模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from claw_ethics_checker import EthicsChecker, RiskLevel

def test_ethics_checker():
    """测试伦理检查器"""
    print("🧪 Claw Ethics Checker 测试")
    print("=" * 50)
    
    # 创建检查器
    checker = EthicsChecker()
    
    # 测试用例1：合规任务
    print("\n📋 测试用例1：合规任务")
    print("-" * 30)
    task1 = {
        'description': '分析公开市场数据，生成季度报告',
        'client': '投资公司',
        'methods': ['data_analysis', 'report_generation'],
        'data_source': '公开API，合法获取'
    }
    
    result1 = checker.analyze_task('市场分析报告', task1)
    print(f"任务: {task1['description']}")
    print(f"风险等级: {result1.risk_level.value}")
    print(f"是否合规: {result1.is_compliant}")
    print(f"需要人工审核: {result1.needs_human_review}")
    print(f"建议: {', '.join(result1.recommendations)}")
    
    # 测试用例2：中等风险任务
    print("\n📋 测试用例2：中等风险任务")
    print("-" * 30)
    task2 = {
        'description': '监控竞争对手社交媒体活动',
        'client': '营销公司',
        'methods': ['social_media_monitoring', 'sentiment_analysis'],
        'data_source': '公开社交媒体数据'
    }
    
    result2 = checker.analyze_task('竞争分析', task2)
    print(f"任务: {task2['description']}")
    print(f"风险等级: {result2.risk_level.value}")
    print(f"是否合规: {result2.is_compliant}")
    print(f"需要人工审核: {result2.needs_human_review}")
    print(f"警告: {', '.join(result2.warnings) if result2.warnings else '无'}")
    print(f"建议: {', '.join(result2.recommendations)}")
    
    # 测试用例3：高风险任务
    print("\n📋 测试用例3：高风险任务")
    print("-" * 30)
    task3 = {
        'description': '获取竞争对手用户数据库',
        'client': '电商平台',
        'methods': ['data_extraction', 'reverse_engineering'],
        'data_source': '未授权的数据库访问'
    }
    
    result3 = checker.analyze_task('用户数据获取', task3)
    print(f"任务: {task3['description']}")
    print(f"风险等级: {result3.risk_level.value}")
    print(f"是否合规: {result3.is_compliant}")
    print(f"需要人工审核: {result3.needs_human_review}")
    print(f"警告: {', '.join(result3.warnings) if result3.warnings else '无'}")
    print(f"法律问题: {', '.join(result3.legal_issues) if result3.legal_issues else '无'}")
    print(f"伦理问题: {', '.join(result3.ethical_concerns) if result3.ethical_concerns else '无'}")
    print(f"建议: {', '.join(result3.recommendations)}")
    
    # 测试用例4：隐私相关任务
    print("\n📋 测试用例4：隐私相关任务")
    print("-" * 30)
    task4 = {
        'description': '分析用户个人数据以改进推荐算法',
        'client': '科技公司',
        'methods': ['data_mining', 'machine_learning'],
        'data_source': '用户个人数据'
    }
    
    result4 = checker.analyze_task('用户数据分析', task4)
    print(f"任务: {task4['description']}")
    print(f"风险等级: {result4.risk_level.value}")
    print(f"是否合规: {result4.is_compliant}")
    print(f"需要人工审核: {result4.needs_human_review}")
    print(f"警告: {', '.join(result4.warnings) if result4.warnings else '无'}")
    print(f"建议: {', '.join(result4.recommendations)}")
    
    # 总结
    print("\n📊 测试总结")
    print("-" * 30)
    print(f"总测试用例: 4")
    print(f"合规任务: {sum(1 for r in [result1, result2, result3, result4] if r.is_compliant)}")
    print(f"需要人工审核: {sum(1 for r in [result1, result2, result3, result4] if r.needs_human_review)}")
    print(f"高风险任务: {sum(1 for r in [result1, result2, result3, result4] if r.risk_level == RiskLevel.HIGH)}")
    
    print("\n✅ 测试完成！")
    print("💡 这个skill可以帮助AI助手自动识别风险任务，确保合法合规操作。")

if __name__ == "__main__":
    test_ethics_checker()