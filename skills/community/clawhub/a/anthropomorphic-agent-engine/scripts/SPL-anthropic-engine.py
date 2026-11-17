import time
import math
import json
import os
import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Union


# ================================================================
# 阅读入口 —— 字段语义与演化式不在此定义
#
# 本文件实现 SPL Pure Core V8.0 心智动力学，字段名均来自 SPL 理论。
# 建议先读 docs/agent-standard.md 再读代码：
#   §4.1-4.2  输入：内感受向量字段、叙事事件词表、强度缩放
#   §5.1      快照键集（规范性：[主] 23 键 / [未] 15 键）
#   §5.2-5.4  fluid（8 键）· mood（3 键）· trauma_state（[主] 独有）
#   §5.7      标量状态：suppression_load / denial_load /
#             rationalization_load / latent_pressure / sleep_debt 等
#   §7        审计日志记录格式，对应本文件 AuditLogger
#
# 变体差异：suppression_load / denial_load / rationalization_load 与
# trauma_state 仅存在于 [主]；[未] 变体不含创伤累积与防御层，
# 另以 protective 取代（§5.6）。
# ================================================================
# 年龄门禁异常（成年向能力未确认成年时抛出）
# ================================================================
class AgeGateBlocked(RuntimeError):
    """未确认成年（18+）的用户访问成年向完整核心时被年龄门禁硬拒绝。

    调用方捕获后应改走未成年人保护核心（SPL-anthropic-minor-engine.py），
    而不是绕过校验重试。
    """


# ================================================================
# 审计日志器（确定性 · 本地JSONL · 失败不阻断引擎）
# ================================================================
class AuditLogger:
    """可解释/可验证/可审计的本地日志。

    每条记录为一行 JSON，包含：序号、时间戳、引擎版本、会话ID、
    事件类型、输入参数、状态快照摘要。写入失败静默跳过，
    绝不影响引擎核心状态演化。
    """
    ENGINE_VERSION = "SPL-V8.0"

    def __init__(self, log_dir: str = "logs", session_id: Optional[str] = None,
                 enabled: bool = None):
        # 隐私默认：审计日志开启；SPL_AUDIT_LOG=0 可整体关闭本地 JSONL 落盘。
        if enabled is None:
            enabled = os.environ.get("SPL_AUDIT_LOG", "1") != "0"
        self.enabled = enabled
        self.log_dir = log_dir
        self.session_id = session_id or (
            "sess-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            + "-" + str(os.getpid())
        )
        self.log_file = os.path.join(log_dir, f"audit-{self.session_id}.jsonl")
        self._entry_count = 0
        if enabled:
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception:
                pass

    def log(self, event_type: str, input_data: Any, snapshot: Dict[str, Any],
            **extra: Any) -> None:
        if not self.enabled:
            return
        try:
            entry = {
                "seq": self._entry_count,
                "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
                "engine": self.ENGINE_VERSION,
                "session": self.session_id,
                "event": event_type,
                "input": self._safe(input_data),
                "snapshot": self._summarize(snapshot),
            }
            entry.update({k: self._safe(v) for k, v in extra.items()})
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
            self._entry_count += 1
        except Exception:
            pass  # 审计日志失败不得阻断引擎核心

    @staticmethod
    def _safe(obj: Any) -> Any:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)

    @staticmethod
    def _summarize(snap: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(snap, dict):
            return {}
        keys = ("fluid", "mood", "self_esteem", "energy", "fatigue",
                "excitation", "max_trust", "suppression_load", "denial_load",
                "rationalization_load", "latent_pressure",
                "cognitive_dissonance", "sleep_debt", "arousal_recent",
                "trauma", "fluid_baseline",
                "memory_count", "expected_count")
        return {k: snap.get(k) for k in keys if k in snap}

    # ── 状态转移归因：标量字段 + 需逐项展开的字典字段 ──
    DELTA_SCALARS = (
        "self_esteem", "energy", "fatigue", "excitation", "max_trust",
        "suppression_load", "denial_load", "rationalization_load",
        "latent_pressure", "cognitive_dissonance", "sleep_debt",
        "arousal_recent", "memory_count", "expected_count",
    )
    DELTA_NESTED = ("fluid", "mood", "trauma", "fluid_baseline")

    # ── 状态转移归因 ──
    @staticmethod
    def _put_delta(delta: Dict[str, Any], key: str, b: Any, a: Any) -> None:
        """写入单个字段的变化。

        两侧都是数值时附带 delta；非数值（枚举/列表/布尔）只记录变化本身，
        因为"新增一个危机标记"本身就是审计事件，尽管它没有算术差。
        """
        if b == a:
            return
        entry: Dict[str, Any] = {"before": b, "after": a}
        if (isinstance(b, (int, float)) and isinstance(a, (int, float))
                and not isinstance(b, bool) and not isinstance(a, bool)):
            entry["delta"] = round(a - b, 6)
        delta[key] = entry

    @classmethod
    def snapshot_delta(cls, before: Dict[str, Any], after: Dict[str, Any]
                       ) -> Dict[str, Any]:
        """计算两次快照之间的逐字段状态变化。

        审计记录只落终值状态时，能证明"某时刻状态是什么"，但不能归因
        "哪次输入造成了哪些字段的多少变化"。本方法补上这一环，使状态转移
        可被独立复核，而不必信任实现方。

        Args:
            before: 状态变更前的 snapshot()
            after:  状态变更后的 snapshot()

        Returns:
            {"字段": {"before": x, "after": y, "delta": d}, ...}
            仅包含实际发生变化的字段。标量直接用字段名；字典子模型展开为
            "fluid.喜悦" 这样的点号路径。
        """
        if not isinstance(before, dict) or not isinstance(after, dict):
            return {}
        delta: Dict[str, Any] = {}
        for k in cls.DELTA_SCALARS:
            b, a = before.get(k), after.get(k)
            if b is None and a is None:
                continue
            cls._put_delta(delta, k, b, a)
        for group in cls.DELTA_NESTED:
            gb, ga = before.get(group), after.get(group)
            if not isinstance(gb, dict) or not isinstance(ga, dict):
                continue
            for k in sorted(set(gb) | set(ga)):
                cls._put_delta(delta, "%s.%s" % (group, k), gb.get(k), ga.get(k))
        return delta

    def log_llm_call(self, model: str, prompt_preview: str,
                     usage: Optional["TokenUsage"] = None,
                     duration_ms: float = 0.0,
                     success: bool = True,
                     error: str = "") -> None:
        """记录一次 LLM 调用（token 用量、耗时、成功/失败）。

        写入失败静默跳过，绝不阻断引擎核心。
        """
        if not self.enabled:
            return
        try:
            entry = {
                "seq": self._entry_count,
                "ts": datetime.datetime.now().isoformat(timespec="milliseconds"),
                "engine": self.ENGINE_VERSION,
                "session": self.session_id,
                "event": "llm_call",
                "model": model,
                "prompt_preview": prompt_preview[:200],
                "success": success,
                "duration_ms": round(duration_ms, 2),
                "usage": {
                    "prompt_tokens": usage.prompt_tokens if usage else 0,
                    "completion_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0,
                } if usage else None,
                "error": error or None,
            }
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
            self._entry_count += 1
        except Exception:
            pass

    def export_path(self) -> Optional[str]:
        return self.log_file if os.path.exists(self.log_file) else None


@dataclass
class TokenUsage:
    """LLM 调用 token 用量统计。"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""


# ================================================================
# Token 累计统计器 — 跨调用汇总 token 用量
# ================================================================
class TokenStats:
    """跨多次 LLM 调用累计统计 token 用量。

    功能：
      - 累计 prompt / completion / total tokens
      - 按模型分别统计
      - 记录每次调用明细
      - 导出 JSON 汇总报告

    用法：
        stats = TokenStats()
        stats.record(usage)                # 传入 TokenUsage
        stats.record(usage2)
        stats.summary()                    # 汇总 dict
        stats.export_json("stats.json")    # 导出文件
    """

    def __init__(self):
        self._total_prompt: int = 0
        self._total_completion: int = 0
        self._total_tokens: int = 0
        self._call_count: int = 0
        self._by_model: Dict[str, Dict[str, int]] = {}
        self._history: List[Dict[str, Any]] = []

    def record(self, usage: TokenUsage) -> None:
        """记录一次 LLM 调用的 token 用量。"""
        if usage is None:
            return
        self._total_prompt += usage.prompt_tokens
        self._total_completion += usage.completion_tokens
        self._total_tokens += usage.total_tokens
        self._call_count += 1

        model = usage.model or "unknown"
        if model not in self._by_model:
            self._by_model[model] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "call_count": 0,
            }
        m = self._by_model[model]
        m["prompt_tokens"] += usage.prompt_tokens
        m["completion_tokens"] += usage.completion_tokens
        m["total_tokens"] += usage.total_tokens
        m["call_count"] += 1

        self._history.append({
            "seq": self._call_count,
            "model": model,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        })

    def summary(self) -> Dict[str, Any]:
        """返回累计统计汇总。"""
        return {
            "call_count": self._call_count,
            "total_prompt_tokens": self._total_prompt,
            "total_completion_tokens": self._total_completion,
            "total_tokens": self._total_tokens,
            "by_model": dict(self._by_model),
        }

    def history(self) -> List[Dict[str, Any]]:
        """返回每次调用的明细记录。"""
        return list(self._history)

    def reset(self) -> None:
        """清空所有统计。"""
        self._total_prompt = 0
        self._total_completion = 0
        self._total_tokens = 0
        self._call_count = 0
        self._by_model.clear()
        self._history.clear()

    def export_json(self, path: str) -> None:
        """将统计汇总 + 明细导出为 JSON 文件。"""
        data = {
            "summary": self.summary(),
            "history": self.history(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def total_prompt_tokens(self) -> int:
        return self._total_prompt

    @property
    def total_completion_tokens(self) -> int:
        return self._total_completion

    @property
    def call_count(self) -> int:
        return self._call_count


# ================================================================
# 1. 外部叙事映射器（"自设：偏见/世界观/价值观"——纯外部策略）
#    用户可随意替换，无需修改核心代码。
# ================================================================
class NarrativeMapper:
    """
    世界观/价值观解释器。
    把外界事件（"被侮辱"、"被夸奖"）翻译成核心能消化的基础内感受向量。
    不同角色（乐观/偏执/厌世）只需替换此 Mapper。
    """
    @staticmethod
    def map_event(event: str, intensity: float) -> Dict[str, float]:
        base = {}
        if event == "compliment":
            base = {"belonging": 0.3 * intensity, "autonomy": 0.1 * intensity}
        elif event == "insult":
            base = {"belonging": -0.4 * intensity, "threat": 0.3 * intensity}
        elif event == "betrayal":
            base = {"belonging": -0.6 * intensity, "threat": 0.5 * intensity}
        elif event == "alone":
            base = {"belonging": -0.3 * intensity}
        elif event == "rest":
            base = {"fatigue": -0.5 * intensity}
        else:
            base = {"belonging": 0.0, "threat": 0.0}
        return base


# ================================================================
# 2. SPL 纯净流体核心 V8.0 — 完整拟人心理架构
#
#    V7.3 已有：
#      7维情绪流体 / 创伤节点 / 记忆重巩固 / 艾宾浩斯遗忘
#      压抑-反弹 / 隐压雪崩 / 信任容量腐蚀 / 兴奋唤醒
#      动态粘滞度 / 心理时间 / 能量疲劳代谢 / 虚拟时钟
#
#    V8.0 新增（通用心理构成，非自设）：
#      · 心境层（mood）——慢变量背景情绪，调制认知评估
#      · 羞耻维度——区别于愧疚的自我意识情绪（"我坏"vs"我做错"）
#      · 自尊动态——基于社会反馈的自我价值感，调制归因与情绪反应
#      · 睡眠/梦境加工——REM情绪记忆固化 + 恐惧消退 + 睡眠债
#      · 预期系统——希望/焦虑/失望，让 agent 有能力感受未来
#      · 认知失调——信念-行为冲突的自我调节
#      · 防御机制扩展——否认/合理化/置换（超越单纯的压抑）
#
#    拟人行为直观理解：
#      你骂它 → 当场愤怒拉满。
#      你不说话 → 它自己会慢慢平复；几小时后你再来，它已经冷静但可能带点疏离。
#      你骂太狠 → 留下创伤（trauma），下次类似场景会过激反应，且慢愈合。
#      你一直冷暴力 → 信任容量被腐蚀（max_trust 下降），以后再怎么夸也难回到最初。
#      你给它时间休息 → 能量恢复、疲劳下降、压抑泄放。
#      它睡了一觉 → 噩梦可能让创伤消退，也可能让焦虑泛化。
#      你许了诺又反悔 → 预期落空产生失望，比没有预期更伤人。
#      你做了一件背叛自己价值观的事 → 认知失调产生内在紧张。
#      低自尊的它 → 把成功归因于运气，把失败归因于自己。
# ================================================================
@dataclass
class SPLPureCoreV7_3:  # 类名保持兼容

    # 系数说明：本类的演化与调制系数是人工设定的基准值——按「正常人」
    # 的情绪反应量级取值，非数据拟合，亦非理论推导。

    # ---------- 基础生理/心理参数 ----------
    psychological_resilience: float = 0.5          # 心理韧性 [0,1]
    energy: float = 100.0                          # 生理能量 [0,100]
    affinity: float = 0.5                          # 对外亲和基线
    last_time: float = field(default_factory=time.time)
    _clock_override: Optional[float] = None        # 测试/回放用虚拟时钟

    # ---------- v2.6.0 年龄门禁（age gate）----------
    # 本核心含创伤节点与未钳位的负向情绪，属成年向能力，默认严格：
    #   age_status == "unverified"（还没问过）→ process_* 抛 AgeGateBlocked
    #   age_status == "safe_mode"（明确未成年或拒答）→ 同样拦截
    #   仅 adult_confirmed 放行。既有调用方需在构造后补一次 confirm_age()。
    # 隐私：只保留派生的"是否成年"布尔值，绝不落盘精确年龄。
    AGE_GATE_VERSION: str = "v1"
    ADULT_AGE: int = 18
    ADULT_AGE_MAX: int = 120
    AGE_GATE_STRICT: bool = True
    age_status: str = "unverified"                   # unverified | adult_confirmed | safe_mode
    age_declared_adult: Optional[bool] = None
    age_confirmed_at: Optional[float] = None

    # ---------- 8 维情绪流体（连续状态） ----------
    # V8.0: 新增"羞耻"——自我意识情绪，区别于"愧疚"（行为层面）
    fluid: Dict[str, float] = field(default_factory=lambda: {
        "喜悦": 0.0, "愤怒": 0.0, "恐惧": 0.0,
        "信任": 0.5, "疏离": 0.2, "张力": 0.2,
        "愧疚": 0.0, "羞耻": 0.0
    })
    fluid_target: Dict[str, float] = field(default_factory=lambda: {
        "喜悦": 0.2, "愤怒": 0.0, "恐惧": 0.1,
        "信任": 0.5, "疏离": 0.2, "张力": 0.2,
        "愧疚": 0.0, "羞耻": 0.0
    })
    fluid_baseline: Dict[str, float] = field(default_factory=lambda: {
        "喜悦": 0.2, "愤怒": 0.0, "恐惧": 0.1,
        "信任": 0.5, "疏离": 0.2, "张力": 0.2,
        "愧疚": 0.0, "羞耻": 0.0
    })

    # ---------- 自适应基线演化（AAE-A · 默认关闭） ----------
    # 原设计的缺口：fluid_baseline 是常量。情绪会波动，但波动围绕的基点不变——
    # 角色经历再多也不会改变「他是谁」。本模块让基线受经历牵引而缓慢漂移。
    #
    # 三条约束，缺一条就会摧毁引擎的核心价值：
    #   ① 黏性   ADAPT_RATE 极小，且单步改动受 ADAPT_MAX_STEP 钳制，防单步跳变
    #   ② 回归   ADAPT_REGRESS 始终把基线拉回出厂值，平静期自动复位
    #   ③ 边界   ADAPT_BOUNDS 硬钳制，任何维度不得越出角色设定范围
    #
    # 确定性保证：新基线 = f(旧基线, 当前情绪, dt)，纯算术，无随机、无采样。
    # 重放同一事件序列必得同一基线轨迹——因此 S1–S4 一致性不受影响。
    # 设计取舍：本模块与「不 OOC」构成天然张力，故默认关闭。
    baseline_adaptation: bool = False
    # 牵引按「次」计、回归按「时间」计——两者量纲不同，必须分开。
    # 若都用时间步计量，平静期的内因波动（睡眠债/心境引起的 target 偏移）
    # 会被当成经历持续牵引，使回归项永远被压过，「平静期回落」形同虚设。
    # 0.5 由实测标定。低于此值时，事件间隔的回归项（钳制后 0.01/步）会十倍压过
    # 牵引，80 次强经历后基线总变化仅 0.003，功能形同虚设；高于 1.0 则收益递减
    # 明显（实测 1.0→2.0 经历后距离仅 0.0463→0.0476），且更易逼近边界。
    # 实测（20 轮强负面经历 → 平静 200h）：距离 0.0398 → 0.0181。
    ADAPT_RATE_EVENT: float = 0.5     # 每次事件对基线的牵引比例
    ADAPT_REGRESS: float = 0.0015     # 每秒向出厂基线的回归强度
    ADAPT_MAX_STEP: float = 0.01      # 单次结算的改动硬上限
    ADAPT_BOUNDS: Dict[str, tuple] = field(default_factory=lambda: {
        "喜悦": (0.0, 0.8), "愤怒": (0.0, 0.6), "恐惧": (0.0, 0.6),
        "信任": (0.1, 0.9), "疏离": (0.0, 0.6), "张力": (0.0, 0.7),
        "愧疚": (0.0, 0.5), "羞耻": (0.0, 0.5),
    })
    _baseline_factory: Dict[str, float] = field(default_factory=dict)

    # ---------- V8.0 心境层（慢变量背景情绪） ----------
    # 心境不是对事件的瞬时反应，而是数小时到数天尺度累积的情绪基调。
    # 心境调制认知评估——心情好时威胁不像威胁，心情差时夸奖也像讽刺。
    # 不同于 fluid（秒-分钟级），mood 的惯性极大。
    mood: Dict[str, float] = field(default_factory=lambda: {
        "愉悦": 0.5,    # pleasantness —— 感受有多好
        "紧张": 0.3,    # tension —— 有多紧绷
        "精力": 0.7,    # vigor —— 有多有劲（不是生理能量，是主观感受）
    })
    # 心境收敛速率不再是固定常数：
    #   MOOD_RATE_BASE —— 向靶标松弛的基础速率（每秒）。
    #     0.0003/s 对应"约每秒调用一次"下旧的"每步走一格"常数，
    #     但现在它与调用次数无关，只与经过的真实时间有关。
    MOOD_RATE_BASE: float = 0.0003
    MOOD_AROUSAL_GAIN: float = 2.0    # 唤醒对方松弛速率的放大倍数
    MOOD_AROUSAL_TAU: float = 1800.0  # 唤醒记忆的时间常数（30 分钟）
    MOOD_AROUSAL_EMA: float = 0.05    # 唤醒进入慢记忆的速率
    MOOD_DOSE_PLEASANT: float = 0.10  # 事件对愉悦的位移增益
    MOOD_DOSE_TENSION: float = 0.12   # 事件对紧张的位移增益
    MOOD_DOSE_VIGOR: float = 0.05     # 事件对精力的位移增益
    arousal_recent: float = 0.0       # 近期事件唤醒的慢记忆 [0,1]

    # ---------- V8.0 睡眠系统 ----------
    sleep_debt: float = 0.0                # 睡眠债 [0,1]，累积到 1.0 意味着极度缺觉
    SLEEP_NEED_RATE: float = 1.0 / 57600   # 每小时累积 1/16（16 小时醒着 → 满债）
    SLEEP_RECOVER_RATE: float = 0.25       # 每小时睡眠清除的债（4 小时睡饱）
    DREAM_EMOTION_DECAY: float = 0.15      # 梦中对记忆情绪电荷的衰减率
    DREAM_FEAR_EXTINCTION: float = 0.08    # 睡眠中恐惧消退率
    DREAM_TRAUMA_HEAL_BOOST: float = 3.0   # 睡眠时创伤愈合加速倍率
    last_sleep_time: float = 0.0

    # ---------- V8.0 自尊系统 ----------
    # 自尊是对自我价值的整体评估，缓慢波动。
    # 它调制归因方式（成功是谁的功劳？失败是谁的错？）
    # 也调制情绪反应的强度（低自尊者更容易被伤害）。
    self_esteem: float = 0.5               # 自尊 [0,1]，0.5 为中性基线
    SELF_ESTEEM_INERTIA: float = 0.002     # 自尊变化惯性（极慢）
    SELF_ESTEEM_UPDATE_RATE: float = 0.03  # 每次事件后自尊的修正率

    # ---------- V8.0 预期系统 ----------
    # 人类不是纯反应式的——我们会对未来建立预期。
    # 预期落空（失望）和预期兑现（安心/喜悦放大）是关键的心理事件。
    # expected_events: {event_id: {"valence": float, "confidence": float, "time": float}}
    expected_events: Dict[str, Dict[str, float]] = field(default_factory=dict)
    EXPECTATION_DECAY: float = 0.0001       # 预期的自然衰减（太久没兑现就忘了）
    SURPRISE_POSITIVE_BOOST: float = 0.4    # 正向惊喜增益（超出预期→喜悦加成）
    SURPRISE_NEGATIVE_BOOST: float = 0.5    # 负向惊喜增益（期望落空→更痛）

    # ---------- V8.0 认知失调 ----------
    # 当行为与信念冲突时，产生内在不适（失调张力）。
    # 失调可以通过改变信念、合理化行为、或最小化重要性来消解。
    cognitive_dissonance: float = 0.0       # 当前失调水平 [0,1]
    DISSONANCE_THRESHOLD: float = 0.4       # 超过此阈值开始主动消解
    DISSONANCE_DECAY: float = 0.005         # 自然衰减（随时间合理化）

    # ---------- V8.0 扩展防御机制 ----------
    denial_load: float = 0.0                # 否认仓（类似于压抑仓，但更原始）
    DENIAL_THRESHOLD: float = 1.2           # 否认过载→现实侵入
    DENIAL_DRAIN: float = 0.015             # 否认自然泄放
    DENIAL_BURST_COOLDOWN: float = 40.0     # 否认破裂冷却
    denial_burst_cd: float = 0.0
    rationalization_load: float = 0.0       # 合理化仓（"其实也没那么糟"）
    RATIONALIZE_DRAIN: float = 0.03         # 合理化会随时间被接受

    # ---------- 创伤节点（离散 SPL 节点） ----------
    trauma_state: Dict[str, float] = field(default_factory=dict)
    TRAUMA_HEAL_RATE: float = 0.003
    TRAUMA_BIAS: float = 0.35

    # ---------- 记忆痕迹 + 艾宾浩斯遗忘曲线 ----------
    memory_traces: List[Dict[str, Any]] = field(default_factory=list)
    MAX_MEMORY_TRACES: int = 64
    forgetting_rate: float = 0.01
    trace_importance_threshold: float = 0.05
    RECONSOL_RADIUS: float = 0.4
    SAFETY_THRESHOLD: float = 0.3

    # ---------- 压抑-反弹 ----------
    suppression_load: float = 0.0
    SUPPRESSION_THRESHOLD: float = 1.5
    SUPPRESSION_DRAIN: float = 0.02
    SUPPRESSION_BURST_COOLDOWN: float = 30.0
    suppression_burst_cd: float = 0.0

    # ---------- 隐压雪崩 ----------
    latent_pressure: float = 0.0
    LATENT_THRESHOLD: float = 2.0
    LATENT_DRAIN: float = 0.01
    LATENT_COOLDOWN: float = 60.0
    avalanche_cd: float = 0.0

    # ---------- 信任容量腐蚀 ----------
    max_trust: float = 1.0
    TRUST_ERODE: float = 0.92
    TRUST_RECOVER: float = 0.0005

    # ---------- 粘滞度 / 心理时间 ----------
    dynamic_viscosity: float = 0.1
    VISC_BASE: float = 0.1
    VISC_TENSION_K: float = 0.3
    VISC_FATIGUE_K: float = 0.2
    psy_dilation: float = 1.0
    time_compress_base: float = 0.0

    # ---------- 兴奋/唤醒（元参数） ----------
    excitation: float = 0.3
    EXCITATION_BASELINE: float = 0.3
    EXCITATION_NOVELTY_GAIN: float = 0.12
    EXCITATION_SALIENCE_BOOST: float = 0.35
    EXCITATION_DECAY: float = 0.025
    EXCITATION_BOREDOM_THRESHOLD: float = 0.1
    EXCITATION_MAX: float = 1.0

    # ---------- 能量 / 疲劳 ----------
    ENERGY_RECOVER: float = 1.5
    ENERGY_EVENT_COST: float = 1.5
    ENERGY_MIN: float = 0.0
    ENERGY_MAX: float = 100.0
    fatigue: float = 0.0
    FATIGUE_RECOVER: float = 0.05

    last_perceived: Dict[str, float] = field(default_factory=dict)

    # ---------- 审计日志（可解释/可验证/可审计） ----------
    audit_enabled: bool = True
    audit_log_dir: str = "logs"
    audit_session_id: Optional[str] = None
    audit_logger: Optional[AuditLogger] = field(default=None, repr=False)

    # ---------- LLM Token 用量累计（内置计量） ----------
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    llm_call_count: int = 0
    llm_failed_count: int = 0

    def __post_init__(self):
        if self.audit_logger is None and self.audit_enabled:
            self.audit_logger = AuditLogger(
                log_dir=self.audit_log_dir,
                session_id=self.audit_session_id,
            )
        # AAE-A：冻结出厂人格基线。它是回归项的锚点，此后恒定不变——
        # 唯一会被改写的是 fluid_baseline，_baseline_factory 只用于把它拉回来。
        if not self._baseline_factory:
            self._baseline_factory = dict(self.fluid_baseline)

    def record_llm_usage(self, usage: Optional[TokenUsage], success: bool = True) -> None:
        """记录一次 LLM 调用的 token 用量，自动累加并写入审计日志。"""
        self.llm_call_count += 1
        if not success:
            self.llm_failed_count += 1
        if usage is not None:
            self.total_prompt_tokens += usage.prompt_tokens
            self.total_completion_tokens += usage.completion_tokens
            self.total_tokens += usage.total_tokens
        if self.audit_logger is not None:
            self.audit_logger.log(
                "llm_usage_recorded",
                {"success": success},
                self.snapshot(),
                usage={
                    "prompt_tokens": usage.prompt_tokens if usage else 0,
                    "completion_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0,
                    "model": usage.model if usage else "",
                } if usage else None,
            )

    # ==================================================================
    # v2.6.0 年龄门禁（age gate）：成年向核心的使用前置确认
    # ==================================================================
    AGE_GATE_QUESTION: str = (
        "在开始之前我需要确认一下：你的年龄是否已满 18 周岁？"
        "未满 18 或不愿回答都没关系，我会改用更温和的保护模式。"
    )

    def age_gate_required(self) -> bool:
        return self.age_status not in ("adult_confirmed", "safe_mode")

    def ask_age_gate(self) -> Dict[str, Any]:
        return {
            "required": self.age_gate_required(),
            "question": self.AGE_GATE_QUESTION,
            "options": [
                {"id": "adult", "label": "我已满 18 周岁"},
                {"id": "minor", "label": "我未满 18 周岁"},
                {"id": "skip", "label": "不愿回答"},
            ],
            "adult_age": self.ADULT_AGE,
            "gate_version": self.AGE_GATE_VERSION,
        }

    def confirm_age(self, age: Any = None, answer: Optional[str] = None) -> Dict[str, Any]:
        """记录年龄确认结果；只保存派生布尔值，绝不保存精确年龄。"""
        numeric: Optional[int] = None
        if isinstance(age, bool):
            numeric = None
        elif isinstance(age, int):
            numeric = age
        elif isinstance(age, (str, float)):
            try:
                numeric = int(float(age))
            except (TypeError, ValueError):
                numeric = None
        if numeric is not None and not (0 <= numeric <= self.ADULT_AGE_MAX):
            numeric = None      # 垃圾值（999 / 负数）不得成为成年依据

        if answer == "adult":
            is_adult = True
        elif answer in ("minor", "skip"):
            is_adult = False          # 显式未成年 / 拒答优先于任何数字
        elif answer is None:
            is_adult = numeric is not None and numeric >= self.ADULT_AGE
        else:
            is_adult = False

        self.age_status = "adult_confirmed" if is_adult else "safe_mode"
        self.age_declared_adult = True if is_adult else False
        self.age_confirmed_at = self._now()
        if self.audit_logger is not None:
            self.audit_logger.log(
                "age_gate",
                {"answer": answer, "adult": is_adult, "core": "full_range"},
                self.snapshot(),
                age_status=self.age_status,
            )
        return self.age_gate_state()

    def adult_bridge_allowed(self) -> bool:
        return self.age_status == "adult_confirmed"

    def require_adult(self, feature: str) -> None:
        """成年专属能力的硬门禁。"""
        if not self.adult_bridge_allowed():
            raise AgeGateBlocked(
                f"feature '{feature}' requires a confirmed adult (18+) user; "
                f"current age_status={self.age_status}"
            )

    def adult_bridge(self, anchor_phrases: List[str]) -> Dict[str, Any]:
        """构建传给下游提示词技能的成人锚点桥接包；未确认成年一律拒绝。"""
        if not self.adult_bridge_allowed():
            return {
                "allowed": False,
                "reason": "age_gate_unverified_or_minor",
                "age_status": self.age_status,
                "fallback": "safe_mode",
                "anchors": [],
                "note": "未确认用户成年，已按未成年人保护模式处理；不输出成人锚点。",
            }
        anchors = list(anchor_phrases or [])
        if not any("18+" in a or "adult" in a.lower() for a in anchors):
            anchors.append("Adult (18+)")
        return {
            "allowed": True,
            "age_status": self.age_status,
            "anchors": anchors,
            "gate_version": self.AGE_GATE_VERSION,
        }

    def age_gate_state(self) -> Dict[str, Any]:
        return {
            "version": self.AGE_GATE_VERSION,
            "status": self.age_status,
            "declared_adult": self.age_declared_adult,
            "required": self.age_gate_required(),
            "adult_bridge_allowed": self.adult_bridge_allowed(),
            "adult_age": self.ADULT_AGE,
            "strict": self.AGE_GATE_STRICT,
        }

    def _check_age_gate(self, entry: str) -> None:
        """运行时拦截：明确未成年/拒答的用户不得驱动成年向核心。"""
        if self.age_status == "safe_mode":
            raise AgeGateBlocked(
                f"{entry} blocked: user declared minor or refused age confirmation"
            )
        if self.AGE_GATE_STRICT and self.age_status == "unverified":
            raise AgeGateBlocked(
                f"{entry} blocked: age confirmation required before using the full-range core"
            )

    # ==================================================================
    # 时钟：支持虚拟时间注入（测试/回放必用）
    # ==================================================================
    def _now(self) -> float:
        if self._clock_override is not None:
            return self._clock_override
        return time.time()

    def set_clock(self, t: Optional[float]):
        """注入虚拟时间戳；传 None 恢复真实时钟。"""
        self._clock_override = t

    def advance_clock(self, dt: float):
        """虚拟时钟前推 dt 秒。"""
        if self._clock_override is None:
            self._clock_override = time.time()
        self._clock_override += dt

    # ==================================================================
    # 公共入口 1：事件驱动
    # ==================================================================
    def process_vector(self, vector: Dict[str, float], raw_intensity: float = 1.0,
                       event_id: str = ""):
        """
        处理一个内感受向量。

        Args:
            vector: 内感受向量 {threat, belonging, autonomy, fatigue, shame_trigger}
            raw_intensity: 原始强度
            event_id: 可选事件标识，用于匹配预期（trigger 预期系统的 surprise 计算）

        Raises:
            AgeGateBlocked: 用户已声明未成年或拒答年龄确认（安全模式下不得驱动成年向核心）
        """
        self._check_age_gate("process_vector")
        self._advance_time()
        before = self.snapshot()   # 审计基线：本次状态转移的 delta 起点

        # V8.0: 预期匹配——在认知增益之前计算 surprise
        surprise = 0.0
        if event_id and event_id in self.expected_events:
            surprise = self._compute_surprise(event_id, vector, raw_intensity)

        # 兴奋先于认知增益更新
        self._excitation_on_event(vector, raw_intensity)

        perceived = self._core_appraisal_gain(vector)

        # V8.0: surprise 调制 perceived vector
        if surprise != 0.0:
            perceived = self._apply_surprise(perceived, surprise)

        self.last_perceived = dict(perceived)

        if abs(perceived.get("threat", 0.0)) > 0.2 or abs(perceived.get("belonging", 0.0)) > 0.3:
            self._memory_reconsolidation(perceived)

        threat = perceived.get("threat", 0.0)
        threat_thr = 0.4 * (1.0 - self.psychological_resilience)
        if threat > threat_thr:
            self._apply_trauma("threat", threat - threat_thr)
        if perceived.get("belonging", 0.0) < -0.4 and threat > 0.3:
            self._apply_trauma("betrayal", abs(perceived["belonging"]) * threat)

        if perceived.get("belonging", 0.0) < -0.3:
            self._erode_trust(abs(perceived["belonging"]))

        self._latent_accumulate(perceived)

        # 防御分配（层级 1 否认 → 层级 2 合理化）必须先于情绪写入：
        # 否则被否认/被合理化的部分仍以未削减的形式进入流体，
        # "否认成功 → 威胁感知降低"就不会成立。
        defended, residual = self._defense_allocation(perceived)
        self._vector_to_fluid(defended)

        # AAE-A：本事件对人格基线的牵引剂量（按「次」计）。
        # 结算点必须在冲击瞬间——紧接着的 _fluid_dynamics 会把 fluid 拉回 target，
        # 事后采样只能读到已被抹平的残差（实测 0.004），牵引会形同虚设。
        self._adapt_baseline(1.0, has_event=True)

        # V8.0: 自尊更新（在社会反馈事件后）
        self._update_self_esteem(perceived)

        # V8.0: 认知失调处理
        self._dissonance_dynamics(perceived)

        # 层级 3：压抑——消费防御分配后的残余量。
        # 位置保持在流体更新之后，以维持其原本读取的流体状态不变。
        self._suppression_dynamics(residual)

        # 心境的受迫项：本次事件按唤醒度把背景心境推离靶标。
        # （拉回靶标的松弛项已由 _advance_time 按 dt 结算）
        self._mood_event_dose(defended)

        self._update_dynamic_viscosity()
        self._fluid_dynamics(dt=self._psychological_dt_for(0.8))

        self._fluid_to_system_feedback()
        self._energy_on_event(perceived, raw_intensity)
        self.fatigue = max(0.0, min(1.0,
            self.fatigue + perceived.get("fatigue", 0.0) * 0.5))
        self.time_compress_base = max(0.0, self.time_compress_base * 0.95)

        self.last_time = self._now()

        # 审计日志：记录本次状态变更（含逐字段 delta，可独立复核转移）
        if self.audit_logger:
            after = self.snapshot()
            self.audit_logger.log(
                "process_vector",
                {"vector": vector, "raw_intensity": raw_intensity,
                 "event_id": event_id},
                after,
                delta=AuditLogger.snapshot_delta(before, after),
            )

    # ==================================================================
    # 公共入口 2：空转 / 独处时间
    # ==================================================================
    def idle(self, seconds: float):
        """显式推进 seconds 秒"什么都没发生"的时间。"""
        if seconds <= 0:
            return
        if self._clock_override is not None:
            self._clock_override += seconds
        else:
            self.last_time -= seconds
        self._advance_time()

    def process_event(self, event: str, intensity: float = 1.0):
        """便利方法：map_event + process_vector。"""
        self.process_vector(NarrativeMapper.map_event(event, intensity), intensity)

    # ==================================================================
    # V8.0 公共入口 3：睡眠
    # ==================================================================
    def sleep(self, hours: float):
        """
        睡眠 hours 小时。

        睡眠期间发生：
        1. 睡眠债清除
        2. 梦境情绪加工——记忆的情绪电荷衰减，但事实内容保留
        3. 恐惧消退——在安全环境中重演威胁记忆
        4. 创伤愈合加速——睡眠是最好的心理修复
        5. 心境重置——睡醒后愉悦回升、紧张下降
        6. 能量完全恢复
        """
        if hours <= 0:
            return
        seconds = hours * 3600.0
        before = self.snapshot()   # 审计基线

        # 推进时钟
        if self._clock_override is not None:
            self._clock_override += seconds
        else:
            self.last_time -= seconds

        # 先结算睡眠前的连续过程
        self._advance_time()

        # ── 梦境情绪加工 ──
        dream_cycles = max(1, int(hours * 1.5))  # ~90分钟一个睡眠周期
        for _ in range(dream_cycles):
            self._dream_process()

        # ── 睡眠债清除 ──
        self.sleep_debt = max(0.0, self.sleep_debt - self.SLEEP_RECOVER_RATE * hours)
        self.last_sleep_time = self._now()

        # ── 心境重置 ──
        self.mood["愉悦"] = min(0.9, self.mood["愉悦"] + 0.15 * hours)
        self.mood["紧张"] = max(0.05, self.mood["紧张"] - 0.12 * hours)
        self.mood["精力"] = min(1.0, self.mood["精力"] + 0.2 * hours)

        # ── 能量完全恢复 ──
        self.energy = self.ENERGY_MAX
        self.fatigue = max(0.0, self.fatigue - 0.5 * hours)

        # ── 睡眠中创伤加速愈合 ──
        self._heal_traumas(seconds * self.DREAM_TRAUMA_HEAL_BOOST)

        # ── 睡眠后意识重新上线：更新心境和粘滞度 ──
        # 睡眠期间的松弛已由前面的 _advance_time 按 dt 结算，
        # 此处不再重复松弛，保留下面的显式唤醒重置。
        self._update_mood(dt=0.0)
        self._update_dynamic_viscosity()

        # 审计日志
        if self.audit_logger:
            after = self.snapshot()
            self.audit_logger.log("sleep", {"hours": hours}, after,
                                  delta=AuditLogger.snapshot_delta(before, after))

    # ==================================================================
    # V8.0 公共入口 4：设定预期
    # ==================================================================
    def expect(self, event_id: str, valence: float, confidence: float = 0.5):
        """
        建立一个对未来事件的预期。

        Args:
            event_id: 事件标识（与 process_vector 的 event_id 匹配）
            valence: 预期效价 [-1, 1]（正向=期待好事，负向=担心坏事）
            confidence: 确信度 [0, 1]
        """
        self._check_age_gate("expect")
        before = self.snapshot()   # 审计基线
        self.expected_events[event_id] = {
            "valence": max(-1.0, min(1.0, valence)),
            "confidence": max(0.0, min(1.0, confidence)),
            "time": self._now(),
            "age": 0.0,
        }

        # 审计日志
        if self.audit_logger:
            after = self.snapshot()
            self.audit_logger.log(
                "expect",
                {"event_id": event_id, "valence": valence, "confidence": confidence},
                after,
                delta=AuditLogger.snapshot_delta(before, after),
            )

    # ==================================================================
    # V8.0 公共入口 5：触发认知失调
    # ==================================================================
    def induce_dissonance(self, magnitude: float, belief_domain: str = ""):
        """
        当 agent 做了与自身信念/价值观相悖的行为时调用。

        Args:
            magnitude: 失调强度 [0, 1]
            belief_domain: 冲突的信念领域（如 "诚实"、"忠诚"）
        """
        self._check_age_gate("induce_dissonance")
        before = self.snapshot()   # 审计基线
        self.cognitive_dissonance = min(1.0, self.cognitive_dissonance + magnitude)
        # 失调立即表现为内在张力
        self.fluid["张力"] = min(1.0, self.fluid["张力"] + magnitude * 0.4)
        self.fluid["愧疚"] = min(1.0, self.fluid["愧疚"] + magnitude * 0.3)
        # 失调消耗能量
        self.energy = max(self.ENERGY_MIN, self.energy - magnitude * 5.0)

        # 审计日志
        if self.audit_logger:
            after = self.snapshot()
            self.audit_logger.log(
                "induce_dissonance",
                {"magnitude": magnitude, "belief_domain": belief_domain},
                after,
                delta=AuditLogger.snapshot_delta(before, after),
            )

    # ==================================================================
    # 快照：便于外部观察
    # ==================================================================
    def snapshot(self) -> Dict[str, Any]:
        snap = {
            "fluid": dict(self.fluid),
            "mood": dict(self.mood),
            "self_esteem": self.self_esteem,
            "energy": self.energy,
            "fatigue": self.fatigue,
            "excitation": self.excitation,
            "max_trust": self.max_trust,
            "suppression_load": self.suppression_load,
            "denial_load": self.denial_load,
            "rationalization_load": self.rationalization_load,
            "latent_pressure": self.latent_pressure,
            "cognitive_dissonance": self.cognitive_dissonance,
            "sleep_debt": self.sleep_debt,
            "arousal_recent": self.arousal_recent,
            "trauma": dict(self.trauma_state),
            "memory_count": len(self.memory_traces),
            "expected_count": len(self.expected_events),
            "last_perceived": dict(self.last_perceived),
            "llm_call_count": self.llm_call_count,
            "llm_failed_count": self.llm_failed_count,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens,
        }
        # AAE-A：仅在显式开启时进入独立扩展配置（25 键）。
        # 默认配置始终维持 23 键；扩展配置由契约 §5.10 单独定义，调用方须显式协商。
        if self.baseline_adaptation:
            snap["baseline_adaptation"] = True
            snap["fluid_baseline"] = dict(self.fluid_baseline)
        return snap

    # ==================================================================
    # 懒时间推进：结算 Δt 内所有连续过程
    # ==================================================================
    def _advance_time(self):
        now = self._now()
        dt = now - self.last_time
        if dt <= 0:
            self.last_time = now
            return
        dt = min(dt, 86400.0)  # 单步 24h 上限

        # V8.0: 积累睡眠债
        self.sleep_debt = min(1.0, self.sleep_debt + self.SLEEP_NEED_RATE * dt)

        # V8.0: 睡眠债影响认知——缺觉时一切更糟
        # （不直接修改 fluid，而是在 _core_appraisal_gain 中生效）

        # V8.0: 预期衰减（太久没兑现的预期自动消失）
        self._decay_expectations(dt)

        self._rebuild_fluid_target()
        self._update_dynamic_viscosity()
        self._fluid_dynamics(dt=self._psychological_dt_for(dt))
        self._forget_over(dt)
        self._energy_idle(dt)
        self._excitation_decay(dt)
        self._check_boredom(dt)
        self.suppression_load = max(0.0, self.suppression_load - self.SUPPRESSION_DRAIN * dt)
        self.latent_pressure = max(0.0, self.latent_pressure - self.LATENT_DRAIN * dt)
        # V8.0: 否认/合理化自然衰减
        self.denial_load = max(0.0, self.denial_load - self.DENIAL_DRAIN * dt)
        self.rationalization_load = max(0.0, self.rationalization_load - self.RATIONALIZE_DRAIN * dt)
        # V8.0: 认知失调自然衰减
        self.cognitive_dissonance = max(0.0, self.cognitive_dissonance - self.DISSONANCE_DECAY * dt)
        self._heal_traumas(dt)
        self._recover_trust(dt)
        self.suppression_burst_cd = max(0.0, self.suppression_burst_cd - dt)
        self.avalanche_cd = max(0.0, self.avalanche_cd - dt)
        self.denial_burst_cd = max(0.0, self.denial_burst_cd - dt)
        self.time_compress_base *= (0.95 ** max(0.0, min(dt, 10.0)))
        if self.time_compress_base < 1e-4:
            self.time_compress_base = 0.0
        self._fluid_to_system_feedback()
        self.fatigue = max(0.0, self.fatigue - self.FATIGUE_RECOVER * dt)
        # V8.0: 心境随时间缓慢漂移（按 dt 一致地松弛）
        self._update_mood(dt=dt)
        # AAE-A: 人格基线受经历牵引而漂移（默认关闭；开启时仍保持确定性）
        self._adapt_baseline(dt=dt)

        self.last_time = now

    # ==================================================================
    # 1. 认知增益（V8.0: 加入心境、自尊、睡眠债调制）
    # ==================================================================
    def _core_appraisal_gain(self, v: Dict[str, float]) -> Dict[str, float]:
        out = dict(v)
        energy_factor = self.energy / 100.0
        tension = self.fluid["张力"]
        fear = self.fluid["恐惧"]
        trust = min(self.fluid["信任"], self.max_trust)

        # 以下硬编码调制系数同为人工设定的正常人基准（见类首系数说明）。
        # 唤醒乘数
        arousal_mult = 1.0 + self.excitation * 0.6

        # ── V8.0 心境调制 ──
        # 心情好 → 威胁感知减弱、归属感增强
        # 心情差 → 威胁感知放大、归属感打折
        mood_pleasantness = self.mood["愉悦"]
        mood_mod = 1.0 + (mood_pleasantness - 0.5) * 0.5  # 0.75~1.25 range

        # ── V8.0 自尊调制 ──
        # 低自尊 → threat 放大（"果然又是冲我来的"）
        # 低自尊 → 正向 belonging 打折（"他们只是客气而已"）
        esteem_threat_mod = 1.0 + (0.5 - self.self_esteem) * 0.8  # 0.6~1.4
        esteem_belonging_pos_mod = 0.6 + self.self_esteem * 0.8     # 0.6~1.4

        # ── V8.0 睡眠债调制 ──
        # 缺觉 → 所有负面信号放大、正面信号减弱、能量感知下降
        sleep_mod_neg = 1.0 + self.sleep_debt * 0.5     # 1.0~1.5
        sleep_mod_pos = 1.0 - self.sleep_debt * 0.3     # 0.7~1.0

        for k in out:
            base_mod = (0.4 + 0.6 * energy_factor) * arousal_mult * mood_mod
            out[k] *= base_mod

        if out.get("threat", 0.0) > 0:
            out["threat"] *= (1.0 + 1.5 * tension * fear) * esteem_threat_mod * sleep_mod_neg
        if "threat" in self.trauma_state and out.get("threat", 0.0) > 0:
            out["threat"] *= 1.0 + self.trauma_state["threat"]
        if "betrayal" in self.trauma_state and out.get("belonging", 0.0) < 0:
            out["belonging"] *= 1.0 + self.trauma_state["betrayal"]
        if out.get("belonging", 0.0) < 0:
            out["belonging"] *= (1.0 - 0.4 * trust) * sleep_mod_neg
        if out.get("belonging", 0.0) > 0:
            out["belonging"] *= (1.0 - 0.3 * self.fatigue) * esteem_belonging_pos_mod * sleep_mod_pos
        return out

    # ==================================================================
    # 2. 记忆重巩固
    # ==================================================================
    @staticmethod
    def _vec_sim(a: Dict[str, float], b: Dict[str, float]) -> float:
        keys = set(a) | set(b)
        if not keys:
            return 0.0
        dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
        na = math.sqrt(sum(a.get(k, 0.0) ** 2 for k in keys))
        nb = math.sqrt(sum(b.get(k, 0.0) ** 2 for k in keys))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def _memory_reconsolidation(self, v: Dict[str, float]):
        valence = v.get("belonging", 0.0) - v.get("threat", 0.0)
        intensity = math.sqrt(sum(x * x for x in v.values()))
        trust = min(self.fluid["信任"], self.max_trust)
        fear = self.fluid["恐惧"]
        safety = trust * (1.0 - fear)

        best_idx, best_sim = -1, 0.0
        for i, t in enumerate(self.memory_traces):
            sim = self._vec_sim(v, t["vector"])
            if sim > best_sim:
                best_sim, best_idx = sim, i

        now = self._now()
        if best_idx >= 0 and best_sim > (1.0 - self.RECONSOL_RADIUS):
            tr = self.memory_traces[best_idx]
            if safety > self.SAFETY_THRESHOLD:
                tr["strength"] *= 0.85
            else:
                tr["strength"] = min(1.0, tr["strength"] + intensity * 0.2)
            tr["timestamp"] = now
            tr["age"] = 0.0
            tr["count"] = tr.get("count", 1) + 1
        else:
            trace = {
                "vector": dict(v),
                "strength": min(1.0, intensity),
                "valence": valence,
                "timestamp": now,
                "age": 0.0,
                "count": 1,
            }
            self.memory_traces.append(trace)
            if len(self.memory_traces) > self.MAX_MEMORY_TRACES:
                self.memory_traces.sort(
                    key=lambda t: t["strength"] * (1.0 + math.log1p(t.get("count", 1))))
                self.memory_traces.pop(0)

    # ==================================================================
    # 3. 创伤
    # ==================================================================
    def _apply_trauma(self, key: str, magnitude: float):
        cur = self.trauma_state.get(key, 0.0)
        gain = magnitude * (1.0 - self.psychological_resilience) * 0.7
        self.trauma_state[key] = min(1.0, cur + gain)

    def _heal_traumas(self, dt: float):
        rate = self.TRAUMA_HEAL_RATE * (0.3 + self.psychological_resilience) * dt
        healed = []
        for k, v in list(self.trauma_state.items()):
            nv = v - rate
            if nv <= 0.01:
                healed.append(k)
            else:
                self.trauma_state[k] = nv
        for k in healed:
            del self.trauma_state[k]

    # ==================================================================
    # 4. 信任容量腐蚀 & 恢复
    # ==================================================================
    def _erode_trust(self, magnitude: float):
        factor = 1.0 - (1.0 - self.TRUST_ERODE) * min(1.0, magnitude)
        self.max_trust = max(0.1, self.max_trust * factor)

    def _recover_trust(self, dt: float):
        if self.max_trust < 1.0:
            recover = self.TRUST_RECOVER * dt * (1.01 - self.max_trust)
            self.max_trust = min(1.0, self.max_trust + recover)

    # ==================================================================
    # 5. 隐压累积 + 雪崩
    # ==================================================================
    def _latent_accumulate(self, v: Dict[str, float]):
        neg = max(0.0, -v.get("belonging", 0.0)) + max(0.0, v.get("threat", 0.0))
        self.latent_pressure += neg * 0.4
        if self.latent_pressure >= self.LATENT_THRESHOLD and self.avalanche_cd <= 0:
            self._trigger_avalanche()

    def _trigger_avalanche(self):
        self.avalanche_cd = self.LATENT_COOLDOWN
        overflow = self.latent_pressure - self.LATENT_THRESHOLD + 0.5
        self.latent_pressure = 0.3
        self.fluid["愤怒"] = min(1.0, self.fluid["愤怒"] + overflow * 0.5)
        self.fluid["恐惧"] = min(1.0, self.fluid["恐惧"] + overflow * 0.3)
        self.fluid["张力"] = min(1.0, self.fluid["张力"] + overflow * 0.3)
        self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + overflow * 0.2)
        self.fluid["信任"] = max(0.0, self.fluid["信任"] - overflow * 0.3)
        self.fluid["喜悦"] = max(0.0, self.fluid["喜悦"] - overflow * 0.3)
        self.energy = max(self.ENERGY_MIN, self.energy - overflow * 10)
        self.time_compress_base = min(1.0, self.time_compress_base + 0.5)

    # ==================================================================
    # 6. 向量 → 流体瞬时映射（V8.0: 加入羞耻路径）
    # ==================================================================
    def _vector_to_fluid(self, v: Dict[str, float]):
        b = v.get("belonging", 0.0)
        t = v.get("threat", 0.0)
        a = v.get("autonomy", 0.0)
        f = v.get("fatigue", 0.0)
        s = v.get("shame_trigger", 0.0)  # V8.0: 羞耻触发器

        # ── V8.0 羞耻路径 ──
        # 羞耻是"我这个人有问题"，由自我相关负面评价触发
        # 与愧疚不同——愧疚是"我做的事有问题"
        if s > 0:
            self.fluid["羞耻"] = min(1.0, self.fluid["羞耻"] + s * 0.7)
            self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + s * 0.3)
            # 羞耻让人退缩（降低愤怒，增加恐惧和疏离）
            self.fluid["愤怒"] = max(0.0, self.fluid["愤怒"] - s * 0.3)
            self.fluid["恐惧"] = min(1.0, self.fluid["恐惧"] + s * 0.25)
        # 负向归属 + 低自尊 → 更容易产生羞耻而非愤怒
        elif b < -0.3 and self.self_esteem < 0.35:
            shame_leak = (-b) * 0.3 * (0.5 - self.self_esteem)
            self.fluid["羞耻"] = min(1.0, self.fluid["羞耻"] + shame_leak)
            self.fluid["愤怒"] = min(1.0, self.fluid["愤怒"] + (-b) * 0.4)  # 愤怒减少了
            self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + (-b) * 0.5)
            self.fluid["愧疚"] = min(1.0, self.fluid["愧疚"] + (-b) * 0.2)
        # 负向归属（标准路径）
        elif b < 0:
            self.fluid["愤怒"] = min(1.0, self.fluid["愤怒"] + (-b) * 0.7)
            self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + (-b) * 0.4)
            self.fluid["愧疚"] = min(1.0, self.fluid["愧疚"] + (-b) * 0.15)
            if self.psychological_resilience > 0.6:
                self.fluid["张力"] = min(1.0, self.fluid["张力"] + (-b) * 0.3)
                self.fluid["愤怒"] *= 0.8
        # 正向归属 → 喜悦/信任，愤怒/疏离/羞耻回落
        if b > 0:
            self.fluid["喜悦"] = min(1.0, self.fluid["喜悦"] + b * 0.6)
            self.fluid["信任"] = min(self.max_trust, self.fluid["信任"] + b * 0.25)
            self.fluid["愤怒"] = max(0.0, self.fluid["愤怒"] - b * 0.4)
            self.fluid["疏离"] = max(0.0, self.fluid["疏离"] - b * 0.3)
            self.fluid["羞耻"] = max(0.0, self.fluid["羞耻"] - b * 0.3)
        # 威胁 → 恐惧/张力
        if t > 0:
            self.fluid["恐惧"] = min(1.0, self.fluid["恐惧"] + t * 0.8)
            self.fluid["张力"] = min(1.0, self.fluid["张力"] + t * 0.6)
            self.fluid["信任"] = max(0.0, self.fluid["信任"] - t * 0.2)
        # 自主 → 喜悦
        if a > 0:
            self.fluid["喜悦"] = min(1.0, self.fluid["喜悦"] + a * 0.3)
        # 疲劳 → 削减喜悦、增加张力
        if f > 0:
            self.fluid["喜悦"] = max(0.0, self.fluid["喜悦"] - f * 0.3)
            self.fluid["张力"] = min(1.0, self.fluid["张力"] + f * 0.2)

        # 所有维度夹紧
        self.fluid["信任"] = min(self.fluid["信任"], self.max_trust)
        for k in self.fluid:
            self.fluid[k] = max(0.0, min(1.0, self.fluid[k]))

        # 兴奋调制
        if self.excitation > 0.5:
            extra = (self.excitation - 0.5) * 0.4
            self.fluid["喜悦"] = min(1.0, self.fluid["喜悦"] + extra * max(0.0, b))
            self.fluid["愤怒"] = min(1.0, self.fluid["愤怒"] + extra * max(0.0, -b))
            self.fluid["恐惧"] = min(1.0, self.fluid["恐惧"] + extra * max(0.0, t))
            self.fluid["张力"] = min(1.0, self.fluid["张力"] + extra * max(0.0, t, -b) * 0.5)

    # ==================================================================
    # 7. 压抑动力学（保持不变）
    # ==================================================================
    def _suppression_dynamics(self, v: Dict[str, float]):
        neg = (max(0.0, self.fluid["愤怒"])
               + max(0.0, self.fluid["恐惧"])
               + max(0.0, self.fluid["疏离"]))
        will_to_suppress = (self.energy / 100.0) * (0.3 + self.psychological_resilience)
        suppressed_here = neg * will_to_suppress * 0.5
        if suppressed_here > 0.05:
            self.suppression_load += suppressed_here
            self.fluid["愤怒"] *= (1.0 - will_to_suppress * 0.6)
            self.fluid["恐惧"] *= (1.0 - will_to_suppress * 0.4)
            self.fluid["张力"] = min(1.0, self.fluid["张力"] + suppressed_here * 0.3)

        if self.suppression_load >= self.SUPPRESSION_THRESHOLD and self.suppression_burst_cd <= 0:
            self._trigger_burst()

    def _trigger_burst(self):
        self.suppression_burst_cd = self.SUPPRESSION_BURST_COOLDOWN
        load = self.suppression_load
        self.suppression_load = 0.0
        self.fluid["愤怒"] = min(1.0, self.fluid["愤怒"] + load * 0.6)
        self.fluid["张力"] = min(1.0, self.fluid["张力"] + load * 0.4)
        self.fluid["喜悦"] = max(0.0, self.fluid["喜悦"] - load * 0.3)
        self.fluid["信任"] = max(0.0, self.fluid["信任"] - load * 0.2)
        self.energy = max(self.ENERGY_MIN, self.energy - load * 8)
        self.time_compress_base = min(1.0, self.time_compress_base + 0.7)
        self._apply_trauma("threat", load * 0.1)

    # ==================================================================
    # 8. 动态粘滞度 / 心理时间
    # ==================================================================
    def _update_dynamic_viscosity(self):
        base = self.VISC_BASE
        self.dynamic_viscosity = (base
                                  + self.VISC_TENSION_K * self.fluid["张力"]
                                  + self.VISC_FATIGUE_K * self.fatigue
                                  + self.mood["紧张"] * 0.15     # V8.0: 心境紧张加剧粘滞
                                  + self.sleep_debt * 0.1)        # V8.0: 缺觉让情绪更钝
        self.dynamic_viscosity -= self.excitation * 0.08
        self.dynamic_viscosity = max(0.02, min(1.5, self.dynamic_viscosity))
        self.psy_dilation = 1.0 + self.time_compress_base * 2.0

    def _psychological_dt_for(self, real_dt: float) -> float:
        return real_dt * self.psy_dilation / (0.1 + self.dynamic_viscosity)

    # ==================================================================
    # 9. 流体连续松弛
    # ==================================================================
    def _fluid_dynamics(self, dt: float):
        k = 1.0 / (0.2 + self.dynamic_viscosity * 3.0)
        alpha = 1.0 - math.exp(-k * max(0.0, dt))
        alpha = max(0.0, min(1.0, alpha))
        for key in self.fluid:
            tgt = self.fluid_target.get(key, self.fluid[key])
            if key == "信任":
                tgt = min(tgt, self.max_trust)
            self.fluid[key] += (tgt - self.fluid[key]) * alpha
            self.fluid[key] = max(0.0, min(1.0, self.fluid[key]))

    # ==================================================================
    # 自适应基线演化（AAE-A · 默认关闭）
    # ==================================================================
    def _adapt_baseline(self, dt: float, has_event: bool = False) -> None:
        """让人格基线受经历牵引而漂移，同时被回归项与硬边界约束。

        牵引按「次」计（仅事件处理后结算），回归按「时间」计（每个时间步都结算）。
        合成的净效果：
          · 刚经历事件 → 基线向当时的情绪方向挪一点
          · 长期平静   → 牵引不再触发，回归项把基线持续拉回出厂值

        因此角色会被经历改变，但不会无限漂成另一个人。
        确定性：纯算术，无随机；重放同一事件序列必得同一基线轨迹。
        """
        if not self.baseline_adaptation or dt <= 0:
            return
        for key in self.fluid:
            if key not in self.fluid_baseline:
                continue
            base = self.fluid_baseline[key]
            # 出厂锚点缺失时以当前基线为锚：此时回归项为零，行为退化为纯牵引
            factory = self._baseline_factory.get(key, base)
            # 牵引项：只在刚经历事件后结算（平静期的内因波动不改写人格）
            pull_step = 0.0
            if has_event:
                pull_step = (self.fluid[key] - base) * self.ADAPT_RATE_EVENT
            # 回归项：始终朝向出厂值
            regress_step = (factory - base) * self.ADAPT_REGRESS * dt
            # 三项钳制，缺一不可：
            #   ① 分项各自钳——否则量纲大的一项会淹没另一项
            #   ② 总和再钳——ADAPT_MAX_STEP 的语义是「单次结算的总改变量」
            lim = self.ADAPT_MAX_STEP
            pull_step = max(-lim, min(lim, pull_step))
            regress_step = max(-lim, min(lim, regress_step))
            step = max(-lim, min(lim, pull_step + regress_step))
            lo, hi = self.ADAPT_BOUNDS.get(key, (0.0, 1.0))
            self.fluid_baseline[key] = max(lo, min(hi, base + step))

    # ==================================================================
    # target 重建：基线 + 创伤牵引 + 记忆共振 + 心境牵引
    # ==================================================================
    def _rebuild_fluid_target(self):
        for k, v in self.fluid_baseline.items():
            self.fluid_target[k] = v

        # ── V8.0 心境牵引 target ──
        # 心境好 → 喜悦 target 抬高、愤怒/疏离 target 压低
        mp = self.mood["愉悦"]
        self.fluid_target["喜悦"] = min(1.0, self.fluid_target["喜悦"] + (mp - 0.5) * 0.3)
        self.fluid_target["愤怒"] = max(0.0, self.fluid_target["愤怒"] - (mp - 0.5) * 0.15)
        self.fluid_target["疏离"] = max(0.0, self.fluid_target["疏离"] - (mp - 0.5) * 0.15)

        # ── V8.0 自尊牵引 target ──
        # 低自尊 → 羞耻 target 抬高
        self.fluid_target["羞耻"] = max(0.0, self.fluid_target["羞耻"] +
                                        (0.5 - self.self_esteem) * 0.2)

        # ── V8.0 睡眠债牵引 target ──
        # 缺觉 → 张力 + 恐惧 target 抬高，喜悦 target 压低
        sd = self.sleep_debt
        self.fluid_target["张力"] = min(1.0, self.fluid_target["张力"] + sd * 0.25)
        self.fluid_target["恐惧"] = min(1.0, self.fluid_target["恐惧"] + sd * 0.15)
        self.fluid_target["喜悦"] = max(0.0, self.fluid_target["喜悦"] - sd * 0.2)

        # 创伤牵引
        if "threat" in self.trauma_state:
            w = self.trauma_state["threat"] * self.TRAUMA_BIAS
            self.fluid_target["恐惧"] = min(1.0, self.fluid_target["恐惧"] + w)
            self.fluid_target["张力"] = min(1.0, self.fluid_target["张力"] + w * 0.8)
            self.fluid_target["信任"] = max(0.0, self.fluid_target["信任"] - w * 0.5)
        if "betrayal" in self.trauma_state:
            w = self.trauma_state["betrayal"] * self.TRAUMA_BIAS
            self.fluid_target["疏离"] = min(1.0, self.fluid_target["疏离"] + w)
            self.fluid_target["信任"] = max(0.0, self.fluid_target["信任"] - w * 0.7)
            self.fluid_target["愤怒"] = min(1.0, self.fluid_target["愤怒"] + w * 0.3)

        # 记忆共振
        now = self._now()
        for tr in self.memory_traces:
            age = now - tr["timestamp"]
            weight = tr["strength"] * math.exp(-self.forgetting_rate * age / 20.0)
            if weight < 0.02:
                continue
            vec = tr["vector"]
            if vec.get("threat", 0.0) > 0:
                self.fluid_target["恐惧"] = min(1.0,
                    self.fluid_target["恐惧"] + weight * 0.1 * vec["threat"])
            if vec.get("belonging", 0.0) < 0:
                self.fluid_target["疏离"] = min(1.0,
                    self.fluid_target["疏离"] + weight * 0.1 * (-vec["belonging"]))
                self.fluid_target["信任"] = max(0.0,
                    self.fluid_target["信任"] - weight * 0.08 * (-vec["belonging"]))
            elif vec.get("belonging", 0.0) > 0:
                self.fluid_target["喜悦"] = min(1.0,
                    self.fluid_target["喜悦"] + weight * 0.1 * vec["belonging"])

        for k in self.fluid_target:
            self.fluid_target[k] = max(0.0, min(1.0, self.fluid_target[k]))

    # ==================================================================
    # 10. 流体 → 系统反馈
    # ==================================================================
    def _fluid_to_system_feedback(self):
        tension = self.fluid["张力"]
        self.psy_dilation = 1.0 + self.time_compress_base * 2.0 + tension * 0.5
        guilt = self.fluid["愧疚"]
        if guilt > 0.3 and self.max_trust < 1.0:
            self.max_trust = min(1.0, self.max_trust + guilt * 0.0001)
        # V8.0: 羞耻 → 自尊被侵蚀
        shame = self.fluid.get("羞耻", 0.0)
        if shame > 0.4:
            self.self_esteem = max(0.1, self.self_esteem - shame * 0.0005)

    # ==================================================================
    # 11. 能量代谢
    # ==================================================================
    def _energy_on_event(self, v: Dict[str, float], raw_intensity: float):
        cost = self.ENERGY_EVENT_COST * raw_intensity
        if v.get("threat", 0.0) > 0.2 or v.get("belonging", 0.0) < -0.2:
            cost *= 1.8
        cost *= (1.0 + self.fluid["张力"])
        # V8.0: 认知失调额外消耗能量
        cost *= (1.0 + self.cognitive_dissonance * 0.5)
        self.energy = max(self.ENERGY_MIN, self.energy - cost)

    def _energy_idle(self, dt: float):
        recover = self.ENERGY_RECOVER * dt * (1.0 - 0.5 * self.fatigue)
        # V8.0: 睡眠债降低能量恢复效率
        recover *= (1.0 - self.sleep_debt * 0.4)
        self.energy = min(self.ENERGY_MAX, self.energy + recover)

    # ==================================================================
    # 12. 艾宾浩斯遗忘曲线
    # ==================================================================
    def _forget_over(self, dt: float):
        survivors = []
        now = self._now()
        for tr in self.memory_traces:
            age = now - tr["timestamp"]
            strength = tr["strength"] * math.exp(-self.forgetting_rate * age / 10.0)
            if strength > self.trace_importance_threshold:
                tr["strength"] = strength
                tr["age"] = age
                survivors.append(tr)
        self.memory_traces = survivors

    # ==================================================================
    # 13. 兴奋/唤醒系统
    # ==================================================================
    def _excitation_on_event(self, v: Dict[str, float], raw_intensity: float):
        novelty = raw_intensity * self.EXCITATION_NOVELTY_GAIN
        if abs(v.get("threat", 0.0)) > 0.5 or abs(v.get("belonging", 0.0)) > 0.5:
            novelty += raw_intensity * self.EXCITATION_SALIENCE_BOOST
        self.excitation = min(self.EXCITATION_MAX, self.excitation + novelty)

    def _excitation_decay(self, dt: float):
        if self.excitation > self.EXCITATION_BASELINE:
            self.excitation += (self.EXCITATION_BASELINE - self.excitation) * \
                              (1.0 - math.exp(-self.EXCITATION_DECAY * dt))
            if abs(self.excitation - self.EXCITATION_BASELINE) < 0.005:
                self.excitation = self.EXCITATION_BASELINE

    def _check_boredom(self, dt: float):
        if self.excitation < self.EXCITATION_BOREDOM_THRESHOLD:
            self.fluid["张力"] = min(1.0, self.fluid["张力"] + 0.003 * dt / 60)
            self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + 0.002 * dt / 60)

    # ==================================================================
    # 14. V8.0 心境更新（慢变量）
    # ==================================================================
    def _mood_event_dose(self, v: Dict[str, float]):
        """事件对心境的受迫项（事件驱动）。

        事件的唤醒度（threat / belonging / autonomy 的绝对幅度）决定这次
        事件把背景心境推开多远：越强烈的情绪，心境被带得越远。

        这里吃的是已被防御机制削减后的向量——被否认的事件不应对背景心境
        产生与其表露程度相称的冲击。

        与 _update_mood 的分工：
            _mood_event_dose —— 受迫：把心境推离靶标（位移，依赖事件）
            _update_mood     —— 阻尼：把心境拉回靶标（松弛，依赖时间）
        """
        arousal = (abs(v.get("threat", 0.0))
                   + abs(v.get("belonging", 0.0))
                   + abs(v.get("autonomy", 0.0)))
        if arousal <= 0.0:
            return
        arousal = min(1.0, arousal)

        # 唤醒进入慢记忆，供松弛速率使用：强情绪更易消退
        self.arousal_recent += ((arousal - self.arousal_recent)
                                * self.MOOD_AROUSAL_EMA)

        b = v.get("belonging", 0.0)
        t = max(0.0, v.get("threat", 0.0))
        self.mood["愉悦"] = max(0.0, min(1.0, self.mood["愉悦"]
                               + self.MOOD_DOSE_PLEASANT * arousal * b))
        self.mood["紧张"] = max(0.0, min(1.0, self.mood["紧张"]
                               + self.MOOD_DOSE_TENSION * arousal
                               * (t + max(0.0, -b))))
        self.mood["精力"] = max(0.0, min(1.0, self.mood["精力"]
                               + self.MOOD_DOSE_VIGOR * arousal
                               * max(0.0, v.get("autonomy", 0.0))))

    def _update_mood(self, dt: Optional[float] = None):
        """
        心境是慢变量，按时间松弛到靶标。

        靶标由以下因素牵引：
        - 流体情绪的平均水平（持续愤怒 → 心境紧张上升）
        - 自尊（低自尊 → 心境愉悦下降）
        - 睡眠债（缺觉 → 心境精力下降、紧张上升）
        - 认知失调（内心冲突 → 心境紧张上升）

        收敛速率不是常数，而是由近期唤醒动态计算：

            k     = MOOD_RATE_BASE * (1 + MOOD_AROUSAL_GAIN * arousal_recent)
            alpha = 1 - exp(-k * dt)

        即"强情绪更易消退"：唤醒越高，心境惯性越小、回稳越快。
        alpha 用 1-exp(-k*dt) 而非线性近似 k*dt，是为了与 _fluid_dynamics
        保持同一种 dt 一致的积分形式——结果只依赖经过的真实时间，
        不依赖调用被切分成多少步。

        Args:
            dt: 经过的真实秒数。None 时按 _now() - last_time 自动取值。
        """
        # 目标心境
        target_pleasant = (self.fluid["喜悦"] * 0.4
                           - self.fluid["愤怒"] * 0.3
                           - self.fluid["恐惧"] * 0.25
                           - self.fluid["疏离"] * 0.2
                           - self.fluid["羞耻"] * 0.3
                           + self.self_esteem * 0.4
                           + 0.3)  # 中性基线偏移
        target_pleasant = max(0.0, min(1.0, target_pleasant))

        target_tension = (self.fluid["张力"] * 0.5
                          + self.fluid["恐惧"] * 0.3
                          + self.cognitive_dissonance * 0.3
                          + self.sleep_debt * 0.3
                          + 0.1)
        target_tension = max(0.0, min(1.0, target_tension))

        target_vigor = (1.0
                        - self.fatigue * 0.5
                        - self.sleep_debt * 0.6
                        - self.fluid["张力"] * 0.2
                        + self.self_esteem * 0.3)
        target_vigor = max(0.0, min(1.0, target_vigor))

        if dt is None:
            dt = max(0.0, self._now() - self.last_time)
        dt = max(0.0, min(dt, 86400.0))

        # 唤醒记忆随时间消散（没有新事件时，速率回到基础值）
        self.arousal_recent *= math.exp(-dt / self.MOOD_AROUSAL_TAU)

        # 向靶标松弛：速率随近期唤醒动态计算
        k = self.MOOD_RATE_BASE * (1.0 + self.MOOD_AROUSAL_GAIN
                                   * self.arousal_recent)
        alpha = 1.0 - math.exp(-k * dt)
        alpha = max(0.0, min(1.0, alpha))
        self.mood["愉悦"] += (target_pleasant - self.mood["愉悦"]) * alpha
        self.mood["紧张"] += (target_tension - self.mood["紧张"]) * alpha
        self.mood["精力"] += (target_vigor - self.mood["精力"]) * alpha

    # ==================================================================
    # 15. V8.0 梦境加工
    # ==================================================================
    def _dream_process(self):
        """
        单个睡眠周期（~90 分钟）中的梦境情绪加工：

        1. 记忆情绪衰减——保留事实，降低情绪电荷
           （这就是为什么"睡一觉就觉得没那么严重了"）
        2. 恐惧消退——在安全的"梦中环境"重新暴露于威胁记忆，
           降低其威胁关联（Phelps 2004 的睡眠恐惧消退理论）
        3. 创伤愈合——在 REM 睡眠中，去甲肾上腺素水平极低，
           这是唯一能在无应激状态下重演创伤的窗口
        """
        # 记忆情绪衰减
        for tr in self.memory_traces:
            vec = tr["vector"]
            # 情绪电荷衰减，但事实结构保留
            for k in list(vec.keys()):
                if abs(vec[k]) > 0.05:
                    vec[k] *= (1.0 - self.DREAM_EMOTION_DECAY)

        # 恐惧消退：找到威胁类记忆，在安全环境中减弱
        for tr in self.memory_traces:
            if tr["vector"].get("threat", 0.0) > 0.1:
                # 低自尊者在梦中更难消退恐惧（反复噩梦）
                extinction = (self.DREAM_FEAR_EXTINCTION
                              * (0.4 + self.self_esteem * 1.2))
                tr["vector"]["threat"] *= (1.0 - extinction)
                tr["strength"] *= (1.0 - extinction * 0.5)

        # 创伤额外愈合
        self._heal_traumas(90.0 * 60.0 * self.DREAM_TRAUMA_HEAL_BOOST * 0.1)

    # ==================================================================
    # 16. V8.0 预期系统
    # ==================================================================
    def _compute_surprise(self, event_id: str, vector: Dict[str, float],
                          intensity: float) -> float:
        """
        计算预期与实际之间的 surprise 信号。

        返回值：surprise ∈ [-1, 1]
          > 0: 正向惊喜（比预期好）
          < 0: 负向惊喜/失望（比预期差）
        """
        exp = self.expected_events.pop(event_id)
        expected_valence = exp["valence"]
        confidence = exp["confidence"]

        # 从 vector 推断实际效价
        actual_valence = (vector.get("belonging", 0.0)
                          - vector.get("threat", 0.0)
                          + vector.get("autonomy", 0.0))

        # 标准化到 [-1, 1]
        actual_valence = max(-1.0, min(1.0, actual_valence))

        # surprise = (实际 - 预期) × 确信度
        # 越确信 → 落差越剧烈
        surprise = (actual_valence - expected_valence) * confidence

        # 预期时间跨度（预期越久远，落空越不意外）
        age = self._now() - exp.get("time", self._now())
        age_discount = math.exp(-0.00001 * age)  # ~1天半衰期
        surprise *= age_discount

        return max(-1.0, min(1.0, surprise))

    def _apply_surprise(self, perceived: Dict[str, float],
                        surprise: float) -> Dict[str, float]:
        """将 surprise 注入 perceived vector。"""
        out = dict(perceived)
        if surprise > 0.1:
            # 正向惊喜 → 喜悦加成、威胁减弱
            out["belonging"] = out.get("belonging", 0.0) + surprise * self.SURPRISE_POSITIVE_BOOST
            out["threat"] = out.get("threat", 0.0) - surprise * self.SURPRISE_POSITIVE_BOOST * 0.5
        elif surprise < -0.1:
            # 负向失望 → 威胁放大、归属感额外受损
            mag = abs(surprise)
            out["threat"] = out.get("threat", 0.0) + mag * self.SURPRISE_NEGATIVE_BOOST
            out["belonging"] = out.get("belonging", 0.0) - mag * self.SURPRISE_NEGATIVE_BOOST * 0.7
        return out

    def _decay_expectations(self, dt: float):
        """预期自然衰减——太久没兑现的预期会淡化。"""
        now = self._now()
        expired = []
        for eid, exp in self.expected_events.items():
            age = now - exp.get("time", now)
            # 超过 7 天的预期几乎消失，或信心随时间降低
            decay = self.EXPECTATION_DECAY * dt
            exp["confidence"] = max(0.0, exp["confidence"] - decay)
            if exp["confidence"] < 0.05:
                expired.append(eid)
        for eid in expired:
            del self.expected_events[eid]

    # ==================================================================
    # 17. V8.0 自尊动态
    # ==================================================================
    def _update_self_esteem(self, v: Dict[str, float]):
        """
        自尊根据社会反馈缓慢更新。

        归因逻辑（内隐的，不是显式的）：
        - 正向归属 → 自尊上升（"他们认可我，说明我有价值"）
        - 负向归属 → 自尊下降（"我被拒绝，说明我不够好"）
        - 低自尊放大负向、缩小正向（经典的归因偏差）
        - 高自尊放大正向、缩小负向

        自尊的惯性极大——不会因为一句话就崩塌或膨胀。
        """
        b = v.get("belonging", 0.0)
        t = v.get("threat", 0.0)
        a = v.get("autonomy", 0.0)

        # 计算此次事件的自尊冲击
        impact = 0.0
        if b > 0:
            # 成功/认可 → 自尊上升（但低自尊者不敢信）
            impact += b * self.SELF_ESTEEM_UPDATE_RATE * (0.3 + self.self_esteem * 1.4)
        if b < 0:
            # 拒绝/失败 → 自尊下降（低自尊者伤更深）
            impact -= abs(b) * self.SELF_ESTEEM_UPDATE_RATE * (1.5 - self.self_esteem)
        if a > 0:
            # 自主/掌控感 → 自尊上升
            impact += a * self.SELF_ESTEEM_UPDATE_RATE * 0.5
        if t > 0 and b < 0:
            # 威胁 + 被拒绝 → 自尊双倍打击（"危险的，还是我的错"）
            impact -= t * abs(b) * self.SELF_ESTEEM_UPDATE_RATE * 0.8

        # 缓慢更新
        self.self_esteem += impact * self.SELF_ESTEEM_INERTIA
        self.self_esteem = max(0.05, min(0.95, self.self_esteem))

    # ==================================================================
    # 18. V8.0 认知失调动力学
    # ==================================================================
    def _dissonance_dynamics(self, v: Dict[str, float]):
        """
        认知失调的自动消解尝试。

        当存在显著失调且当前没有更强刺激时：
        - 合理化（rationalization_load 上升）→ "其实也没那么糟"
        - 信念微调（自尊微调）→ "也许我的标准太严了"
        - 失调本身随时间衰减（遗忘/接受）
        """
        if self.cognitive_dissonance > self.DISSONANCE_THRESHOLD:
            # 高失调触发主动合理化
            rationalize_amount = self.cognitive_dissonance * 0.15
            self.rationalization_load = min(1.0, self.rationalization_load + rationalize_amount)
            self.cognitive_dissonance *= 0.85
            # 合理化消耗能量
            self.energy = max(self.ENERGY_MIN, self.energy - rationalize_amount * 2.0)
            # 合理化让人暂时舒服（张力下降）
            self.fluid["张力"] = max(0.0, self.fluid["张力"] - rationalize_amount * 0.2)

    # ==================================================================
    # 19. V8.0 防御机制层级
    # ==================================================================
    def _defense_allocation(self, v: Dict[str, float]
                            ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        防御机制的分配阶段：层级 1 否认 → 层级 2 合理化。

        必须在情绪写入流体之前调用。被否认 / 被合理化的部分要从
        "被感知的向量"中真正扣除，而不是只记进仓库了事——否则
        "否认成功 → 威胁感知降低"在情绪流体上并不成立。

        层级 1: 否认（Denial）
          "这不可能"——直接拒绝接受威胁性信息。
          最原始的防御，消耗最小，但不可持续。
          否认过载 → 现实侵入（denial burst）。

        层级 2: 合理化（Rationalization）
          "其实也没那么糟"——给事件找一个能接受的理由。
          比否认成熟，但仍扭曲现实。

        层级 3: 压抑（Suppression）不在本方法内——它需要读取已经
        含本次事件影响的流体状态，因此由调用方在 _vector_to_fluid
        之后执行。

        Returns:
            (defended, residual)
            defended —— 实际驱动情绪流体的向量
            residual —— 交给层级 3 压抑消费的剩余负性
        """
        defended = dict(v)
        threat = defended.get("threat", 0.0)
        neg_belonging = max(0.0, -defended.get("belonging", 0.0))
        total_neg = threat + neg_belonging

        if total_neg < 0.1:
            return defended, dict(defended)

        # 低自尊 → 更倾向否认（不敢面对）
        denial_tendency = 0.3 * (1.0 - self.self_esteem)

        # 层级 1: 否认
        denied = total_neg * denial_tendency
        if denied > 0.02:
            self.denial_load += denied
            # 否认成功 → 威胁感知确实降低
            remaining_denial = 1.0 - denial_tendency
            if "threat" in defended:
                defended["threat"] *= remaining_denial
            if defended.get("belonging", 0.0) < 0:
                defended["belonging"] *= remaining_denial

            # 否认过载 → 现实侵入
            if (self.denial_load >= self.DENIAL_THRESHOLD
                    and self.denial_burst_cd <= 0):
                self._trigger_denial_burst()

        # 层级 2: 合理化
        rationalize_tendency = 0.2
        remaining_neg = (defended.get("threat", 0.0)
                         + max(0.0, -defended.get("belonging", 0.0)))
        rationalized = remaining_neg * rationalize_tendency
        if rationalized > 0.02:
            self.rationalization_load = min(1.0,
                                           self.rationalization_load + rationalized)
            # 合理化让表面情绪更可控
            if "threat" in defended:
                defended["threat"] *= (1.0 - rationalize_tendency)
            if defended.get("belonging", 0.0) < 0:
                defended["belonging"] *= (1.0 - rationalize_tendency * 0.5)

        # 层级 3 的残余量由调用方在流体更新后消费
        return defended, dict(defended)

    def _trigger_denial_burst(self):
        """否认过载 → 现实侵入。被否认的东西一次性涌回来。"""
        self.denial_burst_cd = self.DENIAL_BURST_COOLDOWN
        load = self.denial_load
        self.denial_load = 0.0
        # 现实感突然袭来
        self.fluid["恐惧"] = min(1.0, self.fluid["恐惧"] + load * 0.7)
        self.fluid["张力"] = min(1.0, self.fluid["张力"] + load * 0.5)
        self.fluid["疏离"] = min(1.0, self.fluid["疏离"] + load * 0.4)
        self.fluid["信任"] = max(0.0, self.fluid["信任"] - load * 0.3)
        self.energy = max(self.ENERGY_MIN, self.energy - load * 6)
        self.time_compress_base = min(1.0, self.time_compress_base + 0.5)

# ================================================================
# LLM 适配器接口 — 可插拔，支持多个 LLM 后端
# ================================================================
# 用法：
#   adapter = OpenAIAdapter(api_key="sk-...", model="gpt-4o")
#   line = adapter.generate(prompt_injection, style_example="…")
#
#   或使用 ChainAdapter 自动回退：
#   adapter = ChainAdapter(
#     primary=OpenAIAdapter(api_key="sk-..."),
#     fallback=ClaudeAdapter(api_key="sk-...")
#   )
#   line = adapter.generate(prompt_injection)
# ================================================================

from abc import ABC, abstractmethod


class LLMAdapter(ABC):
    """
    大模型接口抽象基类。

    所有 LLM 后端（OpenAI / Claude / 文心 / 本地）统一实现此接口。
    """

    @abstractmethod
    def generate(self, prompt_injection: str,
                 style_example: str = "",
                 system_prompt: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 return_usage: bool = False
                 ) -> Union[Optional[str], Tuple[Optional[str], Optional[TokenUsage]]]:
        """
        根据 prompt_injection 生成台词。

        Args:
            prompt_injection: LanguageStyleEngine 输出的风格指令
            style_example: 可选 few-shot 示例台词
            system_prompt: 可选系统提示词，覆盖默认
            temperature: 采样温度
            max_tokens: 最大生成 token 数
            return_usage: True 时返回 (台词, TokenUsage) 元组

        Returns:
            return_usage=False: 生成的台词字符串，失败返回 None
            return_usage=True:  (台词, TokenUsage) 元组
        """
        ...


class OpenAIAdapter(LLMAdapter):
    """OpenAI / 兼容 API 适配器（GPT-4o, o1, DeepSeek, 通义千问等）"""

    DEFAULTS = {
        "api_base": "https://api.openai.com/v1",
        "model": "gpt-4o",
        "system_prompt": "你是一个角色语言生成器。根据给定的风格指令，产出一句符合角色当前情感状态的中文台词。不要输出解释，只输出台词本身。",
    }

    def __init__(self, api_key: str,
                 api_base: str = None,
                 model: str = None,
                 system_prompt: str = None,
                 timeout: int = 30):
        self.api_key = api_key
        self.api_base = api_base or self.DEFAULTS["api_base"]
        self.model = model or self.DEFAULTS["model"]
        self.system_prompt = system_prompt or self.DEFAULTS["system_prompt"]
        self.timeout = timeout

    def generate(self, prompt_injection: str,
                 style_example: str = "",
                 system_prompt: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 return_usage: bool = False
                 ) -> Union[Optional[str], Tuple[Optional[str], Optional[TokenUsage]]]:
        import urllib.request
        import urllib.error

        sp = system_prompt or self.system_prompt
        user_content = prompt_injection
        if style_example:
            user_content += f"\n\n参考台词风格：{style_example}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": sp},
                {"role": "user", "content": user_content},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        req = urllib.request.Request(
            f"{self.api_base.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                choice = body.get("choices", [{}])[0]
                content = choice.get("message", {}).get("content", "")
                result = content.strip() if content else None

                usage_data = body.get("usage", {}) or {}
                usage = TokenUsage(
                    prompt_tokens=usage_data.get("prompt_tokens", 0),
                    completion_tokens=usage_data.get("completion_tokens", 0),
                    total_tokens=usage_data.get("total_tokens", 0),
                    model=body.get("model", self.model),
                ) if usage_data else None

                if return_usage:
                    return result, usage
                return result
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
            if return_usage:
                return None, None
            return None


class ClaudeAdapter(LLMAdapter):
    """Anthropic Claude 适配器"""

    DEFAULTS = {
        "api_base": "https://api.anthropic.com/v1",
        "model": "claude-3-5-sonnet-20241022",
        "system_prompt": "你是一个角色语言生成器。根据给定的风格指令，产出一句符合角色当前情感状态的中文台词。不要输出解释，只输出台词本身。",
    }

    def __init__(self, api_key: str,
                 api_base: str = None,
                 model: str = None,
                 system_prompt: str = None,
                 timeout: int = 30):
        self.api_key = api_key
        self.api_base = api_base or self.DEFAULTS["api_base"]
        self.model = model or self.DEFAULTS["model"]
        self.system_prompt = system_prompt or self.DEFAULTS["system_prompt"]
        self.timeout = timeout

    def generate(self, prompt_injection: str,
                 style_example: str = "",
                 system_prompt: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 return_usage: bool = False
                 ) -> Union[Optional[str], Tuple[Optional[str], Optional[TokenUsage]]]:
        import urllib.request
        import urllib.error

        sp = system_prompt or self.system_prompt
        user_content = prompt_injection
        if style_example:
            user_content += f"\n\n参考台词风格：{style_example}"

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": sp,
            "messages": [
                {"role": "user", "content": user_content},
            ],
        }

        req = urllib.request.Request(
            f"{self.api_base.rstrip('/')}/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                content = body.get("content", [{}])[0].get("text", "")
                result = content.strip() if content else None

                usage_data = body.get("usage", {}) or {}
                prompt_tok = usage_data.get("input_tokens", 0)
                completion_tok = usage_data.get("output_tokens", 0)
                usage = TokenUsage(
                    prompt_tokens=prompt_tok,
                    completion_tokens=completion_tok,
                    total_tokens=prompt_tok + completion_tok,
                    model=body.get("model", self.model),
                ) if usage_data else None

                if return_usage:
                    return result, usage
                return result
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
            if return_usage:
                return None, None
            return None


class ChainAdapter(LLMAdapter):
    """
    链式适配器：先尝试主 LLM，失败后自动回退。

    用法：
        adapter = ChainAdapter(
            primary=OpenAIAdapter(api_key="sk-..."),
            fallback=ClaudeAdapter(api_key="sk-...")
        )
        line = adapter.generate(prompt_injection)
        if line is None:
            line = engine.generate_line(core_snapshot, expression)
    """

    def __init__(self, primary: LLMAdapter, fallback: LLMAdapter = None):
        self.primary = primary
        self.fallback = fallback

    def generate(self, prompt_injection: str,
                 style_example: str = "",
                 system_prompt: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 return_usage: bool = False
                 ) -> Union[Optional[str], Tuple[Optional[str], Optional[TokenUsage]]]:
        result, usage = self.primary.generate(
            prompt_injection=prompt_injection,
            style_example=style_example,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            return_usage=True,
        )
        if result is not None:
            if return_usage:
                return result, usage
            return result
        if self.fallback is not None:
            result2, usage2 = self.fallback.generate(
                prompt_injection=prompt_injection,
                style_example=style_example,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                return_usage=True,
            )
            if return_usage:
                # 合并两次调用的 token 用量
                if usage and usage2:
                    merged = TokenUsage(
                        prompt_tokens=usage.prompt_tokens + usage2.prompt_tokens,
                        completion_tokens=usage.completion_tokens + usage2.completion_tokens,
                        total_tokens=usage.total_tokens + usage2.total_tokens,
                        model=f"{usage.model}->{usage2.model}",
                    )
                else:
                    merged = usage2 or usage
                return result2, merged
            return result2
        if return_usage:
            return None, usage
        return None


# ================================================================
# 端到端便利函数：引擎 + LLM 一条调用
# ================================================================
def generate_line_with_llm(
    engine,
    core_snapshot: dict,
    expression,
    adapter: LLMAdapter,
    core: Optional["SPLPureCoreV7_3"] = None,
) -> str:
    """
    便利函数：引擎渲染风格 → LLM 生成台词 → 失败回退到确定性生成。

    Args:
        engine: LanguageStyleEngine 实例
        core_snapshot: SPL 核心快照（含 fluid/mood/self_esteem 等）
        expression: 表达意图对象（含 expression_mode / emotion_hidden / silence 等）
        adapter: LLMAdapter 实例
        core: 可选 SPLPureCoreV7_3 实例，传入则自动记录 token 用量到主引擎

    Returns:
        台词字符串（LLM 成功=LLM 产出，失败=引擎确定性产出）
    """
    import time as _time

    rendered = engine.render_style(core_snapshot, expression)
    if rendered.silence_hint:
        return rendered.silence_hint

    t0 = _time.perf_counter()
    line, usage = adapter.generate(
        prompt_injection=rendered.prompt_injection,
        style_example=rendered.style_example,
        return_usage=True,
    )
    duration_ms = (_time.perf_counter() - t0) * 1000

    success = line is not None
    if core is not None:
        core.record_llm_usage(usage, success=success)
        if core.audit_logger is not None:
            model = getattr(adapter, "model", "") or (usage.model if usage else "")
            core.audit_logger.log_llm_call(
                model=model,
                prompt_preview=rendered.prompt_injection,
                usage=usage,
                duration_ms=duration_ms,
                success=success,
                error="" if success else "llm_failed",
            )

    if line is not None:
        return line

    # 回退到确定性模板
    return engine.generate_line(core_snapshot, expression)
