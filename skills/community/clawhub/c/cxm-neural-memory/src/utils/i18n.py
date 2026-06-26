import yaml
import os
from pathlib import Path
from typing import Dict, Any

class I18n:
    _instance = None
    _data: Dict[str, Any] = {}
    _current_lang = "en"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18n, cls).__new__(cls)
        return cls._instance

    def load(self, lang: str):
        self._current_lang = lang
        locale_path = Path(__file__).parent.parent / "locales" / f"{lang}.yaml"
        
        if not locale_path.exists():
            # Fallback to English
            locale_path = Path(__file__).parent.parent / "locales" / "en.yaml"
            
        if locale_path.exists():
            with open(locale_path, 'r', encoding='utf-8') as f:
                self._data = yaml.safe_load(f) or {}

    def t(self, key_path: str, default: str = None) -> str:
        """Translate a key like 'cli.ask.title'"""
        keys = key_path.split('.')
        value = self._data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default or key_path
        return str(value)

# Global translator instance
i18n = I18n()
_ = i18n.t
