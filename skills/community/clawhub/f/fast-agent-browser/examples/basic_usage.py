#!/usr/bin/env python3
"""
Example usage of Agent Browser
"""

from src.browser import BrowserAgent


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    with BrowserAgent() as agent:
        # Open a page
        agent.open("https://example.com")
        print(f"✓ Opened: {agent.page.url}")
        
        # Get title
        title = agent.page.title()
        print(f"✓ Title: {title}")
        
        # Get snapshot
        tree = agent.snapshot()
        print(f"✓ Snapshot: {len(tree)} characters")
        
        # Take screenshot
        agent.screenshot("example.png")
        print("✓ Screenshot saved: example.png")


def example_interactive():
    """Interactive elements example"""
    print("\n" + "=" * 60)
    print("Example 2: Interactive Elements")
    print("=" * 60)
    
    with BrowserAgent() as agent:
        agent.open("https://example.com")
        
        # Get interactive elements only
        tree = agent.snapshot(interactive=True)
        print(f"✓ Interactive snapshot: {len(tree)} characters")
        
        # Check if element is visible
        visible = agent.is_visible("h1")
        print(f"✓ H1 visible: {visible}")
        
        # Get text
        text = agent.get_text("h1")
        print(f"✓ H1 text: {text}")


def example_screenshot():
    """Screenshot examples"""
    print("\n" + "=" * 60)
    print("Example 3: Screenshots")
    print("=" * 60)
    
    with BrowserAgent() as agent:
        agent.open("https://example.com")
        
        # Normal screenshot
        agent.screenshot("page_normal.png")
        print("✓ Normal screenshot saved")
        
        # Full page screenshot
        agent.screenshot("page_full.png", full_page=True)
        print("✓ Full page screenshot saved")


def example_context_manager():
    """Context manager example"""
    print("\n" + "=" * 60)
    print("Example 4: Context Manager")
    print("=" * 60)
    
    # Using context manager (auto-closes)
    with BrowserAgent() as agent:
        agent.open("https://example.com")
        print(f"✓ In context: {agent.page.url}")
    
    print("✓ Auto-closed after context")


def example_manual_close():
    """Manual close example"""
    print("\n" + "=" * 60)
    print("Example 5: Manual Close")
    print("=" * 60)
    
    agent = BrowserAgent()
    try:
        agent.open("https://example.com")
        print(f"✓ Opened: {agent.page.url}")
    finally:
        agent.close()
        print("✓ Manually closed")


if __name__ == '__main__':
    print("\n🌐 Agent Browser Examples\n")
    
    example_basic_usage()
    example_interactive()
    example_screenshot()
    example_context_manager()
    example_manual_close()
    
    print("\n" + "=" * 60)
    print("✓ All examples completed!")
    print("=" * 60)
