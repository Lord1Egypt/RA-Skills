# Social Platform Specifications

Detailed platform requirements for social video content. Use this reference when choosing formats, resolutions, and duration limits for each platform.

> **Note:** Platform specs change frequently. Verify current limits on the platform's creator documentation before publishing.

## Platform Quick Reference

| Platform | Aspect Ratio | Resolution | Max Duration | Codec | Max File Size |
|----------|-------------|------------|--------------|-------|---------------|
| Instagram Reels | 9:16 | 1080x1920 | 90s | H.264 | 4GB |
| TikTok | 9:16 | 1080x1920 | 60s (default) | H.264 | 287MB |
| YouTube Shorts | 9:16 | 1080x1920 | 60s | H.264 | 256MB |
| Instagram Feed | 1:1 or 4:5 | 1080x1080 | 60s | H.264 | 4GB |
| YouTube | 16:9 | 1920x1080 | 12hr | H.264 | 256GB |
| LinkedIn | 1:1 or 16:9 | 1080x1080 | 10min | H.264 | 5GB |
| Twitter/X | 16:9 or 1:1 | 1920x1080 | 2min 20s | H.264 | 512MB |

All platforms support H.264 codec. Remotion renders H.264 by default -- no special configuration needed.

## Vertical (9:16) Design Guide

Vertical is the dominant format for short-form social content (Reels, TikTok, YouTube Shorts).

**Safe zone:**
- Top 180px may be covered by status bar, platform header, or notification bar
- Bottom 280px may be covered by caption text, username, like/share buttons
- **Effective content area:** 1080x1460 centered within 1080x1920
- Keep all critical text and visuals within the middle 76% of the height

**Text placement:**
- Center-weight all text (vertically and horizontally)
- Avoid placing text in the top 10% or bottom 15% of the frame
- Left-align body text with 40-60px horizontal padding

**Typography:**
- Minimum text size: **48px** for mobile readability
- Headlines: 56-72px
- Body text: 48-56px
- Use high-contrast colors (white on dark, or dark on light backgrounds)
- Bold weight for hook text -- thin fonts disappear on small screens

**Backgrounds:**
- Full-bleed images or solid colors (never letterbox)
- Dark backgrounds (#1a1a2e, #000000) work well for text-heavy content
- Gradient backgrounds add visual interest without distraction

**Composition example:**

```tsx
<Composition
  id="ReelsVideo"
  component={SocialVideo}
  durationInFrames={1800}  // 30s
  fps={60}
  width={1080}
  height={1920}
  defaultProps={{ text: "Hook text here", bgColor: "#1a1a2e" }}
/>
```

## Square (1:1) Design Guide

Square works universally across all platforms as feed content. It is the safest format for cross-platform distribution.

**Layout:**
- Balanced, centered compositions work best
- Equal visual weight on all sides
- No safe zone issues -- the full frame is visible on all platforms

**Typography:**
- Text can be slightly smaller than vertical: **40px** minimum
- Feed viewing distance is typically closer than full-screen vertical
- Center-align headlines, left-align body text

**Best for:**
- Instagram feed posts
- Facebook feed posts
- LinkedIn feed posts
- Cross-platform content (one render, multiple platforms)

**Composition example:**

```tsx
<Composition
  id="FeedPost"
  component={SocialVideo}
  durationInFrames={900}  // 15s
  fps={60}
  width={1080}
  height={1080}
  defaultProps={{ text: "Feed content", bgColor: "#0a0a1a" }}
/>
```

## Landscape (16:9) Design Guide

Landscape is the native YouTube format and works well on LinkedIn and Twitter/X.

**Layout:**
- Standard web video composition rules apply
- Wider canvas allows side-by-side layouts (text + image)
- Cinematic feel -- good for product demos and explainers

**Typography:**
- Minimum text size: **32px**
- More room for multi-line text and detailed information
- Subtitles: 28-36px at the bottom of the frame

**Best for:**
- YouTube (standard and long-form)
- LinkedIn native video
- Twitter/X timeline video
- Embedded web video

**Composition example:**

```tsx
<Composition
  id="YouTubeVideo"
  component={SocialVideo}
  durationInFrames={3600}  // 60s
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{ text: "YouTube content", bgColor: "#0f0f1a" }}
/>
```

## Render Commands

Render each platform format as a separate file:

```bash
# Vertical (Reels, TikTok, YouTube Shorts)
npx remotion render src/index.ts ReelsVideo out/reels.mp4

# Square (Instagram feed, Facebook, LinkedIn)
npx remotion render src/index.ts FeedPost out/feed-post.mp4

# Landscape (YouTube, LinkedIn, Twitter/X)
npx remotion render src/index.ts YouTubeVideo out/youtube.mp4
```

## Multi-Platform Strategy

Create one Remotion project with multiple Compositions to target every platform from a single codebase:

1. **Shared scene components** -- Write content scenes (hook, main content, CTA) as reusable React components
2. **Layout wrappers** -- Create format-specific layout components that adapt padding, text size, and positioning
3. **Multiple Compositions** -- Register one Composition per platform format in Root.tsx, each using the same scene components but with different dimensions
4. **Batch render** -- Render all formats with separate commands:

```bash
npx remotion render src/index.ts ReelsVideo out/reels.mp4
npx remotion render src/index.ts FeedPost out/feed-post.mp4
npx remotion render src/index.ts YouTubeVideo out/youtube.mp4
```

**Adaptive text size pattern:**

```tsx
import { useVideoConfig } from "remotion";

const AdaptiveText: React.FC<{ children: string }> = ({ children }) => {
  const { width } = useVideoConfig();
  // Scale text based on composition width
  const fontSize = width <= 1080 ? 56 : 42;

  return <h1 style={{ fontSize, color: "white", textAlign: "center" }}>{children}</h1>;
};
```

This approach lets one team produce content for all platforms without duplicating creative work.
