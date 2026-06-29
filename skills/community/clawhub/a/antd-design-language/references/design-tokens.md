# Ant Design v5 — Design Tokens & Theming

v5's biggest shift: the design language is encoded as **design tokens** in a **CSS-in-JS** runtime,
not a static Less stylesheet. This is the technical expression of the **Growing** and **Certainty**
values — one source of truth that the system re-derives into a whole theme.

## The three-layer token architecture

A **derivation pipeline**, not just naming buckets:

```
Seed Token  ──(algorithm)──►  Map Token  ──(semantic mapping)──►  Alias Token
 design intent                 scales/gradients                    component-facing
```

### 1. Seed Tokens — the origin of all design intent

A tiny set of root decisions. Change a seed → the algorithm recomputes everything downstream.

| Seed | Default | Controls |
| --- | --- | --- |
| `colorPrimary` | `#1677FF` | brand color → whole primary palette |
| `colorSuccess` / `colorWarning` / `colorError` / `colorInfo` | `#52C41A` / `#FAAD14` / `#FF4D4F` / `#1677FF` | status palettes |
| `colorTextBase` | `#000` | text colors (derived at opacities) |
| `colorBgBase` | `#FFF` | background colors |
| `fontSize` | `14` | the type scale |
| `borderRadius` | `6` | all radii |
| `sizeUnit` | `4` | base spacing unit |
| `sizeStep` | `4` | spacing increment |
| `wireframe` | `false` | flat/wireframe rendering toggle |
| `motion` | `true` | enable/disable animation |

### 2. Map Tokens — algorithmic scales derived from seeds

Gradient variables computed from seeds: the **10-step color palettes** (`colorPrimaryBg`,
`colorPrimaryHover`, `colorPrimaryActive`, `colorPrimaryBorder`…), the **size scale**
(`sizeXXS…sizeXXL`), the **font-size scale** (`fontSizeSM…fontSizeHeading1`), radius steps, etc.
You rarely set these directly — they're the algorithm's output.

### 3. Alias Tokens — semantic, component-facing

Convenience aliases mapped from Map tokens, used by components in bulk: `colorLink`,
`colorTextDisabled`, `colorBgContainer`, `colorBorder`, `controlHeight`, `boxShadowSecondary`,
`colorTextHeading`. Override an alias to restyle *many* components at once.

> **Mental model:** set **seeds** to change the *brand*; tweak **aliases** to change *behavior across
> components*; override **component tokens** (below) for one component only.

## The three algorithms

Algorithms transform seeds → maps. They're **combinable**:

| Algorithm | Effect |
| --- | --- |
| `theme.defaultAlgorithm` | standard light theme |
| `theme.darkAlgorithm` | dark theme (re-derives the whole tree) |
| `theme.compactAlgorithm` | denser sizing/spacing for data-heavy enterprise screens |

```ts
// dark + compact together
import { theme } from 'antd'
const algorithm = [theme.darkAlgorithm, theme.compactAlgorithm]
```

*Why this matters:* dark mode and compact mode are **free and consistent** — you don't maintain a
separate stylesheet, so they can't drift. That's **Certainty** + **Growing** in code.

## Theming with `ConfigProvider`

Global theme:

```tsx
import { ConfigProvider, theme } from 'antd'

export default function App({ children }) {
  return (
    <ConfigProvider
      theme={{
        // 1) algorithm(s)
        algorithm: theme.defaultAlgorithm,        // or [darkAlgorithm, compactAlgorithm]
        // 2) seed overrides → re-derive the system
        token: {
          colorPrimary: '#1677FF',
          borderRadius: 6,
          fontSize: 14,
        },
        // 3) per-component overrides (component tokens) — scoped, don't leak
        components: {
          Button: { controlHeight: 36, primaryShadow: 'none' },
          Table:  { headerBg: '#F5F7FA', borderColor: '#EEE' },
        },
      }}
    >
      {children}
    </ConfigProvider>
  )
}
```

### Nesting & scoping

`ConfigProvider` nests — wrap a subtree to theme just that area (e.g., a marketing banner inside an
admin app). Inner providers inherit + override outer ones. This supports **modular growth** without a
global rewrite.

### Reading tokens in your own components

```tsx
import { theme } from 'antd'
const { useToken } = theme
function MyBox() {
  const { token } = useToken()
  return <div style={{ padding: token.padding, borderRadius: token.borderRadius,
                       color: token.colorTextSecondary, background: token.colorBgContainer }} />
}
```

*Always consume tokens instead of hardcoding hex/px* — that's how your custom UI stays consistent
with antd and inherits dark/compact themes automatically (**Repetition / Certainty**).

## Static vs runtime, SSR, and migration notes

- **CSS-in-JS** (default) enables runtime theming (live brand-color switching) but adds a style
  runtime; for **SSR**, extract critical CSS with `@ant-design/cssinjs` (`StyleProvider` +
  `extractStyle`) to avoid FOUC.
- For zero-runtime needs, antd offers a **CSS variable** mode (`cssVar: true`) — tokens become CSS
  custom properties, smaller and themeable via `:root`.
- Migrating from **v4 Less variables** (`@primary-color`) → v5 tokens (`colorPrimary`): there's no
  Less override anymore; map old variables to tokens. (And the brand color changed `#1890FF → #1677FF`.)

## Practical theming recipes

- **Re-brand:** set `token.colorPrimary` to the brand hex; the algorithm builds matching
  hover/active/bg/border steps. Don't hand-pick those.
- **Denser admin:** add `compactAlgorithm`; optionally lower `controlHeight` alias.
- **Rounded/sharp:** set `borderRadius` seed (e.g., `2` for sharp enterprise, `8` for friendly).
- **Dark toggle:** swap `algorithm` between `defaultAlgorithm` and `darkAlgorithm` from state.
- **One-off component look:** use `components.{Comp}` tokens, not global overrides — keeps blast
  radius small (**Tesler's Law**: absorb complexity locally, not system-wide).

See `assets/theme.example.ts` for a copy-paste theme covering brand + light/dark/compact + a couple
of component overrides.
