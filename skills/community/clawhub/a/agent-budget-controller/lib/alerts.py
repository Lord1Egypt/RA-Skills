"""Budget alert logic."""

from typing import Optional, Tuple


class AlertLevel:
    """Alert severity levels."""
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    EXCEEDED = "exceeded"


class BudgetAlerts:
    """Manages budget alerts and threshold checks."""
    
    # Thresholds
    WARNING_THRESHOLD = 0.70   # 70%
    CRITICAL_THRESHOLD = 0.90  # 90%
    EXCEEDED_THRESHOLD = 1.00  # 100%
    
    @staticmethod
    def get_alert_level(used: float, limit: Optional[float]) -> Tuple[str, float]:
        """
        Get alert level for usage vs limit.
        
        Returns:
            (level, percentage) tuple
        """
        if limit is None or limit == 0:
            return AlertLevel.OK, 0.0
        
        percentage = used / limit
        
        if percentage >= BudgetAlerts.EXCEEDED_THRESHOLD:
            return AlertLevel.EXCEEDED, percentage
        elif percentage >= BudgetAlerts.CRITICAL_THRESHOLD:
            return AlertLevel.CRITICAL, percentage
        elif percentage >= BudgetAlerts.WARNING_THRESHOLD:
            return AlertLevel.WARNING, percentage
        else:
            return AlertLevel.OK, percentage
    
    @staticmethod
    def get_alert_emoji(level: str) -> str:
        """Get emoji for alert level."""
        return {
            AlertLevel.OK: "✅",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EXCEEDED: "🚫"
        }.get(level, "❓")
    
    @staticmethod
    def get_alert_color(level: str) -> str:
        """Get ANSI color code for alert level."""
        return {
            AlertLevel.OK: "\033[92m",      # Green
            AlertLevel.WARNING: "\033[93m", # Yellow
            AlertLevel.CRITICAL: "\033[91m", # Red
            AlertLevel.EXCEEDED: "\033[91m\033[1m"  # Bold Red
        }.get(level, "\033[0m")
    
    @staticmethod
    def format_percentage_bar(percentage: float, width: int = 10) -> str:
        """Format percentage as visual bar."""
        filled = int(percentage * width)
        filled = min(filled, width)  # Cap at width
        
        bar = "⬜" * filled + "⬛" * (width - filled)
        return bar
    
    @staticmethod
    def should_block(used: float, limit: Optional[float]) -> bool:
        """Check if usage should be blocked."""
        level, _ = BudgetAlerts.get_alert_level(used, limit)
        return level == AlertLevel.EXCEEDED
    
    @staticmethod
    def get_alert_message(level: str, percentage: float, 
                         period: str, agent: Optional[str] = None) -> str:
        """Generate alert message."""
        emoji = BudgetAlerts.get_alert_emoji(level)
        target = f"Agent '{agent}'" if agent else "Global"
        
        if level == AlertLevel.OK:
            return f"{emoji} {target} {period} budget is healthy ({percentage:.1%})"
        elif level == AlertLevel.WARNING:
            return f"{emoji} {target} {period} budget warning: {percentage:.1%} used"
        elif level == AlertLevel.CRITICAL:
            return f"{emoji} {target} {period} budget critical: {percentage:.1%} used!"
        elif level == AlertLevel.EXCEEDED:
            return f"{emoji} {target} {period} budget EXCEEDED: {percentage:.1%} used!"
        else:
            return f"Unknown alert level: {level}"
