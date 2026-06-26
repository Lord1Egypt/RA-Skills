# HS Codes for Semiconductor Materials Trade Tracking

## Primary Semiconductor HS Codes

| HS Code | Description | What it covers | Trackability |
|---|---|---|---|
| **3818.00** | Chemical elements/compounds doped for electronics | Silicon wafers, doped substrates | Excellent — very specific |
| **8486** | Semiconductor manufacturing equipment | All fab equipment | Excellent |
| 8486.10 | Ion implantation apparatus | Ion implanters | Good |
| 8486.20 | Lithography/exposure equipment | Steppers, scanners, EUV | Good |
| 8486.30 | Deposition/etch equipment | CVD, PVD, etch tools | Good |
| 8486.40 | Assembly/packaging equipment | Die bonders, wire bonders | Good |
| 8486.90 | Parts for semiconductor equipment | Replacement parts, components | Good |
| **3707.90** | Photographic chemical preparations | Photoresists | Good |
| **2811.11** | Hydrogen fluoride (HF) | Electronic-grade HF | Good |
| **2812.90** | Halides of non-metals | NF3, fluorine compounds | Moderate |
| **2804.61** | Silicon >99.99% purity | Semiconductor polysilicon | Good |
| **2529.21** | Fluorspar >97% CaF2 | Acid-grade fluorspar (HF feedstock) | Excellent |
| **2529.22** | Fluorspar <97% CaF2 | Metallurgical-grade | Good |
| **2615.10** | Zirconium ores/concentrates | Zircon sand (hafnium source) | Good |
| **2615.90** | Niobium/tantalum ores | Coltan, tantalite | Good |
| **2847.00** | Hydrogen peroxide | H2O2 (cleaning chemical) | Moderate (not semi-specific) |
| **3824.99** | Chemical preparations n.e.s. | CMP slurry, specialty chemicals | Poor — generic catch-all |
| **3405.90** | Polishes/creams | Some CMP slurries | Poor |
| **7108-7112** | Precious metals | Au, Ag, Pt bonding wire, targets | Poor — mixed with jewelry |

## Country-Specific Code Granularity

| Country | Digits | Notes |
|---|---|---|
| Japan | 9-digit | Very detailed for semiconductor materials |
| Korea | 10-digit HSK | Very detailed |
| Taiwan | 11-digit CCC | Excellent granularity |
| China | 10-digit | Reports to Comtrade but some opacity on strategic materials |
| USA | 10-digit HTS | Very detailed; Schedule B for exports |
| EU | 8-digit CN | Eurostat COMEXT database |

## Key Country Codes for Comtrade Queries

| Country | ISO Numeric | ISO Alpha |
|---|---|---|
| Japan | 392 | JPN |
| South Korea | 410 | KOR |
| USA | 842 | USA |
| China | 156 | CHN |
| Taiwan | 490 | — (reported as "Other Asia, nes") |
| Netherlands | 528 | NLD |
| Germany | 276 | DEU |
| France | 250 | FRA |
| Australia | 036 | AUS |

## Tracking Strategies

### Monitor Japan→Korea semiconductor materials flow (2019 dispute impact):
```
HS 3707 (photoresists): Japan→Korea, 2018-2024
HS 2811.11 (HF): Japan→Korea, 2018-2024
```

### Monitor equipment exports to China (export control impact):
```
HS 8486 (all semi equipment): Netherlands→China, 2020-2024
HS 8486 (all semi equipment): Japan→China, 2020-2024
HS 8486 (all semi equipment): USA→China, 2020-2024
```

### Monitor China's raw material imports:
```
HS 3818 (wafers): Japan→China + Korea→China
HS 3707 (photoresist): Japan→China
HS 2529.21 (fluorspar): China exports to world (dominance tracking)
```

## Chemical Registration Databases

For identifying who imports/manufactures specific chemicals:

| Database | Country | URL | Best approach |
|---|---|---|---|
| **ECHA** | EU | echa.europa.eu | Search by CAS number → see all EU registrants |
| **PubChem** | US/Global | pubchem.ncbi.nlm.nih.gov | Chemical properties, safety data, FREE API |
| **K-REACH** | Korea | kreach.me | Who imports >1 tonne into Korea |
| **EPA CDR** | US | epa.gov/chemical-data-reporting | US manufacturing sites above 25K lbs/yr |
| **J-CHECK** | Japan | nite.go.jp (CHRIP) | Substance classification (less company data) |

## Key CAS Numbers for Semiconductor Chemical Searches

| Chemical | CAS Number | Primary use |
|---|---|---|
| Hydrofluoric acid (HF) | 7664-39-3 | Oxide etch, wafer cleaning |
| Nitrogen trifluoride (NF3) | 7783-54-2 | Chamber cleaning gas |
| PGMEA | 108-65-6 | Photoresist solvent |
| TMAH | 75-59-2 | Photoresist developer |
| TEOS | 78-10-4 | CVD precursor (SiO2 deposition) |
| TEMAH | 352535-01-4 | ALD precursor (HfO2) |
| HMDS | 999-97-3 | Adhesion promoter for resists |
| Hydrogen peroxide (H2O2) | 7722-84-1 | Wafer cleaning (SC-1/SC-2) |
| Sulfuric acid (H2SO4) | 7664-93-9 | SPM cleaning |
| Phosphoric acid (H3PO4) | 7664-38-2 | 3D NAND staircase etch |
