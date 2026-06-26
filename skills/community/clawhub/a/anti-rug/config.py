"""
Configuration module for Anti-Rug Token Security Checker.
All hardcoded values extracted for maintainability.
"""

from typing import Set, List, Dict, Any

# ══════════════════════════════════════════════════════════════
# API Configuration
# ══════════════════════════════════════════════════════════════

GOPLUS_ENDPOINTS: List[str] = [
    "https://api.gopluslabs.io",
    "https://api.gopluslabs.io",  # Retry fallback
]

REQUEST_TIMEOUT: int = 8
RETRY_WAIT: float = 1.2

# ══════════════════════════════════════════════════════════════
# Dead/Black Hole Addresses
# ══════════════════════════════════════════════════════════════

DEAD_ADDRESSES: Set[str] = {
    "0x0000000000000000000000000000000000000000",
    "0x000000000000000000000000000000000000dead",
    "0xdead000000000000000042069420694206942069",
    "0x0000000000000000000000000000000000000001",
}

# ══════════════════════════════════════════════════════════════
# Chain Configuration
# ══════════════════════════════════════════════════════════════

CHAIN_NAMES: Dict[str, str] = {
    "1":     "Ethereum Mainnet",
    "56":    "BNB Smart Chain (BSC)",
    "137":   "Polygon",
    "42161": "Arbitrum One",
    "8453":  "Base",
    "10":    "Optimism",
    "43114": "Avalanche C-Chain",
    "solana": "Solana",
}

# ══════════════════════════════════════════════════════════════
# Scenario Classification Configuration
# ══════════════════════════════════════════════════════════════

# Scenario A: Mainstream/Pegged Assets
SCENARIO_A_SYMBOLS: Set[str] = {
    "usdt", "usdc", "fdusd", "tusd", "busd", "dai", "usdd", "pyusd",
    "lusd", "frax", "usdp", "gusd", "susd", "cusd", "musd", "ousd",
    "weth", "wbtc", "wbnb", "wmatic", "wavax", "wftm", "wop",
    "btcb", "eth",
}

SCENARIO_A_NAME_KEYWORDS: List[str] = [
    "binance-peg", "peg ", " peg", "wrapped ", "bridged ",
    "tether", "circle", "usd coin", "frax", "dai stablecoin",
]

# Scenario B: Eco-value tokens threshold
SCENARIO_B_MIN_HOLDERS: int = 500

# Protocol/DEX address tags
PROTOCOL_TAGS: Set[str] = {
    "pancakeswap", "uniswap", "sushiswap", "curve", "aave", "compound",
    "venus", "alpaca", "biswap", "dodo", "balancer", "lido", "staking",
    "pool", "treasury", "reserve", "governance", "timelock", "multisig",
    "gnosis", "safe", "lock", "vesting",
}

# ══════════════════════════════════════════════════════════════
# Risk Score Weights
# ══════════════════════════════════════════════════════════════

RISK_WEIGHTS: Dict[str, float] = {
    "contract": 0.40,
    "tax": 0.25,
    "liquidity": 0.20,
    "concentration": 0.15,
}

# Scenario-specific weight adjustments
SCENARIO_WEIGHTS: Dict[str, Dict[str, float]] = {
    "A": {"contract": 0.50, "tax": 0.30, "liquidity": 0.10, "concentration": 0.10},
    "B": {"contract": 0.40, "tax": 0.20, "liquidity": 0.20, "concentration": 0.20},
    "C": {"contract": 0.35, "tax": 0.25, "liquidity": 0.20, "concentration": 0.20},
}

# ══════════════════════════════════════════════════════════════
# Fatal Rules Configuration
# ══════════════════════════════════════════════════════════════

FATAL_RULES: List[Dict[str, Any]] = [
    {
        "check": lambda ind: ind.get("is_honeypot", False),
        "code": "HONEYPOT",
        "description": "🛑 貔貅盘（Honeypot）",
        "implication": "代币无法卖出，买入资金将被永久锁死",
    },
    {
        "check": lambda ind: ind.get("sell_tax", 0) > 50,
        "code": "EXTREME_TAX",
        "description": "🛑 极端卖出税率",
        "implication": "卖出税超过50%，资金实际上无法退出",
    },
    {
        "check": lambda ind: ind.get("selfdestruct", False),
        "code": "SELFDESTRUCT",
        "description": "🛑 合约自毁函数",
        "implication": "团队可随时销毁合约，导致代币归零",
    },
    {
        "check": lambda ind: ind.get("hidden_owner", False),
        "code": "HIDDEN_OWNER",
        "description": "🛑 隐藏 Owner",
        "implication": "合约实际控制权被隐匿，极度危险",
    },
    {
        "check": lambda ind: ind.get("can_take_back_ownership", False),
        "code": "OWNERSHIP_RECLAIM",
        "description": "🛑 Owner 权限可被夺回",
        "implication": "即使显示已 Renounce，团队仍可通过隐藏机制重新取得控制权",
    },
    {
        "check": lambda ind: ind.get("owner_change_balance", False),
        "code": "BALANCE_MANIPULATION",
        "description": "🛑 Owner 可修改余额",
        "implication": "团队可任意修改账户余额，随时清零用户持仓",
    },
]
