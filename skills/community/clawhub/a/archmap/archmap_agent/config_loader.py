import yaml
from pathlib import Path
from typing import Any

DEFAULT_CONFIGS = {
    "global_config.yaml": {
        "project_name": "",
        "source_root": "",
        "baseline_root": "./baselines",
        "mode": "full",
        "max_input_chars": 12000,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "log_level": "INFO",
    },
    "baseline_config.yaml": {
        "baseline_dir_name": "{project_name}",
        "full_index_file": "full_index.json",
        "vector_cache_file": "vector_cache.json",
        "atomic_write": True,
    },
    "recognizer_config.yaml": {
        "top_k": 5,
        "high_threshold": 0.75,
        "low_threshold": 0.45,
    },
    "worker_agent_config.yaml": {
        "granularity_check": True,
        "max_workers": 4,
    },
    "master_agent_config.yaml": {
        "mark_shared": True,
    },
    "render_config.yaml": {
        "report_templates": [
            "01_执行摘要.md",
            "02_架构图.md",
            "03_数据链路图.md",
            "04_时序图.md",
            "05_模块资产清单.md",
            "06_API资产清单.md",
            "07_存储资产清单.md",
            "08_依赖矩阵.md",
            "09_粒度校验报告.md",
        ],
    },
    "evolution_config.yaml": {
        "enable_review": True,
    },
}


class ConfigLoader:
    def __init__(self, config_root: str | Path):
        self.config_root = Path(config_root)
        self.configs: dict[str, Any] = {}

    def load_all(self) -> dict[str, Any]:
        merged = {}
        for filename, defaults in DEFAULT_CONFIGS.items():
            path = self.config_root / filename
            user = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
            user = user if isinstance(user, dict) else {}
            merged[filename.replace(".yaml", "")] = {**defaults, **user}
        self.configs = merged
        return merged

    def get(self, key: str, default: Any = None) -> Any:
        for cfg in self.configs.values():
            if key in cfg:
                return cfg[key]
        return default
