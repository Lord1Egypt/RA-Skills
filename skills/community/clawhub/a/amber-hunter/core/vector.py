"""
core/vector.py — LanceDB 向量存储与检索（v1.2.31 P1-2）
向量胶囊写入、top_k 语义检索、删除
Multi-embedding provider abstraction via core.embedding
"""
from __future__ import annotations

import sys, shutil
from pathlib import Path

HOME = Path.home()
VECTOR_DIR = HOME / ".amber-hunter" / "lance_db"

# P1-2: 使用统一的 embedding provider 而非 hardcoded MiniLM
_embed_provider = None


def _get_embed_provider():
    """获取 embedding provider（lazy load，线程安全）。"""
    global _embed_provider
    if _embed_provider is not None:
        return _embed_provider
    from core.embedding import get_cached_embed
    _embed_provider = get_cached_embed()
    return _embed_provider


def reset_embed_provider():
    """重置缓存的 provider（配置变更后调用）。

    同时清除 vector 本地缓存和 embedding 模块缓存，确保下次调用重新加载。
    """
    global _embed_provider
    _embed_provider = None
    # 同步重置 embedding 模块的全局缓存
    from core.embedding import reset_embed_provider as _reset_global
    _reset_global()


def init_vector_db() -> "lancedb.db.LanceDB":
    """初始化 LanceDB 目录和 capsule_vectors 表。"""
    import lancedb
    import pyarrow as pa

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(VECTOR_DIR))

    # P1-2: 获取 dimension（不同 provider 不同维度）
    provider = _get_embed_provider()
    dim = provider.config.dimension if hasattr(provider, 'config') else 384

    try:
        if "capsule_vectors" not in db.list_tables().tables:
            schema = pa.schema([
                ("capsule_id", pa.string()),
                ("text", pa.string()),
                ("vector", pa.list_(pa.float32(), dim)),
                ("created_at", pa.float64()),
            ])
            db.create_table("capsule_vectors", schema=schema)
    except Exception:
        pass  # 表可能已被其他进程创建

    return db


def index_capsule(capsule_id: str, memo: str, created_at: float) -> bool:
    """
    计算 memo 的 embedding，存入 LanceDB。
    memo 为解密后原文（memo 字段不加密，content 字段才加密）。
    P1-2: 使用统一的 embedding provider。
    """
    try:
        db = init_vector_db()
        provider = _get_embed_provider()
        vec = provider.encode(memo[:512])  # 截断避免超长
        # encode 返回 np.ndarray，单个向量展平
        vec_list = vec.tolist() if hasattr(vec, 'tolist') else list(vec)
        tbl = db.open_table("capsule_vectors")
        tbl.add([{
            "capsule_id": capsule_id,
            "text": memo[:512],
            "vector": vec_list,
            "created_at": created_at,
        }])
        return True
    except Exception as e:
        import sys
        print(f"[vector] index_capsule failed: {e}", file=sys.stderr)
        return False


def search_vectors(query: str, limit: int = 20) -> list[dict]:
    """
    LanceDB top_k 语义检索。
    返回 [{capsule_id, lance_score, text}, ...]
    lance_score = 1 - normalized_distance（越大越相关，1=完全匹配）
    P1-2: 使用统一的 embedding provider。
    """
    try:
        db = init_vector_db()
        provider = _get_embed_provider()
        q_vec = provider.encode(query[:512])
        q_list = q_vec.tolist() if hasattr(q_vec, 'tolist') else list(q_vec)
        tbl = db.open_table("capsule_vectors")
        rs = tbl.search(q_list, vector_column_name="vector") \
              .limit(limit) \
              .to_list()
        return [
            {
                "capsule_id": r["capsule_id"],
                "lance_score": max(0.0, 1.0 - r["_distance"]),
                "text": r.get("text", ""),
            }
            for r in rs
        ]
    except Exception as e:
        import sys
        print(f"[vector] search_vectors failed: {e}", file=sys.stderr)
        return []


def delete_vector(capsule_id: str) -> bool:
    """删除指定 capsule_id 的向量（胶囊删除时调用）。"""
    try:
        db = init_vector_db()
        tbl = db.open_table("capsule_vectors")
        tbl.delete(f"capsule_id = '{capsule_id}'")
        return True
    except Exception as e:
        import sys
        print(f"[vector] delete_vector failed: {e}", file=sys.stderr)
        return False


def get_vector_stats() -> dict:
    """返回向量库统计信息（用于调试和 /status）。"""
    try:
        import os
        db = init_vector_db()
        if "capsule_vectors" not in db.list_tables().tables:
            return {"count": 0, "vector_db_size_mb": 0}
        tbl = db.open_table("capsule_vectors")
        count = tbl.count_rows()
        # Recursively sum all files under VECTOR_DIR (LanceDB stores data in subdirs)
        size_bytes = sum(
            os.path.getsize(os.path.join(root, f))
            for root, dirs, files in os.walk(str(VECTOR_DIR))
            for f in files
        )
        size_mb = size_bytes / (1024 * 1024)
        return {"count": count, "vector_db_size_mb": round(size_mb, 2)}
    except Exception:
        return {"count": 0, "vector_db_size_mb": 0}
