#!/usr/bin/env python3
"""
API Key Rotation Manager
支持多个 API Key 的轮换和管理
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class KeyRotationManager:
    def __init__(self, config_path: str = None):
        """初始化 Key 轮换管理器"""
        if config_path is None:
            config_path = Path.home() / '.openclaw' / 'openclaw.json'
        
        self.config_path = Path(config_path)
        self.rotation_state_path = self.config_path.parent / 'key-rotation-state.json'
    
    def _load_rotation_state(self) -> dict:
        """加载轮换状态"""
        if not self.rotation_state_path.exists():
            return {
                'providers': {},
                'version': '1.0'
            }
        
        with open(self.rotation_state_path, 'r') as f:
            return json.load(f)
    
    def _save_rotation_state(self, state: dict):
        """保存轮换状态"""
        with open(self.rotation_state_path, 'w') as f:
            json.dump(state, f, indent=2)
            f.write('\n')
    
    def add_keys(self, provider_name: str, keys: List[str]):
        """为 provider 添加多个 API Key"""
        state = self._load_rotation_state()
        
        if provider_name not in state['providers']:
            state['providers'][provider_name] = {
                'keys': [],
                'current_index': 0,
                'key_stats': {}
            }
        
        provider_state = state['providers'][provider_name]
        
        # 添加新 Key
        for key in keys:
            if key not in provider_state['keys']:
                provider_state['keys'].append(key)
                provider_state['key_stats'][key] = {
                    'last_used': None,
                    'error_count': 0,
                    'cooldown_until': None,
                    'disabled_until': None,
                    'disabled_reason': None
                }
        
        self._save_rotation_state(state)
        return True
    
    def get_current_key(self, provider_name: str) -> Optional[str]:
        """获取当前应该使用的 Key"""
        state = self._load_rotation_state()
        
        if provider_name not in state['providers']:
            return None
        
        provider_state = state['providers'][provider_name]
        keys = provider_state['keys']
        
        if not keys:
            return None
        
        # 找到第一个可用的 Key
        now = time.time()
        
        for i in range(len(keys)):
            idx = (provider_state['current_index'] + i) % len(keys)
            key = keys[idx]
            stats = provider_state['key_stats'][key]
            
            # 检查是否在 Cooldown
            if stats['cooldown_until'] and stats['cooldown_until'] > now:
                continue
            
            # 检查是否被禁用
            if stats['disabled_until'] and stats['disabled_until'] > now:
                continue
            
            # 找到可用的 Key
            provider_state['current_index'] = idx
            stats['last_used'] = now
            self._save_rotation_state(state)
            
            return key
        
        # 所有 Key 都不可用，返回第一个
        return keys[0]
    
    def rotate_key(self, provider_name: str, reason: str = 'rate_limit'):
        """轮换到下一个 Key"""
        state = self._load_rotation_state()
        
        if provider_name not in state['providers']:
            return False
        
        provider_state = state['providers'][provider_name]
        keys = provider_state['keys']
        
        if len(keys) <= 1:
            return False
        
        # 记录当前 Key 的错误
        current_key = keys[provider_state['current_index']]
        stats = provider_state['key_stats'][current_key]
        stats['error_count'] += 1
        
        # 设置 Cooldown
        if reason == 'rate_limit':
            # 指数退避：1分钟 → 5分钟 → 25分钟 → 1小时
            cooldown_minutes = [1, 5, 25, 60]
            error_count = min(stats['error_count'], len(cooldown_minutes))
            cooldown_seconds = cooldown_minutes[error_count - 1] * 60
            stats['cooldown_until'] = time.time() + cooldown_seconds
        
        elif reason == 'billing':
            # 余额不足：禁用 5 小时
            stats['disabled_until'] = time.time() + (5 * 3600)
            stats['disabled_reason'] = 'billing'
        
        # 切换到下一个 Key
        provider_state['current_index'] = (provider_state['current_index'] + 1) % len(keys)
        
        self._save_rotation_state(state)
        return True
    
    def get_key_stats(self, provider_name: str) -> List[Dict]:
        """获取所有 Key 的统计信息"""
        state = self._load_rotation_state()
        
        if provider_name not in state['providers']:
            return []
        
        provider_state = state['providers'][provider_name]
        keys = provider_state['keys']
        
        result = []
        now = time.time()
        
        for i, key in enumerate(keys):
            stats = provider_state['key_stats'][key]
            
            # 计算状态
            status = 'active'
            status_detail = None
            
            if stats['disabled_until'] and stats['disabled_until'] > now:
                status = 'disabled'
                remaining = int((stats['disabled_until'] - now) / 60)
                status_detail = f"{stats['disabled_reason']} ({remaining} min)"
            
            elif stats['cooldown_until'] and stats['cooldown_until'] > now:
                status = 'cooldown'
                remaining = int((stats['cooldown_until'] - now) / 60)
                status_detail = f"{remaining} min"
            
            result.append({
                'index': i,
                'key': key[:8] + '...' if len(key) > 8 else key,
                'status': status,
                'status_detail': status_detail,
                'error_count': stats['error_count'],
                'last_used': datetime.fromtimestamp(stats['last_used']).strftime('%Y-%m-%d %H:%M:%S') if stats['last_used'] else 'Never',
                'is_current': i == provider_state['current_index']
            })
        
        return result
    
    def reset_key_stats(self, provider_name: str, key_index: int = None):
        """重置 Key 的统计信息"""
        state = self._load_rotation_state()
        
        if provider_name not in state['providers']:
            return False
        
        provider_state = state['providers'][provider_name]
        keys = provider_state['keys']
        
        if key_index is not None:
            # 重置指定 Key
            if key_index >= len(keys):
                return False
            
            key = keys[key_index]
            provider_state['key_stats'][key] = {
                'last_used': None,
                'error_count': 0,
                'cooldown_until': None,
                'disabled_until': None,
                'disabled_reason': None
            }
        else:
            # 重置所有 Key
            for key in keys:
                provider_state['key_stats'][key] = {
                    'last_used': None,
                    'error_count': 0,
                    'cooldown_until': None,
                    'disabled_until': None,
                    'disabled_reason': None
                }
        
        self._save_rotation_state(state)
        return True

def main():
    """测试"""
    manager = KeyRotationManager()
    
    # 添加测试 Key
    manager.add_keys('openai', [
        'sk-test-key-1',
        'sk-test-key-2',
        'sk-test-key-3'
    ])
    
    # 获取当前 Key
    current = manager.get_current_key('openai')
    print(f"Current key: {current}")
    
    # 查看统计
    stats = manager.get_key_stats('openai')
    for s in stats:
        print(f"Key {s['index']}: {s['key']} - {s['status']} - Errors: {s['error_count']}")

if __name__ == '__main__':
    main()
