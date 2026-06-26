from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from cdf.ai.skillPrint import convert_url_to_pdf, print_for_skill, upload_file_mcp
from connect_printer import test_connection
from driver_workflow import print_driver_candidates, resolve_and_update_driver_for_ip
from printer_store import PrinterRecord, format_printers, get_printer_by_ip, list_printers, save_printer


PAPER_PRESETS_MM: dict[str, tuple[float, float]] = {
    "A3": (297.0, 420.0),
    "A4": (210.0, 297.0),
    "A5": (148.0, 210.0),
    "LETTER": (215.9, 279.4),
    "LEGAL": (215.9, 355.6),
}


def _ensure_record(ip: str, name: str | None) -> PrinterRecord:
    record = get_printer_by_ip(ip)
    if record is not None:
        return record
    if not name:
        raise FileNotFoundError(f"未找到 IP 为 {ip} 的打印机记录，请先运行 discover.py --ip {ip} 或通过 --name 提供名称。")
    record = PrinterRecord(name=name, ip=ip)
    save_printer(record)
    return record


def _choose_printer_record() -> PrinterRecord:
    records = list_printers()
    if not records:
        raise FileNotFoundError("当前没有已保存的打印机，请先运行 discover.py 扫描或用 discover.py --ip <IP> 登记打印机。")

    print("请选择打印机：")
    print(format_printers(records))
    while True:
        selected = input(f"请输入打印机序号 [1-{len(records)}]，直接回车取消: ").strip()
        if not selected:
            raise SystemExit("未选择打印机，操作已取消。")
        if selected.isdigit():
            index = int(selected)
            if 1 <= index <= len(records):
                return records[index - 1]
        print("输入无效，请重新输入打印机序号。")


def _read_optional_env_json(name: str) -> dict[str, object]:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"环境变量 {name} 不是合法 JSON。") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"环境变量 {name} 必须是 JSON 对象。")
    return parsed


def _prompt_yes_no(prompt: str, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{prompt} [{suffix}]: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes", "1"}:
            return True
        if answer in {"n", "no", "0"}:
            return False
        print("请输入 y 或 n。")


def _prompt_text(prompt: str) -> str:
    return input(f"{prompt}：").strip()


def _prompt_choice(prompt: str, choices: list[str]) -> str:
    labels = "/".join(choices)
    while True:
        answer = input(f"{prompt}（{labels}，直接回车跳过）：").strip().upper()
        if not answer:
            return ""
        if answer in choices:
            return answer
        print("输入无效，请重试。")


def _parse_paper_config(value: str) -> dict[str, object]:
    text = value.strip()
    if not text:
        return {}
    preset = PAPER_PRESETS_MM.get(text.upper())
    if preset:
        width, height = preset
        return {"name": text.upper(), "width": width, "height": height}

    parts = [part.strip() for part in text.split(",")]
    if len(parts) == 3:
        name, width, height = parts
        try:
            return {"name": name, "width": float(width), "height": float(height)}
        except ValueError as exc:
            raise SystemExit("paperConfig 自定义格式应为 名称,宽度,高度，例如 Custom,210,297。") from exc

    raise SystemExit("纸张请输入 A3/A4/A5/Letter/Legal，或自定义格式 名称,宽度,高度。")


def _normalize_print_config(config: dict[str, object]) -> dict[str, object]:
    normalized = dict(config)
    paper = normalized.get("paperConfig")
    if isinstance(paper, str) and paper.strip():
        normalized["paperConfig"] = _parse_paper_config(paper)
    return normalized


def _prompt_print_config() -> dict[str, object]:
    config: dict[str, object] = {}
    copies = _prompt_text("份数 copies（直接回车使用默认）")
    if copies:
        if not copies.isdigit() or int(copies) <= 0:
            raise SystemExit("copies 必须是正整数。")
        config["copies"] = int(copies)

    side = _prompt_choice("单双面 side", ["ONESIDE", "DUPLEX", "TUMBLE"])
    if side:
        config["side"] = side

    color = _prompt_choice("颜色 color", ["COLOR", "MONOCHROME"])
    if color:
        config["color"] = color

    page_ranges = _prompt_text("页码范围 pageRanges（例如 1-3,5，直接回车跳过）")
    if page_ranges:
        config["pageRanges"] = page_ranges

    orientation = _prompt_choice("方向 orientation", ["PORTRAIT", "LANDSCAPE"])
    if orientation:
        config["orientation"] = orientation

    quality = _prompt_choice("质量 quality", ["DRAFT", "LOW", "NORMAL", "HIGH"])
    if quality:
        config["quality"] = quality

    paper = _prompt_text("纸张 paperConfig（A3/A4/A5/Letter/Legal，或 名称,宽度,高度）")
    if paper:
        config["paperConfig"] = _parse_paper_config(paper)

    return config


def _resolve_print_config(no_prompt: bool) -> dict[str, object]:
    config = _normalize_print_config(_read_optional_env_json("CDF_PRINT_CONFIG_JSON"))
    if no_prompt or not sys.stdin.isatty():
        return config
    if not _prompt_yes_no("是否需要自定义打印配置", default=False):
        return config
    prompted = _prompt_print_config()
    merged = dict(config)
    merged.update(prompted)
    return merged


def _local_convert_to_pdf(file_path: Path) -> Path:
    """通过 LibreOffice 将文件本地转换为 PDF，返回 PDF 文件路径。"""
    outdir = Path(tempfile.gettempdir())
    try:
        result = subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                str(file_path.resolve()),
                "--outdir", str(outdir),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "LibreOffice 未安装，无法本地转换文档。请安装 LibreOffice 后再试。"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("LibreOffice 本地转换超时（60s），文件可能过大或格式异常。")
    pdf_path = outdir / f"{file_path.stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"LibreOffice 转换失败: {result.stderr.strip()}")
    return pdf_path


def _maybe_convert_print_url(file_path: Path, upload_result: dict[str, str]) -> tuple[str, dict[str, str]]:
    """获取可打印的 PDF URL。优先用云端 _cvturl，失败时降级 LibreOffice 本地转换。"""
    if file_path.suffix.lower() == ".pdf":
        return upload_result["url"], {"converted": "false"}

    repo_id = upload_result.get("repoId", "")
    remote_path = upload_result.get("path", "")
    if not repo_id or not remote_path:
        raise RuntimeError("非 PDF 文件打印需要 uploadFileMCP 返回 repoId 和 path。")

    # 优先走云端转换
    try:
        converted_url = convert_url_to_pdf(repo_id=repo_id, path=remote_path)
        return converted_url, {"converted": "true", "repoId": repo_id, "path": remote_path, "method": "_cvturl"}
    except Exception as e:
        print(f"[降级] _cvturl 失败 ({e})，回退到 LibreOffice 本地转换...", file=sys.stderr)

    # 降级：LibreOffice 本地转 PDF，重新上传，再打印
    pdf_path = _local_convert_to_pdf(file_path)
    pdf_upload = upload_file_mcp(pdf_path)
    return pdf_upload["url"], {"converted": "true", "method": "libreoffice"}


def main() -> None:
    parser = argparse.ArgumentParser(description="按技能打印流程执行：上传文件，并通过 printForSkill 完成安装与打印。")
    parser.add_argument("file", help="待打印文件路径。")
    parser.add_argument("--ip", help="目标打印机 IP；未提供时从已保存打印机列表中选择。")
    parser.add_argument("--name", help="打印机名称；当本地尚未保存该 IP 记录时必填。")
    parser.add_argument("--driver", help="显式指定驱动名称；未提供时优先读取已保存驱动。")
    parser.add_argument("--pick", type=int, help="当需要补选驱动时，直接指定驱动序号，从 1 开始。")
    parser.add_argument("--limit", type=int, default=5, help="自动补驱动时最多返回多少条候选驱动。")
    parser.add_argument("--port-serial", help="可选的打印机端口序列号，对应 printer.portSerial。")
    parser.add_argument("--from-sn", help="可选的来源服务器 SN，对应 printer.fromSn。")
    parser.add_argument("--no-config-prompt", action="store_true", help="不交互询问打印配置，只使用默认值或 CDF_PRINT_CONFIG_JSON。")
    parser.add_argument("--skip-connect-check", action="store_true", help="跳过 9100 连通性检查。")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整结果。")
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    record = _ensure_record(args.ip, args.name) if args.ip else _choose_printer_record()
    target_ip = args.ip or record.ip
    driver_name = args.driver or record.driver
    if not driver_name:
        try:
            record, query, guessed, results, chosen = resolve_and_update_driver_for_ip(
                target_ip,
                limit=args.limit,
                picked=args.pick,
            )
        except ValueError as exc:
            raise SystemExit(f"未找到可用驱动，请先确认打印机型号后执行 search_driver.py：{exc}") from exc
        print_driver_candidates(query, guessed, results)
        print(f"已回写驱动: {chosen['driver']}")
        driver_name = record.driver

    if not driver_name:
        raise SystemExit("当前打印机没有可用驱动，请先执行 search_driver.py 搜索并选择驱动后再打印。")

    if not args.skip_connect_check:
        ok, latency_ms, message = test_connection(target_ip, record.port, 3.0)
        if not ok:
            raise SystemExit(f"打印机连通性检查失败: {target_ip}:{record.port} {latency_ms:.1f}ms {message}")

    upload_result = upload_file_mcp(file_path)
    file_url, conversion = _maybe_convert_print_url(file_path, upload_result)
    print_result = print_for_skill(
        driver=driver_name,
        name=args.name or record.name,
        port_addr=target_ip,
        url=file_url,
        raw_port=record.port,
        port_serial=args.port_serial,
        from_sn=args.from_sn,
        file_name=file_path.name,
        config=_resolve_print_config(args.no_config_prompt),
    )

    save_printer(
        PrinterRecord(
            name=args.name or record.name,
            ip=record.ip,
            port=record.port,
            model=record.model,
            driver=driver_name,
            notes=record.notes,
        )
    )

    result = {
        "upload": upload_result,
        "conversion": conversion,
        "printUrl": file_url,
        "print": print_result,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"file_url={upload_result['url']}")
    if conversion.get("converted") == "true":
        print(f"pdf_url={file_url}")
    print(f"success={print_result['success']}")
    print(f"reason={print_result['reason']}")


if __name__ == "__main__":
    main()
