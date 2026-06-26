# QM/MM 混合模拟故障排查

## 错误代码索引

| 错误代码 | 描述 | 快速修复 |
|---------|------|---------|
| ERROR-001 | QM 软件不可用 | 安装 CP2K/ORCA 或重新编译 GROMACS |
| ERROR-002 | QM 区域定义错误 | 检查 QM_RESIDUES 或 QM_ATOMS |
| ERROR-003 | 索引文件生成失败 | 验证残基名称和原子索引 |
| ERROR-004 | pdb2gmx 失败 | 检查 PDB 格式和力场选择 |
| ERROR-005 | SCF 不收敛 | 增加迭代次数或调整收敛标准 |
| ERROR-006 | grompp 失败 | 检查拓扑和 MDP 参数 |
| ERROR-007 | 能量最小化失败 | 检查系统结构和 QM/MM 配置 |
| ERROR-008 | NVT 平衡失败 | 减小时间步长或检查温度耦合 |
| ERROR-009 | NPT 平衡失败 | 检查压力耦合参数 |
| ERROR-010 | 生产模拟失败 | 检查模拟参数和系统稳定性 |

---

## ERROR-001: QM 软件不可用

### 症状
```
[ERROR-001] 未找到可用的 QM 软件
```

### 原因
- CP2K 或 ORCA 未安装
- GROMACS 未编译 CP2K 支持
- 环境变量未配置

### 解决方案

#### 方案 1: 安装 CP2K
```bash
# Ubuntu/Debian
sudo apt-get install cp2k

# 从源码编译
git clone --recursive https://github.com/cp2k/cp2k.git
cd cp2k
make -j 4 ARCH=Linux-x86-64-gfortran VERSION=psmp
```

#### 方案 2: 重新编译 GROMACS (推荐)
```bash
cd gromacs-2026.1
mkdir build && cd build
cmake .. -DGMX_CP2K=ON -DCMAKE_INSTALL_PREFIX=/usr/local/gromacs
make -j 4
sudo make install
```

#### 方案 3: 安装 ORCA
```bash
# 从官网下载: https://orcaforum.kofo.mpg.de/
# 解压并添加到 PATH
export PATH=/path/to/orca:$PATH
```

#### 方案 4: 使用外部 QM 接口
```bash
# 如果 GROMACS 未编译 CP2K 支持，使用 ORCA
QM_SOFTWARE=orca ./qmmm.sh
```

---

## ERROR-002: QM 区域定义错误

### 症状
```
[ERROR-002] QM_RESIDUES 未定义
[ERROR-002] QM_ATOMS 未定义
```

### 原因
- 未指定 QM 区域
- QM_SELECTION 与参数不匹配

### 解决方案

#### 方案 1: 基于残基选择
```bash
QM_SELECTION=residue QM_RESIDUES="LIG,HEM" ./qmmm.sh
```

#### 方案 2: 基于原子索引选择
```bash
QM_SELECTION=index QM_ATOMS="1-50,100-150" ./qmmm.sh
```

#### 方案 3: 自动检测 (推荐小分子配体)
```bash
QM_SELECTION=auto QM_RESIDUES="LIG" ./qmmm.sh
```

#### 方案 4: 手动创建索引文件
```bash
gmx make_ndx -f system.gro -o index.ndx
# 选择 QM 原子并命名为 "QMatoms"
QM_SELECTION=manual ./qmmm.sh
```

---

## ERROR-003: 索引文件生成失败

### 症状
```
[ERROR-003] 无法生成 QM 索引
```

### 原因
- 残基名称拼写错误
- 原子索引超出范围
- 结构文件格式错误

### 解决方案

#### 方案 1: 验证残基名称
```bash
# 查看所有残基名称
gmx dump -s system.gro | grep "resname"

# 使用正确的残基名称
QM_RESIDUES="LIG" ./qmmm.sh  # 注意大小写
```

#### 方案 2: 验证原子索引
```bash
# 查看原子总数
gmx check -f system.gro

# 确保索引在有效范围内
QM_ATOMS="1-50" ./qmmm.sh  # 不要超过总原子数
```

#### 方案 3: 修复结构文件
```bash
# 重新生成 GRO 文件
gmx editconf -f system.pdb -o system.gro
```

---

## ERROR-004: pdb2gmx 失败

### 症状
```
[ERROR-004] pdb2gmx 失败
```

### 原因
- PDB 文件格式错误
- 缺少氢原子
- 力场不支持某些残基

### 解决方案

#### 方案 1: 清理 PDB 文件
```bash
# 移除非标准残基
grep "^ATOM\|^HETATM" protein.pdb > clean.pdb

# 使用 pdb4amber 清理
pdb4amber -i protein.pdb -o clean.pdb
```

#### 方案 2: 添加氢原子
```bash
# 使用 reduce
reduce protein.pdb > protein_H.pdb

# 或使用 pdb2gmx 的 -ignh 选项
gmx pdb2gmx -f protein.pdb -o system.gro -ignh
```

#### 方案 3: 更换力场
```bash
# 尝试不同的力场
MM_FORCEFIELD=charmm36 ./qmmm.sh
MM_FORCEFIELD=oplsaa ./qmmm.sh
```

#### 方案 4: 手动提供拓扑
```bash
# 如果已有拓扑文件
INPUT_GRO=system.gro INPUT_TOP=topol.top ./qmmm.sh
```

---

## ERROR-005: SCF 不收敛

### 症状
```
[ERROR-005] SCF 未收敛
SCF run NOT converged (CP2K)
SCF NOT CONVERGED (ORCA)
```

### 原因
- 初始猜测不佳
- 收敛标准过严
- 系统电荷/多重度错误
- QM 区域定义不合理

### 解决方案

#### 方案 1: 增加 SCF 迭代次数 (CP2K)
编辑 `qmmm.inp`:
```
&SCF
  MAX_SCF 100  # 从 50 增加到 100
  EPS_SCF 1.0E-5  # 放宽收敛标准
&END SCF
```

#### 方案 2: 使用更好的初始猜测
```
&SCF
  SCF_GUESS RESTART  # 使用上一步的波函数
&END SCF
```

#### 方案 3: 调整收敛算法 (ORCA)
编辑 `qmmm.inp`:
```
%scf
  MaxIter 200
  SlowConv true  # 使用慢收敛模式
  DIISMaxEq 10
end
```

#### 方案 4: 检查电荷和多重度
```bash
# 确保电荷和多重度正确
QM_CHARGE=0 QM_MULTIPLICITY=1 ./qmmm.sh

# 对于自由基系统
QM_MULTIPLICITY=2 ./qmmm.sh
```

#### 方案 5: 减小 QM 区域
```bash
# 只包含关键原子
QM_ATOMS="1-30" ./qmmm.sh  # 减小 QM 区域
```

---

## ERROR-006: grompp 失败

### 症状
```
[ERROR-006] grompp (EM/NVT/NPT/MD) 失败
```

### 原因
- MDP 参数错误
- 拓扑文件不完整
- 索引组不存在
- QM/MM 参数不兼容

### 解决方案

#### 方案 1: 检查 MDP 参数
```bash
# 查看详细错误信息
gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr

# 允许警告 (谨慎使用)
gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr -maxwarn 2
```

#### 方案 2: 验证拓扑文件
```bash
# 检查拓扑完整性
gmx check -s topol.top

# 重新生成拓扑
gmx pdb2gmx -f protein.pdb -o system.gro -p topol.top
```

#### 方案 3: 检查索引组
```bash
# 查看所有索引组
gmx make_ndx -f system.gro -n index.ndx

# 确保 "QMatoms" 组存在
```

#### 方案 4: 调整 QM/MM 参数
```bash
# 如果 GROMACS 不支持某些 QM/MM 参数，移除或修改
# 编辑 MDP 文件，注释掉不支持的参数
```

---

## ERROR-007: 能量最小化失败

### 症状
```
[ERROR-007] mdrun (EM) 失败
LINCS warnings
Segmentation fault
```

### 原因
- 原子重叠
- QM/MM 边界不合理
- 力场参数缺失
- 系统电荷不平衡

### 解决方案

#### 方案 1: 增加能量最小化步数
```bash
# 编辑 em.mdp
nsteps = 100000  # 从 50000 增加
emtol = 5000.0   # 放宽收敛标准
```

#### 方案 2: 使用更温和的最小化方法
```bash
# 先用 steep，再用 cg
integrator = steep  # 第一阶段
# 然后
integrator = cg     # 第二阶段
```

#### 方案 3: 检查 QM/MM 边界
```bash
# 确保边界不切断共价键
# 使用 Link atom 方法
LINK_ATOM_METHOD=hydrogen ./qmmm.sh
```

#### 方案 4: 添加位置限制
```bash
# 对 QM 区域添加弱限制
define = -DPOSRES_QM
```

#### 方案 5: 检查系统电荷
```bash
# 确保系统总电荷为整数
gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr -v
# 查看 "System has non-zero total charge" 警告
```

---

## ERROR-008: NVT 平衡失败

### 症状
```
[ERROR-008] mdrun (NVT) 失败
Temperature coupling failed
LINCS warnings
```

### 原因
- 时间步长过大
- 温度耦合参数不当
- 系统未充分最小化
- QM 计算不稳定

### 解决方案

#### 方案 1: 减小时间步长
```bash
DT=0.0005 ./qmmm.sh  # 从 1 fs 减到 0.5 fs
```

#### 方案 2: 调整温度耦合
```bash
# 编辑 nvt.mdp
tau_t = 0.5  # 从 0.1 增加到 0.5
```

#### 方案 3: 延长 NVT 时间
```bash
# 编辑 nvt.mdp
nsteps = 100000  # 增加平衡时间
```

#### 方案 4: 分阶段加热
```bash
# 先 100K，再 200K，最后 300K
TEMPERATURE=100 ./qmmm.sh  # 第一阶段
TEMPERATURE=200 ./qmmm.sh  # 第二阶段
TEMPERATURE=300 ./qmmm.sh  # 第三阶段
```

#### 方案 5: 检查 EM 质量
```bash
# 确保 EM 充分收敛
echo "Potential" | gmx energy -f em.edr -o potential.xvg
# 查看能量是否稳定
```

---

## ERROR-009: NPT 平衡失败

### 症状
```
[ERROR-009] mdrun (NPT) 失败
Pressure coupling failed
Box deformation
```

### 原因
- 压力耦合参数不当
- 盒子尺寸不合理
- NVT 未充分平衡
- 可压缩性设置错误

### 解决方案

#### 方案 1: 调整压力耦合参数
```bash
# 编辑 npt.mdp
tau_p = 5.0  # 从 2.0 增加到 5.0
pcoupl = Berendsen  # 先用 Berendsen，再用 Parrinello-Rahman
```

#### 方案 2: 延长 NPT 时间
```bash
# 编辑 npt.mdp
nsteps = 100000  # 增加平衡时间
```

#### 方案 3: 检查盒子尺寸
```bash
# 确保盒子足够大
gmx editconf -f system.gro -o system.gro -d 1.5  # 增加边距
```

#### 方案 4: 分阶段压力耦合
```bash
# 第一阶段: Berendsen
pcoupl = Berendsen
tau_p = 2.0

# 第二阶段: Parrinello-Rahman
pcoupl = Parrinello-Rahman
tau_p = 5.0
```

---

## ERROR-010: 生产模拟失败

### 症状
```
[ERROR-010] mdrun (MD) 失败
Simulation unstable
QM calculation failed
```

### 原因
- 平衡不充分
- QM/MM 参数不合理
- 时间步长过大
- QM 软件崩溃

### 解决方案

#### 方案 1: 延长平衡时间
```bash
# 重新运行 NVT 和 NPT，增加时间
# 确保 RMSD 和能量稳定
```

#### 方案 2: 减小时间步长
```bash
DT=0.0005 ./qmmm.sh  # 使用 0.5 fs
```

#### 方案 3: 检查 QM 日志
```bash
# CP2K
tail -100 qmmm.out

# ORCA
tail -100 qmmm.log

# 查找 SCF 不收敛或其他错误
```

#### 方案 4: 调整 QM 参数
```bash
# 使用更稳定的泛函
QM_METHOD=PBE ./qmmm.sh  # 而不是 B3LYP

# 使用更小的基组
QM_BASIS=DZVP-MOLOPT-SR-GTH ./qmmm.sh
```

#### 方案 5: 检查检查点文件
```bash
# 从检查点恢复
gmx mdrun -deffnm md -cpi md.cpt -append
```

---

## ERROR-011: ORCA 多核并行失败 (OpenMPI)

### 症状
```
mpirun has detected an attempt to run as root.
ORCA finished by error termination in Startup
```
或 ORCA 使用 `%pal nprocs N end` (N>1) 时卡死无输出

### 原因 (按优先级排查)

1. **Root 权限被 OpenMPI 拒绝** — 最常见原因
2. **主机名不在 /etc/hosts** — Docker/AutoDL 容器通病
3. **Docker 容器缺少 SYS_PTRACE capability** — 底层限制

### 解决方案

#### Fix 1: 允许 root 运行 MPI
```bash
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
# ⚠️ 仅单用户/隔离环境写入 ~/.bashrc
# 共享系统上在终端手动 export，避免影响其他用户
```

#### Fix 2: 添加主机名到 /etc/hosts
> ⚠️ **安全提示**: `/etc/hosts` 是系统关键文件。修改前确认对系统的影响，生产环境需管理员审批。仅容器/隔离环境使用。

```bash
# ⚠️ 修改系统文件 — 仅在 AutoDL/Docker 等动态容器中使用
echo "127.0.0.1 $(hostname)" >> /etc/hosts
# 验证: ping -c1 $(hostname)
```
> ℹ️ 这一步对 AutoDL/Docker 容器至关重要！容器主机名是动态的，
> 不在 /etc/hosts 中会导致 OpenMPI 进程间无法通信。
> 在物理机/共享集群上，不应修改 /etc/hosts，应联系系统管理员配置域名解析。

#### Fix 3: Docker 容器需要 --cap-add=SYS_PTRACE
> ⚠️ `SYS_PTRACE` 是 Linux security capability，授予容器进程 ptrace 权限。仅信任的容器镜像使用。
如果在容器内完成 Fix 1+2 后 mpirun 仍卡死：
```bash
# 测试: timeout 5 mpirun -np 2 hostname
# 如果卡死 → 容器缺少 SYS_PTRACE capability
```
**需要容器管理员**在启动时添加：
```bash
docker run --cap-add=SYS_PTRACE ...
```
如果无法修改容器权限，只能使用单核模式 (`%pal nprocs 1 end`)

### 完整环境配置 (推荐写入 ~/.bashrc)
```bash
# === ORCA 6.0 MPI 环境 ===
export ORCA_DIR=/path/to/orca_6_0_1
export PATH=$ORCA_DIR:$PATH
export LD_LIBRARY_PATH=$ORCA_DIR/lib:$LD_LIBRARY_PATH
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
```

### 参考
- [ORCA 6.0 Manual - Calling the Program (Serial and Parallel)](https://www.faccts.de/docs/orca/6.0/manual/contents/parallel.html)
- [OpenMPI FAQ: Running as root](https://www.open-mpi.org/faq/?category=running#running-as-root)

---

## 性能优化

### 1. 减小 QM 区域
```bash
# 只包含关键原子 (活性位点、配体)
QM_ATOMS="1-30" ./qmmm.sh
```

### 2. 使用 GPU 加速 MM 部分
```bash
GPU_ID=0 ./qmmm.sh
```

### 3. 并行化 QM 计算
```bash
QM_NPROC=8 ./qmmm.sh
```

### 4. 使用更快的泛函
```bash
QM_METHOD=PBE ./qmmm.sh  # 比 B3LYP 快
```

### 5. 减小基组
```bash
QM_BASIS=DZVP-MOLOPT-SR-GTH ./qmmm.sh  # 比 TZVP 快
```

---

## 调试技巧

### 1. 逐步运行
```bash
# 只运行 EM
# 手动编辑脚本，注释掉 NVT/NPT/MD 部分
```

### 2. 查看详细日志
```bash
# 增加日志级别
gmx mdrun -deffnm md -v -stepout 100
```

### 3. 可视化结构
```bash
# 使用 VMD 或 PyMOL 检查 QM/MM 边界
vmd system.gro
```

### 4. 检查能量组成
```bash
echo "Potential Kinetic-En. Total-Energy Temperature Pressure" | \
  gmx energy -f md.edr -o energy_components.xvg
```

### 5. 监控 QM 计算
```bash
# 实时查看 QM 输出
tail -f qmmm.out  # CP2K
tail -f qmmm.log  # ORCA
```

---

## 常见问题 FAQ

### Q1: QM/MM 比纯 MM 慢多少？
A: 通常慢 10-100 倍，取决于 QM 区域大小和方法。

### Q2: 如何选择 QM 区域？
A: 包含反应中心、配体、关键残基。避免切断共价键。

### Q3: 哪个 QM 软件更好？
A: CP2K 与 GROMACS 集成更好，ORCA 功能更丰富。

### Q4: 如何验证 QM/MM 结果？
A: 与纯 QM 计算对比，检查能量守恒，分析轨迹稳定性。

### Q5: 可以用 GPU 加速 QM 计算吗？
A: CP2K 支持 GPU (CUDA)，ORCA 部分支持。

---

## 参考资源

- [GROMACS QM/MM 文档](https://manual.gromacs.org/current/reference-manual/special/qmmm.html)
- [CP2K 手册](https://manual.cp2k.org/)
- [ORCA 手册](https://orcaforum.kofo.mpg.de/app.php/portal)
- [QM/MM 教程](https://www.cp2k.org/howto:qmmm)

---

生成时间: $(date)
