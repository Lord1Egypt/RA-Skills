# production-errors.md - 生产模拟故障排查

## 常见错误

### [ERROR-001] 未知参数
**症状:** `未知参数: XXX`
**原因:** 参数名错误
**解决:**
```bash
# 正确参数
--input npt.gro
--topology topol.top
--output md
--time 1000
--cores 2
--checkpoint md.cpt
```

### [ERROR-002] gmx 未安装
**症状:** `gmx 未安装`
**原因:** GROMACS 未加载
**解决:**
```bash
source /usr/local/gromacs/bin/GMXRC
```

### [ERROR-003] 缺少 --input
**症状:** `缺少 --input`
**原因:** 未指定输入结构
**解决:**
```bash
--input npt.gro  # 从 NPT 平衡态开始
```

### [ERROR-004] 缺少 --topology
**症状:** `缺少 --topology`
**原因:** 未指定拓扑文件
**解决:**
```bash
--topology topol.top
```

### [ERROR-005] 输入文件不存在
**症状:** `输入文件不存在: XXX`
**原因:** 文件路径错误或文件未生成
**解决:**
```bash
ls -lh npt.gro  # 检查文件
```

### [ERROR-007] grompp 失败
**症状:** `grompp 失败`
**原因:** MDP 参数错误或拓扑不匹配
**解决:**
```bash
# 检查详细错误
gmx grompp -f md.mdp -c npt.gro -p topol.top -o md.tpr
```

**常见原因:**
- 温度/压力耦合组不匹配
- 约束设置错误
- 时间步长过大

### [ERROR-008] mdrun 失败
**症状:** `mdrun 失败`
**原因:** 系统不稳定或参数不当
**解决:**

**1. 检查系统稳定性**
```bash
# 查看能量
echo "10 0" | gmx energy -f npt.edr -o potential.xvg
```

**2. 减少时间步长**
```bash
# 从 2 fs 降到 1 fs
dt = 0.001
```

**3. 增强约束**
```bash
# 约束所有键
constraints = all-bonds
```

### [ERROR-009] 轨迹文件未生成
**症状:** `轨迹文件未生成`
**原因:** mdrun 提前终止
**解决:**
```bash
# 检查日志
tail -100 md.log
```

### [ERROR-010] 能量文件未生成
**症状:** `能量文件未生成`
**原因:** mdrun 提前终止
**解决:**
```bash
# 检查日志
tail -100 md.log
```

---

## 性能优化

### 温度/压力异常

**症状:** 温度或压力偏离目标值
**原因:** 
- 平衡不充分
- 耦合参数不当
- 系统太小

**解决:**

**1. 延长平衡时间**
```bash
# NPT 平衡至少 1 ns
--time 1000  # 1 ns
```

**2. 调整耦合参数**
```bash
# 温度耦合
tau-t = 0.1 0.1  # 更快响应

# 压力耦合
tau-p = 2.0      # 标准值
```

**3. 检查系统大小**
```bash
# 盒子至少 1.2 nm cutoff
gmx editconf -f protein.gro -d 1.5 -bt dodecahedron
```

### 性能低下

**症状:** ns/day < 5
**原因:**
- 核心数不足
- 系统太大
- 未使用 GPU

**解决:**

**1. 增加核心数**
```bash
--cores 8  # 使用更多核心
```

**2. 使用 GPU**
```bash
gmx mdrun -v -deffnm md -nb gpu -pme gpu
```

**3. 优化 PME**
```bash
# 调整 Fourier spacing
fourierspacing = 0.15  # 从 0.12 增大
```

---

## 手册参考

- **Manual 3.3.3:** 生产模拟参数
- **Manual 3.4.4:** LINCS 约束算法
- **Manual 3.4.5:** V-rescale 恒温器
- **Manual 3.4.6:** Parrinello-Rahman 恒压器
- **Manual 3.4.7:** PME 静电
- **Manual 7.3.23:** mdrun 性能优化

---

## 检查点恢复

**从中断恢复:**
```bash
bash production.sh \
  --input npt.gro \
  --topology topol.top \
  --checkpoint md.cpt \
  --time 1000
```

**注意:**
- 检查点文件 (.cpt) 包含完整状态
- 可以无缝继续模拟
- 输出文件会追加，不会覆盖
