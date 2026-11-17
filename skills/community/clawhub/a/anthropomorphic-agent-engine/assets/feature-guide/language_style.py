# ================================================================
# 语言风格渲染系统（Language Style Engine）—— 【自设模块 / 指导说明】
# ================================================================
# 定位：MVC架构中的 View（视图层）/ Translator（翻译层）。
# 作用：监听 SPL Core V8.0 的内部状态（流体、心境、防御机制），
#      将其转化为结构化的语言学特征和 LLM 提示词指令。
#
# 【本模块定位为企业/政府接入的指导说明】
#   模块不改写底层心理引擎，只把内部状态翻译成"角色该怎么说话"的文字指令。
#   所有角色人格均由接入方【直接自设】（离散档位，无连续数学），
#   企业/政府按角色设定填表即可，无需理解内部公式。
#
# 机制：
# - 能量/疲劳决定话语的长短与语速（句长、省略号频率）。
# - 压抑/否认机制决定防御性修辞（绝对否定词、辩解性连词）。
# - 情绪流体（如羞耻、愤怒）决定语气温度与社交距离。
# - 语言人格 = 接入方自设的【表达档位】（克制/回避/亲密/直接/对抗），
#   决定内部状态如何被隐藏/扭曲后才出口（internal_state ≠ spoken_text）。
# ================================================================

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


# ================================================================
# 【语言人格模块 Language Persona】—— 表达过滤层（接入方自设）
#
# 核心原则：internal_state ≠ spoken_text
#   心理状态（SPL Core 输出）必须先经过语言人格过滤，才能变成台词。
#   一个控制欲强、情绪不外露的角色（如祁皇英），内心恐惧 0.8，
#   不会说"我担心你"，而会说"不要再做这种无意义的冒险"。
#
# 自设方式（企业/政府接入）：
#   LanguagePersona   → 直接选【表达档位】(mode) + 是否启用沉默策略(silence_policy)
#   StyleProfile      → 风格：决定【怎么说】（句长/正式度/讽刺，亦为静态自设）
#   render_style()    → 渲染：把过滤后的意图变成文字指令
# 注：本层不做连续数学，仅做轻量装配；动态部分只剩"高情绪+低能量→沉默"。
# ================================================================

@dataclass
class LanguagePersona:
    """
    角色的语言人格——由接入方【直接自设】的离散档位，不做连续数学。
    企业/政府按角色设定填下表即可，无需理解底层公式。
    """
    # 表达档位：直接选其一
    #   "restrained"      克制冷峻，情绪锁死，高控制
    #   "confrontational" 锋锐直白，正面挑明
    #   "evasive"         闪躲回避，答非所问
    #   "intimate"        松弛亲昵，卸下防备
    #   "direct"          坦率直接，情绪如常表露（默认）
    mode: str = "direct"

    # 沉默策略：高情绪 + 低能量时，是否改以动作/旁白代替语言（不说话）
    silence_policy: bool = False

    # 沉默时的动作/旁白描写（自设；留空则使用通用默认）
    silence_hint: str = ""


@dataclass
class ExpressionResult:
    """
    表达过滤输出——心理状态经人格过滤后的"该怎么说/该不该说"。
    """
    expression_mode: str              # "restrained" / "direct" / "confrontational" / "evasive" / "intimate"
    emotion_hidden: float             # 心理被隐藏比例 [0,1]
    speech_intention: str             # "indirect_protection" / "direct_disclosure" / "power_assertion" / "concealment"
    should_silence: bool              # 是否触发沉默策略
    silence_hint: str = ""            # 沉默时的动作/旁白提示（should_silence=True 时使用）


class DefenseExpression:
    """
    防御机制 → 语言的模板映射（原 defense_expression.py 职责，融入本模块）。
    当检测到高防御载荷时，返回对应的台词意图模板，供渲染层参考。
    """
    # 内部心理状态 → 表面台词模板
    UTTERANCE_TEMPLATES: Dict[str, Dict[str, str]] = {
        "denial": {
            "intention": "indirect_protection",
            "line": "只是觉得你留下更方便。",
        },
        "rationalization": {
            "intention": "concealment",
            "line": "你的能力还有利用价值。",
        },
        "projection": {
            "intention": "power_assertion",
            "line": "看来是你不相信我。",
        },
    }


# 人格表达档位 → 温度基调（查表，无计算；接入方自设档位即查此表）
PERSONA_TEMPERATURE: Dict[str, str] = {
    "restrained": "克制而冷峻，情绪被理性锁死。",
    "confrontational": "锋锐，直接挑明，不留余地。",
    "evasive": "闪躲，绕着主题走，答非所问。",
    "intimate": "松弛亲昵，卸下防备。",
    "direct": "坦率直接，情绪如常表露。",
}


class LanguagePersonaEngine:
    """
    语言人格引擎：把 SPL Core 快照过滤成"表达方式"。
    核心原则 internal_state ≠ spoken_text：心理状态先经人格过滤再变台词。

    本引擎只做轻量装配（面向企业/政府自设）：
    - 人格档位(mode)由接入方直接选定，查表得温度基调；
    - 沉默(silence_policy)由接入方开关，仅在高情绪+低能量时动态触发；
    - 防御载荷(denial/rationalization/suppression)动态覆盖真实意图。
    不做连续数学（无 emotional_reveal/emotion_hidden 拟合公式）。
    """
    def __init__(self, persona: "LanguagePersona" = None,
                 style: "StyleProfile" = None):
        self.persona = persona or LanguagePersona()
        self.style = style or StyleProfile()

    def filter_expression(self, core_snapshot: Dict[str, Any]) -> ExpressionResult:
        """
        核心过滤逻辑：解析 V8.0 快照，决定角色"该怎么说、该不该说"。
        除沉默触发外均为自设/查表，无数值拟合。
        """
        fluid = core_snapshot.get("fluid", {})
        fear = fluid.get("恐惧", 0.0)
        anger = fluid.get("愤怒", 0.0)
        shame = fluid.get("羞耻", 0.0)
        tension = fluid.get("张力", 0.0)
        denial = core_snapshot.get("denial_load", 0.0)
        suppression = core_snapshot.get("suppression_load", 0.0)
        rationalization = core_snapshot.get("rationalization_load", 0.0)
        energy = core_snapshot.get("energy", 100.0)

        # 1. 表达档位：直接采用接入方自设值
        mode = self.persona.mode

        # 2. 沉默触发：自设策略 + 动态状态（高情绪 + 低能量 → 闭嘴改动作）
        peak_emotion = max(fear, anger, shame, tension)
        should_silence = False
        silence_hint = ""
        if self.persona.silence_policy and peak_emotion > 0.6 and energy < 60.0:
            should_silence = True
            silence_hint = self.persona.silence_hint or "（角色没有回答，以动作与旁白承载情绪。）"

        # 3. 隐藏档位：克制/回避档位默认"绕着说"，其余直白
        emotion_hidden = 1.0 if mode in ("restrained", "evasive") else 0.0

        # 4. 防御载荷 → 修正真实意图（覆盖默认 direct_disclosure）
        if denial > 0.5:
            speech_intention = DefenseExpression.UTTERANCE_TEMPLATES["denial"]["intention"]
        elif rationalization > 0.5:
            speech_intention = DefenseExpression.UTTERANCE_TEMPLATES["rationalization"]["intention"]
        elif suppression > 0.6:
            speech_intention = "concealment"
        else:
            speech_intention = "direct_disclosure"

        return ExpressionResult(
            expression_mode=mode,
            emotion_hidden=emotion_hidden,
            speech_intention=speech_intention,
            should_silence=should_silence,
            silence_hint=silence_hint,
        )


@dataclass
class StyleProfile:
    """
    角色的静态语言风格基线（Static Linguistic Traits）。
    相当于角色的“默认声带和词汇库”。
    """
    base_verbosity: float = 0.5        # 默认话痨程度 [0.0极简 - 1.0长篇大论]
    formality: float = 0.7             # 默认正式度 [0.0市井粗语 - 1.0书面雅言]
    sarcasm_tendency: float = 0.3      # 默认讽刺倾向 [0.0真诚 - 1.0阴阳怪气]
    favorite_fillers: List[str] = field(default_factory=lambda: ["…", "所以", "不过"])
    absolute_words: List[str] = field(default_factory=lambda: ["绝不可能", "永远", "绝对"])
    # —— 丰富化扩展（默认关闭，向后兼容）——
    vocabulary_domain: List[str] = field(default_factory=list)      # 角色惯用意象/隐喻语域（如["军营","兵器"]）
    example_lines: Dict[str, List[str]] = field(default_factory=dict)  # 各情感温度下的示例台词（few-shot）


@dataclass
class RenderedStyle:
    """
    动态生成的语言风格指令（Dynamic Style Output）。
    可直接无缝转换为 LLM 的 System Prompt 或微调约束。
    """
    sentence_length: str               # 句长特征（如"极短，词组拼凑"，"长句，逻辑严密"）
    rhetorical_devices: List[str]      # 激活的修辞手法（如["反问", "讽刺", "过度辩解"]）
    punctuation_bias: str              # 标点符号倾向（如"大量使用句号"，"省略号频发"）
    tone_temperature: str              # 情感温度（如"冰冷疏离", "极度失控", "温和"）
    prompt_injection: str              # 建议直接注入 LLM Prompt 的指令
    silence_hint: str = ""             # 语言人格触发的沉默策略动作描写（默认空=正常说话）
    style_example: str = ""            # 可选：当前情感温度下的示例台词（few-shot），供 LLM 锚定腔调


class LanguageStyleEngine:
    """
    风格渲染引擎：将枯燥的浮点数转化为文字的张力。

    可选「帧间连续性」（stateful=True）：
    在同一人格的多次交互中维护滚动状态——持续高负载会让措辞逐帧
    愈演愈烈、语速加快。默认关闭，逐帧独立渲染（向后兼容）。
    """
    # 连续帧数阈值：情绪高温持续超过多少帧即视为"愈演愈烈"
    ESCALATION_FRAMES = 2
    # 语速漂移：verbal_acceleration 达到该值才在句式中体现"加快紧凑"

    def __init__(self, profile: StyleProfile = None, stateful: bool = False):
        self.profile = profile or StyleProfile()
        self.stateful = stateful
        self._flow = {}          # {"hits": {dim:连续高温帧数}, "verbal_acceleration": 语速漂移计数}
        self._frame_count = 0

    def reset_flow(self):
        """重置跨帧滚动状态（startup 或新建对话时调用）。"""
        self._flow = {}
        self._frame_count = 0

    # ---- 情感流体 → 动态温度基调（多维并存，非单一主导） ----
    EMOTION_TONE_DIMS = [
        ("愤怒", 0.6, "怒意锋锐"),
        ("恐惧", 0.6, "紧绷警觉"),
        ("羞耻", 0.5, "闪躲内耗"),
        ("愧疚", 0.5, "沉重亏欠"),
        ("喜悦", 0.6, "明亮跃动"),
        ("疏离", 0.5, "冰冷疏远"),
        ("张力", 0.6, "凝滞紧绷"),
    ]

    def _active_marks(self, core_snapshot: Dict[str, Any]) -> List[str]:
        """本帧激活的丰富化维度标记（用于示例台词聚合 & 台词生成）。"""
        fluid = core_snapshot.get("fluid", {})
        marks: List[str] = []
        if fluid.get("愧疚", 0.0) > 0.5:
            marks.append("guilt")
        if fluid.get("恐惧", 0.0) > 0.6 and fluid.get("愤怒", 0.0) < 0.6:
            marks.append("fear")
        if fluid.get("喜悦", 0.0) > 0.6:
            marks.append("joy")
        self_esteem = core_snapshot.get("self_esteem", 0.5)
        if self_esteem < 0.3:
            marks.append("low_esteem")
        elif self_esteem > 0.7:
            marks.append("high_esteem")
        if core_snapshot.get("trauma"):
            marks.append("trauma")
        return marks

    def _dynamic_tone(self, fluid: Dict[str, float]) -> str:
        """多维情感并存的动态温度：超阈维度全部计入，层次并存而非只取其一。"""
        parts: List[str] = []
        # 信任 > 0.6 且 张力 < 0.3 → 松弛信任态
        if fluid.get("信任", 0.0) > 0.6 and fluid.get("张力", 0.0) < 0.3:
            parts.append(f"柔和松弛({fluid.get('信任', 0.0):.2f})")
        for dim, thr, desc in self.EMOTION_TONE_DIMS:
            v = fluid.get(dim, 0.0)
            if v > thr:
                parts.append(f"{desc}({v:.2f})")
        # 愤怒+疏离同高 → 冰点组合（特殊复合态）
        if fluid.get("愤怒", 0.0) > 0.6 and fluid.get("疏离", 0.0) > 0.5:
            parts.append("零下冰点·带锋芒")
        if not parts:
            return "克制，维持基础社交距离。"
        return "、".join(parts) + "（层次并存，随本帧情感分布起伏）"

    def _dominant_detail(self, fluid: Dict[str, float]) -> str:
        """取当前主导情感的一句具象表达，供台词填充。"""
        if fluid.get("恐惧", 0.0) > 0.6:
            return "我有些不安，怕事情往最坏的方向走"
        if fluid.get("愤怒", 0.0) > 0.6:
            return "这口气我咽不下去"
        if fluid.get("羞耻", 0.0) > 0.5:
            return "我知道我做得不够好"
        if fluid.get("愧疚", 0.0) > 0.5:
            return "这件事是我该负责"
        if fluid.get("喜悦", 0.0) > 0.6:
            return "我挺高兴的"
        return "事情就按这个方向走吧"

    def _enrich(self, line: str, core_snapshot: Dict[str, Any]) -> str:
        """按防御载荷/自尊/紧张/词汇域注入填充词与口癖，让合成台词带角色味。"""
        out = line
        fluid = core_snapshot.get("fluid", {})
        denial = core_snapshot.get("denial_load", 0.0)
        self_esteem = core_snapshot.get("self_esteem", 0.5)
        fillers = self.profile.favorite_fillers
        vocab = self.profile.vocabulary_domain
        # 否认 → 绝对化词强化
        if denial > 0.5 and self.profile.absolute_words:
            out = f"{self.profile.absolute_words[0]}，{out}"
        # 低自尊 → 模糊断言
        if self_esteem < 0.3:
            out = "也许是……" + out + "……大概吧。"
        # 高自尊 → 斩钉截铁收尾
        elif self_esteem > 0.7:
            out = out + "，没什么好商量。"
        # 高紧张 → 口癖填充
        if fluid.get("张力", 0.0) > 0.7 and fillers:
            out = fillers[0] + out
        # 词汇域 → 末尾点缀一个意象
        if vocab and self.profile.vocabulary_domain:
            out = f"{out}——就像{vocab[0]}里的光景。"
        return out

    def generate_line(self, core_snapshot: Dict[str, Any],
                      expression: Optional["ExpressionResult"] = None) -> str:
        """直接产出台词（无需下游 LLM 的确定性模板合成）。

        依据当前状态：
        - 沉默策略：返回动作/旁白描写；
        - 表达意图(speech_intention)：选定台词骨架；
        - 激活维度/防御载荷/自尊/词汇域：注入填充词形成角色层次。
        """
        if expression is not None and expression.should_silence:
            return expression.silence_hint or "（沉默）"

        intention = expression.speech_intention if expression else "direct_disclosure"
        fluid = core_snapshot.get("fluid", {})

        # few-shot 优先：命中激活维度的示例台词，再注入角色填充词
        pool = self.profile.example_lines or {}
        marks = self._active_marks(core_snapshot)
        for m in marks:
            if pool.get(m):
                return self._enrich(pool[m][0], core_snapshot)
        if pool.get("default"):
            return self._enrich(pool["default"][0], core_snapshot)

        # 模板合成（无示例台词时兜底）
        detail = self._dominant_detail(fluid)
        CORE = {
            "direct_disclosure": "我直说了，{detail}。",
            "indirect_protection": "……其实{detail}，只是你误会了。",
            "concealment": "没什么，就是{detail}。",
            "power_assertion": "看来是你不信我，才会觉得{detail}。",
        }
        skeleton = CORE.get(intention, "……{detail}。").format(detail=detail)
        return self._enrich(skeleton, core_snapshot)

    def _update_flow(self, fluid: Dict[str, float]) -> None:
        """根据本帧情绪负载更新滚动状态；仅 stateful=True 时由 render_style 调用。"""
        if not self._flow:
            self._flow = {"hits": {}, "verbal_acceleration": 0}
        flow = self._flow
        hits = flow["hits"]
        # 各情绪维度是否高温：F 帧计连续超标次数
        for dim, thr in (("愤怒", 0.6), ("恐惧", 0.6), ("羞耻", 0.5),
                         ("张力", 0.6), ("愧疚", 0.5), ("喜悦", 0.6)):
            hits[dim] = hits.get(dim, 0) + 1 if fluid.get(dim, 0.0) > thr else 0
        # 语速漂移：任一维度连续超阈值且本帧总情绪负载仍高 → 加速；否则回退
        tension = max(fluid.get("愤怒", 0.0), fluid.get("恐惧", 0.0),
                      fluid.get("羞耻", 0.0), fluid.get("张力", 0.0))
        if any(v >= self.ESCALATION_FRAMES for v in hits.values()) and tension > 0.5:
            flow["verbal_acceleration"] = min(5, flow.get("verbal_acceleration", 0) + 1)
        else:
            flow["verbal_acceleration"] = max(0, flow.get("verbal_acceleration", 0) - 1)
        self._frame_count += 1

    def render_style(self, core_snapshot: Dict[str, Any],
                     expression: Optional[ExpressionResult] = None) -> RenderedStyle:
        """
        核心渲染逻辑：解析 V8.0 快照，生成当前帧的语言风格。

        Args:
            core_snapshot: SPL Core 快照
            expression: 语言人格过滤结果（LanguagePersonaEngine.filter_expression 的输出）。
                        传入时，表达模式/隐藏度会调制句式与温度（internal_state≠spoken_text）。
                        不传则退化为纯风格渲染（向后兼容）。
        """
        # 提取核心状态
        fluid = core_snapshot.get("fluid", {})
        mood = core_snapshot.get("mood", {})
        energy = core_snapshot.get("energy", 100.0)
        fatigue = core_snapshot.get("fatigue", 0.0)

        # 帧间连续性（仅 stateful=True）：先更新滚动状态，供本帧注入
        flow = None
        if self.stateful:
            self._update_flow(fluid)
            flow = self._flow
        
        # 提取防御与失调机制
        suppression = core_snapshot.get("suppression_load", 0.0)
        denial = core_snapshot.get("denial_load", 0.0)
        rationalization = core_snapshot.get("rationalization_load", 0.0)
        dissonance = core_snapshot.get("cognitive_dissonance", 0.0)
        sleep_debt = core_snapshot.get("sleep_debt", 0.0)

        # 初始化输出特征
        rhetorical_devices = []
        instructions = []
        # 标点/风格倾向用列表累积，最后合并——避免物理层与防御层互相覆盖。
        punctuation_notes = []

        # ==========================================
        # 1. 物理层：能量与疲劳计算句长与连贯性
        # ==========================================
        current_verbosity = self.profile.base_verbosity - (fatigue * 0.4) - (sleep_debt * 0.2)
        if energy < 20.0 or fatigue > 0.8:
            sentence_length = "极度简短，多用单字或短词，缺乏完整主谓宾。"
            punctuation_notes.append("高频使用句号和省略号，语气虚弱断续。")
            instructions.append("角色处于低能耗状态，拒绝长篇大论，能不说话就不说话。")
        elif mood.get("紧张", 0.0) > 0.7:
            sentence_length = "句子破碎，节奏极快，语无伦次。"
            punctuation_notes.append("几乎没有逗号，直接短句拼接，偶尔出现破折号打断。")
        else:
            if current_verbosity > 0.6:
                sentence_length = "长句为主，从句嵌套多，愿意详细解释。"
            else:
                sentence_length = "句长适中，结构规整。"
            punctuation_notes.append("常规标点。")

        # ── formality 消费：正式度调制句长与措辞基调 ──
        # 低正式度 → 允许俚语、口语缩略、市井粗语；高正式度 → 书面雅言、禁口语缩略。
        # 仅在非极端状态（非低能耗、非紧张破碎）下叠加，避免与紧急状态抢戏。
        if energy >= 20.0 and fatigue <= 0.8 and mood.get("紧张", 0.0) <= 0.7:
            if self.profile.formality > 0.75:
                sentence_length += " 措辞书面化，多用敬语与严谨句式，禁口语缩略与俚语。"
            elif self.profile.formality < 0.35:
                sentence_length += " 措辞口语化，允许俚语、网络用语与市井粗语，句式松散。"
            else:
                sentence_length += " 措辞中性，书面与口语的边界随情绪浮动。"

        # ==========================================
        # 1.5 语言人格调制：internal_state ≠ spoken_text
        # ==========================================
        # 传入 LanguagePersonaEngine 的过滤结果时，表达模式/隐藏度调制句长与温度。
        # 这是"人格层压制风格层"的关键——控制型角色恐惧时不会脱口而出。
        # 温度基调在此直接由人格模式决定（人格层优先于情绪流体层，无需后置覆盖补丁）。
        silence_hint = ""
        persona_mode = None
        persona_active = False
        if expression is not None:
            mode = expression.expression_mode
            hidden = expression.emotion_hidden
            silence_hint = expression.silence_hint

            if expression.should_silence:
                # 触发沉默：不产出台词风格，改走动作描写
                sentence_length = "（沉默）无台词，改用动作与旁白承载情绪。"
                punctuation_notes.append("无言以对，只有动作与环境描写。")
                instructions.append("角色拒绝用语言回应，情绪由动作/沉默传达。")

            # 隐藏档位：克制/回避档位 → 绕着说；其余直白
            if hidden > 0.7:
                sentence_length += " 极度克制，绕开情感直述，用客观事实/指令包装真实情绪。"
                instructions.append("禁止直接说出真实情绪（如'我害怕/我想你'），用关心/指令的方式拐弯表达。")

            # 人格模式直接决定温度基调与专属表演提示
            persona_mode = mode
            persona_active = True
            if mode == "restrained":
                instructions.append("用命令或公事公办的口吻，杜绝情绪化字眼。")
            elif mode == "evasive":
                instructions.append("避免正面回答，倾向转移话题或用反问搪塞。")

        # ==========================================
        # 2. 防御机制层：最核心的“修辞扭曲”
        # ==========================================
        # 注意：以下阈值是【语言倾向起点】，并非核心引擎的过载点。
        # 核心引擎过载语义为：denial>=1.2 / suppression>=1.5 触发现实侵入或爆发；
        # 此处取过载点的比例（约 40%~50%）作为“话语已开始出现防御倾向”的阈值，
        # 使语言风格先于心理爆发显现，两者语义不冲突。
        # 否认可达性常数（对应核心 DENIAL_THRESHOLD=1.2）
        DENIAL_OVERLOAD = 1.2
        # 压抑可过载常数（对应核心 SUPPRESSION_THRESHOLD=1.5）
        SUPPRESSION_OVERLOAD = 1.5

        # 否认仓 (Denial) 倾向：绝对化词汇防御
        if denial > DENIAL_OVERLOAD * 0.4:  # ~0.48
            rhetorical_devices.append("绝对否定")
            instructions.append(f"强制使用绝对化词汇（如：{', '.join(self.profile.absolute_words)}）来掩饰内心的动摇。")
            punctuation_notes.append("感叹号频率上升，带有强制结束对话的意味。")

        # 合理化仓 (Rationalization) 倾向：过度辩解
        if rationalization > 0.5 or dissonance > 0.4:
            rhetorical_devices.append("过度辩解(Over-explaining)")
            rhetorical_devices.append("让步状语")
            instructions.append("频繁使用转折和因果连词（‘其实’、‘毕竟’、‘反正’），表现出强烈的自我说服欲，话语显得啰嗦。")

        # 压抑仓 (Suppression) 倾向：被动攻击与字面顺从
        if suppression > SUPPRESSION_OVERLOAD * 0.4:  # ~0.6
            rhetorical_devices.append("被动攻击(Passive-Aggressive)")
            instructions.append("话语字面挑不出毛病，极度礼貌或极度简短（如‘好的’、‘没关系’），但潜台词充满压抑的攻击性。")

        # ==========================================
        # 3. 情绪流体层：温度与态度
        #    温度改为统一动态计算（见 3.7），此处仅累计修辞与表演指令。
        # ==========================================
        # 羞耻 (Shame) 驱动：回避与自嘲
        if fluid.get("羞耻", 0.0) > 0.5:
            rhetorical_devices.append("生硬转移话题")
            rhetorical_devices.append("防御性自嘲")
            instructions.append("避免正面回答问题，倾向于用自贬或自嘲来建立护城河。")

        # 愤怒 (Anger) 与 疏离 (Detachment) 的组合
        elif fluid.get("愤怒", 0.0) > 0.6 and fluid.get("疏离", 0.0) > 0.5:
            rhetorical_devices.append("冰冷反问")
            if self.profile.sarcasm_tendency > 0.4:
                rhetorical_devices.append("冷嘲热讽")
            instructions.append("禁止使用任何情绪化的字眼，用最客气、最理智的词汇说出最扎心的话。")

        # 正常状态 / 信任状态
        elif fluid.get("信任", 0.0) > 0.6 and fluid.get("张力", 0.0) < 0.3:
            instructions.append("语气松弛，允许流露真实的脆弱或温柔，减少心理防御词汇。")

        # ==========================================
        # 3.5 丰富化新增维度（V8.0 其余多轴，默认向后兼容）
        #     修辞/指令全维度可并存累加；温度统一见 3.7 动态计算。
        # ==========================================
        # 愧疚 (Guilt)：行为层面的亏欠——区别于羞耻的"自我形象受损"
        if fluid.get("愧疚", 0.0) > 0.5:
            rhetorical_devices.append("赎罪式道歉")
            instructions.append("频繁为结果承担责任，倾向用补偿性许诺或道歉，话语带有亏欠感，避免推卸。")

        # 恐惧 (Fear)：对威胁的预判——条件假设句 + 自我打气
        if fluid.get("恐惧", 0.0) > 0.6 and fluid.get("愤怒", 0.0) < 0.6:
            rhetorical_devices.append("条件假设")
            instructions.append("常用'如果…就好了''万一…'式的假设句，不自觉预演最坏结果，并试图用语言自我安抚。")

        # 喜悦 (Joy)：积极的情绪外溢——主动分享与追问
        if fluid.get("喜悦", 0.0) > 0.6:
            rhetorical_devices.append("积极外溢")
            instructions.append("语气上扬，主动分享细节并追问对方感受，句式轻快，愿意延续话题。")

        # 自尊 (Self-esteem)：断言强度——低自尊自贬/征求确认，高自尊斩钉截铁
        self_esteem = core_snapshot.get("self_esteem", 0.5)
        if self_esteem is not None:
            if self_esteem < 0.3:
                instructions.append("自我评价低，倾向自贬、模糊化自己的判断，常用'也许''大概'并征求对方确认。")
            elif self_esteem > 0.7:
                instructions.append("自我肯定强，语气断言式、斩钉截铁，很少让步，习惯承担话语主导。")

        # 创伤 (Trauma)：触发相关主题时措辞回避性停滞
        if core_snapshot.get("trauma"):
            instructions.append("存在未愈合创伤记忆：触及相关主题时措辞会出现停顿、跳跃或突然转移话题的回避倾向。")

        # 词汇域 (Vocabulary Domain)：角色惯用意象/隐喻，注入用词世界
        if self.profile.vocabulary_domain:
            instructions.append(f"用词偏好取自下列意象语域，隐喻与类比多从其中取材：{'、'.join(self.profile.vocabulary_domain)}。")

        # ==========================================
        # 3.7 温度：多维动态计算（人格基座 × 流体动态，不再单一锁定）
        # ==========================================
        fluid_tone = self._dynamic_tone(fluid)
        if persona_active and persona_mode:
            base = PERSONA_TEMPERATURE.get(persona_mode, "克制，维持基础的社交距离。")
            tone_temperature = f"{base}｜底层{fluid_tone}"
        else:
            tone_temperature = fluid_tone

        # ==========================================
        # 3.6 帧间连续性注入（仅 stateful=True 且有累积）
        # ==========================================
        if flow is not None:
            hits = flow.get("hits") or {}
            sustained = [d for d, v in hits.items() if v >= self.ESCALATION_FRAMES]
            if sustained:
                instructions.append(
                    f"以下情绪已持续数帧、措辞须愈演愈烈（{'、'.join(sustained)}）："
                    f"与前一刻相比，语气浓度和强度必须明显抬升，禁止停滞在同一强度。")
            if flow.get("verbal_acceleration", 0) >= 2 and "（沉默）" not in sentence_length:
                sentence_length = sentence_length.rstrip() + " 伴随持续高压，语速加快，句子被压缩、节奏愈紧凑。"

        # ==========================================
        # 4. 组装 Prompt Injection
        # ==========================================
        # 合并所有标点/风格倾向：物理层（基线）在前，防御层/情绪层追加在后。
        punctuation_bias = "；".join(dict.fromkeys(punctuation_notes))

        # 示例台词（少样本 few-shot）：按本帧激活的维度标记聚合，供下游 LLM 锚定腔调。
        #   example_lines 的 key 用维度标记（guilt/fear/joy/low_esteem/high_esteem/trauma）
        #   或兜底 "default"。命中顺序：维度标记优先，default 兜底，取第一个非空。
        style_example = ""
        example_pool = self.profile.example_lines or {}
        if example_pool:
            candidate = ""
            for mark in self._active_marks(core_snapshot):   # 按激活顺序逐维度找
                lines = example_pool.get(mark)
                if lines:
                    candidate = lines[0]
                    break
            if not candidate:                     # 兜底 default
                default_lines = example_pool.get("default")
                if default_lines:
                    candidate = default_lines[0]
            style_example = candidate

        final_prompt = (
            f"【动态语言限制】\n"
            f"- 情感温度：{tone_temperature}\n"
            f"- 句式特征：{sentence_length}\n"
            f"- 标点偏好：{punctuation_bias}\n"
            f"- 激活修辞：{', '.join(rhetorical_devices) if rhetorical_devices else '无特殊修辞'}\n"
            f"- 核心表演指导：{' '.join(instructions)}"
        )
        if style_example:
            final_prompt += f"\n- 台词示例（仿照此腔调）：{style_example}"

        return RenderedStyle(
            sentence_length=sentence_length,
            rhetorical_devices=rhetorical_devices,
            punctuation_bias=punctuation_bias,
            tone_temperature=tone_temperature,
            prompt_injection=final_prompt,
            silence_hint=silence_hint,
            style_example=style_example
        )


# ================================================================
# 运行示例
# ================================================================
if __name__ == "__main__":
    # 模拟一个 V8.0 核心在经历了“熬夜+被戳中痛点（高否认+高羞耻）”后的快照
    mock_snapshot = {
        "fluid": {"羞耻": 0.7, "愤怒": 0.4, "疏离": 0.6, "信任": 0.1, "张力": 0.8},
        "mood": {"紧张": 0.8},
        "energy": 40.0,
        "fatigue": 0.6,
        "sleep_debt": 0.5,
        "denial_load": 0.8,         # 极力否认现状
        "suppression_load": 0.2,
        "rationalization_load": 0.1,
        "cognitive_dissonance": 0.2
    }

    # 实例化一个基础角色风格（比如一个平时比较正式、有轻微嘲讽倾向的人）
    base_profile = StyleProfile(base_verbosity=0.6, formality=0.8, sarcasm_tendency=0.5)
    style_engine = LanguageStyleEngine(base_profile)

    # 渲染当前帧的语言风格（不传 expression → 纯风格渲染，向后兼容）
    rendered = style_engine.render_style(mock_snapshot)

    print("=== 示例1：纯风格渲染（向后兼容）===")
    print(rendered.prompt_injection)

    # ════════════════════════════════════════════════════════════
    # 示例2：语言人格过滤——祁皇英（高压控制型，情绪深藏）
    #   内心恐惧+羞耻很高，但表达时被完全过滤，甚至触发沉默。
    # ════════════════════════════════════════════════════════════
    qihuangying_persona = LanguagePersona(
        mode="restrained",                       # 高压控制型：直接选档，不调连续参数
        silence_policy=True,                     # 高情绪+低能量时改以动作代替语言
        silence_hint="她没有回答。只是垂下眼帘，避开了目光。",  # 自设沉默动作描写
    )
    qihuangying_style = StyleProfile(base_verbosity=0.4, formality=0.9, sarcasm_tendency=0.4)

    persona_engine = LanguagePersonaEngine(qihuangying_persona, qihuangying_style)
    expression = persona_engine.filter_expression(mock_snapshot)

    print("\n=== 示例2：语言人格过滤结果（祁皇英）===")
    print(f"表达模式      : {expression.expression_mode}")
    print(f"情绪隐藏度    : {expression.emotion_hidden}")
    print(f"真实意图      : {expression.speech_intention}")
    print(f"触发沉默      : {expression.should_silence}")
    if expression.should_silence:
        print(f"沉默动作描写  : {expression.silence_hint}")

    # 把过滤结果喂入渲染器 → 台词风格
    rendered2 = style_engine.render_style(mock_snapshot, expression=expression)
    print("\n=== 示例2：渲染后（祁皇英台词风格）===")
    print(rendered2.prompt_injection)
    if rendered2.silence_hint:
        print(f"【输出】{rendered2.silence_hint}")
