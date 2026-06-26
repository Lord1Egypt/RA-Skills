# Replica Exchange Errors - 故障排查手册

**适用脚本:** `scripts/advanced/replica-exchange.sh`

---

## ERROR-001: TPR生成失败

### 症状
```
ERROR-001: 副本 X TPR生成失败
Fatal error:
Too many warnings (1)
```

### 可能原因
1. **温度设置冲突**
   - MDP文件中温度组数量与拓扑不匹配
   
2. **自由能参数错误**
   - Lambda状态数量与副本数量不匹配
   - 软核参数设置不当

3. **拓扑文件问题**
   - 缺少自由能相关的拓扑定义

### 解决方案

**方案 1: 检查温度组**
```bash
# 查看拓扑中的分子组
grep "^\[ molecules \]" -A 10 topol.top

# 修改MDP中的温度组
# 如果只有一个分子类型:
tc-grps = System
tau_t = 0.1
ref_t = 300

# 如果有多个分子类型(如Protein + Water):
tc-grps = Protein Non-Protein
tau_t = 0.1 0.1
ref_t = 300 300
```

**方案 2: 修复Lambda参数**
```bash
# 确保lambda数量等于副本数量
# 在脚本中设置:
export NUM_REPLICAS=8
export LAMBDA_STATES="0.0,0.1,0.3,0.5,0.7,0.9,0.95,1.0"

# 或使用自动生成(均匀分布)
unset LAMBDA_STATES
```

**方案 3: 增加maxwarn**
```bash
# 如果警告不严重,可以忽略
gmx grompp -f md.mdp -c system.gro -p topol.top -o md.tpr -maxwarn 2
```

---

## ERROR-002: 副本交换失败

### 症状
```
ERROR-002: 副本交换失败
Fatal error:
Replica exchange requires all replicas to have the same number of atoms
```

### 可能原因
1. **副本结构不一致**
   - 不同副本使用了不同的输入结构
   - 拓扑文件不同

2. **自由能设置错误**
   - 某些副本启用了自由能,某些没有

### 解决方案

**方案 1: 确保所有副本使用相同输入**
```bash
# 检查所有副本的原子数
for i in {0..7}; do
    gmx check -s replica_$i/md.tpr 2>&1 | grep "natoms"
done

# 确保所有副本使用相同的GRO和TOP
# 在脚本中验证:
check_file "$INPUT_GRO"
check_file "$INPUT_TOP"
```

**方案 2: 统一自由能设置**
```bash
# 温度REMD: 所有副本都不使用自由能
# 哈密顿REMD: 所有副本都使用自由能

# 检查MDP文件
for i in {0..7}; do
    echo "Replica $i:"
    grep "free_energy" replica_$i/md.mdp
done
```

---

## ERROR-003: MPI启动失败

### 症状
```
ERROR-003: MPI启动失败
Fatal error:
Not enough processors available
```

### 可能原因
1. **副本数量超过可用核心**
   - 每个副本需要至少1个MPI进程

2. **资源限制**
   - 系统资源不足

### 解决方案

**方案 1: 减少副本数量**
```bash
export NUM_REPLICAS=4  # 减少到可用核心数
./replica-exchange.sh
```

**方案 2: 调整线程数**
```bash
# 减少每副本的OpenMP线程数
export NTOMP=1
export NUM_REPLICAS=8
./replica-exchange.sh
```

**方案 3: 使用线程MPI**
```bash
# 使用-ntmpi而不是真实MPI
gmx mdrun -v -deffnm md \
    -multidir replica_* \
    -replex 1000 \
    -ntmpi 8 \
    -ntomp 2
```

---

## ERROR-004: 交换接受率过低

### 症状
```
[WARN] 接受率过低 (<10%)
建议: 减小温度范围或增加副本数量
```

### 可能原因
1. **温度间隔过大**
   - 相邻副本温度差异太大
   - 能量重叠不足

2. **副本数量过少**
   - 无法覆盖温度范围

3. **系统尺寸过大**
   - 大系统需要更密集的温度分布

### 解决方案

**方案 1: 增加副本数量**
```bash
export NUM_REPLICAS=16  # 从8增加到16
export TEMP_MIN=300
export TEMP_MAX=400
./replica-exchange.sh
```

**方案 2: 减小温度范围**
```bash
export NUM_REPLICAS=8
export TEMP_MIN=300
export TEMP_MAX=350  # 从400减小到350
./replica-exchange.sh
```

**方案 3: 使用非均匀温度分布**
```bash
# 脚本已使用指数分布(最优)
# T_i = T_min * (T_max/T_min)^(i/(N-1))
# 这是推荐的温度分布方式
```

**方案 4: 增加交换频率**
```bash
export EXCHANGE_INTERVAL=500  # 从1000减小到500
./replica-exchange.sh
```

---

## ERROR-005: 交换接受率过高

### 症状
```
[WARN] 接受率过高 (>40%)
建议: 增大温度范围或减少副本数量
```

### 可能原因
1. **温度间隔过小**
   - 相邻副本温度过于接近
   - 浪费计算资源

2. **副本数量过多**
   - 超过必要数量

### 解决方案

**方案 1: 减少副本数量**
```bash
export NUM_REPLICAS=6  # 从8减少到6
./replica-exchange.sh
```

**方案 2: 增大温度范围**
```bash
export TEMP_MIN=300
export TEMP_MAX=450  # 从400增加到450
./replica-exchange.sh
```

**方案 3: 减少交换频率**
```bash
export EXCHANGE_INTERVAL=2000  # 从1000增加到2000
./replica-exchange.sh
```

---

## ERROR-006: 解复用失败

### 症状
```
[WARN] demux.pl 未找到,跳过解复用
```

### 可能原因
1. **demux.pl脚本缺失**
   - GROMACS安装时未包含scripts目录

2. **脚本不在PATH中**

### 解决方案

**方案 1: 查找demux.pl**
```bash
# 查找GROMACS安装目录中的demux.pl
find /usr -name "demux.pl" 2>/dev/null
find $HOME -name "demux.pl" 2>/dev/null

# 添加到PATH
export PATH=$PATH:/path/to/gromacs/scripts
```

**方案 2: 从源码获取**
```bash
# 下载GROMACS源码
wget https://ftp.gromacs.org/gromacs/gromacs-2026.1.tar.gz
tar xzf gromacs-2026.1.tar.gz

# 复制demux.pl
cp gromacs-2026.1/scripts/demux.pl /usr/local/bin/
chmod +x /usr/local/bin/demux.pl
```

**方案 3: 手动解复用**
```bash
# 使用Python脚本手动解复用
# (需要自己编写或使用第三方工具)

# 或者直接分析各副本轨迹
for i in {0..7}; do
    echo "分析副本 $i"
    gmx rms -s replica_$i/md.tpr -f replica_$i/md.xtc -o replica_$i/rmsd.xvg
done
```

---

## ERROR-007: GPU资源冲突

### 症状
```
ERROR-007: GPU资源冲突
Fatal error:
On rank 0 failed to initialize GPU #0
```

### 可能原因
1. **GPU数量不足**
   - 副本数量超过GPU数量

2. **GPU已被占用**
   - 其他进程正在使用GPU

3. **GPU分配不当**

### 解决方案

**方案 1: 指定GPU**
```bash
# 查看可用GPU
nvidia-smi

# 指定GPU ID
export GPU_IDS="0,1,2,3"
./replica-exchange.sh
```

**方案 2: 使用CPU**
```bash
# 不使用GPU
unset GPU_IDS
./replica-exchange.sh
```

**方案 3: 减少副本数量匹配GPU数量**
```bash
# 如果有4个GPU
export NUM_REPLICAS=4
./replica-exchange.sh
```

---

## ERROR-008: 内存不足

### 症状
```
ERROR-008: 内存不足
Fatal error:
Not enough memory available
```

### 可能原因
1. **副本数量过多**
   - 每个副本都需要独立内存

2. **系统尺寸过大**
   - 大系统 × 多副本 = 巨大内存需求

### 解决方案

**方案 1: 减少副本数量**
```bash
export NUM_REPLICAS=4  # 减少副本数量
./replica-exchange.sh
```

**方案 2: 减小系统尺寸**
```bash
# 使用更小的盒子
gmx editconf -f system.gro -o small_box.gro -c -d 1.0 -bt dodecahedron

# 重新溶剂化
gmx solvate -cp small_box.gro -cs spc216.gro -o solvated.gro -p topol.top
```

**方案 3: 分批运行**
```bash
# 将副本分成多批运行
# 批次1: 副本0-3
# 批次2: 副本4-7
# (需要手动修改脚本)
```

---

## ERROR-009: 检查点文件不兼容

### 症状
```
ERROR-009: 检查点文件不兼容
Fatal error:
Checkpoint file is for a simulation of X atoms, while the current system has Y atoms
```

### 可能原因
1. **使用了错误的检查点文件**
   - 检查点来自不同的系统

2. **拓扑已修改**
   - 在生成检查点后修改了拓扑

### 解决方案

**方案 1: 不使用检查点**
```bash
# 从头开始运行
unset INPUT_CPT
./replica-exchange.sh
```

**方案 2: 使用正确的检查点**
```bash
# 确保检查点与当前系统匹配
gmx check -s npt.tpr -c npt.cpt

# 使用匹配的检查点
export INPUT_CPT=npt.cpt
./replica-exchange.sh
```

**方案 3: 重新生成速度**
```bash
# 在MDP中启用速度生成
gen_vel = yes
gen_temp = 300
gen_seed = -1
```

---

## 最佳实践

### 1. 温度REMD参数选择

```bash
# 小系统 (<10,000原子)
NUM_REPLICAS=8-12
TEMP_RANGE=300-400K
EXCHANGE_INTERVAL=1000

# 中等系统 (10,000-50,000原子)
NUM_REPLICAS=12-24
TEMP_RANGE=300-400K
EXCHANGE_INTERVAL=1000

# 大系统 (>50,000原子)
NUM_REPLICAS=24-48
TEMP_RANGE=300-350K
EXCHANGE_INTERVAL=500-1000
```

### 2. 交换间隔选择

```bash
# 快速运动系统(溶液中小分子)
EXCHANGE_INTERVAL=100-500

# 中等速度系统(蛋白质)
EXCHANGE_INTERVAL=500-1000

# 慢速系统(膜蛋白)
EXCHANGE_INTERVAL=1000-2000
```

### 3. 监控交换统计

```bash
# 实时监控交换
tail -f replica_0/md.log | grep "Repl ex"

# 计算当前接受率
grep "Repl ex" replica_0/md.log | tail -100 | grep -c "x"
```

### 4. 资源优化

```bash
# 平衡CPU和GPU使用
# 如果有N个GPU:
NUM_REPLICAS=N
NTOMP=4-8  # 每副本使用多个线程

# 如果只有CPU:
NUM_REPLICAS=总核心数/NTOMP
NTOMP=2-4
```

---

## 参考文献

1. Sugita & Okamoto (1999). Replica-exchange molecular dynamics method for protein folding. *Chem. Phys. Lett.* **314**, 141-151.

2. GROMACS Manual 5.4.12: Replica exchange

3. Patriksson & van der Spoel (2008). A temperature predictor for parallel tempering simulations. *Phys. Chem. Chem. Phys.* **10**, 2073-2077.

4. Rathore et al. (2005). Optimal allocation of replicas in parallel tempering simulations. *J. Chem. Phys.* **122**, 024111.
