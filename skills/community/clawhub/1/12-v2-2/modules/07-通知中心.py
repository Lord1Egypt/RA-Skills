# -*- coding: utf-8 -*-
"""
===================================
通知中心模块 - V2.2完整版
===================================

核心功能:
1. 整合多种通知渠道（邮件/微信/飞书/Telegram）
2. 统一消息格式
3. 优先级管理
4. 发送失败重试
5. 消息队列
6. 模板管理
7. 推送频率控制
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import queue
import threading

logger = logging.getLogger(__name__)


# ============================================
# 数据结构定义
# ============================================

class NotificationChannel(Enum):
    """通知渠道"""
    EMAIL = "email"
    WECHAT = "wechat"
    FEISHU = "feishu"
    TELEGRAM = "telegram"
    DINGTALK = "dingtalk"
    WEBHOOK = "webhook"


class NotificationPriority(Enum):
    """通知优先级"""
    LOW = 1      # 低优先级（汇总报告）
    NORMAL = 2   # 普通优先级（一般信号）
    HIGH = 3     # 高优先级（重要信号）
    URGENT = 4   # 紧急优先级（风险警报）


@dataclass
class NotificationMessage:
    """通知消息"""
    title: str                           # 消息标题
    content: str                         # 消息内容
    channel: NotificationChannel         # 目标渠道
    priority: NotificationPriority = NotificationPriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)

    # 重试信息
    retry_count: int = 0
    max_retries: int = 3
    last_error: str = ""

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    def should_retry(self) -> bool:
        """判断是否应该重试"""
        return self.retry_count < self.max_retries


@dataclass
class NotificationConfig:
    """通知配置"""
    # 邮件配置
    email_enabled: bool = False
    email_smtp_server: str = "smtp.qq.com"
    email_smtp_port: int = 587
    email_sender: str = ""
    email_password: str = ""
    email_receivers: List[str] = field(default_factory=list)

    # 企业微信配置
    wechat_enabled: bool = False
    wechat_webhook_url: str = ""

    # 飞书配置
    feishu_enabled: bool = False
    feishu_webhook_url: str = ""

    # Telegram配置
    telegram_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # 钉钉配置
    dingtalk_enabled: bool = False
    dingtalk_webhook_url: str = ""

    # 推送频率控制
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100


# ============================================
# 通知渠道基类
# ============================================

class BaseNotifier:
    """通知渠道基类"""

    channel_type: NotificationChannel = NotificationChannel.EMAIL
    name: str = "BaseNotifier"

    def __init__(self, config: NotificationConfig):
        self.config = config
        self.enabled = self._check_enabled()

    def _check_enabled(self) -> bool:
        """检查是否启用"""
        return False

    def send(self, message: NotificationMessage) -> bool:
        """发送消息"""
        if not self.enabled:
            logger.debug(f"{self.name}: 未启用")
            return False

        try:
            return self._do_send(message)
        except Exception as e:
            logger.error(f"{self.name}: 发送失败 - {e}")
            return False

    def _do_send(self, message: NotificationMessage) -> bool:
        """实际发送逻辑（子类实现）"""
        raise NotImplementedError


# ============================================
# 邮件通知渠道
# ============================================

class EmailNotifierChannel(BaseNotifier):
    """邮件通知渠道"""

    channel_type = NotificationChannel.EMAIL
    name = "EmailNotifier"

    def _check_enabled(self) -> bool:
        return self.config.email_enabled

    def _do_send(self, message: NotificationMessage) -> bool:
        """发送邮件"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.header import Header

            # 创建邮件
            msg = MIMEText(message.content, 'plain', 'utf-8')
            msg['Subject'] = Header(message.title, 'utf-8')
            msg['From'] = self.config.email_sender
            msg['To'] = ', '.join(self.config.email_receivers)

            # 发送
            with smtplib.SMTP(
                self.config.email_smtp_server,
                self.config.email_smtp_port
            ) as server:
                server.starttls()
                server.login(
                    self.config.email_sender,
                    self.config.email_password
                )
                server.send_message(msg)

            logger.info(f"{self.name}: 邮件发送成功")
            return True

        except Exception as e:
            logger.error(f"{self.name}: 发送失败 - {e}")
            return False


# ============================================
# Webhook通知渠道（企业微信/飞书/钉钉）
# ============================================

class WebhookNotifier(BaseNotifier):
    """Webhook通知渠道"""

    def __init__(self, config: NotificationConfig, channel_type: NotificationChannel):
        super().__init__(config)
        self.channel_type = channel_type

    def _check_enabled(self) -> bool:
        if self.channel_type == NotificationChannel.WECHAT:
            return self.config.wechat_enabled
        elif self.channel_type == NotificationChannel.FEISHU:
            return self.config.feishu_enabled
        elif self.channel_type == NotificationChannel.DINGTALK:
            return self.config.dingtalk_enabled
        return False

    def _get_webhook_url(self) -> str:
        """获取Webhook URL"""
        if self.channel_type == NotificationChannel.WECHAT:
            return self.config.wechat_webhook_url
        elif self.channel_type == NotificationChannel.FEISHU:
            return self.config.feishu_webhook_url
        elif self.channel_type == NotificationChannel.DINGTALK:
            return self.config.dingtalk_webhook_url
        return ""

    def _do_send(self, message: NotificationMessage) -> bool:
        """发送Webhook请求"""
        try:
            import requests

            url = self._get_webhook_url()
            if not url:
                logger.warning(f"{self.name}: 未配置Webhook URL")
                return False

            # 企业微信/飞书/钉钉格式
            if self.channel_type in [NotificationChannel.WECHAT, NotificationChannel.FEISHU]:
                payload = {
                    "msgtype": "text",
                    "text": {
                        "content": f"{message.title}\n\n{message.content}"
                    }
                }
            elif self.channel_type == NotificationChannel.DINGTALK:
                payload = {
                    "msgtype": "text",
                    "text": {
                        "content": f"{message.title}\n\n{message.content}"
                    }
                }
            else:
                payload = {
                    "title": message.title,
                    "content": message.content
                }

            response = requests.post(
                url,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"{self.name}: Webhook发送成功")
                return True
            else:
                logger.error(f"{self.name}: Webhook返回错误 {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"{self.name}: 发送失败 - {e}")
            return False


# ============================================
# Telegram通知渠道
# ============================================

class TelegramNotifier(BaseNotifier):
    """Telegram通知渠道"""

    channel_type = NotificationChannel.TELEGRAM
    name = "TelegramNotifier"

    def _check_enabled(self) -> bool:
        return self.config.telegram_enabled

    def _do_send(self, message: NotificationMessage) -> bool:
        """发送Telegram消息"""
        try:
            import requests

            url = f"https://api.telegram.org/bot{self.config.telegram_bot_token}/sendMessage"

            payload = {
                "chat_id": self.config.telegram_chat_id,
                "text": f"*{message.title}*\n\n{message.content}",
                "parse_mode": "Markdown"
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                logger.info(f"{self.name}: Telegram发送成功")
                return True
            else:
                logger.error(f"{self.name}: Telegram返回错误 {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"{self.name}: 发送失败 - {e}")
            return False


# ============================================
# 通知中心
# ============================================

class NotificationCenter:
    """
    通知中心

    功能：
    1. 整合多种通知渠道
    2. 消息队列管理
    3. 优先级处理
    4. 失败重试
    5. 频率控制
    """

    def __init__(self, config: NotificationConfig):
        """初始化通知中心"""
        self.config = config
        self.notifiers = []
        self.message_queue = queue.PriorityQueue()
        self.send_history = {}  # 发送历史记录

        # 频率控制
        self.send_count_minute = 0
        self.send_count_hour = 0
        self.last_reset = datetime.now()

        # 初始化通知渠道
        self._init_notifiers()

        # 启动发送线程
        self.running = False
        self.send_thread = None

        logger.info(f"通知中心初始化完成 (渠道数: {len(self.notifiers)})")

    def _init_notifiers(self):
        """初始化通知渠道"""
        # 邮件
        email_notifier = EmailNotifierChannel(self.config)
        self.notifiers.append(email_notifier)

        # 企业微信
        if self.config.wechat_enabled:
            wechat_notifier = WebhookNotifier(
                self.config,
                NotificationChannel.WECHAT
            )
            self.notifiers.append(wechat_notifier)

        # 飞书
        if self.config.feishu_enabled:
            feishu_notifier = WebhookNotifier(
                self.config,
                NotificationChannel.FEISHU
            )
            self.notifiers.append(feishu_notifier)

        # 钉钉
        if self.config.dingtalk_enabled:
            dingtalk_notifier = WebhookNotifier(
                self.config,
                NotificationChannel.DINGTALK
            )
            self.notifiers.append(dingtalk_notifier)

        # Telegram
        if self.config.telegram_enabled:
            telegram_notifier = TelegramNotifier(self.config)
            self.notifiers.append(telegram_notifier)

        logger.info(f"已启用渠道: {[n.name for n in self.notifiers if n.enabled]}")

    def send(
        self,
        title: str,
        content: str,
        channels: Optional[List[NotificationChannel]] = None,
        priority: NotificationPriority = NotificationPriority.NORMAL
    ):
        """
        发送通知

        Args:
            title: 消息标题
            content: 消息内容
            channels: 目标渠道列表（None表示全部）
            priority: 优先级
        """
        # 检查频率限制
        if not self._check_rate_limit():
            logger.warning("达到频率限制，消息被丢弃")
            return

        # 创建消息
        message = NotificationMessage(
            title=title,
            content=content,
            channel=channels[0] if channels else NotificationChannel.EMAIL,
            priority=priority
        )

        # 添加到队列
        self.message_queue.put((priority.value, message))

        logger.debug(f"消息已加入队列: {title}")

    def send_buy_signal(self, **kwargs):
        """发送买入信号"""
        self.send(
            title=f"🟢 买入信号: {kwargs.get('name', '')}",
            content=self._format_buy_signal(**kwargs),
            priority=NotificationPriority.HIGH
        )

    def send_sell_signal(self, **kwargs):
        """发送卖出信号"""
        self.send(
            title=f"🔴 卖出信号: {kwargs.get('name', '')}",
            content=self._format_sell_signal(**kwargs),
            priority=NotificationPriority.HIGH
        )

    def send_risk_alert(self, **kwargs):
        """发送风险警报"""
        self.send(
            title=f"⚠️ 风险警报: {kwargs.get('name', '')}",
            content=self._format_risk_alert(**kwargs),
            priority=NotificationPriority.URGENT
        )

    def send_daily_report(self, **kwargs):
        """发送每日报告"""
        self.send(
            title=f"📊 每日报告 {kwargs.get('date', '')}",
            content=self._format_daily_report(**kwargs),
            priority=NotificationPriority.LOW
        )

    def start(self):
        """启动发送线程"""
        if self.running:
            logger.warning("发送线程已在运行")
            return

        self.running = True
        self.send_thread = threading.Thread(
            target=self._send_loop,
            daemon=True
        )
        self.send_thread.start()
        logger.info("通知中心已启动")

    def stop(self):
        """停止发送线程"""
        self.running = False
        if self.send_thread:
            self.send_thread.join(timeout=5)
        logger.info("通知中心已停止")

    def _send_loop(self):
        """发送循环（在独立线程中运行）"""
        while self.running:
            try:
                # 从队列获取消息
                if self.message_queue.empty():
                    continue

                priority_value, message = self.message_queue.get(timeout=1)

                # 发送到所有渠道
                for notifier in self.notifiers:
                    if not notifier.enabled:
                        continue

                    # 发送
                    success = notifier.send(message)

                    if not success:
                        # 重试逻辑
                        message.retry_count += 1
                        if message.should_retry():
                            # 重新加入队列
                            self.message_queue.put((priority_value, message))
                            logger.warning(f"{notifier.name}: 发送失败，将重试 "
                                          f"({message.retry_count}/{message.max_retries})")

            except Exception as e:
                logger.error(f"发送循环错误: {e}")

    def _check_rate_limit(self) -> bool:
        """检查频率限制"""
        now = datetime.now()

        # 重置计数器
        if now - self.last_reset > timedelta(hours=1):
            self.send_count_minute = 0
            self.send_count_hour = 0
            self.last_reset = now

        # 检查限制
        if self.config.rate_limit_enabled:
            if (self.send_count_minute >= self.config.rate_limit_per_minute or
                self.send_count_hour >= self.config.rate_limit_per_hour):
                return False

        return True

    @staticmethod
    def _format_buy_signal(**kwargs) -> str:
        """格式化买入信号"""
        return f"""
股票: {kwargs.get('name', '')}({kwargs.get('code', '')})
买入价: {kwargs.get('price', 0):.2f}元
信号评分: {kwargs.get('signal_score', 0):.2f}/10
建议止损: {kwargs.get('stop_loss', 0):.2f}元
建议止盈: {kwargs.get('take_profit', 0):.2f}元
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()

    @staticmethod
    def _format_sell_signal(**kwargs) -> str:
        """格式化卖出信号"""
        return f"""
股票: {kwargs.get('name', '')}({kwargs.get('code', '')})
卖出价: {kwargs.get('price', 0):.2f}元
卖出原因: {kwargs.get('reason', '')}
收益率: {kwargs.get('pnl', 0)*100:+.2f}%
持仓天数: {kwargs.get('holding_days', 0)}天
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()

    @staticmethod
    def _format_risk_alert(**kwargs) -> str:
        """格式化风险警报"""
        return f"""
股票: {kwargs.get('name', '')}({kwargs.get('code', '')}
当前价格: {kwargs.get('current_price', 0):.2f}元
回撤幅度: {kwargs.get('drawdown', 0)*100:.2f}%
最大回撤: {kwargs.get('max_drawdown', 0)*100:.2f}%
风险提示: 回撤已超过预警线，请及时关注！
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()

    @staticmethod
    def _format_daily_report(**kwargs) -> str:
        """格式化每日报告"""
        positions = kwargs.get('positions', [])
        pos_str = "\n".join([
            f"  {p.get('name', '')}({p.get('code', '')}): "
            f"{'✅' if p.get('pnl', 0) > 0 else '❌'} "
            f"{p.get('pnl', 0)*100:+.2f}%"
            for p in positions[:10]
        ])

        return f"""
持仓数量: {len(positions)}
总收益率: {kwargs.get('total_pnl', 0)*100:+.2f}%
胜率: {kwargs.get('win_rate', 0)*100:.1f}%

持仓明细:
{pos_str}

时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("=" * 60)
    print("测试通知中心")
    print("=" * 60)

    # 创建配置
    config = NotificationConfig(
        email_enabled=False,  # 设为True测试邮件
        wechat_enabled=False,
        feishu_enabled=False,
        telegram_enabled=False,
        rate_limit_enabled=True
    )

    # 创建通知中心
    center = NotificationCenter(config)

    # 测试发送
    print("\n发送测试消息...")
    center.send(
        title="测试消息",
        content="这是一条测试消息",
        priority=NotificationPriority.NORMAL
    )

    print("测试完成")
    print("=" * 60)
