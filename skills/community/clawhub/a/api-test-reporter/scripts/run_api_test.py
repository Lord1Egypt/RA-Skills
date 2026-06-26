#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 API 接口自动化测试执行器 v2.0

用法：
    python run_api_test.py --config test_config.json
    python run_api_test.py --config test_config.json --output ./reports

特性：
- 支持 db_fixture：测试前从 MySQL 数据库加载真实数据，注入 {{占位符}}
- 支持 remove_fixed：在指定用例中移除某个固定参数
- 响应校验默认不校验 HTTP 状态码（ISP 接口规范）
- 兼容云端（response.xxx）和本地（model.xxx）两种返参结构
- 报告模板与数据分离，HTML 极速生成

test_config.json 格式：
{
  "meta": {
    "title": "...", "base_url": "...", "method": "...",
    "version": "6.0", "timeout": 30, "http_method": "POST",
    "url_params": {}
  },
  "fixed_params": {"taxNo": "..."},
  "db_fixture": {
    "connection": {"host":"...", "port":3306, "user":"...", "password":"...", "database":"..."},
    "queries": [
      {
        "name": "sample",
        "sql": "SELECT INV_NUM FROM bw_jms_main1 LIMIT 1",
        "mapping": {"invoiceNumber": "INV_NUM"}
      }
    ]
  },
  "test_cases": [
    {
      "id": "TC_001", "group": "正常流程", "name": "...", "desc": "...",
      "body": {"invoiceNumber": "{{invoiceNumber}}"},
      "expect": {"success": true},
      "remove_fixed": ["可选：要移除的固定参数名"]
    }
  ]
}
"""

import argparse
import json
import os
import re
import sys
import time
import datetime
import requests
from typing import Any, Dict, List, Optional


# ============================================================
# DB Fixture
# ============================================================

def load_db_fixture(cfg: Dict) -> Dict[str, Any]:
    """从 db_fixture 配置连接数据库，执行各 SQL，返回变量映射字典"""
    if not cfg:
        return {}
    conn_cfg = cfg.get("connection", {})
    queries = cfg.get("queries", [])
    if not conn_cfg or not queries:
        return {}

    try:
        import pymysql
    except ImportError:
        print("[WARN] db_fixture 需要 pymysql：pip install pymysql")
        return {}

    vars_map: Dict[str, Any] = {}
    conn = None
    try:
        conn = pymysql.connect(
            host=conn_cfg.get("host", "127.0.0.1"),
            port=int(conn_cfg.get("port", 3306)),
            user=conn_cfg.get("user", "root"),
            password=conn_cfg.get("password", ""),
            database=conn_cfg.get("database", ""),
            charset=conn_cfg.get("charset", "utf8mb4"),
            connect_timeout=10,
        )
        print("[DB] 连接 {}:{}/{}".format(
            conn_cfg.get("host"), conn_cfg.get("port"), conn_cfg.get("database")))

        cur = conn.cursor(pymysql.cursors.DictCursor)
        for q in queries:
            name = q.get("name", "unnamed")
            sql = q.get("sql", "")
            mapping = q.get("mapping", {})
            if not sql:
                continue
            try:
                cur.execute(sql)
                row = cur.fetchone()
                if row:
                    for var_name, col_name in mapping.items():
                        val = row.get(col_name)
                        vars_map[var_name] = str(val) if val is not None else None
                        print("[DB][{}] {}={!r}".format(name, var_name, vars_map[var_name]))
                else:
                    print("[DB][{}] 查询无数据".format(name))
                    for var_name in mapping:
                        vars_map[var_name] = None
            except Exception as e:
                print("[DB][{}] SQL 失败: {}".format(name, e))
        cur.close()
    except Exception as e:
        print("[DB] 连接失败: {}".format(e))
    finally:
        if conn:
            conn.close()
    return vars_map


def apply_fixture(value: Any, vars_map: Dict[str, Any]) -> Any:
    """递归将 {{变量名}} 替换为真实值"""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{{") and stripped.endswith("}}"):
            var_name = stripped[2:-2].strip()
            return vars_map.get(var_name, value)
        def _repl(m):
            v = vars_map.get(m.group(1).strip())
            return str(v) if v is not None else m.group(0)
        return re.sub(r"\{\{(\w+)\}\}", _repl, value)
    elif isinstance(value, dict):
        return {k: apply_fixture(v, vars_map) for k, v in value.items()}
    elif isinstance(value, list):
        return [apply_fixture(item, vars_map) for item in value]
    return value


# ============================================================
# HTTP 请求
# ============================================================

def build_url(meta: Dict) -> str:
    """构建请求 URL（含 query 参数）"""
    base_url = meta["base_url"].rstrip("/")
    parts = []
    if meta.get("method"):
        parts.append("method=" + meta["method"])
    if meta.get("version"):
        parts.append("version=" + str(meta["version"]))
    for k, v in meta.get("url_params", {}).items():
        parts.append("{}={}".format(k, v))
    return base_url + "?" + "&".join(parts) if parts else base_url


def send_request(url: str, body: Dict, timeout: int = 30,
                 http_method: str = "POST") -> Dict:
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    try:
        if http_method.upper() == "GET":
            resp = requests.get(url, params=body, headers=headers, timeout=timeout)
        else:
            resp = requests.post(url, json=body, headers=headers, timeout=timeout)
        try:
            return {"status_code": resp.status_code, "body": resp.json(),
                    "raw": resp.text, "error": None}
        except Exception:
            return {"status_code": resp.status_code, "body": None,
                    "raw": resp.text, "error": "响应非JSON格式"}
    except requests.exceptions.ConnectionError as e:
        return {"status_code": None, "body": None, "raw": None, "error": "连接失败: " + str(e)}
    except requests.exceptions.Timeout:
        return {"status_code": None, "body": None, "raw": None, "error": "请求超时"}
    except Exception as e:
        return {"status_code": None, "body": None, "raw": None, "error": str(e)}


# ============================================================
# 响应校验（默认不校验 HTTP 状态码）
# ============================================================

def _get_nested(data: Any, path: str) -> Any:
    """按点分路径取嵌套值"""
    cur = data
    for p in path.split("."):
        if cur is None:
            return None
        if isinstance(cur, list):
            try:
                cur = cur[int(p)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur


def check_response(resp: Dict, expectations: Dict) -> Dict:
    """
    校验响应，返回 {"passed": bool, "details": [...]}

    规则：
    1. 网络/解析错误 → 直接失败
    2. success 校验：
       - 期望 True  → 检查 success，并检查 invoiceList/response/model 非空
       - 期望 False → 只检查 success=False，不检查数据
    3. response.{field} / model.{field} 路径校验
    4. has_response / check_page_data / error_field_exists → 结构性校验
    5. custom_checks → 自定义路径校验
    6. 默认不校验 HTTP 状态码（除非 expect 中明确配置 http_status）
    """
    details = []
    passed = True

    if resp.get("error"):
        return {"passed": False, "details": ["请求异常: " + resp["error"]]}

    # 仅当 expect 中明确配置 http_status 时才校验（不是默认行为）
    if "http_status" in expectations:
        exp_status = expectations["http_status"]
        act_status = resp["status_code"]
        if act_status == exp_status:
            details.append("[PASS] HTTP状态码 {}".format(act_status))
        else:
            passed = False
            details.append("[FAIL] HTTP状态码期望 {}，实际 {}".format(exp_status, act_status))

    body = resp.get("body")
    if body is None:
        return {"passed": False, "details": details + ["[FAIL] 响应体解析失败"]}

    # ── success 校验 ──
    if "success" in expectations:
        exp = expectations["success"]
        act = body.get("success")
        if act == exp:
            details.append("[PASS] success={}".format(act))
            if exp is True:
                # 云端：response.invoiceList；本地：model.invoiceList；根级别兜底
                invoice_list = None
                resp_data = body.get("response")
                if isinstance(resp_data, dict):
                    invoice_list = resp_data.get("invoiceList")
                if invoice_list is None:
                    model_data = body.get("model")
                    if isinstance(model_data, dict):
                        invoice_list = model_data.get("invoiceList")
                if invoice_list is None:
                    invoice_list = body.get("invoiceList")

                if invoice_list is None:
                    details.append("[SKIP] invoiceList 不存在，跳过非空校验")
                elif len(invoice_list) == 0:
                    passed = False
                    details.append("[FAIL] invoiceList 为空（success=True 但无数据）")
                else:
                    details.append("[PASS] invoiceList 非空，共 {} 条".format(len(invoice_list)))
        else:
            passed = False
            details.append("[FAIL] success 期望 {}，实际 {}".format(exp, act))

    # ── response.{field} / model.{field} 路径校验 ──
    for key, exp_val in expectations.items():
        if key in ("success", "has_response", "check_page_data",
                   "error_field_exists", "response_field", "custom_checks", "http_status"):
            continue
        if "." in key:
            act_val = _get_nested(body, key)
            if str(act_val) == str(exp_val):
                details.append("[PASS] {} = {}".format(key, act_val))
            else:
                passed = False
                details.append("[FAIL] {} 期望 {}，实际 {}".format(key, exp_val, act_val))

    # ── has_response ──
    if expectations.get("has_response"):
        field_name = expectations.get("response_field")
        if field_name:
            data_val = body.get(field_name)
        else:
            data_val = body.get("model")
            field_name = "model"
            if data_val is None:
                data_val = body.get("response")
                field_name = "response"
        if data_val is not None:
            details.append("[PASS] {} 字段存在".format(field_name))
        elif body.get("success") is False:
            details.append("[INFO] {} 为空（业务错误）".format(field_name))
        else:
            passed = False
            details.append("[FAIL] {} 字段为空".format(field_name))

    # ── error_field_exists ──
    if expectations.get("error_field_exists"):
        if body.get("errorResponse") is not None:
            details.append("[PASS] errorResponse 字段存在")
        else:
            passed = False
            details.append("[FAIL] errorResponse 字段不存在")

    # ── check_page_data ──
    if expectations.get("check_page_data"):
        field_name = expectations.get("response_field")
        if field_name:
            data_val = body.get(field_name)
        else:
            data_val = body.get("model")
            field_name = "model"
            if data_val is None:
                data_val = body.get("response")
                field_name = "response"
        if isinstance(data_val, list):
            details.append("[PASS] {} 返回列表，共 {} 条".format(field_name, len(data_val)))
        elif isinstance(data_val, dict):
            cnt = data_val.get("total") or data_val.get("totalCount") or data_val.get("count")
            details.append("[PASS] {} 返回对象{}".format(
                field_name, "，总数={}".format(cnt) if cnt is not None else ""))
        elif data_val is None:
            if body.get("success") is False:
                details.append("[INFO] {} 为空（业务错误）".format(field_name))
            else:
                details.append("[INFO] {} 为空（可能无数据）".format(field_name))

    # ── custom_checks ──
    for chk in expectations.get("custom_checks", []):
        try:
            path = chk.get("path", "")
            op = chk.get("op", "exists")
            exp_val = chk.get("value")
            act_val = _get_nested(body, path)
            if op == "exists":
                ok = act_val is not None
            elif op == "not_exists":
                ok = act_val is None
            elif op == "eq":
                ok = str(act_val) == str(exp_val)
            elif op == "ne":
                ok = str(act_val) != str(exp_val)
            elif op == "contains":
                ok = exp_val in str(act_val)
            elif op == "gt":
                ok = float(act_val) > float(exp_val)
            elif op == "lt":
                ok = float(act_val) < float(exp_val)
            else:
                details.append("[WARN] 未知 op: " + op)
                continue
            label = "[PASS]" if ok else "[FAIL]"
            if not ok:
                passed = False
            details.append("{} 自定义校验 {} {} {} → 实际: {}".format(
                label, path, op, exp_val, act_val))
        except Exception as e:
            details.append("[WARN] 自定义校验异常: " + str(e))

    return {"passed": passed, "details": details}


# ============================================================
# 测试执行
# ============================================================

def run_tests(config: Dict) -> List[Dict]:
    meta = config["meta"]
    fixed = config.get("fixed_params", {})
    test_cases = config["test_cases"]
    url = build_url(meta)
    timeout = meta.get("timeout", 30)
    http_method = meta.get("http_method", "POST")

    # ---- 加载 DB Fixture ----
    fixture_vars: Dict[str, Any] = {}
    if config.get("db_fixture"):
        print("\n[DB] 加载数据库夹具...")
        fixture_vars = load_db_fixture(config["db_fixture"])
        if fixture_vars:
            print("[DB] 已加载 {} 个变量: {}\n".format(
                len(fixture_vars), list(fixture_vars.keys())))
        else:
            print("[DB] 未加载到数据，占位符保持原样\n")

    total = len(test_cases)
    results = []

    print("=" * 60)
    print("  接口测试: " + (meta.get("title") or meta.get("method") or ""))
    print("  请求地址: " + url)
    print("  用例数:   " + str(total))
    print("=" * 60)

    for idx, tc in enumerate(test_cases, 1):
        print("[{:03d}/{}] {} - {}".format(idx, total, tc["id"], tc["name"]))

        merged = {**fixed, **tc.get("body", {})}

        # remove_fixed：移除指定的固定参数
        for key in tc.get("remove_fixed", []):
            merged.pop(key, None)

        if fixture_vars:
            merged = apply_fixture(merged, fixture_vars)

        body = {k: v for k, v in merged.items()
                if v is not None and k != "_override_fixed"}

        start = time.time()
        resp = send_request(url, body, timeout=timeout, http_method=http_method)
        elapsed_ms = round((time.time() - start) * 1000)

        check = check_response(resp, tc.get("expect", {}))
        print("         {}  {}ms".format("[PASS]" if check["passed"] else "[FAIL]", elapsed_ms))

        results.append({
            "id": tc["id"],
            "group": tc.get("group", "未分组"),
            "name": tc["name"],
            "desc": tc.get("desc", ""),
            "request_url": url,
            "request_body": body,
            "expect": tc.get("expect", {}),
            "response_status": resp["status_code"],
            "response_body": resp["body"],
            "response_raw": resp["raw"] if resp["body"] is None else None,
            "response_error": resp["error"],
            "elapsed_ms": elapsed_ms,
            "passed": check["passed"],
            "check_details": check["details"],
        })

    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    print("\n" + "=" * 60)
    print("  完成: {}  通过: {}  失败: {}  通过率: {}%".format(
        total, passed, failed,
        round(passed / total * 100, 1) if total else 0))
    print("=" * 60)
    return results


# ============================================================
# 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="通用 API 接口自动化测试执行器")
    parser.add_argument("--config", required=True, help="测试配置文件路径（JSON）")
    parser.add_argument("--output", default=None, help="报告输出目录（默认与配置文件同目录）")
    args = parser.parse_args()

    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        print("[ERROR] 配置文件不存在: " + config_path)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    results = run_tests(config)

    out_dir = args.output if args.output else os.path.dirname(config_path)
    os.makedirs(out_dir, exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = config["meta"].get("method", "api_test").replace(".", "_")
    json_path = os.path.join(out_dir, "test_results_{}_{}.json".format(safe_title, ts))
    html_path = os.path.join(out_dir, "test_report_{}_{}.html".format(safe_title, ts))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print("[OK] JSON 结果: " + json_path)

    # 调用报告生成器
    report_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_report.py")
    if os.path.exists(report_script):
        import subprocess
        subprocess.run(
            [sys.executable, report_script,
             "--results", json_path,
             "--output", html_path,
             "--title", config["meta"].get("title", "接口测试报告"),
             "--method", config["meta"].get("method", ""),
             "--url", config["meta"].get("base_url", ""),
             "--version", str(config["meta"].get("version", "")),
             ],
            check=True
        )
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_report", report_script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        meta = config["meta"]
        mod.generate_report(
            results=results,
            output_path=html_path,
            title=meta.get("title", "接口测试报告"),
            method=meta.get("method", ""),
            url=meta.get("base_url", ""),
            version=str(meta.get("version", "")),
        )

    print("[OK] HTML 报告: " + html_path)


if __name__ == "__main__":
    main()
