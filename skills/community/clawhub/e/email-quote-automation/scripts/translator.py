"""
Translation module
Supports translating non-target language emails to target language
翻译模块
支持将非目标语言邮件翻译为目标语言
"""

import re
import sys
import os

# Add config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))
import config

from langdetect import detect

try:
    from googletrans import Translator as GoogleFreeTranslator
except ImportError:
    GoogleFreeTranslator = None

def is_target_language(text):
    """Detect if text is already in target language"""
    target_lang = config.TRANSLATION_CONFIG['default_target_lang']
    if target_lang.startswith('zh'):
        # For Chinese, check if it contains enough Chinese characters
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]+', text))
        total_chars = len(text.strip())
        if total_chars == 0:
            return True
        return (chinese_chars / total_chars) > 0.3
    else:
        # For other languages, use langdetect
        try:
            detected = detect(text)
            return detected.startswith(target_lang.split('-')[0])
        except:
            return True

class Translator:
    def __init__(self):
        self.config = config.TRANSLATION_CONFIG
        self.engine = self.config['engine']
        self.target_lang = self.config['default_target_lang']
        self.translator = None
        
        if self.engine == 'google_free' and GoogleFreeTranslator:
            self.translator = GoogleFreeTranslator()
    
    def translate(self, text):
        """Translate text, return original if already in target language"""
        if not self.config['enabled']:
            return text, False
        
        if is_target_language(text):
            return text, False
        
        if self.engine == 'none':
            return text, False
        
        if self.engine == 'google_free' and self.translator:
            try:
                result = self.translator.translate(text, dest=self.target_lang)
                return result.text, True
            except Exception as e:
                print(f"Google translation error: {e}")
                return text, False
        
        # If translation fails or engine unavailable, return original
        return text, False

def translate_text(text):
    """Convenience function to translate text"""
    trans = Translator()
    return trans.translate(text)
