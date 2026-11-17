"""文本分段与长文路由辅助（v2.6 新增）。

chunked_call 支持 10 万字级文档处理：
- 按语义边界分段（段落 → 句子 → 硬切三级降级）
- map-reduce 摘要合并
- 单次分段调用不超过模型上下文窗口

设计：纯标准库，零依赖，离线可用。
"""

import re


def estimate_tokens_simple(text):
    """快速估算 token 数（粗略：1 中文字≈1.5 token，1 英文词≈1.3 token）。"""
    if not text:
        return 0
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    en = len(re.findall(r"[a-zA-Z]+", text))
    other = len(text) - cn - sum(len(w) for w in re.findall(r"[a-zA-Z]+", text))
    return int(cn * 1.5 + en * 1.3 + other * 0.5)


def split_by_paragraphs(text, max_chars=8000):
    """按段落分段，每段不超过 max_chars。

    分段优先级：双换行 → 单换行 → 句号/问号/感叹号 → 硬切。
    """
    if len(text) <= max_chars:
        return [text]

    # 第一级：按双换行分段
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = ""
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(current) + len(p) + 2 <= max_chars:
            current = current + "\n\n" + p if current else p
        else:
            if current:
                chunks.append(current)
            if len(p) <= max_chars:
                current = p
            else:
                # 段落超长，按句子切分
                sentences = re.split(r"(?<=[。！？!?\.])\s*", p)
                current = ""
                for s in sentences:
                    if not s.strip():
                        continue
                    if len(current) + len(s) + 1 <= max_chars:
                        current = current + s if current else s
                    else:
                        if current:
                            chunks.append(current)
                        if len(s) <= max_chars:
                            current = s
                        else:
                            # 句子超长，硬切
                            for i in range(0, len(s), max_chars):
                                chunks.append(s[i:i + max_chars])
                            current = ""
    if current:
        chunks.append(current)
    return chunks


def chunked_call(chunks, task_fn, reduce_fn=None):
    """对文本分块依次调用 task_fn，再用 reduce_fn 合并。

    task_fn(chunk, idx) 返回该分块的处理结果。
    reduce_fn(results) 将多块结果合并为最终结果。
    若 reduce_fn 为 None，默认用 "\n\n".join(results)。

    返回 {"result": str, "chunks": int, "cost": float}。
    """
    results = []
    for idx, chunk in enumerate(chunks):
        result = task_fn(chunk, idx)
        results.append(result)

    if reduce_fn is None:
        final = "\n\n".join(results)
    else:
        final = reduce_fn(results)

    return {"result": final, "chunks": len(chunks)}


def auto_chunk_length(model_ctx, overhead=1000):
    """根据模型上下文窗口自动推荐分段长度。

    留 overhead tokens 给输出 + 系统提示，分段长度取上下文的 70%。
    """
    usable = max(int((model_ctx - overhead) * 0.7), 2000)
    # 按中文字估算（1 字≈1.5 token），留余量
    return int(usable / 1.5)


def map_reduce_summary(chunks, summary_fn, combine_fn=None):
    """map-reduce 摘要合并：

    1. 对每块调用 summary_fn(chunk, idx) 得到分块摘要
    2. 用 combine_fn(summaries) 合并所有分块摘要
    3. combine_fn 为 None 时直接拼接

    返回 {"summary": str, "chunk_summaries": list, "total_chunks": int}。
    """
    summaries = []
    for idx, chunk in enumerate(chunks):
        s = summary_fn(chunk, idx)
        summaries.append(s)

    if combine_fn:
        combined = combine_fn(summaries)
    else:
        combined = "\n\n".join(summaries)

    return {"summary": combined, "chunk_summaries": summaries, "total_chunks": len(chunks)}
