# Scenario Analysis Workflow

**Question pattern:** "What if X happens?" / "If Japan restricts Y, who's exposed?"

## Step 1: Define the scenario

Specify: What is the disruption? (export restriction, natural disaster, sanctions, company failure, geopolitical event)

## Step 2: Map the affected supply chain nodes

1. Read [chemistry/precursor-chains.md](../chemistry/precursor-chains.md) to trace the full material chain
2. Identify which companies sit at the disrupted node
3. Identify which downstream companies depend on them

## Step 3: Assess exposure

For each affected company/material:
- **Inventory buffer:** How many weeks/months of inventory do fabs typically hold? (varies: gases=days, wafers=weeks, chemicals=1-3 months)
- **Alternative suppliers:** Who else can supply this? At what quality and timeline?
- **Qualification timeline:** How long to qualify a new supplier? (typically 6-24 months for critical materials)
- **Geographic alternatives:** Are there suppliers outside the affected region?

## Step 4: Historical precedent

Search for past disruptions as reference:
- 2019 Japan-Korea HF/photoresist restrictions → how quickly did Korea diversify?
- 2011 Tohoku earthquake → impact on silicon wafer supply
- 2021-2022 substrate shortage → ABF bottleneck impact
- 2024-09 Hurricane Helene → Spruce Pine, NC quartz operations halted (~70-90% of global HPQ supply); mine damage minor but town infrastructure devastated; Sibelco restarted within ~2 weeks; no lasting chip supply disruption (confirmed: NPR, CNN, CNBC, Sibelco/Quartz Corp statements)
- COVID-19 logistics disruptions → semiconductor materials shipping delays

## Multilingual Search Queries

### Korean (시나리오 / 영향):
```
[소재명] 수출 규제 영향            → "[material] export restriction impact"
[소재명] 공급 차질                 → "[material] supply disruption"
[소재명] 재고 부족                 → "[material] inventory shortage"
[소재명] 대체 공급처               → "[material] alternative supply source"
[소재명] 공급망 리스크 대응        → "[material] supply chain risk response"
반도체 [소재명] 수급 전망          → "semiconductor [material] supply-demand outlook"
```

### Japanese (シナリオ / 影響):
```
{材料名} 輸出規制 影響             → "[material] export control impact"
{材料名} 供給不安                  → "[material] supply concern"
{材料名} 在庫不足                  → "[material] inventory shortage"
{材料名} 代替調達                  → "[material] alternative procurement"
{材料名} サプライチェーン リスク   → "[material] supply chain risk"
{材料名} 供給途絶 シナリオ         → "[material] supply disruption scenario"
```

### Chinese — Mainland (情景分析 / 影响):
```
[材料名] 出口管制 影响             → "[material] export control impact"
[材料名] 供应中断                  → "[material] supply disruption"
[材料名] 库存不足                  → "[material] inventory shortage"
[材料名] 替代供应                  → "[material] alternative supply"
[材料名] 供应链风险                → "[material] supply chain risk"
[材料名] 断供 影响                 → "[material] cutoff impact"
```

### Chinese — Taiwan (情境分析 / 影響):
```
[材料名] 出口管制 影響             → "[material] export control impact"
[材料名] 供應中斷                  → "[material] supply disruption"
[材料名] 庫存不足                  → "[material] inventory shortage"
[材料名] 替代供應                  → "[material] alternative supply"
[材料名] 供應鏈 風險 因應          → "[material] supply chain risk response"
[材料名] 斷料 衝擊                 → "[material] material cutoff impact"
```

## Step 5: Output scenario assessment

## Counterfactual check on precedents

Before presenting the scenario assessment, run the [Counterfactual Consistency Check](counterfactual-check.md). Historical parallels are seductive. Ask: "What has changed since my precedent that would make the outcome different this time?" If your scenario is "Japan restricts HF again," remember Korea spent 5 years building domestic HF capacity since 2019. The same trigger can produce a completely different outcome.

```
Scenario: [description]
Affected materials: [list]
Key companies at risk: [list with exposure level]
Estimated impact timeline: [immediate / weeks / months]
Existing inventory buffer: [estimate]
Alternative supply options: [list with qualification timeline]
Historical parallel: [reference case]
Mitigation strategies: [what companies can do]
```
