#!/usr/bin/env python3
"""
ClawHub技能探索工具版本升级脚本
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class ClawHubSkillUpdater:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.abspath(os.path.join(self.script_dir, '..'))
        self.skill_dir = self.project_dir
        self.current_version = "1.0.0"
        self.new_version = "1.1.0"
    
    def read_config(self):
        """读取技能配置文件"""
        config_file = os.path.join(self.skill_dir, 'config.json')
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            return None
    
    def update_config(self, config):
        """更新配置文件中的API优化设置"""
        print("🔧 优化API调用配置")
        
        config['api'] = {
            "max_retries": 3,
            "base_delay": 5,
            "jitter": 2,
            "rate_limit_window": 60,
            "max_calls_per_window": 50
        }
        
        config['version'] = self.new_version
        config['updated_at'] = datetime.now().isoformat()
        
        return config
    
    def write_config(self, config):
        """写入更新后的配置文件"""
        config_file = os.path.join(self.skill_dir, 'config.json')
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            print("✅ 配置文件更新成功")
            return True
        except Exception as e:
            print(f"❌ 写入配置文件失败: {e}")
            return False
    
    def test_api_config(self):
        """测试API优化配置"""
        print("🧪 测试API优化配置")
        
        config = self.read_config()
        
        if config and 'api' in config:
            api_config = config['api']
            
            print(f"✅ API配置检查通过:")
            print(f"   - 最大重试次数: {api_config['max_retries']}")
            print(f"   - 基础延迟: {api_config['base_delay']}秒")
            print(f"   - 抖动范围: ±{api_config['jitter']}秒")
            print(f"   - 速率限制窗口: {api_config['rate_limit_window']}秒")
            print(f"   - 窗口最大调用数: {api_config['max_calls_per_window']}")
            
            return True
        else:
            print("❌ API配置检查失败")
            return False
    
    def publish_skill(self):
        """发布技能到ClawHub"""
        print("🚀 发布ClawHub技能探索工具到ClawHub")
        
        try:
            result = subprocess.run(
                ['clawhub', 'publish', self.skill_dir, '--version', self.new_version, 
                 '--name', 'ClawHub技能探索工具', 
                 '--changelog', '优化API调用策略，提升技能搜索效率和稳定性，改善API限制问题'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ ClawHub技能探索工具发布成功")
                return True
            else:
                print(f"❌ ClawHub技能探索工具发布失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 发布过程失败: {e}")
            return False
    
    def run_upgrade(self):
        """执行完整升级流程"""
        print("=== ClawHub技能探索工具版本升级 ===")
        
        # 读取当前配置
        config = self.read_config()
        if not config:
            return False
        
        # 更新配置
        updated_config = self.update_config(config)
        
        # 写入更新后的配置
        if not self.write_config(updated_config):
            return False
        
        # 测试配置
        if not self.test_api_config():
            return False
        
        # 发布技能
        if not self.publish_skill():
            print("⚠️ ClawHub技能探索工具发布失败，但配置已更新")
            return False
        
        print("🎉 ClawHub技能探索工具版本升级完成!")
        return True

def main():
    updater = ClawHubSkillUpdater()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = updater.test_api_config()
    else:
        success = updater.run_upgrade()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
