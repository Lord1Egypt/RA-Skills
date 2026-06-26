# Exercise Bike Buying Consultant

> Turns any AI agent into an expert exercise bike buying consultant.

## What it does

Guides first-time and replacement exercise bike buyers through a structured consultation to identify exactly which specs they need — bike type, resistance mechanism, flywheel weight, adjustability range, noise behaviour, and connectivity protocol — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across 8 areas: fitness goals, physical profile, space, noise constraints, resistance preferences, connectivity, usage volume, and region
2. Analyses answers using verified exercise bike mechanical and ergonomic standards
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Key domain coverage

- Bike type selection: upright vs recumbent vs spin/indoor cycling vs air (fan) bike
- Resistance type: magnetic (eddy current), friction (pad), air, electromagnetic (app-controlled)
- Flywheel weight guidance: ranges mapped to training intensity levels
- Noise mitigation: belt vs chain drive, magnetic vs friction, fan noise realities
- Connectivity: Bluetooth FTMS vs ANT+ FE-C for app-controlled resistance (ERG mode)
- Adjustability: seat height, handlebar reach, recumbent seat-to-pedal distance
- Frame weight capacity with 10% safety margin applied
- Common buyer mistakes flagged proactively

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/exercise-bike-buying-consultant
