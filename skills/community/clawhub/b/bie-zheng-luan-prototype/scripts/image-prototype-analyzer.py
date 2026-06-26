#!/usr/bin/env python3
"""
图片原型分析器
用于分析设计稿截图、高保真原型图等图片文件
提取UI元素、布局结构、颜色信息等
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    print("错误: 需要安装Pillow")
    print("请运行: pip install Pillow")
    sys.exit(1)

@dataclass
class UIElement:
    """UI元素"""
    type: str              # 元素类型: button, input, text, image, card等
    position: Dict[str, int]  # 位置: {x, y, width, height}
    content: str           # 文本内容或描述
    style: Dict[str, Any]  # 样式信息: 颜色、字体等
    confidence: float      # 识别置信度

@dataclass
class LayoutRegion:
    """布局区域"""
    name: str              # 区域名称: header, sidebar, main, footer等
    position: Dict[str, int]
    elements: List[UIElement]
    background_color: str

@dataclass
class ImageAnalysisResult:
    """图片分析结果"""
    image_path: str
    image_size: Dict[str, int]  # {width, height}
    layout_regions: List[LayoutRegion]
    color_palette: List[str]    # 主要颜色列表
    typography: Dict[str, Any]  # 字体信息
    components: List[Dict[str, Any]]  # 识别出的组件
    statistics: Dict[str, int]
    confidence: float           # 整体置信度

class ImagePrototypeAnalyzer:
    """图片原型分析器"""

    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = None
        self.width = 0
        self.height = 0

    def load_image(self) -> bool:
        """加载图片"""
        try:
            self.image = Image.open(self.image_path)
            self.width, self.height = self.image.size
            return True
        except Exception as e:
            print(f"加载图片失败: {e}")
            return False

    def analyze(self) -> ImageAnalysisResult:
        """分析图片原型"""
        if not self.load_image():
            return None

        # 1. 分析颜色
        color_palette = self._extract_colors()

        # 2. 分析布局区域
        layout_regions = self._analyze_layout()

        # 3. 识别UI元素
        elements = self._identify_elements()

        # 4. 识别组件
        components = self._identify_components(elements)

        # 5. 统计信息
        statistics = self._calculate_statistics(elements)

        # 6. 计算置信度
        confidence = self._calculate_confidence(elements, layout_regions)

        return ImageAnalysisResult(
            image_path=self.image_path,
            image_size={'width': self.width, 'height': self.height},
            layout_regions=layout_regions,
            color_palette=color_palette,
            typography=self._extract_typography_info(),
            components=components,
            statistics=statistics,
            confidence=confidence
        )

    def _extract_colors(self) -> List[str]:
        """提取主要颜色"""
        colors = []

        # 缩小图片以加快颜色提取速度
        small_img = self.image.resize((100, 100))

        # 获取所有像素颜色
        pixels = small_img.getdata()

        # 统计颜色频率
        color_count = {}
        for pixel in pixels:
            # 转换为十六进制颜色
            if isinstance(pixel, int):  # 灰度图
                hex_color = f"#{pixel:02x}{pixel:02x}{pixel:02x}"
            elif len(pixel) >= 3:  # RGB或RGBA
                hex_color = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
            else:
                continue

            color_count[hex_color] = color_count.get(hex_color, 0) + 1

        # 取前10个最常见的颜色
        sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
        colors = [color for color, count in sorted_colors[:10]]

        return colors

    def _analyze_layout(self) -> List[LayoutRegion]:
        """分析布局区域"""
        regions = []

        # 基于图片尺寸推断可能的布局区域
        # 常见的布局比例

        # 头部区域 (顶部10-15%)
        header_height = int(self.height * 0.12)
        regions.append(LayoutRegion(
            name='header',
            position={'x': 0, 'y': 0, 'width': self.width, 'height': header_height},
            elements=[],
            background_color=self._get_region_color(0, 0, self.width, header_height)
        ))

        # 侧边栏区域 (左侧15-20%)
        sidebar_width = int(self.width * 0.18)
        sidebar_height = self.height - header_height - int(self.height * 0.08)  # 减去头部和底部
        regions.append(LayoutRegion(
            name='sidebar',
            position={'x': 0, 'y': header_height, 'width': sidebar_width, 'height': sidebar_height},
            elements=[],
            background_color=self._get_region_color(0, header_height, sidebar_width, sidebar_height)
        ))

        # 主内容区
        main_x = sidebar_width
        main_width = self.width - sidebar_width
        main_height = sidebar_height
        regions.append(LayoutRegion(
            name='main',
            position={'x': main_x, 'y': header_height, 'width': main_width, 'height': main_height},
            elements=[],
            background_color=self._get_region_color(main_x, header_height, main_width, main_height)
        ))

        # 底部区域 (底部5-8%)
        footer_height = int(self.height * 0.08)
        footer_y = self.height - footer_height
        regions.append(LayoutRegion(
            name='footer',
            position={'x': 0, 'y': footer_y, 'width': self.width, 'height': footer_height},
            elements=[],
            background_color=self._get_region_color(0, footer_y, self.width, footer_height)
        ))

        return regions

    def _get_region_color(self, x: int, y: int, width: int, height: int) -> str:
        """获取区域的主要颜色"""
        try:
            # 获取区域中心点的颜色
            center_x = x + width // 2
            center_y = y + height // 2

            # 确保坐标在图片范围内
            center_x = min(max(center_x, 0), self.width - 1)
            center_y = min(max(center_y, 0), self.height - 1)

            pixel = self.image.getpixel((center_x, center_y))

            if isinstance(pixel, int):
                return f"#{pixel:02x}{pixel:02x}{pixel:02x}"
            elif len(pixel) >= 3:
                return f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
            else:
                return "#ffffff"
        except Exception:
            return "#ffffff"

    def _identify_elements(self) -> List[UIElement]:
        """识别UI元素

        注意: 此版本使用基础图像分析技术。
        要获得更精确的UI元素识别，建议:
        1. 使用视觉大模型 (如Claude Vision、GPT-4V等)
        2. 调用外部API进行智能分析
        3. 结合OCR技术提取文本

        当前实现提供:
        - 颜色区域检测
        - 基于尺寸的区域推断
        - 基于位置的元素类型猜测
        """
        elements = []

        # 使用简单的颜色变化检测潜在元素边界
        # 这是一种基础方法，实际应用中应该使用视觉模型

        # 检测可能的按钮区域 (基于颜色差异)
        # 检测可能的输入框区域
        # 检测可能的文本区域

        # 由于没有视觉模型，这里提供占位符输出
        # 实际使用时应该调用视觉大模型

        elements.append(UIElement(
            type='placeholder',
            position={'x': 0, 'y': 0, 'width': self.width, 'height': self.height},
            content='需要使用视觉模型进行精确分析',
            style={'color': '#000000'},
            confidence=0.5
        ))

        return elements

    def _identify_components(self, elements: List[UIElement]) -> List[Dict[str, Any]]:
        """识别组件"""
        components = []

        # 基于元素类型和位置推断组件
        # 这需要视觉模型的支持

        # 提供占位符组件
        components.append({
            'type': 'unknown',
            'description': '需要使用视觉模型进行精确识别',
            'suggested_action': '调用Claude Vision或GPT-4V等视觉模型进行分析'
        })

        return components

    def _extract_typography_info(self) -> Dict[str, Any]:
        """提取字体信息"""
        # 基于颜色和区域推断可能的字体信息
        return {
            'primary_color': '#333333',  # 常见文字颜色
            'secondary_color': '#666666',
            'suggested_font_family': 'sans-serif',
            'note': '需要OCR或视觉模型进行精确识别'
        }

    def _calculate_statistics(self, elements: List[UIElement]) -> Dict[str, int]:
        """计算统计信息"""
        stats = {
            'total_elements': len(elements),
            'image_width': self.width,
            'image_height': self.height,
            'aspect_ratio': round(self.width / self.height, 2) if self.height > 0 else 0
        }

        # 按类型统计
        type_count = {}
        for elem in elements:
            type_count[elem.type] = type_count.get(elem.type, 0) + 1

        stats['element_types'] = type_count

        return stats

    def _calculate_confidence(self, elements: List[UIElement], regions: List[LayoutRegion]) -> float:
        """计算置信度"""
        # 基于分析结果的质量评估置信度
        if len(elements) == 0:
            return 0.3

        avg_confidence = sum(e.confidence for e in elements) / len(elements)

        # 区域识别增加置信度
        layout_bonus = 0.1 * len(regions)

        return min(avg_confidence + layout_bonus, 1.0)

    def to_json(self) -> str:
        """转换为JSON"""
        result = self.analyze()
        if result:
            return json.dumps(asdict(result), ensure_ascii=False, indent=2)
        return "{}"

    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        result = self.analyze()
        if not result:
            return "# 图片分析失败\n无法加载或分析图片。"

        md_lines = []

        md_lines.append("# 图片原型分析报告")
        md_lines.append("")
        md_lines.append(f"**图片路径**: {result.image_path}")
        md_lines.append(f"**图片尺寸**: {result.image_size['width']}x{result.image_size['height']}px")
        md_lines.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append(f"**置信度**: {result.confidence:.2f}")
        md_lines.append("")

        md_lines.append("## 主要颜色")
        md_lines.append("")
        for color in result.color_palette[:5]:
            md_lines.append(f"- {color}")
        md_lines.append("")

        md_lines.append("## 布局区域")
        md_lines.append("")
        for region in result.layout_regions:
            md_lines.append(f"### {region.name}")
            md_lines.append(f"- 位置: ({region.position['x']}, {region.position['y']})")
            md_lines.append(f"- 尺寸: {region.position['width']}x{region.position['height']}px")
            md_lines.append(f"- 背景色: {region.background_color}")
            md_lines.append("")

        md_lines.append("## UI元素")
        md_lines.append("")
        md_lines.append(f"检测到 {result.statistics['total_elements']} 个元素")
        md_lines.append("")

        md_lines.append("## 组件识别")
        md_lines.append("")
        for comp in result.components:
            md_lines.append(f"- **{comp.get('type', '未知')}**: {comp.get('description', '')}")
            md_lines.append(f"  建议: {comp.get('suggested_action', '')}")
        md_lines.append("")

        md_lines.append("## 分析建议")
        md_lines.append("")
        md_lines.append("### 使用视觉模型增强分析")
        md_lines.append("")
        md_lines.append("> ⚠️ **数据传输警告**: 视觉增强分析会将图片发送到外部API服务。")
        md_lines.append("> 请确认图片不包含敏感信息后再启用此功能。")
        md_lines.append("")
        md_lines.append("当前版本使用基础图像分析技术。要获得更精确的分析结果，建议：")
        md_lines.append("")
        md_lines.append("1. **使用Claude Vision**: 需设置环境变量 `ANTHROPIC_API_KEY`")
        md_lines.append("2. **使用GPT-4V**: 调用OpenAI视觉API进行分析")
        md_lines.append("3. **结合OCR技术**: 使用PaddleOCR或Tesseract提取文本内容")
        md_lines.append("")
        md_lines.append("### Claude Vision 分析示例")
        md_lines.append("")
        md_lines.append("```python")
        md_lines.append("# 使用Claude Vision分析图片原型")
        md_lines.append("# 注意：此功能会将图片发送到Anthropic服务器")
        md_lines.append("import anthropic")
        md_lines.append("import os")
        md_lines.append("")
        md_lines.append("# 需要设置环境变量 ANTHROPIC_API_KEY")
        md_lines.append("api_key = os.environ.get('ANTHROPIC_API_KEY')")
        md_lines.append("if not api_key:")
        md_lines.append("    raise ValueError('请设置环境变量 ANTHROPIC_API_KEY')")
        md_lines.append("")
        md_lines.append("client = anthropic.Anthropic(api_key=api_key)")
        md_lines.append("")
        md_lines.append("# 读取图片并编码为base64")
        md_lines.append("import base64")
        md_lines.append("with open(image_path, 'rb') as f:")
        md_lines.append("    image_data = base64.b64encode(f.read()).decode()")
        md_lines.append("")
        md_lines.append("# 发送给Claude进行分析（图片将传输到外部服务器）")
        md_lines.append("response = client.messages.create(")
        md_lines.append("    model='claude-3-opus-20240229',")
        md_lines.append("    max_tokens=4096,")
        md_lines.append("    messages=[{")
        md_lines.append("        'role': 'user',")
        md_lines.append("        'content': [")
        md_lines.append("            {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': image_data}},")
        md_lines.append("            {'type': 'text', 'text': '分析这张UI设计稿，提取：1.页面布局结构 2.UI组件类型 3.交互元素 4.颜色方案 5.文本内容'}")
        md_lines.append("        ]")
        md_lines.append("    }]")
        md_lines.append(")")
        md_lines.append("```")
        md_lines.append("")

        md_lines.append("---")
        md_lines.append("*生成工具: bie-zheng-luan-prototype技能*")
        md_lines.append("*注意: 建议使用视觉大模型获得更精确的分析结果*")

        return "\n".join(md_lines)


def analyze_with_vision_model(image_path: str, analysis_prompt: str = None) -> Dict[str, Any]:
    """使用视觉模型分析图片

    这是一个接口函数，用于调用外部视觉模型进行精确分析。
    需要配置相应的API密钥。

    Args:
        image_path: 图片文件路径
        analysis_prompt: 自定义分析提示词

    Returns:
        视觉模型的详细分析结果
    """
    import base64

    # 默认分析提示词
    default_prompt = """
请详细分析这张UI原型/设计稿图片，提取以下信息：

1. **页面布局结构**：
   - 头部区域内容和元素
   - 侧边栏结构和导航
   - 主内容区布局
   - 底部区域内容

2. **UI组件识别**：
   - 识别所有按钮、输入框、下拉框、表格、卡片等组件
   - 描述每个组件的位置、样式、文案

3. **交互元素**：
   - 可点击元素（按钮、链接）
   - 可输入元素（文本框、下拉框）
   - 导航菜单结构

4. **颜色和样式**：
   - 主色调和辅助色
   - 字体大小和样式推断
   - 间距和布局规律

5. **文本内容**：
   - 所有可见的文字内容
   - 标题、描述、按钮文案

请以结构化格式输出，便于生成技术实现文档。
"""

    prompt = analysis_prompt or default_prompt

    # 读取图片
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
    except Exception as e:
        return {'error': f'读取图片失败: {e}'}

    # 检测图片类型
    image_ext = Path(image_path).suffix.lower()
    media_type_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp'
    }
    media_type = media_type_map.get(image_ext, 'image/png')

    # 这里应该调用实际的视觉模型API
    # 当前返回占位符，实际使用时需要配置API

    return {
        'note': '需要配置视觉模型API（如Claude Vision或GPT-4V）',
        'image_data': image_data[:100] + '...',  # 仅显示部分
        'media_type': media_type,
        'prompt': prompt,
        'suggested_api': 'anthropic.messages.create with image content type'
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python image-prototype-analyzer.py <图片文件> [输出格式: markdown|json]")
        print("示例: python image-prototype-analyzer.py design.png markdown")
        print("")
        print("支持的图片格式: PNG, JPG, JPEG, GIF, WebP, BMP")
        sys.exit(1)

    image_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "markdown"

    if not Path(image_file).exists():
        print(f"错误: 图片文件不存在: {image_file}")
        sys.exit(1)

    # 创建分析器
    analyzer = ImagePrototypeAnalyzer(image_file)

    # 输出结果
    if output_format.lower() == "json":
        result = analyzer.to_json()
    else:
        result = analyzer.to_markdown()

    print(result)


if __name__ == "__main__":
    main()