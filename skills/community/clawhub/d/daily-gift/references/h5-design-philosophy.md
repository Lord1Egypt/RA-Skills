# H5 Design Philosophy

Adapted from frontend-design-ultimate for single-page H5 gift contexts using `p5.js`, canvas, and CSS.

## The Problem: AI-Slop H5 Gifts

Generic AI-generated H5 gifts often share these signs:

### Typography Sins

- only one font weight used throughout
- text all the same size, with no hierarchy
- centered everything with no rhythm
- generic system fonts with no personality

### Color Crimes

- pure black background with white text as lazy dark mode
- no color hierarchy
- random accent colors that do not connect to the gift's mood
- no warmth or temperature in the palette

### Layout Laziness

- everything dead-center on screen
- perfectly symmetrical with no tension
- elements stacked vertically with uniform spacing
- no visual surprise or asymmetry

### Motion Mediocrity

- CSS fade-in on everything with the same timing
- no orchestration
- no easing variety
- no relationship between motion and meaning

### Background Boredom

- solid black or solid dark blue
- plain CSS gradient
- no texture, grain, or depth

## The Solution: Intentional H5 Design

### Color As Emotion

Build the palette from the gift's emotional register:

- dark + confident: deep blacks, muted accents, one bright signal color
- warm + healing: cream, amber, sage, soft pink
- poetic + melancholy: desaturated blues, muted purples, rain-grey
- playful + bright: saturated primaries, white space, clean contrast

Use the `60-30-10` rule: `60%` dominant background, `30%` secondary elements, `10%` accent highlights.

### Typography As Voice

Even when text is rendered on canvas, keep hierarchy:

- one main text: larger and more visible
- supporting text: smaller and lighter
- accent text such as date stamps or labels: tiny and subdued
- use `textSize()` deliberately, not uniformly
- letter spacing matters; loose feels calm, tight feels urgent

### Motion As Narrative

Animation should tell a story rather than merely move:

- stagger entry timing
- match easing to mood
- use delay to create beats
- connect particles to emotional meaning

### Background As Atmosphere

The background is the first thing the viewer feels:

- generated image backgrounds often add richness CSS gradients cannot
- subtle noise or grain removes sterile digital feel
- vignette helps focus attention
- bokeh or soft light circles add depth

## Design Decision Quick Test

Before shipping an H5 gift, ask:

1. Would I screenshot this?
2. Does it feel designed or generated?
3. What is the one element that makes this gift unique?
4. Is the motion orchestrated or random?
5. Does the background have atmosphere or is it just a color?

## Anti-Pattern Detection

| Anti-Pattern | Fix |
|---|---|
| All text same size | Apply clear size hierarchy |
| All text centered with same spacing | Vary position, alignment, and spacing |
| Pure CSS gradient background | Add texture, grain, or generated image |
| Everything fades in at once | Stagger with meaningful delays |
| No color temperature | Choose warm or cool and commit |
| Particles without purpose | Connect particle type to mood |
| Generic system font | Use a more intentional font choice, including a CDN-loaded web font when appropriate |
