# ================================================================
# 世界模型系统（World Model）—— 【自设模块】
# ================================================================
# 这是角色对"世界是什么样的"的基本信念，不是通用心理构成。
# 不同角色有不同的世界模型：
#   - 乐观者：trust_people=0.8, effort_pays_off=0.9
#   - 悲观者：trust_people=0.2, effort_pays_off=0.3
#   - 创伤后：trust_people=0.1, relationship_stability=0.2
#
# 用法：实例化 WorldModel 后，在 NarrativeMapper 或自定义 Mapper
#       中使用 model.beliefs 来调制事件→内感受的翻译。
# ================================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class WorldModel:
    """
    角色的内在工作模型（Internal Working Model）。

    这些是角色对世界的"默认假设"，构成了其认知框架的基础。
    世界模型通过以下方式影响心理：
    1. 调制 NarrativeMapper 的事件翻译
    2. 决定对模糊信号的解释方向（善意 vs 恶意）
    3. 影响预测误差的学习率（确认偏见）
    """

    # ── 基本信念 ──
    trust_people: float = 0.6              # 对他人可信度的一般预期 [0,1]
    relationship_stability: float = 0.6    # 关系是否稳定持久 [0,1]
    effort_pays_off: float = 0.7           # 努力是否有回报 [0,1]
    authority_reliability: float = 0.5     # 权威是否可信 [0,1]
    conflict_danger: float = 0.6           # 冲突的危险程度 [0,1]

    # ── 认知风格 ──
    ambiguity_intolerance: float = 0.4     # 对模糊性的不容忍度 [0,1]
    locus_of_control: float = 0.5          # 内控倾向（>0.5=内控，<0.5=外控）
    openness_to_experience: float = 0.6    # 对新经验的开放度 [0,1]

    # ── 学习参数 ──
    world_learning_rate: float = 0.08      # 世界模型更新速率（人格塑性）
    world_decay: float = 0.01              # 信念稳定性（抗改变）
    negativity_bias_in_learning: float = 0.7  # 负面事件的学习权重

    # ── 历史预测误差（经验学习） ──
    prediction_errors: List[Dict[str, float]] = field(default_factory=list)
    MAX_ERROR_HISTORY: int = 20

    def record_prediction_error(self, domain: str, error: float):
        """记录一次预测误差，用于经验学习。"""
        self.prediction_errors.append({"domain": domain, "error": error, "count": 1})
        if len(self.prediction_errors) > self.MAX_ERROR_HISTORY:
            self.prediction_errors.pop(0)

    def update_belief(self, domain: str, experience: float):
        """
        根据一次经验更新世界信念。

        Args:
            domain: 信念域（"trust_people", "effort_pays_off" 等）
            experience: 本次经验值 [0,1]（如实际他人可信度）
        """
        if not hasattr(self, domain):
            return
        current = getattr(self, domain)
        # 负面经验学习权重更高（负向偏见）
        if experience < current:
            lr = self.world_learning_rate * self.negativity_bias_in_learning
        else:
            lr = self.world_learning_rate * (1.0 - self.negativity_bias_in_learning * 0.5)
        # 向经验方向移动，但受 decay 约束（稳定性）
        new_value = current + lr * (experience - current) * (1.0 - self.world_decay)
        setattr(self, domain, max(0.0, min(1.0, new_value)))

    def interpret_ambiguity(self, signal_valence: float) -> float:
        """
        解释模糊信号。

        高 trust_people → 中性信号偏向正面
        低 trust_people → 中性信号偏向负面
        高 ambiguity_intolerance → 极端化解释（非黑即白）
        """
        trust_bias = (self.trust_people - 0.5) * 2.0  # [-1, 1]
        # 信任越高 → 模糊信号越被正面解读
        adjusted = signal_valence + trust_bias * 0.3 * (1.0 - abs(signal_valence))
        # 不容忍模糊 → 推向极端
        if abs(signal_valence) < 0.3:
            push = self.ambiguity_intolerance * 0.5
            adjusted = push if adjusted > 0 else -push
        return max(-1.0, min(1.0, adjusted))

    def snapshot(self) -> dict:
        """返回世界模型的快照。"""
        return {
            "beliefs": {
                "trust_people": self.trust_people,
                "relationship_stability": self.relationship_stability,
                "effort_pays_off": self.effort_pays_off,
                "authority_reliability": self.authority_reliability,
                "conflict_danger": self.conflict_danger,
            },
            "cognitive_style": {
                "ambiguity_intolerance": self.ambiguity_intolerance,
                "locus_of_control": self.locus_of_control,
                "openness_to_experience": self.openness_to_experience,
            },
            "error_count": len(self.prediction_errors),
        }


# ── 预设角色模板 ──

def optimistic_world() -> WorldModel:
    """乐观者世界模型"""
    return WorldModel(
        trust_people=0.8, effort_pays_off=0.9,
        relationship_stability=0.75, authority_reliability=0.6,
        conflict_danger=0.3, ambiguity_intolerance=0.2,
        locus_of_control=0.7, openness_to_experience=0.8,
    )


def pessimistic_world() -> WorldModel:
    """悲观者世界模型"""
    return WorldModel(
        trust_people=0.3, effort_pays_off=0.3,
        relationship_stability=0.3, authority_reliability=0.3,
        conflict_danger=0.8, ambiguity_intolerance=0.5,
        locus_of_control=0.3, openness_to_experience=0.3,
    )


def traumatized_world() -> WorldModel:
    """创伤后世界模型（信任崩塌）"""
    return WorldModel(
        trust_people=0.1, effort_pays_off=0.4,
        relationship_stability=0.15, authority_reliability=0.2,
        conflict_danger=0.9, ambiguity_intolerance=0.7,
        locus_of_control=0.4, openness_to_experience=0.2,
        negativity_bias_in_learning=0.95,
    )
