#!/usr/bin/env python3
"""数据采集脚本 - 支持多种数据源统一接入"""

import argparse
import json
import os
import sys
from datetime import date, timedelta

yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/data-sources.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] 配置文件不存在: {CONFIG_PATH}")
        print("请先创建 config/data-sources.json，参考 references/data-sources.md")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def collect_mysql(source):
    try:
        from sqlalchemy import create_engine, text
        url = f"mysql+pymysql://{source['user']}:{os.path.expandvars(source['password'])}@{source['host']}:{source.get('port', 3306)}/{source['database']}"
        engine = create_engine(url, connect_args={"connect_timeout": source.get("connect_timeout", 10)})
        results = {}
        with engine.connect() as conn:
            for key, sql in source.get("queries", {}).items():
                row = conn.execute(text(sql)).fetchone()
                results[key] = dict(row._mapping) if row else {}
        return results
    except Exception as e:
        print(f"[ERROR] MySQL 采集失败 ({source['name']}): {e}")
        return {}


def collect_api(source):
    try:
        import requests
        headers = {k: os.path.expandvars(v) for k, v in source.get("headers", {}).items()}
        params = {k: v.replace("{yesterday}", yesterday) for k, v in source.get("params", {}).items()}
        resp = requests.request(source.get("method", "GET"), source["url"], headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # 按 mapping 提取字段
        result = {}
        for field, path in source.get("mapping", {}).items():
            keys = path.split(".")
            val = data
            for k in keys:
                val = val.get(k, {}) if isinstance(val, dict) else {}
            result[field] = val
        return result
    except Exception as e:
        print(f"[ERROR] API 采集失败 ({source['name']}): {e}")
        return {}


def collect_csv(source):
    try:
        import pandas as pd
        df = pd.read_csv(source["path"], encoding=source.get("encoding", "utf-8"))
        df[source["date_column"]] = pd.to_datetime(df[source["date_column"]]).dt.strftime("%Y-%m-%d")
        row = df[df[source["date_column"]] == yesterday]
        if row.empty:
            return {}
        return row[source.get("value_columns", [])].iloc[0].to_dict()
    except Exception as e:
        print(f"[ERROR] CSV 采集失败 ({source['name']}): {e}")
        return {}


def collect_source(source):
    t = source["type"]
    if t in ("mysql", "postgresql"):
        return collect_mysql(source)
    elif t == "api":
        return collect_api(source)
    elif t in ("csv", "excel"):
        return collect_csv(source)
    else:
        print(f"[WARN] 暂不支持的数据源类型: {t}")
        return {}


def cmd_validate(args):
    config = load_config()
    sources = config.get("sources", [])
    target = [s for s in sources if s["name"] == args.source] if args.source else sources
    for s in target:
        print(f"验证数据源: {s['name']} ({s['type']}) ...", end=" ")
        result = collect_source(s)
        print("✓ OK" if result is not None else "✗ FAIL")


def cmd_collect(args):
    config = load_config()
    sources = config.get("sources", [])
    if not args.all and args.source:
        sources = [s for s in sources if s["name"] == args.source]
    all_data = {}
    for s in sources:
        print(f"采集: {s['name']} ...", end=" ")
        data = collect_source(s)
        all_data[s["name"]] = data
        print(f"✓ {len(data)} 个字段")
    out_path = os.path.join(os.path.dirname(__file__), f"../reports/data-{yesterday}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存: {out_path}")


def cmd_test(args):
    print(f"测试 SQL: {args.query}")
    config = load_config()
    db_sources = [s for s in config.get("sources", []) if s["type"] in ("mysql", "postgresql")]
    if not db_sources:
        print("[ERROR] 未找到数据库数据源")
        return
    s = db_sources[0]
    s_copy = dict(s, queries={"test": args.query})
    result = collect_mysql(s_copy)
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="决策简报虾 - 数据采集脚本")
    sub = parser.add_subparsers(dest="cmd")

    p_validate = sub.add_parser("validate", help="验证数据源连接")
    p_validate.add_argument("--source", help="指定数据源名称，不填则验证所有")

    p_collect = sub.add_parser("collect", help="采集数据")
    p_collect.add_argument("--source", help="指定数据源名称")
    p_collect.add_argument("--all", action="store_true", help="采集所有数据源")

    p_test = sub.add_parser("test", help="测试 SQL 查询")
    p_test.add_argument("--query", required=True, help="SQL 语句")

    args = parser.parse_args()
    if args.cmd == "validate":
        cmd_validate(args)
    elif args.cmd == "collect":
        cmd_collect(args)
    elif args.cmd == "test":
        cmd_test(args)
    else:
        parser.print_help()
