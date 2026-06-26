# Dataset Splitter

Split image datasets into train/val/test sets. Supports random split, stratified split, and custom ratios. Use when user needs to split dataset for machine learning training.

## Features

- **Random Split**: Randomly shuffle and split
- **Stratified Split**: Maintain class distribution
- **Custom Ratios**: Configurable train/val/test ratios
- **Annotation Support**: Split images and corresponding annotations together
- **YOLO Format**: Generate YOLO format dataset structure
- **Reproducible**: Set random seed for reproducibility

## Usage

```bash
# Simple split (80/10/10)
python scripts/splitter.py split /path/to/images/ --ratios 80 10 10

# With annotations
python scripts/splitter.py split /path/to/images/ --annotations /path/to/labels/

# YOLO format output
python scripts/splitter.py split /path/to/images/ --output /path/to/dataset/ --yolo

# Stratified by class
python scripts/splitter.py split /path/to/images/ --annotations labels/ --stratify
```

## Examples

```
$ python scripts/splitter.py split ./images --ratios 80 10 10

Splitting dataset...
Total images: 1000
Train: 800 (80%)
Val: 100 (10%)
Test: 100 (10%)

✓ Created train/ (800 images)
✓ Created val/ (100 images)
✓ Created test/ (100 images)
```

## Installation

```bash
pip install pillow
```

## Options

- `--ratios`: Split ratios (train val test), default: 80 10 10
- `--seed`: Random seed for reproducibility
- `--annotations`: Path to annotations (will be split together)
- `--output`: Output directory
- `--yolo`: Output in YOLO dataset format
- `--stratify`: Maintain class distribution
- `--copy`: Copy files instead of moving
