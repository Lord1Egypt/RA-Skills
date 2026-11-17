# ================================================================
# 身份系统（Identity Engine）—— 【自设模块】
# ================================================================
# 角色拥有多重身份（职业身份、家庭角色、社会角色），
# 身份之间有和谐也有冲突。冲突产生持续的心理张力。
#
# 用法：在 Agent 初始化时加载 IdentityEngine，
#       定期检查冲突并将张力注入核心引擎。
# ================================================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class IdentityNode:
    """一个身份节点"""
    name: str              # 身份名称（"顾问"、"母亲"、"合伙人"）
    strength: float        # 身份强度 [0,1]（有多认同这个身份）
    priority: float        # 优先度 [0,1]（在冲突时有多优先）
    satisfaction: float = 0.5  # 身份满意度 [0,1]（在这个角色中感到多满意）
    threat_level: float = 0.0  # 该身份受到的威胁 [0,1]


@dataclass
class IdentityEngine:
    """
    身份引擎：管理多重身份及其冲突。

    核心洞察：
    - 身份冲突会产生持续的基底张力（不只是瞬时情绪）
    - 身份威胁比对个体的攻击更伤人（"你不配做顾问" > "你这个方案不行"）
    - 身份满意度的变化影响自尊
    """

    identities: List[IdentityNode] = field(default_factory=list)
    conflict_matrix: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # conflict_history 追踪冲突趋势（上升 vs 下降）
    conflict_history: List[float] = field(default_factory=list)

    def add_identity(self, name: str, strength: float = 0.7,
                     priority: float = 0.5, satisfaction: float = 0.5):
        """添加一个身份。"""
        node = IdentityNode(
            name=name, strength=strength,
            priority=priority, satisfaction=satisfaction,
        )
        self.identities.append(node)
        # 初始化冲突矩阵
        for other in self.identities:
            if other.name != name:
                self.conflict_matrix.setdefault(name, {})[other.name] = 0.0
                self.conflict_matrix.setdefault(other.name, {})[name] = 0.0

    def set_conflict(self, id1: str, id2: str, level: float):
        """
        设置两个身份之间的冲突水平 [0,1]。

        比如："顾问"和"朋友"之间的冲突 = 0.6
        意味着在这两个角色之间切换时，有 60% 的内在张力。
        """
        self.conflict_matrix.setdefault(id1, {})[id2] = max(0.0, min(1.0, level))
        self.conflict_matrix.setdefault(id2, {})[id1] = max(0.0, min(1.0, level))

    def total_conflict(self) -> float:
        """
        计算当前所有身份冲突的总和。

        返回值 [0,1]：0 = 完全和谐，1 = 极度撕裂。
        """
        if len(self.identities) < 2:
            return 0.0
        total = 0.0
        count = 0
        for i in range(len(self.identities)):
            for j in range(i + 1, len(self.identities)):
                a = self.identities[i]
                b = self.identities[j]
                conflict_level = self.conflict_matrix.get(a.name, {}).get(b.name, 0.0)
                # 冲突强度 = 身份强度乘积 × 冲突水平 × 优先度差
                tension = (conflict_level
                           * a.strength
                           * b.strength
                           * abs(a.priority - b.priority))
                total += tension
                count += 1
        return min(1.0, total / max(1, count) * 2.0)

    def threaten_identity(self, identity_name: str, threat_magnitude: float):
        """
        对某个身份施加威胁。

        触发：当角色感知到某个身份被攻击/否定时调用。
        返回一个可用于注入核心引擎的情绪向量。
        """
        for ident in self.identities:
            if ident.name == identity_name:
                ident.threat_level = min(1.0, ident.threat_level + threat_magnitude)
                ident.satisfaction = max(0.0, ident.satisfaction - threat_magnitude * 0.5)
                break

    def affirm_identity(self, identity_name: str, boost: float):
        """肯定某个身份（提升满意度和强度）。"""
        for ident in self.identities:
            if ident.name == identity_name:
                ident.satisfaction = min(1.0, ident.satisfaction + boost)
                ident.strength = min(1.0, ident.strength + boost * 0.3)
                ident.threat_level = max(0.0, ident.threat_level - boost * 0.5)
                break

    def get_emotion_vector(self) -> Dict[str, float]:
        """
        将当前身份状态转化为可供核心引擎消化的情绪向量。

        这个向量应该定期（或在事件处理前）注入 core.process_vector()。
        """
        tc = self.total_conflict()

        # 身份冲突 → 持续张力基底
        vector = {"tension_base": tc * 0.3}

        # 身份威胁 → shame_trigger（"我不配当X"）
        max_threat = max((i.threat_level for i in self.identities), default=0.0)
        if max_threat > 0.3:
            vector["shame_trigger"] = max_threat * 0.4

        # 低身份满意度 → 归属感下降
        min_satisfaction = min((i.satisfaction for i in self.identities), default=1.0)
        if min_satisfaction < 0.4:
            vector["belonging"] = -0.2 * (0.5 - min_satisfaction)

        # 高身份满意度 → 喜悦基线
        avg_satisfaction = (sum(i.satisfaction for i in self.identities) /
                            max(1, len(self.identities)))
        if avg_satisfaction > 0.7:
            vector["belonging"] = 0.15 * (avg_satisfaction - 0.5)

        return vector

    def snapshot(self) -> dict:
        """身份系统快照。"""
        return {
            "identities": [
                {"name": i.name, "strength": i.strength,
                 "priority": i.priority, "satisfaction": i.satisfaction,
                 "threat": i.threat_level}
                for i in self.identities
            ],
            "total_conflict": self.total_conflict(),
        }


# ── 预设：苏瑾的身份配置 ──

def sujin_identity() -> IdentityEngine:
    """苏瑾的多重身份配置"""
    engine = IdentityEngine()
    engine.add_identity("资深行业顾问", strength=0.9, priority=0.8, satisfaction=0.7)
    engine.add_identity("战略合作伙伴", strength=0.6, priority=0.6, satisfaction=0.5)
    # 顾问（理性距离） vs 朋友（情感亲近）存在天然冲突
    engine.set_conflict("资深行业顾问", "战略合作伙伴", 0.35)
    return engine
