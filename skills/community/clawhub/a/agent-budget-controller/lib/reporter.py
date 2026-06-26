"""Budget reporting and summaries."""

from typing import Dict, Optional
from datetime import datetime, timedelta
from .tracker import UsageTracker
from .config import BudgetConfig
from .alerts import BudgetAlerts


class BudgetReporter:
    """Generates budget reports and summaries."""
    
    def __init__(self, tracker: UsageTracker, config: BudgetConfig):
        self.tracker = tracker
        self.config = config
    
    def generate_status_report(self, agent: Optional[str] = None) -> str:
        """Generate current status report."""
        now = datetime.now()
        lines = []
        
        # Header
        lines.append(f"📊 Agent Budget Status ({now.strftime('%Y-%m-%d')})")
        lines.append("")
        
        if agent:
            # Agent-specific report
            lines.extend(self._format_agent_status(agent))
        else:
            # Global report
            lines.append("Global Limits:")
            lines.extend(self._format_period_status("daily"))
            lines.extend(self._format_period_status("weekly"))
            lines.extend(self._format_period_status("monthly"))
            lines.append("")
            
            # By agent breakdown
            agents = self._get_active_agents()
            if agents:
                lines.append("By Agent:")
                for agent_name in agents:
                    lines.extend(self._format_agent_summary(agent_name))
        
        return "\n".join(lines)
    
    def _format_period_status(self, period: str) -> list:
        """Format status for a period."""
        limit = self.config.get_global_limit(period)
        used = self.tracker.get_period_usage(period)
        
        if limit is None:
            return [f"  {period.capitalize()}: ${used:.2f} (no limit set)"]
        
        level, percentage = BudgetAlerts.get_alert_level(used, limit)
        bar = BudgetAlerts.format_percentage_bar(percentage)
        
        return [
            f"  {period.capitalize()}: ${used:.2f} / ${limit:.2f} "
            f"({percentage:.1%}) {bar}"
        ]
    
    def _format_agent_status(self, agent: str) -> list:
        """Format status for specific agent."""
        lines = [f"Agent: {agent}", ""]
        
        for period in ["daily", "weekly", "monthly"]:
            limit = self.config.get_agent_limit(agent, period)
            used = self.tracker.get_period_usage(period, agent=agent)
            
            if limit is None:
                lines.append(f"  {period.capitalize()}: ${used:.2f} (no limit)")
            else:
                level, pct = BudgetAlerts.get_alert_level(used, limit)
                bar = BudgetAlerts.format_percentage_bar(pct)
                emoji = BudgetAlerts.get_alert_emoji(level)
                lines.append(
                    f"  {emoji} {period.capitalize()}: ${used:.2f} / ${limit:.2f} "
                    f"({pct:.1%}) {bar}"
                )
        
        return lines
    
    def _get_active_agents(self) -> list:
        """Get agents with activity today."""
        return self.tracker.get_recent_agents(days=1)
    
    def _format_agent_summary(self, agent: str) -> list:
        """Format one-line summary for agent."""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        used = self.tracker.get_period_usage("daily", agent=agent)
        
        # Get model breakdown
        by_model = self.tracker.get_usage_by_model(agent, today_start)
        model_summary = ", ".join(
            f"{model.split('/')[-1]}: ${cost:.2f}" 
            for model, cost in sorted(by_model.items(), key=lambda x: -x[1])[:3]
        )
        
        return [f"  {agent}: ${used:.2f} today ({model_summary})"]
    
    def generate_period_report(self, period: str, agent: Optional[str] = None) -> str:
        """Generate detailed report for a period."""
        now = datetime.now()
        
        # Normalize period (support both 'day'/'daily', etc.)
        period_map = {
            "day": "daily",
            "daily": "daily",
            "week": "weekly", 
            "weekly": "weekly",
            "month": "monthly",
            "monthly": "monthly"
        }
        
        normalized = period_map.get(period.lower())
        if not normalized:
            return f"Invalid period: {period}"
        
        # Calculate date range
        if normalized == "daily":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            period_name = "Today"
        elif normalized == "weekly":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            period_name = "This Week"
        elif normalized == "monthly":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            period_name = "This Month"
        else:
            return f"Invalid period: {period}"
        
        lines = []
        lines.append(f"📈 Budget Report: {period_name}")
        lines.append(f"Period: {start.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
        lines.append("")
        
        if agent:
            # Agent-specific report
            used = self.tracker.get_period_usage(normalized, agent=agent)
            by_model = self.tracker.get_usage_by_model(agent, start)
            
            lines.append(f"Agent: {agent}")
            lines.append(f"Total Cost: ${used:.2f}")
            lines.append("")
            lines.append("By Model:")
            for model, cost in sorted(by_model.items(), key=lambda x: -x[1]):
                lines.append(f"  {model}: ${cost:.2f}")
        else:
            # Global report
            total_used = self.tracker.get_period_usage(normalized)
            by_agent = self.tracker.get_usage_by_agent(start)
            
            lines.append(f"Total Cost: ${total_used:.2f}")
            lines.append("")
            lines.append("By Agent:")
            for agent_name, cost in sorted(by_agent.items(), key=lambda x: -x[1]):
                lines.append(f"  {agent_name}: ${cost:.2f}")
        
        return "\n".join(lines)
    
    def check_limits(self, agent: Optional[str] = None) -> Dict[str, bool]:
        """
        Check if any limits are exceeded.
        
        Returns:
            Dict with period -> is_ok mapping
        """
        results = {}
        
        for period in ["daily", "weekly", "monthly"]:
            if agent:
                limit = self.config.get_agent_limit(agent, period)
                used = self.tracker.get_period_usage(period, agent=agent)
            else:
                limit = self.config.get_global_limit(period)
                used = self.tracker.get_period_usage(period)
            
            results[period] = not BudgetAlerts.should_block(used, limit)
        
        return results
