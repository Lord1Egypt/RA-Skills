---
name: game-dev-qa-test
description: >
  QA and testing workflow for game development. Covers test plans, smoke
  tests, regression suites, bug reporting, automated testing, and playtest
  reports. Structured for solo devs and small teams.
triggers:
  - "QA testing"
  - "test my game"
  - "write test plan"
  - "game testing"
  - "bug report"
  - "playtest session"
  - "regression test"
  - "quality assurance"
---

# Game Dev QA — Testing & Quality Assurance

## 🎯 Purpose

Catch bugs before players do. Structured QA workflow for solo developers and
small teams: test plans, smoke tests, regression testing, bug tracking, and
playtest reports. Adapted for game-specific testing challenges (fun,
performance, edge cases that players will find instantly).

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for writing test plans and reports. Can create test suites as files. |
| **Claude Code** | Can write unit tests (GDScript, C# nunit). Can run test commands if CI is set up. |
| **Cursor/Windsurf** | Good for writing and running unit tests alongside code. |
| **GitHub Copilot** | Can generate unit tests from code. Good for test-first workflows. |
| **Generic LLM Chat** | Provide test plan templates and test case examples. User runs them manually. |
| **Any AI** | All can produce test plans, bug report templates, and testing checklists. |

---

## 📂 Document Structure

Create in `game-dev-studio/qa/`:

```
qa/
├── test-plan.md           ← Master test plan
├── smoke-tests.md         ← Quick sanity checks
├── regression-suite.md    ← Full regression test suite
├── bug-report.md          ← Bug report template
├── playtest-report.md     ← Playtest session template
└── automated/             ← (If applicable) CI test scripts
```

---

## 📋 Phase 1: Test Plan

### Step 1.1 — Test Scope

Ask:
> **"What's being tested?"**
>
> ```
> 1) Feature test — specific system/mechanic
> 2) Build test — complete build, all systems
> 3) Regression — everything that was previously working
> 4) Performance — framerate, memory, loading times
> 5) Compatibility — multiple platforms/hardware
> 6) Playtest — fun, pacing, difficulty
> ```

### Step 1.2 — Test Plan Template

```markdown
# Test Plan: [Feature / Build Name]

**Version:** [build version]
**Date:** [YYYY-MM-DD]
**Tester:** [name]

## Scope
[What's being tested]

## Out of Scope
[What's NOT being tested — helps focus]

## Test Environment
- **Platform:** [Windows/Mac/Linux/Web/Mobile]
- **OS Version:** [e.g. Windows 11 23H2]
- **Hardware:** [CPU, GPU, RAM]
- **Engine Version:** [e.g. Godot 4.6]
- **Build ID:** [commit hash or build number]

## Priority Definitions
| Priority | Meaning | Response Time |
|----------|---------|---------------|
| P0 - Critical | Blocks shipping, game crashes | Immediate |
| P1 - High | Major feature broken, no workaround | Same day |
| P2 - Medium | Feature partially broken, workaround exists | This sprint |
| P3 - Low | Cosmetic, minor, nice-to-fix | Backlog |

## Test Cases
[See below for test case format]
```

---

## 🧪 Phase 2: Test Cases

### Step 2.1 — Test Case Format

```markdown
### TC-[number]: [Short description]

**Priority:** [P0/P1/P2/P3]
**Type:** [Functional / Performance / Usability / Regression]
**Preconditions:**
- [State required before starting]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
[What should happen]

**Actual Result:**
[To be filled during testing]

**Status:** [Pass / Fail / Blocked / Not Tested]
```

### Step 2.2 — Game-Specific Test Categories

**Movement Tests:**
```
TC-001: Player can move in all 4/8 directions
TC-002: Movement speed is consistent across terrain types
TC-003: Player cannot move outside level bounds
TC-004: Jump height is consistent
TC-005: Double jump works (if feature exists)
```

**Combat Tests:**
```
TC-010: Basic attack deals correct damage
TC-011: Enemy dies when health reaches 0
TC-012: Enemy respawns correctly (if applicable)
TC-013: Projectile hits register correctly
TC-014: Damage numbers display correctly (if applicable)
```

**UI Tests:**
```
TC-020: Main menu buttons navigate to correct screens
TC-021: Pause menu pauses game
TC-022: Settings save after restart
TC-023: Tooltips work on hover
```

**Save/Load Tests:**
```
TC-030: Game saves correctly
TC-031: Saved game loads correctly
TC-032: Multiple save slots work
TC-033: Corrupted save handled gracefully
```

**Edge Case Tests:**
```
TC-040: Alt+Tab and return works
TC-041: Window resize works
TC-042: Rapid input (mashing buttons)
TC-043: Game starts with no save data
TC-044: Very long play session (memory leak check)
```

---

## 🔥 Phase 3: Smoke Tests

For quick sanity checks before each build. Should take <5 minutes.

```markdown
# Smoke Test Checklist

## Pre-Build
- [ ] Project compiles without errors
- [ ] All scenes load without errors
- [ ] No missing asset errors in console

## Core Loop
- [ ] Player can start a new game
- [ ] Player can complete core loop once
- [ ] Player can die/get game over
- [ ] Player can restart

## UI
- [ ] Main menu → play works
- [ ] Pause menu works (Esc / Start)
- [ ] Settings accessible
- [ ] Quit works

## Input
- [ ] Keyboard input registers
- [ ] Mouse input registers
- [ ] Controller input registers (if applicable)

## Audio
- [ ] Music plays
- [ ] SFX play
- [ ] Volume controls work

## Performance
- [ ] Framerate is stable (no major drops)
- [ ] No visible memory leaks
- [ ] Loading times are acceptable

## Build
- [ ] Build completes
- [ ] Build runs on target platform
- [ ] Build version/correctly labeled
```

---

## 🔁 Phase 4: Regression Testing

### Step 4.1 — When to Run

Run full regression suite:
- Before major release
- After significant engine upgrade
- After refactoring core systems

Run partial regression:
- After each sprint
- After bugfixes to critical system

### Step 4.2 — Regression Template

```markdown
# Regression Suite v[version]

## System: [System Name]
- [ ] TC-001: [description]
- [ ] TC-002: [description]
- [ ] Previously fixed bug #XX: [description]

## System: [System Name]
- [ ] TC-010: [description]
- [ ] TC-011: [description]
- ...

## Known Issues (not retesting)
- Bug #XX — [description] — deferred to v[next]
```

---

## 🐛 Phase 5: Bug Reporting

### Step 5.1 — Bug Report Template

```markdown
# Bug Report

**ID:** BUG-[number]
**Date:** [YYYY-MM-DD]
**Reporter:** [name]

## Summary
[One-line description]

## Severity
[P0 / P1 / P2 / P3]

## Environment
- **Platform:** [Windows/Mac/Linux/Web/Mobile]
- **Build:** [version/commit]
- **OS:** [version]
- **Hardware:** [if relevant]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Frequency
[Always / Often / Sometimes / Rarely / Once]

## Workaround
[If any]

## Attachments
- [ ] Screenshot/video
- [ ] Log file
- [ ] Save file

## Status
[New / Triaged / In Progress / Fixed / Verified / Won't Fix / Duplicate]
```

---

## 🎮 Phase 6: Playtest Reports

### Step 6.1 — Playtest Session

```markdown
# Playtest Report

**Build:** [version]
**Date:** [YYYY-MM-DD]
**Tester(s):** [names]
**Session length:** [time]

## Test Focus
[What we wanted to learn]

## Observations
### What worked
- [ ]
- [ ]

### What confused players
- [ ]
- [ ]

### Where they got stuck
- [ ]
- [ ]

### What they loved
- [ ]
- [ ]

### What they complained about
- [ ]
- [ ]

## Metrics (if captured)
- Completion rate: [X%]
- Average play time: [X minutes]
- Deaths: [count]
- Softlocks: [count]

## Quotes
> "[Memorable player quote]"

## Issues Found
| ID | Severity | Summary |
|----|----------|---------|
| BUG-XX | P1 | [summary] |
| BUG-XX | P2 | [summary] |

## Recommendations
1. [High priority fix]
2. [Design change]
3. [Content addition/cut]

## Next Session
- [ ] Fix P0/P1 bugs
- [ ] Address design feedback
- [ ] Schedule follow-up playtest
```

---

## 🤖 Phase 7: Automated Testing

### Step 7.1 — Engine-Specific Automation

**Godot (GDScript):**
```gdscript
# Use the built-in GUT (Godot Unit Test) framework
# Or GDScript 2.0's built-in unit testing
extends GutTest

func test_player_takes_damage():
    var player = Player.new()
    player.take_damage(10)
    assert_eq(player.health, 90, "Player should lose 10 HP")
```

**Unity (C#):**
```csharp
using NUnit.Framework;

public class PlayerTests
{
    [Test]
    public void PlayerTakesDamage()
    {
        var player = new GameObject().AddComponent<Player>();
        player.TakeDamage(10);
        Assert.AreEqual(90, player.Health);
    }
}
```

**Unreal (C++):**
```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FPlayerDamageTest, "Game.Player.Damage",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FPlayerDamageTest::RunTest(const FString& Parameters)
{
    // Test implementation
    return true;
}
```

### Step 7.2 — CI Integration

```yaml
# .github/workflows/test.yml
name: Game Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run unit tests
        run: godot --headless --test
```

---

## ✅ Final QA Sign-Off

```markdown
# QA Sign-Off: [Build Version]

**Date:** [YYYY-MM-DD]
**QA Lead:** [name]

## Summary
- **Tests run:** [count]
- **Passed:** [count]
- **Failed:** [count]
- **Blocked:** [count]

## P0/P1 Issues
| ID | Summary | Status |
|----|---------|--------|
| BUG-XX | [summary] | Fixed/Verified |

## Verdict
- [ ] **Pass** — All P0/P1 fixed and verified
- [ ] **Conditional Pass** — Known P1 with workaround, P0 all fixed
- [ ] **Fail** — Unresolved P0/P1 blocking release
```
