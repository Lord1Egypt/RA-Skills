# Semiconductor Material Chemistry Chains

> 1. Photoresist | 2. Hafnium Precursor | 3. High-Purity HF | 4. NF3 | 5. Silicon Wafer | 6. CMP Slurry | 7. Sputtering Target (Cu) | 8. Tungsten / Molybdenum | CAS Numbers

Trace-back from fab to mine for critical materials. Use this to understand tier-2 and tier-3 dependencies.

Every chain, company name, and share figure below is a lead, not a verified map. The chain
structures show what the landscape might look like. Your investigation should verify these
connections, find where they're wrong, and discover nodes or suppliers that aren't listed.
Share figures are training-data estimates (~2023-2024). [VERIFY] tags mark concentration
claims that are worth investigating but not worth citing without fresh evidence.

## 1. Photoresist Chain

```
EUV/ArF resist (at fab)
├── Resist formulators: JSR, TOK (4186.T), Shin-Etsu (4063.T), Sumitomo Chemical, Fujifilm, DuPont
│   ├── Photoacid generators (PAGs)
│   │   └── Toyo Gosei (4970.T) — suspected dominant [VERIFY]
│   │   └── San-Apro, Heraeus (smaller)
│   ├── Resist polymer resins/monomers
│   │   └── Osaka Organic Chemical (4187.T) — acrylic/methacrylic monomers
│   │   └── Daicel (4202.T) — adamantane monomers for ArF
│   │   └── Maruzen Petrochemical — hydroxystyrene polymers for KrF
│   └── Solvents (semiconductor-grade PGMEA, PGME)
│       └── Tokuyama (4043.T), Daicel, Dow, LyondellBasell
│           └── Propylene oxide → petrochemical crackers (commodity)
```
**Investigate:** Toyo Gosei PAG concentration. Japan reportedly dominates resist formulation.

## 2. Hafnium Precursor Chain (High-k Gate Dielectric)

```
HfO2 film via ALD (at fab)
├── TEMAH/TDMAH precursor
│   └── Entegris (US), Adeka (4401.T, Japan), UP Chemical (Korea), DNF (092070.KQ, Korea), SK Trichem (Korea)
│       ├── Hafnium tetrachloride (HfCl4)
│       │   └── ATI Allegheny (US), CEZUS/Framatome (France), Materion (US)
│       │       ├── Hafnium metal / HfO2
│       │       │   └── CEZUS/Orano (France) — reported largest [VERIFY]
│       │       │   └── ATI/Wah Chang (Albany, OR, USA)
│       │       │   └── State Nuclear Baotou (China)
│       │       │       ├── Hf/Zr SEPARATION — only ~4-5 facilities worldwide
│       │       │       │   (Nuclear byproduct: Zr without Hf needed for fuel rods)
│       │       │       │   └── CEZUS (Jarrie, France), ATI (Albany, OR), Westinghouse (Ogden, UT), CNNC Baotou (China)
│       │       │       └── Zircon sand (ZrSiO4) mining
│       │       │           └── Iluka Resources (Australia, ASX: ILU) — world's largest
│       │       │           └── Tronox (US/Australia/South Africa)
│       │       │           └── Rio Tinto (Richards Bay, South Africa)
│       │       │           └── Kenmare Resources (Mozambique, LSE: KMR)
```
**Investigate:** CEZUS/Framatome reported Hf production dominance. Hf supply linked to nuclear fuel industry (Zr/Hf separation coupling).

## 3. High-Purity HF Chain

```
Electronic-grade HF (UHPA, <1ppb metals, at fab)
├── Ultra-purification (multi-stage distillation)
│   └── Stella Chemifa (4109.T, Japan) — believed top globally [VERIFY]
│   └── Morita Chemical (Japan, private) [VERIFY]
│   └── Daikin (6367.T), Solvay (Belgium), Honeywell (US), Do-Fluoride (002407.SZ, China)
│       ├── Technical-grade anhydrous HF
│       │   └── Mexichem/Orbia (Mexico), Honeywell, Solvay, Juhua Group (China), Dongyue Group (China, 0189.HK)
│       │       └── Fluorspar (CaF2) mining — acid-grade >97%
│       │           └── China reportedly dominant in global supply [VERIFY]
│       │           └── Mexico (Orbia operations)
│       │           └── South Africa, Vietnam, Kenya
```
**Investigate:** Stella Chemifa reported purification dominance. China reported fluorspar dominance. Central to 2019 Japan-Korea dispute (historically confirmed).

## 4. NF3 (Chamber Cleaning Gas) Chain

```
NF3 gas (at fab)
├── SK Specialty/SK Materials (Korea) — suspected major global position [VERIFY]
├── Kanto Denka Kogyo (4047.T, Japan)
├── Hyosung Chemical (298000.KS, Korea)
├── Central Glass (4044.T, Japan), Mitsui Chemicals (Japan), Air Products (US), Linde
│   ├── Synthesis: NH3 + 3F2 → NF3 + 3HF
│   │   ├── Elemental fluorine (F2) — electrolysis of KF·2HF (Simons process)
│   │   └── Ammonia (NH3) — Haber-Bosch (commodity)
│   └── All feeds back to HF/fluorspar chain (same upstream as #3)
```

## 5. Silicon Wafer Chain

```
300mm polished/epitaxial wafer (at fab)
├── Shin-Etsu Handotai/SEH (Japan, parent 4063.T) — suspected major position
├── SUMCO (3436.T, Japan) — suspected major position
├── Siltronic (WAF.DE, Germany)
├── SK Siltron (Korea, SK subsidiary)
├── GlobalWafers (6488.TWO, Taiwan)
│   ├── Czochralski crystal growth from polysilicon melt
│   │   ├── Electronic-grade polysilicon (11N purity)
│   │   │   └── Wacker Chemie (WCH.DE, Germany) — largest
│   │   │   └── Tokuyama (4043.T, Japan)
│   │   │   └── Hemlock Semiconductor (US; Corning Inc. 80.5%, Shin-Etsu Handotai 19.5%; $325M CHIPS Act funding for new facility)
│   │   │   └── REC Silicon (Norway/US)
│   │   │   NOTE: Solar-grade poly (6-9N) is a DIFFERENT market (Tongwei, GCL, Daqo = China)
│   │   │       ├── Trichlorosilane (TCS) reduction (Siemens process)
│   │   │       │   └── Metallurgical-grade silicon (MG-Si)
│   │   │       │       └── Carbothermic reduction of quartz
│   │   │       │       └── Elkem (Norway/China), Ferroglobe (Spain/US), Chinese producers
│   │   │       │       └── China suspected dominant in MG-Si
│   │   │       └── Quartz / silica sand
│   │   │           └── Spruce Pine, NC (USA) — reported highest purity globally, suspected dominant to near-monopoly in world HPQ supply [VERIFY]
│   │   │           └── Sibelco ($200M expansion to double capacity + $500M "Expansion 2" for 2024-2027)
│   │   │           └── The Quartz Corp (Imerys/Norsk Mineral JV)
│   │   └── Quartz crucibles (for CZ pulling)
│   │       └── Ferrotec (6890.T, Japan) — suspected major position
│   │       └── Shin-Etsu Quartz (Japan)
```
**Investigate:** Spruce Pine quartz concentration (unique geology claim). Shin-Etsu+SUMCO suspected combined dominance in 300mm wafers. Wacker+Hemlock+Tokuyama reported to control semiconductor-grade poly.

## 6. CMP Slurry Chain

```
CMP slurry (at fab)
├── Entegris/CMC Materials (US) — #1
├── Fujimi (5384.T, Japan)
├── AGC (5201.T, Japan)
├── Anji Microelectronics (688019.SS, China)
│   ├── Colloidal silica nanoparticles (for oxide CMP)
│   │   └── Fuso Chemical (4368.T, Japan) — reported dominant [VERIFY]
│   │   └── Evonik (Germany), Nippon Shokubai (Japan)
│   └── Ceria (CeO2) nanoparticles (for STI CMP)
│       └── Solvay/Rhodia (Belgium)
│       └── Rare earth separation
│           └── China Northern Rare Earth (600111.SS) — China reportedly dominant in RE processing [VERIFY]
│           └── Lynas (Australia, ASX: LYC), MP Materials (US, NYSE: MP)
│           └── Ore: bastnasite, monazite, ion-adsorption clays
│               └── China (Bayan Obo), USA (Mountain Pass), Australia (Mt Weld)
```

## 7. Sputtering Target Chain (Copper)

```
Ultra-high-purity Cu target (6N+, at fab)
├── JX Advanced Metals (5016.T, TSE Prime since March 2025; ENEOS retains ~49.9%) — believed top globally [VERIFY]
├── Mitsubishi Materials (5711.T, Japan)
├── Honeywell (US), Linde Electronics
│   ├── 6N copper electrolytic refining
│   │   └── JX Advanced Metals, Mitsubishi Materials, Sumitomo Metal Mining
│   └── LME-grade copper cathode
│       └── Codelco (Chile), Freeport-McMoRan (US), BHP (Australia), Glencore
│       └── Copper ore mining: Chile (largest producer), Peru, DRC, Zambia, Argentina (emerging)

Tantalum target chain:
├── JX Advanced Metals, H.C. Starck/Masan HT (Germany/Vietnam), Plansee (Austria)
│   └── Ta metal processing
│       └── Global Advanced Metals (Australia), Ningxia Orient Tantalum (China)
│       └── Coltan/tantalite ore: DRC reportedly dominant in artisanal supply [CONFLICT MINERAL]
│       └── Also: tin slag (Malaysia/Thailand secondary source)
```

## 8. Tungsten / Molybdenum Interconnect Transition

```
WF6 → CVD tungsten fill (contact/via, current mainstream)
├── Linde (US/Germany), SK Specialty (Korea), Guangdong Huate (688268.SS, China)
│   └── Tungsten hexafluoride from W metal + F2
│       └── China suspected dominant in tungsten supply [VERIFY]
│       └── Almonty Industries (Sangdong mine, Korea, producing Dec 2025) — largest non-China project
│       └── Pure Tungsten (Ssangjon mine, Korea, first concentrate Jun 2026)

Mo precursor → ALD/CVD molybdenum (emerging replacement at sub-2nm nodes)
├── Air Liquide (Korea Mo precursor plant, inaugurated 2025) — first dedicated facility
│   └── Molybdenum metal/compounds
│       └── China suspected dominant in Mo mine production [VERIFY]
│       └── Chile (Codelco), USA (Freeport), Peru (copper mining byproduct)
```
**Investigate:** If Mo deposition reaches HVM at sub-2nm nodes, WF6 demand growth slows. Watch Air Liquide Korea capacity and TSMC/Samsung process announcements.

## Key CAS Numbers for Chemical Database Searches

| Chemical | CAS Number | Use |
|----------|-----------|-----|
| Hydrofluoric acid (HF) | 7664-39-3 | Oxide etch, wafer cleaning |
| Nitrogen trifluoride (NF3) | 7783-54-2 | CVD chamber cleaning |
| PGMEA | 108-65-6 | Photoresist solvent |
| TMAH | 75-59-2 | Photoresist developer |
| TEOS | 78-10-4 | CVD precursor (SiO2) |
| TEMAH | 352535-01-4 | ALD precursor (HfO2) |
| HMDS | 999-97-3 | Adhesion promoter |
| Hydrogen peroxide | 7722-84-1 | Wafer cleaning (SC-1/SC-2) |
