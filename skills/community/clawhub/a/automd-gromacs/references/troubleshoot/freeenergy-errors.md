# 自由能计算故障排查

本文档用于诊断和解决 `freeenergy.sh` 脚本执行过程中的错误。

---

## 错误代码索引

- [ERROR-001](#error-001) - GROMACS 未安装或未找到
- [ERROR-002](#error-002) - ACPYPE 未安装
- [ERROR-003](#error-003) - 配体参数化失败
- [ERROR-004](#error-004) - 能量最小化不收敛
- [ERROR-005](#error-005) - λ 窗口模拟崩溃
- [ERROR-006](#error-006) - BAR 分析失败
- [ERROR-007](#error-007) - 自由能误差过大
- [ERROR-008](#error-008) - dH/dλ 重叠不足

---

## ERROR-001: GROMACS 未安装或未找到

### 症状
```
ERROR: GROMACS not found
Please install GROMACS or source GMXRC
```

### 原因
- GROMACS 未安装
- GROMACS 已安装但未加载到环境

### 解决方案

**方案 1: 安装 GROMACS**
```bash
# 参考 docs/installation.md
# 或使用包管理器
sudo apt install gromacs  # Ubuntu/Debian
```

**方案 2: 加载 GROMACS 环境**
```bash
source /usr/local/gromacs/bin/GMXRC
# 或
export PATH=/usr/local/gromacs/bin:$PATH
```

**验证:**
```bash
gmx --version
# 应该显示 GROMACS 版本信息
```

---

## ERROR-002: ACPYPE 未安装

### 症状
```
ERROR: ACPYPE not found

配体参数化需要 ACPYPE 工具。请选择以下方案之一:

方案 1: 安装 ACPYPE
  conda install -c conda-forge acpype
  或访问: https://github.com/alanwilter/acpype

方案 2: 使用在线工具
  - LigParGen: http://zarbi.chem.yale.edu/ligpargen/
  - SwissParam: http://www.swissparam.ch/

方案 3: 手动准备配体拓扑
  准备以下文件并放在当前目录:
  - ligand.gro (配体坐标)
  - ligand.itp (配体拓扑)

详细指南: troubleshoot/freeenergy-errors.md#error-002
```

### 原因
ACPYPE (小分子参数化工具) 未安装

### 解决方案

**方案 1: 安装 ACPYPE (推荐)**
```bash
# 使用 conda (推荐)
conda install -c conda-forge acpype

# 或使用 pip
pip install acpype

# 或从源码安装
git clone https://github.com/alanwilter/acpype.git
cd acpype
python setup.py install

# 验证安装
acpype --help
```

**方案 2: 使用在线工具**

**LigParGen (OPLS-AA 力场)**
- 网址: http://zarbi.chem.yale.edu/ligpargen/
- 步骤:
  1. 上传配体结构 (MOL/PDB/SMILES)
  2. 选择 "GROMACS" 输出格式
  3. 下载生成的 .gro 和 .itp 文件
  4. 将文件重命名为 ligand.gro 和 ligand.itp

**SwissParam (CHARMM 力场)**
- 网址: http://www.swissparam.ch/
- 步骤:
  1. 上传配体结构 (MOL2/PDB)
  2. 下载参数文件
  3. 转换为 GROMACS 格式

**ATB (Automated Topology Builder)**
- 网址: https://atb.uq.edu.au/
- 支持多种力场
- 提供完整的 GROMACS 拓扑

**方案 3: 使用 AmberTools (GAFF 力场)**
```bash
# 安装 AmberTools
conda install -c conda-forge ambertools

# 使用 antechamber 参数化
antechamber -i ligand.mol2 -fi mol2 -o ligand.mol2 -fo mol2 -c bcc -nc 0
parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod

# 转换为 GROMACS 格式
acpype -p ligand.prmtop -x ligand.inpcrd
```

**方案 4: 手动准备配体拓扑**

如果使用在线工具或其他方法生成了配体参数，需要准备以下文件:

**ligand.gro** (配体坐标文件)
```
Ligand structure
   12
    1LIG     C1    1   1.000   2.000   3.000
    1LIG     C2    2   1.100   2.100   3.100
    ...
   5.0   5.0   5.0
```

**ligand.itp** (配体拓扑文件)
```
[ moleculetype ]
; Name            nrexcl
LIG               3

[ atoms ]
;   nr  type  resi  res  atom  cgnr     charge      mass
     1   ca     1   LIG    C1    1     -0.115    12.01
     2   ca     1   LIG    C2    2     -0.115    12.01
     ...

[ bonds ]
;   ai    aj funct            c0            c1
     1     2     1
     ...

[ angles ]
;   ai    aj    ak funct            c0            c1
     1     2     3     1
     ...

[ dihedrals ]
;   ai    aj    ak    al funct            c0            c1
     1     2     3     4     9
     ...
```

**验证拓扑文件:**
```bash
# 检查拓扑语法
gmx grompp -f em.mdp -c ligand.gro -p ligand.itp -o test.tpr -maxwarn 10

# 如果成功生成 test.tpr，说明拓扑文件正确
```

**手册参考:**
- GROMACS Manual: Chapter 5.5 (Force Fields)
- GROMACS Manual: Chapter 5.6 (Topology File Format)
- How-To Guide: Parameterization of New Molecules

**依赖工具安装指南:**
参考 `references/tools/INSTALLATION.md` 获取详细的工具安装说明。

---

## ERROR-003: 配体参数化失败

### 症状
```
ERROR: Ligand parameterization failed
Check ligand structure and charge
```

### 原因
- 配体结构有问题 (缺失氢原子、错误键连接)
- 电荷未指定或不合理
- 力场不支持该分子类型

### 诊断步骤

**1. 检查配体结构**
```bash
# 使用 Open Babel 检查
obabel ligand.mol2 -O ligand_check.pdb
# 查看是否有警告

# 检查氢原子
grep " H " ligand.mol2 | wc -l
```

**2. 检查电荷**
```bash
# 配体总电荷应该是整数
# 检查 mol2 文件中的电荷列
awk '{sum+=$9} END {print sum}' ligand.mol2
```

**3. 可视化检查**
```bash
pymol ligand.mol2
# 检查:
# - 键连接是否正确
# - 是否有孤立原子
# - 立体化学是否合理
```

### 解决方案

**方案 1: 修复配体结构**
```bash
# 添加氢原子
obabel ligand.sdf -O ligand_H.mol2 -h

# 优化几何
obabel ligand.mol2 -O ligand_opt.mol2 --gen3d
```

**方案 2: 使用在线工具**
- **ATB**: https://atb.uq.edu.au/
  - 上传分子结构
  - 自动生成 GROMACS 拓扑
  - 下载 .itp 和 .gro 文件

**方案 3: 手动参数化**
参考手册: Chapter 5.6 (Topology)

---

## ERROR-004: 能量最小化不收敛

### 症状
```
WARNING: Energy minimization did not converge
Maximum force > 1000 kJ/mol/nm
```

### 原因
- 初始结构有严重的原子重叠
- 配体-蛋白质接触不合理
- 拓扑文件有错误

### 诊断步骤

**1. 检查最大力**
```bash
echo "10 0" | gmx energy -f em.edr -o potential.xvg
tail em.log | grep "Fmax"
```

**2. 检查能量组分**
```bash
echo "1 2 3 7 8 0" | gmx energy -f em.edr -o components.xvg
# 查看哪个能量项异常高
```

**3. 可视化检查**
```bash
pymol em.gro
# 查找原子重叠区域
```

### 解决方案

**方案 1: 更严格的能量最小化**
```bash
# 修改 em.mdp
emtol = 100.0      # 从 1000 降到 100
nsteps = 100000    # 增加步数
emstep = 0.001     # 减小步长
```

**方案 2: 分步最小化**
```bash
# 第一步: 只优化氢原子
define = -DPOSRES  # 限制重原子

# 第二步: 优化侧链
define = -DPOSRES_BACKBONE

# 第三步: 全系统优化
# 不使用位置限制
```

**方案 3: 检查初始结构**
```bash
# 重新对接配体
# 或手动调整配体位置
```

**手册参考:**
- Chapter 5.4 (Algorithms - Energy Minimization)
- Chapter 3.10 (Common Errors)

---

## ERROR-005: λ 窗口模拟崩溃

### 症状
```
ERROR: mdrun failed for lambda window X
LINCS WARNING or segmentation fault
```

### 原因
- 时间步长太大
- 软核参数不当
- 系统不稳定

### 诊断步骤

**1. 检查日志**
```bash
tail -50 logs/mdrun_lambda_X.log
grep -i "error\|warning\|fatal" logs/mdrun_lambda_X.log
```

**2. 检查 LINCS 警告**
```bash
grep "LINCS" logs/mdrun_lambda_X.log
```

**3. 检查能量**
```bash
echo "10 16 0" | gmx energy -f lambda_X/md.edr -o check.xvg
```

### 解决方案

**方案 1: 调整软核参数**
```bash
# 在 md.mdp 中修改
sc-alpha = 0.5    # 尝试 0.3-0.7
sc-power = 1      # 或 2
sc-sigma = 0.3    # 尝试 0.25-0.35
```

**方案 2: 减小时间步长**
```bash
dt = 0.001  # 从 0.002 减到 0.001
```

**方案 3: 延长平衡时间**
```bash
# 在每个 λ 窗口前先做 NVT/NPT 平衡
# 使用该 λ 值但不记录 dH/dλ
```

**手册参考:**
- Chapter 5.8 (Free Energy Calculations)
- 软核参数选择指南

---

## ERROR-006: BAR 分析失败

### 症状
```
ERROR: gmx bar failed
Not enough overlap between states
```

### 原因
- λ 窗口间隔太大
- 模拟时间太短
- dH/dλ 分布不重叠

### 诊断步骤

**1. 检查重叠**
```bash
gmx bar -f lambda_*/md.xvg -o bar.xvg -oi barint.xvg
xmgrace barint.xvg
# 查看相邻窗口的重叠程度
```

**2. 检查 dH/dλ 分布**
```bash
# 查看每个窗口的 dH/dλ
for i in lambda_*/md.xvg; do
    echo "Processing $i"
    grep -v "^[@#]" $i | awk '{print $2}' | sort -n | uniq -c
done
```

### 解决方案

**方案 1: 增加 λ 窗口**
```bash
# 从 21 个增加到 41 个
--lambda-windows 41
# λ 间隔从 0.05 减到 0.025
```

**方案 2: 延长模拟时间**
```bash
# 从 5 ns 增加到 10 ns 每窗口
--production 10000
```

**方案 3: 使用 MBAR**
```bash
# 如果 BAR 失败,尝试 MBAR
# 需要安装 pymbar
pip install pymbar
# 使用 alchemical-analysis 工具
```

**手册参考:**
- Chapter 5.8.3 (BAR Method)
- Best Practices for Free Energy Calculations

---

## ERROR-007: 自由能误差过大

### 症状
```
WARNING: Free energy error > 1 kcal/mol
ΔG = -8.5 ± 2.3 kJ/mol (± 0.55 kcal/mol)
```

### 原因
- 采样不足
- 系统未充分平衡
- λ 窗口设置不当

### 判断标准
- **优秀**: 误差 < 0.5 kcal/mol
- **可接受**: 误差 0.5-1.0 kcal/mol
- **需改进**: 误差 > 1.0 kcal/mol

### 解决方案

**方案 1: 延长模拟**
```bash
# 每窗口从 5 ns 增加到 10-20 ns
--production 20000
```

**方案 2: 增加窗口数**
```bash
# 特别是在 λ=0 和 λ=1 附近
# 使用非均匀分布
```

**方案 3: 检查平衡**
```bash
# 分析每个窗口的能量时间序列
for i in lambda_*/md.edr; do
    echo "10 0" | gmx energy -f $i -o energy_$i.xvg
done
# 检查是否有趋势 (未平衡)
```

**方案 4: 多次重复**
```bash
# 运行 3-5 次独立模拟
# 计算平均值和标准差
```

---

## ERROR-008: dH/dλ 重叠不足

### 症状
```
WARNING: Poor overlap between lambda states
Overlap < 0.03 for states X and X+1
```

### 原因
- λ 间隔太大
- 软核参数不当
- 相互作用变化太剧烈

### 诊断步骤

**1. 可视化重叠**
```bash
xmgrace barint.xvg
# 查看重叠矩阵
# 对角线附近应该有明显的重叠
```

**2. 检查 dH/dλ 分布**
```bash
# 绘制每个窗口的 dH/dλ 直方图
for i in $(seq 0 20); do
    grep -v "^[@#]" lambda_$(printf "%02d" $i)/md.xvg | \
    awk '{print $2}' > dhdl_$i.dat
done
```

### 解决方案

**方案 1: 局部加密**
```bash
# 在重叠不足的区域增加窗口
# 例如在 λ=0.4-0.6 之间加密
```

**方案 2: 调整软核参数**
```bash
# 增加 sc-alpha 使变化更平滑
sc-alpha = 0.7  # 从 0.5 增加到 0.7
```

**方案 3: 分阶段耦合**
```bash
# 先耦合静电,再耦合范德华
# 使用不同的 λ 向量
```

**手册参考:**
- Chapter 5.8.4 (Soft-core Interactions)
- Overlap Analysis Best Practices

---

## 常见问题 FAQ

### Q1: 自由能计算需要多长时间?

**A:** 取决于系统大小和窗口数
- 小系统 (< 50k 原子): 21 窗口 × 5 ns = 约 1-2 天 (GPU)
- 中等系统 (50-100k 原子): 约 3-5 天
- 大系统 (> 100k 原子): 约 1-2 周

**加速方法:**
- 使用 GPU: `-nb gpu -pme gpu`
- 并行运行窗口: 多 GPU 或集群
- 减少窗口数 (但要保证重叠)

### Q2: 如何验证结果可靠性?

**A:** 多重验证
1. **误差检查**: < 1 kcal/mol
2. **重叠检查**: 相邻窗口重叠 > 0.03
3. **收敛检查**: 能量时间序列无趋势
4. **重复性**: 多次独立模拟结果一致
5. **与实验比较**: 如果有实验数据

### Q3: 结果与实验差异大怎么办?

**A:** 系统性检查
1. **力场选择**: 尝试不同力场
2. **水模型**: TIP3P vs TIP4P vs SPC/E
3. **盒子大小**: 是否足够大
4. **离子浓度**: 是否匹配实验
5. **质子化状态**: pH 相关的质子化
6. **构象采样**: 是否需要增强采样

### Q4: 可以用于其他类型的自由能吗?

**A:** 可以,但需要修改
- **溶剂化自由能**: 只需配体在水中和真空中
- **突变自由能**: 修改拓扑文件
- **pKa 计算**: 质子化/去质子化
- **相对结合自由能**: 两个配体的差值

---

## 参考资源

### 手册章节
- Chapter 5.8: Free Energy Calculations
- Chapter 5.8.1: Thermodynamic Integration
- Chapter 5.8.2: Free Energy Perturbation
- Chapter 5.8.3: Bennett Acceptance Ratio
- Chapter 5.8.4: Soft-core Interactions

### 推荐论文
1. Bennett (1976) - BAR 方法原始论文
2. Shirts & Chodera (2008) - MBAR 方法
3. Klimovich et al. (2015) - 自由能计算最佳实践
4. Gapsys et al. (2015) - PMX 工具

### 在线资源
- GROMACS 教程: http://www.mdtutorials.com/
- Alchemistry.org: 自由能计算社区
- Living Journal of Computational Molecular Science

---

**最后更新:** 2026-04-07
**基于:** GROMACS 2026.1 + 实战经验
