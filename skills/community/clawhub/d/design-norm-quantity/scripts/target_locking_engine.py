# -*- coding: utf-8 -*-
"""
度量衡目标锁定法引擎 v1.0
(MEG Target Locking Engine)

核心理念：从±3%目标倒推实现路径

目标分解：
±3% = 输入精度(±1%) + 模型精度(±1%) + 校准精度(±1%)

作者：度量衡智库
日期：2026-04-04
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PrecisionLevel(Enum):
    """精度等级"""
    LEVEL_1_TRADITIONAL = ("传统估算", 25.0)
    LEVEL_2_ML_ENHANCED = ("ML增强", 15.0)
    LEVEL_3_PROBABILISTIC = ("概率估算", 10.0)
    LEVEL_4_BIM_AUTO = ("BIM自动算量", 6.0)
    LEVEL_5_BIM_REALTIME = ("BIM+实时", 3.0)  # 目标达成
    
    def __init__(self, name_cn: str, target_error: float):
        self.name_cn = name_cn
        self.target_error = target_error


@dataclass
class TargetDecomposition:
    """目标分解"""
    total_target: float          # 总体目标 (±%)
    input_precision: float       # 输入精度 (±%)
    model_precision: float       # 模型精度 (±%)
    calibration_precision: float # 校准精度 (±%)
    
    @classmethod
    def for_target(cls, target: float) -> 'TargetDecomposition':
        """根据目标创建分解"""
        # 均匀分解
        part = target / 3
        return cls(
            total_target=target,
            input_precision=part,
            model_precision=part,
            calibration_precision=part
        )
    
    def check_feasibility(self) -> Tuple[bool, str]:
        """检查可行性"""
        if self.total_target > 25:
            return False, "目标过大，当前技术无法达成"
        if self.total_target < 1:
            return False, "目标过小，物理极限约束"
        if self.input_precision + self.model_precision + self.calibration_precision > self.total_target:
            return False, "分解精度之和超过目标"
        return True, "目标可达成"
        
    def get_required_methods(self) -> List[str]:
        """获取所需方法"""
        methods = []
        
        # 输入精度所需方法
        if self.input_precision <= 1.0:
            methods.append("BIM自动提取工程量")
            methods.append("实时市场价格")
        elif self.input_precision <= 3.0:
            methods.append("设计规范配比")
            methods.append("官方造价指标")
        else:
            methods.append("经验估算")
            
        # 模型精度所需方法
        if self.model_precision <= 1.0:
            methods.append("深度神经网络MEG-Net")
            methods.append("贝叶斯概率模型")
        elif self.model_precision <= 3.0:
            methods.append("XGBoost集成学习")
            methods.append("案例推理CBR")
        else:
            methods.append("传统回归模型")
            
        # 校准精度所需方法
        if self.calibration_precision <= 1.0:
            methods.append("实时市场校准")
            methods.append("企业定额对比")
        elif self.calibration_precision <= 3.0:
            methods.append("历史项目校准")
            methods.append("专家评审")
        else:
            methods.append("单点估算")
            
        return methods
        
    def to_dict(self) -> Dict:
        return {
            "total_target": f"±{self.total_target}%",
            "input_precision": f"±{self.input_precision}%",
            "model_precision": f"±{self.model_precision}%",
            "calibration_precision": f"±{self.calibration_precision}%",
            "methods": self.get_required_methods()
        }


@dataclass
class PrecisionGap:
    """精度差距分析"""
    current_level: PrecisionLevel
    target_level: PrecisionLevel
    gap: float
    methods_needed: List[str]
    estimated_effort: str  # 高/中/低
    
    @classmethod
    def analyze(cls, current: float, target: float) -> 'PrecisionGap':
        """分析精度差距"""
        # 确定当前和目标等级
        current_level = cls._find_closest_level(current)
        target_level = cls._find_closest_level(target)
        gap = current - target
        
        # 确定所需方法
        methods = []
        if gap > 5:
            methods = ["引入BIM自动算量", "升级神经网络", "实时数据对接"]
        elif gap > 2:
            methods = ["ML算法融合", "蒙特卡洛增强", "多源数据整合"]
        elif gap > 1:
            methods = ["超参数优化", "特征工程", "集成学习增强"]
        else:
            methods = ["微调模型", "增加训练数据"]
            
        # 评估工作量
        if gap > 10:
            effort = "高"
        elif gap > 5:
            effort = "中"
        else:
            effort = "低"
            
        return cls(
            current_level=current_level,
            target_level=target_level,
            gap=gap,
            methods_needed=methods,
            estimated_effort=effort
        )
        
    @staticmethod
    def _find_closest_level(error: float) -> PrecisionLevel:
        """找到最接近的精度等级"""
        levels = list(PrecisionLevel)
        closest = levels[0]
        min_diff = abs(error - closest.value[1])
        
        for level in levels:
            diff = abs(error - level.value[1])
            if diff < min_diff:
                min_diff = diff
                closest = level
                
        return closest


class TargetLockingEngine:
    """
    目标锁定引擎
    
    核心功能：
    1. 目标分解 - 将±3%分解为可执行的子目标
    2. 路径规划 - 规划从当前到目标的路径
    3. 进度跟踪 - 跟踪各子目标的达成情况
    4. 动态调整 - 根据实际情况动态调整
    """
    
    def __init__(self, target_precision: float = 3.0):
        self.target_precision = target_precision
        self.decomposition = TargetDecomposition.for_target(target_precision)
        self.is_feasible, self.feasibility_msg = self.decomposition.check_feasibility()
        
        # 路径规划
        self.path = self._plan_path()
        
    def _plan_path(self) -> List[Dict]:
        """规划实现路径"""
        path = []
        current_error = 25.0  # 从传统估算开始
        
        while current_error > self.target_precision:
            gap = PrecisionGap.analyze(current_error, self.target_precision)
            
            step = {
                "from": f"±{current_error}%",
                "to": f"±{max(gap.target_level.value[1], self.target_precision)}%",
                "gap": gap.gap,
                "level": gap.target_level.name_cn,
                "methods": gap.methods_needed,
                "effort": gap.estimated_effort
            }
            path.append(step)
            
            current_error = gap.target_level.value[1]
            
        return path
        
    def get_decomposition_report(self) -> str:
        """生成目标分解报告"""
        report = []
        report.append("=" * 60)
        report.append("目标锁定法 · ±3%精度分解报告")
        report.append("=" * 60)
        report.append("")
        report.append("[*] 总体目标: +-{:.1f}%".format(self.target_precision))
        report.append("[OK] 可行性: {}".format(self.feasibility_msg))
        report.append("")
        report.append("[=] 精度分解:")
        report.append(f"  ├─ 输入精度:   ±{self.decomposition.input_precision}%")
        report.append(f"  ├─ 模型精度:   ±{self.decomposition.model_precision}%")
        report.append(f"  └─ 校准精度:   ±{self.decomposition.calibration_precision}%")
        report.append("")
        report.append("[-] 所需方法:")
        for method in self.decomposition.get_required_methods():
            report.append("  - {}".format(method))
        report.append("")
        report.append("[>] 实现路径:")
        for i, step in enumerate(self.path):
            report.append(f"  {i+1}. {step['from']} → {step['to']} [{step['level']}]")
            report.append(f"     方法: {', '.join(step['methods'])}")
            report.append(f"     工作量: {step['effort']}")
            
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
        
    def lock_target(self, current_precision: float) -> Dict:
        """锁定目标，返回调整建议"""
        gap = PrecisionGap.analyze(current_precision, self.target_precision)
        
        return {
            "status": "locked" if current_precision <= self.target_precision else "unlocked",
            "current": f"±{current_precision}%",
            "target": f"±{self.target_precision}%",
            "gap": gap.gap,
            "level": gap.target_level.name_cn,
            "next_steps": gap.methods_needed,
            "effort": gap.estimated_effort
        }


class PrecisionTracker:
    """
    精度跟踪器
    
    跟踪各精度组件的达成情况
    """
    
    def __init__(self):
        self.input_precision = None
        self.model_precision = None
        self.calibration_precision = None
        self.history = []
        
    def update(self, component: str, precision: float, timestamp: str = None):
        """更新组件精度"""
        if component == "input":
            self.input_precision = precision
        elif component == "model":
            self.model_precision = precision
        elif component == "calibration":
            self.calibration_precision = precision
            
        self.history.append({
            "component": component,
            "precision": precision,
            "timestamp": timestamp
        })
        
    def get_total_precision(self) -> Optional[float]:
        """计算总体精度"""
        if all([self.input_precision, self.model_precision, self.calibration_precision]):
            return np.sqrt(
                self.input_precision**2 + 
                self.model_precision**2 + 
                self.calibration_precision**2
            )
        return None
        
    def get_report(self) -> str:
        """生成报告"""
        total = self.get_total_precision()
        
        report = []
        report.append("精度跟踪报告")
        report.append("-" * 40)
        report.append(f"输入精度: {f'±{self.input_precision}%' if self.input_precision else '未设置'}")
        report.append(f"模型精度: {f'±{self.model_precision}%' if self.model_precision else '未设置'}")
        report.append(f"校准精度: {f'±{self.calibration_precision}%' if self.calibration_precision else '未设置'}")
        report.append("-" * 40)
        report.append(f"总体精度 (RSS): {f'±{total:.2f}%' if total else '计算中...'}")
        
        return "\n".join(report)


def demo_target_locking():
    """演示目标锁定法"""
    print("=" * 60)
    print("目标锁定法引擎 v1.0")
    print("=" * 60)
    print()
    
    # 创建引擎
    engine = TargetLockingEngine(target_precision=3.0)
    
    # 输出分解报告
    print(engine.get_decomposition_report())
    
    # 锁定测试
    print()
    print("精度锁定测试:")
    print("-" * 40)
    
    test_precisions = [25.0, 15.0, 10.0, 6.0, 3.0, 2.5]
    
    for precision in test_precisions:
        result = engine.lock_target(precision)
        status = "[OK]" if result['status'] == 'locked' else "[>>]"
        print("  当前 {:>8} -> {} {}".format("+-{:.1f}%".format(precision), status, result['level']))
        
    # 精度跟踪演示
    print()
    print("精度跟踪演示:")
    print("-" * 40)
    
    tracker = PrecisionTracker()
    tracker.update("input", 1.5)
    tracker.update("model", 1.2)
    tracker.update("calibration", 0.8)
    
    print(tracker.get_report())
    
    print()
    print("=" * 60)
    print("目标锁定法演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    demo_target_locking()
