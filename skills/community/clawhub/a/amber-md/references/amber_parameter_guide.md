# Amber MD Parameter Guide

## Core controls
- `nstlim`: number of MD steps
- `dt`: timestep in ps
- `temp0`: target temperature
- `ntb`: box / boundary mode
- `ntp`: pressure coupling
- `cut`: nonbonded cutoff
- `ntwx`: trajectory write interval
- `ntpr`: energy print interval

## Common durations
- 1 ns: `nstlim=500000` with `dt=0.002`
- 10 ns: `nstlim=5000000`
- 100 ns: `nstlim=50000000`

## Typical production settings
- Temperature: 300 K
- Pressure: 1 atm
- Timestep: 2 fs
- Ensemble: NPT
