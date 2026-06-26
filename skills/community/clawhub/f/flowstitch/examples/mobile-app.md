# Example: Mobile App Design

This shows FlowStitch §2B in action — generating a native-feeling mobile app screen with proper touch ergonomics, safe areas, and mobile conventions.

---

## Input

**User:** "I need screens for Wandr, a travel planning mobile app. Clean and modern."

---

## Generated DESIGN.md (Mobile App Edition)

```markdown
# Design System: Wandr Mobile App
**Platform:** iOS (iPhone 14/15 target)

## 1. Visual Theme & Atmosphere
Wandr captures the feeling of paging through a beautifully curated travel magazine — but on your phone. The design is **airy and editorial**: generous imagery, warm whites that feel like quality paper, and an accent that evokes Mediterranean blue sky. The UI stays invisible so the destination photography can be the star.

## 2. Color Palette & Roles
- **Warm White** (#FAFAF8) — Primary background (warm, not clinical)
- **Sand** (#F5F0E8) — Card and bottom sheet surfaces
- **Sky Blue** (#0EA5E9) — Primary accent: CTAs, active tabs, interactive elements
- **Charcoal** (#1C1917) — Primary text
- **Warm Gray** (#78716C) — Secondary text, labels, metadata
- **Cloud** (#E7E5E4) — Borders and dividers
- **Success** (#16A34A) — Booked/confirmed states
- **Amber** (#D97706) — Deals, limited availability

## 3. Typography Rules
- **Font:** DM Serif Display (headlines) + Inter (body/labels)
- **Display (destination names):** DM Serif Display, 28–32px, regular weight, charcoal
- **Section Headers:** Inter semibold 600, 16px, charcoal
- **Body:** Inter regular 400, 15px, line-height 1.5
- **Labels/Meta:** Inter regular 400, 12px, warm gray
- **Minimum text size:** 12px (never smaller — prevents iOS accessibility zoom trigger)

## 4. Component Stylings
* **Destination Cards:** 16px corner radius, full-bleed image (16:9), gradient overlay at bottom, title in white over image. Horizontal scrollable row.
* **Bottom Tab Bar:** 49px height, 5 tabs (Explore/Trips/Search/Saved/Profile), icons (24px) + labels (10px), active = Sky Blue icon + label, inactive = warm gray.
* **Navigation Bar:** 44px height, back chevron (left), destination name (center), share icon (right). Blurs content behind it (frosted glass effect).
* **CTAs:** Full-width Sky Blue (#0EA5E9), 52px height, 12px radius, Inter semibold 500 16px white text.
* **Bottom Sheet:** 20px top corners radius, drag handle (32×4px, Cloud color, centered). Elevated with modal overlay.
* **Filter Chips:** 32px height pill, selected = Sky Blue 10% bg + Sky Blue text + Sky Blue border, unselected = Cloud border + charcoal text.

## 5. Layout Principles (Mobile-First)
- **Safe areas:** 47px status bar (top), 34px home indicator (bottom)
- **Content padding:** 16px horizontal, 16px vertical
- **Tap target minimum:** 44×44px — all interactive elements
- **Card width:** Full-width minus 32px (16px margins each side)
- **Image aspect ratios:** 16:9 for destination cards, 1:1 for profile avatars
- **Scroll direction:** Vertical primary; horizontal for card carousels only

## 6. Design System Notes for Stitch Generation

**DESIGN SYSTEM (REQUIRED):**
- Platform: Mobile, iOS-first
- Theme: Light, editorial, photography-first, warm
- Background: Warm White (#FAFAF8) — primary screen background
- Surface: Sand (#F5F0E8) — cards and bottom sheet surfaces
- Primary Accent: Sky Blue (#0EA5E9) — CTAs and active states
- Text Primary: Charcoal (#1C1917) — headlines and body
- Text Secondary: Warm Gray (#78716C) — labels and metadata
- Font: DM Serif Display (destination names) + Inter (all other text)
- Bottom Tab Bar: 49px height, 5 tabs, active = Sky Blue icon+label
- Cards: 16:9 image, gradient overlay, 16px corners, full-width card rows
- CTAs: Full-width buttons, 52px height, 12px radius, Sky Blue fill
- Safe Areas: Status bar (47px top), home indicator (34px bottom) — NO interactive elements in safe zones
- Minimum tap target: 44×44px for all interactive elements
- Mood: Editorial travel magazine — airy, warm, photography-first
```

---

## Example Screen — Home/Explore

```markdown
The main Explore screen of Wandr travel planning app.

**DESIGN SYSTEM (REQUIRED):**
[paste Section 6 block from above]

**Screen Structure:**
1. **Status Bar Area (top 47px):** System status bar — time, battery, signal. Warm White background.
2. **Navigation Bar (44px):** Wandr logo (center). Profile avatar + bell icon (right).
3. **Search Bar:** Full-width, Sand background, cloud border, "Where to next?" placeholder, 12px radius
4. **"Featured Destinations" Section:** Section header label. Horizontal scrollable card row — 3 cards visible (2.5 shown to hint scroll). Each card: destination photo, name overlay, heart icon.
5. **"Your Upcoming Trips" Section:** Section header. Vertical card list — each shows destination photo (left), trip name, dates, traveler count, progress indicator.
6. **"Trending This Week" Section:** 2-column grid of smaller cards with destination and price.
7. **Bottom Tab Bar (49px + 34px safe area):** Explore (active/Sky Blue), Trips, Search, Saved, Profile.
8. **Home Indicator Area (34px):** Empty safe area at bottom.
```

---

## Safe Area Implementation (React Native / CSS)

```tsx
// React Native: use SafeAreaView
import { SafeAreaView } from 'react-native-safe-area-context'
<SafeAreaView edges={['top', 'bottom']}>
  <Content />
</SafeAreaView>

// CSS (PWA / web app): env() variables
.screen-container {
  padding-top: max(16px, env(safe-area-inset-top));
  padding-bottom: max(16px, env(safe-area-inset-bottom));
}

// Tailwind (with Tailwind CSS v3 plugin):
// pt-safe pb-safe (requires tailwindcss-safe-area plugin)
```

---

## Mobile App vs. Web Mobile: Key Differences

| Decision | Mobile App (this example) | Web Mobile-First |
|:---|:---|:---|
| Navigation | Bottom tab bar (49px) | Top hamburger or nav |
| Bottom safe area | Always respected | Usually ignored |
| Touch targets | 44px hard minimum | Aim for 44px but often miss |
| Pull-to-refresh | Implied behavior | Rarely implemented |
| Fonts | System font preferred | Web fonts fine |
| Gestures | Swipe, pinch, long-press | Tap and scroll only |
