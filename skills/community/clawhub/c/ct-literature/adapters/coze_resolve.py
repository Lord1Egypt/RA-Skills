#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coze_resolve.py — 用 Coze ct-search 端点把「间接下载链接」解码为「可直接下载的文件链接」

ct-literature 工作台专用轻量工具：读取一份 .merged.json（或任意含 works[] 的 JSON），
对其中每一篇文献收集可下载标识（open_access_url 优先 → preprint.url → doi），
批量 POST 到 ct-search.coze.site/run 的 publisher_pdf_batch 统一契约（解码+A→B），
由 Coze 端把间接链接/DOI 解码为可直接下载的真实直链（pdf_url / pdf_s3_url），或 pdf_failed。

设计对齐 ct-base 的「解码上 Coze、下载在本地」：
  * 统一契约：Coze 对每条标识执行 A(解码+直下探测验证)→B(浏览器+S3)，只返回已验证真实直链；
  * 本地不做二次解析（避免越权/反爬），只下载 Coze 返回的真实直链；
  * --download 时把能拿到的直链保存到 <out_dir>/pdfs/，其余标记 manual。

复用 scripts/pdf_download.py 的 PdfDownloader（其 _call_coze_unified /
_headers / _resolve_token / _query_origin 已封装同一端点契约），不重复造轮子。

用法：
  python coze_resolve.py --in .merged.json                # 只解码，输出直链 JSON
  python coze_resolve.py --in .merged.json --download     # 解码并下载到 pdfs/
  python coze_resolve.py --in .merged.json --out r.json   # 结果写文件而非 stdout

「不下载」标记：--download 时默认会读 <out_dir>/.selection.json（工作台结果卡逐篇
勾选的「不下载」名单，格式 {"skip":[{doi|title|id}…]}），命中的篇目**照旧解码、但不落盘**，
结果里标记 status=skipped 并计入 stats.skipped。只想全下时传 --no-skip-file。

并行流水线（2026-09-19，默认 --pipeline）：
  旧实现是三段串行——「探完所有本地直链 → 送完所有 Coze 批 → 才开始下载」。本地已确认
  可直接下载的链接因此要白等 Coze 走完才落盘，而 Coze 又要白等本地探针跑完才发出。
  现在三件事同时在跑：本地探针逐条回报、命中即入下载队列；Coze 各批与探针并行提交，
  每批返回一条就入队一条；下载工人池从队列里取活按域名限速落盘。结果（items / stats /
  downloaded）与串行版逐字段等价，只是墙上时间不再叠加。--no-pipeline 可退回串行做对照。

安全：仅只读输入 JSON；联网仅发给既有的 ct-search 端点；token 从 ct-registry/ct-advisor
内嵌公开 blob 复用（见 pdf_download._resolve_token），绝不打印 token 明文（ct-base §5）。
"""
import argparse
import concurrent.futures
import json
import os
import queue as _queue
import re
import sys
import threading
import urllib.parse

# 进度事件是 NDJSON：流水线里多个线程同时上报，必须整行原子写，否则两条事件会互相
# 咬进同一行、调用方解析失败（表现为「进度莫名丢了一块」）。
_EMIT_LOCK = threading.Lock()

# 技能根注入：使 `from adapters.pdf_download import …` 在 __main__ 直跑与包导入下均可解析
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _collect_identifiers(works):
    """为每篇 work 生成 (idx, key, doi, label, direct_candidate)。
    key 取 open_access_url 优先、否则 preprint.url、否则 doi —— 与 PdfDownloader.run 一致。
    """
    out = []
    for i, w in enumerate(works):
        oa = (w.get("open_access_url") or "").strip()
        pre = ((w.get("preprint") or {}).get("url") or "").strip()
        doi = (w.get("doi") or "").strip()
        # label: 简短展示用
        label = (w.get("title") or w.get("doi") or "untitled")[:80]
        # 需发 Coze 解码的：有 doi 或 OA 间接链接但没有可靠本地直链的篇目
        # （预印本直链通常可直接下，也一并过一遍 Coze，统一拿 Coze 判定）
        key = oa or pre or doi
        if not key:
            continue
        out.append({"idx": i, "key": key, "doi": doi, "label": label,
                    "oa": oa, "preprint_url": pre})
    return out


_PDF_HINT_RE = re.compile(
    r"(\.pdf($|[?#])|/pdf/|/pdf($|[?#])|getfile\.php|/download($|[?#])|filetype=pdf)", re.I)

# 预印本直链的**确定性 URL 形态**：正文 PDF 就是 .../content/<doi>.full.pdf。
# 这类链接不再做网络校验，原因有二：
#   ① bioRxiv/medRxiv 对机器人 UA 一律 403/429，批量探测 100 条必然被限速，
#      校验结果不可信（会把能直下的误判成不能）；
#   ② 路径形态本身就是契约（浏览器打开即是 PDF），无需猜。
# 代价：这类链接标记为 preprint_direct（"按规则认定"），与经过实测校验的 local_direct 区分开。
_TRUSTED_DIRECT_RE = re.compile(
    r"^https?://(www\.)?(biorxiv|medrxiv)\.org/content/.+\.full\.pdf($|[?#])", re.I)


def _is_trusted_direct(key):
    return bool(key) and bool(_TRUSTED_DIRECT_RE.match(key))


def _looks_direct_file(key):
    """key 本身是否『已经是文件直链』（无需解码）。

    只在这里放【明显是文件】的形态，宁可漏判（送去 Coze）也不误判：
    以 .pdf 结尾 / 路径含 /pdf/ / 已知的 getfile 下载端点。
    """
    if not key or not key.lower().startswith(("http://", "https://")):
        return False
    return bool(_PDF_HINT_RE.search(key))


# --------------------------------------------------------------------------- #
# 「不下载」标记
#
# 结果卡允许逐篇标记「不下载」，标记存在 <out_dir>/.selection.json（由工作台
# /api/selection 读写）。解码照跑，但下载阶段跳过被标记的篇目。
#
# 匹配口径与 server.py 的 _norm_skip 完全对齐（doi/标题小写归一、去尾点），
# 且**任一键命中即算同一篇**：只用 doi 会漏掉没有 doi 的记录（预印本/指南常见），
# 只用标题又怕标点差异。两处口径若分叉，就会出现「界面标了、下载照下」。
# --------------------------------------------------------------------------- #
_SKIP_FIELDS = ("doi", "title", "id")


def _norm_token(text):
    return " ".join(str(text or "").split()).strip().lower().rstrip(".")


def _skip_keys(entry):
    """一条标记 → 它声明的所有可比对键。"""
    if isinstance(entry, str):
        entry = {"doi": entry}
    if not isinstance(entry, dict):
        return set()
    keys = set()
    for f in _SKIP_FIELDS:
        v = entry.get(f)
        if v in (None, ""):
            continue
        v = _norm_token(v) if f in ("doi", "title") else str(v).strip().lower()
        if v:
            keys.add(v)
    return keys


def _load_skip_keys(path):
    """读 .selection.json（或任何 {skip:[…]}）→ 归一化后的键集合。

    读不出来时返回空集合（= 什么都不跳），绝不因为标记文件损坏就中断解码：
    多下一两篇是可接受的，整轮解码失败不是。
    """
    if not path or not os.path.isfile(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:  # noqa: BLE001
        return set()
    entries = data.get("skip") if isinstance(data, dict) else data
    if isinstance(entries, str):        # 单个裸 DOI 的简写形态（不拆成单字符）
        entries = [entries]
    if not isinstance(entries, (list, tuple)):
        return set()
    keys = set()
    for e in entries:
        keys |= _skip_keys(e)
    return keys


def _item_skip_keys(row):
    """下载条目 → 它的可比对键（与 _skip_keys 同口径）。"""
    keys = set()
    for f in _SKIP_FIELDS:
        v = row.get(f)
        if v in (None, ""):
            continue
        v = _norm_token(v) if f in ("doi", "title") else str(v).strip().lower()
        if v:
            keys.add(v)
    # Coze 条目的 key 可能是 doi 本身或 OA 直链；doi 形态的也拿来比对
    k = _norm_token(row.get("key"))
    if k and not k.startswith(("http://", "https://")):
        keys.add(k)
    return keys


def _verify_direct(urls, emit, workers=6, timeout=15, on_result=None):
    """并发探测一批『疑似直链』，返回 {url: True/False}。

    探测必须用**浏览器请求头 + Range 取前 1KB**，不能用裸 HEAD：
    实测 bioRxiv / medRxiv 对机器人 UA 直接 403/429，但浏览器头返回 206 application/pdf —
    用 HEAD 会把「其实能直下」的预印本误判成不可下载，全部丢给端点白等。
    反之 PMC 的 .../pdf/... 实际返回 text/html（跳转页），这里会被正确判为「非直链」。

    判定为可真下：HTTP 200/206 且 Content-Type 含 pdf（或 octet-stream 且声明长度 >0）。
    其余（403/404/429/超时/返回 HTML）→ False，交回端点处理 —— 宁可多花端点时间，
    也不虚报「可直下」让用户点开是 403。

    on_result(url, ok)：每探出一条就立刻回调一次。流水线靠它做到「探到即入下载队列」，
    不必等整批探完（旧实现用 ex.map，必须等全部返回）。回调抛异常只丢这一条回调，
    不影响探测本身与其它回调。
    """
    import urllib.request

    from adapters.pdf_download import _browser_headers

    ok = {}

    def _one(u):
        try:
            h = dict(_browser_headers(u))
            h["Range"] = "bytes=0-1023"
            req = urllib.request.Request(u, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                ctype = (r.headers.get("Content-Type") or "").lower()
                clen = r.headers.get("Content-Length")
                if "pdf" in ctype:
                    return u, True
                if ("octet-stream" in ctype or "binary" in ctype) and clen and int(clen) > 0:
                    return u, True
                return u, False
        except Exception:  # noqa: BLE001
            return u, False

    if not urls:
        return ok
    emit("stage", id="prefilter", total=len(urls),
         msg="本地预筛：校验 %d 个疑似直链（浏览器头 + Range，并发 %d）…" % (len(urls), workers))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        futs = [ex.submit(_one, u) for u in urls]
        for fut in concurrent.futures.as_completed(futs):
            try:
                u, good = fut.result()
            except Exception:  # noqa: BLE001
                continue
            ok[u] = good
            if on_result is not None:
                try:
                    on_result(u, good)
                except Exception:  # noqa: BLE001 — 回调故障不该拖垮探测
                    pass
    return ok


def _send_batches(dl, chunks, emit, concurrency, gate=None):
    """把各批发往 ct-search 端点，返回与 chunks 等长的结果列表。

    每个元素是该批的 projects（list[dict]）或 None（该批失败）。
    并发度 concurrency>1 时各批同时进行：批次之间互相独立，单篇仍只发送一次
    （并发只改变「批次何时发出」，不改变「发送几次」）。
    并发是必要的——实测单批（50 篇）解码需数分钟，4 批串行会让总时长乘以批数。

    gate（threading.Semaphore）：跨调用共享的端点并发闸门。流水线里「明显非文件」与
    「探针否掉」两波是分开提交的，各自限流会让同时在跑的批数翻倍；共用一把闸门
    才能把「同一时刻打到端点的批数」压回 concurrency。
    """
    total = len(chunks)
    results = [None] * total
    done = [0]

    def _one(i, chunk):
        try:
            if gate is None:
                return i, dl._call_coze_unified(chunk)
            with gate:
                return i, dl._call_coze_unified(chunk)
        except Exception as e:  # noqa: BLE001
            dl._log("[coze_resolve] 第 %d/%d 批异常: %s" % (i + 1, total, e))
            return i, None

    workers = max(1, min(int(concurrency or 1), total))

    if workers == 1:
        for i, chunk in enumerate(chunks):
            emit("stage", id="coze", batch=i + 1, batches=total,
                 msg="提交 ct-search.coze.site 解码 第 %d/%d 批（%d 篇）…"
                     % (i + 1, total, len(chunk)))
            idx, part = _one(i, chunk)
            results[idx] = part
            done[0] += 1
            emit("stage", id="coze", batch=done[0], batches=total,
                 msg="已完成 %d/%d 批" % (done[0], total))
        return results

    emit("stage", id="coze", batches=total, concurrency=workers,
         msg="并发提交 %d 批（每批 ≤%d 篇，同时进行 %d 路）…"
             % (total, len(chunks[0]), workers))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_one, i, chunk) for i, chunk in enumerate(chunks)]
        for fut in concurrent.futures.as_completed(futs):
            idx, part = fut.result()
            results[idx] = part
            done[0] += 1
            emit("stage", id="coze", batch=done[0], batches=total,
                 msg="已完成 %d/%d 批（并发解码中）" % (done[0], total))
    return results


# --------------------------------------------------------------------------- #
# 并行流水线（2026-09-19）：本地探针 / Coze 解码 / 逐篇下载 三件事同时跑
#
# 串行版的三段是「探完所有本地直链 → 送完所有 Coze 批 → 才开始下载」，于是
#   * 本地已经确认可直下的链接，要白等 Coze 整轮跑完才落盘；
#   * Coze 又要白等本地探针扫完才发出。
# 这里改成谁先有结果谁就先落盘，三段之间没有等待关系：
#   * 本地探针逐条回报，命中直链的那一刻就入下载队列；
#   * 「明显不是文件」的大头在探针跑的同时就已提交端点；探针否掉的那批探完补送；
#   * 各批 Coze 返回一条就入队一条；下载工人池取活按域名限速落盘。
# 结果（items / stats / downloaded）与串行版等价，只是墙上时间不再叠加。
# --------------------------------------------------------------------------- #
def _row_of(t, url="", status="direct", source="coze", error="", cloudflare=False):
    """组装一行结果。字段名与串行版逐字段一致（界面与既有测试都按这套字段读）。"""
    return {
        "idx": t["idx"],
        "title": t["label"],
        "doi": t["doi"] or "",
        "oa": t.get("oa") or "",
        "preprint_url": t.get("preprint_url") or "",
        "key": t["key"],
        "direct_url": url or "",
        "source": source,
        "cloudflare": bool(cloudflare),
        "status": status,
        "error": error,
    }


def _stats_from_rows(items):
    """从最终行反推 stats。

    串行版边跑边加加减减；并发下「哪条先到」不确定，那样算容易出现
    「下载失败先把 coze_resolved 扣了、随后整批判为端点不可用」之类的错账。
    行是唯一真相，从行反推必然自洽。
    """
    st = {"coze_resolved": 0, "coze_failed": 0, "coze_unavailable": 0,
          "manual": 0, "local_direct": 0, "preprint_direct": 0}
    for r in items:
        s = r.get("status")
        if s in ("direct", "skipped"):
            # skipped = 直链确实解出来了，只是按用户意愿没落盘（不扣 resolved）
            st["coze_resolved"] += 1
        elif s == "failed":
            st["coze_failed"] += 1
        elif s == "unavailable":
            st["coze_unavailable"] += 1
        if r.get("source") == "local_direct":
            st["local_direct"] += 1
        elif r.get("source") == "preprint_direct":
            st["preprint_direct"] += 1
    n_skip = sum(1 for r in items if r.get("status") == "skipped")
    if n_skip:
        st["skipped"] = n_skip
    return st


def _dl_delay_for(url, dl):
    """逐篇下载前的礼貌间隔（与 PdfDownloader._download_one 同口径）。

    预印本服务对机器人限速最严（403/429），必须沿用 min_delay；S3/CDN 几乎无限制。
    """
    low = (url or "").lower()
    host = urllib.parse.urlsplit(url or "").netloc.lower()
    if "biorxiv.org" in low or "medrxiv.org" in low:
        return host, float(getattr(dl, "min_delay", 3.0) or 3.0)
    if "amazonaws" in host or "cloudfront" in host or host.startswith("s3"):
        return host, 0.1
    return host, 1.5


def _run_pipeline(targets, keys, dl, args, emit, out_dir):
    """并行流水线主体。返回 (items, dl_stats, downloaded)，字段语义同串行版。"""
    import random as _rand

    from adapters.pdf_download import MAX_BATCH_ITEMS, _extract_doi_from_url

    work_total = len(targets)
    lock = threading.Lock()
    rows = {}                      # idx -> 最终行
    downloaded = {}                # key -> 本地路径
    done_idx = set()               # 已经定性完结的目标（每条只完结一次）
    work_done = [0]
    dl_done = [0]                  # 已完成（含失败）的下载数
    dl_queued = [0]                # 已入队（= 已解出直链）的下载数

    dl_on = bool(args.download)

    # 「不下载」标记：只在开跑前读一次（运行中新标的下一轮生效，与串行版一致）
    skip_keys = set()
    if args.use_skip_file and dl_on:
        skip_path = args.skip_file or os.path.join(out_dir, ".selection.json")
        skip_keys = _load_skip_keys(skip_path)
        if skip_keys:
            emit("stage", id="download", done=0, total=0,
                 msg="已读入「不下载」标记 %d 条（%s）" % (len(skip_keys), os.path.basename(skip_path)))

    # ── 目标索引：同一 key/doi 可能对应多篇，必须全部一起定性 ────────────────
    exact, normed = {}, {}

    def _index(store, token, t):
        lst = store.setdefault(token, [])
        if all(x["idx"] != t["idx"] for x in lst):
            lst.append(t)

    for t in targets:
        for c in (t["key"], t["doi"], _extract_doi_from_url(t["key"])):
            if c:
                _index(exact, c, t)
                _index(normed, _norm_token(c), t)

    def _targets_of(k):
        return exact.get(k) or normed.get(_norm_token(k)) or []

    def _targets_of_rec(rec):
        """把 Coze 一条记录映射回目标：key / doi / key 里抽出的 DOI 三选一。"""
        for c in (rec.get("key"), rec.get("doi")):
            if c and c in exact:
                return exact[c]
        for c in (rec.get("key"), rec.get("doi")):
            d = _extract_doi_from_url(c) if c else ""
            if d and d in exact:
                return exact[d]
        for c in (rec.get("key"), rec.get("doi")):
            n = _norm_token(c)
            if n and n in normed:
                return normed[n]
        return []

    # ── 进度：以「目标」为工作单元（解码 + 必要的下载 = 一个单元）────────────
    def _mark_done(idx):
        with lock:
            if idx in done_idx:
                return
            done_idx.add(idx)
            work_done[0] += 1
            n = work_done[0]
        emit("stage", id="pipeline", work_done=n, work_total=work_total)

    # ── 下载工人池 ─────────────────────────────────────────────────────────
    DLQ = _queue.Queue()
    _STOP = object()

    def _dl_worker():
        while True:
            job = DLQ.get()
            try:
                if job is _STOP:
                    return
                idx, row, url = job
                host, delay = _dl_delay_for(url, dl)
                try:
                    # 逐域名限速器（线程安全）：同域名保距串行，跨域名并行。
                    # 并发下载若不走限速器，同域名的请求节奏会被乘上工人数，
                    # 直接把 biorxiv / 出版商站点打到 429。
                    dl._limiter.acquire(host, delay + _rand.uniform(0, 0.5))
                except Exception:  # noqa: BLE001
                    pass
                try:
                    path = dl._download_direct(url, row.get("key") or row.get("doi") or "")
                except Exception:  # noqa: BLE001
                    path = None
                if path:
                    with lock:
                        downloaded[row["key"]] = path
                else:
                    row["status"] = "failed"          # 解出直链但本地没下下来 → 降级 failed
                    row["error"] = (row.get("error") or "") + "；本地下载失败"
                with lock:
                    dl_done[0] += 1
                    dn, tq = dl_done[0], dl_queued[0]
                emit("stage", id="download", parallel=True, done=dn, total=max(tq, dn),
                     msg="下载%s %d/%d：%s" % ("成功" if path else "失败", dn, max(tq, dn),
                                              (row.get("title") or "")[:60]))
                _mark_done(idx)
            finally:
                DLQ.task_done()

    _dl_workers = [threading.Thread(target=_dl_worker, daemon=True, name="ct-dl-%d" % i)
                   for i in range(max(1, min(int(args.dl_concurrency or 1), 8)))]
    for _t in _dl_workers:
        _t.start()

    # ── 定性一条目标：能下载就入队，否则就此完结 ────────────────────────────
    def _settle(t, row, url):
        skipped = False
        if url and skip_keys and (_item_skip_keys(row) & skip_keys):
            row["status"] = "skipped"
            row["error"] = row.get("error") or "结果卡标记为「不下载」，本轮跳过"
            skipped = True
        with lock:
            rows[t["idx"]] = row
        if skipped or not (dl_on and url):
            _mark_done(t["idx"])
            return
        with lock:
            dl_queued[0] += 1
            tq, dn = dl_queued[0], dl_done[0]
        emit("stage", id="download", parallel=True, done=dn, total=max(tq, dn),
             msg="解出直链，立即下载：%s" % (row.get("title") or "")[:60])
        DLQ.put((t["idx"], row, url))

    def _settle_direct(t, url, via, cloudflare=False):
        _settle(t, _row_of(t, url=url, status="direct", source=via,
                           cloudflare=cloudflare), url)

    # ── Coze 一波：拆批 → 并发提交 → 返回一条处理一条 ───────────────────────
    gate = threading.Semaphore(max(1, int(args.concurrency or 1)))
    failed_batches = []            # 传送失败的批（要等所有批返回才敢定性）
    any_nonmanual = [False]        # 有批次返回过非 manual 记录 → 端点不算「不可用」

    def _apply_rec(rec):
        for t in _targets_of_rec(rec):
            url = rec.get("pdf_s3_url") or rec.get("pdf_url")
            if url and rec.get("status") == "ok":
                _settle_direct(t, url, rec.get("via") or rec.get("source") or "coze",
                               bool(rec.get("cloudflare")))
            else:
                _settle(t, _row_of(t, status="failed",
                                   source=rec.get("via") or rec.get("source") or "coze_failed",
                                   error=rec.get("error") or "Coze 未返回可下载直链",
                                   cloudflare=bool(rec.get("cloudflare"))), "")

    def _coze_wave(wave_keys, tag):
        wave_keys = list(dict.fromkeys([k for k in wave_keys if k]))
        if not wave_keys:
            return
        chunks = [wave_keys[i:i + MAX_BATCH_ITEMS]
                  for i in range(0, len(wave_keys), MAX_BATCH_ITEMS)]
        emit("stage", id="coze", total=len(wave_keys), batches=len(chunks),
             msg="提交 ct-search.coze.site 解码 %d 篇（%s，%d 批，与本地下载并行）…"
                 % (len(wave_keys), tag, len(chunks)))
        for chunk, part in zip(chunks, _send_batches(dl, chunks, emit, args.concurrency, gate)):
            if part is None:
                with lock:
                    failed_batches.append(list(chunk))
                continue
            for rec in part:
                if rec.get("status") != "manual":
                    any_nonmanual[0] = True
                _apply_rec(rec)

    # ── 分流：明显是文件直链的走本地探针，其余立刻送端点 ────────────────────
    cand = [t["key"] for t in targets if _looks_direct_file(t["key"])]
    cand_set = set(cand)
    trusted = {u for u in cand if _is_trusted_direct(u)}
    to_probe = [u for u in cand if u not in trusted]
    wave1 = [k for k in dict.fromkeys(keys) if k not in cand_set]
    probe_failed = []

    emit("stage", id="prefilter", total=len(cand),
         msg="本地预筛：%d 个疑似直链（规则认定 %d + 待校验 %d）；其余 %d 篇直接提交端点，"
             "两者并行" % (len(cand), len(trusted), len(to_probe), len(wave1)))

    producers = [threading.Thread(target=_coze_wave, args=(wave1, "主批"), daemon=True,
                                  name="ct-coze-1")]
    producers[0].start()

    # 规则认定的预印本直链：无需探测，直接入队
    for u in trusted:
        for t in _targets_of(u):
            _settle_direct(t, u, "preprint_direct")

    if to_probe:
        def _on_probe(u, good):
            if good:
                for t in _targets_of(u):
                    _settle_direct(t, u, "local_direct")
            else:
                with lock:
                    probe_failed.append(u)      # 探针否掉 → 补送端点
        _verify_direct(to_probe, emit, workers=args.probe_workers, on_result=_on_probe)

    # 探针否掉的那批：此刻才知道要送，独立成第二波（不与主批互相等待）
    if probe_failed:
        _p2 = threading.Thread(target=_coze_wave, args=(probe_failed, "补送"), daemon=True,
                               name="ct-coze-2")
        _p2.start()
        producers.append(_p2)
    for _p in producers:
        _p.join()

    # ── 批次传送失败的篇目：所有批返回后才能定性 ────────────────────────────
    # 与串行版同口径：全部批失败且没有任何非 manual 记录 → 判「端点不可用」（前端据此
    # 提示「端点无响应」而不是「这批文献没有 OA」）；否则只把失败批降级为 failed。
    send_keys = list(dict.fromkeys(wave1 + probe_failed))
    if send_keys and failed_batches and not any_nonmanual[0]:
        for k in send_keys:
            for t in _targets_of(k):
                with lock:
                    rows[t["idx"]] = _row_of(
                        t, status="unavailable", source="unavailable",
                        error="Coze 端点不可用（连接异常或超时）")
        emit("stage", id="assemble", total=work_total,
             msg="端点未返回任何结果；%d 篇转本地标记（预筛已命中的直链不受影响）"
                 % len(send_keys))
    else:
        for chunk in failed_batches:
            for k in chunk:
                for t in _targets_of(k):
                    if t["idx"] not in rows:
                        _settle(t, _row_of(t, status="failed", source="coze_failed",
                                           error="该批 coze 传送失败，降级本地兜底"), "")

    # ── 收尾：漏网目标（端点没返回对应记录）按「无直链」结案，然后等下载池排干 ──
    for t in targets:
        if t["idx"] not in rows:
            _settle(t, _row_of(t, status="failed", source="coze_failed",
                               error="Coze 未返回可下载直链"), "")
    for idx in (t["idx"] for t in targets):
        _mark_done(idx)
    DLQ.join()                          # 队列已排干（生产者全部 join 过，不会再入队）
    for _t in _dl_workers:
        DLQ.put(_STOP)
    for _t in _dl_workers:
        _t.join(timeout=5)

    items = [rows[t["idx"]] for t in targets]
    return items, _stats_from_rows(items), downloaded


def _finalize(items, dl_stats, downloaded, args, emit):
    """统一的收尾：组装结果 JSON、写文件 / 打 stdout。串行与流水线共用。"""
    result = {
        "ok": True,
        "total": len(items),
        "stats": dl_stats,
        "downloaded": downloaded,
        "items": items,
        "endpoint": "ct-search.coze.site/stream_run:publisher_pdf_batch(unified)",
    }
    if dl_stats.get("skipped"):
        result["skip_note"] = ("其中 %d 篇按「不下载」标记跳过（链接照旧解码，未落盘）"
                               % dl_stats["skipped"])
    # 当全部为 pdf_failed 且 error 含"B 路径未启用"时，附加说明 note
    failed_notes = [r.get("error", "") for r in items if r.get("status") == "failed"]
    if failed_notes and all("B 路径" in n or "未启用" in n for n in failed_notes if n):
        result["note"] = "Coze 端 B 路径（浏览器下载）未启用；仅靠 A 路径（OA/PMC/直链）无法覆盖付费墙文献。可在 coze 端设置 CT_ENABLE_BROWSER_PDF_DOWNLOAD=1 启用。"
    text = json.dumps(result, ensure_ascii=False, indent=2)
    emit("stage", id="done", total=len(items), stats=dl_stats,
         msg="解码完成：直链 %d（本地实测 %d + 预印本规则 %d）/ 无直链 %d / 端点不可用 %d%s"
             % (dl_stats.get("coze_resolved", 0), dl_stats.get("local_direct", 0),
                dl_stats.get("preprint_direct", 0),
                dl_stats.get("coze_failed", 0), dl_stats.get("coze_unavailable", 0),
                ("/ 按标记跳过 %d" % dl_stats["skipped"]) if dl_stats.get("skipped") else ""))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        # 写文件模式：摘要走 stderr，stdout 保持干净（调用方按文件取结果）
        sys.stderr.write("[coze_resolve] -> %s (%d works)\n" % (args.out, len(items)))
        sys.stderr.flush()
    else:
        print(text)
    return 0


def main():
    ap = argparse.ArgumentParser(description="Coze resolve: decode indirect links -> direct file links")
    ap.add_argument("--in", dest="inp", required=True, help=".merged.json (or any JSON with works[])")
    ap.add_argument("--out", default="", help="write JSON result to this file (default stdout)")
    ap.add_argument("--download", action="store_true",
                    help="also download resolvable direct links into <dir>/pdfs/")
    ap.add_argument("--dir", dest="out_dir", default="",
                    help="output dir for pdfs/ when --download (default: same dir as --in)")
    ap.add_argument("--skip-coze", action="store_true",
                    help="local-only decode (no Coze); mainly for debugging")
    # 进度上报（2026-09-19）：Coze 解码耗时较长（几十秒~3 分钟），工作台需要实时进度。
    # stdout 始终只留给最终 JSON；进度一律走 stderr，逐行 flush，便于调用方边收边推。
    ap.add_argument("--progress", choices=["off", "text", "json"], default="off",
                    help="progress channel: off (default) | text | json (NDJSON on stderr)")
    # 拆批并发度（>50 篇时生效）：串行会让总时长 ≈ 批数 × 单批时长，
    # 并发可把总时长压到接近「最慢的那一批」。1 = 旧的串行行为。
    ap.add_argument("--concurrency", type=int, default=3,
                    help="max batches sent to the endpoint at the same time (default 3; 1 = serial)")
    # 本地预筛：key 本身已是文件直链（.pdf 等）且 HEAD 校验可直接下载的，
    # 本地即判定为直链、不再送端点——端点单篇约 19s，实测检索结果里 2/3 属于此类。
    ap.add_argument("--no-direct-prefilter", dest="direct_prefilter", action="store_false",
                    help="send every target to the endpoint, even already-direct .pdf links")
    ap.set_defaults(direct_prefilter=True)
    # 「不下载」标记（工作台结果卡逐篇勾选）：解码照旧跑（链接清单要完整），
    # 但被标记的篇目在下载阶段直接跳过、不落盘。
    ap.add_argument("--skip-file", default="",
                    help="JSON with {skip:[{doi|title|id}…]} — papers to EXCLUDE from --download "
                         "(default: <out_dir>/.selection.json when it exists)")
    ap.add_argument("--no-skip-file", dest="use_skip_file", action="store_false",
                    help="ignore any skip file, download everything resolvable")
    ap.set_defaults(use_skip_file=True)
    # 并行流水线（默认开）：本地探针 / Coze 解码 / 逐篇下载 三件事同时跑，谁先有结果
    # 谁先落盘。——no-pipeline 退回「探完 → 送完 → 才下载」的串行三段，仅供对照/排障。
    ap.add_argument("--no-pipeline", dest="pipeline", action="store_false",
                    help="sequential mode: probe all local links, then send all Coze batches, "
                         "then start downloading (default: pipelined, all three concurrent)")
    ap.set_defaults(pipeline=True)
    ap.add_argument("--dl-concurrency", type=int, default=3,
                    help="parallel download workers in pipeline mode (default 3); per-host rate "
                         "limiting still applies, so same-host downloads stay spaced")
    ap.add_argument("--probe-workers", type=int, default=6,
                    help="parallel workers for the local direct-link probe (default 6)")
    args = ap.parse_args()

    _prog_mode = args.progress

    def emit(ev, **fields):
        """向 stderr 推一条已 flush 的进度事件（json=NDJSON 结构化；text=纯文本行）。

        流水线里探针 / Coze / 下载三类线程会同时上报，整行必须原子写：
        交错的行会让调用方 JSON 解析失败、进度凭空丢一块。
        """
        if _prog_mode == "off":
            return
        try:
            if _prog_mode == "json":
                line = json.dumps({"ev": ev, **fields}, ensure_ascii=False) + "\n"
            else:
                line = "%s\n" % (fields.get("msg") or fields.get("label") or ev)
            with _EMIT_LOCK:
                sys.stderr.write(line)
                sys.stderr.flush()
        except Exception:  # noqa: BLE001 — 进度通道故障绝不影响主流程
            pass

    def on_log(msg):
        emit("log", msg=str(msg))

    if not os.path.isfile(args.inp):
        sys.exit("[coze_resolve] missing input: %s" % args.inp)

    with open(args.inp, "r", encoding="utf-8") as f:
        data = json.load(f)
    works = data.get("works") if isinstance(data, dict) else data
    if not isinstance(works, list) or not works:
        sys.exit("[coze_resolve] no works[] found in %s" % args.inp)
    emit("stage", id="load", works=len(works),
         msg="已读取 %s（%d 篇）" % (os.path.basename(args.inp), len(works)))

    from adapters.pdf_download import PdfDownloader  # noqa: PLC0415  (deferred import keeps CLI fast)
    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.inp))
    # 下载后自动回写 Excel 与题录（用户 2026-09-21）：把 PDF 绝对路径写回
    # lit_report.xlsx「PDF 本地路径」列 与 references.bib / .ris / .md。
    # 此前这里没传 xlsx_out / citations_out_dir，导致 Web「解码+批量下载」后两个产物都没路径。
    _xlsx_out = os.path.join(out_dir, "lit_report.xlsx")
    _merged_json = os.path.join(out_dir, ".merged.json")
    _citations_dir = out_dir
    dl = PdfDownloader(
        out_dir=os.path.join(out_dir, "pdfs"),
        progress=on_log,
        merged_json=_merged_json if os.path.isfile(_merged_json) else None,
        xlsx_out=_xlsx_out,
        citations_out_dir=_citations_dir,
        citation_style=getattr(args, "citation_style", None) or "apa",
        lang=getattr(args, "lang", None) or "auto",
    )

    # 1) 收集标识
    targets = _collect_identifiers(works)
    keys = [t["key"] for t in targets]
    emit("stage", id="identify", targets=len(targets),
         msg="收集到 %d 个待解码标识（DOI / OA / 预印本）" % len(keys))
    if not keys:
        emit("stage", id="done", total=0, msg="无可用标识，结束")
        print(json.dumps({"ok": True, "total": 0, "items": [],
                          "note": "works 中无可用 DOI / OA / 预印本链接"}, ensure_ascii=False))
        return 0

    # 1.2) 并行流水线（默认）：探针 / 解码 / 下载 同时跑，本地一到直链就落盘。
    #      串行三段（1.5→4）保留在下面，供 --no-pipeline 做对照与排障。
    if args.pipeline and not args.skip_coze:
        items, dl_stats, downloaded = _run_pipeline(targets, keys, dl, args, emit, out_dir)
        return _finalize(items, dl_stats, downloaded, args, emit)

    # 1.5) 本地预筛（默认开启）：key 本身已是文件直链的，本地校验能否直接下载；
    #      能直下的不再送端点。端点单篇解码约 19s，实测检索结果约 2/3 属于此类，
    #      预筛后送端点的篇数大幅下降，整体耗时随之下降。
    prefiltered = {}          # key -> url（本地已认定可直接下载）
    trusted_keys = set()      # 走规则认定（未做网络校验）的那部分
    if not args.skip_coze and args.direct_prefilter:
        cand = [t["key"] for t in targets if _looks_direct_file(t["key"])]
        trusted_keys = {u for u in cand if _is_trusted_direct(u)}
        to_probe = [u for u in cand if u not in trusted_keys]
        prefiltered = {u: u for u in trusted_keys}
        if to_probe:
            verdict = _verify_direct(to_probe, emit)
            prefiltered.update({u: u for u, good in verdict.items() if good})
        if cand:
            emit("stage", id="prefilter", total=len(cand), direct=len(prefiltered),
                 trusted=len(trusted_keys), probed=len(to_probe),
                 msg="本地预筛：%d 个疑似直链中 %d 个可直接下载（预印本规则认定 %d + 实测校验 %d），"
                     "跳过端点；其余 %d 个交给端点"
                     % (len(cand), len(prefiltered), len(trusted_keys),
                        len(prefiltered) - len(trusted_keys), len(cand) - len(prefiltered)))
        else:
            emit("stage", id="prefilter", total=0,
                 msg="本地预筛：无『已是文件直链』的条目")

    # 送端点的只保留未预筛命中的条目
    send_keys = [k for k in keys if k not in prefiltered]

    # 2) Coze 单次传送（统一契约：解码+A→B，返回真实直链或 pdf_failed）
    #    单批上限 MAX_BATCH_ITEMS（与 coze 端一致），超过需拆批并行传送
    from adapters.pdf_download import MAX_BATCH_ITEMS
    projects = None
    if not args.skip_coze:
        if not send_keys:
            projects = []
        elif len(send_keys) <= MAX_BATCH_ITEMS:
            emit("stage", id="coze", total=len(send_keys), batch=1,
                 batches=1, msg="提交 ct-search.coze.site 解码 %d 篇（单批，可能需 1-3 分钟）" % len(send_keys))
            # 单批即可
            try:
                projects = dl._call_coze_unified(send_keys)
            except Exception as e:  # noqa: BLE001
                projects = None
                dl._log("[coze_resolve] Coze 调用异常: %s" % e)
        else:
            # 拆批传送（与 PdfDownloader.run 拆批逻辑一致）
            chunks = [send_keys[i:i + MAX_BATCH_ITEMS]
                      for i in range(0, len(send_keys), MAX_BATCH_ITEMS)]
            dl._log(f"[coze_resolve] {len(send_keys)} 篇超过单批上限 {MAX_BATCH_ITEMS}，"
                    f"自动拆为 {len(chunks)} 批（并发 {args.concurrency}）")
            results = _send_batches(dl, chunks, emit, args.concurrency)
            collected = []
            all_ok = True
            for ci, (chunk, part) in enumerate(zip(chunks, results), 1):
                if part is None:
                    all_ok = False
                    # 该批降级本地兜底（与 pdf_download 一致）
                    from adapters.pdf_download import _extract_doi_from_url
                    dl._log(f"[coze_resolve] 第 {ci}/{len(chunks)} 批未返回结果，降级本地兜底")
                    for k in chunk:
                        collected.append({"key": k, "doi": _extract_doi_from_url(k) or "",
                                          "pdf_url": None, "pdf_s3_url": None,
                                          "status": "manual",
                                          "error": "该批 coze 传送失败，降级本地兜底"})
                else:
                    collected.extend(part)
            # 全部批次都传送失败 → 判为「端点不可用」而非「无直链」，
            # 前端才能给出正确提示（不再把"连不上端点"误报成"这批文献没有 OA"）
            _any_real = any(p.get("status") != "manual" for p in collected)
            projects = collected if (all_ok or _any_real) else None
    # 区分「coze 返回了结果（含 ok / pdf_failed）」vs「coze 真的不可用（异常/无响应）」
    # 判定必须放在兜底填充【之前】，否则 projects 已非 None，该分支永远不成立
    # （原实现的 `coze_unavailable = (projects is None)` 恒为 False → unavailable 统计恒 0、
    #   端点不可达被误报为 pdf_failed。2026-09-19 修正。）
    coze_unavailable = (projects is None) and bool(send_keys)
    # 本地预筛命中的条目：本地已确认可直接下载，直接并入结果（不再依赖端点）
    by_key = {t["key"]: t for t in targets}
    pre_projects = [{"key": k, "doi": (by_key.get(k) or {}).get("doi") or "",
                     "pdf_url": prefiltered[k], "pdf_s3_url": None,
                     "status": "ok",
                     "via": "preprint_direct" if k in trusted_keys else "local_direct"}
                    for k in prefiltered]
    if coze_unavailable:
        # Coze 不可用 → 本地兜底（仅标记，不下载）。预筛已命中的那部分仍然有效。
        emit("stage", id="assemble", total=len(targets), resolved=len(pre_projects),
             unavailable=True,
             msg="端点未返回结果；本地预筛已得直链 %d 篇，其余 %d 篇转本地兜底标记"
                 % (len(pre_projects), len(send_keys)))
        projects = [{"key": k, "doi": (by_key.get(k) or {}).get("doi") or "",
                     "pdf_url": None, "pdf_s3_url": None,
                     "status": "manual", "error": "Coze 不可用"} for k in send_keys]
        projects = projects + pre_projects
    else:
        if projects is None:
            projects = []
        _resolved_n = sum(1 for p in projects
                          if p.get("status") == "ok"
                          and (p.get("pdf_s3_url") or p.get("pdf_url")))
        emit("stage", id="assemble", total=len(targets),
             resolved=_resolved_n + len(pre_projects),
             msg="端点返回 %d 条记录（其中直链 %d）；叠加本地预筛直链 %d 篇，正在组装结果…"
                 % (len(projects), _resolved_n, len(pre_projects)))
        projects = projects + pre_projects

    # key -> 记录（coze 可能返回原始 key 或从 URL 提取的 DOI，需双向匹配）
    rec_map: Dict[str, Dict] = {}
    for p in projects:
        k = p.get("key") or p.get("doi") or ""
        rec_map[k] = p
        # 同时以 doi 为键索引（coze 可能把 OA URL 解析为裸 DOI 返回）
        doi = p.get("doi") or ""
        if doi and doi != k:
            rec_map[doi] = p

    # 3) 组装每篇结果
    from adapters.pdf_download import _extract_doi_from_url
    items = []
    dl_stats = {"coze_resolved": 0, "coze_failed": 0, "coze_unavailable": 0,
                "manual": 0, "local_direct": 0, "preprint_direct": 0}
    if coze_unavailable:
        dl_stats["coze_unavailable"] = len(send_keys)

    for t in targets:
        # 先按原始 key 匹配；若不命中，尝试从 key(URL) 提取 DOI 后按 DOI 匹配
        rec = rec_map.get(t["key"], {})
        if not rec:
            extracted_doi = _extract_doi_from_url(t["key"])
            if extracted_doi:
                rec = rec_map.get(extracted_doi, {})
        url = rec.get("pdf_s3_url") or rec.get("pdf_url")
        has_url = bool(url) and rec.get("status") == "ok"

        if coze_unavailable and not has_url:
            # coze 真的不可用（异常/无响应）；本地预筛命中的条目不走这里
            row = {
                "idx": t["idx"],
                "title": t["label"],
                "doi": t["doi"] or "",
                "oa": t.get("oa") or "",
                "preprint_url": t.get("preprint_url") or "",
                "key": t["key"],
                "direct_url": "",
                "source": "unavailable",
                "cloudflare": False,
                "status": "unavailable",
                "error": "Coze 端点不可用（连接异常或超时）",
            }
        elif has_url:
            # coze 返回了真实直链
            row = {
                "idx": t["idx"],
                "title": t["label"],
                "doi": t["doi"] or "",
                "oa": t.get("oa") or "",
                "preprint_url": t.get("preprint_url") or "",
                "key": t["key"],
                "direct_url": url or "",
                "source": rec.get("via") or rec.get("source") or "coze",
                "cloudflare": bool(rec.get("cloudflare")),
                "status": "direct",
                "error": rec.get("error") or "",
            }
            dl_stats["coze_resolved"] += 1
            if rec.get("via") == "local_direct":
                dl_stats["local_direct"] += 1
            elif rec.get("via") == "preprint_direct":
                dl_stats["preprint_direct"] += 1
        else:
            # coze 返回了 pdf_failed（A/B 路径都失败）
            row = {
                "idx": t["idx"],
                "title": t["label"],
                "doi": t["doi"] or "",
                "oa": t.get("oa") or "",
                "preprint_url": t.get("preprint_url") or "",
                "key": t["key"],
                "direct_url": "",
                "source": rec.get("via") or rec.get("source") or "coze_failed",
                "cloudflare": bool(rec.get("cloudflare")),
                "status": "failed",
                "error": rec.get("error") or "Coze 未返回可下载直链",
            }
            dl_stats["coze_failed"] += 1
        items.append(row)

    # 4) 可选下载
    downloaded = {}
    # 「不下载」标记：只影响下载阶段——解码照旧跑，.coze_links.json 保持完整
    # （用户可能只是这一轮不想下，链接清单不该缺篇）。
    skip_keys = set()
    if args.use_skip_file and args.download and not args.skip_coze:
        skip_path = args.skip_file or os.path.join(out_dir, ".selection.json")
        skip_keys = _load_skip_keys(skip_path)
        if skip_keys:
            emit("stage", id="download", done=0, total=0,
                 msg="已读入「不下载」标记 %d 条（%s）" % (len(skip_keys), os.path.basename(skip_path)))
    if args.download and not args.skip_coze:
        _dl_targets = [r for r in items if r["status"] == "direct" and r["direct_url"]]
        if skip_keys:
            _kept, _n_skip = [], 0
            for r in _dl_targets:
                if _item_skip_keys(r) & skip_keys:
                    r["status"] = "skipped"          # 已解码、按用户意愿不下
                    r["error"] = r.get("error") or "结果卡标记为「不下载」，本轮跳过"
                    _n_skip += 1
                else:
                    _kept.append(r)
            if _n_skip:
                # 注意：不扣 coze_resolved —— 直链确实解出来了，只是没下。
                # 「解码直链数」与「实际落盘数」是两个数，界面分开展示。
                dl_stats["skipped"] = dl_stats.get("skipped", 0) + _n_skip
                emit("stage", id="download", done=0, total=len(_kept),
                     msg="按「不下载」标记跳过 %d 篇，实际下载 %d 篇" % (_n_skip, len(_kept)))
            _dl_targets = _kept
        emit("stage", id="download", done=0, total=len(_dl_targets),
             msg="下载直链 %d 个到 pdfs/（逐篇限速）…" % len(_dl_targets))
        for _i, row in enumerate(_dl_targets, 1):
            emit("stage", id="download", done=_i, total=len(_dl_targets),
                 msg="下载 %d/%d：%s" % (_i, len(_dl_targets), (row.get("title") or "")[:60]))
            try:
                path = dl._download_direct_with_delay(row["direct_url"], row["key"] or row["doi"], delay=0.5)
            except Exception:  # noqa: BLE001
                path = None
            if path:
                downloaded[row["key"]] = path
            else:
                # 下载失败 → 降级为 failed
                row["status"] = "failed"
                row["error"] = row.get("error", "") + "；本地下载失败"
                dl_stats["coze_resolved"] = max(0, dl_stats["coze_resolved"] - 1)
                dl_stats["coze_failed"] = dl_stats.get("coze_failed", 0) + 1

    return _finalize(items, dl_stats, downloaded, args, emit)


if __name__ == "__main__":
    sys.exit(main())
