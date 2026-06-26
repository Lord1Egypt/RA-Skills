# Accelerated MD 故障排查

## 快速诊断

```bash
# 检查 PLUMED 可用性
gmx mdrun -h 2>&1 | grep -i plumed

# 检查预运行结果
grep "Average" prerun.log

# 检查 aMD 参数
grep -E "E_DIHED|ALPHA_DIHED|E_TOT|ALPHA_TOT" accelerated-md.log

# 检查加速效果
grep "Boost" md.log
```

---

## 常见错误

### ERROR-001: PLUMED 不可用
**症状:**
```
ERROR: GROMACS was not compiled with PLUMED support
```

**原因:** GROMACS 编译时未启用 PLUMED

**Fix:**
```bash
# 方案1: 重新编译 GROMACS (推荐)
cd ~/gromacs-source
cmake .. -DGMX_PLUMED=ON
make -j$(nproc)
sudo make install

# 方案2: 使用 Metadynamics 替代
export AMD_METHOD=metadynamics
bash scripts/advanced/accelerated-md.sh
```

**预防:** 安装时启用 PLUMED 支持

---

### ERROR-002: 预运行失败
**症状:**
```
ERROR: Prerun simulation failed
```

**原因:** 
- 输入文件缺失/损坏
- 系统不稳定
- 资源不足

**Fix:**
```bash
# 检查输入文件
ls -lh system.gro topol.top npt.cpt

# 手动运行预运行
gmx grompp -f prerun.mdp -c system.gro -p topol.top -o prerun.tpr
gmx mdrun -deffnm prerun -ntomp 4

# 检查能量
gmx energy -f prerun.edr -o energy.xvg
# 选择: 11 (Dihedral), 12 (Potential)

# 如果已有预运行结果
export PRERUN_DONE=true
export AMD_E_DIHED=<value>
export AMD_ALPHA_DIHED=<value>
export AMD_E_TOT=<value>
export AMD_ALPHA_TOT=<value>
bash scripts/advanced/accelerated-md.sh
```

**预防:** 确保系统已充分平衡

---

### ERROR-003: aMD 参数不合理
**症状:**
```
WARNING: aMD parameters may be too aggressive
ERROR: System exploded during aMD simulation
```

**原因:**
- E_DIHED/E_TOT 设置过高
- ALPHA 设置过小
- 加速过于激进

**Fix:**
```bash
# 方案1: 使用保守参数
export AMD_E_DIHED=<avg_dihed + 3.5*std>  # 降低到 3.5σ
export AMD_ALPHA_DIHED=<0.2*avg_dihed>    # 增大到 0.2
export AMD_E_TOT=<avg_tot + 0.15*Natoms>  # 降低到 0.15
export AMD_ALPHA_TOT=<0.15*Natoms>        # 增大到 0.15
bash scripts/advanced/accelerated-md.sh

# 方案2: 仅加速二面角 (更温和)
export AMD_TYPE=dihedral
bash scripts/advanced/accelerated-md.sh

# 方案3: 使用 well-tempered metadynamics 替代
export AMD_METHOD=metadynamics
bash scripts/advanced/metadynamics.sh
```

**预防:** 从保守参数开始，逐步增加加速强度

---

### ERROR-004: 二面角能量计算失败
**症状:**
```
ERROR: Failed to extract dihedral energy from prerun
```

**原因:**
- 预运行输出不完整
- 能量文件损坏
- 系统无二面角项

**Fix:**
```bash
# 检查能量项
gmx energy -f prerun.edr
# 查看是否有 "Dihedral" 项

# 如果无二面角项 (如小分子)
export AMD_TYPE=total
bash scripts/advanced/accelerated-md.sh

# 手动指定参数
export AMD_E_DIHED=500  # kJ/mol
export AMD_ALPHA_DIHED=100
bash scripts/advanced/accelerated-md.sh
```

**预防:** 确认系统包含二面角相互作用

---

### ERROR-005: PLUMED 配置错误
**症状:**
```
ERROR: PLUMED input file is invalid
+++ PLUMED error
```

**原因:**
- plumed.dat 语法错误
- CV 定义不正确
- 原子索引超出范围

**Fix:**
```bash
# 检查 PLUMED 配置
plumed driver --plumed plumed.dat --ixyz system.gro

# 查看详细错误
cat md.log | grep -A 10 "PLUMED error"

# 修复常见问题
# 1. 原子索引从1开始 (不是0)
# 2. 确保所有原子存在
# 3. 检查 UNITS 声明

# 使用简化配置
cat > plumed.dat << EOF
# Accelerated MD via PLUMED
UNITS LENGTH=nm TIME=ps ENERGY=kJ/mol

# 定义二面角 CV
phi: TORSION ATOMS=5,7,9,15
psi: TORSION ATOMS=7,9,15,17

# aMD bias
amd: EXTERNAL ARG=phi,psi FILE=amd_params.dat

PRINT ARG=phi,psi,amd.bias FILE=COLVAR STRIDE=100
EOF

bash scripts/advanced/accelerated-md.sh
```

**预防:** 使用脚本自动生成 PLUMED 配置

---

### ERROR-006: 加速效果不明显
**症状:**
```
WARNING: Boost energy is very small
WARNING: Sampling enhancement is minimal
```

**原因:**
- aMD 参数过于保守
- 模拟时间不足
- 系统本身采样充分

**Fix:**
```bash
# 方案1: 增加加速强度
export AMD_E_DIHED=<avg_dihed + 5*std>    # 提高到 5σ
export AMD_ALPHA_DIHED=<0.15*avg_dihed>   # 减小到 0.15
export AMD_E_TOT=<avg_tot + 0.25*Natoms>  # 提高到 0.25
export AMD_ALPHA_TOT=<0.1*Natoms>         # 减小到 0.1
bash scripts/advanced/accelerated-md.sh

# 方案2: 延长模拟时间
export SIM_TIME=50000  # 50 ns
bash scripts/advanced/accelerated-md.sh

# 方案3: 使用 dual-boost (同时加速二面角和总能量)
export AMD_TYPE=dual
bash scripts/advanced/accelerated-md.sh

# 方案4: 切换到其他增强采样方法
bash scripts/advanced/metadynamics.sh
bash scripts/advanced/replica-exchange.sh
```

**预防:** 根据系统特性选择合适的加速参数

---

### ERROR-007: 重加权失败
**症状:**
```
ERROR: Failed to compute reweighted free energy
WARNING: Boost energy distribution is too broad
```

**原因:**
- 加速过于激进
- 统计不足
- Boost 能量分布不合理

**Fix:**
```bash
# 检查 Boost 能量分布
gmx energy -f md.edr -o boost.xvg
# 选择 Boost 相关项

# 如果分布过宽 (σ_boost > 10 kT)
# 方案1: 使用更保守的参数重新运行
export AMD_ALPHA_DIHED=<增大20%>
export AMD_ALPHA_TOT=<增大20%>
bash scripts/advanced/accelerated-md.sh

# 方案2: 使用 Maclaurin 级数重加权 (更稳定)
python3 << EOF
import numpy as np
boost = np.loadtxt('boost.xvg', comments=['#', '@'])[:, 1]
kT = 2.494  # kJ/mol at 300K
weights = np.exp(boost / kT)
# Maclaurin 展开到 2 阶
weights_approx = 1 + boost/kT + 0.5*(boost/kT)**2
print(f"Effective samples: {len(boost) / np.mean(weights):.0f}")
EOF

# 方案3: 延长模拟增加统计
export SIM_TIME=100000  # 100 ns
bash scripts/advanced/accelerated-md.sh
```

**预防:** 
- 使用 dual-boost 时 ALPHA 参数要更保守
- 确保 σ_boost < 10 kT

---

### ERROR-008: 检查点重启失败
**症状:**
```
ERROR: Cannot restart from checkpoint with different aMD parameters
```

**原因:** aMD 参数在重启时发生变化

**Fix:**
```bash
# 方案1: 使用相同参数重启
export AMD_E_DIHED=<原值>
export AMD_ALPHA_DIHED=<原值>
export AMD_E_TOT=<原值>
export AMD_ALPHA_TOT=<原值>
gmx mdrun -deffnm md -cpi md.cpt -append

# 方案2: 从头开始新模拟
rm -f md.cpt
bash scripts/advanced/accelerated-md.sh

# 方案3: 转换检查点 (如果参数变化不大)
gmx convert-tpr -s md.tpr -o md_new.tpr
gmx mdrun -s md_new.tpr -cpi md.cpt -deffnm md_new
```

**预防:** 记录 aMD 参数到日志文件

---

### ERROR-009: 内存不足
**症状:**
```
ERROR: Out of memory
Killed
```

**原因:**
- 系统过大
- 输出频率过高
- 多副本并行

**Fix:**
```bash
# 减少输出频率
export NSTXOUT=50000    # 每 100 ps 输出一次
export NSTVOUT=0        # 不输出速度
export NSTFOUT=0        # 不输出力
bash scripts/advanced/accelerated-md.sh

# 使用压缩输出
export COMPRESSED_X=yes
bash scripts/advanced/accelerated-md.sh

# 减少并行数
export NTOMP=2
bash scripts/advanced/accelerated-md.sh
```

**预防:** 根据系统大小调整输出频率

---

### ERROR-010: LINCS 警告
**症状:**
```
WARNING: LINCS failed to converge
Step 12345, time 24.69 (ps)  LINCS WARNING
```

**原因:**
- 加速导致键长约束不稳定
- 时间步长过大
- 系统受到过大扰动

**Fix:**
```bash
# 方案1: 减小时间步长
export DT=0.001  # 1 fs
bash scripts/advanced/accelerated-md.sh

# 方案2: 使用更保守的 aMD 参数
export AMD_ALPHA_DIHED=<增大50%>
export AMD_ALPHA_TOT=<增大50%>
bash scripts/advanced/accelerated-md.sh

# 方案3: 增加 LINCS 迭代次数
# 在 mdp 文件中添加:
# lincs-iter = 2
# lincs-order = 6

# 方案4: 使用 SHAKE 替代 LINCS
# constraints = h-bonds
# constraint-algorithm = shake
```

**预防:** 从保守参数开始，逐步增加加速强度

---

## 参数调优指南

### 推荐参数范围

**二面角加速 (Dihedral Boost):**
```bash
# 保守 (适合初次尝试)
AMD_E_DIHED = <avg_dihed + 3.5*std>
AMD_ALPHA_DIHED = 0.2 * <avg_dihed>

# 标准 (推荐)
AMD_E_DIHED = <avg_dihed + 4*std>
AMD_ALPHA_DIHED = 0.16 * <avg_dihed>

# 激进 (需要谨慎)
AMD_E_DIHED = <avg_dihed + 5*std>
AMD_ALPHA_DIHED = 0.12 * <avg_dihed>
```

**总能量加速 (Total Boost):**
```bash
# 保守
AMD_E_TOT = <avg_tot + 0.15*Natoms>
AMD_ALPHA_TOT = 0.15 * Natoms

# 标准
AMD_E_TOT = <avg_tot + 0.2*Natoms>
AMD_ALPHA_TOT = 0.16 * Natoms

# 激进
AMD_E_TOT = <avg_tot + 0.25*Natoms>
AMD_ALPHA_TOT = 0.12 * Natoms
```

### 加速类型选择

| 类型 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| dihedral | 蛋白质构象变化 | 针对性强，稳定 | 仅加速二面角 |
| total | 小分子，配体 | 全局加速 | 可能过于激进 |
| dual | 复杂体系 | 平衡性好 | 参数调优复杂 |

### 预运行时间建议

| 系统大小 | 预运行时间 | 说明 |
|---------|-----------|------|
| < 10k 原子 | 100 ps | 快速估计 |
| 10k-50k | 200-500 ps | 标准 |
| > 50k | 1 ns | 充分采样 |

---

## 性能优化

### 计算资源配置
```bash
# CPU 优化
export NTOMP=4              # 4 线程
export OMP_NUM_THREADS=4

# GPU 加速 (如果可用)
export GPU_ID=0
gmx mdrun -deffnm md -ntomp 4 -gpu_id 0

# 多节点并行 (MPI)
mpirun -np 4 gmx_mpi mdrun -deffnm md -ntomp 2
```

### 输出优化
```bash
# 减少输出频率 (节省磁盘空间)
export NSTXOUT=50000        # 每 100 ps
export NSTLOG=5000          # 每 10 ps
export NSTENERGY=5000       # 每 10 ps

# 压缩输出
export COMPRESSED_X=yes
```

---

## 结果验证

### 检查加速效果
```bash
# 1. Boost 能量统计
gmx energy -f md.edr -o boost.xvg
# 选择 Boost 相关项
# 期望: 平均 Boost > 0, σ_boost < 10 kT

# 2. 二面角分布
gmx angle -f md.xtc -n angle.ndx -od dihedral_dist.xvg
# 对比常规 MD: aMD 应覆盖更广的二面角空间

# 3. RMSD 分析
gmx rms -s md.tpr -f md.xtc -o rmsd.xvg
# 期望: aMD 的 RMSD 波动更大 (探索更多构象)

# 4. 自由能重构 (如果使用 PLUMED)
plumed sum_hills --hills HILLS --outfile fes.dat
```

### 质量检查清单
- [ ] Boost 能量分布合理 (σ < 10 kT)
- [ ] 系统稳定 (无 LINCS 警告)
- [ ] 采样增强明显 (RMSD/二面角分布更广)
- [ ] 能量守恒 (总能量无漂移)
- [ ] 温度稳定 (T = 300 ± 5 K)

---

## 方法对比

### aMD vs 其他增强采样方法

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| aMD | 简单，无需 CV | 重加权复杂 | 全局构象搜索 |
| Metadynamics | CV 明确，易重加权 | 需要选择 CV | 已知反应坐标 |
| REMD | 严格，易分析 | 计算量大 | 小系统，充足资源 |
| Umbrella | PMF 精确 | 需要反应路径 | 自由能计算 |

### 何时使用 aMD
- ✅ 探索蛋白质构象空间
- ✅ 配体结合路径搜索
- ✅ 不知道反应坐标
- ❌ 需要精确自由能 (用 Umbrella/Metadynamics)
- ❌ 系统过大 (> 100k 原子)

---

## 参考资料

### 关键文献
1. Hamelberg et al. (2004) - aMD 原始论文
2. Pierce et al. (2012) - Dual-boost aMD
3. Miao et al. (2014) - GaMD (高斯加速 MD)

### GROMACS 手册
- Chapter 7.3.24: Accelerated MD
- Chapter 5.8: Enhanced Sampling

### PLUMED 文档
- https://www.plumed.org/doc-v2.8/user-doc/html/_a_m_d.html

---

**最后更新:** 2026-04-09  
**版本:** 1.0  
**维护者:** AutoMD-GROMACS 项目组
