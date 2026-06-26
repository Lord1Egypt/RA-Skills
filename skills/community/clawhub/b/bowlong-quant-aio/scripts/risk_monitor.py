#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
quant-aio 风险监控系统
实时监控仓位、盈亏、回撤，及时告警

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
源码开放，欢迎完善，共同进步
GitHub: https://github.com/simonstang/bolong-quant

功能：
- 实时仓位监控
- 回撤预警
- 单日亏损限制
- 单笔亏损限制
- 异动告警（涨跌幅/成交量异常）
- Telegram推送通知
"""

import os
import sys
import time
import json
import yaml
import logging
import threading
from datetime import datetime, time as dtime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import argparse

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"  # 触发止损


class AlertType(Enum):
    """告警类型"""
    DAILY_LOSS = "daily_loss"           # 单日亏损超限
    TOTAL_DRAWDOWN = "total_drawdown"   # 总回撤超限
    POSITION_LIMIT = "position_limit"   # 仓位超限
    UNUSUAL_VOLUME = "unusual_volume"   # 异动
    TRADE_LIMIT = "trade_limit"        # 交易次数超限
    PRICE_ALERT = "price_alert"         # 价格告警
    RISK_CHECK = "risk_check"           # 风控检查通过


@dataclass
class Alert:
    """告警"""
    level: AlertLevel
    alert_type: AlertType
    title: str
    message: str
    timestamp: str = ""
    data: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class RiskMetrics:
    """风险指标"""
    total_value: float
    cash: float
    position_value: float
    position_ratio: float
    daily_pnl: float
    daily_pnl_pct: float
    total_pnl: float
    total_pnl_pct: float
    drawdown: float
    drawdown_pct: float
    trade_count_today: int
    positions: List[Dict] = field(default_factory=list)


class TelegramNotifier:
    """Telegram通知器"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}"
    
    def send(self, message: str, parse_mode: str = "Markdown") -> bool:
        """发送消息"""
        if not self.token or not self.chat_id:
            logger.warning("⚠️ Telegram未配置，跳过通知")
            return False
        
        try:
            import requests
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                logger.info(f"📱 Telegram通知已发送")
                return True
            else:
                logger.error(f"❌ Telegram发送失败: {result.get('description')}")
                return False
        
        except Exception as e:
            logger.error(f"❌ Telegram异常: {e}")
            return False
    
    def send_alert(self, alert: Alert) -> bool:
        """发送告警"""
        emoji = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🚨"
        }
        
        message = f"""{emoji.get(alert.level, "📢")} *{alert.title}*

_{alert.message}_

⏰ {alert.timestamp}"""
        
        return self.send(message)


class RiskMonitor:
    """风险监控"""
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        risk_cfg = self.config.get('risk', {})
        notify_cfg = self.config.get('notify', {})
        
        # 风控规则
        self.position_rules = risk_cfg.get('position', {})
        self.loss_rules = risk_cfg.get('loss_limit', {})
        self.alert_rules = risk_cfg.get('alert', {})
        self.trade_rules = risk_cfg.get('trade_limit', {})
        
        # 通知器
        self.notifier = None
        if notify_cfg.get('enabled'):
            telegram_cfg = notify_cfg.get('telegram', {})
            token = os.getenv('PUSH_TOKEN', telegram_cfg.get('token', ''))
            chat_id = os.getenv('PUSH_CHAT_ID', telegram_cfg.get('chat_id', ''))
            if token and chat_id:
                self.notifier = TelegramNotifier(token, chat_id)
                logger.info("✅ Telegram通知已配置")
        
        # 状态
        self.initial_cash = self.config.get('backtest', {}).get('initial_cash', 1_000_000)
        self.peak_value = self.initial_cash  # 历史最高净值
        self.today_trades = 0
        self.today_date = datetime.now().strftime('%Y-%m-%d')
        self.alerts_history: List[Alert] = []
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.check_interval = risk_cfg.get('check_interval', 60)  # 默认60秒检查一次
    
    def check_position_limit(self, position_ratio: float) -> Optional[Alert]:
        """检查仓位限制"""
        max_position = self.position_rules.get('max_total', 0.80)
        
        if position_ratio > max_position:
            return Alert(
                level=AlertLevel.WARNING,
                alert_type=AlertType.POSITION_LIMIT,
                title="⚠️ 仓位超限",
                message=f"当前仓位 {position_ratio:.1%} 超过上限 {max_position:.1%}，建议减仓",
                data={'position_ratio': position_ratio, 'limit': max_position}
            )
        
        return None
    
    def check_daily_loss(self, daily_pnl_pct: float) -> Optional[Alert]:
        """检查单日亏损"""
        max_daily_loss = self.loss_rules.get('daily', 0.02)
        
        if daily_pnl_pct < -max_daily_loss:
            return Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.DAILY_LOSS,
                title="🚨 单日亏损超限",
                message=f"今日亏损 {daily_pnl_pct:.2%} 超过止损线 {max_daily_loss:.2%}，建议平仓观望",
                data={'daily_pnl_pct': daily_pnl_pct, 'limit': -max_daily_loss}
            )
        
        return None
    
    def check_drawdown(self, total_value: float) -> Tuple[float, float]:
        """检查总回撤，返回(回撤额, 回撤比例)"""
        if total_value > self.peak_value:
            self.peak_value = total_value
        
        drawdown = self.peak_value - total_value
        drawdown_pct = drawdown / self.peak_value if self.peak_value > 0 else 0
        
        return drawdown, drawdown_pct
    
    def check_total_drawdown(self, drawdown_pct: float) -> Optional[Alert]:
        """检查总回撤限制"""
        max_drawdown = self.loss_rules.get('total_drawdown', 0.15)
        
        if drawdown_pct > max_drawdown:
            return Alert(
                level=AlertLevel.CRITICAL,
                alert_type=AlertType.TOTAL_DRAWDOWN,
                title="🚨 总回撤超限",
                message=f"当前回撤 {drawdown_pct:.2%} 超过上限 {max_drawdown:.2%}，建议清仓止损",
                data={'drawdown_pct': drawdown_pct, 'limit': max_drawdown}
            )
        
        return None
    
    def check_trade_limit(self, trade_count_today: int) -> Optional[Alert]:
        """检查交易次数限制"""
        max_trades = self.trade_rules.get('max_per_day', 20)
        
        if trade_count_today >= max_trades:
            return Alert(
                level=AlertLevel.WARNING,
                alert_type=AlertType.TRADE_LIMIT,
                title="⚠️ 今日交易次数已达上限",
                message=f"今日已交易 {trade_count_today} 次，达到上限 {max_trades} 次",
                data={'trade_count': trade_count_today, 'limit': max_trades}
            )
        
        return None
    
    def check_unusual_volume(self, symbol: str, volume_change_pct: float, 
                            threshold: float = 200) -> Optional[Alert]:
        """检查异动（量能异常）"""
        if abs(volume_change_pct) > threshold:
            direction = "放大" if volume_change_pct > 0 else "萎缩"
            return Alert(
                level=AlertLevel.WARNING,
                alert_type=AlertType.UNUSUAL_VOLUME,
                title=f"⚠️ {symbol} 成交量{direction}",
                message=f"{symbol} 成交量{direction} {abs(volume_change_pct):.0f}%，注意风险",
                data={'symbol': symbol, 'change_pct': volume_change_pct}
            )
        
        return None
    
    def check_price_alert(self, symbol: str, price_change_pct: float,
                         threshold: float = 5.0) -> Optional[Alert]:
        """检查价格异动"""
        if abs(price_change_pct) > threshold:
            direction = "大涨" if price_change_pct > 0 else "大跌"
            return Alert(
                level=AlertLevel.WARNING,
                alert_type=AlertType.PRICE_ALERT,
                title=f"⚠️ {symbol} {direction}",
                message=f"{symbol} 今日{direction} {price_change_pct:.2f}%，注意风险",
                data={'symbol': symbol, 'change_pct': price_change_pct}
            )
        
        return None
    
    def get_risk_metrics(self, account_data: Dict, positions_data: List[Dict]) -> RiskMetrics:
        """获取当前风险指标"""
        total_value = account_data.get('total_asset', 0)
        cash = account_data.get('cash', 0)
        position_value = total_value - cash
        
        position_ratio = position_value / total_value if total_value > 0 else 0
        
        daily_pnl = account_data.get('today_pnl', 0)
        daily_pnl_pct = daily_pnl / total_value if total_value > 0 else 0
        
        total_pnl = total_value - self.initial_cash
        total_pnl_pct = total_pnl / self.initial_cash if self.initial_cash > 0 else 0
        
        drawdown, drawdown_pct = self.check_drawdown(total_value)
        
        # 重置交易计数（新的一天）
        today = datetime.now().strftime('%Y-%m-%d')
        if today != self.today_date:
            self.today_trades = 0
            self.today_date = today
        
        return RiskMetrics(
            total_value=total_value,
            cash=cash,
            position_value=position_value,
            position_ratio=position_ratio,
            daily_pnl=daily_pnl,
            daily_pnl_pct=daily_pnl_pct,
            total_pnl=total_pnl,
            total_pnl_pct=total_pnl_pct,
            drawdown=drawdown,
            drawdown_pct=drawdown_pct,
            trade_count_today=self.today_trades,
            positions=positions_data
        )
    
    def check_all(self, metrics: RiskMetrics) -> List[Alert]:
        """执行所有风控检查"""
        alerts = []
        
        # 1. 仓位检查
        alert = self.check_position_limit(metrics.position_ratio)
        if alert:
            alerts.append(alert)
        
        # 2. 单日亏损检查
        alert = self.check_daily_loss(metrics.daily_pnl_pct)
        if alert:
            alerts.append(alert)
        
        # 3. 总回撤检查
        alert = self.check_total_drawdown(metrics.drawdown_pct)
        if alert:
            alerts.append(alert)
        
        # 4. 交易次数检查
        alert = self.check_trade_limit(metrics.trade_count_today)
        if alert:
            alerts.append(alert)
        
        # 5. 各持仓异动检查
        for pos in metrics.positions:
            # 价格异动
            price_change = pos.get('price_change_pct', 0)
            alert = self.check_price_alert(pos.get('symbol', ''), price_change)
            if alert:
                alerts.append(alert)
            
            # 成交量异动
            volume_change = pos.get('volume_change_pct', 0)
            alert = self.check_unusual_volume(pos.get('symbol', ''), volume_change)
            if alert:
                alerts.append(alert)
        
        return alerts
    
    def record_trade(self):
        """记录一笔交易"""
        self.today_trades += 1
        logger.debug(f"📝 交易次数: {self.today_trades}")
    
    def notify(self, alert: Alert) -> bool:
        """发送告警通知"""
        self.alerts_history.append(alert)
        
        # 记录日志
        level_str = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🚨"
        }
        
        logger.log(
            logging.WARNING if alert.level != AlertLevel.INFO else logging.INFO,
            f"{level_str.get(alert.level)} {alert.title}: {alert.message}"
        )
        
        # 发送通知
        if self.notifier:
            return self.notifier.send_alert(alert)
        
        return False
    
    def generate_report(self, metrics: RiskMetrics, alerts: List[Alert] = None) -> str:
        """生成风控报告"""
        # 状态图标
        def status(cond: bool) -> str:
            return "✅" if cond else "❌"
        
        def pct(val: float) -> str:
            return f"{val:+.2%}"
        
        max_position = self.position_rules.get('max_total', 0.80)
        max_daily_loss = self.loss_rules.get('daily', 0.02)
        max_drawdown = self.loss_rules.get('total_drawdown', 0.15)
        
        # 告警汇总
        warnings = [a for a in (alerts or []) if a.level == AlertLevel.WARNING]
        criticals = [a for a in (alerts or []) if a.level == AlertLevel.CRITICAL]
        
        report = f"""# 🔔 风控日报 · {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 💰 账户概览

| 指标 | 数值 | 状态 |
|------|------|------|
| 总资产 | {metrics.total_value:>15,.2f} | - |
| 可用资金 | {metrics.cash:>15,.2f} | - |
| 持仓市值 | {metrics.position_value:>15,.2f} | - |
| 仓位 | {metrics.position_ratio:>15.2%} | {status(metrics.position_ratio <= max_position)} |

---

## 📊 盈亏状况

| 指标 | 数值 | 限制 | 状态 |
|------|------|------|------|
| 今日盈亏 | {pct(metrics.daily_pnl_pct):>10} | > {-max_daily_loss:.2%} | {status(metrics.daily_pnl_pct >= -max_daily_loss)} |
| 总盈亏 | {pct(metrics.total_pnl_pct):>10} | - | - |
| 历史最高 | {self.peak_value:>15,.2f} | - | - |
| 当前回撤 | {pct(-metrics.drawdown_pct):>10} | < {-max_drawdown:.2%} | {status(metrics.drawdown_pct <= max_drawdown)} |

---

## 📋 持仓状况

"""
        if not metrics.positions:
            report += "_暂无持仓_\n\n"
        else:
            report += f"| 代码 | 方向 | 持仓 | 成本 | 现价 | 盈亏 | 盈亏% |\n"
            report += f"|------|------|------|------|------|------|------|\n"
            
            for pos in metrics.positions:
                direction = "多" if pos.get('direction') == 'buy' else "空"
                pnl = pos.get('unrealized_pnl', 0)
                pnl_pct = pos.get('pnl_pct', 0)
                report += f"| {pos.get('symbol', ''):<6} | {direction:<4} | {pos.get('volume', 0):>6} | {pos.get('avg_cost', 0):>6.2f} | {pos.get('current_price', 0):>6.2f} | {pnl:>+8.2f} | {pct(pnl_pct/100):>6} |\n"
            
            report += "\n"
        
        # 告警汇总
        report += f"""---

## ⚠️ 告警汇总

| 级别 | 数量 |
|------|------|
| 🚨 严重 | {len(criticals)} |
| ⚠️ 警告 | {len(warnings)} |

"""
        
        if criticals:
            report += "### 🚨 严重告警\n\n"
            for alert in criticals:
                report += f"- **{alert.title}**: {alert.message}\n"
            report += "\n"
        
        if warnings:
            report += "### ⚠️ 警告告警\n\n"
            for alert in warnings:
                report += f"- **{alert.title}**: {alert.message}\n"
            report += "\n"
        
        if not alerts:
            report += "_✅ 所有指标正常_\n\n"
        
        # 建议
        report += """---

## 💡 操作建议

"""
        suggestions = []
        
        if metrics.position_ratio > max_position:
            suggestions.append(f"⚠️ 建议减仓至{max_position:.0%}以下，当前仓位{metrics.position_ratio:.1%}")
        
        if metrics.daily_pnl_pct < -max_daily_loss:
            suggestions.append("🚨 建议平仓观望，等待机会")
        elif metrics.daily_pnl_pct < -max_daily_loss * 0.5:
            suggestions.append("⚠️ 关注仓位，控制风险")
        
        if metrics.drawdown_pct > max_drawdown * 0.7:
            suggestions.append(f"⚠️ 回撤接近上限({max_drawdown:.0%})，建议谨慎")
        
        if metrics.trade_count_today > self.trade_rules.get('max_per_day', 20) * 0.8:
            suggestions.append(f"⚠️ 今日交易次数较多({metrics.trade_count_today})，注意休息")
        
        if suggestions:
            for s in suggestions:
                report += f"- {s}\n"
        else:
            report += "- ✅ 各项指标正常，可继续执行策略\n"
        
        report += f"""
---

_风控系统 v1.0 · quant-aio_
"""
        
        return report
    
    def start_monitoring(self, get_account_func, get_positions_func):
        """
        启动实时监控（后台线程）
        
        Args:
            get_account_func: 获取账户信息的函数
            get_positions_func: 获取持仓信息的函数
        """
        if self.monitoring:
            logger.warning("⚠️ 监控已在运行中")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(get_account_func, get_positions_func),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"✅ 风控监控已启动（间隔{self.check_interval}秒）")
    
    def _monitor_loop(self, get_account_func, get_positions_func):
        """监控循环"""
        last_report_time = datetime.now()
        
        while self.monitoring:
            try:
                # 获取数据
                account_data = get_account_func()
                positions_data = get_positions_func()
                
                if account_data is None:
                    logger.warning("⚠️ 无法获取账户数据")
                    time.sleep(self.check_interval)
                    continue
                
                # 获取风险指标
                metrics = self.get_risk_metrics(account_data, positions_data or [])
                
                # 执行检查
                alerts = self.check_all(metrics)
                
                # 发送告警通知
                for alert in alerts:
                    self.notify(alert)
                
                # 每30分钟发送一次汇总报告
                now = datetime.now()
                if (now - last_report_time).seconds >= 1800:  # 30分钟
                    report = self.generate_report(metrics, alerts)
                    if self.notifier:
                        self.notifier.send(f"📊 *{now.strftime('%H:%M')} 风控汇总*\n\n" + 
                                         self._summarize_metrics(metrics))
                    last_report_time = now
                
                # 保存最新指标
                self._latest_metrics = metrics
                self._latest_alerts = alerts
                
            except Exception as e:
                logger.error(f"❌ 监控异常: {e}", exc_info=True)
            
            time.sleep(self.check_interval)
    
    def _summarize_metrics(self, metrics: RiskMetrics) -> str:
        """生成简洁的指标摘要"""
        return f"""总资产: {metrics.total_value:,.0f}
仓位: {metrics.position_ratio:.1%}
今日: {metrics.daily_pnl_pct:+.2%}
回撤: {metrics.drawdown_pct:.2%}
交易: {metrics.trade_count_today}次"""
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("⏹️ 风控监控已停止")
    
    def get_status(self) -> Dict:
        """获取监控状态"""
        return {
            'monitoring': self.monitoring,
            'initial_cash': self.initial_cash,
            'peak_value': self.peak_value,
            'today_trades': self.today_trades,
            'alerts_today': len([a for a in self.alerts_history 
                                 if a.timestamp.startswith(datetime.now().strftime('%Y-%m-%d'))]),
            'latest_metrics': self._latest_metrics if hasattr(self, '_latest_metrics') else None
        }


# ==================== 命令行 ====================

def main():
    parser = argparse.ArgumentParser(description='quant-aio 风控监控')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件')
    parser.add_argument('--once', action='store_true', help='仅检查一次')
    parser.add_argument('--interval', type=int, default=60, help='检查间隔（秒）')
    
    args = parser.parse_args()
    
    # 加载配置
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"❌ 配置加载失败: {e}")
        sys.exit(1)
    
    # 创建监控器
    monitor = RiskMonitor(args.config)
    monitor.check_interval = args.interval
    
    # 模拟数据（实际使用时替换为真实数据源）
    def mock_get_account():
        import random
        base = 1_050_000
        return {
            'total_asset': base + random.uniform(-50000, 30000),
            'cash': random.uniform(400000, 600000),
            'today_pnl': random.uniform(-15000, 20000)
        }
    
    def mock_get_positions():
        return [
            {'symbol': '600519', 'direction': 'buy', 'volume': 500, 
             'avg_cost': 1750, 'current_price': 1800, 'unrealized_pnl': 25000, 'pnl_pct': 2.86},
            {'symbol': '000858', 'direction': 'buy', 'volume': 1000,
             'avg_cost': 165, 'current_price': 162, 'unrealized_pnl': -3000, 'pnl_pct': -1.82}
        ]
    
    logger.info("⚠️ 使用模拟数据，仅供测试")
    
    if args.once:
        # 单次检查
        account = mock_get_account()
        positions = mock_get_positions()
        
        metrics = monitor.get_risk_metrics(account, positions)
        alerts = monitor.check_all(metrics)
        
        report = monitor.generate_report(metrics, alerts)
        print(report)
        
        for alert in alerts:
            if alert.level != AlertLevel.INFO:
                monitor.notify(alert)
    
    else:
        # 启动实时监控
        logger.info("📊 启动实时监控...")
        monitor.start_monitoring(mock_get_account, mock_get_positions)
        
        try:
            while True:
                time.sleep(10)
                status = monitor.get_status()
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                      f"监控中 | 仓位: {status['latest_metrics'].position_ratio:.1% if status['latest_metrics'] else 0:.1%} "
                      f"| 今日交易: {status['today_trades']}次", end='')
        except KeyboardInterrupt:
            print("\n\n⏹️ 停止监控...")
            monitor.stop_monitoring()


if __name__ == '__main__':
    main()
