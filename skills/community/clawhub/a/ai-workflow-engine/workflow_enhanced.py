#!/usr/bin/env python3
"""AI Workflow Enhanced - 增强功能"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable
from dataclasses import dataclass, field


# ==================== AI模型支持 ====================
class AIModel:
    """AI模型统一接口"""
    
    def __init__(self, provider="openai", api_key=None):
        self.provider = provider
        self.api_key = api_key
    
    def chat(self, prompt, model="gpt-4", **kwargs):
        """通用聊天接口"""
        if self.provider == "openai":
            return self._openai_chat(prompt, model, **kwargs)
        elif self.provider == "anthropic":
            return self._anthropic_chat(prompt, model, **kwargs)
        elif self.provider == "deepseek":
            return self._deepseek_chat(prompt, model, **kwargs)
        return {"error": "Unknown provider"}
    
    def _openai_chat(self, prompt, model, **kwargs):
        try:
            import openai
            openai.api_key = self.api_key
            resp = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}], **kwargs)
            return {"content": resp.choices[0].message.content, "model": model}
        except Exception as e:
            return {"error": str(e)}
    
    def _anthropic_chat(self, prompt, model, **kwargs):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            resp = client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
            return {"content": resp.content[0].text, "model": model}
        except Exception as e:
            return {"error": str(e)}
    
    def _deepseek_chat(self, prompt, model="deepseek-chat", **kwargs):
        try:
            import requests
            resp = requests.post("https://api.deepseek.com/v1/chat/completions", 
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]})
            return resp.json()
        except Exception as e:
            return {"error": str(e)}


# ==================== 工作流调度 ====================
class WorkflowScheduler:
    """工作流调度器"""
    
    def __init__(self):
        self.jobs = {}
    
    def schedule(self, workflow, interval_seconds, name=None):
        """定时执行"""
        job_id = name or hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.jobs[job_id] = {
            "workflow": workflow,
            "interval": interval_seconds,
            "last_run": None,
            "enabled": True
        }
        return job_id
    
    def run_pending(self):
        """运行到期的任务"""
        now = datetime.now()
        for job_id, job in list(self.jobs.items()):
            if not job["enabled"]:
                continue
            if job["last_run"] is None or (now - job["last_run"]).total_seconds() >= job["interval"]:
                try:
                    job["workflow"].run()
                    job["last_run"] = now
                except Exception as e:
                    logging.error(f"Job {job_id} failed: {e}")
    
    def cancel(self, job_id):
        """取消任务"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = False
            return True
        return False


# ==================== Webhook触发 ====================
class WebhookTrigger:
    """Webhook触发器"""
    
    def __init__(self):
        self.handlers = {}
    
    def register(self, event, handler):
        """注册处理函数"""
        self.handlers[event] = handler
    
    def trigger(self, event, data):
        """触发"""
        if event in self.handlers:
            return self.handlers[event](data)
        return None
    
    def call_webhook(self, url, method="POST", data=None, headers=None):
        """调用外部Webhook"""
        import requests
        return requests.request(method, url, json=data, headers=headers or {})


# ==================== 缓存系统 ====================
class Cache:
    """简单缓存"""
    
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key):
        if key in self.cache:
            value, expire = self.cache[key]
            if datetime.now().timestamp() < expire:
                return value
            del self.cache[key]
        return None
    
    def set(self, key, value, ttl=None):
        expire = datetime.now().timestamp() + (ttl or self.ttl)
        self.cache[key] = (value, expire)
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        self.cache.clear()


# ==================== 限流器 ====================
class RateLimiter:
    """限流器"""
    
    def __init__(self, max_calls, period_seconds):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = []
    
    def allow(self):
        """检查是否允许调用"""
        now = datetime.now().timestamp()
        self.calls = [t for t in self.calls if now - t < self.period]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
    
    def wait_time(self):
        """等待时间"""
        if len(self.calls) < self.max_calls:
            return 0
        return self.period - (datetime.now().timestamp() - self.calls[0])


# ==================== 消息队列 ====================
class MessageQueue:
    """简单消息队列"""
    
    def __init__(self):
        self.queue = []
    
    def put(self, message):
        """入队"""
        self.queue.append(message)
    
    def get(self):
        """出队"""
        return self.queue.pop(0) if self.queue else None
    
    def size(self):
        """队列大小"""
        return len(self.queue)
    
    def clear(self):
        """清空"""
        self.queue.clear()


# ==================== 观察者模式 ====================
class Observable:
    """观察者"""
    
    def __init__(self):
        self.observers = []
    
    def add_observer(self, observer):
        """添加观察者"""
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        """移除观察者"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self, *args, **kwargs):
        """通知所有观察者"""
        for observer in self.observers:
            observer(*args, **kwargs)


# ==================== 限流工作流 ====================
class RateLimitedWorkflow:
    """限流工作流"""
    
    def __init__(self, workflow, max_calls, period_seconds):
        self.workflow = workflow
        self.limiter = RateLimiter(max_calls, period_seconds)
    
    def run(self, *args, **kwargs):
        if self.limiter.allow():
            return self.workflow.run(*args, **kwargs)
        else:
            wait = self.limiter.wait_time()
            logging.warning(f"Rate limited, wait {wait}s")


# ==================== HTTP中间件 ====================
class HTTPMiddleware:
    """HTTP中间件"""
    
    def __init__(self):
        self.middlewares = []
    
    def use(self, middleware):
        self.middlewares.append(middleware)
    
    def process(self, request):
        for mw in self.middlewares:
            request = mw(request)
        return request


# ==================== 重试策略 ====================
class RetryStrategy:
    """重试策略"""
    
    def __init__(self, max_retries=3, backoff="exponential"):
        self.max_retries = max_retries
        self.backoff = backoff
    
    def execute(self, func, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                if self.backoff == "exponential":
                    time.sleep(2 ** attempt)
                else:
                    time.sleep(1)


# ==================== 断路器 ====================
class CircuitBreaker:
    """断路器"""
    
    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if datetime.now().timestamp() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.now().timestamp()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise e


if __name__ == "__main__":
    print("AI Workflow Enhanced loaded")