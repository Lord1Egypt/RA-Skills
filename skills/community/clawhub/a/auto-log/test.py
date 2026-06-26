"""
Auto Log Skill — test script
Run: python3 test.py
"""

from auto_log_skill import AutoLogSkill

def test_create_log():
    skill = AutoLogSkill()
    path = skill.create_daily_log("test-agent")
    assert path.exists(), "Log file should be created"
    print(f"✅ Test 1 passed — log created: {path}")

def test_append_event():
    skill = AutoLogSkill()
    result = skill.append_event("Integration test started", section="Events")
    assert result, "append_event should return True"
    print("✅ Test 2 passed — event appended")

def test_append_task():
    skill = AutoLogSkill()
    result = skill.append_task("Unit tests", "✅", "All passed")
    assert result, "append_task should return True"
    print("✅ Test 3 passed — task appended")

def test_add_todo():
    skill = AutoLogSkill()
    result = skill.add_todo("Review PR before 5 PM")
    assert result, "add_todo should return True"
    print("✅ Test 4 passed — todo added")

def test_get_summary():
    skill = AutoLogSkill()
    summary = skill.get_summary()
    assert isinstance(summary, str) and len(summary) > 0, "Summary should be a non-empty string"
    print("✅ Test 5 passed — summary retrieved")
    print(f"\n--- Summary preview ---\n{summary[:300]}\n---")

if __name__ == "__main__":
    print("🧪 Auto Log Skill — Test Suite\n")
    test_create_log()
    test_append_event()
    test_append_task()
    test_add_todo()
    test_get_summary()
    print("\n✅ All tests passed")
