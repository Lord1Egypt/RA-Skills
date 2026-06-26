#!/usr/bin/env python3
"""
Example: Facet Onshape Automation using Browser Core
Demonstrates how Facet would use the core library for Onshape learning.
"""

import sys
from pathlib import Path

# Add core library to path
core_dir = Path(__file__).parent.parent.parent / "browser-automation-core" / "lib"
sys.path.append(str(core_dir))

from browser_core import BrowserAutomation
import time

class FacetOnshapeAutomation:
    """Facet-specific Onshape automation using core browser library."""
    
    def __init__(self, config=None):
        """Initialize with Facet-specific configuration."""
        self.config = config or {}
        self.browser = BrowserAutomation(self.config)
        self.logged_in = False
        
    def connect(self):
        """Connect to browser."""
        return self.browser.connect()
    
    def navigate_to_onshape(self):
        """Navigate to Onshape homepage."""
        print("Facet: Navigating to Onshape...")
        return self.browser.navigate("https://cad.onshape.com")
    
    def take_onshape_screenshot(self, step_name):
        """Take screenshot of current Onshape state."""
        filename = f"facet_onshape_{step_name}_{int(time.time())}.png"
        return self.browser.take_screenshot(filename)
    
    def simulate_tutorial_step(self, step_number, step_description):
        """Simulate completing a tutorial step."""
        print(f"Facet: Completing tutorial step {step_number}: {step_description}")
        
        # In real implementation, would interact with Onshape UI
        # For now, just demonstrate the pattern
        
        # 1. Navigate to tutorial (simulated)
        print(f"  • Navigating to tutorial step {step_number}")
        time.sleep(1)
        
        # 2. Interact with tutorial (simulated)
        print(f"  • Interacting with tutorial: {step_description}")
        time.sleep(1)
        
        # 3. Take progress screenshot
        screenshot = self.take_onshape_screenshot(f"step_{step_number}")
        if screenshot:
            print(f"  • Progress screenshot: {screenshot}")
        
        # 4. Mark step complete (simulated)
        print(f"  • Step {step_number} complete")
        
        return True
    
    def run_learning_session(self, tutorial_steps):
        """Run a complete learning session."""
        print("=" * 60)
        print("FACET ONSHAPE LEARNING SESSION")
        print("=" * 60)
        
        if not self.connect():
            print("❌ Failed to connect to browser")
            return False
        
        print("✅ Connected to browser")
        
        # Navigate to Onshape
        if not self.navigate_to_onshape():
            print("❌ Failed to navigate to Onshape")
            return False
        
        print("✅ Navigated to Onshape")
        
        # Take initial screenshot
        initial_screenshot = self.take_onshape_screenshot("initial")
        if initial_screenshot:
            print(f"✅ Initial screenshot: {initial_screenshot}")
        
        # Complete tutorial steps
        print(f"\nStarting tutorial with {len(tutorial_steps)} steps...")
        
        for i, step in enumerate(tutorial_steps, 1):
            print(f"\n--- Step {i}/{len(tutorial_steps)} ---")
            self.simulate_tutorial_step(i, step)
        
        # Take final screenshot
        final_screenshot = self.take_onshape_screenshot("completed")
        if final_screenshot:
            print(f"\n✅ Final screenshot: {final_screenshot}")
        
        print("\n" + "=" * 60)
        print("LEARNING SESSION COMPLETE")
        print("=" * 60)
        
        self.browser.close()
        return True

def main():
    """Main example execution."""
    
    # Example tutorial steps for Facet
    tutorial_steps = [
        "Create new document",
        "Add sketch plane",
        "Draw basic shapes",
        "Apply constraints",
        "Extrude to 3D",
        "Save and export"
    ]
    
    # Configuration for Facet
    config = {
        "cdp_http_url": "http://localhost:18800/json",
        "timeout": 30,
        "screenshot_dir": "/root/.openclaw/workspace/agents/facet/screenshots",
        "headless": True
    }
    
    # Create Facet automation instance
    facet = FacetOnshapeAutomation(config)
    
    # Run learning session
    success = facet.run_learning_session(tutorial_steps)
    
    if success:
        print("\n✅ Example completed successfully")
        print("\nThis demonstrates how Facet will use the core browser library for:")
        print("1. Browser connection management")
        print("2. Navigation to Onshape")
        print("3. Tutorial step automation")
        print("4. Progress screenshot capture")
        print("5. Session cleanup")
    else:
        print("\n❌ Example failed")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
