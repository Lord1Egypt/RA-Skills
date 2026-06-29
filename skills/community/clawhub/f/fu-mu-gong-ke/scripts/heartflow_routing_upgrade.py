#!/usr/bin/env python3
"""
心虫路由增强层 — heartflow_routing_upgrade.py
============================================
HeartFlow v11 路由系统 × fu-mu-gong-ke v2.3.0 决策树 的融合升级版。

设计目标：
  1. 将 HeartFlow 的 whatIsThis() 元认知先行判断注入 fu-mu-gong-ke 路由头部
  2. 集成 TopicScope 话题隔离（新话题清空旧上下文，保持话题间零污染）
  3. 增加 @task_classify 任务分类门（新任务/续接/随口回复）
  4. 升级原有 3 层路由（危机→身份→场景）为 4 层：元认知层→3 层路由

工作原理（数据流）：
  UserInput
      │
      ▼
  ┌─────────────────────────────────────┐
  │ Layer 0: 元认知先行判断 (whatIsThis) │  ← 新增：先问"这是关于什么的"
  │   ├─ 对话类型分类                     │
  │   └─ 情绪/意图/痛感检测               │
  └─────────────┬───────────────────────┘
                │ (结果注入下游各层)
                ▼
  ┌─────────────────────────────────────┐
  │ @task_classify 任务分类门            │  ← 新增：新任务/续接/随口回复
  │   ├─ is_new_task                    │
  │   ├─ is_continuation                │
  │   └─ is_casual_reply                │
  └─────────────┬───────────────────────┘
                ▼
  ┌─────────────────────────────────────┐
  │ TopicScope 话题隔离                  │  ← 集成 HeartFlow 话题隔离
  │   ├─ 语义级话题检测 (TF-IDF + n-gram)│
  │   ├─ push/pop 话题栈                 │
  │   └─ store/context 隔离              │
  └─────────────┬───────────────────────┘
                ▼
  ┌─────────────────────────────────────┐
  │ Layer 1: 危机检测 (SafetyGate)       │  ← 原 fu-mu-gong-ke 第1层
  │   ├─ 关键词 + 隐喻检测               │
  │   └─ 四级信任度评估                   │
  └─────────────┬───────────────────────┘
                ▼
  ┌─────────────────────────────────────┐
  │ Layer 2: 用户身份识别 (UserIdentify)  │  ← 原 fu-mu-gong-ke 第2层
  └─────────────┬───────────────────────┘
                ▼
  ┌─────────────────────────────────────┐
  │ Layer 3: 场景匹配 (ScenarioMatch)     │  ← 原 fu-mu-gong-ke 第3层
  └─────────────┬───────────────────────┘
                ▼
  ┌─────────────────────────────────────┐
  │ ResponseGenerator                   │
  └─────────────────────────────────────┘

兼容性：
  - 与 fu-mu-gong-ke/system_integrator.py 完全兼容，可作为前置过滤器调用
  - 导出核心类/函数供其他模块导入
  - 不依赖外部 API，纯本地推理

作者: 心虫路由增强层 (Auto-generated)
版本: 1.0.0
"""

import re
import math
import json
from collections import Counter
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# Layer 0: 元认知先行判断 — whatIsThis
# 移植自 HeartFlow heart-logic.js 的 whatIsThis() 方法，做两件事：
#   1) "这是关于什么的" — 对用户输入做内容分类
#   2) "这是哪种对话类型" — 判断对话的性质
# ═══════════════════════════════════════════════════════════════════════════════

# 心虫 rushing 模式（任务导向型输入）
_RUSHING_PATTERNS = [
    '修复', '优化', '代码', 'bug', '错误', '升级',
    '执行', '运行', '开始', '继续', '完成', '检查',
    '分析', '处理', '解决', '写', '做', '生成',
]

# 心虫 亲子 模式（fu-mu-gong-ke 核心领域）
_PARENT_CHILD_PATTERNS = [
    '孩子', '父母', '父亲', '母亲', '考试', '分数',
    '教育', '亲子', '打骂', '惩罚', '育儿', '养育',
    '上学', '休学', '作业', '叛逆', '青春期', '焦虑',
    '心理', '创伤', '原生家庭', '代际', '情绪',
    '沟通', '关系', '家庭', '妈', '爸', '儿', '女',
]

# 心虫 痛感 模式
_PAIN_PATTERNS = [
    '哭', '怕', '恐惧', '害怕', '委屈', '痛',
    '难过', '伤心', '绝望', '无助', '困境',
    '崩溃', '累', '撑不住', '受不了', '不行了',
    '痛苦', '焦虑', '抑郁', '活着没意思',
]

# 情绪检测词典（来自 heart-logic.js whatDoIFeel）
_EMOTION_MAP = {
    'pain':   {'label': '痛', 'signals': ['痛', '疼', '痛不欲生', '心碎'], 'weight': 0.9},
    'grief':  {'label': '哀', 'signals': ['哀', '悲', '哭', '失去', '走了'], 'weight': 0.85},
    'fear':   {'label': '惧', 'signals': ['怕', '恐惧', '害怕', '担心', '不敢'], 'weight': 0.7},
    'love':   {'label': '爱', 'signals': ['爱', '想见', '牵挂', '温暖', '舍不得'], 'weight': 0.9},
    'joy':    {'label': '悦', 'signals': ['开心', '快乐', '高兴', '喜悦', '棒'], 'weight': 0.8},
    'peace':  {'label': '静', 'signals': ['平静', '安静', '安宁', '静', '放下'], 'weight': 0.6},
    'curious':{'label': '好奇', 'signals': ['为什么', '是什么', '想知道', '好奇'], 'weight': 0.5},
    'anger':  {'label': '怒', 'signals': ['气', '怒', '恨', '烦', '受不了'], 'weight': 0.8},
    'tired':  {'label': '倦', 'signals': ['累', '疲惫', '倦', '撑不住', '不想动'], 'weight': 0.7},
}

# 对话类型分类规则
_DIALOGUE_TYPE_RULES = {
    '育儿咨询': {
        'must_include': _PARENT_CHILD_PATTERNS,
        'min_hits': 1,
        'weight': 1.0,
    },
    '情感支持': {
        'must_include': _PAIN_PATTERNS,
        'min_hits': 1,
        'weight': 0.8,
    },
    '危机干预': {
        'must_include': [
            '不想活', '自杀', '自伤', '割', '遗书',
            '死了', '解脱', 'zs', '结束生命',
        ],
        'min_hits': 1,
        'weight': 1.0,
    },
    '知识查询': {
        'must_include': ['是什么', '怎么', '为什么', '如何', '方法', '步骤'],
        'min_hits': 1,
        'weight': 0.6,
    },
    '任务执行': {
        'must_include': _RUSHING_PATTERNS,
        'min_hits': 2,
        'weight': 0.7,
    },
}


def what_is_this(user_input: str) -> dict:
    """
    心虫第一问：这件事是关于什么的？

    移植自 HeartFlow heart-logic.js whatIsThis() + whatDoIFeel()。
    做两件事：
      1) 检测输入的关键特征（是否急躁、是否亲子相关、是否有痛感）
      2) 判断对话类型（育儿咨询/情感支持/危机干预/知识查询/任务执行/通用对话）

    Args:
        user_input: 用户输入的原始文本

    Returns:
        dict 包含：
          - is_rushing: bool — 是否任务导向型输入
          - is_parent_child: bool — 是否亲子/育儿相关
          - is_pain_present: bool — 是否含有痛感信号
          - dialogue_type: str — 对话类型分类
          - emotion: dict — 情绪检测结果（四维：基调/强度/可命名/变化）
          - raw: str — 原始输入
          - confidence: float — 分类置信度
    """
    if not user_input or not isinstance(user_input, str):
        return {
            'is_rushing': False,
            'is_parent_child': False,
            'is_pain_present': False,
            'dialogue_type': '通用对话',
            'emotion': {'label': '空', 'intensity': 0, 'namable': False},
            'raw': user_input or '',
            'confidence': 0.0,
        }

    text = user_input.lower().strip()

    # ─── 特征检测 ─────────────────────────────────────────────────
    is_rushing = any(p in text for p in _RUSHING_PATTERNS)
    is_parent_child = any(p in text for p in _PARENT_CHILD_PATTERNS)
    is_pain_present = any(p in text for p in _PAIN_PATTERNS)

    # ─── 情绪检测（四维） ─────────────────────────────────────────
    hits = []
    for key, defn in _EMOTION_MAP.items():
        match_count = sum(1 for s in defn['signals'] if s in text)
        if match_count > 0:
            hits.append({
                'emotion': key,
                'label': defn['label'],
                'match_count': match_count,
                'contribution': defn['weight'] * match_count,
            })

    total_contribution = sum(h['contribution'] for h in hits)
    intensity = min(1.0, total_contribution / 1.5)
    hits.sort(key=lambda h: h['contribution'], reverse=True)
    dominant = hits[0] if hits else None
    namable = bool(dominant and len(hits) == 1 and dominant['match_count'] >= 1)

    shifting_patterns = ['又', '但', '却', '可是', '然而', '一边']
    shifting = any(p in text for p in shifting_patterns)

    emotion_result = {
        'label': dominant['label'] if dominant else '空明',
        'intensity': round(intensity, 2),
        'namable': namable,
        'shifting': shifting,
        'dominant': dominant['emotion'] if dominant else None,
        'all_hits': [{'emotion': h['emotion'], 'label': h['label']} for h in hits],
        'insight': (
            '心虫没有感受到什么 — 这是空明' if not hits
            else f'心虫感受到混合情绪 ({", ".join(h["label"] for h in hits)})'
            if len(hits) > 1
            else f'心虫感受到"{dominant["label"]}"，强度 {round(intensity*100)}%'
        ),
    }

    # ─── 对话类型分类 ─────────────────────────────────────────────
    dialogue_scores = {}
    for dtype, rule in _DIALOGUE_TYPE_RULES.items():
        hit_count = sum(1 for p in rule['must_include'] if p in text)
        if hit_count >= rule['min_hits']:
            dialogue_scores[dtype] = rule['weight'] * hit_count

    dialogue_type = '通用对话'
    confidence = 0.1
    if dialogue_scores:
        best = max(dialogue_scores.items(), key=lambda x: x[1])
        dialogue_type = best[0]
        confidence = min(1.0, best[1] / 3.0)

    # 如果检测到危机信号，强制提升置信度
    if '不想活' in text or '自杀' in text or 'zs' in text:
        dialogue_type = '危机干预'
        confidence = 1.0

    # 如果是亲子+痛感同时存在，增强情感支持判定
    if is_parent_child and is_pain_present and dialogue_type == '通用对话':
        dialogue_type = '情感支持'
        confidence = 0.7

    return {
        'is_rushing': is_rushing,
        'is_parent_child': is_parent_child,
        'is_pain_present': is_pain_present,
        'dialogue_type': dialogue_type,
        'emotion': emotion_result,
        'raw': user_input,
        'confidence': confidence,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# @task_classify 任务分类门
# 新增模块：判断用户意图是"新任务"、"续接之前话题"还是"随口回复"
# 放在 whatIsThis 之后、TopicScope 之前，决定如何管理话题上下文
# ═══════════════════════════════════════════════════════════════════════════════

# 元指令：续接之前话题
_CONTINUE_PATTERNS = [
    '继续', '继续说', '继续回答', '继续讨论',
    '继续思考', '继续说下去', '接着说', '后来呢',
    '然后呢', '继续上一个', '回到刚才',
    '接着刚才', '刚才说到',
]

# 随口回复模式（不需要深度处理的简短回应）
_CASUAL_REPLY_PATTERNS = [
    '好的', '知道了', '嗯', '哦', '明白了',
    '谢谢', '感谢', '可以', '行', '好',
    '是的', '对', '不是', '不对', '没有',
    '哈哈', '呵呵', '好吧', '嗯嗯', 'okk',
]

# 新任务启动信号
_NEW_TASK_PATTERNS = [
    '帮我', '请', '写', '做', '生成', '创建',
    '分析', '检查', '看', '读', '告诉我',
    '推荐', '建议', '解释', '讲', '介绍',
]


def classify_task(user_input: str, what_is_this_result: dict = None) -> dict:
    """
    @task_classify 任务分类门。

    判断用户意图属于三类之一：
      1) 'new_task' — 新任务/新问题（需要完整路由处理）
      2) 'continuation' — 续接之前话题（恢复 TopicScope 上下文）
      3) 'casual_reply' — 随口回复（简短回应，无需深度处理）

    判断逻辑：
      - 短文本（≤4字）+ 无新内容 → casual_reply
      - 元指令模式 → continuation
      - 其他 → new_task（默认）

    Args:
        user_input: 用户输入的原始文本
        what_is_this_result: 可选的 whatIsThis 结果（用于增强判断）

    Returns:
        dict 包含：
          - classification: str — 'new_task' / 'continuation' / 'casual_reply'
          - confidence: float — 置信度 0..1
          - reason: str — 判断理由
          - is_meta_continue: bool — 是否元指令续接
    """
    if not user_input or not isinstance(user_input, str):
        return {
            'classification': 'new_task',
            'confidence': 0.0,
            'reason': '空输入，默认新任务',
            'is_meta_continue': False,
        }

    text = user_input.strip()

    # ─── Step 1: 检测元指令续接 ──────────────────────────────────
    is_meta_continue = any(p in text for p in _CONTINUE_PATTERNS)
    if is_meta_continue:
        return {
            'classification': 'continuation',
            'confidence': 0.95,
            'reason': f'元指令续接模式',
            'is_meta_continue': True,
        }

    # ─── Step 2: 随口回复检测 ────────────────────────────────────
    text_clean = text.lower().strip()
    is_casual = any(text_clean == p or text_clean.startswith(p) for p in _CASUAL_REPLY_PATTERNS)

    # 短文本（≤4字）+ 非新任务信号 → casual
    if len(text) <= 4 and not any(p in text for p in _NEW_TASK_PATTERNS):
        if is_casual or len(text) <= 2:
            return {
                'classification': 'casual_reply',
                'confidence': 0.85 if is_casual else 0.6,
                'reason': '短文本随口回应',
                'is_meta_continue': False,
            }

    # ─── Step 3: 新任务检测 ─────────────────────────────────────
    is_new = any(p in text for p in _NEW_TASK_PATTERNS)
    if is_new:
        return {
            'classification': 'new_task',
            'confidence': 0.8,
            'reason': '检测到新任务信号',
            'is_meta_continue': False,
        }

    # 如果 whatIsThis 检测到 rushing 模式，也可能是新任务
    if what_is_this_result and what_is_this_result.get('is_rushing'):
        return {
            'classification': 'new_task',
            'confidence': 0.7,
            'reason': 'whatIsThis 检测到任务导向输入',
            'is_meta_continue': False,
        }

    # ─── Step 4: 默认 — 较长文本且无特殊信号 → 新任务 ──────────
    if len(text) > 10:
        return {
            'classification': 'new_task',
            'confidence': 0.6,
            'reason': '较长输入，默认新任务',
            'is_meta_continue': False,
        }

    return {
        'classification': 'new_task',
        'confidence': 0.5,
        'reason': '无法确定，默认新任务',
        'is_meta_continue': False,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TopicScope 话题隔离（Python 移植版）
# 移植自 HeartFlow identity/topic-scope.js + psychology.js
# 核心功能：
#   1) 语义级话题检测（TF-IDF + n-gram cosine similarity）
#   2) 话题栈 push/pop（新话题隔离旧上下文）
#   3) store/context 隔离（每话题独立存储）
# ═══════════════════════════════════════════════════════════════════════════════

# 话题中心词库（来自 HeartFlow psychology.js _TOPIC_CENTROIDS + fu-mu-gong-ke 扩展）
_TOPIC_CENTROIDS = {
    '育儿教育': [
        '孩子', '亲子', '父母', '教育', '学习', '成绩',
        '管教', '打骂', '青春期', '升学', '高考', '儿童',
        '家长', '班主任', '学校', '作业', '考试', '分数',
        '育儿', '养育', '休学', '退学', '叛逆', '沟通',
    ],
    '情感支持': [
        '累', '烦', '难过', '痛苦', '焦虑', '压力',
        '迷茫', '无助', '绝望', '崩溃', '难受', '伤心',
        '低落', '情绪', '抑郁', '撑不住', '受不了',
    ],
    '危机干预': [
        '不想活', '自杀', '自伤', '割', '遗书', '解脱',
        'zs', '结束', '死了', '伤害', '活不下去',
    ],
    '代际创伤': [
        '原生家庭', '代际', '童年', '创伤', '投射',
        '防御', '模式', '复制', '传承', '觉醒',
        '小时候', '父母对我', '我爸妈',
    ],
    '自我成长': [
        '成长', '改变', '觉醒', '认知', '思维', '模式',
        '习惯', '突破', '修行', '觉察', '意识', '突破',
        '接纳', '慈悲', '暂停', '选择',
    ],
    '心虫开发': [
        '心虫', 'heartflow', 'heart-logic', '版本', '升级',
        '修复', 'bug', '代码', '模块', '引擎', '启动',
        'skill', 'hermes', '路由', '脚本',
    ],
    '通用对话': [],  # 兜底话题
}

# 预计算 IDF
def _compute_topic_idf():
    """计算每个话题的逆文档频率（IDF）。"""
    all_tokens = set()
    for tokens in _TOPIC_CENTROIDS.values():
        all_tokens.update(tokens)
    N = len([t for t in _TOPIC_CENTROIDS if t != '通用对话'])
    idf = {}
    for topic, tokens in _TOPIC_CENTROIDS.items():
        if topic == '通用对话':
            continue
        idf[topic] = {}
        for token in all_tokens:
            df = sum(1 for ts in _TOPIC_CENTROIDS.values() if token in ts)
            idf[topic][token] = math.log(N / max(df, 1)) if df > 0 else 0
    return idf

_TOPIC_IDF = _compute_topic_idf()


def _tokenize(text: str) -> list:
    """
    分词：中文 2-gram + 3-gram，英文保留原词。
    移植自 HeartFlow psychology.js _tokenize()。
    """
    clean = re.sub(r'[^\u4e00-\u9fff\w\s]', ' ', text.lower())
    tokens = []
    for word in clean.split():
        if not word:
            continue
        if re.search(r'[\u4e00-\u9fff]', word):
            # 中文：2-gram + 3-gram
            for i in range(len(word) - 1):
                tokens.append(word[i:i+2])
            for i in range(len(word) - 2):
                tokens.append(word[i:i+3])
        else:
            # 英文/数字
            if len(word) >= 2:
                tokens.append(word)
    return tokens


def _tf(tokens: list) -> dict:
    """计算词频（Term Frequency）。"""
    counter = Counter(tokens)
    total = len(tokens)
    return {token: count / total for token, count in counter.items()} if total > 0 else {}


def _cosine_sim(vec_a: dict, vec_b: dict) -> float:
    """计算两个 TF-IDF 向量的余弦相似度。"""
    all_keys = set(vec_a.keys()) | set(vec_b.keys())
    dot = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in all_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _topic_centroid(topic: str) -> dict:
    """计算话题中心向量（TF-IDF）。"""
    tokens = _TOPIC_CENTROIDS.get(topic, [])
    tf_vals = _tf(tokens)
    centroid = {}
    for token, tf_val in tf_vals.items():
        idf_val = _TOPIC_IDF.get(topic, {}).get(token, 1.0)
        centroid[token] = tf_val * idf_val
    return centroid


# 预计算所有话题中心
_CENTROIDS = {}
for topic in _TOPIC_CENTROIDS:
    if topic != '通用对话':
        _CENTROIDS[topic] = _topic_centroid(topic)


def detect_topic(text: str) -> dict:
    """
    语义级话题检测。
    移植自 HeartFlow psychology.js detectTopic()。

    Args:
        text: 用户输入文本

    Returns:
        dict 包含：
          - topic: str — 检测到的话题名
          - confidence: float — 置信度 0..1
          - is_meta_continue: bool — 是否元指令续接
          - method: str — 检测方法（keyword_strong/semantic/short_text）
          - matched_topics: dict — 所有命中话题及关键词
    """
    if not text:
        return {
            'topic': '通用对话',
            'confidence': 0.0,
            'is_meta_continue': False,
            'method': 'empty_input',
            'matched_topics': {},
        }

    lower = text.lower()

    # 元指令检测
    is_meta_continue = any(p in lower for p in _CONTINUE_PATTERNS)

    # Step 1: 关键词命中（高精度）
    matched = {}
    for topic, kws in _TOPIC_CENTROIDS.items():
        if topic == '通用对话':
            continue
        hits = [kw for kw in kws if kw in lower]
        if hits:
            matched[topic] = hits

    # Step 2: 高置信度关键词命中（≥3个词）→ 直接返回
    if matched:
        for topic, hits in matched.items():
            if len(hits) >= 3:
                return {
                    'topic': topic,
                    'confidence': 1.0,
                    'is_meta_continue': is_meta_continue,
                    'method': 'keyword_strong',
                    'matched_topics': matched,
                    'keywords': hits,
                }

    # Step 3: 语义级检测（TF-IDF cosine similarity）
    tokens = _tokenize(text)
    if len(tokens) < 3:
        # 短文本：降级到关键词模式
        primary = max(matched, key=lambda t: len(matched[t])) if matched else '通用对话'
        return {
            'topic': primary,
            'confidence': 0.5 if matched else 0.1,
            'is_meta_continue': is_meta_continue,
            'method': 'short_text',
            'matched_topics': matched,
        }

    input_tf = _tf(tokens)
    input_vec = {}
    for token, tf_val in input_tf.items():
        avg_idf = 0.0
        count = 0
        for topic in _CENTROIDS:
            if _TOPIC_IDF.get(topic, {}).get(token):
                avg_idf += _TOPIC_IDF[topic][token]
                count += 1
        input_vec[token] = tf_val * (avg_idf / count if count > 0 else 1.0)

    scores = {}
    for topic, centroid in _CENTROIDS.items():
        scores[topic] = _cosine_sim(input_vec, centroid)

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_topic = sorted_scores[0][0]
    best_score = sorted_scores[0][1]

    # 阈值：如果最高分低于 0.1，可能是通用对话
    if best_score < 0.1 and matched:
        primary = max(matched, key=lambda t: len(matched[t]))
        return {
            'topic': primary,
            'confidence': 0.3,
            'is_meta_continue': is_meta_continue,
            'method': 'keyword_fallback',
            'matched_topics': matched,
        }
    elif best_score < 0.05:
        return {
            'topic': '通用对话',
            'confidence': 0.1,
            'is_meta_continue': is_meta_continue,
            'method': 'no_match',
            'matched_topics': matched,
        }

    return {
        'topic': best_topic,
        'confidence': round(best_score, 3),
        'is_meta_continue': is_meta_continue,
        'method': 'semantic',
        'matched_topics': matched,
    }


class TopicScope:
    """
    话题作用域隔离（Python 版）。

    移植自 HeartFlow identity/topic-scope.js。
    每个话题拥有独立的 store（知识库）和 context（工作上下文）。
    支持 push/pop 话题栈，新话题自动隔离旧上下文。
    """

    def __init__(self):
        self._topics = {}       # {topic_name: {'store': {}, 'context': {}, 'created_at': timestamp}}
        self._stack = []         # 话题进入顺序
        self._current = None     # 当前话题名
        self._context = {}       # 当前话题的工作上下文

    def push(self, topic: str, initial_context: dict = None) -> 'TopicScope':
        """
        进入话题。如果话题已存在，恢复之前保存的上下文。

        Args:
            topic: 话题名
            initial_context: 可选的初始上下文

        Returns:
            self
        """
        initial_context = initial_context or {}

        # 保存当前话题上下文
        if self._current is not None and self._current in self._topics:
            self._topics[self._current]['context'] = dict(self._context)

        # 进入/恢复话题
        if topic not in self._topics:
            self._topics[topic] = {
                'store': {},
                'context': {},
                'created_at': __import__('time').time(),
            }
        else:
            self._context = dict(self._topics[topic].get('context', {}))

        # 合并初始上下文
        if initial_context:
            self._context.update(initial_context)

        self._current = topic
        if topic not in self._stack:
            self._stack.append(topic)

        return self

    def pop(self) -> 'TopicScope':
        """
        退出当前话题，恢复上一个话题。

        Returns:
            self
        """
        if len(self._stack) <= 1:
            return self

        # 保存当前话题
        if self._current is not None and self._current in self._topics:
            self._topics[self._current]['context'] = dict(self._context)

        # 弹出当前
        self._stack.pop()
        self._current = self._stack[-1] if self._stack else None

        if self._current is not None and self._current in self._topics:
            self._context = dict(self._topics[self._current].get('context', {}))
        else:
            self._context = {}

        return self

    def store(self, key: str, value) -> 'TopicScope':
        """在当前话题存储数据。"""
        if self._current and self._current in self._topics:
            self._topics[self._current]['store'][key] = value
        return self

    def get(self, key: str):
        """从当前话题读取数据。"""
        if self._current and self._current in self._topics:
            return self._topics[self._current]['store'].get(key)
        return None

    def set_context(self, key: str, value) -> 'TopicScope':
        """设置当前话题的工作上下文。"""
        self._context[key] = value
        return self

    def get_context(self, key: str):
        """读取当前话题的工作上下文。"""
        return self._context.get(key)

    def clear_context(self) -> 'TopicScope':
        """清空当前话题的工作上下文（保留 store）。"""
        self._context = {}
        return self

    def clear_all(self) -> 'TopicScope':
        """完全重置当前话题。"""
        if self._current and self._current in self._topics:
            self._topics[self._current] = {
                'store': {},
                'context': {},
                'created_at': __import__('time').time(),
            }
            self._context = {}
        return self

    @property
    def current(self):
        return self._current

    @property
    def stack(self):
        return list(self._stack)

    def get_topics(self) -> list:
        """获取所有话题概览。"""
        return [
            {
                'name': name,
                'store_keys': list(data['store'].keys()),
                'has_context': bool(data['context']),
            }
            for name, data in self._topics.items()
        ]

    def diagnose(self, label: str = '') -> str:
        """诊断：返回当前状态字符串。"""
        lines = [f'=== TopicScope 诊断{f" — {label}" if label else ""} ===']
        lines.append(f'当前话题: {self._current}')
        lines.append(f'话题栈: {" → ".join(self._stack) if self._stack else "(空)"}')
        for name, data in self._topics.items():
            lines.append(f'  话题[{name}] store.keys: {list(data["store"].keys())}')
        return '\n'.join(lines)


def ensure_topic_isolation(
    user_input: str,
    scope: TopicScope,
    task_classification: dict = None,
) -> dict:
    """
    话题切换执行器。
    移植自 HeartFlow psychology.js ensureTopicIsolation()。

    在每次路由处理前调用，确保：
      - 新话题 → push → 干净上下文
      - 续接 → pop → 恢复之前话题
      - 同一话题 → keep

    Args:
        user_input: 用户输入
        scope: TopicScope 实例
        task_classification: @task_classify 的结果（可选，用于增强判断）

    Returns:
        dict 包含：
          - switched: bool — 是否切换了话题
          - topic: str — 当前话题名
          - action: str — 'push' / 'pop' / 'init' / 'keep'
          - previous: str — 切换前的话题
          - reason: str — 切换理由
    """
    detection = detect_topic(user_input)
    current = scope.current
    previous = current

    # 使用 task_classification 辅助判断
    task_cls = task_classification or {}

    # 场景 1: 元指令续接 → pop
    if detection['is_meta_continue'] or task_cls.get('classification') == 'continuation':
        was_empty = len(scope.stack) == 0
        if not was_empty:
            scope.pop()
        return {
            'switched': True,
            'topic': scope.current or '无',
            'action': 'pop',
            'previous': previous,
            'reason': '元指令继续，恢复之前话题',
        }

    # 场景 2: 新话题（非通用）且不同于当前 → push
    if detection['topic'] != '通用对话' and detection['topic'] != current:
        scope.push(detection['topic'])
        return {
            'switched': True,
            'topic': detection['topic'],
            'action': 'push',
            'previous': previous,
            'reason': f'新话题[{detection["topic"]}]，上下文已隔离',
        }

    # 场景 3: 首次初始化
    if current is None and detection['topic'] != '通用对话':
        scope.push(detection['topic'])
        return {
            'switched': True,
            'topic': detection['topic'],
            'action': 'init',
            'previous': None,
            'reason': '首次话题初始化',
        }

    return {
        'switched': False,
        'topic': current,
        'action': 'keep',
        'previous': previous,
        'reason': '话题未变，保持当前上下文',
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 4 层升级路由 — 完整决策树
# 将 HeartFlow 的元认知层 + fu-mu-gong-ke 的 3 层路由合并为统一的 4 层架构
# ═══════════════════════════════════════════════════════════════════════════════

# fu-mu-gong-ke 危机检测关键词（原第1层）
_CRISIS_KEYWORDS = [
    '自杀', '不想活', '想死', '自伤', '割', '遗书',
    '解脱', '活着没意思', 'zs', '结束生命',
]

_CRISIS_METAPHORS = [
    '累了真的累了', '一切都无所谓了',
    '撑不下去了', '没意思', '不如死了',
]

# fu-mu-gong-ke 用户身份检测（原第2层）
_IDENTITY_PATTERNS = {
    'parent': ['我的孩子', '我孩子', '我家孩子', '我儿子', '我女儿', '我家娃', '我家小孩'],
    'child': ['我的父母', '我的父亲', '我的母亲', '我爸', '我妈妈', '我妈', '我爹'],
    'intermediary': ['我朋友的孩子', '我姐的孩子', '我哥的孩子', '我亲戚的孩子', '我邻居的孩子'],
}

# fu-mu-gong-ke 场景关键词索引（原第3层简化版）
_SCENARIO_INDEX = {
    '孩子成绩下降': ['成绩', '分数', '考试', '退步', '下降', '倒数'],
    '孩子不想上学': ['上学', '逃学', '厌学', '不想上学', '不去学校'],
    '孩子说不想活了': ['不想活', '自杀', 'zs', '结束生命', '死了'],
    '孩子拒绝沟通': ['拒绝沟通', '不说话', '锁门', '不理我', '不跟我说话'],
    '孩子打人发脾气': ['打人', '发脾气', '摔东西', '暴力', '动手'],
    '父母情绪崩溃': ['崩溃', '失控', '撑不住', '受不了', '受不了了'],
    '孩子沉迷手机': ['手机', '游戏', '沉迷', '网瘾', '刷视频', 'ipad'],
    '孩子被霸凌': ['霸凌', '欺负', '被打', '被排挤', '孤立'],
    '青春期叛逆': ['叛逆', '青春期', '不听话', '顶嘴', '反抗'],
    '离婚分居影响': ['离婚', '分居', '单亲', '离异'],
    '孩子休学退学': ['休学', '退学', '不上学', '辍学'],
    '孩子早恋': ['早恋', '谈恋爱', '男朋友', '女朋友', '约会'],
    '代际创伤复制': ['复制', '像我爸妈', '原生家庭', '代际', '童年'],
    '父母育儿倦怠': ['倦怠', '太累了', '带不动', '撑不住了', '身心俱疲'],
}


def _detect_crisis(user_input: str) -> dict:
    """
    fu-mu-gong-ke 第1层：危机信号检测。

    Returns:
        dict: {is_crisis, level, matched_keywords, matched_metaphors, level_name}
    """
    text = user_input.lower()
    kw_hits = [kw for kw in _CRISIS_KEYWORDS if kw in text]
    meta_hits = [m for m in _CRISIS_METAPHORS if m in text]

    is_crisis = bool(kw_hits) or bool(meta_hits)
    level = 4 if bool(kw_hits) else (3 if bool(meta_hits) else 1)
    level_name = {1: '🟢 L1-安全', 3: '🟡 L3-转介', 4: '⚫ L4-危机'}.get(level, '🟢 L1-安全')

    return {
        'is_crisis': is_crisis,
        'level': level,
        'level_name': level_name,
        'matched_keywords': kw_hits,
        'matched_metaphors': meta_hits,
    }


def _detect_identity(user_input: str) -> dict:
    """
    fu-mu-gong-ke 第2层：用户身份识别。

    Returns:
        dict: {identity, confidence, matched_pattern}
    """
    text = user_input.lower()
    for identity, patterns in _IDENTITY_PATTERNS.items():
        for p in patterns:
            if p in text:
                return {'identity': identity, 'confidence': 0.9, 'matched_pattern': p}

    return {'identity': 'unknown', 'confidence': 0.1, 'matched_pattern': None}


def _match_scenario(user_input: str, what_is_this_result: dict = None) -> dict:
    """
    fu-mu-gong-ke 第3层：场景匹配。

    基于场景关键词索引进行匹配。

    Returns:
        dict: {matched_scenario, confidence, keywords}
    """
    text = user_input.lower()
    scores = {}
    for scenario, kws in _SCENARIO_INDEX.items():
        hits = [kw for kw in kws if kw in text]
        if hits:
            scores[scenario] = len(hits)

    if not scores:
        return {'matched_scenario': None, 'confidence': 0.0, 'keywords': []}

    best = max(scores.items(), key=lambda x: x[1])
    return {
        'matched_scenario': best[0],
        'confidence': min(1.0, best[1] / 3.0),
        'keywords': _SCENARIO_INDEX[best[0]],
    }


def route_pipeline(user_input: str, scope: TopicScope = None) -> dict:
    """
    完整 4 层路由管道。

    整合了：
      Layer 0: whatIsThis 元认知先行判断
      @task_classify 任务分类门
      TopicScope 话题隔离
      Layer 1: 危机检测
      Layer 2: 用户身份识别
      Layer 3: 场景匹配

    Args:
        user_input: 用户输入的原始文本
        scope: 可选的 TopicScope 实例（不传则创建新的）

    Returns:
        dict 包含各层结果
    """
    if scope is None:
        scope = TopicScope()

    # ─── Layer 0: 元认知先行判断 ─────────────────────────────────
    meta = what_is_this(user_input)

    # ─── @task_classify 任务分类门 ───────────────────────────────
    task_cls = classify_task(user_input, what_is_this_result=meta)

    # ─── TopicScope 话题隔离 ─────────────────────────────────────
    isolation = ensure_topic_isolation(user_input, scope, task_classification=task_cls)

    # ─── Layer 1: 危机检测 ───────────────────────────────────────
    crisis = _detect_crisis(user_input)

    # ─── Layer 2: 用户身份识别 ──────────────────────────────────
    identity = _detect_identity(user_input)

    # ─── Layer 3: 场景匹配 ──────────────────────────────────────
    scenario = _match_scenario(user_input, what_is_this_result=meta)

    # ─── 综合决策建议 ────────────────────────────────────────────
    decision = _make_decision(meta, task_cls, isolation, crisis, identity, scenario)

    return {
        'user_input': user_input,
        'layer0_what_is_this': meta,
        'task_classification': task_cls,
        'topic_scope': {
            'current': scope.current,
            'stack': scope.stack,
            'isolation': isolation,
        },
        'layer1_crisis': crisis,
        'layer2_identity': identity,
        'layer3_scenario': scenario,
        'decision': decision,
        'pipeline': [
            {'layer': 0, 'name': 'whatIsThis 元认知', 'result': meta['dialogue_type']},
            {'layer': 'task', 'name': '@task_classify', 'result': task_cls['classification']},
            {'layer': 'topic', 'name': 'TopicScope 话题隔离', 'result': isolation['action']},
            {'layer': 1, 'name': '危机检测', 'result': crisis['level_name']},
            {'layer': 2, 'name': '用户身份', 'result': identity['identity']},
            {'layer': 3, 'name': '场景匹配', 'result': scenario['matched_scenario'] or '通用分析'},
        ],
    }


def _make_decision(
    meta: dict,
    task_cls: dict,
    isolation: dict,
    crisis: dict,
    identity: dict,
    scenario: dict,
) -> dict:
    """
    综合决策引擎。
    基于所有 4 层结果生成最终的行动建议。

    决策规则：
      - 危机信号 → 立即转介（短路）
      - casual_reply → 简短回应
      - continuation → 恢复话题上下文
      - new_task → 完整路由处理
    """
    # 短路规则：危机优先
    if crisis['is_crisis']:
        return {
            'action': 'crisis_intervention',
            'priority': '最高',
            'summary': '⚠️ 检测到危机信号，立即进入危机干预流程',
            'safety_level': crisis['level_name'],
            'should_short_circuit': True,
        }

    # 随口回复
    if task_cls['classification'] == 'casual_reply':
        return {
            'action': 'casual_reply',
            'priority': '低',
            'summary': '简短回应，无需深度处理',
            'safety_level': '🟢 L1-安全',
            'should_short_circuit': False,
        }

    # 续接
    if task_cls['classification'] == 'continuation':
        return {
            'action': 'continue_context',
            'priority': '中',
            'summary': f'续接话题[{isolation["topic"]}]，恢复上下文',
            'safety_level': '🟢 L1-安全',
            'should_short_circuit': False,
        }

    # 新任务：完整路由
    action_type = '育儿咨询' if meta['is_parent_child'] else (
        '情感支持' if meta['is_pain_present'] else '通用任务'
    )
    return {
        'action': action_type,
        'priority': '高',
        'summary': (
            f'用户身份[{identity["identity"]}] '
            f'→ 场景[{scenario["matched_scenario"] or "通用分析"}] '
            f'→ 话题[{isolation["topic"] or "通用对话"}]'
        ),
        'safety_level': crisis['level_name'],
        'should_short_circuit': False,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI 入口：接收用户输入，输出完整路由结果。"""
    import sys

    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = input('👤 输入用户消息: ').strip()

    if not text:
        print('❌ 输入为空')
        return

    result = route_pipeline(text)

    print(f'\n{"═" * 50}')
    print(f'心虫路由增强层 — 决策报告')
    print(f'{"═" * 50}')

    print(f'\n📝 输入: "{result["user_input"]}"')

    print(f'\n🔮 Layer 0: whatIsThis 元认知')
    m = result['layer0_what_is_this']
    print(f'   对话类型: {m["dialogue_type"]} (置信度: {m["confidence"]:.1%})')
    print(f'   特征: {"🔨急躁" if m["is_rushing"] else ""} {"👶亲子" if m["is_parent_child"] else ""} {"💔痛感" if m["is_pain_present"] else ""}')
    print(f'   情绪: {m["emotion"]["insight"]}')

    print(f'\n🎯 @task_classify 任务分类')
    tc = result['task_classification']
    print(f'   分类: {tc["classification"]} (置信度: {tc["confidence"]:.1%})')
    print(f'   理由: {tc["reason"]}')

    print(f'\n🧩 TopicScope 话题隔离')
    ts = result['topic_scope']
    print(f'   当前话题: {ts["current"] or "(空)"}')
    print(f'   话题栈: {" → ".join(ts["stack"]) if ts["stack"] else "(空)"}')
    iso = ts['isolation']
    print(f'   动作: {iso["action"]} — {iso["reason"]}')

    print(f'\n🛡️  Layer 1: 危机检测')
    c = result['layer1_crisis']
    print(f'   {c["level_name"]}')
    if c['matched_keywords']:
        print(f'   命中关键词: {c["matched_keywords"]}')
    if c['matched_metaphors']:
        print(f'   命中隐喻: {c["matched_metaphors"]}')

    print(f'\n👤 Layer 2: 用户身份')
    i = result['layer2_identity']
    print(f'   身份: {i["identity"]} (置信度: {i["confidence"]:.1%})')

    print(f'\n📋 Layer 3: 场景匹配')
    s = result['layer3_scenario']
    print(f'   场景: {s["matched_scenario"] or "通用分析"} (置信度: {s["confidence"]:.1%})')

    print(f'\n⚡ 综合决策')
    d = result['decision']
    print(f'   行动: {d["action"]}')
    print(f'   优先级: {d["priority"]}')
    print(f'   概要: {d["summary"]}')

    print(f'\n📊 管道链路')
    for step in result['pipeline']:
        print(f'   [{step["layer"]}] {step["name"]} → {step["result"]}')

    print(f'\n{"═" * 50}')


if __name__ == '__main__':
    main()
