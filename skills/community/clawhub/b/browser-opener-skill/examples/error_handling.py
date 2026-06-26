#!/usr/bin/env python3
"""
Error handling examples for the browser opener skill.
"""

from scripts.open_browser import BrowserOpener

def demonstrate_error_handling():
    """Demonstrate various error handling scenarios."""
    opener = BrowserOpener()
    
    # Example 1: Empty URL
    print("=== Testing Empty URL ===")
    try:
        opener.open_url("")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 2: Invalid URL format
    print("\n=== Testing Invalid URL Format ===")
    try:
        opener.open_url("not-a-url")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 3: Non-existent browser
    print("\n=== Testing Non-existent Browser ===")
    try:
        opener.open_url("https://www.google.com", browser_name="nonexistent-browser")
    except (ValueError, FileNotFoundError) as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 4: Browser not available on current platform
    print("\n=== Testing Platform-specific Browser ===")
    try:
        opener.open_url("https://www.google.com", browser_name="safari")
    except (ValueError, FileNotFoundError) as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 5: Successful opening with error handling
    print("\n=== Testing Successful Opening ===")
    try:
        success = opener.open_url("https://www.google.com", browser_name="chrome")
        if success:
            print("✓ Successfully opened URL")
        else:
            print("✗ Failed to open URL")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def safe_browser_opening(url, browser_name="default", **kwargs):
    """Safely open a browser with comprehensive error handling."""
    opener = BrowserOpener()
    
    try:
        # Validate URL
        if not url:
            raise ValueError("URL is required")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Try to open the browser
        success = opener.open_url(url, browser_name=browser_name, **kwargs)
        
        if success:
            print(f"✓ Successfully opened {url} in {browser_name}")
            return True
        else:
            print(f"✗ Failed to open {url} in {browser_name}")
            return False
            
    except ValueError as e:
        print(f"✗ Invalid URL or browser name: {e}")
        return False
    except FileNotFoundError as e:
        print(f"✗ Browser not found: {e}")
        return False
    except PermissionError as e:
        print(f"✗ Permission denied: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Demonstrate error handling and safe browser opening."""
    print("=== Browser Opener Error Handling Examples ===\n")
    
    # Demonstrate various error scenarios
    demonstrate_error_handling()
    
    print("\n=== Safe Browser Opening Example ===")
    # Use the safe wrapper function
    safe_browser_opening("https://www.google.com", browser_name="chrome")
    safe_browser_opening("https://www.bing.com", browser_name="firefox")
    safe_browser_opening("", browser_name="chrome")  # This will fail gracefully
    safe_browser_opening("invalid-url", browser_name="chrome")  # This will fail gracefully

if __name__ == "__main__":
    main()