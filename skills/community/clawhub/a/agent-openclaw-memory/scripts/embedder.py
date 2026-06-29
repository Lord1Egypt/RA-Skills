"""
embedder.py — 统一嵌入向量服务
所有脚本从此处获取嵌入向量，自带三级降级：
1. LM Studio（主，OpenAI 兼容 embedding 服务）
2. 本地 ONNX 模型（备，同机运行）
3. 纯 numpy 哈希向量（底线，搜索结果退化但不崩）
"""

import json
import os
import time
import hashlib
import numpy as np
from pathlib import Path

# LM Studio 配置 — 从 shared_config 读取（唯一真相源）
from shared_config import LMSTUDIO_EMBED_URL as LMSTUDIO_URL, LMSTUDIO_KEY, EMBED_MODEL

# Qdrant 向量维度
EMBED_DIMS = 768

# 本地 ONNX 模型缓存
ONNX_MODEL_PATH = Path.home() / ".openclaw" / "embed_model.onnx"
ONNX_MODEL_URL = "https://huggingface.co/Xenova/all-MiniLM-L6-v2/resolve/main/onnx/model.onnx"

# 性能统计
_stats = {"lm_studio": 0, "local_onnx": 0, "numpy_hash": 0, "failed": 0, "cache_hit": 0}

# 嵌入向量本地缓存（LRU，最多 500 条，5 分钟 TTL）
_cache_lock = __import__("threading").Lock()
_cache = {}
_CACHE_MAX = 500
_CACHE_TTL = 300  # 5 分钟


def _cache_key(text: str) -> str:
    """生成缓存键（取前 500 字符 hash，平衡命中率和特异性）"""
    h = hashlib.md5(text[:500].encode("utf-8")).hexdigest()
    return h


def _cache_get(text: str) -> np.ndarray | None:
    with _cache_lock:
        entry = _cache.get(_cache_key(text))
        if entry:
            vec, ts = entry
            if time.time() - ts < _CACHE_TTL:
                _stats["cache_hit"] += 1
                return vec.copy()
            else:
                del _cache[_cache_key(text)]
    return None


def _cache_set(text: str, vec: np.ndarray):
    with _cache_lock:
        if len(_cache) >= _CACHE_MAX:
            # 淘汰最旧的 20%
            oldest = sorted(_cache.items(), key=lambda x: x[1][1])[: _CACHE_MAX // 5]
            for k, _ in oldest:
                del _cache[k]
        _cache[_cache_key(text)] = (vec.copy(), time.time())


def _lm_studio_embed(text: str) -> np.ndarray | None:
    """Level 1: LM Studio"""
    import requests
    resp = requests.post(
        LMSTUDIO_URL,
        headers={"Authorization": f"Bearer {LMSTUDIO_KEY}"},
        json={"input": text[:2000], "model": EMBED_MODEL},
        timeout=60,
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("data"):
            return np.array(data["data"][0]["embedding"], dtype=np.float32)
    return None


def _local_onnx_embed(text: str) -> np.ndarray | None:
    """Level 2: 本地 ONNX 模型（自动下载，一次性的）"""
    try:
        import onnxruntime as ort

        if not ONNX_MODEL_PATH.exists():
            # 首次运行，下载模型
            print(f"[embedder] 下载本地 ONNX 模型到 {ONNX_MODEL_PATH}...")
            import urllib.request
            ONNX_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(ONNX_MODEL_URL, ONNX_MODEL_PATH)
            print("[embedder] 下载完成")

        # 简单的 tokenizer + model 推理
        # 使用 onnxruntime 的 minimal 模式
        session = ort.InferenceSession(str(ONNX_MODEL_PATH))
        # MiniLM 输出 384 维，需要上采样到 768 维
        # 简化版：直接拼接到 768
        input_name = session.get_inputs()[0].name
        # 这里需要 tokenizer... 简化处理
        return None  # 暂未实现完整 pipeline

    except Exception:
        return None


def _numpy_hash_embed(text: str) -> np.ndarray:
    """Level 3: 纯 numpy 哈希向量（底线保底）
    
    用 MD5 哈希生成确定性向量，确保相同文本总是相同向量。
    语义质量差（不是真正的 embedding），但 Qdrant 可以正常检索。
    """
    vec = np.zeros(EMBED_DIMS, dtype=np.float32)
    # 按字符 n-gram 哈希到向量位置
    text_bytes = text.encode("utf-8")
    for i in range(len(text_bytes)):
        h = hashlib.md5(text_bytes[max(0, i - 4):i + 4]).digest()
        pos = int.from_bytes(h[:4], "big") % EMBED_DIMS
        val = int.from_bytes(h[4:8], "big") / (2 ** 32)
        vec[pos] += val

    # 归一化
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def get_embedding(text: str, retries: int = 1) -> np.ndarray | None:
    """获取嵌入向量（三级降级 + 本地缓存）

    相同文本 5 分钟内直接返回缓存，跳过网络调用。
    """
    if not text or not text.strip():
        return None

    # Level 0: 本地缓存（命中直接返回，0 网络调用）
    cached = _cache_get(text)
    if cached is not None:
        return cached

    # Level 1: LM Studio（重试机制）
    for attempt in range(retries + 1):
        try:
            vec = _lm_studio_embed(text)
            if vec is not None and len(vec) == EMBED_DIMS:
                _stats["lm_studio"] += 1
                _cache_set(text, vec)
                return vec
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            print(f"[embedder] LM Studio 不可用: {e}")

    # Level 2: 本地 ONNX
    try:
        vec = _local_onnx_embed(text)
        if vec is not None and len(vec) > 0:
            # 确保维度匹配
            if len(vec) != EMBED_DIMS:
                # 上采样/下采样到 768 维
                if len(vec) < EMBED_DIMS:
                    vec = np.pad(vec, (0, EMBED_DIMS - len(vec)))
                else:
                    vec = vec[:EMBED_DIMS]
            _stats["local_onnx"] += 1
            return vec.astype(np.float32)
    except Exception:
        pass

    # Level 3: 纯 numpy 哈希（底线）
    _stats["numpy_hash"] += 1
    return _numpy_hash_embed(text)


def print_stats():
    """打印 embedding 统计"""
    total = sum(_stats.values())
    if total == 0:
        print("[embedder] 尚无调用")
        return
    print(f"[embedder] LM Studio: {_stats['lm_studio']} ({_stats['lm_studio']/total*100:.0f}%) | "
          f"缓存命中: {_stats['cache_hit']} ({_stats['cache_hit']/total*100:.0f}%) | "
          f"本地 ONNX: {_stats['local_onnx']} ({_stats['local_onnx']/total*100:.0f}%) | "
          f"哈希兜底: {_stats['numpy_hash']} ({_stats['numpy_hash']/total*100:.0f}%) | "
          f"失败: {_stats['failed']}")


def prewarm() -> bool:
    """预暖嵌入模型，确保 LM Studio 已加载模型（再走批量嵌入）。

    Returns True 如果 LM Studio 嵌入服务就绪。
    """
    import requests
    # Step 1: 检查 LM Studio 是否在线
    try:
        models_url = LMSTUDIO_URL.rsplit("/", 2)[0] + "/v1/models"
        resp = requests.get(
            models_url,
            headers={"Authorization": f"Bearer {LMSTUDIO_KEY}"},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("id", "") for m in data.get("data", [])]
            if EMBED_MODEL not in models:
                print(f"[embedder] 模型 {EMBED_MODEL} 未加载，触发加载...")
    except Exception:
        pass

    # Step 2: 发送预热请求（触发模型加载，timeout=120 给足加载时间）
    print(f"[embedder] 预暖嵌入模型 {EMBED_MODEL}...")
    t0 = time.time()
    try:
        resp = requests.post(
            LMSTUDIO_URL,
            headers={"Authorization": f"Bearer {LMSTUDIO_KEY}"},
            json={"input": "prewarm", "model": EMBED_MODEL},
            timeout=120,
        )
        if resp.status_code == 200:
            elapsed = time.time() - t0
            data = resp.json()
            if data.get("data"):
                dims = len(data["data"][0].get("embedding", []))
                print(f"[embedder] 预暖完成 ({elapsed:.1f}s, dims={dims})")
                return True
    except Exception as e:
        print(f"[embedder] 预暖失败 ({time.time() - t0:.1f}s): {e}")
    return False


if __name__ == "__main__":
    # 测试
    import sys
    test_text = sys.argv[1] if len(sys.argv) > 1 else "test text"
    vec = get_embedding(test_text)
    if vec is not None:
        print(f"向量维度: {len(vec)}")
        print(f"前 5 维: {vec[:5]}")
        print_stats()
    else:
        print("嵌入失败")
