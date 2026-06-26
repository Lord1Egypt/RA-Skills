"""LLM 项目评分 - 统一 rubric"""

from src.config import AppConfig
from src.storage.models import Project, Score
from src.storage.database import Database
from src.utils.llm_client import LLMClient

RUBRIC_VERSION = "v1.0"

SCORING_PROMPT = """你是一个 GitHub 开源项目评审专家，专注于 AI Agent 领域。
请根据以下固定评分标准对项目进行打分（每项 1-10 分）：

## 评分维度

### 新颖度 (novelty) - 权重 30%
- 1-3: 常见方案的简单封装，无新意
- 4-6: 在现有方案上有一定改进或新组合
- 7-10: 提出了新的范式/架构/思路，让人眼前一亮

### 实用性 (practicality) - 权重 30%
- 1-3: 纯学术 demo，难以实际使用
- 4-6: 可运行但场景有限
- 7-10: 可直接用于生产或个人项目，解决真实痛点

### 内容适配度 (content_fit) - 权重 25%
- 1-3: 太底层/太学术，难以向非技术受众讲解
- 4-6: 技术人群会感兴趣，但需要较多解释
- 7-10: 有视觉效果/demo/对比，容易做出吸引人的内容

### 上手难度 (ease_of_use) - 权重 15%
- 1-3: 环境复杂，依赖多，文档差
- 4-6: 需要一定配置但文档清晰
- 7-10: pip install 即可用，README 即教程

## 输入信息
- 项目名: {name}
- 描述: {description}
- 语言: {language}
- Stars: {stars}
- 最近更新: {last_updated}
- Topics: {topics}
- README 摘要:
{readme_excerpt}

请严格按以下 JSON 格式输出，不要输出其他内容：
{{
  "novelty": <分数>,
  "practicality": <分数>,
  "content_fit": <分数>,
  "ease_of_use": <分数>,
  "reason": "<一句话评价>"
}}"""


class ProjectScorer:
    """项目评分器"""

    def __init__(self, config: AppConfig, llm: LLMClient, db: Database):
        self.config = config
        self.llm = llm
        self.db = db
        self.weights = config.weights

    def score_project(self, project: Project) -> Score:
        """对单个项目评分"""
        prompt = SCORING_PROMPT.format(
            name=project.name,
            description=project.description,
            language=project.language,
            stars=project.stars,
            last_updated=project.last_updated,
            topics=", ".join(project.topics),
            readme_excerpt=project.readme_excerpt,
        )

        result = self.llm.chat_json(prompt, temperature=0.3)

        novelty = float(result["novelty"])
        practicality = float(result["practicality"])
        content_fit = float(result["content_fit"])
        ease_of_use = float(result["ease_of_use"])

        total = (
            novelty * self.weights.novelty
            + practicality * self.weights.practicality
            + content_fit * self.weights.content_fit
            + ease_of_use * self.weights.ease_of_use
        )

        return Score(
            project_id=project.id,
            rubric_version=RUBRIC_VERSION,
            novelty=novelty,
            practicality=practicality,
            content_fit=content_fit,
            ease_of_use=ease_of_use,
            total_score=round(total, 2),
            scoring_reason=result.get("reason", ""),
            llm_model=self.llm.model,
        )

    def score_batch(self, projects: list[Project]) -> list[Score]:
        """批量评分"""
        scores = []
        for project in projects:
            try:
                # 先写入 DB 获取 ID
                project.id = self.db.insert_project(project)
                score = self.score_project(project)
                score.id = self.db.insert_score(score)
                scores.append(score)
                print(f"  ✓ {project.repo_full_name}: {score.total_score} ({score.scoring_reason})")
            except Exception as e:
                print(f"  ✗ {project.repo_full_name}: 评分失败 - {e}")
        return scores
