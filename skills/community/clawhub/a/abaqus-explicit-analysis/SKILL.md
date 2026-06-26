---
name: abaqus-explicit-analysis
description: Abaqus/Explicit 显式动力学分析专用技能。覆盖跌落、冲击、爆炸、成形等瞬态非线性问题。包含建模要点、材料/单元/接触设置、稳定性控制、能量平衡验证和常见坑点排查。
metadata:
  openclaw:
    emoji: 💥
  version: 1.1.0
  created: 2026-04-25
  updated: 2026-04-25
  domain: 有限元分析/显式动力学
tags:
  - explicit
  - impact
  - drop-test
  - nonlinear
---

# Abaqus/Explicit 显式动力学分析技能

> 官方文档: https://www.3ds.com/products/simulia/abaqus/explicit
> Abaqus/Explicit 是显式动力有限元求解器，适合模拟高速瞬态和高度非线性事件。

## 官方分析类型 (来自 3DS SIMULIA)
- **非线性动力应力分析** (Nonlinear Dynamic Stress Analysis)
- **声学分析** (Acoustics)
- **热/结构多物理场** (Thermal/Structural Multi-physics)
- **离散单元法 DEM** (Discrete Element Method，颗粒模拟)
- **耦合欧拉-拉格朗日 CEL** (Coupled Eulerian-Lagrangian)
- **光滑粒子流体动力学 SPH** (Smooth Particle Hydrodynamics)

## 官方材料模型 (来自 3DS SIMULIA)
- 线性弹性与粘弹性 (Linear Elasticity & Viscoelasticity)
- 非线性粘弹性 (Nonlinear Viscoelasticity)
- 各向同性与随动塑性 (Isotropic & Kinematic Plasticity)
- 损伤与断裂力学 (Damage & Fracture Mechanics)
- 低密度率相关泡沫 (Low-density, Rate-dependent Foam)
- 状态方程：非牛顿流体、理想气体 (Equation of States)

## 触发场景

- 跌落/冲击分析（drop test, impact）
- 爆炸/爆轰分析（blast, detonation）
- 金属成形/冲压（forming, stamping）
- 高速碰撞/穿甲（high-velocity impact, penetration）
- 任何涉及大变形、材料失效、强非线性的瞬态动力学问题
- 需要将 `.cae` / `.jnl` 转换为可重复运行的 Python 脚本

## 核心原则

1. **显式 = 时间驱动**：分析步时间是物理时间，不是伪时间。0.02s 就是真实世界中的 20ms。
2. **条件稳定**：时间步长由最小时步决定（CFL条件），网格越密步长越小，计算量越大。
3. **能量守恒是金标准**：总能（ETOTAL）应基本恒定，动能→内能的转换反映物理过程。
4. **接触是核心难点**：显式中接触处理决定结果可信度，无摩擦/有摩擦选择直接影响结果。

---

## 建模要点

### 1. 零件类型选择

| 场景 | 推荐单元 | 说明 |
|------|---------|------|
| 薄壁结构（厚度/特征尺寸 < 1/10） | `S4R` / `S3R` 壳单元 | 本案例类型，2mm板厚 vs 1m尺寸 |
| 实体结构 | `C3D8R` 六面体 / `C3D10M` 四面体 | 大变形推荐 C3D8R |
| 刚体部件 | 壳/实体 + `RigidBody` 约束 | 如本例中的地面 |
| 超弹性/橡胶 | `C3D8RH`（杂交） | 不可压缩材料必须杂交 |

**关键规则**：显式分析中，**避免使用二阶单元**（如 C3D20、S8R），一阶减缩积分单元（C3D8R、S4R）是首选。

### 2. 网格策略

```python
# 显式网格种子设置
part.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=0.02)
part.setMeshControls(elemShape=QUAD, technique=STRUCTURED)
part.generateMesh()

# 单元类型（显式库）
part.setElementType(
    elemTypes=(
        ElemType(elemCode=S4R, elemLibrary=EXPLICIT, hourglassControl=DEFAULT),
        ElemType(elemCode=S3R, elemLibrary=EXPLICIT)  # 自动三角过渡
    ),
    regions=...
)
```

**网格尺寸估算公式**：
```
稳定时间步长 dt ≈ L_min / c
其中: L_min = 最小单元特征长度
      c = sqrt(E/rho) = 材料波速（钢约 5000 m/s）
```
对钢材，0.02m 网格 ≈ 3μs 稳定步长，0.02s 分析需 ~7000 步。

### 3. 材料定义顺序

显式分析中材料定义**必须**包含密度，否则无法计算惯性力：

```python
mat = model.Material(name='DQSK36')
mat.Density(table=((7850.0, ), ))          # 必须先定义密度
mat.Elastic(table=((207e9, 0.28), ))        # 弹性模量 + 泊松比
mat.Plastic(table=(                          # 塑性数据
    (154.31e6, 0.0),   (221.76e6, 0.02),    # (屈服应力, 塑性应变)
    ...
))
```

**塑性数据注意**：
- 第一点必须是 `(屈服应力, 0.0)`
- 数据点越密集，硬化曲线越准确
- 最大塑性应变应覆盖预期变形范围

### 4. 壳截面设置

```python
model.HomogeneousShellSection(
    material='DQSK36', name='Section-1',
    thickness=0.002,       # 壳厚
    numIntPts=5,           # Simpson 积分点数（推荐5）
    integrationRule=SIMPSON
)
```

### 5. 刚体定义

将不需要变形的部件设为刚体可**大幅减少计算量**：

```python
# 先创建参考点
rp = assembly.instances['Part-Ground-1'].InterestingPoint(
    assembly.instances['Part-Ground-1'].edges[4], CENTER)
assembly.ReferencePoint(point=rp)

# 设为刚体
model.RigidBody(
    name='Rigid-Ground',
    bodyRegion=Region(faces=...),
    refPointRegion=Region(referencePoints=(refPoint, ))
)

# 约束参考点
model.EncastreBC(name='BC-1', createStepName='Initial',
    region=Region(referencePoints=(refPoint, )))
```

⚠️ **警告**：刚体部件**不会输出**积分点变量（应力、应变）。如果后处理需要看刚体的应力，不要设为刚体。

---

## 分析步设置

### ExplicitDynamicsStep

```python
model.ExplicitDynamicsStep(
    name='Step-1', previous='Initial',
    timePeriod=0.02,       # 物理时间（秒）
    maxIncrement=0.0005    # 最大增量步（可选）
)
```

**时间步选择**：
- 跌落分析：通常 5~50ms 足够
- 冲击分析：1~10ms
- 爆炸分析：1~100ms
- **预估原则**：观察对象运动特征时间 = 特征距离 / 特征速度

### 输出请求

```python
# 场输出（云图用）
model.fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=50,  # 输出帧数
    variables=('S', 'PE', 'PEEQ', 'LE', 'U', 'V', 'A', 'CFORCE', 'STH')
)

# 历史输出（曲线/能量用）
model.historyOutputRequests['H-Output-1'].setValues(
    variables=('ALLAE', 'ALLCD', 'ALLDC', 'ALLDMD', 'ALLFD', 'ALLIE',
               'ALLKE', 'ALLPD', 'ALLSE', 'ALLVD', 'ALLWK', 'ALLCW',
               'ALLMW', 'ALLPW', 'ETOTAL')
)
```

**关键字段说明**：

| 变量 | 含义 | 用途 |
|------|------|------|
| `S` | 应力 | 查看应力分布 |
| `PEEQ` | 等效塑性应变 | 判断永久变形程度 |
| `ALLKE` | 总动能 | 观察速度衰减 |
| `ALLIE` | 总内能 | 观察能量吸收 |
| `ALLAE` | 伪应变能 | **沙漏控制指标** |
| `ETOTAL` | 总能量 | **能量守恒验证** |
| `ALLFD` | 摩擦耗散能 | 有摩擦接触时检查 |
| `ALLVD` | 粘性耗散能 | 阻尼相关 |

---

## 接触设置（最重要部分）

### 通用接触（推荐）

```python
# 创建接触属性
model.ContactProperty('IntProp-1')
model.interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS  # 或 PENALTY + frictionCoefficient=0.2
)
# 可选法向行为
# model.interactionProperties['IntProp-1'].NormalBehavior(
#     pressureOverclosure=HARD, allowSeparation=ON,
#     constraintEnforcementMethod=DEFAULT
# )

# 创建通用接触
model.ContactExp(createStepName='Step-1', name='Int-1')
model.interactions['Int-1'].includedPairs.setValuesInStep(
    stepName='Step-1', useAllstar=ON)
model.interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1'
)
```

**摩擦系数参考**：

| 接触对 | 摩擦系数 |
|--------|---------|
| 钢-钢（干） | 0.3~0.6 |
| 钢-钢（润滑） | 0.05~0.15 |
| 钢-混凝土 | 0.4~0.7 |
| 钢-橡胶 | 0.5~1.0 |
| 自接触 | 0.1~0.3 |

### 接触初始化警告处理

运行时常遇到初始过闭合警告：

```
***WARNING: There are 68 initial node-face overclosures.
***WARNING: 36 secondary nodes are coincident with reference plane.
***WARNING: 546 surface intersections detected.
```

**处理策略**：
1. **微调初始位置**：将下落物体提高 0.1~0.5mm，确保无初始接触
2. **使用接触间隙**：在接触属性中添加 `*CONTACT CLEARANCE ASSIGNMENT`
3. **如果是物理接触**（如预紧状态）：忽略警告，Abaqus 会自动处理
4. **检查网格对齐**：接触区域网格尺寸匹配可减少警告

### 自接触

对于可能发生自折叠的结构（如薄板冲击后翻折），需启用自接触：

```python
model.ContactExp(createStepName='Step-1', name='SelfContact')
model.interactions['SelfContact'].includedPairs.setValuesInStep(
    stepName='Step-1', useAllstar=ON)
model.interactions['SelfContact'].contactPropertyAssignments.appendInStep(
    assignments=((SELF, SELF, 'IntProp-1'), ), stepName='Step-1'
)
```

---

## 加载与边界条件

### 初速度加载

显式分析中初速度是最常用的加载方式（模拟自由落体、冲击等）：

```python
model.Velocity(
    name='Velocity-Box',
    region=Region(
        faces=..., edges=..., vertices=...  # 必须指定整个部件
    ),
    velocity1=0.0, velocity2=-10.0, velocity3=0.0,  # Vx, Vy, Vz
    distributionType=MAGNITUDE
)
```

⚠️ **注意**：`Velocity` 载荷的 `region` 必须覆盖部件的**所有面、边、顶点**，否则未被覆盖的节点初速度为零，会导致内部应力波。

### 重力加载

```python
model.Gravity(createStepName='Step-1', name='Gravity',
    comp1=0.0, comp2=-9.81, comp3=0.0, distributionType=UNIFORM)
```

**初速度 vs 重力**：
- 如果只关心冲击瞬间效应，用初速度即可
- 如果需要模拟完整自由落体过程（含重力加速阶段），用重力+零初速
- 本例用初速度 -10m/s（等效约 5m 高度自由落体），更聚焦碰撞过程

---

## 作业设置

### CPU 和内存

```python
mdb.Job(
    name='Job-Explicit-Drop', model='Model-1',
    numCpus=4,               # 根据实际 CPU 核心数调整
    numDomains=4,            # 通常等于 numCpus
    parallelizationMethodExplicit=DOMAIN,
    explicitPrecision=SINGLE,    # 单精度（显式推荐）
    nodalOutputPrecision=SINGLE,
    multiprocessingMode=DEFAULT,
    memory=90, memoryUnits=PERCENTAGE
)
```

**关键决策**：
- `explicitPrecision=SINGLE`：显式分析用单精度足够，双精度会显著增加内存和时间
- `numCpus`：不要超过物理核心数，超线程不会提升显式计算性能
- 并行效率：显式分析并行效率较高（80~95%），4核 ≈ 3.5倍加速

### 提交与等待

```python
mdb.jobs['Job-Explicit-Drop'].submit(consistencyChecking=OFF)
mdb.jobs['Job-Explicit-Drop'].waitForCompletion()
```

---

## 结果验证清单

### ✅ 能量守恒检查

```python
# 在 Abaqus/CAE 中检查：
# Result -> History Output -> ETOTAL
# 曲线应该基本水平（允许 ±5% 波动）
```

**判断标准**：
- `ETOTAL` 变化 < 5%：结果可信
- `ETOTAL` 变化 5~10%：可接受，但需谨慎解读
- `ETOTAL` 变化 > 10%：结果不可信，需检查接触/网格

### ✅ 沙漏控制检查

```python
# ALLAE / ALLIE < 5%  优秀
# ALLAE / ALLIE < 10% 可接受
# ALLAE / ALLIE > 10% 需改进
```

如果沙漏能过高：
```python
# 修改单元类型，增加沙漏控制
ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT, hourglassControl=ENHANCED)
# 或使用 C3D8I（完全积分，无沙漏但计算量大）
```

### ✅ 接触穿透检查

在后处理中检查接触面是否有异常穿透（一个部件穿入另一个部件）。正常穿透量应 < 单元尺寸的 10%。

### ✅ 时间步稳定性

```
# 在 .sta 文件中检查 STABLE INCREMENT
# 如果稳定步长剧烈波动，可能意味着：
# 1. 单元畸变严重
# 2. 接触状态频繁变化
# 3. 材料软化导致波速降低
```

---

## 常见坑点与解决方案

### 坑 1：忘了定义密度

**现象**：分析不报错，但结果全为零或无意义
**原因**：显式分析基于 F=ma，没有密度就没有惯性力
**解决**：材料定义中必须包含 `Density`

### 坑 2：分析时间设置过长

**现象**：计算时间极长，结果末尾出现大量数值噪声
**原因**：显式是条件稳定的，分析时间越长，总步数越多
**解决**：只计算关心的物理时间段，用多个分析步分段

### 坑 3：初速度只加在了面上

**现象**：结果出现异常应力波，从内部向外扩散
**原因**：`Velocity` 载荷的 region 未覆盖所有节点
**解决**：region 必须包含 faces + edges + vertices

### 坑 4：接触属性忘记在分析步中激活

**现象**：部件直接穿过彼此，无接触力
**原因**：`ContactExp` 的 `createStepName` 与实际分析步不匹配
**解决**：确保接触在需要它的分析步开始时激活

### 坑 5：壳单元正反面搞反

**现象**：接触只在单侧生效，或应力分布异常
**原因**：壳单元的 SNEG/SPOS 面方向定义错误
**解决**：在 CAE 中 Display -> Part Display Options -> Show normals 检查法向

### 坑 6：网格尺寸不均匀导致极小时间步

**现象**：计算极慢，.sta 文件中时间步长异常小
**原因**：局部网格过密，成为限制步长的瓶颈
**解决**：统一网格尺寸，或用 `seedEdgeByNumber` 而非 `seedEdgeBySize`

### 坑 7：刚体定义后还想看应力

**现象**：后处理中刚体部件没有应力/应变云图
**原因**：刚体不参与变形计算，自然没有应力结果
**解决**：如果确实需要看应力，不要设为刚体；如果只是为了减少计算量但又要看结果，改用 `*RIGID BODY, PINNED` 只约束自由度

---

## Python 脚本模板

以下是标准的显式分析 Python 脚本结构：

```python
# -*- coding: mbcs -*-
"""Abaqus/Explicit Analysis Script Template"""
from abaqus import *
from abaqusConstants import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *

# 1. 创建模型
mdb.Model(name='Explicit-Model')
model = mdb.models['Explicit-Model']

# 2. 创建零件（几何/网格）
# ... Part creation and meshing ...

# 3. 定义材料
mat = model.Material(name='Material-1')
mat.Density(table=((rho, ), ))
mat.Elastic(table=((E, nu), ))
mat.Plastic(table=plastic_data)

# 4. 定义截面并分配
model.HomogeneousShellSection(material='Material-1', name='Section-1',
    thickness=t, numIntPts=5)

# 5. 装配
# ... Instance creation and positioning ...

# 6. 定义分析步
model.ExplicitDynamicsStep(name='Step-1', previous='Initial',
    timePeriod=time_period)

# 7. 输出请求
model.fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=num_frames, variables=('S', 'PEEQ', 'U', 'V'))
model.historyOutputRequests['H-Output-1'].setValues(
    variables=('ALLKE', 'ALLIE', 'ALLAE', 'ETOTAL'))

# 8. 接触
model.ContactProperty('IntProp-1')
model.interactionProperties['IntProp-1'].TangentialBehavior(formulation=FRICTIONLESS)
model.ContactExp(createStepName='Step-1', name='Int-1')
model.interactions['Int-1'].includedPairs.setValuesInStep(stepName='Step-1', useAllstar=ON)
model.interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1')

# 9. 边界条件与加载
# ... BC and loads ...

# 10. 作业提交
mdb.Job(name='Job-1', model='Explicit-Model', numCpus=num_cpus,
    numDomains=num_cpus, explicitPrecision=SINGLE,
    parallelizationMethodExplicit=DOMAIN)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1'].waitForCompletion()
```

---

## 后处理快速命令

```python
# 在 Abaqus/CAE 命令行或脚本中使用
from viewerModules import *

odb = session.openOdb(name='Job-1.odb')
vp = session.viewports['Viewport: 1']
vp.setValues(displayedObject=odb)

# Mises 应力
vp.odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=INTEGRATION_POINT,
    refinement=(INVARIANT, 'Mises'))
vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))

# 等效塑性应变
vp.odbDisplay.setPrimaryVariable(variableLabel='PEEQ', outputPosition=INTEGRATION_POINT)

# 能量历史曲线
xy1 = session.XYDataFromHistory(name='ALLKE', odb=odb,
    outputVariableName='Kinetic energy: ALLKE for Whole Model')
xy2 = session.XYDataFromHistory(name='ALLIE', odb=odb,
    outputVariableName='Internal energy: ALLIE for Whole Model')
xy3 = session.XYDataFromHistory(name='ETOTAL', odb=odb,
    outputVariableName='Total energy: ETOTAL for Whole Model')
session.XYPlot('Energy History')
session.curves['Energy History'].addData(xy1, xy2, xy3)

# 截图
session.printToFile(fileName='result', format=PNG,
    canvasObjects=(vp, ))
```

---

## 参考资源

- Abaqus Analysis User's Guide: "Explicit Dynamic Analysis"
- Abaqus Example Problems Manual: "Drop Test of a Package"
- 官方产品页面: https://www.3ds.com/products/simulia/abaqus/explicit
- 用户文档: https://abaqus.uclouvain.be/ (UCL镜像)
- 资源中心: https://www.3ds.com/products/simulia/resource-center
- LS-DYNA Keyword Manual（对比参考）
- 本案例参考模型：`Explicit-Drop.cae` / `Explicit-Drop-Script.py`
