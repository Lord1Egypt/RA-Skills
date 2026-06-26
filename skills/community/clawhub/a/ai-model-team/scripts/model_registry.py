"""
Model Registry
P2: Model versioning, training data range, feature signatures
"""
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# ============ Configuration ============
MODEL_REGISTRY_PATH = Path(__file__).parent.parent / "model_registry.json"


@dataclass
class ModelVersion:
    """模型版本记录"""
    model_name: str
    version: str
    model_type: str  # timeseries/sentiment/hybrid
    trained_data_range: str  # e.g., "2020-01-01 to 2024-12-31"
    features_used: List[str]
    feature_signature: str  # hash of features
    metrics: Dict[str, float]  # validation metrics
    created_at: str
    created_by: str
    status: str  # active/deprecated/retired
    path: str
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ModelRegistry:
    """模型注册表"""
    
    def __init__(self, registry_path: str = None):
        self.registry_path = Path(registry_path) if registry_path else MODEL_REGISTRY_PATH
        self.models: Dict[str, List[ModelVersion]] = {}  # model_name -> versions
        self._load()
    
    def _load(self):
        """从文件加载注册表"""
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                data = json.load(f)
                for model_name, versions in data.items():
                    self.models[model_name] = [
                        ModelVersion(**v) for v in versions
                    ]
    
    def _save(self):
        """保存注册表到文件"""
        data = {
            model_name: [v.to_dict() for v in versions]
            for model_name, versions in self.models.items()
        }
        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def compute_feature_signature(features: List[str]) -> str:
        """计算特征签名"""
        features_sorted = sorted(features)
        content = "|".join(features_sorted)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def register(
        self,
        model_name: str,
        version: str,
        model_type: str,
        trained_data_range: str,
        features: List[str],
        metrics: Dict[str, float],
        created_by: str = "system",
        status: str = "active",
        path: str = ""
    ) -> ModelVersion:
        """注册新模型版本"""
        record = ModelVersion(
            model_name=model_name,
            version=version,
            model_type=model_type,
            trained_data_range=trained_data_range,
            features=features,
            feature_signature=self.compute_feature_signature(features),
            metrics=metrics,
            created_at=datetime.now(timezone.utc).isoformat(),
            created_by=created_by,
            status=status,
            path=path
        )
        
        if model_name not in self.models:
            self.models[model_name] = []
        
        # 检查是否已存在
        existing = [v for v in self.models[model_name] if v.version == version]
        if existing:
            # 更新
            idx = self.models[model_name].index(existing[0])
            self.models[model_name][idx] = record
        else:
            self.models[model_name].append(record)
        
        self._save()
        return record
    
    def get_active(self, model_name: str) -> Optional[ModelVersion]:
        """获取活跃版本"""
        if model_name not in self.models:
            return None
        active = [v for v in self.models[model_name] if v.status == "active"]
        return active[0] if active else None
    
    def get_all_versions(self, model_name: str) -> List[ModelVersion]:
        """获取所有版本"""
        return self.models.get(model_name, [])
    
    def deprecate(self, model_name: str, version: str, reason: str = ""):
        """弃用模型版本"""
        if model_name not in self.models:
            return
        
        for v in self.models[model_name]:
            if v.version == version:
                v.status = "deprecated"
                if v.metadata is None:
                    v.metadata = {}
                v.metadata["deprecated_reason"] = reason
                v.metadata["deprecated_at"] = datetime.now(timezone.utc).isoformat()
        
        self._save()
    
    def get_summary(self) -> Dict:
        """获取注册表摘要"""
        summary = {}
        for model_name, versions in self.models.items():
            active = [v for v in versions if v.status == "active"]
            summary[model_name] = {
                "total_versions": len(versions),
                "active_version": active[0].version if active else None,
                "types": list(set(v.model_type for v in versions))
            }
        return summary


# Global registry
_registry: Optional[ModelRegistry] = None

def get_model_registry() -> ModelRegistry:
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry


def register_default_models():
    """注册默认模型"""
    registry = get_model_registry()
    
    # Kronos
    registry.register(
        model_name="kronos-base",
        version="v1.0.0",
        model_type="timeseries",
        trained_data_range="2018-01-01 to 2024-06-30",
        features=["close", "open", "high", "low", "vol", "ohlc_patterns"],
        metrics={"val_accuracy": 0.72, "directional_accuracy": 0.68},
        created_by="neoquasar",
        path="~/.agents/skills/ai-hedge-fund-skill/models/kronos-base"
    )
    
    # TimesFM
    registry.register(
        model_name="timesfm-2.5-200m",
        version="v2.5.0",
        model_type="timeseries",
        trained_data_range="1950-01-01 to 2023-12-31",
        features=["numeric_timeseries"],
        metrics={"mae": 0.12, "mase": 0.85},
        created_by="google",
        path="google/timesfm-2.5-200m-pytorch"
    )
    
    # Chronos-2
    registry.register(
        model_name="chronos-2",
        version="v2.0.0",
        model_type="timeseries",
        trained_data_range="Multi-domain training",
        features=["numeric_timeseries", "quantile_predictions"],
        metrics={"coverage_90": 0.91},
        created_by="amazon",
        path="amazon/chronos-2"
    )
    
    # FinBERT
    registry.register(
        model_name="finbert-sentiment",
        version="v1.0.0",
        model_type="sentiment",
        trained_data_range="Financial news corpus",
        features=["text", "financial_sentiment"],
        metrics={"accuracy": 0.75, "f1": 0.73},
        created_by="prosusai",
        path="ProsusAI/finbert"
    )
    
    return registry
