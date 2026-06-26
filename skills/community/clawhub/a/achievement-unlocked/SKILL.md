---
name: achievement-unlocked
version: 1.0.0
description: >
  Gaming-style achievement system for real coding work. Tracks milestones,
  unlocks badges, levels up your developer profile, and drops rare
  achievements for legendary feats. Because fixing a production bug at 3am
  deserves more than a Jira ticket closure — it deserves a trophy.
author: J. DeVere Cooley
category: fun-tools
tags:
  - gamification
  - achievements
  - motivation
  - tracking
metadata:
  openclaw:
    emoji: "🏆"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - productivity
---

# Achievement Unlocked

> "Every RPG character starts at Level 1. So did every senior engineer. The difference is, RPG characters get XP notifications."

## What It Does

Real work, real achievements. Every commit, every bug fix, every test written, every refactor completed earns XP and progress toward achievements. Some are common. Some are rare. Some are legendary — and you won't know they exist until you accidentally trigger them at 2am on a Tuesday.

This isn't a toy. It's a **recognition engine** for the invisible work developers do every day that nobody celebrates.

## Achievement Categories

### 🟢 Common Achievements (Easy to earn, everyone gets these)

| Achievement | How to Unlock | XP |
|---|---|---|
| **First Blood** | Make your first commit to the project | 10 |
| **Hello World** | Create your first new file | 10 |
| **Bug Squasher** | Fix your first bug (commit message contains "fix") | 25 |
| **Test Believer** | Write your first test | 25 |
| **Clean Plate** | Commit with zero linter warnings | 15 |
| **Documentation Hero** | Update a README or doc file | 20 |
| **Code Janitor** | Delete more lines than you add in a commit | 20 |
| **Morning Person** | First commit before 7am | 10 |
| **Night Owl** | Commit after midnight | 10 |
| **Weekend Warrior** | Commit on a Saturday or Sunday | 15 |

### 🔵 Uncommon Achievements (Require consistent effort)

| Achievement | How to Unlock | XP |
|---|---|---|
| **Streak!** | Commit every day for 7 consecutive days | 100 |
| **Centurion** | Reach 100 commits on the project | 150 |
| **Test Fanatic** | Achieve 80%+ code coverage | 200 |
| **Polyglot** | Commit code in 3+ different languages | 75 |
| **Architect** | Create 5+ new modules/packages | 100 |
| **Humanitarian** | Fix 10 bugs | 100 |
| **The Deleter** | Remove 1,000+ lines in a single PR | 100 |
| **Zero Warnings** | 5 consecutive commits with zero linter warnings | 75 |
| **Review Machine** | Review (comment on) 10+ PRs | 100 |
| **Multi-Branch** | Work on 3+ branches in a single day | 50 |

### 🟣 Rare Achievements (Impressive milestones)

| Achievement | How to Unlock | XP |
|---|---|---|
| **Marathon** | Commit every day for 30 consecutive days | 500 |
| **Thousand Cuts** | Make 1,000 commits on the project | 750 |
| **Full Coverage** | Achieve 95%+ code coverage | 500 |
| **Dependency Diet** | Remove a dependency (net negative in package.json) | 250 |
| **The Rewriter** | Rewrite a module that's older than 1 year | 300 |
| **Mentor** | Your code gets copied/referenced by 3+ other modules | 250 |
| **The Minimalist** | Ship a feature in under 50 lines | 200 |
| **One-Liner** | Fix a critical bug with a single line change | 300 |
| **Green Machine** | 50 consecutive passing CI builds | 400 |
| **No Rollback** | Deploy 20 times with zero rollbacks | 350 |

### 🟡 Epic Achievements (Legendary feats)

| Achievement | How to Unlock | XP |
|---|---|---|
| **The Phoenix** | Resurrect a failed project to passing CI | 1000 |
| **Immortal Streak** | Commit every day for 100 consecutive days | 2000 |
| **10x Developer** | Remove 10x more lines than you add (lifetime) | 1500 |
| **Zero Bug Sprint** | Complete a full sprint with zero bugs filed | 1000 |
| **The Mass Extinction** | Delete an entire deprecated module (500+ lines) | 750 |
| **Performance Wizard** | Improve a benchmark by 10x+ | 1000 |
| **The Untouchable** | Go 30 days with zero bugs attributed to your code | 1500 |

### 🔴 Secret Achievements (You don't know they exist until you trigger them)

```
These are HIDDEN. You'll only see them when they pop up.
Examples of what might trigger them (but we're not telling you exactly):

  ??? — "Did you just..."
  ??? — "We've all been there"
  ??? — "That's not how you spell 'Wednesday'"
  ??? — "git push --force to main? Bold."
  ??? — "3am on Christmas? Really?"
  ??? — "You fixed it by deleting the entire file"
  ??? — "11 merge conflicts resolved in one commit"
  ??? — "The commit message was longer than the code change"
  ??? — "You wrote more comments than code"
  ??? — "Same bug fixed for the third time"
```

## The Developer Profile

```
╔══════════════════════════════════════════════════════════════╗
║                 🏆 ACHIEVEMENT UNLOCKED 🏆                   ║
║                                                              ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │  🎮 DEVELOPER PROFILE                                │   ║
║  │                                                       │   ║
║  │  Level: 14 — "The Refactorer"                        │   ║
║  │  Total XP: 3,475 / 4,000 (next level)               │   ║
║  │  ████████████████████░░░░░  87%                      │   ║
║  │                                                       │   ║
║  │  Achievements: 27 / 47 unlocked (57%)                │   ║
║  │  🟢 Common:    10/10  (100%)                          │   ║
║  │  🔵 Uncommon:   8/10  (80%)                           │   ║
║  │  🟣 Rare:       5/10  (50%)                           │   ║
║  │  🟡 Epic:       2/7   (29%)                           │   ║
║  │  🔴 Secret:     2/10  (20%)                           │   ║
║  │                                                       │   ║
║  │  Most Recent:                                         │   ║
║  │  🟣 "One-Liner" — Fixed critical auth bypass with     │   ║
║  │     a single character change (= → ===)               │   ║
║  │     Earned: 300 XP — March 3, 2026                    │   ║
║  │                                                       │   ║
║  │  Rarest Achievement:                                  │   ║
║  │  🟡 "The Phoenix" — Resurrected the CI pipeline       │   ║
║  │     after 3 weeks of red. 1000 XP.                    │   ║
║  │                                                       │   ║
║  │  Next Unlock Candidates:                              │   ║
║  │  ├── 🔵 "Streak!" — 5/7 consecutive commit days      │   ║
║  │  ├── 🟣 "Marathon" — 22/30 consecutive commit days    │   ║
║  │  └── 🔵 "Centurion" — 87/100 commits                 │   ║
║  └──────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════╝
```

## Level Titles

| Level | XP Required | Title |
|---|---|---|
| 1 | 0 | "The Intern" |
| 2 | 50 | "Copy-Paster" |
| 3 | 150 | "Stack Overflow Tourist" |
| 4 | 300 | "Bug Generator" |
| 5 | 500 | "It Works On My Machine" |
| 7 | 1,000 | "The Debugger" |
| 10 | 2,000 | "The Builder" |
| 14 | 3,500 | "The Refactorer" |
| 18 | 6,000 | "The Architect" |
| 22 | 10,000 | "The Wizard" |
| 25 | 15,000 | "Mass Deleter of Code" |
| 30 | 25,000 | "Mass Deleter of Bugs" |
| 40 | 50,000 | "Legend" |
| 50 | 100,000 | "Is This Your Full-Time Job?" |

## Achievement Unlock Notification

When you trigger an achievement:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🏆 ACHIEVEMENT UNLOCKED!                               ║
║                                                          ║
║   ┌────────────────────────────────────────────────┐     ║
║   │  🟣 ONE-LINER                                  │     ║
║   │                                                 │     ║
║   │  "Fixed a critical bug with a single line."     │     ║
║   │                                                 │     ║
║   │  The most dangerous code is the code that's     │     ║
║   │  almost right. You found the one character      │     ║
║   │  that made the difference. Surgical.            │     ║
║   │                                                 │     ║
║   │  +300 XP                                        │     ║
║   │  Level 14 → Level 14 (175 XP to next level)    │     ║
║   └────────────────────────────────────────────────┘     ║
║                                                          ║
║   🎯 NEXT: "Centurion" — 13 more commits to unlock      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Team Leaderboard

```
╔══════════════════════════════════════════════════════════════╗
║                  TEAM LEADERBOARD                           ║
║                  March 2026                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  #  Name        Level  XP      Achievements  Rarest         ║
║  ── ────────── ─────  ──────  ────────────  ──────────────  ║
║  1  @jcooley    14    3,475   27/47         The Phoenix     ║
║  2  @sara       12    2,890   24/47         Immortal Streak ║
║  3  @mike       10    2,100   19/47         Performance Wiz ║
║  4  @dev_b       8    1,500   15/47         Green Machine   ║
║  5  @newbie      3      180    6/47         Night Owl       ║
║                                                              ║
║  THIS WEEK'S MVP: @sara — unlocked 3 achievements           ║
║  THIS WEEK'S MOMENT: @mike — "One-Liner" on prod hotfix     ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- Runs automatically in the background — achievements trigger on qualifying events
- Check your profile anytime to see progress
- Check the leaderboard for friendly competition
- After a tough week — see proof that you actually accomplished things

## Why It Matters

Developer work is invisible. You don't get a trophy for fixing a race condition. You don't get applause for deleting 2,000 lines of dead code. You don't get XP for surviving a 3am production incident.

Now you do.

Zero external dependencies. Zero API calls. Pure git-history-powered gamification.
