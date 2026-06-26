# Color Accessibility for TUI Design

Reference for accessible color usage in terminal user interfaces. Based on WCAG (Web Content Accessibility Guidelines) standards and validated color-blind safe palettes.

## 1. Core Standard: WCAG Color Requirements

### WCAG 1.4.1 — Use of Color (Level A, Minimum)

**Rule:** Color must NOT be the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.

**TUI implications:**
- Status indicators (success/error/warning) must include text labels or distinct symbols, not just color
- Selected/active items must have additional cues: `▸` prefix, `[ ]`/`[x]` markers, reverse video, bold, or border changes
- Navigation state (active tab, current item) must be distinguishable without color: underline, bold, bracket markers

**Examples of compliant design:**

| Scenario | ❌ Color Only | ✅ Color + Additional Cue |
|----------|--------------|--------------------------|
| Error state | Red text | Red text + `✗` icon + "Error:" label |
| Success state | Green text | Green text + `✓` icon + "Done:" label |
| Selected item | Cyan background | Cyan background + `▸` prefix + bold |
| Active tab | Blue underline | Blue + bold + `[Tab Name]` brackets |
| Warning | Yellow text | Yellow text + `⚠` icon + "Warning:" label |

### WCAG 1.4.3 — Contrast (Level AA)

**Rule:** Text and background must have sufficient contrast ratio:
- Normal text: ≥ 4.5:1
- Large text (bold or 18pt+): ≥ 3:1
- Non-text UI elements (borders, icons): ≥ 3:1

**TUI-specific notes:**
- Terminal emulators vary in color rendering — design for worst-case contrast
- `dim` text on dark backgrounds often fails contrast requirements; test against common terminal themes
- Prefer high-contrast pairings: white-on-black, cyan-on-black, yellow-on-black

### Contrast-Safe Text/Background Pairs (Dark Terminal)

| Foreground | Background | Approx. Ratio | Safe? |
|------------|------------|---------------|-------|
| White | Black | ~21:1 | ✅ |
| Cyan | Black | ~8:1 | ✅ |
| Yellow | Black | ~12:1 | ✅ |
| Green | Black | ~6:1 | ✅ |
| Blue | Black | ~3.5:1 | ⚠️ Borderline |
| Red | Black | ~4:1 | ⚠️ Borderline |
| Gray (dim) | Black | ~3:1 | ❌ Below AA for body text |

## 2. Color-Blind Safe Palettes for TUI

### Okabe-Ito Palette (Scientific Gold Standard)

Recommended by Nature and other journals. Covers protanopia (red-blind), deuteranopia (green-blind), and tritanopia (blue-blind).

| Name | Hex | ANSI Approximation | Semantic Use |
|------|-----|--------------------|----|
| Black | `#000000` | `black` | Background, text |
| Orange | `#E69F00` | `yellow` (bright) | Warning, attention |
| Sky Blue | `#56B4E9` | `cyan` | Info, links |
| Bluish Green | `#009E73` | `green` | Success, positive |
| Yellow | `#F0E442` | `yellow` | Highlight, caution |
| Blue | `#0072B2` | `blue` | Primary, navigation |
| Vermilion | `#D55E00` | `red` (bright) | Error, critical |
| Reddish Purple | `#CC79A7` | `magenta` | Accent, special |

### IBM Color Blind Safe Palette

Optimized for enterprise UI, red-green blind and blue-yellow blind safe:

| Name | Hex | ANSI Approximation | Semantic Use |
|------|-----|--------------------|----|
| Blue | `#648FFF` | `blue` (bright) | Primary |
| Purple | `#785EF0` | `magenta` | Secondary |
| Magenta | `#DC267F` | `red` (bright) | Error, danger |
| Orange | `#FE6100` | `yellow` | Warning |
| Yellow | `#FFB000` | `yellow` (bright) | Attention, highlight |

### TUI Semantic Color Mapping (Accessibility-First)

Preferred semantic-to-ANSI mapping that avoids dangerous combinations:

| Semantic | Recommended ANSI | Avoid | Reason |
|----------|-----------------|-------|--------|
| `primary` | `blue` or `cyan` | — | High visibility on dark backgrounds |
| `secondary` | `magenta` | — | Distinguishable from primary |
| `success` | `green` + `✓` symbol | Green alone | Red-green blind cannot distinguish from error by color |
| `error` | `red` + `✗` symbol | Red alone | Red-green blind cannot distinguish from success by color |
| `warning` | `yellow` + `⚠` symbol | Yellow alone | Must have symbol for color-independent meaning |
| `info` | `cyan` + `ℹ` symbol | Blue (low contrast) | Cyan has better contrast on dark backgrounds |
| `muted` | `gray` (avoid dim) | `dim` on dark bg | `dim` often fails contrast requirements |

## 3. Design Principles

### Dangerous Color Combinations (Avoid)

These pairs are commonly confused by color-blind users:

| Pair | Affected Type | Safe Alternative |
|------|---------------|-----------------|
| Red — Green | Protanopia, Deuteranopia (~8% males) | Blue — Orange |
| Green — Brown | Deuteranopia | Blue — Yellow |
| Blue — Purple | Tritanopia | Blue — Orange |
| Light Green — Yellow | Deuteranopia | Cyan — Yellow |
| Blue — Gray | Tritanopia | Blue — White |

### Safe Primary Combinations

| Pair | Why Safe | Best For |
|------|----------|----------|
| Blue — Orange | Distinguishable in all color-blind types | Error/success indicators |
| Black — Orange | High contrast + color-blind safe | Warnings on dark bg |
| Cyan — Yellow | Different luminance + safe | Info/highlight differentiation |
| White — Magenta | High contrast + safe | Active/inactive states |

### Multi-Channel Encoding Principle

Never rely on color alone. Always combine with at least one additional channel:

| Channel | TUI Implementation |
|---------|--------------------|
| Shape/Symbol | Prefix icons: `✓` `✗` `⚠` `ℹ` `▸` `●` `○` |
| Text label | "Error:", "Success:", "Warning:" prefixes |
| Bold/Dim | Bold for emphasis, normal for secondary |
| Reverse video | Inverted bg/fg for selection |
| Border style | Different border for active vs inactive panels |
| Position/Indentation | Selected items indented or prefixed |

### Luminance Differentiation

Color blindness typically does NOT affect brightness perception. When choosing colors:

- Ensure paired colors differ significantly in luminance (brightness)
- Dark blue vs light yellow ✅ (luminance differs)
- Red vs green ❌ (similar luminance in grayscale)
- Test by converting to grayscale — elements should remain distinguishable

## 4. TUI-Specific Implementation Guidelines

### Status Indicators

```
# Compliant status display
✓ Build passed          (green + checkmark + "passed" text)
✗ Tests failed          (red + cross + "failed" text)
⚠ 3 warnings           (yellow + triangle + "warnings" text)
ℹ Running migrations    (cyan + info symbol + description)
```

### List Selection

```
# Compliant list selection (multiple cues)
  Normal item           (white, no prefix)
▸ Selected item         (cyan + bold + prefix arrow)
  Another item          (white, no prefix)
```

### Tab Navigation

```
# Compliant tabs (multiple cues)
 [Files]  Commits   Branches   Tags
  ^bold    ^normal   ^normal   ^normal
  ^cyan    ^gray     ^gray     ^gray
  ^bracket
```

### Data Visualization in TUI

For sparklines, bar charts, or status distributions:
- Use Okabe-Ito or IBM palette colors
- Add value labels next to colored elements
- Use pattern differentiation where possible (░ ▒ ▓ █ for different categories)
- Never use rainbow color schemes

### Progress and Status Bars

```
# Compliant progress bar
[████████░░░░░░░░░░░░] 40% Building...
 ^green     ^gray       ^label (always show percentage + text)
```

## 5. Framework-Specific Color Accessibility

### BubbleTea (Go)

```go
// Use lipgloss adaptive colors for theme compatibility
var (
    successStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("2")).  // green
        Bold(true)
    errorStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("1")).  // red
        Bold(true)
)

// Always pair color with symbol
func renderStatus(ok bool) string {
    if ok {
        return successStyle.Render("✓ Passed")
    }
    return errorStyle.Render("✗ Failed")
}
```

### Ink (React/JSX)

```jsx
// Compliant status component
const Status = ({ type, message }) => (
  <Text color={colorMap[type]} bold>
    {symbolMap[type]} {message}
  </Text>
);

const symbolMap = { success: '✓', error: '✗', warning: '⚠', info: 'ℹ' };
const colorMap = { success: 'green', error: 'red', warning: 'yellow', info: 'cyan' };
```

### Textual (Python)

```python
# Compliant status with CSS classes
class StatusWidget(Static):
    def render(self) -> str:
        symbols = {"success": "✓", "error": "✗", "warning": "⚠", "info": "ℹ"}
        return f"{symbols[self.variant]} {self.message}"

# CSS ensures both color AND bold for status types
# .success { color: green; text-style: bold; }
# .error { color: red; text-style: bold; }
```

## 6. Validation Checklist

Before finalizing any TUI design, verify:

- [ ] No information is conveyed by color alone (WCAG 1.4.1)
- [ ] All status indicators have text labels AND/OR symbols in addition to color
- [ ] Selected/active states have non-color cues (bold, prefix, reverse, border)
- [ ] Text-to-background contrast ≥ 4.5:1 for body text (WCAG 1.4.3)
- [ ] No red-green pairings used as sole differentiator
- [ ] `dim` text verified against target terminal theme for readability
- [ ] Color semantics are consistent throughout the interface
- [ ] Design remains usable in grayscale (luminance test)
