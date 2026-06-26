---
name: rice-phenotype-prediction
description: >-
  Predict rice agronomic traits (yield, plant height, heading date, grain size, etc.)
  from genotype and environmental data using pre-trained MMoE deep learning models.
  Use when the user asks about rice phenotype prediction, crop trait estimation,
  genotype-environment interaction, or environmental stress effects on rice.
  Supports Chinese and English. Trigger terms: 水稻, 表型, 预测, 株高, 产量, 粒长,
  抽穗期, 千粒重, 结实率, rice, phenotype, yield, trait, stress.
---

# Rice Phenotype Prediction

Self-contained skill for predicting 10 rice agronomic traits via pre-trained MMoE models.
All models, data, and scripts are inside this directory — give users this one folder.

## Setup

### First-time check
```bash
python <SKILL_DIR>/scripts/check_env.py
```
This verifies Python dependencies and data integrity. If packages are missing:
```bash
pip install -r <SKILL_DIR>/requirements.txt
```

Required: `torch>=2.0 numpy pandas scikit-learn scipy requests`
GPU is optional — CPU works (just slower). If GPU is present, `cuda:0` is used automatically.

### `<SKILL_DIR>` convention

Throughout this file, `<SKILL_DIR>` means the absolute path to this skill's root directory
(the folder containing this SKILL.md). When running commands, substitute with the actual path.
`--base_dir` is optional; if omitted, scripts auto-detect it from their own location.

## Supported Traits

| Code | Chinese | English | Unit |
|------|---------|---------|------|
| HD | 抽穗期 | Heading Date | days |
| PH | 株高 | Plant Height | cm |
| PL | 穗长 | Panicle Length | cm |
| TN | 分蘖数 | Tiller Number | count |
| GP | 每穗粒数 | Grains Per Panicle | count |
| SSR | 结实率 | Seed Setting Rate | % |
| TGW | 千粒重 | Thousand Grain Weight | g |
| GL | 粒长 | Grain Length | mm |
| GW | 粒宽 | Grain Width | mm |
| Y | 产量 | Yield | kg/ha |

## Supported Locations (7 built-in stations)

| Code | City | Lat | Lon |
|------|------|-----|-----|
| km | 昆明 | 25.02 | 102.68 |
| gzl | 六盘水 | 26.59 | 104.83 |
| nn | 南宁 | 22.82 | 108.37 |
| wh | 武汉 | 30.58 | 114.27 |
| hf | 合肥 | 31.82 | 117.25 |
| hz | 杭州 | 30.25 | 120.17 |
| th | 通化 | 41.73 | 125.94 |

Any input lat/lon is auto-matched to the nearest station via Haversine distance.
For locations with internet, daily weather data can also be fetched from NASA POWER API for the exact coordinates.

## Stress Types

| Type | Chinese | Default effect |
|------|---------|----------------|
| high_temp | 高温胁迫 | +3°C max / +2°C min |
| low_temp | 低温胁迫 | -3°C max / -2°C min |
| drought | 干旱胁迫 | 90% precipitation reduction |
| flood | 涝害胁迫 | 3x precipitation increase |
| low_light | 寡照胁迫 | 60% PAR reduction |

## Prediction Commands

### Full prediction (recommended)
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1
```

### Genotype-only / environment-only
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --mode gene
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --mode env
```

### Specific traits
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --trait PH,Y
```

### With stress
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --stress high_temp
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --stress high_temp --stress_delta 5.0
```

### Multiple samples
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample "sample1,sample2,sample3"
```

### Custom genotype file
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --genotype_file /path/to/user_vae.csv
```
Format: CSV with 1024 columns (VAE-encoded features), first column = sample index.

### Force CPU / specific device
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --device cpu
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --device cuda:0
```

### Human-readable table
```bash
python <SKILL_DIR>/scripts/predict.py --lat 30.5 --lon 114.3 --sample sample1 --output table
```

### All CLI arguments
| Arg | Default | Description |
|-----|---------|-------------|
| `--lat` | required | Latitude |
| `--lon` | required | Longitude |
| `--sample` | None | Built-in sample ID(s), comma-separated (sample1..sample3925) |
| `--genotype_file` | None | Custom 1024-dim VAE CSV path |
| `--mode` | full | `gene`, `env`, or `full` |
| `--trait` | all | Comma-separated trait codes or `all` |
| `--stress` | None | Stress type name |
| `--stress_delta` | None | Override temperature delta |
| `--device` | auto | `auto`, `cpu`, or `cuda:0` |
| `--year` | 2024 | Year for environmental data |
| `--output` | json | `json` or `table` |
| `--base_dir` | auto | Override skill directory path |

## Handling User Requests

### 1. Extract location
- "经纬度30.5, 114.3" → `--lat 30.5 --lon 114.3`
- "武汉" → `--lat 30.58 --lon 114.27`
- "北纬25度，东经103度" → `--lat 25 --lon 103`

### 2. Map trait names
- 株高/plant height → PH
- 产量/yield → Y
- 粒长/grain length → GL
- 抽穗期/heading date → HD
- 千粒重/1000-grain weight → TGW
- 穗长/panicle length → PL
- 结实率/seed setting rate → SSR
- 每穗粒数/grains per panicle → GP
- 粒宽/grain width → GW
- 分蘖数/tiller number → TN

### 3. Map stress requests
- 高温/heat → high_temp
- 低温/cold/chilling → low_temp
- 干旱/drought → drought
- 洪涝/flooding → flood
- 阴天/寡照/low light → low_light
- "高温+5度" → `--stress high_temp --stress_delta 5.0`

### 4. Genotype data
- Built-in samples: `--sample sample1` (3925 available: sample1..sample3925)
- User file: `--genotype_file /path/to/file.csv`

### 5. Interpreting output
JSON contains: `location`, `genotype_prediction`, `environment_prediction`, `stress_prediction`, `trait_info`.

Report `environment_prediction` as primary (has environmental context).
Compare `genotype_prediction` as baseline.
For stress, compare normal vs stressed values.

Rounding: HD/TN/GP → integer, PH/PL/TGW/SSR → 1 decimal, GL/GW → 2 decimals, Y → integer.

## Directory Structure
```
rice_prediction/                   ← give users this folder
├── SKILL.md                       ← this file
├── requirements.txt               ← pip dependencies
├── data/
│   ├── grid_points.json           ← 7 station coordinates
│   ├── vae_features.csv           ← 3925 built-in genotype samples (1024-dim VAE)
│   ├── season_history.csv         ← historical season data for normalization
│   ├── env_cache/                 ← cached daily weather (auto-populated)
│   ├── models_env/                ← 10 trait-specific env+gene models (~4.6MB each)
│   └── models_gene/               ← 7 location-specific genotype models (~8MB each)
└── scripts/
    ├── predict.py                 ← main entry point
    ├── check_env.py               ← dependency checker
    ├── model_def.py               ← MMoE model architectures
    ├── grid_manager.py            ← nearest grid point finder
    ├── env_data_fetcher.py        ← NASA POWER API fetcher + cache
    ├── env_processor.py           ← environmental feature engineering
    └── stress_simulator.py        ← stress scenario simulation
```

## Architecture (for reference)
- **Model**: Multi-gate Mixture-of-Experts (MMoE) with ResidualMLP experts
- **Genotype features**: 1024-dim VAE latent encoding of genomic data
- **Environment features**: 53 season-aggregated variables from daily weather
- **Environmental data**: NASA POWER API (auto-fetched and cached locally)
