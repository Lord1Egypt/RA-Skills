# Fluid Network Analyzer Skill

## Overview

Fluid Network Analyzer is a prototype industrial skill for modeling, solving, and analyzing fluid networks.

The skill supports:

- TOML-based network modeling
- Steady-state pressure and flow solving
- Scenario-based system analysis
- Connectivity and flow path analysis
- Automatic Markdown report generation

This skill is designed to be used by AI agents to assist engineers in fluid network design and reliability analysis.

---

## Capabilities

### 1. Generate Network Model

Generate a TOML network description from natural language.

Input:
- natural language description of a fluid system

Output:
- TOML network definition

---

### 2. Solve Fluid Network

Solve steady-state pressure and flow distribution.

Input:
- TOML network file
- scenario name

Output:
- node pressures
- branch flows
- velocities
- pressure drops

---

### 3. Scenario Analysis

Analyze system reliability under different operating conditions.

Input:
- network model
- scenario definition

Output:
- connectivity analysis
- flow path analysis
- load functionality check
- Markdown analysis report

---

## Example Use Case

User request:

Design a fluid network with one source and two loads.

Agent workflow:

1. Generate TOML network model
2. Run solver to compute pressures and flows
3. Run scenario analysis
4. Generate Markdown report

---

## Outputs

The skill can generate:

- node pressure tables
- branch flow results
- load functionality analysis
- connectivity paths
- Markdown scenario reports

Example reports:

- `report_normal.md`
- `report_valve_closed.md`

---

## Intended Use

This skill can be used for:

- hydraulic system analysis
- industrial piping network analysis
- digital twin simulations
- AI-assisted engineering design

---

## License

MIT-0