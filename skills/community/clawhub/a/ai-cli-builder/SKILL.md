---
name: cli-builder
description: >
  Activate this skill whenever a user asks to build, design, or improve a
  command-line interface (CLI) tool. This includes: building CLIs in Node.js
  (Commander, yargs, oclif, Ink), Python (Click, Typer, argparse, Rich),
  Go (cobra, urfave/cli, bubbletea), or Rust (clap), argument parsing and
  validation, interactive prompts and TUI (terminal UI), output formatting
  (tables, colors, progress bars, spinners), configuration file management,
  shell completions, man pages, packaging and distribution (npm, PyPI,
  Homebrew, goreleaser, single-binary builds), plugin systems, and CLI
  testing strategies. Also activate for questions about terminal colors,
  ANSI escape codes, stdin/stdout piping, or cross-platform CLI behavior.
---

# CLI Builder Skill

Build professional command-line tools that users love. Follow the sections
relevant to your current task.

---

## 1. CLI Design Principles

### 1.1 Core rules
1. **Do one thing well** — follow Unix philosophy
2. **Predictable behavior** — no surprises, follow conventions
3. **Helpful errors** — tell the user what went wrong AND how to fix it
4. **Progressive disclosure** — simple by default, powerful with flags
5. **Respect the pipeline** — support stdin/stdout, structured output
6. **Exit codes matter** — 0 = success, 1 = error, 2 = usage error

### 1.2 Command structure conventions
```
tool <command> [subcommand] [flags] [arguments]

# Examples:
git commit -m "message"
docker compose up -d
npm install --save-dev typescript
```

### 1.3 Flag conventions
- Short flags: `-v`, `-f`, `-n 5`
- Long flags: `--verbose`, `--force`, `--count 5`
- Boolean flags: `--verbose` / `--no-verbose`
- Always provide both short and long forms for common flags
- Standard flags every CLI should have: `--help`, `--version`, `--verbose`, `--quiet`

---

## 2. Node.js CLIs

### 2.1 Commander.js (most popular)
```typescript
#!/usr/bin/env node
import { Command } from "commander";
import { version } from "../package.json";

const program = new Command();

program
  .name("mytool")
  .description("My awesome CLI tool")
  .version(version);

program
  .command("init")
  .description("Initialize a new project")
  .argument("<name>", "Project name")
  .option("-t, --template <template>", "Template to use", "default")
  .option("--no-git", "Skip git initialization")
  .action(async (name, options) => {
    console.log(`Creating project: ${name}`);
    console.log(`Template: ${options.template}`);
    console.log(`Git: ${options.git}`);
    // ... implementation
  });

program
  .command("build")
  .description("Build the project")
  .option("-w, --watch", "Watch for changes")
  .option("-o, --outdir <dir>", "Output directory", "dist")
  .action(async (options) => {
    // ... implementation
  });

program.parse();
```

### 2.2 package.json setup
```json
{
  "name": "mytool",
  "version": "1.0.0",
  "bin": {
    "mytool": "./dist/cli.js"
  },
  "type": "module",
  "scripts": {
    "build": "tsup src/cli.ts --format esm",
    "dev": "tsx src/cli.ts"
  }
}
```

### 2.3 Interactive prompts (inquirer / @inquirer/prompts)
```typescript
import { input, select, confirm } from "@inquirer/prompts";

const name = await input({ message: "Project name:" });
const template = await select({
  message: "Choose a template:",
  choices: [
    { name: "Minimal", value: "minimal" },
    { name: "Full", value: "full" },
    { name: "API", value: "api" },
  ],
});
const proceed = await confirm({ message: "Create project?" });
```

---

## 3. Python CLIs

### 3.1 Typer (modern, type-hint based)
```python
import typer
from typing import Optional
from typing_extensions import Annotated

app = typer.Typer(help="My awesome CLI tool")

@app.command()
def init(
    name: str,
    template: Annotated[str, typer.Option("--template", "-t", help="Template")] = "default",
    git: Annotated[bool, typer.Option("--git/--no-git", help="Init git")] = True,
):
    """Initialize a new project."""
    typer.echo(f"Creating project: {name}")
    typer.echo(f"Template: {template}")

@app.command()
def build(
    watch: Annotated[bool, typer.Option("--watch", "-w")] = False,
    outdir: Annotated[str, typer.Option("--outdir", "-o")] = "dist",
):
    """Build the project."""
    if watch:
        typer.echo("Watching for changes...")

if __name__ == "__main__":
    app()
```

### 3.2 Click (battle-tested)
```python
import click

@click.group()
@click.version_option()
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.argument("name")
@click.option("--template", "-t", default="default", help="Template to use")
@click.option("--git/--no-git", default=True, help="Initialize git")
def init(name, template, git):
    """Initialize a new project."""
    click.echo(f"Creating project: {name}")

if __name__ == "__main__":
    cli()
```

### 3.3 Rich output
```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# Styled output
console.print("[bold green]Success![/] Project created.")
console.print("[red]Error:[/] File not found.", style="bold")

# Tables
table = Table(title="Dependencies")
table.add_column("Package", style="cyan")
table.add_column("Version", style="green")
table.add_column("Status")
table.add_row("react", "18.3.0", "[green]Up to date[/]")
table.add_row("webpack", "5.91.0", "[yellow]Update available[/]")
console.print(table)

# Progress
for item in track(range(100), description="Processing..."):
    process(item)
```

---

## 4. Go CLIs

### 4.1 Cobra (standard for Go CLIs)
```go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "mytool",
    Short: "My awesome CLI tool",
}

var initCmd = &cobra.Command{
    Use:   "init <name>",
    Short: "Initialize a new project",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        template, _ := cmd.Flags().GetString("template")
        fmt.Printf("Creating project: %s (template: %s)\n", name, template)
        return nil
    },
}

func init() {
    initCmd.Flags().StringP("template", "t", "default", "Template to use")
    initCmd.Flags().Bool("no-git", false, "Skip git initialization")
    rootCmd.AddCommand(initCmd)
}

func Execute() error {
    return rootCmd.Execute()
}
```

### 4.2 Bubbletea (TUI framework)
```go
package main

import (
    "fmt"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 { m.cursor-- }
        case "down", "j":
            if m.cursor < len(m.choices)-1 { m.cursor++ }
        case "enter", " ":
            if _, ok := m.selected[m.cursor]; ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    s := "Select features:\n\n"
    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i { cursor = ">" }
        checked := " "
        if _, ok := m.selected[i]; ok { checked = "x" }
        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }
    s += "\nPress q to quit.\n"
    return s
}
```

---

## 5. Output Formatting

### 5.1 Colors (Node.js with chalk)
```typescript
import chalk from "chalk";

console.log(chalk.green("Success!"));
console.log(chalk.red.bold("Error:"), "Something went wrong");
console.log(chalk.yellow("Warning:"), "Deprecated feature");
console.log(chalk.cyan("Info:"), "Processing 42 files...");
```

### 5.2 Spinners and progress
```typescript
import ora from "ora";

const spinner = ora("Installing dependencies...").start();
await installDeps();
spinner.succeed("Dependencies installed");

// Or on failure:
spinner.fail("Installation failed");
```

### 5.3 Tables
```typescript
import { table } from "table";

const data = [
  ["Name", "Version", "Status"],
  ["react", "18.3.0", "OK"],
  ["webpack", "5.91.0", "Update available"],
];
console.log(table(data));
```

### 5.4 Output modes
Support both human and machine-readable output:
```typescript
program
  .option("--json", "Output as JSON")
  .option("--quiet", "Minimal output");

function output(data: unknown, opts: { json?: boolean; quiet?: boolean }) {
  if (opts.json) {
    console.log(JSON.stringify(data, null, 2));
  } else if (opts.quiet) {
    console.log(data.id); // Just the essential value
  } else {
    // Pretty human-readable output
    printTable(data);
  }
}
```

---

## 6. Configuration Management

### 6.1 Config file locations
```typescript
import os from "os";
import path from "path";

function getConfigDir(appName: string): string {
  const platform = process.platform;
  if (platform === "win32") {
    return path.join(process.env.APPDATA || "", appName);
  }
  if (platform === "darwin") {
    return path.join(os.homedir(), "Library", "Application Support", appName);
  }
  return path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), ".config"), appName);
}
```

### 6.2 Config precedence
1. Command-line flags (highest priority)
2. Environment variables
3. Project-local config (`.mytoolrc`, `mytool.config.js`)
4. User config (`~/.config/mytool/config.json`)
5. Default values (lowest priority)

### 6.3 Config file with cosmiconfig
```typescript
import { cosmiconfig } from "cosmiconfig";

const explorer = cosmiconfig("mytool");
const result = await explorer.search();
// Searches: .mytoolrc, .mytoolrc.json, .mytoolrc.yaml,
// mytool.config.js, package.json "mytool" field
```

---

## 7. Shell Completions

### 7.1 Bash completions (Commander.js)
```bash
# Generate completion script
mytool completion bash > /etc/bash_completion.d/mytool

# Or for user-local:
mytool completion bash >> ~/.bashrc
```

### 7.2 Cobra auto-completions (Go)
```go
rootCmd.AddCommand(&cobra.Command{
    Use:   "completion [bash|zsh|fish]",
    Short: "Generate shell completion script",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        switch args[0] {
        case "bash":
            return rootCmd.GenBashCompletion(os.Stdout)
        case "zsh":
            return rootCmd.GenZshCompletion(os.Stdout)
        case "fish":
            return rootCmd.GenFishCompletion(os.Stdout, true)
        }
        return fmt.Errorf("unsupported shell: %s", args[0])
    },
})
```

---

## 8. Packaging & Distribution

### 8.1 Node.js → npm
```bash
npm publish           # Publish to npm registry
npx mytool            # Users can run without installing
```

### 8.2 Python → PyPI
```bash
pip install build twine
python -m build
twine upload dist/*
```

### 8.3 Go → goreleaser
```yaml
# .goreleaser.yaml
builds:
  - env: [CGO_ENABLED=0]
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
brews:
  - repository:
      owner: myorg
      name: homebrew-tap
    homepage: https://github.com/myorg/mytool
    description: My awesome CLI tool
```

### 8.4 Single binary (Node.js)
```bash
# Using pkg
npx pkg . --targets node20-linux-x64,node20-macos-x64,node20-win-x64

# Using bun
bun build ./src/cli.ts --compile --outfile mytool
```

### 8.5 Homebrew formula
```ruby
class Mytool < Formula
  desc "My awesome CLI tool"
  homepage "https://github.com/myorg/mytool"
  url "https://github.com/myorg/mytool/releases/download/v1.0.0/mytool-1.0.0.tar.gz"
  sha256 "abc123..."

  depends_on "node@20"

  def install
    bin.install "mytool"
  end

  test do
    assert_match "1.0.0", shell_output("#{bin}/mytool --version")
  end
end
```

---

## 9. Testing CLIs

### 9.1 Testing command output
```typescript
import { execSync } from "child_process";

describe("mytool CLI", () => {
  it("shows help", () => {
    const output = execSync("node dist/cli.js --help").toString();
    expect(output).toContain("My awesome CLI tool");
    expect(output).toContain("init");
    expect(output).toContain("build");
  });

  it("shows version", () => {
    const output = execSync("node dist/cli.js --version").toString();
    expect(output.trim()).toMatch(/^\d+\.\d+\.\d+$/);
  });

  it("exits with code 2 on unknown command", () => {
    try {
      execSync("node dist/cli.js unknown 2>&1");
    } catch (err) {
      expect(err.status).toBe(2);
    }
  });
});
```

### 9.2 Testing with Go
```go
func TestInitCommand(t *testing.T) {
    buf := new(bytes.Buffer)
    rootCmd.SetOut(buf)
    rootCmd.SetArgs([]string{"init", "myproject"})
    err := rootCmd.Execute()
    assert.NoError(t, err)
    assert.Contains(t, buf.String(), "Creating project: myproject")
}
```

---

## 10. Common Pitfalls

1. **No error messages** — print what went wrong and how to fix it.
2. **Swallowing errors** — always exit with non-zero code on failure.
3. **No `--help`** — every command needs help text.
4. **Hardcoded paths** — use XDG dirs, respect `$HOME`.
5. **No stdin support** — allow piping (`cat file | mytool process`).
6. **Colors in pipes** — detect TTY, disable colors when piped.
7. **No `--version`** — users need to know what they're running.
8. **Global state** — makes testing hard; use dependency injection.
