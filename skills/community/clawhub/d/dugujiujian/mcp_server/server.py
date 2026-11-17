#!/usr/bin/env python3
"""
股票九剑 · MCP Server
=====================
将九式分析引擎暴露为 MCP (Model Context Protocol) 工具。
支持 Claude Desktop / OpenClaw / Hermes / Cursor / 任何 MCP 兼容平台。

启动方式：
    python server.py
    # 或通过各平台的 MCP 配置自动启动

暴露的工具：
    analyze_stock  — 全管线分析：获取数据 → 计算特征 → 九式匹配 → 综合研判
    get_framework  — 获取股票九剑框架知识（供 AI 理解体系）
    generate_chart — 生成 K 线技术分析图

作者: 股票九剑 Skill System
版本: 1.0.0
"""

import sys
import os
import json
import io
from pathlib import Path
from typing import Optional, Any

# ── 确保 scripts 目录在 path 中 ──────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Windows 编码修复
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except (ValueError, AttributeError):
        pass

# ── MCP SDK ─────────────────────────────────────────────
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="股票九剑",
    instructions="""A股短线抓涨技法 —— 九式规则匹配引擎。
融合第一性原理、博弈论、行为经济学进行多维度技术分析。

使用方法：
1. analyze_stock(code) — 对指定股票进行全管线分析
2. get_framework(sword?) — 获取九式框架知识
3. generate_chart(code) — 生成K线技术分析图

核心原则：
- 千种形态，不过涨跌 → 去繁就简
- 高矮长短，量能为先 → 量能不可伪造
- 利空出尽，尚可一等；利好曝光，谨防风险 → 博弈论思维
- 平和心态，时常默念 → 用规则取代情绪""",
)

# ── 懒加载模块 ──────────────────────────────────────────
_fetch = None
_compute = None
_rules = None
_plot = None


def _load_modules():
    """延迟加载，减少启动时间"""
    global _fetch, _compute, _rules, _plot
    if _fetch is None:
        import fetch_data as _fetch
        import compute_features as _compute
        import nine_swords_rules as _rules
        import plot_charts as _plot
    return _fetch, _compute, _rules, _plot


# ══════════════════════════════════════════════════════════
# 工具 1: 全管线分析
# ══════════════════════════════════════════════════════════

@mcp.tool()
def analyze_stock(
    code: str,
    days: int = 120,
    include_chart: bool = False,
    news: Optional[str] = None,
) -> dict:
    """
    对 A 股进行独孤九剑全管线分析：获取日K线数据 → 计算19+维技术特征 → 匹配九式规则 → 总诀式综合研判。

    参数:
        code: A股股票代码，如 "600519"（贵州茅台）、"002594"（比亚迪）
        days: 历史数据回溯天数，默认120天，建议范围 60-250
        include_chart: 是否生成K线技术分析图（PNG），默认False
        news: 可选的新闻/公告描述，用于破气式（消息判别）。如 "公司发布年报，净利润增长30%"

    返回:
        {
            "success": true/false,
            "code": "600519",
            "name": "股票名称",
            "core_metrics": {...},        // 核心指标摘要
            "swords_signals": {...},      // 九式匹配结果
            "zong_jue": {...},            // 总诀式综合研判
            "support_resistance": {...},  // 支撑阻力位
            "gaps": [...],                // 缺口信息
            "chart_path": "..."           // 图表路径（如果 include_chart=true）
        }
    """
    fetch, compute, rules, plot = _load_modules()

    result = {
        "success": False,
        "code": code,
        "name": "",
        "fetched_at": "",
        "errors": [],
    }

    # Step 1: 获取数据
    raw = fetch.fetch_all(code, days=days)
    if not raw["success"]:
        result["errors"] = raw.get("errors", ["数据获取失败"])
        return result

    result["name"] = raw["name"]
    result["fetched_at"] = raw["fetched_at"]

    # Step 2: 计算特征
    features = compute.compute_all_features(
        raw["daily_kline"],
        raw.get("fund_flow"),
        raw.get("minute_60"),
    )

    result["core_metrics"] = features["summary"]
    result["support_resistance"] = {
        "supports": features.get("supports", []),
        "resistances": features.get("resistances", []),
    }
    result["gaps"] = features.get("gaps", [])

    # Step 3: 破气式 — 消息分析
    news_data = None
    if news:
        # 简单的情感推断
        positive_words = ["增长", "盈利", "突破", "利好", "中标", "回购", "增持", "分红", "增长", "超预期"]
        negative_words = ["下降", "亏损", "减持", "处罚", "诉讼", "退市", "暴雷", "计提", "减值", "下滑"]

        sentiment = "neutral"
        if any(w in news for w in positive_words):
            sentiment = "positive"
        if any(w in news for w in negative_words):
            sentiment = "negative" if sentiment != "positive" else "mixed"

        # 检查是否已提前反应
        pre_reaction = abs(features["summary"].get("pct_change", 0)) > 5

        news_data = {
            "content": news,
            "sentiment": sentiment,
            "published": True,
            "pre_reaction": pre_reaction,
        }

    # Step 4: 九式匹配
    swords_result = rules.match_all_swords(features, news=news_data)

    result["swords_signals"] = {
        k: {
            "name": _sword_name(k),
            "triggered": v["triggered"],
            "strength": v["strength"],
            "reasons": v.get("reasons", []),
            "warnings": v.get("warnings", []),
        }
        for k, v in swords_result["signals"].items()
    }

    result["zong_jue"] = {
        "triggered_swords": swords_result["zong_jue"]["triggered_swords"],
        "sword_count": swords_result["zong_jue"]["sword_count"],
        "confidence": round(swords_result["zong_jue"]["confidence"], 1),
        "risk_level": swords_result["zong_jue"]["risk_level"],
        "recommendation": swords_result["zong_jue"]["recommendation"],
        "synergies": swords_result["zong_jue"]["synergies"],
        "conflicts": swords_result["zong_jue"]["conflicts"],
    }

    # Step 5: 图表（可选）
    if include_chart:
        try:
            chart_path = plot.plot_analysis_chart(
                features["data"],
                swords_result["signals"],
                swords_result["zong_jue"],
                code,
                raw["name"],
            )
            result["chart_path"] = chart_path
        except Exception as e:
            result["errors"].append(f"图表生成失败: {str(e)}")

    result["success"] = True
    return result


# ══════════════════════════════════════════════════════════
# 工具 2: 获取框架知识
# ══════════════════════════════════════════════════════════

@mcp.tool()
def get_framework(sword: Optional[str] = None) -> dict:
    """
    获取独孤九剑框架的完整知识。AI 调用此工具来理解分析体系和各招式的含义。

    参数:
        sword: 指定招式名称（可选）。不指定则返回全部。
               可选值: "总诀式" "破剑式" "破刀式" "破枪式" "破鞭式" "破索式" "破掌式" "破箭式" "破气式"

    返回:
        {
            "core_philosophy": "...",    // 核心理念
            "formula": {...},            // 总口诀拆解
            "swords": {...},             // 九式详解
            "auxiliary": {...},          // 辅助概念（五十买点、斐波那契、分时黄线等）
            "risk_management": {...}     // 风险控制框架
        }
    """
    sword_details = {
        "总诀式": {
            "poem": "诗文八千卷，尘嚣三十年。功名化粪土，一梦醉弄弦。",
            "role": "顶层框架，多维度信号互证",
            "trigger": "至少2个招式同时触发，信号不矛盾，置信度≥60",
            "core_logic": "当量能、形态、时间周期、心理状态四个独立维度的信号收敛于同一点 → 一剑封喉",
            "mental_model": "格栅模型（Latticework of Mental Models）—— 芒格",
        },
        "破剑式": {
            "poem": "长剑自来双刃，英雄但求无名。走马伴月酒醒，十步一杀绝情。",
            "role": "突破买入，把握起爆点",
            "market_logic": "系统从盘整态切换到趋势态的相变临界。振幅收窄=多空暂时平衡→即将打破",
            "conditions": [
                "前3日振幅持续收窄（蓄势）",
                "当日成交量 ≥ 5日均量的1.5倍",
                "价格突破20日内最高价",
                "当日收阳线",
                "加分：在斐波那契时间窗口（5/8/13天）",
            ],
            "failure": "假突破（无放量配合）、突破后立即回落收阴（诱多）",
            "stop_loss": "突破日最低价下方1%",
        },
        "破刀式": {
            "poem": "提笔诗文三千首，煮酒且论情与愁。此生何必太长久，一起梦蝶回商周。",
            "role": "趋势中途加仓，空中加油",
            "market_logic": "趋势是自增强循环（索罗斯反身性）。空中加油=确认正反馈未被切断",
            "conditions": [
                "处于上升趋势（MA21斜率向上）",
                "价格回踩5/8日均线但未有效跌破",
                "回调过程缩量（筹码锁定）",
                "近3日内再度放量上攻",
                "当日收阳确认",
            ],
            "failure": "回调跌破MA21（趋势可能逆转）、回调放量（可能是出货）",
            "stop_loss": "最近回调低点下方1%",
        },
        "破枪式": {
            "poem": "壮志豪情霸云天，气贯九霄揽彩烟。走马能腾万山涧，一支长矛战众仙。",
            "role": "追踪主力资金，借力打力",
            "market_logic": "主力是市场系统的关键影响节点。资金流向=主力行为的直接痕迹",
            "conditions": [
                "连续3日主力资金净流入",
                "同期价格涨幅<3%（主力仍在吃货）",
                "成交量温和放大（非脉冲式对倒）",
                "价格站在MA5之上",
            ],
            "failure": "主力对倒制造假放量、托单出货",
            "stop_loss": "主力流入起点日最低价",
        },
        "破鞭式": {
            "poem": "百转回还走川疆，飘渺错愕游仙乡。把盏醉梦儿时曲，可有阿娇待未央？",
            "role": "震荡市策略，上下画线",
            "market_logic": "震荡区间=系统的约束边界。在边界做反向操作：下沿买、上沿卖",
            "conditions": [
                "价格在明确箱体内（振幅<15%）",
                "布林带宽度适中（3-20%）",
                "RSI在30-70之间",
                "当前靠近下沿（<35%）→买点 | 上沿（>65%）→卖点",
            ],
            "failure": "假突破→止损、箱体被有效突破→停止打墙转为趋势策略",
            "stop_loss": "箱体下沿下方2%",
        },
        "破索式": {
            "poem": "君子礼谦谦，进退有后先。手持八卦扇，观星可知天。",
            "role": "左侧交易，底部吃货",
            "market_logic": "跌幅足够→悲观共识达极致。地量→卖盘枯竭。均线走平→下跌动能耗尽",
            "conditions": [
                "累计跌幅≥30%",
                "底部横盘≥8天，振幅<10%",
                "出现地量（20日成交量分位<20%）",
                "均线走平收敛（MA5-MA21差距<5%）",
                "不再创新低",
            ],
            "failure": "接飞刀（均线下持续下跌）、基本面断裂、底部还有地下室",
            "stop_loss": "最近低点下方3%",
        },
        "破掌式": {
            "poem": "一曲高歌仗剑行，胸中尚有几多情。秋风何必落叶净，我自雄翱似孤鹰。",
            "role": "短线打墙，高抛低吸",
            "market_logic": "破鞭式的快进快出版。要求换手率适中（有流动性但无过度投机）",
            "conditions": [
                "存在清晰短期箱体（15天内，振幅2-15%）",
                "换手率3-15%",
                "当前在箱体下沿（位置<35%）",
                "下沿处缩量",
                "RSI<40辅助确认",
            ],
            "failure": "箱体突破、流动性不足导致无法及时退出",
            "stop_loss": "箱体下沿下方1%",
        },
        "破箭式": {
            "poem": "箭镞本求利，淬砺良甚难。砺将何所用，砺以射凶残。",
            "role": "缺口交易，利用价格跳跃信号",
            "market_logic": "跳空=价格连续性被打破=强烈供需失衡。缺口不回补=方向能量极强",
            "conditions": [
                "存在3日内未回补的缺口",
                "缺口幅度≥1%",
                "缺口当日放量配合",
                "向上缺口+价格稳在缺口上方→做多",
            ],
            "failure": "缺口回补（信号失效）、缺口类型误判（衰竭缺口误作突破缺口）",
            "stop_loss": "向上缺口：缺口上沿下方1%",
        },
        "破气式": {
            "poem": "三生念，落花僵，一曲梦回乡。难醒醉黄梁，此心尽沧桑。",
            "role": "消息面的博弈论分析",
            "market_logic": "利好曝光→所有买家已入场→只剩卖盘→跌。利空出尽→所有卖家已离场→只剩买盘→涨",
            "conditions": [
                "存在近期公告/新闻",
                "判断消息方向（利好/利空）",
                "判断市场是否已提前定价",
                "利好+已公开+已上涨 → 卖出/不追",
                "利空+已公开+已大跌 → 等待底部信号",
            ],
            "failure": "消息解读错误、市场反应与预期相反",
            "stop_loss": "视具体消息影响幅度而定",
        },
    }

    core_philosophy = {
        "core_quote": "千种形态，不过涨跌。如同阴阳，极致必反。高矮长短，量能为先。周期波动，五八一三。",
        "four_dimensions": "方向（涨跌）+ 能量（量能）+ 时间（周期）+ 位置（均线/分割位）",
        "key_principles": [
            "成交量是不可伪造的共识强度指标",
            "斐波那契时间周期（5/8/13/21/34天）是市场参与者集体决策节奏的自然收敛",
            "利好曝光，谨防风险；利空出尽，尚可一等（纯博弈论推导）",
            "平和心态，时常默念；神清志明，一剑当先（元认知对冲杏仁核）",
        ],
    }

    auxiliary = {
        "五十买点": "50种买入模式分为趋势追随型（右侧）和均值回归型（左侧）两大类",
        "周期波动_五八一三": "3/5/8/13/21/34天是重要的变盘窗口。从最近重要高低点开始计数，窗口期±1天有效",
        "分时黄线": "分时均线=VWAP=市场平均成本。价格在黄线上方=日内强势",
        "盘口大单": "大单占比>30%=主力在活动。大单买入+价格不涨=压盘吸筹",
    }

    risk_management = {
        "principles": [
            "任何单一招式不能作为满仓依据",
            "多招式共鸣（≥2）才能加仓",
            "止损永远在入场前设定",
            "流动性不足时（换手率<1%），所有信号打折",
            "基本面结构断裂（ST/*ST/退市），所有信号无效",
        ],
        "stop_loss_by_sword": {k: v.get("stop_loss", "N/A") for k, v in sword_details.items()},
    }

    if sword:
        sword_key = sword.strip()
        if sword_key in sword_details:
            return {
                "sword": sword_key,
                "detail": sword_details[sword_key],
                "core_philosophy": core_philosophy,
                "risk_management": risk_management,
            }
        else:
            return {
                "error": f"未知招式: {sword}",
                "available": list(sword_details.keys()),
            }

    return {
        "core_philosophy": core_philosophy,
        "swords": sword_details,
        "auxiliary": auxiliary,
        "risk_management": risk_management,
    }


# ══════════════════════════════════════════════════════════
# 工具 3: 生成图表
# ══════════════════════════════════════════════════════════

@mcp.tool()
def generate_chart(code: str, days: int = 120) -> dict:
    """
    为指定股票生成独孤九剑技术分析 K 线图（含均线、布林带、RSI、成交量）。

    参数:
        code: A股股票代码
        days: 回溯天数，默认120

    返回:
        {
            "success": true/false,
            "chart_path": "图表PNG路径",
            "code": "...",
            "name": "..."
        }
    """
    fetch, compute, rules, plot = _load_modules()

    result = {"success": False, "code": code, "name": "", "chart_path": ""}

    raw = fetch.fetch_all(code, days=days)
    if not raw["success"]:
        result["error"] = "数据获取失败"
        return result

    result["name"] = raw["name"]

    features = compute.compute_all_features(
        raw["daily_kline"],
        raw.get("fund_flow"),
        raw.get("minute_60"),
    )

    swords_result = rules.match_all_swords(features)

    try:
        chart_path = plot.plot_analysis_chart(
            features["data"],
            swords_result["signals"],
            swords_result["zong_jue"],
            code,
            raw["name"],
        )
        result["chart_path"] = chart_path
        result["success"] = True
    except Exception as e:
        result["error"] = f"图表生成失败: {str(e)}"

    return result


# ══════════════════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════════════════

def _sword_name(key: str) -> str:
    """招式 key → 中文名"""
    names = {
        "po_jian": "破剑式（起爆点）",
        "po_dao": "破刀式（空中加油）",
        "po_qiang": "破枪式（主力跟踪）",
        "po_bian": "破鞭式（上下画线）",
        "po_suo": "破索式（底部吃货）",
        "po_zhang": "破掌式（短线打墙）",
        "po_jian_2": "破箭式（缺口策略）",
        "po_qi": "破气式（消息判别）",
    }
    return names.get(key, key)


# ══════════════════════════════════════════════════════════
# 启动入口
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("⚔️  独孤九剑 MCP Server 启动中...", file=sys.stderr)
    print(f"   Scripts: {SCRIPTS_DIR}", file=sys.stderr)
    mcp.run()
