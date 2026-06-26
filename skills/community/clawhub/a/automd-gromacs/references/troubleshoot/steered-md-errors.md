# Steered MD 故障排查指南

## 常见错误场景

### ERROR-001: 拉力组定义错误

**症状**:
```
Fatal error:
Group 'Ligand' not found in index file
```

**原因**: 索引文件中不存在指定的拉力组

**解决方案**:
```bash
# 1. 查看可用组
gmx make_ndx -f system.gro -n index.ndx
# 输入 'q' 退出并查看组列表

# 2. 创建自定义组
gmx make_ndx -f system.gro -o index.ndx
# 输入: r LIG (选择残基名为LIG的原子)
# 输入: name 20 Ligand (将组20命名为Ligand)
# 输入: q (保存退出)

# 3. 重新运行
INPUT_NDX=index.ndx PULL_GROUP2=Ligand ./steered-md.sh
```

**自动修复**: 脚本会自动生成默认索引文件并列出可用组

---

### ERROR-002: 拉力速率不合理

**症状**:
```
Warning: pull rate is very high (0.5 nm/ps)
System may become unstable
```

**原因**: 拉力速率过大导致系统不稳定

**推荐值**:
- **Constant velocity**: 0.001-0.01 nm/ps (慢速拉伸)
- **Constant force**: 100-1000 kJ/mol/nm

**解决方案**:
```bash
# 减小拉力速率
PULL_RATE=0.005 ./steered-md.sh

# 或增加模拟时间以获得相同的总位移
SIM_TIME=5000 PULL_RATE=0.002 ./steered-md.sh
```

**自动修复**: 脚本会自动调整到推荐范围

---

### ERROR-003: 几何配置错误

**症状**:
```
Fatal error:
pull-coord1-geometry = angle requires 3 groups
Only 2 groups provided
```

**原因**: 拉力几何类型与提供的组数量不匹配

**几何类型要求**:
- `distance`: 2组 (参考组 + 拉力组)
- `direction`: 2组 + 方向向量
- `cylinder`: 2组 + 方向向量 + 半径
- `angle`: 3组 (定义角度的三个点)
- `dihedral`: 6组 (定义二面角的六个点)

**解决方案**:
```bash
# angle 几何
PULL_GEOMETRY=angle \
PULL_GROUP1=Protein \
PULL_GROUP2=Ligand \
PULL_GROUP3=System \
./steered-md.sh

# dihedral 几何
PULL_GEOMETRY=dihedral \
PULL_GROUP1=G1 PULL_GROUP2=G2 \
PULL_GROUP3=G3 PULL_GROUP4=G4 \
PULL_GROUP5=G5 PULL_GROUP6=G6 \
./steered-md.sh
```

**自动修复**: 脚本会验证组数量并提供默认值

---

### ERROR-004: 初始距离检测失败

**症状**:
```
Warning: Could not auto-detect initial distance
Using default value 0.0
```

**原因**: 无法自动计算两组之间的初始距离

**解决方案**:
```bash
# 手动指定初始距离
PULL_INIT=2.5 ./steered-md.sh

# 或使用 gmx distance 手动计算
echo "Protein Ligand" | gmx distance -s system.gro -n index.ndx \
    -select "com of group Protein" -select2 "com of group Ligand"
```

**自动修复**: 脚本会尝试使用 gmx distance 自动检测

---

### ERROR-005: 拉力方向未定义

**症状**:
```
Fatal error:
pull-coord1-geometry = direction requires pull-coord1-vec
```

**原因**: direction 几何需要指定拉力方向向量

**解决方案**:
```bash
# 指定拉力方向 (归一化向量)
PULL_GEOMETRY=direction PULL_VEC="0 0 1" ./steered-md.sh  # Z方向
PULL_GEOMETRY=direction PULL_VEC="1 0 0" ./steered-md.sh  # X方向
PULL_GEOMETRY=direction PULL_VEC="0.707 0.707 0" ./steered-md.sh  # XY对角线
```

**默认值**: `0 0 1` (Z方向)

---

### ERROR-006: 圆柱半径过大

**症状**:
```
Warning: pull-cylinder-r (2.5 nm) is larger than half the box size
This may cause artifacts
```

**原因**: 圆柱半径超过盒子尺寸的一半

**解决方案**:
```bash
# 减小圆柱半径
CYLINDER_R=1.0 ./steered-md.sh

# 或增大盒子尺寸 (在系统准备阶段)
gmx editconf -f system.gro -o system_box.gro -box 8 8 8
```

**推荐值**: < 盒子最小边长的 40%

---

### ERROR-007: 模拟崩溃 (LINCS warning)

**症状**:
```
Step 12450: LINCS WARNING
relative constraint deviation after LINCS:
max 15.234 (between atoms 1234 and 1235)
```

**原因**: 拉力过大或速率过快导致约束失败

**解决方案**:
```bash
# 1. 减小拉力速率
PULL_RATE=0.001 ./steered-md.sh

# 2. 减小时间步长
DT=0.001 ./steered-md.sh

# 3. 使用更强的约束算法
# 在 MDP 中设置:
# lincs_iter = 2
# lincs_order = 6

# 4. 增加弹簧常数 (constant-velocity模式)
PULL_K=2000 ./steered-md.sh
```

**自动修复**: 脚本会从检查点重启

---

### ERROR-008: 拉力数据缺失

**症状**:
```
Warning: pullf.xvg not found
Cannot analyze force curve
```

**原因**: 
- 模拟未完成
- 输出频率设置错误
- 磁盘空间不足

**解决方案**:
```bash
# 1. 检查模拟是否完成
grep "Finished mdrun" pull.log

# 2. 检查磁盘空间
df -h .

# 3. 检查输出频率 (在 MDP 中)
# pull-nstxout = 100
# pull-nstfout = 100

# 4. 从检查点重启
cd steered-md
gmx mdrun -v -deffnm pull -cpi pull.cpt
```

---

### ERROR-009: 伞状采样窗口生成失败

**症状**:
```
Warning: Only constant-velocity mode supports umbrella window generation
```

**原因**: 仅 constant-velocity 模式可以自动生成伞状采样窗口

**解决方案**:
```bash
# 使用 constant-velocity 模式
PULL_MODE=constant-velocity PULL_RATE=0.01 ./steered-md.sh

# 或手动创建窗口配置
cat > umbrella_windows.dat << EOF
# window_id  distance(nm)  spring_constant(kJ/mol/nm²)
0  1.0  1000
1  1.1  1000
2  1.2  1000
...
EOF
```

---

### ERROR-010: 多组拉力配置错误

**症状**:
```
Fatal error:
pull-ncoords = 1 but multiple pull coordinates requested
```

**原因**: 当前脚本仅支持单个拉力坐标

**解决方案**:
```bash
# 如需多个拉力坐标,手动编辑 MDP 文件:
cat >> pull.mdp << EOF
pull-ncoords            = 2

; Coordinate 2
pull-coord2-geometry    = distance
pull-coord2-groups      = 1 3
pull-coord2-type        = umbrella
pull-coord2-k           = 1000
EOF

# 然后手动运行 grompp 和 mdrun
gmx grompp -f pull.mdp -c system.gro -p topol.top -o pull.tpr
gmx mdrun -v -deffnm pull
```

---

## 性能优化

### 优化-001: GPU 加速

```bash
# 使用 GPU
GPU_ID=0 ./steered-md.sh

# 多 GPU
GPU_ID="0 1" NTOMP=2 ./steered-md.sh
```

### 优化-002: 并行化

```bash
# 增加 OpenMP 线程
NTOMP=8 ./steered-md.sh

# 注意: 拉力模拟通常不支持 MPI 并行
```

### 优化-003: 减少输出频率

```bash
# 编辑 MDP 文件
sed -i 's/nstxout-compressed      = 5000/nstxout-compressed      = 10000/' pull.mdp
sed -i 's/pull-nstxout            = 100/pull-nstxout            = 500/' pull.mdp
```

---

## 结果验证

### 检查-001: 拉力曲线合理性

```bash
# 查看拉力统计
cat force_stats.txt

# 预期:
# - 平均力: 正值 (拉伸) 或负值 (压缩)
# - 标准差: < 平均力的 50%
# - 无异常尖峰
```

### 检查-002: 距离变化

```bash
# 绘制距离-时间曲线
xmgrace pullx.xvg

# 预期:
# - constant-velocity: 线性增长
# - constant-force: 非线性增长
# - umbrella: 围绕参考值振荡
```

### 检查-003: 能量守恒

```bash
# 提取总能量
echo "Total-Energy" | gmx energy -f pull.edr -o energy.xvg

# 预期: 能量漂移 < 0.5% (NVT) 或 1% (NPT)
```

---

## 参考资料

- GROMACS Manual 5.8.4: Pull Code
- Izrailev et al. (1997). Steered molecular dynamics
- Jarzynski (1997). Nonequilibrium equality for free energy differences
- Park & Schulten (2004). Calculating potentials of mean force from SMD

---

## 快速诊断流程

```bash
# 1. 检查输入文件
ls -lh system.gro topol.top index.ndx

# 2. 验证拉力组
grep "^\[" index.ndx

# 3. 检查 MDP 配置
grep "pull" pull.mdp

# 4. 查看模拟日志
tail -100 pull.log

# 5. 检查输出文件
ls -lh pull*.xvg

# 6. 分析拉力曲线
xmgrace pullf.xvg pullx.xvg
```
