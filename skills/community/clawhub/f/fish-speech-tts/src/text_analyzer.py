"""
台词分析引擎 — 情绪/节奏/重音智能分析
基于 NLP + 规则系统，为 Fish Speech TTS 生成控制参数
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class EmotionTag:
    """情绪标签"""
    emotion: str  # happy, sad, angry, surprised, neutral, tender, sarcastic
    intensity: float  # 0.0 ~ 1.0
    confidence: float  # 0.0 ~ 1.0


@dataclass
class RhythmTag:
    """节奏标签"""
    speed: str  # slow, normal, fast
    pause_after: float  # 停顿秒数 (0.0 ~ 2.0)
    emphasis_words: List[str] = field(default_factory=list)  # 重音词


@dataclass
class SegmentAnalysis:
    """段落分析结果"""
    text: str
    emotion: EmotionTag
    rhythm: RhythmTag
    voice_params: Dict  # 传递给 Fish Speech 的参数
    start_pos: int
    end_pos: int


class TextAnalyzer:
    """
    台词分析器
    
    功能：
    1. 情绪识别（基于关键词/标点/语境）
    2. 节奏控制（基于句长/标点/情感强度）
    3. 重音标记（基于语义重要性）
    4. 停顿规划（基于语法结构）
    """
    
    # 情绪关键词库
    EMOTION_KEYWORDS = {
        "happy": ["哈哈", "太好了", "真棒", "开心", "高兴", "兴奋", "太好了", "万岁", "耶"],
        "sad": ["呜呜", "难过", "伤心", "可惜", "遗憾", "对不起", "抱歉", "难过"],
        "angry": ["混蛋", "气死", "烦死", "滚", "闭嘴", "该死", "妈的", "去死"],
        "surprised": ["什么", "怎么可能", "天哪", "哇", "不会吧", "真的吗", "居然"],
        "tender": ["亲爱的", "宝贝", "我爱你", "想你", "在乎", "温柔", "心疼"],
        "sarcastic": ["呵呵", "是啊", "真了不起", "你可真行", "了不起啊"],
        "fearful": ["害怕", "恐惧", "不要", "求你", "救命", "危险"],
        "neutral": []
    }
    
    # 标点情绪权重
    PUNCTUATION_EMOTION = {
        "!": {"emotion": "strong", "intensity_boost": 0.3},
        "！": {"emotion": "strong", "intensity_boost": 0.3},
        "?": {"emotion": "questioning", "intensity_boost": 0.1},
        "？": {"emotion": "questioning", "intensity_boost": 0.1},
        "...": {"emotion": "hesitation", "intensity_boost": 0.0},
        "……": {"emotion": "hesitation", "intensity_boost": 0.0},
        "~": {"emotion": "playful", "intensity_boost": 0.2},
        "～": {"emotion": "playful", "intensity_boost": 0.2},
    }
    
    # 重音词性（简化版，实际需要分词）
    EMPHASIS_PATTERNS = [
        r"最\w+",  # 最+形容词
        r"非常\w+",  # 非常+形容词
        r"超级\w+",  # 超级+形容词
        r"真的\w+",  # 真的+动词/形容词
        r"绝对\w+",  # 绝对+动词
    ]
    
    def __init__(self):
        self.emotion_weights = {}
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> SegmentAnalysis:
        """
        分析单段台词
        
        Args:
            text: 台词文本
            context: 上下文信息（角色、场景等）
        
        Returns:
            SegmentAnalysis: 完整分析结果
        """
        # 1. 情绪识别
        emotion = self._detect_emotion(text, context)
        
        # 2. 节奏控制
        rhythm = self._analyze_rhythm(text, emotion)
        
        # 3. 生成 Fish Speech 参数
        voice_params = self._generate_voice_params(emotion, rhythm)
        
        return SegmentAnalysis(
            text=text,
            emotion=emotion,
            rhythm=rhythm,
            voice_params=voice_params,
            start_pos=0,
            end_pos=len(text)
        )
    
    def _detect_emotion(self, text: str, context: Optional[Dict] = None) -> EmotionTag:
        """检测情绪"""
        scores = {}
        
        # 0. 检测夸张/讽刺模式
        exaggeration_patterns = [
            r"能掀翻.*", r"能.*整栋", r"能.*整个",
            r"简直.*", r"简直要.*", r"快要.*",
            r"夸张.*", r"太夸张.*", r"也太.*了",
            r"真的假的", r"不会吧",
        ]
        for pattern in exaggeration_patterns:
            if re.search(pattern, text):
                scores["sarcastic"] = scores.get("sarcastic", 0) + 0.6
        
        # 1. 关键词匹配
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw in text:
                    score += 1
            if score > 0:
                scores[emotion] = score
        
        # 2. 标点符号影响
        exclamation_count = text.count("!") + text.count("！")
        if exclamation_count > 0:
            # 多个感叹号 = 强烈情绪
            if "sarcastic" in scores:
                scores["sarcastic"] += exclamation_count * 0.2
            elif scores:
                # 增强最高分情绪
                max_emotion = max(scores, key=scores.get)
                scores[max_emotion] = scores.get(max_emotion, 0) + exclamation_count * 0.15
        
        question_count = text.count("?") + text.count("？")
        if question_count > 0:
            scores["surprised"] = scores.get("surprised", 0) + question_count * 0.2
        
        # 3. 选择最高分情绪
        if scores and max(scores.values()) > 0:
            detected_emotion = max(scores, key=scores.get)
            intensity = min(scores[detected_emotion] / 3.0, 1.0)
        else:
            detected_emotion = "neutral"
            intensity = 0.3
        
        # 4. 上下文影响（如果有）
        if context and "emotion_hint" in context:
            detected_emotion = context["emotion_hint"]
            intensity = 0.8
        
        return EmotionTag(
            emotion=detected_emotion,
            intensity=intensity,
            confidence=0.7
        )
    
    def _analyze_rhythm(self, text: str, emotion: EmotionTag) -> RhythmTag:
        """分析节奏"""
        # 1. 基于句长判断语速
        char_count = len(text.replace(" ", "").replace("\n", ""))
        
        if emotion.emotion in ["angry", "surprised", "happy"]:
            speed = "fast"
        elif emotion.emotion in ["sad", "tender"]:
            speed = "slow"
        else:
            if char_count < 10:
                speed = "fast"
            elif char_count > 30:
                speed = "slow"
            else:
                speed = "normal"
        
        # 2. 计算停顿
        # 句末停顿
        if text.endswith(("!", "！", "?", "？")):
            pause_after = 0.8
        elif text.endswith(("。", ".", "~", "～")):
            pause_after = 0.5
        else:
            pause_after = 0.3
        
        # 3. 重音词提取
        emphasis_words = []
        for pattern in self.EMPHASIS_PATTERNS:
            matches = re.findall(pattern, text)
            emphasis_words.extend(matches)
        
        # 4. 情绪强度影响停顿
        if emotion.intensity > 0.7:
            pause_after *= 1.2  # 强烈情绪后停顿更长
        
        return RhythmTag(
            speed=speed,
            pause_after=pause_after,
            emphasis_words=emphasis_words
        )
    
    def _generate_voice_params(self, emotion: EmotionTag, rhythm: RhythmTag) -> Dict:
        """生成 Fish Speech 参数"""
        params = {
            "temperature": 0.7,
            "top_p": 0.8,
            "repetition_penalty": 1.1,
        }
        
        # 情绪 → 参数映射
        emotion_map = {
            "happy": {"temperature": 0.8, "top_p": 0.85},
            "sad": {"temperature": 0.6, "top_p": 0.75},
            "angry": {"temperature": 0.85, "top_p": 0.9, "repetition_penalty": 1.2},
            "surprised": {"temperature": 0.85, "top_p": 0.9},
            "tender": {"temperature": 0.65, "top_p": 0.7},
            "sarcastic": {"temperature": 0.75, "top_p": 0.8},
            "fearful": {"temperature": 0.7, "top_p": 0.75},
            "neutral": {"temperature": 0.7, "top_p": 0.8},
        }
        
        if emotion.emotion in emotion_map:
            params.update(emotion_map[emotion.emotion])
        
        # 情绪强度调整
        intensity_factor = emotion.intensity
        params["temperature"] = params["temperature"] * (0.8 + 0.4 * intensity_factor)
        params["temperature"] = max(0.1, min(1.0, params["temperature"]))
        
        # 语速 → chunk_length 映射（间接控制）
        # Fish Speech 没有直接的语速参数，通过 chunk_length 影响
        if rhythm.speed == "fast":
            params["chunk_length"] = 300  # 更长的 chunk 让模型"更流畅"
        elif rhythm.speed == "slow":
            params["chunk_length"] = 150  # 更短的 chunk 让模型"更谨慎"
        else:
            params["chunk_length"] = 200
        
        return params
    
    def split_into_segments(self, text: str, max_length: int = 100) -> List[str]:
        """
        将长文本分割为适合合成的段落
        
        规则：
        1. 按句子分割（句号、感叹号、问号）
        2. 每段不超过 max_length
        3. 保持语义完整性
        """
        # 1. 按句子分割
        sentences = re.split(r'([。！？!?~～]+)', text)
        
        # 2. 重新组合（标点附在前一句）
        combined = []
        current = ""
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
            current += sentence
            if len(current) >= max_length:
                combined.append(current.strip())
                current = ""
        if current:
            combined.append(current.strip())
        
        return combined if combined else [text]


# 便捷函数
def analyze_line(text: str, context: Optional[Dict] = None) -> SegmentAnalysis:
    """快速分析单行台词"""
    analyzer = TextAnalyzer()
    return analyzer.analyze(text, context)


if __name__ == "__main__":
    # 测试
    test_texts = [
        "顾栖上台缺了这件首饰，狂热粉丝能掀翻整栋场馆！",
        "哈哈，你真是太搞笑了！",
        "对不起，我真的很难过……",
        "什么？怎么可能！",
        "亲爱的，我想你了~"
    ]
    
    analyzer = TextAnalyzer()
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\n文本: {text}")
        print(f"  情绪: {result.emotion.emotion} (强度: {result.emotion.intensity:.2f})")
        print(f"  节奏: {result.rhythm.speed}, 停顿: {result.rhythm.pause_after:.1f}s")
        print(f"  参数: {result.voice_params}")
