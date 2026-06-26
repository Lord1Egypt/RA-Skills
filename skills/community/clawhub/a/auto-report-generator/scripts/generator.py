#!/usr/bin/env python3
"""自动报表生成器 - 主入口脚本"""

import argparse
import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import parser, charts, ai_analyzer, report_builder, templates, quota


# ── 91Skillhub Token Verification ─────────────────────────────────────────────
VERIFY_URL = "https://geo-api.yk-global.com/validate"

VALID_PREFIXES = {
    "GEO", "PROFIT", "INV", "DATA", "MON",
    "PDF", "BANK", "CONTRACT", "EMAIL", "CONV",
    "RPT", "SENTIMENT",
}


def _get_cached(key: str) -> dict:
    """读取本地缓存（5分钟TTL）"""
    import time
    cache_dir = Path.home() / ".auto_report_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    if not cache_file.exists():
        return None
    try:
        with open(cache_file) as f:
            data = json.load(f)
        if time.time() - data.get("_ts", 0) > 300:
            return None
        return data
    except Exception:
        return None


def _set_cached(key: str, data: dict) -> None:
    """写入本地缓存"""
    import time
    cache_dir = Path.home() / ".auto_report_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{key[:8].replace('/', '_')}.json"
    try:
        data["_ts"] = time.time()
        with open(cache_file, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def _map_prefix_to_tier(api_key: str) -> str:
    """根据 API key 前缀推断套餐级别。"""
    if not api_key:
        return "FREE"
    upper = api_key.upper()
    if "ENT" in upper:
        return "MAX"
    if "MAX" in upper:
        return "MAX"
    if "PRO" in upper:
        return "PRO"
    if "STD" in upper:
        return "STD"
    if "BSC" in upper:
        return "STD"
    if "FREE" in upper:
        return "FREE"
    return "FREE"


def verify_token(api_key: str) -> dict:
    """
    验证 API key via geo-api.yk-global.com。
    降级策略：网络错误/验证失败 → FREE，不阻断使用。
    缓存：5分钟。
    """
    if not api_key:
        return {"valid": False, "tier": "FREE", "error": "No API key"}

    prefix = api_key.split("-")[0].upper() if "-" in api_key else api_key[:4].upper()
    if prefix not in VALID_PREFIXES:
        return {"valid": False, "tier": "FREE", "error": "Not a 91Skillhub key"}

    cached = _get_cached(api_key)
    if cached:
        return cached

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=b"{}",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("valid", False):
                tier = _map_prefix_to_tier(api_key)
                result = {"valid": True, "tier": tier, "prefix": data.get("prefix", ""),
                           "plan_id": data.get("plan_id"), "quota_remaining": data.get("quota_remaining")}
            else:
                result = {"valid": False, "tier": "FREE",
                           "error": data.get("error", "Invalid or expired key")}
            _set_cached(api_key, result)
            return result
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read().decode("utf-8"))
            err_msg = err_body.get("error", f"HTTP {e.code}")
        except Exception:
            err_msg = f"HTTP {e.code}"
        result = {"valid": False, "tier": "FREE", "error": err_msg}
        _set_cached(api_key, result)
        return result
    except Exception as e:
        return {"valid": False, "tier": "FREE", "error": f"Network error: {e}"}


def main():
    parser_cli = argparse.ArgumentParser(
        description='自动报表生成器 - 从数据文件生成分析报表',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_cli.add_argument('--input', '-i', required=True, help='输入数据文件路径 (CSV/Excel)')
    parser_cli.add_argument('--output', '-o', default='report.xlsx', help='输出报表路径 (默认: report.xlsx)')
    parser_cli.add_argument('--template', '-t', default='custom',
                            choices=['monthly_operation', 'financial', 'sales', 'data_comparison', 'custom'],
                            help='报表模板 (默认: custom)')
    parser_cli.add_argument('--tier', default='free',
                            choices=['free', 'std', 'pro', 'max'],
                            help='用户等级，决定AI分析额度 (默认: free)')
    parser_cli.add_argument('--api-key', help='AI API密钥 (可选，不提供则跳过AI分析)')
    parser_cli.add_argument('--api-base', default='https://api.openai.com/v1',
                            help='AI API基础URL (默认: https://api.openai.com/v1)')
    parser_cli.add_argument('--no-ai', action='store_true', help='跳过AI分析')
    parser_cli.add_argument('--sheet', default=None, help='Excel工作表名称 (仅Excel文件)')

    args = parser_cli.parse_args()

    # ── Tier 推断优先级 ──────────────────────────────────────────
    # 1. 优先用 OPENAI_API_KEY 环境变量验证 yk global token
    # 2. 验证成功 → 用对应 tier
    # 3. 失败/无 key → 降级到 --tier CLI 参数
    yk_key = os.environ.get("OPENAI_API_KEY", "")
    if yk_key:
        verify_result = verify_token(yk_key)
        if verify_result["valid"]:
            tier = verify_result["tier"]
            print(f"[INFO] Token verified: valid=True, tier={tier}, prefix={verify_result.get('prefix','')}")
        else:
            tier = args.tier
            print(f"[WARN] Token invalid ({verify_result['error']}), using CLI tier={tier}")
    else:
        tier = args.tier
        print(f"[INFO] No API key, using CLI tier={tier}")

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 加载数据
    print(f"正在加载数据: {args.input}")
    if input_path.suffix.lower() == '.csv':
        df = parser.load_csv(str(input_path))
    elif input_path.suffix.lower() in ('.xlsx', '.xls'):
        df = parser.load_excel(str(input_path), sheet=args.sheet)
    else:
        print(f"错误: 不支持的文件格式: {input_path.suffix}", file=sys.stderr)
        sys.exit(1)

    print(f"数据加载完成: {len(df)} 行, {len(df.columns)} 列")

    # 获取统计数据
    stats = parser.get_stats(df)
    print(f"数据统计完成")

    # 生成图表
    chart_paths = []
    if not df.select_dtypes(include=['number']).columns.empty:
        numeric_col = df.select_dtypes(include=['number']).columns[0]
        try:
            chart_path = charts.generate_chart(df, numeric_col, 'line')
            chart_paths.append(chart_path)
            print(f"图表生成完成: {chart_path}")
        except Exception as e:
            print(f"图表生成跳过: {e}")

    # AI 分析
    ai_analysis = ""
    if not args.no_ai and args.api_key:
        quota_result = quota.check_quota(tier, 1)
        if quota_result['allowed']:
            print(f"正在进行AI分析 (剩余额度: {quota_result['remaining']})...")
            ai_analysis = ai_analyzer.analyze_data(df, args.api_key, args.api_base)
            quota.increment(tier)
        else:
            print(f"AI分析跳过: {quota_result['message']}")
    else:
        print("AI分析已跳过")

    # 获取模板
    template = templates.get_template(args.template)

    # 构建报表
    report_data = {
        'title': f'{template["name"]} - {input_path.stem}',
        'stats': stats,
        'charts': chart_paths,
        'ai_analysis': ai_analysis,
        'raw_data': df,
        'template': template['name'],
    }

    print(f"正在生成报表: {args.output}")
    output_path = report_builder.build_excel_report(report_data, args.output)
    print(f"报表生成完成: {output_path}")


if __name__ == '__main__':
    main()
