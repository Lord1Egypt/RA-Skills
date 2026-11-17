"""语义缓存（本地、零密钥、零联网，省 token）。

- 精确命中：归一化 query 后做哈希，完全一致的请求直接返回缓存结果，跳过 API 调用。
- 模糊命中（可选）：用 embedding 相似度（sentence-transformers，可选安装）或 difflib 字符匹配。
- 存储：本地 SQLite，带 TTL 自动过期。

安全：仅缓存 query 与对应回复文本，不缓存任何密钥；路径在用户主目录。

embedding 依赖（可选）：pip install sentence-transformers
- 安装后：自动启用 embedding 相似度，阈值 0.85，大幅降低语义误命中
- 未安装：降级 difflib 字符匹配（原有逻辑），零强制依赖
"""

import os
import sqlite3
import hashlib
import time
import re
import difflib

DEFAULT_CACHE_DB = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "cache.db")
FUZZY_THRESHOLD = 0.80
EMBEDDING_THRESHOLD = 0.85
MIN_FUZZY_LEN = 8

# 全局 embedding 模型缓存（懒加载，避免重复 import）
_embedding_model = None
_embedding_available = None  # None=未检测, True=可用, False=不可用


def _get_embedding_model():
    """懒加载 sentence-transformers 模型（内存缓存，避免重复 import）。返回 model 或 None。"""
    global _embedding_model, _embedding_available
    if _embedding_available is not None:
        return _embedding_model
    try:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        _embedding_available = True
    except ImportError:
        _embedding_model = None
        _embedding_available = False
    except Exception:
        _embedding_model = None
        _embedding_available = False
    return _embedding_model


def _embedding_similarity(text1, text2):
    """计算两段文本的 cosine similarity。返回 0~1。模型不可用时返回 None。"""
    model = _get_embedding_model()
    if model is None:
        return None
    try:
        emb1 = model.encode([text1])[0]
        emb2 = model.encode([text2])[0]
        import numpy as np
        cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8)
        return float(cos_sim)
    except Exception:
        return None


def _norm(text):
    """归一化：去空白、转小写、去标点。用于缓存 key。"""
    if not text:
        return ""
    s = text.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\u4e00-\u9fff]+", " ", s)
    return s.strip()


def _conn(db_path=None):
    db = db_path or DEFAULT_CACHE_DB
    if db == ":memory:":
        return sqlite3.connect(":memory:")
    os.makedirs(os.path.dirname(db), exist_ok=True)
    c = sqlite3.connect(db)
    c.execute(
        """CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qhash TEXT UNIQUE, norm_query TEXT,
            provider TEXT, model TEXT, response TEXT,
            created_at REAL
        )"""
    )
    c.commit()
    return c


def get(prompt, ttl_hours=168, fuzzy=False, db_path=None):
    """返回缓存命中时的 (provider, model, response)，否则 None。"""
    norm = _norm(prompt)
    if not norm:
        return None
    qh = hashlib.sha256(norm.encode("utf-8")).hexdigest()
    c = _conn(db_path)
    try:
        now = time.time()
        row = c.execute(
            "SELECT provider, model, response, created_at FROM cache WHERE qhash=?",
            (qh,),
        ).fetchone()
        if row:
            provider, model, resp, created = row
            if (now - created) <= ttl_hours * 3600:
                return (provider, model, resp)
            else:
                c.execute("DELETE FROM cache WHERE qhash=?", (qh,))
                c.commit()

        if fuzzy:
            # 过短的 query 跳过模糊匹配，避免短句误命中
            if len(norm) < MIN_FUZZY_LEN:
                pass  # 不做模糊，直接返回 None
            else:
                rows = c.execute(
                    "SELECT provider, model, response, norm_query, created_at FROM cache"
                ).fetchall()
                best = None
                best_ratio = 0.0
                use_embedding = False
                # 尝试 embedding 相似度（如果模型可用）
                if _get_embedding_model() is not None:
                    use_embedding = True
                    rows_cache = list(rows)  # 避免重复查询
                    for provider, model, resp, nq, created in rows_cache:
                        if (now - created) > ttl_hours * 3600:
                            continue
                        sim = _embedding_similarity(norm, nq)
                        if sim is not None and sim > best_ratio:
                            best_ratio = sim
                            best = (provider, model, resp)
                if not use_embedding:
                    # 降级：difflib 字符匹配
                    for provider, model, resp, nq, created in rows:
                        if (now - created) > ttl_hours * 3600:
                            continue
                        ratio = difflib.SequenceMatcher(None, norm, nq).ratio()
                        # 长度惩罚：两句话长度差异越大，越可能是不同问题
                        len_a, len_b = len(norm), len(nq)
                        if min(len_a, len_b) > 0:
                            length_penalty = min(len_a, len_b) / max(len_a, len_b)
                        else:
                            length_penalty = 0.0
                        adjusted_ratio = ratio * (0.8 + 0.2 * length_penalty)
                        if adjusted_ratio > best_ratio:
                            best_ratio = adjusted_ratio
                            best = (provider, model, resp)
                threshold = EMBEDDING_THRESHOLD if use_embedding else FUZZY_THRESHOLD
                if best and best_ratio >= threshold:
                    return best
    finally:
        c.close()
    return None


def put(prompt, provider, model, response, db_path=None):
    """写入缓存（幂等：同 key 覆盖）。"""
    norm = _norm(prompt)
    if not norm:
        return
    qh = hashlib.sha256(norm.encode("utf-8")).hexdigest()
    c = _conn(db_path)
    try:
        c.execute(
            "INSERT OR REPLACE INTO cache (qhash, norm_query, provider, model, response, created_at) "
            "VALUES (?,?,?,?,?,?)",
            (qh, norm, provider, model, response, time.time()),
        )
        c.commit()
    finally:
        c.close()


def stats(db_path=None):
    c = _conn(db_path)
    try:
        n = c.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
        return {"entries": n}
    finally:
        c.close()


def clear(db_path=None):
    c = _conn(db_path)
    try:
        n = c.execute("DELETE FROM cache").rowcount
        c.commit()
        return n
    finally:
        c.close()
