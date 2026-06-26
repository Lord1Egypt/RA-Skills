# Mobile App Pipeline

Use this when the user wants a mobile app, app MVP, mobile-first product flow, or native-style interface for iOS, Android, or cross-platform delivery.

## Recommended strategy
- Default to **mobile-first**
- Add **task-efficiency-first** for utility or productivity apps
- Add **clarity-first** for onboarding, transactional, or form-heavy apps
- Add **accessibility-first** when the app is broad-consumer or high-frequency-use

## Step 1. Clarify essentials
- Who is the primary user?
- What is the main recurring task in the app?
- What should users be able to do within the first 30-60 seconds?
- Is this consumer, creator, team, or internal tooling?
- Is the target closer to iOS, Android, or shared cross-platform behavior?

## Step 2. Define design direction
- Common style choices: minimal / platform-adaptive / dark mode / soft modern / data-light
- Typical navigation: bottom nav / tab bar / stacked flow / adaptive tabs + detail
- Typical surfaces: cards, lists, sheets, full-screen flows, modals
- Key interaction goal: simple one-hand-friendly flows with clear feedback

## Step 3. Build screen plan
Typical screens:
1. Onboarding or entry screen
2. Home / overview screen
3. Primary task flow screen
4. Detail screen
5. Search / filter / list screen if needed
6. Profile / settings screen
7. Empty / loading / error / success states

## Step 4. Build plan requirements
- Clear primary action per screen
- Touch-safe spacing and controls
- Strong hierarchy for thumb-friendly scanning
- Platform-aware components and motion
- Sheet/modal behavior that feels predictable
- Reduced friction in forms and repeated actions

## Step 5. Review priorities
Focus review on:
- touch target size and spacing
- bottom navigation or tab clarity
- onboarding friction
- form usability on small screens
- gesture safety and clear alternatives
- empty/loading/error feedback
- readability in bright/dark contexts
- accessibility for motion, contrast, labels, and screen readers

## Common risks
- Too much desktop thinking copied into mobile
- Crowded screens with weak hierarchy
- Hidden actions behind unclear gestures
- Tiny tap targets or cramped spacing
- Overuse of modals and nested flows
- No clear first-time-user path

## Next prompt shape
"Design a mobile app for [user type] focused on [primary task], with a [style] direction, [iOS/Android/adaptive] interaction patterns, and a simple flow across [key screens]."
