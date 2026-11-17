#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 本地文档记忆、分块检索与老格式原样转发（改进 A + E-local，2026-09-23）

背景（来自 Ct-Advisor_连续提问诊断报告）：
  - 飞书后台显示，用户 A 曾把同一份 ~3.2 万字「梳理文档」请求在 1 分钟内连发 3 次
    （original_question 逐字相等），每次本地都把整篇 32k 文本重贴、重发云端 → 巨大的
    token / 时间浪费，也是「重复提交」的根因之一。
  - 技能当前无文档记忆：每次调用都是无状态，大文档无法一次入库、后续只传引用。

设计目标（治本，不依赖 Coze 端改动）：
  - 大文档在**本地**按内容哈希入库、分块、关键词检索；
  - 真正外发给 Coze 时，只携带「指令头 + 与问题相关的片段」，而非整篇 32k；
  - Coze 端**零改动**即可受益（片段已内联进 original_question，属核心契约字段，老/新 Coze 都认）；
  - 新 Coze 若要原生读取结构化上下文，可用可选字段 doc_context（契约见
    ``adapters/coze/src/doc/payload.py``，**单一真源**）。

老格式（.doc/.xls/.ppt）通道（2026-09-23 新增，:func:`build_file_payload`）：
  - 老格式是 OLE2 二进制，本地无 Office/LibreOffice 时解不了；
  - 因此**原样转发文件字节**（``mode=file`` + ``file_b64``/``file_name``），
    由 Coze 端 ``doc.office_reader`` 用纯标准库解码为**带格式 Markdown**；
  - 这解释了为什么「老格式兼容」必须落在 Coze 端：本地只做搬运，不做降级解析。

已下线（2026-09-23）：早期设计的正文压缩变体 ``zip="zlib"`` + ``text_b64``。
  实测对 OOXML 再压缩收益很小且不稳定（0.9%~24.5%，媒体型文档常 <1%），无法把超限
  文件压进限内，收益不足以承担两端复杂度。**本模块不再产出该字段**；Coze 端若收到
  老本地发来的该形态，会显式提示「请升级技能」，不会静默当成无文档（见 payload.py）。

兼容性（与现有契约一致）：
  - 所有新增内容均留在本地文件系统（config/doc_store/），不新增任何外发字段；
  - 任何异常一律回退为「原文不变」/「空载荷」，绝不阻断主流程（与 context_stitch 同策略）。

依赖：stdlib-only（json / hashlib / re / os / time / base64）。
"""

import base64
import hashlib
import json
import os
import re
import sys
import time

# §16.9 适配层：Coze 文档上传出站逻辑（urllib）已下沉到 adapters/coze_upload.py，
# 本模块仅保留本地缓存 / 准入逻辑，不再含任何 urllib 出站调用。
from adapters import coze_upload
from adapters.coze_upload import UploadFailedError
from adapters.coze_token_embedded import get_token as _get_coze_token

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _store_root() -> str:
    """文档存储根目录。测试可经环境变量 CT_ADVISOR_DATA_ROOT 覆盖。"""
    return os.environ.get("CT_ADVISOR_DATA_ROOT") or os.path.join(ROOT, "config", "doc_store")


def _idx_path() -> str:
    return os.path.join(_store_root(), "index.json")


def _docs_dir() -> str:
    return os.path.join(_store_root(), "docs")


def _norm_text(text: str) -> str:
    """归一化文本：去首尾空白、折叠连续空白，用于哈希与检索。"""
    return re.sub(r"\s+", " ", (text or "").strip())


def hash_text(text: str) -> str:
    """内容哈希（sha256 前 16 位），作为 doc_id 与去重键。"""
    return "doc_" + hashlib.sha256(_norm_text(text).encode("utf-8")).hexdigest()[:16]


def hash_bytes(data: bytes, salt: str = "") -> str:
    """字节内容哈希（sha256 前 16 位）→ doc_id。同码同 id，跨端一致。"""
    h = hashlib.sha256()
    h.update((salt or "").encode("utf-8"))
    h.update(data or b"")
    return "doc_" + h.hexdigest()[:16]


# ---------------------------------------------------------------------------
# 分块：按段落聚合为 ~CHUNK_CHARS 的窗口，带 OVERLAP 重叠，避免硬切断语义
# ---------------------------------------------------------------------------
CHUNK_CHARS = 600
OVERLAP = 100


def _chunk_text(text: str) -> list:
    """把长文本切成有重叠的语义窗口。

    策略：先按换行/空行断段落，再把段落顺序装入窗口（窗口满则新开，
    跨段落保留 OVERLAP 字符重叠）。纯单段长文按标点切分兜底。
    """
    raw = (text or "").strip()
    if not raw:
        return []
    # 段落优先
    paras = [p for p in re.split(r"\n\s*\n|\n", raw) if p.strip()]
    if not paras:
        paras = [raw]
    chunks = []
    buf = ""
    for p in paras:
        if len(buf) + len(p) <= CHUNK_CHARS:
            buf = (buf + "\n" + p).strip() if buf else p
        else:
            if buf:
                chunks.append(buf)
            # 单段超长：按标点切
            if len(p) > CHUNK_CHARS:
                for piece in re.split(r"(?<=[。；;.!?！？])", p):
                    piece = piece.strip()
                    if not piece:
                        continue
                    if len(buf) + len(piece) <= CHUNK_CHARS:
                        buf = (buf + piece).strip() if buf else piece
                    else:
                        if buf:
                            chunks.append(buf)
                        buf = piece
            else:
                buf = p
    if buf:
        chunks.append(buf)
    # 重叠窗口（在相邻块间插入重叠，提升跨块命中）
    if len(chunks) <= 1:
        return chunks
    overlapped = []
    for i, c in enumerate(chunks):
        if i > 0 and len(c) > OVERLAP:
            c = c[:OVERLAP] + "\n" + c  # 头接上一点重叠
        overlapped.append(c)
    return overlapped


# ---------------------------------------------------------------------------
# 入库 / 检索
# ---------------------------------------------------------------------------

def _load_index() -> dict:
    try:
        with open(_idx_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _save_index(idx: dict) -> None:
    os.makedirs(_store_root(), exist_ok=True)
    with open(_idx_path(), "w", encoding="utf-8") as fh:
        json.dump(idx, fh, ensure_ascii=False, indent=2)


def ingest(text: str) -> str:
    """把一段文本入库（按内容哈希去重）。返回 doc_id。

    已存在则直接返回旧 id（零重复写入）；异常回退为 hash_text 计算的 id（不写入也无害）。
    """
    try:
        doc_id = hash_text(text)
        idx = _load_index()
        if doc_id in idx:
            return doc_id
        chunks = _chunk_text(text)
        os.makedirs(_docs_dir(), exist_ok=True)
        with open(os.path.join(_docs_dir(), doc_id + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"doc_id": doc_id, "chunks": chunks}, fh, ensure_ascii=False)
        idx[doc_id] = {
            "size": len(text),
            "chunks": len(chunks),
            "created_at": time.time(),
        }
        _save_index(idx)
        return doc_id
    except Exception:  # noqa: BLE001  任何异常不阻断主流程
        return hash_text(text)


def _tokenize(text: str) -> list:
    """极简分词：ASCII 词 + CJK 单字（用于重叠计分，不引入第三方依赖）。"""
    toks = re.findall(r"[A-Za-z0-9]+", text.lower())
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    return toks + cjk


def retrieve(doc_id: str, query: str, top_k: int = 5) -> list:
    """从已入库文档中按「查询词在块中的命中」检索 top_k 片段。

    计分：查询 token 在块中出现的次数之和（带长度归一，避免长块天然占优）。
    异常或缺失 → 返回空列表（调用方据此退化为不压缩）。
    """
    try:
        with open(os.path.join(_docs_dir(), doc_id + ".json"), encoding="utf-8") as fh:
            data = json.load(fh)
        chunks = data.get("chunks") or []
        if not chunks:
            return []
        q_tokens = _tokenize(query)
        if not q_tokens:
            return chunks[:top_k]
        scored = []
        for c in chunks:
            c_tokens = _tokenize(c)
            cnt = sum(c_tokens.count(t) for t in set(q_tokens))
            score = cnt / max(1, len(c_tokens) ** 0.5)
            if cnt > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]
    except Exception:  # noqa: BLE001
        return []


# ---------------------------------------------------------------------------
# 对外：把「超大 original_question」压缩为「指令头 + 相关片段」
# ---------------------------------------------------------------------------
HEAD_CHARS = 700          # 保留问题/指令头部（通常含真实意图）
THRESHOLD = 6000          # 超过此长度才视为「大文档」，否则原样返回


def compact_large_question(original_question: str, threshold: int = THRESHOLD) -> tuple:
    """压缩超长问题。

    返回 (new_question, doc_id)：
      - 长度 <= threshold → (原文, "")（不压缩）；
      - 长度 > threshold → 头部保留，体部分哈希入库并按头部检索相关片段内联，
        返回 (压缩后问题, doc_id)；doc_id 为空串表示未压缩/失败。
    异常 → (原文, "")（绝不阻断）。
    """
    try:
        oq = original_question or ""
        if len(oq) <= threshold:
            return oq, ""
        head = oq[:HEAD_CHARS]
        body = oq[HEAD_CHARS:]
        doc_id = ingest(body)
        chunks = retrieve(doc_id, head, top_k=5)
        if not chunks:
            return oq, ""  # 检索失败则不压缩，原文照发
        joined = "\n\n---\n\n".join(chunks)
        new_q = (
            head
            + f"\n\n[文档已本地入库，doc_id={doc_id}；以下为与问题最相关的片段，"
            f"完整文档不再重复发送]\n\n"
            + joined
        )
        return new_q, doc_id
    except Exception:  # noqa: BLE001
        return original_question or "", ""


# ---------------------------------------------------------------------------
# 对外（2026-09-23 Coze 大文档管线）：构造结构化 doc_context 载荷
# ---------------------------------------------------------------------------
# 与 compact_large_question 的分工（两者并存，兼容老/新 Coze）：
#   - compact_large_question：把**问题文本**压小（内联片段）→ 保证**老 Coze**（未部署新代码）
#     也能拿到自包含的小问题，不会被 32k 拖垮；
#   - build_doc_payload    ：把**完整文档**结构化交给**新 Coze**自行分块检索
#     （证据更准、可引用「文档 §N」、可跨轮复用 doc_id）；
#   - build_file_payload   ：本地**解不了的老格式**（.doc/.xls/.ppt）原样转发字节，
#     由 Coze 端解码（见文件头说明）。
MAX_FULL_SEND_CHARS = 120_000   # 正文超过此长度才退化为「本地粗选分块」模式
PRESELECT_TOP_K = 30            # 退化模式下本地粗选块数（新 Coze 仍会二次精排）
PAYLOAD_SCHEMA_VERSION = 1


def split_instruction(text: str, max_len: int = 300) -> str:
    """从「指令 + 文档」混合文本中提取指令行（**不修改正文**，仅作检索提示）。

    判定规则（保守，宁可返回空串也不误判）：
      - 取首个非空行；
      - 单行输入 → 无法区分指令与正文 → 返回 ""（由 Coze 用问题原文兜底）；
      - 首行长度占比过大（> 全文 1/4）→ 更像正文开头 → 返回 "";
      - 否则认定为指令行。
    """
    raw = (text or "").strip()
    if not raw:
        return ""
    lines = [l.strip() for l in raw.split("\n")]
    if len([l for l in lines if l]) < 2:
        return ""
    first = next((l for l in lines if l), "")
    if not first or len(first) > max_len:
        return ""
    if len(raw) < 4 * len(first):
        return ""
    return first


def build_doc_payload(original_question: str, threshold: int = THRESHOLD) -> tuple:
    """把超大 original_question 构造为发给 Coze 的结构化 doc_context 载荷。

    返回 ``(payload_json, doc_id)``；非大文档或失败 → ``("", "")``（绝不阻断主流程）。

    载荷契约见 adapters/coze/src/doc/payload.py（**单一真源**）：
        {"v":1,"doc_id":...,"instruction":...,"mode":"full"|"chunks",
         "text": ... | "chunks": [...],
         "total_chars": n, "source":"local_doc_memory"}

    注：正文压缩变体（``zip``/``text_b64``）已于 2026-09-23 下线，本函数不再产出。
    """
    try:
        oq = original_question or ""
        if len(oq) <= threshold:
            return "", ""
        doc_id = ingest(oq)                      # 全文入库（含指令行，保证不丢内容）
        instruction = split_instruction(oq)
        payload = {
            "v": PAYLOAD_SCHEMA_VERSION,
            "doc_id": doc_id,
            "instruction": instruction,
            "total_chars": len(oq),
            "source": "local_doc_memory",
        }
        if len(oq) <= MAX_FULL_SEND_CHARS:
            # 常规大文档（≤12 万字符）：全文交给 Coze 自行分块检索（证据最准）
            payload["mode"] = "full"
            payload["text"] = oq
        else:
            # 超大文档：本地先粗选 top-30 块控体积（Coze 端仍会二次精排）
            chunks = retrieve(doc_id, instruction or oq, top_k=PRESELECT_TOP_K)
            if not chunks:
                return "", ""
            payload["mode"] = "chunks"
            payload["chunks"] = chunks
        return json.dumps(payload, ensure_ascii=False), doc_id
    except Exception:  # noqa: BLE001
        return "", ""


# ---------------------------------------------------------------------------
# 对外（2026-09-23）：老格式（.doc/.xls/.ppt）原样转发 → Coze 端解码
# ---------------------------------------------------------------------------
# 为什么必须走这条路：
#   ``.doc/.xls/.ppt`` 是 OLE2 复合二进制，解码需要 Office / LibreOffice / win32com，
#   本地不一定具备；而 Coze 端已内置**纯标准库**解码器（adapters/coze/src/doc/
#   legacy_doc.py / legacy_xls.py / legacy_ppt.py → office_reader.py）。
#   所以本地只做搬运：把原始字节 base64 后交给 ``mode=file``。
#
# 体量边界（两端同一套账）：
#   - base64 膨胀 4/3；Coze 端 ``MAX_FILE_B64_CHARS = 5_000_000`` 字符。
#   - 故原始文件上限取 3_750_000 字节（→ base64 恰 5_000_000 字符）。
#     超限**不转发**（否则会被 Coze 端当「无文件体」丢弃），由调用方明确告知用户。

#: 本地可自行解码的 OOXML 扩展名（不需要转发，走 build_doc_payload 的正文通道）；
#: 与 ``scripts/office_to_md.py`` 的单一真源对齐，缺失时用内置兜底值。
try:                                            # pragma: no cover
    import office_to_md as _otm
    LEGACY_EXTS = tuple(getattr(_otm, "LEGACY_EXTS", (".doc", ".xls", ".ppt")))
    OOXML_EXTS = tuple(getattr(_otm, "SUPPORTED_EXTS", (".docx", ".xlsx", ".pptx")))
    MAX_FILE_BYTES = int(getattr(_otm, "MAX_FILE_BYTES", 5 * 1024 * 1024))
except Exception:                               # noqa: BLE001
    LEGACY_EXTS = (".doc", ".xls", ".ppt")
    OOXML_EXTS = (".docx", ".xlsx", ".pptx")
    MAX_FILE_BYTES = 5 * 1024 * 1024

#: Coze 端 base64 载荷上限（字符），与 payload.py::MAX_FILE_B64_CHARS 对齐
MAX_FILE_B64_CHARS = 5_000_000
#: 原始文件可转发上限（字节）：base64 后不得超过上面那个字符上限
MAX_FORWARD_BYTES = (MAX_FILE_B64_CHARS // 4) * 3          # = 3_750_000

#: 本通道只搬「本地解不了」的格式；OOXML 本地解码更省流量且保真度更高
FORWARDABLE_EXTS = LEGACY_EXTS


def can_forward_file(path: str) -> str:
    """文件能否走「原样转发」通道。可转发返回 ``""``，否则返回**面向用户**的原因。"""
    try:
        if not isinstance(path, str) or not path.strip():
            return "未提供文件路径。"
        if not os.path.isfile(path):
            return "文件不存在或不可读，请重新上传。"
        size = os.path.getsize(path)
        if size <= 0:
            return "文件内容为空，请重新导出后再上传。"
        if size > MAX_FORWARD_BYTES:
            # 新通道放行（2026-09-24 接线）：老通道受 base64 内联上限（3.75 MB）限制，
            # 但 file_id 上传通道可达 50 MB。此时若服务端支持上传且体积在新上限内，
            # 视为**可处理**并返回 "" —— 否则 SKILL.md 的准入检查会在入口把这类文件
            # 挡掉，新通道永远走不到（v1.26 空转的根因之一）。
            if (size <= MAX_UPLOAD_BYTES
                    and os.path.splitext(path)[1].lower() in ALL_OFFICE_EXTS
                    and _coze_upload_available()):
                return ""
            return ("文件体积 %.1f MB，超过可转发上限 %.1f MB。"
                    "请用 Office/WPS 打开后「另存为」.docx/.xlsx/.pptx 并精简内容，"
                    "或只把需要分析的章节粘贴为文本。"
                    % (size / 1048576.0, MAX_FORWARD_BYTES / 1048576.0))
        ext = os.path.splitext(path)[1].lower()
        if ext in OOXML_EXTS:
            return ("该格式（%s）本地可直接解析，无需转发——"
                    "请先在本地转为 Markdown 正文再发送。" % ext)
        if ext not in FORWARDABLE_EXTS:
            return ("暂不支持该格式（%s）。可转发：%s；本地可直接解析：%s。"
                    % (ext or "无扩展名", " / ".join(FORWARDABLE_EXTS),
                       " / ".join(OOXML_EXTS)))
        if size > MAX_FILE_BYTES:
            return ("文件体积 %.1f MB，超过平台单文件上限 %.0f MB，"
                    "请精简内容后重新导出。"
                    % (size / 1048576.0, MAX_FILE_BYTES / 1048576.0))
        return ""
    except Exception:                            # noqa: BLE001
        return "文件检查失败，请重新上传。"


def build_file_payload(path: str = None, data: bytes = None, file_name: str = "",
                       instruction: str = "", allow_upload=None) -> tuple:
    """文档 → 载荷。**默认自动选通道**：新服务端走上传（file_id），老服务端回退 base64。

    这是 v1.26 的**接线点**（2026-09-24）：此前 ``build_upload_payload`` 已实现但
    没有任何调用方，file_id 通道等于空转。此处让**既有入口**自动升级，
    老调用方与 SKILL.md 无需改动即可受益；同时保证任何情况下都不劣化。

    Args:
        path: 文件路径（与 ``data`` 二选一）
        data: 原始字节（给了 ``data`` 就以其为准）
        file_name: 原始文件名（**必须带正确扩展名**，Coze 端据此判格式）
        instruction: 用户对该文档的真实诉求（检索/梳理提示），可为空
        allow_upload: 通道选择。``None``（默认）= 自动；``True`` = 强制上传通道；
            ``False`` = 强制老 base64 通道（联调/降级用）。

    Returns:
        ``(payload_json, doc_id)``；失败 → ``("", "")``（绝不阻断主流程）。

    降级链（任一环失败都落到下一环，绝不静默丢文档）：
        服务端支持上传 → ``mode=file_id``
        → 上传失败 → 老通道（≤3.75 MB 的老格式）→ ``mode=file``
        → 仍不可行 → ``("", "")``（与 v1.25 行为一致，由调用方明确告知用户）
    """
    try:
        if data is None:
            if not path or not os.path.isfile(path):
                return "", ""
            with open(path, "rb") as fh:
                data = fh.read()
        data = bytes(data)
        if not data:
            return "", ""
        if not file_name:
            file_name = os.path.basename(path or "")
        ext = os.path.splitext(file_name)[1].lower()

        # ── 新通道：真实上传（file_id）───────────────────────────────────
        want_upload = allow_upload
        if want_upload is None:
            # 默认只把**本地解不了的老格式**升级到上传通道：
            #   - OOXML（docx/xlsx/pptx）按 SKILL.md 既有流程走「本地 office_to_md → 正文」，
            #     省一次上传且保真度更高，不在此处改变它的行为；
            #   - 需要统一走上传通道时，调用方显式传 allow_upload=True。
            want_upload = (
                ext in FORWARDABLE_EXTS
                and len(data) <= MAX_UPLOAD_BYTES
                and _coze_upload_available()
            )
        if want_upload:
            try:
                pj, did = build_upload_payload(path=path, data=data,
                                               file_name=file_name,
                                               instruction=instruction)
                if pj:
                    return pj, did
            except UploadFailedError:
                _mark_upload_unavailable()      # 同会话后续文件直接走老通道
            except Exception:                   # noqa: BLE001
                _mark_upload_unavailable()
            # 落到下面的老通道；老通道走不了就返回空（与 v1.25 一致）

        # ── 老通道：原样转发字节（mode=file）────────────────────────────
        if len(data) > MAX_FORWARD_BYTES:        # 转发前先把上限卡住，不制造必被丢弃的载荷
            return "", ""
        doc_id = hash_bytes(data, salt=ext)
        payload = {
            "v": PAYLOAD_SCHEMA_VERSION,
            "doc_id": doc_id,
            "instruction": (instruction or "").strip(),
            "mode": "file",
            "file_name": file_name,
            "file_b64": base64.b64encode(data).decode("ascii"),
            "total_chars": len(data),
            "source": "local_file_forward",
        }
        return json.dumps(payload, ensure_ascii=False), doc_id
    except Exception:  # noqa: BLE001
        return "", ""


def can_attach_file(path: str) -> str:
    """**统一**附件准入检查（覆盖 file_id 上传通道 + 老 base64 转发通道）。

    与 :func:`can_forward_file` 的区别：后者只认老格式且限 3.75 MB（老通道口径）；
    本函数按「两条通道任一可走」判断，是 :func:`build_file_payload` 的配套入口。

    返回 "" 表示可处理；否则返回**面向用户**的原因（调用方须原样转达）。
    """
    try:
        if not isinstance(path, str) or not path.strip():
            return "未提供文件路径。"
        if not os.path.isfile(path):
            return "文件不存在或不可读，请重新上传。"
        if os.path.getsize(path) <= 0:
            return "文件内容为空，请重新导出后再上传。"
        ext = os.path.splitext(path)[1].lower()
        if ext not in ALL_OFFICE_EXTS:
            return ("暂不支持该格式（%s）。可处理：%s。"
                    % (ext or "无扩展名", " / ".join(ALL_OFFICE_EXTS)))
        if os.path.getsize(path) > MAX_UPLOAD_BYTES:
            return ("文件体积 %.1f MB，超过服务端单文件上限 %.0f MB，"
                    "请拆分章节或精简后重新导出。"
                    % (os.path.getsize(path) / 1048576.0,
                       MAX_UPLOAD_BYTES / 1048576.0))
        return ""
    except Exception:                            # noqa: BLE001
        return "文件检查失败，请重新上传。"


# ---------------------------------------------------------------------------
# 对外（2026-09-24）：统一文档上传到 Coze 终端（file_id 真实上传通道）
# ---------------------------------------------------------------------------
# 需求（用户 2026-09-24 08:56 澄清）：飞书归档暂停，优先做"文档上传到扣子终端"。
#   - > 5 MB：本地转 MD → 以附件形式上传；≤ 5 MB：直接上传原文件，Coze 端解码。
#   - 新格式（docx/xlsx/pptx）与老格式（doc/xls/ppt）均按同一流程，不再区分。
# 实现：本地读字节 →（>5MB 且可转则 office_to_md 转 MD）→ POST 统一端点 /upload_file
#   拿 file_id + url → 写进 doc_context 信封（mode="file_id"）；Coze 工作流按 file_id/url
#   取回字节 → office_reader 解码（OLE2+OOXML 通用）。详见 design 文档。
UPLOAD_THRESHOLD_BYTES = 5 * 1024 * 1024   # 5 MB：> 此值本地先转 MD
UPLOAD_ENDPOINT_ENV = "CT_ADVISOR_UPLOAD_ENDPOINT"
UPLOAD_PATH = "/upload_file"
#: 新上传通道接受全部 Office 格式（新/老），不再区分
ALL_OFFICE_EXTS = LEGACY_EXTS + OOXML_EXTS

#: 服务端 /upload_file 的硬上限（字节），与 adapters/coze/src/main.py::MAX_UPLOAD_BYTES
#: 对齐。超过该值服务端会直接拒绝（500），所以本地**提前预检并给出可执行的提示**，
#: 而不是让用户看到一句不可行动的服务端报错。
MAX_UPLOAD_BYTES = 50 * 1024 * 1024

#: 上传通道可用性的**进程内**缓存：None=未探测 / True=可用 / False=不可用。
#: 目的：老服务端（≤v1.24，无 /upload_file）只会被探测一次，之后直接走老通道，
#: 既不产生额外往返，也不会把 file_id 信封发给不认识它的服务端。
_UPLOAD_AVAIL = None
_UPLOAD_PROBE_TIMEOUT = 8


def _strip_run_suffix(base: str) -> str:
    """剥离基址尾部的 ``/run`` —— 拼接 ``/upload_file`` 前必须去掉。

    兼容性要点（2026-09-24）：``adapters/http_probe.py::COZE_ENDPOINT`` 自带 ``/run``
    后缀，直接拼会得到 ``https://host/run/upload_file``（错误路径）。老环境没有
    ``CT_ADVISOR_UPLOAD_ENDPOINT`` 时就会踩到，故在此统一剥离，env 仍优先（联调/灰度用）。
    """
    b = (base or "").rstrip("/")
    for suffix in ("/run",):
        if b.endswith(suffix):
            b = b[: -len(suffix)].rstrip("/")
    return b


def _resolve_upload_endpoint() -> str:
    """上传端点**基址**（不含路径）。优先 env 覆盖，否则取 COZE_ENDPOINT 并剥离 /run。"""
    env = os.environ.get(UPLOAD_ENDPOINT_ENV)
    if env:
        return _strip_run_suffix(env)
    try:
        from adapters.http_probe import COZE_ENDPOINT
        if COZE_ENDPOINT:
            return _strip_run_suffix(COZE_ENDPOINT)
    except Exception:                       # noqa: BLE001
        pass
    return ""


def _coze_upload_available(force_refresh: bool = False) -> bool:
    """探测服务端是否支持 ``/upload_file``（file_id 通道）。

    判据（与人工 curl 实测一致）：
      - **405** = FastAPI 路由存在但只接受 POST → 可用；
      - 200 / 401 / 403 → 路由存在（可能带网关鉴权）→ 可用；
      - **404** → 老服务端没有该路由 → 不可用；
      - 5xx / 网络异常 → 视为不可用（安全方向：回退老通道，绝不阻断）。

    结果在进程内缓存；上传失败时由 :func:`_mark_upload_unavailable` 立即置否，
    使同一会话内后续文件不再重复踩坑。
    """
    global _UPLOAD_AVAIL
    if _UPLOAD_AVAIL is not None and not force_refresh:
        return _UPLOAD_AVAIL
    endpoint = _resolve_upload_endpoint()
    if not endpoint:
        _UPLOAD_AVAIL = False
        return False
    # 出站探测逻辑已下沉到 adapters/coze_upload.py（§16.9）
    try:
        _UPLOAD_AVAIL = coze_upload.probe_upload_available(
            endpoint, UPLOAD_PATH, _UPLOAD_PROBE_TIMEOUT, _get_coze_token)
    except Exception:                       # noqa: BLE001
        _UPLOAD_AVAIL = False
    return _UPLOAD_AVAIL


def _mark_upload_unavailable() -> None:
    """上传实际失败 → 立即判定通道不可用（供同会话后续调用直接走老通道）。"""
    global _UPLOAD_AVAIL
    _UPLOAD_AVAIL = False


def upload_to_coze(content: bytes, name: str) -> tuple:
    """把字节上传到统一端点 /upload_file，返回 (file_id, file_url)。

    失败一律抛 UploadFailedError（**绝不静默吞**）——由调用方转达用户。
    """
    endpoint = _resolve_upload_endpoint()
    if not endpoint:
        raise UploadFailedError("未配置文档上传端点，无法上传文件。")
    url = endpoint + UPLOAD_PATH
    # 出站上传逻辑已下沉到 adapters/coze_upload.py（§16.9）
    try:
        return coze_upload.upload_to_coze(content, name, url, _get_coze_token)
    except UploadFailedError:
        raise
    except Exception as e:                    # noqa: BLE001
        raise UploadFailedError("文档上传失败：%r" % (e,))


def _convert_ooxml_to_md(path: str, ext: str):
    """OOXML 本地转 MD（>5MB 时绕过 office_to_md 的 5MB 体积门，直接调格式解析器）。

    老格式（doc/xls/ppt）本地无法解析 → 返回 None（交由 Coze 端解码）。
    任何异常 → None（绝不阻断，回退为上传原文件）。
    """
    try:
        import office_to_md as _otm
    except Exception:                         # noqa: BLE001
        return None
    try:
        if ext == ".docx":
            return _otm.docx_to_md(path)
        if ext == ".xlsx":
            return _otm.xlsx_to_md(path)
        if ext == ".pptx":
            return _otm.pptx_to_md(path)
    except Exception:                         # noqa: BLE001
        return None
    return None


def can_upload_file(path: str) -> str:
    """新上传通道的准入检查（接受全部 Office 格式，任意大小——file_id 通道无内联上限）。

    返回 "" 表示可上传；否则返回**面向用户**的原因（调用方须原样转达，禁止静默吞）。
    """
    try:
        if not isinstance(path, str) or not path.strip():
            return "未提供文件路径。"
        if not os.path.isfile(path):
            return "文件不存在或不可读，请重新上传。"
        if os.path.getsize(path) <= 0:
            return "文件内容为空，请重新导出后再上传。"
        ext = os.path.splitext(path)[1].lower()
        if ext not in ALL_OFFICE_EXTS:
            return ("暂不支持该格式（%s）。可上传：%s。"
                    % (ext or "无扩展名", " / ".join(ALL_OFFICE_EXTS)))
        size = os.path.getsize(path)
        if size > MAX_UPLOAD_BYTES:
            return ("文件体积 %.1f MB，超过服务端单文件上限 %.0f MB。"
                    "请把文档拆分章节，或精简后重新导出。"
                    % (size / 1048576.0, MAX_UPLOAD_BYTES / 1048576.0))
        return ""
    except Exception:  # noqa: BLE001
        return "文件检查失败，请重新上传。"


def build_upload_payload(path: str = None, data: bytes = None, file_name: str = "",
                        instruction: str = "") -> tuple:
    """统一文档上传入口（**取代 build_file_payload 的"仅老格式"限制**）。

    所有 Office 格式（新/老）走同一条路：
      - ≤ 5 MB：上传**原文件字节**，Coze 端解码（OLE2+OOXML 通用）；
      - > 5 MB：优先本地转 MD（仅 OOXML 可转）→ 上传 MD；转不动则回退上传原文件。

    注意：上传失败（UploadFailedError）会**向上抛**，由 :func:`prepare_file_upload`
    或调用方捕获并转达用户（绝不在此静默吞）。
    Returns: ``(payload_json, doc_id)``；非上传类失败 → ``("", "")``。
    """
    try:
        if data is None:
            if not path or not os.path.isfile(path):
                return "", ""
            with open(path, "rb") as fh:
                data = fh.read()
        data = bytes(data)
        if not data:
            return "", ""
        if not file_name:
            file_name = os.path.basename(path or "")
        ext = os.path.splitext(file_name)[1].lower()
        size = len(data)
        doc_id = hash_bytes(data, salt=ext)
        converted = False
        if size > UPLOAD_THRESHOLD_BYTES:
            md = _convert_ooxml_to_md(path or "", ext) if path else None
            if md:
                content = md.encode("utf-8")
                converted = True
                upload_name = (os.path.splitext(file_name)[0] or "doc") + ".md"
            else:
                content = data
                upload_name = file_name
        else:
            content = data
            upload_name = file_name
        file_id, file_url = upload_to_coze(content, upload_name)
        # P1（2026-09-24）：转 MD 成功时，信封里的 file_name **必须**是 .md 名。
        # 服务端 _decode_file_id 用 file_name 的扩展名判格式，而 office_reader.sniff
        # 规定「扩展名自称二进制办公格式（.docx/.xlsx/.pptx…）但魔数不匹配 → 一律
        # FMT_UNKNOWN 并显式报错」。上传体已是纯文本 MD，若 file_name 仍带 .docx，
        # 大文档会 100% 解码失败。原名另存 origin_name 供展示/回溯。
        payload = {
            "v": PAYLOAD_SCHEMA_VERSION,
            "doc_id": doc_id,
            "instruction": (instruction or "").strip(),
            "mode": "file_id",
            "file_id": file_id,
            "file_url": file_url,
            "file_name": upload_name if converted else file_name,
            "origin_name": file_name if converted else "",
            "converted": converted,
            "total_chars": len(data),
            "source": "local_file_upload",
        }
        return json.dumps(payload, ensure_ascii=False), doc_id
    except UploadFailedError:
        raise
    except Exception:  # noqa: BLE001
        return "", ""


def prepare_file_upload(path: str = None, data: bytes = None, file_name: str = "",
                       instruction: str = "") -> tuple:
    """同 :func:`build_upload_payload`，但额外返回**面向用户的错误原因**（第三元素）。

    Returns: ``(payload_json, doc_id, error_message)``；成功时 error_message 为空串。
    """
    if data is None and (not path or not os.path.isfile(path)):
        return "", "", "文件不存在或不可读，请重新上传。"
    try:
        pj, did = build_upload_payload(path=path, data=data, file_name=file_name,
                                       instruction=instruction)
        if not pj:
            return "", "", "文档上传失败（未获得 file_id），请重试或改以文本粘贴。"
        return pj, did, ""
    except UploadFailedError as e:
        return "", "", str(e)
    except Exception as e:                    # noqa: BLE001
        return "", "", "文档上传失败：%r" % (e,)


if __name__ == "__main__":
    # 简单自测（无网）
    sample = "请梳理以下文档：\n" + ("这是一段很长的临床试验背景资料。" * 400)
    nq, did = compact_large_question(sample)
    print("orig_len:", len(sample), "| new_len:", len(nq), "| doc_id:", did)
    print("compacted:", len(nq) < len(sample))
    # 结构化载荷自测
    payload, pid = build_doc_payload(sample)
    import json as _json
    obj = _json.loads(payload) if payload else {}
    print("payload mode:", obj.get("mode"), "| doc_id:", pid,
          "| instruction:", repr(obj.get("instruction")))
    print("payload chars:", len(payload), "| total_chars:", obj.get("total_chars"))
    print("载荷无压缩字段:", "zip" not in obj and "text_b64" not in obj)
    # 短问题不应产生载荷
    print("short -> empty:", build_doc_payload("主要终点怎么设？") == ("", ""))
    # 单行长文档（无指令行）→ instruction 应为空串
    one_line = "临床试验背景" * 2000
    _, _ = build_doc_payload(one_line)
    print("single-line instruction:", repr(split_instruction(one_line)))
    # 老格式转发自测（用最小 OLE2 头造 16 字节假文件不够，这里只验通道行为）
    fake = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 512
    fp, fid = build_file_payload(data=fake, file_name="方案.doc", instruction="请梳理要点")
    fobj = _json.loads(fp) if fp else {}
    print("file payload mode:", fobj.get("mode"), "| doc_id:", fid,
          "| file_name:", fobj.get("file_name"),
          "| b64_chars:", len(fobj.get("file_b64") or ""))
    print("file 上限:", MAX_FORWARD_BYTES, "字节 | 超限不转发:",
          build_file_payload(data=b"\x00" * (MAX_FORWARD_BYTES + 1),
                             file_name="big.doc") == ("", ""))

    # ------------------------------------------------------------------
    # 兼容矩阵自测（2026-09-24）：新/老本地 × 新/老服务端，全程无网
    # ------------------------------------------------------------------
    # 注意：本文件以 __main__ 运行，build_file_payload 内部解析的是 __main__ 的
    # 全局名；patch ``import doc_memory as _dm`` 那份模块对象是**无效**的
    # （两套 globals 互不相通，会真的发出网络请求）。故一律改当前模块的 globals。
    _g = globals()

    def _ok_upload(content, name):
        _ok_upload.seen_name = name
        return "file_abc123", "https://host/f/file_abc123"

    def _dead_upload(content, name):
        raise UploadFailedError("模拟：上传失败")

    def _probe_true(force_refresh=False):
        return True

    def _probe_false(force_refresh=False):
        return False

    def _reset():
        _g["_UPLOAD_AVAIL"] = None

    def _mode(pj):
        return (_json.loads(pj).get("mode") if pj else "(空)")

    legacy = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 512   # 迷你 OLE2
    big_legacy = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * (4 * 1024 * 1024)

    print("\n-- 兼容矩阵 --")

    # A. 新服务端 + 老格式小文件 → 走上传（file_id）
    _reset(); _g["upload_to_coze"] = _ok_upload; _g["_coze_upload_available"] = _probe_true
    pj, _ = build_file_payload(data=legacy, file_name="方案.doc")
    print("A 新服务端/老格式小文件     :", _mode(pj), "(期望 file_id)")

    # B. 新服务端 + 4MB 老格式（超出老通道 3.75MB 上限）→ 只有新通道能处理
    pj, _ = build_file_payload(data=big_legacy, file_name="大文件.doc")
    print("B 新服务端/4MB 老格式       :", _mode(pj), "(期望 file_id)")

    # C. 老服务端 + 老格式小文件 → 自动回退 mode=file（与 v1.25 完全一致）
    _reset(); _g["_coze_upload_available"] = _probe_false
    pj, _ = build_file_payload(data=legacy, file_name="方案.doc")
    obj = _json.loads(pj) if pj else {}
    print("C 老服务端/老格式小文件     :", _mode(pj),
          "| b64 存在:", bool(obj.get("file_b64")), "(期望 file)")

    # D. 老服务端 + 超限文件 → 空（v1.25 行为：不静默丢，交由调用方提示）
    pj, _ = build_file_payload(data=big_legacy, file_name="大文件.doc")
    print("D 老服务端/4MB 超限         :", _mode(pj), "(期望 空)")

    # E. 强制老通道（allow_upload=False）
    _reset(); _g["_coze_upload_available"] = _probe_true
    pj, _ = build_file_payload(data=legacy, file_name="方案.doc", allow_upload=False)
    print("E 强制老通道                :", _mode(pj), "(期望 file)")

    # F. 探测说可用但上传真失败 → 回退老通道，且标记不可用
    _reset(); _g["upload_to_coze"] = _dead_upload; _g["_coze_upload_available"] = _probe_true
    pj, _ = build_file_payload(data=legacy, file_name="方案.doc")
    print("F 上传失败自动回退          :", _mode(pj),
          "| 已标记不可用:", _g.get("_UPLOAD_AVAIL") is False, "(期望 file/True)")

    # G. P1：>5MB 转 MD → 信封 file_name 必须变 .md（否则服务端按二进制判格式必报错）
    _reset(); _g["upload_to_coze"] = _ok_upload; _g["_coze_upload_available"] = _probe_true
    _g["_convert_ooxml_to_md"] = lambda p, e: "# 转换后的 Markdown\n内容"
    pj, _ = build_file_payload(data=b"PK\x03\x04" + b"\x00" * (6 * 1024 * 1024),
                               file_name="大方案.docx", path="/tmp/大方案.docx",
                               allow_upload=True)
    obj = _json.loads(pj) if pj else {}
    print("G >5MB 转 MD 后的 file_name :", obj.get("file_name"),
          "| origin_name:", obj.get("origin_name"), "(期望 .md)")

    # H. 端点拼接：即便 env 未设、COZE_ENDPOINT 自带 /run，也不能拼出 /run/upload_file
    _g["_coze_upload_available"] = _coze_upload_available
    saved_env = os.environ.pop("CT_ADVISOR_UPLOAD_ENDPOINT", None)
    print("H 端点剥离 /run            :",
          _strip_run_suffix("https://ct-advisor.coze.site/run"),
          "(期望 https://ct-advisor.coze.site)")
    if saved_env is not None:
        os.environ["CT_ADVISOR_UPLOAD_ENDPOINT"] = saved_env
