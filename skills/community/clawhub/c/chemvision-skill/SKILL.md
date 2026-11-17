---
name: chemvision
description: Use this skill when the user asks about chemistry — chemical names, molecular structures (SMILES), molecular formulas, molecular weights, safety information (GHS hazards), or chemical reaction predictions. Supports Chinese and English chemical names, IUPAC names, and common names. Calls PubChem and OPSIN real chemistry databases to reduce LLM hallucinations. Returns molecular structure images and chemical equation renderings.
metadata:
  skill_version: "3.3.0"
  tags: ["AIPC", "chemistry", "agent", "tool-calling", "pubchem"]
---

# ChemVision AI 化学家

化学数据查询服务 — PubChem + OPSIN 真实数据库，分子结构图 + 化学方程式渲染。

## When to Use

- Chemical compound queries (name → structure, SMILES → info)
- Safety / GHS hazard information
- Chemical reaction prediction (Agent answers, tools provide data)
- Molecular structure image rendering

## Step 0: Ensure Service Is Running

```bash
cd {this_skill_dir} && python manage.py status
```

> **Port note**: Default port is 8899. If occupied, the service auto-selects the next free port (8900, 8901...). Run `python manage.py status` to see the actual port. The service uses `CHEMVISION_PORT` env var (not `SERVER_PORT`) to avoid conflicts with the Agent host process.

If not running: `python manage.py start`
To stop: `python manage.py stop`

## Step 1: Call Tools

POST to `http://localhost:8899/api/tools/call`.

### name_to_structure

```bash
curl -s -X POST http://localhost:8899/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"name_to_structure","arguments":{"name":"苯甲酸"}}'
```

Returns SMILES, formula, weight, `svg_url`.

**Important**: Tools only accept English names. If the user asks in Chinese, Agent must translate to English first, then call the tool. Example: "苯甲酸" → "benzoic acid".

### inspect_smiles

```bash
curl -s -X POST http://localhost:8899/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"inspect_smiles","arguments":{"smiles":"CCO"}}'
```

### safety_info

```bash
curl -s -X POST http://localhost:8899/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"safety_info","arguments":{"query":"benzene"}}'
```

### predict_reaction

Queries chemical data for reactants. Agent should answer the reaction itself.

```bash
curl -s -X POST http://localhost:8899/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"predict_reaction","arguments":{"reactants":"acetic acid + ethanol"}}'
```

## Step 2: Show Results

### Molecular structure

1. Open `svg_url` from tool result in browser
2. Screenshot → save file
3. Send to user: `send_file_to_user(file_path="xxx.png", caption="分子结构图")`

### Chemical equation

After answering a reaction, render the equation:

1. Open in browser: `http://localhost:8899/api/formula/{equation}`
2. Screenshot → save file
3. Send to user: `send_file_to_user(file_path="xxx.png", caption="化学方程式")`

**Equation format rules:**
- Subscripts automatic: `H2O`, `CH3COOH`, `Ca(OH)2`
- Superscripts: `Fe^{2+}`, `SO4^{2-}`
- Arrows: `->` (one way), `<=>` (equilibrium)
- Conditions: `[加热]`, `[催化剂]` (shown above/below arrow)
- Example: `CH3COOH+C2H5OH<=>[浓硫酸][加热]CH3COOC2H5+H2O`

### Fallback

If `predict_reaction` fails, the Agent answers directly using its own chemistry knowledge, then renders the equation via `/api/formula/`.

## Notes

- Pure data tools — NO LLM dependency, ALL reasoning by Agent
- All data from PubChem/OPSIN real databases
- Local only — chemistry data never leaves the machine
- Swagger UI: http://localhost:8899/docs
