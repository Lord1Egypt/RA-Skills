# -*- coding: utf-8 -*-
"""
===================================
邮件通知模块 - V2.2
===================================

设计参考: daily_stock_analysis的NotificationService

核心功能:
1. SMTP邮件发送
2. 多种推送类型（买入/卖出/警报/汇总）
3. 模板化消息格式
4. 支持多个收件人
5. 推送开关配置
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

class NotificationType(Enum):
    """通知类型"""
    BUY_SIGNAL = "buy_signal"           # 买入信号
    SELL_SIGNAL = "sell_signal"         # 卖出信号
    RISK_ALERT = "risk_alert"           # 风险警报
    DAILY_REPORT = "daily_report"       # 每日报告
    MARKET_REVIEW = "market_review"     # 大盘复盘
    SYSTEM_ALERT = "system_alert"       # 系统警报


@dataclass
class NotificationConfig:
    """通知配置"""
    enabled: bool = False                      # 总开关
    smtp_server: str = "smtp.qq.com"          # SMTP服务器
    smtp_port: int = 587                      # SMTP端口
    sender: str = ""                          # 发件人邮箱
    password: str = ""                        # 邮箱授权码
    receivers: List[str] = None               # 收件人列表

    # 推送类型开关
    send_buy_signal: bool = True
    send_sell_signal: bool = True
    send_risk_alert: bool = True
    send_daily_report: bool = False
    send_market_review: bool = False

    def __post_init__(self):
        if self.receivers is None:
            self.receivers = []


# ============================================
# 邮件通知器
# ============================================

class EmailNotifier:
    """
    邮件通知器

    功能：
    1. 买入信号推送
    2. 卖出信号推送
    3. 风险警报推送
    4. 每日汇总报告
    5. 大盘复盘推送
    """

    def __init__(self, config: NotificationConfig):
        """
        初始化通知器

        Args:
            config: 通知配置
        """
        self.config = config

        if not self.config.enabled:
            logger.info("邮件通知已禁用")
            return

        if not self.config.sender or not self.config.password:
            logger.warning("邮件配置不完整，通知功能不可用")
            return

        logger.info(f"邮件通知器初始化完成 (发件人: {self.config.sender})")

    def is_enabled(self, notification_type: NotificationType) -> bool:
        """
        检查指定类型的通知是否启用

        Args:
            notification_type: 通知类型

        Returns:
            bool: 是否启用
        """
        if not self.config.enabled:
            return False

        type_map = {
            NotificationType.BUY_SIGNAL: self.config.send_buy_signal,
            NotificationType.SELL_SIGNAL: self.config.send_sell_signal,
            NotificationType.RISK_ALERT: self.config.send_risk_alert,
            NotificationType.DAILY_REPORT: self.config.send_daily_report,
            NotificationType.MARKET_REVIEW: self.config.send_market_review,
            NotificationType.SYSTEM_ALERT: True,
        }

        return type_map.get(notification_type, False)

    def send_buy_signal(
        self,
        code: str,
        name: str,
        price: float,
        signal_score: float,
        market_env: str = "neutral"
    ):
        """
        发送买入信号

        Args:
            code: 股票代码
            name: 股票名称
            price: 买入价格
            signal_score: 信号评分
            market_env: 市场环境
        """
        if not self.is_enabled(NotificationType.BUY_SIGNAL):
            return

        subject = f"🟢 买入信号: {name}({code})"

        # 止损止盈价位
        stop_loss_price = price * 0.95
        take_profit_price = price * 1.10

        body = f"""
{'='*60}
买入信号触发
{'='*60}

📌 股票信息:
  股票: {name}({code})
  买入价: {price:.2f}元
  信号评分: {signal_score:.2f}/10
  市场环境: {market_env}

📊 交易建议:
  止损价: {stop_loss_price:.2f}元 (-5%)
  目标价: {take_profit_price:.2f}元 (+10%)

⏰ 交易时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 操作提示:
  - 建议开盘后买入
  - 严格执行止损纪律
  - 达到目标价分批止盈

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.info(f"发送买入信号: {name}({code})")

    def send_sell_signal(
        self,
        code: str,
        name: str,
        price: float,
        reason: str,
        buy_price: float,
        holding_days: int
    ):
        """
        发送卖出信号

        Args:
            code: 股票代码
            name: 股票名称
            price: 卖出价格
            reason: 卖出原因
            buy_price: 买入价格
            holding_days: 持仓天数
        """
        if not self.is_enabled(NotificationType.SELL_SIGNAL):
            return

        # 计算收益率
        pnl = (price - buy_price) / buy_price * 100
        pnl_amount = price - buy_price

        # 判断盈亏
        emoji = "✅" if pnl > 0 else "❌"
        status = "盈利" if pnl > 0 else "亏损"

        subject = f"🔴 卖出信号: {name}({code})"

        body = f"""
{'='*60}
卖出信号触发
{'='*60}

📌 股票信息:
  股票: {name}({code})
  卖出价: {price:.2f}元
  买入价: {buy_price:.2f}元
  卖出原因: {reason}

💰 收益情况:
  {emoji} {status}: {pnl:+.2f}%
  盈亏额: {pnl_amount:+.2f}元/股
  持仓天数: {holding_days}天

⏰ 交易时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.info(f"发送卖出信号: {name}({code}), 原因: {reason}")

    def send_risk_alert(
        self,
        code: str,
        name: str,
        current_price: float,
        drawdown: float,
        max_drawdown: float
    ):
        """
        发送风险警报

        Args:
            code: 股票代码
            name: 股票名称
            current_price: 当前价格
            drawdown: 当前回撤
            max_drawdown: 最大回撤
        """
        if not self.is_enabled(NotificationType.RISK_ALERT):
            return

        subject = f"⚠️ 风险警报: {name}({code})"

        # 判断警报级别
        if drawdown < -0.08:
            level = "🔴 严重"
        elif drawdown < -0.05:
            level = "🟠 警告"
        else:
            level = "🟡 注意"

        body = f"""
{'='*60}
风险警报触发
{'='*60}

📌 股票信息:
  股票: {name}({code})
  当前价格: {current_price:.2f}元

⚠️  风险指标:
  警报级别: {level}
  当前回撤: {drawdown*100:.2f}%
  最大回撤: {max_drawdown*100:.2f}%

💡 风险提示:
  - 回撤已超过预警线
  - 请及时关注持仓
  - 建议设置止损保护

⏰ 警报时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.warning(f"发送风险警报: {name}({code}), 回撤: {drawdown*100:.2f}%")

    def send_daily_report(
        self,
        positions: List[Dict],
        total_pnl: float,
        win_rate: float,
        market_env: str
    ):
        """
        发送每日汇总报告

        Args:
            positions: 持仓列表
            total_pnl: 总收益率
            win_rate: 胜率
            market_env: 市场环境
        """
        if not self.is_enabled(NotificationType.DAILY_REPORT):
            return

        # 统计持仓
        total_positions = len(positions)
        profitable_positions = sum(1 for p in positions if p.get('pnl', 0) > 0)

        subject = f"📊 每日交易报告 {datetime.now().strftime('%Y-%m-%d')}"

        # 持仓明细
        positions_str = ""
        if positions:
            positions_str = "\n持仓明细:\n"
            for p in positions[:10]:  # 最多显示10个
                code = p.get('code', '')
                name = p.get('name', '')
                pnl = p.get('pnl', 0) * 100
                emoji = "✅" if pnl > 0 else "❌"
                positions_str += f"  {emoji} {name}({code}): {pnl:+.2f}%\n"

            if len(positions) > 10:
                positions_str += f"  ... 还有 {len(positions)-10} 只股票\n"

        body = f"""
{'='*60}
每日交易汇总报告
{'='*60}

📈 整体表现:
  持仓数量: {total_positions}
  盈利股票: {profitable_positions}/{total_positions}
  总收益率: {total_pnl*100:+.2f}%
  交易胜率: {win_rate*100:.1f}%

🌍 市场环境: {market_env.upper()}

{positions_str}

⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 今日总结:
  - {'收益良好' if total_pnl > 0 else '收益不佳，需调整策略'}
  - {'胜率达标' if win_rate > 0.5 else '胜率待提升'}
  - 建议继续严格执行交易纪律

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.info(f"发送每日报告: 持仓{total_positions}只, 收益{total_pnl*100:+.2f}%")

    def send_market_review(
        self,
        overview: Dict[str, Any],
        environment: str
    ):
        """
        发送大盘复盘

        Args:
            overview: 市场概览
            environment: 市场环境
        """
        if not self.is_enabled(NotificationType.MARKET_REVIEW):
            return

        subject = f"🌏 大盘复盘 {datetime.now().strftime('%Y-%m-%d')}"

        # 指数信息
        indices_str = ""
        for idx in overview.get('indices', []):
            name = idx.get('name', '')
            current = idx.get('current', 0)
            change_pct = idx.get('change_pct', 0)
            emoji = "🟢" if change_pct > 0 else "🔴"
            indices_str += f"  {emoji} {name}: {current:.2f} ({change_pct:+.2f}%)\n"

        # 市场统计
        stats = overview.get('statistics', {})
        if stats:
            stats_str = f"""
  上涨: {stats.get('up_count', 0)} | 下跌: {stats.get('down_count', 0)}
  涨停: {stats.get('limit_up_count', 0)} | 跌停: {stats.get('limit_down_count', 0)}
  成交额: {stats.get('total_amount', 0):.0f}亿"""
        else:
            stats_str = "  数据获取失败"

        body = f"""
{'='*60}
大盘复盘
{'='*60}

📊 主要指数:
{indices_str}

📈 市场统计:
{stats_str}

🌍 市场环境: {environment.upper()}

💡 交易建议:
  - 当前市场{environment}，建议{'正常交易' if environment == 'strong' else '谨慎观望' if environment == 'weak' else '提高门槛'}
  - 买入阈值: {8.5 if environment == 'strong' else 9.5 if environment == 'weak' else 9.0}

⏰ 复盘时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.info(f"发送大盘复盘: 环境={environment}")

    def send_system_alert(self, message: str, level: str = "info"):
        """
        发送系统警报

        Args:
            message: 警报消息
            level: 警报级别 (info/warning/error)
        """
        if not self.is_enabled(NotificationType.SYSTEM_ALERT):
            return

        level_emoji = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '🔴',
        }.get(level, 'ℹ️')

        subject = f"{level_emoji} 系统通知"

        body = f"""
{'='*60}
系统通知
{'='*60}

{message}

⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
AI量化交易系统 V2.2
{'='*60}
        """

        self._send(subject, body)
        logger.info(f"发送系统通知: {message}")

    def _send(self, subject: str, body: str):
        """
        发送邮件

        Args:
            subject: 邮件主题
            body: 邮件内容
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.header import Header

            # 创建邮件
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = self.config.sender
            msg['To'] = ', '.join(self.config.receivers)

            # 连接SMTP服务器
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()  # 启用TLS
                server.login(self.config.sender, self.config.password)
                server.send_message(msg)

            logger.info(f"邮件发送成功: {subject}")

        except Exception as e:
            logger.error(f"邮件发送失败: {e}")


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("测试邮件通知器")
    print("=" * 60)

    # 创建配置（请替换为真实配置）
    config = NotificationConfig(
        enabled=True,  # 设为True才会真正发送
        smtp_server="smtp.qq.com",
        smtp_port=587,
        sender="your_email@qq.com",
        password="your_authorization_code",  # 注意：不是QQ密码，是授权码
        receivers=["receiver@example.com"],
        send_buy_signal=True,
        send_sell_signal=True,
        send_risk_alert=True,
        send_daily_report=True,
    )

    # 创建通知器
    notifier = EmailNotifier(config)

    # 测试各种通知
    print("\n1. 测试买入信号通知...")
    notifier.send_buy_signal(
        code="600519",
        name="贵州茅台",
        price=1680.00,
        signal_score=8.8,
        market_env="strong"
    )

    print("\n2. 测试卖出信号通知...")
    notifier.send_sell_signal(
        code="600519",
        name="贵州茅台",
        price=1750.00,
        reason="止盈",
        buy_price=1680.00,
        holding_days=15
    )

    print("\n3. 测试风险警报通知...")
    notifier.send_risk_alert(
        code="600519",
        name="贵州茅台",
        current_price=1600.00,
        drawdown=-0.08,
        max_drawdown=-0.10
    )

    print("\n4. 测试每日报告通知...")
    positions = [
        {'code': '600519', 'name': '贵州茅台', 'pnl': 0.042},
        {'code': '000858', 'name': '五粮液', 'pnl': -0.015},
        {'code': '600036', 'name': '招商银行', 'pnl': 0.025},
    ]
    notifier.send_daily_report(
        positions=positions,
        total_pnl=0.017,
        win_rate=0.67,
        market_env="neutral"
    )

    print("\n5. 测试系统通知...")
    notifier.send_system_alert("系统启动成功", level="info")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n注意: 上述邮件不会真正发送，因为配置中的enabled=False")
    print("如需真实发送，请:")
    print("1. 设置config.enabled=True")
    print("2. 填写真实的SMTP配置")
    print("3. 替换收件人地址")
