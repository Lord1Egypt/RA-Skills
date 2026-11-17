# dia-ask

**Prompt your locally-running [Dia](https://www.diabrowser.com/) browser from the command line and get its assistant's answer back as an exact text file.**

Dia is The Browser Company's browser; its built-in assistant is an agent that can read logged-in, JS-heavy pages in your real session and write files to disk. `dia-ask` hands that assistant a prompt and returns the **absolute path of a file** it wrote — so you get exact text (formulas, code, long documents) with no screen OCR and no scroll limits.

```bash
node dia-ask-v2.js "summarize the open tab and list every external link" --format md
# → /Users/you/Library/Application Support/Dia/.../dia_out_1730000000000.md
```

It prints one line to stdout: the path. Read that file with your own tools.

Built by [AgentNeo](https://agneo.app) — AI agents with operational rigor, and the open-source safety patterns to run them.

> Built by **[AgentNeo](https://agneo.app)**. This is a small, readable **reference implementation** — take the idea and adapt it.

## Why a file (not stdout text)?

Dia's assistant is an agent that can write to disk. Asking it to **save** its answer to a uniquely-named file and then polling for that file gives you the exact bytes it produced — any length, any format — instead of scraping what's on screen.

## Mental model: Dia is eyes, not hands

Dia **sees and investigates** — it renders logged-in, JS-heavy pages and returns their exact text. Reach for it to **read / research** what's behind a login or heavy JS. It is not a clicker: for actions (filling forms, submitting), use your own tools. Dia looks; you execute.

## Requirements

- **macOS only.** The tool drives Dia through macOS Accessibility (AppleScript/AX) and Core Graphics events.
- **[Dia](https://www.diabrowser.com/) installed.** It runs on *your* Dia and *your* subscription — there is no hosted service here.
- **Accessibility permission** for whatever runs `node` (Terminal, your IDE, etc.): System Settings → Privacy & Security → Accessibility.
- **Node.js ≥ 18.**

## Install

```bash
git clone https://github.com/germankovacevic-lab/dia-ask.git
cd dia-ask
node dia-ask-v2.js "hello, what time is it?"
```

No dependencies — pure Node standard library.

## Usage

```
node dia-ask-v2.js "<prompt>" [--format md|txt|json|csv] [--timeout 300] [--no-fallback] [--debug]
```

| Flag | Default | Meaning |
|------|---------|---------|
| `--format` | `md` | Output file format: `md`, `txt`, `json`, `csv`. |
| `--timeout` | `300` | Seconds to wait for the answer file (long generations can take minutes). |
| `--no-fallback` | off | Fail instead of falling back to the focus-stealing v1 sender. |
| `--debug` | off | Verbose progress + fidelity diagnostics on stderr. |

Examples:

```bash
node dia-ask-v2.js "extract every row of the pricing table on the open page" --format csv
node dia-ask-v2.js "read this paywalled article and give me the key claims" --format txt --timeout 600
```

## How it works

Two senders, same I/O contract (both print the answer file's path):

- **`dia-ask-v2.js` (default, focus-safe).** Posts keycodes straight to Dia's process (`CGEventPostToPid`) and focuses its input via Accessibility **without activating the app**. It never steals your focus and survives you typing in another app mid-send. It types the prompt as real keystrokes, verifies the input char-for-char before submitting (retrying on any dropped key), then waits for a new Dia agent context + the output file.
- **`dia-ask.js` (v1, fallback).** Opens a fresh full-screen Dia window and pastes the prompt — simpler, but it briefly takes focus. v2 falls back to this automatically if the Accessibility path can't take (no Dia window, input not focusable); pass `--no-fallback` to disable.

## Caveats — read these

This is an **unofficial UI-automation** tool, not a supported integration:

- **It depends on Dia's window/Accessibility internals.** The Browser Company can change Dia's UI in any release and break this — treat it as "works until Dia changes," not a stable API.
- **No official API is used.** It drives the app the way a user would (synthetic keystrokes + Accessibility), against *your own* Dia install and subscription. Make sure that's consistent with how you want to use Dia.
- **macOS + Accessibility only.** No Linux/Windows, no headless/CI.
- **Latency.** A round trip is typically tens of seconds to a few minutes depending on the answer.
- **Reference implementation.** It's deliberately small and readable so you can audit it and adapt it; it is not a hardened product.

## Tests

```bash
npm test   # pure logic: prompt building, arg parsing, output discovery, keymap
```

The Accessibility/Core-Graphics injection can only be validated end-to-end against a live Dia; the pure logic around it is unit-tested.

## About

Built and maintained by [AgentNeo](https://agneo.app) — we build AI agents with operational rigor and open-source the safety patterns needed to run them in the real world. Contact: [gk@agneo.app](mailto:gk@agneo.app)

## License

MIT © German Kovacevic
