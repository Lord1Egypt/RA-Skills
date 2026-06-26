"""
DEX Agent Configuration — Base Chain
Direct DEX trading with zero middleman fees.
Our fee: 0.3% on swaps (vs Bankr's 0.65%)
"""

# Base Chain
CHAIN_ID = 8453
RPC_URL = "https://base.llamarpc.com"
BACKUP_RPC = "https://mainnet.base.org"

# Wallet (Bankr custodial wallet — for reading only)
# We need to generate our own wallet for direct trading
BANKR_WALLET = "0xc53D43b614Bc53000513b44B162a1F5efD2E553d"

# Key Token Addresses on Base
TOKENS = {
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDbC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",  # Bridged USDC
    "AERO": "0x940181a94A35A4569E4529A3CDFb74e38FD98631",
    "BRETT": "0x532f27101965dd16442E59d40670FaF5eBB142E4",
    "DEGEN": "0x4ed4E862860beD51a9570b96d89aF5E1B0Efefed",
}

# Uniswap V3 Contracts on Base
UNISWAP = {
    "factory": "0x33128a8fC17869897dcE68Ed026d694621f6FDfD",
    "swap_router_02": "0x2626664c2603336E57B271c5C0b26F421741e481",
    "quoter_v2": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
    "universal_router": "0x6fF5693b99212Da76ad316178A184AB56D299b43",
    "position_manager": "0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1",
}

# Aerodrome Contracts on Base
AERODROME = {
    "router": "0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43",
    "factory": "0x420DD381b31aEf6683db6B902084cB0FFECe40Da",
}

# Trading Parameters
DEFAULT_SLIPPAGE_BPS = 100  # 1% default slippage
MAX_SLIPPAGE_BPS = 500      # 5% max slippage
GAS_LIMIT = 350_000
OUR_FEE_BPS = 30            # 0.3% our fee (vs Bankr's 0.65%)

# Risk Management Defaults
# These can be overridden via trading-config.json at runtime
RISK_DEFAULTS = {
    "max_daily_trades": 8,        # Max new trades per 24h period
    "max_active_positions": 8,    # Max concurrent open positions
    "trade_size_usd": 20,         # Default trade size in USD
    "take_profit_pct": 5.0,       # Take profit trigger (%)
    "stop_loss_pct": 8.0,         # Stop loss trigger (%)
    "max_drawdown_pct": 20.0,     # Max portfolio drawdown before halt
    "cooldown_minutes": 60,       # Min time between trades on same token
    "min_liquidity": 50000,       # Min pool liquidity (USD)
    "min_volume_24h": 100000,     # Min 24h volume (USD)
}

# Fee Collection Wallet (separate from trading wallet)
# TODO: Set up fee collection wallet
FEE_WALLET = None
