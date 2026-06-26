# 配体小分子拓扑生成（acpype + GAFF2）

> 场景：蛋白用 AMBER/CHARMM 力场，需要为小分子配体生成兼容的力场拓扑。

## 工具链

```
小分子结构 (PDB/MOL2/XYZ)
  ↓ obabel → MOL2
  ↓ acpype → GAFF2/GAFF 拓扑
  ↓ → GROMACS .itp + .gro
```

## 前置安装

> ⚠️ **安全提示**: 以下操作修改系统包和 `/etc/` 配置。在共享系统/HPC 上，建议在 conda 环境或容器中操作，避免影响其他用户。仅生产环境可控时执行系统级安装。

```bash
# acpype (AMBER 拓扑生成器)
pip install -i https://pypi.org/simple/ acpype

# 修复 teLeap 库依赖 (Ubuntu) — ⚠️ 系统级操作
# 仅在隔离环境(容器/VM)中执行：
# apt-get install -y libhdf4-0 libhdf5-dev
# echo "/usr/local/lib/python3.10/dist-packages/acpype/amber_linux/lib" > /etc/ld.so.conf.d/acpype.conf
# ldconfig

# 推荐替代方案：在 conda 环境中安装
# conda install -c conda-forge ambertools
```

## 工作流程

### Step 1: 准备配体结构

```bash
# 从复合体 PDB 提取配体
grep "^HETATM" complex.pdb > ligand.pdb
echo "END" >> ligand.pdb

# 或用 ORCA/Gaussian 优化后的结构
# 推荐使用优化后的紧凑结构（避免 acpype "atoms too scattered" 错误）
```

### Step 2: 转换为 MOL2

```bash
obabel ligand.pdb -O ligand.mol2 2>&1 | grep -v Warning
# 检查坐标：应为紧凑结构（所有原子在 5-10 Å 内）
```

### Step 3: 运行 acpype

```bash
# 生成 GAFF2 拓扑
acpype -i ligand.mol2 -b LIG -c gas -a gaff2

# 参数说明：
#   -i: 输入 MOL2 文件
#   -b: 残基名（3 字母，如 PET, LIG, DRG）
#   -c gas: Gasteiger 电荷（不依赖 antechamber）
#   -a gaff2: GAFF2 力场（兼容 AMBER 蛋白力场）
```

### Step 4: 获取输出

```bash
# 输出文件在 LIG.acpype/ 目录下
ls LIG.acpype/
# LIG_GMX.gro        - 配体坐标
# LIG_GMX.itp        - 配体拓扑（GAFF2 atomtypes + 参数）
# posre_LIG.itp      - 位置约束（可选）
```

## 常见问题

### "Atoms TOO scattered (> 3.0 Ang.)"

**原因：** 配体坐标跨度太大（如来自分子对接的坐标）  
**解决：** 使用量子化学优化后的紧凑结构，或用 `-f` 强制跳过（不推荐）

### "Tleap failed / libmfhdf.so.0 not found"

**原因：** AmberTools teLeap 缺少 HDF4 库  
**解决：**
> ⚠️ 系统包安装，仅在隔离环境中执行。
```bash
# ⚠️ 系统级操作 — 优先在 conda 环境中使用 conda install -c conda-forge ambertools
apt-get install -y libhdf4-0
# 创建符号链接
cd /usr/local/lib/python3.10/dist-packages/acpype/amber_linux/lib
ln -sf libmfhdf.so.0.0.0 libmfhdf.so.0
ln -sf libhdf5_hl.so.310.0.2 libhdf5_hl.so.310
ln -sf libhdf5.so.310.2.0 libhdf5.so.310
```

### "ce-c1-ha 0.000 0.000 ATTN, need revision"

**说明：** 某些 GAFF2 参数缺失（可忽略警告，GROMACS 会用默认值）  
**影响：** 对 MD 模拟影响很小

### 电荷选择

| 方法 | 精度 | 速度 | 需要 |
|------|------|------|------|
| `-c gas` | 低 | 快 | obabel |
| `-c bcc` | 中 | 慢 | antechamber (AmberTools) |
| `-c resp` | 高 | 很慢 | Gaussian + antechamber |

推荐先用 `-c gas` 快速生成，后续用 RESP 精修。
