#!/usr/bin/env python3
"""
Earnings Monitor - Daily Earnings Reports
"""

# === CONFIGURATION ===

# Path to Obsidian vault on your Mac (accessed via Scout)
OBSIDIAN_VAULT_PATH = "/Users/wangshangxin/Library/Mobile Documents/iCloud~md~obsidian/Documents/Stock Archive"

# Notion API
NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "2dcdaf9e7441808487d8fce68cceacfc"

# Google Gemini API Key for generating reports
GEMINI_API_KEY = "AIzaSyDSx6s009BFHmERqKLM0NX1-0B620L-JX8"  # Get from https://aistudio.google.com/app/apikey

# Stocks to monitor (your full watch list)
STOCKS = [
    "SMR",    # NuScale Power
    "NBIS",   # Nebius Group
    "PLAB",   # Photronics
    "INOD",   # Innodata
    "RDW",    # Redwire
    "GLW",    # Corning
    "NVDA",   # NVIDIA
    "GOOG",   # Alphabet
    "LI",     # Li Auto
    "AVGO",   # Broadcom
    "MU",     # Micron
    "RMBS",   # Rambus
    "HROW",   # Harrow Health
    "AEP",    # American Electric Power
    "ONDS",   # Ondas Holdings
    "QQQM",   # Invesco NASDAQ 100 ETF
    "SPY",    # S&P 500 ETF
    "TSLA",   # Tesla
    "SANM",   # Sanmina
    "AMD",    # AMD
]
