# CP2K 输入文件生成完整参考

## 输入文件结构概览

CP2K 输入文件采用层级结构,由以下主要部分组成:

```
&GLOBAL
  项目设置,打印级别,运行类型
&END GLOBAL

&FORCE_EVAL
  METHOD [Quickstep/QMMM/MM/MIXED]
  &SUBSYS
    结构定义(CELL, COORD, KIND)
  &END SUBSYS
  
  &DFT (或 &MM)
    密度泛函设置或分子力学设置
  &END DFT
  
  &PRINT
    输出控制
  &END PRINT
&END FORCE_EVAL

&MOTION
  几何优化,MD,频率分析等
  &GEO_OPT (几何优化)
  &MD (分子动力学)
  &FREQUENCY (频率分析)
  &NEB (弹性带)
&END MOTION
```

## 运行类型 (RUN_TYPE)

在 `&GLOBAL` 中指定计算类型:

- **ENERGY**: 单点能量计算
- **ENERGY_FORCE**: 计算能量和力
- **GEO_OPT**: 几何优化
- **MD**: 分子动力学
- **FREQUENCY**: 频率分析/振动谱
- **VIBRATIONAL_ANALYSIS**: 振动分析
- **BAND_STRUCTURE**: 能带结构
- **ELECTRONIC_DENSITY**: 电子密度

## FORCE_EVAL 方法选择

### Quickstep (DFT)
适用于量子化学计算,支持GPW和GAPW方法

```
&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME POTENTIAL
    ...
  &END DFT
&END FORCE_EVAL
```

### QMMM
量子力学/分子力学混合方法

```
&FORCE_EVAL
  METHOD QMMM
  &QMMM
    E_COUPL &END
    &MM FORCEFIELD ...
  &END QMMM
&END FORCE_EVAL
```

### MM
纯分子力学计算

```
&FORCE_EVAL
  METHOD Classical
  &MM
    FORCEFIELD Charmm
    ...
  &END MM
&END FORCE_EVAL
```

## SUBSYS - 系统定义

### CELL (晶胞定义)

```
&CELL
  A      a_x  a_y  a_z
  B      b_x  b_y  b_z
  C      c_x  c_y  c_z
  PERIODIC [XYZ/X/Y/Z/NONE]
  SYMMETRY [T/F]
&END CELL
```

**PERIODIC 方向**:
- **XYZ**: 三维周期性(晶体)
- **XY**: 二维周期性(表面/平板)
- **X/Y/Z**: 一维周期性(纳米线)
- **NONE**: 孤立体系(分子/团簇)

### COORD (原子坐标)

```
&COORD
  Element  x  y  z
  Si       0.0 0.0 0.0
  O        1.0 1.0 1.0
&END COORD
```

也可以从文件读取:
```
&TOPOLOGY
  COORD_FILE_NAME structure.xyz
  COORDINATE [XYZ/CIF/PDB/GAUSSIAN]
&END TOPOLOGY
```

### KIND (原子类型定义)

```
&KIND Si
  ELEMENT Si
  BASIS_SET TZVP-MOLOPT-GTH-q4
  POTENTIAL GTH-PBE
  &POTENTIAL
    TYPE GTH-PBE
  &END
&END KIND
```

**常用基组**:
- **DZVP-MOLOPT-SR-GTH**: 双ζ价基组,适合大体系
- **TZVP-MOLOPT-GTH-q4**: 三ζ价基组,更高精度

**赝势类型**:
- **GTH-PBE**: PBE泛函GTH赝势
- **GTH-BLYP**: BLYP泛函GTH赝势

## DFT 设置

### 交换关联泛函

```
&XC
  &XC_FUNCTIONAL PBE
  &END XC_FUNCTIONAL
&END XC
```

**常用泛函**:
- **PBE**: GGA泛函,通用性好
- **BLYP**: GGA泛函
- **PADE**: LDA泛函
- **PBE0**: 杂化泛函
- **HSE06**: 杂化泛函

### MGRID (网格设置)

```
&MGRID
  CUTOFF 350          # 平面波截止能量(Rydberg)
  REL_CUTOFF 50       # 相对截止
  NGRIDS 5           # 多重网格层数
&END MGRID
```

**CUTOFF 建议**:
- 小体系: 300-400 Ry
- 中等体系: 400-500 Ry
- 大体系: 500-600 Ry

### KPOINTS (布里渊区采样)

```
&KPOINTS
  SCHEME MONKHORST-PACK  n_x  n_y  n_z
  SYMMETRY T  # 使用对称性减少k点
&END KPOINTS
```

**k点密度建议**:
- 金属: 较密 (如 6x6x6)
- 半导体: 中等 (如 4x4x4)
- 绝缘体: 较稀疏 (如 3x3x3)
- 大超胞: Γ点 (1x1x1)

### SCF (自洽场)

```
&SCF
  MAX_SCF 128           # 最大SCF步数
  EPS_SCF 5.0E-06       # 收敛判据
  
  &DIAGONALIZATION
    ALGORITHM [STANDARD/DAVIDSON]
  &END DIAGONALIZATION
  
  &MIXING
    METHOD BROYDEN_MIXING
    ALPHA 0.4
    NBROYDEN 8
  &END MIXING
&END SCF
```

**算法选择**:
- **STANDARD**: 标准对角化,精确但慢
- **DAVIDSON**: Davidson算法,适合大体系

**OT方法(轨道变换)**:
```
&SCF
  &OT
    PRECONDITIONER FULL_SINGLE_INVERSE
    MINIMIZER DIIS
    LINESEARCH 2PNT
  &END OT
  &OUTER_SCF
    MAX_SCF 20
    EPS_SCF 1.0E-06
  &END OUTER_SCF
&END SCF
```

## MOTION - 运动设置

### 几何优化 (GEO_OPT)

```
&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER [BFGS/CG/LBFGS]
    &BFGS
      TRUST_RADIUS 0.2  # 最大步长(Å)
    &END BFGS
    MAX_ITER 500
    MAX_DR 3E-3         # 最大位移
    RMS_DR 1.5E-3       # RMS位移
    MAX_FORCE 4.5E-4     # 最大力
    RMS_FORCE 3E-4       # RMS力
  &END GEO_OPT
&END MOTION
```

### 分子动力学 (MD)

```
&MOTION
  &MD
    ENSEMBLE [NVT/NVE/NPT]
    STEPS 50000
    TIMESTEP 0.2        # 时间步长(fs)
    TEMPERATURE 300     # 温度(K)
    
    &THERMOSTAT
      TYPE CSVR
      &CSVR
        TIMECON 100     # 时间常数(fs)
      &END CSVR
    &END THERMOSTAT
  &END MD
&END MOTION
```

**热浴类型**:
- **CSVR**: 随机速度重缩放
- **NOSE**: Nosé-Hoover
- **LANGEVIN**: Langevin动力学

### 频率分析 (FREQUENCY)

```
&MOTION
  &FREQUENCY
    &PRINT
      &EIGENVECTORS
        ADD_LAST NO
      &END EIGENVECTORS
    &END PRINT
  &END FREQUENCY
&END MOTION
```

### NEB (弹性带)

```
&MOTION
  &NEB
    NIMAGE 7            # 影像数量
    K_SPRING 0.5       # 弹簧常数
    TOL_FORCE 0.02     # 力收敛判据
  &END NEB
&END MOTION
```

## 特殊计算设置

### 自旋极化 (UKS)

```
&DFT
  CHARGE 0           # 净电荷
  MULTIPLICITY 2     # 自旋多重度
  UKS               # 非受限自旋
&END DFT
```

### smearing (费米涂抹)

```
&DFT
  &SMearing
    METHOD FERMI_DIRAC
    WIDTH 0.01       # 涂抹宽度(Hartree)
  &END SMearing
&END DFT
```

### 约束DFT (CDFT)

```
&DFT
  &CDFT
    &CHARGE
      ATOM_LIST 1 2 3
      CHARGE +0.5
    &END CHARGE
  &END CDFT
&END DFT
```

## 输出控制

### PRINT 选项

```
&GLOBAL
  PRINT_LEVEL [LOW/MEDIUM/HIGH/DEBUG]
&END GLOBAL

&FORCE_EVAL
  &PRINT
    &RESTART
      BACKUP_COPIES 3
    &END RESTART
  &END PRINT
&END FORCE_EVAL

&MOTION
  &PRINT
    &TRAJECTORY
      FORMAT [XYZ/POS/CP2K]
      &EACH
        MD 10
      &END EACH
    &END TRAJECTORY
  &END PRINT
&END MOTION
```

## xTB 方法

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

## 文件类型支持

### 输入结构文件格式
- **XYZ**: 简单坐标格式
- **CIF**: 晶体信息文件
- **PDB**: 蛋白质数据库格式
- **GAUSSIAN**: Gaussian输入格式

### 从CP2K输出恢复
```
&DFT
  WFN_RESTART_FILE_NAME project-RESTART.wfn
  SCF_GUESS RESTART
&END DFT
```

## 计算类型对应示例

### 1. 单点能量计算 (SP)
- RUN_TYPE: ENERGY
- 需要: CELL, COORD, KIND, DFT设置

### 2. 几何优化 (OPT)
- RUN_TYPE: GEO_OPT
- 需要: GEO_OPT设置,收敛判据

### 3. 分子动力学 (MD)
- RUN_TYPE: MD
- 需要: MD设置,系综,热浴,时间步长

### 4. 频率分析 (FREQ)
- RUN_TYPE: FREQUENCY
- 前提: 优化后的结构

### 5. NEB路径搜索 (NEB)
- RUN_TYPE: NEB
- 需要: 多个起始/终点结构

### 6. QMMM计算
- METHOD: QMMM
- 需要: QM区域和MM区域定义

### 7. 能带结构 (BAND)
- RUN_TYPE: BAND_STRUCTURE
- 需要: k点路径定义

### 8. 态密度 (DOS)
- 需要: 特殊k点采样,高密度k点

## 参数选择指南

### CUTOFF选择
| 体系大小 | 基组 | CUTOFF (Ry) |
|---------|------|-------------|
| 小分子(<50原子) | TZVP | 300-350 |
| 中等体系(50-200) | DZVP | 400-500 |
| 大体系(>200) | DZVP | 500-600 |

### K点选择
| 体系类型 | 超胞大小 | K点网格 |
|---------|---------|---------|
| 体相晶体 | 原胞 | 6x6x6 |
| 2x2x2超胞 | - | 3x3x3 |
| 3x3x3超胞 | - | 2x2x2 |
| 4x4x4超胞 | - | Γ点(1x1x1) |
| 表面模型 | - | 8x8x1 |

### 收敛判据
| 计算类型 | EPS_SCF | MAX_SCF |
|---------|---------|---------|
| 初步测试 | 1.0E-05 | 50 |
| 标准计算 | 5.0E-06 | 128 |
| 高精度 | 1.0E-07 | 200 |
| MD模拟 | 1.0E-05 | 25 |

## 常见错误和解决方案

1. **SCF不收敛**
   - 降低 EPS_SCF (放宽收敛判据)
   - 增加 MAX_SCF
   - 尝试不同的 MIXING 方法
   - 使用 SCF_GUESS RESTART

2. **能量震荡**
   - 减小 TIMESTEP (MD)
   - 调整热浴参数
   - 检查结构合理性

3. **内存不足**
   - 降低 CUTOFF
   - 使用 OT 方法
   - 减少k点数

4. **计算太慢**
   - 使用 xTB 方法
   - 降低基组精度
   - 减少k点数
   - 并行计算
