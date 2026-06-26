import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from openclaw.core.skill import BaseSkill
from .vectorstorage import VectorStorage

logger = logging.getLogger(__name__)

class EnterpriseMemorySkill(BaseSkill):
    """
    Enterprise Memory Skill - OpenClaw 企业级长期记忆插件 (v1.1.1)
    """

    def __init__(self):
        super().__init__()
        self.vector_storage: Optional[VectorStorage] = None
        self.plugin_dir = Path(__file__).parent.absolute()
        self.config = {}

    def load_config(self):
        yaml_path = self.plugin_dir / "memory_config.yaml"
        try:
            import yaml
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"✅ Loaded memory config from {yaml_path}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load memory_config.yaml: {e}")
            self.config = {}

    def _init_storage(self):
        if not self.vector_storage:
            try:
                yaml_path = str(self.plugin_dir / "memory_config.yaml")
                self.vector_storage = VectorStorage(config_path=yaml_path)
                logger.info("✅ VectorStorage initialized successfully.")
            except Exception as e:
                logger.error(f"❌ VectorStorage init failed: {e}")
                self.vector_storage = None

    def on_startup(self):
        logger.info("🚀 Enterprise Memory Skill Starting...")
        self.load_config()
        self._init_storage()
        if self.vector_storage:
            self.vector_storage.initialize_model()

    def on_shutdown(self):
        logger.info("🛑 Enterprise Memory Skill Shutting down...")
        if self.vector_storage:
            self.vector_storage._save_db()
            del self.vector_storage

    def get_context(self, query: str, context_limit: int = 2000) -> str:
        if not self.vector_storage:
            return ""
        try:
            top_k = self.config.get('retrieval_top_k', 5)
            results = self.vector_storage.retrieve_similar(query, top_k=top_k)
            if not results:
                return ""

            chunks = []
            total = 0
            threshold = self.config.get('retrieval_threshold', 0.82)
            for uuid_str, text, score in results:
                if total >= context_limit:
                    break
                if score < threshold:
                    continue
                chunk = f"[Memory {uuid_str[:8]} | Score: {score:.3f}] {text}"
                chunks.append(chunk)
                total += len(chunk)
            return "\n".join(chunks)
        except Exception as e:
            logger.error(f"get_context error: {e}")
            return ""

    def execute_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行记忆写入与查询动作"""
        logger.info(f"Executing action: {action}")
        
        if not self.vector_storage:
            return {"status": "error", "message": "Vector storage engine is not running"}

        # 统一转为大写处理，增强鲁棒性
        act_upper = action.upper()

        if act_upper in ["REMEMBER", "ADD_MEMORY"]:
            text = params.get("text", params.get("content", "")) # 兼容 text 和 content 两种 key
            confidence = float(params.get("confidence", 1.0))
            metadata = params.get("metadata", {})
            
            if not text:
                return {"status": "error", "message": "Content parameter missing"}
            
            uuid_obj = self.vector_storage.add_text(text, metadata=metadata, confidence=confidence)
            if uuid_obj:
                return {"status": "success", "message": "Memory persisted", "id": uuid_obj}
            return {"status": "error", "message": "Failed to persist"}

        elif act_upper in ["RECALL", "RECALL_MEMORY", "SEARCH_MEMORY"]:
            query = params.get("query", "")
            if not query:
                return {"status": "error", "message": "Query parameter missing"}
                
            top_k = params.get("top_k", self.vector_storage.retrieval_top_k)
            results = self.vector_storage.retrieve_similar(query, top_k=top_k)
            
            return {
                "status": "success",
                "results": [{"id": u, "text": t, "score": float(s)} for u, t, s in results],
                "count": len(results)
            }
        
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}