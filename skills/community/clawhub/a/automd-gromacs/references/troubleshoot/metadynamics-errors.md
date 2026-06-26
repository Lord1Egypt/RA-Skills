# Metadynamics 故障排查指南

## 常见错误场景

### ERROR-001: PLUMED 不可用
**症状**: 
```
[ERROR] PLUMED 未安装
[ERROR] GROMACS 未编译 PLUMED 支持
```

**原因**: GROMACS 编译时未启用 PLUMED 支持

**解决方案**:
```bash
# 方案 1: 重新编译 GROMACS (推荐)
cd gromacs-2026.1
mkdir build && cd build
cmake .. -DGMX_USE_PLUMED=ON -DCMAKE_INSTALL_PREFIX=/usr/local/gromacs
make -j$(nproc)
sudo make install

# 方案 2: 使用 AWH 方法 (无需 PLUMED)
METHOD=awh ./metadynamics.sh

# 方案 3: 手动安装 PLUMED
git clone https://github.com/plumed/plumed2.git
cd plumed2
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
```

**预防措施**:
- 安装 GROMACS 前检查 PLUMED 依赖
- 使用 `gmx mdrun -h | grep plumed` 验证支持

---

### ERROR-002: 集合变量定义错误
**症状**:
```
PLUMED: ERROR: atom index out of range
PLUMED: ERROR: wrong number of atoms for DISTANCE
```

**原因**: CV_ATOMS 参数错误或原子索引超出范围

**解决方案**:
```bash
# 检查原子数量
gmx dump -s md.tpr | grep "natoms"

# 对于距离 CV (需要 2 个原子)
CV_TYPE=distance CV_ATOMS="10,50" ./metadynamics.sh

# 对于角度 CV (需要 3 个原子)
CV_TYPE=angle CV_ATOMS="10,20,30" ./metadynamics.sh

# 对于二面角 CV (需要 4 个原子)
CV_TYPE=dihedral CV_ATOMS="10,20,30,40" ./metadynamics.sh

# 使用 VMD 或 PyMOL 可视化确认原子索引
```

**自动修复**: 脚本会自动使用默认原子组 (1,2)

---

### ERROR-003: 高斯峰参数不合理
**症状**:
```
[WARN] 高斯峰高度过小/过大
[WARN] 添加间隔过小
```

**原因**: HILL_HEIGHT, HILL_WIDTH, HILL_PACE 参数设置不当

**推荐参数**:
```bash
# 标准 metadynamics
HILL_HEIGHT=1.2      # 1-5 kJ/mol (小系统用小值)
HILL_WIDTH=0.05      # CV 范围的 1-5%
HILL_PACE=500        # 100-1000 步

# Well-tempered metadynamics
METAD_TYPE=well-tempered
BIASFACTOR=10        # 5-20 (越大越保守)
HILL_HEIGHT=1.2      # 可以稍大 (会自动衰减)

# 快速探索 (不精确)
HILL_HEIGHT=5.0
HILL_PACE=200

# 精细采样 (慢但准确)
HILL_HEIGHT=0.5
HILL_PACE=1000
```

**自动修复**: 脚本会自动调整到合理范围

---

### ERROR-004: CV 范围设置错误
**症状**:
```
PLUMED: WARNING: CV value outside GRID range
[WARN] CV 范围无效 (min >= max)
```

**原因**: CV_MIN 和 CV_MAX 设置不合理

**解决方案**:
```bash
# 先运行短时间无偏置模拟,观察 CV 范围
gmx mdrun -deffnm test -nsteps 50000

# 对于距离 CV
CV_MIN=0.0    # 最小距离 (nm)
CV_MAX=3.0    # 最大距离 (nm)

# 对于角度 CV
CV_MIN=0      # 0 度
CV_MAX=180    # 180 度

# 对于二面角 CV
CV_MIN=-180   # -180 度
CV_MAX=180    # 180 度

# 留出 10-20% 余量
# 如果观察到 CV 在 0.5-2.5 nm,设置 0.3-2.8 nm
```

**自动修复**: 脚本会自动交换 min 和 max

---

### ERROR-005: AWH 配置错误
**症状**:
```
grompp: ERROR: pull-coord1-potential-provider must be awh
grompp: ERROR: awh1-dim1-coord-index out of range
```

**原因**: AWH 和 pull code 配置不匹配

**解决方案**:
```bash
# 确保 pull code 和 AWH 一致
# 在 MDP 文件中:
pull                    = yes
pull-coord1-type        = external-potential
pull-coord1-potential-provider = awh

awh                     = yes
awh1-dim1-coord-provider = pull
awh1-dim1-coord-index   = 1  # 对应 pull-coord1

# 检查索引文件
gmx make_ndx -f system.gro -o index.ndx
# 确保 CV_group1 和 CV_group2 存在
```

**自动修复**: 脚本会自动生成匹配的配置

---

### ERROR-006: 模拟不收敛
**症状**:
```
自由能面持续变化
不同时间段的 FES 差异很大
```

**原因**: 模拟时间不足或参数设置不当

**诊断方法**:
```bash
# PLUMED: 比较不同时间段的 FES
plumed sum_hills --hills HILLS --outfile fes_0-50ns.dat --stride 1 --kt 2.5
plumed sum_hills --hills HILLS --outfile fes_50-100ns.dat --stride 1 --kt 2.5 --min-time 50000

# 计算差异
paste fes_0-50ns.dat fes_50-100ns.dat | awk '{print $1, ($2-$4)^2}' | \
    awk '{sum+=$2} END {print "RMSD:", sqrt(sum/NR)}'

# 如果 RMSD > 2 kJ/mol,需要更长时间
```

**解决方案**:
```bash
# 增加模拟时间
SIM_TIME=500000  # 500 ns

# 使用 well-tempered (更快收敛)
METAD_TYPE=well-tempered
BIASFACTOR=10

# 减小高斯峰高度 (更精细)
HILL_HEIGHT=0.5

# 增加添加间隔 (更保守)
HILL_PACE=1000
```

---

### ERROR-007: 内存不足
**症状**:
```
PLUMED: ERROR: cannot allocate memory
Killed (OOM)
```

**原因**: GRID_BIN 过大或系统过大

**解决方案**:
```bash
# 减小网格分辨率 (在 plumed.dat 中)
GRID_BIN=100  # 从 200 减到 100

# 对于多维 CV,使用稀疏网格
GRID_SPARSE=yes

# 增加系统内存或使用更少线程
NTOMP=2

# 使用 AWH (内存效率更高)
METHOD=awh
```

---

### ERROR-008: RMSD CV 参考结构缺失
**症状**:
```
PLUMED: ERROR: cannot open reference.pdb
```

**原因**: 使用 RMSD CV 但未提供参考结构

**解决方案**:
```bash
# 从初始结构提取参考
gmx trjconv -s md.tpr -f system.gro -o reference.pdb -dump 0

# 或使用特定构象
gmx trjconv -s md.tpr -f trajectory.xtc -o reference.pdb -dump 1000

# 确保 reference.pdb 在工作目录
cp reference.pdb metadynamics/
```

---

### ERROR-009: 温度耦合问题
**症状**:
```
温度波动过大
能量不守恒
```

**原因**: 温度控制器设置不当

**解决方案**:
```bash
# 使用 V-rescale (推荐)
tcoupl = V-rescale
tau_t = 0.1  # 快速响应

# 避免使用 Berendsen (不产生正确系综)
# tcoupl = Berendsen  # 不推荐

# 检查温度
echo "Temperature" | gmx energy -f md.edr -o temp.xvg
```

---

### ERROR-010: 检查点重启失败
**症状**:
```
[ERROR] 重启失败
Cannot read checkpoint file
```

**原因**: 检查点文件损坏或不兼容

**解决方案**:
```bash
# 从最后一个完整帧重启
gmx convert-tpr -s md.tpr -until <last_time> -o md_new.tpr
gmx mdrun -deffnm md_new -cpi md.cpt

# 如果检查点完全损坏,从轨迹重启
gmx trjconv -s md.tpr -f md.xtc -o last_frame.gro -dump <last_time>
# 修改 MDP: gen_vel = yes
gmx grompp -f md.mdp -c last_frame.gro -p topol.top -o restart.tpr
gmx mdrun -deffnm restart -plumed plumed.dat

# 合并 HILLS 文件
cat HILLS HILLS_restart > HILLS_combined
```

---

## 性能优化

### 优化 1: 并行化
```bash
# 使用多线程
NTOMP=8 ./metadynamics.sh

# 使用 GPU
GPU_ID=0 ./metadynamics.sh

# MPI + OpenMP (需要 MPI 版本 GROMACS)
mpirun -np 4 gmx_mpi mdrun -ntomp 2 -plumed plumed.dat
```

### 优化 2: 减少输出频率
```bash
# 在 plumed.dat 中
PRINT ARG=d1 FILE=COLVAR STRIDE=1000  # 从 100 增加到 1000
FES STRIDE=10000  # 从 5000 增加到 10000
```

### 优化 3: 使用多副本
```bash
# 多个独立副本 (可并行)
for i in {1..4}; do
    mkdir replica_$i
    cd replica_$i
    ../metadynamics.sh &
    cd ..
done
wait

# 合并 HILLS
cat replica_*/HILLS > HILLS_all
plumed sum_hills --hills HILLS_all --outfile fes_combined.dat
```

---

## 质量检查清单

### 模拟前
- [ ] PLUMED/AWH 可用性检查
- [ ] CV 原子索引验证
- [ ] CV 范围合理性 (运行短测试)
- [ ] 参数文件语法检查 (`plumed driver --plumed plumed.dat`)
- [ ] 系统已充分平衡

### 模拟中
- [ ] 监控 CV 值 (`tail -f COLVAR`)
- [ ] 检查能量稳定性 (`gmx energy -f md.edr`)
- [ ] 观察高斯峰添加 (`tail -f HILLS`)
- [ ] 监控系统资源 (`htop`)

### 模拟后
- [ ] 模拟完整完成 (`grep "Finished mdrun" md.log`)
- [ ] FES 收敛性检查 (比较不同时间段)
- [ ] 能量守恒检查
- [ ] 结果物理合理性 (势垒高度、最小值位置)

---

## 参考资料

### 关键论文
1. Laio & Parrinello (2002). Escaping free-energy minima. PNAS 99, 12562-12566.
2. Barducci et al. (2008). Well-tempered metadynamics. PRL 100, 020603.
3. Lindahl et al. (2015). AWH method. JCTC 11, 3447-3454.

### 在线资源
- PLUMED 官方文档: https://www.plumed.org/doc
- GROMACS AWH 教程: https://manual.gromacs.org/current/reference-manual/special/awh.html
- Metadynamics 教程: https://www.plumed-tutorials.org/

### 推荐工具
- PLUMED-GUI: 可视化 FES
- VMD: 可视化轨迹和 CV
- PyEMMA: 分析 MSM 和自由能

---

## 快速诊断命令

```bash
# 检查 PLUMED 支持
gmx mdrun -h | grep plumed

# 验证 PLUMED 配置
plumed driver --plumed plumed.dat --ixyz dummy.xyz

# 检查模拟状态
tail -100 md.log

# 实时监控 CV
tail -f COLVAR

# 快速计算 FES
plumed sum_hills --hills HILLS --outfile fes.dat --mintozero

# 检查能量
echo "Potential Temperature" | gmx energy -f md.edr

# 检查轨迹完整性
gmx check -f md.xtc

# 提取最后一帧
gmx trjconv -s md.tpr -f md.xtc -o last.gro -dump -1
```
