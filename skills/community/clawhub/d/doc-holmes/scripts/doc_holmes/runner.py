"""批量 runner：工程铁律逐条落实（plan.md T4.1，每条对应一个测试）。

① 路径一律 os.path.realpath 后比较/存储
② os.walk 显式排除：_duplicates/ _non_pdf_assets/ __pycache__/ .git/ 及输出目录
③ 黑名单/完成表用 set
④ 默认单进程；--workers N（N≤4）显式开启并警告
⑤ 每文件超时（engine 层强制）
⑥ watchdog：跟踪最近完成时刻，停滞超阈值的在跑文件记审计 stalled_timeout
⑦ 断点续传：audit.jsonl 重放，已完成且产物仍在 → skip
⑧ python -m compileall 进测试链（tests/test_runner.py）
审计状态：success / failed / timeout / skipped（failed 含产物回滚）
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from . import triage as triage_mod
from .engine_babeldoc import discover_outputs, translate_pdf

EXCLUDE_DIRS = {"_duplicates", "_non_pdf_assets", "__pycache__", ".git",
                "output", "_translated", ".venv", "node_modules"}
AUDIT_NAME = "audit.jsonl"
WATCHDOG_STALL_S = 300


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_pdfs(root: str) -> list:
    """铁律①②：realpath 收集 + 排除目录。"""
    real_root = os.path.realpath(root)
    found = []
    for dirpath, dirnames, filenames in os.walk(real_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if name.lower().endswith(".pdf"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


@dataclass
class BatchResult:
    outdir: str
    total: int = 0
    success: int = 0
    failed: int = 0
    timeout: int = 0
    skipped: int = 0
    entries: list = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""

    def summary(self) -> str:
        return ("汇总: 总计 %d | 成功 %d | 失败 %d | 超时 %d | 跳过(已完成) %d → %s"
                % (self.total, self.success, self.failed, self.timeout,
                   self.skipped, self.outdir))


def _load_done(audit_path: str) -> dict:
    """铁律⑦：重放审计日志。key=sha256 → entry（仅 success）。"""
    done = {}
    if not os.path.isfile(audit_path):
        return done
    with open(audit_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("status") == "success":
                done[entry.get("sha256")] = entry
    return done


def _outputs_intact(entry: dict) -> bool:
    for key in ("dual_path", "mono_path"):
        p = entry.get(key)
        if p and not os.path.isfile(p):
            return False
    return bool(entry.get("dual_path") or entry.get("mono_path"))


class Watchdog:
    """铁律⑥：停滞监测（记录；杀进程由 engine 的 per-file 超时兜底）。"""

    def __init__(self, stall_s: int = WATCHDOG_STALL_S):
        self.stall_s = stall_s
        self.last_progress = time.time()
        self.current = None
        self.stalled = []
        self._stop = threading.Event()
        self._lock = threading.Lock()

    def touch(self, name=None):
        with self._lock:
            self.last_progress = time.time()
            self.current = name

    def start(self):
        def loop():
            while not self._stop.wait(30):
                with self._lock:
                    idle = time.time() - self.last_progress
                    if idle > self.stall_s and self.current:
                        self.stalled.append({"file": self.current, "stall_s": round(idle)})
        t = threading.Thread(target=loop, daemon=True)
        t.start()
        return self

    def stop(self):
        self._stop.set()


def run_batch(input_dir: str, outdir: str, base_url: str, api_key: str, model: str,
              *, workers: int = 1, resume: bool = True, blacklist=None,
              lang_in: str = "en", lang_out: str = "zh", qps: int = 4,
              per_file_timeout_s: int = None, do_triage: bool = True,
              force_tier: str = None, repair: str = "auto",
              no_glossary: bool = False, openai_timeout: int = None,
              part_pages: int = None, glossary: str = "auto",
              medical_glossary: bool = True, glossaries_file=None,
              line_proofread=None, auto_lang: bool = False,
              ocr_mode: str = "auto", ocr_lang: str = "eng",
              password: str = None, seed_terms: bool = False,
              progress=None) -> BatchResult:
    """批量翻译。审计逐文件落 outdir/audit.jsonl；失败文件产物回滚。"""
    if workers > 4:
        raise ValueError("workers 上限 4（子进程并发过高会拖垮宿主机）")
    os.makedirs(outdir, exist_ok=True)
    audit_path = os.path.join(outdir, AUDIT_NAME)
    done = _load_done(audit_path) if resume else {}
    blacklist = {os.path.realpath(x) for x in (blacklist or [])}

    pdfs = list_pdfs(input_dir)
    result = BatchResult(outdir=os.path.realpath(outdir), total=len(pdfs),
                         started_at=time.strftime("%Y-%m-%d %H:%M:%S"))
    dog = Watchdog().start()

    def _append_audit(entry):
        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _one(pdf: str) -> dict:
        real = os.path.realpath(pdf)
        digest = sha256_of(real)
        rel = os.path.relpath(real, os.path.realpath(input_dir))
        if real in blacklist:
            entry = {"path": rel, "sha256": digest, "status": "skipped",
                     "reason": "blacklist"}
            return entry
        prev = done.get(digest)
        if prev and _outputs_intact(prev):
            entry = {"path": rel, "sha256": digest, "status": "skipped",
                     "reason": "already_done(resume)"}
            return entry

        rep = triage_mod.triage_pdf(real) if do_triage else None
        tier = force_tier or (rep.tier if rep else "?")

        # 每文件独立子目录：并发/回滚互不波及（评审 P0-2）— 需在 tier C 前定义
        file_out = os.path.join(outdir, digest[:12])
        os.makedirs(file_out, exist_ok=True)

        # v2.10.0：加密 PDF 批量解密（v2.8.0 遗留 NameError 根治，全分级生效）
        from .glossary_seed import needs_decrypt, decrypt_pdf
        orig_name = os.path.basename(real)
        if needs_decrypt(real):
            if not password:
                return {"path": rel, "sha256": digest, "tier": tier,
                        "status": "failed",
                        "error": "encrypted_needs_password: PDF 已加密，"
                                 "请用 --password 提供密码后重试"
                                 "（或先 qpdf --decrypt 手动解密）"}
            try:
                real = decrypt_pdf(real, password, file_out)
            except Exception as exc:
                return {"path": rel, "sha256": digest, "tier": tier,
                        "status": "failed",
                        "error": "decrypt_failed: %s" % str(exc)[:200]}

        ocr_stats = None
        tmp_ocr = None
        # v2.9.0：C 级走 rebuild→proofread→translate 完整管线（不再跳过）
        if tier == "C":
            ocr_mode_eff = ocr_mode if ocr_mode else "auto"
            if ocr_mode_eff == "off":
                return {"path": rel, "sha256": digest, "tier": "C",
                        "status": "skipped",
                        "reason": "tier_C_ocr_disabled: 扫描件 OCR 已关闭"}
            # rebuild→proofread（translate 单文件同款管线）
            try:
                from .ocr_adapter import rebuild_repaired_textlayer
                # 重建层以原始文件名落盘：引擎产物沿用原文件主干名（对齐单文件通路）
                tmp_ocr = os.path.join(file_out, orig_name)
                line_pf = None
                if line_proofread:
                    line_pf = line_proofread
                ocr_stats = rebuild_repaired_textlayer(
                    real, tmp_ocr, lang=ocr_lang, line_proofread=line_pf)
                real = tmp_ocr
            except Exception as exc:
                import traceback as _tb
                _tb.print_exc()
                return {"path": rel, "sha256": digest, "tier": "C",
                        "status": "failed",
                        "error": "tier_C_rebuild_failed: %s" % str(exc)[:200]}

        # B 级图层去重修复（plan Phase 2）：auto=B 级自动，off 关闭
        repair_stats = None
        if repair != "off" and (repair == "on" or tier == "B"):
            try:
                from .repair_pdf import inspect_pdf_dedup
                repair_stats = inspect_pdf_dedup(real)
            except Exception as exc:
                repair_stats = {"error": str(exc)[:200]}

        # v2.6.0：自动语言检测（auto_lang=True 时覆盖 lang_in）
        eff_lang_in = lang_in
        if auto_lang and rep and rep.tier in ("A", "B"):
            try:
                from .lang_detect import detect_language
                det = detect_language(real)
                if det["lang"] != "en" and det["confidence"] > 0.15:
                    eff_lang_in = det["lang"]
                    print("[语言检测] %s → %s（置信度 %.0f%%）"
                          % (os.path.basename(real), det["lang"],
                             det["confidence"] * 100))
            except Exception:
                pass

        # 铁律⑤：engine 层 per-file 超时
        from .cli import _large_doc_policy
        eff_part, eff_no_glossary, _notices = _large_doc_policy(
            rep.page_count if rep else None, part_pages, glossary)
        if no_glossary:
            eff_no_glossary = True
        extra = []
        if eff_no_glossary:
            extra.append("--no-auto-extract-glossary")
        if eff_part:
            extra.append("--max-pages-per-part")
            extra.append(str(eff_part))
        # 术语表注入：引擎 --glossaries 为单值（逗号分隔多路径，last-wins）
        gp = []
        from .glossary import glossary_csv_ok, glossary_path
        if medical_glossary and lang_in == "en" and lang_out == "zh":
            if glossary_csv_ok():
                gp.append(glossary_path())
        for gf in (glossaries_file or []):
            if os.path.isfile(gf) and glossary_csv_ok(os.path.abspath(gf)):
                gp.append(os.path.abspath(gf))
            else:
                print("[术语表] 用户术语表不存在或格式异常，已跳过：%s" % gf, file=sys.stderr)
        # v2.10.0：文档术语自适应种子（LLM 翻译 → CSV，永不空 target）
        seed_stats = None
        if seed_terms and lang_in == "en" and lang_out == "zh" and not eff_no_glossary:
            try:
                from .glossary_seed import seed_glossary, translate_terms_llm
                seed_stats = seed_glossary(
                    real, glossary_path() if medical_glossary else None, file_out,
                    translate_fn=lambda terms: translate_terms_llm(
                        terms, base_url, api_key, model,
                        timeout=openai_timeout or 60))
                if seed_stats.get("path"):
                    gp.append(seed_stats["path"])
            except Exception as exc:
                seed_stats = {"error": str(exc)[:200]}
        # v2.10.0 评审 P0-1/P1-3：注入外部术语表即关引擎自动抽取（防挂死实例 +
        # 防抽取非空时用户表被遮蔽），与 translate 通路同款语义
        if gp:
            if "--no-auto-extract-glossary" not in extra:
                extra.append("--no-auto-extract-glossary")
            extra = extra + ["--glossaries", ",".join(gp)]
        eng = translate_pdf(
            real, file_out, base_url, api_key, model,
            page_count=rep.page_count if rep else None,
            timeout_s=per_file_timeout_s,
            lang_in=eff_lang_in, lang_out=lang_out, qps=qps, extra_args=extra,
            openai_timeout=openai_timeout)

        if tmp_ocr and os.path.isfile(tmp_ocr):
            try:
                os.remove(tmp_ocr)
            except OSError:
                pass

        entry = {
            "path": rel, "sha256": digest, "tier": tier,
            "status": "success" if eng.ok else ("timeout" if eng.timed_out else "failed"),
            "duration_s": round(eng.duration_s, 1),
            "dual_path": eng.dual_path, "mono_path": eng.mono_path,
            "chars_per_page": rep.chars_per_page if rep else None,
            "triage_reasons": rep.reasons if rep else [],
            "large_doc_policy": {"part_pages": eff_part or 0,
                                 "glossary_skipped": bool(eff_no_glossary or no_glossary)},
            "repair": repair_stats,
            "error": None if eng.ok else eng.stderr_tail[-600:],
        }
        if ocr_stats is not None:
            entry["ocr"] = ocr_stats
        if seed_stats is not None:
            entry["glossary_seeding"] = seed_stats
        if not eng.ok:
            # 回滚：删除本次产生的残缺产物（铁律：失败不留半成品）
            for p in (eng.dual_path, eng.mono_path):
                if p and os.path.isfile(p):
                    try:
                        os.remove(p)
                    except OSError:
                        pass
            entry["dual_path"] = entry["mono_path"] = None
            entry["rolled_back"] = True
        return entry

    def _one_safe(pdf):
        """单文件异常隔离：任何异常只废该文件，不炸整个批次（评审 P1-3）。"""
        try:
            return _one(pdf)
        except Exception as exc:
            real = os.path.realpath(pdf)
            rel = os.path.relpath(real, os.path.realpath(input_dir))
            return {"path": rel, "sha256": None, "tier": "?", "status": "failed",
                    "error": "unhandled: %r" % exc}

    try:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_one_safe, pdf): pdf for pdf in pdfs}
            for fut, pdf in futures.items():
                entry = fut.result()
                _append_audit(entry)
                result.entries.append(entry)
                status = entry["status"]
                if status == "success":
                    result.success += 1
                elif status == "timeout":
                    result.timeout += 1
                elif status == "skipped":
                    result.skipped += 1
                else:
                    result.failed += 1
                dog.touch(os.path.basename(pdf))
                if progress:
                    progress(result.success + result.failed + result.timeout
                             + result.skipped, result.total)
    finally:
        dog.stop()
        if dog.stalled:
            result.entries.extend({"watchdog": s} for s in dog.stalled)

    result.finished_at = time.strftime("%Y-%m-%d %H:%M:%S")
    return result


def write_report(result: BatchResult, report_path: str) -> str:
    """汇总 report.md：指标 + 逐文件状态表。末行含「汇总」字样（验收链依赖）。"""
    lines = ["# doc-holmes 批量翻译报告", "",
             "- 输入总计: %d" % result.total,
             "- 成功 / 失败 / 超时 / 跳过: %d / %d / %d / %d"
             % (result.success, result.failed, result.timeout, result.skipped),
             "- 时间: %s → %s" % (result.started_at, result.finished_at),
             "", "| 文件 | 级别 | 状态 | 耗时s | 备注 |", "|---|---|---|---|---|"]
    for e in result.entries:
        if "watchdog" in e:
            lines.append("| (watchdog) | - | stalled | %s | %s |"
                         % (e["watchdog"]["stall_s"], e["watchdog"]["file"]))
            continue
        note = e.get("error") or e.get("reason") or ""
        # v2.10.0：质量热点/术语种子进入备注列（报告可见性）
        flags = []
        low = (e.get("ocr") or {}).get("low_conf_pages") or []
        if low:
            flags.append("低置信页:" + ",".join(str(x) for x in low[:8])
                         + ("…" if len(low) > 8 else ""))
        seeded = (e.get("glossary_seeding") or {}).get("seeded") or []
        if seeded:
            flags.append("种子术语%d" % len(seeded))
        if flags:
            note = "；".join([str(note)[:60]] + flags)   # 先截错误再拼标记，防标记被截没
        note = str(note).replace("|", "/")[:120]
        lines.append("| %s | %s | %s | %s | %s |"
                     % (e.get("path", "?"), e.get("tier", "-"),
                        e.get("status", "?"), e.get("duration_s", "-"), note))
    # 求星尾注（用户令 10-06：面向人、人自己动手；汇总仍居末——验收链依赖）
    from .report_html import GITHUB_URL, SH_URL
    lines += ["",
              "> 本文档由 doc-holmes 生成（[GitHub](%s) · [SkillHub](%s)）· "
              "觉得有用欢迎 Star / 收藏" % (GITHUB_URL, SH_URL),
              "", result.summary(), ""]
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path
