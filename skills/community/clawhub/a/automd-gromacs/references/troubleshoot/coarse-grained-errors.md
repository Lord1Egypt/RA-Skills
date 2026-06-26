# 粗粒化模拟故障排查

## 常见错误及解决方案

### ERROR-001: MARTINI力场不可用
**症状**: 
```
[ERROR] MARTINI力场目录不存在
```

**原因**: MARTINI力场未安装或路径错误

**解决方案**:
```bash
# 方案1: 自动下载 (脚本会尝试)
# MARTINI 3
wget http://cgmartini.nl/images/parameters/martini_v3.0.0/martini_v3.0.0.tar.gz
tar -xzf martini_v3.0.0.tar.gz

# MARTINI 2
wget http://cgmartini.nl/images/parameters/martini_v2.2/martini_v2.2.tar.gz
tar -xzf martini_v2.2.tar.gz

# 方案2: 手动指定路径
export MARTINI_FF_DIR=/path/to/martini.ff

# 方案3: 从官网下载
# http://cgmartini.nl/index.php/force-field-parameters
```

---

### ERROR-002: martinize工具未找到
**症状**:
```
[WARN] martinize工具未找到
command not found: martinize2
```

**原因**: martinize未安装

**解决方案**:
```bash
# 方案1: 安装martinize2 (MARTINI 3, 推荐)
pip3 install vermouth-martinize

# 方案2: 安装旧版martinize.py (MARTINI 2)
git clone https://github.com/cgmartini/martinize.py
cd martinize.py
chmod +x martinize.py
# 添加到PATH或使用绝对路径

# 验证安装
martinize2 --help
```

---

### ERROR-003: 全原子到粗粒化转换失败
**症状**:
```
[ERROR] martinize2失败
[ERROR] 粗粒化结构生成失败
```

**原因**: 
- PDB格式问题
- 不支持的残基类型
- 缺失原子

**解决方案**:
```bash
# 1. 检查PDB格式
gmx check -f protein.pdb

# 2. 清理PDB (去除HETATM, 修复残基名)
grep "^ATOM" protein.pdb > protein_clean.pdb

# 3. 使用pdb2gmx预处理
gmx pdb2gmx -f protein.pdb -o protein_processed.gro -water tip3p

# 4. 尝试基础参数 (不使用弹性网络)
martinize2 -f protein.pdb -o topol.top -x cg.pdb -ff martini3001

# 5. 手动指定二级结构
martinize2 -f protein.pdb -o topol.top -x cg.pdb -ff martini3001 -ss HHHHHEEEEECCCC

# 6. 检查不支持的残基
# 查看martinize.log中的警告
```

---

### ERROR-004: 时间步长不合理
**症状**:
```
[WARN] 时间步长过小/过大
LINCS WARNING
```

**原因**: 粗粒化模拟使用了全原子的时间步长

**解决方案**:
```bash
# 粗粒化推荐时间步长: 20-30 fs
export DT=0.020  # 20 fs (脚本会自动修正)

# 如果仍然不稳定:
# 1. 减小时间步长
export DT=0.015  # 15 fs

# 2. 增加能量最小化步数
export EM_STEPS=10000

# 3. 延长平衡时间
export NVT_TIME=200
export NPT_TIME=200
```

---

### ERROR-005: 溶剂化失败
**症状**:
```
[ERROR] 溶剂化失败
Could not find solvent molecule
```

**原因**: 粗粒化水模型不可用

**解决方案**:
```bash
# 方案1: 使用MARTINI水珠子
# 脚本会自动创建water.gro

# 方案2: 使用标准水模型 (不推荐，但可用)
gmx solvate -cp box.gro -cs spc216.gro -o solv.gro

# 方案3: 手动创建粗粒化水盒子
# 使用insane工具 (MARTINI官方)
pip install insane
insane -f protein.pdb -o system.gro -p topol.top -sol W

# 方案4: 从MARTINI教程获取水盒子
wget http://cgmartini.nl/images/tutorials/water.gro
```

---

### ERROR-006: 离子添加失败
**症状**:
```
[WARN] 离子添加失败
Group SOL not found
```

**原因**: 粗粒化系统中溶剂组名不同

**解决方案**:
```bash
# 1. 检查溶剂组名
gmx make_ndx -f solv.gro
# 查找 W 或 SOL 组

# 2. 使用正确的组名
echo "W" | gmx genion -s ions.tpr -o ions.gro -pname NA -nname CL -neutral

# 3. 使用MARTINI离子名称
# NA+ CL- (MARTINI 3)
# NA  CL  (MARTINI 2)

# 4. 如果失败，跳过离子
# 脚本会自动继续 (不加离子)
```

---

### ERROR-007: 能量最小化不收敛
**症状**:
```
[WARN] 能量最小化未完全收敛
Maximum force > emtol
```

**原因**: 
- 初始结构冲突严重
- 能量最小化步数不足

**解决方案**:
```bash
# 1. 增加EM步数
export EM_STEPS=10000

# 2. 放宽收敛标准
export EM_TOL=2000  # kJ/mol/nm

# 3. 使用更强的算法
# 修改em.mdp:
integrator = cg  # 共轭梯度 (比steep更强)

# 4. 分阶段最小化
# 先用steep快速下降，再用cg精细优化

# 5. 检查初始结构
gmx check -f cg_ions.gro
# 查看是否有原子重叠
```

---

### ERROR-008: NVT/NPT不稳定
**症状**:
```
LINCS WARNING
Step X, time Y: LINCS failed
```

**原因**: 
- 时间步长过大
- 温度/压力耦合参数不当
- 系统未充分最小化

**解决方案**:
```bash
# 1. 减小时间步长
export DT=0.015  # 15 fs

# 2. 延长平衡时间
export NVT_TIME=200
export NPT_TIME=200

# 3. 使用更保守的耦合参数
# 修改mdp:
tau_t = 2.0      # 温度耦合时间常数 (默认1.0)
tau_p = 20.0     # 压力耦合时间常数 (默认12.0)

# 4. 分阶段释放约束
# 添加位置约束，逐步释放

# 5. 检查EM结果
echo "Potential" | gmx energy -f em.edr -o potential.xvg
# 确保势能合理 (不是极大值)
```

---

### ERROR-009: 反向映射失败
**症状**:
```
[ERROR] backward.py未安装
[ERROR] 反向映射失败
```

**原因**: 反向映射工具未安装

**解决方案**:
```bash
# 方案1: 安装backward.py (推荐)
git clone https://github.com/Tsjerk/Backward
cd Backward
pip install .

# 方案2: 使用CG2AT
pip install cg2at
cg2at -c cg_structure.gro -a aa_template.pdb -o aa_structure.gro

# 方案3: 使用MDAnalysis自定义脚本
pip install MDAnalysis
# 编写Python脚本进行映射

# 方案4: 使用CHARMM-GUI
# 上传CG结构到 http://www.charmm-gui.org/
# 使用Martini Maker进行反向映射
```

---

### ERROR-010: 截断距离警告
**症状**:
```
WARNING: Cut-off distance too small
rcoulomb < 1.0 nm
```

**原因**: MARTINI力场需要较大的截断距离

**解决方案**:
```bash
# MARTINI推荐参数 (脚本已内置):
rcoulomb = 1.1 nm
rvdw     = 1.1 nm

# 如果盒子太小:
# 1. 增大盒子
export CG_BOX_DISTANCE=2.0  # 增加到2.0 nm

# 2. 或使用更小的截断 (不推荐)
# 修改mdp:
rcoulomb = 1.0
rvdw     = 1.0
```

---

### ERROR-011: 静电处理错误
**症状**:
```
ERROR: Reaction-Field not supported
epsilon_r value incorrect
```

**原因**: MARTINI使用特殊的静电处理

**解决方案**:
```bash
# MARTINI标准静电参数 (脚本已内置):
coulombtype = reaction-field
rcoulomb    = 1.1
epsilon_r   = 15    # 相对介电常数
epsilon_rf  = 0     # 无穷远介电常数

# 如果不支持Reaction-Field:
# 使用PME (不推荐，但可用)
coulombtype = PME
rcoulomb    = 1.1
pme_order   = 4
fourierspacing = 0.12
```

---

### ERROR-012: 压力耦合振荡
**症状**:
```
Pressure oscillating wildly
Box size changing rapidly
```

**原因**: 压力耦合时间常数过小

**解决方案**:
```bash
# 粗粒化推荐压力耦合参数:
tau_p = 12.0         # MARTINI推荐 (比全原子大)
compressibility = 3e-4  # 比全原子小 (4.5e-5)

# 如果仍然振荡:
# 1. 增大tau_p
tau_p = 20.0

# 2. 延长NPT平衡
export NPT_TIME=500

# 3. 先用Berendsen稳定，再用Parrinello-Rahman
# NPT阶段1: pcoupl = berendsen
# NPT阶段2: pcoupl = parrinello-rahman
```

---

### ERROR-013: 虚拟位点问题
**症状**:
```
Virtual site construction failed
Dummy atom error
```

**原因**: MARTINI某些残基使用虚拟位点

**解决方案**:
```bash
# 1. 检查拓扑文件中的虚拟位点定义
grep "virtual" topol.top

# 2. 确保GROMACS版本支持虚拟位点
gmx --version

# 3. 使用martinize的-elastic选项
martinize2 -f protein.pdb -o topol.top -x cg.pdb -elastic

# 4. 如果问题持续，禁用虚拟位点
# 编辑topol.top，注释掉虚拟位点行
```

---

### ERROR-014: 多尺度模拟失败
**症状**:
```
[ERROR] 多尺度模拟失败
Backmapping failed
```

**原因**: 反向映射工具不可用或参数不当

**解决方案**:
```bash
# 1. 确保有全原子参考结构
# 反向映射需要原始全原子PDB

# 2. 使用正确的工具链
# AA → CG: martinize2
# CG → AA: backward.py

# 3. 保存中间结果
# 每个阶段都保存结构和拓扑

# 4. 分步执行
# 不要使用multiscale模式，手动执行各阶段
MODE=aa2cg ./coarse-grained.sh
# 然后手动反向映射
MODE=backmapping INPUT_GRO=md.gro ./coarse-grained.sh
```

---

## 性能优化

### 1. GPU加速
```bash
# 粗粒化模拟GPU加速效果显著
export GPU_ID=0
export NTOMP=4

# 检查GPU使用
gmx mdrun -ntmpi 1 -ntomp 4 -gpu_id 0 -nb gpu
```

### 2. 并行化
```bash
# MPI并行 (多节点)
mpirun -np 4 gmx_mpi mdrun -deffnm md

# 混合并行
mpirun -np 2 gmx_mpi mdrun -ntomp 4 -deffnm md
```

### 3. 减少输出
```bash
# 减少轨迹输出频率
nstxout-compressed = 10000  # 每200 ps输出一次

# 只输出感兴趣的组
compressed-x-grps = Protein
```

---

## 最佳实践

### 1. 时间步长选择
- **MARTINI 2**: 20-25 fs
- **MARTINI 3**: 20-30 fs
- **极性溶剂**: 20 fs
- **非极性溶剂**: 30 fs

### 2. 截断距离
- **rcoulomb**: 1.1 nm (标准)
- **rvdw**: 1.1 nm (标准)
- **最小盒子**: 2 × rcoulomb = 2.2 nm

### 3. 温度和压力耦合
- **tau_t**: 1.0 ps (V-rescale)
- **tau_p**: 12.0 ps (Parrinello-Rahman)
- **compressibility**: 3e-4 bar⁻¹

### 4. 平衡时间
- **EM**: 5000-10000 steps
- **NVT**: 100-200 ps
- **NPT**: 100-500 ps
- **Production**: ≥1 μs (粗粒化优势)

### 5. 力场选择
- **蛋白质**: MARTINI 3 (更准确)
- **脂质**: MARTINI 2 (参数更全)
- **混合系统**: 根据主要组分选择

---

## 调试技巧

### 1. 检查能量
```bash
echo "Potential Kinetic Total" | gmx energy -f md.edr -o energy.xvg
xmgrace energy.xvg
# 能量应该稳定，无剧烈波动
```

### 2. 检查温度和压力
```bash
echo "Temperature Pressure" | gmx energy -f md.edr -o temp_press.xvg
# 温度应该在目标值±5K
# 压力可以波动较大 (±100 bar正常)
```

### 3. 检查盒子大小
```bash
echo "Box-X Box-Y Box-Z" | gmx energy -f md.edr -o box.xvg
# NPT平衡后盒子应该稳定
```

### 4. 可视化结构
```bash
# 使用VMD查看粗粒化结构
vmd cg_protein.pdb

# 使用PyMOL
pymol cg_protein.pdb

# 检查珠子分布是否合理
```

### 5. 检查拓扑
```bash
gmx dump -s md.tpr | less
# 查看原子类型、键合参数等
```

---

## 参考资源

### 官方文档
- MARTINI官网: http://cgmartini.nl/
- MARTINI教程: http://cgmartini.nl/index.php/tutorials-general-introduction-gmx5
- GROMACS手册: https://manual.gromacs.org/

### 工具
- martinize2: https://github.com/marrink-lab/vermouth-martinize
- backward.py: https://github.com/Tsjerk/Backward
- insane: https://github.com/Tsjerk/InsaneX

### 论文
- MARTINI 2: Marrink et al. (2007) J. Phys. Chem. B 111, 7812-7824
- MARTINI 3: Souza et al. (2021) Nat. Methods 18, 382-388
- Martinize: Wassenaar et al. (2015) JCTC 11, 2144-2155
