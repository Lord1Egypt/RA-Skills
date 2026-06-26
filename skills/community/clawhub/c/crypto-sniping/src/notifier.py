"""Notification system for alerts and trade updates."""
import logging
import os
from typing import Optional
import requests

from .signals import Signal
from .trader import Trade, Position
from .whale_tracker import WhaleAlert

class Notifier:
    """Send notifications via Telegram and logging."""
    
    def __init__(self, telegram_token: Optional[str] = None, 
                 telegram_chat_id: Optional[str] = None):
        self.telegram_token = telegram_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.telegram_token and self.telegram_chat_id)
        
        if not self.enabled:
            logging.warning("Telegram notifications disabled - set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
    
    def _send_telegram(self, message: str):
        """Send message via Telegram."""
        if not self.enabled:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")
    
    def notify_signal(self, signal: Signal):
        """Notify about trading signal."""
        emoji = "🟢" if signal.type.value == "buy" else "🔴" if signal.type.value == "sell" else "⚪"
        confidence_stars = "⭐" * signal.confidence
        
        message = f"""
{emoji} **Trading Signal: {signal.type.value.upper()}**

**Confidence:** {confidence_stars} ({signal.confidence}/5)
**Price:** ${signal.price:,.2f}
**Indicators:** {', '.join(signal.indicators)}

_Execute with caution_
"""
        logging.info(f"Signal: {signal.type.value} {signal.symbol} @ ${signal.price}")
        self._send_telegram(message)
    
    def notify_trade_opened(self, trade: Trade):
        """Notify about opened trade."""
        emoji = "🚀" if trade.side == "BUY" else "📉"
        
        message = f"""
{emoji} **Position Opened**

**Symbol:** {trade.symbol}
**Side:** {trade.side}
**Entry:** ${trade.entry_price:,.2f}
**Size:** {trade.quantity:.6f}
**Value:** ${trade.quantity * trade.entry_price:,.2f}

_Good luck! 🎯_
"""
        logging.info(f"Opened {trade.side} {trade.symbol} @ ${trade.entry_price}")
        self._send_telegram(message)
    
    def notify_trade_closed(self, trade: Trade):
        """Notify about closed trade."""
        if trade.pnl is None:
            return
        
        emoji = "✅" if trade.pnl > 0 else "❌"
        pnl_emoji = "📈" if trade.pnl > 0 else "📉"
        
        message = f"""
{emoji} **Position Closed**

**Symbol:** {trade.symbol}
**Side:** {trade.side}
**Entry:** ${trade.entry_price:,.2f}
**Exit:** ${trade.exit_price:,.2f}
{pnl_emoji} **P&L:** ${trade.pnl:,.2f} ({trade.pnl_percent:+.2f}%)

_Next trade loading..._
"""
        logging.info(f"Closed {trade.symbol} P&L: ${trade.pnl:.2f}")
        self._send_telegram(message)
    
    def notify_whale_alert(self, alert: WhaleAlert):
        """Notify about whale activity."""
        emoji_map = {
            "LARGE_ORDER": "🐋",
            "LIQUIDATION": "💥",
            "FUNDING_SPIKE": "⚡"
        }
        emoji = emoji_map.get(alert.type, "📊")
        
        message = f"""
{emoji} **Whale Alert: {alert.type}**

**Symbol:** {alert.symbol}
**Side:** {alert.side}
**Size:** ${alert.total_value:,.0f}
**Price:** ${alert.price:,.2f}

_{alert.details}_
"""
        logging.info(f"Whale: {alert.type} {alert.symbol} ${alert.total_value:,.0f}")
        self._send_telegram(message)
    
    def notify_daily_summary(self, trades: int, pnl: float, open_positions: int):
        """Send daily trading summary."""
        emoji = "🟢" if pnl >= 0 else "🔴"
        
        message = f"""
{emoji} **Daily Trading Summary**

**Trades:** {trades}
**P&L:** ${pnl:,.2f}
**Open Positions:** {open_positions}

_Keep building 📈_
"""
        self._send_telegram(message)
    
    def notify_error(self, error_message: str):
        """Notify about error."""
        logging.error(error_message)
        
        message = f"""
⚠️ **Bot Error**

```{error_message}```

_Check logs for details_
"""
        self._send_telegram(message)
