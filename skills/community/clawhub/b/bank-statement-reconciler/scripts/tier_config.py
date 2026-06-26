"""
Tier Configuration for Bank Statement Reconciler
"""
from typing import Optional


# Token prefixes for each tier
TOKEN_PREFIXES = {
    "FREE": "BANK-FREE",
    "BASIC": "BANK-BSC",
    "STANDARD": "BANK-STD",
    "PROFESSIONAL": "BANK-PRO",
    "ENTERPRISE": "BANK-ENT",
}

# Plan IDs (to be filled by yk global backend)
PLAN_IDS = {
    "FREE": None,       # TBD
    "BASIC": None,      # TBD
    "STANDARD": None,   # TBD
    "PROFESSIONAL": None,  # TBD
    "ENTERPRISE": None, # TBD
}


class TierConfig:
    """
    Tier configuration for Bank Statement Reconciler.
    
    Determines feature access based on subscription tier.
    """
    
    def __init__(
        self,
        token: str = None,
        plan_id: str = None,
        tier_name: str = None,
        is_pro: bool = False,
    ):
        """
        Initialize tier configuration.
        
        Args:
            token: User's token (checked for prefix)
            plan_id: Plan ID from subscription
            tier_name: Explicit tier name override
            is_pro: Simple flag for Professional+ features
        """
        self.token = token
        self.plan_id = plan_id
        self.tier_name = tier_name or self._detect_tier()
        self.is_pro = is_pro or self._is_pro_tier()
    
    def _detect_tier(self) -> str:
        """Detect tier from token prefix or plan_id."""
        if not self.token:
            return "FREE"
        
        token_upper = self.token.upper()
        
        for tier_name, prefix in TOKEN_PREFIXES.items():
            if token_upper.startswith(prefix):
                return tier_name
        
        return "FREE"
    
    def _is_pro_tier(self) -> bool:
        """Check if current tier is Professional or higher."""
        pro_tiers = ["PROFESSIONAL", "ENTERPRISE"]
        return self.tier_name in pro_tiers
    
    def get_limits(self) -> dict:
        """Get limits for current tier."""
        limits = {
            "FREE": {
                "monthly_statements": 50,
                "bank_accounts": 1,
                "output_formats": ["text"],
                "alipay_wechat": False,
                "paypal_stripe": False,
                "semantic_matching": False,
                "custom_rules": False,
                "feishu_card": False,
            },
            "BASIC": {
                "monthly_statements": 500,
                "bank_accounts": 3,
                "output_formats": ["text", "excel"],
                "alipay_wechat": False,
                "paypal_stripe": False,
                "semantic_matching": False,
                "custom_rules": False,
                "feishu_card": False,
            },
            "STANDARD": {
                "monthly_statements": 5000,
                "bank_accounts": -1,  # unlimited
                "output_formats": ["text", "excel"],
                "alipay_wechat": True,
                "paypal_stripe": False,
                "semantic_matching": False,
                "custom_rules": False,
                "feishu_card": True,
            },
            "PROFESSIONAL": {
                "monthly_statements": -1,  # unlimited
                "bank_accounts": -1,
                "output_formats": ["text", "excel", "json"],
                "alipay_wechat": True,
                "paypal_stripe": True,
                "semantic_matching": True,
                "custom_rules": False,
                "feishu_card": True,
            },
            "ENTERPRISE": {
                "monthly_statements": -1,
                "bank_accounts": -1,
                "output_formats": ["text", "excel", "json", "api"],
                "alipay_wechat": True,
                "paypal_stripe": True,
                "semantic_matching": True,
                "custom_rules": True,
                "feishu_card": True,
            },
        }
        
        return limits.get(self.tier_name, limits["FREE"])
    
    def can_export_excel(self) -> bool:
        """Check if Excel export is available."""
        formats = self.get_limits().get("output_formats", [])
        return "excel" in formats
    
    def can_use_semantic(self) -> bool:
        """Check if semantic matching is available."""
        return self.get_limits().get("semantic_matching", False)
    
    def can_push_feishu(self) -> bool:
        """Check if Feishu card push is available."""
        return self.get_limits().get("feishu_card", False)
    
    def supports_platform(self, platform: str) -> bool:
        """Check if a specific platform is supported."""
        limits = self.get_limits()
        
        if platform in ["alipay", "wechat"]:
            return limits.get("alipay_wechat", False)
        elif platform in ["paypal", "stripe"]:
            return limits.get("paypal_stripe", False)
        elif platform in ["boc", "icbc", "ccb", "abc", "amazon", "shopify", "temu"]:
            return True  # All tiers support these
        
        return False
    
    def check_limit(self, statement_count: int) -> bool:
        """Check if statement count is within limits."""
        limit = self.get_limits().get("monthly_statements", 50)
        
        if limit == -1:  # Unlimited
            return True
        
        return statement_count <= limit
    
    def validate_token(self, token: str) -> bool:
        """Validate that token matches expected prefix for tier."""
        if not token:
            return True  # No token = Free tier
        
        token_upper = token.upper()
        expected_prefix = TOKEN_PREFIXES.get(self.tier_name, "")
        
        if not expected_prefix:
            return True
        
        return token_upper.startswith(expected_prefix)


def validate_token_for_tier(token: str, required_tier: str) -> bool:
    """
    Validate that a token has the required tier prefix.
    
    Args:
        token: User's token
        required_tier: Minimum required tier name
    
    Returns:
        True if token is valid for the tier
    """
    if not token:
        # No token = Free tier
        return required_tier == "FREE"
    
    token_upper = token.upper()
    required_prefix = TOKEN_PREFIXES.get(required_tier, "")
    
    if not required_prefix:
        return True
    
    return token_upper.startswith(required_prefix)
