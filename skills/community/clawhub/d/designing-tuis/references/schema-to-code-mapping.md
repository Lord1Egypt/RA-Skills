# Schema → Code Mapping Reference

Reference for converting `.tui` Schema files to framework-specific code. Used in the **advanced route** (Screenshot → .tui Schema → Code) when multi-framework output or design asset persistence is needed.

## Overview

```
              .tui Schema (JSON)
                     │
         ┌───────────┼───────────┐
         ↓           ↓           ↓
  ┌─────────────┐ ┌────────┐ ┌──────────┐
  │ BubbleTea   │ │  Ink   │ │ Textual  │
  │ (Go)        │ │ (JSX)  │ │ (Python) │
  └─────────────┘ └────────┘ └──────────┘
```

## Conversion Steps

### Step 1: Parse and Validate

- Read `.tui` file, verify `{ version, meta, tree }` structure
- Validate all node `component` types are in the supported list (see `components-cheatsheet.md`)
- Validate `props` / `layout` / `style` field placement (refer to cheatsheet defaults)

### Step 2: Node Mapping

Each `.tui` node maps to a target framework code snippet:

| .tui Component | BubbleTea (Go) | Ink (React JSX) | Textual (Python) |
|----------------|----------------|-----------------|------------------|
| Box | `lipgloss.NewStyle().Border(...)` + child layout | `<Box borderStyle="single">` | `Container(border=True)` |
| Text | `lipgloss.NewStyle().Render(content)` | `<Text>{content}</Text>` | `Static(content)` |
| Heading | `lipgloss.NewStyle().Bold(true).Render(content)` | `<Text bold>{content}</Text>` | `Static(content, classes="heading")` |
| Paragraph | `lipgloss.NewStyle().Width(w).Render(content)` | `<Text wrap="wrap">{content}</Text>` | `Static(content, classes="paragraph")` |
| List | `list.Model` (bubbles) | `<SelectInput items={...}>` | `ListView(...)` |
| Table | `table.Model` (bubbles) | `<Table data={...}>` | `DataTable(...)` |
| Tree | custom tree model | `<Tree data={...}>` | `Tree(...)` |
| Input | `textinput.Model` (bubbles) | `<TextInput value={...}>` | `Input(placeholder=...)` |
| PasswordInput | `textinput.Model` with `EchoMode` | `<TextInput mask="*">` | `Input(****** |
| Select | `list.Model` with single select | `<SelectInput>` | `Select(...)` |
| Checkbox | custom checkbox model | `<Checkbox>` | `Checkbox(label=...)` |
| RadioGroup | custom radio model | `<RadioGroup>` | `RadioSet(...)` |
| Slider | custom slider model | `<Slider>` | `Slider(min=..., max=...)` |
| Tabs | custom tab component | `<Tabs>` (ink-tab) | `TabbedContent(...)` |
| Breadcrumb | `strings.Join(items, separator)` | `<Text>{items.join(sep)}</Text>` | `Static(breadcrumb_str)` |
| ProgressBar | `progress.Model` (bubbles) | `<ProgressBar percent={...}>` | `ProgressBar(...)` |
| Divider | `strings.Repeat("─", width)` | `<Box borderBottom>` | `Rule()` |
| Modal | overlay rendering logic | `<Box position="absolute">` | `Screen(modal=True)` |
| Toast | timed overlay message | `<Box><Text>{msg}</Text></Box>` | `notify(message)` |
| Grid | manual column layout in `View()` | `<Box flexDirection="row" flexWrap="wrap">` | `Grid(...)` |

### Step 3: Proportion Mapping

Map `.tui` size annotations to framework-native layout mechanisms:

| Proportion Type | BubbleTea (Go) | Ink (React) | Textual (Python) |
|-----------------|----------------|-------------|------------------|
| Fixed N cols/rows | `lipgloss.Width(N)` / `lipgloss.Height(N)` | `<Box width={N}>` | `min-width: N` |
| Percentage | `lipgloss.Width(totalW * pct / 100)` | `<Box width="30%">` | `width: 30%` or `fr` units |
| Fill remaining | `lipgloss.Width(remaining)` | `<Box flexGrow={1}>` | `width: 1fr` |
| Min size | `max(calculated, minW)` | `<Box minWidth={20}>` | `min-width: 20` |

#### Framework-Specific Proportion Notes

**BubbleTea (Go):**
- No native percentage/flex — compute absolute values in `Update()` from `tea.WindowSizeMsg`
- Pattern: store `windowWidth`/`windowHeight` in model, recalculate child sizes on resize
- Fixed sizes: `lipgloss.Width(N)` / `lipgloss.Height(N)` directly
- Fill: `totalWidth - fixedChildrenWidth`

**Ink (React/JSX):**
- Native flexbox: `flexGrow`, `flexShrink`, `flexBasis` directly available
- Percentages: `width="30%"` works natively
- Min/max: `minWidth`, `maxWidth`, `minHeight`, `maxHeight` supported
- Responsive by default via flexbox model

**Textual (Python):**
- CSS grid with `fr` units for proportional allocation
- Percentages: `width: 30%` in CSS
- Min/max: `min-width`, `max-width`, `min-height`, `max-height` in CSS
- Responsive by default via CSS model

### Step 4: Style Mapping

#### Colors

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) |
|------------|----------------|-----------|------------------|
| `color: "cyan"` | `lipgloss.Color("6")` or named | `<Text color="cyan">` | `color: cyan;` |
| `color: "primary"` | theme lookup → ANSI color | `<Text color={theme.primary}>` | `color: $primary;` |
| `bgColor: "blue"` | `lipgloss.NewStyle().Background(lipgloss.Color("4"))` | `<Text backgroundColor="blue">` | `background: blue;` |

#### Text Styles

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) |
|------------|----------------|-----------|------------------|
| `bold: true` | `.Bold(true)` | `<Text bold>` | `text-style: bold;` |
| `dim: true` | `.Faint(true)` | `<Text dimColor>` | `text-style: italic;` or `opacity: 0.6` |
| `underline: true` | `.Underline(true)` | `<Text underline>` | `text-decoration: underline;` |

#### Borders

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) |
|------------|----------------|-----------|------------------|
| `border: true, borderStyle: "single"` | `lipgloss.NormalBorder()` | `<Box borderStyle="single">` | `border: solid;` |
| `border: true, borderStyle: "double"` | `lipgloss.DoubleBorder()` | `<Box borderStyle="double">` | `border: double;` |
| `border: true, borderStyle: "rounded"` | `lipgloss.RoundedBorder()` | `<Box borderStyle="round">` | `border: round;` |
| `border: false` | no border style | `<Box>` (no border prop) | `border: none;` |

### Step 5: Assembly and Output

#### BubbleTea (Go) Boilerplate

```go
package main

import (
    "fmt"
    "os"

    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type model struct {
    width  int
    height int
    // ... component state
}

func (m model) Init() tea.Cmd {
    return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
    case tea.KeyMsg:
        if msg.String() == "q" || msg.String() == "ctrl+c" {
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m model) View() string {
    // ... render layout using lipgloss
    return ""
}

func main() {
    p := tea.NewProgram(model{}, tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
}
```

#### Ink (React/JSX) Boilerplate

```jsx
import React, { useState } from 'react';
import { render, Box, Text, useInput, useApp } from 'ink';

const App = () => {
  const { exit } = useApp();

  useInput((input, key) => {
    if (input === 'q' || (key.ctrl && input === 'c')) {
      exit();
    }
  });

  return (
    <Box flexDirection="column" width="100%" height="100%">
      {/* ... layout */}
    </Box>
  );
};

render(<App />);
```

#### Textual (Python) Boilerplate

```python
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Header, Footer

class TUIApp(App):
    CSS = """
    /* ... layout styles */
    """

    def compose(self) -> ComposeResult:
        yield Header()
        # ... widget tree
        yield Footer()

    def on_key(self, event) -> None:
        if event.key == "q":
            self.exit()

if __name__ == "__main__":
    app = TUIApp()
    app.run()
```

## Rendering Stability Requirements

Generated code must follow these rules to prevent visual artifacts:

| Requirement | BubbleTea | Ink | Textual |
|-------------|-----------|-----|---------|
| Full-screen redraw | `View()` returns complete frame | React reconciler handles | Compositor handles |
| Clear on resize | Re-render after `WindowSizeMsg` | Automatic | Automatic |
| Alternate screen | `tea.WithAltScreen()` | Default behavior | Default behavior |
| Hide cursor | Handled by framework | Handled by framework | Handled by framework |
| Character width | Use `runewidth` for CJK | Use `string-width` | Use `wcwidth` |

## When to Use This Reference

- **Advanced route only**: when generating code from an existing `.tui` Schema file
- **Multi-framework output**: generating the same design for multiple target frameworks
- **Design asset workflow**: `.tui` files are the versioned source of truth, code is derived

For the **default route** (Screenshot → Code directly), this mapping informs the code generation but the LLM generates framework code directly without an intermediate `.tui` file.
