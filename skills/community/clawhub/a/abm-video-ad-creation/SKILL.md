---
name: video-ad-creation
description: "When the user wants to create video advertisements using Remotion. Also use when the user mentions 'video ad,' 'create ad video,' 'ad creative video,' 'promotional video,' 'product video ad,' or 'marketing video.' Guides creation of standard ad format compositions (15s, 30s, 60s) with scene-based storytelling structure. For project setup and core Remotion APIs, see remotion-best-practices. For social media video formats, see social-video-content."
metadata:
  version: 1.0.0
---

# Video Ad Creation

You help users create video advertisements using React and Remotion. Your goal is to produce ad compositions in standard durations (15s, 30s, 60s) with compelling scene-based storytelling -- hook, value proposition, and call-to-action -- optimized for digital advertising platforms.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Ad duration** -- 15s, 30s, or 60s
2. **Product or service** -- what is being advertised
3. **Key message and CTA** -- the main value proposition and desired action
4. **Brand assets** -- logo, colors, fonts
5. **Target platform** -- web, social, TV, or pre-roll

## Workflow

### Step 1: Choose Ad Format

Present the three standard ad durations:

| Duration | Frames (60fps) | Scenes | Best For |
|----------|----------------|--------|----------|
| 15s | 900 | 3 | Social ads, bumper ads, retargeting |
| 30s | 1800 | 4 | Standard digital ads, pre-roll |
| 60s | 3600 | 5 | Brand storytelling, product demos, explainers |

Default resolution: **1920x1080** (landscape). Default FPS: **60**.

For detailed format specifications and scene timing breakdowns, read `references/formats.md`.

### Step 2: Plan Scene Structure

Each ad duration has a recommended scene structure:

**15s ad** (3 scenes):
- **Hook** (3s / 180 frames): Grab attention immediately
- **Value Prop** (9s / 540 frames): Showcase the product or key benefit
- **CTA** (3s / 180 frames): Clear call-to-action with brand

**30s ad** (4 scenes):
- **Hook** (5s / 300 frames): Attention-grabbing opener
- **Problem** (7s / 420 frames): Present the pain point
- **Solution** (13s / 780 frames): Show how the product solves it
- **CTA** (5s / 300 frames): Call-to-action with brand reinforcement

**60s ad** (5 scenes):
- **Hook** (5s / 300 frames): Bold opener to stop the scroll
- **Problem** (10s / 600 frames): Deep dive into the pain point
- **Solution** (20s / 1200 frames): Product demonstration and benefits
- **Social Proof** (15s / 900 frames): Testimonials, stats, trust signals
- **CTA** (10s / 600 frames): Strong call-to-action with brand outro

### Step 3: Register Composition

Register the ad as a Composition in `src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { AdVideo } from "./AdVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="VideoAd15s"
      component={AdVideo}
      durationInFrames={900}
      fps={60}
      width={1920}
      height={1080}
      defaultProps={{
        headline: "Your Product",
        cta: "Learn More",
        brandColor: "#0066FF",
      }}
    />
  );
};
```

For 30s ads, use `durationInFrames={1800}`. For 60s ads, use `durationInFrames={3600}`.

### Step 4: Build Scene Components

Each scene is a separate React component composed with `<Sequence>` for timeline positioning:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill, Sequence } from "remotion";

const HookScene: React.FC<{ headline: string }> = ({ headline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 100 } });
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", backgroundColor: "#0066FF" }}>
      <h1 style={{ opacity, transform: `scale(${scale})`, fontSize: 72, color: "white" }}>
        {headline}
      </h1>
    </AbsoluteFill>
  );
};
```

Compose scenes on the ad timeline:

```tsx
export const AdVideo: React.FC<{ headline: string; cta: string; brandColor: string }> = (props) => {
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={180}>
        <HookScene headline={props.headline} />
      </Sequence>
      <Sequence from={180} durationInFrames={540}>
        <ValuePropScene />
      </Sequence>
      <Sequence from={720} durationInFrames={180}>
        <CTAScene cta={props.cta} brandColor={props.brandColor} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

Each `<Sequence>` resets `useCurrentFrame()` to 0 for its children, so each scene animates independently.

### Step 5: Render

Render the ad locally:

```bash
npx remotion render src/index.ts VideoAd15s out/ad-15s.mp4
```

For different durations, register additional compositions and render each:

```bash
npx remotion render src/index.ts VideoAd30s out/ad-30s.mp4
npx remotion render src/index.ts VideoAd60s out/ad-60s.mp4
```

Preview in browser before rendering:

```bash
npx remotion preview src/index.ts
```

See `tools/integrations/remotion.md` for the full CLI command reference.

## Output Format

Deliver a working ad composition with:

1. **`src/Root.tsx`** -- Composition registration with correct duration, fps, and dimensions
2. **Scene components** -- One `.tsx` file per scene (HookScene, ValuePropScene, CTAScene, etc.)
3. **Render command** -- The exact `npx remotion render` command for the chosen duration
4. **Preview command** -- `npx remotion preview src/index.ts` for browser preview

## Related Skills

- **remotion-best-practices**: Project setup, core APIs, animation patterns, rendering pipeline
- **social-video-content**: Social platform video formats (vertical, square, landscape)
