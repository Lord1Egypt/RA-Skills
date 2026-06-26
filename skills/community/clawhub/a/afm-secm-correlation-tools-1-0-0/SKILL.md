# afm-secm-correlation-tools-1.0.0

AFM topography + SECM electrochemical activity correlation analyzer for electrocatalysis research.

## Overview

Combines atomic force microscopy (AFM) surface morphology data with scanning electrochemical microscopy (SECM) activity maps to reveal structure–activity relationships at the microscale. Identifies whether high electrochemical activity hotspots correspond to topographic features (particles, edges, grain boundaries) or are driven by chemical/electronic factors alone.

## Capabilities

### 1. Data Import
- **AFM**: SPI (.spm), JPK (.jpk Force Map), NT-MDT (.md), Asylum MFP-3D (.txt/.csv), Bruker (.ps), generic CSV (X/Y/Height/Z)
- **SECM**: CSV grid (X/Y/current), ASCII raster, CH Instruments, BioLogic, JPK, custom formats
- Auto-detects scan size, resolution, units (nm/μm/Å)

### 2. Image Preprocessing
- Leveling (1st/2nd order plane fit), flatten rows/columns
- Gaussian low-pass filter (remove high-frequency noise)
- Sharpen (Laplacian kernel) for edge enhancement
- Remove bow/tilt artifacts

### 3. Morphology Feature Extraction
- Roughness parameters: Ra (arithmetic), Rq (RMS), Rz (ten-point height), Rmax
- Grain segmentation (watershed algorithm), grain size distribution (mean Feret diameter)
- Particle detection: height threshold → equivalent circle diameter, aspect ratio, circularity
- Edge/boundary density: detected as high-gradient zones (∇z threshold)
- Bearing ratio and surface area ratio (complexity factor)

### 4. SECM Activity Map Processing
- Background subtraction (median filter), IQR outlier removal
- Normalization: min-max / z-score / relative to macroelectrode reference
- Hotspot detection: top 5–10% pixels (configurable threshold)
- Cross-section profile extraction (horizontal/vertical cuts)

### 5. AFM–SECM Co-registration & Correlation
- **Spatial overlay**: AFM topography heatmap + SECM activity contour, shared colorbar
- **Scatter plot**: local roughness (Ra in 8×8 windows) vs local SECM current, Pearson/Spearman r
- **Topographic masking**: correlation computed only where AFM height > grain boundary threshold
- **Hotspot mapping**: overlay AFM-detected particles with SECM hotspots → particle-activity contingency table
- **Dual-Y time-series**: tip position along cross-section vs height and current simultaneously
- Correlation coefficient classification: r < 0.3 (uncorrelated), 0.3–0.6 (moderate), > 0.6 (strong)

### 6. Reference Databases
- Built-in AFM tips: OLTEP (Au 111), PPP- kont AFMSPA (Si), SNL-10 (soft),q
- Built-in SECM tips: Pt ultramicroelectrode (10 μm), carbon fiber (10 μm), Au nanoelectrode (1 μm)
- Reaction type references: OER_NiOOH, HER_Pt, ORR_Au, CO2RR_Cu, Fe(CN)6³⁻/⁴⁻
- AFM roughness thresholds: Ra < 1 nm (ultrasmooth), 1–5 nm (smooth), 5–20 nm (rough), > 20 nm (very rough)

### 7. Output
- PNG 6-panel correlation dashboard (AFM / SECM / overlay / scatter / profile / statistics)
- Topographic feature table: grain size, particle density, edge density, activity
- Correlation summary CSV: r_Pearson, r_Spearman, p-value, N_windows
- Markdown full report with figure captions

## Usage

```bash
# Full analysis with AFM + SECM files
python afm_secm_correlation.py \
  --afm scan_afm.spm \
  --secm secm_map.csv \
  --output output_afm_secm/ \
  --afm-height-unit nm \
  --secm-current-unit nA \
  --secm-tip-diameter 10 \
  --reaction-type OER_NiOOH

# Quick correlation scatter plot only
python afm_secm_correlation.py \
  --afm scan_afm.spm \
  --secm secm_map.csv \
  --mode scatter \
  --output quick_corr/

# Grid correlation (8x8 windows)
python afm_secm_correlation.py \
  --afm scan_afm.spm \
  --secm secm_map.csv \
  --mode grid-corr \
  --window-size 8 \
  --output grid_corr/
```

## File Formats

| Instrument | AFM Format | SECM Format |
|-----------|-----------|-------------|
| Asylum MFP-3D | .ibw, .txt | CSV grid |
| JPK Instruments | .jpk | CSV grid |
| Bruker / Veeco | .spm, .000 | ASCII |
| NT-MDT | .md, .msr | CSV |
| CH Instruments | — | .jdx |
| BioLogic | — | .mpt |
| Generic | CSV (X/Y/Z) | CSV (X/Y/I) |

## Dependencies
- numpy, scipy, matplotlib, pandas, scikit-image, lmfit, opencv-python (cv2)
