# Chemistry Chain Tracing Workflow
> Pipeline | Step 1: Starting Chemical | Step 2: CAS Lookup | Step 3: Tier-1 (Formulators) | Step 4: Tier-2 (Raw Materials) | Step 5: Tier-3 (Mining) | Step 6: Chokepoints | Step 6b: Counterfactual | Step 7: Patent Validation | Pitfalls | Output

**Question pattern:** "Trace [chemical X] from fab to mine" / "What's upstream of [material Y]?" / "Where does [precursor Z] come from?"

## Investigation Pipeline

```
User Question: "Trace [chemical X] from fab to mine"
    │
    ▼
┌─────────────────────────────────────┐
│  1. IDENTIFY STARTING CHEMICAL      │  What chemical does the fab use?
│     Patent CPC codes + EIA filings  │  Map process step → chemical → CAS
│     SEMI standards (purity grade)   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  2. CAS NUMBER LOOKUP               │  Pin down exact chemical identity
│     PubChem, Common Chemistry       │  Get all synonyms + trade names
│     Resolve ambiguous names         │  Sem-grade vs commodity-grade!
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  3. TIER-1: WHO MAKES SEM-GRADE?    │  Chemical registration DBs:
│     ECHA by CAS → EU registrants    │  ├── ECHA (EU)
│     K-REACH → Korean importers      │  ├── K-REACH (Korea)
│     EPA CDR → US manufacturing      │  ├── EPA CDR (US)
│     DART/EDINET/cninfo product      │  └── SEMICON exhibitor categories
│     disclosure sections             │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  4. TIER-2: RAW MATERIAL INPUTS     │  Filing procurement sections:
│     Synthesis route → feedstocks    │  ├── DART: 원재료 매입 현황
│     What goes IN to make this       │  ├── EDINET: 主要仕入先, 原材料の調達
│     chemical?                       │  ├── cninfo: 前五名供应商 (IPO = gold)
│     Trade data for intermediates    │  └── MOPS: 原物料供應狀況
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  5. TIER-3: MINING / EXTRACTION     │  USGS Mineral Commodity Summaries
│     Geological surveys              │  JOGMEC (Japan mineral dependency)
│     Mining company annual reports   │  Comtrade raw mineral flows
│     Conflict mineral reporting      │  Country production rankings
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  6. CHOKEPOINT ANALYSIS             │  At each tier:
│     Concentration metrics           │  ├── Top-1 share >50%? Monopoly risk
│     Geographic risk                 │  ├── Top-3 share >80%? Oligopoly
│     Substitutability                │  ├── Single-country >60%? Geo risk
│     Qualification cycle time        │  └── Cross-ref bottleneck.md
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  7. PATENT VALIDATION               │  CPC landscape for the chemistry
│     Synthesis/purification patents  │  ├── Who holds purification IP?
│     Co-assignee analysis            │  ├── New entrants filing?
│     New entrant detection           │  └── Confirms or extends the chain
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  8. OUTPUT                          │  ASCII tree diagram (fab → mine)
│     Chokepoint table per tier       │  Evidence chain with sources
│     Confidence grading per node     │  Gaps + recommended next steps
└─────────────────────────────────────┘
```

## Step 1: Identify the Starting Chemical

Given a fab process step, determine which chemicals are consumed.

### Process Step → CPC Code → Chemistry

| Fab Process Step | CPC Code(s) | What Patents Reveal |
|---|---|---|
| ALD (high-k, barrier) | C23C 16/455 | Precursor chemicals (TEMAH, TDMAH, TMA) |
| CVD (oxide, nitride) | C23C 16/44, C23C 16/50 | Source gases (TEOS, SiH4, NH3) |
| Sputtering (metals) | C23C 14/34 | Target materials (Cu, Ta, Ti, W, Co) |
| Photoresist formulation | G03F 7/004 | PAG, polymer resins, solvents |
| EUV resist | G03F 7/09 | Metal-oxide resists, CAR chemistry |
| CMP | B24B 37/044 | Slurry compositions (silica, ceria) |
| Crystal growth | C30B 15/ | Crucible materials, dopants, polysilicon |
| Wet etch/clean | C11D 7/, H01L 21/306 | HF, H2O2, H2SO4, NH4OH |
| HF purification | C01B 7/19 | Ultra-purification IP holders |
| Fluorine chemistry | C01B 7/20 | F2 production, fluorination |
| Rare earth separation | C22B 59/ | Ce, La processing for CMP |
| Silicon purification | C01B 33/035 | Siemens process, FBR polysilicon |

```
# Search: What ALD precursors does Samsung use?
Google Patents: CPC:C23C16/455 AND assignee:"Samsung Electronics"
→ reveals which precursor chemistries Samsung is actively developing
```

### Environmental filings reveal fab chemical inventories

```
# Korean (fab environmental impact assessments)
[fab명] 환경영향평가 사용 화학물질            → "[fab] EIA chemicals used"
[fab명] 유해화학물질 취급시설                  → "[fab] hazardous chemical handling facility"

# Japanese (mandatory PRTR toxic substance reporting)
{fab名} 環境影響評価 使用化学物質              → "[fab] EIA chemicals"
{fab名} PRTR 届出                             → "[fab] PRTR disclosure"

# Chinese — Mainland
[fab名] 环境影响评价 化学品                    → "[fab] EIA chemicals"
[fab名] 危险化学品 使用量                      → "[fab] hazardous chemical usage volume"

# Chinese — Taiwan
[fab名] 環評 化學品                            → "[fab] EIA chemicals"
```

## Step 2: CAS Number Lookup

Pin down exact chemical identity. Semiconductor chemicals often have trade names that differ from IUPAC names.

| Database | URL | Use |
|---|---|---|
| **PubChem** | pubchem.ncbi.nlm.nih.gov | Free API — CAS, synonyms, known manufacturers |
| **Common Chemistry** | commonchemistry.cas.org | CAS's own free lookup (authoritative) |
| **ChemSpider** | chemspider.com | Resolve ambiguous chemical names |

Example: "TEMAH" = tetrakis(ethylmethylamido)hafnium(IV), CAS 352535-01-4. Search ALL synonyms.

Cross-reference with CAS numbers in [chemistry/precursor-chains.md](../chemistry/precursor-chains.md).

## Step 3: Tier-1 Suppliers (Formulators / Purifiers)

"Who makes the semiconductor-grade product?"

### Chemical registration databases — search by CAS number

| Database | Jurisdiction | URL | What It Reveals |
|---|---|---|---|
| **ECHA REACH** | EU | echa.europa.eu | EU registrants by CAS — manufacturer name, tonnage band |
| **K-REACH** | Korea | kreach.me | Korean importers/manufacturers >1 tonne/year |
| **EPA CDR** | US | epa.gov/chemical-data-reporting | US manufacturing sites >25,000 lbs/year |
| **J-CHECK (NITE)** | Japan | nite.go.jp | Japanese substance classification |

```
# Example: Search ECHA for HF manufacturers
ECHA → search CAS 7664-39-3 → registration dossier → registrant list
→ reveals Solvay, Honeywell, Mexichem as EU registrants
→ tonnage band hints at production scale
```

### Filing product disclosure sections

```
# Korean — DART: what does the company make?
[회사명] 사업보고서 → 주요 제품 등의 현황         → what they manufacture
[회사명] 사업보고서 → 매출 현황                    → revenue by product

# Japanese — EDINET: business description
{会社名} 有価証券報告書 → 事業の内容               → business description
{会社名} 有価証券報告書 → セグメント情報           → segment breakdown

# Chinese — cninfo IPO prospectus (RICHEST SOURCE)
[公司名] 招股说明书 → 主营业务分析                 → what they make
[公司名] 招股说明书 → 前五名客户                   → who they sell to (often names fabs)
```

### SEMICON exhibitor category search

Search exhibitor directories for the specific material category (e.g., "ALD precursors", "CMP materials"). The exhibitor list IS the supplier list.

## Step 4: Tier-2 Suppliers (Raw Material Inputs)

"Who supplies raw materials to the chemical manufacturer?" This is the hardest step.

### Method A: Filing raw material procurement sections (most direct)

Each filing system has a section that discloses raw material purchases:

```
# Korean (DART) — CRITICAL SECTION
[화학업체명] 사업보고서 → 원재료 매입 현황          → "raw material purchase status"
→ Lists raw material names, suppliers, purchase amounts

# Japanese (EDINET)
{化学会社名} 有価証券報告書 → 主要仕入先            → "major suppliers"
{化学会社名} 有価証券報告書 → 事業等のリスク → 原材料の供給  → supply dependency in risk section
{化学会社名} → 原材料の調達                         → "raw material procurement"

# Chinese (cninfo) — IPO prospectuses are GOLD
[化学公司] 招股说明书 → 前五名供应商采购额          → top-5 suppliers BY NAME with amounts
[化学公司] 年报 → 原材料采购                        → raw material procurement details
[化学公司] 年报 → 供应商集中度                      → supplier concentration analysis

# Taiwan (MOPS)
[化學公司] 年報 → 原物料供應狀況                    → raw material supply situation
[化學公司] 年報 → 主要進貨廠商                      → main procurement vendors
```

### Method B: Multilingual web search for raw material sourcing

```
# Korean
[화학업체명] 원재료 조달                → "[chemical company] raw material procurement"
[화학업체명] 원료 공급업체              → "[chemical company] raw material supplier"
[원재료명] 원산지                       → "[raw material] origin"

# Japanese
{化学会社名} 原料調達                   → "[chemical company] raw material procurement"
{化学会社名} 主要仕入先                 → "[chemical company] major suppliers"
{原材料名} サプライチェーン             → "[raw material] supply chain"
{化学会社名} 調達リスク                 → "[chemical company] procurement risk"

# Chinese — Mainland
[化学公司] 上游原材料                   → "[chemical company] upstream raw materials"
[化学公司] 原材料供应商                 → "[chemical company] raw material supplier"
[原材料名] 上游产业链                   → "[raw material] upstream industry chain"

# Chinese — Taiwan
[化學公司] 上游原料                     → "[chemical company] upstream raw materials"
[化學公司] 原料來源                     → "[chemical company] raw material source"
```

### Method C: Chemical reaction pathway analysis

Work backwards from the final product through its synthesis to identify constrained feedstocks.

```
Example: NF3 synthesis
  NH3 + 3F2 → NF3 + 3HF
  → requires elemental fluorine (F2) → electrolysis of KF·2HF → requires HF → requires fluorspar (CaF2)
  → requires ammonia (NH3) → Haber-Bosch (commodity, unconstrained)
  Therefore: trace the FLUORINE chain, not the nitrogen chain
```

Sources for synthesis routes: PubChem, patent literature (CPC codes for synthesis methods), Ullmann's Encyclopedia of Industrial Chemistry.

### Method D: Trade data for raw material flows

Use HS codes from [trade/hs-codes.md](../trade/hs-codes.md):

```
Comtrade: HS 2529.21 (acid-grade fluorspar) → China exports to Japan
Comtrade: HS 2615.10 (zirconium ores) → Australia exports to France (CEZUS Hf separation)
e-Stat (Japan 9-digit): granular breakdown of imported raw chemicals
```

## Step 5: Tier-3 — Mining / Extraction

### Geological surveys and mineral databases

| Source | Country | URL | Key Minerals |
|---|---|---|---|
| **USGS Mineral Commodity Summaries** | US | minerals.usgs.gov | Comprehensive global data — production, reserves, companies |
| **Geoscience Australia** | Australia | ga.gov.au | Zircon, rare earths, lithium |
| **JOGMEC** | Japan | jogmec.go.jp | Japanese mineral import dependency reports |
| **KORES** | Korea | kores.or.kr | Korean mineral resource reports |
| **CAGS/MLR** | China | cgs.gov.cn | Chinese mineral production (limited) |

```
# USGS lookup
site:usgs.gov [mineral name] "mineral commodity summaries"
→ production by country, reserves, major producers, prices

# Mining company annual reports
"[mining company] annual report [mineral] production"
```

### Conflict mineral reporting (for Ta, Sn, W, Au — 3TG)

- SEC Form SD filings — US public companies must disclose 3TG sourcing
- RMI (Responsible Minerals Initiative) smelter lists
- Search: `[company] conflict minerals report`

### Multilingual mining/mineral searches

```
# Korean
[광물명] 광산 생산량                    → "[mineral] mine production"
[광물명] 수입 의존도                    → "[mineral] import dependency"
희소금속 공급망                         → "rare metal supply chain"

# Japanese
{鉱物名} 鉱山 生産量                   → "[mineral] mine production"
{鉱物名} 輸入依存度                    → "[mineral] import dependency"
JOGMEC {鉱物名} 鉱物資源マテリアルフロー → "JOGMEC [mineral] material flow"

# Chinese — Mainland
[矿物名] 矿山 产量                     → "[mineral] mine production"
[矿物名] 资源分布                       → "[mineral] resource distribution"
[矿物名] 全球储量                       → "[mineral] global reserves"

# Chinese — Taiwan
[礦物名] 進口依賴度                     → "[mineral] import dependency"
[礦物名] 來源國                         → "[mineral] source countries"
[礦物名] 供應風險                       → "[mineral] supply risk"
```

## Step 6: Chokepoint Analysis

At each tier in the traced chain, assess concentration risk.

### Metrics to calculate

- **Top-1 share >50%** → potential monopoly chokepoint
- **Top-3 combined >80%** → oligopoly chokepoint
- **Single-country >60%** → geographic concentration risk
- **Qualified suppliers ≤3** → semiconductor-grade scarcity (often the real bottleneck)
- **Qualification cycle** → 6-24 months for critical materials

### Red flags

- Only 1-3 facilities worldwide for a separation/purification step (e.g., Hf/Zr separation)
- Nuclear/defense dual-use linkage (Hf linked to Zr fuel rods, Ga/Ge to Chinese export controls)
- Geological uniqueness (Spruce Pine quartz — irreplaceable deposit)
- Cross-industry feedstock competition (fluorspar shared with EV battery LiPF6 production)

### Search for active diversification

```
# Korean
[소재명] 공급선 다변화                  → "[material] supply diversification"
[소재명] 국산화 추진                    → "[material] localization push"

# Japanese
{材料名} 調達先 分散                    → "[material] procurement diversification"
{材料名} セカンドソース                 → "[material] second source"

# Chinese — Mainland
[材料名] 国产替代 进展                  → "[material] domestic substitution progress"
[材料名] 自主可控                       → "[material] self-controllable"

# Chinese — Taiwan
[材料名] 第二供應商                     → "[material] second supplier"
```

Cross-reference with [queries/bottleneck.md](bottleneck.md) for deeper chokepoint assessment and [queries/change-detection.md](change-detection.md) for localization progress.

## Step 6b: Counterfactual check on chokepoints

Before validating with patents, run the [Counterfactual Consistency Check](counterfactual-check.md) on concentration claims. Challenge "Top-1 share >50%" if the figure comes from training knowledge or a single source. The key counterfactual for chokepoints: "What if a facility or supplier exists that I haven't found because they don't publish in the languages I searched?" Also check whether "qualified suppliers ≤3" means truly 3 worldwide, or 3 that you found.

## Step 7: Patent Validation

Use patent data to confirm and extend the chain independently.

```
# CPC landscape — who's active in this chemistry space?
Google Patents: CPC:[code] published:2020-2025
→ aggregate by assignee → all active players

# Synthesis method patents — what feedstocks does production require?
Google Patents: "[chemical name]" AND (synthesis OR preparation OR manufacturing)
→ reveals inputs, confirms reaction pathways

# Purification patents — who holds ultra-purification IP?
Google Patents: CPC:C01B7/191 AND assignee:"Stella Chemifa"
→ confirms dominance in HF purification

# Co-assignee — supply chain relationships
Google Patents: assignee:"[fab company]" AND assignee:"[chemical company]"
→ joint patents confirm collaboration on process chemistry
```

## Common Pitfalls

1. **Semiconductor-grade vs commodity-grade confusion.** Same CAS number, completely different supply chains. Electronic-grade polysilicon (11N, Wacker/Tokuyama/Hemlock) ≠ solar-grade polysilicon (6-9N, Tongwei/GCL/Daqo). Always specify purity.
2. **Trade name vs chemical name.** "TEMAH" in industry press = tetrakis(ethylmethylamido)hafnium(IV) in patents. Search BOTH.
3. **The chokepoint is almost never at the mine.** It's at the purification/separation facility. Fluorspar is abundant; ultra-pure HF purification is concentrated. Zircon sand is plentiful; Hf/Zr separation has ~4-5 facilities worldwide.
4. **Dual-use linkages create non-obvious risks.** Hafnium supply is coupled to nuclear fuel (Zr/Hf separation). Gallium/germanium are under Chinese export controls. These cross-industry dependencies are invisible if you only trace the semiconductor chain.
5. **Chinese tier-shifting.** Chinese tier-1 suppliers may themselves import key intermediates from Japan/Korea. The chain can loop through China and back. Always check 前五名供应商 in their IPO prospectus.
6. **Cross-industry feedstock competition.** Fluorspar feeds both semiconductor HF and EV battery LiPF6. Rare earths feed both CMP ceria and permanent magnets. Demand from adjacent industries affects semiconductor supply.

## Output Format

### Chain Diagram (ASCII tree, fab → mine)

```
[Chemical at fab] (at fab)
├── Tier-1: [Purifier/formulator companies]
│   └── [Intermediate chemical]
│       └── Tier-2: [Intermediate chemical producers]
│           └── [Raw material]
│               └── Tier-3: [Mining/extraction companies]
│                   └── [Ore/mineral] — [Country] [CHOKEPOINT if applicable]
```

### Chokepoint Assessment Table

```
| Tier | Node | Top Supplier(s) | Approx. Share | Geographic Risk | Substitution Difficulty |
|---|---|---|---|---|---|
```

### Evidence Chain

```
- Tier-1 identified via: [ECHA CAS lookup / DART filing / patent search]
- Tier-2 identified via: [원재료 매입 현황 / EDINET 主要仕入先 / IPO prospectus]
- Tier-3 identified via: [USGS Mineral Commodity Summary / mining company report]
```

### Confidence + Gaps

```
CONFIRMED nodes: [list with sources]
INFERRED nodes: [list with reasoning]
GAPS: [what could not be traced — "tier-2 supplier of X to Company Y unknown"]
Recommended verification: [specific next searches]
```
