#!/usr/bin/env python3
"""
Browser Automation using OpenClaw CLI commands.
Simpler approach that uses the existing OpenClaw browser CLI.
"""

import subprocess
import json
import time
import logging
from pathlib import Path
from typing import Dict, Optional, List
import tempfile
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserCLIAutomation:
    """Browser automation using OpenClaw CLI commands."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize browser automation."""
        self.config = config or {}
        self.profile = self.config.get("profile", "openclaw")
        self.timeout = self.config.get("timeout", 30)
        self.screenshot_dir = Path(self.config.get("screenshot_dir", "/tmp/browser_screenshots"))
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Check if browser is running
        self._check_browser_status()
        
        logger.info(f"BrowserCLIAutomation initialized with profile: {self.profile}")
    
    def _check_browser_status(self) -> bool:
        """Check if browser is running."""
        try:
            result = subprocess.run(
                ["openclaw", "browser", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if "running: true" in result.stdout:
                logger.info("Browser is running")
                return True
            else:
                logger.warning("Browser is not running")
                return False
                
        except Exception as e:
            logger.error(f"Failed to check browser status: {e}")
            return False
    
    def _run_browser_command(self, command: List[str], timeout: Optional[int] = None) -> Dict:
        """Run OpenClaw browser command and return result."""
        try:
            full_command = ["openclaw", "browser"] + command
            logger.debug(f"Running command: {' '.join(full_command)}")
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout or self.timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                return {"success": False, "error": result.stderr}
            
            # Try to parse JSON output
            try:
                output = json.loads(result.stdout)
                output["success"] = True
                return output
            except json.JSONDecodeError:
                # Not JSON, return as text
                return {"success": True, "output": result.stdout}
                
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(command)}")
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return {"success": False, "error": str(e)}
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL using OpenClaw browser CLI."""
        logger.info(f"Navigating to: {url}")
        
        result = self._run_browser_command(["navigate", url])
        
        if result.get("success"):
            logger.info(f"Navigation to {url} successful")
            return True
        else:
            logger.error(f"Navigation failed: {result.get('error')}")
            return False
    
    def take_screenshot(self, filename: str) -> Optional[str]:
        """Take screenshot using OpenClaw browser CLI."""
        screenshot_path = self.screenshot_dir / filename
        
        logger.info(f"Taking screenshot: {screenshot_path}")
        
        # Use OpenClaw's screenshot command
        result = self._run_browser_command(["screenshot", f"MEDIA:{screenshot_path}"])
        
        if result.get("success"):
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        else:
            logger.error(f"Screenshot failed: {result.get('error')}")
            return None
    
    def execute_script(self, script: str) -> Optional[str]:
        """Execute JavaScript using OpenClaw browser CLI."""
        logger.info(f"Executing script: {script[:50]}...")
        
        # Create temporary file with script
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(script)
            temp_file = f.name
        
        try:
            result = self._run_browser_command(["evaluate", f"file://{temp_file}"])
            
            if result.get("success"):
                output = result.get("output", "No output")
                logger.info(f"Script executed successfully")
                return output
            else:
                logger.error(f"Script execution failed: {result.get('error')}")
                return None
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def get_page_info(self) -> Optional[Dict]:
        """Get current page information."""
        logger.info("Getting page information")
        
        # Use evaluate to get page title and URL
        script = """
        (function() {
            return {
                title: document.title,
                url: window.location.href,
                readyState: document.readyState
            };
        })();
        """
        
        result = self.execute_script(script)
        if result:
            try:
                return json.loads(result)
            except:
                return {"output": result}
        return None
    
    def fill_form(self, form_data: Dict) -> bool:
        """Fill form using OpenClaw browser CLI."""
        logger.info(f"Filling form with {len(form_data)} fields")
        
        # Create temporary file with form data
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(form_data, f)
            temp_file = f.name
        
        try:
            result = self._run_browser_command(["fill", f"file://{temp_file}"])
            
            if result.get("success"):
                logger.info("Form filled successfully")
                return True
            else:
                logger.error(f"Form fill failed: {result.get('error')}")
                return False
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def click_element(self, selector: str) -> bool:
        """Click element using OpenClaw browser CLI."""
        logger.info(f"Clicking element: {selector}")
        
        # First get snapshot to find element
        snapshot_result = self._run_browser_command(["snapshot", "ai"])
        
        if not snapshot_result.get("success"):
            logger.error("Failed to get page snapshot")
            return False
        
        # In a real implementation, we would parse the snapshot and find the element
        # For now, use the click command with selector
        result = self._run_browser_command(["click", selector])
        
        if result.get("success"):
            logger.info(f"Clicked element: {selector}")
            return True
        else:
            logger.error(f"Click failed: {result.get('error')}")
            return False

# Example usage for Facet
class FacetBrowserAutomation(BrowserCLIAutomation):
    """Facet-specific browser automation."""
    
    def navigate_to_onshape(self) -> bool:
        """Navigate to Onshape."""
        return self.navigate("https://cad.onshape.com")
    
    def take_learning_screenshot(self, step_name: str) -> Optional[str]:
        """Take screenshot of learning progress."""
        filename = f"facet_learning_{step_name}_{int(time.time())}.png"
        return self.take_screenshot(filename)

# Example usage for Ace
class AceBrowserAutomation(BrowserCLIAutomation):
    """Ace-specific browser automation."""
    
    def navigate_to_competition(self, url: str) -> bool:
        """Navigate to competition site."""
        return self.navigate(url)
    
    def take_entry_screenshot(self, step_name: str) -> Optional[str]:
        """Take screenshot of competition entry progress."""
        filename = f"ace_competition_{step_name}_{int(time.time())}.png"
        return self.take_screenshot(filename)

def test_cli_automation():
    """Test CLI-based browser automation."""
    print("Testing OpenClaw CLI Browser Automation")
    print("=" * 50)
    
    # Test basic functionality
    browser = BrowserCLIAutomation()
    
    print("1. Testing navigation...")
    if browser.navigate("https://example.com"):
        print("   ✅ Navigation successful")
        
        # Wait for page to load
        time.sleep(2)
        
        print("2. Testing page info...")
        page_info = browser.get_page_info()
        if page_info:
            print(f"   ✅ Page info: {page_info}")
        
        print("3. Testing screenshot...")
        screenshot = browser.take_screenshot("test_example.png")
        if screenshot:
            print(f"   ✅ Screenshot: {screenshot}")
        
        print("4. Testing script execution...")
        script_result = browser.execute_script("document.title")
        if script_result:
            print(f"   ✅ Script result: {script_result}")
        
        print("\n" + "=" * 50)
        print("✅ CLI Browser Automation Test Complete")
        print("\nReady for agent extensions:")
        print("1. FacetBrowserAutomation - Onshape learning")
        print("2. AceBrowserAutomation - Competition entry")
        return True
    else:
        print("   ❌ Navigation failed")
        return False

if __name__ == "__main__":
    print("OpenClaw CLI Browser Automation Library")
    print("Using existing OpenClaw browser commands")
    print("=" * 50)
    
    if test_cli_automation():
        print("\n🎯 Next steps:")
        print("1. Create Facet extension with Onshape-specific methods")
        print("2. Create Ace extension with competition-specific methods")
        print("3. Implement form filling for competition entry")
        print("4. Add progress tracking and reporting")
    else:
        print("\n❌ Test failed")
        print("\nTroubleshooting:")
        print("1. Check browser is running: openclaw browser status")
        print("2. Check OpenClaw installation")
        print("3. Check command permissions")
