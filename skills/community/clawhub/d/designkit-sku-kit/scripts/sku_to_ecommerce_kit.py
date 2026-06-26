#!/usr/bin/env python3
"""
SKU -> DesignKit 套图流水线（Walmart / MercadoLibre）

功能：
1) 按 SKU 从数据库读取基础信息（标题、图片URL、文案）
2) 自动映射到 DesignKit 电商套图接口参数
3) 跑通 style_create -> style_poll -> render_submit -> render_poll 全流程

依赖：
- psycopg2
- 环境变量 DESIGNKIT_OPENCLAW_AK

可选环境变量（数据库）：
- DB_HOST / DB_PORT / DB_NAME / DB_USER / DB_PASSWORD / DB_SSLMODE

可选参数：
- --env-file 指定 .env 文件（默认会尝试读取 codex 工具的 .env）
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

DEFAULT_ENV_CANDIDATES = [
    "/root/.openclaw/workspace-codex/sql_flow/search_flow_yibai/.env",
    "/root/.openclaw/workspace-main/.env",
]

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGNKIT_SCRIPT = PROJECT_ROOT / "scripts" / "ecommerce_product_kit.py"

TARGET_PRESETS = {
    "walmart": {
        "platform": "amazon",
        "market": "US",
        "language": "English",
        "aspect_ratio": "1:1",
    },
    "mercadolibre": {
        "platform": "amazon",
        "market": "ES",
        "language": "Spanish",
        "aspect_ratio": "1:1",
    },
}


@dataclass
class ProductInfo:
    sku: str
    title: str
    image_url: str
    selling_points: str
    raw: Dict[str, Any]


def load_env_file(path: str) -> None:
    p = pathlib.Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k and k not in os.environ:
            os.environ[k] = v


def ensure_db_env(env_file: Optional[str]) -> None:
    if env_file:
        load_env_file(env_file)
    else:
        for c in DEFAULT_ENV_CANDIDATES:
            load_env_file(c)


def db_connect():
    try:
        import psycopg2  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"缺少 psycopg2 依赖: {e}")

    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"数据库配置缺失: {', '.join(missing)}")

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=int(os.environ.get("DB_CONNECT_TIMEOUT", "20")),
        sslmode=os.environ.get("DB_SSLMODE", "prefer"),
    )


def list_columns(conn, table_name: str = "yibai_product") -> List[str]:
    sql = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = %s
    ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        return [r[0] for r in cur.fetchall()]


def pick_first(d: Dict[str, Any], keys: List[str], default: str = "") -> str:
    for k in keys:
        v = d.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return default


def build_selling_points(row: Dict[str, Any]) -> str:
    candidates = [
        "selling_points",
        "selling_point",
        "bullet_points",
        "features",
        "description",
        "description_en",
        "description_cn",
        "title_en",
        "title_cn",
    ]
    text = pick_first(row, candidates)
    if text:
        return text
    title = pick_first(row, ["title_en", "title_cn", "name", "product_name"], "商品")
    return f"{title}，强调核心功能、材质、使用场景与购买理由。"


def query_product_by_sku(conn, sku: str, table_name: str = "yibai_product") -> ProductInfo:
    cols = list_columns(conn, table_name)
    if not cols:
        raise RuntimeError(f"表 {table_name} 不存在或无字段")

    sku_col = "sku" if "sku" in cols else None
    if not sku_col:
        # 尝试常见替代
        for c in ["product_sku", "item_sku", "code"]:
            if c in cols:
                sku_col = c
                break
    if not sku_col:
        raise RuntimeError(f"表 {table_name} 未找到 SKU 字段，现有字段: {', '.join(cols[:20])}...")

    select_cols = cols[:]
    sql = f'SELECT {", ".join(select_cols)} FROM {table_name} WHERE {sku_col} = %s LIMIT 1'

    with conn.cursor() as cur:
        cur.execute(sql, (sku,))
        row = cur.fetchone()
        if not row:
            raise RuntimeError(f"未找到 SKU={sku} 的产品")

    row_map = {c: row[i] for i, c in enumerate(select_cols)}

    title = pick_first(row_map, ["title_en", "title_cn", "product_title", "name", "product_name"], sku)
    image_url = pick_first(
        row_map,
        [
            "main_img",
            "main_image",
            "image_url",
            "img_url",
            "product_image",
            "image",
        ],
    )
    if not image_url:
        raise RuntimeError(f"SKU={sku} 未找到图片URL字段（尝试了 main_img/main_image/image_url/...）")

    selling_points = build_selling_points(row_map)

    return ProductInfo(
        sku=sku,
        title=title,
        image_url=image_url,
        selling_points=selling_points,
        raw=row_map,
    )


def run_designkit(command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        str(DESIGNKIT_SCRIPT),
        command,
        "--input-json",
        json.dumps(payload, ensure_ascii=False),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"{command} 执行失败: {proc.stderr.strip() or proc.stdout.strip()}")

    out_text = proc.stdout.strip() or proc.stderr.strip()
    try:
        return json.loads(out_text)
    except json.JSONDecodeError:
        # 某些情况下 stderr 有进度日志，stdout 才是 JSON
        lines = [x.strip() for x in proc.stdout.splitlines() if x.strip()]
        if lines:
            return json.loads(lines[-1])
        raise RuntimeError(f"{command} 输出非JSON: {out_text[:500]}")


def wait_style(task_id: str, max_wait_sec: int = 180, interval_sec: int = 2) -> Dict[str, Any]:
    payload = {
        "task_id": task_id,
        "max_wait_sec": max_wait_sec,
        "interval_sec": interval_sec,
    }
    return run_designkit("style_poll", payload)


def wait_render(batch_id: str, product_name: str, output_dir: Optional[str]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "batch_id": batch_id,
        "product_name": product_name,
        "max_wait_sec": 600,
        "interval_sec": 3,
    }
    if output_dir:
        payload["output_dir"] = output_dir
    return run_designkit("render_poll", payload)


def run_full_flow(product: ProductInfo, target_preset: str, output_dir: Optional[str]) -> Dict[str, Any]:
    if target_preset not in TARGET_PRESETS:
        raise RuntimeError(f"不支持 target_preset={target_preset}，仅支持: {', '.join(TARGET_PRESETS)}")

    cfg = TARGET_PRESETS[target_preset]

    # Step 1: 风格创建
    style_create_payload = {
        "image": product.image_url,
        "product_info": product.selling_points,
        "platform": cfg["platform"],
        "market": cfg["market"],
        "market_zh": "美国" if cfg["market"] == "US" else "西班牙",
    }
    style_create = run_designkit("style_create", style_create_payload)
    task_id = style_create.get("task_id")
    if not task_id:
        raise RuntimeError(f"style_create 未返回 task_id: {style_create}")

    # Step 2: 风格轮询
    style_poll = wait_style(task_id)

    # 优先选第一套风格
    brand_style = None
    styles = style_poll.get("styles")
    if isinstance(styles, list) and styles:
        first = styles[0]
        if isinstance(first, dict):
            brand_style = first

    # Step 3: 提交渲染
    render_submit_payload: Dict[str, Any] = {
        "image": product.image_url,
        "product_info": product.selling_points,
        "platform": cfg["platform"],
        "market": cfg["market"],
        "language": cfg["language"],
        "aspect_ratio": cfg["aspect_ratio"],
        "style_name": f"{target_preset}_auto",
        "target_preset": target_preset,
    }
    if brand_style:
        render_submit_payload["brand_style"] = brand_style

    render_submit = run_designkit("render_submit", render_submit_payload)
    batch_id = render_submit.get("batch_id")
    if not batch_id:
        raise RuntimeError(f"render_submit 未返回 batch_id: {render_submit}")

    # Step 4: 轮询并下载
    render_poll = wait_render(batch_id, product.title, output_dir)

    return {
        "ok": True,
        "sku": product.sku,
        "title": product.title,
        "image_url": product.image_url,
        "selling_points": product.selling_points,
        "target_preset": target_preset,
        "style_task_id": task_id,
        "batch_id": batch_id,
        "styles_count": len(styles) if isinstance(styles, list) else 0,
        "media_urls": render_poll.get("media_urls", []),
        "local_paths": render_poll.get("local_paths", []),
        "output_dir": render_poll.get("output_dir"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SKU -> DesignKit 套图流水线")
    parser.add_argument("--sku", required=True, help="产品 SKU")
    parser.add_argument("--target-preset", default="walmart", choices=["walmart", "mercadolibre"], help="目标平台预设")
    parser.add_argument("--env-file", default="", help="可选 .env 文件路径")
    parser.add_argument("--table", default="yibai_product", help="产品表名，默认 yibai_product")
    parser.add_argument("--output-dir", default="", help="套图输出目录")
    parser.add_argument("--dry-run", action="store_true", help="仅查询SKU，不调用DesignKit")
    args = parser.parse_args()

    ensure_db_env(args.env_file or None)

    if not os.environ.get("DESIGNKIT_OPENCLAW_AK"):
        raise RuntimeError("缺少 DESIGNKIT_OPENCLAW_AK，请先 export DESIGNKIT_OPENCLAW_AK=你的AK")

    conn = db_connect()
    try:
        product = query_product_by_sku(conn, args.sku, args.table)
    finally:
        conn.close()

    if args.dry_run:
        print(
            json.dumps(
                {
                    "ok": True,
                    "mode": "dry_run",
                    "sku": product.sku,
                    "title": product.title,
                    "image_url": product.image_url,
                    "selling_points": product.selling_points,
                    "raw_preview_keys": list(product.raw.keys())[:30],
                },
                ensure_ascii=False,
            )
        )
        return

    result = run_full_flow(product, args.target_preset, args.output_dir or None)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
