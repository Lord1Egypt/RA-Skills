---
name: 93pct
description: Autocomplete for agency next steps. Like Google autocomplete but for what to do next. Given any context, returns the top concrete viable actions ranked by ROI/effort ratio. Always outputs exactly one job ID to approve. Named after the 93% standard — every suggestion must clear that bar.
version: 1.0.0
author: Fiesta
tags: [planning, autocomplete, next-steps, agency, productivity]
---

# 93% — Agency Autocomplete

## Doctrine
> "Plan Shannon → Penn Station"

Shannon is the currency of information (Claude Shannon, entropy theory).  
Penn Station is the commuter hub — where everything converges.  
The plan: route all decisions through Shannon (information value) to reach the station (execution).  
Low Shannon = entropy = noise = waste.  
High Shannon = signal = viable next step.

## Usage
```
python3 /root/.openclaw/workspace/skills/93pct/suggest.py          # top 5 next steps now
python3 /root/.openclaw/workspace/skills/93pct/suggest.py --stack  # show approval stack
python3 /root/.openclaw/workspace/skills/93pct/suggest.py --done <id>  # mark completed
```

## Output format
Each suggestion includes:
- Shannon score (0-10, information density)
- Effort (minutes)
- Blocker (what stops it)
- Job ID to approve (if exec needed)
- Exact command or action

## The 93% Bar
A suggestion clears 93% if:
- It is concrete (not "consider doing X")
- It is viable right now (blocker is known and solvable)
- It produces measurable output
- It costs less than it returns
