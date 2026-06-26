# Example Prompt: Product Landing Page

## User Input

> Generate a product landing page for **AirPods Max** wireless headphones in Apple style.
>
> The page should include:
> - A full-screen dark Hero section with a bold headline and subtitle
> - A product features section highlighting key selling points (sound quality, noise cancellation, battery life, spatial audio)
> - A call-to-action section encouraging the user to buy or learn more
>
> Language: English
> Output format: Standalone HTML with CSS custom properties

## Expected Behavior

When the Apple Design Skill processes this prompt, it should:

1. Load `design-tokens.md` to establish CSS custom properties for colors, spacing, shadows, radii, and gradients.
2. Load `typography.md` to select the English font stack (SF Pro Display / SF Pro Text with Inter as Google Fonts fallback).
3. Load `copywriting.md` to refine the headlines into Apple-style fragment sentences (short, punchy, benefit-first).
4. Load `image-curation.md` to apply CSS gradient fallbacks (since no image API is available).
5. Load `layout-patterns.md` to assemble the Hero, feature cards, and CTA sections using the standard templates.

## Expected Output

See `output.html` in this directory for the complete generated result.
