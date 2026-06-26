# Remotion Composition Quality Gate

Use this checklist before rendering your walkthrough video. All ✅ items must be completed.

## ✅ Project Setup

- [ ] Remotion project initialized (or existing verified)
- [ ] Dependencies installed (`@remotion/transitions`, `@remotion/animated-emoji`)
- [ ] Asset directory created (`public/assets/screens/`)
- [ ] `screens.json` manifest created with all screens

## ✅ Asset Preparation

- [ ] All Stitch screenshots downloaded at full resolution (appended `=w{width}`)
- [ ] Images named descriptively and saved to `public/assets/screens/`
- [ ] Image dimensions recorded in `screens.json`
- [ ] Asset paths are correct and relative to `public/`

## ✅ Component Structure

- [ ] `ScreenSlide.tsx` component created
  - [ ] `Props` interface defined with `Readonly<T>`
  - [ ] Zoom animation using `spring()` + `useCurrentFrame()`
  - [ ] Fade animation using `interpolate()`
  - [ ] Text overlay with title and description
- [ ] `WalkthroughComposition.tsx` created
  - [ ] `screens.json` manifest imported
  - [ ] `<Sequence>` components for each screen
  - [ ] Transitions between screens configured
  - [ ] Timing offsets calculated correctly (cumulative frame counts)

## ✅ Configuration

- [ ] `remotion.config.ts` updated
  - [ ] Composition ID matches component name
  - [ ] Video dimensions set (match Stitch screen or target platform)
  - [ ] Frame rate set (30fps default, 60fps for premium)
  - [ ] Duration calculated: `sum of (screen.duration * fps)` for all screens

## ✅ Animations & Transitions

- [ ] Spring animations use sane configs:
  - [ ] `damping`: 8–15 typical
  - [ ] `stiffness`: 60–100 typical
- [ ] Transitions feel smooth (preview at multiple speeds in Studio)
- [ ] Text overlays timed correctly — text visible before screen transitions
- [ ] No jarring or abrupt changes

## ✅ Visual Quality

- [ ] Text readable at all times (sufficient contrast)
- [ ] Font sizes appropriate for video resolution
- [ ] Images display without distortion (aspect ratios maintained)
- [ ] No blurry screenshots (verify source resolution)

## ✅ Preview & Testing

- [ ] Preview in Remotion Studio (`npm run dev`)
- [ ] Scrub through entire timeline frame-by-frame
- [ ] Verified smooth playback at normal speed
- [ ] No rendering errors in console

## ✅ Rendering

- [ ] Render command works: `npx remotion render WalkthroughComposition output.mp4`
- [ ] Codec specified: `--codec h264` (recommended for compatibility)
- [ ] Output video plays correctly in media players
- [ ] File size is reasonable

## 🎨 Optional Enhancements

- [ ] Progress indicator bar showing current screen position
- [ ] Voiceover audio synced with screen timing
- [ ] Animated hotspots highlighting key UI elements
- [ ] Call-to-action card at end of video

## screens.json Schema

```json
{
  "projectName": "My App",
  "screens": [
    {
      "id": "1",
      "title": "Home Screen",
      "description": "Main landing page with hero and CTA",
      "imagePath": "assets/screens/home.png",
      "width": 1440,
      "height": 900,
      "duration": 4
    },
    {
      "id": "2",
      "title": "About Page",
      "description": "Company story and team",
      "imagePath": "assets/screens/about.png",
      "width": 1440,
      "height": 900,
      "duration": 3
    }
  ]
}
```
