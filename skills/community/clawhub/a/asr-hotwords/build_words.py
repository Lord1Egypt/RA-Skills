#!/usr/bin/env python3
"""
ASR 个性化中文歧义词表构建脚本

Pipeline:
  阶段一：数据准备（锚点词表 + 聊天记录解析）
  阶段二：数据预清洗（规则预分析 + LLM 终判）
  阶段三：统计粗筛（词频 + fuzzy pinyin 碰撞检测）
  阶段四：LLM 精炼（审核 + 补充 + 中英混合 + 场景描述）
  阶段五：自动验证（构造测试集 + 模拟纠正 + 评估指标）

Usage:
  python build_words.py \\
    --chat data/chat.txt \\
    --anchors data/anchors.json \\
    --output vocab_table.json \\
    --api-key sk-xxx \\
    --base-url https://api.example.com/v1 \\
    --model claude-sonnet-4-20250514

聊天数据格式:
  用户A：你好
  用户B：你好，方案发给我了吗
  用户A：晨旭说下午发
"""

import argparse
import json
import logging
import multiprocessing
import os
import pickle
import random
import re
import sys
import time
import time as _time
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("build_words")
_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(_handler)
logger.setLevel(logging.INFO)

# --- 依赖检查 ---
try:
    import jieba
    from pypinyin import pinyin, Style
except ImportError as e:
    logger.error(f"缺少依赖: {e}")
    logger.error("请安装: pip install jieba pypinyin")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    logger.error("缺少 openai 包: pip install openai")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


# ============================================================
# 配置
# ============================================================

CONFIG = {
    "min_freq": 3,
    "min_word_length": 2,
    "fuzzy_rules": {
        "ang": "an", "eng": "en", "ing": "in", "ong": "on",
        "zh": "z", "ch": "c", "sh": "s",
    },
    "person_action_words": {
        "说", "来了", "去了", "负责", "跟进", "回复", "问",
        "做的", "那边", "约了", "来", "走了", "请假", "的",
    },
    "stop_words": {
        "的", "了", "把", "给", "在", "和", "是", "我", "你",
        "他", "她", "这", "那", "不", "也", "都", "就", "会",
        "有", "到", "说", "要", "能", "可以", "什么", "怎么",
        "吧", "吗", "呢", "啊", "呀", "哦", "嗯", "好", "对",
        "没有", "一个", "一下", "这个", "那个", "还是",
        "因为", "所以", "但是", "如果", "虽然", "已经", "正在",
        "非常", "比较", "应该", "知道", "觉得", "时候", "现在",
        "然后", "或者", "而且", "不过", "其实", "可能",
    },
    "validation_sample_size": 100,
    "validation_recall_threshold": 0.90,
    "validation_overcorrection_threshold": 0.05,
}


# ============================================================
# 工具：Fuzzy Pinyin
# ============================================================

_fuzzy_cache = {}


def strip_tones(pinyin_str: str) -> str:
    """去除拼音声调"""
    tone_map = str.maketrans(
        "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ",
        "aaaaeeeeiiiioooouuuuüüüü",
    )
    return pinyin_str.translate(tone_map)


def get_fuzzy_pinyin(word: str) -> str:
    """获取模糊拼音（带缓存）"""
    if word in _fuzzy_cache:
        return _fuzzy_cache[word]

    py = pinyin(word, style=Style.TONE)
    raw = " ".join(p[0] for p in py)
    result = strip_tones(raw)

    # 按长度降序应用规则，避免短规则干扰长规则
    rules = CONFIG["fuzzy_rules"]
    for old, new in sorted(rules.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(old, new)

    _fuzzy_cache[word] = result
    return result


# ============================================================
# 缓存：Fuzzy 索引持久化
# ============================================================

def _jieba_dict_mtime() -> float:
    dict_path = os.path.join(os.path.dirname(jieba.__file__), jieba.DEFAULT_DICT_NAME)
    return os.path.getmtime(dict_path) if os.path.exists(dict_path) else 0.0


def _default_cache_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, ".cache", "fuzzy_index.pkl")


def load_cached_index(cache_path: str) -> Optional[Tuple[Dict, Dict]]:
    """从磁盘加载缓存，校验 jieba 词典是否变化。返回 (general_freq, fuzzy_index) 或 None。"""
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, "rb") as f:
            data = pickle.load(f)
        if data.get("dict_mtime") != _jieba_dict_mtime():
            logger.warning("[缓存] jieba 词典已更新，缓存失效，重新构建...")
            return None
        logger.info(f"[缓存] 从缓存加载 fuzzy 索引: {cache_path}")
        return data["general_freq"], data["fuzzy_index"]
    except Exception as e:
        logger.warning(f"[缓存] 加载失败 ({e})，重新构建...")
        return None


def save_cached_index(
    cache_path: str,
    general_freq: Dict[str, int],
    fuzzy_index: Dict[str, List[Tuple[str, int]]],
) -> None:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    data = {
        "dict_mtime": _jieba_dict_mtime(),
        "general_freq": general_freq,
        "fuzzy_index": fuzzy_index,
    }
    with open(cache_path, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    logger.info(f"[缓存] 索引已保存: {cache_path}")


# ============================================================
# 工具：批量分词
# ============================================================

def _tokenize_worker(text):
    """子进程分词 worker"""
    return jieba.lcut(text)

def _init_jieba():
    """子进程初始化 jieba"""
    jieba.initialize()

def batch_tokenize(messages, workers=None):
    """批量分词，结果写入 msg['words']"""
    if workers is None:
        workers = os.cpu_count() or 1
    t0 = _time.time()
    texts = [msg["text"] for msg in messages]
    logger.info(f"批量分词: {len(messages)} 条消息，{workers} 进程")
    if workers <= 1 or len(messages) < 100:
        results = [jieba.lcut(t) for t in texts]
    else:
        with multiprocessing.Pool(workers, initializer=_init_jieba) as pool:
            results = pool.map(_tokenize_worker, texts)
    for msg, words in zip(messages, results):
        msg["words"] = words
    elapsed = _time.time() - t0
    logger.info(f"批量分词完成: {elapsed:.2f}秒")
    return messages

def retokenize_changed(original_messages, cleaned_messages, workers=None):
    """只对文本被修改的消息重新分词，未修改的复用原有 words"""
    changed = []
    for orig, cleaned in zip(original_messages, cleaned_messages):
        if orig["text"] != cleaned["text"]:
            changed.append(cleaned)
        else:
            cleaned["words"] = orig.get("words", jieba.lcut(orig["text"]))
    if changed:
        logger.info(f"重新分词: {len(changed)} 条被修改的消息")
        batch_tokenize(changed, workers)
    return cleaned_messages


# ============================================================
# 工具：LLM 客户端
# ============================================================

class LLMClient:
    """LLM API 客户端"""

    def __init__(self, api_key: str, base_url: str, model: str, api_format: str = "anthropic"):
        self.api_format = api_format
        self.model = model
        if api_format == "anthropic":
            if Anthropic is None:
                raise ImportError("缺少 anthropic 包: pip install anthropic")
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key, base_url=base_url)

    def call(self, prompt: str, system: str = None, max_retries: int = 3) -> str:
        """调用 LLM，返回文本"""
        for attempt in range(max_retries):
            try:
                if self.api_format == "anthropic":
                    kwargs = {
                        "model": self.model,
                        "max_tokens": 16384,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                    if system:
                        kwargs["system"] = system
                    resp = self.client.messages.create(**kwargs)
                    return resp.content[0].text
                else:
                    messages = []
                    if system:
                        messages.append({"role": "system", "content": system})
                    messages.append({"role": "user", "content": prompt})
                    resp = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.1,
                        max_tokens=16384,
                    )
                    return resp.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    interval = 2 ** attempt
                    logger.warning(f"LLM 调用失败 (尝试 {attempt + 1}/{max_retries}): {e}，{interval}秒后重试...")
                    time.sleep(interval)
                else:
                    logger.warning(f"LLM 调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
        raise RuntimeError(f"LLM 调用失败，已重试 {max_retries} 次")

    def call_json(self, prompt: str, system: str = None, max_retries: int = 3):
        """调用 LLM，解析 JSON"""
        text = self.call(prompt, system, max_retries=max_retries)
        return _extract_json(text)


def _extract_json(text: str):
    """从 LLM 响应中提取 JSON"""
    # 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 从 markdown 代码块提取
    m = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # 贪心匹配 JSON 数组或对象
    for pattern in [r"\[.*\]", r"\{.*\}"]:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                continue
    # 尝试修复截断的 JSON（输出被 max_tokens 截断时）
    repaired = _repair_truncated_json(text)
    if repaired is not None:
        return repaired
    raise ValueError(f"无法从 LLM 响应中提取 JSON:\n{text[:500]}")


def _repair_truncated_json(text: str):
    """尝试修复被截断的 JSON 数组。返回解析结果或 None。"""
    # 找到 JSON 数组的开始位置
    start = text.find('[')
    if start == -1:
        return None
    fragment = text[start:]
    # 尝试逐步回退到最后一个完整的 JSON 对象
    # 策略：找最后一个 '},',从那里截断，补上 ']'
    last_complete = fragment.rfind('},')
    if last_complete == -1:
        last_complete = fragment.rfind('}')
    if last_complete == -1:
        return None
    truncated = fragment[:last_complete + 1] + ']'
    try:
        result = json.loads(truncated)
        if isinstance(result, list) and len(result) > 0:
            logger.warning(f"JSON 被截断，已修复（恢复 {len(result)} 个完整条目）")
            return result
    except json.JSONDecodeError:
        pass
    return None


# ============================================================
# 阶段一：数据准备
# ============================================================

def parse_chat(file_path: str) -> List[dict]:
    """
    解析聊天记录文件。
    格式：每行 "发送者：内容" 或 "发送者: 内容"
    """
    messages = []
    pattern = re.compile(r"^(.+?)[：:]\s*(.+)$")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            m = pattern.match(line)
            if m:
                sender = m.group(1).strip()
                content = m.group(2).strip()
                if content:
                    messages.append({
                        "sender": sender,
                        "text": content,
                        "line_no": line_no,
                    })

    logger.info(f"[阶段一] 解析聊天记录: {len(messages)} 条消息")
    return messages


def load_anchors(file_path: str) -> List[dict]:
    """
    加载锚点词表。
    支持格式：
      - 字符串列表: ["晨旭", "宝洁"]
      - 对象列表: [{"term": "晨旭", "category": "person"}, ...]
    """
    if not file_path or not os.path.exists(file_path):
        logger.info("[阶段一] 未提供锚点词表")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        if data and isinstance(data[0], str):
            data = [{"term": w, "category": "unknown"} for w in data]

    logger.info(f"[阶段一] 加载锚点词表: {len(data)} 个词")
    return data


def load_general_freq() -> Dict[str, int]:
    """加载通用中文词频表（jieba 内置词典）"""
    jieba.initialize()
    freq = dict(jieba.dt.FREQ) if hasattr(jieba.dt, "FREQ") else {}
    logger.info(f"[阶段一] 加载通用词频表: {len(freq)} 个词")
    return freq


def build_fuzzy_index(general_freq: Dict[str, int]) -> Dict[str, List[Tuple[str, int]]]:
    """为通用词频表构建 fuzzy pinyin 索引（加速碰撞检测）"""
    index = defaultdict(list)
    count = 0
    for word, freq in general_freq.items():
        if len(word) < 2 or len(word) > 6:
            continue
        fp = get_fuzzy_pinyin(word)
        index[fp].append((word, freq))
        count += 1
    logger.info(f"[阶段一] 构建 fuzzy 索引: {count} 个词")
    return dict(index)


# ============================================================
# 阶段二：数据预清洗
# ============================================================

def rule_pre_analysis(
    messages: List[dict], anchors: List[dict]
) -> List[dict]:
    """规则预分析：四种信号检测"""
    suspicious = []
    anchor_terms = {a["term"] for a in anchors}

    # --- 信号 1：锚点词表反向检测 ---
    anchor_fuzzy = {}  # fuzzy_pinyin → anchor_term
    for a in anchors:
        fp = get_fuzzy_pinyin(a["term"])
        anchor_fuzzy[fp] = a["term"]

    for msg in messages:
        words = msg.get("words") or jieba.lcut(msg["text"])
        for word in words:
            if len(word) < 2:
                continue
            fp = get_fuzzy_pinyin(word)
            if fp in anchor_fuzzy and word != anchor_fuzzy[fp]:
                suspicious.append({
                    "message": msg["text"],
                    "line_no": msg.get("line_no"),
                    "word": word,
                    "suggested": anchor_fuzzy[fp],
                    "fuzzy_pinyin": fp,
                    "signal": "anchor_match",
                    "strength": "strong",
                })

    # --- 信号 2：跨用户交叉验证 ---
    senders = list(set(m["sender"] for m in messages))
    if len(senders) >= 2:
        # 每个发送者的词 → fuzzy pinyin 映射
        sender_fp_map = {}  # sender → {fuzzy_pinyin: word}
        for sender in senders:
            fp_map = {}
            for m in messages:
                if m["sender"] != sender:
                    continue
                for w in (m.get("words") or jieba.lcut(m["text"])):
                    if len(w) >= 2:
                        fp_map[get_fuzzy_pinyin(w)] = w
            sender_fp_map[sender] = fp_map

        for i, s1 in enumerate(senders):
            for s2 in senders[i + 1:]:
                for fp, w1 in sender_fp_map[s1].items():
                    w2 = sender_fp_map[s2].get(fp)
                    if w2 and w1 != w2:
                        # 锚点表中的那个更可能正确
                        if w2 in anchor_terms and w1 not in anchor_terms:
                            suspicious.append({
                                "message": f"[跨用户] {s1}用'{w1}', {s2}用'{w2}'",
                                "word": w1,
                                "suggested": w2,
                                "fuzzy_pinyin": fp,
                                "signal": "cross_user",
                                "strength": "strong",
                            })

    # --- 信号 3：自我修正检测 ---
    for sender in senders:
        sender_msgs = [m for m in messages if m["sender"] == sender]
        for i in range(1, len(sender_msgs)):
            curr_text = sender_msgs[i]["text"]
            prev_text = sender_msgs[i - 1]["text"]

            # 模式：紧跟着只发了一个短词（纠正）
            if len(curr_text) <= 4:
                curr_fp = get_fuzzy_pinyin(curr_text)
                for w in (sender_msgs[i-1].get("words") or jieba.lcut(prev_text)):
                    if len(w) >= 2 and w != curr_text:
                        if get_fuzzy_pinyin(w) == curr_fp:
                            suspicious.append({
                                "message": f"[自我修正] '{prev_text}' → '{curr_text}'",
                                "word": w,
                                "suggested": curr_text,
                                "fuzzy_pinyin": curr_fp,
                                "signal": "self_correction",
                                "strength": "strong",
                            })

    # --- 信号 4：语义异常检测 ---
    person_actions = CONFIG["person_action_words"]
    for msg in messages:
        words = msg.get("words") or jieba.lcut(msg["text"])
        for i, word in enumerate(words):
            if len(word) < 2 or word in anchor_terms:
                continue
            if i + 1 < len(words) and words[i + 1] in person_actions:
                suspicious.append({
                    "message": msg["text"],
                    "line_no": msg.get("line_no"),
                    "word": word,
                    "pattern": f"{word}{words[i + 1]}",
                    "signal": "semantic_anomaly",
                    "strength": "medium",
                })

    # 去重
    seen = set()
    unique = []
    for s in suspicious:
        key = (s.get("word", ""), s.get("signal", ""), str(s.get("line_no", "")))
        if key not in seen:
            seen.add(key)
            unique.append(s)

    logger.info(f"[阶段二] 规则预分析: 发现 {len(unique)} 个可疑项")
    return unique


def llm_data_cleaning(
    messages: List[dict],
    suspicious: List[dict],
    anchors: List[dict],
    llm: LLMClient,
    max_retries: int = 3,
) -> List[dict]:
    """LLM 终判 + 修正聊天记录"""
    if not suspicious:
        logger.info("[阶段二] 无可疑项，跳过 LLM 清洗")
        return messages

    # 构造 prompt
    anchor_str = ", ".join(
        f"{a['term']}({a.get('category', '')})" for a in anchors
    )

    susp_lines = []
    for i, s in enumerate(suspicious, 1):
        line = f"{i}. 消息: \"{s['message']}\"\n   可疑词: \"{s['word']}\""
        if s.get("suggested"):
            line += f" → 可能应为 \"{s['suggested']}\""
        line += f"\n   信号: {s['signal']} [{s['strength']}]"
        if s.get("fuzzy_pinyin"):
            line += f", fuzzy_pinyin={s['fuzzy_pinyin']}"
        susp_lines.append(line)
    susp_str = "\n".join(susp_lines)

    sample = messages[:100] if len(messages) > 100 else messages
    chat_str = "\n".join(
        f"{i + 1}. [{m['sender']}] {m['text']}" for i, m in enumerate(sample)
    )

    prompt = f"""你是一个中文语音识别纠错专家。

## 任务
以下是用户的聊天记录，规则引擎已标注了一些可疑的同音/近音字错误。
请对每个可疑项做最终判断。

## 锚点词表（已确认正确的词汇）
{anchor_str}

## 规则引擎标注的可疑项
{susp_str}

## 聊天记录（上下文参考）
{chat_str}

## 要求
对每个可疑项判断：
1. 是否确实是错误？
2. 如果是错误，正确的词是什么？
3. 置信度：高/中/低

注意：同一个词在不同语境下可能一个是错的一个是对的。
比如"程序说"中的"程序"可能是人名误写，但"过下程序"中的"程序"是正确的。

请用 JSON 数组输出：
[
  {{
    "word": "可疑词",
    "message_fragment": "所在消息的关键片段",
    "is_error": true/false,
    "correct_word": "正确的词（如果 is_error=true）",
    "confidence": "高/中/低",
    "reason": "判断理由"
  }}
]"""

    logger.info("[阶段二] 调用 LLM 进行数据清洗...")
    try:
        result = llm.call_json(prompt, max_retries=max_retries)
    except Exception as e:
        logger.warning(f"LLM 清洗失败: {e}，跳过清洗")
        return messages

    if isinstance(result, dict):
        result = result.get("corrections", result.get("results", [result]))

    # 收集需要修正的项
    corrections = []  # [(wrong_word, correct_word)]
    for item in result:
        if not isinstance(item, dict):
            continue
        if item.get("is_error") and item.get("correct_word"):
            if item.get("confidence") in ("高", "中", "high", "medium"):
                corrections.append((item["word"], item["correct_word"]))

    # 应用修正
    correction_count = 0
    corrected = []
    for msg in messages:
        text = msg["text"]
        original = text
        for wrong, correct in corrections:
            if wrong in text:
                # 逐个替换，避免全量替换引起问题
                text = text.replace(wrong, correct, 1)
        if text != original:
            correction_count += 1
        corrected.append({**msg, "text": text})

    logger.info(f"[阶段二] LLM 清洗完成: 修正了 {correction_count} 条消息")
    return corrected


# ============================================================
# 阶段三：统计粗筛
# ============================================================

def statistical_filter(
    messages: List[dict],
    general_freq: Dict[str, int],
    fuzzy_index: Dict[str, List[Tuple[str, int]]],
    min_freq: int = None,
) -> List[dict]:
    """统计粗筛：词频 + fuzzy pinyin 碰撞检测"""
    min_freq = min_freq if min_freq is not None else CONFIG["min_freq"]
    stop_words = CONFIG["stop_words"]

    # Step 1: 分词 + 词频统计
    word_counter = Counter()
    for msg in messages:
        words = msg.get("words") or jieba.lcut(msg["text"])
        word_counter.update(w for w in words if len(w) >= CONFIG["min_word_length"])

    # Step 2: 过滤
    candidates = {}
    for word, freq in word_counter.items():
        if freq < min_freq:
            continue
        if word in stop_words:
            continue
        if re.match(r"^[\d\W]+$", word):
            continue
        candidates[word] = freq

    logger.info(f"[阶段三] 词频过滤后候选: {len(candidates)} 个")

    # Step 3: 碰撞检测（使用 fuzzy 索引加速）
    rough = []
    for word, user_freq in candidates.items():
        word_fp = get_fuzzy_pinyin(word)
        entries = fuzzy_index.get(word_fp, [])

        # 找同长度的同音/近音词
        confusables = [
            (w, f) for w, f in entries if w != word and len(w) == len(word)
        ]
        if not confusables:
            continue

        word_general_freq = general_freq.get(word, 0)
        top = max(confusables, key=lambda x: x[1])

        # 核心判断：用户的词是不是"非主流"同音词？
        if word_general_freq < top[1]:
            rough.append({
                "term": word,
                "user_frequency": user_freq,
                "general_frequency": word_general_freq,
                "top_confusable": top[0],
                "top_confusable_freq": top[1],
                "fuzzy_pinyin": word_fp,
                "confusables": [w for w, _ in sorted(confusables, key=lambda x: -x[1])[:5]],
            })

    rough.sort(key=lambda x: -x["user_frequency"])
    logger.info(f"[阶段三] 碰撞检测后粗候选: {len(rough)} 个")
    return rough


# ============================================================
# 阶段四：LLM 精炼
# ============================================================

def llm_refine(
    rough_candidates: List[dict],
    messages: List[dict],
    llm: LLMClient,
    max_retries: int = 3,
) -> List[dict]:
    """LLM 精炼：审核 + 补充遗漏 + 中英混合 + 场景描述"""

    # 候选词描述
    if rough_candidates:
        cand_str = "\n".join(
            f"{i}. {c['term']} (用户频率:{c['user_frequency']}) "
            f"→ 可能被 ASR 识别为 \"{c['top_confusable']}\" "
            f"(通用频率:{c['top_confusable_freq']})"
            for i, c in enumerate(rough_candidates, 1)
        )
    else:
        cand_str = "（统计筛选未发现候选词，请从聊天记录中直接发现）"

    # 采样消息
    sample_size = min(150, len(messages))
    sample = random.sample(messages, sample_size) if len(messages) > sample_size else messages
    chat_str = "\n".join(f"- [{m['sender']}] {m['text']}" for m in sample)

    prompt = f"""你是一个 ASR 纠错专家。以下是从用户聊天记录中统计筛选出的候选词，
请判断哪些词在语音识别场景中真正容易被误识别。

## 统计筛选结果
{cand_str}

## 用户聊天记录采样
{chat_str}

## 请完成以下四个任务：

### 任务 1：审核统计结果
对每个候选词判断：是否真的是 ASR 易错词？输出"保留"或"移除"及理由。

### 任务 2：补充遗漏
从聊天记录中找出统计方法遗漏的 ASR 易错词，特别是：
- 专业术语（ASR 通用词典可能未收录）
- 人名、产品名等专有名词

### 任务 3：中英混合词汇识别
从聊天记录中提取用户高频使用的英文词汇和缩写。
这些词在语音输入时，ASR 大概率会转成中文谐音。
对每个英文词列出 2-3 个可能的中文误识别结果。

### 任务 4：添加场景描述
对所有最终保留的词添加一句话场景描述，帮助 LLM 在纠正时判断语境，避免过度纠正。
描述应简洁明了，只说明该词是什么，不要包含使用示例或例句。

## 输出格式（JSON 数组）
[
  {{
    "term": "词",
    "action": "保留/移除/新增",
    "category": "person/company/tech_term/product/other",
    "desc": "一句话场景描述",
    "frequency": 频次,
    "possible_asr_errors": ["错误1", "错误2"],  // 注意：不要包含词条本身，只列出与词条不同的误识别结果
    "source": "statistical/llm_discovered",
    "type": "chinese/english",
    "reason": "判断理由"
  }}
]

请确保输出是合法的 JSON 数组。"""

    logger.info("[阶段四] 调用 LLM 进行精炼...")
    try:
        result = llm.call_json(prompt, max_retries=max_retries)
    except Exception as e:
        logger.warning(f"LLM 精炼失败: {e}，降级使用统计结果")
        return [
            {
                "term": c["term"],
                "category": "unknown",
                "desc": "",
                "frequency": c["user_frequency"],
                "possible_asr_errors": c["confusables"][:3],
                "source": "statistical",
                "type": "chinese",
            }
            for c in rough_candidates
        ]

    if isinstance(result, dict):
        result = result.get("vocab", result.get("results", []))

    refined = []
    for item in result:
        if not isinstance(item, dict):
            continue
        if item.get("action") == "移除":
            continue
        refined.append({
            "term": item.get("term", ""),
            "category": item.get("category", "other"),
            "desc": item.get("desc", ""),
            "frequency": item.get("frequency", 0),
            "possible_asr_errors": item.get("possible_asr_errors", []),
            "source": item.get("source", "unknown"),
            "type": item.get("type", "chinese"),
        })

    logger.info(f"[阶段四] LLM 精炼完成: {len(refined)} 个词条")
    return refined


# ============================================================
# 阶段五：自动验证
# ============================================================

def generate_test_cases(
    vocab: List[dict], messages: List[dict], n: int = 100
) -> List[dict]:
    """用词表反向注入 ASR 错误，生成测试集"""
    term_map = {
        e["term"]: e for e in vocab if e.get("possible_asr_errors")
    }
    if not term_map:
        return []

    cases = []
    shuffled = list(messages)
    random.shuffle(shuffled)

    for msg in shuffled:
        corrupted = msg["text"]
        expected = []
        for term, entry in term_map.items():
            if term in corrupted and entry["possible_asr_errors"]:
                error = random.choice(entry["possible_asr_errors"])
                corrupted = corrupted.replace(term, error, 1)
                expected.append({"error": error, "correct": term})
        if expected:
            cases.append({
                "original": msg["text"],
                "corrupted": corrupted,
                "expected": expected,
            })
        if len(cases) >= n:
            break
    return cases


def validate(
    vocab: List[dict], messages: List[dict], llm: LLMClient
) -> dict:
    """自动验证词表质量"""
    n = CONFIG["validation_sample_size"]
    cases = generate_test_cases(vocab, messages, n=n)

    if not cases:
        logger.info("[阶段五] 无法生成测试用例")
        return {"status": "SKIP", "reason": "无测试数据"}

    logger.info(f"[阶段五] 生成 {len(cases)} 个测试用例，开始验证...")

    # 构建词表 prompt 片段（复用）
    vocab_str = "\n".join(
        f"- {e['term']}（{e.get('desc', '')}）" for e in vocab
    )

    total_expected = sum(len(c["expected"]) for c in cases)
    correct_fixes = 0
    over_corrections = 0
    exact_matches = 0

    for i, tc in enumerate(cases):
        prompt = f"""用户个人词汇表：
{vocab_str}

以下是 ASR 转写的文本，可能存在同音/近音字错误。
请根据用户的个人词汇和上下文，纠正其中的错误。
只修改明确是语音识别错误的词，不要改变原意。
如果没有需要纠正的，原样输出。

ASR 原文：{tc['corrupted']}

请只输出纠正后的文本，不要输出其他任何内容。"""

        try:
            corrected = llm.call(prompt).strip().strip("「」""'\"")
        except Exception as e:
            logger.warning(f"测试 {i + 1} 失败: {e}")
            continue

        # Recall
        for exp in tc["expected"]:
            if exp["correct"] in corrected:
                correct_fixes += 1

        # Exact match
        if corrected.strip() == tc["original"].strip():
            exact_matches += 1

        # Over-correction（简化检测）
        if corrected.strip() != tc["original"].strip():
            orig_words = set(jieba.lcut(tc["original"]))
            corr_words = set(jieba.lcut(corrected))
            expected_set = {e["correct"] for e in tc["expected"]}
            unexpected = corr_words - orig_words - expected_set
            if unexpected:
                over_corrections += 1

        if (i + 1) % 20 == 0:
            logger.info(f"[阶段五] 已验证 {i + 1}/{len(cases)}")

    recall = correct_fixes / total_expected if total_expected else 0
    em_rate = exact_matches / len(cases) if cases else 0
    oc_rate = over_corrections / len(cases) if cases else 0

    metrics = {
        "recall": round(recall, 4),
        "exact_match_rate": round(em_rate, 4),
        "over_correction_rate": round(oc_rate, 4),
        "total_cases": len(cases),
        "total_expected": total_expected,
        "correct_fixes": correct_fixes,
        "exact_matches": exact_matches,
        "over_corrections": over_corrections,
    }

    r_ok = recall >= CONFIG["validation_recall_threshold"]
    o_ok = oc_rate < CONFIG["validation_overcorrection_threshold"]

    if r_ok and o_ok:
        metrics["status"] = "PASS"
    else:
        metrics["status"] = "FAIL"
        issues = []
        if not r_ok:
            issues.append(f"Recall 不足 ({recall:.1%})")
        if not o_ok:
            issues.append(f"过度纠正率过高 ({oc_rate:.1%})")
        metrics["issues"] = issues

    return metrics


# ============================================================
# 主 Pipeline
# ============================================================

def build_pipeline(
    chat_path: str,
    anchor_path: Optional[str],
    output_path: str,
    api_key: str,
    base_url: str,
    model: str,
    validate: bool = False,
    rebuild_cache: bool = False,
    max_retries: int = 3,
    workers: int = None,
    min_freq: int = 3,
    api_format: str = "anthropic",
):
    """执行完整的歧义词表构建 Pipeline"""
    try:
        if not api_key:
            return (False, "请提供 api_key 或设置 OPENAI_API_KEY 环境变量")

        logger.info("=" * 60)
        logger.info("  ASR 个性化中文歧义词表构建")
        logger.info("=" * 60)

        # --- 阶段一 ---
        logger.info("--- 阶段一：数据准备 ---")
        messages = parse_chat(chat_path)
        if not messages:
            logger.error("错误：聊天记录为空")
            return (False, "聊天记录为空")

        anchors = load_anchors(anchor_path)

        cache_path = _default_cache_path()
        cached = None if rebuild_cache else load_cached_index(cache_path)
        if cached:
            general_freq, fuzzy_index = cached
        else:
            general_freq = load_general_freq()
            fuzzy_index = build_fuzzy_index(general_freq)
            save_cached_index(cache_path, general_freq, fuzzy_index)

        llm = LLMClient(api_key=api_key, base_url=base_url, model=model, api_format=api_format)

        # --- 预分词 ---
        batch_tokenize(messages, workers)

        # --- 阶段二 ---
        logger.info("--- 阶段二：数据预清洗 ---")
        original_messages = [{**m} for m in messages]  # 保存原始消息用于比较
        suspicious = rule_pre_analysis(messages, anchors)
        cleaned = llm_data_cleaning(messages, suspicious, anchors, llm, max_retries=max_retries)

        # 清洗后增量重分词
        retokenize_changed(original_messages, cleaned, workers)

        # --- 阶段三 ---
        logger.info("--- 阶段三：统计粗筛 ---")
        rough = statistical_filter(cleaned, general_freq, fuzzy_index, min_freq=min_freq)

        # --- 阶段四 ---
        logger.info("--- 阶段四：LLM 精炼 ---")
        refined = llm_refine(rough, cleaned, llm, max_retries=max_retries)

        # 合并锚点词（未被统计覆盖的）
        existing = {r["term"] for r in refined}
        for anchor in anchors:
            if anchor["term"] not in existing:
                refined.append({
                    "term": anchor["term"],
                    "category": anchor.get("category", "unknown"),
                    "desc": anchor.get("desc", ""),
                    "frequency": 0,
                    "possible_asr_errors": [],
                    "source": "anchor",
                    "type": "chinese",
                })

        logger.info(f"精炼后词表: {len(refined)} 个词条")

        # --- 阶段五 ---
        metrics = {}
        if validate:
            logger.info("--- 阶段五：自动验证 ---")
            metrics = validate(refined, cleaned, llm)
            print(f"\n验证结果:")
            print(f"  Recall:           {metrics.get('recall', 0):.1%}")
            print(f"  Exact Match:      {metrics.get('exact_match_rate', 0):.1%}")
            print(f"  Over-correction:  {metrics.get('over_correction_rate', 0):.1%}")
            print(f"  Status:           {metrics.get('status', 'UNKNOWN')}")
            if metrics.get("issues"):
                for issue in metrics["issues"]:
                    print(f"  ⚠️  {issue}")
        else:
            logger.info("--- 阶段五：跳过验证 ---")
            metrics = {"status": "SKIPPED"}

        # --- 输出 ---
        output = {
            "version": time.strftime("%Y-%m-%d"),
            "build_method": "statistical_filter + llm_refinement",
            "stats": {
                "total_entries": len(refined),
                "chinese_entries": sum(1 for r in refined if r.get("type") != "english"),
                "english_entries": sum(1 for r in refined if r.get("type") == "english"),
                "source_messages": len(messages),
                "validation": {k: v for k, v in metrics.items()} if metrics else {},
            },
            "vocab": refined,
        }

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        logger.info("=" * 60)
        logger.info(f"✅ 词表已保存到: {output_path}")
        logger.info(f"   共 {len(refined)} 个词条")
        logger.info("=" * 60)

        return (True, None)

    except Exception as e:
        logger.error(f"Pipeline 执行失败: {e}")
        return (False, str(e))


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="ASR 个性化中文歧义词表构建",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python build_words.py \\
    --chat data/chat.txt \\
    --anchors data/anchors.json \\
    --output vocab_table.json \\
    --api-key sk-xxx \\
    --base-url https://api.example.com/v1 \\
    --model claude-sonnet-4-20250514

聊天数据格式:
  用户A：你好
  用户B：你好，方案发给我了吗
  用户A：晨旭说下午发
        """,
    )

    parser.add_argument("--chat", required=True, help="聊天记录文件路径")
    parser.add_argument("--anchors", default=None, help="锚点词表 JSON 文件路径")
    parser.add_argument("--output", default="vocab_table.json", help="输出词表路径")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="LLM API Key (或设置 OPENAI_API_KEY 环境变量)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="LLM API Base URL",
    )
    parser.add_argument("--model", default="gpt-4o", help="LLM 模型名称")
    parser.add_argument("--validate", action="store_true", help="执行验证阶段")
    parser.add_argument("--rebuild-cache", action="store_true", help="强制重建 fuzzy 索引缓存")
    parser.add_argument("--max-retries", type=int, default=3, help="LLM 调用最大重试次数（默认 3）")
    parser.add_argument("--workers", "-w", type=int, default=None, help="并行分词进程数（默认自动）")
    parser.add_argument("--min-freq", type=int, default=3, help="最低词频阈值（默认 3）")
    parser.add_argument("--api-format", default="anthropic", choices=["openai", "anthropic"], help="API 格式（默认 anthropic）")

    args = parser.parse_args()

    if not args.api_key:
        logger.error("错误：请提供 --api-key 或设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    build_pipeline(
        chat_path=args.chat,
        anchor_path=args.anchors,
        output_path=args.output,
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        validate=args.validate,
        rebuild_cache=args.rebuild_cache,
        max_retries=args.max_retries,
        workers=args.workers,
        min_freq=args.min_freq,
        api_format=args.api_format,
    )


if __name__ == "__main__":
    main()
