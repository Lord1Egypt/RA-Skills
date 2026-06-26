# Umbrella Sampling Errors - 故障排查手册

**适用脚本:** `scripts/advanced/umbrella.sh`

---

## ERROR-001: grompp 失败 (拉力模拟)

### 症状
```
ERROR-001: grompp 失败
Fatal error:
Group Ligand not found
```

### 可能原因
1. **拉力组不存在**
   - 拓扑中没有定义 Ligand
   - 组名拼写错误

2. **索引文件缺失**
   - 需要自定义索引组

### 解决方案

**方案 1: 创建索引组**
```bash
# 创建索引文件
gmx make_ndx -f complex.gro -o index.ndx

# 在交互界面中:
# > r LIG  (选择配体残基)
# > name 20 Ligand
# > q

# 使用索引文件
gmx grompp -f pull.mdp -c complex.gro -p topol.top -n index.ndx -o pull.tpr
```

**方案 2: 使用残基编号**
```bash
# 如果知道配体残基编号
gmx make_ndx -f complex.gro -o index.ndx
# > r 100  (假设配体是残基 100)
# > name 20 Ligand
# > q
```

**方案 3: 使用分子名称**
```bash
# 查看拓扑中的分子名称
grep "^\[ molecules \]" -A 10 topol.top

# 如果配体叫 "LIG",修改 pull.mdp:
pull_group2_name = LIG
```

---

## ERROR-002: 拉力模拟失败

### 症状
```
ERROR-002: 拉力模拟失败
Step 1234, time 2.468 (ps)
Fatal error:
Distance between pull groups 1 and 2 (5.234 nm) is larger than 0.49 times the box size (10.0 nm)
```

### 可能原因
1. **盒子太小**
   - 拉力距离超过盒子尺寸
   - PBC 导致问题

2. **拉力速率过快**
   - 系统来不及响应
   - 产生高能构象

### 解决方案

**方案 1: 增大盒子**
```bash
# 重新构建系统,使用更大的盒子
gmx editconf -f complex.gro -o box.gro -c -d 2.0 -bt cubic
gmx solvate -cp box.gro -cs spc216.gro -o solvated.gro -p topol.top
# 重新能量最小化和平衡
```

**方案 2: 减小拉力距离**
```bash
export PULL_DISTANCE=2.0  # 减小到 2 nm
./umbrella.sh
```

**方案 3: 降低拉力速率**
```bash
export PULL_RATE=0.005  # 减慢到 0.005 nm/ps
./umbrella.sh
```

**方案 4: 使用拉力方向限制**
```bash
# 在 pull.mdp 中修改
pull_coord1_dim = N N Y  # 只在 Z 方向拉力
```

---

## ERROR-003: 构象提取失败

### 症状
```
ERROR-003: 构象提取失败
Fatal error:
No frames found in trajectory
```

### 可能原因
1. **拉力模拟未完成**
   - 模拟崩溃
   - 轨迹文件损坏

2. **输出频率设置错误**
   - nstxout-compressed 过大
   - 没有生成压缩轨迹

### 解决方案

**方案 1: 检查拉力模拟输出**
```bash
# 检查轨迹文件
gmx check -f pull.xtc

# 如果没有 xtc,检查 trr
ls -lh pull.trr

# 使用 trr 代替
echo "System" | gmx trjconv -s pull.tpr -f pull.trr -o windows/conf.gro -sep
```

**方案 2: 调整输出频率**
```bash
# 在 pull.mdp 中修改
nstxout-compressed = 100  # 每 0.2 ps 输出一次
```

**方案 3: 手动提取构象**
```bash
# 从检查点文件重启并输出
gmx mdrun -v -deffnm pull -cpi pull.cpt -nsteps 0 -x pull.xtc
```

---

## ERROR-004: 未找到 TPR 文件

### 症状
```
ERROR-004: 未找到 TPR 文件
```

### 可能原因
1. **窗口模拟未成功**
   - grompp 失败
   - 窗口目录为空

2. **文件路径错误**

### 解决方案

**方案 1: 检查窗口状态**
```bash
# 查看哪些窗口成功
for i in windows/window_*/; do
    if [[ -f "$i/umbrella.tpr" ]]; then
        echo "OK: $i"
    else
        echo "FAIL: $i"
    fi
done
```

**方案 2: 重新生成失败的窗口**
```bash
# 手动处理失败的窗口
cd windows/window_05
gmx grompp -f umbrella.mdp -c conf.gro -p ../../../topol.top -n ../../../index.ndx -o umbrella.tpr -maxwarn 2
```

**方案 3: 只分析成功的窗口**
```bash
# 手动创建文件列表
ls windows/window_*/umbrella.tpr > tpr_files.dat
ls windows/window_*/pullf.xvg > pullf_files.dat
```

---

## ERROR-005: 未找到 pullf 文件

### 症状
```
ERROR-005: 未找到 pullf 文件
```

### 可能原因
1. **窗口模拟未运行**
   - mdrun 失败
   - 模拟未完成

2. **输出文件名错误**

### 解决方案

**方案 1: 检查模拟状态**
```bash
# 查看哪些窗口完成
for i in windows/window_*/; do
    if [[ -f "$i/pullf.xvg" ]]; then
        echo "OK: $i"
    else
        echo "FAIL: $i"
        # 尝试继续运行
        cd "$i"
        gmx mdrun -v -deffnm umbrella -cpi umbrella.cpt -pf pullf.xvg -px pullx.xvg
        cd ../..
    fi
done
```

**方案 2: 检查输出文件名**
```bash
# 有些版本可能输出为 pullf_umbrella.xvg
ls windows/window_*/pullf*.xvg
```

---

## ERROR-006: WHAM 分析失败

### 症状
```
ERROR-006: WHAM 分析失败
Fatal error:
Not enough data points for WHAM analysis
```

### 可能原因
1. **窗口覆盖不足**
   - 窗口间距太大
   - 窗口数量太少

2. **采样时间不足**
   - 每个窗口采样太短
   - 统计不充分

3. **窗口重叠不够**
   - 相邻窗口没有重叠区域

### 解决方案

**方案 1: 增加窗口数量**
```bash
# 减小窗口间距
export WINDOW_SPACING=0.05  # 从 0.1 减到 0.05
./umbrella.sh
```

**方案 2: 延长采样时间**
```bash
# 增加每窗口采样时间
export SAMPLE_TIME=10000  # 从 5 ns 增到 10 ns
./umbrella.sh
```

**方案 3: 检查窗口分布**
```bash
# 绘制采样直方图
xmgrace hist.xvg

# 应该看到:
# - 各窗口有明显的峰
# - 相邻窗口的峰有重叠
```

**方案 4: 调整 WHAM 参数**
```bash
# 使用更宽松的容差
gmx wham -it tpr_files.dat -if pullf_files.dat -o pmf.xvg -hist hist.xvg -tol 1e-5

# 或增加迭代次数
gmx wham -it tpr_files.dat -if pullf_files.dat -o pmf.xvg -hist hist.xvg -nBootstrap 200
```

---

## 常见问题

### Q1: PMF 曲线不光滑

**原因:** 采样不充分或窗口覆盖不均

**解决方案:**
```bash
# 1. 增加窗口密度
export WINDOW_SPACING=0.05

# 2. 延长采样时间
export SAMPLE_TIME=10000

# 3. 使用更强的伞状势
export WINDOW_FC=2000
```

### Q2: PMF 在边界处发散

**原因:** 边界窗口采样不足

**解决方案:**
```bash
# 1. 延长边界窗口的采样时间
cd windows/window_00
gmx mdrun -v -deffnm umbrella -cpi umbrella.cpt -nsteps 5000000  # 额外 10 ns

# 2. 或在 WHAM 中排除边界窗口
# 手动编辑 tpr_files.dat 和 pullf_files.dat,删除第一个和最后一个窗口
```

### Q3: 某些窗口模拟崩溃

**原因:** 初始构象不稳定

**解决方案:**
```bash
# 1. 对窗口构象进行能量最小化
cd windows/window_05
gmx grompp -f em.mdp -c conf.gro -p ../../../topol.top -o em.tpr
gmx mdrun -v -deffnm em

# 2. 使用最小化后的结构
gmx grompp -f umbrella.mdp -c em.gro -p ../../../topol.top -o umbrella.tpr
```

### Q4: 拉力模拟中配体飞出盒子

**原因:** 盒子太小或拉力方向不对

**解决方案:**
```bash
# 1. 使用更大的盒子
gmx editconf -f complex.gro -o box.gro -c -d 3.0 -bt cubic

# 2. 限制拉力方向
pull_coord1_dim = N N Y  # 只在 Z 方向

# 3. 使用 pull_coord1_geometry = direction
pull_coord1_geometry = direction
pull_coord1_vec = 0 0 1  # Z 方向
```

---

## 预防措施

### 1. 充分的系统准备
```bash
# 确保复合物已充分平衡
# 能量最小化 → NVT → NPT → 短时间 MD
```

### 2. 合理的拉力参数
```bash
# 拉力速率: 0.005-0.01 nm/ps (慢速)
# 拉力距离: 不超过盒子尺寸的 1/3
# 窗口间距: 0.05-0.1 nm
# 伞状势力常数: 1000-3000 kJ/mol/nm²
```

### 3. 充分的采样时间
```bash
# 每个窗口至少 5 ns
# 对于复杂系统,建议 10-20 ns
```

### 4. 监控模拟进度
```bash
# 实时检查窗口状态
watch -n 60 'ls windows/window_*/pullf.xvg | wc -l'

# 检查拉力值
tail -f windows/window_05/pullf.xvg
```

---

## 参考资源

### GROMACS 教程
- [Umbrella Sampling Tutorial](http://www.mdtutorials.com/gmx/umbrella/index.html)
- [WHAM Analysis](http://manual.gromacs.org/documentation/current/onlinehelp/gmx-wham.html)

### 最佳实践
- 窗口间距: 0.05-0.1 nm
- 采样时间: 5-10 ns/窗口
- 伞状势力常数: 1000-3000 kJ/mol/nm²
- 拉力速率: 0.005-0.01 nm/ps
- 窗口重叠: 相邻窗口应有 30-50% 重叠

### 文献参考
- Kumar et al. (1992) J. Comput. Chem. 13, 1011-1021 (WHAM 方法)
- Torrie & Valleau (1977) J. Comput. Phys. 23, 187-199 (伞状采样)

---

**更新时间:** 2026-04-07 04:27
**版本:** 1.0
