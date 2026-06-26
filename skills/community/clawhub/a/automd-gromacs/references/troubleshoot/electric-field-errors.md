# Electric Field 模拟故障排查

## 常见错误及解决方案

### ERROR-001: 电场强度不合理

**症状**:
```
[WARN] 电场强度过大 (2.5 > 2.0 V/nm)
```

**原因**:
- 电场强度超出推荐范围
- 可能导致系统不稳定或非物理行为

**解决方案**:
```bash
# 1. 检查系统类型
# 生物系统: 0.001-0.1 V/nm
# 材料系统: 0.1-2.0 V/nm

# 2. 调整电场强度
FIELD_STRENGTH_Z=0.05  # 生物系统推荐值

# 3. 如果需要强电场,增加平衡时间
SIM_TIME=5000  # 延长到 5 ns
```

**预防措施**:
- 从小电场开始 (0.01 V/nm)
- 逐步增加强度
- 监控系统稳定性 (RMSD, 温度, 压力)

---

### ERROR-002: 振荡参数配置错误

**症状**:
```
[WARN] 角频率过小 (0.5 < 1 ps^-1)
[AUTO-FIX] 增加到 10 ps^-1
```

**原因**:
- 角频率 ω 设置不合理
- 振荡周期与模拟时间不匹配

**解决方案**:
```bash
# 1. 计算合理的角频率
# 周期 T = 2π/ω
# 推荐: 至少观察 5-10 个周期

# 示例: 模拟 1 ns, 周期 100 ps
FIELD_OMEGA=$(echo "2 * 3.14159 / 100" | bc -l)  # ≈ 0.063 ps^-1

# 2. 或使用典型值
FIELD_OMEGA=150  # 对应周期 ≈ 0.042 ps (微波频率)

# 3. 检查中心时间
FIELD_T0=$(echo "$SIM_TIME / 2" | bc -l)  # 模拟中点
```

**参考频率**:
- 微波: 100-500 ps⁻¹ (THz 范围)
- 红外: 1000-10000 ps⁻¹
- 可见光: > 10000 ps⁻¹ (超出 MD 时间步长)

---

### ERROR-003: 脉冲宽度不合理

**症状**:
```
[WARN] 脉冲宽度过大 (600 > 500 ps)
[AUTO-FIX] 减少到模拟时间的 1/4
```

**原因**:
- 脉冲宽度 σ 过大,接近或超过模拟时间
- 脉冲效果不明显

**解决方案**:
```bash
# 1. 脉冲宽度应为模拟时间的 1/10 - 1/4
SIM_TIME=1000
FIELD_SIGMA=$(echo "$SIM_TIME / 10" | bc -l)  # 100 ps

# 2. FWHM (半高全宽) = 2.355 × σ
# 确保 FWHM 在合理范围内

# 3. 调整中心时间确保脉冲在模拟窗口内
FIELD_T0=$(echo "$SIM_TIME / 2" | bc -l)
```

**验证**:
```bash
# 使用 -field 选项查看电场曲线
gmx mdrun -v -deffnm efield -field
# 检查 field.xvg 文件
```

---

### ERROR-004: 电场方向配置错误

**症状**:
```
[WARN] 所有方向电场强度为 0
[AUTO-FIX] 根据 FIELD_DIRECTION 设置默认值
```

**原因**:
- 未正确设置电场强度
- 方向参数与强度参数不匹配

**解决方案**:
```bash
# 方法 1: 使用 FIELD_DIRECTION 自动设置
FIELD_DIRECTION=z  # 自动设置 FIELD_STRENGTH_Z=0.05

# 方法 2: 手动设置各方向强度
FIELD_STRENGTH_X=0.0
FIELD_STRENGTH_Y=0.0
FIELD_STRENGTH_Z=0.05

# 方法 3: 多方向电场
FIELD_DIRECTION=xy
# 自动设置 X=0.035, Y=0.035 (保持总强度 ≈ 0.05)

# 方法 4: 自定义多方向
FIELD_STRENGTH_X=0.03
FIELD_STRENGTH_Y=0.04
FIELD_STRENGTH_Z=0.0
```

**多方向电场强度计算**:
```bash
# 总强度 E_total = √(Ex² + Ey² + Ez²)
# 示例: 要求总强度 0.05 V/nm, 沿 xy 对角线
E_total=0.05
E_x=$(echo "$E_total / sqrt(2)" | bc -l)  # 0.0354
E_y=$E_x
```

---

### ERROR-005: MDP 参数冲突

**症状**:
```
ERROR 1 [file efield.mdp]:
  electric-field-x requires 4 parameters
```

**原因**:
- MDP 文件中电场参数格式错误
- 参数数量不正确

**解决方案**:
```bash
# 正确格式: E0 omega t0 sigma
# 所有 4 个参数都必须提供

# 恒定电场
electric-field-x = 0.05 0 0 0

# 振荡电场 (sigma=0)
electric-field-x = 0.05 150 0 0

# 脉冲电场
electric-field-x = 0.05 150 5 1

# 错误示例 (缺少参数)
# electric-field-x = 0.05  # ❌ 错误
```

---

### ERROR-006: 系统不稳定

**症状**:
```
Step 12500, time 25 (ps)  LINCS WARNING
relative constraint deviation after LINCS:
```

**原因**:
- 电场过强导致系统不稳定
- 时间步长过大
- 约束算法失败

**解决方案**:
```bash
# 1. 减小电场强度
FIELD_STRENGTH_Z=0.01  # 从小值开始

# 2. 减小时间步长
DT=0.001  # 从 2 fs 减到 1 fs

# 3. 增加约束迭代次数 (修改 MDP)
lincs_iter = 2  # 默认 1
lincs_order = 6  # 默认 4

# 4. 使用更严格的约束
constraints = all-bonds  # 约束所有键

# 5. 分阶段施加电场
# 第一阶段: 弱电场平衡
FIELD_STRENGTH_Z=0.01 SIM_TIME=100 OUTPUT_DIR=efield_eq
# 第二阶段: 目标电场
INPUT_CPT=efield_eq/efield.cpt FIELD_STRENGTH_Z=0.05
```

---

### ERROR-007: 偶极矩分析失败

**症状**:
```
[WARN] 偶极矩分析失败
Fatal error: Group Mu-X not found
```

**原因**:
- 系统中没有定义偶极矩组
- 索引文件缺失或不正确

**解决方案**:
```bash
# 1. 检查系统是否有偶极矩
# 需要有电荷分布的分子 (水、蛋白质等)

# 2. 使用正确的组名
echo "System" | gmx dipoles -f efield.xtc -s efield.tpr -o dipole.xvg

# 3. 如果系统无偶极矩,跳过分析
ANALYZE_DIPOLE=no

# 4. 对于特定分子的偶极矩
echo "Protein" | gmx dipoles -f efield.xtc -s efield.tpr -o dipole_protein.xvg
```

---

### ERROR-008: 周期性边界条件效应

**症状**:
- 实际观察到的电场效应比预期强
- 系统行为异常

**原因**:
- PBC 下有效电场强度被放大
- 修正因子取决于盒子大小和介电性质

**解决方案**:
```bash
# 1. 使用更大的盒子
# 减小 PBC 效应
gmx editconf -f system.gro -o system_large.gro -box 8 8 8

# 2. 考虑修正因子
# E_effective = E_applied × correction_factor
# correction_factor 通常 > 1

# 3. 从文献获取修正因子
# 或通过测试确定

# 4. 对于膜系统,考虑使用 Computational Electrophysiology
# (swapcoords 选项,见 GROMACS Manual 5.8.8)
```

**参考**:
- English & MacElroy (2003). J. Chem. Phys. 118, 1589
- GROMACS Manual 5.8.7 (Supporting Information)

---

### ERROR-009: GPU 加速问题

**症状**:
```
NOTE: PME load balancing is not supported with GPUs
```

**原因**:
- 某些 GPU 功能与电场模拟不兼容
- PME 负载平衡在 GPU 上受限

**解决方案**:
```bash
# 1. 禁用 PME 负载平衡 (MDP)
# (通常自动处理)

# 2. 如果 GPU 出现问题,使用 CPU
# 不指定 GPU_ID

# 3. 或使用混合模式
GPU_ID=0  # PME 在 CPU, 非键在 GPU

# 4. 检查 GROMACS GPU 支持
gmx mdrun -h | grep -i gpu
```

---

### ERROR-010: 能量漂移

**症状**:
- 总能量持续上升或下降
- 系统不守恒

**原因**:
- 电场做功导致能量变化 (正常)
- 或时间步长/截断半径不合理

**解决方案**:
```bash
# 1. 区分正常能量变化和漂移
# 电场做功: ΔE = ∫ F·dx = q·E·Δx
# 这是物理的,不是错误

# 2. 检查能量守恒 (无电场对照)
FIELD_STRENGTH_Z=0.0 OUTPUT_DIR=no_field

# 3. 如果确实漂移,减小时间步长
DT=0.001

# 4. 增加截断半径
rcoulomb = 1.2
rvdw = 1.2

# 5. 使用更精确的 PME 参数
pme_order = 6
fourierspacing = 0.10
```

---

## 调试流程

### 1. 基础检查
```bash
# 检查输入文件
gmx check -f system.gro
gmx dump -s efield.tpr | grep "electric-field"

# 检查 MDP 配置
grep "electric-field" efield.mdp
```

### 2. 测试运行
```bash
# 短时间测试
SIM_TIME=10 OUTPUT_DIR=test_efield bash electric-field.sh

# 检查日志
grep -i "error\|warning\|fatal" test_efield/efield.log
```

### 3. 可视化验证
```bash
# 查看电场曲线 (如果使用 -field)
xmgrace field.xvg

# 查看轨迹
gmx view -f efield.xtc -s efield.tpr
```

### 4. 对比分析
```bash
# 无电场对照
FIELD_STRENGTH_Z=0.0 OUTPUT_DIR=control bash electric-field.sh

# 比较 RMSD
echo "Backbone Backbone" | gmx rms -s control/efield.tpr -f control/efield.xtc -o rmsd_control.xvg
echo "Backbone Backbone" | gmx rms -s efield/efield.tpr -f efield/efield.xtc -o rmsd_efield.xvg
```

---

## 性能优化

### 1. 并行化
```bash
# OpenMP 线程数
NTOMP=8  # 根据 CPU 核心数调整

# GPU 加速
GPU_ID=0

# MPI (多节点)
mpirun -np 4 gmx_mpi mdrun -v -deffnm efield
```

### 2. 输出频率
```bash
# 减少输出频率以节省磁盘空间
# 修改 MDP:
nstxout-compressed = 10000  # 每 20 ps 输出一帧
nstlog = 10000
```

### 3. 截断优化
```bash
# 平衡精度和速度
rcoulomb = 1.0  # 默认
rvdw = 1.0
```

---

## 最佳实践

1. **从小电场开始**: 0.01 V/nm → 0.05 V/nm → 目标值
2. **充分平衡**: 在施加电场前确保系统已平衡
3. **监控稳定性**: 实时检查 RMSD, 温度, 压力
4. **对照实验**: 始终运行无电场对照
5. **文献验证**: 参考类似系统的电场强度
6. **PBC 注意**: 考虑周期性边界条件的影响
7. **物理合理性**: 检查结果是否符合物理预期

---

## 参考资源

- GROMACS Manual 3.7: MDP options (electric-field-x/y/z)
- GROMACS Manual 5.8.7: Electric fields
- English & MacElroy (2003). Molecular dynamics simulations of microwave heating
- Saitta et al. (2012). Miller experiments in atomistic simulations
