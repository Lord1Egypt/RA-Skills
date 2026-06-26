#!/usr/bin/env python3
"""Save a username -> Steam64 ID mapping."""
import argparse
from leetify_common import save_steam_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map username to Steam64 ID")
    parser.add_argument("username", help="Telegram/chat username")
    parser.add_argument("steam_id", help="Steam64 ID")
    args = parser.parse_args()
    save_steam_id(args.username, args.steam_id)
