#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常检测器 - 监控广告计划异常情况
支持：消耗异常、转化率波动、低 ROI 预警
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class AnomalyDetector:
    """异常检测器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        # 默认阈值
        self.min_roi = self.config.get('min_roi', 1.5)
        self.max_cpa = self.config.get('max_cpa', 100)
        self.min_consumption = self.config.get('min_consumption', 100)  # 最低消耗阈值
        self.ctr_drop_threshold = self.config.get('ctr_drop_threshold', 0.5)  # CTR 下降 50%
        self.cvr_drop_threshold = self.config.get('cvr_drop_threshold', 0.5)  # CVR 下降 50%
    
    def detect(self, data: List[Dict], historical_data: List[Dict] = None) -> List[Dict]:
        """
        检测异常
        
        Args:
            data: 当前数据
            historical_data: 历史数据 (用于对比)
        
        Returns:
            异常列表
        """
        anomalies = []
        
        # 按广告计划分组
        campaigns = defaultdict(list)
        for item in data:
            key = f"{item.get('platform')}_{item.get('campaign_id')}"
            campaigns[key].append(item)
        
        # 检测每个计划
        for key, items in campaigns.items():
            # 聚合数据
            total_cost = sum(item.get('cost', 0) for item in items)
            total_conversion = sum(item.get('conversion', 0) for item in items)
            total_click = sum(item.get('click', 0) for item in items)
            total_impression = sum(item.get('impression', 0) for item in items)
            
            # 计算指标
            if total_cost < self.min_consumption:
                continue  # 消耗太低，不检测
            
            cpa = total_cost / total_conversion if total_conversion > 0 else float('inf')
            gmv = total_conversion * 200  # 假设客单价 200
            roi = gmv / total_cost if total_cost > 0 else 0
            ctr = total_click / total_impression if total_impression > 0 else 0
            cvr = total_conversion / total_click if total_click > 0 else 0
            
            # 获取计划信息
            sample_item = items[0]
            campaign_info = {
                'platform': sample_item.get('platform'),
                'campaign_id': sample_item.get('campaign_id'),
                'campaign_name': sample_item.get('campaign_name'),
                'cost': total_cost,
                'conversion': total_conversion,
                'cpa': cpa,
                'roi': roi,
                'ctr': ctr * 100,
                'cvr': cvr * 100
            }
            
            # 检测低 ROI
            if roi < self.min_roi:
                anomalies.append({
                    **campaign_info,
                    'anomaly_type': 'low_roi',
                    'severity': 'high' if roi < 0.5 else 'medium',
                    'message': f'ROI 过低 ({roi:.2f} < {self.min_roi})',
                    'suggestion': '考虑暂停或优化广告素材'
                })
            
            # 检测高 CPA
            if cpa > self.max_cpa and total_conversion > 0:
                anomalies.append({
                    **campaign_info,
                    'anomaly_type': 'high_cpa',
                    'severity': 'high' if cpa > self.max_cpa * 2 else 'medium',
                    'message': f'CPA 过高 (¥{cpa:.2f} > ¥{self.max_cpa})',
                    'suggestion': '检查定向设置或降低出价'
                })
            
            # 检测零转化
            if total_conversion == 0 and total_cost > self.min_consumption * 2:
                anomalies.append({
                    **campaign_info,
                    'anomaly_type': 'zero_conversion',
                    'severity': 'high',
                    'message': f'消耗 ¥{total_cost:.2f} 但零转化',
                    'suggestion': '立即检查落地页或暂停计划'
                })
            
            # 与历史数据对比
            if historical_data:
                hist_campaigns = defaultdict(list)
                for item in historical_data:
                    key = f"{item.get('platform')}_{item.get('campaign_id')}"
                    hist_campaigns[key].append(item)
                
                if key in hist_campaigns:
                    hist_items = hist_campaigns[key]
                    hist_click = sum(item.get('click', 0) for item in hist_items)
                    hist_impression = sum(item.get('impression', 0) for item in hist_items)
                    hist_conversion = sum(item.get('conversion', 0) for item in hist_items)
                    
                    hist_ctr = hist_click / hist_impression if hist_impression > 0 else 0
                    hist_cvr = hist_conversion / hist_click if hist_click > 0 else 0
                    
                    # CTR 大幅下降
                    if hist_ctr > 0 and ctr / hist_ctr < self.ctr_drop_threshold:
                        anomalies.append({
                            **campaign_info,
                            'anomaly_type': 'ctr_drop',
                            'severity': 'medium',
                            'message': f'CTR 下降 {((1 - ctr/hist_ctr) * 100):.1f}%',
                            'suggestion': '检查广告素材疲劳度'
                        })
                    
                    # CVR 大幅下降
                    if hist_cvr > 0 and cvr / hist_cvr < self.cvr_drop_threshold:
                        anomalies.append({
                            **campaign_info,
                            'anomaly_type': 'cvr_drop',
                            'severity': 'high',
                            'message': f'CVR 下降 {((1 - cvr/hist_cvr) * 100):.1f}%',
                            'suggestion': '检查落地页或产品问题'
                        })
        
        # 按严重程度排序
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        anomalies.sort(key=lambda x: (severity_order.get(x['severity'], 3), -x['cost']))
        
        return anomalies
    
    def generate_alert_message(self, anomalies: List[Dict]) -> str:
        """生成预警消息"""
        if not anomalies:
            return "✅ 暂无异常广告计划"
        
        high_severity = [a for a in anomalies if a['severity'] == 'high']
        medium_severity = [a for a in anomalies if a['severity'] == 'medium']
        
        message = f"🚨 发现 {len(anomalies)} 个异常广告计划\n\n"
        
        if high_severity:
            message += f"🔴 严重 ({len(high_severity)}):\n"
            for a in high_severity[:5]:  # 最多显示 5 个
                message += f"  • {a['campaign_name']}: {a['message']}\n"
        
        if medium_severity:
            message += f"\n🟡 警告 ({len(medium_severity)}):\n"
            for a in medium_severity[:5]:
                message += f"  • {a['campaign_name']}: {a['message']}\n"
        
        if len(anomalies) > 10:
            message += f"\n... 还有 {len(anomalies) - 10} 个异常计划"
        
        return message


def load_data(file_path: str) -> List[Dict]:
    """加载 JSON 数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='异常检测器')
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='输入数据文件 (JSON 格式)')
    parser.add_argument('--historical', '-H', type=str,
                        help='历史数据文件 (用于对比)')
    parser.add_argument('--min-roi', type=float, default=1.5,
                        help='ROI 阈值 (默认 1.5)')
    parser.add_argument('--max-cpa', type=float, default=100,
                        help='CPA 阈值 (默认 100)')
    parser.add_argument('--min-consumption', type=float, default=100,
                        help='最低消耗阈值 (默认 100)')
    parser.add_argument('--output', '-o', type=str,
                        help='输出异常列表 (JSON 格式)')
    parser.add_argument('--alert', '-a', type=str,
                        help='输出预警消息 (文本文件)')
    
    args = parser.parse_args()
    
    # 加载数据
    print(f"📊 加载数据：{args.input}")
    data = load_data(args.input)
    print(f"   共 {len(data)} 条记录")
    
    historical_data = None
    if args.historical:
        print(f"📊 加载历史数据：{args.historical}")
        historical_data = load_data(args.historical)
        print(f"   共 {len(historical_data)} 条记录")
    
    # 创建检测器
    config = {
        'min_roi': args.min_roi,
        'max_cpa': args.max_cpa,
        'min_consumption': args.min_consumption
    }
    detector = AnomalyDetector(config)
    
    # 执行检测
    print(f"\n🔍 检测异常...")
    anomalies = detector.detect(data, historical_data)
    
    # 输出结果
    print(f"\n{'='*60}")
    if anomalies:
        print(f"🚨 发现 {len(anomalies)} 个异常广告计划")
        
        high_count = len([a for a in anomalies if a['severity'] == 'high'])
        medium_count = len([a for a in anomalies if a['severity'] == 'medium'])
        
        print(f"   🔴 严重：{high_count}")
        print(f"   🟡 警告：{medium_count}")
        
        print(f"\n详细列表:")
        for i, a in enumerate(anomalies[:10], 1):
            print(f"\n{i}. {a['campaign_name']} ({a['campaign_id']})")
            print(f"   平台：{a['platform']}")
            print(f"   消耗：¥{a['cost']:.2f}")
            print(f"   转化：{a['conversion']}")
            print(f"   ROI: {a['roi']:.2f} | CPA: ¥{a['cpa']:.2f}")
            print(f"   异常：{a['message']}")
            print(f"   建议：{a['suggestion']}")
        
        if len(anomalies) > 10:
            print(f"\n... 还有 {len(anomalies) - 10} 个异常计划")
    else:
        print(f"✅ 暂无异常广告计划")
    
    print(f"{'='*60}")
    
    # 保存结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(anomalies, f, ensure_ascii=False, indent=2)
        print(f"\n📁 异常列表已保存到：{args.output}")
    
    # 保存预警消息
    if args.alert:
        alert_message = detector.generate_alert_message(anomalies)
        with open(args.alert, 'w', encoding='utf-8') as f:
            f.write(alert_message)
        print(f"📁 预警消息已保存到：{args.alert}")
    
    # 打印预警消息
    print(f"\n{detector.generate_alert_message(anomalies)}")


if __name__ == '__main__':
    main()
