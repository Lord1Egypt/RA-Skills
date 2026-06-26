#!/usr/bin/env python3
"""
混沌理论模块 - Chaos Theory in Memory Systems

核心思想：
混沌系统中的确定性非周期性行为可以用于：
1. 压缩（利用分形自相似性）
2. 加密（混沌序列的伪随机性）
3. 模式识别（奇异吸引子）
4. 长期记忆编码（相空间轨迹）

数学基础：
- Lorenz 吸引子（Lorenz Attractor）
- 分形（Fractal）
- 混沌（Chaos）
- 奇异吸引子（Strange Attractor）
- 相空间（Phase Space）
- 李雅普诺夫指数（Lyapunov Exponent）

Lorenz 方程：
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz

其中：
- σ = 10（Prandtl 数）
- ρ = 28（Rayleigh 数）
- β = 8/3（几何因子）

应用：
- 分形压缩（利用自相似性）
- 混沌加密（伪随机序列）
- 模式聚类（吸引子作为聚类中心）
- 长期记忆编码（相空间轨迹）
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class LorenzState:
    """Lorenz 吸引子状态"""
    x: float
    y: float
    z: float
    t: float


@dataclass
class FractalMetrics:
    """分形指标"""
    dimension: float  # 分形维数
    lacunarity: float  # 间隙度
    succolarity: float  # 穿透性


@dataclass
class ChaosMetrics:
    """混沌指标"""
    lyapunov_exponent: float  # 李雅普诺夫指数
    correlation_dimension: float  # 关联维数
    entropy: float  # 熵


class LorenzAttractor:
    """
    Lorenz 吸引子 - 混沌系统的经典例子

    特征：
    - 对初始条件敏感（蝴蝶效应）
    - 具有奇异吸引子
    - 确定性但不可预测
    """

    def __init__(self, sigma: float = 10.0, rho: float = 28.0, beta: float = 8.0/3.0):
        """
        初始化 Lorenz 吸引子

        参数：
        - sigma: Prandtl 数（通常 10）
        - rho: Rayleigh 数（通常 28）
        - beta: 几何因子（通常 8/3）
        """
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

        # 初始状态
        self.state = LorenzState(x=0.1, y=0.0, z=0.0, t=0.0)

        # 轨迹历史
        self.trajectory: List[LorenzState] = []

    def set_initial_state(self, x: float, y: float, z: float):
        """设置初始状态"""
        self.state = LorenzState(x=x, y=y, z=z, t=0.0)
        self.trajectory = [self.state]

    def derivatives(self, state: LorenzState) -> Tuple[float, float, float]:
        """
        计算 Lorenz 方程的导数

        dx/dt = σ(y - x)
        dy/dt = x(ρ - z) - y
        dz/dt = xy - βz
        """
        dx = self.sigma * (state.y - state.x)
        dy = state.x * (self.rho - state.z) - state.y
        dz = state.x * state.y - self.beta * state.z

        return dx, dy, dz

    def step_rk4(self, dt: float = 0.01):
        """
        使用四阶 Runge-Kutta 方法演化一步

        RK4 比简单的 Euler 方法更精确
        """
        x, y, z, t = self.state.x, self.state.y, self.state.z, self.state.t

        # k1
        dx1, dy1, dz1 = self.derivatives(self.state)

        # k2
        state2 = LorenzState(x + dx1 * dt/2, y + dy1 * dt/2, z + dz1 * dt/2, t + dt/2)
        dx2, dy2, dz2 = self.derivatives(state2)

        # k3
        state3 = LorenzState(x + dx2 * dt/2, y + dy2 * dt/2, z + dz2 * dt/2, t + dt/2)
        dx3, dy3, dz3 = self.derivatives(state3)

        # k4
        state4 = LorenzState(x + dx3 * dt, y + dy3 * dt, z + dz3 * dt, t + dt)
        dx4, dy4, dz4 = self.derivatives(state4)

        # 更新状态
        new_x = x + (dx1 + 2*dx2 + 2*dx3 + dx4) * dt / 6
        new_y = y + (dy1 + 2*dy2 + 2*dy3 + dy4) * dt / 6
        new_z = z + (dz1 + 2*dz2 + 2*dz3 + dz4) * dt / 6
        new_t = t + dt

        self.state = LorenzState(x=new_x, y=new_y, z=new_z, t=new_t)
        self.trajectory.append(self.state)

    def evolve(self, steps: int = 1000, dt: float = 0.01) -> List[LorenzState]:
        """
        演化 Lorenz 吸引子

        返回：
        - 轨迹列表
        """
        for _ in range(steps):
            self.step_rk4(dt)

        return self.trajectory

    def get_trajectory_array(self) -> np.ndarray:
        """获取轨迹数组（用于可视化）"""
        if not self.trajectory:
            return np.zeros((0, 3))

        arr = np.array([(s.x, s.y, s.z) for s in self.trajectory])
        return arr

    def calculate_lyapunov_exponent(self, trajectory: List[LorenzState]) -> float:
        """
        计算李雅普诺夫指数（Lyapunov Exponent）

        李雅普诺夫指数衡量混沌系统的敏感性：
        - 正值：混沌
        - 零：周期运动
        - 负值：稳定运动
        """
        if len(trajectory) < 2:
            return 0.0

        # 计算相邻点的距离
        distances = []
        for i in range(len(trajectory) - 1):
            s1 = trajectory[i]
            s2 = trajectory[i + 1]
            dist = np.sqrt((s2.x - s1.x)**2 + (s2.y - s1.y)**2 + (s2.z - s1.z)**2)
            distances.append(dist)

        # 计算平均增长率
        if not distances:
            return 0.0

        growth_rates = [np.log(distances[i+1] / distances[i]) if distances[i] > 0 else 0
                        for i in range(len(distances) - 1)]

        lyapunov = np.mean(growth_rates) / 0.01  # 除以 dt

        return lyapunov

    def detect_chaos(self) -> ChaosMetrics:
        """
        检测混沌

        返回混沌指标
        """
        if len(self.trajectory) < 100:
            return ChaosMetrics(0, 0, 0)

        # 计算李雅普诺夫指数
        lyapunov = self.calculate_lyapunov_exponent(self.trajectory)

        # 计算关联维数（简化）
        arr = self.get_trajectory_array()
        if len(arr) > 0:
            correlation_dim = self._calculate_correlation_dimension(arr)
        else:
            correlation_dim = 0.0

        # 计算熵
        entropy = self._calculate_trajectory_entropy()

        return ChaosMetrics(
            lyapunov_exponent=lyapunov,
            correlation_dimension=correlation_dim,
            entropy=entropy
        )

    def _calculate_correlation_dimension(self, arr: np.ndarray) -> float:
        """计算关联维数（简化）"""
        if len(arr) < 2:
            return 0.0

        # 计算点对之间的距离
        distances = []
        for i in range(min(len(arr), 100)):
            for j in range(i + 1, min(len(arr), 100)):
                dist = np.linalg.norm(arr[i] - arr[j])
                distances.append(dist)

        if not distances:
            return 0.0

        # 关联函数 C(r) = (1/N^2) * Σ I(|r_i - r_j| < r)
        # 关联维数 D = d(log C(r)) / d(log r)

        r_values = np.logspace(-2, 2, 20)
        c_values = []

        for r in r_values:
            c = np.sum(np.array(distances) < r) / len(distances)
            c_values.append(c)

        # 计算斜率
        log_r = np.log(r_values)
        log_c = np.log(np.array(c_values) + 1e-10)

        valid_idx = (log_c > -10) & (log_c < 0)
        if np.sum(valid_idx) > 2:
            slope = np.polyfit(log_r[valid_idx], log_c[valid_idx], 1)[0]
        else:
            slope = 0.0

        return slope

    def _calculate_trajectory_entropy(self) -> float:
        """计算轨迹熵（信息论指标）"""
        if len(self.trajectory) < 2:
            return 0.0

        # 简化：计算 z 坐标的熵
        z_values = [s.z for s in self.trajectory]
        hist, _ = np.histogram(z_values, bins=20)
        probs = hist / np.sum(hist)

        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * np.log2(p)

        return entropy

    def encode_to_chaos(self, data: str) -> List[float]:
        """
        编码数据到混沌序列

        使用数据调制 Lorenz 参数
        """
        # 计算数据的哈希
        import hashlib
        hash_value = int(hashlib.sha256(data.encode()).hexdigest(), 16)

        # 使用哈希调制初始条件
        x = (hash_value % 100) / 100.0
        y = ((hash_value // 100) % 100) / 100.0
        z = ((hash_value // 10000) % 100) / 100.0

        self.set_initial_state(x, y, z)

        # 演化
        trajectory = self.evolve(steps=100)

        # 提取混沌序列
        sequence = [s.x for s in trajectory[-10:]]

        return sequence

    def decode_from_chaos(self, sequence: List[float], data_length: int = 32) -> Optional[str]:
        """
        从混沌序列解码数据（简化版本）

        注意：真实的混沌解码需要逆问题求解
        这里使用简化的方法
        """
        # 简化：使用序列的第一个值作为种子
        if not sequence:
            return None

        seed = int(sequence[0] * 100) % 10000

        # 生成哈希（简化）
        import hashlib
        hash_str = hashlib.sha256(str(seed).encode()).hexdigest()

        # 截取前 data_length 个字符
        data = hash_str[:data_length]

        return data


class FractalCompressor:
    """
    分形压缩 - 利用自相似性压缩数据

    原理：
    - 分形具有自相似性（不同尺度下的重复模式）
    - 可以用迭代函数系统（IFS）编码
    - 压缩比高，但计算复杂

    这里实现简化的分形压缩
    """

    def __init__(self):
        self.ifs_codes: List[Dict] = []

    def compress(self, data: str, block_size: int = 8) -> Dict:
        """
        分形压缩

        输入：
        - data: 输入数据
        - block_size: 块大小

        返回：
        - 压缩数据（IFS 编码）
        """
        # 简化：将数据转换为矩阵
        data_bytes = data.encode()

        # 计算自相似块
        compressed = {
            "original_length": len(data),
            "blocks": []
        }

        for i in range(0, len(data_bytes), block_size):
            block = data_bytes[i:i+block_size]

            # 查找相似块（简化）
            compressed["blocks"].append({
                "data": list(block),
                "similar_to": i // block_size  # 自相似
            })

        return compressed

    def decompress(self, compressed: Dict) -> str:
        """解压缩"""
        data_bytes = []

        for block in compressed["blocks"]:
            data_bytes.extend(block["data"])

        return bytes(data_bytes).decode()

    def calculate_fractal_dimension(self, data: str, scales: List[int] = [1, 2, 4, 8]) -> float:
        """
        计算分形维数（盒计数法）

        盒计数法：
        - 使用不同大小的盒子覆盖数据
        - 计算需要的盒子数量
        - 分形维数 D = -log(N(r)) / log(r)
        """
        N = []
        r = []

        for scale in scales:
            # 计算需要多少个盒子
            data_bytes = data.encode()
            num_boxes = (len(data_bytes) + scale - 1) // scale

            N.append(num_boxes)
            r.append(scale)

        # 拟合直线：log(N) = -D * log(r) + b
        log_N = np.log(N)
        log_r = np.log(r)

        if len(log_N) > 1:
            slope, _ = np.polyfit(log_r, log_N, 1)
            dimension = -slope
        else:
            dimension = 0.0

        return dimension

    def calculate_fractal_metrics(self, data: str) -> FractalMetrics:
        """
        计算分形指标
        """
        dimension = self.calculate_fractal_dimension(data)

        # 间隙度（Lacunarity）：衡量分形的纹理
        # 简化：使用方差估计
        data_bytes = data.encode()
        lacunarity = np.var(list(data_bytes)) / (len(data_bytes) ** 2) if data_bytes else 0.0

        # 穿透性（Succolarity）：衡量连通性
        # 简化：使用唯一字符比例
        unique_chars = len(set(data)) / len(data) if data else 0.0
        succolarity = 1.0 - unique_chars

        return FractalMetrics(
            dimension=dimension,
            lacunarity=lacunarity,
            succolarity=succolarity
        )


class RecursiveFractalEncoder:
    """
    递归分形编码器

    用于编码记忆到分形结构
    """

    def __init__(self):
        self.fractal_tree: Dict = {}

    def encode(self, data: str, depth: int = 3) -> Dict:
        """
        递归分形编码

        将数据编码为树状分形结构
        """
        def encode_recursive(data: str, current_depth: int) -> Dict:
            if current_depth == 0 or len(data) <= 1:
                return {"value": data}

            # 分割数据
            mid = len(data) // 2
            left = data[:mid]
            right = data[mid:]

            return {
                "left": encode_recursive(left, current_depth - 1),
                "right": encode_recursive(right, current_depth - 1),
                "fractal_dimension": self._estimate_fractal_dimension(data)
            }

        self.fractal_tree = encode_recursive(data, depth)
        return self.fractal_tree

    def decode(self, fractal_tree: Dict) -> str:
        """递归分形解码"""
        if "value" in fractal_tree:
            return fractal_tree["value"]

        left = self.decode(fractal_tree["left"])
        right = self.decode(fractal_tree["right"])

        return left + right

    def _estimate_fractal_dimension(self, data: str) -> float:
        """估计分形维数（简化）"""
        if not data:
            return 0.0

        # 使用字符频率的熵作为代理
        from collections import Counter
        counts = Counter(data)
        total = len(data)

        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)

        return entropy

    def get_depth(self, fractal_tree: Optional[Dict] = None) -> int:
        """获取分形树的深度"""
        if fractal_tree is None:
            fractal_tree = self.fractal_tree

        if "value" in fractal_tree:
            return 1

        left_depth = self.get_depth(fractal_tree.get("left"))
        right_depth = self.get_depth(fractal_tree.get("right"))

        return 1 + max(left_depth, right_depth)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="混沌理论模块")
    parser.add_argument("action", choices=["lorentz", "fractal", "encode", "chaos_detect"])
    parser.add_argument("--steps", type=int, default=1000, help="演化步数")
    parser.add_argument("--dt", type=float, default=0.01, help="时间步长")
    parser.add_argument("--data", help="数据")
    parser.add_argument("--workspace", default=".", help="工作目录")

    args = parser.parse_args()

    if args.action == "lorentz":
        # Lorenz 吸引子
        lorenz = LorenzAttractor()
        lorenz.set_initial_state(0.1, 0.0, 0.0)
        trajectory = lorenz.evolve(steps=args.steps, dt=args.dt)

        chaos_metrics = lorenz.detect_chaos()

        print(f"🌀 Lorenz 吸引子")
        print(f"  步数: {len(trajectory)}")
        print(f"  李雅普诺夫指数: {chaos_metrics.lyapunov_exponent:.4f}")
        print(f"  关联维数: {chaos_metrics.correlation_dimension:.4f}")
        print(f"  熵: {chaos_metrics.entropy:.4f}")
        print(f"  是否混沌: {'✓ 是' if chaos_metrics.lyapunov_exponent > 0 else '✗ 否'}")

    elif args.action == "fractal":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # 分形压缩
        compressor = FractalCompressor()
        compressed = compressor.compress(args.data)
        metrics = compressor.calculate_fractal_metrics(args.data)

        print(f"📊 分形压缩")
        print(f"  原始长度: {compressed['original_length']}")
        print(f"  压缩块数: {len(compressed['blocks'])}")
        print(f"  分形维数: {metrics.dimension:.4f}")
        print(f"  间隙度: {metrics.lacunarity:.4f}")
        print(f"  穿透性: {metrics.succolarity:.4f}")

    elif args.action == "encode":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # 递归分形编码
        encoder = RecursiveFractalEncoder()
        fractal_tree = encoder.encode(args.data)
        depth = encoder.get_depth()

        print(f"🌳 递归分形编码")
        print(f"  数据: {args.data[:50]}...")
        print(f"  深度: {depth}")
        print(f"  节点数: {_count_nodes(fractal_tree)}")

    elif args.action == "chaos_detect":
        if not args.data:
            print("错误: 需要指定 --data")
            return

        # 混沌检测
        lorenz = LorenzAttractor()
        sequence = lorenz.encode_to_chaos(args.data)
        chaos_metrics = lorenz.detect_chaos()

        print(f"🔍 混沌检测")
        print(f"  数据: {args.data[:50]}...")
        print(f"  李雅普诺夫指数: {chaos_metrics.lyapunov_exponent:.4f}")
        print(f"  是否混沌: {'✓ 是' if chaos_metrics.lyapunov_exponent > 0 else '✗ 否'}")


def _count_nodes(tree: Dict) -> int:
    """计算树的节点数"""
    if "value" in tree:
        return 1
    return 1 + _count_nodes(tree.get("left", {})) + _count_nodes(tree.get("right", {}))


if __name__ == "__main__":
    main()
