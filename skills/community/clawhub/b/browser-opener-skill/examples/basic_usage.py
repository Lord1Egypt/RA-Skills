#!/usr/bin/env python3
"""
Basic usage examples for the browser opener skill.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.open_browser import BrowserOpener

def main():
    opener = BrowserOpener()
    
    # Example 1: Open URL with default browser
    print("Opening Google with default browser...")
    opener.open_url("https://www.google.com")
    
    # Example 2: Open URL with Chrome
    print("Opening Google with Chrome...")
    opener.open_url("https://www.google.com", browser_name="chrome")
    
    # Example 3: Open URL with Firefox in private mode
    print("Opening Google with Firefox in private mode...")
    opener.open_url("https://www.google.com", browser_name="firefox", incognito=True)
    
    # Example 4: Open URL with Edge in new window
    print("Opening Google with Edge in new window...")
    opener.open_url("https://www.google.com", browser_name="edge", new_window=True)

if __name__ == "__main__":
    main()