# GPU MD 运行指南

> 如何在 GROMACS 中正确使用 GPU 加速，避坑指南。

## GPU 加速选项

GROMACS GPU 可卸载以下计算：

| 选项 | 含义 | 适用阶段 |
|------|------|----------|
| `-nb gpu` | 短程非键相互作用 | EM, NVT, NPT, MD |
| `-pme gpu` | PME 长程静电 | **仅 MD/SD 积分器** ⚠️ |
| `-bonded gpu` | 键合相互作用 | **仅 MD/SD 积分器** ⚠️ |
| `-update gpu` | 坐标/约束更新 | **仅 MD/SD 积分器** ⚠️ |

## 各阶段 GPU 使用策略

### 能量最小化 (EM)

```bash
# ✅ 正确：EM 只能用 -nb gpu
gmx mdrun -deffnm em -nb gpu -ntmpi 1 -ntomp 16

# ❌ 错误：EM 不支持 GPU PME/bonded/update
gmx mdrun -deffnm em -nb gpu -pme gpu -bonded gpu -update gpu
# → 错误: "Cannot compute PME interactions on a GPU, because:
#    PME GPU does not support: Non-dynamical integrator"
```

### NVT/NPT/Production MD

```bash
# ✅ 正确：全部 GPU 卸载
gmx mdrun -deffnm md \
  -nb gpu -pme gpu -bonded gpu -update gpu \
  -ntmpi 1 -ntomp 8 -pin on
```

## OMP_NUM_THREADS 冲突

**症状：**
```
Fatal error: Environment variable OMP_NUM_THREADS (13) and the number of
threads requested on the command line (8) have different values.
```

**解决：**
```bash
# 方案 A: 取消环境变量
unset OMP_NUM_THREADS
gmx mdrun ... -ntomp 8

# 方案 B: 匹配环境变量
export OMP_NUM_THREADS=8
gmx mdrun ... -ntomp 8
```

## 性能调优

### 基础命令

```bash
# 推荐配置（单 GPU）
gmx mdrun -deffnm md \
  -nb gpu -pme gpu -bonded gpu -update gpu \
  -ntmpi 1 -ntomp 8 \
  -pin on -pinoffset 0

# -ntmpi 1: 1 个 MPI rank（单 GPU）
# -ntomp N: N 个 OpenMP 线程（CPU 核心的 1/4 ~ 1/2）
# -pin on: 绑定线程到核心
```

### 性能监控

```bash
# GPU 利用率
watch -n 2 nvidia-smi

# 实时 ns/day
tail -f md.log | grep "Performance:"
```

### 预期性能 (RTX 5060 Ti)

| 体系大小 | 性能 (ns/day) |
|----------|---------------|
| ~100k atoms | ~180-210 |
| ~200k atoms | ~90-110 |
| ~500k atoms | ~35-45 |

## 后台运行

```bash
# nohup 后台 + 日志
nohup gmx mdrun -deffnm md \
  -nb gpu -pme gpu -bonded gpu -update gpu \
  -ntmpi 1 -ntomp 8 -pin on > mdrun.out 2>&1 &

# 查看进度
tail -20 mdrun.out
grep "Performance:" md.log | tail -1
```

## GPU 选择

```bash
# 指定 GPU 设备
export GMX_GPU_ID=0          # 使用 GPU 0
gmx mdrun -gpu_id 0 ...      # 或通过命令行

# 多 GPU（需要 MPI）
gmx mdrun -nb gpu -pme gpu -ntmpi 2 -gpu_id 01
```
