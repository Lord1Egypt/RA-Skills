#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
走访质量评分算法模块
基于《C+基础保障服务手册》第十四章客户拜访服务规程
"""

import pandas as pd
from datetime import datetime, timedelta
import json

class VisitScoring:
    """走访质量评分算法"""
    
    def __init__(self):
        """初始化评分权重"""
        # 评分权重配置
        self.weights = {
            'satisfaction': 0.4,      # 满意度 40%
            'deal_rate': 0.3,         # 成交率 30%
            'service_type': 0.2,       # 服务类别 20%
            'detail_record': 0.1        # 详情记录 10%
        }
        
        # 服务类别评分标准
        self.service_type_scores = {
            '入驻服务': 10,
            '费用催缴': 9,
            '投诉处理': 8,
            '日常走访': 7,
            '需求挖掘': 6,
            '其他': 5
        }
    
    def calculate_satisfaction_score(self, satisfaction_rate):
        """计算满意度得分 (0-10分)"""
        if satisfaction_rate >= 0.95:  # 95%以上
            return 10
        elif satisfaction_rate >= 0.90:  # 90-95%
            return 9
        elif satisfaction_rate >= 0.85:  # 85-90%
            return 8
        elif satisfaction_rate >= 0.80:  # 80-85%
            return 7
        elif satisfaction_rate >= 0.70:  # 70-80%
            return 6
        elif satisfaction_rate >= 0.60:  # 60-70%
            return 5
        else:  # 60%以下
            return 3
    
    def calculate_deal_rate_score(self, deal_rate):
        """计算成交率得分 (0-10分)"""
        if deal_rate >= 0.50:  # 50%以上
            return 10
        elif deal_rate >= 0.40:  # 40-50%
            return 9
        elif deal_rate >= 0.30:  # 30-40%
            return 8
        elif deal_rate >= 0.20:  # 20-30%
            return 7
        elif deal_rate >= 0.15:  # 15-20%
            return 6
        elif deal_rate >= 0.10:  # 10-15%
            return 5
        else:  # 10%以下
            return 3
    
    def calculate_service_type_score(self, service_type):
        """计算服务类别得分 (0-10分)"""
        return self.service_type_scores.get(service_type, 5)
    
    def calculate_detail_record_score(self, has_detail_record):
        """计算详情记录得分 (0-10分)"""
        if has_detail_record:
            return 10
        else:
            return 5
    
    def calculate_visit_quality_score(self, visit_data):
        """
        计算走访质量综合得分
        
        Args:
            visit_data: dict, 包含以下字段:
                - satisfaction_rate: float, 满意度比例 (0-1)
                - deal_rate: float, 成交率比例 (0-1)
                - service_type: str, 服务类别
                - has_detail_record: bool, 是否有详情记录
                
        Returns:
            float: 综合得分 (0-10分)
        """
        # 计算各维度得分
        satisfaction_score = self.calculate_satisfaction_score(visit_data['satisfaction_rate'])
        deal_rate_score = self.calculate_deal_rate_score(visit_data['deal_rate'])
        service_type_score = self.calculate_service_type_score(visit_data['service_type'])
        detail_record_score = self.calculate_detail_record_score(visit_data['has_detail_record'])
        
        # 加权计算综合得分
        total_score = (
            satisfaction_score * self.weights['satisfaction'] +
            deal_rate_score * self.weights['deal_rate'] +
            service_type_score * self.weights['service_type'] +
            detail_record_score * self.weights['detail_record']
        )
        
        return round(total_score, 2)
    
    def generate_visit_report(self, visit_records):
        """
        生成走访质量报告
        
        Args:
            visit_records: list, 走访记录列表
            
        Returns:
            dict: 走访质量报告
        """
        if not visit_records:
            return {
                'total_visits': 0,
                'avg_quality_score': 0,
                'satisfaction_avg': 0,
                'deal_rate_avg': 0,
                'service_type_distribution': {},
                'detail_record_rate': 0,
                'recommendations': ['暂无走访数据']
            }
        
        # 计算各项指标
        total_visits = len(visit_records)
        quality_scores = []
        satisfaction_rates = []
        deal_rates = []
        service_type_count = {}
        detail_record_count = 0
        
        for record in visit_records:
            # 计算质量得分
            score = self.calculate_visit_quality_score(record)
            quality_scores.append(score)
            
            # 收集满意度数据
            satisfaction_rates.append(record.get('satisfaction_rate', 0))
            
            # 收集成交率数据
            deal_rates.append(record.get('deal_rate', 0))
            
            # 统计服务类别分布
            service_type = record.get('service_type', '其他')
            service_type_count[service_type] = service_type_count.get(service_type, 0) + 1
            
            # 统计详情记录
            if record.get('has_detail_record', False):
                detail_record_count += 1
        
        # 计算平均值
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        satisfaction_avg = sum(satisfaction_rates) / len(satisfaction_rates) if satisfaction_rates else 0
        deal_rate_avg = sum(deal_rates) / len(deal_rates) if deal_rates else 0
        detail_record_rate = detail_record_count / total_visits if total_visits > 0 else 0
        
        # 生成改进建议
        recommendations = self._generate_recommendations(
            avg_quality_score, satisfaction_avg, deal_rate_avg, 
            detail_record_rate, service_type_count
        )
        
        return {
            'total_visits': total_visits,
            'avg_quality_score': round(avg_quality_score, 2),
            'satisfaction_avg': round(satisfaction_avg * 100, 2),  # 转为百分比
            'deal_rate_avg': round(deal_rate_avg * 100, 2),  # 转为百分比
            'service_type_distribution': service_type_count,
            'detail_record_rate': round(detail_record_rate * 100, 2),  # 转为百分比
            'recommendations': recommendations,
            'score_distribution': self._get_score_distribution(quality_scores)
        }
    
    def _generate_recommendations(self, avg_score, satisfaction, deal_rate, detail_rate, service_types):
        """生成改进建议"""
        recommendations = []
        
        if avg_score < 7.0:
            recommendations.append("走访质量综合得分较低，建议加强走访培训")
        
        if satisfaction < 0.85:
            recommendations.append("满意度低于85%，建议优化服务流程")
        
        if deal_rate < 0.20:
            recommendations.append("成交率低于20%，建议提升需求挖掘能力")
        
        if detail_rate < 0.80:
            recommendations.append("详情记录率低于80%，建议规范走访记录")
        
        # 检查服务类别分布
        if '需求挖掘' not in service_types or service_types.get('需求挖掘', 0) < 5:
            recommendations.append("需求挖掘类走访较少，建议增加此类走访")
        
        if not recommendations:
            recommendations.append("走访质量良好，继续保持")
        
        return recommendations
    
    def _get_score_distribution(self, scores):
        """获取得分分布"""
        distribution = {
            '优秀(9-10分)': 0,
            '良好(8-9分)': 0,
            '中等(7-8分)': 0,
            '待改进(6-7分)': 0,
            '较差(<6分)': 0
        }
        
        for score in scores:
            if score >= 9:
                distribution['优秀(9-10分)'] += 1
            elif score >= 8:
                distribution['良好(8-9分)'] += 1
            elif score >= 7:
                distribution['中等(7-8分)'] += 1
            elif score >= 6:
                distribution['待改进(6-7分)'] += 1
            else:
                distribution['较差(<6分)'] += 1
        
        return distribution

# 示例用法
if __name__ == "__main__":
    # 初始化评分器
    scorer = VisitScoring()
    
    # 示例走访数据
    sample_visits = [
        {
            'satisfaction_rate': 0.95,  # 95%满意度
            'deal_rate': 0.35,         # 35%成交率
            'service_type': '入驻服务',
            'has_detail_record': True
        },
        {
            'satisfaction_rate': 0.88,
            'deal_rate': 0.25,
            'service_type': '费用催缴',
            'has_detail_record': True
        },
        {
            'satisfaction_rate': 0.92,
            'deal_rate': 0.40,
            'service_type': '需求挖掘',
            'has_detail_record': False
        }
    ]
    
    # 计算单条走访质量得分
    score = scorer.calculate_visit_quality_score(sample_visits[0])
    print(f"单条走访质量得分: {score}")
    
    # 生成走访质量报告
    report = scorer.generate_visit_report(sample_visits)
    print(f"\n走访质量报告:")
    print(json.dumps(report, ensure_ascii=False, indent=2))