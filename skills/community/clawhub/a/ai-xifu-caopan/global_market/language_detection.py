#!/usr/bin/env python3
"""
🌍 语言检测模块 — 大叔亲授·审题+质检机制
========================================
从旅行引擎移植到媳妇智投，实现全球双语方案自动匹配。

审题：检测用户输入的语言 → 输出用用户的语言
质检：匹配目标市场的语言 → 输出用市场的语言
输出：{输入语言} / {市场语言} 双语
同语言合并：输入语言=市场语言时单语

版本：v1.0.0 (移植自global-travel-planner v1.14.1)
"""

# ── Language mapping: ISO code → native name ──
LANG_MAP = {
    "zh": "中文",
    "en": "English",
    "ko": "한국어",
    "ja": "日本語",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "pt": "Português",
    "ru": "Русский",
    "ar": "العربية",
    "th": "ไทย",
    "vi": "Tiếng Việt",
    "id": "Bahasa Indonesia",
    "ms": "Bahasa Melayu",
    "hi": "हिन्दी",
    "nl": "Nederlands",
    "it": "Italiano",
    "tr": "Türkçe",
    "pl": "Polski",
    "sv": "Svenska",
    "tl": "Filipino",
    "mn": "Монгол",
    "km": "ភាសាខ្មែរ",
    "lo": "ລາວ",
    "my": "မြန်မာ",
    "ru": "Русский",
    "th": "ไทย",
    "hi": "हिन्दी",
    "el": "Ελληνικά",
    "he": "עברית",
    "ur": "اردو",
    "bn": "বাংলা",
    "ne": "नेपाली",
    "am": "አማርኛ",
    "ha": "Hausa",
    "sw": "Kiswahili",
    "yo": "Yorùbá",
    "ig": "Igbo",
    "zu": "isiZulu",
    "af": "Afrikaans",
    "ka": "ქართული",
    "hy": "Հայերեն",
    "si": "සිංහල",
    "bo": "བོད་སྐད།",
    "dv": "ދިވެހި",
    "chr": "ᏣᎳᎩ",
    "iu": "ᐃᓄᒃᑎᑐᑦ",
    "ii": "ꆈꌠꉙ",
}

# ── Market ISO code → native language code ──
# 大叔说：看目的地匹配语言（质检机制）
MARKET_LANG = {
    # East & Southeast Asia
    "cn": "zh", "hk": "zh", "tw": "zh",
    "jp": "ja", "kr": "ko",
    "th": "th", "vn": "vi", "id": "id", "my": "ms", "sg": "en",
    "ph": "tl", "mn": "mn",
    # South Asia
    "in": "hi", "lk": "si", "bd": "bn", "np": "ne",
    # Middle East / West Asia
    "sa": "ar", "ae": "ar", "qa": "ar", "kw": "ar", "eg": "ar",
    "il": "he", "tr": "tr",
    # Europe
    "uk": "en", "ie": "en",
    "de": "de", "at": "de", "ch": "de",
    "fr": "fr", "be": "fr", "nl": "nl",
    "it": "it", "es": "es", "pt": "pt",
    "se": "sv", "dk": "da", "no": "no", "fi": "fi",
    "pl": "pl", "cz": "cs", "hu": "hu", "gr": "el",
    "ru": "ru", "ro": "ro",
    # Americas
    "us": "en", "ca": "en",
    "mx": "es", "ar": "es", "cl": "es", "co": "es", "pe": "es",
    "br": "pt",
    # Africa
    "za": "en", "ng": "en", "ke": "en", "eg": "ar",
    # Oceania
    "au": "en", "nz": "en",
}


def native_name(code):
    """返回语言代码的本地名称"""
    return LANG_MAP.get(code, code.upper())


def detect_input_lang(input_text=""):
    """
    审题机制：从输入的指令检测使用的是什么语言
    
    大叔亲授：只看输入的文字判断语言，不猜国籍。
    中国人也可能打阿拉伯语、日本人也可能打英文——只看字符，不猜身份。
    
    Args:
        input_text: 用户输入的指令文本
    
    Returns:
        ISO语言代码 ("zh", "en", "ja", "ko", "ar", "ru", ...)
    """
    if not input_text:
        return "zh"
    
    # Unicode块范围检测各大文字系统
    cjk = sum(1 for c in input_text if 0x4E00 <= ord(c) <= 0x9FFF or 0x3400 <= ord(c) <= 0x4DBF)
    kana = sum(1 for c in input_text if 0x3040 <= ord(c) <= 0x309F or 0x30A0 <= ord(c) <= 0x30FF or 0xFF66 <= ord(c) <= 0xFF9F)
    hangul = sum(1 for c in input_text if 0xAC00 <= ord(c) <= 0xD7AF or 0x1100 <= ord(c) <= 0x11FF)
    arabic = sum(1 for c in input_text if 0x0600 <= ord(c) <= 0x06FF or 0x0750 <= ord(c) <= 0x077F or 0x08A0 <= ord(c) <= 0x08FF or 0xFB50 <= ord(c) <= 0xFDFF or 0xFE70 <= ord(c) <= 0xFEFF)
    cyrillic = sum(1 for c in input_text if 0x0400 <= ord(c) <= 0x04FF or 0x0500 <= ord(c) <= 0x052F)
    thai = sum(1 for c in input_text if 0x0E00 <= ord(c) <= 0x0E7F)
    devanagari = sum(1 for c in input_text if 0x0900 <= ord(c) <= 0x097F)
    greek = sum(1 for c in input_text if 0x0370 <= ord(c) <= 0x03FF)
    hebrew = sum(1 for c in input_text if 0x0590 <= ord(c) <= 0x05FF)
    georgian = sum(1 for c in input_text if 0x10A0 <= ord(c) <= 0x10FF or 0x2D00 <= ord(c) <= 0x2D25)
    armenian = sum(1 for c in input_text if 0x0530 <= ord(c) <= 0x058F or 0xFB00 <= ord(c) <= 0xFB17)
    sinhala = sum(1 for c in input_text if 0x0D80 <= ord(c) <= 0x0DFF or 0x111E0 <= ord(c) <= 0x111FF)
    tibetan = sum(1 for c in input_text if 0x0F00 <= ord(c) <= 0x0FFF)
    myanmar = sum(1 for c in input_text if 0x1000 <= ord(c) <= 0x109F or 0xAA60 <= ord(c) <= 0xAA7F)
    khmer = sum(1 for c in input_text if 0x1780 <= ord(c) <= 0x17FF or 0x19E0 <= ord(c) <= 0x19FF)
    lao = sum(1 for c in input_text if 0x0E80 <= ord(c) <= 0x0EFF)
    mongolian = sum(1 for c in input_text if 0x1800 <= ord(c) <= 0x18AF)
    javanese = sum(1 for c in input_text if 0xA980 <= ord(c) <= 0xA9DF)
    thaana = sum(1 for c in input_text if 0x0780 <= ord(c) <= 0x07BF)
    cherokee = sum(1 for c in input_text if 0x13A0 <= ord(c) <= 0x13FF or 0xAB70 <= ord(c) <= 0xABBF)
    ethiopic = sum(1 for c in input_text if 0x1200 <= ord(c) <= 0x137F or 0x1380 <= ord(c) <= 0x139F)
    ascii_letters = sum(1 for c in input_text if c.isascii() and c.isalpha())
    
    scripts = [
        (kana, "ja"), (hangul, "ko"), (arabic, "ar"), (cyrillic, "ru"),
        (thai, "th"), (devanagari, "hi"), (greek, "el"), (hebrew, "he"),
        (georgian, "ka"), (armenian, "hy"), (sinhala, "si"),
        (tibetan, "bo"), (myanmar, "my"), (khmer, "km"), (lao, "lo"),
        (mongolian, "mn"), (javanese, "jv"), (thaana, "dv"),
        (cherokee, "chr"), (ethiopic, "am"), (cjk, "zh"),
    ]
    
    total = sum(s[0] for s in scripts) + ascii_letters
    if total == 0:
        return "zh"
    
    for count, lang in scripts:
        if count > total * 0.1:
            return lang
    
    if ascii_letters > total * 0.4:
        return "en"
    return "zh"


def match_market_lang(market_code):
    """
    质检机制：匹配目标市场的本地语言
    
    Args:
        market_code: 市场ISO代码（cn, us, jp, kr, th...）
    
    Returns:
        ISO语言代码
    """
    return MARKET_LANG.get(market_code.lower(), "en")


# ── 双语文本生成辅助函数 ──
# 用于模板中的T()/H()/P()调用

class BilingualText:
    """双语文本生成器，自动适配输入语言+市场语言"""
    
    def __init__(self, user_text_en="", user_text_zh="", 
                 input_lang="zh", dest_lang="zh"):
        self.input_lang = input_lang
        self.dest_lang = dest_lang
        self.input_native = native_name(input_lang)
        self.dest_native = native_name(dest_lang)
        
        # 输入语言的内容
        if input_lang == "zh":
            self.user_text = user_text_zh
        else:
            self.user_text = user_text_en
        
        # 市场语言的内容
        if dest_lang == "zh":
            self.dest_text = user_text_zh
        else:
            self.dest_text = user_text_en
    
    @property
    def bilingual(self):
        """返回双语格式的文本"""
        if self.input_lang == self.dest_lang:
            return f"{self.input_native}: {self.user_text}"
        return f"{self.input_native}: {self.user_text} / {self.dest_native}: {self.dest_text}"
    
    @property
    def header(self):
        """返回双语表头标签"""
        if self.input_lang == self.dest_lang:
            return self.input_native
        return f"{self.input_native} / {self.dest_native}"
    
    @property
    def item_label(self):
        """返回双语条目标签"""
        if self.input_lang == "zh":
            en_name = "Item"
            cn_name = "项目"
        else:
            en_name = "Item"
            cn_name = "项目"
        
        if self.input_lang == self.dest_lang:
            return f"{en_name} / {self.input_native if self.input_lang != 'zh' else '项目'}"
        
        if self.input_lang == "zh":
            return f"{en_name} / {cn_name}"
        return f"{en_name} / {self.input_native}"
