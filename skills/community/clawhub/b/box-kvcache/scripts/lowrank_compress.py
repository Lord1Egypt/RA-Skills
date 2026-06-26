#!/usr/bin/env python3
"""
box-kvcache: 低秩分解压缩工具
使用 SVD/PCA 对 KV Cache 进行降维压缩
"""

import numpy as np
import argparse
from typing import Tuple, Optional
import json


class KVCacheLowRank:
    """
    KV Cache 低秩分解压缩
    
    使用截断 SVD (Truncated SVD) 对 KV 矩阵进行降维:
    - 原始: [seq_len, hidden_dim] → 压缩: [seq_len, rank] + [rank] + [rank, hidden_dim]
    - 压缩率 ≈ hidden_dim / rank
    """
    
    def __init__(self, rank: int = 256):
        """
        Args:
            rank: 压缩后的秩（维度）
        """
        self.rank = rank
        self.U: Optional[np.ndarray] = None
        self.S: Optional[np.ndarray] = None
        self.Vt: Optional[np.ndarray] = None
        self.original_shape: Optional[tuple] = None
        
    def compress(self, matrix: np.ndarray) -> dict:
        """
        对 KV Cache 进行低秩分解压缩
        
        Args:
            matrix: 输入矩阵，形状 [seq_len, hidden_dim]
        
        Returns:
            dict: 包含压缩结果的字典
        """
        self.original_shape = matrix.shape
        seq_len, hidden_dim = matrix.shape
        
        # SVD 分解
        # matrix ≈ U @ diag(S) @ Vt
        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        
        # 截断到指定 rank
        actual_rank = min(self.rank, len(S))
        self.U = U[:, :actual_rank]
        self.S = S[:actual_rank]
        self.Vt = Vt[:actual_rank, :]
        
        # 计算压缩比
        original_size = matrix.size * matrix.itemsize
        compressed_size = (self.U.size + self.S.size + self.Vt.size) * self.S.itemsize
        compression_ratio = original_size / compressed_size
        
        return {
            "U_shape": self.U.shape,
            "S_shape": self.S.shape,
            "Vt_shape": self.Vt.shape,
            "compression_ratio": compression_ratio,
            "original_size_mb": original_size / 1024 / 1024,
            "compressed_size_mb": compressed_size / 1024 / 1024,
            "memory_saved_mb": (original_size - compressed_size) / 1024 / 1024
        }
    
    def decompress(self) -> np.ndarray:
        """
        从压缩形式恢复原始矩阵
        
        Returns:
            恢复后的矩阵
        """
        if self.U is None or self.S is None or self.Vt is None:
            raise ValueError("请先调用 compress()")
        
        # 恢复: U @ diag(S) @ Vt
        return np.dot(self.U * self.S, self.Vt)
    
    def save_compressed(self, filepath: str):
        """保存压缩后的数据到文件"""
        if self.U is None:
            raise ValueError("请先调用 compress()")
        
        np.savez(
            filepath,
            U=self.U,
            S=self.S,
            Vt=self.Vt,
            original_shape=np.array(self.original_shape)
        )
        print(f"压缩数据已保存到: {filepath}")
    
    def load_compressed(self, filepath: str):
        """从文件加载压缩数据"""
        data = np.load(filepath, allow_pickle=True)
        self.U = data["U"]
        self.S = data["S"]
        self.Vt = data["Vt"]
        self.original_shape = tuple(data["original_shape"])
        print(f"已加载压缩数据，形状: U={self.U.shape}, S={self.S.shape}, Vt={self.Vt.shape}")


class StreamingKVCompressor:
    """
    流式 KV Cache 压缩器
    支持增量压缩，适合长对话场景
    """
    
    def __init__(self, rank: int = 128, seq_chunk: int = 512):
        """
        Args:
            rank: 压缩秩
            seq_chunk: 每个chunk的序列长度
        """
        self.rank = rank
        self.seq_chunk = seq_chunk
        self.chunks: list = []
        
    def add_chunk(self, kv_chunk: np.ndarray):
        """
        添加一个新的 KV chunk
        
        Args:
            kv_chunk: 形状 [chunk_size, hidden_dim]
        """
        compressor = KVCacheLowRank(rank=self.rank)
        result = compressor.compress(kv_chunk)
        self.chunks.append({
            "U": compressor.U,
            "S": compressor.S,
            "Vt": compressor.Vt,
            "result": result
        })
        
    def get_total_compression(self) -> dict:
        """获取总体压缩统计"""
        total_original = sum(c["result"]["original_size_mb"] for c in self.chunks)
        total_compressed = sum(c["result"]["compressed_size_mb"] for c in self.chunks)
        
        return {
            "num_chunks": len(self.chunks),
            "total_original_mb": total_original,
            "total_compressed_mb": total_compressed,
            "total_saved_mb": total_original - total_compressed,
            "avg_compression_ratio": total_original / total_compressed if total_compressed > 0 else 0
        }


def demo():
    """演示低秩压缩效果"""
    print("=" * 50)
    print("box-kvcache 低秩分解压缩演示")
    print("=" * 50)
    
    # 配置
    seq_len = 2048
    hidden_dim = 4096
    rank = 256
    
    print(f"\n模拟 KV Cache:")
    print(f"  形状: [{seq_len}, {hidden_dim}]")
    print(f"  数据类型: float16")
    print(f"  压缩后秩: {rank}")
    print(f"  理论压缩比: {hidden_dim / rank:.1f}x")
    
    # 生成模拟数据（模拟真实的 KV Cache 分布）
    np.random.seed(42)
    
    # 生成一个低秩的矩阵（模拟真实KV Cache）
    # 真实 KV Cache 通常有一定的低秩结构
    U_real = np.random.randn(seq_len, 512).astype(np.float16)
    S_real = np.random.rand(512).astype(np.float16) * 10
    Vt_real = np.random.randn(512, hidden_dim).astype(np.float16)
    kv_cache = np.dot(U_real * S_real, Vt_real).astype(np.float16)
    
    # 添加一些噪声
    kv_cache += np.random.randn(seq_len, hidden_dim).astype(np.float16) * 0.1
    
    original_size = kv_cache.nbytes / 1024 / 1024
    print(f"\n原始大小: {original_size:.2f} MB")
    
    # 压缩
    print(f"\n--- 低秩分解压缩 (rank={rank}) ---")
    compressor = KVCacheLowRank(rank=rank)
    result = compressor.compress(kv_cache)
    
    print(f"U 形状: {result['U_shape']}")
    print(f"S 形状: {result['S_shape']}")
    print(f"Vt 形状: {result['Vt_shape']}")
    print(f"压缩比: {result['compression_ratio']:.2f}x")
    print(f"压缩后大小: {result['compressed_size_mb']:.2f} MB")
    print(f"节省内存: {result['memory_saved_mb']:.2f} MB")
    
    # 恢复并评估质量
    restored = compressor.decompress()
    
    # 计算误差
    mse = np.mean((kv_cache - restored) ** 2)
    max_err = np.max(np.abs(kv_cache - restored))
    signal_power = np.mean(kv_cache ** 2)
    snr = 10 * np.log10(signal_power / mse)
    
    print(f"\n--- 恢复质量 ---")
    print(f"MSE: {mse:.6f}")
    print(f"最大误差: {max_err:.4f}")
    print(f"SNR: {snr:.2f} dB")
    
    # 对比不同 rank
    print("\n--- 不同 rank 的压缩效果 ---")
    print(f"{'Rank':<8} {'压缩比':<10} {'压缩后(MB)':<12} {'SNR(dB)':<10}")
    print("-" * 40)
    
    for test_rank in [64, 128, 256, 512]:
        comp = KVCacheLowRank(rank=test_rank)
        comp.compress(kv_cache)
        restored_test = comp.decompress()
        
        mse_t = np.mean((kv_cache - restored_test) ** 2)
        snr_t = 10 * np.log10(signal_power / mse_t) if mse_t > 0 else 100
        
        result_t = comp.compress(kv_cache)
        print(f"{test_rank:<8} {result_t['compression_ratio']:<10.2f} {result_t['compressed_size_mb']:<12.2f} {snr_t:<10.2f}")
    
    print("\n" + "=" * 50)
    print("结论: rank 128-256 在压缩比和精度间平衡较好")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="KV Cache 低秩分解压缩工具")
    parser.add_argument("--rank", type=int, default=256, help="压缩后秩")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--seq-len", type=int, default=2048, help="序列长度")
    parser.add_argument("--hidden-dim", type=int, default=4096, help="隐藏层维度")
    parser.add_argument("--save", type=str, help="保存压缩数据到文件")
    args = parser.parse_args()
    
    if args.demo:
        demo()
        return
    
    # 简单测试
    np.random.seed(42)
    seq_len, hidden_dim = args.seq_len, args.hidden_dim
    
    print(f"生成测试数据 [{seq_len}, {hidden_dim}]...")
    kv = np.random.randn(seq_len, hidden_dim).astype(np.float16)
    
    compressor = KVCacheLowRank(rank=args.rank)
    result = compressor.compress(kv)
    
    print(f"\n压缩结果:")
    print(f"  原始大小: {result['original_size_mb']:.2f} MB")
    print(f"  压缩后: {result['compressed_size_mb']:.2f} MB")
    print(f"  压缩比: {result['compression_ratio']:.2f}x")
    print(f"  节省: {result['memory_saved_mb']:.2f} MB")
    
    if args.save:
        compressor.save_compressed(args.save)


if __name__ == "__main__":
    main()
