#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color Toolkit - 智能颜色推荐引擎
基于语义解析生成配色方案
"""

import random
import re
from typing import List, Dict, Any, Optional, Tuple
from color_toolkit import ColorCore, convert_color, get_palette, HSL
from preview_generator import generate_palette_page_html, generate_full_preview_html


# ============ 颜色语义映射表 ============

# 主题/情绪 → 主色调
THEME_PRIMARY_COLORS = {
    # 情感/氛围
    "科技": ("#0066FF", "#00D4FF", "#1A1A2E"),
    "科技感": ("#0066FF", "#00D4FF", "#1A1A2E"),
    "未来": ("#00FFFF", "#FF00FF", "#000033"),
    "未来感": ("#00FFFF", "#FF00FF", "#000033"),
    "赛博朋克": ("#00FFFF", "#FF0080", "#0D0221"),

    "温暖": ("#FF6B35", "#FFB347", "#FFF3E0"),
    "温暖感": ("#FF6B35", "#FFB347", "#FFF3E0"),
    "热情": ("#FF4500", "#FF6347", "#FFDAB9"),
    "活力": ("#FF5722", "#FFC107", "#FFEB3B"),

    "自然": ("#4CAF50", "#8BC34A", "#E8F5E9"),
    "自然感": ("#4CAF50", "#8BC34A", "#E8F5E9"),
    "环保": ("#2E7D32", "#81C784", "#C8E6C9"),
    "春天": ("#4CAF50", "#E91E63", "#FF9800"),
    "夏季": ("#00BCD4", "#4CAF50", "#FFEB3B"),
    "秋季": ("#FF5722", "#795548", "#FF9800"),
    "冬季": ("#607D8B", "#90A4AE", "#ECEFF1"),

    "专业": ("#1565C0", "#0D47A1", "#E3F2FD"),
    "商务": ("#37474F", "#546E7A", "#ECEFF1"),
    "金融": ("#1565C0", "#FFD700", "#0D47A1"),
    "医疗": ("#2196F3", "#4CAF50", "#FFFFFF"),

    "可爱": ("#FF69B4", "#FFB6C1", "#FFF0F5"),
    "甜美": ("#FF69B4", "#DDA0DD", "#FFF0F5"),
    "少女": ("#FFB6C1", "#FF69B4", "#FFF0F5"),
    "浪漫": ("#E91E63", "#F8BBD9", "#FFF0F5"),

    "优雅": ("#9C27B0", "#673AB7", "#F3E5F5"),
    "高贵": ("#6A1B9A", "#FFD700", "#4A148C"),
    "奢华": ("#FFD700", "#4A148C", "#1A1A1A"),

    "简约": ("#212121", "#757575", "#FAFAFA"),
    "极简": ("#000000", "#FFFFFF", "#F5F5F5"),
    "北欧": ("#ECEFF1", "#90A4AE", "#37474F"),
    "日式": ("#EFEBE9", "#D7CCC8", "#5D4037"),

    "复古": ("#8B4513", "#D2691E", "#FFF8DC"),
    "怀旧": ("#CD853F", "#DEB887", "#FAEBD7"),
    "工业": ("#424242", "#FF5722", "#212121"),

    "艺术": ("#9C27B0", "#E91E63", "#FFEB3B"),
    "创意": ("#673AB7", "#FF5722", "#00BCD4"),
    "活力": ("#FF5722", "#FFC107", "#FFEB3B"),

    "清新": ("#00BCD4", "#4CAF50", "#E0F7FA"),
    "清爽": ("#00BCD4", "#B2EBF2", "#FFFFFF"),
    "海洋": ("#006994", "#00CED1", "#E0F7FA"),

    "神秘": ("#4A148C", "#7B1FA2", "#1A1A2E"),
    "暗夜": ("#1A1A1A", "#37474F", "#263238"),
    "暗黑": ("#000000", "#212121", "#424242"),

    "活力": ("#FF5722", "#FFC107", "#FFEB3B"),
    "运动": ("#FF5722", "#4CAF50", "#2196F3"),
    "青春": ("#FF5722", "#E91E63", "#9C27B0"),
}

# 情感词汇 → 微调参数
EMOTION_ADJUSTMENTS = {
    "活泼": {"saturation_boost": 15, "lightness_range": (40, 70)},
    "稳重": {"saturation_boost": -10, "lightness_range": (30, 60)},
    "柔和": {"saturation_boost": -20, "lightness_range": (60, 85)},
    "强烈": {"saturation_boost": 20, "lightness_range": (35, 65)},
    "低调": {"saturation_boost": -30, "lightness_range": (25, 75)},
    "明亮": {"saturation_boost": 10, "lightness_range": (55, 85)},
    "深沉": {"saturation_boost": 5, "lightness_range": (15, 45)},
    "轻快": {"saturation_boost": 10, "lightness_range": (55, 80)},
    "神秘": {"saturation_boost": 15, "lightness_range": (20, 50)},
    "温暖": {"saturation_boost": 10, "lightness_range": (45, 70)},
    "清凉": {"saturation_boost": 5, "lightness_range": (40, 75)},
}


# ============ 语义解析器 ============

class ColorSemanticParser:
    """解析用户描述，提取颜色需求"""

    @staticmethod
    def parse(description: str) -> Dict[str, Any]:
        """
        解析用户描述

        Returns:
            {
                "themes": ["科技", "未来感"],
                "emotions": ["专业", "稳重"],
                "mood": "warm/cool/neutral",
                "brightness": "dark/bright/medium",
                "saturation": "vivid/muted/soft"
            }
        """
        desc = description.lower()

        # 提取主题
        themes = []
        for theme in THEME_PRIMARY_COLORS.keys():
            if theme.lower() in desc or theme in desc:
                themes.append(theme)

        # 情感词汇
        emotions = []
        for emotion in EMOTION_ADJUSTMENTS.keys():
            if emotion.lower() in desc or emotion in desc:
                emotions.append(emotion)

        # 色温判断
        warm_words = ["暖", "热", "阳", "活力", "热情", "活力", "warm", "hot", "sun"]
        cool_words = ["冷", "冰", "科技", "清新", "cool", "ice", "tech", "fresh"]
        mood = "neutral"
        if any(w in desc for w in warm_words):
            mood = "warm"
        elif any(w in desc for w in cool_words):
            mood = "cool"

        # 亮度判断
        bright_words = ["亮", "浅", "淡", "明", "bright", "light", "soft"]
        dark_words = ["暗", "深", "浓", "dark", "deep", "rich"]
        brightness = "medium"
        if any(w in desc for w in bright_words):
            brightness = "bright"
        elif any(w in desc for w in dark_words):
            brightness = "dark"

        # 饱和度
        vivid_words = ["鲜", "纯", "强烈", "vivid", "pure", "strong"]
        muted_words = ["柔", "淡", "粉", "muted", "soft", "pastel"]
        saturation = "medium"
        if any(w in desc for w in vivid_words):
            saturation = "vivid"
        elif any(w in desc for w in muted_words):
            saturation = "muted"

        return {
            "themes": themes if themes else ["自定义"],
            "emotions": emotions,
            "mood": mood,
            "brightness": brightness,
            "saturation": saturation,
            "original": description
        }


# ============ 颜色推荐引擎 ============

class ColorRecommender:
    """智能颜色推荐引擎"""

    def __init__(self):
        self.parser = ColorSemanticParser()

    def recommend(self, description: str) -> Dict[str, Any]:
        """
        根据描述推荐颜色方案

        Args:
            description: 用户描述（如"科技感蓝色"、"春天主题"）

        Returns:
            完整的配色方案
        """
        # 1. 解析语义
        parsed = self.parser.parse(description)

        # 2. 确定主题配色
        theme_key = parsed["themes"][0] if parsed["themes"] else "自定义"
        base_colors = THEME_PRIMARY_COLORS.get(theme_key, self._generate_random_base())

        # 3. 提取主色
        primary_hex = base_colors[0]
        primary_rgb = ColorCore.hex_to_rgb(primary_hex)
        primary_hsl = ColorCore.rgb_to_hsl(primary_rgb.r, primary_rgb.g, primary_rgb.b)

        # 4. 应用情感微调
        adjusted_hsl = self._apply_emotion_adjustment(
            primary_hsl,
            parsed["emotions"],
            parsed["brightness"],
            parsed["saturation"]
        )

        # 5. 生成完整配色
        adjusted_rgb = ColorCore.hsl_to_rgb(adjusted_hsl.h, adjusted_hsl.s, adjusted_hsl.l)
        final_primary = ColorCore.rgb_to_hex(adjusted_rgb.r, adjusted_rgb.g, adjusted_rgb.b)

        # 6. 生成辅助色
        secondary_colors = self._generate_secondary_colors(final_primary, parsed)

        # 7. 生成强调色
        accent_color = self._generate_accent_color(final_primary, parsed)

        # 8. 确定背景和文字色
        background, text_color = self._determine_bg_text(final_primary, parsed)

        # 9. 生成调色板
        palette = self._build_palette(final_primary, secondary_colors, accent_color)

        return {
            "request": description,
            "parsed": parsed,
            "palette": {
                "primary": {
                    "hex": final_primary,
                    "name": self._get_color_name(final_primary),
                    **convert_color(final_primary)
                },
                "secondary": [
                    {
                        "hex": c,
                        "name": self._get_color_name(c),
                        **convert_color(c)
                    }
                    for c in secondary_colors
                ],
                "accent": {
                    "hex": accent_color,
                    "name": self._get_color_name(accent_color),
                    **convert_color(accent_color)
                },
                "background": background,
                "text": text_color
            },
            "full_palette": palette
        }

    def recommend_multiple(self, descriptions: List[str]) -> List[Dict[str, Any]]:
        """推荐多个配色方案"""
        return [self.recommend(desc) for desc in descriptions]

    def _generate_random_base(self) -> Tuple[str, str, str]:
        """生成随机基准色"""
        hues = [0, 30, 60, 120, 180, 210, 270, 300]
        h = random.choice(hues)
        s = 60 + random.random() * 30
        l = 45 + random.random() * 20
        rgb = ColorCore.hsl_to_rgb(h, s, l)
        hex_color = ColorCore.rgb_to_hex(rgb.r, rgb.g, rgb.b)
        return (hex_color, "#FFFFFF", "#000000")

    def _apply_emotion_adjustment(self, hsl, emotions: List[str],
                                   brightness: str, saturation: str) -> 'HSL':
        """应用情感调整"""
        h, s, l = hsl.h, hsl.s, hsl.l

        # 应用情感词调整
        for emotion in emotions:
            adj = EMOTION_ADJUSTMENTS.get(emotion, {})
            s += adj.get("saturation_boost", 0)
            if "lightness_range" in adj:
                l = sum(adj["lightness_range"]) / 2

        # 应用亮度偏好
        if brightness == "dark":
            l = min(45, l * 0.7)
        elif brightness == "bright":
            l = min(85, l * 1.2)

        # 应用饱和度偏好
        if saturation == "vivid":
            s = min(100, s * 1.2)
        elif saturation == "muted":
            s = max(20, s * 0.6)

        # 限制范围
        s = max(0, min(100, s))
        l = max(10, min(90, l))

        return HSL(h=h, s=s, l=l)

    def _generate_secondary_colors(self, primary_hex: str, parsed: Dict) -> List[str]:
        """生成辅助色"""
        primary_rgb = ColorCore.hex_to_rgb(primary_hex)
        primary_hsl = ColorCore.rgb_to_hsl(primary_rgb.r, primary_rgb.g, primary_rgb.b)

        # 基于主色生成互补/类似色
        complement_hsl = HSL(
            h=(primary_hsl.h + 180) % 360,
            s=primary_hsl.s * 0.8,
            l=min(70, primary_hsl.l * 1.1)
        )
        complement_rgb = ColorCore.hsl_to_rgb(complement_hsl.h, complement_hsl.s, complement_hsl.l)
        complement = ColorCore.rgb_to_hex(complement_rgb.r, complement_rgb.g, complement_rgb.b)

        # 类似色
        analogous_hsl = HSL(
            h=(primary_hsl.h + 30) % 360,
            s=primary_hsl.s * 0.9,
            l=min(75, primary_hsl.l * 1.15)
        )
        analogous_rgb = ColorCore.hsl_to_rgb(analogous_hsl.h, analogous_hsl.s, analogous_hsl.l)
        analogous = ColorCore.rgb_to_hex(analogous_rgb.r, analogous_rgb.g, analogous_rgb.b)

        return [complement, analogous]

    def _generate_accent_color(self, primary_hex: str, parsed: Dict) -> str:
        """生成强调色"""
        primary_rgb = ColorCore.hex_to_rgb(primary_hex)
        primary_hsl = ColorCore.rgb_to_hsl(primary_rgb.r, primary_rgb.g, primary_rgb.b)

        # 对比强调色
        accent_hsl = HSL(
            h=(primary_hsl.h + 120) % 360,
            s=min(100, primary_hsl.s * 1.2),
            l=50
        )
        accent_rgb = ColorCore.hsl_to_rgb(accent_hsl.h, accent_hsl.s, accent_hsl.l)
        return ColorCore.rgb_to_hex(accent_rgb.r, accent_rgb.g, accent_rgb.b)

    def _determine_bg_text(self, primary_hex: str, parsed: Dict) -> Tuple[str, str]:
        """确定背景和文字色"""
        primary_rgb = ColorCore.hex_to_rgb(primary_hex)
        luminance = float(ColorCore.calculate_luminance(primary_rgb.r, primary_rgb.g, primary_rgb.b))

        if luminance < 0.3:
            # 深色主色
            background = "#FFFFFF"
            text_color = "#1A1A1A"
        elif luminance > 0.7:
            # 浅色主色
            background = "#1A1A1A"
            text_color = "#FFFFFF"
        else:
            # 中等亮度
            background = "#F5F5F5"
            text_color = "#1A1A1A"

        return background, text_color

    def _build_palette(self, primary: str, secondary: List[str], accent: str) -> List[str]:
        """构建完整调色板"""
        palette = [primary] + secondary + [accent]
        return palette

    @staticmethod
    def _get_color_name(hex_color: str) -> str:
        """获取颜色名称"""
        rgb = ColorCore.hex_to_rgb(hex_color)
        hsl = ColorCore.rgb_to_hsl(rgb.r, rgb.g, rgb.b)

        # 基于HSL判断颜色名
        h, s, l = hsl.h, hsl.s, hsl.l

        if s < 10:
            if l < 20:
                return "深灰"
            elif l > 80:
                return "浅灰"
            return "灰色"

        names = [
            (0, 15, "红"),
            (15, 30, "橙红"),
            (30, 45, "橙"),
            (45, 60, "橙黄"),
            (60, 75, "黄"),
            (75, 90, "黄绿"),
            (90, 120, "绿"),
            (120, 150, "青绿"),
            (150, 180, "青"),
            (180, 210, "蓝绿"),
            (210, 240, "蓝"),
            (240, 270, "靛蓝"),
            (270, 300, "紫"),
            (300, 330, "紫红"),
            (330, 345, "粉"),
            (345, 360, "红"),
        ]

        for start, end, name in names:
            if start <= h < end:
                prefix = "深" if l < 35 else ("浅" if l > 70 else "")
                return f"{prefix}{name}"

        return "彩色"


# ============ 便捷函数 ============

def recommend_color(description: str, generate_preview: bool = True,
                   output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    推荐颜色方案

    Args:
        description: 描述（中文/英文）
        generate_preview: 是否生成HTML预览
        output_path: 预览文件路径

    Returns:
        配色方案字典
    """
    recommender = ColorRecommender()
    result = recommender.recommend(description)

    # 生成预览
    if generate_preview:
        palette_colors = result["full_palette"]
        html_content = generate_palette_page_html(
            palette_colors,
            palette_title=f"配色方案 - {description}",
            output_path=output_path
        )
        result["preview_path"] = output_path or "palette_preview.html"
        result["preview_html"] = html_content

    return result


def format_recommendation_output(result: Dict[str, Any]) -> str:
    """格式化输出推荐结果"""
    palette = result["palette"]
    parsed = result["parsed"]

    output = f"""
## 配色方案推荐

**原始描述**: {result["request"]}
**解析结果**: 主题[{', '.join(parsed['themes'])}] | 亮度[{parsed['brightness']}] | 饱和度[{parsed['saturation']}]

---

### 主色
| 属性 | 值 |
|------|-----|
| HEX | {palette['primary']['hex'].upper()} |
| RGB | rgb({palette['primary']['rgb']['r']}, {palette['primary']['rgb']['g']}, {palette['primary']['rgb']['b']}) |
| HSL | hsl({palette['primary']['hsl']['h']}, {palette['primary']['hsl']['s']}%, {palette['primary']['hsl']['l']}%) |
| 名称 | {palette['primary']['name']} |

### 辅助色
"""

    for i, sec in enumerate(palette["secondary"], 1):
        output += f"""
**辅助色 {i}**
- HEX: {sec['hex'].upper()}
- RGB: rgb({sec['rgb']['r']}, {sec['rgb']['g']}, {sec['rgb']['b']})
- 名称: {sec['name']}
"""

    output += f"""
### 强调色
- HEX: {palette['accent']['hex'].upper()}
- RGB: rgb({palette['accent']['rgb']['r']}, {palette['accent']['rgb']['g']}, {palette['accent']['rgb']['b']})
- 名称: {palette['accent']['name']}

### 背景与文字
- 背景色: {palette['background']}
- 文字色: {palette['text']}

---
**完整调色板**: {' | '.join([c.upper() for c in result['full_palette']])}
"""

    if result.get("preview_path"):
        output += f"\n📄 预览文件: {result['preview_path']}"

    return output


if __name__ == "__main__":
    # 测试
    result = recommend_color("科技感 蓝色", output_path="test_palette.html")
    print(format_recommendation_output(result))
