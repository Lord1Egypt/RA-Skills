"""Budget configuration management."""

import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class BudgetConfig:
    """Manages budget limits and configuration."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.config_file = config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default config
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "global_limits": {
                "daily": None,
                "weekly": None,
                "monthly": None
            },
            "agent_limits": {}
        }
    
    def save_config(self) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config["updated_at"] = datetime.now().isoformat()
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_global_limit(self, period: str, amount: float) -> None:
        """Set global budget limit."""
        if period not in ["daily", "weekly", "monthly"]:
            raise ValueError(f"Invalid period: {period}")
        
        self.config["global_limits"][period] = amount
        self.save_config()
    
    def set_agent_limit(self, agent: str, period: str, amount: float) -> None:
        """Set agent-specific budget limit."""
        if period not in ["daily", "weekly", "monthly"]:
            raise ValueError(f"Invalid period: {period}")
        
        if agent not in self.config["agent_limits"]:
            self.config["agent_limits"][agent] = {
                "daily": None,
                "weekly": None,
                "monthly": None
            }
        
        self.config["agent_limits"][agent][period] = amount
        self.save_config()
    
    def get_global_limit(self, period: str) -> Optional[float]:
        """Get global budget limit."""
        return self.config["global_limits"].get(period)
    
    def get_agent_limit(self, agent: str, period: str) -> Optional[float]:
        """Get agent-specific budget limit."""
        agent_config = self.config["agent_limits"].get(agent, {})
        return agent_config.get(period)
    
    def list_agents(self) -> list:
        """List all agents with configured limits."""
        return list(self.config["agent_limits"].keys())
    
    def get_all_limits(self) -> dict:
        """Get all configured limits."""
        return {
            "global": self.config["global_limits"],
            "agents": self.config["agent_limits"]
        }
