"""AI 配图生成 - OpenAI 兼容协议"""

from src.utils.image_client import ImageClient
from src.config import ImageConfig


class AIImageGenerator:
    """AI 概念配图生成器"""

    def __init__(self, config: ImageConfig):
        self.client = ImageClient(config)
        self.enabled = bool(config.api_key)

    def generate_concept(
        self,
        description: str,
        output_path: str,
    ) -> str:
        """生成概念配图（如"多个 AI 协作"的意境图）"""
        if not self.enabled:
            print("  ⚠ AI 配图未配置 (IMAGE_API_KEY)，跳过")
            return ""

        prompt = (
            f"A clean, modern tech illustration representing: {description}. "
            "Flat design, geometric shapes, soft gradients, "
            "tech blue and purple color scheme, minimalist style, "
            "no text, no watermark."
        )

        try:
            return self.client.generate(prompt, output_path)
        except Exception as e:
            print(f"  ⚠ AI 配图生成失败: {e}")
            return ""

    def generate_cover_bg(
        self,
        project_name: str,
        output_path: str,
    ) -> str:
        """生成封面背景图"""
        if not self.enabled:
            return ""

        prompt = (
            f"Abstract tech background for a project called '{project_name}'. "
            "Soft gradient, geometric patterns, neural network nodes, "
            "blue and purple tones, clean and modern, no text."
        )

        try:
            return self.client.generate(prompt, output_path)
        except Exception as e:
            print(f"  ⚠ 封面背景生成失败: {e}")
            return ""
