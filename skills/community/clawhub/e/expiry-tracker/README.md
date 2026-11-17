# Expiry Tracker 🥛⏰

> Track food expiry dates, get daily alerts, reduce food waste.

## The Problem

The average household throws away **30% of the food they buy**. Most of it spoils because people forget what's in the fridge and when it expires.

## The Solution

A simple command-line tool that:
- 📦 Tracks perishable items with expiry dates
- ⏰ Alerts you before food goes bad
- 💡 Suggests what to cook with soon-to-expire items
- 📊 Generates waste reports so you can spot patterns

## Quick Start

```bash
# Add items after grocery shopping
python scripts/expiry_tracker.py add "milk" --days 7
python scripts/expiry_tracker.py add "chicken breast" --days 3
python scripts/expiry_tracker.py add "spinach"  # auto: 4 days (leafy greens)

# Or batch add from a receipt
python scripts/expiry_tracker.py batch "milk, eggs, bread, chicken, yogurt, spinach, berries"

# Check what needs attention today
python scripts/expiry_tracker.py today

# Full inventory
python scripts/expiry_tracker.py inventory

# Mark items as consumed or wasted
python scripts/expiry_tracker.py remove "milk"           # consumed
python scripts/expiry_tracker.py remove "spinach" --wasted  # tossed

# Weekly waste report
python scripts/expiry_tracker.py report
```

## Features

- **Auto-categorization**: 10 food categories with keyword matching
- **Smart defaults**: Knows that chicken lasts 3 days, carrots 14 days
- **Recipe hints**: Suggests how to use soon-to-expire items
- **Waste tracking**: Records what was consumed vs wasted for pattern analysis
- **No dependencies**: Pure Python stdlib, runs anywhere

## Installation

```bash
git clone https://github.com/voronindenis5/expiry-tracker.git
cd expiry-tracker
python scripts/expiry_tracker.py today
```

Data is stored in `~/.expiry_tracker.json`.

## License

MIT © Denis Voronin
