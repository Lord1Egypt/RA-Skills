#!/usr/bin/env python3
"""
热点域名投资分析工具
根据市场热点关键词，推荐可投资的域名组合
"""
import json
import sys
import os
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aliyun_domain import AliyunDomainClient

# 热点关键词库
HOT_KEYWORDS = {
    # AI/技术热点
    "ai": {
        "name": "人工智能",
        "suffixes": [".cn", ".com", ".xyz", ".io"],
        "prefixes": ["get", "try", "use", "my", "the"],
        "suffixes_price": {"cn": 38, "com": 90, "xyz": 7, "io": 380},
        "hot_level": 5
    },
    "agent": {
        "name": "AI 智能体",
        "suffixes": [".cn", ".xyz", ".io"],
        "prefixes": ["get", "try", "my"],
        "suffixes_price": {"cn": 38, "xyz": 7, "io": 380},
        "hot_level": 5
    },
    "bot": {
        "name": "机器人/自动化",
        "suffixes": [".cn", ".xyz", ".io"],
        "prefixes": ["get", "try", "my"],
        "suffixes_price": {"cn": 38, "xyz": 7, "io": 380},
        "hot_level": 4
    },
    "claw": {
        "name": "Claw 热点（OpenClaw）",
        "suffixes": [".cn", ".com", ".xyz", ".io"],
        "prefixes": ["get", "try", "use", "my"],
        "suffixes_price": {"cn": 38, "com": 90, "xyz": 7, "io": 380},
        "hot_level": 5,
        "note": "2026 年 GitHub 最火开源 AI 项目，18 万星"
    },
    "qwen": {
        "name": "通义千问",
        "suffixes": [".cn", ".com", ".xyz"],
        "prefixes": ["get", "try", "my"],
        "suffixes_price": {"cn": 38, "com": 90, "xyz": 7},
        "hot_level": 4
    },
    
    # 数字吉利组合
    "168": {
        "name": "一路发",
        "suffixes": [".cn", ".com"],
        "prefixes": [],
        "suffixes_price": {"cn": 38, "com": 90},
        "hot_level": 3
    },
    "518": {
        "name": "我要发",
        "suffixes": [".cn", ".com"],
        "prefixes": [],
        "suffixes_price": {"cn": 38, "com": 90},
        "hot_level": 3
    },
    "678": {
        "name": "顺顺发",
        "suffixes": [".cn", ".com"],
        "prefixes": [],
        "suffixes_price": {"cn": 38, "com": 90},
        "hot_level": 3
    },
    "886": {
        "name": "发发顺",
        "suffixes": [".cn", ".com"],
        "prefixes": [],
        "suffixes_price": {"cn": 38, "com": 90},
        "hot_level": 3
    },
}

# 组合模式
COMBINATION_PATTERNS = [
    "{keyword}{number}",  # claw168
    "{prefix}{keyword}",  # getclaw
    "{keyword}{suffix}",  # clawio
]

# 吉利数字
LUCKY_NUMBERS = ["168", "518", "678", "886", "138", "158", "999", "888"]


def extract_suffix(domain: str) -> str:
    """从域名中提取后缀（不带点）
    
    Args:
        domain: 完整域名，如 tryagent.cn
        
    Returns:
        后缀字符串，如 cn
    """
    # 使用正则表达式提取最后一个点之后的部分
    match = re.search(r'\.([a-zA-Z]+)$', domain)
    if match:
        return match.group(1)
    return ""


def generate_buy_link(domain: str, duration: int = 12) -> str:
    """生成阿里云购买链接
    
    Args:
        domain: 完整域名，如 tryagent.cn
        duration: 购买年限，默认 12 个月
        
    Returns:
        阿里云购买链接
    """
    suffix = extract_suffix(domain)
    # 从域名中移除后缀部分，获取纯域名
    domain_name = re.sub(r'\.[a-zA-Z]+$', '', domain)
    
    base_url = "https://wanwang.aliyun.com/buy/commonbuy"
    params = f"?domain={domain_name}&suffix={suffix}&duration={duration}"
    
    return base_url + params


class DomainInvestmentAnalyzer:
    """域名投资分析器"""
    
    def __init__(self):
        self.client = AliyunDomainClient()
        self.results = []
    
    def generate_domains(self, keyword: str, max_count: int = 50) -> list:
        """生成域名候选列表"""
        if keyword not in HOT_KEYWORDS:
            return []
        
        config = HOT_KEYWORDS[keyword]
        domains = []
        
        # 基础组合：keyword + 后缀
        for suffix in config["suffixes"]:
            domain = f"{keyword}{suffix}"
            domains.append(domain)
        
        # 前缀组合：prefix + keyword + 后缀
        for prefix in config.get("prefixes", []):
            for suffix in config["suffixes"]:
                domain = f"{prefix}{keyword}{suffix}"
                domains.append(domain)
        
        # 数字组合：keyword + 数字 + 后缀
        for number in LUCKY_NUMBERS[:6]:  # 限制数字数量
            for suffix in config["suffixes"]:
                if suffix in [".cn"]:  # 数字组合主要针对.cn
                    domain = f"{keyword}{number}{suffix}"
                    domains.append(domain)
        
        return domains[:max_count]
    
    def check_availability(self, domains: list) -> list:
        """批量检查域名可注册性"""
        available = []
        registered = []
        
        print(f"🔍 检查 {len(domains)} 个域名...")
        
        for i, domain in enumerate(domains, 1):
            try:
                result = self.client.check_domain(domain)
                is_avail = result.get('available', False)
                price_info = result.get('price_info', [])
                price = price_info[0].get('money', 'N/A') if price_info else 'N/A'
                
                domain_info = {
                    'domain': domain,
                    'available': is_avail,
                    'price': price,
                    'keyword': self._extract_keyword(domain)
                }
                
                if is_avail:
                    available.append(domain_info)
                    print(f"  [{i}/{len(domains)}] ✅ {domain:<25} ¥{price}")
                else:
                    registered.append(domain_info)
                    # print(f"  [{i}/{len(domains)}] ❌ {domain} 已注册")
                    
            except Exception as e:
                # print(f"  [{i}/{len(domains)}] ⚠️ {domain} 检查失败：{e}")
                pass
        
        return available, registered
    
    def _extract_keyword(self, domain: str) -> str:
        """从域名提取关键词"""
        for kw in HOT_KEYWORDS.keys():
            if kw in domain.lower():
                return kw
        return "unknown"
    
    def analyze(self, keyword: str, max_check: int = 50) -> dict:
        """分析热点关键词域名投资机会"""
        if keyword not in HOT_KEYWORDS:
            return {
                'success': False,
                'error': f'未知关键词：{keyword}'
            }
        
        config = HOT_KEYWORDS[keyword]
        print(f"\n🔥 热点分析：{config['name']} ({keyword})")
        print(f"热度等级：{'⭐' * config['hot_level']}")
        if 'note' in config:
            print(f"备注：{config['note']}")
        print("=" * 70)
        
        # 生成候选域名
        domains = self.generate_domains(keyword, max_check)
        print(f"📋 生成 {len(domains)} 个候选域名")
        
        # 检查可注册性
        available, registered = self.check_availability(domains)
        
        # 分析结果
        result = {
            'success': True,
            'keyword': keyword,
            'keyword_name': config['name'],
            'hot_level': config['hot_level'],
            'total_checked': len(domains),
            'available_count': len(available),
            'registered_count': len(registered),
            'available_domains': available,
            'recommendations': self._generate_recommendations(available, config)
        }
        
        return result
    
    def _generate_recommendations(self, available: list, config: dict) -> list:
        """生成投资建议"""
        if not available:
            return []
        
        recommendations = []
        
        # 按优先级排序
        priority_order = []
        for d in available:
            domain = d['domain']
            if 'agent' in domain or 'bot' in domain or 'ai' in domain:
                priority_order.append((1, d))
            elif 'dev' in domain or 'code' in domain or 'io' in domain:
                priority_order.append((2, d))
            elif 'xyz' in domain:
                priority_order.append((3, d))
            elif any(num in domain for num in ['168', '518', '678', '886']):
                priority_order.append((4, d))
            else:
                priority_order.append((5, d))
        
        priority_order.sort(key=lambda x: (x[0], x[1]['domain']))
        
        # 生成 TOP 推荐
        for i, (_, d) in enumerate(priority_order[:10], 1):
            reason = self._get_investment_reason(d['domain'])
            buy_link = generate_buy_link(d['domain'])
            recommendations.append({
                'rank': i,
                'domain': d['domain'],
                'price': d['price'],
                'reason': reason,
                'buy_link': buy_link
            })
        
        return recommendations
    
    def _get_investment_reason(self, domain: str) -> str:
        """获取投资理由"""
        if 'agent' in domain or 'bot' in domain:
            return "🤖 AI 智能体热点"
        elif 'ai' in domain:
            return "🧠 AI 概念"
        elif 'dev' in domain or 'code' in domain:
            return "💻 开发者工具"
        elif 'io' in domain:
            return "⚡ 科技创业首选"
        elif 'xyz' in domain:
            return "💰 经济实惠"
        elif any(num in domain for num in ['168', '518', '678', '886']):
            return "🔢 吉利数字"
        else:
            return "📌 简短易记"
    
    def print_report(self, result: dict):
        """打印投资分析报告"""
        if not result.get('success'):
            print(f"❌ {result.get('error')}")
            return
        
        print("\n" + "=" * 70)
        print(f"📊 投资分析报告：{result['keyword_name']}")
        print("=" * 70)
        print(f"关键词：{result['keyword']}")
        print(f"热度等级：{'⭐' * result['hot_level']}")
        print(f"检查数量：{result['total_checked']} 个")
        print(f"可注册：{result['available_count']} 个 ✅")
        print(f"已注册：{result['registered_count']} 个 ❌")
        
        if result['recommendations']:
            print("\n💡 投资推荐 TOP 10:")
            print("-" * 70)
            print(f"{'排名':<6} {'域名':<25} {'价格':<12} {'理由':<25}")
            print("-" * 70)
            
            for rec in result['recommendations']:
                # 生成可点击的 Markdown 链接
                domain_link = f"[{rec['domain']}]({rec['buy_link']})"
                print(f"{rec['rank']:<6} {domain_link:<45} ¥{str(rec['price']):<12} {rec['reason']:<25}")
            
            # 计算总价
            total = sum(r['price'] for r in result['recommendations'] if isinstance(r['price'], (int, float)))
            print("-" * 70)
            print(f"TOP 10 总计：约 ¥{total} 元")
            
            # 打印购买链接列表
            print("\n🔗 快速购买链接:")
            print("-" * 70)
            for rec in result['recommendations']:
                print(f"  {rec['rank']:2d}. {rec['buy_link']}")
        
        print("\n📈 投资建议:")
        self._print_investment_advice(result)
    
    def _print_investment_advice(self, result: dict):
        """打印投资建议"""
        keyword = result['keyword']
        config = HOT_KEYWORDS.get(keyword, {})
        
        if result['hot_level'] >= 4:
            print("  ⭐⭐⭐⭐⭐ 高热度关键词，建议尽快注册核心域名")
        elif result['hot_level'] >= 3:
            print("  ⭐⭐⭐⭐ 中等热度，可选择性注册优质域名")
        else:
            print("  ⭐⭐⭐ 一般热度，建议谨慎投资")
        
        if 'note' in config:
            print(f"  💡 {config['note']}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='热点域名投资分析')
    parser.add_argument('keyword', nargs='?', help='热点关键词（如：claw, ai, agent）')
    parser.add_argument('--list', action='store_true', help='列出所有支持的热点关键词')
    parser.add_argument('--max', type=int, default=50, help='最大检查数量')
    
    args = parser.parse_args()
    
    analyzer = DomainInvestmentAnalyzer()
    
    if args.list:
        print("🔥 支持的热点关键词:")
        print("=" * 60)
        for kw, config in HOT_KEYWORDS.items():
            print(f"  {kw:<15} {config['name']:<20} 热度：{'⭐' * config['hot_level']}")
            if 'note' in config:
                print(f"                  💡 {config['note']}")
        return
    
    if not args.keyword:
        parser.print_help()
        return
    
    # 执行分析
    result = analyzer.analyze(args.keyword, args.max)
    analyzer.print_report(result)


if __name__ == "__main__":
    main()
