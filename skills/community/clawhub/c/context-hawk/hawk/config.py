"""
config.py — hawk 配置管理

功能：
- 从环境变量 / openclaw.json 读取配置
- 提供配置热重载
"""

import os
import json


# ─── All tunable constants ────────────────────────────────────────────────────
#
# Override via environment variables or ~/.hawk/config.json
#
# Env var format: HAWK_* (uppercase, underscore-separated)
# e.g. HAWK_DECAY_RATE=0.9
#
# ─── Memory / Decay ─────────────────────────────────────────────────────────

DECAY_RATE = float(os.environ.get('HAWK_DECAY_RATE', '0.95'))
"""
Daily importance decay multiplier for idle memories.
Range: 0.8–0.99. Default 0.95.
- Higher (e.g. 0.98) = memories fade slowly, better for frequent-use agents
- Lower (e.g. 0.9)  = memories fade quickly, better for low-frequency agents
Tradeoff: slow decay risks stale memories staying relevant; fast decay risks losing useful context.
"""

WORKING_TTL_DAYS = int(os.environ.get('HAWK_WORKING_TTL_DAYS', '1'))
"""
Max days a memory stays in 'working' layer before decaying to 'short'.
Default 1. Short tasks / conversations should use 0–1.
"""

SHORT_TTL_DAYS = int(os.environ.get('HAWK_SHORT_TTL_DAYS', '7'))
"""
Days before short-layer memory importance decays toward working.
Default 7. Balance between memory retention and context bloat.
"""

LONG_TTL_DAYS = int(os.environ.get('HAWK_LONG_TTL_DAYS', '90'))
"""
Days before long-layer memory is considered for archive promotion.
Default 90. Increase for high-value project context; decrease for fast-changing tasks.
"""

ARCHIVE_TTL_DAYS = int(os.environ.get('HAWK_ARCHIVE_TTL_DAYS', '180'))
"""
Days before archived memories are permanently deleted.
Default 180. Increase for compliance/legal context; decrease to save storage.
"""

# ─── Importance Thresholds ────────────────────────────────────────────────────

IMPORTANCE_THRESHOLD_LOW = float(os.environ.get('HAWK_IMPORTANCE_LOW', '0.3'))
"""
Memories below this importance AND accessed > ARCHIVE_TTL_DAYS are deleted.
Range: 0.1–0.5. Default 0.3.
Raise to auto-delete more aggressively; lower to keep more memories.
"""

IMPORTANCE_THRESHOLD_HIGH = float(os.environ.get('HAWK_IMPORTANCE_HIGH', '0.8'))
"""
Memories at or above this importance are promoted to 'long' layer immediately.
Range: 0.6–1.0. Default 0.8.
Raise to require more explicit importance before long-term storage.
"""

# ─── Retrieval ──────────────────────────────────────────────────────────────

RECALL_TOP_K = int(os.environ.get('HAWK_RECALL_TOP_K', '5'))
"""
Number of memories to retrieve per recall query.
Default 5. Increase for complex multi-task agents; decrease to save tokens.
"""

RECALL_MIN_SCORE = float(os.environ.get('HAWK_RECALL_MIN_SCORE', '0.6'))
"""
Minimum relevance score (0–1) for a memory to be included in results.
Range: 0.0–1.0. Default 0.6.
Raise for stricter recall (fewer but more relevant); lower for permissive recall.
Note: Only applies to LanceDB distance-derived scores in hybrid search.
"""

CAPTURE_MAX_CHUNKS = int(os.environ.get('HAWK_CAPTURE_MAX_CHUNKS', '3'))
"""
Max number of memory chunks to extract per response.
Default 3. Increase to capture more per turn; decrease to reduce noise.
"""

CAPTURE_IMPORTANCE_THRESHOLD = float(os.environ.get('HAWK_CAPTURE_THRESHOLD', '0.5'))
"""
Min importance (0–1) for a chunk to be stored during capture.
Default 0.5. Raise to only store high-value memories; lower to store everything.
"""

# ─── Compression ─────────────────────────────────────────────────────────────

SUMMARY_MAX_CHARS = int(os.environ.get('HAWK_SUMMARY_MAX_CHARS', '200'))
"""
Max characters when summarizing a memory during compression.
Default 200. Increase for richer summaries; decrease to save storage.
"""

COMPRESS_RATIO_THRESHOLD = float(os.environ.get('HAWK_COMPRESS_RATIO', '0.5'))
"""
In smart compression: min ratio of kept tokens to max_tokens before we start
adding back filler messages.
Default 0.5 (50%). Lower = keep more messages; higher = stay leaner.
"""

# ─── Embedding ──────────────────────────────────────────────────────────────

EMBEDDING_DIMENSIONS = int(os.environ.get('HAWK_EMBEDDING_DIMENSIONS', '1536'))
"""
Embedding vector dimension. Must match your embedding model.
Default 1536 (OpenAI text-embedding-3-small). 384 for all-MiniLM-L6-v2.
Setting wrong dimension causes LanceDB errors on insert.
"""


class Config:
    """hawk 配置"""

    DEFAULTS = {
        "db_path": "~/.hawk/lancedb",
        "memories_path": "~/.hawk/memories.json",
        "governance_path": "~/.hawk/governance.log",
        "openai_api_key": "",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "recall_top_k": RECALL_TOP_K,
        "recall_min_score": RECALL_MIN_SCORE,
        "capture_max_chunks": CAPTURE_MAX_CHUNKS,
        "capture_importance_threshold": CAPTURE_IMPORTANCE_THRESHOLD,
        "decay_rate": DECAY_RATE,
        "working_ttl_days": WORKING_TTL_DAYS,
        "short_ttl_days": SHORT_TTL_DAYS,
        "long_ttl_days": LONG_TTL_DAYS,
        "archive_ttl_days": ARCHIVE_TTL_DAYS,
    }

    def __init__(self, config_path: str = None):
        self._config = {**self.DEFAULTS}
        self.config_path = config_path or os.path.expanduser("~/.hawk/config.json")
        self._load()

    def _load(self):
        # 配置文件（用户配置优先于默认值）
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
            except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
                print(f"[Config] Warning: failed to load {self.config_path}: {e}. Using defaults.")

        # 环境变量覆盖（最高优先级）
        # Generic: any HAWK_* env var overrides the matching underscore-key in config.
        # e.g. HAWK_DECAY_RATE=0.9 → config['decay_rate'] = 0.9
        # Type coercion: try int/float, otherwise keep as string.
        _int_keys = {'recall_top_k', 'capture_max_chunks', 'working_ttl_days', 'short_ttl_days',
                     'long_ttl_days', 'archive_ttl_days', 'embedding_dimensions'}
        _float_keys = {'decay_rate', 'recall_min_score', 'capture_importance_threshold',
                       'importance_threshold_low', 'importance_threshold_high', 'compress_ratio_threshold',
                       'summary_max_chars'}
        for env_key in os.environ:
            if env_key.startswith('HAWK_'):
                config_key = env_key[len('HAWK_'):].lower()
                if config_key and config_key in self._config:
                    val = os.environ[env_key]
                    if config_key in _int_keys:
                        try: val = int(val)
                        except ValueError: pass
                    elif config_key in _float_keys:
                        try: val = float(val)
                        except ValueError: pass
                    self._config[config_key] = val

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def set(self, key: str, value):
        self._config[key] = value

    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def reload(self):
        self._load()
