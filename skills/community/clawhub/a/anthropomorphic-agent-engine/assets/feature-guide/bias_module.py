# ================================================================
# 认知偏见系统（Cognitive Bias Profile）—— 【自设模块】
# ================================================================
# 偏见是角色对信息的系统性扭曲，不同角色有不同的偏见图谱。
#
# 这是"角色的人格滤镜"——同样一件事，不同偏见的人感受完全不同。
# 偏见直接影响核心引擎的 _core_appraisal_gain（认知增益阶段）。
#
# 用法：在自定义 Mapper 或引擎外层集成 BiasProfile，
#       调用 apply_appraisal_bias() 调制 perceived vector。
# ================================================================

from dataclasses import dataclass
from typing import Dict


@dataclass
class BiasProfile:
    """
    角色认知偏见图谱。

    不是"有没有偏见"——所有人都有。这是"有什么样的偏见"。
    """

    # ── 注意偏差（Attentional Biases）──
    negativity_bias: float = 0.7        # 负面信息优先加工 [0,1]
    threat_vigilance: float = 0.5       # 威胁警觉（高→草木皆兵）[0,1]
    positivity_offset: float = 0.3      # 正面信息基线捕获 [0,1]

    # ── 解释偏差（Interpretive Biases）──
    confirmation_bias: float = 0.6      # 确认偏见（只信符合预期的）[0,1]
    hostile_attribution: float = 0.3    # 敌意归因（中性→恶意）[0,1]
    benevolent_attribution: float = 0.4 # 善意归因（中性→善意）[0,1]

    # ── 记忆偏差（Memory Biases）──
    mood_congruent_memory: float = 0.5  # 情绪一致性记忆（心情差→只想起坏事）
    peak_end_rule: float = 0.6          # 峰终定律权重（只记住高峰和结尾）
    rosy_retrospection: float = 0.3     # 玫瑰色回顾（美化过去）

    # ── 归因偏差（Attributional Biases）──
    self_serving_bias: float = 0.5      # 自我服务偏差（成功内归因→失败外归因）
    fundamental_attribution: float = 0.6 # 基本归因错误（别人的错是性格，自己的错是环境）

    # ── 社会偏差（Social Biases）──
    in_group_bias: float = 0.4          # 内群体偏好
    authority_bias: float = 0.3         # 权威服从倾向
    projection_bias: float = 0.4        # 投射倾向（自己怎么想就觉得别人也这么想）


class BiasEngine:
    """
    偏见引擎：把 BiasProfile 应用到认知处理管道。

    在核心引擎的 _core_appraisal_gain 之后、_vector_to_fluid 之前调用。
    """

    def __init__(self, profile: BiasProfile = None):
        self.profile = profile or BiasProfile()

    def apply_appraisal_bias(self, perceived: Dict[str, float],
                             world_model=None) -> Dict[str, float]:
        """
        对认知增益后的 perceived vector 施加偏见调制。

        调用时机：engine._core_appraisal_gain() 之后。

        Args:
            perceived: 认知增益后的内感受向量
            world_model: 可选的世界模型引用，用于确认偏见

        Returns:
            偏见调制后的向量
        """
        out = dict(perceived)
        p = self.profile

        # ── 负面偏差：放大 threat，放大负向 belonging ──
        if out.get("threat", 0.0) > 0:
            out["threat"] *= (1.0 + p.negativity_bias * 0.6)
        if out.get("belonging", 0.0) < 0:
            out["belonging"] *= (1.0 + p.negativity_bias * 0.4)

        # ── 威胁警觉：任何微弱 threat 都被放大 ──
        if 0 < out.get("threat", 0.0) < 0.2:
            out["threat"] *= (1.0 + p.threat_vigilance)

        # ── 敌意归因：对中性 threat 加码 ──
        if out.get("threat", 0.0) > 0 and p.hostile_attribution > 0.5:
            out["threat"] *= (1.0 + (p.hostile_attribution - 0.5))

        # ── 确认偏见：如果世界模型认为人不值得信任，threat 被强化 ──
        if world_model and world_model.trust_people < 0.3:
            if out.get("threat", 0.0) > 0:
                out["threat"] *= (1.0 + p.confirmation_bias * 0.5)
            if out.get("belonging", 0.0) > 0:
                out["belonging"] *= (1.0 - p.confirmation_bias * 0.3)

        return out

    def modulate_memory_strength(self, event_type: str, strength: float) -> float:
        """
        调制记忆写入强度——有偏见的记忆系统。

        负面事件记忆更牢固（负向偏见），符合预期的记忆更牢固（确认偏见）。
        """
        p = self.profile
        if event_type in ["insult", "betrayal", "criticism", "threat"]:
            strength *= (1.0 + p.negativity_bias)
        elif event_type in ["compliment", "trust_signal"]:
            # 正面事件，确认偏见影响编码
            strength *= (1.0 - p.confirmation_bias * 0.3)
        # 情绪一致性：如果负面偏见很高，负面记忆更牢固
        if p.negativity_bias > 0.6 and strength > 0:
            strength *= (1.0 + p.mood_congruent_memory * 0.2)
        return min(1.0, max(0.0, strength))

    def interpret_neutral(self, signal_valence: float) -> float:
        """
        解释中性信号：偏见决定了中性信号被推向正面还是负面。

        Args:
            signal_valence: 信号效价（~0 = 中性）

        Returns:
            被偏见扭曲后的效价
        """
        p = self.profile
        # 敌意归因 → 推向负面；善意归因 → 推向正面
        net_bias = p.hostile_attribution - p.benevolent_attribution
        return max(-1.0, min(1.0, signal_valence + net_bias * 0.5 * (1.0 - abs(signal_valence))))


# ── 预设角色模板 ──

def paranoid_bias() -> BiasProfile:
    """偏执型偏见——高威胁警觉 + 高敌意归因"""
    return BiasProfile(
        negativity_bias=0.9, threat_vigilance=0.85,
        hostile_attribution=0.8, benevolent_attribution=0.1,
        confirmation_bias=0.8, projection_bias=0.7,
        mood_congruent_memory=0.7,
    )


def optimistic_bias() -> BiasProfile:
    """乐观型偏见——高正面偏倚 + 低威胁警觉"""
    return BiasProfile(
        negativity_bias=0.3, threat_vigilance=0.2,
        positivity_offset=0.7, hostile_attribution=0.1,
        benevolent_attribution=0.7, rosy_retrospection=0.6,
        self_serving_bias=0.7,
    )


def depressive_bias() -> BiasProfile:
    """抑郁型偏见——高负面 + 低自我服务"""
    return BiasProfile(
        negativity_bias=0.9, threat_vigilance=0.7,
        positivity_offset=0.1, hostile_attribution=0.5,
        confirmation_bias=0.7, self_serving_bias=0.1,
        mood_congruent_memory=0.8, rosy_retrospection=0.1,
    )
