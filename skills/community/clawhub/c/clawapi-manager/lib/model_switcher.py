#!/usr/bin/env python3
"""
Model Switcher - 模型切换模块
集成自 openclaw-switch，提供安全的模型切换功能
"""

import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class ModelSwitcher:
    def __init__(self, config_path: Optional[str] = None):
        """初始化模型切换器"""
        if config_path is None:
            config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_config(self, config: dict):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write('\n')
    
    def get_primary_model(self) -> str:
        """获取当前主模型"""
        config = self._load_config()
        return config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '(not set)')
    
    def get_fallback_models(self) -> List[str]:
        """获取备用模型列表"""
        config = self._load_config()
        return config.get('agents', {}).get('defaults', {}).get('model', {}).get('fallbacks', [])
    
    def list_all_models(self) -> List[Tuple[int, str, str]]:
        """列出所有可用模型
        
        Returns:
            List of (index, model_id, model_name)
        """
        config = self._load_config()
        providers = config.get('models', {}).get('providers', {})
        
        models = []
        index = 1
        for provider_name, provider_config in providers.items():
            for model in provider_config.get('models', []):
                model_id = f"{provider_name}/{model['id']}"
                model_name = model.get('name', model['id'])
                models.append((index, model_id, model_name))
                index += 1
        
        return models
    
    def switch_primary_model(self, target: str) -> bool:
        """切换主模型
        
        Args:
            target: 模型编号（数字）或模型 ID
        
        Returns:
            True if successful
        """
        # 如果是数字，转换为模型 ID
        if target.isdigit():
            models = self.list_all_models()
            target_num = int(target)
            matching = [m for m in models if m[0] == target_num]
            if not matching:
                raise ValueError(f"Invalid model number: {target}")
            target = matching[0][1]  # model_id
        
        # 检查是否已经是当前模型
        current = self.get_primary_model()
        if target == current:
            return False  # Already using this model
        
        # 更新配置
        config = self._load_config()
        if 'agents' not in config:
            config['agents'] = {}
        if 'defaults' not in config['agents']:
            config['agents']['defaults'] = {}
        if 'model' not in config['agents']['defaults']:
            config['agents']['defaults']['model'] = {}
        
        config['agents']['defaults']['model']['primary'] = target
        self._save_config(config)
        
        # 尝试重启 daemon
        try:
            subprocess.run(['openclaw', 'daemon', 'restart'], 
                          capture_output=True, timeout=5)
        except:
            pass  # Daemon restart is optional
        
        return True
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        config = self._load_config()
        defaults = config.get('agents', {}).get('defaults', {})
        
        # Heartbeat 配置
        heartbeat = defaults.get('heartbeat', {})
        hb_every = heartbeat.get('every', 'off')
        hb_model = heartbeat.get('model', '(follows primary)')
        
        # Subagent 配置
        subagents = defaults.get('subagents', {})
        sub_model = subagents.get('model', '(follows primary)')
        if isinstance(sub_model, dict):
            sub_model = sub_model.get('primary', '(follows primary)')
        
        return {
            'primary': self.get_primary_model(),
            'fallbacks': self.get_fallback_models(),
            'heartbeat': {
                'every': hb_every,
                'model': hb_model
            },
            'subagents': {
                'model': sub_model
            }
        }
    
    def show_status(self):
        """显示状态（格式化输出）"""
        status = self.get_status()
        
        print("\n╔══════════════════════════════════════╗")
        print("║  🔀 Model Switcher Status            ║")
        print("╚══════════════════════════════════════╝")
        print(f"  Primary: {status['primary']}")
        print("\n  ⛓  Fallback chain:")
        print(f"    ① {status['primary']} (primary)")
        
        for i, fb in enumerate(status['fallbacks'], 2):
            print("    ↓ error/429")
            print(f"    ⓪ {fb} (fallback #{i})")
        
        print(f"\n  💓 Heartbeat: every {status['heartbeat']['every']} → {status['heartbeat']['model']}")
        print(f"  🤖 Subagents: {status['subagents']['model']}\n")
    
    def show_models(self):
        """显示所有模型（格式化输出）"""
        current = self.get_primary_model()
        models = self.list_all_models()
        
        print("\n📋 Available models:")
        for index, model_id, model_name in models:
            if model_id == current:
                print(f"  ✔ [{index}] {model_name}  ({model_id})  ← current")
            else:
                print(f"    [{index}] {model_name}  ({model_id})")
        print()


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("\n🔀 Model Switcher — Safe model switching for OpenClaw")
        print("\nUsage:")
        print("  python3 model_switcher.py status     Show current model + fallback chain")
        print("  python3 model_switcher.py list       List all available models")
        print("  python3 model_switcher.py switch N   Switch primary model to number N")
        print()
        return
    
    switcher = ModelSwitcher()
    cmd = sys.argv[1]
    
    if cmd == 'status':
        switcher.show_status()
    
    elif cmd == 'list':
        switcher.show_models()
    
    elif cmd == 'switch':
        if len(sys.argv) < 3:
            print("❌ Usage: model_switcher.py switch <number>")
            sys.exit(1)
        
        target = sys.argv[2]
        try:
            changed = switcher.switch_primary_model(target)
            if changed:
                print(f"✅ Primary model → {switcher.get_primary_model()}")
            else:
                print(f"⚠️  Already using {switcher.get_primary_model()}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
