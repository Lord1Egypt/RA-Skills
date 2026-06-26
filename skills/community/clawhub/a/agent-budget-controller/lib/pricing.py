"""Model pricing data - per 1M tokens."""

import json
from pathlib import Path
from typing import Dict, Optional

# Default pricing (USD per 1M tokens)
# Updated as of 2026-03
DEFAULT_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "o1": {"input": 15.00, "output": 60.00},
    "o1-mini": {"input": 3.00, "output": 12.00},
}


class PricingTable:
    """Manages model pricing data."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.pricing_file = config_dir / "pricing.json"
        self.pricing = self._load_pricing()
    
    def _load_pricing(self) -> Dict[str, Dict[str, float]]:
        """Load pricing from file or use defaults."""
        if self.pricing_file.exists():
            try:
                with open(self.pricing_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return DEFAULT_PRICING.copy()
    
    def save_pricing(self) -> None:
        """Save current pricing to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.pricing_file, 'w') as f:
            json.dump(self.pricing, f, indent=2)
    
    def get_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for given token usage."""
        # Normalize model name (remove provider prefix if present)
        model_name = model.split('/')[-1] if '/' in model else model
        
        # Try exact match first
        if model_name in self.pricing:
            prices = self.pricing[model_name]
        else:
            # Try fuzzy match (e.g., "claude-sonnet-4-20250514" → "claude-sonnet-4-5")
            matched = self._fuzzy_match(model_name)
            if matched:
                prices = self.pricing[matched]
            else:
                # Unknown model - use conservative estimate
                prices = {"input": 5.00, "output": 20.00}
        
        input_cost = (input_tokens / 1_000_000) * prices["input"]
        output_cost = (output_tokens / 1_000_000) * prices["output"]
        
        return input_cost + output_cost
    
    def _fuzzy_match(self, model_name: str) -> Optional[str]:
        """Try to match model name with known models."""
        model_lower = model_name.lower()
        
        # Try prefix matching
        for known_model in self.pricing:
            if model_lower.startswith(known_model.lower().replace('-', '').replace('.', '')):
                return known_model
            if known_model.lower().replace('-', '').replace('.', '') in model_lower:
                return known_model
        
        return None
    
    def list_models(self) -> Dict[str, Dict[str, float]]:
        """Return all known models and their pricing."""
        return self.pricing.copy()
    
    def update_model(self, model: str, input_price: float, output_price: float) -> None:
        """Update or add model pricing."""
        self.pricing[model] = {"input": input_price, "output": output_price}
        self.save_pricing()
