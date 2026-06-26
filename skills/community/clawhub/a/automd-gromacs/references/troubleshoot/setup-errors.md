# 系统准备故障排查

本文档用于诊断和解决 `setup.sh` 脚本执行过程中的错误。

---

## 错误代码索引

- [ERROR-001](#error-001) - GROMACS 未找到
- [ERROR-002](#error-002) - 未知力场
- [ERROR-003](#error-003) - pdb2gmx 失败
- [ERROR-004](#error-004) - editconf 失败
- [ERROR-005](#error-005) - solvate 失败
- [ERROR-006](#error-006) - grompp (ions) 失败
- [ERROR-007](#error-007) - genion 失败
- [ERROR-008](#error-008) - grompp (EM) 失败
- [ERROR-009](#error-009) - 能量最小化失败
- [ERROR-010](#error-010) - 跨力场拓扑重复 include
- [ERROR-011](#error-011) - GPU PME 不支持非动力学积分器
- [ERROR-012](#error-012) - OMP_NUM_THREADS 冲突

---

## ERROR-001: GROMACS 未找到

### 症状
```
ERROR: GROMACS not found
```

### 解决方案
```bash
# 加载 GROMACS 环境
source /usr/local/gromacs/bin/GMXRC

# 验证
gmx --version
```

---

## ERROR-002: 未知力场

### 症状
```
ERROR: Unknown forcefield: xxx
```

### 支持的力场
- `amber99sb-ildn` (推荐,蛋白质)
- `amber14sb` (新版 AMBER)
- `charmm27` (CHARMM 力场)
- `charmm36` (新版 CHARMM)
- `gromos54a7` (GROMOS 力场)

### 解决方案
```bash
# 使用支持的力场
./setup.sh --input protein.pdb --forcefield amber99sb-ildn
```

---

## ERROR-003: pdb2gmx 失败

### 症状
```
ERROR: pdb2gmx failed
Fatal error: Residue 'XXX' not found in database
```

### 常见原因

**1. 非标准残基**
- 配体、辅因子、修饰残基
- 需要单独参数化

**2. 缺失原子**
- PDB 文件不完整
- 需要补全

**3. 多条链**
- 需要 TER 记录分隔

### 诊断步骤

**检查 PDB 文件:**
```bash
# 查看残基类型
grep "^ATOM" protein.pdb | awk '{print $4}' | sort -u

# 查看非标准残基
grep "^HETATM" protein.pdb | awk '{print $4}' | sort -u
```

### 解决方案

**方案 1: 移除非标准残基**
```bash
# 只保留蛋白质
grep "^ATOM" protein.pdb > protein_clean.pdb
```

**方案 2: 补全缺失原子**
```bash
# 使用 PDB2PQR 或 MODELLER
pdb2pqr --ff=AMBER protein.pdb protein_fixed.pdb
```

**方案 3: 添加 TER 记录**
```bash
# 在链之间添加 TER
# 手动编辑或使用脚本
```

**方案 4: 忽略氢原子**
```bash
# pdb2gmx 会自动添加氢原子
# 使用 -ignh 选项 (脚本已包含)
```

**手册参考:**
- Chapter 5.6.1 (Topology Generation)
- How-To: Adding Residues to Force Field

---

## ERROR-004: editconf 失败

### 症状
```
ERROR: editconf failed
```

### 常见原因
- 输入文件格式错误
- 盒子参数不合理

### 解决方案

**检查输入:**
```bash
# 查看 protein.gro
head -20 protein.gro
tail -5 protein.gro
```

**调整盒子参数:**
```bash
# 增加距离 (默认 1.0 nm)
./setup.sh --input protein.pdb --box-distance 1.5

# 改变盒子类型
./setup.sh --input protein.pdb --box-type dodecahedron
```

---

## ERROR-005: solvate 失败

### 症状
```
ERROR: solvate failed
Can not find solvent configuration
```

### 原因
- 溶剂模型文件未找到
- GROMACS 安装不完整

### 解决方案

**检查溶剂文件:**
```bash
# 查找 spc216.gro
find /usr/local/gromacs -name "spc216.gro"

# 或使用绝对路径
gmx solvate -cp box.gro -cs /path/to/spc216.gro -o solv.gro -p topol.top
```

---

## ERROR-006: grompp (ions) 失败

### 症状
```
ERROR: grompp for ions failed
```

### 常见原因
- 拓扑文件错误
- MDP 参数不兼容

### 解决方案

**检查拓扑:**
```bash
# 查看 topol.top
grep "^#include" topol.top
grep "^[ \t]*[A-Z]" topol.top | tail -10
```

**使用 -maxwarn:**
```bash
# 脚本已使用 -maxwarn 1
# 如果警告过多,检查具体原因
```

---

## ERROR-007: genion 失败

### 症状
```
ERROR: genion failed
Not enough solvent molecules
```

### 原因
- 盒子太小,水分子不足
- 离子浓度太高

### 解决方案

**方案 1: 增大盒子**
```bash
./setup.sh --input protein.pdb --box-distance 1.5
```

**方案 2: 降低离子浓度**
```bash
./setup.sh --input protein.pdb --ion-conc 0.1
```

**方案 3: 只中和**
```bash
# 脚本默认会中和 + 添加盐
# 如果只需要中和,修改脚本
```

---

## ERROR-008: grompp (EM) 失败

### 症状
```
ERROR: grompp for EM failed
```

### 常见原因
- 拓扑与坐标不匹配
- MDP 参数错误

### 诊断步骤

**检查原子数:**
```bash
# 坐标文件
grep "^ATOM" system.gro | wc -l

# 拓扑文件
gmx dump -s ions.tpr 2>&1 | grep "natoms"
```

**检查日志:**
```bash
cat logs/grompp_em.log
```

### 解决方案

**重新生成拓扑:**
```bash
# 从头开始
rm -rf output/*
./setup.sh --input protein.pdb --output output
```

---

## ERROR-009: 能量最小化失败

### 症状
```
ERROR: Energy minimization failed
LINCS WARNING or segmentation fault
```

### 常见原因

**1. 原子重叠**
- 初始结构有问题
- 配体-蛋白质冲突

**2. 拓扑错误**
- 键长/键角参数错误
- 力场不匹配

**3. 系统不稳定**
- 盒子太小
- 离子位置不合理

### 诊断步骤

**1. 检查日志**
```bash
tail -100 logs/mdrun_em.log
grep -i "warning\|error" logs/mdrun_em.log
```

**2. 检查能量**
```bash
echo "10 0" | gmx energy -f em.edr -o potential.xvg
xmgrace potential.xvg
# 查看能量是否下降
```

**3. 可视化**
```bash
pymol system.gro
# 查找原子重叠
```

### 解决方案

**方案 1: 更严格的最小化**
```bash
# 修改 em.mdp
emtol = 100.0      # 从 1000 降到 100
nsteps = 100000    # 增加步数
emstep = 0.001     # 减小步长
```

**方案 2: 分步最小化**
```bash
# 第一步: 限制蛋白质,只优化水和离子
# 第二步: 限制骨架,优化侧链
# 第三步: 全系统优化
```

**方案 3: 检查初始结构**
```bash
# 使用更好的 PDB 文件
# 或手动修复问题区域
```

**手册参考:**
- Chapter 5.4 (Energy Minimization)
- Chapter 3.10 (Common Errors)

---

## 质量检查清单

### 拓扑生成后
- [ ] 所有残基都被识别
- [ ] 没有缺失原子警告
- [ ] 二硫键正确识别

### 溶剂化后
- [ ] 水分子数量合理 (约 10-15 个/nm³)
- [ ] 盒子足够大 (蛋白质到边界 > 1 nm)
- [ ] 没有水分子在蛋白质内部

### 添加离子后
- [ ] 系统电中性 (如果选择中和)
- [ ] 离子浓度合理 (0.1-0.15 M)
- [ ] Na+ 和 Cl- 数量合理

### 能量最小化后
- [ ] 势能为负值
- [ ] 势能 < -100,000 kJ/mol (取决于系统大小)
- [ ] 没有 LINCS 警告
- [ ] 最大力 < 1000 kJ/mol/nm

---

---

## ERROR-010: 跨力场拓扑重复 include

### 症状

**"Found a second defaults directive"**
```
Fatal error: Syntax error - File forcefield.itp, line 15
Last line read: '[ defaults ]'
Invalid order for directive defaults
```

**"moleculetype SOL is redefined"**
```
ERROR 1 [file tip3p.itp, line 3]: moleculetype SOL is redefined
```

### 原因

构建蛋白+配体跨力场体系时，`system.top` 和 `protein_body.itp` 都 include 了 forcefield.itp，导致 `[ defaults ]` 和 `[ moleculetype SOL ]` 重复。

### 解决方案

```bash
# 从蛋白拓扑中删除重复的 include 行
sed -e '/#include.*forcefield/d' \
    -e '/#include.*tip3p/d' \
    -e '/#include.*ions/d' \
    -e '/#include.*posre/d' \
    protein/protein_topol.top > protein_clean.itp

# system.top 只 include 一次 forcefield/water/ions
# 详细操作见 references/gpu/cross-forcefield-system.md
```

**GROMACS include 顺序铁律：**
```
[ defaults ]       ← 强制最先，只能一次
[ atomtypes ]      ← 可用多次，累加新 atomtype
[ moleculetype ]   ← 每分子一次
[ system ]         ← 只能一次，最后
[ molecules ]      ← 只能一次，最后
```

---

## ERROR-011: GPU PME 不支持非动力学积分器

### 症状
```
Fatal error:
Inconsistency in user input:
Cannot compute PME interactions on a GPU, because:
  PME GPU does not support:
    Non-dynamical integrator (use md, sd, etc).
```

### 原因

能量最小化使用 `integrator = steep`，GPU PME 只支持 MD/SD 等动力学积分器。

### 解决方案

```bash
# EM 阶段：只用 -nb gpu，不用 -pme gpu / -bonded gpu / -update gpu
gmx mdrun -deffnm em -nb gpu -ntmpi 1 -ntomp 16

# MD 阶段：全部 GPU 加速
gmx mdrun -deffnm md -nb gpu -pme gpu -bonded gpu -update gpu -ntmpi 1 -ntomp 8
```

**各阶段 GPU 兼容性：**
| 阶段 | `-nb gpu` | `-pme gpu` | `-bonded gpu` | `-update gpu` |
|------|:---------:|:----------:|:-------------:|:-------------:|
| EM   | ✅ | ❌ | ❌ | ❌ |
| NVT  | ✅ | ✅ | ✅ | ✅ |
| NPT  | ✅ | ✅ | ✅ | ✅ |
| MD   | ✅ | ✅ | ✅ | ✅ |

---

## ERROR-012: OMP_NUM_THREADS 冲突

### 症状
```
Fatal error:
Environment variable OMP_NUM_THREADS (13) and the number of
threads requested on the command line (8) have different values.
```

### 解决方案

```bash
# 方案 A: 取消环境变量（推荐）
unset OMP_NUM_THREADS
gmx mdrun ... -ntomp 8

# 方案 B: 匹配
unset OMP_NUM_THREADS
# 或在启动脚本开头加 unset OMP_NUM_THREADS
```

---

## 最佳实践

### 1. PDB 文件准备
```bash
# 移除水分子和离子
grep "^ATOM" original.pdb > protein_only.pdb

# 检查结构
pymol protein_only.pdb
# 查看:
# - 是否有缺失残基
# - 是否有多个构象
# - 是否有非标准残基
```

### 2. 力场选择
- **蛋白质**: AMBER99SB-ILDN 或 CHARMM36
- **核酸**: AMBER14SB 或 CHARMM36
- **膜**: CHARMM36 或 Slipids
- **小分子**: GAFF (需要单独参数化)

### 3. 盒子大小
- **最小距离**: 1.0 nm (快速测试)
- **推荐距离**: 1.2-1.5 nm (生产模拟)
- **长程静电**: > 1.0 nm (PME 要求)

### 4. 离子浓度
- **生理条件**: 0.15 M NaCl
- **低盐**: 0.05-0.1 M
- **高盐**: 0.2-0.5 M

### 5. 能量最小化
- **快速检查**: emtol=1000, nsteps=5000
- **标准**: emtol=1000, nsteps=50000
- **严格**: emtol=100, nsteps=100000

---

## 常见问题 FAQ

### Q1: 为什么要忽略氢原子 (-ignh)?
**A:** PDB 文件中的氢原子位置通常不准确,pdb2gmx 会根据力场重新添加。

### Q2: 如何处理二硫键?
**A:** pdb2gmx 会自动检测,或使用 `-ss` 选项手动指定。

### Q3: 可以用其他水模型吗?
**A:** 可以,但要与力场匹配:
- AMBER: TIP3P
- CHARMM: TIP3P 或 TIP4P
- GROMOS: SPC 或 SPC/E

### Q4: 盒子类型如何选择?
**A:** 
- **Cubic**: 简单,但体积大
- **Dodecahedron**: 节省 ~29% 体积
- **Octahedron**: 节省 ~27% 体积

### Q5: 能量最小化不收敛怎么办?
**A:** 通常不是大问题,只要:
- 势能为负值
- 没有 LINCS 警告
- 可以继续平衡模拟

---

**最后更新:** 2026-04-07
**基于:** GROMACS 2026.1 + 实战经验
