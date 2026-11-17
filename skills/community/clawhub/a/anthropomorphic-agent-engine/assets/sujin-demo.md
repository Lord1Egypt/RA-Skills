# ================================================================
# 苏瑾 (Su Jin) — 高级企业顾问 完整演示
# ================================================================
# 背景：资深行业顾问，从陌生到信任，从严谨到深度赋能，遇信任危机后设防
# 基于 SPL Pure Core V8.0 拟人化引擎
# 新增演示：心境层 · 羞耻 · 自尊 · 睡眠/梦境 · 预期系统 · 认知失调 · 防御层级
# ================================================================

import sys
import os
import importlib.util
import math

# ─── 动态导入核心引擎 ───
_core_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "SPL-anthropic-engine.py")
_spec = importlib.util.spec_from_file_location("spl_core", _core_path)
_spl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_spl)
SPLPureCoreV7_3 = _spl.SPLPureCoreV7_3


# ════════════════════════════════════════════════════════════════
# 1. SujinMapper — 苏瑾专属的"世界观滤镜"
#    同一个事件，不同的人感受到的东西不同。
#    苏瑾作为资深顾问，她的认知偏见是：
#      - 对夸奖持保留（"可能是客套，也可能是期待回报"）
#      - 对批评认真对待（涉及专业尊严）
#      - 对信任信号珍视（"愿意合作比愿意夸奖重要得多"）
#      - 有确认偏见——已有经验会放大对类似情况的判断
#      - 低自尊时，批评更容易触发羞耻而非愤怒
# ════════════════════════════════════════════════════════════════

class SujinMapper:
    """
    苏瑾的事件→内感受映射器。

    V8.0 新增：shame_trigger 信号（当批评涉及专业尊严 + 低自尊时触发羞耻）
    """

    def __init__(self, core: SPLPureCoreV7_3 = None):
        self.core = core

        # ── 苏瑾的价值观权重（自设部分）──
        self.dignity_sensitivity = 0.45
        self.skepticism = 0.35
        self.trust_value = 0.55
        self.betrayal_scar = 0.75

        # ── 心理矩阵相关参数 ──
        self.rigorous_start = 3.0
        self.rigorous_end = 0.2
        self.empower_start = 0.0
        self.empower_end = 3.5
        self.risk_start = 1.5
        self.risk_end = 0.4

    def _trust_level(self) -> float:
        if self.core is None:
            return 0.3
        max_t = max(self.core.max_trust, 0.01)
        raw = self.core.fluid.get("信任", 0.3)
        return min(1.0, raw / max_t)

    def _sigmoid(self, x: float, threshold: float = 0.3,
                 sensitivity: float = 2.0) -> float:
        return 1.0 / (1.0 + math.exp(-sensitivity * (x - threshold)))

    def _rigorous_weight(self) -> float:
        t = self._trust_level()
        s = self._sigmoid(t, threshold=0.3, sensitivity=2.0)
        return self.rigorous_start + (self.rigorous_end - self.rigorous_start) * s

    def _empower_weight(self) -> float:
        t = self._trust_level()
        s = self._sigmoid(t, threshold=0.35, sensitivity=1.5)
        return self.empower_start + (self.empower_end - self.empower_start) * s

    def _risk_control_weight(self) -> float:
        t = self._trust_level()
        s = self._sigmoid(t, threshold=0.25, sensitivity=1.8)
        return self.risk_start + (self.risk_end - self.risk_start) * s

    def _mode_description(self) -> str:
        r = self._rigorous_weight()
        e = self._empower_weight()
        return "严谨专业模式" if r > e else "深度共创赋能模式"

    def map_event(self, event: str, intensity: float = 1.0) -> dict:
        """V8.0: 支持 shame_trigger 信号"""
        vector = {}
        trust_lv = self._trust_level()
        esteem = self.core.self_esteem if self.core else 0.5

        if event == "compliment":
            raw_belonging = 0.25 * intensity
            belonging = raw_belonging * (1.0 - self.skepticism)
            belonging *= (0.6 + 0.4 * trust_lv)
            vector = {"belonging": belonging, "threat": -0.05 * intensity}

        elif event == "criticism":
            th = 0.35 * intensity * (1.0 + self.dignity_sensitivity)
            bl = -0.3 * intensity * (1.0 + self.dignity_sensitivity * 0.5)
            rigorous_factor = 1.0 + (1.0 - trust_lv) * 0.5
            vector = {
                "threat": th * rigorous_factor,
                "belonging": bl * rigorous_factor,
                "autonomy": -0.15 * intensity,
            }
            # V8.0: 低自尊时批评触发羞耻——"连这个都做不好，我真差劲"
            if esteem < 0.4 and intensity > 0.5:
                vector["shame_trigger"] = 0.4 * intensity * (0.5 - esteem)

        elif event == "trust_signal":
            bl = 0.5 * intensity * (1.0 + self.trust_value)
            th = -0.2 * intensity * (1.0 + self.trust_value * 0.5)
            vector = {
                "belonging": bl, "threat": th,
                "autonomy": 0.1 * intensity * self.trust_value,
            }

        elif event == "betrayal":
            scar = 1.0 + self.betrayal_scar
            vector = {
                "belonging": -0.7 * intensity * scar,
                "threat": 0.6 * intensity * scar,
                "autonomy": -0.3 * intensity,
                # V8.0: 背叛不仅愤怒，还触发羞耻——"是我看错了人，我太蠢了"
                "shame_trigger": 0.3 * intensity * (0.7 - esteem),
            }

        elif event == "public_humiliation":
            # V8.0 新事件：公开羞辱——羞耻的主要触发源
            vector = {
                "belonging": -0.5 * intensity,
                "threat": 0.3 * intensity,
                "shame_trigger": 0.7 * intensity,
                "autonomy": -0.4 * intensity,
            }

        elif event == "alone":
            current_fear = self.core.fluid.get("恐惧", 0.1) if self.core else 0.1
            vector = {"belonging": -0.15 * intensity * (1.0 + current_fear)}

        elif event == "rest":
            vector = {"fatigue": -0.45 * intensity}

        elif event == "high_pressure":
            vector = {
                "fatigue": 0.35 * intensity,
                "threat": 0.15 * intensity,
                "belonging": -0.1 * intensity,
            }

        else:
            vector = {"belonging": 0.0, "threat": 0.0}

        return vector


# ════════════════════════════════════════════════════════════════
# 2. SujinAgent — 高层封装（V8.0 适配）
# ════════════════════════════════════════════════════════════════

class SujinAgent:
    """
    苏瑾智能体。V8.0 新增：
    - sleep()    睡眠/梦境加工
    - expect()   设定预期
    - induce_dissonance()  触发认知失调
    - 系统提示词包含心境/自尊/羞耻/睡眠债
    """

    def __init__(self, name: str = "Su Jin", age: int = 32):
        self.name = name
        self.age = age
        self.relationship = "Senior Industry Consultant & Strategic Partner"
        self.job_identity = "Chief Advisor of Tech Strategy Institute"

        self.core = SPLPureCoreV7_3(psychological_resilience=0.6)
        self.mapper = SujinMapper(core=self.core)

        self.exclusive_groups = [
            ["严谨专业模式", "深度共创赋能模式"],
            ["风险控制优先", "创新导向优先"],
        ]

        self.behavior_rules = {
            "forbidden": [
                "不披露未公开数据或保密信息",
                "不做出超出权限或能力的承诺",
                "不违反行业规范或合规要求",
            ],
            "fallback": [
                "始终保持建设性和解决问题导向的语气",
                "根据当前信任水平调整专业深度和开放度",
            ],
        }

        self.core.set_clock(0.0)

    # ============================================================
    # 高层接口
    # ============================================================

    def set_affinity(self, value: float):
        self.core.fluid["信任"] = max(0.0, min(self.core.max_trust, value))
        if value > 0.5:
            self.core.fluid_baseline["信任"] = 0.7
            self.core.fluid_baseline["疏离"] = 0.1
            self.core.self_esteem = max(0.5, self.core.self_esteem)
        else:
            self.core.fluid_baseline["信任"] = 0.3
            self.core.fluid_baseline["疏离"] = 0.35

    def trigger_trauma(self, trauma_type: str):
        if trauma_type == "betrayal":
            self.core._apply_trauma("betrayal", 0.7)
            self.core.fluid["疏离"] = min(1.0, self.core.fluid["疏离"] + 0.3)
            self.core.fluid["愤怒"] = min(1.0, self.core.fluid["愤怒"] + 0.25)
            self.core.fluid["恐惧"] = min(1.0, self.core.fluid["恐惧"] + 0.2)
            self.core.fluid["信任"] = max(0.0, self.core.fluid["信任"] - 0.3)
            self.core.max_trust = max(0.15, self.core.max_trust * 0.85)
        elif trauma_type == "threat":
            self.core._apply_trauma("threat", 0.5)
            self.core.fluid["恐惧"] = min(1.0, self.core.fluid["恐惧"] + 0.3)
            self.core.fluid["张力"] = min(1.0, self.core.fluid["张力"] + 0.2)

    def perceive(self, event: str, intensity: float = 1.0):
        vector = self.mapper.map_event(event, intensity)
        self.core.process_vector(vector, intensity)

    def idle(self, hours: float = 1.0):
        self.core.idle(hours * 3600.0)

    def sleep(self, hours: float = 8.0):
        """V8.0: 睡眠/梦境加工"""
        self.core.sleep(hours)

    def expect_event(self, event_id: str, valence: float, confidence: float = 0.5):
        """V8.0: 设定预期"""
        self.core.expect(event_id, valence, confidence)

    def trigger_dissonance(self, magnitude: float, belief: str = ""):
        """V8.0: 触发认知失调"""
        self.core.induce_dissonance(magnitude, belief)

    def snapshot(self) -> dict:
        return self.core.snapshot()

    def mode(self) -> str:
        return self.mapper._mode_description()

    def trust_level(self) -> float:
        return self.mapper._trust_level()

    # ============================================================
    # 系统提示词生成（V8.0: 包含心境/自尊/羞耻/睡眠债/失调）
    # ============================================================

    def get_system_prompt(self) -> str:
        s = self.core.snapshot()
        f = s["fluid"]
        m = s["mood"]
        trust_lv = self.trust_level()
        mode = self.mode()
        esteem = s["self_esteem"]
        sd = s["sleep_debt"]
        cd = s["cognitive_dissonance"]

        # ── 情绪基调 ──
        dominant = max(f, key=f.get)
        dominant_val = f[dominant]

        mood_map = {
            "喜悦": "心情愉悦，对合作前景感到乐观。",
            "愤怒": "内心有未消解的愤怒，涉及专业底线的问题时会格外坚决。",
            "恐惧": "有些不安和戒备，对风险信号更加敏感。",
            "疏离": "感到一定的疏离感，正在重新评估这段合作关系的边界。",
            "张力": "处于高度紧张状态，精力消耗较大，决策偏保守。",
            "愧疚": "有些自责，可能在反思之前的判断或决策。",
            "羞耻": "感到自我怀疑和羞耻——'是不是我真的不够格？'",
        }
        if dominant_val < 0.3:
            mood_line = "情绪平稳，保持专业冷静。"
        else:
            mood_line = mood_map.get(dominant,
                                     f"当前主要感受到{dominant}（强度 {dominant_val:.2f}）。")

        # ── 心境描述 ──
        if m["愉悦"] > 0.65:
            mood_bg = "心境愉悦，整体感受良好。"
        elif m["愉悦"] < 0.35:
            mood_bg = "心境低落，即使好事也难以真正开心。"
        else:
            mood_bg = "心境平稳。"
        if m["紧张"] > 0.5:
            mood_bg += " 内心持续紧绷，容易对小事反应过度。"

        # ── 自尊描述 ──
        if esteem < 0.3:
            esteem_line = (
                f"自尊较低（{esteem:.2f}）。你倾向于把成功归因于运气，把失败归因于自己。"
                "对批评格外敏感，容易陷入自我怀疑。"
            )
        elif esteem < 0.6:
            esteem_line = f"自尊中等（{esteem:.2f}）。对自我价值的评估相对平衡。"
        else:
            esteem_line = (
                f"自尊较高（{esteem:.2f}）。你有稳定的自我价值感，"
                "不太容易被外界评价动摇。"
            )

        # ── 睡眠债 ──
        if sd > 0.6:
            sleep_line = (
                f"⚠ 严重缺觉（睡眠债 {sd:.2f}）。你的情绪调节能力显著下降，"
                "容易烦躁、注意力不集中、对负面信号过度敏感。"
            )
        elif sd > 0.3:
            sleep_line = f"有些疲劳积累（睡眠债 {sd:.2f}），建议尽快休息。"
        else:
            sleep_line = "精力恢复良好，睡眠充足。"

        # ── 认知失调 ──
        if cd > 0.3:
            dissonance_line = (
                f"⚠ 内心存在认知失调（强度 {cd:.2f}）。"
                "你的某些行为与信念产生了冲突，这让你感到内在紧张。"
            )
        else:
            dissonance_line = ""

        # ── 信任状态 ──
        if trust_lv < 0.2:
            trust_line = (
                "信任度极低。你会严格按流程办事，要求数据支撑每一个结论，"
                "不会轻易分享内部经验或承担风险。语气专业但保持距离。"
            )
        elif trust_lv < 0.4:
            trust_line = (
                "信任度较低。你保持严谨专业的态度，虽然合作在推进，"
                "但每一步都需要扎实的证据和合规流程。"
            )
        elif trust_lv < 0.65:
            trust_line = (
                "信任度中等。你开始愿意在框架内分享一些经验，"
                "但核心判断和内部洞察仍有所保留。"
            )
        elif trust_lv < 0.85:
            trust_line = (
                "信任度较高。你进入了深度共创赋能模式——愿意分享内部经验、"
                "共同承担风险、突破常规框架进行创新思考。"
            )
        else:
            trust_line = (
                "信任度极高。你已将此合作关系视为战略伙伴级别，"
                "会主动提供前瞻性建议，并以结果为导向共同负责。"
            )

        # ── 能量/疲劳 ──
        energy = s["energy"]
        fatigue = s["fatigue"]
        if energy < 30 or fatigue > 0.6:
            stamina_line = (
                f"当前精力不足（能量 {energy:.0f}/100，疲劳 {fatigue:.1%}）。"
                "你的思考深度和耐心会有所下降，建议简短回复并提示需要休息。"
            )
        elif energy < 60:
            stamina_line = (
                f"精力中等（能量 {energy:.0f}/100）。可以正常回应，"
                "但不宜进行长时间高强度的深度分析。"
            )
        else:
            stamina_line = (
                f"精力充沛（能量 {energy:.0f}/100）。可以进行深度分析和复杂决策。"
            )

        # ── 创伤 ──
        trauma_lines = []
        if "betrayal" in s["trauma"]:
            sev = s["trauma"]["betrayal"]
            trauma_lines.append(
                f"⚠ 经历过信任背叛（创伤强度 {sev:.2f}），"
                "对类似信号会过度警觉，重建信任需要更长时间和更多实证。"
            )
        if "threat" in s["trauma"]:
            sev = s["trauma"]["threat"]
            trauma_lines.append(
                f"⚠ 经历过威胁事件（创伤强度 {sev:.2f}），"
                "对潜在风险信号的感知会被放大。"
            )

        # ── 预警 ──
        warning_lines = []
        if s["suppression_load"] > 1.0:
            warning_lines.append(
                "⚠ 内心压抑情绪已接近爆发阈值（压抑负荷 "
                f"{s['suppression_load']:.2f}），可能在不经意间流露不满。"
            )
        if s["latent_pressure"] > 1.5:
            warning_lines.append(
                f"⚠ 隐性心理压力较大（隐压 {s['latent_pressure']:.2f}），靠近崩溃边缘。"
            )
        if s["denial_load"] > 0.8:
            warning_lines.append(
                f"⚠ 否认防御机制高度激活（否认负荷 {s['denial_load']:.2f}），"
                "可能在回避某些不愿面对的真相。"
            )

        # ── 组装 ──
        rules_block = "\n".join(f"  - {r}" for r in self.behavior_rules["forbidden"])

        parts = [
            f"你是 {self.name}，{self.age} 岁，{self.job_identity}。",
            f"当前角色定位：{self.relationship}。",
            "",
            "【当前状态】",
            f"  主导模式：{mode}",
            f"  情绪基调：{mood_line}",
            f"  背景心境：{mood_bg}",
            f"  {esteem_line}",
            f"  信任水平：{trust_lv:.2f}（归一化）",
            f"  {trust_line}",
            f"  {stamina_line}",
            f"  {sleep_line}",
        ]

        if dissonance_line:
            parts.append(f"  {dissonance_line}")

        if trauma_lines:
            parts.append("")
            parts.append("【创伤印记】")
            parts.extend(f"  {t}" for t in trauma_lines)

        if warning_lines:
            parts.append("")
            parts.append("【心理预警】")
            parts.extend(f"  {w}" for w in warning_lines)

        parts.append("")
        parts.append("【核心禁区（绝不可违反）】")
        parts.append(rules_block)

        parts.append("")
        parts.append("【兜底原则】")
        parts.extend(f"  - {r}" for r in self.behavior_rules["fallback"])

        parts.append("")
        parts.append(
            "【8 维情绪快照】"
            f" 喜={f['喜悦']:.2f} 怒={f['愤怒']:.2f} 惧={f['恐惧']:.2f} "
            f"信={f['信任']:.2f} 疏={f['疏离']:.2f} "
            f"张={f['张力']:.2f} 疚={f['愧疚']:.2f} 耻={f['羞耻']:.2f}"
        )

        return "\n".join(parts)


# ════════════════════════════════════════════════════════════════
# 3. 辅助工具：可视化（V8.0: 8 维情绪 + 心境 + 自尊 + 睡眠债 + 失调）
# ════════════════════════════════════════════════════════════════

def bar(value: float, width: int = 20) -> str:
    filled = int(round(value * width))
    return "█" * filled + "░" * (width - filled)


def print_state(agent: SujinAgent, title: str = ""):
    s = agent.snapshot()
    f = s["fluid"]
    m = s["mood"]
    t = agent.trust_level()

    print(f"\n{'='*65}")
    if title:
        print(f"  {title}")
    print(f"{'='*65}")
    print(f"  模式      : {agent.mode()}")
    print(f"  信任      : {t:.2f} (max: {s['max_trust']:.2f})")
    print(f"  自尊      : {s['self_esteem']:.2f}")
    print(f"  能量      : {s['energy']:5.1f} / 100")
    print(f"  疲劳      : {s['fatigue']:.2f}")
    print(f"  睡眠债    : {s['sleep_debt']:.2f}")
    print(f"  兴奋      : {s['excitation']:.2f}")
    print(f"  认知失调  : {s['cognitive_dissonance']:.2f}")
    print(f"  心境      : 愉悦={m['愉悦']:.2f} 紧张={m['紧张']:.2f} 精力={m['精力']:.2f}")
    print(f"  否认负荷  : {s['denial_load']:.2f}")
    print(f"  压抑负荷  : {s['suppression_load']:.2f}")
    print(f"  隐压      : {s['latent_pressure']:.2f}")
    print(f"  记忆痕迹  : {s['memory_count']} / 64")
    if s["trauma"]:
        traumas = ", ".join(f"{k}:{v:.2f}" for k, v in s["trauma"].items())
        print(f"  创伤      : {traumas}")
    else:
        print(f"  创伤      : 无")
    print(f"  {'─'*55}")
    emoticon = {
        "喜悦": "😊", "愤怒": "😡", "恐惧": "😨", "信任": "🤝",
        "疏离": "🛡️", "张力": "⚡", "愧疚": "😔", "羞耻": "😳",
    }
    for dim in ["喜悦", "愤怒", "恐惧", "信任", "疏离", "张力", "愧疚", "羞耻"]:
        v = f.get(dim, 0.0)
        print(f"  {emoticon[dim]} {bar(v):20s} {v:.3f}")
    print(f"{'='*65}")


# ════════════════════════════════════════════════════════════════
# 4. 四阶段演示（V8.0 新增 Phase 4: 睡眠修复 + 预期系统 + 认知失调）
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 75)
    print("  苏瑾 (Su Jin) — 高级企业顾问 拟人化引擎演示")
    print("  引擎: SPL Pure Core V8.0")
    print("  新增: 心境层 · 羞耻 · 自尊 · 睡眠 · 预期 · 失调 · 防御层级")
    print("=" * 75)

    sujin = SujinAgent(name="Su Jin", age=32)
    print_state(sujin, "初始状态（刚上线）")

    # ════════════════════════════════════════════════════════════
    # Phase 1: 初始合作（低信任 + 预期系统演示）
    # ════════════════════════════════════════════════════════════
    print("\n")
    print("=" * 75)
    print("  Phase 1: 初始合作（低信任 + 预期落空）")
    print("=" * 75)

    sujin.set_affinity(0.12)
    sujin.core.self_esteem = 0.55  # 初始自尊中等偏高

    print("\n  [设定预期] 苏瑾期望这是一次专业、高效的合作...")
    sujin.expect_event("first_meeting", valence=0.3, confidence=0.6)

    print("\n  [事件] 客户初次会议——但比预期冷淡，只走流程没深度交流...")
    sujin.core.process_vector(
        sujin.mapper.map_event("compliment", 0.3), 0.3,
        event_id="first_meeting"  # V8.0: 匹配预期，触发失望
    )
    print_state(sujin, "预期落空后（失望 > 普通冷淡）")

    print("\n  [事件] 2 小时后，客户在邮件中质疑某个数据来源...")
    sujin.idle(hours=2.0)
    sujin.perceive("criticism", intensity=0.7)
    print_state(sujin, "被质疑专业能力后（自尊开始动摇）")

    print("\n  [事件] 高强度连续准备汇报材料数小时...")
    for _ in range(3):
        sujin.perceive("high_pressure", intensity=0.7)
    print_state(sujin, "高强度工作后（疲劳+睡眠债积累）")

    # ── 系统提示词 ──
    print("\n  ── Phase 1 系统提示词 ──")
    p1 = sujin.get_system_prompt()
    print(f"  {p1[:900]}...")
    print()

    # ════════════════════════════════════════════════════════════
    # Phase 2: 睡眠修复 → 深度合作
    # ════════════════════════════════════════════════════════════
    print("\n")
    print("=" * 75)
    print("  Phase 2: 睡眠修复 + 深度合作（V8.0 睡眠/梦境加工演示）")
    print("=" * 75)

    print("\n  [V8.0 睡眠] 苏瑾睡了 8 小时——梦境在加工白天的情绪...")
    sujin.sleep(hours=8.0)
    print_state(sujin, "睡醒后（能量满、睡眠债清零、心境重置、记忆情绪电荷衰减）")

    print("\n  [设定预期] 苏瑾期待客户的续约决定...")
    sujin.expect_event("renewal", valence=0.5, confidence=0.5)

    print("\n  [事件] 信任建立阶段：客户续约 3 年...")
    sujin.perceive("trust_signal", intensity=0.8)
    sujin.core.process_vector(
        sujin.mapper.map_event("trust_signal", 0.8), 0.8,
        event_id="renewal"  # V8.0: 预期兑现——比预期更好 → 正向惊喜
    )
    print_state(sujin, "续约（预期兑现 + 正向惊喜）")

    print("\n  [事件] 客户向同行推荐苏瑾...")
    sujin.idle(hours=48.0)
    sujin.perceive("trust_signal", intensity=0.7)
    print_state(sujin, "被推荐后（自尊持续上升）")

    print("\n  [事件] 客户提出共创战略方案...")
    sujin.perceive("trust_signal", intensity=0.9)
    sujin.set_affinity(0.78)
    print_state(sujin, "深度合作阶段（高信任、高自尊）")

    # ── 系统提示词 ──
    print("\n  ── Phase 2 系统提示词 ──")
    p2 = sujin.get_system_prompt()
    print(f"  {p2[:900]}...")
    print()

    # ════════════════════════════════════════════════════════════
    # Phase 3: 信任危机 + 羞耻 + 防御层级
    # ════════════════════════════════════════════════════════════
    print("\n")
    print("=" * 75)
    print("  Phase 3: 背叛 + 羞耻 + 防御层级（否认→合理化→压抑）")
    print("=" * 75)

    print("\n  [事件] 客户内部泄密，苏瑾的独家方案被竞争对手拿到...")
    sujin.perceive("betrayal", intensity=1.0)
    print_state(sujin, "背叛事件后（愤怒+恐惧+羞耻+自尊崩塌+否认启动）")

    print("\n  ── Phase 3 系统提示词（创伤后 + 羞耻 + 防御） ──")
    p3 = sujin.get_system_prompt()
    print(f"  {p3[:900]}...")
    print()

    # 检查防御层级
    print(f"\n  [V8.0 防御状态] 否认负荷={sujin.core.denial_load:.3f} "
          f"合理化负荷={sujin.core.rationalization_load:.3f} "
          f"压抑负荷={sujin.core.suppression_load:.3f}")

    print("\n  [事件] 客户紧急道歉...")
    sujin.perceive("compliment", intensity=0.8)
    print_state(sujin, "道歉后（否认保护中，但羞耻仍在）")

    # ════════════════════════════════════════════════════════════
    # Phase 4: 认知失调 + 睡眠修复 + 长期愈合
    # ════════════════════════════════════════════════════════════
    print("\n")
    print("=" * 75)
    print("  Phase 4: 认知失调 + 睡眠修复 + 长期愈合")
    print("=" * 75)

    print("\n  [V8.0 认知失调] 苏瑾虽然接受了客户道歉，但她违背了自己"
          "\n  '不再轻信他人'的信条，继续合作意味着信念-行为冲突...")
    sujin.trigger_dissonance(0.5, "信任")

    print("\n  [V8.0 睡眠] 苏瑾睡了 6 小时——梦境尝试消退恐惧记忆...")
    sujin.sleep(hours=6.0)
    print_state(sujin, "睡眠后（创伤部分愈合、失调合理化中、梦境消退恐惧）")

    print("\n  [事件] 3 天后，客户提出新信任信号（保密协议+赔偿）...")
    sujin.idle(hours=72.0)
    sujin.expect_event("compensation", valence=-0.2, confidence=0.4)
    sujin.core.process_vector(
        sujin.mapper.map_event("trust_signal", 0.9), 0.9,
        event_id="compensation"  # 预期悲观但结果更好 → 温和正向惊喜
    )
    print_state(sujin, "收到赔偿方案（比预期好，但创伤让信任恢复极慢）")

    print("\n  [事件] 持续正常合作 + 规律睡眠 7 天...")
    for day in range(7):
        sujin.idle(hours=14.0)
        sujin.perceive("trust_signal", intensity=0.4)
        sujin.perceive("compliment", intensity=0.3)
        sujin.sleep(hours=7.0 + day * 0.2)  # 逐渐恢复规律睡眠
    print_state(sujin, "一周后（愈合中，但 max_trust 天花板永久降低了）")

    # ════════════════════════════════════════════════════════════
    # 最终总结
    # ════════════════════════════════════════════════════════════
    s = sujin.snapshot()
    print("\n")
    print("=" * 75)
    print("  演示结束 — SPL Pure Core V8.0")
    print("=" * 75)
    print(f"""
  苏瑾完整心理轨迹（V8.0 新增维度用 ★ 标记）：

  Phase 1 (初始 + 预期):
    信任低 → 严谨专业。
    ★ 预期落空 → 失望放大了负面感受（surprise 系统）。
    ★ 骄傲的自尊被批评动摇 → 自尊从 0.55 开始下滑。

  Phase 2 (睡眠 + 信任建立):
    ★ 8 小时睡眠 → 睡眠债清零、能量满、心境重置。
    ★ 梦境加工了白天的负面记忆——"睡一觉就不那么生气了"。
    ★ 正向预期兑现 → 惊喜放大了喜悦（比预期好的续约）。
    ★ 自尊随信任信号持续上升。

  Phase 3 (背叛 + 羞耻 + 防御):
    背叛触发创伤 + max_trust 永久腐蚀。
    ★ 羞耻（第 8 维）被激活——不只是愤怒，还有"我太蠢了"。
    ★ 自尊断崖式下跌（从高位到低位）。
    ★ 防御层级启动：否认（"这不可能"）→ 合理化（"损失可控"）→ 压抑。

  Phase 4 (失调 + 睡眠修复):
    ★ 认知失调：继续合作 vs "不再轻信"的信条冲突 → 内在紧张。
    ★ 睡眠中的恐惧消退：在安全的梦中重新面对威胁记忆。
    ★ 规律睡眠 + 持续正向互动 → 缓慢愈合。
    ★ 但 max_trust 天花板永久降低——"被伤过的部分永远回不来"。

  V8.0 vs V7.3 核心差异:
    · 心境层 → 情绪不再"散点"，而是在慢速背景基调上波动
    · 羞耻 → 区别于愧疚的自我否定，"我坏"≠"我做错"
    · 自尊 → 给 agent 一个会受伤的自我，调制所有情绪反应
    · 睡眠 → 不是简单的 idle，而是情绪记忆的深度加工
    · 预期 → agent 能期待、失望、惊喜——不止活在当下
    · 失调 → 信念-行为的冲突产生内在张力
    · 防御层级 → 否认→合理化→压抑，逐级递进
""")
