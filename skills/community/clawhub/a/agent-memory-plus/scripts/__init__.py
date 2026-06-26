"""
Agent Memory System - Scripts Package

为智能体提供记忆能力的核心基础设施
"""

__version__ = "2.1.0"

# 核心模块
from .types import *
from .perception import PerceptionMemoryStore
from .short_term import SemanticBucket, ShortTermMemoryManager, AsynchronousExtractor
from .short_term_insight import (
    TopicCluster,
    TopicRelation,
    ExtractionDecision,
    ShortTermInsightResult,
    ShortTermInsightAnalyzer,
)
from .long_term import LongTermMemoryManager
from .context_reconstructor import (
    QualityEvaluator,
    WeightAdapter,
    ContextReconstructor,
)
from .insight_module import InsightPool, DetachedObserver, InsightModule
from .state_capture import GlobalStateCapture
from .heat_manager import HeatManager
from .conflict_resolver import ConflictResolver
from .privacy import (
    ConsentStatus,
    DataSensitivity,
    StoragePolicy,
    RetentionPeriod,
    ConsentRecord,
    PrivacyConfig,
    DataClassification,
    PrivacyAuditLog,
    SensitiveDataDetector,
    PrivacyManager,
    PRIVACY_NOTICE_TEMPLATE,
)
from .encryption import (
    EncryptedData,
    KeyInfo,
    EncryptionConfig,
    KeyManager,
    DataEncryptor,
    EncryptedFileStorage,
    encrypt_data_with_password,
    decrypt_data_with_password,
    generate_encryption_key,
    CRYPTO_AVAILABLE,
)
from .memory_index import (
    TextProcessor,
    MemoryIndexer,
    MemoryDocument,
    SearchResult,
    IndexStats,
)
from .incremental_sync import (
    SyncStatus,
    SyncState,
    ExtractionRecord,
    SyncStats,
    IncrementalSync,
)
from .credential_manager import (
    CredentialRecord,
    CredentialStorage,
    CredentialManager,
    create_credential_manager,
)
from .chain_reasoning import (
    ChainReasoningEnhancer,
    create_chain_reasoning_enhancer,
)

__all__ = [
    # 类型
    "types",
    # 感知记忆
    "PerceptionMemoryStore",
    # 短期记忆
    "SemanticBucket",
    "ShortTermMemoryManager",
    "AsynchronousExtractor",
    # 短期记忆洞察
    "TopicCluster",
    "TopicRelation",
    "ExtractionDecision",
    "ShortTermInsightResult",
    "ShortTermInsightAnalyzer",
    # 长期记忆
    "LongTermMemoryManager",
    # 上下文重构
    "QualityEvaluator",
    "WeightAdapter",
    "ContextReconstructor",
    # 洞察模块
    "InsightPool",
    "DetachedObserver",
    "InsightModule",
    # 状态捕捉
    "GlobalStateCapture",
    # 冷热度管理
    "HeatManager",
    # 冲突解决
    "ConflictResolver",
    # 隐私配置
    "ConsentStatus",
    "DataSensitivity",
    "StoragePolicy",
    "RetentionPeriod",
    "ConsentRecord",
    "PrivacyConfig",
    "DataClassification",
    "PrivacyAuditLog",
    "SensitiveDataDetector",
    "PrivacyManager",
    "PRIVACY_NOTICE_TEMPLATE",
    # 加密模块
    "EncryptedData",
    "KeyInfo",
    "EncryptionConfig",
    "KeyManager",
    "DataEncryptor",
    "EncryptedFileStorage",
    "encrypt_data_with_password",
    "decrypt_data_with_password",
    "generate_encryption_key",
    "CRYPTO_AVAILABLE",
    # 记忆索引
    "TextProcessor",
    "MemoryIndexer",
    "MemoryDocument",
    "SearchResult",
    "IndexStats",
    # 增量同步
    "SyncStatus",
    "SyncState",
    "ExtractionRecord",
    "SyncStats",
    "IncrementalSync",
    # 凭证管理
    "CredentialRecord",
    "CredentialStorage",
    "CredentialManager",
    "create_credential_manager",
    # 链式推理增强
    "ChainReasoningEnhancer",
    "create_chain_reasoning_enhancer",
]
