# archviz-skills Mermaid Demo

Three diagrams demonstrating restrained design in Obsidian/GitHub.

## 1. Ranking Bar

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#f5f0eb', 'primaryTextColor': '#1B365D', 'primaryBorderColor': '#a8a29e', 'lineColor': '#002FA7', 'fontSize': '13px'}}}%%
xychart-beta
    title "Project Phases (weeks)"
    x-axis ["V1 Setup", "V2 Core", "V3 Polish"]
    y-axis "Weeks" 0 --> 10
    bar [6, 7, 4]
```

## 2. Process Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#f5f0eb', 'primaryTextColor': '#1B365D', 'primaryBorderColor': '#a8a29e', 'lineColor': '#a8a29e', 'fontSize': '13px'}}}%%
flowchart LR
    A[Brief] --> B[Design]
    B --> C[Build]
    C --> D[Test]
    D --> E[Ship]

    style A fill:#e8e4e0,stroke:#a8a29e,color:#44403c
    style E fill:#e4e8f0,stroke:#002FA7,color:#1B365D
```

## 3. Gantt (codes only + table)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#94a3b8', 'primaryTextColor': '#334155', 'taskBkgColor': '#e8e4e0', 'section0Color': '#e4e0dc', 'section1Color': '#e0e7e4'}}}%%
gantt
    title Roadmap
    dateFormat YYYY-MM-DD
    section V1
    A1 :a1, 2026-07-01, 6w
    A2 :a2, after a1, 7w
    section V2
    B1 :b1, after a2, 5w
    B2 :b2, after b1, 5w
```

| Code | Task | Duration | Deliverable |
|---|---|---|---|
| A1 | Setup + Swift basics | 6w | Dev environment ready |
| A2 | Core CRUD + ledger | 7w | Working data layer |
| B1 | iCloud sync | 5w | Cloud persistence |
| B2 | Charts + export | 5w | Visual analytics |
