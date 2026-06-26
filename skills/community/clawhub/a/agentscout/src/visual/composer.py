"""HTML 模板 → 合成图片"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from src.config import PROJECT_ROOT


# 模板目录
TEMPLATES_DIR = PROJECT_ROOT / "templates"


def get_template_env() -> Environment:
    """获取 Jinja2 模板环境"""
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )


def html_to_image(
    html_content: str,
    output_path: str,
    width: int = 1080,
    height: int = 1440,
) -> str:
    """将 HTML 字符串渲染为图片"""
    from html2image import Html2Image

    output_dir = str(Path(output_path).parent)
    filename = Path(output_path).name
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    hti = Html2Image(output_path=output_dir, size=(width, height))
    hti.screenshot(html_str=html_content, save_as=filename)
    return output_path


class CardComposer:
    """卡片合成器 - 使用 HTML 模板生成小红书配图"""

    def __init__(self):
        self.env = get_template_env()

    def create_cover(
        self,
        project_name: str,
        description: str,
        stars: int,
        highlight: str,
        output_path: str,
        template_name: str = "cover_tech_blue.html",
    ) -> str:
        """生成封面图（P1）"""
        template = self.env.get_template(template_name)
        html = template.render(
            project_name=project_name,
            description=description,
            stars=stars,
            highlight=highlight,
        )
        return html_to_image(html, output_path)

    def create_step_card(
        self,
        steps: list[dict],
        output_path: str,
        card_title: str = "快速上手",
    ) -> str:
        """生成步骤教程卡片（P7-P8）"""
        template = self.env.get_template("step_card.html")
        html = template.render(steps=steps, card_title=card_title)
        return html_to_image(html, output_path)

    def create_architecture_card(
        self,
        architecture_text: str,
        output_path: str,
        project_name: str = "",
    ) -> str:
        """生成架构图卡片（P3-P4）"""
        template = self.env.get_template("architecture.html")
        html = template.render(
            architecture=architecture_text,
            project_name=project_name,
        )
        return html_to_image(html, output_path)

    def create_summary_card(
        self,
        summary: str,
        project_name: str,
        repo_url: str,
        output_path: str,
    ) -> str:
        """生成总结卡片（P9）"""
        template = self.env.get_template("summary_card.html")
        html = template.render(
            summary=summary,
            project_name=project_name,
            repo_url=repo_url,
        )
        return html_to_image(html, output_path)
