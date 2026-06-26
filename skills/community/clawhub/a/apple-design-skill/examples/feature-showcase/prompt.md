# Example Prompt: Feature Showcase Page

## User Input

> Create a feature showcase page highlighting 4 key features of **Apple Watch**, Apple style. Language: Chinese (zh-CN).
>
> The page should include:
> - A full-screen dark Hero section with a bold Chinese headline using 对仗 or 四字格 patterns
> - A scroll-animated section introducing the product vision
> - A feature comparison cards section showcasing 4 key features (health monitoring, fitness tracking, connectivity, battery life)
> - A call-to-action section encouraging the user to explore or buy
>
> Language: Chinese (zh-CN)
> Output format: Standalone HTML with CSS custom properties

## Expected Behavior

When the Apple Design Skill processes this prompt, it should:

1. Load `design-tokens.md` to establish CSS custom properties for colors, spacing, shadows, radii, and gradients.
2. Load `typography.md` to detect Chinese (zh-CN) and select the PingFang SC font stack with Noto Sans SC as Google Fonts fallback.
3. Load `copywriting.md` to apply Chinese copywriting patterns — 对仗 (parallel structure), 四字格 (four-character idiom), and 反问 (rhetorical question) — for headlines and body copy.
4. Load `image-curation.md` to apply CSS gradient fallbacks (since no image API is available).
5. Load `layout-patterns.md` to assemble the Hero, scroll-animated section, feature comparison cards, and CTA sections using the standard templates.

## Key Differences from English Example

This example demonstrates the Skill's Chinese language capabilities:

- **Font stack:** PingFang SC → Hiragino Sans GB → Microsoft YaHei → Noto Sans SC (Google Fonts fallback)
- **Letter spacing:** Chinese headings use `0.04em` tracking (vs. English `-0.015em`)
- **Copywriting patterns:** 对仗, 四字格, 反问 instead of English fragment sentences and superlatives
- **Title constraints:** ≤ 12 Chinese characters for headlines, ≤ 30 characters for subtitles
- **`lang` attribute:** `<html lang="zh-CN">` for correct font rendering

## Expected Output

See `output.html` in this directory for the complete generated result.
