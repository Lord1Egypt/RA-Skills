# Ad Format Specifications

Detailed format specs for video advertisements. All durations use **60fps** and **1920x1080** (landscape) as defaults.

## Quick Reference

| Duration | Frames | Scenes | Use Case |
|----------|--------|--------|----------|
| 15s | 900 | 3 | Social ads, bumper ads, retargeting |
| 30s | 1800 | 4 | Standard digital ads, pre-roll |
| 60s | 3600 | 5 | Brand storytelling, product demos, explainers |

**Frame calculation:** `duration_seconds * fps = frames` (e.g., 15 * 60 = 900)

## 15-Second Ad Template

Total: **900 frames** at 60fps

| Scene | Time | Frames | Purpose | Recommended Animations |
|-------|------|--------|---------|----------------------|
| Hook | 0-3s | 0-179 | Grab attention instantly | Bold text entrance with `spring()`, fast scale-up |
| Value Prop | 3-12s | 180-719 | Product showcase, key benefit | Image/text fade-in with `interpolate()`, slide transitions |
| CTA | 12-15s | 720-899 | Call-to-action, brand logo | Button bounce with `spring()`, logo fade-in |

**Best practices for 15s:**
- Front-load the hook -- viewers decide in the first second
- One message only -- no time for multiple value props
- Large text (64px+) -- many viewers watch on mobile
- Brand visible throughout (logo watermark or brand color)

### Composition Registration

```tsx
<Composition
  id="VideoAd15s"
  component={AdVideo}
  durationInFrames={900}
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{ headline: "Your Product", cta: "Learn More", brandColor: "#0066FF" }}
/>
```

## 30-Second Ad Template

Total: **1800 frames** at 60fps

| Scene | Time | Frames | Purpose | Recommended Animations |
|-------|------|--------|---------|----------------------|
| Hook | 0-5s | 0-299 | Attention-grabbing opener | Bold text `spring()`, background movement |
| Problem | 5-12s | 300-719 | Present the pain point | Text fade-in, icon animations |
| Solution | 12-25s | 720-1499 | Product solves the problem | Product image scale, feature callouts |
| CTA | 25-30s | 1500-1799 | Call-to-action, brand outro | Button animation, logo + URL reveal |

**Best practices for 30s:**
- Problem-solution structure works best at this length
- Show the product in action during the Solution scene
- End card should include logo, CTA button, and website URL
- Pacing: quick hook, deliberate middle, punchy close

### Composition Registration

```tsx
<Composition
  id="VideoAd30s"
  component={AdVideo}
  durationInFrames={1800}
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{ headline: "Solve Your Problem", cta: "Get Started", brandColor: "#0066FF" }}
/>
```

## 60-Second Ad Template

Total: **3600 frames** at 60fps

| Scene | Time | Frames | Purpose | Recommended Animations |
|-------|------|--------|---------|----------------------|
| Hook | 0-5s | 0-299 | Bold opener to stop the scroll | Large text `spring()`, dramatic reveal |
| Problem | 5-15s | 300-899 | Deep dive into pain point | Animated stats, icon sequences |
| Solution | 15-35s | 900-2099 | Product demo and benefits | Product walkthrough, feature highlights |
| Social Proof | 35-50s | 2100-2999 | Testimonials, stats, trust | Quote fade-ins, number counters |
| CTA | 50-60s | 3000-3599 | Strong call-to-action, brand outro | Button bounce, logo + URL + offer |

**Best practices for 60s:**
- Full storytelling arc -- enough time to build emotional connection
- Social proof scene builds credibility before the ask
- Can include multiple product features in the Solution scene
- End card can be more elaborate (offer details, multiple CTAs)

### Composition Registration

```tsx
<Composition
  id="VideoAd60s"
  component={AdVideo}
  durationInFrames={3600}
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{ headline: "The Full Story", cta: "Start Free Trial", brandColor: "#0066FF" }}
/>
```

## Resolution Specs

| Format | Resolution | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Standard landscape | 1920x1080 | 16:9 | Web ads, YouTube pre-roll, TV |
| Square variant | 1080x1080 | 1:1 | Social feed ads (Instagram, Facebook, LinkedIn) |
| Vertical variant | 1080x1920 | 9:16 | Story/reel ads (Instagram, TikTok, Snapchat) |

For social-specific format details, see the **social-video-content** skill.

## Common Ad Patterns

### Text Overlay on Background

Layer text over a full-bleed background using `AbsoluteFill`:

```tsx
<AbsoluteFill>
  <AbsoluteFill style={{ backgroundColor: brandColor }} />
  <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
    <h1 style={{ fontSize: 72, color: "white" }}>{headline}</h1>
  </AbsoluteFill>
</AbsoluteFill>
```

### Product Showcase

Animate a product image with scale and opacity:

```tsx
const scale = interpolate(frame, [0, 30], [0.8, 1], { extrapolateRight: "clamp" });
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

<Img src={productImage} style={{ transform: `scale(${scale})`, opacity }} />
```

### Price/Offer Callout

Use `spring()` for a bounce-in effect on price or discount text:

```tsx
const scale = spring({ frame, fps, config: { damping: 8, stiffness: 200 } });

<div style={{ transform: `scale(${scale})`, fontSize: 64, fontWeight: "bold" }}>
  50% OFF
</div>
```

### End Card

Brand logo, CTA button, and website URL composed together:

```tsx
const logoOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
const buttonScale = spring({ frame: frame - 10, fps, config: { damping: 10 } });

<AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 }}>
  <Img src={logo} style={{ opacity: logoOpacity, width: 200 }} />
  <div style={{ transform: `scale(${Math.max(0, buttonScale)})`, padding: "20px 40px", backgroundColor: brandColor, borderRadius: 8 }}>
    <span style={{ fontSize: 36, color: "white" }}>{cta}</span>
  </div>
  <span style={{ opacity: logoOpacity, fontSize: 24, color: "#ccc" }}>www.example.com</span>
</AbsoluteFill>
```
