#!/usr/bin/env python3
"""
Usage Statistics Manager
使用统计管理器
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class UsageStatsManager:
    def __init__(self, config_path: str = None):
        """初始化使用统计管理器"""
        if config_path is None:
            config_path = Path.home() / '.openclaw' / 'openclaw.json'
        
        self.config_path = Path(config_path)
        self.stats_path = self.config_path.parent / 'usage-stats.json'
    
    def _load_stats(self) -> dict:
        """加载统计数据"""
        if not self.stats_path.exists():
            return {
                'providers': {},
                'version': '1.0'
            }
        
        with open(self.stats_path, 'r') as f:
            return json.load(f)
    
    def _save_stats(self, stats: dict):
        """保存统计数据"""
        with open(self.stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
            f.write('\n')
    
    def record_request(self, provider_name: str, success: bool = True):
        """记录请求"""
        stats = self._load_stats()
        
        if provider_name not in stats['providers']:
            stats['providers'][provider_name] = {
                'total_requests': 0,
                'success_requests': 0,
                'error_requests': 0,
                'last_used': None,
                'first_used': None,
                'errors': {}
            }
        
        provider_stats = stats['providers'][provider_name]
        
        # 更新计数
        provider_stats['total_requests'] += 1
        if success:
            provider_stats['success_requests'] += 1
        else:
            provider_stats['error_requests'] += 1
        
        # 更新时间
        now = time.time()
        provider_stats['last_used'] = now
        if not provider_stats['first_used']:
            provider_stats['first_used'] = now
        
        self._save_stats(stats)
    
    def record_error(self, provider_name: str, error_type: str):
        """记录错误"""
        stats = self._load_stats()
        
        if provider_name not in stats['providers']:
            self.record_request(provider_name, success=False)
            stats = self._load_stats()
        
        provider_stats = stats['providers'][provider_name]
        
        # 记录错误类型
        if error_type not in provider_stats['errors']:
            provider_stats['errors'][error_type] = 0
        provider_stats['errors'][error_type] += 1
        
        self._save_stats(stats)
    
    def get_provider_stats(self, provider_name: str) -> Dict:
        """获取 provider 统计"""
        stats = self._load_stats()
        
        if provider_name not in stats['providers']:
            return {
                'provider': provider_name,
                'total_requests': 0,
                'success_requests': 0,
                'error_requests': 0,
                'success_rate': 0.0,
                'last_used': 'Never',
                'first_used': 'Never',
                'errors': {}
            }
        
        provider_stats = stats['providers'][provider_name]
        
        # 计算成功率
        total = provider_stats['total_requests']
        success_rate = (provider_stats['success_requests'] / total * 100) if total > 0 else 0.0
        
        return {
            'provider': provider_name,
            'total_requests': provider_stats['total_requests'],
            'success_requests': provider_stats['success_requests'],
            'error_requests': provider_stats['error_requests'],
            'success_rate': round(success_rate, 2),
            'last_used': datetime.fromtimestamp(provider_stats['last_used']).strftime('%Y-%m-%d %H:%M:%S') if provider_stats['last_used'] else 'Never',
            'first_used': datetime.fromtimestamp(provider_stats['first_used']).strftime('%Y-%m-%d %H:%M:%S') if provider_stats['first_used'] else 'Never',
            'errors': provider_stats['errors']
        }
    
    def get_all_stats(self) -> List[Dict]:
        """获取所有 provider 的统计"""
        stats = self._load_stats()
        
        result = []
        for provider_name in stats['providers'].keys():
            result.append(self.get_provider_stats(provider_name))
        
        # 按请求数排序
        result.sort(key=lambda x: x['total_requests'], reverse=True)
        
        return result
    
    def reset_stats(self, provider_name: str = None):
        """重置统计"""
        stats = self._load_stats()
        
        if provider_name:
            # 重置指定 provider
            if provider_name in stats['providers']:
                del stats['providers'][provider_name]
        else:
            # 重置所有
            stats['providers'] = {}
        
        self._save_stats(stats)
        return True
    
    def format_stats(self, provider_stats: Dict) -> str:
        """格式化统计输出"""
        output = f"**{provider_stats['provider']}**\n"
        output += f"总请求: {provider_stats['total_requests']}\n"
        output += f"成功: {provider_stats['success_requests']}\n"
        output += f"失败: {provider_stats['error_requests']}\n"
        output += f"成功率: {provider_stats['success_rate']}%\n"
        output += f"首次使用: {provider_stats['first_used']}\n"
        output += f"最后使用: {provider_stats['last_used']}\n"
        
        if provider_stats['errors']:
            output += "\n错误类型:\n"
            for error_type, count in provider_stats['errors'].items():
                output += f"  • {error_type}: {count}\n"
        
        return output

def main():
    """测试"""
    manager = UsageStatsManager()
    
    # 模拟请求
    manager.record_request('openai', success=True)
    manager.record_request('openai', success=True)
    manager.record_request('openai', success=False)
    manager.record_error('openai', 'rate_limit')
    
    # 查看统计
    stats = manager.get_provider_stats('openai')
    print(manager.format_stats(stats))

if __name__ == '__main__':
    main()
