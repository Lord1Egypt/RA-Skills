# CP2K 输入文件生成器 Skill - 使用指南

## Skill 概述

`cp2k-input-generator` Skill 旨在帮助用户根据计算要求和结构文件,自动生成准确可用的 CP2K 输入文件 (.inp)。

## 主要功能

### 1. 支持多种计算类型
- ✅ 单点能量计算 (ENERGY)
- ✅ 几何优化 (GEO_OPT)
- ✅ 分子动力学 (MD)
- ✅ 频率分析 (FREQUENCY)
- ✅ NEB 路径搜索 (NEB)
- ✅ 能带结构 (BAND_STRUCTURE)
- ✅ 态密度 (DOS)
- ✅ QMMM 计算

### 2. 支持多种结构文件格式
- ✅ XYZ 格式 (.xyz)
- ✅ CIF 格式 (.cif)
- ✅ PDB 格式 (.pdb)
- ✅ Gaussian 格式 (.gjf, .com)
- ✅ 从 CP2K 输出文件提取结构

### 3. 智能参数选择
- 根据体系大小自动选择基组
- 根据周期性自动设置 k 点
- 根据计算类型推荐 CUTOFF
- 自动配置 SCF 收敛参数

### 4. 支持多种计算方法
- Quickstep (DFT)
- QMMM (量子力学/分子力学混合)
- Classical/MM (纯分子力学)
- xTB (半经验方法)

## 文件结构

```
cp2k-input-generator/
├── SKILL.md                      # Skill 主文档,包含完整的执行指南
├── references/
│   └── cp2k_input_reference.md   # CP2K 输入文件完整参考
└── scripts/
    └── generate_cp2k_input.py    # Python 生成脚本
```

## 使用方法

### 方法 1: 通过 AI 助手使用(推荐)

直接向 AI 助手描述你的计算需求,例如:

```
"帮我生成一个 CP2K 输入文件用于几何优化。
结构文件是 structure.xyz,
使用 PBE 泛函,体系是金属铜,
净电荷为 0,自旋多重度为 1。"
```

AI 助手会自动:
1. 读取并解析结构文件
2. 确定合适的计算参数
3. 生成输入文件
4. 输出为 `function.inp`

### 方法 2: 使用 Python 脚本

#### 单点能量计算

```bash
python scripts/generate_cp2k_input.py energy structure.xyz \
  -o function.inp \
  -p energy_calc \
  -c 0 \
  -m 1 \
  -f PBE
```

#### 几何优化

```bash
python scripts/generate_cp2k_input.py opt structure.xyz \
  -o geo_opt.inp \
  -p opt_calc \
  -c 0 \
  -m 1 \
  -f PBE \
  --optimizer BFGS \
  --max-iter 500
```

#### 分子动力学

```bash
python scripts/generate_cp2k_input.py md structure.xyz \
  -o md.inp \
  -p md_calc \
  -c 0 \
  -m 1 \
  -f PBE \
  --ensemble NVT \
  --steps 50000 \
  --timestep 0.5 \
  --temperature 300
```

## 命令行参数说明

### 通用参数
- `calculation_type`: 计算类型 (energy/opt/md/freq)
- `structure_file`: 结构文件路径
- `-o, --output`: 输出文件名 (默认: function.inp)
- `-p, --project`: 项目名称
- `-c, --charge`: 净电荷 (默认: 0)
- `-m, --multiplicity`: 自旋多重度 (默认: 1)
- `-f, --functional`: 交换关联泛函 (默认: PBE)

### MD 专用参数
- `--ensemble`: 系综 (默认: NVT)
- `--steps`: MD 步数 (默认: 50000)
- `--timestep`: 时间步长 fs (默认: 0.5)
- `--temperature`: 温度 K (默认: 300)

### 几何优化专用参数
- `--optimizer`: 优化器 (默认: BFGS)
- `--max-iter`: 最大迭代次数 (默认: 500)

## 使用示例

### 示例 1: 简单单点计算

**用户请求:**
```
"用 CP2K 计算这个分子的能量,
结构在 water.xyz,
使用 PBE 泛函。"
```

**生成的输入文件:**
```
&GLOBAL
  PROJECT water_energy
  PRINT_LEVEL LOW
  RUN_TYPE ENERGY
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep
  &SUBSYS
    &CELL
      ...
    &END CELL
    &COORD
      O       0.00000000    0.00000000    0.11926200
      H       0.00000000    0.76323900   -0.47704700
      H       0.00000000   -0.76323900   -0.47704700
    &END COORD
    &KIND O
      ELEMENT O
      BASIS_SET TZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE
    &END KIND
    &KIND H
      ELEMENT H
      BASIS_SET TZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE
    &END KIND
  &END SUBSYS
  
  &DFT
    BASIS_SET_FILE_NAME  BASIS_MOLOPT
    POTENTIAL_FILE_NAME  POTENTIAL
    CHARGE    0
    MULTIPLICITY    1
    &QS
      EPS_DEFAULT 1E-10
    &END QS
    &POISSON
      PERIODIC NONE
      PSOLVER MT
    &END POISSON
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
    &MGRID
      CUTOFF 350
      REL_CUTOFF 50
      NGRIDS 5
    &END MGRID
    &SCF
      MAX_SCF 128
      EPS_SCF 5.0E-06
      &DIAGONALIZATION
        ALGORITHM STANDARD
      &END DIAGONALIZATION
      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.4
        NBROYDEN 8
      &END MIXING
    &END SCF
  &END DFT
&END FORCE_EVAL
```

### 示例 2: 晶体几何优化

**用户请求:**
```
"优化硅晶体的结构,
结构文件是 silicon.cif,
周期性是 XYZ 方向,
使用 3x3x3 的 k 点网格。"
```

### 示例 3: 表面体系的分子动力学

**用户请求:**
```
"做一个铜表面的分子动力学模拟,
结构在 copper_surface.pdb,
温度 300 K, 1 ps 的模拟时间,
使用 NVT 系综,CSVR 热浴。"
```

## 参数选择指南

### CUTOFF 选择

| 体系大小 | 基组类型 | 推荐值 |
|---------|---------|--------|
| 小分子 (<50 原子) | TZVP-MOLOPT | 300-350 Ry |
| 中等体系 (50-200 原子) | DZVP-MOLOPT | 400-500 Ry |
| 大体系 (>200 原子) | DZVP-MOLOPT | 500-600 Ry |

### k 点选择

| 体系类型 | 超胞大小 | 推荐 k 点 |
|---------|---------|----------|
| 体相晶体 | 原胞 | 6x6x6 |
| | 2x2x2 超胞 | 3x3x3 |
| | 3x3x3 超胞 | Γ 点 |
| 表面/平板 | - | 8x8x1 或 6x6x1 |
| 纳米线 | - | 1x1x6 或 1x1x4 |

### SCF 收敛判据

| 计算类型 | EPS_SCF | MAX_SCF |
|---------|---------|---------|
| 初步测试 | 1.0E-05 | 50 |
| 标准计算 | 5.0E-06 | 128 |
| 高精度 | 1.0E-07 | 200 |
| MD 模拟 | 1.0E-05 | 25 |

## 特殊计算处理

### 自旋极化计算

对于有未成对电子的体系,需要设置自旋参数:

```
&DFT
  CHARGE 0
  MULTIPLICITY 3    # 2S+1, S 为总自旋
  UKS               # 启用非受限自旋
  ...
&END DFT
```

### 金属体系

金属体系需要 smearing 和密 k 点采样:

```
&DFT
  &SMearing
    METHOD FERMI_DIRAC
    WIDTH 0.01
  &END SMearing
  ...
  &KPOINTS
    SCHEME MONKHORST-PACK  8  8  8
  &END KPOINTS
&END DFT
```

### xTB 半经验方法

适合大体系的快速计算:

```
&DFT
  &QS
    METHOD xTB
    &xTB
      DO_EWALD T
      CHECK_ATOMIC_CHARGES F
      &PARAMETER
        DISPERSION_PARAMETER_FILE dftd3.dat
        PARAM_FILE_NAME xTB_parameters
      &END PARAMETER
    &END xTB
  &END QS
&END DFT
```

## 常见问题

### Q: 如何从 CP2K 输出文件提取结构?

A: AI 助手会自动从 CP2K 输出文件中提取最后的原子坐标,用于生成新的输入文件。

### Q: SCF 不收敛怎么办?

A: 可以尝试:
1. 降低收敛判据 (EPS_SCF)
2. 增加混合参数 (ALPHA)
3. 使用不同的混合方法
4. 提高 CUTOFF
5. 使用 smearing (金属体系)

### Q: 计算太慢怎么办?

A: 可以尝试:
1. 降低基组精度
2. 减少k点数
3. 使用 xTB 方法
4. 使用 OT 方法
5. 并行计算

### Q: 如何设置 QMMM 计算?

A: 需要指定 QM 区域和 MM 区域,并设置耦合参数。AI 助手会根据你的描述生成相应的 QMMM 输入文件。

## 参考资源

- **CP2K 官方网站**: https://www.cp2k.org/
- **用户工作区示例**: `/file/` 目录下的各种计算示例
- **Skill 参考文档**: `references/cp2k_input_reference.md`

## 技术支持

如果遇到问题:
1. 查阅 `references/cp2k_input_reference.md` 参考文档
2. 查看 `/file/` 目录下的示例文件
3. 访问 CP2K 官方网站获取帮助

## 更新日志

### v1.0.0 (2026-03-12)
- 初始版本发布
- 支持基本计算类型 (energy, opt, md)
- 支持多种结构文件格式
- 智能参数选择
- 完整的参考文档

## 贡献

欢迎提出改进建议和功能请求!
