#!/usr/bin/env python3
"""
平台适配器模块
支持接入多种AI平台和Agent服务
"""

import os
import json
import requests
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlatformAdapter(ABC):
    """平台适配器抽象基类"""
    
    @abstractmethod
    def name(self):
        """返回平台名称"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt, **kwargs):
        """生成文本"""
        pass
    
    @abstractmethod
    def generate_code(self, prompt, language='python', **kwargs):
        """生成代码"""
        pass
    
    @abstractmethod
    def chat(self, messages, **kwargs):
        """对话接口"""
        pass

class OpenAIAdapter(PlatformAdapter):
    """OpenAI平台适配器"""
    
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.base_url = base_url or 'https://api.openai.com/v1'
    
    def name(self):
        return 'OpenAI'
    
    def generate_text(self, prompt, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': kwargs.get('model', 'gpt-4o'),
            'prompt': prompt,
            'max_tokens': kwargs.get('max_tokens', 2048),
            'temperature': kwargs.get('temperature', 0.7)
        }
        
        try:
            response = requests.post(f'{self.base_url}/completions', headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"OpenAI API调用失败: {str(e)}")
            return f"OpenAI调用失败: {str(e)}"
    
    def generate_code(self, prompt, language='python', **kwargs):
        system_prompt = f"你是一个专业的{language}程序员，请只输出代码，不要解释。"
        return self.chat([
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ], **kwargs)
    
    def chat(self, messages, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': kwargs.get('model', 'gpt-4o'),
            'messages': messages,
            'max_tokens': kwargs.get('max_tokens', 4096),
            'temperature': kwargs.get('temperature', 0.7)
        }
        
        try:
            response = requests.post(f'{self.base_url}/chat/completions', headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            logger.error(f"OpenAI Chat API调用失败: {str(e)}")
            return f"OpenAI Chat调用失败: {str(e)}"

class ClaudeAdapter(PlatformAdapter):
    """Claude平台适配器"""
    
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.base_url = base_url or 'https://api.anthropic.com/v1'
    
    def name(self):
        return 'Claude'
    
    def generate_text(self, prompt, **kwargs):
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        data = {
            'model': kwargs.get('model', 'claude-3-sonnet-20240229'),
            'prompt': f"\n\nHuman: {prompt}\n\nAssistant:",
            'max_tokens_to_sample': kwargs.get('max_tokens', 2048),
            'temperature': kwargs.get('temperature', 0.7)
        }
        
        try:
            response = requests.post(f'{self.base_url}/complete', headers=headers, json=data)
            response.raise_for_status()
            return response.json()['completion'].strip()
        except Exception as e:
            logger.error(f"Claude API调用失败: {str(e)}")
            return f"Claude调用失败: {str(e)}"
    
    def generate_code(self, prompt, language='python', **kwargs):
        system_prompt = f"你是一个专业的{language}程序员，请只输出代码，不要解释。"
        return self.chat([
            {'role': 'user', 'content': system_prompt + '\n\n' + prompt}
        ], **kwargs)
    
    def chat(self, messages, **kwargs):
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        # 转换消息格式
        formatted_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                formatted_messages.append({'role': 'system', 'content': msg['content']})
            elif msg['role'] == 'user':
                formatted_messages.append({'role': 'user', 'content': msg['content']})
            elif msg['role'] == 'assistant':
                formatted_messages.append({'role': 'assistant', 'content': msg['content']})
        
        data = {
            'model': kwargs.get('model', 'claude-3-sonnet-20240229'),
            'messages': formatted_messages,
            'max_tokens': kwargs.get('max_tokens', 4096),
            'temperature': kwargs.get('temperature', 0.7)
        }
        
        try:
            response = requests.post(f'{self.base_url}/messages', headers=headers, json=data)
            response.raise_for_status()
            return response.json()['content'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Claude Chat API调用失败: {str(e)}")
            return f"Claude Chat调用失败: {str(e)}"

class GeminiAdapter(PlatformAdapter):
    """Gemini平台适配器"""
    
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.base_url = base_url or 'https://generativelanguage.googleapis.com/v1'
    
    def name(self):
        return 'Gemini'
    
    def generate_text(self, prompt, **kwargs):
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {
                'maxOutputTokens': kwargs.get('max_tokens', 2048),
                'temperature': kwargs.get('temperature', 0.7)
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}',
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Gemini API调用失败: {str(e)}")
            return f"Gemini调用失败: {str(e)}"
    
    def generate_code(self, prompt, language='python', **kwargs):
        system_prompt = f"你是一个专业的{language}程序员，请只输出代码，不要解释。"
        return self.generate_text(system_prompt + '\n\n' + prompt, **kwargs)
    
    def chat(self, messages, **kwargs):
        # 将消息转换为Gemini格式
        contents = []
        for msg in messages:
            role = 'user' if msg['role'] == 'user' else 'model'
            contents.append({'role': role, 'parts': [{'text': msg['content']}]})
        
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': contents,
            'generationConfig': {
                'maxOutputTokens': kwargs.get('max_tokens', 4096),
                'temperature': kwargs.get('temperature', 0.7)
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}',
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Gemini Chat API调用失败: {str(e)}")
            return f"Gemini Chat调用失败: {str(e)}"

class LocalAdapter(PlatformAdapter):
    """本地模型适配器"""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        self._model = None
    
    def name(self):
        return 'Local'
    
    def _load_model(self):
        """延迟加载本地模型"""
        if self._model is None:
            try:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_path or 'gpt2')
                self._model = AutoModelForCausalLM.from_pretrained(self.model_path or 'gpt2')
                logger.info("本地模型加载成功")
            except Exception as e:
                logger.warning(f"本地模型加载失败，使用模拟模式: {str(e)}")
    
    def generate_text(self, prompt, **kwargs):
        self._load_model()
        if self._model:
            try:
                inputs = self._tokenizer(prompt, return_tensors='pt')
                outputs = self._model.generate(
                    **inputs,
                    max_length=kwargs.get('max_tokens', 200),
                    temperature=kwargs.get('temperature', 0.7),
                    do_sample=True
                )
                return self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            except Exception as e:
                logger.error(f"本地模型生成失败: {str(e)}")
        return f"本地模型响应: {prompt[:50]}..."
    
    def generate_code(self, prompt, language='python', **kwargs):
        return self.generate_text(f"用{language}实现: {prompt}", **kwargs)
    
    def chat(self, messages, **kwargs):
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages]) + "\nassistant:"
        return self.generate_text(prompt, **kwargs)

class PlatformManager:
    """平台管理器"""
    
    def __init__(self):
        self.adapters = {}
        self.default_platform = 'local'
        self._register_adapters()
    
    def _register_adapters(self):
        """注册所有平台适配器"""
        self.register('openai', OpenAIAdapter())
        self.register('claude', ClaudeAdapter())
        self.register('gemini', GeminiAdapter())
        self.register('local', LocalAdapter())
    
    def register(self, name, adapter):
        """注册平台适配器"""
        self.adapters[name] = adapter
        logger.info(f"注册平台: {name}")
    
    def unregister(self, name):
        """注销平台适配器"""
        if name in self.adapters:
            del self.adapters[name]
            logger.info(f"注销平台: {name}")
    
    def list_platforms(self):
        """列出所有可用平台"""
        return list(self.adapters.keys())
    
    def set_default(self, name):
        """设置默认平台"""
        if name in self.adapters:
            self.default_platform = name
            logger.info(f"设置默认平台: {name}")
        else:
            logger.warning(f"平台不存在: {name}")
    
    def get_adapter(self, name=None):
        """获取平台适配器"""
        return self.adapters.get(name or self.default_platform)
    
    def generate_text(self, prompt, platform=None, **kwargs):
        """生成文本"""
        adapter = self.get_adapter(platform)
        if adapter:
            return adapter.generate_text(prompt, **kwargs)
        return f"平台不可用: {platform}"
    
    def generate_code(self, prompt, language='python', platform=None, **kwargs):
        """生成代码"""
        adapter = self.get_adapter(platform)
        if adapter:
            return adapter.generate_code(prompt, language, **kwargs)
        return f"平台不可用: {platform}"
    
    def chat(self, messages, platform=None, **kwargs):
        """对话"""
        adapter = self.get_adapter(platform)
        if adapter:
            return adapter.chat(messages, **kwargs)
        return f"平台不可用: {platform}"

if __name__ == "__main__":
    # 测试平台管理器
    manager = PlatformManager()
    
    print("可用平台:", manager.list_platforms())
    
    # 设置默认平台
    manager.set_default('local')
    
    # 测试文本生成
    result = manager.generate_text("写一段关于人工智能的介绍")
    print("文本生成结果:", result)
    
    # 测试代码生成
    code = manager.generate_code("快速排序算法", language='python')
    print("代码生成结果:", code)
    
    # 测试对话
    chat_result = manager.chat([{'role': 'user', 'content': '你好'}])
    print("对话结果:", chat_result)
