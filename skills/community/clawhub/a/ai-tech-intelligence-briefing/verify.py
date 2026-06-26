#!/usr/bin/env python3
"""Quick verification script."""

import sys
from pathlib import Path

sys.path.insert(0, str((Path(__file__).parent / 'scripts').absolute()))

def verify():
    """Verify the skill works correctly."""
    print("🔍 Verifying Daily Intelligence Briefing v1.0...\n")
    
    try:
        import briefing
        
        # Test 1: Generate
        obj = briefing.DailyBriefing()
        result = obj.generate(save=True)
        
        assert "DAILY INTELLIGENCE BRIEFING" in result
        assert "TOP STORIES" in result
        print("✅ Generation test passed")
        
        # Test 2: Save/Fetch
        date = "2026-03-11"
        saved_path = obj.save(result, date)
        fetched = obj.fetch(date)
        assert fetched == result
        print("✅ Save/Fetch test passed")
        
        # Test 3: List
        files = obj.list_available()
        assert isinstance(files, list)
        assert len(files) >= 1
        print(f"✅ List test passed ({len(files)} briefing(s))")
        
        # Test 4: Demo content
        stories = obj.get_demo_content()
        assert len(stories) >= 5
        print(f"✅ Demo content test passed ({len(stories)} demo stories)")
        
        print("\n" + "="*50)
        print("🎉 All tests passed! Ready for publishing!")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
