#!/usr/bin/env python3
"""
测试 Kimi API 搜索功能
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai import OpenAI

def test_kimi_search():
    """测试 Kimi API 搜索"""
    # 从 .env 加载
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value and key not in os.environ:
                        os.environ[key] = value
    
    api_key = os.getenv("KIMI_API_KEY", "")
    print(f"Kimi API Key 设置: {'是' if api_key else '否'}")
    print(f"Key 长度: {len(api_key)}")
    print(f"Key 前缀: {api_key[:20]}..." if api_key else "Key 为空")
    
    if not api_key:
        print("❌ 错误: KIMI_API_KEY 未设置")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
        
        # 测试简单对话（不带搜索工具）
        print("\n--- 测试 1: 简单对话 ---")
        response = client.chat.completions.create(
            model="kimi-k2-5",
            messages=[
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": "你好，请回复'测试成功'"}
            ],
            temperature=0.3,
            timeout=30
        )
        print(f"✅ 简单对话成功: {response.choices[0].message.content[:50]}...")
        
        # 测试带 web_search 工具的调用
        print("\n--- 测试 2: 带 web_search 工具的搜索 ---")
        response = client.chat.completions.create(
            model="kimi-k2-5",
            messages=[
                {"role": "system", "content": "你是一个新闻搜索助手"},
                {"role": "user", "content": "搜索关于'人工智能'的最新新闻，返回3条"}
            ],
            tools=[{
                "type": "builtin_function",
                "function": {"name": "web_search"}
            }],
            temperature=0.3,
            timeout=60
        )
        
        content = response.choices[0].message.content
        print(f"✅ 搜索成功，返回内容长度: {len(content)}")
        print(f"内容预览: {content[:200]}...")
        return True
        
    except Exception as e:
        print(f"\n❌ 错误类型: {type(e).__name__}")
        print(f"❌ 错误信息: {e}")
        
        # 尝试获取更详细的错误
        if hasattr(e, 'response'):
            print(f"\n--- HTTP 响应详情 ---")
            print(f"Status: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            if hasattr(e.response, 'text'):
                print(f"Body: {e.response.text[:500]}")
        
        # 检查是否是认证错误
        error_str = str(e).lower()
        if "auth" in error_str or "key" in error_str or "unauthorized" in error_str:
            print("\n⚠️ 可能是 API Key 无效或已过期")
        elif "rate" in error_str or "limit" in error_str:
            print("\n⚠️ 可能是 API 速率限制")
        elif "timeout" in error_str or "time out" in error_str:
            print("\n⚠️ 请求超时")
        
        return False

if __name__ == "__main__":
    success = test_kimi_search()
    sys.exit(0 if success else 1)
