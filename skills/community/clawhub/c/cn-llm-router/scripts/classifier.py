"""任务分类器（规则 + 启发式，零依赖、零密钥）。

输入一段 prompt，输出路由建议所需的结构化特征：
- task_type   : classify / extract / summarize / translate / reason / code / long / general
- needs_reasoning : 是否需要推理（是 → 偏好带 reasoner 的模型）
- length_bucket: short(<4k) / mid(4k-32k) / long(>32k) 以字符粗略估算
- budget_sensitive: 是否对价格敏感（批量 / 分类 / 抽取场景）
- multimodal  : 是否需要多模态能力（image / audio）

设计：初期用规则 + 关键词 + 长度启发式，不调用任何模型，毫秒级、可离线。
设 confidence 阈值，低于阈值时由路由引擎回退到 quality / manual。
"""

import re

# 关键词 → 任务类型
KEYWORD_MAP = [
    ("reason", r"推理|分析|为什么|原因|推导|证明|论证|逻辑|本质|根因|复杂|深度|思考|拆解"),
    ("code", r"代码|函数|脚本|bug|编程|python|java|js|正则|算法|接口|sql|报错|debug|编译"),
    ("translate", r"翻译|translate|英译中|中译英|本地化"),
    ("summarize", r"总结|摘要|概括|提炼|归纳|要点|小结"),
    ("extract", r"抽取|提取|识别|解析|抽取实体|抽取字段|抽取信息|结构化|抽取出"),
    ("classify", r"分类|判断|是不是|是否属于|打标|标签|归为|鉴别|检测"),
    ("long", r"长篇|长文档|整本书|全文|论文|报告|合同全文|长文"),
]

# v2.4 多模态关键词
IMAGE_KEYWORDS = re.compile(
    r"图片|图像|看看|看一下|看图|画面|照片中|这张图|那张图|视觉|"
    r"图像识别|图片识别|ocr|看图识|描述图|解读图|图中有|图上是|"
    r"画面上|这张图|那张图"
)
AUDIO_KEYWORDS = re.compile(
    r"音频|语音|声音|听听|听一下|音频识别|语音识别|转文字|"
    r"语音转文字|asr|识别语音|识别音频|语音分析|这段音频|这段录音"
)

REASON_HINT = re.compile(r"推理|分析|为什么|原因|推导|证明|论证|逻辑|本质|根因|复杂|深度|思考|拆解|逐步")
LONG_CHAR_THRESHOLD = 32000   # ≈ 32k token（粗略：1 中文字≈1 token）
MID_CHAR_THRESHOLD = 4000     # ≈ 4k token


def classify(prompt, task_hint=None):
    """返回分类结果 dict。

    prompt: 用户输入文本
    task_hint: 用户/上游显式给出的任务类型（优先），如 'code' / 'reason'
    """
    if prompt is None:
        prompt = ""
    text = prompt.strip()
    char_len = len(text)

    # 1) 显式 hint 优先
    if task_hint and task_hint in {k for k, _ in KEYWORD_MAP} | {"general"}:
        task_type = task_hint
    else:
        # 2) 关键词匹配（按顺序，第一个命中为准）
        task_type = "general"
        for t, pat in KEYWORD_MAP:
            if re.search(pat, text):
                task_type = t
                break

    needs_reasoning = bool(REASON_HINT.search(text)) or task_type == "reason"

    if char_len > LONG_CHAR_THRESHOLD:
        length_bucket = "long"
    elif char_len > MID_CHAR_THRESHOLD:
        length_bucket = "mid"
    else:
        length_bucket = "short"

    # 批量 / 简单任务对价格更敏感
    budget_sensitive = task_type in ("classify", "extract", "summarize", "translate")

    # 是否适合流式输出：
    #   对话/翻译/代码/摘要/写作 → 逐字生成体验好，建议流式；
    #   数学推理/复杂推导 → 需完整思维链，建议一次性返回（避免半截推理误导）；
    #   结构化抽取/分类 → 结果通常需整体解析（如 JSON），一次性更稳妥。
    # 纯规则判断，零额外开销。
    if needs_reasoning or task_type in ("reason", "extract", "classify"):
        stream_friendly = False
    else:
        # general / translate / code / summarize / long 等适合流式
        stream_friendly = True

    # 置信度：关键词命中且长度适中 → 高；纯 general 且无推理词 → 低
    if task_type != "general" or needs_reasoning:
        confidence = 0.8
    else:
        confidence = 0.4

    # v2.4 多模态检测：image（视觉）/ audio（音频）
    multimodal = None
    if IMAGE_KEYWORDS.search(text):
        multimodal = "image"
    elif AUDIO_KEYWORDS.search(text):
        multimodal = "audio"

    return {
        "task_type": task_type,
        "needs_reasoning": needs_reasoning,
        "length_bucket": length_bucket,
        "budget_sensitive": budget_sensitive,
        "stream_friendly": stream_friendly,
        "confidence": confidence,
        "char_len": char_len,
        "multimodal": multimodal,
    }
