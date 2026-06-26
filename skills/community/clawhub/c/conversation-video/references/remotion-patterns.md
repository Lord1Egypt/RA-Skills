# Remotion Patterns Reference

Quick patterns for building richer conversation videos with Remotion.

## Table of Contents
1. Loading transcript from JSON
2. Loading audio and syncing
3. Word-by-word reveal
4. Auto-scaling text
5. Export / render commands

---

## 1. Loading transcript from JSON

Place `data/conversation.json` next to your src folder:

```json
[
  {"speaker": "Alice", "text": "Hello", "duration": 60},
  {"speaker": "Bob",   "text": "Hi there", "duration": 45}
]
```

```tsx
import { getVideoMetadata } from "@remotion/media-utils";

const data = require("../data/conversation.json");
```

## 2. Audio sync

Put audio in `public/audio.wav`, then:

```tsx
import { Audio, staticFile } from "remotion";

// In your main component:
<Audio src={staticFile("audio.wav")} />
```

Derive `durationInFrames` from audio duration:

```tsx
import { getVideoMetadata } from "@remotion/media-utils";

const metadata = await getVideoMetadata(staticFile("audio.wav"));
const durationInFrames = Math.ceil(metadata.durationInSeconds * 30);
```

## 3. Word-by-word reveal

Split text into words and fade each in:

```tsx
const words = text.split(" ");
words.map((word, wi) => {
  const wordStart = start + wi * 5;
  const opacity = interpolate(frame, [wordStart, wordStart + 4], [0, 1]);
  return <span key={wi} style={{ opacity }}>{word} </span>;
});
```

## 4. Auto-scale text to fit bubble

Measure text width with a helper, scale down font-size if it exceeds max.

## 5. Render

```bash
npx remotion render src/index.ts Conversation out/video.mp4
```

Preview in studio:
```bash
npx remotion studio src/index.ts
```
