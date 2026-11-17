# -*- coding: utf-8 -*-
"""
Article-to-Video Skill - Default Configuration
All settings can be overridden via command-line arguments.
"""

import os

# ============================================================
# TTS Configuration
# ============================================================
TTS_CONFIG = {
    # Primary engine: edge-tts (free, high quality)
    "engine": "edge-tts",
    # Default voice (Chinese female, natural and warm)
    "voice": "zh-CN-XiaoxiaoNeural",
    # Available Chinese voices
    "voices": {
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",   # 女声, 亲切自然
        "xiaoyi":   "zh-CN-XiaoyiNeural",      # 女声, 温柔甜美
        "yunxi":    "zh-CN-YunxiNeural",        # 男声, 年轻活力
        "yunyang":  "zh-CN-YunyangNeural",      # 男声, 专业播音
        "yunjian":  "zh-CN-YunjianNeural",      # 男声, 体育解说
    },
    # English voices
    "voices_en": {
        "jenny":  "en-US-JennyNeural",
        "guy":    "en-US-GuyNeural",
        "aria":   "en-US-AriaNeural",
    },
    # Rate adjustment: -50% to +200%, or specific values like "+10%", "-5%"
    "rate": "+0%",
    # Pitch adjustment
    "pitch": "+0Hz",
    # Delay between TTS calls (seconds) - anti-throttle for edge-tts 429
    "delay_between_calls": 2.0,
    # Max retries on 429 rate limit error
    "max_retries": 3,
    # Fallback chain when primary engine fails
    "fallback_chain": ["edge-tts", "gtts", "pyttsx3"],
}

# ============================================================
# Voice Profiles — 一键预设组合 (voice + rate + pitch + volume + bgm)
# Usage: --profile professional
# ============================================================
VOICE_PROFILES = {
    "professional": {
        # 专业播音 — 适合商务报告、金融分析、政策解读
        "label": "专业播音",
        "voice": "zh-CN-YunyangNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "narration_volume": "-3dB",
        "bgm_style": "corporate",
    },
    "casual": {
        # 轻松聊天 — 适合博客文章、生活分享、随笔
        "label": "轻松聊天",
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+10%",
        "pitch": "+2Hz",
        "narration_volume": "-1dB",
        "bgm_style": "acoustic",
    },
    "energetic": {
        # 活力解说 — 适合科技资讯、产品发布、赛事回顾
        "label": "活力解说",
        "voice": "zh-CN-YunxiNeural",
        "rate": "+15%",
        "pitch": "+5Hz",
        "narration_volume": "+0dB",
        "bgm_style": "electronic",
    },
    "documentary": {
        # 纪录片风格 — 适合历史人文、深度报道、科普长文
        "label": "纪录片风格",
        "voice": "zh-CN-YunjianNeural",
        "rate": "-5%",
        "pitch": "-2Hz",
        "narration_volume": "-5dB",
        "bgm_style": "cinematic",
    },
    "warm": {
        # 温柔讲述 — 适合教育课程、儿童读物、情感故事
        "label": "温柔讲述",
        "voice": "zh-CN-XiaoyiNeural",
        "rate": "-5%",
        "pitch": "+0Hz",
        "narration_volume": "-2dB",
        "bgm_style": "soft",
    },
}

# ============================================================
# Video Configuration
# ============================================================
VIDEO_CONFIG = {
    # Output resolution presets
    "platforms": {
        "youtube":    {"width": 1920, "height": 1080, "fps": 30},
        "tiktok":     {"width": 1080, "height": 1920, "fps": 30},
        "xiaohongshu": {"width": 1080, "height": 1440, "fps": 30},
        "bilibili":   {"width": 1920, "height": 1080, "fps": 30},
        "square":     {"width": 1080, "height": 1080, "fps": 30},
    },
    # Default platform
    "default_platform": "youtube",
    # Default resolution (overridden by platform preset)
    "width": 1920,
    "height": 1080,
    "fps": 30,
    # Video encoding
    "video_codec": "libx264",
    "video_preset": "medium",       # ultrafast, fast, medium, slow, slower
    "video_crf": 23,               # 18 (high quality) to 28 (small file)
    "pixel_format": "yuv420p",
    # Audio encoding
    "audio_codec": "aac",
    "audio_bitrate": "192k",
    "audio_sample_rate": 44100,
}

# ============================================================
# Visual Effects Configuration
# ============================================================
EFFECTS_CONFIG = {
    # Ken Burns effect (slow zoom on static images)
    "ken_burns": True,
    "ken_burns_zoom_start": 1.0,
    "ken_burns_zoom_end": 1.15,     # Zoom to 115% over clip duration
    "ken_burns_pan": True,          # Also pan while zooming

    # Scene transitions
    "transition": "fade",           # fade, dissolve, slideleft, slideright, wipeup, circleopen
    "transition_duration": 0.5,     # Seconds

    # Subtitle burning
    "subtitle": True,
    "subtitle_font": "Microsoft YaHei",  # Font family name (not file path)
    "subtitle_font_size": 12,
    "subtitle_color": "&H00FFFFFF&",      # ASS hex: white (format: &H00BBGGRR&)
    "subtitle_border_color": "&H00000000&",  # ASS hex: black
    "subtitle_border_width": 2,
    "subtitle_position": "bottom",  # bottom, center, top

    # Background music
    "bgm": True,
    "bgm_volume": "-15dB",          # BGM attenuated relative to narration
    "narration_volume": "-3dB",
    "bgm_fade_in": 2.0,             # Seconds
    "bgm_fade_out": 3.0,            # Seconds
}

# ============================================================
# BGM Configuration — 背景音乐分类库
# assets/bgm/<style>/ 目录下存放对应风格的无版权音乐
# ============================================================
BGM_CONFIG = {
    # BGM 风格 → 对应目录名 (assets/bgm/<style>/)
    "styles": {
        "corporate":   {"dir": "corporate",   "label": "企业商务", "volume": "-18dB"},
        "acoustic":    {"dir": "acoustic",    "label": "轻音乐",   "volume": "-15dB"},
        "electronic":  {"dir": "electronic",  "label": "电子律动", "volume": "-20dB"},
        "cinematic":   {"dir": "cinematic",   "label": "电影感",   "volume": "-12dB"},
        "soft":        {"dir": "soft",        "label": "温柔舒缓", "volume": "-16dB"},
    },
    # 默认 BGM 风格 (当 content_type 未匹配时使用)
    "default_style": "corporate",
    # 是否自动根据内容类型选择 BGM
    "auto_select": True,
    # content_type → bgm_style 映射
    "type_bgm_map": {
        "business":     "corporate",
        "technology":   "electronic",
        "education":    "soft",
        "news":         "corporate",
        "lifestyle":    "acoustic",
        "finance":      "corporate",
        "science":      "cinematic",
        "default":      "corporate",
    },
}

# ============================================================
# Slide Template Configuration
# ============================================================
SLIDE_CONFIG = {
    # Template mode: "template" (HTML rendering) or "ai" (GenerateImage)
    "mode": "template",
    # Color themes
    "themes": {
        "default":  {"bg": "#1a1a2e", "accent": "#7c3aed", "text": "#ffffff"},
        "light":    {"bg": "#f8f9fa", "accent": "#7c3aed", "text": "#1a1a2e"},
        "dark":     {"bg": "#0f0f0f", "accent": "#a78bfa", "text": "#f8f9fa"},
        "warm":     {"bg": "#2d1810", "accent": "#f59e0b", "text": "#fef3c7"},
        "ocean":    {"bg": "#0c1e3a", "accent": "#06b6d4", "text": "#e0f2fe"},
    },
    "default_theme": "default",
    # Font families
    "font_title": "Microsoft YaHei, sans-serif",
    "font_body": "Microsoft YaHei, sans-serif",
    "font_mono": "Consolas, monospace",
}

# ============================================================
# AI Image Generation Configuration
# 用于 parse_doc.py 的 _generate_image_prompt 和 create_slides.py 的 AI 模式
# ============================================================
AI_IMAGE_CONFIG = {
    # 图片尺寸预设 (对应 GenerateImage 工具的 image_size 参数)
    "image_size": "landscape_16_9",  # 2560x1440, 适合 YouTube/B站
    # 默认风格前缀 (会根据 content_type 覆盖)
    "default_style": "modern, clean, professional, suitable for educational video",
    # 是否在 prompt 中包含 "No text in image" 指令
    "no_text": True,
    # 内容类型 → AI 图片风格映射
    # 每种类型定义: artistic_style (艺术风格), color_mood (色调氛围), composition (构图)
    "type_style_map": {
        "finance": {
            "artistic_style": "professional financial infographic style, sleek corporate aesthetic",
            "color_mood": "deep blue and gold tones, conveying trust and wealth",
            "composition": "clean data visualization layout, balanced composition",
        },
        "business": {
            "artistic_style": "modern corporate illustration, minimalist business aesthetic",
            "color_mood": "purple and white tones, professional and authoritative",
            "composition": "centered focal point with supporting elements",
        },
        "technology": {
            "artistic_style": "futuristic tech illustration, digital cyberpunk aesthetic",
            "color_mood": "dark background with neon cyan and purple accents",
            "composition": "dynamic diagonal composition, tech elements and circuit patterns",
        },
        "science": {
            "artistic_style": "scientific illustration style, detailed and precise",
            "color_mood": "deep blue and teal tones, conveying depth and discovery",
            "composition": "symmetrical layout with research elements and data",
        },
        "education": {
            "artistic_style": "warm educational illustration, friendly and approachable",
            "color_mood": "warm orange and soft blue tones, inviting and calm",
            "composition": "clear visual hierarchy with teaching elements",
        },
        "news": {
            "artistic_style": "editorial news illustration, clean and impactful",
            "color_mood": "white background with red and blue accent colors",
            "composition": "bold focal point with news-related imagery",
        },
        "lifestyle": {
            "artistic_style": "lifestyle photography style, natural and warm",
            "color_mood": "soft warm tones with natural lighting",
            "composition": "lifestyle scene with cozy atmosphere",
        },
        "default": {
            "artistic_style": "modern, clean, professional illustration",
            "color_mood": "balanced color palette, neutral tones",
            "composition": "centered composition with clear focal point",
        },
    },
}

# ============================================================
# Content Type Configuration — 内容类型自动检测与风格匹配
# parse_doc.py 使用 CONTENT_TYPE_KEYWORDS 检测文档类型
# create_slides.py / assemble_video.py 使用 CONTENT_TYPE_STYLES 应用对应视觉参数
# ============================================================

# 内容类型关键词表 (按优先级排序，越靠前越优先匹配)
CONTENT_TYPE_KEYWORDS = {
    "finance": [
        # 金融/投资
        "金融", "投资", "证券", "股票", "基金", "债券", "银行", "利率",
        "收益", "风险", "资产", "负债", "估值", "市盈率", "财报",
        "invest", "finance", "stock", "bond", "portfolio", "revenue",
        "profit", "asset", "liability", "valuation", "IPO",
    ],
    "business": [
        # 商业/管理
        "企业", "管理", "战略", "市场", "营销", "品牌", "运营",
        "供应链", "客户", "商业模式", "竞争", "并购",
        "business", "strategy", "marketing", "brand", "operation",
        "supply chain", "customer", "competitive",
    ],
    "technology": [
        # 科技/IT
        "技术", "软件", "硬件", "算法", "编程", "代码", "API",
        "人工智能", "AI", "机器学习", "大数据", "云计算", "区块链",
        "架构", "数据库", "服务器", "开源", "框架",
        "technology", "software", "algorithm", "programming",
        "artificial intelligence", "machine learning", "cloud", "blockchain",
    ],
    "science": [
        # 科学/研究
        "研究", "实验", "理论", "假设", "数据", "分析", "结论",
        "物理", "化学", "生物", "医学", "气候", "宇宙",
        "research", "experiment", "theory", "hypothesis", "analysis",
        "physics", "chemistry", "biology", "medical",
    ],
    "education": [
        # 教育/教程
        "教程", "课程", "学习", "教学", "知识", "入门", "进阶",
        "练习", "示例", "步骤", "讲解", "重点", "考点",
        "tutorial", "course", "learn", "teach", "lesson",
        "example", "step by step", "guide",
    ],
    "news": [
        # 新闻/资讯
        "新闻", "报道", "记者", "据悉", "消息", "宣布",
        "今日", "近期", "最新", "突发", "独家",
        "news", "report", "according to", "announced", "breaking",
    ],
    "lifestyle": [
        # 生活/随笔
        "生活", "旅行", "美食", "健身", "心情", "感受", "随笔",
        "日记", "推荐", "体验", "攻略",
        "lifestyle", "travel", "food", "fitness", "experience",
    ],
}

# 内容类型 → 视觉风格预设
# 每种类型定义: 主题配色、字体风格、动画参数、转场风格
CONTENT_TYPE_STYLES = {
    "finance": {
        "label": "金融财经",
        "theme": "ocean",              # 深蓝底，专业感
        "theme_override": {            # 覆盖默认主题配色
            "bg": "#0c1e3a",
            "accent": "#06b6d4",
            "text": "#e0f2fe",
            "accent_secondary": "#f59e0b",  # 金色辅助色
        },
        "font_title": "Georgia, 'Microsoft YaHei', serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "slow",     # slow: 1.0→1.08, normal: 1.0→1.15, fast: 1.0→1.25
        "transition": "fade",
        "transition_duration": 0.8,
        "subtitle_position": "bottom",
    },
    "business": {
        "label": "商业管理",
        "theme": "default",
        "theme_override": {
            "bg": "#1a1a2e",
            "accent": "#7c3aed",
            "text": "#ffffff",
            "accent_secondary": "#06b6d4",
        },
        "font_title": "'Microsoft YaHei', sans-serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "normal",
        "transition": "fade",
        "transition_duration": 0.5,
        "subtitle_position": "bottom",
    },
    "technology": {
        "label": "科技互联网",
        "theme": "dark",
        "theme_override": {
            "bg": "#0f0f0f",
            "accent": "#22d3ee",
            "text": "#f8f9fa",
            "accent_secondary": "#a78bfa",
        },
        "font_title": "'Consolas', 'Microsoft YaHei', monospace",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "fast",
        "transition": "slideleft",
        "transition_duration": 0.3,
        "subtitle_position": "bottom",
    },
    "science": {
        "label": "科学研究",
        "theme": "ocean",
        "theme_override": {
            "bg": "#0c1e3a",
            "accent": "#06b6d4",
            "text": "#e0f2fe",
            "accent_secondary": "#a78bfa",
        },
        "font_title": "Georgia, 'Microsoft YaHei', serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "slow",
        "transition": "dissolve",
        "transition_duration": 1.0,
        "subtitle_position": "center",
    },
    "education": {
        "label": "教育教程",
        "theme": "warm",
        "theme_override": {
            "bg": "#2d1810",
            "accent": "#f59e0b",
            "text": "#fef3c7",
            "accent_secondary": "#06b6d4",
        },
        "font_title": "'Microsoft YaHei', sans-serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "normal",
        "transition": "fade",
        "transition_duration": 0.5,
        "subtitle_position": "bottom",
    },
    "news": {
        "label": "新闻资讯",
        "theme": "light",
        "theme_override": {
            "bg": "#f8f9fa",
            "accent": "#dc2626",
            "text": "#1a1a2e",
            "accent_secondary": "#1e40af",
        },
        "font_title": "Georgia, 'Microsoft YaHei', serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "fast",
        "transition": "fade",
        "transition_duration": 0.3,
        "subtitle_position": "bottom",
    },
    "lifestyle": {
        "label": "生活随笔",
        "theme": "warm",
        "theme_override": {
            "bg": "#2d1810",
            "accent": "#f59e0b",
            "text": "#fef3c7",
            "accent_secondary": "#06b6d4",
        },
        "font_title": "'Microsoft YaHei', sans-serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "normal",
        "transition": "dissolve",
        "transition_duration": 0.8,
        "subtitle_position": "bottom",
    },
    "default": {
        "label": "通用",
        "theme": "default",
        "theme_override": None,   # 使用默认主题
        "font_title": "'Microsoft YaHei', sans-serif",
        "font_body": "'Microsoft YaHei', sans-serif",
        "ken_burns_speed": "normal",
        "transition": "fade",
        "transition_duration": 0.5,
        "subtitle_position": "bottom",
    },
}

# Ken Burns 速度 → zoom/pan 参数映射
# pan_range: 最大平移距离（源像素），越大移动越明显
KEN_BURNS_SPEED_MAP = {
    "slow":   {"zoom_start": 1.0, "zoom_end": 1.08, "pan": True, "pan_range": 60},
    "normal": {"zoom_start": 1.0, "zoom_end": 1.15, "pan": True, "pan_range": 80},
    "fast":   {"zoom_start": 1.0, "zoom_end": 1.25, "pan": False, "pan_range": 100},
}

# ============================================================
# Document Parsing Configuration
# ============================================================
PARSE_CONFIG = {
    # Max chars per scene (controls scene splitting)
    "max_chars_per_scene": 500,
    # Min chars per scene (merge very short scenes)
    "min_chars_per_scene": 50,
    # Chinese reading speed (chars per second)
    "cn_chars_per_sec": 4.5,
    # English reading speed (words per second)
    "en_words_per_sec": 2.8,
    # Skip empty headings
    "skip_empty_headings": True,
    # Extract images from PDF
    "extract_pdf_images": True,
    # Convert tables to text summary
    "table_to_text": True,
}

# ============================================================
# Paths Configuration
# ============================================================

# Skill root: dynamically computed from this file's location
# config.py is in <skill_root>/scripts/config.py
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _detect_ffmpeg():
    """Detect best available FFmpeg binary.
    Prefers imageio-ffmpeg (full codec support) over system FFmpeg.
    """
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def _detect_ffprobe():
    """Detect ffprobe path (same dir as ffmpeg, or system)."""
    ffmpeg_path = _detect_ffmpeg()
    if ffmpeg_path and ffmpeg_path != "ffmpeg":
        base = os.path.dirname(ffmpeg_path)
        probe = os.path.join(base, "ffprobe.exe")
        if os.path.exists(probe):
            return probe
    return "ffprobe"


PATHS_CONFIG = {
    # Skill root (auto-detected from this file's location)
    "skill_root": _SKILL_ROOT,
    # Temp working directory (use ASCII-only paths for FFmpeg compatibility)
    "temp_dir": os.path.join(_SKILL_ROOT, "tmp"),
    # Assets directory (BGM, fonts, etc.)
    "assets_dir": os.path.join(_SKILL_ROOT, "assets"),
    # FFmpeg binary (auto-detect: prefers imageio-ffmpeg bundled binary)
    "ffmpeg": _detect_ffmpeg(),
    "ffprobe": _detect_ffprobe(),
}

# ============================================================
# Caching & Resume Configuration
# ============================================================
CACHE_CONFIG = {
    # Enable caching (skip regeneration if text hash matches)
    "enabled": True,
    # Cache directory (auto-computed from skill root)
    "cache_dir": os.path.join(_SKILL_ROOT, "tmp", ".cache"),
    # Max cache size in MB (0 = unlimited)
    "max_size_mb": 1024,
    # Enable breakpoint resume
    "resume": True,
    # Progress file
    "progress_file": "progress.json",
}

# ============================================================
# Concurrency Configuration
# ============================================================
CONCURRENCY_CONFIG = {
    # Number of parallel image generation tasks
    "image_workers": 2,
    # TTS is always serial (edge-tts rate limit)
    "tts_workers": 1,
    # Video assembly is always serial
    "video_workers": 1,
}
