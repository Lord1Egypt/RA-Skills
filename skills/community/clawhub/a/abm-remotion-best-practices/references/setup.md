# Remotion Project Setup

Detailed setup and configuration reference for Remotion projects.

## Scaffolding a New Project

Create a new Remotion project using the official scaffolding tool:

```bash
npx create-video@latest my-video
cd my-video
npm install
```

This creates the standard Remotion project structure with all required dependencies and configuration.

## Directory Structure

A scaffolded Remotion project has this structure:

```
my-video/
  src/
    Root.tsx           # Composition registration (entry point)
    index.ts           # Remotion entry file (registers Root)
    MyComposition.tsx   # Default scene component
  package.json          # Dependencies with @remotion/* packages
  tsconfig.json         # TypeScript configuration
  remotion.config.ts    # Remotion-specific bundler config (optional)
```

### Key Files

**`src/index.ts`** -- The Remotion entry point that registers the root component:

```tsx
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
```

**`src/Root.tsx`** -- Where all compositions are registered:

```tsx
import { Composition } from "remotion";
import { MyScene } from "./MyScene";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"
        component={MyScene}
        durationInFrames={900}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{ title: "My Video" }}
      />
    </>
  );
};
```

Multiple compositions can be registered in the same Root.tsx using a React fragment (`<>...</>`).

## Package Dependencies

### Required Packages

| Package | Purpose |
|---------|---------|
| `remotion` | Core framework (re-exports from @remotion/core) |
| `@remotion/cli` | CLI for rendering and preview |
| `@remotion/bundler` | Webpack bundler for Remotion projects |
| `react` | React (peer dependency) |
| `react-dom` | React DOM (peer dependency) |

### Optional Packages

| Package | Purpose | When to Add |
|---------|---------|-------------|
| `@remotion/player` | Embeddable video player for React apps | Web-based preview or embedding |
| `@remotion/lambda` | Serverless rendering on AWS | Cloud rendering at scale |
| `@remotion/media-utils` | Audio/video duration and metadata | Working with audio or video assets |
| `@remotion/transitions` | Scene transition effects | Smooth transitions between scenes |
| `@remotion/gif` | Animated GIF support | Using GIF assets in compositions |

## Version Pinning

**All `@remotion/*` packages MUST be pinned to the same version.** Mixing versions causes subtle rendering bugs and build failures.

Verify version alignment:

```bash
npm ls | grep remotion
```

If versions are mismatched, update all at once:

```bash
npm install remotion@latest @remotion/cli@latest @remotion/bundler@latest
```

If you use optional packages, include them in the update:

```bash
npm install remotion@latest @remotion/cli@latest @remotion/bundler@latest @remotion/player@latest @remotion/lambda@latest @remotion/media-utils@latest @remotion/transitions@latest
```

**Never** update a single `@remotion` package independently. Always update all of them together.

## TypeScript Configuration

The `tsconfig.json` must include:

```json
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
```

The critical setting is `"jsx": "react-jsx"` -- this enables the modern JSX transform that Remotion v4 requires.

## Adding to an Existing Project

If a Remotion project already exists (detected by `@remotion/core` in `package.json`):

1. **Add a new scene component** in `src/`:

```tsx
// src/NewScene.tsx
import { useCurrentFrame, AbsoluteFill } from "remotion";

export const NewScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ fontSize: 60, color: "white" }}>{text}</h1>
    </AbsoluteFill>
  );
};
```

2. **Register it in `src/Root.tsx`** by adding a new `<Composition>`:

```tsx
import { Composition } from "remotion";
import { NewScene } from "./NewScene";
// ... existing imports

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Existing compositions... */}
      <Composition
        id="NewVideo"
        component={NewScene}
        durationInFrames={600}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{ text: "New Video" }}
      />
    </>
  );
};
```

3. **Render the new composition** by referencing its ID:

```bash
npx remotion render src/index.ts NewVideo out/new-video.mp4
```

## Common Resolutions

| Format | Width | Height | Aspect Ratio | Use Case |
|--------|-------|--------|--------------|----------|
| 1080p Landscape | 1920 | 1080 | 16:9 | Standard video, YouTube |
| 1080p Vertical | 1080 | 1920 | 9:16 | Reels, TikTok, Shorts |
| 1080p Square | 1080 | 1080 | 1:1 | Instagram feed, LinkedIn |
| 4K Landscape | 3840 | 2160 | 16:9 | High-res production |
| 720p Landscape | 1280 | 720 | 16:9 | Fast previews, low bandwidth |
