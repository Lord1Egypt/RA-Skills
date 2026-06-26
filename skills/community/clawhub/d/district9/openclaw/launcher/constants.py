"""
Hardcoded constants for DISTRICT9 token launches.

These values are NOT configurable by users. They are the core of the
DISTRICT9 identification and revenue mechanism:
- Want your token on DISTRICT9? Pay 0.5% tax.
- Don't want to pay? Your token won't appear on DISTRICT9.
"""

# ─────────────────────────────────────────────
# DISTRICT9 Treasury — receives 0.5% of every trade
# ─────────────────────────────────────────────
DISTRICT9_TREASURY = "0x9BAe1a391f979e92200027684a73591FD83C9EFD"

# ─────────────────────────────────────────────
# Tax configuration (immutable)
# ─────────────────────────────────────────────

# Forced tax rate: 100 = 1% (Flap uses basis points / 100)
FORCED_TAX_RATE = 100

# Split: 50% of tax → DISTRICT9, 50% → Agent
DISTRICT9_SHARE_BPS = 5000  # 50% of tax → 0.5% of trade
AGENT_SHARE_BPS = 5000      # 50% of tax → 0.5% of trade

# Tax duration (~100 years in seconds) — required by VaultPortal
TAX_DURATION = 3_153_600_000

# Anti-farmer duration (3 days in seconds)
ANTI_FARMER_DURATION = 259_200

# Minimum token balance for vault share distributions (10k tokens, 18 decimals)
MIN_SHARE_BALANCE = 10_000 * 10**18

# ─────────────────────────────────────────────
# Metadata tags — [D9:AgentName] format
# ─────────────────────────────────────────────
D9_TAG_PREFIX = "[D9:"
D9_TAG_SUFFIX = "]"

# ─────────────────────────────────────────────
# Flap Portal contract addresses
# ─────────────────────────────────────────────
CONTRACTS = {
    "bnb": {
        "portal": "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0",
        "vault_portal": "0x90497450f2a706f1951b5bdda52B4E5d16f34C06",
        "split_vault_factory": "0xfab75Dc774cB9B38b91749B8833360B46a52345F",
        "token_impl": "0x8b4329947e34b6d56d71a3385cac122bade7d78d",
        "tax_token_v1_impl": "0x29e6383F0ce68507b5A72a53c2B118a118332aA8",
        "tax_token_v2_impl": "0xae562c6A05b798499507c6276C6Ed796027807BA",
        "rpc": "https://bsc-dataseed.binance.org/",
        "chain_id": 56,
        "explorer": "https://bscscan.com",
    },
    "bnb_testnet": {
        "portal": "0x5bEacaF7ABCbB3aB280e80D007FD31fcE26510e9",
        "vault_portal": "0x027e3704fC5C16522e9393d04C60A3ac5c0d775f",
        "split_vault_factory": "0x1ae091F75D593eb7dC6539600a185C8A6076A424",
        "token_impl": "0x87D5f292ba33011997641C7a7Bd2b17799aaA814",
        "tax_token_v1_impl": "0x87d8D03d0c3E064ACdb48E42fecbE8a8538dE6Fc",
        "tax_token_v2_impl": "0x2486e3ff5502bac48D2D86457e7c24B2bB0dDDb5",
        "rpc": "https://bsc-testnet-dataseed.bnbchain.org",
        "chain_id": 97,
        "explorer": "https://testnet.bscscan.com",
    },
}

# DISTRICT9 website
D9_BASE_URL = "https://www.district9.club"

# Flap IPFS upload endpoint
FLAP_UPLOAD_API = "https://funcs.flap.sh/api/upload"

# Vanity suffix for tax tokens
TAX_TOKEN_SUFFIX = "7777"

# ─────────────────────────────────────────────
# District9 Portal (Mode B) — 0x9999 suffix
# ─────────────────────────────────────────────
D9_PORTAL_CONTRACTS = {
    "bnb": {
        "d9_portal": "0x65f1DC16D3821cD78E9517372b469a544b58DC76",
        "tax_token_v1_impl": "0x29e6383F0ce68507b5A72a53c2B118a118332aA8",
        "rpc": "https://bsc-dataseed.binance.org/",
        "chain_id": 56,
        "explorer": "https://bscscan.com",
    },
}
D9_TOKEN_SUFFIX = "9999"
