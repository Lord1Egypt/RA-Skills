# Enhanced Sampling 故障排查

## 常见错误速查

| 错误代码 | 症状 | 原因 | 修复方案 |
|---------|------|------|---------|
| ERROR-001 | grompp失败: annealing参数错误 | 时间点/温度点数量不匹配 | 检查annealing-npoints与数组长度 |
| ERROR-002 | 退火温度过高导致系统崩溃 | TEMP_MAX > 1000 K | 限制到800 K或减小时间步长 |
| ERROR-003 | 扩展系综lambda不跳跃 | nstexpanded过大或权重未收敛 | 减小到100-500步,增加模拟时间 |
| ERROR-004 | Wang-Landau不收敛 | wl-ratio设置不当 | 降低到0.5-0.8,增加模拟时间 |
| ERROR-005 | Lambda访问不均匀 | lambda分布不合理 | 使用端点密集分布 |
| ERROR-006 | 扩展系综检查点错误 | 已知GROMACS bug | 避免-update gpu或用modular simulator |
| ERROR-007 | 退火后结构不稳定 | 降温过快 | 增加降温阶段时间或控制点 |
| ERROR-008 | 内存不足 | 输出频率过高 | 增大nstxout-compressed |

---

## ERROR-001: grompp失败 - annealing参数错误

### 症状
```
ERROR 1 [file enhanced.mdp]:
  annealing-npoints is 5 but annealing-time has 4 entries
```

### 原因
- `annealing-npoints` 与 `annealing-time`/`annealing-temp` 数组长度不匹配
- 脚本生成退火时间表时计算错误

### 修复
```bash
# 检查MDP文件
grep "annealing" enhanced.mdp

# 手动修正
annealing-npoints       = 5
annealing-time          = 0 250 500 750 1000
annealing-temp          = 300 400 500 400 300
```

### 预防
- 脚本已内置验证: `validate_annealing_params()`
- 自动生成时间表: `generate_annealing_schedule()`

---

## ERROR-002: 退火温度过高导致系统崩溃

### 症状
```
Step 12500: Water molecule starting at atom 1234 can not be settled.
LINCS WARNING: bonds that rotated more than 30 degrees
```

### 原因
- `TEMP_MAX` 设置过高 (> 1000 K)
- 高温下分子运动剧烈,约束算法失效
- 时间步长过大

### 修复
```bash
# 方案1: 降低最高温度
TEMP_MAX=600 bash enhanced-sampling.sh

# 方案2: 减小时间步长
DT=0.001 TEMP_MAX=800 bash enhanced-sampling.sh

# 方案3: 使用更强约束
# 在MDP中添加:
lincs_iter              = 2
lincs_order             = 6
```

### 预防
- 脚本自动限制: `TEMP_MAX > 1000 → 800 K`
- 推荐范围: 300-600 K (蛋白质), 300-800 K (小分子)

---

## ERROR-003: 扩展系综lambda不跳跃

### 症状
```
# lambda.xvg 显示lambda始终为0
0.0    0
2.0    0
4.0    0
...
```

### 原因
1. `nstexpanded` 过大 (> 1000步)
2. Wang-Landau权重未收敛
3. lambda能量差过大,接受率为0

### 修复
```bash
# 方案1: 减小尝试间隔
NSTEXPANDED=100 bash enhanced-sampling.sh

# 方案2: 增加模拟时间
SIM_TIME=50000 bash enhanced-sampling.sh

# 方案3: 调整WL参数
WL_SCALE=0.5 WL_RATIO=0.5 bash enhanced-sampling.sh

# 方案4: 减少lambda状态数
NUM_LAMBDA=7 bash enhanced-sampling.sh
```

### 诊断
```bash
# 检查lambda尝试频率
grep "Repl ex" enhanced.log | head -20

# 检查接受率
grep "Acceptance" enhanced.log
```

### 预防
- 脚本自动调整: `NSTEXPANDED < 10 → 50`
- 推荐: 100-500步

---

## ERROR-004: Wang-Landau不收敛

### 症状
```
# 模拟结束但权重仍在剧烈波动
# lambda访问极不均匀
```

### 原因
- `wl-ratio` 设置过高 (> 0.9)
- `wl-scale` 过大
- 模拟时间不足

### 修复
```bash
# 方案1: 降低收敛判据
WL_RATIO=0.6 bash enhanced-sampling.sh

# 方案2: 减小缩放因子
WL_SCALE=0.5 bash enhanced-sampling.sh

# 方案3: 大幅增加模拟时间
SIM_TIME=100000 bash enhanced-sampling.sh

# 方案4: 使用预设权重
# 从先前模拟提取权重,在MDP中设置:
lmc-weights-equil       = no
init-lambda-weights     = 0.0 0.5 1.2 2.0 ...
```

### 诊断
```bash
# 检查WL历史
grep "Wang-Landau" enhanced.log

# 分析lambda访问
awk '!/^[@#]/ {count[int($2)]++} END {
    for (i in count) print i, count[i]
}' lambda.xvg | sort -n
```

### 预防
- 推荐: `wl-ratio=0.5-0.8`, `wl-scale=0.5-0.8`
- 至少运行 10-50 ns

---

## ERROR-005: Lambda访问不均匀

### 症状
```
Lambda状态访问统计:
State 0: 45000 次
State 1: 8000 次
State 2: 500 次
State 3: 50 次
State 4-10: 0 次
```

### 原因
- Lambda分布不合理 (能量差过大)
- 软核参数不当
- 端点未密集采样

### 修复
```bash
# 方案1: 使用端点密集分布
# 脚本已自动实现: 0.0, 0.05, 0.1, ..., 0.9, 0.95, 1.0

# 方案2: 调整软核参数
# 在MDP中修改:
sc-alpha                = 0.7  # 增大到0.5-0.7
sc-sigma                = 0.25 # 减小到0.25-0.3

# 方案3: 增加lambda状态数
NUM_LAMBDA=15 bash enhanced-sampling.sh

# 方案4: 分阶段解耦
LAMBDA_TYPE=vdw bash enhanced-sampling.sh  # 先解耦vdW
# 然后用结果作为输入
LAMBDA_TYPE=coul bash enhanced-sampling.sh # 再解耦静电
```

### 诊断
```bash
# 计算相邻lambda能量差
echo "Lambda" | gmx energy -f enhanced.edr -o dhdl.xvg
# 理想: ΔH < 5-10 kJ/mol

# 可视化访问分布
awk '!/^[@#]/ {count[int($2)]++} END {
    for (i=0; i<11; i++) print i, count[i]+0
}' lambda.xvg | xmgrace -
```

---

## ERROR-006: 扩展系综检查点错误

### 症状
```
WARNING: Expanded ensemble state was not correctly checkpointed
Simulation may not be reproducible
```

### 原因
- GROMACS已知bug (Issue 4629)
- Legacy simulator在检查点步骤未记录MC移动

### 修复
```bash
# 方案1: 避免使用GPU更新 (强制modular simulator)
gmx mdrun -v -deffnm enhanced -ntomp 4 -nb cpu

# 方案2: 不从检查点重启
# 如果必须重启,从头开始

# 方案3: 使用旧版GROMACS (< 2024)
```

### 预防
- 检查GROMACS版本: `gmx --version`
- 如果 >= 2024, 避免 `-update gpu`

---

## ERROR-007: 退火后结构不稳定

### 症状
```
# 降温后RMSD持续增大
# 蛋白质展开或聚集
```

### 原因
- 降温速率过快 (< 100 ps)
- 高温时采样到非物理构象
- 缺少位置限制

### 修复
```bash
# 方案1: 增加降温时间
ANNEALING_TIME=5000 bash enhanced-sampling.sh

# 方案2: 增加控制点数 (更平滑)
ANNEALING_POINTS=10 bash enhanced-sampling.sh

# 方案3: 降低最高温度
TEMP_MAX=400 bash enhanced-sampling.sh

# 方案4: 添加骨架限制
# 在MDP中:
define                  = -DPOSRES
```

### 诊断
```bash
# 分析温度-RMSD关系
paste <(awk '!/^[@#]/ {print $1, $2}' energy.xvg) \
      <(awk '!/^[@#]/ {print $2}' rmsd.xvg) | xmgrace -

# 检查二级结构变化
echo "Protein" | gmx do_dssp -s enhanced.tpr -f enhanced.xtc -o dssp.xpm
```

---

## ERROR-008: 内存不足

### 症状
```
malloc(): Cannot allocate memory
Killed
```

### 原因
- 输出频率过高 (`nstxout-compressed=100`)
- 长时间模拟 (> 100 ns)
- 大系统 (> 100k 原子)

### 修复
```bash
# 方案1: 减少输出频率
# 在MDP中:
nstxout-compressed      = 10000  # 每20 ps输出一次

# 方案2: 只输出关键原子
compressed-x-grps       = Protein  # 只输出蛋白质

# 方案3: 分段运行
SIM_TIME=10000 bash enhanced-sampling.sh
# 然后从检查点继续
INPUT_CPT=enhanced.cpt SIM_TIME=20000 bash enhanced-sampling.sh
```

---

## 性能优化

### 1. GPU加速
```bash
# 使用GPU
GPU_ID=0 bash enhanced-sampling.sh

# 多GPU (扩展系综不支持)
```

### 2. 并行优化
```bash
# 调整OpenMP线程数
NTOMP=8 bash enhanced-sampling.sh

# 检查性能
gmx mdrun -v -deffnm enhanced -ntomp 4 -pin on -tunepme yes
```

### 3. 减少输出
```bash
# 最小输出配置
nstlog                  = 10000
nstxout-compressed      = 10000
nstdhdl                 = 500  # 扩展系综
```

---

## 调试技巧

### 1. 测试运行
```bash
# 短时间测试
SIM_TIME=100 bash enhanced-sampling.sh

# 检查退火时间表
grep "annealing" enhanced.mdp

# 检查lambda分布
grep "lambdas" enhanced.mdp
```

### 2. 日志分析
```bash
# 检查警告
grep -i "warning\|error" enhanced.log

# 检查性能
grep "Performance" enhanced.log

# 检查lambda跳跃 (扩展系综)
grep "Repl ex" enhanced.log | tail -20
```

### 3. 能量监控
```bash
# 实时监控
tail -f enhanced.log | grep "Step"

# 提取关键能量
echo "Potential Kinetic Temperature" | gmx energy -f enhanced.edr -o monitor.xvg
xmgrace monitor.xvg
```

---

## 最佳实践

### Simulated Annealing
1. **温度范围**: 300-600 K (蛋白质), 300-800 K (小分子)
2. **升温速率**: 50-100 K/ns
3. **保持时间**: 总时间的30-40%
4. **降温速率**: 20-50 K/ns (比升温慢)
5. **控制点**: 5-10个 (平滑曲线)

### Expanded Ensemble
1. **Lambda数量**: 7-21个
2. **端点密集**: 0.0, 0.05, 0.1, ..., 0.9, 0.95, 1.0
3. **尝试间隔**: 100-500步
4. **WL参数**: scale=0.5-0.8, ratio=0.5-0.8
5. **模拟时间**: 至少10-50 ns
6. **软核参数**: alpha=0.5-0.7, sigma=0.25-0.3

### 组合使用
```bash
# 先退火探索构象空间
SAMPLING_METHOD=annealing SIM_TIME=5000 bash enhanced-sampling.sh

# 再用扩展系综计算自由能
INPUT_GRO=enhanced/enhanced.gro \
INPUT_CPT=enhanced/enhanced.cpt \
SAMPLING_METHOD=expanded \
SIM_TIME=50000 \
bash enhanced-sampling.sh
```

---

## 参考资源

### 文档
- GROMACS Manual 5.4.6: Simulated Annealing
- GROMACS Manual 5.4.14: Expanded Ensemble
- Issue 4629: Expanded ensemble checkpoint bug

### 工具
- `gmx energy`: 能量分析
- `gmx bar`: 自由能计算
- `xmgrace`: 数据可视化

### 论文
- Kirkpatrick et al. (1983). Optimization by simulated annealing. Science 220, 671-680.
- Lyubartsev et al. (1992). New approach to Monte Carlo calculation. J. Chem. Phys. 96, 1776.
- Wang & Landau (2001). Efficient random walk algorithm. Phys. Rev. Lett. 86, 2050.
