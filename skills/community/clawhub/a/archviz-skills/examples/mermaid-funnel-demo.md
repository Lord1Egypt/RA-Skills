# Funnel demo · archviz-skills

Reading this as: **conversion funnel** for reviewers, restrained, Warm Paper.

```
COMPLEXITY=3  DENSITY=4  RESTRAINT=8
```

See `templates/mermaid/funnel.mmd` for the full template with ASCII fallback.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#e8e4e0', 'primaryTextColor': '#1B365D', 'primaryBorderColor': '#a8a29e', 'lineColor': '#002FA7', 'fontSize': '13px'}}}%%
flowchart TD
    A["提交申请\n320人"] -->|审核通过| B["通过初审\n280人 87.5%"]
    B -->|评审| C["通过复审\n210人 75%"]
    C -->|公示| D["最终入选\n180人 85.7%"]
    D -->|入职| E["实际到岗\n168人 93.3%"]
```

Caption: 5 阶段漏斗，初审到到岗整体留存率 52.5%，主要流失在复审环节（25%）。