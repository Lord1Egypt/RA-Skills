"""Usage tracking with JSONL append-only log."""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class UsageTracker:
    """Tracks LLM API usage and costs."""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.usage_log = data_dir / "usage.jsonl"
    
    def log_usage(self, agent: str, model: str, input_tokens: int, 
                  output_tokens: int, cost: float) -> None:
        """Append usage record to log."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost
        }
        
        with open(self.usage_log, 'a') as f:
            f.write(json.dumps(record) + '\n')
    
    def get_usage(self, agent: Optional[str] = None, 
                  start_date: Optional[datetime] = None,
                  end_date: Optional[datetime] = None) -> List[dict]:
        """Get usage records with optional filters."""
        if not self.usage_log.exists():
            return []
        
        records = []
        with open(self.usage_log, 'r') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    
                    # Apply filters
                    if agent and record.get("agent") != agent:
                        continue
                    
                    record_time = datetime.fromisoformat(record["timestamp"])
                    if start_date and record_time < start_date:
                        continue
                    if end_date and record_time > end_date:
                        continue
                    
                    records.append(record)
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return records
    
    def get_period_usage(self, period: str, agent: Optional[str] = None) -> float:
        """Get total cost for a period (day/week/month)."""
        now = datetime.now()
        
        if period == "daily":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            # Start of week (Monday)
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "monthly":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Invalid period: {period}")
        
        records = self.get_usage(agent=agent, start_date=start)
        return sum(r.get("cost", 0) for r in records)
    
    def get_usage_by_agent(self, start_date: datetime, end_date: Optional[datetime] = None) -> Dict[str, float]:
        """Get usage breakdown by agent."""
        records = self.get_usage(start_date=start_date, end_date=end_date)
        
        by_agent = defaultdict(float)
        for record in records:
            by_agent[record["agent"]] += record.get("cost", 0)
        
        return dict(by_agent)
    
    def get_usage_by_model(self, agent: str, start_date: datetime, 
                           end_date: Optional[datetime] = None) -> Dict[str, float]:
        """Get usage breakdown by model for an agent."""
        records = self.get_usage(agent=agent, start_date=start_date, end_date=end_date)
        
        by_model = defaultdict(float)
        for record in records:
            by_model[record["model"]] += record.get("cost", 0)
        
        return dict(by_model)
    
    def get_recent_agents(self, days: int = 7) -> List[str]:
        """Get list of agents with activity in recent days."""
        start = datetime.now() - timedelta(days=days)
        records = self.get_usage(start_date=start)
        
        agents = set(r["agent"] for r in records)
        return sorted(agents)
