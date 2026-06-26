# Remotion Animation Patterns

Detailed animation reference covering interpolation, spring physics, easing, and transition effects.

## interpolate()

Maps a frame number to an animated value. The core animation primitive in Remotion.

### Basic Usage

```tsx
import { useCurrentFrame, interpolate } from "remotion";

const frame = useCurrentFrame();

// Fade in over frames 0-30
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});
```

### Parameters

```tsx
interpolate(
  input,        // Current value (usually frame number)
  inputRange,   // Array of input breakpoints [0, 30, 60]
  outputRange,  // Array of output values [0, 1, 0]
  options       // Optional configuration
)
```

### Extrapolation Options

Control what happens when the input is outside the defined range:

| Option | Value | Behavior |
|--------|-------|----------|
| `extrapolateLeft` | `"clamp"` | Clamp to first output value |
| `extrapolateLeft` | `"extend"` | Continue the curve (default) |
| `extrapolateLeft` | `"identity"` | Return input as-is |
| `extrapolateLeft` | `"wrap"` | Wrap around the range |
| `extrapolateRight` | `"clamp"` | Clamp to last output value |
| `extrapolateRight` | `"extend"` | Continue the curve (default) |
| `extrapolateRight` | `"identity"` | Return input as-is |
| `extrapolateRight` | `"wrap"` | Wrap around the range |

**Best practice:** Always use `extrapolateRight: "clamp"` unless you specifically want values to exceed the output range.

### Multi-Step Interpolation

Use multiple breakpoints for complex animations:

```tsx
// Fade in, hold, then fade out
const opacity = interpolate(
  frame,
  [0, 30, 60, 90],   // Four breakpoints
  [0, 1, 1, 0],      // Corresponding values
  { extrapolateRight: "clamp" }
);

// Slide in from left, hold, slide out to right
const translateX = interpolate(
  frame,
  [0, 30, 120, 150],
  [-500, 0, 0, 500],
  { extrapolateRight: "clamp" }
);
```

### Using with Easing

Apply easing functions for non-linear motion:

```tsx
import { interpolate, Easing } from "remotion";

const opacity = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  extrapolateRight: "clamp",
});
```

## spring()

Physics-based animation for natural motion. Ideal for scale, position, and bounce effects.

### Basic Usage

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
  config: {
    damping: 12,
    stiffness: 100,
    mass: 1,
  },
});
```

**Always** get `fps` from `useVideoConfig()` -- never hardcode it.

### Configuration Options

| Option | Default | Effect |
|--------|---------|--------|
| `damping` | 10 | Higher = less oscillation. Range: 0-100 |
| `stiffness` | 100 | Higher = faster snap. Range: 0-500 |
| `mass` | 1 | Higher = heavier, slower. Range: 0.1-10 |
| `overshootClamping` | false | If true, stops at target without overshoot |

### Common Presets

```tsx
// Snappy entrance (no bounce)
spring({ frame, fps, config: { damping: 20, stiffness: 200, overshootClamping: true } });

// Bouncy entrance
spring({ frame, fps, config: { damping: 8, stiffness: 150, mass: 0.8 } });

// Slow, heavy entrance
spring({ frame, fps, config: { damping: 15, stiffness: 80, mass: 2 } });

// Gentle settle
spring({ frame, fps, config: { damping: 12, stiffness: 100, mass: 1 } });
```

### Delayed Spring

Use the `delay` parameter to start the spring at a specific frame:

```tsx
const scale = spring({
  frame,
  fps,
  delay: 30,  // Start spring at frame 30
  config: { damping: 12, stiffness: 100 },
});
```

### Duration Override

Override physics simulation with a fixed duration:

```tsx
const value = spring({
  frame,
  fps,
  durationInFrames: 60,  // Complete in exactly 60 frames
  config: { damping: 12, stiffness: 100 },
});
```

## Easing Functions

Import easing functions from `remotion` for use with `interpolate()`:

```tsx
import { Easing } from "remotion";
```

### Common Easing Presets

| Function | Effect |
|----------|--------|
| `Easing.linear` | No easing (default) |
| `Easing.ease` | Smooth ease-in-out |
| `Easing.in(Easing.ease)` | Ease in only |
| `Easing.out(Easing.ease)` | Ease out only |
| `Easing.inOut(Easing.ease)` | Ease in and out |
| `Easing.bezier(x1, y1, x2, y2)` | Custom cubic bezier |

### Custom Bezier Curves

```tsx
// CSS ease equivalent
const easeCSS = Easing.bezier(0.25, 0.1, 0.25, 1);

// Fast start, slow end
const easeOut = Easing.bezier(0, 0, 0.58, 1);

// Slow start, fast end
const easeIn = Easing.bezier(0.42, 0, 1, 1);

// Use with interpolate
const opacity = interpolate(frame, [0, 30], [0, 1], {
  easing: easeCSS,
  extrapolateRight: "clamp",
});
```

## Image Animation Patterns

### Scale + Fade Entrance

```tsx
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
const scale = spring({ frame, fps, config: { damping: 12, stiffness: 100 } });

<img
  src={imageUrl}
  style={{
    opacity,
    transform: `scale(${scale})`,
    width: 400,
    height: 300,
  }}
/>
```

### Slide In from Side

```tsx
const translateX = interpolate(frame, [0, 30], [-600, 0], {
  easing: Easing.out(Easing.ease),
  extrapolateRight: "clamp",
});

<div style={{ transform: `translateX(${translateX}px)` }}>
  <img src={imageUrl} style={{ width: "100%" }} />
</div>
```

### Ken Burns Effect (Slow Zoom + Pan)

```tsx
const scale = interpolate(frame, [0, 300], [1, 1.3], { extrapolateRight: "clamp" });
const translateX = interpolate(frame, [0, 300], [0, -50], { extrapolateRight: "clamp" });

<div style={{ overflow: "hidden", width: 1920, height: 1080 }}>
  <img
    src={imageUrl}
    style={{
      transform: `scale(${scale}) translateX(${translateX}px)`,
      width: "100%",
      height: "100%",
      objectFit: "cover",
    }}
  />
</div>
```

## Text Animation Patterns

### Character-by-Character Reveal

```tsx
const text = "Hello World";
const charsShown = interpolate(frame, [0, 60], [0, text.length], {
  extrapolateRight: "clamp",
});

<h1 style={{ fontSize: 80, color: "white" }}>
  {text.slice(0, Math.round(charsShown))}
</h1>
```

### Typewriter with Cursor

```tsx
const text = "Welcome to Remotion";
const charsShown = Math.round(
  interpolate(frame, [0, 90], [0, text.length], { extrapolateRight: "clamp" })
);
const cursorVisible = frame % 30 < 15; // Blink every 0.5s at 60fps

<h1 style={{ fontSize: 60, color: "white", fontFamily: "monospace" }}>
  {text.slice(0, charsShown)}
  <span style={{ opacity: cursorVisible ? 1 : 0 }}>|</span>
</h1>
```

Note: The cursor blink uses a frame-based modulo, which is deterministic (safe for Remotion rendering).

### Staggered Word Entrance

```tsx
const words = ["Build", "Ship", "Grow"];

{words.map((word, i) => {
  const delay = i * 15; // 15 frames between each word
  const wordOpacity = interpolate(frame, [delay, delay + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wordY = interpolate(frame, [delay, delay + 20], [30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <span
      key={word}
      style={{
        opacity: wordOpacity,
        transform: `translateY(${wordY}px)`,
        display: "inline-block",
        marginRight: 20,
        fontSize: 80,
        color: "white",
      }}
    >
      {word}
    </span>
  );
})}
```

## Deterministic Randomness

**Never use `Math.random()` in Remotion.** It produces different values on each render, breaking deterministic output.

Use the `random()` function from the `remotion` package:

```tsx
import { random } from "remotion";

// Deterministic random value seeded by string
const rotation = random("particle-rotation") * 360;
const xOffset = random("particle-x") * 1920;

// Use index for unique per-item values
{items.map((item, i) => {
  const randomDelay = random(`delay-${i}`) * 30;
  const randomScale = 0.5 + random(`scale-${i}`) * 0.5;
  // ...
})}
```

`random('seed')` returns a number between 0 and 1, deterministic for the same seed string.

## Advanced: TransitionSeries

The `@remotion/transitions` package provides smooth transitions between scenes.

### Installation

```bash
npm install @remotion/transitions
```

Ensure the version matches your other `@remotion/*` packages.

### Fade Transition

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { linearTiming } from "@remotion/transitions";

export const MyVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={300}>
        <SceneA />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />
      <TransitionSeries.Sequence durationInFrames={300}>
        <SceneB />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

### Available Transitions

| Transition | Import | Effect |
|-----------|--------|--------|
| `fade()` | `@remotion/transitions/fade` | Crossfade between scenes |
| `slide()` | `@remotion/transitions/slide` | Slide in from a direction |
| `wipe()` | `@remotion/transitions/wipe` | Wipe from one side |
| `flip()` | `@remotion/transitions/flip` | 3D flip effect |

### Timing Options

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

// Linear timing (fixed duration)
linearTiming({ durationInFrames: 30 })

// Spring-based timing (physics-based)
springTiming({ config: { damping: 12, stiffness: 100 } })
```

The transition duration overlaps the adjacent sequences -- it does not add extra frames to the total timeline.
