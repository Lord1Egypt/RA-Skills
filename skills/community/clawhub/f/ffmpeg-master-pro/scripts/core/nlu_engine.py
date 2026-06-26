"""
自然语言理解引擎
解析用户输入，识别意图和参数
"""

import re
from typing import Dict, List, Optional
from enum import Enum


class IntentType(Enum):
    """意图类型枚举"""

    TRANSCODE = "transcode"  # 转码
    COMPRESS = "compress"  # 压缩
    CROP = "crop"  # 剪辑
    MERGE = "merge"  # 合并
    SUBTITLE_EXTRACT = "subtitle_extract"  # 提取字幕
    SUBTITLE_EMBED = "subtitle_embed"  # 嵌入字幕
    SUBTITLE_BURN = "subtitle_burn"  # 烧录字幕
    SUBTITLE_CONVERT = "subtitle_convert"  # 字幕格式转换
    WATERMARK = "watermark"  # 添加水印
    ROTATE = "rotate"  # 旋转
    RESIZE = "resize"  # 调整大小
    FILTER = "filter"  # 应用滤镜
    BATCH = "batch"  # 批量处理
    EXTRACT_AUDIO = "extract_audio"  # 提取音频
    EXTRACT_FRAMES = "extract_frames"  # 提取帧
    CREATE_GIF = "create_gif"  # 创建 GIF
    SPEED_CHANGE = "speed_change"  # 变速
    VOLUME_CHANGE = "volume_change"  # 音量调整
    UNKNOWN = "unknown"  # 未知意图


class NLUEngine:
    """自然语言理解引擎"""

    def __init__(self):
        """初始化 NLU 引擎"""
        self.intent_patterns = self._init_intent_patterns()
        self.param_patterns = self._init_param_patterns()

    def _init_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """初始化意图识别模式"""
        return {
            IntentType.TRANSCODE: [
                r"转码|格式转换|转换.*格式|convert|transcode",
                r"改为.*格式|变成.*格式",
            ],
            IntentType.COMPRESS: [
                r"压缩|减小文件|缩小|compress",
                r"\d+MB|\d+GB.*以内|目标大小|限制大小",
                r".*到\s*\d+MB|.*到\s*\d+GB",
            ],
            IntentType.CROP: [
                r"剪辑|裁剪|crop|cut",
                r"从.*到.*|截取.*片段",
                r"\d+:\d+.*\d+:\d+|提取\d+秒",
            ],
            IntentType.MERGE: [r"合并|拼接|连接|merge|concat", r"多个视频|合成.*个"],
            IntentType.SUBTITLE_EXTRACT: [
                r"提取字幕|导出字幕|subtitle.*extract",
                r"分离字幕|字幕提取",
                r"中文字幕|英文字幕|字幕.*中文|字幕.*英文",
                r"提取.*字幕|导出.*字幕|字幕.*导出|字幕.*提取",
            ],
            IntentType.SUBTITLE_EMBED: [
                r"嵌入字幕|添加字幕|软字幕|subtitle.*embed",
                r"封装字幕|内嵌字幕",
            ],
            IntentType.SUBTITLE_BURN: [r"烧录字幕|硬字幕|subtitle.*burn", r"字幕.*画面|字幕.*视频"],
            IntentType.SUBTITLE_CONVERT: [
                r"字幕.*转换|convert.*subtitle",
                r"srt.*ass|ass.*srt|字幕格式",
            ],
            IntentType.WATERMARK: [r"水印|watermark|logo", r"添加.*图|叠加.*图片"],
            IntentType.ROTATE: [r"旋转|翻转|rotate|flip", r"\d+度|顺时针|逆时针"],
            IntentType.RESIZE: [
                r"调整.*大小|resize|scale",
                r"分辨率|1920x1080|1080p|720p|480p",
                r"宽度|高度",
            ],
            IntentType.FILTER: [
                r"滤镜|filter|效果|特效",
                r"模糊|锐化|亮度|对比度|饱和度",
                r"黑白|灰度|复古|模糊",
            ],
            IntentType.BATCH: [r"批量|batch|所有.*|多个.*", r"整个目录|全部视频|所有文件"],
            IntentType.EXTRACT_AUDIO: [r"提取音频|分离音频|extract.*audio", r"音频.*提取|只取音频"],
            IntentType.EXTRACT_FRAMES: [r"提取帧|截图|frame.*extract", r"每秒.*帧|生成图片"],
            IntentType.CREATE_GIF: [r"gif|动图|create.*gif", r"生成.*gif"],
            IntentType.SPEED_CHANGE: [r"变速|加速|减速|speed", r"\d+倍速|快进|慢放"],
            IntentType.VOLUME_CHANGE: [r"音量|volume|声音.*大|声音.*小", r"音量.*\d+|%.*音量"],
        }

    def _init_param_patterns(self) -> Dict[str, str]:
        """初始化参数提取模式"""
        return {
            "target_size": r"(\d+(?:\.\d+)?)\s*(MB|GB|mb|gb)",
            "resolution": r"(1920x1080|1280x720|854x480|3840x2160|1080p|720p|480p|4K)",
            "time_range": r"(\d{1,2}):(\d{2})[:：](\d{2})\s*[-~到]\s*(\d{1,2}):(\d{2})[:：](\d{2})",
            "duration": r"(\d+)\s*秒|(\d+):(\d+)",
            "subtitle_lang": r"(中文|英文|英文|en|cn|zh)",
            "watermark_position": r"(左上|右上|左下|右下|center|中间|top.*left|top.*right|bottom.*left|bottom.*right)",
            "rotation": r"(\d+)\s*度|90度|180度|270度",
            "scale": r"(\d+)%|缩放.*(\d+)",
            "speed": r"(\d+(?:\.\d+)?)\s*倍速|(\d+(?:\.\d+)?)x",
            "volume": r"音量.*?(\d+)%|volume.*?(\d+)",
            "fps": r"(\d+)\s*fps|帧率.*?(\d+)",
        }

    def parse(self, user_input: str) -> Dict:
        """
        解析用户输入

        Args:
            user_input: 用户输入的自然语言文本

        Returns:
            包含意图和参数的字典
        """
        # 识别意图
        intent = self._recognize_intent(user_input)

        # 提取参数
        params = self._extract_params(user_input, intent)

        # 提取文件路径
        files = self._extract_files(user_input)

        # 提取滤镜信息
        filters = self._extract_filters(user_input)

        return {
            "intent": intent,
            "params": params,
            "files": files,
            "filters": filters,
            "raw_input": user_input,
        }

    def _recognize_intent(self, text: str) -> IntentType:
        """识别用户意图"""
        text_lower = text.lower()

        # 计算每个意图的匹配分数
        scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches
            if score > 0:
                scores[intent] = score

        # 返回分数最高的意图
        if scores:
            return max(scores, key=lambda intent: scores[intent])

        return IntentType.UNKNOWN

    def _extract_params(self, text: str, intent: IntentType) -> Dict:
        """提取参数"""
        params = {}

        # 使用参数提取器
        extractors = {
            "target_size": self._extract_target_size,
            "resolution": self._extract_resolution,
            "time_range": self._extract_time_range,
            "subtitle_lang": self._extract_subtitle_lang,
            "watermark_position": self._extract_watermark_position,
            "rotation": self._extract_rotation,
            "scale": self._extract_scale,
            "speed": self._extract_speed,
            "volume": self._extract_volume,
            "fps": self._extract_fps,
        }

        # 执行所有提取器
        for param_name, extractor in extractors.items():
            extracted = extractor(text)
            if extracted is not None:
                params.update(extracted)

        # 根据意图提取特定参数
        intent_params = self._extract_intent_specific_params(text, intent)
        params.update(intent_params)

        return params

    def _extract_target_size(self, text: str) -> Optional[Dict]:
        """提取目标大小"""
        match = re.search(self.param_patterns["target_size"], text, re.IGNORECASE)
        if not match:
            return None

        size_value = float(match.group(1))
        size_unit = match.group(2).upper()
        return {"target_size_mb": size_value if size_unit == "MB" else size_value * 1024}

    def _extract_resolution(self, text: str) -> Optional[Dict]:
        """提取分辨率"""
        match = re.search(self.param_patterns["resolution"], text, re.IGNORECASE)
        if not match:
            return None

        res = match.group(1).lower()
        res_map = {
            "1920x1080": (1920, 1080),
            "1080p": (1920, 1080),
            "1280x720": (1280, 720),
            "720p": (1280, 720),
            "854x480": (854, 480),
            "480p": (854, 480),
            "3840x2160": (3840, 2160),
            "4k": (3840, 2160),
        }

        if res in res_map:
            return {"resolution": res_map[res]}
        return None

    def _extract_time_range(self, text: str) -> Optional[Dict]:
        """提取时间范围"""
        match = re.search(self.param_patterns["time_range"], text)
        if not match:
            return None

        start_h, start_m, start_s, end_h, end_m, end_s = match.groups()
        return {
            "start_time": f"{start_h}:{start_m}:{start_s}",
            "end_time": f"{end_h}:{end_m}:{end_s}",
        }

    def _extract_subtitle_lang(self, text: str) -> Optional[Dict]:
        """提取字幕语言"""
        match = re.search(self.param_patterns["subtitle_lang"], text, re.IGNORECASE)
        if not match:
            return None

        lang = match.group(1).lower()
        lang_map = {
            "中文": "chi",
            "cn": "chi",
            "zh": "chi",
            "英文": "eng",
            "en": "eng",
            "english": "eng",
        }

        return {"subtitle_lang": lang_map.get(lang, lang)}

    def _extract_watermark_position(self, text: str) -> Optional[Dict]:
        """提取水印位置"""
        match = re.search(self.param_patterns["watermark_position"], text, re.IGNORECASE)
        if match:
            return {"watermark_position": match.group(1)}
        return None

    def _extract_rotation(self, text: str) -> Optional[Dict]:
        """提取旋转角度"""
        match = re.search(self.param_patterns["rotation"], text, re.IGNORECASE)
        if match:
            return {"rotation_angle": int(match.group(1))}
        return None

    def _extract_scale(self, text: str) -> Optional[Dict]:
        """提取缩放比例"""
        match = re.search(self.param_patterns["scale"], text, re.IGNORECASE)
        if match:
            return {"scale_percent": int(match.group(1))}
        return None

    def _extract_speed(self, text: str) -> Optional[Dict]:
        """提取速度"""
        match = re.search(self.param_patterns["speed"], text, re.IGNORECASE)
        if match:
            return {"speed_factor": float(match.group(1))}
        return None

    def _extract_volume(self, text: str) -> Optional[Dict]:
        """提取音量"""
        match = re.search(self.param_patterns["volume"], text, re.IGNORECASE)
        if match:
            return {"volume_percent": int(match.group(1))}
        return None

    def _extract_fps(self, text: str) -> Optional[Dict]:
        """提取帧率"""
        match = re.search(self.param_patterns["fps"], text, re.IGNORECASE)
        if match:
            return {"fps": int(match.group(1))}
        return None

    def _extract_intent_specific_params(self, text: str, intent: IntentType) -> Dict:
        """根据意图提取特定参数"""
        params = {}

        if intent == IntentType.COMPRESS:
            if "保持质量" in text or "高质量" in text:
                params["preserve_quality"] = True
            if "保持分辨率" in text:
                params["preserve_resolution"] = True

        elif intent == IntentType.SUBTITLE_BURN:
            if "字体" in text:
                font_match = re.search(r"字体[:：]\s*(\S+)", text)
                if font_match:
                    params["font"] = font_match.group(1)

        return params

    def _extract_files(self, text: str) -> List[str]:
        """提取文件路径"""
        # 匹配常见视频格式
        video_pattern = r"[\w\-\.:/\\]+\.(?:mp4|mkv|avi|mov|flv|wmv|webm|m4v|mpg|mpeg)"
        files = re.findall(video_pattern, text, re.IGNORECASE)
        return files

    def _extract_filters(self, text: str) -> List[Dict]:
        """提取滤镜信息"""
        filters = []

        # 模糊
        if "模糊" in text or "blur" in text.lower():
            filters.append({"type": "blur", "params": {}})

        # 锐化
        if "锐化" in text or "sharpen" in text.lower():
            filters.append({"type": "sharpen", "params": {}})

        # 亮度
        brightness_match = re.search(r"亮度.*?([+-]?\d+)%", text)
        if brightness_match:
            value = int(brightness_match.group(1)) / 100
            filters.append({"type": "brightness", "params": {"value": value}})

        # 对比度
        contrast_match = re.search(r"对比度.*?([+-]?\d+)%", text)
        if contrast_match:
            value = int(contrast_match.group(1)) / 100
            filters.append({"type": "contrast", "params": {"value": value}})

        # 饱和度
        saturation_match = re.search(r"饱和度.*?([+-]?\d+)%", text)
        if saturation_match:
            value = int(saturation_match.group(1)) / 100
            filters.append({"type": "saturation", "params": {"value": value}})

        # 黑白/灰度
        if "黑白" in text or "灰度" in text or "grayscale" in text.lower():
            filters.append({"type": "grayscale", "params": {}})

        # 怀旧/复古
        if "怀旧" in text or "复古" in text or "vintage" in text.lower():
            filters.append({"type": "vintage", "params": {}})

        return filters


# 使用示例
if __name__ == "__main__":
    engine = NLUEngine()

    # 测试案例
    test_cases = [
        "将视频压缩到 500MB",
        "提取视频中的中英文字幕",
        "在视频右下角添加水印",
        "把视频从 0:10:00 剪辑到 0:15:30",
        "批量转换所有 MP4 文件为 MKV",
        "视频旋转 90 度，亮度增加 20%",
    ]

    for test in test_cases:
        print(f"\n输入: {test}")
        result = engine.parse(test)
        print(f"意图: {result['intent'].value}")
        print(f"参数: {result['params']}")
        print(f"文件: {result['files']}")
        print(f"滤镜: {result['filters']}")
