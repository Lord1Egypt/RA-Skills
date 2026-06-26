#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROI 分析器 - 计算广告投入产出比
支持多维度分析和对比
"""

import json
import argparse
from typing import Dict, List
from datetime import datetime


class ROIAnalyzer:
    """ROI 分析器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.default_gmv_multiplier = 1.0  # GMV 倍数，可根据实际情况调整
    
    def analyze(self, data: List[Dict], group_by: str = 'platform') -> Dict:
        """
        分析 ROI 数据
        
        Args:
            data: 广告数据列表
            group_by: 分组维度 (platform, campaign, date)
        
        Returns:
            分析结果字典
        """
        # 按维度分组
        groups = {}
        for item in data:
            if group_by == 'platform':
                key = item.get('platform', 'unknown')
            elif group_by == 'campaign':
                key = f"{item.get('platform')}_{item.get('campaign_id')}"
            elif group_by == 'date':
                key = item.get('date', 'unknown')
            else:
                key = 'all'
            
            if key not in groups:
                groups[key] = {
                    'impression': 0,
                    'click': 0,
                    'cost': 0,
                    'conversion': 0,
                    'conversion_cost': 0,
                    'items': []
                }
            
            groups[key]['impression'] += item.get('impression', 0)
            groups[key]['click'] += item.get('click', 0)
            groups[key]['cost'] += item.get('cost', 0)
            groups[key]['conversion'] += item.get('conversion', 0)
            groups[key]['conversion_cost'] += item.get('conversion_cost', 0)
            groups[key]['items'].append(item)
        
        # 计算指标
        results = {}
        for key, stats in groups.items():
            # 基础指标
            impression = stats['impression']
            click = stats['click']
            cost = stats['cost']
            conversion = stats['conversion']
            
            # 衍生指标
            ctr = (click / impression * 100) if impression > 0 else 0
            cvr = (conversion / click * 100) if click > 0 else 0
            cpc = (cost / click) if click > 0 else 0
            cpa = (cost / conversion) if conversion > 0 else 0
            
            # 估算 GMV 和 ROI (需要实际订单数据)
            # 这里使用转化成本作为参考
            estimated_gmv = conversion * self.default_gmv_multiplier * 200  # 假设客单价 200
            roi = (estimated_gmv / cost) if cost > 0 else 0
            
            results[key] = {
                'impression': impression,
                'click': click,
                'cost': round(cost, 2),
                'conversion': conversion,
                'ctr': round(ctr, 2),
                'cvr': round(cvr, 2),
                'cpc': round(cpc, 2),
                'cpa': round(cpa, 2),
                'estimated_gmv': round(estimated_gmv, 2),
                'roi': round(roi, 2),
                'item_count': len(stats['items'])
            }
        
        return results
    
    def compare_periods(self, current_data: List[Dict], previous_data: List[Dict]) -> Dict:
        """对比两个时期的数据"""
        current_stats = self.analyze(current_data, group_by='all')['all']
        previous_stats = self.analyze(previous_data, group_by='all')['all']
        
        comparison = {}
        for key in ['cost', 'conversion', 'ctr', 'cvr', 'cpa', 'roi']:
            current_val = current_stats.get(key, 0)
            previous_val = previous_stats.get(key, 0)
            
            if previous_val > 0:
                change = ((current_val - previous_val) / previous_val) * 100
            else:
                change = 0 if current_val == 0 else 100
            
            comparison[key] = {
                'current': current_val,
                'previous': previous_val,
                'change': round(change, 2),
                'trend': 'up' if change > 0 else ('down' if change < 0 else 'flat')
            }
        
        return comparison
    
    def get_top_performers(self, data: List[Dict], metric: str = 'roi', top_n: int = 10) -> List[Dict]:
        """获取表现最好的广告计划"""
        # 按广告计划分组
        campaigns = {}
        for item in data:
            key = f"{item.get('platform')}_{item.get('campaign_id')}"
            if key not in campaigns:
                campaigns[key] = {
                    'platform': item.get('platform'),
                    'campaign_id': item.get('campaign_id'),
                    'campaign_name': item.get('campaign_name'),
                    'cost': 0,
                    'conversion': 0
                }
            campaigns[key]['cost'] += item.get('cost', 0)
            campaigns[key]['conversion'] += item.get('conversion', 0)
        
        # 计算 ROI
        for key, camp in campaigns.items():
            estimated_gmv = camp['conversion'] * 200  # 假设客单价 200
            camp['roi'] = round(estimated_gmv / camp['cost'], 2) if camp['cost'] > 0 else 0
        
        # 排序
        sorted_campaigns = sorted(
            campaigns.values(),
            key=lambda x: x.get(metric, 0),
            reverse=True
        )
        
        return sorted_campaigns[:top_n]
    
    def get_worst_performers(self, data: List[Dict], metric: str = 'roi', top_n: int = 10) -> List[Dict]:
        """获取表现最差的广告计划"""
        top = self.get_top_performers(data, metric, len(data))
        return list(reversed(top))[:top_n]


def load_data(file_path: str) -> List[Dict]:
    """加载 JSON 数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='ROI 分析器')
    parser.add_argument('--input', '-i', type=str, required=True,
                        help='输入数据文件 (JSON 格式)')
    parser.add_argument('--group-by', '-g', type=str, default='platform',
                        choices=['platform', 'campaign', 'date', 'all'],
                        help='分组维度')
    parser.add_argument('--top', '-t', type=int, default=10,
                        help='显示 Top N 广告计划')
    parser.add_argument('--output', '-o', type=str,
                        help='输出分析结果 (JSON 格式)')
    parser.add_argument('--gmv-multiplier', type=float, default=1.0,
                        help='GMV 估算倍数')
    
    args = parser.parse_args()
    
    # 加载数据
    print(f"📊 加载数据：{args.input}")
    data = load_data(args.input)
    print(f"   共 {len(data)} 条记录")
    
    # 创建分析器
    analyzer = ROIAnalyzer({'gmv_multiplier': args.gmv_multiplier})
    
    # 执行分析
    print(f"\n📈 按 {args.group_by} 分组分析...")
    results = analyzer.analyze(data, group_by=args.group_by)
    
    # 打印结果
    print(f"\n{'='*80}")
    print(f"ROI 分析结果 (按 {args.group_by} 分组)")
    print(f"{'='*80}")
    
    for key, stats in sorted(results.items(), key=lambda x: x[1]['roi'], reverse=True):
        print(f"\n{key}:")
        print(f"   消耗：¥{stats['cost']:,.2f}")
        print(f"   转化：{stats['conversion']}")
        print(f"   CTR: {stats['ctr']:.2f}%")
        print(f"   CVR: {stats['cvr']:.2f}%")
        print(f"   CPA: ¥{stats['cpa']:.2f}")
        print(f"   ROI: {stats['roi']:.2f}")
    
    # Top 广告计划
    print(f"\n{'='*80}")
    print(f"🏆 Top {args.top} 广告计划 (按 ROI)")
    print(f"{'='*80}")
    
    top_campaigns = analyzer.get_top_performers(data, metric='roi', top_n=args.top)
    for i, camp in enumerate(top_campaigns, 1):
        print(f"{i}. {camp['campaign_name']} ({camp['campaign_id']})")
        print(f"   平台：{camp['platform']} | 消耗：¥{camp['cost']:.2f} | ROI: {camp['roi']:.2f}")
    
    # 输出结果
    if args.output:
        output_data = {
            'analysis': results,
            'top_campaigns': top_campaigns,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 分析结果已保存到：{args.output}")


if __name__ == '__main__':
    main()
