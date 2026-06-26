# AutoMD-Viz

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Billwanttobetop/automd-viz)

**Publication-Quality Visualization for Molecular Dynamics Simulations**

Generate journal-ready figures from MD simulation data with one command. Supports Nature, Science, and Cell journal styles.

---

## ✨ Features

- 🎨 **Molecular Structure Visualization** - High-quality PyMOL rendering
- 📊 **Data Plotting** - Publication-ready charts with Matplotlib/Seaborn
- 🎬 **Trajectory Visualization** - PCA, t-SNE, UMAP projections
- 📦 **Automated Reports** - One-click figure generation
- 🎯 **Journal Styles** - Nature, Science, Cell presets
- 🔧 **High Resolution** - 300-600 DPI, vector formats (SVG/PDF/EPS)

---

## 🚀 Quick Start

### Installation

```bash
# Via ClawHub (recommended)
clawhub install automd-viz

# Or clone from GitHub
git clone https://github.com/Billwanttobetop/automd-viz.git
cd automd-viz
chmod +x automd-viz.sh
```

### Basic Usage

```bash
# Generate protein structure figure
./automd-viz.sh --type structure --structure protein.pdb --style nature

# Plot time-series data
./automd-viz.sh --type data --input rmsd.xvg --style science

# Visualize trajectory
./automd-viz.sh --type trajectory --structure protein.pdb --trajectory md.xtc

# Generate complete report
./automd-viz.sh --type report --input analysis-results/ --style nature
```

---

## 📊 Visualization Types

### 1. Structure Visualization

Generate high-quality molecular structure figures.

```bash
./automd-viz.sh --type structure \
  --structure protein.pdb \
  --style nature \
  --representation cartoon \
  --color spectrum \
  --resolution 600
```

**Output:** High-resolution PNG + PyMOL session file

### 2. Data Plotting

Plot RMSD, RMSF, energy, and other time-series data.

```bash
./automd-viz.sh --type data \
  --input rmsd.xvg \
  --style science \
  --xlabel "Time (ns)" \
  --ylabel "RMSD (nm)"
```

**Output:** PDF (vector) + PNG (raster)

### 3. Trajectory Visualization

Visualize conformational space with dimensionality reduction.

```bash
./automd-viz.sh --type trajectory \
  --structure protein.pdb \
  --trajectory md.xtc \
  --method pca \
  --style nature
```

**Output:** 2D/3D projections + Free energy landscape

### 4. Automated Report

Generate a complete set of publication-ready figures.

```bash
./automd-viz.sh --type report \
  --structure protein.pdb \
  --trajectory md.xtc \
  --input analysis-results/ \
  --style nature
```

**Output:** Complete figure set + Summary report

---

## 🎨 Journal Styles

| Style | Font | Size | Line Width | Format |
|-------|------|------|------------|--------|
| **Nature** | Arial | 7-9 pt | 0.5-1.0 pt | PDF/EPS |
| **Science** | Helvetica | 8-10 pt | 0.75-1.25 pt | PDF/EPS |
| **Cell** | Arial | 8-12 pt | 1.0-1.5 pt | PDF/EPS |

All styles use colorblind-friendly palettes.

---

## 🔧 Dependencies

**Required:**
- Python 3.7+
- NumPy
- Matplotlib
- Seaborn

**Optional:**
- PyMOL (structure visualization)
- scikit-learn (PCA/t-SNE)
- umap-learn (UMAP)
- MDAnalysis (trajectory processing)

**Install all dependencies:**
```bash
pip install numpy matplotlib seaborn scikit-learn umap-learn MDAnalysis
```

---

## 🤝 Integration with AutoMD-GROMACS

AutoMD-Viz works seamlessly with [AutoMD-GROMACS](https://github.com/Billwanttobetop/automd-gromacs) analysis results.

```bash
# Run GROMACS analysis
advanced-analysis -s md.tpr -f md.xtc

# Visualize results
automd-viz --type report --input advanced-analysis/ --style nature
```

**Supported analysis outputs:**
- Basic analysis (RMSD/RMSF/Rg)
- Advanced analysis (PCA/Clustering/DCCM)
- Binding analysis (MM-PBSA/Interactions)
- Trajectory analysis (MSM/TPT)
- Property analysis (Diffusion/Viscosity)

---

## 📖 Examples

See the [examples/](examples/) directory for complete workflows:

- **Protein structure** - Lysozyme visualization
- **Protein-ligand** - Binding site analysis
- **Membrane protein** - Lipid bilayer system
- **Trajectory analysis** - Conformational dynamics

---

## 🐛 Troubleshooting

**Common issues:**

1. **PyMOL not found**
   ```bash
   # Install PyMOL
   conda install -c conda-forge pymol-open-source
   # Or use --no-structure flag
   ```

2. **Font issues**
   ```bash
   # Use fallback fonts
   ./automd-viz.sh --font-fallback
   ```

3. **Memory errors**
   ```bash
   # Reduce trajectory frames
   ./automd-viz.sh --stride 10
   ```

See [publication-viz-errors.md](publication-viz-errors.md) for detailed troubleshooting.

---

## 📚 Documentation

- [SKILL.md](SKILL.md) - Complete usage guide
- [publication-viz-errors.md](publication-viz-errors.md) - Troubleshooting guide
- [examples/](examples/) - Example workflows

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Author:** Xuan Guo  
**Email:** xguo608@connect.hkust-gz.edu.cn  
**GitHub:** [@Billwanttobetop](https://github.com/Billwanttobetop)

---

## 🌟 Citation

If you use AutoMD-Viz in your research, please cite:

```bibtex
@software{automd_viz,
  author = {Guo, Xuan},
  title = {AutoMD-Viz: Publication-Quality Visualization for Molecular Dynamics},
  year = {2026},
  url = {https://github.com/Billwanttobetop/automd-viz}
}
```

---

## 🔗 Related Projects

- [AutoMD-GROMACS](https://github.com/Billwanttobetop/automd-gromacs) - Automated GROMACS workflows
- [AutoMD-AMBER](https://github.com/Billwanttobetop/automd-amber) - AMBER automation (planned)
- [AutoMD-NAMD](https://github.com/Billwanttobetop/automd-namd) - NAMD automation (planned)

---

**Made with ❤️ for the MD community**
