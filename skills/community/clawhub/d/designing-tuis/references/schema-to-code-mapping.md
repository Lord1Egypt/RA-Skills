# Schema → Code Mapping Reference

Reference for converting `.tui` Schema files to framework-specific code. Used in the **advanced route** (Screenshot → .tui Schema → Code) when multi-framework output or design asset persistence is needed.

## Overview

```
              .tui Schema (JSON)
                     │
         ┌───────────┼───────────┬───────────┐
         ↓           ↓           ↓           ↓
  ┌─────────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐
  │ BubbleTea   │ │  Ink   │ │ Textual  │ │ Ratatui  │
  │ (Go)        │ │ (JSX)  │ │ (Python) │ │ (Rust)   │
  └─────────────┘ └────────┘ └──────────┘ └──────────┘
```

## Conversion Steps

### Step 1: Parse and Validate

- Read `.tui` file, verify `{ version, meta, tree }` structure
- Validate all node `component` types are in the supported list (see `components-cheatsheet.md`)
- Validate `props` / `layout` / `style` field placement (refer to cheatsheet defaults)

### Step 2: Node Mapping

Each `.tui` node maps to a target framework code snippet:

| .tui Component | BubbleTea (Go) | Ink (React JSX) | Textual (Python) | Ratatui (Rust) | Ratatui (Rust) |
|----------------|----------------|-----------------|------------------|----------------|----------------|
| Box | `lipgloss.NewStyle().Border(...)` + child layout | `<Box borderStyle="single">` | `Container(border=True)` | `Block::default().borders(Borders::ALL)` | `Block::default().borders(Borders::ALL)` |
| Text | `lipgloss.NewStyle().Render(content)` | `<Text>{content}</Text>` | `Static(content)` | `Paragraph::new(content)` | `Paragraph::new(content)` |
| Heading | `lipgloss.NewStyle().Bold(true).Render(content)` | `<Text bold>{content}</Text>` | `Static(content, classes="heading")` | `Paragraph::new(content).style(Style::new().add_modifier(Modifier::BOLD))` |
| Paragraph | `lipgloss.NewStyle().Width(w).Render(content)` | `<Text wrap="wrap">{content}</Text>` | `Static(content, classes="paragraph")` | `Paragraph::new(content).wrap(Wrap { trim: true })` |
| List | `list.Model` (bubbles) | `<SelectInput items={...}>` | `ListView(...)` | `List::new(items)` |
| Table | `table.Model` (bubbles) | `<Table data={...}>` | `DataTable(...)` | `Table::new(rows, cols)` |
| Tree | custom tree model | `<Tree data={...}>` | `Tree(...)` | custom `Tree` widget or `tui-tree-widget` crate |
| Input | `textinput.Model` (bubbles) | `<TextInput value={...}>` | `Input(placeholder=...)` | `Input::default()` (from `ratatui-widgets`) or `tui-textarea` |
| PasswordInput | `textinput.Model` with `EchoMode` | `<TextInput mask="*">` | `Input(password=True)` | `Input::default().mask('*')` |
| Select | `list.Model` with single select | `<SelectInput>` | `Select(...)` | `List::new(items).highlight_style(...)` |
| Checkbox | custom checkbox model | `<Checkbox>` | `Checkbox(label=...)` | custom toggle with `[]` / `[x]` + `Paragraph` |
| RadioGroup | custom radio model | `<RadioGroup>` | `RadioSet(...)` | custom with `()` / `(•)` + `Paragraph` |
| Slider | custom slider model | `<Slider>` | `Slider(min=..., max=...)` | custom with `Gauge` or `LineGauge` |
| Tabs | custom tab component | `<Tabs>` (ink-tab) | `TabbedContent(...)` | `Tabs::new(titles)` |
| Breadcrumb | `strings.Join(items, separator)` | `<Text>{items.join(sep)}</Text>` | `Static(breadcrumb_str)` | `Paragraph::new(items.join(" > "))` |
| ProgressBar | `progress.Model` (bubbles) | `<ProgressBar percent={...}>` | `ProgressBar(...)` | `Gauge::default().percent(ratio)` |
| Divider | `strings.Repeat("─", width)` | `<Box borderBottom>` | `Rule()` | `Line::from("─".repeat(width))` or custom border |
| Modal | overlay rendering logic | `<Box position="absolute">` | `Screen(modal=True)` | overlay with `Clear` + centered `Block` |
| Toast | timed overlay message | `<Box><Text>{msg}</Text></Box>` | `notify(message)` | timed overlay with `Popup` or custom widget |
| Grid | manual column layout in `View()` | `<Box flexDirection="row" flexWrap="wrap">` | `Grid(...)` | `Layout::default().constraints([...])` + `split()` |

### Step 3: Proportion Mapping

Map `.tui` size annotations to framework-native layout mechanisms:

| Proportion Type | BubbleTea (Go) | Ink (React) | Textual (Python) | Ratatui (Rust) |
|-----------------|----------------|-------------|------------------|----------------|
| Fixed N cols/rows | `lipgloss.Width(N)` / `lipgloss.Height(N)` | `<Box width={N}>` | `min-width: N` | `Constraint::Length(N)` or `Constraint::Min(N)` |
| Percentage | `lipgloss.Width(totalW * pct / 100)` | `<Box width="30%">` | `width: 30%` or `fr` units | `Constraint::Percentage(pct)` |
| Fill remaining | `lipgloss.Width(remaining)` | `<Box flexGrow={1}>` | `width: 1fr` | `Constraint::Min(0)` or `Constraint::Percentage(100)` in remaining area |
| Min size | `max(calculated, minW)` | `<Box minWidth={20}>` | `min-width: 20` | `Constraint::Min(minW)` |

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

**Ratatui (Rust):**
- Layout system via `Layout::default().constraints([...])` + `split(area)`
- `Constraint::Length(N)` for fixed, `Constraint::Percentage(pct)` for percentage, `Constraint::Min(N)` for fill/min
- No native CSS-like model — constraints are resolved per-frame in `draw()`
- Pattern: define constraints once, call `layout.split(area)` in each `draw()` call, then render widgets into the resulting `Rect`s

### Step 4: Style Mapping

#### Colors

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) | Ratatui (Rust) |
|------------|----------------|-----------|------------------|
| `color: "cyan"` | `lipgloss.Color("6")` or named | `<Text color="cyan">` | `color: cyan;` | `Style::default().fg(Color::Cyan)` |
| `color: "primary"` | theme lookup → ANSI color | `<Text color={theme.primary}>` | `color: $primary;` | theme lookup → `Style::default().fg(theme.primary)` |
| `bgColor: "blue"` | `lipgloss.NewStyle().Background(lipgloss.Color("4"))` | `<Text backgroundColor="blue">` | `background: blue;` | `Style::default().bg(Color::Blue)` |

#### Text Styles

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) | Ratatui (Rust) |
|------------|----------------|-----------|------------------|
| `bold: true` | `.Bold(true)` | `<Text bold>` | `text-style: bold;` | `.add_modifier(Modifier::BOLD)` |
| `dim: true` | `.Faint(true)` | `<Text dimColor>` | `text-style: italic;` or `opacity: 0.6` | `.add_modifier(Modifier::DIM)` |
| `underline: true` | `.Underline(true)` | `<Text underline>` | `text-decoration: underline;` | `.add_modifier(Modifier::UNDERLINED)` |

#### Borders

| .tui style | BubbleTea (Go) | Ink (JSX) | Textual (Python) | Ratatui (Rust) |
|------------|----------------|-----------|------------------|
| `border: true, borderStyle: "single"` | `lipgloss.NormalBorder()` | `<Box borderStyle="single">` | `border: solid;` | `Borders::ALL` with default single-line border |
| `border: true, borderStyle: "double"` | `lipgloss.DoubleBorder()` | `<Box borderStyle="double">` | `border: double;` | `Borders::ALL` with custom double-line `Set` from `border::DOUBLE` |
| `border: true, borderStyle: "rounded"` | `lipgloss.RoundedBorder()` | `<Box borderStyle="round">` | `border: round;` | `Borders::ALL` with `Set` from `border::ROUNDED` |
| `border: false` | no border style | `<Box>` (no border prop) | `border: none;` | `Borders::NONE` |

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

#### Ratatui (Rust) Boilerplate

```rust
use crossterm::event::{self, Event, KeyCode};
use ratatui::{
    backend::Backend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, Paragraph, Clear},
    Frame, Terminal,
};
use std::io;

struct App {
    // ... component state
}

impl App {
    fn new() -> Self {
        Self { /* ... */ }
    }

    fn draw<B: Backend>(&mut self, frame: &mut Frame<B>) {
        let area = frame.size();
        // ... layout with Layout::default().constraints([...]).split(area)
        // ... render widgets into rects
    }

    fn run<B: Backend>(mut self, terminal: &mut Terminal<B>) -> io::Result<()> {
        loop {
            terminal.draw(|f| self.draw(f))?;
            if let Event::Key(key) = event::read()? {
                match key.code {
                    KeyCode::Char('q') | KeyCode::Esc => return Ok(()),
                    _ => {}
                }
            }
        }
    }
}

fn main() -> io::Result<()> {
    crossterm::terminal::enable_raw_mode()?;
    let mut terminal = Terminal::new(ratatui::backend::CrosstermBackend::new(io::stdout()))?;
    let app = App::new();
    let result = app.run(&mut terminal);
    crossterm::terminal::disable_raw_mode()?;
    result
}
```

## Rendering Stability Requirements

Generated code must follow these rules to prevent visual artifacts:

| Requirement | BubbleTea | Ink | Textual | Ratatui |
|-------------|-----------|-----|---------|---------|
| Full-screen redraw | `View()` returns complete frame | React reconciler handles | Compositor handles | `Frame::render_widget` draws to full buffer each frame |
| Clear on resize | Re-render after `WindowSizeMsg` | Automatic | Automatic | Re-draw on `Resize` event; buffer auto-cleared |
| Alternate screen | `tea.WithAltScreen()` | Default behavior | Default behavior | Use `terminal.enter_alternate_screen()?` |
| Hide cursor | Handled by framework | Handled by framework | Handled by framework | `terminal.hide_cursor()?` or `Frame::set_cursor` |
| Character width | Use `runewidth` for CJK | Use `string-width` | Use `wcwidth` | `ratatui` uses `unicode-width` crate internally |

## When to Use This Reference

- **Advanced route only**: when generating code from an existing `.tui` Schema file
- **Multi-framework output**: generating the same design for multiple target frameworks
- **Design asset workflow**: `.tui` files are the versioned source of truth, code is derived

For the **default route** (Screenshot → Code directly), this mapping informs the code generation but the LLM generates framework code directly without an intermediate `.tui` file.
