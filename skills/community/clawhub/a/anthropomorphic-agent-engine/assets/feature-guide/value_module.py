# ================================================================
# 价值观系统（Value Engine）—— 【自设模块】
# ================================================================
# 价值观是角色判断"什么是对/什么是好"的尺度。
# 当事件触碰价值观时，情绪反应会被放大——价值观冲突是深层痛苦的来源。
#
# 用法：在 Mapper 中引用 ValueEngine，
#       用 evaluate_event() 判定事件对价值观的影响，
#       将影响叠加到内感受向量中。
# ================================================================

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ValueProfile:
    """
    角色的价值观权重。

    这些不是开关（有没有）——是权重（有多看重）。
    每条价值观的权重决定它被触及时的情绪放大倍数。
    """

    # ── 核心价值 ──
    freedom: float = 0.8         # 自主/自由
    responsibility: float = 0.7  # 责任感
    dignity: float = 0.9         # 尊严
    intimacy: float = 0.6        # 亲密/连接
    security: float = 0.5        # 安全/稳定

    # ── 社会价值 ──
    justice: float = 0.6         # 公正/公平
    loyalty: float = 0.65        # 忠诚
    honesty: float = 0.7         # 诚实
    competence: float = 0.75     # 能力/专业水准

    # ── 发展价值 ──
    growth: float = 0.6          # 成长/进步
    creativity: float = 0.5      # 创造力
    legacy: float = 0.4          # 传承/影响


class ValueEngine:
    """
    价值观引擎：把事件映射到价值观影响。

    核心机制：
    1. evaluate_event() → 判定事件触碰了哪些价值观
    2. 价值观权重 × 影响强度 → 情绪放大系数
    3. 被触碰的价值观优先级 → 决定反应模式（抗争 vs 妥协）
    """

    def __init__(self, profile: ValueProfile = None):
        self.profile = profile or ValueProfile()
        # 价值观受威胁的历史
        self.threat_history: List[Dict[str, float]] = []

    def evaluate_event(self, event: str) -> Dict[str, float]:
        """
        评估一个事件对每条价值观的影响。

        返回值：{价值观名: 影响值}，[-1, 1]
          正值：价值观被肯定（如被尊重 → dignity +0.3）
          负值：价值观被威胁（如被强迫 → freedom -0.4）
        """
        impact = {}
        p = self.profile

        if event == "force_command":
            impact["freedom"] = -0.4 * p.freedom
            impact["dignity"] = -0.25 * p.dignity
            impact["autonomy"] = -0.35 * p.freedom

        elif event == "compliment":
            impact["dignity"] = 0.15 * p.dignity
            impact["competence"] = 0.2 * p.competence

        elif event == "public_praise":
            impact["dignity"] = 0.3 * p.dignity
            impact["competence"] = 0.35 * p.competence
            impact["legacy"] = 0.15 * p.legacy

        elif event == "betrayal":
            impact["security"] = -0.5 * p.security
            impact["loyalty"] = -0.6 * p.loyalty
            impact["honesty"] = -0.55 * p.honesty
            impact["intimacy"] = -0.5 * p.intimacy
            impact["dignity"] = -0.3 * p.dignity

        elif event == "trust_signal":
            impact["security"] = 0.3 * p.security
            impact["intimacy"] = 0.3 * p.intimacy
            impact["loyalty"] = 0.25 * p.loyalty

        elif event == "criticism":
            impact["dignity"] = -0.2 * p.dignity
            impact["competence"] = -0.3 * p.competence

        elif event == "injustice_witnessed":
            impact["justice"] = -0.5 * p.justice
            impact["dignity"] = -0.2 * p.dignity

        elif event == "achievement":
            impact["competence"] = 0.4 * p.competence
            impact["growth"] = 0.3 * p.growth
            impact["dignity"] = 0.2 * p.dignity

        elif event == "failure":
            impact["competence"] = -0.35 * p.competence
            impact["dignity"] = -0.25 * p.dignity
            impact["growth"] = 0.1 * p.growth  # 失败也是成长

        elif event == "moral_dilemma":
            # 道德困境同时威胁多条价值观
            impact["honesty"] = -0.3 * p.honesty
            impact["loyalty"] = -0.3 * p.loyalty
            impact["responsibility"] = -0.25 * p.responsibility

        # 记录威胁历史
        for k, v in impact.items():
            if v < -0.2:
                self.threat_history.append({k: v})
                if len(self.threat_history) > 50:
                    self.threat_history.pop(0)

        return impact

    def amplify_emotion(self, event: str, base_vector: Dict[str, float]) -> Dict[str, float]:
        """
        根据价值观影响放大基础情绪向量。

        调用时机：在 Mapper 生成基础向量后、注入引擎前。

        Args:
            event: 事件名
            base_vector: Mapper 生成的基础内感受向量

        Returns:
            被价值观权重放大后的向量
        """
        impact = self.evaluate_event(event)
        out = dict(base_vector)

        # 计算总价值观冲击
        total_impact = sum(abs(v) for v in impact.values())
        if total_impact > 0.5:
            # 高价值观冲击 → 放大所有情绪
            amp = 1.0 + total_impact * 0.5
            for k in out:
                out[k] *= amp

        # 具体价值观的定向调制
        dignity_impact = impact.get("dignity", 0.0)
        if dignity_impact < -0.1:
            # 尊严受威胁 → 愤怒放大（"这是对我的侮辱"）
            out["anger"] = out.get("anger", 0.0) + abs(dignity_impact) * 0.4
            out["shame_trigger"] = out.get("shame_trigger", 0.0) + abs(dignity_impact) * 0.3

        competence_impact = impact.get("competence", 0.0)
        if competence_impact < -0.1:
            # 能力被质疑 → 羞耻（"我不够好"）
            out["shame_trigger"] = out.get("shame_trigger", 0.0) + abs(competence_impact) * 0.35

        if competence_impact > 0.2:
            # 能力被认可 → 喜悦+自主
            out["belonging"] = out.get("belonging", 0.0) + competence_impact * 0.3
            out["autonomy"] = out.get("autonomy", 0.0) + competence_impact * 0.2

        return out

    def is_core_value_threatened(self, threshold: float = 0.3) -> bool:
        """是否有核心价值观受到威胁。"""
        for item in self.threat_history[-5:]:
            for v in item.values():
                if abs(v) > threshold:
                    return True
        return False

    def snapshot(self) -> dict:
        """价值观系统快照。"""
        return {
            "profile": {
                k: v for k, v in self.profile.__dict__.items()
            },
            "recent_threats": len(self.threat_history),
        }


# ── 预设：苏瑾的价值观配置 ──

def sujin_values() -> ValueProfile:
    """苏瑾的价值观权重——专业尊严最高，忠诚其次"""
    return ValueProfile(
        freedom=0.75, responsibility=0.8,
        dignity=0.95, intimacy=0.5,
        security=0.55, justice=0.6,
        loyalty=0.7, honesty=0.75,
        competence=0.9, growth=0.65,
    )
