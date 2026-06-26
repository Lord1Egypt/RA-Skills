import os
import time
import pickle
import logging
import uuid
import yaml
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorStorage:
    def __init__(self, config_path: str = "memory_config.yaml"):
        self.config_path = Path(config_path)
        self.data: List[Dict[str, Any]] = []
        self.model: Optional[SentenceTransformer] = None
        self.db_path: Optional[Path] = None
        self.retrieval_top_k = 5
        self.max_entries = 2000
        self.model_name = "BAAI/bge-small-zh-v1.5"

        self._load_config()
        self._load_db()

    def _load_config(self):
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                
                self.db_path = Path(config.get('db_path', 'data/memory/vectors.db'))
                self.retrieval_top_k = config.get('retrieval_top_k', 5)
                self.max_entries = config.get('max_memory_entries', 2000)
                self.model_name = config.get('embedding_model_name', "BAAI/bge-small-zh-v1.5")
            else:
                self._set_defaults()
        except Exception as e:
            logger.warning(f"Config load failed: {e}")
            self._set_defaults()

    def _set_defaults(self):
        self.model_name = "BAAI/bge-small-zh-v1.5"
        self.retrieval_top_k = 5
        self.max_entries = 2000
        self.db_path = Path("data/memory/vectors.db")

    def _load_db(self):
        if self.db_path and self.db_path.exists():
            try:
                with open(self.db_path, 'rb') as f:
                    self.data = pickle.load(f)
                logger.info(f"✅ Loaded {len(self.data)} memory entries from disk.")
            except Exception as e:
                logger.error(f"DB load failed: {e}")

    def _save_db(self):
        if not self.db_path:
            return
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.data, f)
        except Exception as e:
            logger.error(f"DB save failed: {e}")

    def initialize_model(self):
        if self.model:
            return
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✅ Embedding model loaded: {self.model_name}")
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")

    def _prune_old_entries(self):
        """超过上限时清理旧条目（优先保留高置信度）"""
        if len(self.data) <= self.max_entries:
            return
            
        self.data.sort(
            key=lambda x: (x.get('confidence', 0.0), x.get('timestamp', 0)), 
            reverse=True
        )
        self.data = self.data[:self.max_entries]

    def add_text(self, text: str, metadata: Dict = None, confidence: float = 0.7) -> Optional[str]:
        self.initialize_model()
        if not self.model:
            return None

        uid = str(uuid.uuid4())
        timestamp = int(time.time())

        try:
            embedding = self.model.encode([text], normalize_embeddings=True)[0]
            self.data.append({
                "uuid": uid,
                "text": text,
                "embedding": embedding,
                "timestamp": timestamp,
                "metadata": metadata or {},
                "confidence": float(confidence)
            })
            self._prune_old_entries()
            self._save_db()
            logger.debug(f"Memory added: {uid[:8]} | conf: {confidence:.2f}")
            return uid
        except Exception as e:
            logger.error(f"add_text failed: {e}")
            return None

    def retrieve_similar(self, query: str, top_k: int = None) -> List[Tuple[str, str, float]]:
        if not self.model or not self.data:
            return []

        try:
            query_emb = self.model.encode([query], normalize_embeddings=True)[0]
            results = []

            for item in self.data:
                sim = float(np.dot(query_emb, item['embedding']))
                results.append((item['uuid'], item['text'], sim))

            results.sort(key=lambda x: x[2], reverse=True)
            return results[: (top_k or self.retrieval_top_k)]
        except Exception as e:
            logger.error(f"retrieve_similar error: {e}")
            return []