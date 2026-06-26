"""
万能反爬 Skill - OpenClaw 数据导出模块
将采集到的统一 VehicleInfo 数据转为 OpenClaw 兼容格式
支持 JSON / CSV / JSONL 输出
"""

import os
import csv
import json
import logging
from datetime import datetime
from typing import Optional

from config import OPENCLAW_OUTPUT_DIR, OPENCLAW_OUTPUT_FORMAT
from data_models import VehicleInfo, ScrapeResult

logger = logging.getLogger("openclaw_export")


# ─── OpenClaw 数据格式定义 ─────────────────────────────

def vehicle_to_openclaw(vehicle: VehicleInfo) -> dict:
    """
    将 VehicleInfo 转为 OpenClaw 标准文档格式

    OpenClaw 文档结构:
    - url: 来源 URL
    - title: 文档标题
    - content: 主要文本内容（结构化描述）
    - metadata: 附加元数据
    - source: 来源标识
    - timestamp: 采集时间
    """
    # 构建结构化内容描述
    content_parts = []

    if vehicle.title:
        content_parts.append(f"车辆名称: {vehicle.title}")
    if vehicle.brand:
        content_parts.append(f"品牌: {vehicle.brand}")
    if vehicle.series:
        content_parts.append(f"车系: {vehicle.series}")
    if vehicle.model:
        content_parts.append(f"车型: {vehicle.model}")
    if vehicle.year:
        content_parts.append(f"年款: {vehicle.year}款")
    if vehicle.price:
        content_parts.append(f"售价: {vehicle.price}万元")
    if vehicle.original_price:
        content_parts.append(f"新车指导价: {vehicle.original_price}万元")
    if vehicle.mileage:
        content_parts.append(f"里程: {vehicle.mileage}")
    if vehicle.plate_date:
        content_parts.append(f"上牌日期: {vehicle.plate_date}")
    if vehicle.plate_city:
        content_parts.append(f"上牌城市: {vehicle.plate_city}")
    if vehicle.color:
        content_parts.append(f"颜色: {vehicle.color}")

    # 技术参数
    tech_parts = []
    if vehicle.engine:
        tech_parts.append(f"发动机: {vehicle.engine}")
    if vehicle.transmission:
        tech_parts.append(f"变速箱: {vehicle.transmission}")
    if vehicle.fuel_type:
        tech_parts.append(f"燃油类型: {vehicle.fuel_type}")
    if vehicle.drive_type:
        tech_parts.append(f"驱动方式: {vehicle.drive_type}")
    if vehicle.displacement:
        tech_parts.append(f"排量: {vehicle.displacement}")
    if vehicle.body_type:
        tech_parts.append(f"车身类型: {vehicle.body_type}")
    if vehicle.emission_standard:
        tech_parts.append(f"排放标准: {vehicle.emission_standard}")
    if vehicle.seats:
        tech_parts.append(f"座位数: {vehicle.seats}座")

    # 电动车
    if vehicle.battery_capacity:
        tech_parts.append(f"电池容量: {vehicle.battery_capacity}")
    if vehicle.range_km:
        tech_parts.append(f"续航里程: {vehicle.range_km}km")

    if tech_parts:
        content_parts.append("\n--- 技术参数 ---")
        content_parts.extend(tech_parts)

    # 商家信息
    if vehicle.dealer_name:
        content_parts.append(f"\n--- 商家 ---")
        content_parts.append(f"商家: {vehicle.dealer_name}")
        if vehicle.dealer_city:
            content_parts.append(f"城市: {vehicle.dealer_city}")
        if vehicle.dealer_address:
            content_parts.append(f"地址: {vehicle.dealer_address}")

    # 描述
    if vehicle.highlights:
        content_parts.append(f"\n亮点: {vehicle.highlights}")
    if vehicle.description:
        content_parts.append(f"\n描述: {vehicle.description}")

    content = "\n".join(content_parts)

    # OpenClaw 文档
    doc = {
        "url": vehicle.source_url,
        "title": vehicle.title or f"{vehicle.brand} {vehicle.series} {vehicle.year}",
        "content": content,
        "source": f"car_scraper_{vehicle.source}",
        "timestamp": vehicle.scraped_at or datetime.now().isoformat(),
        "metadata": {
            "source_platform": vehicle.source,
            "source_id": vehicle.source_id,
            "vehicle_type": "used_car",
            "brand": vehicle.brand,
            "series": vehicle.series,
            "model": vehicle.model,
            "year": vehicle.year,
            "price_cny_wan": vehicle.price,
            "original_price_cny_wan": vehicle.original_price,
            "mileage": vehicle.mileage,
            "mileage_km": vehicle.mileage_km,
            "fuel_type": vehicle.fuel_type,
            "transmission": vehicle.transmission,
            "body_type": vehicle.body_type,
            "color": vehicle.color,
            "plate_city": vehicle.plate_city,
            "plate_date": vehicle.plate_date,
            "vin": vehicle.vin,
            "emission_standard": vehicle.emission_standard,
            "images": vehicle.images,
            "thumbnail": vehicle.thumbnail,
            "dealer_name": vehicle.dealer_name,
            "dealer_city": vehicle.dealer_city,
            "condition_tags": vehicle.condition_tags,
        },
    }

    # 清理空值
    doc["metadata"] = {k: v for k, v in doc["metadata"].items() if v}

    return doc


# ─── 导出函数 ────────────────────────────────────────

def export_to_json(
    vehicles: list[VehicleInfo],
    filename: str,
    output_dir: Optional[str] = None,
) -> str:
    """导出为 JSON 文件"""
    output_dir = output_dir or OPENCLAW_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    docs = [vehicle_to_openclaw(v) for v in vehicles]
    filepath = os.path.join(output_dir, f"{filename}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    logger.info(f"JSON 导出完成: {filepath} ({len(docs)} 条)")
    return filepath


def export_to_jsonl(
    vehicles: list[VehicleInfo],
    filename: str,
    output_dir: Optional[str] = None,
) -> str:
    """导出为 JSONL 文件（每行一条 JSON，适合大数据量流式处理）"""
    output_dir = output_dir or OPENCLAW_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{filename}.jsonl")

    with open(filepath, "w", encoding="utf-8") as f:
        for v in vehicles:
            doc = vehicle_to_openclaw(v)
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    logger.info(f"JSONL 导出完成: {filepath} ({len(vehicles)} 条)")
    return filepath


def export_to_csv(
    vehicles: list[VehicleInfo],
    filename: str,
    output_dir: Optional[str] = None,
) -> str:
    """导出为 CSV 文件"""
    output_dir = output_dir or OPENCLAW_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{filename}.csv")

    csv_fields = [
        "source", "source_id", "source_url", "title", "brand", "series",
        "model", "year", "price", "original_price", "mileage", "mileage_km",
        "color", "plate_city", "plate_date", "vin",
        "fuel_type", "engine", "transmission", "drive_type", "body_type",
        "displacement", "seats", "emission_standard",
        "battery_capacity", "range_km",
        "dealer_name", "dealer_city", "dealer_phone",
        "thumbnail", "images_count", "condition_tags", "scraped_at",
    ]

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()

        for v in vehicles:
            row = {
                "source": v.source,
                "source_id": v.source_id,
                "source_url": v.source_url,
                "title": v.title,
                "brand": v.brand,
                "series": v.series,
                "model": v.model,
                "year": v.year,
                "price": v.price,
                "original_price": v.original_price,
                "mileage": v.mileage,
                "mileage_km": v.mileage_km,
                "color": v.color,
                "plate_city": v.plate_city,
                "plate_date": v.plate_date,
                "vin": v.vin,
                "fuel_type": v.fuel_type,
                "engine": v.engine,
                "transmission": v.transmission,
                "drive_type": v.drive_type,
                "body_type": v.body_type,
                "displacement": v.displacement,
                "seats": v.seats,
                "emission_standard": v.emission_standard,
                "battery_capacity": v.battery_capacity,
                "range_km": v.range_km,
                "dealer_name": v.dealer_name,
                "dealer_city": v.dealer_city,
                "dealer_phone": v.dealer_phone,
                "thumbnail": v.thumbnail,
                "images_count": len(v.images),
                "condition_tags": "|".join(v.condition_tags),
                "scraped_at": v.scraped_at,
            }
            writer.writerow(row)

    logger.info(f"CSV 导出完成: {filepath} ({len(vehicles)} 条)")
    return filepath


def export_scrape_result(
    result: ScrapeResult,
    output_format: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> list[str]:
    """
    导出单个平台的采集结果

    Args:
        result: 采集结果
        output_format: 输出格式 json/jsonl/csv/all
        output_dir: 输出目录

    Returns:
        导出的文件路径列表
    """
    fmt = output_format or OPENCLAW_OUTPUT_FORMAT
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{result.source}_{timestamp}"

    files = []

    if fmt in ("json", "all", "both"):
        files.append(export_to_json(result.vehicles, base_name, output_dir))

    if fmt in ("jsonl", "all"):
        files.append(export_to_jsonl(result.vehicles, base_name, output_dir))

    if fmt in ("csv", "all", "both"):
        files.append(export_to_csv(result.vehicles, base_name, output_dir))

    return files


def export_all_results(
    results: list[ScrapeResult],
    output_format: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> list[str]:
    """
    导出所有平台的采集结果，同时生成合并文件

    Returns:
        导出的文件路径列表
    """
    all_files = []

    # 分别导出每个平台
    for result in results:
        if result.vehicles:
            files = export_scrape_result(result, output_format, output_dir)
            all_files.extend(files)

    # 合并导出
    all_vehicles = []
    for result in results:
        all_vehicles.extend(result.vehicles)

    if all_vehicles:
        fmt = output_format or OPENCLAW_OUTPUT_FORMAT
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"all_platforms_{timestamp}"
        output_dir = output_dir or OPENCLAW_OUTPUT_DIR

        if fmt in ("json", "all", "both"):
            all_files.append(export_to_json(all_vehicles, base_name, output_dir))
        if fmt in ("jsonl", "all"):
            all_files.append(export_to_jsonl(all_vehicles, base_name, output_dir))
        if fmt in ("csv", "all", "both"):
            all_files.append(export_to_csv(all_vehicles, base_name, output_dir))

    logger.info(f"全部导出完成: {len(all_files)} 个文件, 共 {len(all_vehicles)} 条数据")
    return all_files
