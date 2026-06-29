---
name: game-dev-release
description: >
  Release management for game development. Covers release checklists, patch
  notes, hotfix process, day-1 patch strategy, launch checklist, platform
  store submission, and post-launch support workflow.
triggers:
  - "prepare for release"
  - "release checklist"
  - "ship my game"
  - "patch notes"
  - "hotfix"
  - "launch preparation"
  - "day 1 patch"
  - "game launch"
  - "deploy game"
---

# Game Dev Release — Release Management

## 🎯 Purpose

Ship a game build to players with confidence. Covers full release lifecycle:
pre-launch checklist, build pipeline, store submission, patch notes, hotfix
process, and post-launch support.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for maintaining release checklists, patch notes, and documentation. |
| **Claude Code** | Can build export scripts, run release builds, and create store metadata files. |
| **Cursor/Windsurf** | Can help with release configuration and store-specific files. |
| **GitHub Copilot** | Chat can help write store descriptions and patch notes. |
| **Generic LLM Chat** | Provide checklist guidance and template content. User executes manually. |
| **Any AI** | All can produce checklists and templates. Build-capable AIs can automate parts of the pipeline. |

**Warning:** Store submission (Steam, Epic, App Store, etc.) requires manual
steps that cannot be fully automated. The AI can prepare files and metadata
but cannot submit to store portals.

---

## 📂 Document Structure

Create in `game-dev-studio/release/`:

```
release/
├── release-plan.md       ← Master release plan
├── launch-checklist.md   ← Final launch checklist
├── patch-notes.md        ← Patch notes history
├── hotfix-process.md     ← Emergency fix workflow
└── store/               ← Store-specific materials
    ├── steam/           ← Steam store assets
    ├── itch/            ← itch.io assets
    └── epic/            ← Epic Games Store assets
```

---

## 📋 Phase 1: Release Planning

### Step 1.1 — Define Release

Ask:
> **"What kind of release is this?"**
>
> ```
> 1) Alpha — internal/pre-alpha, close team only
> 2) Beta — external testers, may be public
> 3) Early Access — paid access during development
> 4) Full Launch — 1.0 public release
> 5) Patch / Update — post-launch content or fix release
> 6) Game Jam — 48-72 hour compressed release
> ```

### Step 1.2 — Release Schedule

Ask:
> **"Target release date?"** (be realistic)

Then work backward:

```
T-8 weeks:  Feature freeze
T-6 weeks:  Beta build to testers
T-4 weeks:  Content complete
T-2 weeks:  Localization + store assets
T-1 week:   Final QA pass
T-0:        Gold master build
T+0:        Launch
T+1 day:    Day-1 patch (if needed)
T+1 week:   Post-launch assessment
```

### Step 1.3 — Version Numbering

Use [Semantic Versioning](https://semver.org/) for games:

```
MAJOR.MINOR.PATCH

v1.0.0  — First release
v1.1.0  — Feature update
v1.1.1  — Bugfix patch
v2.0.0  — Major update (breaking changes)
```

Game jam / iterative builds can use date-based:

```
v2024.06.24 — Build from June 24, 2024
v1.0.0-beta.1 — Beta version
```

---

## ✅ Phase 2: Pre-Launch Checklist

### Step 2.1 — Final QA

```markdown
# Pre-Launch QA Checklist

- [ ] **Full regression suite passed** (see `qa-test`)
- [ ] **All P0/P1 bugs fixed** or documented as known issues
- [ ] **Performance targets met** on minimum spec hardware
- [ ] **Load testing** (concurrent users if multiplayer)
- [ ] **Memory leak check** (30+ minute session)
- [ ] **Save/load tested** across multiple sessions
- [ ] **Achievements/leaderboards verified** (if applicable)
- [ ] **All languages/locales display correctly**
- [ ] **Accessibility features verified**
```

### Step 2.2 — Build Pipeline

```markdown
# Build Pipeline Checklist

- [ ] **Build script verified** — one-command build
- [ ] **All platforms build successfully:**
  - [ ] Windows
  - [ ] Mac
  - [ ] Linux
  - [ ] Web (HTML5)
  - [ ] Mobile (Android/iOS)
  - [ ] Console (if applicable)
- [ ] **Build versioning correct** — version number in build
- [ ] **Build reproducible** — same commit = same build
- [ ] **Build size optimized** — no unnecessary assets
- [ ] **Build compression tested** — load times acceptable
- [ ] **Gold master build created** and archived
```

### Step 2.3 — Store + Distribution

**Steam:**
```markdown
# Steam Store Checklist

- [ ] Steamworks SDK integrated
- [ ] Steam DRM tested (if using)
- [ ] Steam achievements set up
- [ ] Steam leaderboards set up
- [ ] Cloud saves working
- [ ] Store page submitted and approved
- [ ] Trailer / screenshots uploaded
- [ ] Description and tags finalized
- [ ] Pricing set
- [ ] Release date set in Steam backend
- [ ] Build depot uploaded and set as default
- [ ] Launch discount configured (if any)
- [ ] Community hub / forums set up
```

**itch.io:**
```markdown
# itch.io Checklist

- [ ] Game page created
- [ ] Upload build(s) (Windows, Mac, Linux)
- [ ] Web build hosted on itch (if HTML5)
- [ ] Screenshots and trailer
- [ ] Description and tags
- [ ] Pricing set (free or paid)
- [ ] Embedded analytics set up
- [ ] Community features enabled
```

---

## 📝 Phase 3: Patch Notes

### Step 3.1 — Writing Patch Notes

Template:

```markdown
# Patch Notes — v[version]

**Build:** [build number]
**Release Date:** [YYYY-MM-DD]

---

## 🆕 New Features
- [Feature 1]
- [Feature 2]

## 🔧 Improvements
- [Improvement 1]
- [Improvement 2]

## 🐛 Bug Fixes
- Fixed [issue]
- Fixed [issue]

## ⚖️ Balance Changes
- [Balance change 1]
- [Balance change 2]

## 🎨 Art / Audio
- [Art/audio change]

## 🗺️ Levels
- [Level change]

## Known Issues
- [Issue 1] — ETA: [date/version]
- [Issue 2] — ETA: [date/version]

---

**Download:** [link]
```

### Step 3.2 — Patch Notes Guidelines

- **Tone:** Professional but warm. Match your game's tone.
- **Length:** Long enough to be informative, short enough to scan.
- **Format:** Bullet points. Group by category.
- **Sections:** Features first, then fixes. Never lead with bugs.
- **Credit:** Thank testers, contributors, community.
- **Known issues:** Honest about what's not fixed yet.

---

## 🔥 Phase 4: Hotfix Process

### Step 4.1 — When to Hotfix

**HOTFIX TRIGGER:** Critical bug that blocks play. Examples:
- Crash on startup
- Corrupted save files
- Game-breaking progression blocker
- Security vulnerability

**DO NOT HOTFIX for:**
- Minor visual bugs
- Balance issues
- Feature requests
- Performance improvements

### Step 4.2 — Hotfix Workflow

```
1. BUG REPORTED (P0)
2. TRIAGE [15 min]
   - Is it actually P0? 
   - Can we reproduce?
   - Root cause known?
3. FIX [as fast as possible]
   - Create branch: hotfix/[description]
   - Fix the bug
   - Test the fix
   - Fix only the bug — no scope creep
4. BUILD [automated]
   - Increment PATCH version: v1.0.0 → v1.0.1
5. REVIEW [30 min]
   - Code review (if team)
   - QA verify fix
   - QA smoke test build
6. RELEASE
   - Push build to stores
   - Update all platforms
7. ANNOUNCE
   - Post patch notes
   - Communicate to players
```

### Step 4.3 — Hotfix Branching

```
main ──── v1.0.0 ──── v1.0.1 (hotfix) ──── merge back
              \
hotfix/ ────── crash-on-startup
```

Always merge hotfix branch back into main/dev branches.

### Step 4.4 — Hotfix Checklist

```markdown
# Hotfix: [BUG-ID]

**Bug:** [summary]
**Severity:** P0
**Found in:** v[version]

## Process
- [ ] Bug confirmed and reproduced
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Fix tested (fixes the bug)
- [ ] Smoke test (no regressions)
- [ ] Build created: v[version+patch]
- [ ] Build uploaded to stores
- [ ] Patch notes written and posted
- [ ] Community notified

## Post-Hotfix
- [ ] Hotfix merged to dev branch
- [ ] Automated test added (if possible)
- [ ] Post-mortem written (if warranted)
```

---

## 🚀 Phase 5: Launch Day

### Step 5.1 — Final Pre-Launch

```markdown
# Launch Day Checklist

## T-24 Hours
- [ ] Gold master build verified
- [ ] Store pages finalized and reviewed
- [ ] Release date/time confirmed
- [ ] Social media posts scheduled
- [ ] Press build sent to media (if applicable)
- [ ] Backup builds stored (offline + cloud)
- [ ] Discord/community channels ready
- [ ] Support email/contact set up

## T-2 Hours
- [ ] Final smoke test of live build
- [ ] Server monitoring set up (if multiplayer)
- [ ] Analytics/dashboard verified
- [ ] Team communication channels open
- [ ] Emergency rollback plan ready

## T-0: Launch
- [ ] Push build live on stores
- [ ] Flip "release" switch in store backend
- [ ] Post launch announcement
- [ ] Monitor social media channels
- [ ] Monitor crash reporting
- [ ] Monitor server load (if applicable)
- [ ] Have a snack. You earned it. 🎉

## T+1 Hour
- [ ] Check for critical bug reports
- [ ] Check store reviews/ratings
- [ ] Respond to initial player feedback
- [ ] Send thank-you to testers/backers
```

### Step 5.2 — Day-1 Patch

Prepare before launch:

> **"Should we prepare a day-1 patch?"**

Plan:
- Fix minor bugs found during certification/review
- Do NOT add new features
- Submit for certification alongside launch build
- Release day-1 patch when approved (usually 1-3 days after launch)

Day-1 patch strategy:
```
Launch build: v1.0.0  — what goes to reviewers, press, streamers
Day-1 patch:  v1.0.1  — what players get on day 1 (if approved in time)
```

### Step 5.3 — Launch Communication

```markdown
# Launch Announcement Template

> 🎮 **[Game Title]** is OUT NOW on [Platforms]!
>
> [One-sentence hook]
>
> [Link to store page]
>
> Thank you to everyone who supported us during development!
>
> #gamedev #indiegame [Genre] [Platform]
```

Post to:
- Steam News
- Twitter / X
- Discord
- Reddit (relevant subreddits)
- itch.io community
- Personal blog / website

---

## 📊 Phase 6: Post-Launch

### Step 6.1 — First Week Monitoring

```markdown
# Post-Launch Monitoring (Week 1)

| Metric | Target | Current | Notes |
|--------|--------|---------|-------|
| Crash rate | < 1% | [X%] | |
| Avg playtime | [target] | [X min] | |
| Completion rate | [target] | [X%] | |
| Store rating | 4+ | [X.X] | |
| Reviews | [target] | [count] | |
| Support tickets | [target] | [count] | |
```

### Step 6.2 — Post-Launch Roadmap

Ask after launch:
> **"What's next?"**
>
> ```
> 1) Content update(s) — new levels, characters, items
> 2) Quality-of-life update — address feedback
> 3) Porting — new platform release
> 4) DLC — paid expansion
> 5) New project — move on
> 6) Maintenance mode — critical fixes only
> ```

### Step 6.3 — Patch Cycle

```
Week 1:   Critical hotfixes only
Week 2-3: QoL patch addressing top player feedback
Month 1:  First content update
Month 2+: Regular content updates or move to maintenance
```

---

## 📄 Final Output

```markdown
# [Game Title] — Release Plan v1.0

**Launch Date:** [YYYY-MM-DD]
**Version:** v1.0.0

## Release Type
[Alpha / Beta / Early Access / Full Launch / Patch]

## Platforms
- [ ] Steam
- [ ] itch.io
- [ ] Epic Games Store
- [ ] GOG
- [ ] Game Pass
- [ ] Nintendo Switch
- [ ] PlayStation 5
- [ ] Xbox Series X|S
- [ ] Mobile (iOS/Android)
- [ ] Web (HTML5)
- [ ] Other: [specify]

## Schedule
| Milestone | Date | Status |
|-----------|------|--------|
| Feature freeze | [date] | [pending/done] |
| Beta build | [date] | [pending/done] |
| Content complete | [date] | [pending/done] |
| Gold master | [date] | [pending/done] |
| Launch | [date] | [pending/done] |
| Day-1 patch | [date] | [planned] |

## Budget
- **Release build size:** [X MB / GB]
- **Certification costs:** [amount] (if console)
- **Build pipeline:** [auto/manual]

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Crash on launch | Low | Critical | Load testing, crash reporting |
| Store page rejected | Medium | High | Submit early for review |
| Server overload | Low | Medium | Auto-scaling (if multiplayer) |
| Bad reviews on launch | Medium | Medium | Day-1 patch ready |

## Contingency
- **Crash on startup:** Roll back to previous build. Investigate, hotfix.
- **Store rejection:** Fix issues, resubmit. Delay launch if needed.
- **Server issues:** Vertical scaling, communicate with players.
- **Negative reception:** Day-1 patch, community engagement, QoL update planned.
```
