#!/usr/bin/env python3
"""
ClawHub技能探索工具延迟发布脚本
用于解决API速率限制问题
"""

import time
import random
import subprocess
from datetime import datetime

class DelayedPublisher:
    def __init__(self):
        self.skill_dir = '/Users/sunyanguang/.openclaw/workspace/custom-skills/clawhub-skill-explorer'
        self.wait_minutes = random.uniform(2, 5)
        self.max_retries = 3
    
    def wait_for_rate_limit(self):
        """等待API速率限制解除"""
        print(f"等待 {self.wait_minutes:.1f} 分钟后重试")
        time.sleep(self.wait_minutes * 60)
    
    def publish_skill(self, retry_count=0):
        """发布技能到ClawHub"""
        print(f"📦 第 {retry_count + 1} 次发布尝试")
        
        try:
            result = subprocess.run(
                ['clawhub', 'publish', self.skill_dir, '--version', '1.1.0',
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
                error_msg = result.stderr.strip()
                
                if "Rate limit exceeded" in error_msg or "429" in error_msg:
                    print("⚠️ API速率限制，等待后重试")
                    self.wait_for_rate_limit()
                    return self.publish_skill(retry_count + 1)
                else:
                    print(f"❌ ClawHub技能探索工具发布失败: {error_msg}")
                    return False
        
        except Exception as e:
            print(f"❌ 发布过程失败: {e}")
            
            if retry_count < self.max_retries:
                print("等待后重试...")
                self.wait_for_rate_limit()
                return self.publish_skill(retry_count + 1)
            else:
                return False
    
    def run(self):
        """执行延迟发布"""
        print("=== ClawHub技能探索工具延迟发布 ===")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.publish_skill():
            print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print("💔 所有发布尝试均失败")
            return False

def main():
    publisher = DelayedPublisher()
    success = publisher.run()
    
    if success:
        print("🎉 ClawHub技能探索工具版本升级完成!")
        return 0
    else:
        print("❌ 延迟发布失败")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
