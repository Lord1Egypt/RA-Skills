# Change Detection Workflow

**Question pattern:** "What's changed in X supply chain?" / "How has Y supplier landscape shifted?"

## Key Events That Reshape Semiconductor Supply Chains

### Geopolitical triggers:
- **2019 Japan-Korea export restrictions** (HF, photoresist, fluorinated polyimide)
- **2020-2024 US-China export controls** (Entity List, equipment restrictions, advanced chip bans)
- **CHIPS Act equivalents** (US, EU, Japan, Korea, India — subsidy-driven reshoring)

### Market triggers:
- **HBM/AI demand surge** (2023-present) — reshaping packaging, test, thermal materials supply
- **Automotive electrification** — SiC/GaN power semiconductor demand
- **Memory cycle swings** — affects materials/equipment procurement patterns

## Investigation Method

1. **Establish baseline** — What was the supply chain structure BEFORE the change event?
2. **Identify the trigger** — What event caused or is causing the shift?
3. **Search for evidence of change:**
   - New supplier qualifications (search: 국산화 성공, 通过验证, 供給開始)
   - Capacity expansion announcements (환경영향평가, 工場建設, 新工場)
   - Trade flow changes (compare UN Comtrade data across years)
   - Patent filing shifts (new entrants filing in previously concentrated areas)
   - Equity research notes on supplier diversification
4. **Assess degree of change:**
   - Has actual market share shifted, or just announced intent?
   - Are new suppliers qualified for production or still in evaluation?
   - What's the timeline to meaningful diversification?

## Search Patterns for Change Detection

### Korean (국산화 / localization tracking):
```
[소재명] 국산화 성공     → "[material] localization success"
[소재명] 탈일본          → "[material] de-Japan"
[소재명] 공급선 이원화    → "[material] dual-sourcing"
[소재명] 대체 공급업체    → "[material] alternative supplier"
```

### Chinese (国产替代 / domestic substitution):
```
[材料名] 国产替代 进展    → "[material] domestic substitution progress"
[材料名] 国产化率         → "[material] localization rate"
[材料名] 填补国内空白     → "[material] fill domestic gap"
[公司名] 实现量产         → "[Company] achieved mass production"
```

### Japanese (supply chain restructuring):
```
{材料名} サプライチェーン 再編    → "[material] supply chain restructuring"
{材料名} 国内生産 強化           → "[material] domestic production strengthening"
{材料名} 調達先 分散             → "[material] procurement source diversification"
```

### Chinese — Taiwan (供應鏈變動):
```
[材料名] 供應鏈 變動              → "[material] supply chain change"
[材料名] 第二供應來源             → "[material] second supply source"
[材料名] 在地化                   → "[material] localization" (Taiwan phrasing)
[公司名] 供應商 調整              → "[company] supplier adjustment"
[材料名] 供應鏈 重組              → "[material] supply chain restructuring"
[公司名] 新供應商 導入            → "[company] new supplier introduction"
```

## Counterfactual check on causality

Before attributing a supply chain change to a specific cause, run the [Counterfactual Consistency Check](counterfactual-check.md). The key question: "Would this change have happened anyway, regardless of the trigger I'm attributing it to?" Example: Soulbrain gaining Korean HF market share after 2019 could be the 소부장 policy working, or it could be Samsung expanding capacity and needing more HF from any supplier. Separate correlation from causation.
