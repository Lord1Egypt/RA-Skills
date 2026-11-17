#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试共享 mock 库（机制化：mock 一次写对，所有测试复用——消除「每个测试内嵌
fake 各写各错」的修补模式）。
适用边界（审计备忘）：NCBIMock 的 esummary 响应不含 result.uids——仅适用于
pubmed_title_reverse_lookup 流；pubmed_pmid_exists 流（依赖 uids 检查）请扩展。用法：

    from _mocks import NCBIMock
    with unittest.mock.patch("urllib.request.urlopen",
                             side_effect=NCBIMock(esearch_hits={...},
                                                  summaries={...})):
        ...

约定：mock 按 URL 特征分发（esearch/esummary/其他），各分支独立返回，
**不共享解析逻辑**（解析错一个分支不影响其他分支的可见性——测试失败信息
必须能定位到分支）。"""
import glob
import json
import os
import urllib.parse


class _Ctx:
    """urlopen 上下文模拟（read/enter/exit）。"""

    def __init__(self, payload):
        self._payload = payload

    def read(self, n=-1):
        return json.dumps(self._payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class NCBIMock:
    """NCBI E-utilities 双跳 mock（esearch → esummary）。

    esearch_hits: {nwords:int → idlist:list[str]}——按查询词数（[Title] 计数）
                  分发命中（用于词数递减重试的测试）。
    default_ids:  无词数匹配时的默认命中。
    summaries:    {pmid → esummary 文档}；未登记的 PMID 自动生成最小文档。
    """

    def __init__(self, esearch_hits=None, default_ids=None, summaries=None):
        self.esearch_hits = esearch_hits or {}
        self.default_ids = default_ids or []
        self.summaries = summaries or {}
        self.calls = []  # [(kind, term_or_ids)]——断言调用序列用

    def __call__(self, req, timeout=None):
        u = req.full_url
        if "esearch" in u:
            term = urllib.parse.unquote(u.split("term=", 1)[1]) if "term=" in u else ""
            nwords = term.count("[Title]")
            self.calls.append(("esearch", term))
            ids = self.esearch_hits.get(nwords, self.default_ids)
            return _Ctx({"esearchresult": {"idlist": ids}})
        # esummary
        ids_str = u.split("id=", 1)[1].split("&")[0] if "id=" in u else ""
        ids = ids_str.split(",") if ids_str else []
        self.calls.append(("esummary", ",".join(ids)))
        result = {}
        for pid in ids:
            doc = dict(self.summaries.get(pid) or {})
            doc.setdefault("title", f"Placeholder title for {pid}")
            doc.setdefault("source", "J Test")
            doc.setdefault("pubdate", "2020 Jan")
            result[pid] = doc
        return _Ctx({"result": result, "esearchresult": {"idlist": ids}})


def fresh_engine_state(vr_module):
    """引擎全局可变状态隔离（测试间污染防护——机制化，勿在单个测试里手工清）。
    清空：断路器/NCBI/S2 限速器/网络降级标记。"""
    vr_module._CB.clear()
    vr_module._NCBI_LAST[0] = 0.0
    vr_module._S2_LAST[0] = 0.0
    vr_module._NET_STATE["degraded"] = False
    vr_module._NET_STATE.get("fail_hosts", {}).clear()
    vr_module._NET_STATE.get("ok_hosts", set()).clear()


def engine_full_text():
    """v6.0.0 模块化布局适配：引擎源码文本=壳 verify_refs.py + 全部 ch_*.py 拼接。

    「源码含 X 文本」类断言统一走本 helper（单文件时代直接读 verify_refs.py，
    模块化后文本分布于壳与各层模块——拼接读取保持断言意图不变）。"""
    import glob as _glob
    _base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
    parts = [open(os.path.join(_base, "verify_refs.py"), encoding="utf-8").read()]
    for p in sorted(_glob.glob(os.path.join(_base, "ch_*.py"))):
        parts.append(open(p, encoding="utf-8").read())
    return "\n".join(parts)
