#!/usr/bin/env python3
"""
新闻翻译模块
支持多种翻译服务：
1. MyMemory (免费，无需 API key)
2. 百度翻译 (需要 API key)
3. DeepL (需要 API key)
"""
import requests
import os
import hashlib
import random

class Translator:
    def __init__(self, service='mymemory', api_key=None, secret_key=None):
        """
        初始化翻译器
        
        Args:
            service: 翻译服务 ('mymemory', 'baidu', 'deepl')
            api_key: API key
            secret_key: 密钥 (百度翻译需要)
        """
        self.service = service
        self.api_key = api_key or os.environ.get('TRANSLATE_API_KEY')
        self.secret_key = secret_key or os.environ.get('TRANSLATE_SECRET_KEY')
        
        # 百度翻译配置
        self.baidu_appid = self.api_key
        self.baidu_secret = self.secret_key
        self.baidu_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        
        # MyMemory API (免费)
        self.mymemory_url = 'https://api.mymemory.translated.net/get'
        
        # DeepL API
        self.deepl_url = 'https://api-free.deepl.com/v2/translate'
    
    def translate(self, text, source='en', target='zh'):
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            source: 源语言 ('en', 'zh', 'auto')
            target: 目标语言 ('zh', 'en')
            
        Returns:
            翻译后的文本
        """
        if not text or len(text.strip()) < 5:
            return text
        
        # 检测是否需要翻译
        if source == 'en' and target == 'zh':
            # 简单检测是否包含中文
            if any('\u4e00' <= c <= '\u9fff' for c in text[:100]):
                return text  # 已经包含中文，可能不需要翻译
        
        try:
            if self.service == 'baidu' and self.baidu_appid:
                return self._translate_baidu(text, source, target)
            elif self.service == 'deepl' and self.api_key:
                return self._translate_deepl(text, source, target)
            else:
                return self._translate_mymemory(text, source, target)
        except Exception as e:
            print(f"翻译失败：{e}")
            return text
    
    def _translate_mymemory(self, text, source, target):
        """使用 MyMemory 免费翻译"""
        # MyMemory 有长度限制，分段翻译
        max_len = 400
        segments = []
        
        for i in range(0, len(text), max_len):
            segment = text[i:i+max_len]
            params = {
                'q': segment,
                'langpair': f'{source}|{target}'
            }
            resp = requests.get(self.mymemory_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if 'responseData' in data and 'translatedText' in data['responseData']:
                segments.append(data['responseData']['translatedText'])
            else:
                segments.append(segment)  # 翻译失败，返回原文
        
        return ' '.join(segments)
    
    def _translate_baidu(self, text, source, target):
        """使用百度翻译"""
        # 语言代码转换
        lang_map = {'en': 'en', 'zh': 'zh', 'auto': 'auto'}
        source = lang_map.get(source, 'auto')
        target = lang_map.get(target, 'zh')
        
        # 生成签名
        salt = random.randint(32768, 65536)
        sign_str = f"{self.baidu_appid}{text}{salt}{self.baidu_secret}"
        sign = hashlib.md5(sign_str.encode()).hexdigest()
        
        params = {
            'q': text,
            'from': source,
            'to': target,
            'appid': self.baidu_appid,
            'salt': salt,
            'sign': sign
        }
        
        resp = requests.get(self.baidu_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if 'trans_result' in data:
            return ' '.join([item['dst'] for item in data['trans_result']])
        else:
            raise Exception(f"百度翻译错误：{data.get('error_msg', 'Unknown error')}")
    
    def _translate_deepl(self, text, source, target):
        """使用 DeepL 翻译"""
        # 语言代码转换
        lang_map = {'en': 'EN', 'zh': 'ZH'}
        target_lang = lang_map.get(target, 'ZH')
        
        headers = {
            'Authorization': f'DeepL-Auth-Key {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'text': [text],
            'target_lang': target_lang
        }
        
        resp = requests.post(self.deepl_url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        
        if 'translations' in result:
            return result['translations'][0]['text']
        else:
            raise Exception(f"DeepL 翻译错误：{result}")


def translate_text(text, source='en', target='zh'):
    """
    便捷翻译函数
    
    Args:
        text: 要翻译的文本
        source: 源语言
        target: 目标语言
        
    Returns:
        翻译后的文本
    """
    # 自动选择翻译服务
    translator = Translator()
    return translator.translate(text, source, target)


if __name__ == '__main__':
    # 测试
    test_en = "Many users are switching to Claude following controversies surrounding ChatGPT."
    
    print("测试翻译:")
    print(f"原文：{test_en}")
    print(f"译文：{translate_text(test_en)}")
