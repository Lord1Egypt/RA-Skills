#!/usr/bin/env python3
"""doc-holmes 命令行入口。

子命令：triage（体检分级）/ translate（单文件翻译）/ batch（批量）/
report（汇总报告）/ selfcheck（环境自检）。全部中文帮助。
退出码：0 成功；2 配置/参数错误；3 引擎失败；4 批量部分失败。
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__
from .endpoints import (ENV_FILE, EndpointError, PaidEndpointError,
                        load_endpoint_config)


def _print_triage(reports, as_json=False):
    if as_json:
        print(json.dumps([r.to_dict() for r in reports], ensure_ascii=False, indent=2))
        return
    header = "%-4s %-9s %8s %6s %6s  %s" % ("级别", "文件", "字符/页", "重复", "水印", "说明")
    print(header)
    print("-" * len(header.expandtabs()))
    for r in reports:
        name = os.path.basename(r.path)[:36]
        reasons = "；".join(r.reasons)[:80]
        print("%-4s %-9s %8.0f %6d %6d  %s"
              % (r.tier, name, r.chars_per_page, r.duplicate_pairs,
                 r.watermark_lines, reasons))
    tiers = [r.tier for r in reports]
    print("\n汇总: A=%d B=%d C=%d，共 %d 份"
          % (tiers.count("A"), tiers.count("B"), tiers.count("C"), len(tiers)))


def cmd_triage(args) -> int:
    from .triage import triage_path
    reports = []
    for p in args.paths:
        reports.extend(triage_path(p, sample_pages=args.sample_pages))
    if not reports:
        print("未找到 PDF 文件。", file=sys.stderr)
        return 2
    _print_triage(reports, as_json=args.json)
    return 0


AUTO_SPLIT_PAGES_THRESHOLD = 40   # 页数阈值：超过即自动分段 + 自动跳过术语抽取
AUTO_SPLIT_PART_SIZE = 25


def _large_doc_policy(page_count, part_pages, glossary):
    """大文档自动策略（v2.0.0）：返回 (effective_part_pages, effective_no_glossary, notices)。

    - part_pages: None=自动（页数≥阈值按 25 页/段）；0=显式关闭分段；N=显式段大小
    - glossary: "auto" 时大文档自动跳过术语抽取（STTT 案例：巨型提示超时）；"off" 强制关
    """
    notices = []
    eff_part = part_pages
    eff_no_glossary = (glossary == "off")
    if page_count and page_count >= AUTO_SPLIT_PAGES_THRESHOLD:
        if eff_part is None:
            eff_part = AUTO_SPLIT_PART_SIZE
            notices.append("[大文档] %d 页 ≥ %d：自动按 %d 页/段分段翻译（--part-pages 0 可关闭）"
                           % (page_count, AUTO_SPLIT_PAGES_THRESHOLD, AUTO_SPLIT_PART_SIZE))
        if glossary == "auto":
            eff_no_glossary = True
            notices.append("[大文档] 自动跳过术语抽取（防巨型提示超时；--glossary auto 可感知）")
    return eff_part, eff_no_glossary, notices


def _hotspot_note(ocr_stats):
    """C级页级质量热点一句话（v2.10.0）；无热点返回 None。"""
    low = (ocr_stats or {}).get("low_conf_pages") or []
    if not low:
        return None
    show = ",".join(str(p) for p in low[:12]) + ("…" if len(low) > 12 else "")
    return "低置信页 %d 页（建议人工复核）：%s" % (len(low), show)


def _translate_one(pdf, outdir, ep, *, lang_in, lang_out, pages, no_dual, no_mono,
                   qps, tier_mode, ocr_mode, ocr_lang, timeout_s, repair_mode="auto",
                   no_glossary=False, part_pages=None, glossary="auto",
                   medical_glossary=True, glossaries_file=None,
                   ocr_proofread=True, output_format="pdf",
                   auto_lang=False, password=None,
                   seed_terms=False):
    """单文件完整通路：triage → (C 级 OCR) → 引擎 → (C 级说明页) → audit。"""
    from . import triage as triage_mod
    from .engine_babeldoc import translate_pdf

    # v2.8.0：加密 PDF 自动解密
    from .glossary_seed import needs_decrypt, decrypt_pdf
    if needs_decrypt(pdf):
        if not password:
            print("[加密] PDF 已加密但未提供密码。\n"
                  "  · --password <密码> 提供密码后自动解密重试\n"
                  "  · 或先手动解密（qpdf --decrypt in.pdf out.pdf）", file=sys.stderr)
            return 2, None, None
        outdir = outdir or "."
        try:
            pdf = decrypt_pdf(pdf, password, outdir)
            print("[加密] 解密成功 → %s" % pdf)
        except RuntimeError as exc:
            print("[加密] 解密失败：%s" % exc, file=sys.stderr)
            return 2, None, None

    os.makedirs(outdir, exist_ok=True)
    rep = triage_mod.triage_pdf(pdf)
    tier = rep.tier if tier_mode in (None, "auto") else tier_mode
    # 大文档自动策略（v2.0.0）：分段 + 术语抽取跳过（必须在 extra 使用前计算）
    # 用户显式给 --pages 时跳过自动策略（局部小任务不该被强跳术语/强分段）；
    # 显式 --part-pages 仍被尊重
    policy_page_count = None if pages else rep.page_count
    auto_part = part_pages
    eff_part, eff_no_glossary, policy_notices = _large_doc_policy(
        policy_page_count, auto_part, glossary)
    for notice in policy_notices:
        print(notice)

    extra = []
    if rep.two_column:
        extra += ["--split-short-lines"]
    if tier == "C":
        # OCR 重建层（图像+隐形文本）会被引擎的扫插件检测拦下，此为官方通道开关
        extra += ["--skip-scanned-detection"]

    # B 级图层重复检测（只读；on=全文档强制含 A 级，auto=仅 B 级，off=关闭）
    repair_stats = None
    work_pdf = pdf
    if repair_mode != "off" and (repair_mode == "on" or tier == "B"):
        try:
            from .repair_pdf import inspect_pdf_dedup
            repair_stats = inspect_pdf_dedup(pdf)
        except Exception as exc:   # 检测失败不拖死翻译（评审 P1）
            repair_stats = {"error": str(exc)[:200]}
        if repair_stats.get("spans_duplicated"):
            print("[B级] 同位置重复 span：%d 个（双重打印或伪粗体；示例：%s）"
                  % (repair_stats["spans_duplicated"],
                     (repair_stats["examples"][0] if repair_stats.get("examples") else "")[:40]))

    ocr_stats = None
    tmp_ocr = None
    if tier == "C":
        info = None
        if ocr_mode != "off":
            from . import ocr_adapter
            info = ocr_adapter.tesseract_info()
        if not info or not info.get("available"):
            print("[C级] 这是扫描件/无文本层 PDF，需要 OCR 实验通道：\n"
                  "  · 安装 tesseract：apt install tesseract-ocr（中文再加 tesseract-ocr-chi-sim）\n"
                  "  · 或改用有文本层的原生 PDF（doc-holmes 对 A/B 级承诺翻译质量）\n"
                  "  · 本文件未翻译。", file=sys.stderr)
            return 2, rep, None
        print("[C级] 走 OCR 实验通道（预览质量）：%s" % info.get("version", "tesseract"))
        tmp_ocr = os.path.join(outdir, os.path.basename(pdf))
        line_proofread = None
        if repair_mode != "off" and ocr_proofread:
            # v2.3.0：页级 LLM 错字校对（走用户自配端点，仅纠错不改写）
            from .proofread import make_page_proofread
            line_proofread = make_page_proofread(
                ep.base_url, ep.api_key, ep.model, timeout=ep.timeout or 120)
            print("[C级] LLM 错字校对已启用（--no-ocr-proofread 可关）")
        if repair_mode == "off":
            ocr_stats = ocr_adapter.ocr_pdf_to_textlayer(pdf, tmp_ocr, lang=ocr_lang)
        else:
            # v2.0.0：自建修复后隐形文本层（行级修复真实作用于译文源）
            ocr_stats = ocr_adapter.rebuild_repaired_textlayer(
                pdf, tmp_ocr, lang=ocr_lang, line_proofread=line_proofread)
            if ocr_stats.get("proofread_error"):
                print("[C级] 错字校对失败（已降级原文）：%s"
                      % ocr_stats["proofread_error"][:100])
            else:
                print("[C级] 错字校对：%d 行修正 / %d 行修复 / %d 字符"
                      % (ocr_stats.get("proofread_lines_changed", 0),
                         ocr_stats.get("lines_repaired", 0), ocr_stats.get("chars", 0)))
        if "pages_with_text" in ocr_stats:      # 旧 tesseract 直出层
            print("[C级] OCR 完成：%(pages)d 页，%(pages_with_text)d 页有文本，共 %(ocr_chars)d 字符"
                  % ocr_stats)
        else:                                    # v2.0.0 修复重建层
            print("[C级] OCR 完成：%(pages)d 页，%(lines)d 行，共 %(chars)d 字符"
                  % ocr_stats)
        hotspot = _hotspot_note(ocr_stats)
        if hotspot:
            print("[C级] %s" % hotspot)
        work_pdf = tmp_ocr

    if eff_part:
        extra = extra + ["--max-pages-per-part", str(eff_part)]
    # 术语表注入：引擎 --glossaries 为单值（逗号分隔多路径，last-wins）
    gp = []
    from .glossary import glossary_csv_ok, glossary_path
    if medical_glossary and lang_in == "en" and lang_out == "zh":
        if glossary_csv_ok():
            gp.append(glossary_path())
        else:
            print("[术语表] 内置医学术语表缺失或格式异常，已跳过注入（不影响翻译，仅术语一致性略降）")
    for gf in (glossaries_file or []):
        if os.path.isfile(gf) and glossary_csv_ok(os.path.abspath(gf)):
            gp.append(os.path.abspath(gf))
        else:
            print("[术语表] 用户术语表不存在或格式异常，已跳过：%s" % gf, file=sys.stderr)
    # v2.10.0：文档术语自适应种子（LLM 翻译 → CSV，永不空 target；
    # v2.8.0 空 target 行致引擎崩溃的机制层根治，--no-seed-terms 自此真接线）
    seed_stats = None
    if seed_terms and lang_in == "en" and lang_out == "zh" and not eff_no_glossary:
        try:
            from .glossary_seed import seed_glossary, translate_terms_llm
            seed_stats = seed_glossary(
                work_pdf, glossary_path() if medical_glossary else None, outdir,
                translate_fn=lambda terms: translate_terms_llm(
                    terms, ep.base_url, ep.api_key, ep.model,
                    timeout=ep.timeout or 60))
            if seed_stats.get("path"):
                gp.append(seed_stats["path"])
                print("[术语表] 自适应种子：注入 %d 个文档术语（内置表已覆盖 %d 个）"
                      % (len(seed_stats["seeded"]),
                         seed_stats.get("builtin_covered", 0)))
        except Exception as exc:
            print("[术语表] 自适应种子失败（不影响翻译）：%s" % str(exc)[:120],
                  file=sys.stderr)
            seed_stats = {"error": str(exc)[:200]}
    # v2.10.0 评审 P0-1/P1-3：注入外部术语表时必须关闭引擎自动术语抽取——
    # 引擎抽取阶段与用户表并存存在挂死实例（battery 6/6 实锤），且抽取非空时
    # 用户表被引擎遮蔽（注入形同虚设）。关抽取 = 注入真实生效 + 挂死阶段不存在。
    if gp or no_glossary or eff_no_glossary:
        extra.append("--no-auto-extract-glossary")
    if gp:
        extra = extra + ["--glossaries", ",".join(gp)]   # 引擎按逗号 split，不能带空格
    # v2.10.0：translate 通路 auto_lang 实装（此前仅 batch 生效，translate 为死旗标）
    eff_lang_in = lang_in
    if auto_lang and tier in ("A", "B"):
        try:
            from .lang_detect import detect_language
            det = detect_language(pdf)
            if det["lang"] != "en" and det["confidence"] > 0.15:
                eff_lang_in = det["lang"]
                print("[语言检测] %s → %s（置信度 %.0f%%）"
                      % (os.path.basename(pdf), det["lang"],
                         det["confidence"] * 100))
        except Exception:
            pass
    eng = translate_pdf(work_pdf, outdir, ep.base_url, ep.api_key, ep.model,
                        page_count=rep.page_count, timeout_s=timeout_s,
                        lang_in=eff_lang_in, lang_out=lang_out, qps=qps,
                        pages=pages, no_dual=no_dual, no_mono=no_mono,
                        openai_timeout=ep.timeout,
                        extra_args=extra)

    if tmp_ocr and os.path.isfile(tmp_ocr):
        try:
            os.remove(tmp_ocr)
        except OSError:
            pass

    audit = {
        "path": os.path.realpath(pdf), "tier": tier,
        "triage": rep.to_dict(), "engine": eng.to_dict(),
        "ocr": ocr_stats, "repair": repair_stats, "ok": eng.ok,
        "glossary_seeding": seed_stats,
        "large_doc_policy": {"part_pages": eff_part or 0,
                             "glossary_skipped": bool(eff_no_glossary or no_glossary)},
    }
    if eng.ok:
        from .ocr_adapter import attach_preview_notice
        if tier == "C":
            for p in (eng.dual_path, eng.mono_path):
                if p:
                    attach_preview_notice(p)
            audit["preview_quality_notice"] = True
        audit_path = os.path.join(
            outdir, os.path.splitext(os.path.basename(pdf))[0] + ".audit.json")
        with open(audit_path, "w", encoding="utf-8") as f:
            json.dump(audit, f, ensure_ascii=False, indent=2)
        print("✔ 翻译完成（%s 级，%.0fs）" % (tier, eng.duration_s))
        if output_format == 'docx':
            from .docx_output import pdf_to_docx
            for pdf_out in filter(None, [eng.dual_path, eng.mono_path]):
                try:
                    docx_path = pdf_to_docx(pdf_out, outdir)
                    print("  DOCX: %s" % docx_path)
                except Exception as exc:
                    print("  DOCX 转换失败（PDF 不受影响）：%s" % str(exc)[:120],
                          file=sys.stderr)
        if eng.dual_path:
            print("  双语对照: %s" % eng.dual_path)
        if eng.mono_path:
            print("  纯译文:   %s" % eng.mono_path)
        return 0, rep, audit
    print("✘ 翻译失败（%s）" % (audit["engine"]["stderr_tail"].splitlines()[-1][:160]
                             if audit["engine"]["stderr_tail"] else "原因未知"),
          file=sys.stderr)
    if seed_stats and seed_stats.get("path"):
        print("  提示：本次注入了实验性种子术语表，可去掉 --seed-terms 重试。",
              file=sys.stderr)
    return 3, rep, audit


def cmd_translate(args) -> int:
    try:
        ep = load_endpoint_config()
    except (EndpointError, PaidEndpointError) as exc:
        print("配置错误：%s" % exc, file=sys.stderr)
        return 2
    try:
        from .engine_babeldoc import find_engine_bin
        find_engine_bin()
    except Exception as exc:
        print("引擎不可用：%s" % exc, file=sys.stderr)
        return 2
    if os.path.isdir(args.pdf):
        print("%s 是目录——单文件请用 translate，目录批量请用：\n"
              "  doc-holmes batch %s -o <输出目录>" % (args.pdf, args.pdf), file=sys.stderr)
        return 2
    if args.part_pages is not None and args.part_pages < 0:
        print("--part-pages 不能为负数", file=sys.stderr)
        return 2
    # v2.2.0：DOCX/PPTX 输入（libreoffice 转 PDF 后走现有管线）
    work_input = args.pdf
    if os.path.splitext(args.pdf)[1].lower() in (".docx", ".pptx", ".ppt"):
        from .office_input import convert_to_pdf
        try:
            work_input = convert_to_pdf(
                args.pdf, args.output or os.path.join(
                    os.path.dirname(os.path.realpath(args.pdf)) or ".", "_translated"))
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2
    if not os.path.isfile(work_input):
        print("文件不存在：%s" % args.pdf, file=sys.stderr)
        return 2
    outdir = args.output or os.path.join(
        os.path.dirname(os.path.realpath(work_input)) or ".", "_translated")
    code, _, _ = _translate_one(
        work_input, outdir, ep, lang_in=args.lang_in, lang_out=args.lang_out,
        pages=args.pages, no_dual=args.no_dual, no_mono=args.no_mono,
        qps=args.qps if args.qps is not None else ep.qps, tier_mode=args.tier, ocr_mode=args.ocr,
        ocr_lang=args.ocr_lang, timeout_s=args.timeout_s,
        repair_mode=args.repair, no_glossary=args.no_glossary,
        part_pages=args.part_pages, glossary=args.glossary,
        medical_glossary=not args.no_medical_glossary,
        glossaries_file=args.glossaries_file,
        ocr_proofread=not args.no_ocr_proofread,
        output_format=args.output_format,
        auto_lang=args.auto_lang,
        password=args.password, seed_terms=args.seed_terms)
    return code


def cmd_batch(args) -> int:
    from .runner import run_batch, write_report
    try:
        ep = load_endpoint_config()
    except (EndpointError, PaidEndpointError) as exc:
        print("配置错误：%s" % exc, file=sys.stderr)
        return 2
    if not os.path.isdir(args.input_dir):
        print("目录不存在：%s" % args.input_dir, file=sys.stderr)
        return 2
    if args.workers > 1:
        print("⚠ 多进程并发已开启（%d workers）：引擎为子进程，请注意内存与限速。" % args.workers)

    def prog(done, total):
        sys.stdout.write("\r[%d/%d]" % (done, total))
        sys.stdout.flush()

    # v2.10.0：C 级 LLM 错字校对真实接线（v2.9.0 声明与实现脱节的根治）
    line_proofread = None
    if not args.no_ocr_proofread:
        from .proofread import make_page_proofread
        line_proofread = make_page_proofread(
            ep.base_url, ep.api_key, ep.model, timeout=ep.timeout or 120)

    result = run_batch(
        args.input_dir, args.output, ep.base_url, ep.api_key, ep.model,
        workers=args.workers, resume=not args.no_resume,
        blacklist=args.blacklist or [], lang_in=args.lang_in,
        lang_out=args.lang_out, qps=args.qps if args.qps is not None else ep.qps,
        per_file_timeout_s=args.timeout_s, force_tier=args.tier,
        repair=args.repair, no_glossary=args.no_glossary,
        openai_timeout=ep.timeout, part_pages=args.part_pages,
        glossary=args.glossary, medical_glossary=not args.no_medical_glossary,
        glossaries_file=args.glossaries_file,
        line_proofread=line_proofread,
        password=args.password,
        seed_terms=args.seed_terms,
        auto_lang=args.auto_lang,
        progress=prog if not args.quiet else None)
    if not args.quiet:
        print()
    report_path = os.path.join(args.output, "report.md")
    write_report(result, report_path)
    try:
        from .report_html import write_html
        html_path = write_html(result, args.output)
        print("报告: %s（可视化: %s）" % (report_path, html_path))
    except Exception as exc:   # html 失败不影响 md 报告与批次结果
        print("报告: %s（HTML 生成失败: %s）" % (report_path, str(exc)[:80]))
    print(result.summary())
    return 0 if (result.failed == 0 and result.timeout == 0) else 4


def cmd_report(args) -> int:
    from .runner import write_report, _load_done
    if not os.path.isdir(args.outdir):
        print("目录不存在：%s" % args.outdir, file=sys.stderr)
        return 2
    audit_path = os.path.join(args.outdir, "audit.jsonl")
    done = _load_done(audit_path)
    if not done:
        print("没有可汇总的成功记录（%s）。" % audit_path, file=sys.stderr)
        return 2
    from .runner import BatchResult
    r = BatchResult(outdir=args.outdir, total=len(done), success=len(done))
    for e in done.values():
        r.entries.append(e)
    report_path = os.path.join(args.outdir, "report.md")
    write_report(r, report_path)
    print("报告: %s" % report_path)
    return 0


def cmd_selfcheck(args) -> int:
    checks = []

    def add(name, ok, note=""):
        checks.append((name, bool(ok), note))

    import platform
    add("python>=3.10", sys.version_info >= (3, 10), platform.python_version())
    try:
        import pymupdf  # noqa: F401
        add("pymupdf", True, pymupdf.__version__ if hasattr(pymupdf, "__version__") else "ok")
    except Exception as exc:
        add("pymupdf", False, str(exc))
    from .engine_babeldoc import find_engine_bin, EngineNotFoundError
    try:
        add("pdf2zh_next 引擎", True, find_engine_bin())
    except EngineNotFoundError as exc:
        add("pdf2zh_next 引擎", False, str(exc).splitlines()[0])
    from .ocr_adapter import tesseract_info
    tess = tesseract_info()
    add("tesseract（C级 OCR，可选）", tess.get("available", False),
        tess.get("version", tess.get("reason", "")))
    gpu = "未检测到"
    try:
        import subprocess as sp
        r = sp.run(["nvidia-smi", "-L"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            gpu = r.stdout.strip().splitlines()[0]
    except Exception:
        pass
    add("GPU（可选，加速版面分析）", gpu != "未检测到", gpu)

    ep_note = ""
    ep_ok = False
    try:
        ep = load_endpoint_config()
        ep_ok = True
        ep_note = "%s @ %s" % (ep.model, ep.base_url)
    except (EndpointError, PaidEndpointError) as exc:
        ep_note = str(exc).splitlines()[0]
    add("翻译端点配置", ep_ok, ep_note)

    if args.net and ep_ok:
        try:
            import urllib.request
            req = urllib.request.Request(
                ep.base_url + "/chat/completions",
                data=json.dumps({"model": ep.model, "messages": [
                    {"role": "user", "content": "ping"}], "max_tokens": 1}).encode(),
                headers={"Authorization": "Bearer " + ep.api_key,
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                add("端点连通（--net）", resp.status == 200, "HTTP %s" % resp.status)
        except Exception as exc:
            add("端点连通（--net）", False, str(exc)[:120])

    print()
    all_ok = True
    for name, ok, note in checks:
        mark = "✅" if ok else ("⚠️" if "可选" in name else "❌")
        if not ok and "可选" not in name:
            all_ok = False
        print("%s %-28s %s" % (mark, name, note))
    print("\n汇总: %s" % ("PASS 全部关键项通过" if all_ok else "FAIL 有关键项未通过"))
    return 0 if all_ok else 2


def cmd_merge(args) -> int:
    from .pdf_tools import merge_pdfs
    try:
        out = merge_pdfs(args.inputs, args.output)
        print("✔ 合并完成：%s" % out)
        return 0
    except Exception as exc:
        print("%s" % exc, file=sys.stderr)
        return 2


def cmd_split(args) -> int:
    from .pdf_tools import split_pdf
    if not os.path.isfile(args.pdf):
        print("文件不存在：%s" % args.pdf, file=sys.stderr)
        return 2
    outdir = args.output or os.path.join(
        os.path.dirname(os.path.realpath(args.pdf)) or ".", "split_out")
    try:
        outs = split_pdf(args.pdf, outdir, args.pages_spec)
    except Exception as exc:
        print("%s" % exc, file=sys.stderr)
        return 2
    print("✔ 拆分完成：%d 段 → %s" % (len(outs), outdir))
    for p in outs:
        print("  %s" % p)
    return 0


def cmd_estimate(args) -> int:
    from .pdf_tools import estimate_pdf
    if not os.path.isfile(args.pdf):
        print("文件不存在：%s" % args.pdf, file=sys.stderr)
        return 2
    try:
        est = estimate_pdf(args.pdf, chunk_pages=args.part_pages, qps=args.qps)
    except Exception as exc:
        print("预估失败：%s" % str(exc)[:200], file=sys.stderr)
        return 2
    print("页数：%d | 字符量：%d | 含图页：%d" % (est["pages"], est["chars"], est["image_pages"]))
    if est["parts"] > 1:
        print("分段策略：%d 页/段 × %d 段（≥%d 页自动分段；--part-pages 可调）"
              % (est["chunk_pages"], est["parts"], 40))
        print("术语抽取：自动跳过（大文档防超时）")
    print("预计时长：约 %s 分钟（qps=%s，经验系数 45s/页，实际视版面复杂度浮动）"
          % (est["estimated_minutes"], args.qps))
    return 0


def cmd_extract(args) -> int:
    from .direct_mode import DirectModeError, extract_lines
    if not os.path.isfile(args.pdf):
        print("文件不存在：%s" % args.pdf, file=sys.stderr)
        return 2
    outdir = args.output or os.path.join(
        os.path.dirname(os.path.realpath(args.pdf)) or ".", "_direct")
    try:
        doc = extract_lines(args.pdf, pages_spec=args.pages,
                            force_b=args.force_b, lang_out=args.lang_out)
    except DirectModeError as exc:
        print("✘ %s" % exc, file=sys.stderr)
        return 2
    os.makedirs(outdir, exist_ok=True)
    json_path = os.path.join(outdir, "doc.direct.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    n = sum(len(p["lines"]) for p in doc["pages"])
    print("✔ 抽取完成（%s 级，%d 页 %d 行）→ %s"
          % (doc["tier"], doc["pages_total"], n, json_path))
    if doc.get("rotation_skipped_pages"):
        print("  注意：旋转页 %s 未抽取（apply 时原样保留）"
              % ",".join(map(str, doc["rotation_skipped_pages"])), file=sys.stderr)
    print("下一步：翻译 JSON 中每条 line 的 text → 同条写入 translated（留空=保留原文），")
    print("然后：doc-holmes apply %s -o %s [--dual]" % (json_path, outdir))
    return 0


def cmd_apply(args) -> int:
    from .direct_mode import DirectModeError, apply_translation
    if not os.path.isfile(args.json):
        print("文件不存在：%s" % args.json, file=sys.stderr)
        return 2
    try:
        with open(args.json, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print("JSON 读取失败：%s" % exc, file=sys.stderr)
        return 2
    outdir = args.output or os.path.join(
        os.path.dirname(os.path.realpath(args.json)) or ".", "direct_out")
    try:
        audit = apply_translation(doc, outdir, dual=args.dual,
                                  out_stem=args.name, pdf_override=args.pdf)
    except DirectModeError as exc:
        print("✘ %s" % exc, file=sys.stderr)
        return 2
    audit_path = os.path.join(outdir, "direct.audit.json")
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    print("✔ 直翻回填完成（%d/%d 行翻译，%d 行保留原文）"
          % (audit["lines_translated"], audit["lines_total"],
             audit["lines_kept_original"]))
    print("  纯译文: %s" % audit["mono_path"])
    if audit.get("dual_path"):
        print("  对照版: %s" % audit["dual_path"])
    if audit.get("rotation_skipped_pages"):
        print("  旋转页原样保留：%s"
              % ",".join(map(str, audit["rotation_skipped_pages"])), file=sys.stderr)
    if audit.get("lines_overflow"):
        print("  注意：%d 行译文过长已压到最小字号仍超出原行框（复杂版面建议走引擎通路）"
              % audit["lines_overflow"], file=sys.stderr)
    print("  审计:   %s" % audit_path)
    return 0


def cmd_setup(args) -> int:
    from .setup_wizard import status_report, validate_and_write
    from .endpoints import EndpointError
    if args.base_url or args.api_key:
        try:
            res = validate_and_write(
                args.base_url, args.api_key, model=args.model,
                env_file=args.env_file, skip_ping=args.skip_ping)
        except EndpointError as exc:
            print("✘ %s" % exc, file=sys.stderr)
            return 2
        except OSError as exc:
            print("✘ 配置文件写入失败：%s" % exc, file=sys.stderr)
            return 2
        print("✔ 配置已写入 %s（权限 0600）" % res["env_file"])
        print("  连通校验：%s" % res["ping"]["detail"])
        print("  模型：%s" % res["model"])
        return 0
    rep = status_report(env_file=args.env_file)
    print("doc-holmes 环境现状：")
    print("  端点: %s" % (rep.get("endpoint") or
                         "未配置（%s）" % rep.get("endpoint_hint", "缺少配置")))
    print("  引擎: %s" % (rep.get("engine") or
                         "未安装（%s）" % rep.get("engine_hint", "")))
    print("  OCR : %s" % ("可用" if rep.get("ocr") else
                         "未装（%s）" % (rep.get("ocr_hint") or "")))
    print("\n一键配置：doc-holmes setup --base-url <端点> --api-key <你的key> [--model 模型名]")
    print("（零引擎/零key 的轻量路线见：doc-holmes extract --help）")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="doc-holmes",
        description="保持原文排版的外文 PDF 精准翻译（体检分级 A/B/C + BabelDOC 引擎）")
    ap.add_argument("--version", action="version", version="doc-holmes %s" % __version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("triage", help="体检分级：A(高保真)/B(有噪)/C(扫描需OCR)")
    p.add_argument("paths", nargs="+", help="PDF 文件或目录")
    p.add_argument("--sample-pages", type=int, default=3, help="采样页数（默认 3）")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.set_defaults(func=cmd_triage)

    p = sub.add_parser("translate", help="翻译单个 PDF（输出 双语对照 + 纯译文）")
    p.add_argument("pdf", help="输入 PDF 路径")
    p.add_argument("-o", "--output", help="输出目录（默认输入旁 _translated/）")
    p.add_argument("--lang-in", default="en", help="源语言（默认 en）")
    p.add_argument("--lang-out", default="zh", help="目标语言（默认 zh）")
    p.add_argument("--pages", help="页范围，如 1-5")
    p.add_argument("--tier", choices=["auto", "A", "B", "C"], default="auto",
                   help="强制分级（默认 auto 体检决定）")
    p.add_argument("--ocr", choices=["auto", "off"], default="auto",
                   help="C 级（扫描件）OCR 通道开关（默认 auto）")
    p.add_argument("--ocr-lang", default="eng", help="OCR 语言包（默认 eng，可用 eng+chi_sim）")
    p.add_argument("--no-dual", action="store_true", help="不输出双语对照版")
    p.add_argument("--no-mono", action="store_true", help="不输出纯译文版")
    p.add_argument("--qps", type=int, default=None, help="翻译请求速率（默认 4，防限流）")
    p.add_argument("--timeout-s", type=int, default=None, help="单文件超时秒数")
    p.add_argument("--repair", choices=["auto", "on", "off"], default="auto",
                   help="B 级图层重复检测（只读，任何模式都不改 PDF；auto=仅 B 级；"
                        "on=全文档强制含 A 级；off=关闭）")
    p.add_argument("--no-glossary", action="store_true",
                   help="关闭自动术语抽取（大文档该阶段可能超时；术语一致性会略降）")
    p.add_argument("--part-pages", type=int, default=None,
                   help="分段翻译每段页数（0=不分段；默认自动：≥40 页按 25 页/段）")
    p.add_argument("--glossary", choices=["auto", "off"], default="auto",
                   help="术语抽取策略（auto=大文档自动跳过；off=始终跳过）")
    p.add_argument("--no-medical-glossary", action="store_true",
                   help="关闭内置医学术语表注入（en→zh 时默认注入核心术语，提升一致性）")
    p.add_argument("--glossaries-file", action="append", default=None, metavar="CSV",
                   help="用户自定义术语表 csv（source,target,tgt_lng；可重复叠加）")
    p.add_argument("--no-ocr-proofread", action="store_true",
                   help="关闭 C 级 OCR 文本的 LLM 错字校对（默认开，走你配置的端点）")
    p.add_argument("--password", default=None, help="加密 PDF 的密码（自动 qpdf 解密）")
    p.add_argument("--seed-terms", action="store_true",
                   help="开启术语自适应种子（实验性，默认关）：抽取文档高频术语，"
                        "经你配置的端点翻译后注入术语表，提升文档内术语一致性；"
                        "个别文档组合可能触发引擎错误，失败时可去掉本旗标重试")
    p.add_argument("--output-format", choices=["pdf", "docx"], default="pdf",
                   help="输出格式：pdf=仅 PDF（默认）；docx=翻译 PDF 追加可编辑 DOCX（需 LibreOffice）")
    p.add_argument("--auto-lang", action="store_true",
                   help="自动检测源语言（默认 en；auto_lang 后覆盖 --lang-in）")
    p.set_defaults(func=cmd_translate)

    p = sub.add_parser("merge", help="合并多个 PDF（分段翻译产物合并回单档）")
    p.add_argument("inputs", nargs="+", help="输入 PDF（按顺序）")
    p.add_argument("-o", "--output", required=True, help="输出 PDF 路径")
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("split", help="按页范围拆分 PDF（如 1-25,26-50）")
    p.add_argument("pdf", help="输入 PDF")
    p.add_argument("--pages", required=True, dest="pages_spec",
                   help="页范围表达式（1-based 含端点，如 1-25,26,30-）")
    p.add_argument("-o", "--output", default=None, help="输出目录（默认输入旁 split_out/）")
    p.set_defaults(func=cmd_split)

    p = sub.add_parser("estimate", help="干跑预估：页数/字符量/分段策略/预计时长（不碰端点）")
    p.add_argument("pdf", help="输入 PDF")
    p.add_argument("--part-pages", type=int, default=25, help="假定的每段页数")
    p.add_argument("--qps", type=float, default=1.0, help="假定请求速率（影响时长预估）")
    p.set_defaults(func=cmd_estimate)

    p = sub.add_parser("batch", help="批量翻译目录下全部 PDF（断点续传 + 审计）")
    p.add_argument("input_dir", help="输入目录（递归收集 PDF）")
    p.add_argument("-o", "--output", required=True, help="输出目录")
    p.add_argument("--workers", type=int, default=1, help="并发数 1-4（默认 1）")
    p.add_argument("--no-resume", action="store_true", help="忽略历史审计强制重跑")
    p.add_argument("--blacklist", nargs="*", default=[], help="黑名单文件路径列表")
    p.add_argument("--lang-in", default="en")
    p.add_argument("--lang-out", default="zh")
    p.add_argument("--qps", type=int, default=None)
    p.add_argument("--tier", choices=["auto", "A", "B", "C"], default="auto")
    p.add_argument("--timeout-s", type=int, default=None)
    p.add_argument("--repair", choices=["auto", "on", "off"], default="auto",
                   help="B 级图层重复检测（只读；默认 auto，on=全文档强制）")
    p.add_argument("--no-glossary", action="store_true",
                   help="关闭自动术语抽取（大文档防超时）")
    p.add_argument("--part-pages", type=int, default=None,
                   help="分段翻译每段页数（默认自动：≥40 页按 25 页/段）")
    p.add_argument("--glossary", choices=["auto", "off"], default="auto")
    p.add_argument("--no-medical-glossary", action="store_true")
    p.add_argument("--glossaries-file", action="append", default=None, metavar="CSV")
    p.add_argument("--password", default=None,
                   help="加密 PDF 的密码（自动 qpdf 解密，批量全分级生效）")
    p.add_argument("--no-ocr-proofread", action="store_true",
                   help="关闭 C 级 OCR 文本的 LLM 错字校对（默认开，走你配置的端点）")
    p.add_argument("--seed-terms", action="store_true",
                   help="开启术语自适应种子（实验性，默认关，同 translate）")
    p.add_argument("--auto-lang", action="store_true",
                   help="自动检测源语言（batch 通路）")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=cmd_batch)

    p = sub.add_parser("report", help="从 batch 输出目录汇总 report.md")
    p.add_argument("outdir", help="batch 的输出目录（含 audit.jsonl）")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("selfcheck", help="环境自检：依赖/引擎/OCR/GPU/端点")
    p.add_argument("--net", action="store_true", help="附带真实端点连通性探测")
    p.set_defaults(func=cmd_selfcheck)

    p = sub.add_parser("extract", help="零依赖直翻·步骤一：行级抽取（免引擎免key，仅 A 级）")
    p.add_argument("pdf", help="输入 PDF")
    p.add_argument("-o", "--output", help="输出目录（默认输入旁 _direct/）")
    p.add_argument("--pages", help="页范围，如 1-5")
    p.add_argument("--lang-out", default="zh", help="目标语言标记（默认 zh）")
    p.add_argument("--force-b", action="store_true",
                   help="B 级（图层有噪）显式放行——redaction 在重叠字形下可能损字，后果自担")
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("apply", help="零依赖直翻·步骤二：译文 JSON 回填（离线，保图保矢量）")
    p.add_argument("json", help="extract 产出的 doc.direct.json（译文已填入 translated）")
    p.add_argument("-o", "--output", help="输出目录（默认 JSON 旁 direct_out/）")
    p.add_argument("--dual", action="store_true", help="追加左右对照版式（左原文右译文）")
    p.add_argument("--pdf", default=None, help="源 PDF 被移动时显式指定（sha256 必须一致）")
    p.add_argument("--name", default=None, help="输出文件主干名（默认沿用源文件名）")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("setup", help="一键配置：写端点配置+连通校验+引擎指引（绝不代装任何包）")
    p.add_argument("--base-url", default=None, help="你的 OpenAI 兼容端点")
    p.add_argument("--api-key", default=None, help="你的 API key")
    p.add_argument("--model", default=None, help="模型名（默认 glm-4.5-flash）")
    p.add_argument("--env-file", default=None,
                   help="配置文件路径（默认 ~/.config/doc-holmes/env；合并写入会剥除既有注释行）")
    p.add_argument("--skip-ping", action="store_true",
                   help="跳过连通校验强制写入（内网白名单等场景）")
    p.set_defaults(func=cmd_setup)
    return ap


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
