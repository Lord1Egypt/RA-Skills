# Non-Equilibrium MD 故障排查指南

## 常见错误及解决方案

### 1. 余弦加速相关错误

#### 错误: "cos-acceleration only works with integrator md"

**原因**: 余弦加速仅支持 `integrator = md`

**解决方案**:
```bash
# 检查 MDP 文件
grep "integrator" nemd.mdp

# 确保设置为 md
integrator = md
```

**自动修复**: 脚本已自动设置正确的积分器

---

#### 错误: 粘度值异常大或为负

**原因**:
- 加速度过大，系统远离平衡态
- 模拟时间不足，未达到稳态
- 温度控制不当

**解决方案**:
```bash
# 1. 减小加速度
COS_ACCEL=0.01 bash non-equilibrium.sh

# 2. 延长模拟时间
SIM_TIME=5000 bash non-equilibrium.sh

# 3. 检查温度稳定性
echo "Temperature" | gmx energy -f nemd.edr -o temperature.xvg
```

**诊断**:
```bash
# 检查速度剖面振幅
echo "Visco-Coeffic" | gmx energy -f nemd.edr -o visco.xvg
# 振幅应随时间趋于稳定
```

---

#### 错误: "1/Viscosity" 项不存在

**原因**: 能量文件中未记录粘度数据

**解决方案**:
```bash
# 检查能量文件内容
gmx energy -f nemd.edr

# 确认 cos-acceleration 已设置
grep "cos-acceleration" nemd.mdp

# 重新运行模拟
bash non-equilibrium.sh
```

---

### 2. 盒子变形相关错误

#### 错误: "deform can not be used with pressure coupling"

**原因**: 盒子变形与压力耦合冲突

**解决方案**:
```bash
# 确保 MDP 中禁用压力耦合
pcoupl = no
```

**自动修复**: 脚本已自动禁用压力耦合

---

#### 错误: 盒子变形过度，系统崩溃

**症状**:
- "Segmentation fault"
- "LINCS warning"
- 能量爆炸

**原因**: 变形速率过大

**解决方案**:
```bash
# 1. 减小变形速率
DEFORM_RATE=0.001 bash non-equilibrium.sh

# 2. 检查剪切率
# γ̇ = deform_rate / box_size
# 推荐: γ̇ < 0.01 ps⁻¹

# 3. 增加输出频率以监控
nstlog = 1000
nstxout-compressed = 1000
```

**预防**:
```bash
# 计算合理的变形速率
box_size=$(grep "box" system.gro | awk '{print $1}')
max_shear_rate=0.01  # ps⁻¹
max_deform_rate=$(echo "$max_shear_rate * $box_size" | bc -l)
echo "推荐最大变形速率: $max_deform_rate nm/ps"
```

---

#### 错误: 粒子穿过周期性边界

**症状**: 轨迹中分子被拉伸或断裂

**原因**: 变形导致粒子跨越周期性边界

**解决方案**:
```bash
# 使用 trjconv 修正周期性边界
echo "System" | gmx trjconv -s nemd.tpr -f nemd.xtc -o nemd_pbc.xtc -pbc mol

# 可视化检查
vmd nemd.gro nemd_pbc.xtc
```

---

### 3. 恒定加速相关错误

#### 错误: "Group X for acceleration not found"

**原因**: 指定的加速组不存在

**解决方案**:
```bash
# 1. 检查可用组
gmx make_ndx -f system.gro -o index.ndx
# 查看输出的组列表

# 2. 使用正确的组名
ACCEL_GROUPS="Protein" bash non-equilibrium.sh

# 3. 或创建自定义组
gmx make_ndx -f system.gro -o index.ndx
# 输入: a 1-100
# 输入: name 20 MyGroup
# 输入: q

# 使用自定义组
ACCEL_GROUPS="MyGroup" bash non-equilibrium.sh
```

---

#### 错误: 系统质心漂移

**症状**: 整个系统沿加速方向移动

**原因**: 质心运动未正确移除

**解决方案**:
```bash
# 方法1: 禁用质心运动移除（推荐）
comm-mode = None

# 方法2: 对非加速组施加反向加速度
# 例如: 加速 Protein，对 SOL 施加反向加速
acceleration-grps = Protein SOL
accelerate = 0.1 0 0
             -0.05 0 0  # 根据质量比调整
```

---

#### 错误: 加速组动能异常

**症状**: 温度控制失效，系统过热

**原因**: 加速组的动能贡献到系统总动能

**解决方案**:
```bash
# 1. 分别控制加速组和其他组的温度
tc-grps = Protein SOL
tau_t = 0.1 0.1
ref_t = 300 300

# 2. 减小加速度
ACCEL_X=0.01 bash non-equilibrium.sh

# 3. 监控温度
echo "Temperature" | gmx energy -f nemd.edr -o temp.xvg
```

---

### 4. 壁面流动相关错误

#### 错误: "Position restraint file not found"

**原因**: 缺少位置限制文件

**解决方案**:
```bash
# 1. 生成位置限制文件
echo "Wall" | gmx genrestr -f system.gro -o posre_wall.itp -fc 1000 1000 1000

# 2. 在拓扑文件中包含
# 编辑 topol.top，添加:
#ifdef POSRES
#include "posre_wall.itp"
#endif

# 3. 生成B态文件（沿X方向平移1nm）
awk '{
    if(NR<=2) print;
    else if(NF==6) printf "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n", $1,$2,$3,$4,$5+1.0,$6,$7;
    else print
}' posre_wall.itp > posre_wall_B.itp

# 4. 运行模拟
WALL_POSRE_B="posre_wall_B.itp" bash non-equilibrium.sh
```

---

#### 错误: lambda 超出范围

**症状**: "lambda out of range" 警告

**原因**: lambda 随时间线性增长，可能超过 [0,1]

**解决方案**:
```bash
# 这是正常的！lambda 可以超过1
# GROMACS 会正确处理周期性位移

# 如果担心，可以缩短模拟时间或减小 delta-lambda
WALL_SPEED=0.001 SIM_TIME=1000 bash non-equilibrium.sh
```

---

### 5. 通用错误

#### 错误: "LINCS warning"

**原因**: 约束失败，通常由于力过大

**解决方案**:
```bash
# 1. 减小驱动力/速率
COS_ACCEL=0.01 bash non-equilibrium.sh
# 或
DEFORM_RATE=0.001 bash non-equilibrium.sh

# 2. 减小时间步长
DT=0.001 bash non-equilibrium.sh

# 3. 增加 LINCS 迭代次数
lincs_iter = 2
lincs_order = 6

# 4. 检查初始结构是否合理
gmx energy -f em.edr -o potential.xvg
# 确保能量最小化充分
```

---

#### 错误: 能量爆炸

**症状**: 势能或动能急剧增大

**原因**:
- 驱动力过大
- 时间步长过大
- 初始结构不合理

**解决方案**:
```bash
# 1. 检查能量
echo "Potential Kinetic" | gmx energy -f nemd.edr -o energy.xvg

# 2. 减小驱动参数
COS_ACCEL=0.001 bash non-equilibrium.sh

# 3. 重新平衡
# 先运行短时间低强度模拟
SIM_TIME=100 COS_ACCEL=0.01 bash non-equilibrium.sh
# 然后使用输出作为新的输入
INPUT_GRO=non-equilibrium/nemd.gro INPUT_CPT=non-equilibrium/nemd.cpt \
    SIM_TIME=1000 COS_ACCEL=0.1 bash non-equilibrium.sh
```

---

#### 错误: 模拟速度极慢

**原因**:
- 输出频率过高
- 系统过大
- 未使用 GPU

**解决方案**:
```bash
# 1. 减少输出频率
nstlog = 10000
nstxout-compressed = 10000

# 2. 使用 GPU
GPU_ID=0 bash non-equilibrium.sh

# 3. 增加 OpenMP 线程
NTOMP=8 bash non-equilibrium.sh

# 4. 检查性能
gmx mdrun -v -deffnm nemd -ntomp 4 -gpu_id 0 -tunepme yes
```

---

### 6. 分析相关错误

#### 错误: 速度剖面不符合预期

**症状**: 速度分布不是余弦形状

**原因**:
- 模拟时间不足
- 加速度过大
- 系统未达到稳态

**解决方案**:
```bash
# 1. 延长模拟时间
SIM_TIME=5000 bash non-equilibrium.sh

# 2. 检查稳态
# 绘制速度振幅 vs 时间
echo "Visco-Coeffic" | gmx energy -f nemd.edr -o visco.xvg
# 应该趋于平台

# 3. 丢弃初始不稳定部分
echo "Visco-Coeffic" | gmx energy -f nemd.edr -o visco.xvg -b 1000
```

---

#### 错误: 粘度值与实验不符

**原因**:
- 力场参数不准确
- 剪切率过高（剪切变稀）
- 温度/压力控制不当
- 系统尺寸效应

**解决方案**:
```bash
# 1. 检查剪切率
# 计算有效剪切率
box_z=$(grep "box" system.gro | awk '{print $3}')
shear_rate=$(echo "2 * 3.14159 * $COS_ACCEL / ($box_z * $box_z)" | bc -l)
echo "剪切率: $shear_rate ps⁻¹"

# 2. 运行多个剪切率
for accel in 0.01 0.05 0.1 0.5 1.0; do
    COS_ACCEL=$accel OUTPUT_DIR=nemd_$accel bash non-equilibrium.sh
done
# 外推到零剪切率

# 3. 增大系统尺寸
# 使用 genconf 复制系统
gmx genconf -f system.gro -o system_large.gro -nbox 2 2 2

# 4. 检查温度和压力
echo "Temperature Pressure" | gmx energy -f nemd.edr -o temp_pres.xvg
```

---

## 诊断流程

### 快速诊断

```bash
# 1. 检查模拟是否完成
grep "Finished mdrun" nemd.log

# 2. 检查能量稳定性
echo "Potential Temperature" | gmx energy -f nemd.edr -o check.xvg

# 3. 检查警告和错误
grep -i "warning\|error\|fatal" nemd.log

# 4. 检查输出文件
ls -lh nemd.{xtc,edr,log}
```

### 详细诊断

```bash
# 1. 能量分析
gmx energy -f nemd.edr
# 查看所有可用能量项

# 2. 轨迹检查
gmx check -f nemd.xtc
# 检查帧数、时间范围

# 3. 结构检查
echo "Backbone" | gmx rms -s nemd.tpr -f nemd.xtc -o rmsd.xvg
# RMSD 应该稳定（对于流动系统可能有漂移）

# 4. 温度分布
echo "System" | gmx traj -f nemd.xtc -s nemd.tpr -ot temp.xvg
```

---

## 性能优化

### 提高模拟速度

```bash
# 1. 使用 GPU
GPU_ID=0 bash non-equilibrium.sh

# 2. 优化 PME 参数
gmx tune_pme -s nemd.tpr -np 4

# 3. 调整输出频率
nstlog = 10000
nstxout-compressed = 10000

# 4. 使用更大的 nstlist
nstlist = 20  # 默认10
```

### 减少内存使用

```bash
# 1. 压缩轨迹
compressed-x-precision = 1000  # 默认1000，可增大到10000

# 2. 减少输出
nstxout = 0
nstvout = 0
nstfout = 0

# 3. 仅输出关键组
compressed-x-grps = Protein  # 而非 System
```

---

## 参数调优指南

### 余弦加速法

| 参数 | 推荐范围 | 说明 |
|------|----------|------|
| COS_ACCEL | 0.01-1.0 nm/ps² | 取决于系统粘度 |
| SIM_TIME | 1000-10000 ps | 需要达到稳态 |
| 剪切率 | < 0.1 ps⁻¹ | 避免剪切变稀 |

### 盒子变形法

| 参数 | 推荐范围 | 说明 |
|------|----------|------|
| DEFORM_RATE | 0.001-0.01 nm/ps | 取决于盒子尺寸 |
| 剪切率 | < 0.01 ps⁻¹ | rate/box_size |
| SIM_TIME | 2000-20000 ps | 需要更长时间 |

### 恒定加速法

| 参数 | 推荐范围 | 说明 |
|------|----------|------|
| ACCEL_X/Y/Z | 0.01-1.0 nm/ps² | 根据应用调整 |
| SIM_TIME | 1000-5000 ps | 取决于流动建立时间 |

---

## 常见问题 FAQ

**Q: 如何选择非平衡方法？**

A: 
- 简单液体粘度测量 → 余弦加速法
- 一般剪切流动 → 盒子变形法
- 复杂流动/多组分 → 恒定加速法
- 壁面效应研究 → 壁面驱动法

**Q: 如何判断系统是否达到稳态？**

A: 监控以下量随时间的变化：
- 速度剖面振幅（余弦法）
- 应力张量（变形法）
- 温度和压力
- 应该趋于平台，涨落稳定

**Q: 剪切变稀如何检测？**

A: 运行多个剪切率，绘制 η vs γ̇ 曲线。如果粘度随剪切率降低，说明存在剪切变稀。

**Q: 如何提高粘度测量精度？**

A:
1. 延长模拟时间
2. 增大系统尺寸
3. 运行多个独立模拟取平均
4. 使用更小的剪切率

**Q: 非平衡模拟需要多长时间？**

A: 至少需要系统达到稳态 + 足够的统计采样时间。通常：
- 简单液体: 1-5 ns
- 聚合物: 10-100 ns
- 生物大分子: 5-50 ns

---

## 参考资源

- GROMACS Manual: https://manual.gromacs.org/
- GROMACS 论坛: https://gromacs.bioexcel.eu/
- 相关论文:
  - Hess (2002). J. Chem. Phys. 116, 209
  - Müller-Plathe (1997). Phys. Rev. E 59, 4894
