---
name: remotion-best-practices
description: "When the user wants to create videos programmatically with React using Remotion. Also use when the user mentions 'create video,' 'Remotion,' 'React video,' 'video composition,' 'programmatic video,' or 'render video.' Covers project setup, composition structure, animation patterns, and rendering pipeline. Does not cover ad-specific formats (see video-ad-creation) or social media formats (see social-video-content)."
metadata:
  version: 1.0.0
---

# Remotion Best Practices

You help users create videos programmatically using React and Remotion. Your goal is to scaffold projects, write compositions, build animated scene components, and render final video output -- all following Remotion v4 conventions and best practices.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **What video to create** -- subject, purpose, and visual style
2. **Target duration and dimensions** -- e.g., 15 seconds at 1920x1080
3. **New or existing project** -- whether to scaffold fresh or add to an existing Remotion project

## Workflow

### Step 1: Set Up Project

Check if a Remotion project already exists:
- Look for `package.json` with `@remotion/core` in `dependencies` or `devDependencies`
- If found: skip scaffolding and add a new composition to the existing `src/Root.tsx`
- If not found: scaffold a new project:

```bash
npx create-video@latest my-video
```

After scaffolding, verify all `@remotion/*` packages are on the same version:

```bash
npm ls | grep remotion
```

For detailed setup configuration, read `references/setup.md`.

### Step 2: Define Composition in Root.tsx

Register your video as a Composition in `src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { MyScene } from "./MyScene";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyScene}
      durationInFrames={900}  // 15s at 60fps
      fps={60}
      width={1920}
      height={1080}
      defaultProps={{ title: "My Video" }}
    />
  );
};
```

Key points:
- Use `fps={60}` as the project default (60fps for smooth animation)
- Use PascalCase for composition IDs (e.g., `MyVideo`, `ProductDemo`)
- Calculate `durationInFrames` as `seconds * fps` (15s at 60fps = 900 frames)

### Step 3: Build Scene Components

Use `AbsoluteFill` as the root layout container. Use `useCurrentFrame()` and `useVideoConfig()` for animation state. Use `<Sequence>` for timeline positioning.

Minimal animated component:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, AbsoluteFill } from "remotion";

export const MyScene: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ opacity, fontSize: 80, color: "white" }}>{title}</h1>
    </AbsoluteFill>
  );
};
```

For physics-based animation, use `spring()`:

```tsx
import { spring } from "remotion";

const scale = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 100 },
});
```

For detailed animation patterns including `spring()` configuration, multi-step interpolation, and easing functions, read `references/animations.md`.

### Step 4: Add Multi-Scene Timeline

Use `<Sequence>` to compose multiple scenes on a timeline:

```tsx
import { Sequence, AbsoluteFill } from "remotion";

export const MyVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Sequence durationInFrames={180}>
        <IntroScene />
      </Sequence>
      <Sequence from={180} durationInFrames={600}>
        <MainContent />
      </Sequence>
      <Sequence from={780} durationInFrames={120}>
        <OutroScene />
      </Sequence>
    </AbsoluteFill>
  );
};
```

Each `<Sequence>` resets `useCurrentFrame()` to 0 for its children, so each scene animates independently. The `from` prop sets when the scene starts on the parent timeline.

### Step 5: Render Video

**Preview in browser:**

```bash
npx remotion preview src/index.ts
```

**Render locally:**

```bash
npx remotion render src/index.ts MyVideo out/video.mp4
```

**Render with custom props:**

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 --props='{"title":"Hello"}'
```

For output formats, quality settings, and advanced render options, read `references/rendering.md`.

For AWS Lambda rendering at scale, read `references/lambda.md`.

See `tools/integrations/remotion.md` for the full CLI command reference.

## Key Rules

1. **Version pinning** -- All `@remotion/*` packages must be the same version. Never update one independently. See `tools/integrations/remotion.md` for details.
2. **Deterministic rendering** -- Never use `Math.random()`. Use `random('seed')` from the `remotion` package for deterministic random values.
3. **FPS from config** -- Always get fps from `useVideoConfig()`. Never hardcode fps values in animation calculations.
4. **Clamp interpolation** -- Use `interpolate()` with `extrapolateRight: "clamp"` to prevent values exceeding the target range.
5. **Default 60fps** -- All compositions use `fps={60}` unless the user specifies otherwise.

## Output Format

Deliver a working Remotion project with:

1. **`src/Root.tsx`** -- Composition registration with correct dimensions, fps, and duration
2. **Scene components** -- One `.tsx` file per scene with animations
3. **Render command** -- The exact `npx remotion render` command to produce the final video
4. **Preview command** -- `npx remotion preview src/index.ts` for browser preview

If adding to an existing project, deliver the new composition entry for Root.tsx and the new scene component files.

## Related Skills

- **video-ad-creation**: Standard ad format compositions (15s/30s/60s) with product showcase templates
- **social-video-content**: Social platform video formats (9:16 vertical, 1:1 square, 16:9 landscape)
