"""
配置设置模块

Infrastructure 层的配置加载功能。
遵循 OpenClaw SecretRef 规范进行密钥管理，不支持直接读取环境变量。

架构原则：
- 所有敏感配置必须通过 SecretRef 注入
- Domain 层不直接导入 settings，配置通过 Application 层注入
- 符合 ClawHub 安全规范，避免被标记为危险
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union

from ..llm.config import LLMConfig
from .secret_ref import SecretRefResolver

# ==================== 路径默认值 ====================
DEFAULT_DOCUMENT_PATH = Path("./documents")
DEFAULT_OUTPUT_DIR = Path("./output")


# ==================== OCR 默认值 ====================
DEFAULT_OCR_BACKEND = "none"


@dataclass
class CheckerConfig:
    """
    检查器配置数据类

    从环境变量或 SecretRef 加载配置，传递给 Domain 层检查器。
    遵循『Domain 层不能直接 import settings』的架构原则。

    Attributes:
        similarity_threshold: 语义匹配相似度阈值
        use_semantic: 是否启用语义匹配
        project_period: 项目周期（用于时效性检查）
        visual_enabled: 是否启用视觉检查
        visual_confidence_threshold: 视觉检测置信度阈值
        visual_default_check_type: 默认视觉检查类型
        llm_config: LLM 配置
        embed_api_key: 嵌入模型 API 密钥
        embed_base_url: 嵌入模型 API 端点
        embed_model: 嵌入模型名称
        embed_timeout: 嵌入模型请求超时
        embed_max_retries: 嵌入模型最大重试次数
        secret_providers: SecretRef 提供者配置
    """

    # 完整性检查器配置
    similarity_threshold: float = 0.75
    use_semantic: bool = True

    # 时效性检查器配置
    project_period: Optional[Dict[str, str]] = None

    # 视觉检查器配置
    visual_enabled: bool = True
    visual_confidence_threshold: float = 0.7
    visual_default_check_type: str = "both"

    # 视觉模型配置（用于印章/签名检测，可选，默认使用 LLM 配置）
    vision_api_key: Optional[str] = None
    vision_base_url: Optional[str] = None
    vision_model: str = "qwen3-vl-flash"

    # LLM 配置
    llm_config: LLMConfig = field(default_factory=lambda: LLMConfig(api_key=""))

    # 嵌入模型配置（用于语义匹配）
    embed_api_key: Optional[str] = None
    embed_base_url: Optional[str] = None
    embed_model: str = "text-embedding-v1"
    embed_timeout: float = 30.0
    embed_max_retries: int = 3

    # OCR 配置
    ocr_backend: str = "none"

    # PDF 转换器配置
    pdf_zoom_factor: float = 2.0  # PDF 渲染缩放因子，影响印章清晰度

    # RAG 配置（时效性检查有效期提取）
    rag_enabled: bool = True                       # 是否启用 Micro-RAG
    rag_chunk_size: int = 200                      # 分块字符数
    rag_chunk_overlap: int = 50                    # 相邻分块重叠字符数
    rag_top_k: int = 2                             # 返回最高分 Chunk 数量
    rag_circuit_breaker_threshold: float = 0.25   # 燃断阈値，全部得分小于此値时跳过 LLM

    # SecretRef 提供者配置
    secret_providers: Optional[Dict[str, Any]] = None

    @classmethod
    def from_secret_ref(
        cls,
        secret_providers: Optional[Dict[str, Any]] = None,
        secrets: Optional[Dict[str, Union[str, Dict]]] = None
    ) -> "CheckerConfig":
        """
        从 SecretRef 创建配置

        所有敏感配置必须通过 SecretRef 传入，符合 ClawHub 安全规范。
        非敏感配置使用默认值，也可通过 secrets 字典传入普通字符串。

        Args:
            secret_providers: SecretRef 提供者配置
            secrets: 密钥配置字典，值可以是普通字符串或 SecretRef 对象
                例如: {"llm_api_key": {"source": "env", "provider": "default", "id": "LLM_API_KEY"}}
                或: {"llm_model": "gpt-4o"}  # 普通字符串值

        Returns:
            CheckerConfig 实例

        Raises:
            ValueError: 当必需的配置项未提供时
        """
        secrets = secrets or {}
        
        # 创建 SecretRef 解析器
        resolver = SecretRefResolver(secret_providers)
        
        # 辅助函数：解析值（支持 SecretRef 和普通字符串）
        def resolve_value(key: str, default: str = "") -> str:
            """从 secrets 字典解析值"""
            if key in secrets:
                value = resolver.resolve(secrets[key])
                if value is not None:
                    return value
            return default
        
        # 必需的配置项
        llm_api_key = resolve_value("llm_api_key")
        if not llm_api_key:
            raise ValueError("llm_api_key is required. Provide it via secrets dict with SecretRef or plain string.")
        
        # LLM 配置
        llm_config = LLMConfig(
            api_key=llm_api_key,
            base_url=resolve_value("llm_base_url", "https://api.openai.com/v1"),
            model=resolve_value("llm_model", "gpt-4o"),
            timeout=int(resolve_value("llm_timeout", "60")),
            max_retries=int(resolve_value("llm_max_retries", "3")),
            system_prompt="你是一个专业的合规审查清单生成助手。",
        )

        # 嵌入模型配置（优先使用专用配置，否则使用 LLM 配置）
        embed_api_key = resolve_value("embed_api_key") or llm_api_key
        embed_base_url = resolve_value("embed_base_url") or llm_config.base_url
        embed_model = resolve_value("embed_model", "text-embedding-v1")

        # 视觉模型配置（优先使用专用配置，否则使用 LLM 配置）
        vision_api_key = resolve_value("vision_api_key") or llm_api_key
        vision_base_url = resolve_value("vision_base_url") or llm_config.base_url
        vision_model = resolve_value("vision_model", "qwen3-vl-flash")

        return cls(
            similarity_threshold=float(resolve_value("similarity_threshold", "0.75")),
            use_semantic=resolve_value("use_semantic", "true").lower() == "true",
            visual_enabled=resolve_value("visual_enabled", "true").lower() == "true",
            visual_confidence_threshold=float(resolve_value("visual_confidence_threshold", "0.7")),
            visual_default_check_type=resolve_value("visual_check_type", "both"),
            llm_config=llm_config,
            embed_api_key=embed_api_key if embed_api_key else None,
            embed_base_url=embed_base_url if embed_base_url else None,
            embed_model=embed_model,
            vision_api_key=vision_api_key if vision_api_key else None,
            vision_base_url=vision_base_url if vision_base_url else None,
            vision_model=vision_model,
            ocr_backend=resolve_value("ocr_backend", "none"),
            pdf_zoom_factor=float(resolve_value("pdf_zoom_factor", "2.0")),
            rag_enabled=resolve_value("rag_enabled", "true").lower() == "true",
            rag_chunk_size=int(resolve_value("rag_chunk_size", "200")),
            rag_chunk_overlap=int(resolve_value("rag_chunk_overlap", "50")),
            rag_top_k=int(resolve_value("rag_top_k", "2")),
            rag_circuit_breaker_threshold=float(
                resolve_value("rag_circuit_breaker_threshold", "0.25")
            ),
            secret_providers=secret_providers,
        )


def generate_output_path(project_id: str, output_dir: Optional[Path] = None) -> Path:
    """
    生成报告输出路径

    Args:
        project_id: 项目标识符
        output_dir: 输出目录，默认为 DEFAULT_OUTPUT_DIR

    Returns:
        输出文件的 Path 对象
    """
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"compliance_report_{project_id}.pdf"


def scan_default_documents(doc_path: Optional[Path] = None) -> List[str]:
    """
    扫描默认文档目录

    Args:
        doc_path: 文档目录路径，默认为 DEFAULT_DOCUMENT_PATH

    Returns:
        文档文件路径列表
    """
    doc_path = doc_path or DEFAULT_DOCUMENT_PATH

    if not doc_path.exists():
        return []

    supported_extensions = {".pdf", ".docx", ".doc"}
    document_paths = []

    for ext in supported_extensions:
        for file_path in doc_path.glob(f"*{ext}"):
            if file_path.is_file():
                document_paths.append(str(file_path))

    return sorted(document_paths)


def get_ocr_backend(ocr_backend: Optional[str] = None) -> str:
    """
    获取 OCR 后端类型

    Args:
        ocr_backend: OCR 后端类型，默认为 DEFAULT_OCR_BACKEND

    Returns:
        OCR 后端类型: "none", "paddle", "aliyun"
    """
    return ocr_backend or DEFAULT_OCR_BACKEND


def get_aliyun_ocr_credentials(
    access_key_id: Optional[str] = None,
    access_key_secret: Optional[str] = None
) -> Optional[Tuple[str, str]]:
    """
    获取阿里云 OCR 凭证

    Args:
        access_key_id: Access Key ID
        access_key_secret: Access Key Secret

    Returns:
        (access_key_id, access_key_secret) 元组，未配置则返回 None
    """
    if access_key_id and access_key_secret:
        return (access_key_id, access_key_secret)
    return None
