#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dawn Data Collector v1.0
用途: 批量采集ETF/股票的技术指标数据用于ML训练
数据源: HTSC query-indicator (MACD/KDJ/RSI/资金流等)
"""

import os, sys, json, subprocess, time, re, datetime, warnings
from pathlib import Path

warnings.filterwarnings("ignore")

HTSC_SCRIPT = os.path.join(
    os.path.expanduser("~"), ".openclaw", "skills", "query-indicator", "query_indicator.py"
)

DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / ".." / "dawn-trader" / "data"
RAW_DIR = DATA_DIR / "raw"
FACTORS_DIR = DATA_DIR / "factors"
os.makedirs(FACTORS_DIR, exist_ok=True)

# 监控的ETF池（比赛持仓 + 扩展候选）
ETF_POOL = {
    "515580": "科技100ETF华泰柏瑞",
    "588090": "科创50ETF华泰柏瑞",
    "560910": "电池ETF华泰柏瑞",
    "513110": "纳指ETF",
    "588000": "科创50ETF华夏",
    "159915": "创业板ETF",
    "510050": "上证50ETF",
    "510300": "沪深300ETF",
    "512880": "证券ETF",
    "515790": "光伏ETF",
    "512480": "半导体ETF",
    "159941": "纳指ETF",
    "513100": "纳指ETF",
    "518880": "黄金ETF",
}


def fetch_indicators(code: str, name: str) -> dict:
    """从HTSC query-indicator获取完整技术指标"""
    if not os.path.exists(HTSC_SCRIPT):
        return {"error": "query-indicator不可用"}
    
    try:
        result = subprocess.run(
            ["py", "-X", "utf8", HTSC_SCRIPT, "queryIndicator",
             "--query", f"{code}{name}今天MACD、KDJ、RSI、换手率、成交量、振幅、主力资金流向、市盈率"],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        output = result.stdout or result.stderr
        data = json.loads(output)
        if data.get("ok"):
            answer = data["data"]["answer"]
            indicators = parse_indicators(answer)
            indicators["code"] = code
            indicators["name"] = name
            indicators["raw"] = answer
            return indicators
        return {"error": data.get("error", {}).get("message", "")}
    except json.JSONDecodeError:
        return {"error": "JSON解析失败"}
    except subprocess.TimeoutExpired:
        return {"error": "超时"}
    except Exception as e:
        return {"error": str(e)}


def parse_indicators(text: str) -> dict:
    """从自然语言中提取所有可解析的指标"""
    result = {}
    
    patterns = {
        "macd": r'MACD[是为：:]*\s*([-\d.]+)',
        "kdj_j": r'(?:KDJ的|KDJ[是为])?J\s*值?[是为：:]*\s*([\d.]+)',
        "rsi": r'RSI[是为：:]*\s*([\d.]+)',
        "turnover": r'换手率[是为：:]*\s*([\d.]+)%',
        "volume": r'成交量\s*([\d.]+)万手',
        "amount": r'成交额\s*([-\d.]+)万',
        "amplitude": r'振幅[是为：:]*\s*([\d.]+)%',
        "pe": r'市盈率[是为：:]*\s*([-\d.]+)',
    }
    
    for key, pattern in patterns.items():
        m = re.search(pattern, text)
        if m:
            result[key] = float(m.group(1))
    
    # 资金流向（支持多种格式）
    for flow_type in ["主力", "超大单", "大单", "中单", "小单"]:
        m_in = re.search(rf'{flow_type}净流入\s*([-\d.]+)万', text)
        m_out = re.search(rf'{flow_type}净流出\s*([-\d.]+)万', text)
        if m_in:
            result[f"{flow_type}_flow"] = float(m_in.group(1))
        elif m_out:
            result[f"{flow_type}_flow"] = -float(m_out.group(1))
    
    # 涨跌幅
    m = re.search(r'涨跌幅[是为：:]*\s*([-\d.]+)%', text)
    if m:
        result["change_pct"] = float(m.group(1))
    
    # 价格区间
    m = re.search(r'价格区间\s*([\d.]+)元至\s*([\d.]+)元', text)
    if m:
        result["low_today"] = float(m.group(1))
        result["high_today"] = float(m.group(2))
    
    return result


def collect_all(codes: dict = None) -> dict:
    """批量采集全部标的的技术指标"""
    if codes is None:
        codes = ETF_POOL
    
    results = {}
    total = len(codes)
    
    print(f"[OK] 开始采集 {total} 只标的...")
    
    for i, (code, name) in enumerate(codes.items(), 1):
        print(f"  [{i}/{total}] {name}({code})...", end=" ", flush=True)
        data = fetch_indicators(code, name)
        
        if "error" in data and data.get("macd") is None:
            print(f"[FAIL] {data['error']}")
            results[code] = {"error": data["error"]}
        else:
            # 提取结构化数据，去raw
            clean = {k: v for k, v in data.items() if k != "raw"}
            if clean.get("macd"):
                print(f"[OK] MACD={clean['macd']} J={clean.get('kdj_j','?')} RSI={clean.get('rsi','?')} 主力={clean.get('主力_flow','?')}万")
            else:
                print(f"[PARTIAL] 部分数据: {list(clean.keys())}")
            results[code] = clean
        
        # 避免请求过快
        if i < total:
            time.sleep(0.5)
    
    return results


def save_results(results: dict, name: str = "indicators"):
    """保存采集结果"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    path = FACTORS_DIR / f"{name}_{timestamp}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 已保存: {path}")
    
    # 同时保存最新版本（无时间戳，方便程序读取）
    latest = FACTORS_DIR / f"{name}_latest.json"
    with open(latest, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[OK] 已保存最新版: {latest}")
    
    return path


def summary(results: dict) -> str:
    """生成采集摘要"""
    total = len(results)
    ok = sum(1 for v in results.values() if "macd" in v and v["macd"] is not None)
    partial = sum(1 for v in results.values() if "error" not in v and "macd" not in v)
    failed = sum(1 for v in results.values() if "error" in v)
    
    lines = [
        f"[RESULT] 采集完成: {total}只标的",
        f"  [OK] {ok} 完整 | [PARTIAL] {partial} 部分 | [FAIL] {failed} 失败",
    ]
    
    if ok > 0:
        lines.append("\n完整数据标的:")
        for code, data in results.items():
            if "macd" in data:
                lines.append(
                    f"  {data.get('name', code)}: "
                    f"MACD={data['macd']} "
                    f"J={data.get('kdj_j', '?')} "
                    f"RSI={data.get('rsi', '?')} "
                    f"主力={data.get('主力_flow', 0):+.0f}万 "
                    f"量比={data.get('volume_ratio', '?')}"
                )
    
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dawn Data Collector")
    parser.add_argument("--targets", choices=["etf", "etf_pool", "all"], default="etf",
                       help="采集目标: etf=持仓4只, etf_pool=14只候选池")
    parser.add_argument("--codes", type=str, help="逗号分隔的股票代码")
    
    args = parser.parse_args()
    
    if args.codes:
        codes = {}
        for c in args.codes.split(","):
            codes[c.strip()] = c.strip()
    elif args.targets == "etf":
        codes = {k: v for k, v in ETF_POOL.items() if k in ["515580", "588090", "560910", "513110"]}
    elif args.targets == "etf_pool":
        codes = ETF_POOL
    else:
        codes = ETF_POOL
    
    results = collect_all(codes)
    save_results(results, f"indicators_{args.targets}")
    print("\n" + summary(results))


if __name__ == "__main__":
    main()
