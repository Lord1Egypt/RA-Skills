#!/usr/bin/env python3
"""
生成决策仪表盘 Markdown 报告
基于数据驱动的投资分析，输出可执行的决策仪表盘
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install pandas numpy")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_realtime_data(data_dir: Path) -> Optional[Dict]:
    """加载实时数据"""
    csv_files = list(data_dir.glob('*_realtime.csv'))
    if not csv_files:
        return None
    df = pd.read_csv(csv_files[0])
    return df.iloc[0].to_dict() if not df.empty else None


def load_indicators(data_dir: Path) -> Optional[pd.DataFrame]:
    """加载技术指标数据"""
    csv_files = list(data_dir.glob('*_indicators.csv'))
    if not csv_files:
        return None
    return pd.read_csv(csv_files[0])


def load_risk_metrics(data_dir: Path) -> Optional[Dict]:
    """加载风险指标数据"""
    json_files = list(data_dir.glob('*_risk_metrics.json'))
    if not json_files:
        return None
    with open(json_files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def load_search_intel(data_dir: Path) -> Optional[Dict]:
    """加载搜索情报数据"""
    json_files = list(data_dir.glob('*_search_intel.json'))
    if not json_files:
        return None
    with open(json_files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_dashboard(stock_name: str, stock_code: str,
                        realtime_data: Optional[Dict],
                        indicators_df: Optional[pd.DataFrame],
                        risk_metrics: Optional[Dict],
                        search_intel: Optional[Dict]) -> str:
    """生成决策仪表盘 Markdown"""
    
    if realtime_data is None or indicators_df is None:
        return "# 错误：缺少必要的数据文件\n\n请确保已执行数据采集和指标计算脚本。"
    
    # 获取最新指标
    latest = indicators_df.iloc[-1]
    
    # 趋势分析
    ma5 = latest.get('MA5', 0)
    ma10 = latest.get('MA10', 0)
    ma20 = latest.get('MA20', 0)
    
    if ma5 > ma10 > ma20:
        ma_alignment = "多头排列"
        trend_strength = "强势" if (ma5 - ma10) / ma10 > 0.02 else "温和"
    elif ma5 < ma10 < ma20:
        ma_alignment = "空头排列"
        trend_strength = "弱势"
    else:
        ma_alignment = "缠绕"
        trend_strength = "震荡"
    
    # 价格分析
    current_price = realtime_data.get('最新价', 0)
    bias_ma5 = ((current_price - ma5) / ma5) * 100 if ma5 > 0 else 0
    bias_warning = "是" if bias_ma5 > 5 else "否"
    
    # 量能分析
    # 注意：这里需要从indicators_df获取量比数据，假设已计算
    volume_ratio = 1.0  # 占位，实际应从数据中获取
    volume_status = "放量" if volume_ratio > 1.5 else "缩量" if volume_ratio < 0.7 else "正常"
    
    # 筹码分析（占位）
    chip_concentration = 15.0  # 占位
    chip_status = "集中" if chip_concentration < 15 else "较分散" if chip_concentration < 20 else "分散"
    
    # 风险评估
    max_dd = risk_metrics.get('max_drawdown', {}).get('max_drawdown_pct', 0) if risk_metrics else 0
    sharpe = risk_metrics.get('sharpe_ratio', 0) if risk_metrics else 0
    
    # 信号分类
    if ma_alignment == "多头排列" and bias_ma5 < 5 and max_dd > -30:
        signal_type = "🟢买入信号"
        recommendation = "谨慎买入"
    elif ma_alignment == "空头排列" or bias_ma5 > 10:
        signal_type = "🔴卖出信号"
        recommendation = "规避风险"
    else:
        signal_type = "🟡持有观望"
        recommendation = "观望为主"
    
    # 生成核心结论
    one_sentence = f"{ma_alignment}且乖离率{bias_ma5:.2f}%，{'需警惕追高' if bias_warning == '是' else '技术面良好'}"
    
    # 支撑/阻力位
    support_levels = [f"{ma5:.2f}元(MA5)", f"{ma10:.2f}元(MA10)"]
    resistance_levels = [f"{current_price * 1.05:.2f}元", f"{current_price * 1.10:.2f}元"]
    
    # 精确点位
    ideal_buy = ma10  # 回踩MA10
    stop_loss = ma20  # 跌破MA20
    take_profit = current_price * 1.15  # +15%
    
    # 检查清单
    checklist = [
        f"{'✅' if ma_alignment == '多头排列' else '❌'} 多头排列（MA5 > MA10 > MA20）",
        f"{'✅' if bias_ma5 < 5 else '⚠️'} 乖离率合理（{bias_ma5:.2f}% {'<' if bias_ma5 < 5 else '>'} 5%）",
        f"{'⚠️' if volume_status == '缩量' else '✅'} 量能状态：{volume_status}",
        f"{'✅' if chip_status == '集中' else '⚠️'} 筹码{chip_status}（{chip_concentration:.1f}%）",
    ]
    
    # 情报分析（如果有）
    latest_news = "暂无数据"
    risk_alerts = []
    positive_catalysts = []
    market_sentiment = "中性"
    
    if search_intel:
        latest_news = "请根据 web_search 结果填写最新消息"
        risk_alerts = ["请根据风险排查搜索结果填写"]
        positive_catalysts = ["请根据行业热点搜索结果填写"]
    
    # 生成 Markdown
    md = f"""# 🎯 {stock_name}({stock_code}) 决策仪表盘

**报告日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**数据来源**: AkShare + YFinance

---

## 📊 核心结论

{signal_type}

**{one_sentence}**

- **空仓者**: {'等待回调至{ideal_buy:.2f}元附近再考虑买入' if signal_type != '🔴卖出信号' else '暂不建议买入'}
- **持仓者**: {'持有观望，设置止损{stop_loss:.2f}元' if signal_type == '🟡持有观望' else '考虑减仓' if signal_type == '🔴卖出信号' else '继续持有'}

---

## 📈 数据视角

### 趋势分析
- **均线排列**: {ma_alignment}
- **MA5**: {ma5:.2f} 元
- **MA10**: {ma10:.2f} 元
- **MA20**: {ma20:.2f} 元
- **趋势强度**: {trend_strength}

### 价格分析
- **当前价**: {current_price:.2f} 元
- **乖离率(MA5)**: {bias_ma5:.2f}%
- **追高警报**: {bias_warning}
- **支撑位**: {', '.join(support_levels)}
- **压力位**: {', '.join(resistance_levels)}

### 量能分析
- **量比**: {volume_ratio:.2f}
- **量能状态**: {volume_status}
- **量价配合**: {"待分析"}

### 筹码分析
- **90%筹码集中度**: {chip_concentration:.1f}%
- **筹码状态**: {chip_status}
- **分析**: 筹码结构{chip_status}，主力控盘力度{'较强' if chip_concentration < 15 else '一般' if chip_concentration < 20 else '较弱'}

---

## 📰 情报速览

### 💭 舆情情绪
{market_sentiment}

### 🚨 风险警报
{chr(10).join([f"- {alert}" for alert in risk_alerts]) if risk_alerts else '- 暂无重大风险警报'}

### ✨ 利好催化
{chr(10).join([f"- {catalyst}" for catalyst in positive_catalysts]) if positive_catalysts else '- 暂无明显利好催化'}

### 📢 最新动态
{latest_news}

**注意**: 以上情报部分需要 Agent 执行 web_search 后填写真实搜索结果。

---

## 🎯 作战计划

### 狙击点位
- **理想买入点**: {ideal_buy:.2f} 元（回踩MA10附近）
- **止损位**: {stop_loss:.2f} 元（跌破MA20）
- **目标位**: {take_profit:.2f} 元（+15%）

### 行动检查清单
{chr(10).join(checklist)}

### 执行步骤
建议等待回调至{ideal_buy:.2f}元附近（MA10支撑），确认量能放大后分批买入，首次仓位不超过10%。

---

## ⚠️ 风险提示

- 本报告基于历史数据和客观指标生成，不构成投资建议
- 投资者应独立判断并承担投资风险
- 股市有风险，投资需谨慎

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析方法**: 数据驱动 + 交易纪律约束
"""
    
    return md


def main():
    parser = argparse.ArgumentParser(description='生成决策仪表盘 Markdown 报告')
    parser.add_argument('--stock-name', required=True, help='股票名称')
    parser.add_argument('--stock-code', required=True, help='股票代码')
    parser.add_argument('--data-dir', required=True, help='数据文件目录')
    parser.add_argument('--output', required=True, help='输出 Markdown 文件路径')
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    
    # 加载数据
    logger.info("加载数据文件...")
    realtime_data = load_realtime_data(data_dir)
    indicators_df = load_indicators(data_dir)
    risk_metrics = load_risk_metrics(data_dir)
    search_intel = load_search_intel(data_dir)
    
    # 生成决策仪表盘
    logger.info("生成决策仪表盘...")
    dashboard_md = generate_dashboard(
        args.stock_name,
        args.stock_code,
        realtime_data,
        indicators_df,
        risk_metrics,
        search_intel
    )
    
    # 保存 Markdown
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_md)
    
    logger.info("=" * 60)
    logger.info(f"✅ 决策仪表盘已生成: {output_path}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
