# Adding a New Composition

## Overview

A composition = one Remotion visual style + registry metadata that describes what shots to search for.

Adding a new composition requires changes in two places:
1. `src/skill/registry.ts` — shot slots + props builder
2. `src/remotion/` — the actual Remotion React component + registration in `Root.tsx`

## Step 1: Define the Composition in registry.ts

Add a new `CompositionMeta` object and append it to `REGISTRY`:

```typescript
const myCompositionMeta: CompositionMeta = {
  id:          'MyComposition',      // Must match Remotion composition id exactly
  label:       'My Label',           // Shown in CLI and LLM selection
  description: 'One-line description for LLM to choose this over others',
  musicStyle:  'jazz upbeat background cinematic',  // English, passed to yt-dlp search

  shotSlots: [
    // Each slot = one shot searched + one clip in final video
    { query: '搜索词 or English query', mood: 'calm', extra: { caption: 'Title text', location: 'Place' } },
    { query: 'second shot query',       mood: 'fast', extra: { caption: 'Second text' } },
    // ... add as many slots as needed
  ],

  buildProps(clips, title, bgm, showAttribution = true) {
    return {
      fps: 30,
      title,
      bgm,
      attribution: showAttribution ? 'ShotAI 检索 · Remotion 合成' : undefined,
      clips: clips.map(c => ({
        src:       c.src,
        startTime: c.startTime,
        endTime:   c.endTime,
        summary:   c.summary,
        caption:   c.caption ?? '',    // match whatever fields your Remotion component expects
      })),
    };
  },
};

export const REGISTRY: CompositionMeta[] = [
  // ... existing entries ...
  myCompositionMeta,   // add here
];
```

### ShotSlot fields

| Field | Type | Purpose |
|-------|------|---------|
| `query` | string | Natural language search sent to ShotAI |
| `mood` | string? | Expected mood for shot scoring: `'fast'` `'slow'` `'calm'` `'urban'` |
| `extra` | object? | Static fields merged into each clip (e.g. `caption`, `cityName`, `location`) |

### ClipAnnotation fields (set by LLM annotateClips)

These can override or supplement `extra` fields at runtime:

| Field | Type | Used by |
|-------|------|---------|
| `tone` | `'warm'\|'cool'` | SwitzerlandScenic, any color-graded comp |
| `dramatic` | boolean | SportsHighlight (triggers slow-mo effect) |
| `kenBurns` | `'zoom-in'\|'zoom-out'\|'pan-left'\|'pan-right'` | NatureWild |
| `caption` | string | Any comp with text overlay |
| `textBg` | `Record<string,'light'\|'dark'>` | Auto-set by keyframe brightness analysis |

## Step 2: Create the Remotion Component

Create `src/remotion/compositions/MyComposition.tsx`. Use an existing composition as reference (e.g. copy `TravelVlog.tsx` and adapt).

Key points:
- Accept `clips`, `title`, `bgm`, and any custom fields in props
- Use `<Video>` from `remotion` for each clip, positioned with `<Sequence>`
- Duration is computed in `Root.tsx` based on clip durations

## Step 3: Register in Root.tsx

In `src/remotion/Root.tsx`, add:

```typescript
import { MyComposition } from './compositions/MyComposition';

// Inside the registerRoot callback, add:
<Composition
  id="MyComposition"
  component={MyComposition}
  durationInFrames={totalFrames}   // calculate from clips
  fps={30}
  width={1920}
  height={1080}
  defaultProps={defaultProps}
/>
```

Refer to how other compositions are registered for the exact pattern.

## Step 4: Test

```bash
# Test with heuristic mode (no LLM needed)
AGENT_PROVIDER=none npx tsx src/skill/cli.ts "test" --composition MyComposition

# Preview in Remotion Studio
npm run studio
```
