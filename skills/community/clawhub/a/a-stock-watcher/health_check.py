#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源健康检查模块
功能：定期检查各数据源可用性，自动选择最优数据源
"""

import requests
import time
from datetime import datetime
from typing import Dict, List

class DataSourceHealth:
    """数据源健康检查类"""
    
    def __init__(self):
        """初始化数据源列表"""
        self.sources = {
            'tencent': {
                'name': '腾讯财经',
                'url': 'http://qt.gtimg.cn/q=sh600000',
                'timeout': 5,
                'priority': 1
            },
            'eastmoney': {
                'name': '东方财富',
                'url': 'http://push2.eastmoney.com/api/qt/stock/get?secid=1.600000&fields=f43,f44,f45',
                'timeout': 5,
                'priority': 2
            },
            'sina': {
                'name': '新浪财经',
                'url': 'http://hq.sinajs.cn/list=sh600000',
                'timeout': 10,
                'priority': 3
            }
        }
        self.health_status = {}
    
    def check_source(self, source_id: str) -> Dict:
        """
        检查单个数据源健康状态
        
        Args:
            source_id: 数据源 ID
        
        Returns:
            健康状态字典
        """
        source = self.sources[source_id]
        result = {
            'id': source_id,
            'name': source['name'],
            'status': 'unknown',
            'response_time': None,
            'error': None,
            'checked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            start_time = time.time()
            response = requests.get(source['url'], timeout=source['timeout'])
            elapsed = (time.time() - start_time) * 1000  # 毫秒
            
            result['response_time'] = round(elapsed, 2)
            
            if response.status_code == 200:
                result['status'] = 'healthy'
            else:
                result['status'] = 'error'
                result['error'] = f'HTTP {response.status_code}'
        
        except requests.Timeout:
            result['status'] = 'timeout'
            result['error'] = '请求超时'
        except requests.ConnectionError:
            result['status'] = 'unreachable'
            result['error'] = '无法连接'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def check_all(self) -> Dict:
        """
        检查所有数据源健康状态
        
        Returns:
            所有数据源的健康状态
        """
        print("=" * 60)
        print("数据源健康检查")
        print("=" * 60)
        
        results = {}
        healthy_count = 0
        
        for source_id in sorted(self.sources.keys(), key=lambda x: self.sources[x]['priority']):
            result = self.check_source(source_id)
            results[source_id] = result
            
            status_icon = "✅" if result['status'] == 'healthy' else "❌"
            response_str = f"{result['response_time']}ms" if result['response_time'] else "N/A"
            
            print(f"\n{status_icon} {result['name']} ({source_id})")
            print(f"   状态：{result['status']}")
            print(f"   响应时间：{response_str}")
            if result['error']:
                print(f"   错误：{result['error']}")
            
            if result['status'] == 'healthy':
                healthy_count += 1
        
        print(f"\n{'='*60}")
        print(f"健康数据源：{healthy_count}/{len(self.sources)}")
        print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        self.health_status = results
        return results
    
    def get_best_source(self) -> str:
        """
        获取最佳可用数据源
        
        Returns:
            最佳数据源 ID
        """
        if not self.health_status:
            self.check_all()
        
        healthy_sources = [
            (sid, data) for sid, data in self.health_status.items()
            if data['status'] == 'healthy' and data['response_time'] is not None
        ]
        
        if not healthy_sources:
            return 'sina'  # 默认降级到新浪
        
        # 按响应时间排序
        healthy_sources.sort(key=lambda x: x[1]['response_time'])
        
        best = healthy_sources[0][0]
        print(f"\n🚀 推荐数据源：{self.sources[best]['name']} ({best})")
        print(f"   响应时间：{healthy_sources[0][1]['response_time']}ms")
        
        return best
    
    def generate_report(self) -> str:
        """
        生成健康检查报告
        
        Returns:
            格式化的报告字符串
        """
        if not self.health_status:
            self.check_all()
        
        report = []
        report.append("╔════════════════════════════════════════╗")
        report.append("║     数据源健康检查报告                 ║")
        report.append(f"║     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}            ║")
        report.append("╚════════════════════════════════════════╝")
        
        healthy_count = sum(1 for s in self.health_status.values() if s['status'] == 'healthy')
        
        report.append(f"\n总体状态：{healthy_count}/{len(self.health_status)} 数据源健康")
        report.append("\n详细状态:")
        report.append("-" * 60)
        
        for sid, data in self.health_status.items():
            icon = "✅" if data['status'] == 'healthy' else "❌"
            report.append(f"{icon} {data['name']} ({sid})")
            report.append(f"   状态：{data['status']}")
            if data['response_time']:
                report.append(f"   响应：{data['response_time']}ms")
            if data['error']:
                report.append(f"   错误：{data['error']}")
            report.append("")
        
        best = self.get_best_source()
        report.append(f"\n💡 建议使用：{self.sources[best]['name']}")
        report.append("-" * 60)
        
        return "\n".join(report)


# 测试
if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    checker = DataSourceHealth()
    
    # 执行健康检查
    checker.check_all()
    
    # 获取最佳数据源
    best = checker.get_best_source()
    
    # 生成报告
    print("\n" + "=" * 60)
    print("完整报告:")
    print("=" * 60)
    report = checker.generate_report()
    print(report)
