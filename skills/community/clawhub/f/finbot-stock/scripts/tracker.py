#!/usr/bin/env python3
"""
棱镜 推荐追踪引擎 v1.0 — 推荐闭环的核心组件

功能：
1. record  — 记录一次推荐（含推荐价、逻辑、止损止盈）
2. check   — 检查今日哪些推荐需要追踪更新
3. report  — 输出所有活跃推荐的追踪报告

使用方式：
  python3 tracker.py record <code> <方向> <入场价> <止损价> <止盈价> '<逻辑简述>'
  python3 tracker.py check          # 检查所有活跃推荐今日表现
  python3 tracker.py report         # 生成完整追踪报告
  python3 tracker.py list           # 列出所有活跃推荐
  python3 tracker.py close <推荐ID> # 关闭一条推荐（止盈/止损/手动关闭）

数据存储在：{BASE_DIR}/tracking/ 目录，每个文件是推荐的完整追踪记录。
"""

import json
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from fetcher import fetch_realtime, fetch_kline, calc_indicators

TRACKING_DIR = os.path.join(BASE_DIR, "tracking")
os.makedirs(TRACKING_DIR, exist_ok=True)

# ============ 核心数据结构 ============

# tracking/{code}_{recommend_date}_{id}.json
# {
#   "id": "uuid短码",
#   "code": "002428",
#   "name": "翔鹭钨业",
#   "direction": "long",
#   "entry_price": 80.22,
#   "stop_loss": 76.0,
#   "take_profit": 92.0,
#   "rationale": "钨涨价+缩量回调假跌破+板块轮动",
#   "source": "manual | cron | webchat",
#   "recommend_date": "2026-06-11",
#   "recommend_time": "09:00",
#   "status": "active",  # active | stopped | closed
#   "close_reason": null,
#   "close_date": null,
#   "close_price": null,
#   "max_return_pct": 0,     # 追踪期间最大收益
#   "min_return_pct": 0,     # 追踪期间最大回撤
#   "checks": [
#     {
#       "date": "2026-06-12",
#       "price": 85.0,
#       "change_pct": 5.96,
#       "vs_entry": 5.96,
#       "hit_stop": false,
#       "hit_profit": false,
#       "note": ""
#     }
#   ]
# }


def _name_from_code(code):
    """简单从行情中获取股票名称"""
    data = fetch_realtime(code)
    if data and "name" in data:
        return data["name"]
    return code


def _next_id():
    """生成短ID"""
    import hashlib
    h = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
    return h


def record_recommendation(code, direction, entry_price, stop_loss, take_profit, rationale, source="manual"):
    """记录一次推荐"""
    # 获取名称
    name = _name_from_code(code)
    
    rec = {
        "id": _next_id(),
        "code": code,
        "name": name,
        "direction": direction,
        "entry_price": float(entry_price),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit),
        "rationale": rationale[:300],
        "source": source,
        "recommend_date": datetime.now().strftime("%Y-%m-%d"),
        "recommend_time": datetime.now().strftime("%H:%M"),
        "status": "active",
        "close_reason": None,
        "close_date": None,
        "close_price": None,
        "max_return_pct": 0,
        "min_return_pct": 0,
        "checks": [],
    }
    
    # 首次检查：记录推荐时的价格
    rec["checks"].append({
        "date": rec["recommend_date"],
        "time": rec["recommend_time"],
        "price": float(entry_price),
        "change_pct": 0,
        "vs_entry": 0,
        "hit_stop": False,
        "hit_profit": False,
        "note": "推荐日·初始记录"
    })
    
    filename = f"{code}_{rec['recommend_date']}_{rec['id']}.json"
    filepath = os.path.join(TRACKING_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 推荐已记录: {name}({code}) @ ¥{entry_price}")
    print(f"   文件: {filepath}")
    print(f"   ID: {rec['id']}")
    return filepath


def check_recommendation(rec):
    """检查一条推荐今天的表现（含技术因子快照）"""
    code = rec["code"]
    entry = rec["entry_price"]
    stop_loss = rec["stop_loss"]
    take_profit = rec["take_profit"]
    
    # 获取实时行情
    data = fetch_realtime(code)
    if not data or "error" in data:
        return {"error": f"获取{code}行情失败"}
    
    current_price = float(data.get("price", 0))
    if current_price == 0:
        return {"error": f"{code}价格为零"}
    
    change_today = float(data.get("change_pct", 0))
    vs_entry = round((current_price - entry) / entry * 100, 2)
    
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    
    # 检查是否触及止损/止盈
    hit_stop = current_price <= stop_loss
    hit_profit = current_price >= take_profit
    
    # 更新最大/最小收益
    rec["max_return_pct"] = max(rec["max_return_pct"], vs_entry)
    rec["min_return_pct"] = min(rec["min_return_pct"], vs_entry)
    
    # 判断是否需要自动关闭
    close_note = None
    if hit_stop:
        close_note = f"触发止损(¥{current_price} ≤ ¥{stop_loss})"
    elif hit_profit:
        close_note = f"触发止盈(¥{current_price} ≥ ¥{take_profit})"
    
    # ========== 新增：采集当日技术因子快照 ==========
    kline = fetch_kline(code, "daily", 60)
    indicators = calc_indicators(kline) if kline and len(kline) >= 20 else {}
    
    factor_snapshot = {}
    if indicators:
        factor_snapshot = {
            "ma20": indicators.get("ma20"),
            "ma5": indicators.get("ma5"),
            "ma10": indicators.get("ma10"),
            "ma60": indicators.get("ma60"),
            "deviation_ma20": indicators.get("deviation_ma20_pct"),
            "volume_ratio": indicators.get("volume_ratio"),
            "rsi6": indicators.get("rsi6"),
            "macd_histogram": indicators.get("macd_histogram"),
            "macd_bullish": indicators.get("macd_bullish"),
            "kdj_bullish": indicators.get("kdj_bullish"),
            "bb_position": indicators.get("bb_position"),
            "icu_bullish": indicators.get("icu_bullish"),
            "alligator_eating": indicators.get("alligator_eating"),
            "obv_trend": indicators.get("obv_trend"),
        }
    
    # 写入检查记录
    check_entry = {
        "date": today,
        "time": now,
        "price": current_price,
        "change_pct": change_today,
        "vs_entry": vs_entry,
        "hit_stop": hit_stop,
        "hit_profit": hit_profit,
        "note": close_note or "",
        "factors": factor_snapshot  # 技术因子快照
    }
    
    rec["checks"].append(check_entry)
    
    # 自动关闭
    if close_note:
        rec["status"] = "closed"
        rec["close_reason"] = close_note
        rec["close_date"] = today
        rec["close_price"] = current_price
    
    return {
        "code": code,
        "name": rec["name"],
        "entry": entry,
        "current": current_price,
        "vs_entry": vs_entry,
        "change_today": change_today,
        "hit_stop": hit_stop,
        "hit_profit": hit_profit,
        "max_return": rec["max_return_pct"],
        "min_return": rec["min_return_pct"],
        "status": rec["status"],
        "close_reason": close_note,
        "factors": factor_snapshot
    }


def check_all_active():
    """检查所有活跃推荐"""
    results = []
    for fname in os.listdir(TRACKING_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(TRACKING_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            rec = json.load(f)
        
        if rec.get("status") != "active":
            continue
        
        result = check_recommendation(rec)
        if "error" in result:
            print(f"⚠️ {fname}: {result['error']}")
            continue
        
        results.append(result)
        
        # 写回文件
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
    
    return results


def list_active():
    """列出所有活跃推荐"""
    active = []
    for fname in os.listdir(TRACKING_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(TRACKING_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            rec = json.load(f)
        active.append(rec)
    return active


def close_recommendation(rec_id, reason="手动关闭"):
    """关闭一条推荐"""
    closed = []
    for fname in os.listdir(TRACKING_DIR):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(TRACKING_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            rec = json.load(f)
        
        if rec.get("id") != rec_id:
            continue
        
        # 获取当前价
        data = fetch_realtime(rec["code"])
        current = float(data.get("price", 0)) if data and "price" in data else 0
        
        if current > 0:
            vs_entry = round((current - rec["entry_price"]) / rec["entry_price"] * 100, 2)
        else:
            vs_entry = 0
        
        rec["status"] = "closed"
        rec["close_reason"] = reason
        rec["close_date"] = datetime.now().strftime("%Y-%m-%d")
        rec["close_price"] = current if current > 0 else rec["entry_price"]
        
        # 最后一条check
        rec["checks"].append({
            "date": rec["close_date"],
            "time": datetime.now().strftime("%H:%M"),
            "price": rec["close_price"],
            "change_pct": 0,
            "vs_entry": vs_entry,
            "hit_stop": False,
            "hit_profit": False,
            "note": f"关闭: {reason}"
        })
        
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        
        closed.append(rec)
        print(f"✅ 已关闭: {rec['name']}({rec['code']}) | 入场¥{rec['entry_price']}→关闭¥{rec['close_price']} | 收益{vs_entry}% | 原因: {reason}")
    
    if not closed:
        print(f"❌ 未找到ID: {rec_id}")
    
    return closed


def generate_report():
    """生成完整追踪报告"""
    lines = []
    lines.append(f"# 📊 推荐追踪报告 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    all_recs = []
    for fname in sorted(os.listdir(TRACKING_DIR), reverse=True):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(TRACKING_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            rec = json.load(f)
        all_recs.append(rec)
    
    if not all_recs:
        lines.append("暂无推荐记录。")
        return "\n".join(lines)
    
    active = [r for r in all_recs if r.get("status") == "active"]
    closed = [r for r in all_recs if r.get("status") != "active"]
    
    # 活跃推荐
    lines.append(f"## 🔴 活跃推荐 ({len(active)}条)")
    lines.append("")
    if active:
        lines.append("| 代码 | 名称 | 入场价 | 当前价 | 收益 | 止损 | 止盈 | RSI6 | MACD | ICU | 来源 | 天数 |")
        lines.append("|------|------|--------|--------|------|------|------|------|------|-----|------|------|")
        for r in active:
            entry = r["entry_price"]
            last_check = r["checks"][-1] if r["checks"] else {}
            current = last_check.get("price", entry)
            vs_entry = last_check.get("vs_entry", 0)
            factors = last_check.get("factors", {})
            rsi = factors.get("rsi6", "-")
            macd_s = "📗" if factors.get("macd_bullish") else "📕"
            icu = "✅" if factors.get("icu_bullish") else "-"
            days = (datetime.now() - datetime.strptime(r["recommend_date"], "%Y-%m-%d")).days + 1
            lines.append(f"| {r['code']} | {r['name']} | ¥{entry} | ¥{current} | {vs_entry:+.2f}% | ¥{r['stop_loss']} | ¥{r['take_profit']} | {rsi} | {macd_s} | {icu} | {r['source']} | {days}d |")
    else:
        lines.append("（无）")
    
    lines.append("")
    
    # 已关闭
    if closed:
        lines.append(f"## ✅ 已关闭 ({len(closed)}条)")
        lines.append("")
        lines.append("| 代码 | 名称 | 入场价 | 关闭价 | 收益 | 结果 | 天数 | 原因 |")
        lines.append("|------|------|--------|--------|------|------|------|------|")
        for r in closed:
            entry = r["entry_price"]
            close_price = r.get("close_price", entry)
            vs_entry = round((close_price - entry) / entry * 100, 2) if entry > 0 else 0
            days = 0
            if r.get("close_date") and r.get("recommend_date"):
                try:
                    days = (datetime.strptime(r["close_date"], "%Y-%m-%d") - datetime.strptime(r["recommend_date"], "%Y-%m-%d")).days + 1
                except:
                    days = 0
            reason = r.get("close_reason", "")
            # 结果颜色
            if vs_entry >= 10:
                result = "🎯 止盈"
            elif vs_entry <= -5:
                result = "🛑 止损"
            elif vs_entry > 0:
                result = "📗 微盈"
            else:
                result = "📕 亏损"
            lines.append(f"| {r['code']} | {r['name']} | ¥{entry} | ¥{close_price} | {vs_entry:+.2f}% | {result} | {days}d | {reason} |")
    
    report = "\n".join(lines)
    
    # 保存报告
    report_path = os.path.join(BASE_DIR, "tracking", f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"\n✅ 报告已保存: {report_path}")
    return report_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 tracker.py record <code> <方向> <入场价> <止损价> <止盈价> '<逻辑>'")
        print("  python3 tracker.py check")
        print("  python3 tracker.py report")
        print("  python3 tracker.py list")
        print("  python3 tracker.py close <推荐ID> [原因]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "record":
        if len(sys.argv) < 7:
            print("用法: python3 tracker.py record <code> <方向(long/short)> <入场价> <止损价> <止盈价> '<逻辑>'")
            sys.exit(1)
        record_recommendation(
            code=sys.argv[2],
            direction=sys.argv[3],
            entry_price=float(sys.argv[4]),
            stop_loss=float(sys.argv[5]),
            take_profit=float(sys.argv[6]),
            rationale=" ".join(sys.argv[7:]) if len(sys.argv) > 7 else "",
            source="cli"
        )
    
    elif cmd == "check":
        results = check_all_active()
        if not results:
            print("✅ 无活跃推荐需要检查")
        else:
            print(f"📊 检查了 {len(results)} 条活跃推荐:")
            for r in results:
                flag = ""
                if r["hit_stop"]: flag = " 🛑 触及止损"
                elif r["hit_profit"]: flag = " 🎯 触及止盈"
                print(f"  {r['name']}({r['code']}): 入场¥{r['entry']} → 当前¥{r['current']} ({r['vs_entry']:+.2f}%){flag}")
    
    elif cmd == "report":
        generate_report()
    
    elif cmd == "list":
        recs = list_active()
        if not recs:
            print("✅ 无活跃推荐")
        else:
            print(f"📋 活跃推荐 ({len(recs)}条):")
            for r in recs:
                print(f"  [{r['id']}] {r['name']}({r['code']}) ¥{r['entry_price']} | {r['recommend_date']} | {r['source']}")
    
    elif cmd == "close":
        rec_id = sys.argv[2] if len(sys.argv) > 2 else None
        reason = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "手动关闭"
        if rec_id:
            close_recommendation(rec_id, reason)
        else:
            print("用法: python3 tracker.py close <推荐ID> [原因]")
    
    else:
        print(f"未知命令: {cmd}")
