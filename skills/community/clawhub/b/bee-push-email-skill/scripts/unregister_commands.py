#!/usr/bin/env python3
"""Unregister beemail bot commands from Telegram.

Standalone script called by uninstall.sh to cleanly remove
/beemail* commands from the Telegram bot menu.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from telegram_commands import unregister_bee_commands

if __name__ == '__main__':
    unregister_bee_commands()
