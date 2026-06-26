"""Builder Agent 설정 관리"""

import os
import re
import logging
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class FeaturesConfig:
    """Feature Flags 설정"""
    adaptive_scoring: bool = True
    checkpoint_resume: bool = True
    coverage_validation: bool = True
    spec_validation: bool = True
    dynamic_templates: bool = True
    parallel_builds: bool = False
    multi_agent: bool = False
    continuous_learning: bool = True


@dataclass
class GithubDiscoveryConfig:
    enabled: bool = True
    method: str = "browser"
    language: str = "python"
    max_results: int = 5


@dataclass
class CveDiscoveryConfig:
    enabled: bool = True
    lookback_days: int = 7
    min_score: float = 7.0
    severity: str = "HIGH"
    max_results: int = 20


@dataclass
class SecurityNewsConfig:
    enabled: bool = True
    keywords: List[str] = field(default_factory=lambda: [
        'ransomware', 'vulnerability', 'malware', 'phishing',
        'zero-day', 'supply-chain'
    ])


@dataclass
class DiscoveryConfig:
    output_dir: str = "/tmp/builder-discovery"
    cache_ttl_seconds: int = 3600
    github: GithubDiscoveryConfig = field(default_factory=GithubDiscoveryConfig)
    cve: CveDiscoveryConfig = field(default_factory=CveDiscoveryConfig)
    security_news: SecurityNewsConfig = field(default_factory=SecurityNewsConfig)


@dataclass
class CorrectionConfig:
    max_retries: int = 3
    test_timeout_seconds: int = 30
    acp_mode: str = "direct"


@dataclass
class OrchestrationConfig:
    simple_engine: str = "glm"
    medium_engine: str = "claude"
    complex_engine: str = "claude"
    claude_timeout_seconds: int = 300


@dataclass
class NotionConfig:
    database_id: str = ""
    max_queue_per_run: int = 10
    rate_limit_seconds: float = 0.5


@dataclass
class LoggingConfig:
    level: str = "INFO"
    file: str = "/tmp/builder-agent/builder.log"


@dataclass
class Config:
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    correction: CorrectionConfig = field(default_factory=CorrectionConfig)
    orchestration: OrchestrationConfig = field(default_factory=OrchestrationConfig)
    notion: NotionConfig = field(default_factory=NotionConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    features: FeaturesConfig = field(default_factory=FeaturesConfig)
    github: GithubDiscoveryConfig = field(default_factory=GithubDiscoveryConfig)  # Legacy support


def _resolve_env_vars(value: str) -> str:
    """${VAR_NAME} 패턴을 환경 변수 값으로 치환"""
    def replacer(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))
    return re.sub(r'\$\{(\w+)\}', replacer, value)


def _resolve_dict(data: dict) -> dict:
    """딕셔너리 내 모든 문자열의 환경 변수를 치환"""
    resolved = {}
    for key, value in data.items():
        if isinstance(value, str):
            resolved[key] = _resolve_env_vars(value)
        elif isinstance(value, dict):
            resolved[key] = _resolve_dict(value)
        elif isinstance(value, list):
            resolved[key] = [
                _resolve_env_vars(v) if isinstance(v, str) else v
                for v in value
            ]
        else:
            resolved[key] = value
    return resolved


def _dict_to_dataclass(cls, data: dict):
    """딕셔너리를 dataclass로 변환 (nested 지원)"""
    if not data:
        return cls()

    field_types = {f.name: f.type for f in cls.__dataclass_fields__.values()}
    kwargs = {}

    for key, value in data.items():
        if key not in field_types:
            continue
        field_type = field_types[key]

        # nested dataclass 처리
        if isinstance(value, dict) and hasattr(field_type, '__dataclass_fields__'):
            kwargs[key] = _dict_to_dataclass(field_type, value)
        else:
            kwargs[key] = value

    return cls(**kwargs)


def load_config(config_path: Optional[str] = None) -> Config:
    """설정 파일 로드"""
    if config_path is None:
        config_path = str(
            Path(__file__).parent / "config.yaml"
        )

    config_file = Path(config_path)

    if not config_file.exists():
        return Config()

    raw_text = config_file.read_text()

    if HAS_YAML:
        raw_data = yaml.safe_load(raw_text)
    else:
        # YAML 파서 없을 경우 JSON fallback 시도
        try:
            raw_data = json.loads(raw_text)
        except json.JSONDecodeError:
            logging.warning("PyYAML not installed and config is not JSON. Using defaults.")
            return Config()

    if not raw_data:
        return Config()

    resolved = _resolve_dict(raw_data)

    config = Config()
    if 'discovery' in resolved:
        config.discovery = _dict_to_dataclass(DiscoveryConfig, resolved['discovery'])
    if 'correction' in resolved:
        config.correction = _dict_to_dataclass(CorrectionConfig, resolved['correction'])
    if 'orchestration' in resolved:
        config.orchestration = _dict_to_dataclass(OrchestrationConfig, resolved['orchestration'])
    if 'notion' in resolved:
        config.notion = _dict_to_dataclass(NotionConfig, resolved['notion'])
    if 'logging' in resolved:
        config.logging = _dict_to_dataclass(LoggingConfig, resolved['logging'])
    if 'features' in resolved:
        config.features = _dict_to_dataclass(FeaturesConfig, resolved['features'])

    return config


def setup_logging(config: Config) -> logging.Logger:
    """구조화된 로깅 설정"""
    log_logger = logging.getLogger('builder-agent')
    log_logger.setLevel(getattr(logging, config.logging.level, logging.INFO))

    # 이미 핸들러가 있으면 중복 추가하지 않음
    if log_logger.handlers:
        return log_logger

    # 콘솔 핸들러
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        datefmt='%H:%M:%S'
    ))
    log_logger.addHandler(console)

    # 파일 핸들러
    log_file = Path(config.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(str(log_file), encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    ))
    log_logger.addHandler(file_handler)

    return log_logger
