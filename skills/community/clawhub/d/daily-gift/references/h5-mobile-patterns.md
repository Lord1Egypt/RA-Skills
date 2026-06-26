# H5 Mobile Patterns

Adapted from frontend-design-ultimate for single-page H5 gifts viewed on mobile phones.

## Why This Matters

Daily gift H5s are viewed almost exclusively on mobile phones such as Telegram or WeChat in-app browsers. Every design decision must be mobile-first.

## Viewport Setup

Always include:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```

## Font Size Rules

- Minimum body text: `13px`
- Main display text: use `clamp()` or `vw` units to scale with screen width
- iOS zooms on input focus if `font-size < 16px`; avoid form elements below that
- Test readability at `375px` width, the narrowest common screen

## Touch Target Sizes

- Minimum `44x44px` for any tappable element
- Audio toggle button: at least `36x36px` with adequate padding
- If the gift has tap interactions, make tap zones generous

## Safe Areas

- Top `44px`: may be covered by the phone status bar or in-app browser header
- Bottom `34px`: may be covered by the iPhone home indicator
- Keep critical content away from edges; use padding of at least `16px` on all sides

## Canvas Sizing

For `p5.js` gifts:

```javascript
function setup() {
  createCanvas(windowWidth, windowHeight);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
```

Always handle `windowResized()`. Phones rotate, and in-app browsers may resize mid-session.

## Text on Canvas

When using `p5.js text()`:

- `textSize` should be relative to canvas width, not hardcoded pixels
- Example: `textSize(width * 0.04)` instead of `textSize(16)`
- This keeps text proportional across screen sizes
- Test on both narrow (`375px`) and wide (`428px`) phone screens

## Aspect Ratio Considerations

Most gift H5s work best at full-screen mobile, approximately `9:16` to `9:19.5`:

- do not design for desktop-width layouts
- do not assume landscape orientation
- vertical scrolling is acceptable, but auto-play gifts should fit one screen

## Performance

Mobile phones have limited GPU and CPU:

- keep particle count under `100` for smooth animation unless there is a strong reason otherwise
- avoid heavy blur filters on large areas
- base64-encoded audio should be under `500KB`
- total HTML file size should stay under `1MB` for fast loading
- test mentally for mid-range phones, not just flagship devices

## Color and Contrast

- phone screens vary widely in brightness and color accuracy
- avoid very low contrast text
- dark mode gifts often look richer on OLED screens
- consider both bright daylight and dark-room viewing

## Common Mobile Failures

| Failure | Fix |
|---|---|
| Text too small to read | Use relative sizing such as `vw` or width-based sizing |
| Tap targets too small | Keep minimum `44x44px` |
| Content behind status bar | Add top padding |
| Canvas does not resize on rotate | Implement `windowResized()` |
| Animation janky on older phones | Reduce particle count |
| Audio does not play | Add a `touchstart` listener for the first interaction |
| File too large, slow to load | Compress audio and limit total size |
