"""长文分块一键链的任务模板与合并器（v2.9.0 新增）。

把 v2.6 的 text_splitter 从「手动接力」补齐为「分块 → 并行 → 合并」完整链。

两类内置任务模板：
- summarize（摘要）：块摘要 → 再汇总（map-reduce），输出连贯总摘要
- translate（翻译）：块翻译按序拼接 + 术语一致性检查（术语表抽取 + 替换建议）

设计：纯标准库，零依赖，离线可用。LLM 调用由调用方通过 task_fn 注入，
本模块只负责编排与合并策略（符合 #9 自研优先，API 可插拔）。
"""

import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import text_splitter

TEMPLATES = ("summarize", "translate")

PROMPTS = {
    "summarize": "请用中文总结以下文本的核心要点，保留关键数据与结论：\n\n{chunk}",
    "translate": "请将以下文本翻译为流畅的中文，保持术语一致、语序自然：\n\n{chunk}",
    "combine_summary": "以下是某长文档的分段摘要，请综合成一份连贯完整的总摘要，去除重复：\n\n{parts}",
    "translate_term_check": (
        "请检查以下翻译的术语一致性：列出同一原文术语被译成不同译法的地方，"
        "给出统一建议。若无问题输出「术语一致」。\n\n{text}"
    ),
}


def make_task_fn(task_type, call_fn):
    """把用户提供的 call_fn(prompt)->str 包装成分块任务函数。"""
    template = PROMPTS.get(task_type, PROMPTS["summarize"])

    def task_fn(chunk, idx):
        return call_fn(template.format(chunk=chunk))

    return task_fn


def merge_summary(chunk_summaries, call_fn=None):
    """摘要合并：块摘要再汇总。

    call_fn 存在时用 combine_summary 提示词让模型汇总（更连贯）；
    否则本地拼接去重（离线兜底）。
    """
    if not chunk_summaries:
        return ""
    if call_fn:
        parts = "\n\n".join("[%d] %s" % (i + 1, s) for i, s in enumerate(chunk_summaries))
        try:
            return call_fn(PROMPTS["combine_summary"].format(parts=parts))
        except Exception:
            pass  # 汇总调用失败 → 本地兜底
    # 本地兜底：按行去重拼接
    seen = set()
    out = []
    for s in chunk_summaries:
        for line in str(s).splitlines():
            key = line.strip()
            if key and key not in seen:
                seen.add(key)
                out.append(line.strip())
    return "\n".join(out)


def _extract_terms(text, min_len=2, max_len=12):
    """本地粗抽中文/英文术语（高频名词短语），用于一致性检查兜底。"""
    # 英文词或中文 2-12 字短语（简化：按标点切分后取候选）
    en = re.findall(r"\b[A-Za-z][A-Za-z0-9_-]{1,20}\b", text)
    zh = re.findall(r"[\u4e00-\u9fff]{2,%d}" % max_len, text)
    freq = {}
    for t in en + zh:
        if len(t) < min_len:
            continue
        freq[t] = freq.get(t, 0) + 1
    # 出现≥2次的视为候选术语
    return sorted([t for t, n in freq.items() if n >= 2], key=lambda t: -freq[t])[:30]


def merge_translate(chunk_translations, call_fn=None, check_terms=True):
    """翻译合并：按序拼接 + 术语一致性检查。

    返回 dict:
      result      按序拼接的译文
      term_check  术语检查结论（字符串）
      terms       抽取的候选术语列表
    """
    valid = [str(t) if t else "" for t in chunk_translations]
    result = "\n\n".join(valid)
    terms = _extract_terms(result) if check_terms else []
    term_check = "术语检查已跳过"
    if check_terms:
        if len(terms) < 2:
            term_check = "术语一致（候选术语不足，未发现冲突）"
        elif call_fn:
            try:
                term_check = call_fn(PROMPTS["translate_term_check"].format(text=result))
            except Exception:
                term_check = "术语检查调用失败，候选术语：%s" % "、".join(terms[:10])
        else:
            term_check = "本地候选术语：%s（建议人工复核）" % "、".join(terms[:10])
    return {
        "result": result,
        "term_check": term_check,
        "terms": terms,
    }


def longchain(text, task_type, call_fn, model_ctx=32000, max_workers=4,
              chunk_chars=None, validate=True):
    """长文一键链：分块 → 并行 → 合并。

    task_type: summarize / translate
    call_fn(prompt)->str：由调用方注入的模型调用函数（LLM 可插拔）
    model_ctx: 目标模型上下文窗口（如 32000），用于自动分段长度
    max_workers: 并发数（由 hardware.profile() 决定）
    返回 dict：完整结果 + 各环节元信息
    """
    if task_type not in TEMPLATES:
        raise ValueError("不支持的长文任务类型: %s（支持 %s）" % (task_type, "/".join(TEMPLATES)))
    if not text or not str(text).strip():
        raise ValueError("输入文本为空")

    if chunk_chars is None:
        chunk_chars = text_splitter.auto_chunk_length(model_ctx)
    chunk_chars = max(500, int(chunk_chars))
    chunks = text_splitter.split_by_paragraphs(str(text), max_chars=chunk_chars)
    task_fn = make_task_fn(task_type, call_fn)

    # summarize 的 reduce 需要二次调用模型，故这里先取各块结果再单独合并
    parallel = text_splitter.chunked_call_parallel(chunks, task_fn, max_workers=max_workers)
    values = parallel["chunk_values"]

    if task_type == "summarize":
        final = merge_summary(values, call_fn=call_fn)
        extra = {}
    else:
        merged = merge_translate(values, call_fn=call_fn, check_terms=True)
        final = merged["result"]
        extra = {"term_check": merged["term_check"], "terms": merged["terms"]}

    out = {
        "task_type": task_type,
        "result": final,
        "chunks": parallel["chunks"],
        "workers": parallel["workers"],
        "chunk_chars": chunk_chars,
        "errors": parallel["errors"],
        "input_chars": len(str(text)),
    }
    out.update(extra)
    return out


def render_longchain(result):
    """人类可读输出。"""
    lines = []
    lines.append("📄 长文一键链完成（%s）" % result["task_type"])
    lines.append("  输入 %d 字 → 分 %d 块，并发 %d" % (
        result["input_chars"], result["chunks"], result["workers"]))
    if result.get("errors"):
        lines.append("  ⚠️  %d 块处理出错：%s" % (len(result["errors"]), result["errors"][0][:60]))
    if result.get("term_check"):
        lines.append("  术语一致性：%s" % result["term_check"])
    lines.append("")
    lines.append(result["result"])
    return "\n".join(lines)
