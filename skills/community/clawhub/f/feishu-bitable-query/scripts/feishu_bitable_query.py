#!/usr/bin/env python3
"""
飞书 Bitable 通用查询工具
支持 filter、sort、字段选择、自定义输出格式、全量分页

用法:
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY [options]

示例:
  # 基本查询
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY --all-pages

  # 带 filter
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --filter 'CurrentValue.[状态]="执行中"' --all-pages

  # 指定返回字段
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --fields '["任务描述","状态","更新"]' --all-pages

  # 自定义 compact 输出（只输出指定字段的精简 JSON）
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --compact-fields '["任务描述","任务状态","更新"]' --all-pages

  # 输出为 JSONL（每行一条记录，方便管道处理）
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --format jsonl --all-pages

  # 输出为 TSV 表格
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --compact-fields '["Issue ID","描述","状态"]' --format tsv --all-pages

  # 统计模式（只输出总数）
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --filter 'CurrentValue.[状态]="执行中"' --count

  # 通过 view_id 使用视图自带的筛选排序
  python3 feishu_bitable_query.py --app-token XXX --table-id YYY \
    --view-id vewXXX --all-pages
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import os
import re
from datetime import datetime, timezone, timedelta

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")


def get_credentials():
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    feishu = config.get("channels", {}).get("feishu", {})
    return feishu.get("appId"), feishu.get("appSecret")


def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise Exception(f"Auth failed: {result}")
    return result["tenant_access_token"]


def list_records(token, app_token, table_id, filter_expr=None, sort=None,
                 page_size=100, page_token=None, field_names=None, view_id=None):
    """GET /records — 使用公式语法 filter"""
    base_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"

    params = {"page_size": str(page_size)}
    if page_token:
        params["page_token"] = page_token
    if filter_expr:
        params["filter"] = filter_expr
    if sort:
        params["sort"] = sort
    if field_names:
        params["field_names"] = field_names
    if view_id:
        params["view_id"] = view_id

    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 0:
        raise Exception(f"API error: {result.get('msg')} (code: {result.get('code')})")

    return result.get("data", {})


def search_records(token, app_token, table_id, filter_info=None, sort=None,
                   page_size=100, page_token=None, field_names=None, view_id=None):
    """POST /records/search — 使用 JSON 结构体 filter（支持日期 isGreater/isLess 等）"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search?page_size={page_size}"
    if page_token:
        url += f"&page_token={page_token}"

    body = {}
    if filter_info:
        body["filter"] = filter_info
    if sort:
        body["sort"] = sort
    if field_names:
        body["field_names"] = field_names if isinstance(field_names, list) else json.loads(field_names)
    if view_id:
        body["view_id"] = view_id

    req = urllib.request.Request(url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 0:
        raise Exception(f"Search API error: {result.get('msg')} (code: {result.get('code')})")

    return result.get("data", {})


def format_field_value(val):
    """将 Bitable 字段值转为可读字符串"""
    if val is None:
        return ""
    if isinstance(val, (str, int, float, bool)):
        return str(val)
    if isinstance(val, list):
        # User 字段: [{name, id, ...}]
        if val and isinstance(val[0], dict):
            if "name" in val[0]:
                return ", ".join(u.get("name", "?") for u in val)
            # Search API text 字段: [{text: "xxx", type: "text"}, {text: "url", type: "url"}]
            if "type" in val[0] and "text" in val[0]:
                return "".join(str(u.get("text") or "") for u in val).strip()
            if "text" in val[0]:
                return ", ".join(str(u.get("text") or "?") for u in val)
        # MultiSelect: ["optXXX", ...] — 保持原值
        return ", ".join(str(v) for v in val)
    if isinstance(val, dict):
        # User 字段（单人）: {users: [{name, id}]}
        users = val.get("users", [])
        if users:
            return ", ".join(u.get("name", "?") for u in users)
        # Search API link 字段: {link_record_ids: [...], text: "xxx"} 或无 text
        if "link_record_ids" in val:
            return val.get("text", "")
        # URL 字段: {text, link}
        if "text" in val:
            return val["text"]
        # Mention 字段
        if "link" in val:
            return val["link"]
        return json.dumps(val, ensure_ascii=False)
    return str(val)


def ts_to_str(ts):
    """毫秒时间戳转日期字符串"""
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return str(ts)


def extract_compact(fields, compact_field_list):
    """从 fields 中提取指定字段，自动格式化"""
    result = {}
    for fname in compact_field_list:
        val = fields.get(fname)
        # 特殊处理时间戳字段（常见名称）
        if fname in ("更新", "创建时间", "开始时间", "结束时间") and isinstance(val, (int, float)):
            result[fname] = ts_to_str(val)
        else:
            result[fname] = format_field_value(val)
    return result


def parse_time_filters(expr_list):
    """解析 --time-filter 参数列表，返回过滤函数列表。

    格式: 字段名:规则
    规则支持:
      Nd   — 最近 N 天内（前后各 N 天）
      Nd+  — 未来 N 天内
      Nd-  — 过去 N 天内
      >YYYY-MM-DD  — 晚于指定日期
      <YYYY-MM-DD  — 早于指定日期
      YYYY-MM-DD~YYYY-MM-DD — 日期范围

    示例:
      结束时间:14d    — 结束时间在前后 14 天内
      更新:30d-       — 更新在过去 30 天内
      结束时间:>2026-02-16
      开始时间:2026-01-01~2026-03-01
    """
    filters = []
    now = datetime.now(timezone.utc)

    for expr in expr_list:
        if ":" not in expr:
            sys.stderr.write(f"Warning: invalid time-filter '{expr}', skipping\n")
            continue

        field_name, rule = expr.split(":", 1)

        # Nd / Nd+ / Nd-
        m = re.match(r'^(\d+)d([+-]?)$', rule)
        if m:
            days = int(m.group(1))
            direction = m.group(2)
            if direction == '+':
                ts_min = int(now.timestamp() * 1000)
                ts_max = int((now + timedelta(days=days)).timestamp() * 1000)
            elif direction == '-':
                ts_min = int((now - timedelta(days=days)).timestamp() * 1000)
                ts_max = int(now.timestamp() * 1000)
            else:
                ts_min = int((now - timedelta(days=days)).timestamp() * 1000)
                ts_max = int((now + timedelta(days=days)).timestamp() * 1000)
            filters.append((field_name, ts_min, ts_max))
            continue

        # >YYYY-MM-DD
        m = re.match(r'^>(\d{4}-\d{2}-\d{2})$', rule)
        if m:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            ts_min = int(dt.timestamp() * 1000)
            ts_max = None
            filters.append((field_name, ts_min, ts_max))
            continue

        # <YYYY-MM-DD
        m = re.match(r'^<(\d{4}-\d{2}-\d{2})$', rule)
        if m:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            ts_min = None
            ts_max = int(dt.timestamp() * 1000)
            filters.append((field_name, ts_min, ts_max))
            continue

        # YYYY-MM-DD~YYYY-MM-DD
        m = re.match(r'^(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})$', rule)
        if m:
            dt1 = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            dt2 = datetime.strptime(m.group(2), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            ts_min = int(dt1.timestamp() * 1000)
            ts_max = int(dt2.timestamp() * 1000)
            filters.append((field_name, ts_min, ts_max))
            continue

        sys.stderr.write(f"Warning: unrecognized time-filter rule '{rule}' for field '{field_name}', skipping\n")

    return filters


def apply_time_filters(fields_raw, time_filters):
    """对原始 fields 数据应用时间过滤。返回 True 表示保留。"""
    for field_name, ts_min, ts_max in time_filters:
        val = fields_raw.get(field_name)
        if val is None:
            return False
        try:
            ts = int(val)
        except (ValueError, TypeError):
            return False
        if ts_min is not None and ts < ts_min:
            return False
        if ts_max is not None and ts > ts_max:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="飞书 Bitable 通用查询工具")
    parser.add_argument("--app-token", required=True, help="Bitable app token")
    parser.add_argument("--table-id", required=True, help="Table ID")
    parser.add_argument("--filter", help="Filter expression (公式语法, 走 GET list API)")
    parser.add_argument("--filter-json", help="JSON filter (结构体语法, 走 POST search API, 支持日期 isGreater/isLess)")
    parser.add_argument("--sort", help="Sort expression")
    parser.add_argument("--page-size", type=int, default=500, help="Page size (1-500, default 500)")
    parser.add_argument("--page-token", help="Pagination token (for manual pagination)")
    parser.add_argument("--fields", help='要从 API 获取的字段, JSON array, e.g. \'["a","b"]\'')
    parser.add_argument("--view-id", help="View ID (使用视图自带的筛选排序)")
    parser.add_argument("--all-pages", action="store_true", help="自动拉取所有页")
    parser.add_argument("--count", action="store_true", help="只输出总数")

    # 输出格式
    parser.add_argument("--compact-fields", help='精简输出的字段列表, JSON array, e.g. \'["描述","状态"]\'')
    parser.add_argument("--format", choices=["json", "jsonl", "tsv"], default="json",
                        help="输出格式: json (default), jsonl (每行一条), tsv (表格)")
    parser.add_argument("--include-id", action="store_true", help="输出中包含 record_id")
    parser.add_argument("--time-filter", action="append", default=[],
                        help="本地时间过滤 (可多次使用). 格式: 字段名:规则. "
                             "规则: Nd(前后N天) Nd+(未来N天) Nd-(过去N天) "
                             ">YYYY-MM-DD <YYYY-MM-DD YYYY-MM-DD~YYYY-MM-DD")

    args = parser.parse_args()

    # Auth
    app_id, app_secret = get_credentials()
    token = get_tenant_access_token(app_id, app_secret)

    compact_fields = json.loads(args.compact_fields) if args.compact_fields else None
    time_filters = parse_time_filters(args.time_filter) if args.time_filter else []
    filter_info = json.loads(args.filter_json) if args.filter_json else None
    use_search_api = filter_info is not None

    all_records = []
    filtered_count = 0
    page_token = args.page_token
    page = 0

    while True:
        page += 1
        if use_search_api:
            data = search_records(
                token, args.app_token, args.table_id,
                filter_info=filter_info,
                sort=args.sort,
                page_size=args.page_size,
                page_token=page_token,
                field_names=args.fields,
                view_id=args.view_id,
            )
        else:
            data = list_records(
                token, args.app_token, args.table_id,
                filter_expr=args.filter,
                sort=args.sort,
                page_size=args.page_size,
                page_token=page_token,
                field_names=args.fields,
                view_id=args.view_id,
            )

        items = data.get("items", [])
        total = data.get("total", 0)
        has_more = data.get("has_more", False)

        sys.stderr.write(f"Page {page}: {len(items)} records (total in table: {total})\n")

        if args.count and page == 1:
            print(total)
            return

        for item in items:
            fields = item.get("fields", {})
            record_id = item.get("record_id", "")

            # 本地时间过滤（在 compact 转换之前，用原始时间戳）
            if time_filters and not apply_time_filters(fields, time_filters):
                filtered_count += 1
                continue

            if compact_fields:
                row = extract_compact(fields, compact_fields)
                if args.include_id:
                    row = {"record_id": record_id, **row}
            else:
                row = item
                if not args.include_id and "record_id" not in (compact_fields or []):
                    pass  # keep full record as-is

            all_records.append(row)

        if not args.all_pages or not has_more:
            break
        page_token = data.get("page_token")
        if not page_token:
            break

    if time_filters:
        sys.stderr.write(f"Fetched {len(all_records)} records (filtered out {filtered_count})\n")
    else:
        sys.stderr.write(f"Fetched {len(all_records)} records total\n")

    # Output
    if args.format == "jsonl":
        for row in all_records:
            print(json.dumps(row, ensure_ascii=False))
    elif args.format == "tsv":
        if compact_fields:
            header_fields = (["record_id"] if args.include_id else []) + compact_fields
        elif all_records:
            header_fields = list(all_records[0].keys()) if isinstance(all_records[0], dict) else []
        else:
            header_fields = []
        print("\t".join(header_fields))
        for row in all_records:
            if isinstance(row, dict):
                vals = []
                for h in header_fields:
                    v = row.get(h, row.get("fields", {}).get(h, ""))
                    if isinstance(v, str):
                        vals.append(v.replace("\t", " ").replace("\n", " "))
                    else:
                        vals.append(format_field_value(v).replace("\t", " ").replace("\n", " "))
                print("\t".join(vals))
    else:  # json
        if not args.all_pages and page == 1:
            output = {
                "total": total,
                "has_more": has_more,
                "page_token": data.get("page_token"),
                "count": len(all_records),
                "records": all_records,
            }
        else:
            output = all_records
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
