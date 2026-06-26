"""统一配置加载 - 从 .env 文件和环境变量读取所有配置"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class GitHubConfig:
    token: str = ""
    search_queries: list[str] = field(default_factory=lambda: [
        "AI agent framework stars:>100 pushed:>2025-01-01",
        "multi-agent LLM stars:>50 pushed:>2025-01-01",
        "autonomous agent tool-use stars:>50 pushed:>2025-01-01",
        "LLM orchestration agent stars:>30 pushed:>2025-01-01",
        "agentic workflow stars:>30 pushed:>2025-01-01",
    ])
    watch_orgs: list[str] = field(default_factory=lambda: [
        "langchain-ai", "microsoft", "openai", "anthropics",
        "crewAIInc", "thunlp", "modelscope",
    ])
    max_results_per_query: int = 30
    recent_days: int = 30


@dataclass
class LLMConfig:
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096


@dataclass
class ImageConfig:
    api_key: str = ""
    base_url: str = "https://api.siliconflow.cn/v1"
    model: str = "black-forest-labs/FLUX.1-schnell"
    size: str = "1024x1024"
    style_prefix: str = "flat illustration, tech style, minimalist, "


@dataclass
class ScoreWeights:
    novelty: float = 0.30
    practicality: float = 0.30
    content_fit: float = 0.25
    ease_of_use: float = 0.15


@dataclass
class AppConfig:
    github: GitHubConfig = field(default_factory=GitHubConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    image: ImageConfig = field(default_factory=ImageConfig)
    weights: ScoreWeights = field(default_factory=ScoreWeights)
    topk_size: int = 20
    present_top_n: int = 3
    db_path: str = ""
    output_dir: str = ""

    def __post_init__(self):
        if not self.db_path:
            self.db_path = str(PROJECT_ROOT / "data" / "agentscout.db")
        if not self.output_dir:
            self.output_dir = str(PROJECT_ROOT / "output")


def load_config() -> AppConfig:
    """从环境变量加载配置"""
    config = AppConfig(
        github=GitHubConfig(
            token=os.getenv("GITHUB_TOKEN", ""),
        ),
        llm=LLMConfig(
            api_key=os.getenv("LLM_API_KEY", ""),
            base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
            model=os.getenv("LLM_MODEL", "gpt-4o"),
        ),
        image=ImageConfig(
            api_key=os.getenv("IMAGE_API_KEY", ""),
            base_url=os.getenv("IMAGE_BASE_URL", "https://api.siliconflow.cn/v1"),
            model=os.getenv("IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell"),
            size=os.getenv("IMAGE_SIZE", "1024x1024"),
            style_prefix=os.getenv("IMAGE_STYLE", "flat illustration, tech style, minimalist, "),
        ),
        weights=ScoreWeights(
            novelty=float(os.getenv("SCORE_WEIGHT_NOVELTY", "0.3")),
            practicality=float(os.getenv("SCORE_WEIGHT_PRACTICALITY", "0.3")),
            content_fit=float(os.getenv("SCORE_WEIGHT_CONTENT_FIT", "0.25")),
            ease_of_use=float(os.getenv("SCORE_WEIGHT_EASE", "0.15")),
        ),
        topk_size=int(os.getenv("TOPK_SIZE", "20")),
        present_top_n=int(os.getenv("PRESENT_TOP_N", "3")),
    )
    return config
