import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class CharacterInfo:
    name: str
    description: str
    traits: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)


class AnchorExtractor:
    def __init__(self):
        self.character_patterns = [
            r'([^，。！？\n]{2,4})[，,：:]\s*(\d+岁|性格[^，。]+|身份[^，。]+|手持[^，。]+)',
            r'([^，。！？\n]{2,4})[是为一]\s*(?:个|位)?([^，。！？\n]{2,20})',
            r'名叫([^，。！？\n]{2,8})[，,]([^，。！？\n]+)',
        ]
        self.world_patterns = [
            r'(世界|大陆|朝代|时代|背景)[是为：:]\s*([^，。\n]+)',
            r'(存在|有)[^，。]*?([^，。]+族|[^，。]+教|[^，。]+门|[^，。]+派)',
        ]
        self.plot_keywords = ['寻找', '追杀', '复仇', '冒险', '探索', '拯救', '保护', '追求', '目标', '任务']

    def extract_characters(self, text: str) -> List[CharacterInfo]:
        characters = []
        seen_names = set()

        for pattern in self.character_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                name = match[0].strip()
                desc = match[1].strip() if len(match) > 1 else ""

                if name and name not in seen_names and len(name) <= 8:
                    seen_names.add(name)
                    traits = self._extract_traits(desc)
                    characters.append(CharacterInfo(
                        name=name,
                        description=desc,
                        traits=traits
                    ))

        return characters

    def _extract_traits(self, text: str) -> List[str]:
        trait_keywords = ['性格', '善良', '勇敢', '聪明', '洒脱', '嫉恶如仇', '温柔', '冷酷', '机智']
        traits = []
        for keyword in trait_keywords:
            if keyword in text:
                traits.append(keyword)
        return traits

    def extract_world_setting(self, text: str) -> str:
        world_info = []

        for pattern in self.world_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    world_info.append(''.join(match))
                else:
                    world_info.append(match)

        style_keywords = ['武侠', '仙侠', '玄幻', '古风', '现代', '科幻', '奇幻']
        for keyword in style_keywords:
            if keyword in text:
                world_info.append(f"{keyword}世界")
                break

        return '；'.join(world_info) if world_info else "未明确设定"

    def extract_main_plot(self, text: str) -> str:
        sentences = re.split(r'[。！？\n]', text)
        plot_sentences = []

        for sentence in sentences:
            for keyword in self.plot_keywords:
                if keyword in sentence and len(sentence) > 5:
                    plot_sentences.append(sentence.strip())
                    break

        if plot_sentences:
            return '；'.join(plot_sentences[:3])
        return "未明确主线"

    def extract_writing_style(self, text: str) -> str:
        style_indicators = {
            '古风': ['之', '乎', '者', '也', '矣', '焉'],
            '现代': ['的', '了', '着', '过', '吗', '呢'],
            '简洁': lambda t: len(re.findall(r'[，。]', t)) / max(len(t), 1) > 0.05,
            '细腻': lambda t: len(re.findall(r'[的地得]', t)) / max(len(t), 1) > 0.03,
        }

        detected_styles = []

        for style, indicators in style_indicators.items():
            if callable(indicators):
                if indicators(text):
                    detected_styles.append(style)
            else:
                count = sum(text.count(char) for char in indicators)
                if count > len(text) * 0.01:
                    detected_styles.append(style)

        return '、'.join(detected_styles) if detected_styles else "通用风格"

    def extract_anchors(self, text: str, manual_hints: Dict[str, str] = None) -> Dict[str, str]:
        anchors = {}

        characters = self.extract_characters(text)
        if characters:
            char_desc = '；'.join([
                f"{c.name}：{c.description}"
                for c in characters[:5]
            ])
            anchors['人设'] = char_desc

        world = self.extract_world_setting(text)
        if world != "未明确设定":
            anchors['世界观'] = world

        plot = self.extract_main_plot(text)
        if plot != "未明确主线":
            anchors['核心剧情'] = plot

        style = self.extract_writing_style(text)
        anchors['文风'] = style

        if manual_hints:
            for key, value in manual_hints.items():
                if key not in anchors:
                    anchors[key] = value

        return anchors

    def update_anchors_with_new_content(
        self,
        existing_anchors: Dict[str, str],
        new_text: str
    ) -> Dict[str, str]:
        new_anchors = self.extract_anchors(new_text)

        updated = existing_anchors.copy()

        for key, value in new_anchors.items():
            if key in updated:
                if key == '人设':
                    existing_chars = updated[key]
                    new_chars = value
                    if new_chars and new_chars not in existing_chars:
                        updated[key] = f"{existing_chars}；{new_chars}"
                elif key == '核心剧情':
                    existing_plot = updated[key]
                    new_plot = value
                    if new_plot and new_plot not in existing_plot:
                        updated[key] = f"{existing_plot}；后续：{new_plot}"
            else:
                updated[key] = value

        return updated
