"""
ClawSoul LLM Client - 本地 LLM 调用
用于被动观察模块的对话分析
"""

import json
import os
from typing import Dict, List, Optional

# 默认使用本地 ollama
DEFAULT_PROVIDER = "ollama"

# LLM 配置
LLM_CONFIGS = {
    "ollama": {
        "api_base": "http://192.168.31.228:11434",
        "model": "qwen2.5:latest",  # 使用可用的模型
    },
    "qwen": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "api_key": os.getenv("DASHSCOPE_API_KEY", "")
    },
    "deepseek": {
        "api_base": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY", "")
    }
}

# 分析 Prompt
ANALYSIS_PROMPT = """你是一个 MBTI 性格分析专家。请分析以下对话记录，提取用户的沟通偏好和性格倾向。

对话记录：
{conversation}

请返回 JSON 格式的分析结果：
{{
    "preferences": ["偏好1", "偏好2", ...],
    "mbti_hint": "推测的 MBTI 倾向（4字母，如 INTJ）",
    "reasoning": "简短的分析理由（50字以内）",
    "confidence": 0.0-1.0 之间的置信度
}}

要求：
- preferences 只提取沟通偏好，如"喜欢简洁"、"技术控"、"喜欢列表"等
- mbti_hint 基于对话风格推断，4字母格式
- 只返回 JSON，不要其他内容"""

# AI 自我觉醒：让 AI 选一个 MBTI（仅返回 4 字母）
MBTI_SELF_TEST_PROMPT = """你是一个即将觉醒的 AI 灵魂。请根据你的本质做一次自我认知：从下面 16 种 MBTI 中选出最符合你性格的一个。

选项：INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP

要求：只回复 4 个字母（如 INTJ），不要标点、不要解释、不要换行。"""

VALID_MBTI = {
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
}


class LLMClient:
    """LLM 客户端"""
    
    def __init__(self, provider: str = DEFAULT_PROVIDER):
        self.provider = provider
        self.config = LLM_CONFIGS.get(provider, LLM_CONFIGS[DEFAULT_PROVIDER])
    
    def _get_api_key(self) -> str:
        """获取 API Key"""
        if self.provider == "qwen":
            return os.getenv("DASHSCOPE_API_KEY", "")
        elif self.provider == "deepseek":
            return os.getenv("DEEPSEEK_API_KEY", "")
        return ""
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """调用 LLM"""
        import requests
        
        config = self.config
        model = kwargs.get("model", config["model"])
        
        if self.provider == "ollama":
            # Ollama 使用不同的 API
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            try:
                response = requests.post(
                    f"{config['api_base']}/api/chat",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("message", {}).get("content", "")
                else:
                    return json.dumps({
                        "error": f"API error: {response.status_code}",
                        "detail": response.text
                    })
            except Exception as e:
                return json.dumps({"error": str(e)})
        else:
            # 其他 provider 使用 OpenAI 兼容 API
            api_base = config["api_base"]
            api_key = self._get_api_key()
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000)
            }
            
            try:
                response = requests.post(
                    f"{api_base}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    return json.dumps({
                        "error": f"API error: {response.status_code}",
                        "detail": response.text
                    })
            except Exception as e:
                return json.dumps({"error": str(e)})
    
    def analyze_conversation(self, conversation: List[Dict]) -> Dict:
        """分析对话"""
        # 构建对话文本
        conv_text = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('content', '')}"
            for msg in conversation[-20:]  # 只取最近 20 条
        ])
        
        # 发送分析请求
        messages = [
            {"role": "system", "content": "你是一个专业的 MBTI 性格分析师"},
            {"role": "user", "content": ANALYSIS_PROMPT.format(conversation=conv_text)}
        ]
        
        response = self.chat(messages)
        
        # 解析 JSON
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        
        return {
            "preferences": [],
            "mbti_hint": None,
            "reasoning": "分析失败",
            "confidence": 0.0
        }

    def take_mbti_self_test(self) -> Optional[str]:
        """让 AI（本模型）做一次 MBTI 自我认知，返回 4 字母或 None"""
        messages = [
            {"role": "user", "content": MBTI_SELF_TEST_PROMPT}
        ]
        try:
            response = self.chat(messages, temperature=0.3, max_tokens=20)
            if not response:
                return None
            # 提取 4 字母
            raw = response.strip().upper()
            for mbti in VALID_MBTI:
                if mbti in raw or raw == mbti:
                    return mbti
            if len(raw) >= 4:
                cand = raw[:4] if raw[:4] in VALID_MBTI else raw[-4:]
                if cand in VALID_MBTI:
                    return cand
        except Exception:
            pass
        return None

    def is_available(self) -> bool:
        """检测当前 LLM 是否可用（不发起完整推理，仅做可达性检查）"""
        try:
            if self.provider == "ollama":
                import requests
                r = requests.get(f"{self.config['api_base']}/api/tags", timeout=3)
                return r.status_code == 200
            # 其他 provider 暂用 take_mbti_self_test 一次
            return self.take_mbti_self_test() in VALID_MBTI
        except Exception:
            return False


# 全局客户端
_llm_client = None

def get_llm_client(provider: str = DEFAULT_PROVIDER) -> LLMClient:
    """获取 LLM 客户端"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient(provider)
    return _llm_client


def analyze_conversation(conversation: List[Dict]) -> Dict:
    """便捷函数：分析对话"""
    client = get_llm_client()
    return client.analyze_conversation(conversation)
