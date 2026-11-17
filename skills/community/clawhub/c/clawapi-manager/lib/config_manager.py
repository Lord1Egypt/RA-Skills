#!/usr/bin/env python3
"""
ClawAPI Config Manager - openclaw.json API 配置管理器
统一管理 providers、keys、models、fallbacks
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ClawAPIConfigManager:
    def __init__(self, config_path: str = None):
        """初始化配置管理器"""
        if config_path is None:
            config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        self.backup_dir = self.config_path.parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> dict:
        """加载配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_config(self, config: dict, backup: bool = True):
        """保存配置（自动备份）"""
        if backup:
            self._backup()
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write('\n')
    
    def _backup(self):
        """备份当前配置"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"openclaw_{timestamp}.json"
        shutil.copy(self.config_path, backup_file)
        
        # 只保留最近 10 个备份
        backups = sorted(self.backup_dir.glob("openclaw_*.json"))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                old_backup.unlink()
        
        return backup_file
    
    # ========== Provider 管理 ==========
    
    def list_providers(self) -> List[Dict]:
        """列出所有 providers"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        result = []
        for name, provider in providers.items():
            result.append({
                'name': name,
                'base_url': provider.get('baseUrl', ''),  # ← 修复：使用 baseUrl
                'api_key': provider.get('apiKey', '')[:8] + '...' if provider.get('apiKey') else '(not set)',
                'model_count': len(provider.get('models', [])),
                'protocol': provider.get('api', 'openai-compatible')
            })
        
        return result
    
    def add_provider(self, name: str, base_url: str, api_key: str, 
                    models: List[Dict] = None, protocol: str = 'openai-compatible'):
        """添加新的 provider"""
        config = self._load_config()
        
        if 'models' not in config:
            config['models'] = {}
        if 'providers' not in config['models']:
            config['models']['providers'] = {}
        
        if name in config['models']['providers']:
            raise ValueError(f"Provider '{name}' already exists")
        
        config['models']['providers'][name] = {
            'baseUrl': base_url,  # ← 修复：使用 baseUrl（小写 U）
            'apiKey': api_key,
            'api': protocol,
            'models': models or []
        }
        
        self._save_config(config)
        return True
    
    def remove_provider(self, name: str):
        """删除 provider"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if name not in providers:
            raise ValueError(f"Provider '{name}' not found")
        
        del providers[name]
        self._save_config(config)
        return True
    
    def update_api_key(self, provider_name: str, new_key: str):
        """更新 API key"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        providers[provider_name]['apiKey'] = new_key
        self._save_config(config)
        return True
    
    # ========== Model 管理 ==========
    
    def list_models(self, provider_name: str = None) -> List[Dict]:
        """列出模型"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        result = []
        
        if provider_name:
            # 只列出指定 provider 的模型
            if provider_name not in providers:
                raise ValueError(f"Provider '{provider_name}' not found")
            
            for model in providers[provider_name].get('models', []):
                result.append({
                    'provider': provider_name,
                    'id': model['id'],
                    'name': model.get('name', model['id']),
                    'full_id': f"{provider_name}/{model['id']}"
                })
        else:
            # 列出所有模型
            for pname, provider in providers.items():
                for model in provider.get('models', []):
                    result.append({
                        'provider': pname,
                        'id': model['id'],
                        'name': model.get('name', model['id']),
                        'full_id': f"{pname}/{model['id']}"
                    })
        
        return result
    
    def add_model(self, provider_name: str, model_id: str, 
                 model_name: str = None, **kwargs):
        """添加模型到 provider"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        model_data = {
            'id': model_id,
            'name': model_name or model_id,
            **kwargs
        }
        
        providers[provider_name]['models'].append(model_data)
        self._save_config(config)
        return True
    
    def remove_model(self, provider_name: str, model_id: str):
        """删除模型"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        models = providers[provider_name]['models']
        providers[provider_name]['models'] = [
            m for m in models if m['id'] != model_id
        ]
        
        self._save_config(config)
        return True
    
    # ========== Primary & Fallback 管理 ==========
    
    def get_primary_model(self) -> str:
        """获取主模型"""
        config = self._load_config()
        return config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '(not set)')
    
    def set_primary_model(self, model_id: str):
        """设置主模型"""
        config = self._load_config()
        
        if 'agents' not in config:
            config['agents'] = {}
        if 'defaults' not in config['agents']:
            config['agents']['defaults'] = {}
        if 'model' not in config['agents']['defaults']:
            config['agents']['defaults']['model'] = {}
        
        config['agents']['defaults']['model']['primary'] = model_id
        self._save_config(config)
        return True
    
    def get_fallbacks(self) -> List[str]:
        """获取 fallback 链"""
        config = self._load_config()
        return config.get('agents', {}).get('defaults', {}).get('model', {}).get('fallbacks', [])
    
    def set_fallbacks(self, fallback_list: List[str]):
        """设置 fallback 链"""
        config = self._load_config()
        
        if 'agents' not in config:
            config['agents'] = {}
        if 'defaults' not in config['agents']:
            config['agents']['defaults'] = {}
        if 'model' not in config['agents']['defaults']:
            config['agents']['defaults']['model'] = {}
        
        config['agents']['defaults']['model']['fallbacks'] = fallback_list
        self._save_config(config)
        return True
    
    def add_fallback(self, model_id: str):
        """添加 fallback 模型"""
        fallbacks = self.get_fallbacks()
        if model_id not in fallbacks:
            fallbacks.append(model_id)
            self.set_fallbacks(fallbacks)
        return True
    
    def remove_fallback(self, model_id: str):
        """删除 fallback 模型"""
        fallbacks = self.get_fallbacks()
        fallbacks = [f for f in fallbacks if f != model_id]
        self.set_fallbacks(fallbacks)
        return True
    
    # ========== 测试 & 验证 ==========
    
    def test_provider(self, provider_name: str) -> Dict:
        """测试 provider 连通性"""
        import requests
        
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        provider = providers[provider_name]
        base_url = provider.get('baseURL', '')
        api_key = provider.get('apiKey', '')
        
        try:
            # 尝试调用 API
            response = requests.get(
                f"{base_url}/models",
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=5
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'message': 'OK' if response.status_code == 200 else response.text[:100]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_backups(self) -> List[Dict]:
        """列出所有备份"""
        backups = sorted(self.backup_dir.glob("openclaw_*.json"), reverse=True)
        
        result = []
        for backup in backups:
            result.append({
                'filename': backup.name,
                'path': str(backup),
                'size': backup.stat().st_size,
                'created': datetime.fromtimestamp(backup.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return result
    
    def restore_backup(self, backup_filename: str):
        """恢复备份"""
        backup_file = self.backup_dir / backup_filename
        
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup not found: {backup_filename}")
        
        # 先备份当前配置
        self._backup()
        
        # 恢复
        shutil.copy(backup_file, self.config_path)
        return True
    
    # ========== 显示 ==========
    
    def show_status(self):
        """显示完整状态"""
        print("\n╔══════════════════════════════════════╗")
        print("║  ClawAPI Config Manager              ║")
        print("╚══════════════════════════════════════╝")
        
        # Primary & Fallbacks
        print(f"\n  Primary: {self.get_primary_model()}")
        print("\n  Fallback chain:")
        for i, fb in enumerate(self.get_fallbacks(), 1):
            print(f"    {i}. {fb}")
        
        # Providers
        print("\n  Providers:")
        for provider in self.list_providers():
            print(f"    • {provider['name']}: {provider['model_count']} models")
        
        # Validation
        validation = self.validate_config()
        if validation['valid']:
            print("\n  ✅ Configuration valid")
        else:
            print("\n  ⚠️  Issues found:")
            for issue in validation['issues']:
                print(f"    - {issue}")
        
        print()
# ========== Channel 管理 ==========
    
    def list_channels(self) -> List[Dict]:
        """列出所有 channels"""
        config = self._load_config()
        channels = config.get('channels', {})
        
        result = []
        for name, channel_config in channels.items():
            result.append({
                'name': name,
                'type': channel_config.get('type', 'unknown'),
                'enabled': channel_config.get('enabled', False),
                'config': 'Configured' if channel_config else 'Not configured'
            })
        
        return result
    
    def add_channel(self, name: str, channel_type: str, config_data: Dict):
        """添加 channel"""
        config = self._load_config()
        
        if 'channels' not in config:
            config['channels'] = {}
        
        if name in config['channels']:
            raise ValueError(f"Channel '{name}' already exists")
        
        config['channels'][name] = {
            'type': channel_type,
            'enabled': True,
            **config_data
        }
        
        self._save_config(config)
        return True
    
    def update_channel(self, name: str, updates: Dict):
        """更新 channel 配置"""
        config = self._load_config()
        channels = config.get('channels', {})
        
        if name not in channels:
            raise ValueError(f"Channel '{name}' not found")
        
        channels[name].update(updates)
        self._save_config(config)
        return True
    
    def remove_channel(self, name: str):
        """删除 channel"""
        config = self._load_config()
        channels = config.get('channels', {})
        
        if name not in channels:
            raise ValueError(f"Channel '{name}' not found")
        
        del channels[name]
        self._save_config(config)
        return True
    
    def toggle_channel(self, name: str):
        """切换 channel 启用状态"""
        config = self._load_config()
        channels = config.get('channels', {})
        
        if name not in channels:
            raise ValueError(f"Channel '{name}' not found")
        
        current = channels[name].get('enabled', False)
        channels[name]['enabled'] = not current
        
        self._save_config(config)
        return not current
    
    # ========== 协议管理 ==========
    
    SUPPORTED_PROTOCOLS = {
        'anthropic-messages': {
            'name': 'Anthropic Messages API',
            'endpoint': '/v1/messages',
            'auth_header': 'x-api-key',
            'description': 'Claude API (Anthropic)'
        },
        'openai-chat': {
            'name': 'OpenAI Chat Completions',
            'endpoint': '/v1/chat/completions',
            'auth_header': 'Authorization',
            'description': 'OpenAI GPT API'
        },
        'openai-compatible': {
            'name': 'OpenAI Compatible',
            'endpoint': '/v1/chat/completions',
            'auth_header': 'Authorization',
            'description': 'OpenAI-compatible API (default)'
        }
    }
    
    def get_provider_protocol(self, provider_name: str) -> str:
        """获取 provider 的协议类型"""
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        # 优先读取配置中的 api 字段
        return providers[provider_name].get('api', 'openai-compatible')
    
    def set_provider_protocol(self, provider_name: str, protocol: str):
        """设置 provider 的协议类型"""
        if protocol not in self.SUPPORTED_PROTOCOLS:
            raise ValueError(f"Unsupported protocol: {protocol}. Supported: {list(self.SUPPORTED_PROTOCOLS.keys())}")
        
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        providers[provider_name]['api'] = protocol
        self._save_config(config)
        return True
    
    def list_protocols(self) -> List[Dict]:
        """列出所有支持的协议"""
        return [
            {
                'id': protocol_id,
                'name': info['name'],
                'description': info['description']
            }
            for protocol_id, info in self.SUPPORTED_PROTOCOLS.items()
        ]




    def validate_config(self):
        """验证配置文件"""
        config = self._load_config()
        issues = []
        
        # 检查默认模型配置
        default_model = config.get('agents', {}).get('defaults', {}).get('model')
        if default_model and isinstance(default_model, str):
            if '/' in default_model:
                parts = default_model.split('/')
                if len(parts) > 2 or ':' in default_model:
                    issues.append({
                        'type': 'invalid_default_model',
                        'current': default_model,
                        'fix': 'Should be: provider/model-id'
                    })
        
        # 检查根级别的无效 key
        invalid_root_keys = ['model']
        for key in invalid_root_keys:
            if key in config:
                issues.append({
                    'type': 'invalid_root_key',
                    'key': key,
                    'value': config[key],
                    'fix': f'Move to agents.defaults.{key}'
                })
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def auto_fix(self):
        """自动修复常见配置问题"""
        validation = self.validate_config()
        if validation['valid']:
            return {'fixed': 0, 'issues': []}
        
        config = self._load_config()
        fixed = []
        
        for issue in validation['issues']:
            if issue['type'] == 'invalid_default_model':
                old = issue['current']
                parts = old.replace(':', '/').split('/')
                if len(parts) >= 2:
                    new = f"{parts[-2]}/{parts[-1]}"
                    if 'agents' not in config:
                        config['agents'] = {}
                    if 'defaults' not in config['agents']:
                        config['agents']['defaults'] = {}
                    config['agents']['defaults']['model'] = new
                    fixed.append(f"Fixed default model: {old} → {new}")
            
            elif issue['type'] == 'invalid_root_key':
                del config[issue['key']]
                fixed.append(f"Removed invalid root key: {issue['key']}")
        
        if fixed:
            self._save_config(config)
        
        return {'fixed': len(fixed), 'issues': fixed}


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("\n🔧 ClawAPI Config Manager")
        print("\nProvider Management:")
        print("  list-providers              List all providers")
        print("  add-provider <name> <url> <key>")

    def validate_config(self) -> dict:
        """验证配置文件"""
        config = self._load_config()
        issues = []
        
        # 检查模型 ID 格式
        providers = config.get('models', {}).get('providers', {})
        for name, provider in providers.items():
            for model in provider.get('models', []):
                model_id = model.get('id', '')
                # 检查是否有错误的前缀
                if '/' in model_id and model_id.count('/') > 1:
                    issues.append({
                        'type': 'invalid_model_id',
                        'provider': name,
                        'model': model_id,
                        'fix': f'{name}/{model_id.split("/")[-1]}'
                    })
        
        # 检查默认模型配置
        default_model = config.get('agents', {}).get('defaults', {}).get('model')
        if default_model and '/' in default_model:
            parts = default_model.split('/')
            if len(parts) > 2 or ':' in default_model:
                issues.append({
                    'type': 'invalid_default_model',
                    'current': default_model,
                    'fix': 'Should be: provider/model-id'
                })
        
        # 检查根级别的无效 key
        invalid_root_keys = ['model']
        for key in invalid_root_keys:
            if key in config:
                issues.append({
                    'type': 'invalid_root_key',
                    'key': key,
                    'value': config[key],
                    'fix': f'Move to agents.defaults.{key}'
                })
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def auto_fix(self) -> dict:
        """自动修复常见配置问题"""
        validation = self.validate_config()
        if validation['valid']:
            return {'fixed': 0, 'issues': []}
        
        config = self._load_config()
        fixed = []
        
        for issue in validation['issues']:
            if issue['type'] == 'invalid_default_model':
                old = issue['current']
                parts = old.replace(':', '/').split('/')
                if len(parts) >= 2:
                    new = f"{parts[-2]}/{parts[-1]}"
                    config['agents']['defaults']['model'] = new
                    fixed.append(f"Fixed default model: {old} → {new}")
            
            elif issue['type'] == 'invalid_root_key':
                del config[issue['key']]
                fixed.append(f"Removed invalid root key: {issue['key']}")
        
        if fixed:
            self._save_config(config)
        
        return {'fixed': len(fixed), 'issues': fixed}
