---
name: cp2k-input-generator
description: This skill should be used when generating CP2K input files (.inp) for quantum chemistry calculations. Use when users request CP2K input file creation from structural files (cif, pdb, xyz, etc.) or CP2K output files, with specifications for calculation types (energy calculation, geometry optimization, molecular dynamics, frequency analysis, NEB, etc.), computational methods (DFT, QMMM, MM), and other parameters.
license: MIT
---

# CP2K 输入文件生成器

## Skill 概述

本 Skill 用于根据用户的计算要求和结构文件,生成准确可用的 CP2K 输入文件。支持多种计算类型、结构格式和计算方法,并能够根据体系特征自动选择合适的参数。

## 触发词

当用户提及以下内容时应该使用此 Skill:

- "生成 CP2K 输入文件"
- "创建 .inp 文件"
- "CP2K calculation input"
- "准备 CP2K 计算任务"
- "写一个 CP2K 输入文件"
- "帮我生成 CP2K 的输入"
- 包含计算类型关键词: "单点计算", "几何优化", "分子动力学", "MD", "频率分析", "NEB", "能带结构", "DOS"
- 提及结构文件格式: cif, pdb, xyz, gaussian
- 从 CP2K 输出文件生成新的输入

## 执行流程

### 步骤 1: 理解计算需求

向用户确认或从描述中提取以下信息:

**必需参数:**
1. **计算类型** (RUN_TYPE):
   - ENERGY / ENERGY_FORCE: 单点能量计算
   - GEO_OPT: 几何优化
   - MD: 分子动力学
   - FREQUENCY: 频率分析
   - VIBRATIONAL_ANALYSIS: 振动分析
   - BAND_STRUCTURE: 能带结构
   - NEB: 弹性带路径搜索

2. **结构文件**:
   - 支持格式: .xyz, .cif, .pdb, .gjf, .com
   - 或提供直接的坐标数据

**重要参数(如果没有提供需要询问):**
3. **计算方法**:
   - Quickstep (DFT): 密度泛函理论
   - QMMM: 量子力学/分子力学混合方法
   - Classical/MM: 纯分子力学
   - xTB: 半经验方法

4. **周期性条件**:
   - XYZ: 三维周期性(晶体)
   - XY: 二维周期性(表面/平板)
   - X/Y/Z: 一维周期性(纳米线)
   - NONE: 孤立体系(分子/团簇)

5. **电荷和自旋**:
   - CHARGE: 净电荷
   - MULTIPLICITY: 自旋多重度(如果自旋极化)

**可选参数(如果没有提供可以使用默认值):**
6. **交换关联泛函**: PBE, BLYP, PBE0, HSE06 等
7. **基组类型**: DZVP-MOLOPT, TZVP-MOLOPT 等
8. **k点采样**: Monkhorst-Pack 网格
9. **CUTOFF**: 平面波截止能量
10. **SCF 收敛判据**
11. **MD 参数**: 系综,温度,时间步长,步数
12. **几何优化参数**: 优化器,收敛判据,最大迭代次数

### 步骤 2: 读取和解析结构文件

使用 `read_file` 工具读取结构文件内容,然后:

- **CIF 文件**: 提取晶胞参数和原子坐标
- **PDB 文件**: 提取原子类型和坐标,注意元素符号
- **XYZ 文件**: 提取原子类型和坐标
- **Gaussian 文件**: 提取原子类型和坐标
- **CP2K 输出文件**: 从输出中提取最后的结构坐标

### 步骤 3: 确定计算参数

根据体系特征和计算需求,智能选择参数:

**基组选择:**
```
体系大小判断:
- 小体系 (<50 原子): TZVP-MOLOPT-GTH
- 中等体系 (50-200 原子): DZVP-MOLOPT-SR-GTH  
- 大体系 (>200 原子): DZVP-MOLOPT-SR-GTH
```

**CUTOFF 选择:**
```
- 小分子: 300-350 Ry
- 中等体系: 400-500 Ry
- 大体系: 500-600 Ry
```

**k点选择:**
```
周期性体系:
- 原胞: 4x4x4 或 6x6x6
- 2x2x2 超胞: 2x2x2
- 3x3x3 超胞: Γ 点 (1x1x1)
- 4x4x4 超胞: Γ 点 (1x1x1)
- 表面模型: 8x8x1 或 6x6x1
```

**SCF 参数:**
```
- MAX_SCF: 128 (标准), 300 (困难体系)
- EPS_SCF: 5.0E-06 (标准), 1.0E-05 (快速), 1.0E-07 (高精度)
- DIAGONALIZATION: STANDARD (小体系), DAVIDSON (大体系)
- MIXING: BROYDEN_MIXING 或 PULAY_MIXING
```

### 步骤 4: 生成输入文件内容

根据计算类型生成相应的输入文件结构:

#### 通用结构框架:

```
&GLOBAL
  PROJECT <project_name>
  PRINT_LEVEL <level>
  RUN_TYPE <calculation_type>
&END GLOBAL

&FORCE_EVAL
  METHOD <Quickstep/QMMM/Classical>
  &SUBSYS
    &CELL
     晶胞定义
    &END CELL
    &COORD
      原子坐标
    &END COORD
    &KIND
      每种元素类型的基组和赝势
    &END KIND
  &END SUBSYS
  
  &DFT
    BASIS_SET_FILE_NAME
    POTENTIAL_FILE_NAME
    CHARGE
    MULTIPLICITY
    [UKS] (如果自旋极化)
    &KPOINTS
      k点设置
    &END KPOINTS
    &QS
    &END QS
    &POISSON
    &END POISSON
    &XC
      &XC_FUNCTIONAL <PBE/BLYP/PBE0/HSE06>
      &END XC_FUNCTIONAL
    &END XC
    &MGRID
      CUTOFF
      REL_CUTOFF
      NGRIDS
    &END MGRID
    &SCF
      收敛设置
    &END SCF
  &END DFT
&END FORCE_EVAL

&MOTION
  根据计算类型添加相应设置
&END MOTION
```

#### 不同计算类型的 MOTION 设置:

**GEO_OPT (几何优化):**
```
&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER <BFGS/CG/LBFGS>
    &BFGS
      TRUST_RADIUS 0.2
    &END BFGS
    MAX_ITER 500
    MAX_DR 3E-3
    RMS_DR 1.5E-3
    MAX_FORCE 4.5E-4
    RMS_FORCE 3E-4
  &END GEO_OPT
  &PRINT
    &TRAJECTORY
      FORMAT xyz
    &END TRAJECTORY
  &END PRINT
&END MOTION
```

**MD (分子动力学):**
```
&MOTION
  &MD
    ENSEMBLE <NVT/NVE/NPT>
    STEPS 50000
    TIMESTEP 0.2-1.0  # fs
    TEMPERATURE 300
    &THERMOSTAT
      TYPE <CSVR/NOSE/LANGEVIN>
      &<THERMOSTAT_TYPE>
        TIMECON 100
      &END <THERMOSTAT_TYPE>
    &END THERMOSTAT
  &END MD
  &PRINT
    &TRAJECTORY
      &EACH
        MD 10
      &END EACH
      FORMAT xyz
    &END TRAJECTORY
  &END PRINT
&END MOTION
```

**FREQUENCY (频率分析):**
```
&MOTION
  &FREQUENCY
    &PRINT
      &EIGENVECTORS
      &END EIGENVECTORS
    &END PRINT
  &END FREQUENCY
&END MOTION
```

**NEB (弹性带):**
```
&MOTION
  &NEB
    NIMAGE 7
    K_SPRING 0.5
    TOL_FORCE 0.02
  &END NEB
&END MOTION
```

### 步骤 5: 处理特殊情况

**自旋极化计算:**
- 添加 `UKS` 关键字
- 设置正确的 `MULTIPLICITY` 值
- 对于铁磁性系统,设置所有原子的初始磁矩

**金属体系:**
- 使用 Fermi-Dirac smearing
- 设置 `&SMearing METHOD FERMI_DIRAC WIDTH 0.01`
- 使用较密的 k 点采样

**表面/平板模型:**
- 周期性设置为 XY
- 使用适当的真空层(通常 >15 Å)
- k 点设置为 8x8x1 或类似

**QMMM 计算:**
- METHOD 设置为 QMMM
- 定义 QM 和 MM 区域
- 设置耦合参数

**xTB 方法:**
- 在 `&QS` 中设置 `METHOD xTB`
- 添加 `&xTB` 部分
- 包含必要的参数文件

### 步骤 6: 使用辅助脚本(可选)

对于复杂的输入文件生成,可以使用 `scripts/generate_cp2k_input.py` 脚本:

```bash
python scripts/generate_cp2k_input.py <calculation_type> <structure_file> \
  -o function.inp \
  -p <project_name> \
  -c <charge> \
  -m <multiplicity> \
  -f <functional>
```

支持的命令:
- `energy`: 单点能量计算
- `opt`: 几何优化
- `md`: 分子动力学

### 步骤 7: 输入文件验证

生成输入文件后,检查:

1. **语法正确性**:
   - 所有 `&SECTION` 都有对应的 `&END SECTION`
   - 关键字拼写正确
   - 参数在合理范围内

2. **参数一致性**:
   - CHARGE 和 MULTIPLICITY 匹配
   - CUTOFF 和基组匹配
   - k 点和周期性匹配

3. **文件路径**:
   - 结构文件路径正确
   - 基组文件和赝势文件路径正确

4. **资源预估**:
   - 估算计算所需的内存和 CPU 核心数
   - 提醒用户计算可能需要的时间

### 步骤 8: 输出文件

将生成的输入文件写入 `function.inp`:

```python
# 使用 write_to_file 工具
write_to_file(
    filePath="/path/to/function.inp",
    content=inp_content
)
```

## 参考资源

### 内部参考文档

在 `references/cp2k_input_reference.md` 中包含:

- 完整的 CP2K 输入文件结构说明
- 各个关键字的详细解释
- 不同计算类型的示例
- 参数选择指南
- 常见错误和解决方案

### 外部参考

当遇到复杂情况或特殊需求时,参考:

1. **CP2K 官方文档**: https://www.cp2k.org/
   - Input Reference: 详细的关键字说明
   - Howtos: 特定计算类型的教程

2. **用户工作区的示例文件**:
   - `/file/SP/`: 单点计算示例
   - `/file/opt/`: 几何优化示例
   - `/file/MD/`: 分子动力学示例
   - `/file/NEB/`: NEB 计算示例
   - `/file/DOS/`: 态密度示例
   - `/file/freq/`: 频率分析示例
   - `/file/QMMM/`: QMMM 计算示例

### 加载参考文档

在生成输入文件时,如果需要详细参考:

```python
read_file("references/cp2k_input_reference.md")
```

## 计算类型快速参考

| 计算类型 | RUN_TYPE | 主要用途 | 关键参数 |
|---------|----------|---------|---------|
| 单点能量 | ENERGY | 计算体系总能量 | CUTOFF, k-points |
| 能量+力 | ENERGY_FORCE | MD前准备 | 同上 |
| 几何优化 | GEO_OPT | 优化结构 | OPTIMIZER, 收敛判据 |
| 分子动力学 | MD | 模拟时间演化 | ENSEMBLE, TIMESTEP, STEPS |
| 频率分析 | FREQUENCY | 计算振动频率 | - |
| 能带结构 | BAND_STRUCTURE | 固体能带 | k点路径 |
| 态密度 | ENERGY + 特殊k点 | 电子态密度 | 高密度k点 |
| NEB | NEB | 反应路径 | NIMAGE, K_SPRING |
| QMMM | ENERGY/QMMM | 大体系精确计算 | QM/MM分区 |

## 常见问题处理

**问题 1: SCF 不收敛**
解决方案:
- 降低 EPS_SCF 到 1.0E-05
- 增加混合参数 ALPHA
- 使用不同的混合方法 (BROYDEN_MIXING → PULAY_MIXING)
- 增加网格精度 (提高 CUTOFF)

**问题 2: 计算太慢**
解决方案:
- 降低基组精度 (TZVP → DZVP)
- 减少k点数
- 使用 xTB 方法
- 使用 OT 方法代替 DIAGONALIZATION

**问题 3: 内存不足**
解决方案:
- 降低 CUTOFF
- 使用 DAVIDSON 对角化
- 减少k点数
- 使用 OT 方法

**问题 4: 结果不准确**
解决方案:
- 提高 CUTOFF
- 使用更高精度的基组
- 增加k点采样
- 使用更精确的泛函 (PBE → PBE0 → HSE06)

## 注意事项

1. **始终使用绝对路径** 当引用文件时
2. **保留原始文件** 不要直接修改用户的结构文件
3. **添加有意义的注释** 在输入文件中解释关键参数的选择
4. **提供多种选择** 当有多种可能方案时
5. **询问重要参数** 当不确定时,不要随意设置
6. **参考已有示例** 查看工作区中相似计算的输入文件

## 输出文件命名

默认输出文件名为 `function.inp`,但如果用户指定了项目名称,可以使用:

- `{project_name}.inp`
- `{calculation_type}.inp`
- `calc_{date}.inp`

始终确保输出文件在用户指定的位置。
