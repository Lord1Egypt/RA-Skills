# SKILL.md — AFM Force Curve Analyzer

## Tool Name
`afm-force-curve-analyzer` — AFM nanoindentation & force spectroscopy data analyzer

## When to Use
When analyzing AFM force-distance curves, nanoindentation data, adhesion maps, or force spectroscopy measured during electrochemical cycling (LSV/CV/CP/CA). Triggers on phrases like:
- "AFM force curve分析"
- "force spectroscopy"
- "nanoindentation"
- "adhesion force"
- "Young's modulus AFM"
- "Sneddon模型"

## Analysis Capabilities
- Force-distance (F-D) curve import & preprocessing (baseline subtraction, tip radius correction)
- Young's modulus extraction via Sneddon model (cone/pyramid/spherical indenters)
- Adhesion force (F_ad) & pull-off work calculation
- Multiple indentation models: Hertz, Sneddon (cone/pyramid), JKR, DMT
- Electrochemical potential correlation: modulus/adhesion vs. applied potential
- Deformation recovery analysis (creep/viscoelastic relaxation)
- Force map 2D visualization (adhesion, modulus, deformation)
- Multi-curve statistical comparison (fresh vs. cycled catalyst)
- Built-in reference database: NiOOH/γ-NiOOH/FeOOH/IrO₂/RuO₂/TiO₂/LiCoO₂/Si/Pt/Au

## Input Formats
- CSV/XLSX ( Asylum MFP-3D / Bruker Nanoscope / JPK / NT-MDT / Keysight / Park )
- TXT (force curve single file, force map grid CSV)
- NWI (Nanonis)
- SXM (NT-MDT)

## Output
- PNG multi-panel dashboard (F-D curves + statistics + potential correlation + 2D map)
- CSV with all extracted parameters
- JSON with metadata
- Markdown summary report

## Key Calculations
- Sneddon model: E = (π/2) × F / (δ² × tan α) for conical indenter
- Adhesion work: W_ad = ∫F_ad dδ
- Reduced modulus: 1/E_r = (1−ν²)/E + (1−ν_tip²)/E_tip
- Standard indenters: ν_sample=0.3 (NiOOH), ν_tip=0.17 (SiN), E_tip=97 GPa (SiN)

## Usage
```bash
afm-force-curve-analyzer --input data.csv --indenter conical --tip-radius 20e-9 \
  --poisson 0.3 --output ./results --format png,csv,json,md
```

## Author
Labclaw 🦎 — built 2026-04-17
