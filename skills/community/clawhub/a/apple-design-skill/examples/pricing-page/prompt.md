# Example Prompt: Pricing Comparison Page

## User Input

> Build a pricing comparison page with 3 tiers (Basic, Pro, Enterprise) for a SaaS product in Apple's clean design language.
>
> The page should include:
> - A Hero section with a clean headline introducing the pricing
> - 3 pricing cards in a responsive grid (1→3 columns) showing tier name, price, feature list, and CTA button
> - The "Pro" tier highlighted as the recommended option
> - Scroll reveal animations for a polished feel
>
> Language: English
> Output format: Standalone HTML with CSS custom properties

## Expected Behavior

When the Apple Design Skill processes this prompt, it should:

1. Load `design-tokens.md` to establish CSS custom properties for colors, spacing, shadows, radii, and gradients.
2. Load `typography.md` to select the English font stack (SF Pro Display / SF Pro Text with Inter as Google Fonts fallback).
3. Load `copywriting.md` to refine the headlines into Apple-style fragment sentences (short, punchy, benefit-first).
4. Load `image-curation.md` to apply CSS gradient fallbacks (since no image API is available).
5. Load `layout-patterns.md` to assemble the Hero and pricing card grid using the standard templates, adapting the product grid pattern for pricing tiers.

## Key Differences from Other Examples

This example demonstrates the Skill's versatility beyond product pages:

- **Use case:** SaaS pricing — not a hardware product page
- **Layout adaptation:** The product grid pattern from `layout-patterns.md` is adapted for pricing cards with feature lists and CTA buttons
- **Highlighted tier:** The "Pro" card uses a dark background with gradient accent to stand out as the recommended option
- **Feature lists:** Each card contains a structured list of included features, styled with Apple's restrained typography
- **CTA buttons:** Pill-shaped buttons using `--apple-radius-button` with primary/secondary variants

## Expected Output

See `output.html` in this directory for the complete generated result.
