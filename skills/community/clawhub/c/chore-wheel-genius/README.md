# Chore Wheel Genius 🏠✨

End chore wars forever. This tool assigns household tasks fairly based on
skills, availability, age, and past effort — so nobody feels overworked and
nobody gets a free ride.

## The Problem

Every household fights about chores:
- **"That's not fair!"** — someone always feels they do more
- **"It's not my turn!"** — rotation is random or forgotten
- **"I always get the gross chores!"** — unpleasant tasks pile on one person
- **"I don't know how to do that."** — no skill matching
- **"I was busy!"** — no flexibility for schedules
- **No accountability** — nobody remembers who actually did what

## The Solution

An effort-weighted, skill-matched, fairness-optimized chore assignment system:

1. Each member gets chores matched to their skills and age
2. Total effort is balanced — not just chore count
3. Unpleasant tasks rotate so nobody is stuck
4. History tracks who actually did what
5. Fairness scores reveal who's carrying the load

## Features

- 👨‍👩‍👧‍👦 **Multi-person households** — kids and adults with different capabilities
- ⚖️ **Effort-weighted assignment** — 5 trash runs ≠ 5 bathroom cleans
- 🎯 **Skill matching** — cooks cook, handypeople fix, everyone learns
- 🔄 **Unpleasant chore rotation** — nobody always cleans the toilet
- 📊 **Fairness scores** — quantitative, not emotional
- 📅 **Flexible scheduling** — daily, weekly, monthly frequencies
- 📈 **History tracking** — see trends and who's slacking
- 🏆 **Praise detection** — identify the unsung heroes of the household
- 📋 **Visual charts** — printable weekly chore chart

## Quick Start

```bash
# Set up household
python3 scripts/chore_wheel.py add-member Mom --skills cooking,laundry
python3 scripts/chore_wheel.py add-member Dad --skills repair,cooking
python3 scripts/chore_wheel.py add-member Alice 14
python3 scripts/chore_wheel.py add-member Bob 10

# Define chores
python3 scripts/chore_wheel.py add-chore "Cook dinner" --effort 5 --freq daily --skills cooking
python3 scripts/chore_wheel.py add-chore "Take out trash" --effort 2 --freq daily
python3 scripts/chore_wheel.py add-chore "Clean bathroom" --effort 4 --freq weekly

# Generate assignments
python3 scripts/chore_wheel.py assign

# Track completion
python3 scripts/chore_wheel.py done Alice "Take out trash"

# Check fairness
python3 scripts/chore_wheel.py fairness
```

## Requirements

- Python 3.6+ (stdlib only)

## License

MIT © Denis Voronin
