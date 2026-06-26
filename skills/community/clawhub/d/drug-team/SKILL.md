# drug-team

Meta-skill that orchestrates a team of specialized AI agents for drug design.

## Overview
- **Purpose**: Designs novel drug candidates for a given target/indication with constraints (e.g., \"Design drug for pain relief, logP<3\").
- **Agents**:
  1. **Chem Synth** (uses chemistry-query skill): Proposes molecular scaffolds and synthesis routes.
  2. **Synth Notebook** (uses synth-notebook skill): Visualizes routes, optimizes yields, checks safety.
  3. **Lab Inventory** (uses lab-inventory skill): Checks stock for reagents, estimates costs.
  4. **ADMET**: Predicts QED, SA, logP, TPSA, pKa using RDKit/ML proxies.
  5. **Tox**: Checks PAINS, Brenk alerts, Ames test.
  6. **Pharm**: Evaluates target binding affinity (docking proxy via web/tools).
  7. **Patent Scout** (uses patent_scout.py): Scans for prior art patents, computes novelty score, checks for blocking patents via web searches.
- **Coordination**: Iterative polling and messaging between agents to refine candidates.
- **Output**: Table of top 3 molecules (SMILES, route, scores) + visualizations (e.g., mol images).

## Triggers
- drug design
- design drug
- painkiller
- drug synthesis
- synth pharm
- design molecule
- \"low tox\" drug
- inventory-aware design
- design with stock check
- check stock for synthesis
- patent
- novelty
- prior art

## Usage
When triggered, runs `scripts/orchestrate.py \"{user_query}\"` .

## Integration
- Integrates chemistry-query for initial scaffolds and routes.
- Uses synth-notebook for route visualization, yield optimization, and safety checks.
- Incorporates lab-inventory for reagent stock checking and cost estimation.
- Ranks candidates including feasibility scores based on yield, safety (with SDS scans for route chemicals, risk scores, and alerts), and inventory availability.
- Post-design patent scouting to include novelty scores and blocking status in candidate ranking (\"High novelty: no blocking patents\").

## Dependencies
- RDKit (installed)
- chemistry-query skill (exists)
- synth-notebook skill
- lab-inventory skill
- Matplotlib/Plotly for viz
- OpenClaw subagent spawning
- beautifulsoup4 for patent_scout scraping
