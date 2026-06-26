#!/usr/bin/env python3
"""
AI Annotator - AI 标注器

使用 LLM 进行多维度标注，支持规则预标注和降级处理。
"""

import json
import os
import re
import time
from typing import Dict

from rich.console import Console

console = Console()


class FeatureExtractor:
    """文本特征提取器"""

    EMOTION_KEYWORDS = {
        "紧张": ["危险", "警惕", "杀气", "围攻", "生死", "紧迫", "危机", "窒息"],
        "轻松": ["微笑", "调侃", "悠闲", "放松", "愉快", "笑意", "慵懒"],
        "悲伤": ["泪水", "悲痛", "哀伤", "哭泣", "绝望", "哽咽", "心酸"],
        "热血": ["怒吼", "爆发", "战意", "激昂", "不屈", "沸腾", "豪迈"],
        "温馨": ["温暖", "柔和", "关怀", "拥抱", "甜蜜", "温情", "暖意"],
        "愤怒": ["怒吼", "愤怒", "咆哮", "愤恨", "怒火", "瞪视"],
        "恐惧": ["惊恐", "害怕", "颤抖", "畏惧", "恐慌", "毛骨悚然"],
        "中性": ["平静", "淡淡", "默默", "静静"],
    }

    SCENE_KEYWORDS = {
        "打斗": ["拳", "脚", "剑", "法术", "攻击", "防御", "招式", "灵力", "轰", "劈"],
        "修炼": ["灵气", "经脉", "丹田", "突破", "闭关", "运功", "打坐", "炼化"],
        "对话": ["说道", "问道", "回答", "沉默", "冷笑", "开口", "声音"],
        "探险": ["遗迹", "秘境", "洞穴", "探索", "发现", "入口", "机关"],
        "拍卖": ["拍卖", "竞价", "灵石", "宝物", "出价", "竞拍", "加价"],
        "会议": ["会议", "商议", "讨论", "决定", "计划", "安排"],
        "日常": ["吃饭", "休息", "睡觉", "散步", "闲聊", "日常"],
        "过渡": ["随后", "接着", "然后", "之后", "转眼"],
    }

    ACTION_VERBS = ["冲", "闪", "劈", "刺", "躲", "跃", "飞", "逃", "攻", "防"]
    DESCRIPTION_WORDS = ["缓缓", "慢慢", "静静", "仔细", "认真", "细细", "慢慢"]

    POV_PRONOUNS = {
        "我": "first_person",
        "我们": "first_person",
        "他": "third_person",
        "她": "third_person",
        "他们": "third_person",
        "她们": "third_person",
    }

    def extract_features(self, text: str) -> Dict:
        """
        提取文本特征

        返回:
        {
            'char_count': int,
            'sentence_count': int,
            'avg_sentence_length': float,
            'paragraph_count': int,
            'dialogue_ratio': float,
            'dialogue_turns': int,
            'emotion_scores': Dict[str, float],
            'scene_scores': Dict[str, float],
            'action_density': float,
            'description_density': float,
            'pov_indicators': Dict[str, int],
        }
        """
        char_count = len(text)
        sentence_count = text.count("。") + text.count("！") + text.count("？")
        avg_sentence_length = char_count / max(sentence_count, 1)
        paragraph_count = text.count("\n\n") + 1

        # 对话比例（简化版）
        dialogue_matches = re.findall(r'"([^"]*)"', text)
        dialogue_ratio = sum(len(d) for d in dialogue_matches) / max(char_count, 1)
        dialogue_turns = len(dialogue_matches)

        # 情绪得分
        emotion_scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            count = sum(text.count(kw) for kw in keywords)
            emotion_scores[emotion] = count / max(char_count, 0.001) * 100

        # 场景得分
        scene_scores = {}
        for scene_type, keywords in self.SCENE_KEYWORDS.items():
            count = sum(text.count(kw) for kw in keywords)
            scene_scores[scene_type] = count / max(char_count, 0.001) * 100

        # 节奏分析
        action_density = (
            sum(text.count(v) for v in self.ACTION_VERBS) / max(char_count, 0.001) * 100
        )
        description_density = (
            sum(text.count(w) for w in self.DESCRIPTION_WORDS)
            / max(char_count, 0.001)
            * 100
        )

        # 视角分析
        pov_indicators = {}
        for pronoun, indicator in self.POV_PRONOUNS.items():
            count = text.count(pronoun)
            if count > 0:
                pov_indicators[indicator] = count

        return {
            "char_count": char_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "paragraph_count": paragraph_count,
            "dialogue_ratio": round(dialogue_ratio, 4),
            "dialogue_turns": dialogue_turns,
            "emotion_scores": emotion_scores,
            "scene_scores": scene_scores,
            "action_density": round(action_density, 6),
            "description_density": round(description_density, 6),
            "pov_indicators": pov_indicators,
        }

    def predict_preliminary_tags(self, features: Dict) -> Dict:
        """
        基于规则预测初步标签（作为 AI 标注参考）

        返回:
        {
            '字数区间': '短篇/中篇/长篇',
            '节奏': '快节奏/慢节奏/张弛有度',
            '主情绪': str,
            '主场景': str,
            '对话比例': '高/低',
        }
        """
        tags = {
            "字数区间": self._predict_length_tag(features["char_count"]),
            "节奏": self._predict_pace_tag(features),
            "主情绪": self._predict_emotion_tag(features["emotion_scores"]),
            "主场景": self._predict_scene_tag(features["scene_scores"]),
            "对话比例": "高" if features["dialogue_ratio"] > 0.3 else "低",
        }

        # 视角预测
        if features["pov_indicators"]:
            first_count = features["pov_indicators"].get("first_person", 0)
            third_count = features["pov_indicators"].get("third_person", 0)
            if first_count > third_count * 2:
                tags["视角"] = "第一人称"
            else:
                tags["视角"] = "第三人称"

        return tags

    def _predict_length_tag(self, char_count: int) -> str:
        if char_count < 500:
            return "短篇"
        elif char_count < 2000:
            return "中篇"
        else:
            return "长篇"

    def _predict_pace_tag(self, features: Dict) -> str:
        if features["action_density"] > features["description_density"] * 2:
            return "快节奏"
        elif features["description_density"] > features["action_density"] * 2:
            return "慢节奏"
        else:
            return "张弛有度"

    def _predict_emotion_tag(self, scores: Dict) -> str:
        if not scores:
            return "中性"
        return max(scores.items(), key=lambda x: x[1])[0]

    def _predict_scene_tag(self, scores: Dict) -> str:
        if not scores:
            return "其他"
        return max(scores.items(), key=lambda x: x[1])[0]


class AIAnnotator:
    """AI 标注器 - 使用 LLM 进行多维度标注"""

    ANNOTATION_PROMPT = """你是一个专业的小说编辑，擅长分析网文的写作特点和场景类型。

请分析以下文本片段，并给出多维度标注：

【文本片段】
{text}

【分析要求】
请从以下 10 个维度进行分析，输出 JSON 格式：

1. 场景类型 (scene_type): 从以下选择最匹配的 1-3 个
   - 打斗、修炼、对话、探险、拍卖、会议、日常、过渡、其他

2. 情绪基调 (emotion): 从以下选择最匹配的 1-2 个
   - 紧张、轻松、悲伤、热血、温馨、愤怒、恐惧、中性

3. 写作手法 (techniques): 选择使用的技巧 (最多 3 个)
   - 侧面描写、对比、伏笔、倒叙、插叙、白描、细节描写、心理描写

4. 节奏快慢 (pace): 单选
   - 快节奏、慢节奏、张弛有度

5. 视角类型 (pov): 单选
   - 第一人称、第三人称限知、第三人称全知

6. 角色数量 (character_count): 单选
   - 单人、双人、多人 (3+)

7. 力量层级 (power_level): 如有明确提及则填写
   - 炼气期、筑基期、金丹期、元婴期、不明确

8. 关键元素 (key_elements): 提取 3-5 个关键词
   - 如：剑法、围攻、突破、师徒、复仇

9. 适用场景 (usage): 这个片段适合什么情况下参考
   - 如：学习打斗描写、学习情绪渲染、学习对话写作

10. 质量评分 (quality_score): 1-10 分
    - 文笔流畅度、描写生动性、节奏把控的综合评分

【参考信息】
规则预测标签：{preliminary_tags}

【输出格式】
严格输出 JSON，不要其他内容：
{{
    "scene_type": ["打斗"],
    "emotion": ["紧张", "热血"],
    "techniques": ["细节描写", "侧面描写"],
    "pace": "快节奏",
    "pov": "第三人称限知",
    "character_count": "多人 (3+)",
    "power_level": "炼气期",
    "key_elements": ["围攻", "剑法", "后发先至"],
    "usage": ["学习打斗描写", "学习紧张氛围营造"],
    "quality_score": 8
}}
"""

    def __init__(self, model: str = "dashscope-coding/qwen3.5-plus"):
        self.model = model
        self._session_id = None

    def annotate(
        self, text: str, preliminary_tags: Dict = None, max_retries: int = 3
    ) -> Dict:
        """
        对文本进行 AI 标注

        流程:
        1. 构建 prompt
        2. 调用 LLM (使用 OpenClaw sessions 或本地模型)
        3. 解析 JSON
        4. 降级处理（失败时）
        """
        # 构建 prompt
        prompt = self.ANNOTATION_PROMPT.format(
            text=text[:3000],  # 限制长度
            preliminary_tags=json.dumps(preliminary_tags, ensure_ascii=False)
            if preliminary_tags
            else "无",
        )

        # 调用 LLM（使用 OpenClaw sessions_spawn）
        annotation = None
        for attempt in range(max_retries):
            try:
                annotation = self._call_llm(prompt)
                annotation = json.loads(annotation)
                annotation["validated"] = True
                annotation["fallback"] = False
                break
            except (json.JSONDecodeError, Exception) as e:
                if attempt == max_retries - 1:
                    console.print(f"⚠️  LLM 调用失败，使用降级方案：{str(e)[:50]}")
                    annotation = self._fallback_annotation(text)
                    annotation["validated"] = False
                    annotation["fallback"] = True
                time.sleep(2**attempt)

        # 添加元数据
        annotation["text_length"] = len(text)
        annotation["annotation_model"] = self.model

        return annotation

    def _call_llm(self, prompt: str) -> str:
        """
        调用 LLM API

        使用 OpenAI 兼容 API 调用 DashScope Coding

        注意：DashScope Coding Plan 使用 OpenAI 兼容 API 格式
        Endpoint: https://coding.dashscope.aliyuncs.com/v1

        安全说明:
        - API Key 仅从环境变量 DASHSCOPE_API_KEY 获取
        - 不读取任何配置文件
        - 不存储 API Key 到本地
        """
        try:
            from openai import OpenAI
        except ImportError:
            # 回退到 httpx 直接调用
            return self._call_llm_http(prompt)

        # 获取 API key (仅从环境变量)
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")

        if not api_key:
            raise Exception(
                "未配置 DashScope API Key，请设置环境变量 DASHSCOPE_API_KEY"
            )

        # 创建 OpenAI 客户端 (使用 DashScope Coding endpoint)
        client = OpenAI(
            api_key=api_key, base_url="https://coding.dashscope.aliyuncs.com/v1"
        )

        # 调用 API
        response = client.chat.completions.create(
            model=self.model.replace("dashscope-coding/", ""),  # 去掉前缀
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    def _call_llm_http(self, prompt: str) -> str:
        """
        HTTP 方式调用 DashScope Coding API (回退方案)
        """
        import httpx

        # 获取 API key (仅从环境变量)
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")

        if not api_key:
            raise Exception(
                "未配置 DashScope API Key，请设置环境变量 DASHSCOPE_API_KEY"
            )

        # 构建请求
        url = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model.replace("dashscope-coding/", ""),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.7,
        }

        response = httpx.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    def _fallback_annotation(self, text: str) -> Dict:
        """
        LLM 调用失败时的降级标注

        使用规则预标注的结果
        """
        extractor = FeatureExtractor()
        features = extractor.extract_features(text)
        preliminary_tags = extractor.predict_preliminary_tags(features)

        return {
            "scene_type": [preliminary_tags.get("主场景", "其他")],
            "emotion": [preliminary_tags.get("主情绪", "中性")],
            "techniques": [],
            "pace": preliminary_tags.get("节奏", "张弛有度"),
            "pov": preliminary_tags.get("视角", "第三人称限知"),
            "character_count": "不明确",
            "power_level": "不明确",
            "key_elements": [],
            "usage": ["参考"],
            "quality_score": 5,
            "fallback": True,
        }
