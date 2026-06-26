#!/usr/bin/env python3
"""
自动切换模型 - 主程序
监控token使用和API限流，自动切换到备用模型
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path


class AutoModelSwitch:
    def __init__(self, config_path="config.yaml"):
        self.config = self.load_config(config_path)
        self.state = self.load_state()
        self.current_model = self.state.get("current_model", self.config["models"][0]["model"])
        self.token_usage = self.state.get("token_usage", {})
        self.rate_limits = self.state.get("rate_limits", {})
        
    def load_config(self, config_path):
        """加载配置"""
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_state(self):
        """加载状态"""
        state_path = Path("state/model-switch.json")
        if state_path.exists():
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_state(self):
        """保存状态"""
        state_path = Path("state/model-switch.json")
        state_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.state = {
            "current_model": self.current_model,
            "token_usage": self.token_usage,
            "rate_limits": self.rate_limits,
            "last_update": datetime.now().isoformat()
        }
        
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def get_current_model_config(self):
        """获取当前模型配置"""
        for model in self.config["models"]:
            if model["model"] == self.current_model:
                return model
        return None
    
    def check_token_usage(self):
        """检查token使用情况"""
        model_config = self.get_current_model_config()
        if not model_config or not model_config.get("daily_limit"):
            return None
        
        today = datetime.now().strftime("%Y-%m-%d")
        used = self.token_usage.get(today, {}).get(self.current_model, 0)
        limit = model_config["daily_limit"]
        
        return {
            "used": used,
            "limit": limit,
            "percentage": used / limit,
            "remaining": limit - used
        }
    
    def should_switch(self):
        """判断是否需要切换"""
        # 检查token使用
        usage = self.check_token_usage()
        if usage and usage["percentage"] >= self.config["auto_switch"]["critical_threshold"]:
            return True, "token_limit_exceeded"
        
        # 检查限流
        if self.current_model in self.rate_limits:
            limit_info = self.rate_limits[self.current_model]
            if time.time() - limit_info["timestamp"] < limit_info["retry_after"]:
                return True, "rate_limited"
        
        return False, None
    
    def get_next_model(self):
        """获取下一个可用模型"""
        models = sorted(self.config["models"], key=lambda x: x["priority"])
        
        for model in models:
            # 跳过当前模型
            if model["model"] == self.current_model:
                continue
            
            # 跳过限流中的模型
            if model["model"] in self.rate_limits:
                limit_info = self.rate_limits[model["model"]]
                if time.time() - limit_info["timestamp"] < limit_info["retry_after"]:
                    continue
            
            return model
        
        return None
    
    def switch_model(self, reason="manual"):
        """切换模型"""
        should, reason_code = self.should_switch()
        if not should and reason == "auto":
            return False
        
        next_model = self.get_next_model()
        if not next_model:
            self.notify("❌ 所有模型不可用，请等待")
            return False
        
        old_model = self.current_model
        self.current_model = next_model["model"]
        self.save_state()
        
        if self.config["notification"]["enabled"]:
            self.notify(f"✅ 模型切换：{old_model} → {next_model['name']}（{reason}）")
        
        return True
    
    def update_token_usage(self, model, tokens):
        """更新token使用"""
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.token_usage:
            self.token_usage[today] = {}
        
        self.token_usage[today][model] = self.token_usage[today].get(model, 0) + tokens
        self.save_state()
        
        # 检查是否需要警告
        usage = self.check_token_usage()
        if usage and usage["percentage"] >= self.config["auto_switch"]["warning_threshold"]:
            self.notify(f"⚠️ Token使用已达 {usage['percentage']*100:.1f}%")
    
    def record_rate_limit(self, model, retry_after=60):
        """记录限流"""
        self.rate_limits[model] = {
            "timestamp": time.time(),
            "retry_after": retry_after
        }
        self.save_state()
        
        # 自动切换
        self.switch_model("rate_limited")
    
    def notify(self, message):
        """发送通知"""
        print(f"[AutoModelSwitch] {message}")
        # TODO: 集成OpenClaw消息系统
    
    def get_status(self):
        """获取状态"""
        usage = self.check_token_usage()
        model_config = self.get_current_model_config()
        
        status = {
            "current_model": self.current_model,
            "model_name": model_config["name"] if model_config else "Unknown",
            "token_usage": usage
        }
        
        return status


def main():
    """主函数"""
    switcher = AutoModelSwitch()
    
    # 检查状态
    status = switcher.get_status()
    print(f"当前模型: {status['model_name']}")
    
    if status["token_usage"]:
        print(f"Token使用: {status['token_usage']['used']}/{status['token_usage']['limit']}")
    
    # 检查是否需要切换
    should, reason = switcher.should_switch()
    if should:
        print(f"需要切换模型: {reason}")
        switcher.switch_model(reason)


if __name__ == "__main__":
    main()
