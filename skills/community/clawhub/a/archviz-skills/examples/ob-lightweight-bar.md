```mermaid
%% Obsidian lightweight bar (from archviz-skills; env=OB, type=ranking per report).
%% Use flowchart or xychart for bar; restrained: single IKB, warm paper, short codes.
%% Agent vibe: output this for direct OB render (no Python yet).

%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#f5f0eb',
  'primaryTextColor': '#1B365D',
  'primaryBorderColor': '#a8a29e',
  'lineColor': '#002FA7',
  'fontSize': '13px'
}}}%%
%% Brief: Ranking bar for project phases (restrained, Swiss).
xychart-beta
    title "Project Phases (V1)"
    x-axis ["V1.1 Env", "V1.2 Ledger", "V1.3 Settle"]
    y-axis "Weeks" 0 --> 10
    bar [6, 7, 4]
```

**ASCII alternative (for terminal-like in OB):**
```
Project Phases (V1)
V1.1 Env    |======|
V1.2 Ledger      |=======|
V1.3 Settle           |====|
Legend: |===| = weeks; codes for labels.
```

**Self-contained HTML (paste to OB HTML block for direct interactive browse):**
(See /templates/self-contained-html-viz.txt ; agent fills data for bar type.)

**Notes (per skill):**
- Env=OB → lightweight.
- Type from report: ranking → bar.
- Restrained: single accent #002FA7, warm paper, no junk.
- For deliverables later: run python-viz template for Plotly version.
- Author habit: direct, no filler.
```