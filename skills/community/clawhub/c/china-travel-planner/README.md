# china-travel-planner

An [OpenClaw](https://github.com/nicobailon/openclaw) skill for planning domestic China trips — combining real-time search, metro-aware routing, and itinerary page generation.

## What it does

Given a travel request like "清明去长沙玩三天", this skill produces a practical itinerary with transport options, hotel area recommendations, attraction picks, and a day-by-day schedule. It can also generate a standalone HTML page for the trip plan.

## Key features

- **Real-time search via flyai/Fliggy** — flights, hotels, POIs, and tickets with live pricing and availability
- **Metro-aware planning** — subway line data, station coverage analysis, hotel-to-station matching, and line-coverage optimization
- **Page generation pipeline** — converts a trip plan into structured JSON, then renders it as a self-contained HTML itinerary page (Tailwind CSS, no build step)
- **Wikimedia Commons image search** — finds Creative Commons images for destinations and attractions

## Project structure

```
china-travel-planner/
├── SKILL.md                    # Skill definition and planning workflow
├── references/                 # Prompt references and planning guides
│   ├── domestic-planning-prompts.md
│   ├── subway-aware-planning.md
│   └── structured-output-mode.md
├── scripts/                    # Metro data utilities
│   ├── fetch_subway_data.py    # Download subway network data
│   ├── metro_hotel_match.py    # Match hotels to nearby stations
│   └── coverage_plan_notes.py  # Metro line coverage planning
└── page-generator/             # Trip page generation pipeline
    ├── schema/                 # JSON schema for trip data
    ├── scripts/                # CLI tools (generate, init, image search)
    ├── templates/              # HTML template + JS renderer
    └── examples/               # Example outputs
        └── changsha-2026-03-31/  # Changsha 3-day trip example
```

## Installation

Install as an OpenClaw skill:

```bash
# From ClawHub
clawhub install china-travel-planner

# Or clone manually
git clone https://github.com/gushuaialan1/china-travel-planner.git \
  ~/.openclaw/workspace/skills/china-travel-planner
```

The skill also depends on the [flyai skill](https://github.com/nicobailon/openclaw) for real-time search. Make sure it's installed too.

## How it works

1. **Clarify** — the agent extracts trip parameters (dates, destination, budget, constraints) from your request
2. **Search** — queries flyai/Fliggy for flights, hotels, and POIs; fetches metro data if needed
3. **Plan** — assembles a day-by-day itinerary with transport, meals, and timing
4. **Generate** (optional) — exports the plan as JSON following `page-generator/schema/trip-schema.json`, then renders it into a standalone HTML page

## Example output

See [`page-generator/examples/changsha-2026-03-31/`](page-generator/examples/changsha-2026-03-31/) for a complete Changsha 3-day trip — includes the source JSON data and the generated HTML itinerary page.

## License

MIT
