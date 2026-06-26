# Bottleneck / Chokepoint Identification Workflow

> Concentration Risks | Raw Material Risks | Investigation Method | Multilingual Queries (KO/JA/ZH-CN/ZH-TW) | Counterfactual Check | Output Format

**Question pattern:** "What's the chokepoint in X supply chain?" / "Who's the single-source risk?"

## Suspected Concentration Risks (verify before citing)

These segments are frequently cited in industry press as having high supplier
concentration. All share figures are training-data estimates (~2023-2024) and
should be verified through current SEMI, TechCET, or Yole data before including
in any report. Use these as investigation starting points.

| Company | Material/Equipment | Suspected Position (verify) | Substitutability |
|---------|-------------------|------------|-----------------|
| Ajinomoto Fine-Techno | ABF film (FC-BGA substrate insulation) | Suspected near-monopoly | Near-zero |
| Lasertec (6920.T) | EUV mask inspection equipment | Suspected near-monopoly | Near-zero |
| NuFlare (Toshiba sub) | E-beam mask writers | Suspected near-monopoly | Very low |
| DISCO (6146.T) | Dicing saws | Suspected dominant | Low |
| Shin-Etsu Chemical (4063.T) | Photomask blanks | Suspected dominant | Low |
| Toyo Gosei (4970.T) | Photoacid generators (PAGs) | Suspected dominant | Low |
| SCREEN Holdings (7735.T) | Wafer cleaning equipment | Suspected dominant | Moderate |
| HORIBA (6856.T) | Mass flow controllers | Suspected dominant | Moderate |
| Shin-Etsu + SUMCO | Silicon wafers (combined) | Suspected combined dominance | Moderate |
| Stella Chemifa + Morita | Electronic-grade HF (combined) | Suspected combined dominance | Low |

## Raw Material Concentration Risks (upstream, verify before citing)

These upstream dependencies are reported in industry and geological sources.
Verify with current USGS, ITC, or industry data.

| Material | Reported Source (verify) | Geography risk |
|----------|--------|---------------|
| Fluorspar (CaF2) | China reportedly dominant in acid-grade supply | Feeds into HF, NF3, all fluorine chemistry |
| Rare earths (Ce for CMP) | China reportedly dominant in processing | Ceria for CMP slurry |
| High-purity quartz | Spruce Pine, NC (USA), unique geological deposit | No substitute for CZ crucibles |
| Tantalum (for sputtering targets) | DRC reportedly dominant in artisanal coltan | Conflict mineral |
| Tungsten | China reportedly dominant in mining | Sputtering targets, CVD |
| Hafnium | CEZUS/Framatome (France) believed top supplier | Nuclear industry byproduct, linked to nuclear fuel demand |

## Investigation Method

1. **Map the supply chain node** — What material/equipment is in question?
2. **Count the suppliers** — How many companies globally can provide this at semiconductor grade?
3. **Assess concentration** — What % does the top supplier hold? Top 2? Top 3?
4. **Check geographic concentration** — Are all suppliers in one country/region?
5. **Evaluate substitutability** — Can a fab switch suppliers? How long does qualification take? (typically 6-24 months for materials)
6. **Identify tier-2 dependencies** — Even if there are multiple tier-1 suppliers, do they all depend on the same tier-2 input?
7. **Check for active diversification** — Is anyone investing to break the chokepoint? (Korean 국산화 push, Chinese 国产替代)

## Multilingual Search Queries

### Korean (집중도 / 독점):
```
[소재명] 독점 공급                → "[material] monopoly supply"
[소재명] 단일 공급원              → "[material] single source"
[소재명] 공급 집중                → "[material] supply concentration"
[소재명] 공급 리스크              → "[material] supply risk"
[소재명] 대체 불가                → "[material] irreplaceable"
[소재명] 공급선 다변화 필요       → "[material] needs supply diversification"
```

### Japanese (寡占 / 独占):
```
{材料名} 独占                    → "[material] monopoly"
{材料名} 寡占                    → "[material] oligopoly"
{材料名} 供給リスク              → "[material] supply risk"
{材料名} シェア 集中             → "[material] share concentration"
{材料名} 代替困難                → "[material] hard to substitute"
{材料名} ボトルネック            → "[material] bottleneck"
```

### Chinese — Mainland (垄断 / 卡脖子):
```
[材料名] 垄断                    → "[material] monopoly"
[材料名] 供应集中度              → "[material] supply concentration"
[材料名] 卡脖子                  → "[material] chokepoint/stranglehold"
[材料名] 单一供应商风险          → "[material] single-supplier risk"
[材料名] 不可替代                → "[material] irreplaceable"
[材料名] 供应链安全              → "[material] supply chain security"
```

### Chinese — Taiwan (壟斷 / 供應集中):
```
[材料名] 壟斷                    → "[material] monopoly"
[材料名] 供應集中                → "[material] supply concentration"
[材料名] 單一供應商              → "[material] single supplier"
[材料名] 供應風險                → "[material] supply risk"
[材料名] 替代方案                → "[material] alternatives"
[材料名] 供應鏈韌性              → "[material] supply chain resilience"
```

## Counterfactual check on concentration claims

Before reporting any concentration figure, run the [Counterfactual Consistency Check](counterfactual-check.md). The key question for bottleneck analysis: "What if a supplier exists that I haven't found because they don't publish in the languages I searched?" Also challenge single-source share figures. If your concentration claim comes from one analyst report, that's a lead, not a measurement.

## Output: Chokepoint Assessment

```
Material: [X]
Current suppliers: [list with market share estimates]
Geographic concentration: [country/region breakdown]
Substitution difficulty: [Low/Medium/High/Near-impossible]
Qualification time: [months]
Active diversification efforts: [who's trying to enter]
Upstream dependencies: [tier-2 chokepoints]
Risk scenario: [what happens if supply is disrupted]
Confidence: [level + sources]
```
