"""
Browser Agent - Main browser automation class
"""

from playwright.sync_api import sync_playwright, Page, Browser
from typing import Optional, Dict, Any, List
import time


class BrowserAgent:
    """Browser automation agent using Playwright"""
    
    def __init__(self, headless: bool = True, viewport: str = "1280x720"):
        """
        Initialize browser agent
        
        Args:
            headless: Run browser in headless mode
            viewport: Viewport size (e.g., "1920x1080")
        """
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.headless = headless
        
        # Parse viewport
        try:
            width, height = map(int, viewport.split('x'))
            self.viewport = {"width": width, "height": height}
        except:
            self.viewport = {"width": 1280, "height": 720}
    
    def _ensure_browser(self):
        """Ensure browser is running"""
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        
        if self.browser is None:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        
        if self.page is None:
            self.page = self.browser.new_page(viewport=self.viewport)
    
    def open(self, url: str):
        """
        Navigate to URL
        
        Args:
            url: URL to open
        """
        self._ensure_browser()
        self.page.goto(url, wait_until='networkidle')
    
    def snapshot(self, interactive: bool = False, compact: bool = False, depth: Optional[int] = None) -> str:
        """
        Get accessibility tree snapshot
        
        Args:
            interactive: Only interactive elements
            compact: Compact output
            depth: Limit tree depth
            
        Returns:
            Accessibility tree as string
        """
        self._ensure_browser()
        
        # Get accessibility snapshot
        tree = self.page.accessibility.snapshot()
        
        if tree:
            return self._format_tree(tree, interactive, compact, depth, 0)
        else:
            return "No accessibility tree available"
    
    def _format_tree(self, node: Dict, interactive: bool, compact: bool, depth: Optional[int], level: int) -> str:
        """Format accessibility tree node"""
        if depth is not None and level > depth:
            return ""
        
        # Filter interactive elements if requested
        if interactive:
            role = node.get('role', '')
            if role not in ['button', 'link', 'textbox', 'checkbox', 'combobox', 'menuitem']:
                return ""
        
        # Build node string
        indent = "  " * level
        role = node.get('role', 'unknown')
        name = node.get('name', '')
        
        if compact and not name:
            return ""
        
        result = f"{indent}- {role}"
        if name:
            result += f" \"{name}\""
        
        result += "\n"
        
        # Process children
        children = node.get('children', [])
        for child in children:
            result += self._format_tree(child, interactive, compact, depth, level + 1)
        
        return result
    
    def click(self, selector: str):
        """
        Click an element
        
        Args:
            selector: CSS selector or ref
        """
        self._ensure_browser()
        
        # Handle ref-style selectors (@e1, @e2, etc.)
        if selector.startswith('@'):
            # Convert ref to actual selector
            # This would need implementation based on snapshot refs
            raise NotImplementedError("Ref selectors not yet implemented")
        
        self.page.click(selector)
    
    def fill(self, selector: str, text: str):
        """
        Fill an input field
        
        Args:
            selector: CSS selector
            text: Text to fill
        """
        self._ensure_browser()
        self.page.fill(selector, text)
    
    def screenshot(self, path: str, full_page: bool = False):
        """
        Take a screenshot
        
        Args:
            path: Output path
            full_page: Full page screenshot
        """
        self._ensure_browser()
        self.page.screenshot(path=path, full_page=full_page)
    
    def get_text(self, selector: str) -> str:
        """
        Get text content of an element
        
        Args:
            selector: CSS selector
            
        Returns:
            Text content
        """
        self._ensure_browser()
        return self.page.text_content(selector)
    
    def get_html(self, selector: str) -> str:
        """
        Get innerHTML of an element
        
        Args:
            selector: CSS selector
            
        Returns:
            InnerHTML
        """
        self._ensure_browser()
        return self.page.inner_html(selector)
    
    def is_visible(self, selector: str) -> bool:
        """
        Check if element is visible
        
        Args:
            selector: CSS selector
            
        Returns:
            True if visible
        """
        self._ensure_browser()
        return self.page.is_visible(selector)
    
    def wait(self, selector: str = None, timeout: int = 30000, state: str = "visible",
             text: str = None, url: str = None, load: str = None):
        """
        Wait for element, text, URL, or load state
        
        Args:
            selector: CSS selector to wait for
            timeout: Timeout in milliseconds
            state: Wait state (visible, hidden, attached, detached)
            text: Wait for text to appear
            url: Wait for URL pattern
            load: Wait for load state (load, domcontentloaded, networkidle)
        """
        self._ensure_browser()
        
        if load:
            self.page.wait_for_load_state(load, timeout=timeout)
        elif text:
            self.page.wait_for_function(f"document.body.innerText.includes('{text}')", timeout=timeout)
        elif url:
            self.page.wait_for_url(url, timeout=timeout)
        elif selector:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    def find(self, role: str = None, text: str = None, label: str = None,
             placeholder: str = None, testid: str = None, action: str = None,
             name: str = None, exact: bool = False):
        """
        Find elements using semantic locators
        
        Args:
            role: ARIA role
            text: Text content
            label: Label text
            placeholder: Placeholder text
            testid: data-testid value
            action: Action to perform (click, fill, etc.)
            name: Accessible name
            exact: Exact match
        """
        self._ensure_browser()
        
        # Build locator
        if role:
            if name:
                locator = self.page.get_by_role(role, name=name, exact=exact)
            else:
                locator = self.page.get_by_role(role, exact=exact)
        elif text:
            locator = self.page.get_by_text(text, exact=exact)
        elif label:
            locator = self.page.get_by_label(label, exact=exact)
        elif placeholder:
            locator = self.page.get_by_placeholder(placeholder, exact=exact)
        elif testid:
            locator = self.page.get_by_test_id(testid)
        else:
            raise ValueError("Must specify one of: role, text, label, placeholder, testid")
        
        # Perform action if specified
        if action:
            if action == "click":
                locator.click()
            elif action == "fill":
                # Would need text parameter
                pass
            elif action == "text":
                return locator.text_content()
        
        return locator
    
    def press(self, selector: str, key: str):
        """
        Press a key on an element
        
        Args:
            selector: CSS selector
            key: Key to press (Enter, Tab, etc.)
        """
        self._ensure_browser()
        self.page.press(selector, key)
    
    def hover(self, selector: str):
        """
        Hover over an element
        
        Args:
            selector: CSS selector
        """
        self._ensure_browser()
        self.page.hover(selector)
    
    def check(self, selector: str):
        """
        Check a checkbox
        
        Args:
            selector: CSS selector
        """
        self._ensure_browser()
        self.page.check(selector)
    
    def uncheck(self, selector: str):
        """
        Uncheck a checkbox
        
        Args:
            selector: CSS selector
        """
        self._ensure_browser()
        self.page.uncheck(selector)
    
    def select(self, selector: str, value: str):
        """
        Select dropdown option
        
        Args:
            selector: CSS selector
            value: Option value
        """
        self._ensure_browser()
        self.page.select_option(selector, value)
    
    def scroll(self, selector: str = None, direction: str = "down", pixels: int = 100):
        """
        Scroll page or element
        
        Args:
            selector: CSS selector (None for page)
            direction: Scroll direction (up, down, left, right)
            pixels: Pixels to scroll
        """
        self._ensure_browser()
        
        if selector:
            # Scroll element
            if direction == "down":
                self.page.evaluate(f"document.querySelector('{selector}').scrollBy(0, {pixels})")
            elif direction == "up":
                self.page.evaluate(f"document.querySelector('{selector}').scrollBy(0, -{pixels})")
        else:
            # Scroll page
            if direction == "down":
                self.page.mouse.wheel(0, pixels)
            elif direction == "up":
                self.page.mouse.wheel(0, -pixels)
    
    def upload(self, selector: str, files: List[str]):
        """
        Upload files
        
        Args:
            selector: CSS selector for file input
            files: List of file paths
        """
        self._ensure_browser()
        self.page.set_input_files(selector, files)
    
    def get_value(self, selector: str) -> str:
        """
        Get input value
        
        Args:
            selector: CSS selector
            
        Returns:
            Input value
        """
        self._ensure_browser()
        return self.page.input_value(selector)
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Get element attribute
        
        Args:
            selector: CSS selector
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        self._ensure_browser()
        return self.page.get_attribute(selector, attribute)
    
    def get_box(self, selector: str) -> Dict:
        """
        Get element bounding box
        
        Args:
            selector: CSS selector
            
        Returns:
            Bounding box dict
        """
        self._ensure_browser()
        box = self.page.bounding_box(selector)
        return box if box else {}
    
    def count(self, selector: str) -> int:
        """
        Count matching elements
        
        Args:
            selector: CSS selector
            
        Returns:
            Element count
        """
        self._ensure_browser()
        return self.page.locator(selector).count()
    
    def eval(self, javascript: str) -> Any:
        """
        Execute JavaScript
        
        Args:
            javascript: JavaScript code
            
        Returns:
            Evaluation result
        """
        self._ensure_browser()
        return self.page.evaluate(javascript)
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
            self.browser = None
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
        
        self.page = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
