"""小红书文案生成"""

from src.storage.models import Project, AnalysisResult, PostContent
from src.utils.llm_client import LLMClient
from src.content.tag_generator import TagGenerator


COPYWRITER_SYSTEM = """你是一位小红书爆款内容创作者，专注于 AI/编程/开源项目领域。
你的内容风格：专业但不装，有料但好懂，像一个热心的技术朋友在分享好东西。"""

COPYWRITER_PROMPT = """根据以下项目分析，生成一篇小红书帖子。

## 项目信息
- 名称: {name}
- 仓库: {repo_url}
- Stars: {stars}
- 描述: {description}

## 项目教程
{tutorial}

---

## 小红书文案要求

### 标题规则
- ≤20 字，必须带 emoji
- 制造好奇心或价值感
- 参考句式："发现一个XX神器🔥"、"这个AI项目让我XX😱"、"XX天star破万的开源项目"

### 正文规则
- 300-500 字
- 口语化，像跟朋友聊天
- Hook 开头（前两行决定展开率！）
- 分段清晰，善用 emoji 分隔
- 结尾带 CTA（引导关注/收藏/评论）

### 禁用词
绝对不能出现以下词语：赋能、抓手、底层逻辑、生态、闭环、链路、颗粒度、对齐、拉通、沉淀

### 格式
请直接输出文案，不要解释。标题单独一行，空一行后接正文。"""


class Copywriter:
    """小红书文案生成器"""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.tag_generator = TagGenerator(llm)

    def generate(self, analysis: AnalysisResult, project: Project) -> PostContent:
        """生成完整的小红书文案（含标签）"""
        print("✍️  正在生成小红书文案...")

        prompt = COPYWRITER_PROMPT.format(
            name=project.name,
            repo_url=project.repo_url,
            stars=project.stars,
            description=project.description,
            tutorial=analysis.full_markdown[:3000],
        )

        raw_text = self.llm.chat(prompt, system=COPYWRITER_SYSTEM)

        # 分离标题和正文
        lines = raw_text.strip().split("\n")
        title = lines[0].strip().lstrip("#").strip()
        body = "\n".join(lines[1:]).strip()

        # 生成标签
        tags = self.tag_generator.generate(project, analysis)
        tag_line = " ".join(tags)

        full_text = f"{title}\n\n{body}\n\n{tag_line}"

        return PostContent(
            title=title,
            body=body,
            tags=tags,
            full_text=full_text,
        )
