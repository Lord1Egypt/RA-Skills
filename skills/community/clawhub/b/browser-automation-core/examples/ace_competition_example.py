#!/usr/bin/env python3
"""
Example: Ace Competition Automation using Browser Core
Demonstrates how Ace would use the core library for competition entry.
"""

import sys
from pathlib import Path

# Add core library to path
core_dir = Path(__file__).parent.parent.parent / "browser-automation-core" / "lib"
sys.path.append(str(core_dir))

from browser_core import BrowserAutomation
import time

class AceCompetitionAutomation:
    """Ace-specific competition automation using core browser library."""
    
    def __init__(self, config=None):
        """Initialize with Ace-specific configuration."""
        self.config = config or {}
        self.browser = BrowserAutomation(self.config)
        
    def connect(self):
        """Connect to browser."""
        return self.browser.connect()
    
    def navigate_to_competition(self, url):
        """Navigate to competition page."""
        print(f"Ace: Navigating to competition: {url}")
        return self.browser.navigate(url)
    
    def take_competition_screenshot(self, step_name):
        """Take screenshot of competition entry progress."""
        filename = f"ace_competition_{step_name}_{int(time.time())}.png"
        return self.browser.take_screenshot(filename)
    
    def simulate_form_filling(self, form_data):
        """Simulate filling a competition entry form."""
        print("Ace: Filling competition entry form...")
        
        # In real implementation, would interact with form elements
        # For now, just demonstrate the pattern
        
        for field, value in form_data.items():
            print(f"  • Filling {field}: {value}")
            time.sleep(0.5)
        
        print("  • Form filled successfully")
        return True
    
    def simulate_submission(self):
        """Simulate submitting the competition entry."""
        print("Ace: Submitting competition entry...")
        time.sleep(1)
        print("  • Entry submitted successfully")
        return True
    
    def run_competition_entry(self, competition_url, entry_data):
        """Run a complete competition entry process."""
        print("=" * 60)
        print("ACE COMPETITION ENTRY PROCESS")
        print("=" * 60)
        
        if not self.connect():
            print("❌ Failed to connect to browser")
            return False
        
        print("✅ Connected to browser")
        
        # Navigate to competition
        if not self.navigate_to_competition(competition_url):
            print("❌ Failed to navigate to competition")
            return False
        
        print(f"✅ Navigated to competition: {competition_url}")
        
        # Take initial screenshot
        initial_screenshot = self.take_competition_screenshot("initial")
        if initial_screenshot:
            print(f"✅ Initial screenshot: {initial_screenshot}")
        
        # Fill entry form
        print("\nFilling entry form...")
        self.simulate_form_filling(entry_data)
        
        # Take form screenshot
        form_screenshot = self.take_competition_screenshot("form_filled")
        if form_screenshot:
            print(f"✅ Form screenshot: {form_screenshot}")
        
        # Submit entry
        print("\nSubmitting entry...")
        self.simulate_submission()
        
        # Take submission proof screenshot
        submission_screenshot = self.take_competition_screenshot("submitted")
        if submission_screenshot:
            print(f"✅ Submission proof: {submission_screenshot}")
        
        print("\n" + "=" * 60)
        print("COMPETITION ENTRY COMPLETE")
        print("=" * 60)
        
        self.browser.close()
        return True

def main():
    """Main example execution."""
    
    # Example competition entry data for Ace
    competition_url = "https://example-competition.com/enter"
    entry_data = {
        "full_name": "Stef Ferreira",
        "email": "ace@supplystoreafrica.com",
        "phone": "+27726386189",
        "address": "123 Street, Johannesburg, South Africa",
        "answer": "The best product because...",
        "terms_accepted": True
    }
    
    # Configuration for Ace
    config = {
        "cdp_http_url": "http://localhost:18800/json",
        "timeout": 30,
        "screenshot_dir": "/root/.openclaw/workspace/agents/ace/screenshots",
        "headless": True
    }
    
    # Create Ace automation instance
    ace = AceCompetitionAutomation(config)
    
    # Run competition entry
    success = ace.run_competition_entry(competition_url, entry_data)
    
    if success:
        print("\n✅ Example completed successfully")
        print("\nThis demonstrates how Ace will use the core browser library for:")
        print("1. Browser connection management")
        print("2. Competition site navigation")
        print("3. Form filling automation")
        print("4. Entry submission")
        print("5. Proof screenshot capture")
    else:
        print("\n❌ Example failed")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
