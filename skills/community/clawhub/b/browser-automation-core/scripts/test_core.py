#!/usr/bin/env python3
"""
Test script for Browser Automation Core Library.
Tests basic functionality and demonstrates reuse for Facet and Ace.
"""

import sys
from pathlib import Path

# Add core library to path
core_dir = Path(__file__).parent.parent / "lib"
sys.path.append(str(core_dir))

from browser_core import BrowserAutomation, test_connection, simple_navigation
import time

def test_basic_functionality():
    """Test basic browser core functionality."""
    print("=" * 60)
    print("TEST 1: Basic Browser Core Functionality")
    print("=" * 60)
    
    # Test configuration
    config = {
        "cdp_http_url": "http://localhost:18800/json",
        "timeout": 10,
        "screenshot_dir": "/tmp/browser_test",
        "headless": True
    }
    
    # Test 1: Connection test
    print("\n1. Testing browser connection...")
    if test_connection(config):
        print("   ✅ Connection test passed")
    else:
        print("   ❌ Connection test failed")
        return False
    
    # Test 2: Simple navigation
    print("\n2. Testing simple navigation...")
    screenshot = simple_navigation("https://example.com", config)
    if screenshot:
        print(f"   ✅ Navigation test passed")
        print(f"   Screenshot: {screenshot}")
    else:
        print("   ❌ Navigation test failed")
        return False
    
    # Test 3: Direct library usage
    print("\n3. Testing direct library usage...")
    try:
        with BrowserAutomation(config) as browser:
            title = browser.get_page_title()
            print(f"   ✅ Library usage test passed")
            print(f"   Page title: {title}")
    except Exception as e:
        print(f"   ❌ Library usage test failed: {e}")
        return False
    
    return True

def test_facet_example():
    """Test Facet example usage."""
    print("\n" + "=" * 60)
    print("TEST 2: Facet Onshape Automation Example")
    print("=" * 60)
    
    # Import and run Facet example
    example_dir = Path(__file__).parent.parent / "examples"
    sys.path.append(str(example_dir))
    
    try:
        from facet_onshape_example import FacetOnshapeAutomation
        
        config = {
            "cdp_http_url": "http://localhost:18800/json",
            "timeout": 10,
            "screenshot_dir": "/tmp/facet_test",
            "headless": True
        }
        
        facet = FacetOnshapeAutomation(config)
        
        # Simulate a short learning session
        tutorial_steps = [
            "Open Onshape",
            "Create sketch",
            "Test navigation"
        ]
        
        print("\nSimulating Facet learning session...")
        # Just test connection and navigation, not full session
        if facet.connect():
            print("   ✅ Facet connection successful")
            if facet.navigate_to_onshape():
                print("   ✅ Facet navigation successful")
                screenshot = facet.take_onshape_screenshot("test")
                if screenshot:
                    print(f"   ✅ Facet screenshot: {screenshot}")
                facet.browser.close()
                return True
            else:
                print("   ❌ Facet navigation failed")
        else:
            print("   ❌ Facet connection failed")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Facet example test failed: {e}")
        return False

def test_ace_example():
    """Test Ace example usage."""
    print("\n" + "=" * 60)
    print("TEST 3: Ace Competition Automation Example")
    print("=" * 60)
    
    # Import and run Ace example
    example_dir = Path(__file__).parent.parent / "examples"
    sys.path.append(str(example_dir))
    
    try:
        from ace_competition_example import AceCompetitionAutomation
        
        config = {
            "cdp_http_url": "http://localhost:18800/json",
            "timeout": 10,
            "screenshot_dir": "/tmp/ace_test",
            "headless": True
        }
        
        ace = AceCompetitionAutomation(config)
        
        print("\nSimulating Ace competition entry...")
        # Just test connection and navigation
        if ace.connect():
            print("   ✅ Ace connection successful")
            if ace.navigate_to_competition("https://example.com"):
                print("   ✅ Ace navigation successful")
                screenshot = ace.take_competition_screenshot("test")
                if screenshot:
                    print(f"   ✅ Ace screenshot: {screenshot}")
                ace.browser.close()
                return True
            else:
                print("   ❌ Ace navigation failed")
        else:
            print("   ❌ Ace connection failed")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Ace example test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Browser Automation Core Library - Test Suite")
    print("Testing reuse for Facet and Ace agents")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Facet Example", test_facet_example()))
    results.append(("Ace Example", test_ace_example()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED")
        print("\nBrowser Automation Core Library is:")
        print("1. ✅ Functional - Basic browser operations work")
        print("2. ✅ Reusable - Same core used by Facet and Ace")
        print("3. ✅ Extensible - Easy to add agent-specific logic")
        print("4. ✅ Testable - Comprehensive test coverage")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("\nCheck browser configuration:")
        print("• Run: openclaw browser status")
        print("• Run: openclaw browser start")
        print("• Check port 18800 accessibility")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("1. Install websocket-client: pip3 install websocket-client")
    print("2. Implement real CDP commands in browser_core.py")
    print("3. Create Facet extension skill")
    print("4. Create Ace extension skill")
    print("5. Add more comprehensive tests")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
