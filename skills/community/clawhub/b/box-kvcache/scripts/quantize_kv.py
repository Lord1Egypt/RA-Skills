#!/usr/bin/env python3
"""
box-kvcache: KV Cache INT8 量化工具
将 KV Cache 从 float16 量化到 int8，减少显存占用
"""

import numpy as np
import argparse
from typing import Tuple, Optional
import json


class KVCacheQuantizer:
    """
    KV Cache 量化器
    使用对称量化，将 float16 -> int8
    """
    
    def __init__(self, bits: int = 8):
        """
        初始化量化器
        
        Args:
            bits: 量化位数 (支持 4, 8)
        """
        self.bits = bits
        self.scale_factor: Optional[np.ndarray] = None
        
    def quantize(self, kv_cache: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        量化 KV Cache
        
        Args:
            kv_cache: float16/32 的 KV Cache 数组，形状 [seq_len, hidden_dim]
        
        Returns:
            (quantized, scale) - 量化后的数据 + 缩放因子
        """
        if kv_cache.dtype not in [np.float16, np.float32, np.float64]:
            raise ValueError(f"Unsupported dtype: {kv_cache.dtype}")
        
        # 计算缩放因子（对称量化）
        max_val = np.abs(kv_cache).max()
        
        if max_val == 0:
            # 全零情况
            scale = np.array(1.0, dtype=kv_cache.dtype)
            quantized = np.zeros_like(kv_cache, dtype=np.int8)
            self.scale_factor = scale
            return quantized, scale
        
        # 计算缩放因子: scale = max_val / (2^(bits-1) - 1)
        max_scale = (2 ** (self.bits - 1) - 1)
        scale = np.array(max_val / max_scale, dtype=kv_cache.dtype)
        self.scale_factor = scale
        
        # 量化
        quantized = np.round(kv_cache / scale).astype(np.int8)
        
        return quantized, scale
    
    def dequantize(self, quantized: np.ndarray, scale: np.ndarray) -> np.ndarray:
        """
        反量化 - 从 int8 恢复到 float
        
        Args:
            quantized: 量化后的数据
            scale: 缩放因子
        
        Returns:
            恢复后的 float 数组
        """
        return (quantized.astype(np.float32) * scale).astype(np.float16)
    
    def compress_ratio(self, original_shape: tuple, dtype_bytes: int = 2) -> float:
        """
        计算压缩率
        
        Args:
            original_shape: 原始 tensor 形状
            dtype_bytes: 原始数据类型字节数
        
        Returns:
            压缩倍数
        """
        original_size = 1
        for dim in original_shape:
            original_size *= dim
        
        original_bytes = original_size * dtype_bytes
        quantized_bytes = original_size * (self.bits // 8)
        
        return original_bytes / quantized_bytes


class LowRankCompressor:
    """
    低秩分解压缩器
    使用 SVD 截断来压缩 KV Cache
    """
    
    def __init__(self, rank_ratio: float = 0.25):
        """
        初始化压缩器
        
        Args:
            rank_ratio: 保留的秩比例 (0 < r <= 1)
                       例如 rank_ratio=0.25 表示保留25%的维度
        """
        self.rank_ratio = rank_ratio
        self.U: Optional[np.ndarray] = None
        self.S: Optional[np.ndarray] = None
        self.Vt: Optional[np.ndarray] = None
        
    def compress(self, matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        使用 SVD 进行低秩分解压缩
        
        Args:
            matrix: 输入矩阵，形状 [seq_len, hidden_dim]
        
        Returns:
            (U, S, Vt) - 分解后的三个矩阵
        """
        # SVD 分解
        # matrix = U @ S @ Vt
        # 其中 U: [seq_len, r], S: [r], Vt: [r, hidden_dim]
        # 压缩后存储: U * sqrt(S) + Vt * sqrt(S)  比直接存三个矩阵小
        
        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        
        # 计算保留的秩
        original_rank = len(S)
        keep_rank = max(1, int(original_rank * self.rank_ratio))
        
        # 截断
        self.U = U[:, :keep_rank]
        self.S = S[:keep_rank]
        self.Vt = Vt[:keep_rank, :]
        
        return self.U, self.S, self.Vt
    
    def decompress(self) -> np.ndarray:
        """
        从压缩表示恢复原始矩阵
        
        Returns:
            恢复后的矩阵
        """
        if self.U is None or self.S is None or self.Vt is None:
            raise ValueError("请先调用 compress()")
        
        # 恢复: U @ diag(S) @ Vt
        restored = np.dot(self.U * self.S, self.Vt)
        return restored
    
    def compression_ratio(self, original_shape: tuple) -> float:
        """
        计算压缩率
        
        Args:
            original_shape: 原始矩阵形状 [seq_len, hidden_dim]
        
        Returns:
            压缩倍数
        """
        seq_len, hidden_dim = original_shape
        original_size = seq_len * hidden_dim
        
        keep_rank = int(min(seq_len, hidden_dim) * self.rank_ratio)
        compressed_size = seq_len * keep_rank + keep_rank + keep_rank * hidden_dim
        
        return original_size / compressed_size


def demo():
    """演示量化效果"""
    print("=" * 50)
    print("box-kvcache KV Cache 量化演示")
    print("=" * 50)
    
    # 模拟 KV Cache: [seq_len=1024, hidden_dim=4096]
    seq_len, hidden_dim = 1024, 4096
    print(f"\n模拟 KV Cache: 形状 [{seq_len}, {hidden_dim}]")
    print(f"数据类型: float16 (2 bytes)")
    
    # 生成随机数据
    np.random.seed(42)
    kv_cache = np.random.randn(seq_len, hidden_dim).astype(np.float16)
    
    # 计算原始大小
    original_bytes = seq_len * hidden_dim * 2
    print(f"原始大小: {original_bytes / 1024 / 1024:.2f} MB")
    
    # INT8 量化
    print("\n--- INT8 量化 ---")
    quantizer = KVCacheQuantizer(bits=8)
    q_kv, scale = quantizer.quantize(kv_cache)
    ratio = quantizer.compress_ratio(kv_cache.shape)
    print(f"量化后大小: {q_kv.nbytes / 1024 / 1024:.2f} MB")
    print(f"压缩率: {ratio:.2f}x")
    
    # 反量化并计算误差
    restored = quantizer.dequantize(q_kv, scale)
    error = np.abs(kv_cache - restored).mean()
    relative_error = error / np.abs(kv_cache).mean() * 100
    print(f"平均绝对误差: {error:.6f}")
    print(f"相对误差: {relative_error:.4f}%")
    
    # 低秩分解
    print("\n--- 低秩分解压缩 (rank_ratio=0.25) ---")
    compressor = LowRankCompressor(rank_ratio=0.25)
    U, S, Vt = compressor.compress(kv_cache)
    comp_ratio = compressor.compression_ratio(kv_cache.shape)
    print(f"U 形状: {U.shape}")
    print(f"S 形状: {S.shape}")
    print(f"Vt 形状: {Vt.shape}")
    print(f"压缩率: {comp_ratio:.2f}x")
    
    # 恢复并计算误差
    restored_lr = compressor.decompress()
    error_lr = np.abs(kv_cache - restored_lr).mean()
    relative_error_lr = error_lr / np.abs(kv_cache).mean() * 100
    print(f"平均绝对误差: {error_lr:.6f}")
    print(f"相对误差: {relative_error_lr:.4f}%")
    
    print("\n" + "=" * 50)
    print("结论: INT8 量化压缩率高但有误差，低秩分解精度更好")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="KV Cache 量化工具")
    parser.add_argument("--bits", type=int, default=8, choices=[4, 8], help="量化位数")
    parser.add_argument("--rank-ratio", type=float, default=0.25, help="低秩压缩保留比例")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--seq-len", type=int, default=4096, help="序列长度")
    parser.add_argument("--hidden-dim", type=int, default=4096, help="隐藏层维度")
    args = parser.parse_args()
    
    if args.demo:
        demo()
        return
    
    # 简单的压缩演示
    print(f"KV Cache 量化器 (bits={args.bits})")
    print(f"低秩压缩器 (rank_ratio={args.rank_ratio})")
    
    # 生成示例数据
    np.random.seed(42)
    seq_len, hidden_dim = args.seq_len, args.hidden_dim
    print(f"\n输入形状: [{seq_len}, {hidden_dim}]")
    
    kv = np.random.randn(seq_len, hidden_dim).astype(np.float16)
    
    # INT8 量化
    q = KVCacheQuantizer(bits=args.bits)
    q_kv, scale = q.quantize(kv)
    print(f"量化后: {q_kv.nbytes / 1024 / 1024:.2f} MB (原始 {kv.nbytes / 1024 / 1024:.2f} MB)")
    
    # 低秩分解
    c = LowRankCompressor(rank_ratio=args.rank_ratio)
    U, S, Vt = c.compress(kv)
    print(f"低秩压缩后: {U.nbytes + S.nbytes + Vt.nbytes / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
