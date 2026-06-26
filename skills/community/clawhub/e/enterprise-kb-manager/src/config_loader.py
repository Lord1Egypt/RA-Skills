"""
Configuration loader for Enterprise Knowledge Base Skill
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class KnowledgeBaseConfig:
    """Configuration for Enterprise Knowledge Base"""
    
    # Embedding settings
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: Optional[str] = None
    embedding_provider: str = "openai"
    embedding_base_url: Optional[str] = None
    
    # Chunking settings
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # Retrieval settings
    retrieval_top_k: int = 5
    
    # Milvus settings - 使用系统配置
    milvus_uri: str = ""
    collection_name: str = "enterprise_kb"
    vector_dimension: int = 1536
    metric_type: str = "COSINE"
    
    # Paths - 使用系统配置
    documents_dir: str = ""
    
    # Validation errors
    _errors: list = field(default_factory=list, repr=False)
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        self._errors = []
        
        if self.chunk_size <= 0:
            self._errors.append("chunk_size must be greater than 0")
        
        if self.chunk_overlap < 0:
            self._errors.append("chunk_overlap must be non-negative")
        
        if self.chunk_overlap >= self.chunk_size:
            self._errors.append("chunk_overlap must be less than chunk_size")
        
        if self.retrieval_top_k <= 0:
            self._errors.append("retrieval_top_k must be greater than 0")
        
        # milvus_uri 现在可以为空，会自动使用系统配置
        
        if self.vector_dimension <= 0:
            self._errors.append("vector_dimension must be greater than 0")
        
        valid_metric_types = ["L2", "IP", "COSINE"]
        if self.metric_type not in valid_metric_types:
            self._errors.append(f"metric_type must be one of {valid_metric_types}")
        
        return len(self._errors) == 0
    
    @property
    def errors(self) -> list:
        """Get validation errors"""
        return self._errors


class ConfigLoader:
    """Load and merge configuration from multiple sources"""
    
    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            self.skill_dir = Path(__file__).parent.parent
        else:
            self.skill_dir = Path(skill_dir)
        
        self.default_config_path = self.skill_dir / "config.json"
    
    def load(self) -> KnowledgeBaseConfig:
        """Load configuration from all sources"""
        config_dict = self._load_default_config()
        
        openclaw_config = self._load_openclaw_config()
        if openclaw_config:
            config_dict.update(openclaw_config)
        
        env_config = self._load_env_config()
        config_dict.update(env_config)
        
        config = self._dict_to_config(config_dict)
        
        if not config.validate():
            error_msg = "Configuration validation failed:\n" + "\n".join(
                f"  - {error}" for error in config.errors
            )
            raise ValueError(error_msg)
        
        return config
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration from config.json"""
        if not self.default_config_path.exists():
            return {}
        
        try:
            with open(self.default_config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load default config: {e}")
            return {}
    
    def _load_openclaw_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from OpenClaw's openclaw.json"""
        openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
        
        if not openclaw_config_path.exists():
            return None
        
        try:
            with open(openclaw_config_path, 'r', encoding='utf-8') as f:
                openclaw_data = json.load(f)
            
            config = (
                openclaw_data
                .get("skills", {})
                .get("entries", {})
                .get("kb-manager", {})
                .get("config", {})
            )
            
            return config if config else None
        
        except Exception as e:
            print(f"Warning: Failed to load OpenClaw config: {e}")
            return None
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}
        
        # API Keys
        if "OPENAI_API_KEY" in os.environ:
            config["embeddingApiKey"] = os.environ["OPENAI_API_KEY"]
        
        if "DASHSCOPE_API_KEY" in os.environ:
            config["embeddingApiKey"] = os.environ["DASHSCOPE_API_KEY"]
        
        if "MILVUS_URI" in os.environ:
            config["milvusUri"] = os.environ["MILVUS_URI"]
        
        return config
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> KnowledgeBaseConfig:
        """Convert dictionary to KnowledgeBaseConfig"""
        key_mapping = {
            "embeddingModel": "embedding_model",
            "embeddingApiKey": "embedding_api_key",
            "embeddingProvider": "embedding_provider",
            "embeddingBaseUrl": "embedding_base_url",
            "chunkSize": "chunk_size",
            "chunkOverlap": "chunk_overlap",
            "retrievalTopK": "retrieval_top_k",
            "milvusUri": "milvus_uri",
            "collectionName": "collection_name",
            "vectorDimension": "vector_dimension",
            "metricType": "metric_type",
            "documentsDir": "documents_dir",
        }
        
        python_dict = {}
        for key, value in config_dict.items():
            python_key = key_mapping.get(key, key)
            python_dict[python_key] = value
        
        return KnowledgeBaseConfig(**python_dict)


def load_config(skill_dir: Optional[Path] = None) -> KnowledgeBaseConfig:
    """Convenience function to load configuration"""
    loader = ConfigLoader(skill_dir)
    config = loader.load()
    
    # 如果documents_dir为空，使用系统配置
    if not config.documents_dir:
        try:
            from .system_config import load_system_config
            system_config = load_system_config()
            config.documents_dir = system_config.documents_path
        except Exception as e:
            print(f"⚠️ 无法加载系统配置: {e}")
            # 使用默认路径作为后备
            config.documents_dir = "./documents"
    
    return config


if __name__ == "__main__":
    try:
        config = load_config()
        print("✅ Configuration loaded successfully!")
        print(f"\nConfiguration:")
        print(f"  Embedding Model: {config.embedding_model}")
        print(f"  Chunk Size: {config.chunk_size}")
        print(f"  Chunk Overlap: {config.chunk_overlap}")
        print(f"  Retrieval Top-K: {config.retrieval_top_k}")
        print(f"  Milvus URI: 系统自动配置")
        print(f"  Collection: {config.collection_name}")
        print(f"  Vector Dimension: {config.vector_dimension}")
        print(f"  Metric Type: {config.metric_type}")
    except ValueError as e:
        print(f"❌ Configuration error:\n{e}")
