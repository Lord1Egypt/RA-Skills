# -*- coding: mbcs -*-
#
# Abaqus/CAE Python Script - Explicit Drop Simulation
# Equivalent to: Explicit-Drop.cae / Explicit-Drop.jnl
# Description: 开口方盒以10m/s速度跌落至带半圆形凹坑的刚性地面
#
# 运行方式: abaqus cae noGUI=Explicit-Drop-Script.py
#

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
import sketch

# ============================================================
# 0. 创建模型
# ============================================================
mdb.Model(name='Model-1')
model = mdb.models['Model-1']

# ============================================================
# 1. 创建 Part-Box（开口方盒壳体）
# ============================================================
# 创建矩形草图 (1.0m x 0.8m)
s = model.ConstrainedSketch(name='__profile__', sheetSize=4.0)
s.rectangle(point1=(0.0, 0.0), point2=(1.0, 0.8))

# 创建三维可变形壳体零件，拉伸深度0.6m
model.Part(dimensionality=THREE_D, name='Part-Box', type=DEFORMABLE_BODY)
model.parts['Part-Box'].BaseSolidExtrude(depth=0.6, sketch=s)
del model.sketches['__profile__']

# 删除实体使其成为壳体（移除cell和特定face）
model.parts['Part-Box'].RemoveCells(
    cellList=model.parts['Part-Box'].cells.getSequenceFromMask(mask=('[#1 ]', )))
model.parts['Part-Box'].RemoveFaces(
    deleteCells=False,
    faceList=model.parts['Part-Box'].faces.getSequenceFromMask(mask=('[#2 ]', )))

# ============================================================
# 2. 创建 Part-Ground（带半圆形凹坑的地面壳体）
# ============================================================
# 创建草图：1.6m长的线段 + 半径0.3m的半圆（中心在0.8, 0），然后trim掉多余部分
s = model.ConstrainedSketch(name='__profile__', sheetSize=4.0)
s.Line(point1=(0.0, 0.0), point2=(1.6, 0.0))
s.HorizontalConstraint(entity=s.geometry[2])
s.CircleByCenterPerimeter(center=(0.8, 0.0), point1=(0.8, 0.3))
# Trim曲线形成半圆形凹坑轮廓
s.autoTrimCurve(curve1=s.geometry[3], point1=(0.785, -0.037))
s.autoTrimCurve(curve1=s.geometry[2], point1=(0.785, -0.003))

# 创建三维壳体零件，拉伸深度1.0m
model.Part(dimensionality=THREE_D, name='Part-Ground', type=DEFORMABLE_BODY)
model.parts['Part-Ground'].BaseShellExtrude(depth=1.0, sketch=s)
del model.sketches['__profile__']

# ============================================================
# 3. 定义材料 DQSK36（低碳钢）
# ============================================================
model.Material(name='DQSK36')
model.materials['DQSK36'].Density(table=((7850.0, ), ))
model.materials['DQSK36'].Elastic(table=((207000000000.0, 0.28), ))
# 塑性数据：(屈服应力, 塑性应变)
model.materials['DQSK36'].Plastic(table=(
    (154310000.0, 0.0),   (221760000.0, 0.02), (253850000.0, 0.04),
    (276330000.0, 0.06),  (294000000.0, 0.08), (308720000.0, 0.1),
    (321430000.0, 0.12),  (332660000.0, 0.14), (342770000.0, 0.16),
    (351970000.0, 0.18),  (360440000.0, 0.2),  (368300000.0, 0.22),
    (375640000.0, 0.24),  (382530000.0, 0.26), (389040000.0, 0.28),
    (395200000.0, 0.3),   (401060000.0, 0.32), (406650000.0, 0.34),
    (412000000.0, 0.36),  (417130000.0, 0.38), (422050000.0, 0.4),
    (426790000.0, 0.42),  (431370000.0, 0.44), (435790000.0, 0.46),
    (440060000.0, 0.48),  (444210000.0, 0.5)
))

# ============================================================
# 4. 定义壳截面（厚度2mm）
# ============================================================
model.HomogeneousShellSection(
    material='DQSK36', name='Section-1',
    thickness=0.002, numIntPts=5,
    integrationRule=SIMPSON
)

# 截面分配
model.parts['Part-Ground'].SectionAssignment(
    region=Region(faces=model.parts['Part-Ground'].faces.getSequenceFromMask(mask=('[#7 ]', ))),
    sectionName='Section-1', thicknessAssignment=FROM_SECTION
)
model.parts['Part-Box'].SectionAssignment(
    region=Region(faces=model.parts['Part-Box'].faces.getSequenceFromMask(mask=('[#1f ]', ))),
    sectionName='Section-1', thicknessAssignment=FROM_SECTION
)

# ============================================================
# 5. 网格划分
# ============================================================
# Part-Box 网格：种子尺寸0.02m，四边形结构化网格
model.parts['Part-Box'].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=0.02)
model.parts['Part-Box'].setMeshControls(
    elemShape=QUAD,
    regions=model.parts['Part-Box'].faces.getSequenceFromMask(mask=('[#1f ]', )),
    technique=STRUCTURED
)
model.parts['Part-Box'].generateMesh()
model.parts['Part-Box'].setElementType(
    elemTypes=(
        ElemType(elemCode=S4R, elemLibrary=EXPLICIT, hourglassControl=DEFAULT),
        ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
    ),
    regions=(model.parts['Part-Box'].faces.getSequenceFromMask(mask=('[#1f ]', )), )
)

# Part-Ground 网格：边缘种子+四边形结构化网格
model.parts['Part-Ground'].seedEdgeByNumber(
    constraint=FINER,
    edges=model.parts['Part-Ground'].edges.getSequenceFromMask(mask=('[#1d0 ]', )),
    number=10
)
model.parts['Part-Ground'].seedEdgeBySize(
    constraint=FINER, deviationFactor=0.1,
    edges=model.parts['Part-Ground'].edges.getSequenceFromMask(mask=('[#e2f ]', )),
    size=0.1
)
model.parts['Part-Ground'].setMeshControls(
    elemShape=QUAD,
    regions=model.parts['Part-Ground'].faces.getSequenceFromMask(mask=('[#7 ]', )),
    technique=STRUCTURED
)
model.parts['Part-Ground'].generateMesh()
model.parts['Part-Ground'].setElementType(
    elemTypes=(
        ElemType(elemCode=S4R, elemLibrary=EXPLICIT, hourglassControl=DEFAULT),
        ElemType(elemCode=S3R, elemLibrary=EXPLICIT)
    ),
    regions=(model.parts['Part-Ground'].faces.getSequenceFromMask(mask=('[#7 ]', )), )
)

# ============================================================
# 6. 装配
# ============================================================
model.rootAssembly.DatumCsysByDefault(CARTESIAN)
model.rootAssembly.Instance(dependent=ON, name='Part-Box-1', part=model.parts['Part-Box'])
model.rootAssembly.Instance(dependent=ON, name='Part-Ground-1', part=model.parts['Part-Ground'])

# 将盒子平移到初始位置（高度0.2m）
model.rootAssembly.translate(instanceList=('Part-Box-1', ), vector=(0.3, 0.055, 0.2))

# ============================================================
# 7. 定义显式动力学分析步
# ============================================================
model.ExplicitDynamicsStep(
    name='Step-1', previous='Initial',
    timePeriod=0.02, maxIncrement=0.0005
)

# 场输出请求（50个输出间隔）
model.fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=50,
    variables=('S', 'PE', 'PEEQ', 'LE', 'U', 'V', 'A', 'CFORCE', 'STH')
)

# 历史输出请求（能量平衡等）
model.historyOutputRequests['H-Output-1'].setValues(
    variables=('ALLAE', 'ALLCD', 'ALLDC', 'ALLDMD', 'ALLFD', 'ALLIE',
               'ALLKE', 'ALLPD', 'ALLSE', 'ALLVD', 'ALLWK', 'ALLCW',
               'ALLMW', 'ALLPW', 'ETOTAL')
)

# ============================================================
# 8. 定义刚性地面的参考点和刚体约束
# ============================================================
# 创建参考点（地面边缘中心）
rp = model.rootAssembly.instances['Part-Ground-1'].InterestingPoint(
    model.rootAssembly.instances['Part-Ground-1'].edges[4], CENTER)
model.rootAssembly.ReferencePoint(point=rp)

# 将地面定义为刚体
model.RigidBody(
    name='Rigid-Ground',
    bodyRegion=Region(
        faces=model.rootAssembly.instances['Part-Ground-1'].faces.getSequenceFromMask(mask=('[#7 ]', ))
    ),
    refPointRegion=Region(referencePoints=(model.rootAssembly.referencePoints[6], ))
)

# ============================================================
# 9. 边界条件和载荷
# ============================================================
# 地面全约束（固定）
model.EncastreBC(
    name='BC-1', createStepName='Initial',
    region=Region(referencePoints=(model.rootAssembly.referencePoints[6], ))
)

# 盒子初始速度：Y方向 -10 m/s（向下）
model.Velocity(
    name='Velocity-Box',
    region=Region(
        faces=model.rootAssembly.instances['Part-Box-1'].faces.getSequenceFromMask(mask=('[#1f ]', )),
        edges=model.rootAssembly.instances['Part-Box-1'].edges.getSequenceFromMask(mask=('[#35d ]', )),
        vertices=model.rootAssembly.instances['Part-Box-1'].vertices.getSequenceFromMask(mask=('[#9 ]', ))
    ),
    velocity1=0.0, velocity2=-10.0, velocity3=0.0,
    distributionType=MAGNITUDE
)

# ============================================================
# 10. 接触定义
# ============================================================
# 创建接触属性：无摩擦
model.ContactProperty('IntProp-1')
model.interactionProperties['IntProp-1'].TangentialBehavior(formulation=FRICTIONLESS)

# 创建通用接触
model.ContactExp(createStepName='Step-1', name='Int-1')
model.interactions['Int-1'].includedPairs.setValuesInStep(stepName='Step-1', useAllstar=ON)
model.interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1'
)

# ============================================================
# 11. 创建并提交作业
# ============================================================
mdb.Job(
    name='Job-Explicit-Drop', model='Model-1',
    numCpus=4, numDomains=4,
    parallelizationMethodExplicit=DOMAIN,
    explicitPrecision=SINGLE,
    nodalOutputPrecision=SINGLE,
    multiprocessingMode=DEFAULT,
    activateLoadBalancing=False,
    memory=90, memoryUnits=PERCENTAGE
)

# 提交作业
mdb.jobs['Job-Explicit-Drop'].submit(consistencyChecking=OFF)
mdb.jobs['Job-Explicit-Drop'].waitForCompletion()

print('Job-Explicit-Drop submitted successfully.')
