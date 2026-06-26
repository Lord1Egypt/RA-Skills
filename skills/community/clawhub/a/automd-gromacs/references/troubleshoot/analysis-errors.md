# Analysis Errors - 故障排查手册

**适用脚本:** `scripts/basic/analysis.sh`

---

## ERROR-001: PBC 移除失败

### 症状
```
ERROR-001: PBC 移除失败
Fatal error:
Group Protein not found
```

### 可能原因
1. **索引文件问题**
   - 默认索引组不存在
   - TPR 文件中没有 Protein 组

2. **系统类型不匹配**
   - 非蛋白质系统
   - 自定义分子类型

### 解决方案

**方案 1: 查看可用组**
```bash
# 列出所有索引组
gmx make_ndx -f md.tpr

# 常见组:
# System, Protein, Protein-H, C-alpha, Backbone, etc.
```

**方案 2: 创建自定义索引**
```bash
# 创建索引文件
gmx make_ndx -f md.tpr -o index.ndx

# 在交互界面中:
# > 1 | 13  (选择 Protein 或 SOL)
# > name 20 Protein_SOL
# > q

# 使用自定义索引
gmx trjconv -s md.tpr -f md.xtc -o traj_nopbc.xtc -n index.ndx -pbc mol -center
```

**方案 3: 使用数字索引**
```bash
# 直接使用组编号
echo "1 0" | gmx trjconv -s md.tpr -f md.xtc -o traj_nopbc.xtc -pbc mol -center
# 1 = Protein (居中组)
# 0 = System (输出组)
```

---

## ERROR-002: 轨迹叠合失败

### 症状
```
ERROR-002: 轨迹叠合失败
Fatal error:
Group Backbone not found
```

### 可能原因
1. **叠合组不存在**
   - 默认 Backbone 组缺失
   - 索引文件问题

2. **轨迹文件损坏**
   - 不完整的轨迹
   - 格式错误

### 解决方案

**方案 1: 使用其他叠合组**
```bash
# 常见叠合组:
export FIT_GROUP="C-alpha"    # 只用 Cα 原子
export FIT_GROUP="Protein"    # 所有蛋白质原子
export FIT_GROUP="MainChain"  # 主链原子
```

**方案 2: 创建自定义叠合组**
```bash
# 创建索引
gmx make_ndx -f md.tpr -o index.ndx

# 选择特定残基的主链
# > r 1-50 & 4  (残基 1-50 的 Backbone)
# > name 20 Core_Backbone
# > q

# 使用自定义组
echo "Core_Backbone Core_Backbone" | gmx trjconv -s md.tpr -f traj_nopbc.xtc -o traj_fit.xtc -n index.ndx -fit rot+trans
```

**方案 3: 检查轨迹完整性**
```bash
# 检查轨迹帧数
gmx check -f md.xtc

# 如果损坏,尝试修复
gmx trjconv -f md.xtc -o md_fixed.xtc -b 0 -e 10000
```

---

## ERROR-003: RMSD 计算失败

### 症状
```
ERROR-003: RMSD 计算失败
Fatal error:
Number of atoms in tpr and trajectory don't match
```

### 可能原因
1. **TPR 和轨迹不匹配**
   - 使用了错误的 TPR 文件
   - 轨迹是从不同系统生成的

2. **轨迹预处理问题**
   - trjconv 输出了错误的原子数

### 解决方案

**方案 1: 确认文件匹配**
```bash
# 检查 TPR 原子数
gmx check -s md.tpr | grep atoms

# 检查轨迹原子数
gmx check -f md.xtc | grep atoms

# 应该一致
```

**方案 2: 重新生成轨迹**
```bash
# 确保使用正确的 TPR
gmx trjconv -s md.tpr -f md.xtc -o traj_nopbc.xtc -pbc mol -center
```

**方案 3: 只输出特定组**
```bash
# 在 trjconv 时只输出 Protein
echo "Protein Protein" | gmx trjconv -s md.tpr -f md.xtc -o traj_protein.xtc -pbc mol -center

# 然后用 protein-only TPR
gmx convert-tpr -s md.tpr -o md_protein.tpr -n index.ndx
echo "Backbone" | gmx rms -s md_protein.tpr -f traj_protein.xtc -o rmsd.xvg
```

---

## ERROR-004: RMSF 计算失败

### 症状
```
ERROR-004: RMSF 计算失败
Fatal error:
Group C-alpha not found
```

### 可能原因
1. **C-alpha 组不存在**
   - 非标准残基
   - 核酸或其他分子

### 解决方案

**方案 1: 使用其他组**
```bash
export RMSF_GROUP="Backbone"   # 主链原子
export RMSF_GROUP="Protein"    # 所有蛋白质原子
```

**方案 2: 创建 C-alpha 索引**
```bash
gmx make_ndx -f md.tpr -o index.ndx

# 在交互界面:
# > a CA  (选择所有 CA 原子)
# > name 20 C-alpha
# > q

echo "C-alpha" | gmx rmsf -s md.tpr -f traj_fit.xtc -o rmsf.xvg -n index.ndx -res
```

---

## ERROR-005: Rg 计算失败

### 症状
```
ERROR-005: Rg 计算失败
Fatal error:
Selected group is empty
```

### 可能原因
1. **选择的组为空**
   - 组名错误
   - 系统中不存在该类型原子

### 解决方案

**方案 1: 检查组内容**
```bash
gmx make_ndx -f md.tpr

# 查看组的原子数
# 确保选择的组不为空
```

**方案 2: 使用正确的组**
```bash
# 对于蛋白质系统
export RG_GROUP="Protein"

# 对于复合物系统
export RG_GROUP="Protein"  # 只计算蛋白质的 Rg
```

---

## ERROR-006: 氢键计算失败

### 症状
```
ERROR-006: 氢键计算失败
Fatal error:
No hydrogen bond donors found
```

### 可能原因
1. **氢原子缺失**
   - 使用了 united-atom 力场
   - 轨迹中没有氢原子

2. **组选择错误**
   - 选择的组不包含氢键供体/受体

### 解决方案

**方案 1: 检查氢原子**
```bash
# 查看系统中的氢原子
gmx make_ndx -f md.tpr
# > a H*  (选择所有氢原子)

# 如果没有氢原子,跳过氢键分析
export ANALYZE_HBOND=no
```

**方案 2: 添加氢原子**
```bash
# 从轨迹重建氢原子 (仅适用于某些情况)
gmx trjconv -s md.tpr -f md.xtc -o traj_h.xtc

# 注意: 这通常不可行,因为氢原子位置无法准确重建
```

**方案 3: 使用重原子距离**
```bash
# 使用 mindist 代替 hbond
gmx mindist -s md.tpr -f traj_fit.xtc -od mindist.xvg -pi
```

---

## ERROR-007: SASA 计算失败

### 症状
```
ERROR-007: SASA 计算失败
Fatal error:
Not enough memory
```

### 可能原因
1. **内存不足**
   - 系统太大
   - 轨迹帧数太多

2. **探针半径设置不当**

### 解决方案

**方案 1: 减少轨迹帧数**
```bash
# 只分析部分轨迹
gmx trjconv -f traj_fit.xtc -o traj_short.xtc -b 0 -e 10000 -dt 10

# 使用短轨迹
echo "Protein" | gmx sasa -s md.tpr -f traj_short.xtc -o sasa.xvg
```

**方案 2: 调整探针半径**
```bash
# 使用更大的探针半径 (减少计算量)
echo "Protein" | gmx sasa -s md.tpr -f traj_fit.xtc -o sasa.xvg -probe 0.2
```

**方案 3: 分段计算**
```bash
# 分段计算后合并
for i in {0..10}; do
    b=$((i*1000))
    e=$(((i+1)*1000))
    echo "Protein" | gmx sasa -s md.tpr -f traj_fit.xtc -o sasa_$i.xvg -b $b -e $e
done

# 合并结果
cat sasa_*.xvg | grep -v '^[@#]' > sasa_all.xvg
```

---

## 常见问题

### Q1: 分析结果不合理 (RMSD 过大)

**原因:** 轨迹未正确叠合

**解决方案:**
```bash
# 确保叠合到参考结构
echo "Backbone Backbone" | gmx trjconv -s md.tpr -f md.xtc -o traj_fit.xtc -fit rot+trans

# 检查叠合效果
vmd md.tpr traj_fit.xtc
```

### Q2: RMSF 曲线有尖峰

**原因:** 末端残基或 loop 区域柔性大

**解决方案:**
```bash
# 这是正常现象
# 可以只分析核心区域
gmx make_ndx -f md.tpr
# > r 10-50  (选择核心残基)
# > name 20 Core
# > q

echo "Core" | gmx rmsf -s md.tpr -f traj_fit.xtc -o rmsf_core.xvg -n index.ndx -res
```

### Q3: 氢键数波动很大

**原因:** 氢键本身就是动态的

**解决方案:**
```bash
# 计算移动平均
awk 'BEGIN{n=10} !/^[@#]/ {
    arr[NR%n]=$2; sum+=$2
    if(NR>=n) {sum-=arr[(NR+1)%n]; print $1, sum/n}
}' hbond.xvg > hbond_smooth.xvg
```

### Q4: 分析速度很慢

**原因:** 轨迹太大或帧率太高

**解决方案:**
```bash
# 降低帧率
gmx trjconv -f md.xtc -o md_skip.xtc -skip 10

# 只分析部分时间
export BEGIN_TIME=5000  # 从 5 ns 开始
export END_TIME=10000   # 到 10 ns
```

---

## 预防措施

### 1. 检查输入文件
```bash
# 确认 TPR 和轨迹匹配
gmx check -s md.tpr
gmx check -f md.xtc
```

### 2. 使用标准组名
```bash
# 优先使用 GROMACS 默认组:
# System, Protein, Protein-H, C-alpha, Backbone, MainChain, SideChain
```

### 3. 分步骤执行
```bash
# 不要一次性运行所有分析
# 先测试单个分析,确认无误后再批量运行
export ANALYZE_RMSD=yes
export ANALYZE_RMSF=no
export ANALYZE_RG=no
./analysis.sh
```

### 4. 保存中间文件
```bash
# 保存预处理后的轨迹
# 避免重复预处理
cp traj_fit.xtc ../traj_fit_backup.xtc
```

---

## 参考资源

### GROMACS 分析工具
- `gmx rms` - RMSD 计算
- `gmx rmsf` - RMSF 计算
- `gmx gyrate` - 回旋半径
- `gmx hbond` - 氢键分析
- `gmx sasa` - 溶剂可及表面积
- `gmx do_dssp` - 二级结构分析

### 最佳实践
- 轨迹预处理: 移除 PBC → 居中 → 叠合
- RMSD 参考: 使用 Backbone 或 C-alpha
- RMSF 计算: 使用 C-alpha 或 Backbone
- 氢键定义: 距离 < 0.35 nm, 角度 < 30°

---

**更新时间:** 2026-04-07 04:26
**版本:** 1.0
