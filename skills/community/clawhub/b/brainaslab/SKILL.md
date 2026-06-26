# BrainASLab — FreeSurfer Asymmetry Analyzer

Upload FreeSurfer `lh.aparc.stats` and `rh.aparc.stats`.

This skill automatically:
- Parses cortical ROI metrics
- Computes Asymmetry Index (AS) for Thickness, Area, and Volume
- Generates publication-ready plots
- Outputs AS_results.csv

## Input
- lh.aparc.stats
- rh.aparc.stats

## Output
- AS_results.csv
- AS_bar_*.png
- AS_hist_*.png

## Requirement
- Matlab installed and available in PATH