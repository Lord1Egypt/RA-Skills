# Equilibration Errors - 故障排查手册

**适用脚本:** `scripts/basic/equilibration.sh`

---

## ERROR-001: grompp 失败 (NVT)

### 症状
```
ERROR-001: grompp 失败
Fatal error:
Too many warnings (1)
```

### 可能原因
1. **拓扑文件问题**
   - 缺少位置约束文件 `posre.itp`
   - 拓扑文件路径错误

2. **输入结构问题**
   - 能量最小化未完成
   - 结构文件损坏

3. **MDP 参数冲突**
   - `tc-grps` 与拓扑不匹配
   - 约束参数设置错误

### 解决方案

**方案 1: 检查位置约束文件**
```bash
# 检查 posre.itp 是否存在
ls -lh posre*.itp

# 如果缺失,重新生成拓扑
gmx pdb2gmx -f protein.pdb -o protein.gro -water spce
```

**方案 2: 禁用位置约束**
```bash
# 运行时设置环境变量
export RESTRAINT=none
./equilibration.sh
```

**方案 3: 增加警告容忍度**
```bash
# 修改脚本中的 -maxwarn 参数
gmx grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr -maxwarn 2
```

**方案 4: 检查温度耦合组**
```bash
# 查看拓扑中的分子类型
grep "^\[ molecules \]" -A 10 topol.top

# 确保 tc-grps 匹配
# 如果只有蛋白质,修改为:
tc-grps = Protein
tau_t   = 0.1
ref_t   = 300
```

---

## ERROR-002: NVT 模拟失败

### 症状
```
ERROR-002: NVT 模拟失败
Step 1234, time 2.468 (ps)  LINCS WARNING
relative constraint deviation after LINCS:
```

### 可能原因
1. **能量最小化不充分**
   - 系统存在高能接触
   - 力过大导致约束失败

2. **时间步长过大**
   - 默认 2 fs 对某些系统过大
   - 需要更小的时间步长

3. **温度过高**
   - 初始速度生成温度过高
   - 导致原子运动过快

### 解决方案

**方案 1: 加强能量最小化**
```bash
# 重新进行更严格的能量最小化
gmx grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em

# 检查最终能量
tail em.log | grep "Potential Energy"
# 应该 < -500000 kJ/mol (对于 1AKI 系统)
```

**方案 2: 减小时间步长**
```bash
# 修改 NVT_STEPS 以保持总时间不变
export NVT_STEPS=100000  # 1 fs * 100000 = 100 ps
# 在 nvt.mdp 中设置 dt = 0.001
```

**方案 3: 降低初始温度**
```bash
# 分阶段升温
export TEMPERATURE=100
./equilibration.sh

# 然后继续升温到 300 K
export TEMPERATURE=300
export INPUT_GRO=equilibration/nvt.gro
./equilibration.sh
```

**方案 4: 增强位置约束**
```bash
# 使用更强的约束力常数
export RESTRAINT_FC=5000  # 默认 1000
./equilibration.sh
```

---

## ERROR-003: grompp 失败 (NPT)

### 症状
```
ERROR-003: grompp 失败
Fatal error:
Continuation run requested, but no checkpoint file found
```

### 可能原因
1. **NVT 检查点文件缺失**
   - NVT 模拟未正常完成
   - 文件被意外删除

2. **文件路径错误**
   - 脚本在错误的目录运行
   - 相对路径不正确

### 解决方案

**方案 1: 检查 NVT 输出**
```bash
# 确认 NVT 完成
ls -lh equilibration/nvt.*

# 应该包含:
# nvt.gro  - 结构文件
# nvt.cpt  - 检查点文件
# nvt.edr  - 能量文件
```

**方案 2: 重新运行 NVT**
```bash
# 如果 NVT 未完成,重新运行
cd equilibration
gmx mdrun -v -deffnm nvt -cpi nvt.cpt  # 从检查点继续
```

**方案 3: 不使用检查点**
```bash
# 修改 npt.mdp
continuation = no
gen_vel      = yes
gen_temp     = 300

# 重新生成 TPR (不使用 -t 选项)
gmx grompp -f npt.mdp -c nvt.gro -p topol.top -o npt.tpr
```

---

## ERROR-004: NPT 模拟失败

### 症状
```
ERROR-004: NPT 模拟失败
Step 5678, time 11.356 (ps)
Pressure scaling more than 1%, mu: 1.05 1.05 1.05
```

### 可能原因
1. **压强耦合过强**
   - `tau_p` 过小
   - 系统响应过快

2. **体系未充分平衡**
   - NVT 时间过短
   - 温度未稳定

3. **Parrinello-Rahman 过早使用**
   - 应先用 Berendsen 预平衡
   - 再切换到 Parrinello-Rahman

### 解决方案

**方案 1: 延长 NVT 平衡**
```bash
# 增加 NVT 步数
export NVT_STEPS=100000  # 200 ps
./equilibration.sh
```

**方案 2: 调整压强耦合参数**
```bash
# 在 npt.mdp 中修改
tau_p = 5.0  # 增大到 5.0 ps (默认 2.0)
```

**方案 3: 分阶段压强耦合**
```bash
# 第一阶段: Berendsen (快速预平衡)
pcoupl = Berendsen
tau_p  = 2.0

# 运行 50 ps
gmx mdrun -v -deffnm npt_berendsen -nsteps 25000

# 第二阶段: Parrinello-Rahman (精确平衡)
pcoupl = Parrinello-Rahman
tau_p  = 2.0

# 继续运行
gmx grompp -f npt_pr.mdp -c npt_berendsen.gro -t npt_berendsen.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt
```

---

## ERROR-005: 温度分析失败

### 症状
```
ERROR-005: 温度分析失败
Fatal error:
No such energy term: Temperature
```

### 可能原因
1. **能量文件损坏**
   - EDR 文件不完整
   - 模拟异常终止

2. **能量项名称错误**
   - 不同版本的 GROMACS 名称可能不同

### 解决方案

**方案 1: 查看可用能量项**
```bash
# 列出所有能量项
gmx energy -f nvt.edr

# 常见温度相关项:
# - Temperature
# - T-Protein
# - T-non-Protein
```

**方案 2: 使用正确的能量项名称**
```bash
# 如果是分组温度
echo "T-Protein" | gmx energy -f nvt.edr -o temperature.xvg
```

**方案 3: 重新运行模拟**
```bash
# 如果 EDR 文件损坏,重新运行
rm nvt.edr nvt.log
gmx mdrun -v -deffnm nvt -cpi nvt.cpt
```

---

## ERROR-006: 压强分析失败

### 症状
```
ERROR-006: 压强分析失败
Fatal error:
No such energy term: Pressure
```

### 可能原因
1. **NVT 阶段无压强**
   - NVT 不控制压强
   - 应分析 NPT 的 EDR 文件

2. **能量项名称错误**

### 解决方案

**方案 1: 确认使用 NPT 文件**
```bash
# 压强只在 NPT 阶段有效
echo "Pressure" | gmx energy -f npt.edr -o pressure.xvg
```

**方案 2: 查看可用压强项**
```bash
gmx energy -f npt.edr

# 常见压强相关项:
# - Pressure
# - Pres-XX, Pres-YY, Pres-ZZ (各向异性)
```

---

## ERROR-007: 密度分析失败

### 症状
```
ERROR-007: 密度分析失败
Fatal error:
No such energy term: Density
```

### 可能原因
同 ERROR-006

### 解决方案

**方案 1: 使用 NPT 文件**
```bash
echo "Density" | gmx energy -f npt.edr -o density.xvg
```

**方案 2: 手动计算密度**
```bash
# 从轨迹计算
gmx density -f npt.xtc -s npt.tpr -o density_profile.xvg
```

---

## 常见问题

### Q1: 温度/压强/密度波动很大

**原因:** 平衡时间不足

**解决方案:**
```bash
# 延长平衡时间
export NVT_STEPS=100000  # 200 ps
export NPT_STEPS=100000  # 200 ps
./equilibration.sh
```

### Q2: 系统体积剧烈变化

**原因:** 初始密度不合理

**解决方案:**
```bash
# 在溶剂化时指定盒子大小
gmx editconf -f protein.gro -o box.gro -c -d 1.0 -bt cubic
gmx solvate -cp box.gro -cs spc216.gro -o solvated.gro -p topol.top
```

### Q3: 蛋白质结构变形

**原因:** 位置约束不足或过强

**解决方案:**
```bash
# 调整约束力常数
export RESTRAINT_FC=2000  # 适中的约束

# 或分阶段释放约束
# 第一阶段: 强约束 (5000)
# 第二阶段: 中等约束 (2000)
# 第三阶段: 弱约束 (1000)
# 第四阶段: 无约束 (0)
```

---

## 预防措施

### 1. 充分的能量最小化
```bash
# 确保势能足够低
gmx energy -f em.edr -o potential.xvg
# 对于溶剂化蛋白质系统,应 < -500000 kJ/mol
```

### 2. 渐进式平衡
```bash
# 推荐流程:
# 1. NVT 100 ps (强约束)
# 2. NVT 100 ps (中等约束)
# 3. NPT 100 ps (Berendsen, 中等约束)
# 4. NPT 100 ps (Parrinello-Rahman, 弱约束)
```

### 3. 监控关键指标
```bash
# 实时监控温度
tail -f nvt.log | grep "Temperature"

# 实时监控压强
tail -f npt.log | grep "Pressure"
```

### 4. 保存检查点
```bash
# 定期保存检查点
nstxout-compressed = 500  # 每 1 ps 保存一次
```

---

## 参考资源

### GROMACS 官方文档
- [Temperature coupling](http://manual.gromacs.org/documentation/current/reference-manual/algorithms/temperature-coupling.html)
- [Pressure coupling](http://manual.gromacs.org/documentation/current/reference-manual/algorithms/pressure-coupling.html)

### 最佳实践
- NVT 平衡: 至少 100 ps
- NPT 平衡: 至少 100 ps
- 温度耦合: V-rescale (推荐)
- 压强耦合: Parrinello-Rahman (生产运行)
- 位置约束: 1000 kJ/mol/nm² (标准)

---

**更新时间:** 2026-04-07 04:25
**版本:** 1.0
