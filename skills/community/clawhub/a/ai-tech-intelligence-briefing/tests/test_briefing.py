#!/usr/bin/env python3
"""Test suite for Daily Intelligence Briefing."""

import sys
from pathlib import Path

# Get absolute paths
scripts_path = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_path.absolute()))

import briefing


def test_generate():
    """Test briefing generation."""
    print("🧪 Testing: Generate briefing...")
    
    briefing_obj = briefing.DailyBriefing()
    result = briefing_obj.generate(save=True, verbose=False)
    
    assert "DAILY INTELLIGENCE BRIEFING" in result
    assert len(result) > 100
    assert "TOP STORIES" in result
    
    print("✅ Generate test passed!")
    return True


def test_fetch_save():
    """Test save and fetch cycle."""
    print("🧪 Testing: Save/Fetch cycle...")
    
    briefing_obj = briefing.DailyBriefing()
    date = "2026-03-11"
    
    content = "## Test Briefing\nTest content here."
    path = briefing_obj.save(content, date)
    
    assert Path(path).exists()
    print(f"   Saved to: {path}")
    
    fetched = briefing_obj.fetch(date)
    assert fetched == content
    
    print("✅ Save/Fetch test passed!")
    return True


def test_list_available():
    """Test listing available briefings."""
    print("🧪 Testing: List available briefings...")
    
    briefing_obj = briefing.DailyBriefing()
    files = briefing_obj.list_available()
    
    assert isinstance(files, list)
    assert len(files) >= 1
    
    print(f"   Found {len(files)} briefing(s)")
    print("✅ List test passed!")
    return True


def test_demo_content():
    """Test demo content fallback."""
    print("🧪 Testing: Demo content generation...")
    
    briefing_obj = briefing.DailyBriefing()
    stories = briefing_obj.get_demo_content()
    
    assert len(stories) >= 5
    for story in stories:
        assert 'title' in story
        assert 'url' in story
        assert 'source' in story
        assert 'summary' in story
    
    print("✅ Demo content test passed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("🧪 Running Daily Intelligence Briefing Tests")
    print("="*50 + "\n")
    
    tests = [test_generate, test_fetch_save, test_list_available, test_demo_content]
    passed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
        
        print()
    
    print("="*50)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    print("="*50 + "\n")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
