"""智能标签生成"""

from src.storage.models import Project, AnalysisResult
from src.utils.llm_client import LLMClient

# 固定标签池
FIXED_TAGS = [
    "#AI开源项目",
    "#GitHub宝藏",
    "#AI工具推荐",
    "#程序员日常",
]

TAG_PROMPT = """根据以下 GitHub 项目信息，生成 3-5 个小红书标签。

项目名: {name}
描述: {description}
语言: {language}
Topics: {topics}
内容摘要: {summary}

要求：
- 每个标签以 # 开头
- 标签要有热度（能被搜到）
- 涵盖：项目类型、技术领域、应用场景
- 优先中文标签
- 每行一个标签，不要其他内容

示例：
#多智能体
#清华开源
#AI编程助手
"""


class TagGenerator:
    """标签生成器"""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate(self, project: Project, analysis: AnalysisResult) -> list[str]:
        """生成标签列表：固定标签 + 动态标签"""
        dynamic_tags = self._generate_dynamic(project, analysis)
        all_tags = FIXED_TAGS + dynamic_tags
        # 去重
        seen = set()
        unique = []
        for tag in all_tags:
            normalized = tag.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique.append(normalized)
        return unique

    def _generate_dynamic(self, project: Project, analysis: AnalysisResult) -> list[str]:
        """用 LLM 生成动态标签"""
        try:
            prompt = TAG_PROMPT.format(
                name=project.name,
                description=project.description,
                language=project.language,
                topics=", ".join(project.topics),
                summary=analysis.full_markdown[:500] if analysis.full_markdown else project.description,
            )
            raw = self.llm.chat(prompt, temperature=0.5, max_tokens=200)
            tags = []
            for line in raw.strip().split("\n"):
                line = line.strip()
                if line.startswith("#"):
                    tags.append(line)
            return tags[:5]
        except Exception as e:
            print(f"  ⚠ 动态标签生成失败: {e}")
            return []
