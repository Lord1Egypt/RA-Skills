#!/usr/bin/env python3
"""
域名资产评估仪表盘
提供域名资产总览、到期分布、价值统计和资产建议
"""
import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aliyun_domain import AliyunDomainClient

# 域名后缀价值参考（首年注册价）
SUFFIX_VALUE = {
    'com': 90,
    'cn': 38,
    'net': 90,
    'xyz': 7,
    'io': 380,
    'vip': 15,
    'top': 10,
    'club': 15,
    'shop': 30,
    'info': 20,
    'biz': 20,
    'me': 20,
    'co': 200,
    'ai': 800,
    'cloud': 50,
    'tech': 50,
    'store': 30,
    'online': 30,
    'site': 20,
    'fun': 10,
    'space': 10,
    'live': 20,
    'work': 10,
    'shop': 30,
    'pro': 20,
    'xin': 39,
    'wang': 20,
    'group': 20,
    'site': 10,
    'cyou': 10,
    'cc': 100,
    'tv': 300,
    'asia': 30,
    'mobi': 20,
    'name': 20,
}

# 长度价值系数
LENGTH_MULTIPLIER = {
    1: 1000,  # 单字母
    2: 500,   # 双字母
    3: 200,   # 三字母
    4: 100,   # 四字母
    5: 50,    # 五字母
    6: 20,    # 六字母
    7: 10,    # 七字母
    8: 5,     # 八字母
}

# 关键词价值
KEYWORD_VALUE = {
    'ai': 500,
    'bot': 300,
    'tech': 200,
    'cloud': 200,
    'data': 200,
    'code': 200,
    'dev': 150,
    'app': 150,
    'web': 150,
    'net': 150,
    'lab': 100,
    'hub': 100,
    'pro': 100,
    'plus': 100,
    'max': 100,
}


class DomainAssetDashboard:
    """域名资产评估仪表盘"""
    
    def __init__(self):
        self.client = AliyunDomainClient()
        self.domains = []
        self.assessment = {}
    
    def fetch_domains(self):
        """获取账号下所有域名"""
        print("📊 正在获取域名列表...")
        self.domains = self.client.get_all_domains()
        print(f"✅ 共获取 {len(self.domains)} 个域名")
        return self.domains
    
    def get_domain_details(self, domain_name):
        """获取域名详细信息"""
        try:
            return self.client.query_domain_detail(domain_name)
        except Exception as e:
            return None
    
    def assess_domain_value(self, domain_name):
        """评估单个域名价值"""
        # 提取域名各部分
        parts = domain_name.lower().split('.')
        if len(parts) < 2:
            return {'base_value': 0, 'total_value': 0}
        
        name = parts[0]
        suffix = parts[-1]
        
        # 基础价值（后缀）
        base_value = SUFFIX_VALUE.get(suffix, 50)
        
        # 长度系数
        length = len(name)
        length_mult = LENGTH_MULTIPLIER.get(length, 1)
        if length > 8:
            length_mult = 0.5
        elif length > 12:
            length_mult = 0.2
        
        # 关键词价值
        keyword_bonus = 0
        for keyword, value in KEYWORD_VALUE.items():
            if keyword in name.lower():
                keyword_bonus += value
                break  # 只计算第一个匹配的关键词
        
        # 数字价值
        number_bonus = 0
        if name.isdigit():
            if len(name) <= 3:
                number_bonus = 10000
            elif len(name) <= 4:
                number_bonus = 1000
            elif len(name) <= 5:
                number_bonus = 500
            elif len(name) <= 6:
                number_bonus = 200
        elif any(c.isdigit() for c in name):
            # 含数字
            number_bonus = 50
        
        # 计算总价值
        total_value = (base_value * length_mult) + keyword_bonus + number_bonus
        
        # 市场估值（参考成交价）
        market_value = total_value * 10  # 粗略估算
        
        return {
            'base_value': base_value,
            'length': length,
            'length_multiplier': length_mult,
            'keyword_bonus': keyword_bonus,
            'number_bonus': number_bonus,
            'total_value': total_value,
            'market_value': market_value,
            'suffix': suffix
        }
    
    def analyze_expiration(self, domain_name):
        """分析域名到期时间"""
        try:
            info = self.client.query_domain_detail(domain_name)
            if info and 'ExpirationDate' in info:
                exp_date = info['ExpirationDate']
                # 解析日期
                try:
                    if isinstance(exp_date, str):
                        # 支持多种日期格式
                        for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                            try:
                                exp_datetime = datetime.strptime(exp_date, fmt)
                                break
                            except:
                                continue
                        else:
                            # 如果都失败，尝试直接分割
                            exp_datetime = datetime.strptime(exp_date.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    
                    days_left = (exp_datetime - datetime.now()).days
                    
                    if days_left < 0:
                        status = 'expired'
                    elif days_left <= 7:
                        status = 'urgent'
                    elif days_left <= 30:
                        status = 'warning'
                    elif days_left <= 90:
                        status = 'normal'
                    else:
                        status = 'safe'
                    
                    return {
                        'expiration_date': exp_date,
                        'days_left': days_left,
                        'status': status
                    }
                except Exception as e:
                    return {
                        'expiration_date': exp_date,
                        'days_left': None,
                        'status': 'unknown'
                    }
        except:
            pass
        
        return {
            'expiration_date': None,
            'days_left': None,
            'status': 'unknown'
        }
    
    def generate_assessment(self):
        """生成完整资产评估"""
        if not self.domains:
            self.fetch_domains()
        
        assessment = {
            'summary': {
                'total_domains': len(self.domains),
                'total_value': 0,
                'total_market_value': 0,
                'total_renewal_cost': 0
            },
            'domains': [],
            'expiration_distribution': defaultdict(int),
            'suffix_distribution': defaultdict(int),
            'value_distribution': defaultdict(int),
            'recommendations': []
        }
        
        # 分析每个域名
        for domain in self.domains:
            domain_name = domain.get('DomainName', '')
            
            # 价值评估
            value = self.assess_domain_value(domain_name)
            
            # 到期分析
            expiration = self.analyze_expiration(domain_name)
            
            # 后缀统计
            suffix = value.get('suffix', 'unknown')
            assessment['suffix_distribution'][suffix] += 1
            
            # 到期分布
            exp_status = expiration.get('status', 'unknown')
            assessment['expiration_distribution'][exp_status] += 1
            
            # 价值分布
            market_value = value.get('market_value', 0)
            if market_value < 100:
                assessment['value_distribution']['<100'] += 1
            elif market_value < 500:
                assessment['value_distribution']['100-500'] += 1
            elif market_value < 1000:
                assessment['value_distribution']['500-1000'] += 1
            elif market_value < 5000:
                assessment['value_distribution']['1000-5000'] += 1
            else:
                assessment['value_distribution']['>5000'] += 1
            
            # 累计价值
            assessment['summary']['total_value'] += value.get('total_value', 0)
            assessment['summary']['total_market_value'] += market_value
            assessment['summary']['total_renewal_cost'] += SUFFIX_VALUE.get(suffix, 50)
            
            # 域名详情
            domain_assessment = {
                'domain_name': domain_name,
                'value': value,
                'expiration': expiration,
                'status': domain.get('DomainStatus', '')
            }
            assessment['domains'].append(domain_assessment)
        
        # 生成建议
        assessment['recommendations'] = self._generate_recommendations(assessment)
        
        self.assessment = assessment
        return assessment
    
    def _generate_recommendations(self, assessment):
        """生成资产建议"""
        recommendations = []
        
        # 到期建议
        exp_dist = assessment['expiration_distribution']
        if exp_dist.get('expired', 0) > 0:
            recommendations.append({
                'type': 'urgent',
                'title': '🚨 紧急：有域名已过期',
                'description': f"发现 {exp_dist['expired']} 个域名已过期，需立即处理！",
                'action': '立即续费或赎回'
            })
        
        if exp_dist.get('urgent', 0) > 0:
            recommendations.append({
                'type': 'urgent',
                'title': '⚠️ 警告：有域名即将到期（7 天内）',
                'description': f"发现 {exp_dist['urgent']} 个域名将在 7 天内到期",
                'action': '立即安排续费'
            })
        
        if exp_dist.get('warning', 0) > 0:
            recommendations.append({
                'type': 'warning',
                'title': '📅 提醒：有域名 30 天内到期',
                'description': f"发现 {exp_dist['warning']} 个域名将在 30 天内到期",
                'action': '规划续费预算'
            })
        
        # 价值建议
        value_dist = assessment['value_distribution']
        high_value = value_dist.get('>5000', 0) + value_dist.get('1000-5000', 0)
        if high_value > 0:
            recommendations.append({
                'type': 'opportunity',
                'title': '💎 高价值域名',
                'description': f"发现 {high_value} 个高价值域名（估值>1000 元）",
                'action': '重点保护，考虑出售或开发'
            })
        
        # 后缀建议
        suffix_dist = assessment['suffix_distribution']
        total = assessment['summary']['total_domains']
        
        if suffix_dist.get('com', 0) < total * 0.3 and total > 5:
            recommendations.append({
                'type': 'suggestion',
                'title': '💡 建议增加.com 域名',
                'description': f".com 域名仅 {suffix_dist.get('com', 0)} 个，占比偏低",
                'action': '考虑注册核心品牌的.com 后缀'
            })
        
        # 成本优化建议
        renewal_cost = assessment['summary']['total_renewal_cost']
        if renewal_cost > 1000:
            recommendations.append({
                'type': 'cost',
                'title': '💰 续费成本优化',
                'description': f"年续费成本约¥{renewal_cost}元",
                'action': '考虑使用优惠口令或批量续费'
            })
        
        return recommendations
    
    def print_dashboard(self):
        """打印仪表盘"""
        if not self.assessment:
            self.generate_assessment()
        
        print("\n" + "=" * 80)
        print("🦐 域小虾 - 域名资产评估仪表盘")
        print("=" * 80)
        print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 总体概览
        summary = self.assessment['summary']
        print("📊 资产总览")
        print("-" * 80)
        print(f"  域名总数：     {summary['total_domains']} 个")
        print(f"  评估总价值：   ¥{summary['total_value']:,.0f} 元（注册成本）")
        print(f"  市场估值：     ¥{summary['total_market_value']:,.0f} 元（参考成交价）")
        print(f"  年续费成本：   ¥{summary['total_renewal_cost']:,.0f} 元")
        print(f"  平均单个价值：¥{summary['total_value'] / max(summary['total_domains'], 1):,.0f} 元")
        print()
        
        # 到期分布
        print("⏰ 到期分布")
        print("-" * 80)
        exp_dist = self.assessment['expiration_distribution']
        status_map = {
            'expired': ('🚨 已过期', 'red'),
            'urgent': ('⚠️ 7 天内', 'orange'),
            'warning': ('📅 30 天内', 'yellow'),
            'normal': ('✅ 90 天内', 'blue'),
            'safe': ('🛡️ 安全', 'green'),
            'unknown': ('❓ 未知', 'gray')
        }
        for status, (label, color) in status_map.items():
            count = exp_dist.get(status, 0)
            if count > 0:
                bar = '█' * min(count, 20)
                print(f"  {label:<12} {count:>3} 个 {bar}")
        print()
        
        # 后缀分布
        print("🌐 后缀分布")
        print("-" * 80)
        suffix_dist = sorted(self.assessment['suffix_distribution'].items(), 
                           key=lambda x: x[1], reverse=True)
        for suffix, count in suffix_dist[:10]:
            percentage = count / max(summary['total_domains'], 1) * 100
            bar = '█' * int(percentage / 5)
            print(f"  .{suffix:<8} {count:>3} 个 ({percentage:>5.1f}%) {bar}")
        print()
        
        # 价值分布
        print("💎 价值分布")
        print("-" * 80)
        value_dist = self.assessment['value_distribution']
        for range_name, count in value_dist.items():
            if count > 0:
                percentage = count / max(summary['total_domains'], 1) * 100
                bar = '█' * int(percentage / 5)
                print(f"  {range_name:<12} {count:>3} 个 ({percentage:>5.1f}%) {bar}")
        print()
        
        # 域名详情（TOP 10）
        print("🏆 高价值域名 TOP 10")
        print("-" * 80)
        sorted_domains = sorted(self.assessment['domains'], 
                              key=lambda x: x['value'].get('market_value', 0), 
                              reverse=True)
        print(f"{'排名':<6} {'域名':<30} {'后缀':<8} {'估值':<12} {'到期状态':<12}")
        print("-" * 80)
        for i, d in enumerate(sorted_domains[:10], 1):
            domain_name = d['domain_name'][:28]
            suffix = d['value'].get('suffix', 'N/A')
            market_value = d['value'].get('market_value', 0)
            exp_status = d['expiration'].get('status', 'unknown')
            status_map = {
                'expired': '🚨 过期',
                'urgent': '⚠️ 紧急',
                'warning': '📅 警告',
                'normal': '✅ 正常',
                'safe': '🛡️ 安全',
                'unknown': '❓ 未知'
            }
            status_label = status_map.get(exp_status, exp_status)
            print(f"{i:<6} {domain_name:<30} .{suffix:<7} ¥{market_value:>8,} {status_label:<12}")
        print()
        
        # 资产建议
        print("💡 资产建议")
        print("-" * 80)
        type_priority = {'urgent': 0, 'warning': 1, 'opportunity': 2, 'cost': 3, 'suggestion': 4}
        sorted_recommendations = sorted(self.assessment['recommendations'], 
                                       key=lambda x: type_priority.get(x['type'], 5))
        for rec in sorted_recommendations:
            print(f"  {rec['title']}")
            print(f"    {rec['description']}")
            print(f"    建议：{rec['action']}")
            print()
        
        # 快速操作链接
        print("🔗 快速操作")
        print("-" * 80)
        print("  1. 续费到期域名：https://domain.console.aliyun.com/renew")
        print("  2. 域名管理控制台：https://domain.console.aliyun.com")
        print("  3. 域名交易：https://jiyi.aliyun.com")
        print()
        
        print("=" * 80)


def main():
    """主函数"""
    dashboard = DomainAssetDashboard()
    
    # 获取域名
    dashboard.fetch_domains()
    
    # 生成评估
    dashboard.generate_assessment()
    
    # 打印仪表盘
    dashboard.print_dashboard()
    
    # 保存评估报告
    report_path = os.path.join(os.path.dirname(__file__), '../reports/domain_assessment.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        # 转换 defaultdict 为普通 dict
        assessment = dashboard.assessment.copy()
        assessment['expiration_distribution'] = dict(assessment['expiration_distribution'])
        assessment['suffix_distribution'] = dict(assessment['suffix_distribution'])
        assessment['value_distribution'] = dict(assessment['value_distribution'])
        
        json.dump(assessment, f, ensure_ascii=False, indent=2)
    
    print(f"📄 评估报告已保存：{report_path}")


if __name__ == "__main__":
    main()
