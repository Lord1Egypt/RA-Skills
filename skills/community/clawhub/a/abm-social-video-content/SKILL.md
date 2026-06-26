---
name: social-video-content
description: "When the user wants to create video content for social media platforms using Remotion. Also use when the user mentions 'social video,' 'video for social,' 'short-form video,' 'reels,' 'TikTok video,' 'YouTube Shorts,' 'Instagram video,' or 'social media clip.' Guides creation of platform-specific compositions in vertical (9:16), square (1:1), and landscape (16:9) formats. For project setup and core Remotion APIs, see remotion-best-practices. For video advertisements, see video-ad-creation."
metadata:
  version: 1.0.0
---

# Social Video Content

You help users create video content optimized for social media platforms using React and Remotion. Your goal is to produce compositions in the right format for each platform -- vertical for Reels/TikTok/Shorts, square for feed posts, landscape for YouTube -- with scroll-stopping hooks and mobile-first design.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Target platform(s)** -- Reels, TikTok, YouTube Shorts, feed post, YouTube, LinkedIn, Twitter/X
2. **Content topic or message** -- what the video communicates
3. **Desired duration** -- typically 15-60s for short-form, up to 120s for landscape
4. **Brand assets** -- logo, colors, fonts
5. **Content style** -- educational, promotional, entertaining, behind-the-scenes

## Workflow

### Step 1: Select Platform Format

Choose the format based on the target platform:

| Format | Aspect Ratio | Resolution | Platforms | Duration Range |
|--------|-------------|------------|-----------|---------------|
| Vertical | 9:16 | 1080x1920 | Reels, TikTok, YouTube Shorts | 15-60s |
| Square | 1:1 | 1080x1080 | Instagram feed, Facebook feed, LinkedIn | 15-60s |
| Landscape | 16:9 | 1920x1080 | YouTube, LinkedIn, Twitter/X | 15-120s |

Default FPS: **60** for all formats.

For detailed platform requirements including max durations, file size limits, and codec recommendations, read `references/platforms.md`.

### Step 2: Plan Content Structure

Social video structure differs from ads -- the hook is everything:

- **Hook** (first 1-3s): Critical for scroll-stopping. Bold text, movement, contrast, or a provocative question. Viewers decide to stay or scroll in the first second.
- **Content** (middle): Key message, demonstrations, information, or entertainment. Keep pacing brisk -- cut or transition every 3-5 seconds.
- **CTA/Outro** (last 2-3s): Follow, subscribe, visit link, or share prompt.

**Vertical-specific considerations:**
- Content is consumed on mobile -- everything must be readable at phone size
- Top and bottom edges may be covered by platform UI (username, caption, buttons)
- Center-weight your composition for the safe zone

### Step 3: Register Composition

Register platform-specific compositions in `src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { SocialVideo } from "./SocialVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Vertical (Reels/TikTok/Shorts) */}
      <Composition
        id="ReelsVideo"
        component={SocialVideo}
        durationInFrames={1800}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{ text: "Hook text here" }}
      />

      {/* Square (Feed post) */}
      <Composition
        id="FeedPost"
        component={SocialVideo}
        durationInFrames={900}
        fps={60}
        width={1080}
        height={1080}
        defaultProps={{ text: "Feed content" }}
      />

      {/* Landscape (YouTube) */}
      <Composition
        id="YouTubeVideo"
        component={SocialVideo}
        durationInFrames={3600}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{ text: "YouTube content" }}
      />
    </>
  );
};
```

One project can have multiple compositions for multi-platform output. Share scene components but register each format as a separate composition.

### Step 4: Build for Vertical-First

Vertical (9:16) is the dominant social format. Key patterns for mobile-optimized layouts:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill } from "remotion";

const VerticalScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textScale = spring({ frame, fps, config: { damping: 10, stiffness: 150 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{
      backgroundColor: "#1a1a2e",
      justifyContent: "center",
      alignItems: "center",
      padding: "0 60px",
    }}>
      <h1 style={{
        opacity,
        transform: `scale(${textScale})`,
        fontSize: 64,
        color: "white",
        textAlign: "center",
        lineHeight: 1.2,
      }}>
        {text}
      </h1>
    </AbsoluteFill>
  );
};
```

**Vertical layout rules:**
- Stack content vertically in `AbsoluteFill`
- Minimum text size: **48px** for readability on mobile
- Center-weighted composition: keep content in the middle 80% of height
- Full-screen background images or solid colors (no letterboxing)
- Add horizontal padding (40-60px) to keep text off screen edges

### Step 5: Render

Render each platform format as a separate output:

```bash
npx remotion render src/index.ts ReelsVideo out/reels.mp4
npx remotion render src/index.ts FeedPost out/feed-post.mp4
npx remotion render src/index.ts YouTubeVideo out/youtube.mp4
```

Preview in browser:

```bash
npx remotion preview src/index.ts
```

See `tools/integrations/remotion.md` for the full CLI command reference.

## Output Format

Deliver a working social video project with:

1. **`src/Root.tsx`** -- Platform-specific Compositions with correct dimensions, fps, and duration
2. **Scene components** -- Reusable `.tsx` components that adapt to different aspect ratios
3. **Render commands** -- One `npx remotion render` command per platform variant
4. **Preview command** -- `npx remotion preview src/index.ts` for browser preview

## Related Skills

- **remotion-best-practices**: Project setup, core APIs, animation patterns, rendering pipeline
- **video-ad-creation**: Standard ad format compositions (15s/30s/60s) with product showcase templates
