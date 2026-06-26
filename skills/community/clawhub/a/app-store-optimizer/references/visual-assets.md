# Visual Assets Optimization Guide

## Why Visuals Matter More Than You Think

On iOS, 60-70% of users decide to download based on screenshots alone — before reading a word of the description. Your icon and first two screenshots carry disproportionate weight. Optimize these first; everything else is secondary.

## App Icon

### Design Principles
- Must be instantly readable at 29x29px (notification) through 1024x1024px (App Store)
- Single focal element — don't try to convey multiple ideas
- Category context matters: finance apps trend dark/minimal, health apps trend bright/friendly, productivity apps trend clean/geometric
- Avoid: text (rarely readable at small sizes), screenshots of the app, faces that look generic

### Competitive Differentiation Test
Search your category and screenshot the top 20 icons. Lay them out in a grid. Your icon should be:
- Immediately identifiable as different
- Not a clone of the market leader (confuses users, loses legal)
- Consistent with your positioning (premium vs. accessible)

### A/B Testing Variables (in priority order)
1. Background color (biggest impact)
2. Primary symbol/shape
3. Complexity level (minimal vs. detailed)
4. Text inclusion vs. symbol only

### Technical Specs
- iOS: 1024x1024px PNG, no alpha channel, no rounded corners (Apple applies mask)
- Android: 512x512px PNG, can have alpha, adaptive icon required (108x108dp with safe zone)

---

## Screenshots

### The Core Principle: Story Over Feature List

Screenshots should tell a story in sequence, not showcase a list of features. A user scrolling through should feel a narrative pull — "oh, it does that AND that? I need this."

### Screenshot Sequence Framework

**Screenshot 1 — The Hook (most important)**
- Must work standalone — most users see only this one before deciding
- Show the single most compelling moment in the app
- Overlay text: Bold benefit statement, not feature name
- Bad: "Task Management" | Good: "Done in half the time"
- The image should be the best-looking, most polished screen in your app

**Screenshots 2-3 — Core Value**
- Each addresses a different user concern or desire
- Think "what would make someone who's on the fence download this?"
- Use captions that escalate the value: bigger claim, more specific benefit

**Screenshots 4-5 — Depth & Trust**
- Show breadth of features for users who need convincing
- Social proof if available (user count, star rating visual)
- Edge-case features that differentiate from competitors

**Screenshot 6+ — Nice to Have**
- Localization-specific content
- Platform-specific features
- Awards, press, community

### Caption Copy Formula
Structure: `[What it does] + [What that means for you]`
- "Sync across all devices — pick up exactly where you left off"
- "AI suggests your next task — focus on work, not planning"

### Device Frame Choice
- Frameless (pure UI) converts better in most categories — nothing distracts from the app
- Framed devices work better for: lifestyle apps, social apps, apps where context matters
- Test both; don't assume

### Localization of Screenshots
Different markets need adapted screenshots, not just translated text:
- US/UK: outcome-focused copy ("Get fit in 30 days")
- Japan: feature-focused, more detail, clean aesthetic
- Germany: specification-focused, trust signals
- China: social proof prominent, community features forward

### Technical Specs

| Platform | Portrait | Landscape |
|----------|---------|-----------|
| iPhone 15 Pro Max | 1290x2796px | 2796x1290px |
| iPhone 8/SE | 1242x2208px | 2208x1242px |
| iPad Pro 12.9" | 2048x2732px | 2732x2048px |
| Android phone | 1080x1920px | 1920x1080px |

Upload the largest size — stores scale down. Don't upload blurry upscaled versions.

---

## App Preview Videos (iOS) / Promo Videos (Android)

### When Videos Help (and When They Don't)
Videos help most when:
- Core value is hard to convey in a static screenshot (motion, animation, real-time features)
- The app experience is inherently dynamic (games, creative tools, fitness)
- You have strong production quality

Videos hurt when:
- Production quality is low (worse than no video)
- App is simple and screenshots tell the story fine
- Target market tends to have slower connections

### Video Structure (15-30 seconds)

**0-3 sec: Pattern interrupt**
- Don't start with a logo animation — users skip immediately
- Start with the most visually striking moment, or a relatable problem
- First 2 seconds determine if they keep watching

**3-20 sec: Feature showcase**
- Show real UI, real interactions — not just marketing animations
- Each cut should reveal something new and valuable
- No more than 4-5 distinct feature moments in this window
- Transition pacing: 2-3 seconds per feature for complex, 1-2 for simple

**20-30 sec: Value reinforcement**
- End on a satisfying moment (task completed, goal achieved, insight revealed)
- Tagline if it's short and powerful
- App icon + name (helps with brand recall)

### iOS Preview Video Rules (Apple enforces strictly)
- Must use actual app footage — no simulated interactions
- No marketing overlays showing competitor comparisons
- No claims about pricing ("free", "now on sale")
- No hands/people unless they appear in actual app UI
- Duration: 15-30 seconds
- Must be appropriate for all ages (if targeting 4+)

### Sound Design
- 50%+ of users watch without sound — visuals must convey full story silently
- Add captions/text overlays for key moments
- Music should not carry the narrative

---

## Visual A/B Testing Strategy

### iOS: Product Page Optimization (PPO)
- Available to all apps; run in App Store Connect
- Test: up to 3 variants against control
- Minimum sample size: ~1000 impressions per variant for significance
- Test one variable at a time: icon OR screenshots OR video — not all three
- Run for 7-21 days minimum; avoid running during major updates or seasonal events

### Android: Store Listing Experiments
- Similar to PPO; available in Play Console
- Can test: icon, feature graphic, screenshots, short description
- Run for at least 7 days; aim for 95% confidence before declaring winner

### What to Test First (in order of impact)
1. First screenshot (highest leverage, most users see it)
2. App icon (affects click-through from search)
3. Screenshot captions
4. Screenshot order
5. Video vs. no video
