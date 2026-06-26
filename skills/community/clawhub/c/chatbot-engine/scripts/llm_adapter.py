"""
LLM Adapter - LLM 适配器
支持多种 LLM 服务
"""

from typing import List, Dict, Optional, Any
import os


class LLMAdapter:
    """LLM 适配器"""
    
    PROVIDERS = ['openai', 'anthropic', 'local', 'mock']
    
    def __init__(self, provider: str = 'mock', model: Optional[str] = None,
                api_key: Optional[str] = None, **kwargs):
        """
        初始化 LLM 适配器
        
        Args:
            provider: 提供商 (openai, anthropic, local, mock)
            model: 模型名称
            api_key: API 密钥
        """
        self.provider = provider
        self.model = model or self._get_default_model(provider)
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.client = None
        
        self._init_client(**kwargs)
    
    def _get_default_model(self, provider: str) -> str:
        """获取默认模型"""
        defaults = {
            'openai': 'gpt-3.5-turbo',
            'anthropic': 'claude-3-sonnet-20240229',
            'local': 'llama2',
            'mock': 'mock-model'
        }
        return defaults.get(provider, 'mock-model')
    
    def _init_client(self, **kwargs):
        """初始化客户端"""
        if self.provider == 'openai':
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("openai 包未安装")
        
        elif self.provider == 'anthropic':
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                print("anthropic 包未安装")
        
        elif self.provider == 'local':
            # 本地模型支持
            pass
    
    def generate(self, prompt: str, context: Optional[List[Dict]] = None,
                max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        生成回复
        
        Args:
            prompt: 提示词
            context: 上下文消息列表
            max_tokens: 最大 token 数
            temperature: 温度参数
        
        Returns:
            生成的文本
        """
        messages = self._build_messages(prompt, context)
        
        if self.provider == 'openai' and self.client:
            return self._openai_generate(messages, max_tokens, temperature)
        
        elif self.provider == 'anthropic' and self.client:
            return self._anthropic_generate(prompt, max_tokens, temperature)
        
        elif self.provider == 'local':
            return self._local_generate(messages, max_tokens, temperature)
        
        else:
            return self._mock_generate(prompt)
    
    def _build_messages(self, prompt: str,
                       context: Optional[List[Dict]]) -> List[Dict]:
        """构建消息列表"""
        messages = []
        
        if context:
            messages.extend(context)
        
        messages.append({'role': 'user', 'content': prompt})
        return messages
    
    def _openai_generate(self, messages: List[Dict], max_tokens: int,
                        temperature: float) -> str:
        """OpenAI 生成"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI 生成失败: {e}")
            return self._mock_generate(messages[-1]['content'])
    
    def _anthropic_generate(self, prompt: str, max_tokens: int,
                           temperature: float) -> str:
        """Anthropic 生成"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic 生成失败: {e}")
            return self._mock_generate(prompt)
    
    def _local_generate(self, messages: List[Dict], max_tokens: int,
                       temperature: float) -> str:
        """本地模型生成"""
        # 简化版，实际实现需要加载本地模型
        return self._mock_generate(messages[-1]['content'])
    
    def _mock_generate(self, prompt: str) -> str:
        """模拟生成 (用于测试)"""
        responses = {
            '你好': '你好！有什么我可以帮助你的吗？',
            '再见': '再见！祝您有愉快的一天！',
        }
        
        for key, value in responses.items():
            if key in prompt:
                return value
        
        return f"我理解您的问题: '{prompt[:30]}...'。这是一个模拟回复。"


if __name__ == '__main__':
    # 测试
    llm = LLMAdapter(provider='mock')
    
    print(llm.generate("你好"))
    print(llm.generate("解释一下量子计算"))
