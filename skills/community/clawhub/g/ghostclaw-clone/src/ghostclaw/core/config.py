import json
from pathlib import Path
from typing import Optional, List, Dict, get_origin, get_args, Union
from pydantic import Field, field_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Optional json5 support for comments and nicer formatting
try:
    import json5
    HAS_JSON5 = True
except ImportError:
    HAS_JSON5 = False



def _load_json_or_json5(path: Path) -> dict:
    """Load a JSON or JSON5 file (JSON5 if available, fallback to stdlib json)."""
    if HAS_JSON5:
        with open(path, "r", encoding="utf-8") as f:
            return json5.load(f)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)






class OrchestratorConfig(BaseModel):
    """Configuration for the orchestrator plugin."""
    
    enabled: bool = False
    use_llm: bool = False
    llm_model: str = "openrouter/anthropic/claude-3-sonnet"
    llm_temperature: float = 0.7
    max_tokens: int = 4096
    
    vector_weight: float = 0.7
    heuristics_weight: float = 0.3
    max_plugins: int = 8
    max_concurrent_plugins: int = 4
    
    plugin_history_lookback: int = 50
    
    enable_plan_cache: bool = False
    plan_cache_ttl_hours: int = 24
    plan_cache_file: Optional[str] = None
    
    plan_only: bool = False
    report_plan_details: bool = True
    
    concurrency_limit: Optional[int] = None

    model_config = {"extra": "allow"}


class GhostclawConfig(BaseSettings):
    """
    Configuration manager for Ghostclaw.
    Resolves settings in order: CLI Flags -> Env Vars -> Local Config -> Global Config.
    """

    # AI Configuration
    use_ai: bool = Field(default=False, description="Enable Ghost Engine AI synthesis")
    ai_provider: str = Field(
        default="openrouter", description="AI Provider (openrouter, openai, anthropic)"
    )
    ai_model: Optional[str] = Field(
        default=None, description="Specific LLM model to use"
    )
    api_key: Optional[str] = Field(
        default=None, description="API Key for the selected provider (prefer env var)"
    )
    ai_temperature: float = Field(default=0.7, description="AI temperature (0.0-1.0)")
    ai_max_tokens: int = Field(default=4096, description="Max tokens for AI response")

    # Engine Integration
    use_pyscn: Optional[bool] = Field(
        default=None, description="Explicitly enable/disable PySCN integration"
    )
    use_ai_codeindex: Optional[bool] = Field(
        default=None, description="Explicitly enable/disable AI-CodeIndex integration"
    )

    # Delta-Context Mode (v0.1.10)
    delta_mode: bool = Field(
        default=False,
        description="Enable delta-context analysis (PR-style review on diffs)"
    )
    delta_base_ref: Optional[str] = Field(
        default="HEAD~1",
        description="Git reference to diff against (branch, tag, commit) when delta_mode is enabled"
    )

    # QMD Backend (v0.2.0)
    use_qmd: bool = Field(
        default=False,
        description="Use QMD (Quantum Memory Database) backend for memory operations (experimental)"
    )
    embedding_backend: str = Field(
        default="fastembed",
        description="Embedding backend for QMD hybrid search (fastembed, sentence-transformers, openai)"
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Model name for the embedding backend (sentence-transformers or openai). Fastembed uses its own default."
    )
    embedding_cache_size: int = Field(
        default=1000,
        description="Maximum number of cached query embeddings for QMD (LRU)"
    )
    embedding_cache_ttl: int = Field(
        default=3600,
        description="Embedding cache TTL in seconds (default 1 hour)"
    )
    # AI-Buff settings (Phase 3, not yet released)
    search_cache_size: int = Field(
        default=500,
        description="Maximum number of cached search results for QMD"
    )
    search_cache_ttl: int = Field(
        default=300,
        description="Search result cache TTL in seconds (default 5 minutes)"
    )
    ai_buff_enabled: bool = Field(
        default=False,
        description="Enable AI-Buff optimizations (query planning, caching) for QMD (experimental)"
    )

    # Prefetch settings (Phase 4)
    prefetch_enabled: bool = Field(
        default=True,
        description="Enable pre-fetching of likely-needed runs when ai_buff_enabled is True"
    )
    prefetch_workers: int = Field(
        default=2,
        description="Number of background threads for prefetch operations"
    )
    prefetch_window: int = Field(
        default=2,
        description="Number of adjacent runs to prefetch in sequential strategy (delta analysis)"
    )
    prefetch_hours: int = Field(
        default=24,
        description="Time window in hours for time-based prefetch strategy"
    )
    prefetch_vibe_delta: int = Field(
        default=10,
        description="Vibe score +/- delta for vibe proximity prefetch"
    )
    prefetch_stack_count: int = Field(
        default=5,
        description="Number of recent runs with matching stack to prefetch"
    )

    # Migration settings (Phase 5)
    auto_migrate: bool = Field(
        default=True,
        description="Automatically migrate legacy QMD embeddings in background"
    )
    migration_batch_size: int = Field(
        default=50,
        description="Number of reports to process per migration batch"
    )
    migration_throttle_ms: int = Field(
        default=100,
        description="Milliseconds to wait between migration batches (rate limiting)"
    )

    # Vector Index Optimization (Phase 6)
    max_chunks_per_report: Optional[int] = Field(
        default=None,
        description="Maximum chunks per report in hybrid search results (diversity limit, None = unlimited)"
    )
    vector_index: Optional[Dict] = Field(
        default=None,
        description="Vector index configuration (enabled, type, partitions, sub_vectors, training_sample_size). Example: {\"enabled\": true, \"type\": \"ivf_pq\", \"partitions\": 256, \"sub_vectors\": 64, \"training_sample_size\": 10000}"
    )

    # Analysis Behavior
    dry_run: bool = Field(
        default=False,
        description="Dry run mode: prints prompt and token count without API call",
    )
    verbose: bool = Field(
        default=False,
        description="Verbose mode: saves raw API requests/responses to debug.log",
    )
    patch: bool = Field(
        default=False,
        description="Enable refactor plan/patch suggestions from the AI engine",
    )
    show_progress: bool = Field(
        default=True, description="Show progress bar during analysis"
    )

    # Performance Tuning
    cache_enabled: bool = Field(default=True, description="Enable analysis caching")
    cache_ttl_hours: int = Field(
        default=168, description="Cache TTL in hours (default: 7 days)"
    )
    cache_compression: bool = Field(
        default=True, description="Enable compression for cached reports"
    )
    parallel_enabled: bool = Field(
        default=True, description="Enable parallel file processing"
    )
    concurrency_limit: int = Field(
        default=32, description="Max concurrent file operations"
    )
    batch_size: int = Field(default=50, description="Files per batch for processing")

    # Reliability
    retry_attempts: int = Field(
        default=3, description="Number of retry attempts for transient API failures"
    )
    retry_backoff_factor: float = Field(
        default=1.0, description="Exponential backoff factor (seconds) for retries"
    )
    retry_max_delay: float = Field(
        default=60.0, description="Maximum delay between retry attempts (seconds)"
    )

    # Plugin Management
    plugins_enabled: Optional[List[str]] = Field(
        default=None, description="List of enabled plugin names. None means all enabled."
    )

    # Orchestration (master switch)
    orchestrate: Optional[bool] = Field(
        default=None,
        description="Enable orchestrator routing via ghost-orchestrator plugin"
    )

    # Orchestrator Configuration
    orchestrator: OrchestratorConfig = Field(
        default_factory=OrchestratorConfig,
        description="Orchestrator plugin configuration (routing, LLM, weights). See documentation for options."
    )

    # Analysis Thresholds
    large_file_threshold: int = Field(
        default=300, description="Lines threshold for 'large file' detection"
    )
    max_files_to_analyze: int = Field(
        default=10000, description="Maximum files to analyze (0 = unlimited)"
    )
    exclude_patterns: List[str] = Field(
        default_factory=lambda: [
            "node_modules/",
            ".git/",
            ".ghostclaw/",
            "__pycache__/",
            "*.pyc",
            "venv/",
            ".venv/",
        ],
        description="File patterns to exclude from analysis",
    )
    include_extensions: Optional[List[str]] = Field(
        default=None,
        description="File extensions to include (default: auto-detect from stack)",
    )

    # Output Configuration
    output_format: str = Field(
        default="json", description="Output format (json, markdown, html)"
    )
    report_timestamp: bool = Field(
        default=True, description="Include timestamp in report filenames"
    )
    store_reports: bool = Field(
        default=True, description="Store reports to .ghostclaw/storage/reports/"
    )

    model_config = SettingsConfigDict(
        env_prefix="GHOSTCLAW_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def load(cls, repo_path: str, **cli_overrides) -> "GhostclawConfig":
        """
        Custom loader that merges config files before pydantic initializes.
        Merge order (lowest to highest precedence):
        1. Global Config (~/.ghostclaw/ghostclaw.json)
        2. Local Config (<repo_path>/.ghostclaw/ghostclaw.json)
        3. Environment Variables (handled by pydantic-settings)
        4. CLI overrides (passed as kwargs)
        """
        # Load and combine file configurations
        file_config = {}

        # 1. Global Config
        global_config_path = Path.home() / ".ghostclaw" / "ghostclaw.json"
        if global_config_path.exists():
            try:
                file_config.update(_load_json_or_json5(global_config_path))
            except Exception:
                pass

        # 2. Local Config
        local_config_path = Path(repo_path) / ".ghostclaw" / "ghostclaw.json"
        if local_config_path.exists():
            try:
                local_data = _load_json_or_json5(local_config_path)
            except (json.JSONDecodeError, ValueError) as e:
                # Invalid JSON/JSON5; skip local config
                local_data = None
            if local_data:
                if "api_key" in local_data and local_data["api_key"]:
                    raise ValueError(
                        "SECURITY RISK: API key found in local project configuration "
                        f"({local_config_path}). Please move it to ~/.ghostclaw/ghostclaw.json "
                        "or use the GHOSTCLAW_API_KEY environment variable to prevent committing secrets."
                    )
                file_config.update(local_data)

        # Manually apply precedence: CLI > Env > Local > Global

        default_settings = {k: v.default for k, v in cls.model_fields.items()}

        # Start with defaults
        resolved_config = default_settings.copy()

        # 1. & 2. Apply file config (Local > Global is already resolved in file_config)
        resolved_config.update(file_config)

        # 3. Apply env vars safely via os.environ
        import os

        env_prefix = cls.model_config.get("env_prefix", "")
        for k in cls.model_fields:
            env_key = f"{env_prefix}{k}".upper()
            if env_key in os.environ:
                val = os.environ[env_key]
                # Convert string to bool for boolean fields (including Optional[bool])
                annotation = cls.model_fields[k].annotation
                is_bool_type = annotation is bool or (get_origin(annotation) is Union and bool in get_args(annotation))
                if is_bool_type:
                    val = val.lower() in ("true", "1", "yes")
                resolved_config[k] = val

        # 4. CLI overrides (highest precedence)
        for k, v in cli_overrides.items():
            if v is None:
                continue
            existing = resolved_config.get(k)
            # If override is a dict and existing is a dict (or a Pydantic model), merge
            if isinstance(v, dict):
                if isinstance(existing, dict):
                    merged = {**existing, **v}
                    resolved_config[k] = merged
                elif hasattr(existing, 'model_dump') and not isinstance(existing, type):
                    # existing is a Pydantic model instance; convert to dict and merge
                    merged = {**existing.model_dump(), **v}
                    resolved_config[k] = merged
                else:
                    resolved_config[k] = v
            else:
                resolved_config[k] = v
        
        # Normalize top-level orchestrate flag into orchestrator.enabled for single source of truth
        if 'orchestrate' in resolved_config and resolved_config['orchestrate'] is not None:
            orch_val = resolved_config['orchestrate']
            orch_cfg = resolved_config.get('orchestrator')
            if orch_cfg is None:
                orch_cfg = {}
            elif hasattr(orch_cfg, 'model_dump'):
                orch_cfg = orch_cfg.model_dump()
            elif not isinstance(orch_cfg, dict):
                # Convert to dict if possible (e.g., from a model instance)
                try:
                    orch_cfg = dict(orch_cfg)
                except Exception:
                    orch_cfg = {}
            # Override enabled
            orch_cfg['enabled'] = orch_val
            resolved_config['orchestrator'] = orch_cfg

        # print(f"DEBUG: GhostclawConfig.load - resolved_config['use_ai']={resolved_config.get('use_ai')}")
        return cls(**resolved_config)
