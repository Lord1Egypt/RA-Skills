# 依赖工具安装指南

本文档提供 GROMACS Skills 2.0 所需依赖工具的详细安装说明。

---

## 目录

1. [ACPYPE - 配体参数化工具](#acpype)
2. [AmberTools - AMBER 力场工具集](#ambertools)
3. [insane - 膜系统构建工具](#insane)
4. [其他推荐工具](#其他工具)

---

## ACPYPE

**用途:** 小分子配体参数化，生成 GAFF 力场参数

**适用脚本:** `freeenergy.sh`, `ligand.sh`

### 安装方法

#### 方法 1: Conda (推荐)

```bash
# 创建独立环境 (可选)
conda create -n gromacs-tools python=3.9
conda activate gromacs-tools

# 安装 ACPYPE
conda install -c conda-forge acpype

# 验证安装
acpype --help
```

#### 方法 2: pip

```bash
# 需要 Python 3.6+
pip install acpype

# 验证安装
acpype --help
```

#### 方法 3: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/alanwilter/acpype.git
cd acpype

# 安装
python setup.py install

# 或直接使用
chmod +x acpype.py
sudo cp acpype.py /usr/local/bin/acpype

# 验证安装
acpype --help
```

### 依赖项

ACPYPE 需要以下依赖:
- Python 3.6+
- OpenBabel (可选，用于格式转换)
- AmberTools (可选，用于 GAFF 参数)

### 使用示例

```bash
# 基本用法
acpype -i ligand.mol2 -n 0 -o gmx -b LIG

# 参数说明:
# -i: 输入文件 (支持 MOL2, PDB, MOL)
# -n: 净电荷 (0 = 中性, -1 = 负电荷, +1 = 正电荷)
# -o: 输出格式 (gmx = GROMACS)
# -b: 残基名称 (默认 MOL)

# 输出文件:
# LIG.acpype/LIG_GMX.gro  - 坐标文件
# LIG.acpype/LIG_GMX.itp  - 拓扑文件
```

### 故障排查

**问题 1: 找不到 antechamber**
```bash
# ACPYPE 依赖 AmberTools 的 antechamber
# 安装 AmberTools (见下文)
conda install -c conda-forge ambertools
```

**问题 2: 电荷计算失败**
```bash
# 使用 Gasteiger 电荷代替 AM1-BCC
acpype -i ligand.mol2 -n 0 -c gas -o gmx
```

**问题 3: 不支持的原子类型**
```bash
# 检查配体结构
obabel ligand.mol2 -O check.pdb

# 或使用在线工具 (LigParGen, SwissParam)
```

---

## AmberTools

**用途:** AMBER 力场参数生成，包含 antechamber, parmchk2 等工具

**适用脚本:** `freeenergy.sh`, `ligand.sh`

### 安装方法

#### 方法 1: Conda (推荐)

```bash
# 安装 AmberTools (免费版)
conda install -c conda-forge ambertools

# 验证安装
antechamber -h
parmchk2 -h
```

#### 方法 2: 从源码编译

```bash
# 下载 AmberTools (需要注册)
# https://ambermd.org/GetAmber.php

# 解压
tar xvfj AmberTools23.tar.bz2
cd amber22_src

# 编译
./configure gnu
make install

# 加载环境
source /path/to/amber22/amber.sh

# 验证安装
antechamber -h
```

### 核心工具

**antechamber** - 分子参数化
```bash
# 生成 GAFF 参数
antechamber -i ligand.mol2 -fi mol2 -o ligand.mol2 -fo mol2 -c bcc -nc 0

# 参数说明:
# -i: 输入文件
# -fi: 输入格式
# -o: 输出文件
# -fo: 输出格式
# -c: 电荷方法 (bcc = AM1-BCC, gas = Gasteiger)
# -nc: 净电荷
```

**parmchk2** - 检查和补充参数
```bash
# 生成缺失参数
parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod

# 检查生成的 frcmod 文件
cat ligand.frcmod
```

**tleap** - 生成拓扑文件
```bash
# 创建 tleap 输入文件
cat > tleap.in << EOF
source leaprc.gaff
loadamberparams ligand.frcmod
LIG = loadmol2 ligand.mol2
saveamberparm LIG ligand.prmtop ligand.inpcrd
quit
EOF

# 运行 tleap
tleap -f tleap.in
```

### 与 GROMACS 集成

```bash
# 使用 ACPYPE 转换 AMBER 参数到 GROMACS
acpype -p ligand.prmtop -x ligand.inpcrd

# 或使用 ParmEd
parmed -p ligand.prmtop -c ligand.inpcrd -o ligand.gro
```

---

## insane

**用途:** 粗粒化和全原子膜系统构建

**适用脚本:** `membrane.sh`

### 安装方法

#### 方法 1: 直接下载 (推荐)

```bash
# 下载 insane.py
wget http://cgmartini.nl/images/tools/insane/insane.py

# 或使用备用链接
wget https://github.com/Tsjerk/Insane/raw/master/insane.py

# 添加执行权限
chmod +x insane.py

# 移动到系统路径
sudo mv insane.py /usr/local/bin/insane

# 验证安装
insane --help
```

#### 方法 2: 从 GitHub 安装

```bash
# 克隆仓库
git clone https://github.com/Tsjerk/Insane.git
cd Insane

# 安装
pip install .

# 验证安装
insane --help
```

### 使用示例

**构建简单的 POPC 膜**
```bash
# 10x10 nm 的 POPC 膜
insane -o membrane.gro -p topol.top -l POPC -x 10 -y 10 -z 10 -sol -salt 0.15

# 参数说明:
# -o: 输出坐标文件
# -p: 输出拓扑文件
# -l: 脂质类型 (POPC, POPE, DPPC 等)
# -x, -y, -z: 盒子尺寸 (nm)
# -sol: 添加溶剂
# -salt: 离子浓度 (M)
```

**嵌入蛋白质**
```bash
# 将蛋白质嵌入膜中
insane -f protein.gro -o system.gro -p topol.top -l POPC -x 10 -y 10 -z 10 -sol -salt 0.15

# insane 会自动:
# 1. 检测蛋白质的跨膜区域
# 2. 在蛋白质周围构建膜
# 3. 移除重叠的脂质
# 4. 添加溶剂和离子
```

**混合膜组成**
```bash
# POPC:POPE = 3:1 混合膜
insane -o membrane.gro -p topol.top -l POPC:3 -l POPE:1 -x 10 -y 10 -z 10 -sol -salt 0.15

# 添加胆固醇
insane -o membrane.gro -p topol.top -l POPC:7 -l CHOL:3 -x 10 -y 10 -z 10 -sol -salt 0.15
```

### 支持的脂质类型

**常见磷脂:**
- POPC - 1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine
- POPE - 1-palmitoyl-2-oleoyl-sn-glycero-3-phosphoethanolamine
- DPPC - 1,2-dipalmitoyl-sn-glycero-3-phosphocholine
- DOPC - 1,2-dioleoyl-sn-glycero-3-phosphocholine
- DOPE - 1,2-dioleoyl-sn-glycero-3-phosphoethanolamine

**其他脂质:**
- CHOL - 胆固醇
- POPS - 磷脂酰丝氨酸
- POPG - 磷脂酰甘油

**查看完整列表:**
```bash
insane --help | grep -A 100 "Lipid types"
```

### 故障排查

**问题 1: Python 版本不兼容**
```bash
# insane 需要 Python 2.7 或 3.x
python --version

# 如果版本不对，使用 conda 创建环境
conda create -n insane python=3.8
conda activate insane
```

**问题 2: 蛋白质定位不正确**
```bash
# 手动指定跨膜区域
insane -f protein.gro -o system.gro -center -orient

# 或使用 CHARMM-GUI (更可靠)
```

---

## 其他工具

### OpenBabel

**用途:** 分子格式转换

**安装:**
```bash
# Conda
conda install -c conda-forge openbabel

# Ubuntu/Debian
sudo apt install openbabel

# 验证
obabel --version
```

**使用示例:**
```bash
# 格式转换
obabel ligand.sdf -O ligand.mol2

# 添加氢原子
obabel ligand.mol2 -O ligand_H.mol2 -h

# 3D 结构优化
obabel ligand.smi -O ligand.mol2 --gen3d
```

### PyMOL

**用途:** 分子可视化

**安装:**
```bash
# Conda
conda install -c conda-forge pymol-open-source

# Ubuntu/Debian
sudo apt install pymol

# 验证
pymol --version
```

### VMD

**用途:** 轨迹可视化和分析

**安装:**
```bash
# 下载 (需要注册)
# https://www.ks.uiuc.edu/Research/vmd/

# Ubuntu/Debian
sudo dpkg -i vmd_1.9.4a57.bin.LINUXAMD64-CUDA102-OptiX650-OSPRay185.opengl.tar.gz

# 验证
vmd --version
```

### MDAnalysis

**用途:** Python 轨迹分析库

**安装:**
```bash
# pip
pip install MDAnalysis

# conda
conda install -c conda-forge mdanalysis

# 验证
python -c "import MDAnalysis; print(MDAnalysis.__version__)"
```

### Alchemical Analysis

**用途:** 自由能分析工具

**安装:**
```bash
# pip
pip install alchemical-analysis

# 使用
alchemical_analysis -d lambda_* -p dhdl -u kcal
```

---

## 完整环境配置

### 推荐的 Conda 环境

```bash
# 创建完整的 GROMACS 工具环境
conda create -n gromacs-tools python=3.9
conda activate gromacs-tools

# 安装核心工具
conda install -c conda-forge gromacs
conda install -c conda-forge acpype
conda install -c conda-forge ambertools
conda install -c conda-forge openbabel
conda install -c conda-forge pymol-open-source
conda install -c conda-forge mdanalysis

# 安装 Python 分析工具
pip install alchemical-analysis
pip install pymbar

# 下载 insane
wget http://cgmartini.nl/images/tools/insane/insane.py
chmod +x insane.py
mv insane.py ~/.conda/envs/gromacs-tools/bin/insane

# 验证安装
gmx --version
acpype --help
antechamber -h
insane --help
obabel --version
```

### 环境激活脚本

> ⚠️ **注意**: 将此脚本添加到 shell 启动文件(~/.bashrc)会对所有终端生效，可能造成环境漂移和命令劫持风险。建议仅在需要时手动 `source`。

创建 `~/.gromacs_env.sh`:
```bash
#!/bin/bash
# GROMACS 工具环境激活脚本
# 使用: source ~/.gromacs_env.sh
# ⚠️ 不要添加到 ~/.bashrc，避免环境漂移

# 激活 conda 环境
conda activate gromacs-tools

# 加载 GROMACS (如果从源码编译)
# source /usr/local/gromacs/bin/GMXRC

# 加载 AMBER (如果从源码编译)
# source /path/to/amber22/amber.sh

# 设置环境变量
export GMXLIB=/usr/local/gromacs/share/gromacs/top
export OMP_NUM_THREADS=4

echo "GROMACS tools environment activated"
echo "GROMACS: $(gmx --version | head -1)"
echo "ACPYPE: $(acpype --version 2>&1 | head -1)"
echo "AmberTools: $(antechamber -h 2>&1 | head -1)"
```

使用:
```bash
source ~/.gromacs_env.sh
```

---

## 验证安装

运行以下脚本验证所有工具是否正确安装:

```bash
#!/bin/bash
# 工具安装验证脚本

echo "=== GROMACS Tools Installation Check ==="
echo ""

# GROMACS
if command -v gmx &> /dev/null; then
    echo "✅ GROMACS: $(gmx --version | head -1)"
else
    echo "❌ GROMACS: Not found"
fi

# ACPYPE
if command -v acpype &> /dev/null; then
    echo "✅ ACPYPE: Installed"
else
    echo "❌ ACPYPE: Not found"
fi

# AmberTools
if command -v antechamber &> /dev/null; then
    echo "✅ AmberTools: Installed"
else
    echo "❌ AmberTools: Not found"
fi

# insane
if command -v insane &> /dev/null; then
    echo "✅ insane: Installed"
else
    echo "❌ insane: Not found"
fi

# OpenBabel
if command -v obabel &> /dev/null; then
    echo "✅ OpenBabel: $(obabel --version | head -1)"
else
    echo "⚠️  OpenBabel: Not found (optional)"
fi

# PyMOL
if command -v pymol &> /dev/null; then
    echo "✅ PyMOL: Installed"
else
    echo "⚠️  PyMOL: Not found (optional)"
fi

echo ""
echo "=== Installation Check Complete ==="
```

---

## 故障排查

### 常见问题

**Q1: conda 安装速度慢**
```bash
# 使用 mamba (更快的 conda 替代)
conda install -c conda-forge mamba
mamba install -c conda-forge acpype ambertools
```

**Q2: 权限错误**
```bash
# 不要使用 sudo pip install
# 使用用户安装
pip install --user acpype

# 或使用虚拟环境
python -m venv ~/gromacs-venv
source ~/gromacs-venv/bin/activate
pip install acpype
```

**Q3: 工具版本冲突**
```bash
# 使用独立的 conda 环境
conda create -n gromacs-tools python=3.9
conda activate gromacs-tools
# 在此环境中安装所有工具
```

---

## 参考资源

### 官方文档
- ACPYPE: https://github.com/alanwilter/acpype
- AmberTools: https://ambermd.org/AmberTools.php
- insane: http://cgmartini.nl/index.php/tools2/proteins-and-bilayers/204-insane
- OpenBabel: http://openbabel.org/
- PyMOL: https://pymol.org/

### 教程
- GROMACS Tutorials: http://www.mdtutorials.com/
- Amber Tutorials: https://ambermd.org/tutorials/
- Martini Tutorials: http://cgmartini.nl/index.php/tutorials-general-introduction-gmx5

---

**最后更新:** 2026-04-07  
**版本:** 1.0  
**维护者:** GROMACS Skills 2.0 Team
