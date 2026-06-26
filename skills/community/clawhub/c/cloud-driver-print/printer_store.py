from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


# 统一将打印机配置保存到技能目录下的 printers 子目录中，
# 这样在 openclaw、qclaw 这类平台中随技能一起分发和管理更直接。
REGISTRY_DIR = Path(__file__).resolve().parent / "printers"


@dataclass
class PrinterRecord:
    """描述一台打印机的基础信息。"""

    name: str
    ip: str
    port: int = 9100
    model: str = ""
    driver: str = ""
    notes: str = ""

    def to_markdown(self) -> str:
        """将打印机信息序列化为 Markdown 文本，便于人工查看和后续读取。"""
        lines = [
            f"# {self.name}",
            "",
            f"- Name: {self.name}",
            f"- IP: {self.ip}",
            f"- Port: {self.port}",
            f"- Model: {self.model}",
            f"- Driver: {self.driver}",
        ]
        if self.notes:
            lines.append(f"- Notes: {self.notes}")
        lines.append("")
        return "\n".join(lines)


def ensure_registry_dir() -> Path:
    """确保打印机登记目录存在。"""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    return REGISTRY_DIR


def slugify(name: str) -> str:
    """将打印机名称转换为适合文件名的安全字符串。"""
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-")
    return base or "printer"


def printer_file(name: str) -> Path:
    """根据打印机名称计算其 Markdown 文件路径。"""
    return ensure_registry_dir() / f"{slugify(name)}.md"


def find_printer_by_ip(ip: str) -> Path | None:
    """按 IP 查找已存在的打印机记录文件。"""
    for path in sorted(ensure_registry_dir().glob("*.md")):
        try:
            record = parse_markdown(path)
        except Exception:
            continue
        if record.ip == ip:
            return path
    return None


def get_printer_by_ip(ip: str) -> PrinterRecord | None:
    """按 IP 读取打印机记录。"""
    target = find_printer_by_ip(ip)
    if target is None:
        return None
    return parse_markdown(target)


def save_printer(record: PrinterRecord) -> Path:
    """保存单台打印机信息到 Markdown 文件，存在同 IP 记录时原地更新。"""
    target = find_printer_by_ip(record.ip) or printer_file(record.name)
    if target.exists():
        current = parse_markdown(target)
        record = PrinterRecord(
            name=record.name or current.name,
            ip=record.ip or current.ip,
            port=record.port or current.port,
            model=record.model or current.model,
            driver=record.driver or current.driver,
            notes=record.notes or current.notes,
        )
    target.write_text(record.to_markdown(), encoding="utf-8")
    return target


def update_printer_driver(ip: str, driver: str) -> Path:
    """按 IP 更新打印机驱动名称。"""
    target = find_printer_by_ip(ip)
    if target is None:
        raise FileNotFoundError(f"未找到 IP 为 {ip} 的打印机记录。")
    record = parse_markdown(target)
    record.driver = driver
    target.write_text(record.to_markdown(), encoding="utf-8")
    return target


def parse_markdown(path: Path) -> PrinterRecord:
    """从单个 Markdown 文件反向解析打印机记录。"""
    content = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for line in content.splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        fields[key.strip().lower()] = value.strip()

    name = fields.get("name") or path.stem
    ip = fields.get("ip", "")
    port = int(fields.get("port", "9100"))
    model = fields.get("model", "")
    driver = fields.get("driver", "")
    notes = fields.get("notes", "")
    return PrinterRecord(
        name=name,
        ip=ip,
        port=port,
        model=model,
        driver=driver,
        notes=notes,
    )


def list_printers() -> list[PrinterRecord]:
    """列出当前技能目录下已保存的全部打印机。"""
    if not REGISTRY_DIR.exists():
        return []
    return [parse_markdown(path) for path in sorted(REGISTRY_DIR.glob("*.md"))]


def format_printers(records: Iterable[PrinterRecord]) -> str:
    """将打印机列表格式化为命令行可直接展示的文本。"""
    rows = list(records)
    if not rows:
        return "当前没有已保存的打印机。"
    lines = []
    for idx, row in enumerate(rows, start=1):
        model = row.model or "-"
        driver = row.driver or "-"
        lines.append(f"{idx}. {row.name} | {row.ip}:{row.port} | model={model} | driver={driver}")
    return "\n".join(lines)
