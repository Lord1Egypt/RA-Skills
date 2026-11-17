#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""薄客户端统一 coze 策略调用（纯薄客户端：无本地兜底）。

供 pdf_download / normalize / dedupe_engine 共用，集中封装出站信封
（ct-base coze_io_contract）与 SSE 解析，避免三处重复实现漂移。

设计约束（2026-10-26 源码保护上移）：
  - 被调用的「策略逻辑」全部在 ct-search coze 端执行
    （lit_route / lit_preprint_check / lit_dedup 节点）；本模块只负责
    「把信号送上去、把结果取回来」。
  - 失败一律返回 None（不本地兜底）——coze 不可用 = 该功能不可用。

出站信封与各节点返回结构见 ct-registry/adapters/coze/src/graphs/nodes/lit_*.py。
"""
import json
import urllib.request

from adapters.pdf_download import (
    CT_SEARCH_ENDPOINT,
    _headers,
    _query_origin,
    _skill_version,
    _resolve_locale,
    _resolve_user_language,
    _parse_coze_stream,
)


def call_coze_strategy(source, payload_obj, log_fn=print, timeout=180):
    """统一 coze 策略调用。

    Args:
        source:       coze 端 source 分支名
                      （lit_route / lit_preprint_check / lit_dedup）
        payload_obj:  任意 JSON 可序列化对象（结构由对应 coze 节点约定）
        log_fn:       日志函数（默认 print；PdfDownloader 传 self._log）
        timeout:      请求超时（秒）
    Returns:
        coze 节点的完整最终结果 dict（含 projects + 统计字段），失败返回 None。
    """
    payload = {
        "source": source,
        "keyword": json.dumps(payload_obj, ensure_ascii=False),
        "mode": "search",
        "query_origin": _query_origin(),
        # ct-base coze_io_contract §1.2：技能版本号 = 顶层信封字段
        "skill_version": _skill_version(),
        # ct-base coze_io_contract §1.1：locale = 界面/输出语言（顶层信封）
        "locale": _resolve_locale(),
        # ct-base coze_io_contract §1.1：user_language 承载位 = 请求 params
        "params": {"user_language": _resolve_user_language()},
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        CT_SEARCH_ENDPOINT, data=body, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = _parse_coze_stream(r, log_fn, return_full=True)
    except Exception as e:  # noqa: BLE001
        log_fn(f"[coze:{source}] 调用失败: {type(e).__name__}: {e}")
        return None
    if final is None:
        log_fn(f"[coze:{source}] 未解析到结果（可能 rejected / 执行失败）")
        return None
    # 节点显式返回 error（如未部署 / UNSUPPORTED_SOURCE）→ 视为不可用，交调用方判 skip
    if final.get("error"):
        log_fn(f"[coze:{source}] 节点返回错误: {final.get('error')}")
        return None
    return final
