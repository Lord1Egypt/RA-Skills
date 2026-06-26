from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from pathlib import Path
import json


def get_default_anchor_keys() -> List[str]:
    return ["人设", "世界观", "核心剧情", "文风"]


class ChunkerConfig(BaseModel):
    chunk_size: int = Field(default=1000, description="文本块大小")
    chunk_overlap: int = Field(default=100, description="文本块重叠大小")
    separators: List[str] = Field(
        default=["\n\n", "\n", "。", "！", "？", "，", " "],
        description="文本分割分隔符优先级"
    )


class EmbeddingConfig(BaseModel):
    model_name: str = Field(default="all-MiniLM-L6-v2", description="嵌入模型名称")
    cache_size: int = Field(default=1000, description="嵌入缓存大小")
    cache_ttl: int = Field(default=3600, description="缓存过期时间(秒)")


class ConsistencyConfig(BaseModel):
    threshold: float = Field(default=0.7, description="一致性阈值")
    character_weight: float = Field(default=0.35, description="人设权重")
    plot_weight: float = Field(default=0.30, description="剧情权重")
    style_weight: float = Field(default=0.20, description="文风权重")
    world_weight: float = Field(default=0.15, description="世界观权重")


class WindowConfig(BaseModel):
    max_window_size: int = Field(default=4000, description="滑动窗口最大token数")
    overlap_size: int = Field(default=500, description="窗口重叠大小")
    min_chunk_size: int = Field(default=200, description="最小分块大小")
    max_windows: int = Field(default=20, description="最大窗口数量")


class HistoryConfig(BaseModel):
    max_history: int = Field(default=100, description="最大历史记录数")
    auto_save: bool = Field(default=False, description="是否自动保存")
    save_path: Optional[str] = Field(default=None, description="保存路径")


class PromptConfig(BaseModel):
    template: str = Field(
        default="""请根据以下需求和上下文，续写/创作文本，严格遵守核心设定，保持文风一致：

【用户需求】
{user_prompt}

{relevant_context}
{anchor_prompt}

要求：1. 剧情连贯，不偏离核心设定；2. 人设统一，无矛盾；3. 文风与前文一致。""",
        description="提示词模板"
    )
    max_context_length: int = Field(default=3000, description="最大上下文长度")


class ContextConfig(BaseModel):
    chunker: ChunkerConfig = Field(default_factory=ChunkerConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    consistency: ConsistencyConfig = Field(default_factory=ConsistencyConfig)
    window: WindowConfig = Field(default_factory=WindowConfig)
    history: HistoryConfig = Field(default_factory=HistoryConfig)
    prompt: PromptConfig = Field(default_factory=PromptConfig)

    anchor_keys: List[str] = Field(default_factory=get_default_anchor_keys)

    debug_mode: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")

    class Config:
        extra = "allow"

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextConfig":
        return cls(**data)

    def save_to_file(self, filepath: str):
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> "ContextConfig":
        path = Path(filepath)
        if not path.exists():
            return cls()

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def update(self, **kwargs) -> "ContextConfig":
        data = self.to_dict()
        for key, value in kwargs.items():
            if '.' in key:
                parts = key.split('.')
                current = data
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                data[key] = value
        return ContextConfig.from_dict(data)


config = ContextConfig()
