#!/usr/bin/env python3
"""
Embedding Generator - 向量化生成器

使用 SentenceTransformer 批量生成文本向量，支持断点续传和内存管理。
"""

import gc
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

import psutil
from rich.console import Console

console = Console()


class EmbeddingGenerator:
    """向量化生成器"""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.model_name = model_name
        self._model = None  # 懒加载
        self._dimension = None

    @property
    def model(self):
        """懒加载模型"""
        if self._model is None:
            console.print(f"加载嵌入模型：{self.model_name}")
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self._dimension = self._model.get_sentence_embedding_dimension()
        return self._model

    def generate(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        批量生成向量

        参数:
        - texts: 文本列表
        - batch_size: 批次大小

        返回:
        - numpy 数组 (N x D) 的列表形式
        """
        # 检查内存使用
        self._check_memory()

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = self.model.encode(
                batch,
                batch_size=batch_size,
                show_progress_bar=False,
                normalize_embeddings=True,
                convert_to_numpy=False,
            )
            embeddings.extend(batch_embeddings)

        return [emb.tolist() for emb in embeddings]

    def batch_generate_with_resume(
        self, texts: List[str], checkpoint_file: str, batch_size: int = 32
    ) -> List[List[float]]:
        """
        支持断点续传的批量向量化

        参数:
        - texts: 文本列表
        - checkpoint_file: 断点文件路径
        - batch_size: 批次大小
        """
        # 加载断点
        processed = self._load_checkpoint(checkpoint_file)
        start_idx = len(processed)

        # 批量处理
        embeddings = processed.copy()
        for i in range(start_idx, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = self.generate(batch, batch_size)
            embeddings.extend(batch_embeddings)

            # 保存断点
            self._save_checkpoint(checkpoint_file, embeddings)

            # 进度显示
            progress = (i + len(batch)) / len(texts) * 100
            console.print(f"向量化进度：{progress:.1f}%")

        return embeddings

    def _check_memory(self):
        """检查内存使用"""
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            console.print(f"⚠️  内存使用过高 ({memory.percent:.1f}%)，释放缓存")
            gc.collect()

    def _save_checkpoint(self, checkpoint_file: str, embeddings: List[List[float]]):
        """保存断点"""
        Path(checkpoint_file).parent.mkdir(parents=True, exist_ok=True)
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(
                {"embeddings": embeddings, "timestamp": datetime.now().isoformat()},
                f,
                ensure_ascii=False,
                indent=2,
            )

    def _load_checkpoint(self, checkpoint_file: str) -> List[List[float]]:
        """加载断点"""
        if not os.path.exists(checkpoint_file):
            return []

        with open(checkpoint_file, encoding="utf-8") as f:
            data = json.load(f)

        return data.get("embeddings", [])

    def validate_embeddings(self, embeddings: List[List[float]]) -> dict:
        """验证向量质量"""
        issues = {
            "zero_vectors": 0,
            "nan_values": 0,
            "dimension_mismatch": 0,
        }

        expected_dim = self._dimension
        if expected_dim is None:
            return issues

        for i, emb in enumerate(embeddings):
            if len(emb) != expected_dim:
                issues["dimension_mismatch"] += 1
            if all(v == 0 for v in emb):
                issues["zero_vectors"] += 1
            if any(isinstance(v, float) and v != v for v in emb):
                issues["nan_values"] += 1

        return issues
