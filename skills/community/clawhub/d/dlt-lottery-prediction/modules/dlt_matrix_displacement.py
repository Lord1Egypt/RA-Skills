#!/usr/bin/env python3
"""
DLT矩阵位移分析 - 基于视频10
核心理论：7×5矩阵中号码的位移规律
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class DLTMatrixDisplacement:
    """
    7×5矩阵位移模型：
    
    把35个号码放入7行×5列的矩阵中：
    
        列0  列1  列2  列3  列4
    行0 [1]  [8]  [15] [22] [29]
    行1 [2]  [9]  [16] [23] [30]
    行2 [3]  [10] [17] [24] [31]
    行3 [4]  [11] [18] [25] [32]
    行4 [5]  [12] [19] [26] [33]
    行5 [6]  [13] [20] [27] [34]
    行6 [7]  [14] [21] [28] [35]
    
    分析号码在矩阵中的位置偏移规律：
    1. 行列分散度：号码是否均匀分布在矩阵各处
    2. 对角线倾向：号码是否沿对角线分布
    3. 位置频率：某些矩阵位置是否更容易出现号码
    
    注意：所有参数都有物理上界，确保不会超调
    """
    
    # 7×5矩阵定义
    MATRIX_ROWS = 7
    MATRIX_COLS = 5
    MATRIX = [
        [1,  8,  15, 22, 29],
        [2,  9,  16, 23, 30],
        [3,  10, 17, 24, 31],
        [4,  11, 18, 25, 32],
        [5,  12, 19, 26, 33],
        [6,  13, 20, 27, 34],
        [7,  14, 21, 28, 35],
    ]
    
    # 矩阵位置高频区（从历史数据统计，有界）
    HIGH_FREQ_CELLS = [(0, 2), (1, 3), (2, 1), (3, 4), (4, 2)]
    
    def __init__(self, historical_data=None):
        """
        初始化矩阵位移分析器
        
        Args:
            historical_data: 历史数据DataFrame（包含前区1-5列）
        """
        self.historical_data = historical_data
        self.position_frequency = None  # 矩阵位置频率
        if historical_data is not None:
            self._build_position_frequency()
    
    def _build_position_frequency(self):
        """从历史数据构建矩阵位置频率表"""
        df = self.historical_data
        front_numbers = df[['前区1','前区2','前区3','前区4','前区5']].values
        
        # 初始化位置频率矩阵（7x5）
        self.position_frequency = np.zeros((self.MATRIX_ROWS, self.MATRIX_COLS))
        
        for row in front_numbers:
            for n in row:
                n = int(n)
                pos = self._get_number_position(n)
                if pos is not None:
                    self.position_frequency[pos[0]][pos[1]] += 1
        
        # 归一化（有界：0-1）
        total = self.position_frequency.sum()
        if total > 0:
            self.position_frequency /= total
    
    def _get_number_position(self, n: int) -> Tuple[int, int]:
        """
        获取号码在矩阵中的位置
        
        Args:
            n: 号码（1-35）
            
        Returns:
            Tuple[int, int]: (行, 列) 或 None
        """
        for r in range(self.MATRIX_ROWS):
            for c in range(self.MATRIX_COLS):
                if self.MATRIX[r][c] == n:
                    return (r, c)
        return None
    
    def _get_combo_positions(self, combo: List[int]) -> List[Tuple[int, int]]:
        """
        获取组合中所有号码的位置
        
        Args:
            combo: 候选组合
            
        Returns:
            List[Tuple[int, int]]: 位置列表
        """
        positions = []
        for n in combo:
            pos = self._get_number_position(n)
            if pos:
                positions.append(pos)
        return positions
    
    def calculate_row_distribution(self, combo: List[int]) -> np.ndarray:
        """
        计算行分布（每行号码个数）
        
        Args:
            combo: 候选组合
            
        Returns:
            np.ndarray: 每行的号码个数（7维，有界：0-5）
        """
        row_counts = np.zeros(self.MATRIX_ROWS)
        positions = self._get_combo_positions(combo)
        for r, c in positions:
            row_counts[r] += 1
        return row_counts
    
    def calculate_col_distribution(self, combo: List[int]) -> np.ndarray:
        """
        计算列分布（每列号码个数）
        
        Args:
            combo: 候选组合
            
        Returns:
            np.ndarray: 每列的号码个数（5维，有界：0-5）
        """
        col_counts = np.zeros(self.MATRIX_COLS)
        positions = self._get_combo_positions(combo)
        for r, c in positions:
            col_counts[c] += 1
        return col_counts
    
    def calculate_dispersion_score(self, combo: List[int]) -> float:
        """
        计算矩阵分散度分数
        
        号码越分散在矩阵各处，分数越高
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 分散度分数（0-1，有界）
        """
        positions = self._get_combo_positions(combo)
        if len(positions) == 0:
            return 0.5  # 有界：中性值
        
        # 计算行列覆盖度
        row_counts = self.calculate_row_distribution(combo)
        col_counts = self.calculate_col_distribution(combo)
        
        # 使用的行数/列数越多越分散（有界：0-1）
        row_coverage = np.sum(row_counts > 0) / self.MATRIX_ROWS
        col_coverage = np.sum(col_counts > 0) / self.MATRIX_COLS
        
        return (row_coverage + col_coverage) / 2
    
    def calculate_diagonal_tendency(self, combo: List[int]) -> float:
        """
        计算对角线倾向度
        
        号码沿对角线分布的倾向
        
        对角线特征：|r - c| 相等的号码在同一条对角线上
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 对角线倾向度（0-1，有界）
        """
        positions = self._get_combo_positions(combo)
        if len(positions) < 2:
            return 0.0  # 有界：不足以判断
        
        # 计算位置差的和
        total_diag = 0.0
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # 对角线位置：|r1-c1| ≈ |r2-c2| 时加分
                diag_diff = abs((r1 - c1) - (r2 - c2))
                total_diag += 1.0 / (1.0 + diag_diff)
        
        return min(total_diag / 10, 1.0)  # 有界：不超过1.0
    
    def calculate_center_gravity(self, combo: List[int]) -> float:
        """
        计算中心引力分数
        
        号码越靠近矩阵中心（行3-4，列2-3），分数越高
        
        Args:
            combo: 候选组合
            
        Returns:
            float: 中心引力分数（0-1，有界）
        """
        positions = self._get_combo_positions(combo)
        if len(positions) == 0:
            return 0.5  # 有界：中性值
        
        # 中心位置权重
        center_row = (self.MATRIX_ROWS - 1) / 2  # 3.0
        center_col = (self.MATRIX_COLS - 1) / 2  # 2.0
        
        total_gravity = 0.0
        for r, c in positions:
            # 距离中心的距离（反向）
            dist = np.sqrt((r - center_row) ** 2 + (c - center_col) ** 2)
            # 距离越近，引力越强
            gravity = 1.0 / (1.0 + dist)
            total_gravity += gravity
        
        return min(total_gravity / 5, 1.0)  # 有界：不超过1.0
    
    def get_matrix_score(self, combo: List[int]) -> Dict[str, float]:
        """
        获取矩阵分析综合评分
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict[str, float]: 评分字典
        """
        return {
            'dispersion': self.calculate_dispersion_score(combo),
            'diagonal_tendency': self.calculate_diagonal_tendency(combo),
            'center_gravity': self.calculate_center_gravity(combo),
            'row_distribution': float(np.std(self.calculate_row_distribution(combo))),
            'col_distribution': float(np.std(self.calculate_col_distribution(combo))),
        }
    
    def get_matrix_report(self, combo: List[int]) -> Dict[str, Any]:
        """
        获取矩阵分析报告
        
        Args:
            combo: 候选组合
            
        Returns:
            Dict: 详细分析结果
        """
        positions = self._get_combo_positions(combo)
        row_counts = self.calculate_row_distribution(combo)
        col_counts = self.calculate_col_distribution(combo)
        
        return {
            'combo': combo,
            'positions': positions,
            'row_counts': row_counts.tolist(),
            'col_counts': col_counts.tolist(),
            'row_std': float(np.std(row_counts)),
            'col_std': float(np.std(col_counts)),
            'dispersion': self.calculate_dispersion_score(combo),
            'diagonal_tendency': self.calculate_diagonal_tendency(combo),
            'center_gravity': self.calculate_center_gravity(combo),
        }
