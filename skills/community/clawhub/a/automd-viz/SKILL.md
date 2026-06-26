# AutoMD-Viz - Publication-Quality Visualization for Molecular Dynamics

**Version:** 1.0.0  
**Author:** Xuan Guo (xguo608@connect.hkust-gz.edu.cn)  
**License:** MIT  
**Repository:** https://github.com/Billwanttobetop/automd-viz

---

## 📖 Overview

AutoMD-Viz is a standalone visualization toolkit for generating publication-quality figures from molecular dynamics simulation data. It supports multiple visualization types and journal-specific styles (Nature, Science, Cell).

**Key Features:**
- 🎨 Molecular structure visualization (PyMOL)
- 📊 Data plotting (Matplotlib/Seaborn)
- 🎬 Trajectory visualization (PCA/t-SNE/UMAP)
- 📦 Automated report generation
- 🎯 Journal-specific styles (Nature/Science/Cell)
- 🔧 High-resolution output (300-600 DPI, SVG/PDF/EPS)

---

## 🚀 Quick Start

### Installation

```bash
# Via ClawHub
clawhub install automd-viz

# Or manual installation
git clone https://github.com/Billwanttobetop/automd-viz.git
cd automd-viz
chmod +x automd-viz.sh
```

### Basic Usage

```bash
# Generate protein structure figure
./automd-viz.sh --type structure --structure protein.pdb --style nature

# Plot RMSD/RMSF data
./automd-viz.sh --type data --input rmsd.xvg --style science

# Trajectory visualization (PCA)
./automd-viz.sh --type trajectory --structure protein.pdb --trajectory md.xtc

# Generate complete report
./automd-viz.sh --type report --structure protein.pdb --trajectory md.xtc --style nature
```

---

## 📋 Visualization Types

### 1. Structure Visualization (`--type structure`)

Generate high-quality molecular structure figures using PyMOL.

**Options:**
- `--structure <file>` - Input structure (PDB/GRO)
- `--style <nature|science|cell>` - Journal style
- `--representation <cartoon|surface|sticks>` - Display style
- `--color <spectrum|chain|secondary>` - Coloring scheme
- `--resolution <300|600>` - Output DPI

**Example:**
```bash
./automd-viz.sh --type structure \
  --structure protein.pdb \
  --style nature \
  --representation cartoon \
  --color spectrum \
  --resolution 600
```

**Output:**
- `structure_nature.png` (high-resolution raster)
- `structure_nature.pse` (PyMOL session)

---

### 2. Data Plotting (`--type data`)

Plot time-series data (RMSD, RMSF, energy, etc.) with journal-quality formatting.

**Options:**
- `--input <file>` - Input data file (XVG format)
- `--style <nature|science|cell>` - Journal style
- `--xlabel <text>` - X-axis label
- `--ylabel <text>` - Y-axis label
- `--title <text>` - Plot title

**Example:**
```bash
./automd-viz.sh --type data \
  --input rmsd.xvg \
  --style science \
  --xlabel "Time (ns)" \
  --ylabel "RMSD (nm)"
```

**Output:**
- `data_plot.pdf` (vector graphics)
- `data_plot.png` (raster graphics)

---

### 3. Trajectory Visualization (`--type trajectory`)

Visualize trajectory in reduced dimensionality space (PCA/t-SNE/UMAP).

**Options:**
- `--structure <file>` - Reference structure
- `--trajectory <file>` - Trajectory file (XTC/TRR)
- `--method <pca|tsne|umap>` - Dimensionality reduction method
- `--style <nature|science|cell>` - Journal style

**Example:**
```bash
./automd-viz.sh --type trajectory \
  --structure protein.pdb \
  --trajectory md.xtc \
  --method pca \
  --style nature
```

**Output:**
- `trajectory_pca_2d.pdf` (2D projection)
- `trajectory_pca_3d.pdf` (3D projection)
- `free_energy_landscape.pdf` (FEL)

---

### 4. Automated Report (`--type report`)

Generate a complete set of publication-ready figures.

**Options:**
- `--structure <file>` - Reference structure
- `--trajectory <file>` - Trajectory file
- `--input <dir>` - Analysis results directory
- `--style <nature|science|cell>` - Journal style

**Example:**
```bash
./automd-viz.sh --type report \
  --structure protein.pdb \
  --trajectory md.xtc \
  --input analysis-results/ \
  --style nature
```

**Output:**
- `figures/` directory with all figures
- `VISUALIZATION_REPORT.md` (summary)

---

## 🎨 Journal Styles

### Nature Style
- Font: Arial
- Font size: 7-9 pt
- Line width: 0.5-1.0 pt
- Color: Colorblind-friendly palette
- Format: PDF/EPS (vector)

### Science Style
- Font: Helvetica
- Font size: 8-10 pt
- Line width: 0.75-1.25 pt
- Color: High-contrast palette
- Format: PDF/EPS (vector)

### Cell Style
- Font: Arial
- Font size: 8-12 pt
- Line width: 1.0-1.5 pt
- Color: Vibrant palette
- Format: PDF/EPS (vector)

---

## 🔧 Dependencies

**Required:**
- Python 3.7+
- NumPy
- Matplotlib
- Seaborn

**Optional (for advanced features):**
- PyMOL (structure visualization)
- scikit-learn (PCA/t-SNE)
- umap-learn (UMAP)
- MDAnalysis (trajectory processing)

**Auto-install:**
```bash
pip install numpy matplotlib seaborn scikit-learn umap-learn MDAnalysis
```

---

## 📚 Integration with AutoMD-GROMACS

AutoMD-Viz is designed to work seamlessly with AutoMD-GROMACS analysis results.

**After running analysis:**
```bash
# Run analysis
advanced-analysis -s md.tpr -f md.xtc

# Visualize results
automd-viz --type report --input advanced-analysis/ --style nature
```

**Supported analysis outputs:**
- RMSD/RMSF/Rg (from `analysis.sh`)
- PCA/Clustering (from `advanced-analysis.sh`)
- Binding analysis (from `binding-analysis.sh`)
- Trajectory analysis (from `trajectory-analysis.sh`)
- Property analysis (from `property-analysis.sh`)

---

## 🐛 Troubleshooting

See `publication-viz-errors.md` for common issues and solutions.

**Quick fixes:**
- PyMOL not found → Install PyMOL or use `--no-structure`
- Font issues → Install required fonts or use `--font-fallback`
- Memory errors → Reduce trajectory frames with `--stride`

---

## 📖 Examples

See `examples/` directory for complete workflows:
- `example_protein/` - Protein structure visualization
- `example_ligand/` - Protein-ligand complex
- `example_membrane/` - Membrane protein system
- `example_trajectory/` - Trajectory analysis

---

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 📧 Contact

- Author: Xuan Guo
- Email: xguo608@connect.hkust-gz.edu.cn
- GitHub: @Billwanttobetop
