from __future__ import annotations

from typing import Any

from cdf.ai.searchDriver import guess_model, search_driver
from printer_store import PrinterRecord, get_printer_by_ip, update_printer_driver


def build_driver_query(record: PrinterRecord, explicit_query: str | None = None) -> str:
    """优先使用已发现型号，其次名称，最后才使用显式补充或 IP。"""
    if explicit_query:
        query = explicit_query.strip()
        if query:
            return query
    for candidate in (record.model, record.name, record.ip):
        value = candidate.strip()
        if value:
            return value
    return record.ip


def fetch_driver_candidates(query: str, limit: int = 5) -> tuple[str, list[dict[str, object]]]:
    """根据查询词生成型号猜测并请求驱动候选列表。"""
    guessed = guess_model(query)
    results = search_driver(query=query, guessed_model=guessed, limit=limit)
    return guessed, results


def print_driver_candidates(query: str, guessed_model: str, results: list[dict[str, object]]) -> None:
    """统一输出驱动候选列表。"""
    print("驱动候选：")
    print(f"输入: {query}")
    print(f"猜测型号: {guessed_model}")
    if not results:
        print("未找到驱动候选。")
        return
    for idx, item in enumerate(results, start=1):
        manufacturer = str(item.get("manufacturer", "") or "-")
        match_level = str(item.get("match_level", "") or "-")
        installed = item.get("installed")
        desc = str(item.get("desc", "") or "-")
        installed_text = "-" if installed is None else ("yes" if bool(installed) else "no")
        print(
            f"{idx}. {item['driver']} | 厂商={manufacturer} | 匹配={match_level} | "
            f"已安装={installed_text} | 相似度={item['score']} | 命中词={item['matched_text']} | 描述={desc}"
        )


def choose_driver(results: list[dict[str, object]], picked: int | None = None) -> dict[str, object]:
    """让用户从驱动候选列表中选择一项。"""
    if not results:
        raise ValueError("没有可供选择的驱动候选。")
    if picked is not None:
        if picked < 1 or picked > len(results):
            raise ValueError(f"驱动序号超出范围，应在 1 到 {len(results)} 之间。")
        return results[picked - 1]

    while True:
        selected = input(f"请选择驱动序号 [1-{len(results)}]，直接回车不选择: ").strip()
        if not selected:
            raise SystemExit("未选择驱动，操作已取消。")
        if selected.isdigit():
            index = int(selected)
            if 1 <= index <= len(results):
                return results[index - 1]
        print("输入无效，请重新输入驱动序号。")


def resolve_and_update_driver_for_ip(
    ip: str,
    explicit_query: str | None = None,
    limit: int = 5,
    picked: int | None = None,
) -> tuple[PrinterRecord, str, str, list[dict[str, object]], dict[str, object]]:
    """按 IP 读取打印机、搜索驱动、选择后回写。"""
    record = get_printer_by_ip(ip)
    if record is None:
        raise FileNotFoundError(f"未找到 IP 为 {ip} 的打印机记录，请先运行 discover.py。")

    query = build_driver_query(record, explicit_query=explicit_query)
    guessed_model, results = fetch_driver_candidates(query, limit=limit)
    chosen = choose_driver(results, picked=picked)
    update_printer_driver(ip, str(chosen["driver"]))
    updated_record = get_printer_by_ip(ip)
    if updated_record is None:
        raise FileNotFoundError(f"已回写驱动，但无法重新读取 IP 为 {ip} 的打印机记录。")
    return updated_record, query, guessed_model, results, chosen
