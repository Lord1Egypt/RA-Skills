#!/usr/bin/env python3
"""
统一 LLM 调用接口

配置环境变量：
  LLM_MODEL     - 模型名称，如 gpt-4o-mini、claude-3-haiku 等
  LLM_API_KEY  - 对应的 API Key

使用方式：
  from llm import get_llm_config, call_llm
  model, api_key = get_llm_config()
  response = call_llm(model, prompt_text, api_key)
"""

import json
import os
import sys
import urllib.request
import urllib.error


def get_llm_config() -> tuple:
    """读取 LLM 配置，返回 (model, api_key)"""
    model = os.environ.get("LLM_MODEL", "").strip()
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    return model, api_key


def call_llm(model: str, prompt: str, api_key: str) -> str:
    """
    调用 LLM（OpenAI 兼容接口）

    Args:
        model:   模型名称，如 gpt-4o-mini
        prompt:  发送给模型的提示词
        api_key: API Key

    Returns:
        模型输出的文本

    Raises:
        打印错误信息并返回空字符串
    """
    if not model or not api_key:
        print("【错误】LLM_MODEL 或 LLM_API_KEY 未配置")
        print("请配置环境变量后重试：")
        print("  export LLM_MODEL=your_model_name")
        print("  export LLM_API_KEY=your_api_key")
        return ""

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1200,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return "⚠️ AI 返回内容为空"
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            msg = err_body.get("error", {}).get("message", str(e.code))
        except Exception:
            msg = str(e.code)
        print(f"【HTTP 错误 {e.code}】{msg}")
        return f"⚠️ API 调用失败（HTTP {e.code}）：{msg}"
    except Exception as e:
        print(f"【网络错误】{e}")
        return f"⚠️ 网络错误：{e}"


if __name__ == "__main__":
    model, api_key = get_llm_config()
    if not model or not api_key:
        print("=" * 50)
        print("【错误】LLM 模型未配置")
        print()
        print("请配置以下环境变量：")
        print("  export LLM_MODEL=your_model_name")
        print("  export LLM_API_KEY=your_api_key")
        print()
        print("例如：")
        print("  export LLM_MODEL=gpt-4o-mini")
        print("  export LLM_API_KEY=sk-xxx")
        print("=" * 50)
        sys.exit(1)

    print(f"模型：{model}")
    print("（直接运行 llm.py 无实际用途，请从其他脚本导入使用）")
