#!/usr/bin/env python3
"""
Browser Automation Core Library - Fixed version with CORS handling
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import websocket
import threading
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserAutomation:
    """Core browser automation class using CDP via WebSocket."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize browser automation."""
        self.config = config or {}
        self.cdp_http_url = self.config.get("cdp_http_url", "http://localhost:18800/json")
        self.timeout = self.config.get("timeout", 30)
        self.screenshot_dir = Path(self.config.get("screenshot_dir", "/tmp/browser_screenshots"))
        self.screenshot_dir.mkdir(exist_ok=True)
        
        self.ws = None
        self.message_id = 1
        self.responses = {}
        self.connected = False
        
        logger.info(f"BrowserAutomation initialized with config: {self.config}")
    
    def _get_websocket_url(self) -> Optional[str]:
        """Get WebSocket URL from CDP HTTP endpoint."""
        try:
            response = requests.get(self.cdp_http_url, timeout=5)
            targets = response.json()
            for target in targets:
                if target.get("type") == "page":
                    return target["webSocketDebuggerUrl"]
            return None
        except Exception as e:
            logger.error(f"Failed to get WebSocket URL: {e}")
            return None
    
    def connect(self) -> bool:
        """Connect to browser via WebSocket with proper headers."""
        ws_url = self._get_websocket_url()
        if not ws_url:
            logger.error("No WebSocket URL available")
            return False
        
        try:
            # Create WebSocket connection with custom headers to handle CORS
            self.ws = websocket.create_connection(
                ws_url, 
                timeout=self.timeout,
                # Add origin header to match what browser expects
                header={"Origin": "http://localhost:18800"}
            )
            self.connected = True
            
            # Start message handler thread
            self.handler_thread = threading.Thread(target=self._message_handler, daemon=True)
            self.handler_thread.start()
            
            logger.info(f"Connected to browser via WebSocket: {ws_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            return False
    
    def _message_handler(self):
        """Handle incoming WebSocket messages."""
        while self.connected and self.ws:
            try:
                message = self.ws.recv()
                data = json.loads(message)
                
                # Store response by ID
                if "id" in data:
                    self.responses[data["id"]] = data
                # Handle events (no ID)
                elif "method" in data:
                    self._handle_event(data)
                    
            except websocket.WebSocketConnectionClosedException:
                logger.info("WebSocket connection closed")
                break
            except Exception as e:
                logger.error(f"Error in message handler: {e}")
    
    def _handle_event(self, event: Dict):
        """Handle CDP events."""
        method = event.get("method", "")
        params = event.get("params", {})
        
        # Log important events
        if method in ["Page.loadEventFired", "Network.responseReceived"]:
            logger.debug(f"Event: {method}")
    
    def _send_command(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Send CDP command and wait for response."""
        if not self.connected or not self.ws:
            raise ConnectionError("Not connected to browser")
        
        command_id = self.message_id
        self.message_id += 1
        
        command = {
            "id": command_id,
            "method": method,
            "params": params or {}
        }
        
        self.ws.send(json.dumps(command))
        logger.debug(f"Sent command {command_id}: {method}")
        
        # Wait for response
        start_time = time.time()
        while command_id not in self.responses:
            if time.time() - start_time > self.timeout:
                raise TimeoutError(f"Timeout waiting for response to {method}")
            time.sleep(0.1)
        
        response = self.responses.pop(command_id)
        if "error" in response:
            error_msg = response["error"].get("message", "Unknown error")
            raise RuntimeError(f"CDP error in {method}: {error_msg}")
        
        return response.get("result", {})
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        try:
            # Enable Page domain
            self._send_command("Page.enable")
            
            # Navigate
            result = self._send_command("Page.navigate", {"url": url})
            
            logger.info(f"Navigated to {url}, navigationId: {result.get('navigationId')}")
            
            # Wait a bit for page to load
            time.sleep(2)
            
            logger.info(f"Navigation to {url} complete")
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False
    
    def take_screenshot(self, filename: str, full_page: bool = False) -> Optional[str]:
        """Take screenshot of current page."""
        try:
            # Enable Page domain if not already
            self._send_command("Page.enable")
            
            params = {"format": "png"}
            if full_page:
                # Get page dimensions
                metrics = self._send_command("Page.getLayoutMetrics")
                content_size = metrics.get("contentSize", {})
                params["clip"] = {
                    "x": 0,
                    "y": 0,
                    "width": content_size.get("width", 1280),
                    "height": content_size.get("height", 720),
                    "scale": 1
                }
            
            result = self._send_command("Page.captureScreenshot", params)
            screenshot_data = result.get("data", "")
            
            if not screenshot_data:
                logger.error("No screenshot data received")
                return None
            
            # Save screenshot
            screenshot_path = self.screenshot_dir / filename
            import base64
            with open(screenshot_path, "wb") as f:
                f.write(base64.b64decode(screenshot_data))
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None
    
    def execute_script(self, script: str) -> Any:
        """Execute JavaScript in browser context."""
        try:
            result = self._send_command("Runtime.evaluate", {
                "expression": script,
                "returnByValue": True
            })
            return result.get("result", {}).get("value")
        except Exception as e:
            logger.error(f"Script execution failed: {e}")
            return None
    
    def get_page_title(self) -> Optional[str]:
        """Get current page title."""
        try:
            result = self._send_command("Runtime.evaluate", {
                "expression": "document.title",
                "returnByValue": True
            })
            return result.get("result", {}).get("value")
        except Exception as e:
            logger.error(f"Failed to get page title: {e}")
            return None
    
    def close(self):
        """Close browser connection."""
        if self.ws:
            self.ws.close()
            self.connected = False
            logger.info("Browser connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

# Simple test function
def test_browser_connection():
    """Test if browser connection works."""
    print("Testing browser connection...")
    
    # First check if browser is accessible via HTTP
    try:
        response = requests.get("http://localhost:18800/json", timeout=5)
        targets = response.json()
        print(f"✅ Browser HTTP endpoint accessible. Found {len(targets)} targets.")
        
        # Try to connect via WebSocket
        browser = BrowserAutomation()
        if browser.connect():
            print("✅ WebSocket connection successful")
            
            # Try to get page title
            title = browser.get_page_title()
            print(f"✅ Page title: {title}")
            
            browser.close()
            return True
        else:
            print("❌ WebSocket connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False

if __name__ == "__main__":
    print("Browser Automation Core - Fixed Version Test")
    print("=" * 50)
    
    if test_browser_connection():
        print("\n✅ Browser automation core is working!")
        print("\nReady for:")
        print("1. Facet - Onshape learning automation")
        print("2. Ace - Competition entry automation")
    else:
        print("\n❌ Browser test failed")
        print("\nTroubleshooting:")
        print("1. Check browser is running: openclaw browser status")
        print("2. Check port 18800: curl http://localhost:18800/json")
        print("3. Check WebSocket URL in browser output")
