# Figma Node Interpretation Rules
> Referenced by SKILL.md Step 1. Read this file when analyzing Figma fetch results.

## Style References and Text Sizing

- Note `styleRefs` on nodes — these reference Figma shared styles (design tokens). Nodes sharing the same style ID should use the same code-level token/resource
- Note `textAutoResize` on TEXT nodes — `WIDTH_AND_HEIGHT` means auto-size (wrap_content), `HEIGHT` means fixed width + auto height, absent/NONE means fixed size

## Figma Node Interpretation (apply before generating any platform code)

- **Skip system chrome**: StatusBar, HomeIndicator, NavigationBar are iOS design placeholders — don't generate code for them. Also skip duplicate nodes at the same position (Figma artifacts)
- **Skip invisible nodes**: VECTOR/RECTANGLE with empty fills and all strokes `visible: false`, or `absoluteRenderBounds: null` — these are leftover design artifacts that render nothing
- **layoutAlign=STRETCH**: child fills the cross-axis of its auto-layout parent → `match_parent` on the cross-axis / `.frame(maxWidth: .infinity)`. Only present when it differs from INHERIT
- **layoutPositioning=ABSOLUTE**: child is absolutely positioned within an auto-layout parent → use explicit x/y offset constraints instead of flow layout
- **Container + icon = single view**: A FRAME (with background/cornerRadius) wrapping a small VECTOR/INSTANCE is one ImageView/Image, not nested layouts
- **VECTOR/ELLIPSE compositions = single asset**: Multiple small VECTOR/ELLIPSE siblings inside a FRAME are pieces of one icon — output as a single image reference, not separate views
- **RECTANGLE as background**: When a GROUP's first child is a RECTANGLE matching the GROUP's dimensions, it's a background shape, not a separate view
- **GROUP vs FRAME**: FRAME with `layoutMode` maps to structured layouts (LinearLayout, HStack, etc.); GROUP without `layoutMode` uses absolute positioning — map to ConstraintLayout constraints or explicit offsets
- **Round Figma decimals**: Round dp to nearest integer, sp to nearest 0.5. Snap near-standard values (e.g., 47.99 → 48dp)
- **Width strategy**: Don't blindly copy Figma width values — infer design intent. Elements spanning near-full screen width → `match_parent` + `marginHorizontal`. In side-by-side layouts, identify the "flexible" element (text/content) vs "fixed" element (icon/avatar) and use `0dp` + constraints for the flexible one. See xml-patterns.md "Width Strategy" for full rules.

## Page Architecture Analysis (all platforms)

These rules apply to ALL output platforms (Android XML, Compose, SwiftUI, UIKit). The examples below use Android XML, but the principles are universal — each platform's patterns file has the equivalent implementation.

- Multiple tab labels → likely `TabLayout` + `ViewPager2`, content in Fragment layouts (strong signal, not absolute — ask if unsure)
- Tab color differences between items → selected/unselected state, use `tabSelectedTextColor` / `tabTextColor`, not hardcoded per-tab colors
- Navigation bar with back/close icon → `ImageView` (src + background), not FrameLayout wrapper
- Buttons with icon + text → **always** use `LinearLayout` + `ImageView` + `TextView`. Never use `MaterialButton` with `app:icon` (rendering issues) or `TextView` with `drawableStart`/`drawableEnd` (icon centering issues)
- List item with left sidebar + right content → observe multiple items to judge if equal-height or independent
- **Stacked/overlapping cards** with similar structure (same shape, offset position) → likely a card-switching interaction (swipe, stack, flip). Do NOT generate as separate static Views. Instead, ask the user: "These cards appear stacked — is this a swipe/switch interaction? If so, what's the switching behavior (left-right swipe, tap to flip, auto-play)?" The implementation (custom View, ViewPager2, third-party CardStackView, etc.) depends on the answer.

### Component Variants → Multi-State Code

When INSTANCE nodes have `variantProperties`, they represent different states of the same component.

**How to use:**
1. If the design contains multiple INSTANCE nodes with the same `componentId` but different `variantProperties` (e.g. State=Default, State=Pressed, State=Disabled), these are states of one component
2. Generate **one** view/composable with state handling, not multiple separate views
3. Map common variant properties to platform state mechanisms:

| Variant Property | Android XML | Compose | iOS |
|---|---|---|---|
| State=Default/Pressed/Disabled | `selector` drawable + `state_pressed`/`state_enabled` | `Modifier.clickable` + conditional styling | `UIControl` states / `.disabled()` |
| State=Selected/Unselected | `state_selected` + `duplicateParentState` | `var isSelected by remember` + conditional | `isSelected` property |
| State=Active/Inactive | `state_activated` | boolean state + conditional | custom state |
| Size=Small/Medium/Large | Different dimension values in same layout | Parameterized composable with size enum | Parameterized view |
| Type=Primary/Secondary/Outline | Different style resources | Different color/border params | Different configuration |

4. If only **one state** is present in the design (e.g. only State=Default), still note the variant property — mention to the user that other states exist and ask if they want state handling generated
5. Size and Type variants → generate a parameterized component with enum/sealed class, not hardcoded values

**Example — Button with State variants:**
If Figma shows a button with variantProperties `{"State": "Default"}`, and you know (from componentId) this component also has Pressed and Disabled states:
- Android XML: generate the default state layout + mention selector drawable needed for other states
- Compose: generate a composable with `enabled` parameter + conditional colors/alpha

### Figma Style References → Consistent Token Usage

When nodes have `styleRefs`, they reference Figma's shared styles (design tokens).

**How to use:**
1. Nodes sharing the **same style ID** (e.g. same `styleRefs.fill` value) should use the **same code-level resource/token**, even if the actual hex values happen to be identical
2. This helps identify the designer's semantic intent — two texts with the same `styleRefs.text` ID are meant to use the same text style, even if their fontSize happens to differ slightly (designer oversight)
3. When project scan is available: try to match Figma style semantic names to project resources. For example, if multiple nodes share a fill style and the color is `#0158FF` → likely the project's `@color/primary` or `colorScheme.primary`
4. When generating code, **group by styleRef first, then by value**:
   - Same styleRef → must use same resource reference
   - Same value but different styleRef → can use same resource, but note the discrepancy
   - Different value and different styleRef → different resources

**Practical application:**
- You don't need to resolve the Figma style ID to a name (that requires an extra API call)
- Just use it as a **grouping key**: "these 5 text nodes all share styleRef.text = S:def456, so they should all use the same text style in code"
- If you notice inconsistency (same styleRef but different rendered values), flag it to the user as a potential design inconsistency

## Multi-State Batch Compare

When the user provides multiple Figma frames representing different states of the same page:

1. Use `figma_fetch.py --compare` to get all states + diff
2. The diff output shows exactly what changes between states (color, text, opacity, visibility, etc.)
3. Use diff results to generate appropriate state handling:
   - Color changes → selector drawable / conditional color
   - Opacity changes → alpha animation / enabled state
   - Visibility changes → View.GONE / if-else block
   - Text changes → dynamic text binding
4. Output a state change summary table after the code

**Usage:**
```bash
# Two separate Figma URLs (different frames)
python figma_fetch.py "<url1>" "<url2>" --compare

# Multiple node-ids from the same file
python figma_fetch.py "<base_url>" --nodes "100:200,100:300" --compare
```

The output JSON contains a `nodes` array (one entry per state with its full simplified tree)
and a `diff` object with `changed`, `added`, and `removed` lists.
Base is always the first node; each subsequent node is diffed against it.
`label` is taken from the Figma node name (e.g. the frame name), or falls back to "State 1", "State 2".
