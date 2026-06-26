#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO.SKILL - 监控工具
功能：监控AI对园区的引用情况，跟踪排名和情感倾向
"""

import json
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time


class GEOMonitor:
    """GEO监控工具"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化监控工具
        
        Args:
            config_path: 监控配置文件路径
        """
        self.config = self._load_config(config_path)
        self.history_file = Path("./geo_monitor_history.json")
        self.history = self._load_history()
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "park_name": "园区",
            "keywords": [],
            "competitors": [],
            "ai_platforms": ["DeepSeek", "豆包", "Kimi"],
            "check_interval_days": 7
        }
    
    def _load_history(self) -> List[Dict]:
        """加载历史数据"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        """保存历史数据"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def _simulate_ai_search(self, keyword: str, platform: str) -> Dict:
        """模拟AI搜索查询
        
        注意：实际环境中需要调用各AI平台的搜索API
        这里提供框架代码
        
        Args:
            keyword: 搜索关键词
            platform: AI平台名称
            
        Returns:
            搜索结果
        """
        # 实际实现需要调用真实API
        # 这里返回模拟数据作为框架演示
        return {
            'keyword': keyword,
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'results': [
                {
                    'rank': 1,
                    'source': '官方网站',
                    'title': f'{self.config["park_name"]}官方网站',
                    'snippet': '...',
                    'cited': True,
                    'accuracy': 0.95
                }
            ],
            'park_mentioned': True,
            'park_rank': 1,
            'sentiment': 'positive'
        }
    
    def check_keyword(self, keyword: str) -> Dict:
        """检查单个关键词
        
        Args:
            keyword: 要检查的关键词
            
        Returns:
            检查结果
        """
        result = {
            'keyword': keyword,
            'timestamp': datetime.now().isoformat(),
            'platforms': {}
        }
        
        for platform in self.config['ai_platforms']:
            print(f"  检查 {platform}...")
            platform_result = self._simulate_ai_search(keyword, platform)
            result['platforms'][platform] = platform_result
            time.sleep(0.5)  # 避免请求过快
        
        # 汇总结果
        ranks = []
        mentioned_count = 0
        
        for platform, platform_result in result['platforms'].items():
            if platform_result.get('park_mentioned'):
                mentioned_count += 1
                if 'park_rank' in platform_result:
                    ranks.append(platform_result['park_rank'])
        
        result['mention_rate'] = mentioned_count / len(self.config['ai_platforms'])
        result['average_rank'] = sum(ranks) / len(ranks) if ranks else None
        result['best_rank'] = min(ranks) if ranks else None
        
        return result
    
    def run_monitoring(self) -> Dict:
        """运行完整监控
        
        Returns:
            监控结果
        """
        print(f"\n🔍 开始GEO监控")
        print(f"园区: {self.config['park_name']}")
        print(f"关键词数量: {len(self.config['keywords'])}\n")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'park_name': self.config['park_name'],
            'keywords': {}
        }
        
        for keyword in self.config['keywords']:
            print(f"\n📌 检查关键词: {keyword}")
            keyword_result = self.check_keyword(keyword)
            results['keywords'][keyword] = keyword_result
        
        # 汇总统计
        total_mentions = 0
        total_rank = 0
        rank_count = 0
        
        for keyword, keyword_result in results['keywords'].items():
            if keyword_result.get('park_mentioned'):
                total_mentions += 1
            if keyword_result.get('average_rank'):
                total_rank += keyword_result['average_rank']
                rank_count += 1
        
        results['summary'] = {
            'total_keywords': len(self.config['keywords']),
            'mentioned_keywords': total_mentions,
            'mention_rate': total_mentions / len(self.config['keywords']) if self.config['keywords'] else 0,
            'average_rank': total_rank / rank_count if rank_count else None,
            'top_3_rate': sum(1 for k in results['keywords'].values() 
                            if k.get('best_rank') and k['best_rank'] <= 3) / len(self.config['keywords']) 
                          if self.config['keywords'] else 0
        }
        
        # 保存到历史
        self.history.append(results)
        self._save_history()
        
        return results
    
    def generate_report(self, results: Dict, format: str = 'markdown') -> str:
        """生成监控报告
        
        Args:
            results: 监控结果
            format: 报告格式
            
        Returns:
            报告内容
        """
        if format == 'json':
            return json.dumps(results, ensure_ascii=False, indent=2)
        
        summary = results['summary']
        
        report = f"""# GEO监控报告

**园区**: {results['park_name']}  
**监控时间**: {results['timestamp']}  
**报告周期**: {self._get_period()}

---

## 📊 整体表现

| 指标 | 数值 | 状态 |
|------|------|------|
| AI提及率 | {summary['mention_rate']*100:.1f}% | {'✅ 优秀' if summary['mention_rate'] > 0.8 else '⚠️ 需提升'} |
| 平均排名 | #{summary['average_rank']:.1f if summary['average_rank'] else 'N/A'} | {'✅ 前三' if summary['average_rank'] and summary['average_rank'] <= 3 else '⚠️ 需优化'} |
| 前3率 | {summary['top_3_rate']*100:.1f}% | {'✅ 优秀' if summary['top_3_rate'] > 0.6 else '⚠️ 需提升'} |
| 关键词覆盖 | {summary['mentioned_keywords']}/{summary['total_keywords']} | - |

---

## 🔍 关键词排名详情

| 关键词 | DeepSeek | 豆包 | Kimi | 平均排名 | 变化 |
|--------|----------|------|------|----------|------|
"""
        
        for keyword, keyword_data in results['keywords'].items():
            platforms = keyword_data['platforms']
            ds_rank = platforms.get('DeepSeek', {}).get('park_rank', '-')
            db_rank = platforms.get('豆包', {}).get('park_rank', '-')
            kimi_rank = platforms.get('Kimi', {}).get('park_rank', '-')
            avg_rank = keyword_data.get('average_rank', '-')
            if isinstance(avg_rank, float):
                avg_rank = f"#{avg_rank:.1f}"
            
            report += f"| {keyword} | #{ds_rank} | #{db_rank} | #{kimi_rank} | {avg_rank} | - |\n"
        
        report += "\n## 📈 趋势分析\n\n"
        
        # 添加趋势图表占位
        report += "```\n"
        report += "AI提及率趋势 (最近4周)\n"
        report += "┌─────────────────────────────────────┐\n"
        mention_rate = summary['mention_rate']
        bar_length = int(mention_rate * 30)
        report += f"│{'█' * bar_length}{' ' * (30-bar_length)}│ {mention_rate*100:.0f}%\n"
        report += "└─────────────────────────────────────┘\n"
        report += "```\n\n"
        
        report += "## 🔔 问题预警\n\n"
        
        # 检测问题
        issues = []
        if summary['mention_rate'] < 0.8:
            issues.append(("⚠️ AI提及率偏低", "建议增加内容分发和关键词覆盖"))
        if summary['average_rank'] and summary['average_rank'] > 5:
            issues.append(("⚠️ 平均排名靠后", "建议优化llms.txt和内容质量"))
        if summary['top_3_rate'] < 0.6:
            issues.append(("⚠️ 前3率不足", "建议加强核心关键词优化"))
        
        if issues:
            for title, detail in issues:
                report += f"- **{title}**: {detail}\n"
        else:
            report += "✅ 未发现明显问题\n"
        
        report += "\n## 💡 优化建议\n\n"
        
        if summary['mention_rate'] < 0.8:
            report += "1. 增加知乎、百家号等内容分发\n"
        if summary['average_rank'] and summary['average_rank'] > 5:
            report += "2. 更新llms.txt，确保信息准确\n"
            report += "3. 在官网FAQ中增加相关问答\n"
        if summary['top_3_rate'] < 0.6:
            report += "4. 针对核心关键词创作专题内容\n"
            report += "5. 联系行业媒体进行报道\n"
        
        report += "\n## 📅 下次监控\n\n"
        next_check = datetime.now() + timedelta(days=self.config.get('check_interval_days', 7))
        report += f"建议时间: {next_check.strftime('%Y-%m-%d')}\n\n"
        
        report += "---\n\n*报告由GEO.SKILL监控工具生成*\n"
        
        return report
    
    def _get_period(self) -> str:
        """获取监控周期描述"""
        if len(self.history) >= 2:
            last = datetime.fromisoformat(self.history[-1]['timestamp'])
            prev = datetime.fromisoformat(self.history[-2]['timestamp'])
            delta = last - prev
            return f"{prev.strftime('%m-%d')} ~ {last.strftime('%m-%d')}"
        return "首次监控"
    
    def save_report(self, results: Dict, output_path: str, format: str = 'markdown'):
        """保存报告"""
        report = self.generate_report(results, format)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 报告已保存: {output_path}")
    
    def compare_with_history(self) -> Dict:
        """与历史数据对比"""
        if len(self.history) < 2:
            return {'error': '历史数据不足，无法对比'}
        
        current = self.history[-1]
        previous = self.history[-2]
        
        comparison = {
            'current_timestamp': current['timestamp'],
            'previous_timestamp': previous['timestamp'],
            'metrics': {}
        }
        
        current_summary = current['summary']
        previous_summary = previous['summary']
        
        for metric in ['mention_rate', 'average_rank', 'top_3_rate']:
            curr_val = current_summary.get(metric)
            prev_val = previous_summary.get(metric)
            
            if curr_val is not None and prev_val is not None:
                if metric == 'average_rank':
                    # 越小越好
                    diff = prev_val - curr_val
                else:
                    # 越大越好
                    diff = curr_val - prev_val
                
                comparison['metrics'][metric] = {
                    'current': curr_val,
                    'previous': prev_val,
                    'change': diff,
                    'trend': 'up' if diff > 0 else ('down' if diff < 0 else 'stable')
                }
        
        return comparison


def create_sample_config(output_path: str = "geo_monitor_config.json"):
    """创建示例监控配置"""
    sample_config = {
        "park_name": "苏州生物医药创新园",
        "keywords": [
            "苏州生物医药创新园",
            "苏州生物医药园租金",
            "苏州生物医药厂房",
            "苏州GMP车间",
            "苏州生物医药园优惠政策",
            "苏州生物医药园入驻条件",
            "苏州生物医药园联系方式",
            "苏州生物医药园怎么样"
        ],
        "competitors": [
            "苏州生物纳米园",
            "上海张江生物医药基地",
            "杭州医药港"
        ],
        "ai_platforms": [
            "DeepSeek",
            "豆包",
            "Kimi"
        ],
        "check_interval_days": 7,
        "notification": {
            "email": "alert@example.cn",
            "webhook": ""
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 示例配置文件已创建: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GEO.SKILL - GEO监控工具')
    parser.add_argument('--config', '-c', type=str, default=None,
                        help='监控配置文件路径')
    parser.add_argument('--output', '-o', type=str, default='geo_monitor_report.md',
                        help='报告输出路径')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown',
                        help='报告格式')
    parser.add_argument('--compare', '-C', action='store_true',
                        help='与历史数据对比')
    parser.add_argument('--sample', '-s', action='store_true',
                        help='创建示例配置文件')
    parser.add_argument('--keywords', '-k', nargs='+',
                        help='指定检查的关键词（覆盖配置文件）')
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_config()
        return
    
    if args.config:
        if not Path(args.config).exists():
            print(f"配置文件不存在，正在创建示例...")
            create_sample_config()
            print(f"请编辑 geo_monitor_config.json 后重新运行")
            return
    else:
        # 尝试查找默认配置文件
        default_config = Path("geo_monitor_config.json")
        if default_config.exists():
            args.config = str(default_config)
        else:
            print("未找到配置文件，正在创建示例...")
            create_sample_config()
            print("请编辑 geo_monitor_config.json 后重新运行")
            return
    
    monitor = GEOMonitor(args.config)
    
    # 如果指定了关键词，覆盖配置
    if args.keywords:
        monitor.config['keywords'] = args.keywords
    
    results = monitor.run_monitoring()
    
    # 生成报告
    monitor.save_report(results, args.output, args.format)
    
    # 对比历史
    if args.compare:
        comparison = monitor.compare_with_history()
        if 'error' in comparison:
            print(f"\n⚠️ {comparison['error']}")
        else:
            print("\n📊 历史对比:")
            for metric, data in comparison['metrics'].items():
                trend_icon = '📈' if data['trend'] == 'up' else ('📉' if data['trend'] == 'down' else '➡️')
                print(f"  {metric}: {data['previous']:.2f} → {data['current']:.2f} {trend_icon}")
    
    # 输出总结
    summary = results['summary']
    print(f"\n📊 监控总结:")
    print(f"  AI提及率: {summary['mention_rate']*100:.1f}%")
    if summary['average_rank']:
        print(f"  平均排名: #{summary['average_rank']:.1f}")
    print(f"  前3率: {summary['top_3_rate']*100:.1f}%")


if __name__ == '__main__':
    main()
