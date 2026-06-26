# ClawReceipt

`ClawReceipt` 🧾 is a specialized tool for OpenClaw to automatically capture, process, and manage receipts and financial data using a Retro Neon CLI & TUI.

Primary command: `run.py` (through Python)

## What It Does

- Extracts receipt details (Date, Time, Store, Amount, Category) from OpenClaw via CLI.
- Automatically tracks and monitors spending against a customized monthly budget.
- Triggers `Exceeded Budget!` alerts when total expenses cross the threshold.
- Provides a stunning Terminal UI (TUI) to browse and analyze receipts history.
- Exports receipt data seamlessly to `CSV` or `Excel` formats.
- Integrates flawlessly as an OpenClaw Skill via `SKILL.md`.

## Requirements

- Python `>=3.10`
- Windows (for specific Unicode CLI setup) or Linux/macOS
- OpenClaw CLI (`openclaw`) for triggering the skill

## Install

Clone the repository and prepare your virtual environment:

```bash
git clone https://github.com/OpenKrab/ClawReceipt.git
cd ClawReceipt
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

Initialize your budget (e.g. 5,000 Baht):

```bash
python run.py budget --set 5000
```

Add a new receipt (typically triggered via OpenClaw):

```bash
python run.py add --date "2026-02-27" --time "15:30:00" --store "Seven Eleven" --amount 120.50 --category "อาหาร"
```

Launch the interactive Terminal Dashboard:

```bash
python run.py tui
```

## Main Commands

```bash
# Add a new receipt record
python run.py add --date <YYYY-MM-DD> --time <HH:MM:SS> --store <Name> --amount <Amount> --category <Category>

# List all receipts in the terminal archive
python run.py list

# Open interactive TUI Dashboard
python run.py tui

# Set overall monthly budget
python run.py budget --set <Amount>

# Check current spent vs budget status
python run.py budget

# Silent budget alert check (exit 1 if exceeded, 0 if within)
python run.py alert
```

## Paths Used by Default

- SQLite Database path: `data/receipts.db`
- Source Code: `src/`

## For OpenClaw Agents

- Check `SKILL.md` for proper instructions on integrating standard CLI triggers into OpenClaw's context.
- Avoid running the `tui` command as an automated agent, as it blocks the terminal input indefinitely. Use `add`, `budget`, or `list` for CI/CD or Agentic behavior.

## Development

```bash
pip install -r requirements.txt
# Test the database
python src/db.py
# Test the components
python run.py list
```

## License

MIT
