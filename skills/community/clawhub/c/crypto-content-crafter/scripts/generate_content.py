#!/usr/bin/env python3
"""
Crypto Content Crafter - NFT Collection Content Generator

Generate complete NFT collection launch content from a collection name.
Usage:
    uv run python generate_content.py --name "CyberPunk Zebras" --tagline "Neon meets nature" --supply 5555 --price 0.05 --date "2026-06-01" --theme "cyberpunk zebra"
    uv run python generate_content.py --interactive
"""

import argparse
import sys


def generate_collection_description(name: str, tagline: str, supply: int, price: float, theme: str) -> str:
    """Generate the main collection description."""
    return f"""{name} — {tagline}

Step into the {theme} universe, where generative art meets on-chain utility. {name} is a collection of {supply:,} uniquely crafted digital assets, each procedurally generated with hundreds of possible attributes — ensuring no two are exactly alike.

This is not just a JPEG. Each {name} grants you:
- Governance rights in our {name} DAO
- Early access to all future mints
- Exclusive holder-only events and Discord channels
- Physical merchandise redemption for select traits

Our team has been building in crypto since 2021. We've seen the bear seasons and the bull runs. This collection is our contribution to the next chapter.

Mint Date: TBA | Price: {price} ETH | Supply: {supply:,}

Join the Discord. Secure your spot. The future of {theme} starts here."""


def generate_short_description(name: str, tagline: str, supply: int) -> str:
    """Generate a short 1-2 sentence pitch."""
    return f"""{supply:,} unique {name} NFTs. Each one is a key — to our DAO, to exclusive events, and to a community building the {tagline}."""


def generate_twitter_thread(name: str, tagline: str, supply: int, price: float, theme: str, twitter_handle: str = "yourhandle") -> str:
    """Generate a 7-tweet launch thread."""
    return f"""THREAD: How we built {name}

1/ Imagine owning a piece of {theme} history.

{name} is coming.

2/ {supply:,} unique {theme} NFTs.
Each one's story is written on-chain.
No JPEG dumps. A real ecosystem.

3/ Our artists spent 6 months crafting the {theme} universe.
Hundreds of layers. Thousands of attribute combinations.
Each piece is a 1/1 in the truest sense.

4/ {name} holders get:
- Governance in our DAO
- Early access to future mints
- Exclusive holder events
- Physical merch redemptions

This is what separates us from the shelf.

5/ We've been in crypto since 2021.
We've survived 3 bear markets.
We've learned what lasts: community + utility.

6/ Mint Date: TBA
Price: {price} ETH
Supply: {supply:,}

Join the Discord for whitelist access:
discord.gg/yourserver

Drop "READY" below if you're building with us.

7/ {name} is for the collectors who see beyond the flip.

Not just holders. Partners.

Follow @{twitter_handle} for updates."""


def generate_discord_welcome(name: str, theme: str) -> str:
    """Generate the Discord welcome message."""
    return f"""Welcome to **{name}**, Traveler!

You're early. That's smart.

READ THE #rules BEFORE POSTING.

Quick Links:
#announcements — official news ONLY
#mint-info — everything about the drop  
#general — community hangout
#showcase — show off your {name}
#trading — secondary market talk

New to NFTs? Ask in #new-holders. We've all been there.

REMEMBER: Not financial advice. Always do your own research.

Welcome to the {theme} family."""


def generate_roadmap(name: str) -> str:
    """Generate a 4-phase roadmap."""
    return f"""{name} Roadmap

PHASE 1 — THE LAUNCH
- {name} mint goes live
- Discord community opens fully
- Initial liquidity secured for secondary marketplace

PHASE 2 — THE BUILD (30 Days Post-Mint)
- {name} DAO goes live — holders vote on treasury use
- First exclusive holder event announced
- Community art contest — winning design added to future mint

PHASE 3 — THE EXPANSION (60-90 Days)
- Staking protocol launch
- Partnership announcements (TBA)
- Secondary marketplace listing push
- Merch store opens for trait-based redemption

PHASE 4 — THE FUTURE (180 Days)
- {name} sequel collection announced
- Physical art exhibition featuring holder pieces
- Major platform integration reveal
- Your voice shapes everything. This is DAO governance in action.

The roadmap is a living document. Holders vote on priorities."""


def generate_mint_announcement(name: str, supply: int, price: float, theme: str) -> str:
    """Generate a mint day announcement."""
    return f"""MINT IS LIVE

{name}
{price} ETH | {supply:,} Supply | Ethereum

Why {name}?
- {theme} aesthetic, real utility
- DAO governance for all holders
- Staking + yield coming post-mint

SPREAD THE WORD.
RT this tweet.
Drop "MINTED" below.

Contract: [ADD AFTER LAUNCH]
Discord: discord.gg/yourserver
OpenSea: [ADD AFTER LAUNCH]"""


def interactive_mode():
    """Prompt user for all collection details."""
    print("=== Crypto Content Crafter - Interactive Mode ===\n")
    
    name = input("Collection Name: ").strip()
    tagline = input("Tagline: ").strip()
    theme = input("Theme/Vibe: ").strip()
    
    try:
        supply = int(input("Total Supply (e.g. 5555): ").strip())
        price = float(input("Mint Price in ETH (e.g. 0.05): ").strip())
    except ValueError:
        print("Invalid number. Using defaults.")
        supply = 5555
        price = 0.05
    
    date = input("Mint Date (or 'TBA'): ").strip() or "TBA"
    twitter = input("Twitter Handle (without @): ").strip() or "yourhandle"
    
    return name, tagline, theme, supply, price, date, twitter


def main():
    parser = argparse.ArgumentParser(description="Crypto Content Crafter - NFT Collection Generator")
    parser.add_argument("--name", type=str, help="Collection name")
    parser.add_argument("--tagline", type=str, help="Collection tagline")
    parser.add_argument("--theme", type=str, help="Collection theme/vibe")
    parser.add_argument("--supply", type=int, default=5555, help="Total supply")
    parser.add_argument("--price", type=float, default=0.05, help="Mint price in ETH")
    parser.add_argument("--date", type=str, default="TBA", help="Mint date")
    parser.add_argument("--twitter", type=str, default="yourhandle", help="Twitter handle")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        name, tagline, theme, supply, price, date, twitter = interactive_mode()
    elif not args.name:
        print("Error: --name required or use --interactive")
        print(__doc__)
        sys.exit(1)
    else:
        name = args.name
        tagline = args.tagline or "the future of digital ownership"
        theme = args.theme or "generative art"
        supply = args.supply
        price = args.price
        date = args.date
        twitter = args.twitter
    
    print("\n" + "="*60)
    print(f"CONTENT GENERATED FOR: {name}")
    print("="*60)
    
    print("\n>>> SHORT DESCRIPTION <<<\n")
    print(generate_short_description(name, tagline, supply))
    
    print("\n>>> COLLECTION DESCRIPTION <<<\n")
    print(generate_collection_description(name, tagline, supply, price, theme))
    
    print("\n>>> TWITTER THREAD <<<\n")
    print(generate_twitter_thread(name, tagline, supply, price, theme, twitter))
    
    print("\n>>> DISCORD WELCOME MESSAGE <<<\n")
    print(generate_discord_welcome(name, theme))
    
    print("\n>>> ROADMAP <<<\n")
    print(generate_roadmap(name))
    
    print("\n>>> MINT ANNOUNCEMENT <<<\n")
    print(generate_mint_announcement(name, supply, price, theme))
    
    print("\n" + "="*60)
    print("Content generation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
