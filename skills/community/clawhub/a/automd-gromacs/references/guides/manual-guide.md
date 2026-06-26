# GROMACS 手册和源码使用指南

**目标:** 当 Skills 无法解决问题时，引导用户查阅官方手册和源码进行深度排查

---

## 一、何时需要查阅手册和源码

### 🔴 必须查阅的情况

1. **参数含义不清楚**
   - 不确定 MDP 参数的具体作用
   - 需要了解参数的默认值和取值范围
   - 想知道参数之间的相互影响

2. **遇到未知错误**
   - 错误信息不在 troubleshoot 文档中
   - 错误信息含糊不清
   - 需要了解错误的根本原因

3. **需要高级功能**
   - Skills 未覆盖的功能
   - 需要自定义工作流
   - 需要优化性能

4. **结果异常**
   - 计算结果与预期不符
   - 需要验证算法实现
   - 需要了解数值精度

### 🟡 建议查阅的情况

1. **优化参数设置**
   - 想了解最佳实践
   - 需要针对特定系统调优
   - 想提高计算效率

2. **学习原理**
   - 想深入理解算法
   - 需要引用文献
   - 准备发表论文

---

## 二、手册资源位置

### 本地手册

**位置:** `/root/.openclaw/workspace/gromacs-resources/`

```bash
# 手册分析报告 (结构化索引)
gromacs_manual_analysis.md

# 源码分析报告 (模块索引)
gromacs-source-analysis.md

# 完整手册 PDF (14 MB)
gromacs-2026.1/share/gromacs/manual/gromacs.pdf

# 源代码 (44 MB)
gromacs-2026.1/src/
```

### 在线手册

**官方文档:** https://manual.gromacs.org/2026.1/

**关键章节:**
- User Guide: https://manual.gromacs.org/2026.1/user-guide/index.html
- Reference Manual: https://manual.gromacs.org/2026.1/reference-manual/index.html
- How-To Guides: https://manual.gromacs.org/2026.1/how-to/index.html

---

## 三、快速查找方法

### 方法 1: 使用结构化分析报告

**步骤:**

1. **打开手册分析报告**
```bash
cat /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md
```

2. **查找相关章节**
```bash
# 搜索关键词
grep -i "umbrella" gromacs_manual_analysis.md
grep -i "free energy" gromacs_manual_analysis.md
grep -i "pull code" gromacs_manual_analysis.md
```

3. **定位到具体章节**
```
找到: Chapter 5.8 - Free Energy Calculations
      Section 5.8.3 - Umbrella Sampling
```

4. **查阅完整手册**
```bash
# 打开 PDF 手册,跳转到对应章节
evince gromacs-2026.1/share/gromacs/manual/gromacs.pdf
# 或在线查看
firefox https://manual.gromacs.org/2026.1/reference-manual/special/free-energy-calculations.html
```

### 方法 2: 搜索 MDP 参数

**步骤:**

1. **查找参数定义**
```bash
# 在手册中搜索参数
grep -r "pull_coord1_k" gromacs-2026.1/share/gromacs/manual/
```

2. **查看参数说明**
```
手册位置: Chapter 3.7 - Molecular Dynamics Parameters
在线查看: https://manual.gromacs.org/2026.1/user-guide/mdp-options.html
```

3. **查找示例**
```bash
# 在源码测试用例中查找
find gromacs-2026.1/src -name "*.mdp" | xargs grep "pull_coord1_k"
```

### 方法 3: 查找错误信息

**步骤:**

1. **复制完整错误信息**
```
例如: "Fatal error: Distance between pull groups 1 and 2 (5.234 nm) is larger than 0.49 times the box size"
```

2. **在源码中搜索**
```bash
cd gromacs-2026.1/src
grep -r "is larger than 0.49 times the box size" .
```

3. **找到源文件**
```
找到: src/gromacs/pulling/pull.cpp:234
```

4. **查看代码逻辑**
```bash
# 查看错误产生的条件
vim +234 src/gromacs/pulling/pull.cpp
```

5. **理解错误原因**
```cpp
// 代码显示: 拉力距离不能超过盒子尺寸的 49%
if (distance > 0.49 * box_size) {
    gmx_fatal("Distance between pull groups...");
}
```

### 方法 4: 查找算法实现

**步骤:**

1. **确定功能模块**
```bash
# 查看源码分析报告
cat gromacs-source-analysis.md | grep -A 10 "伞状采样"
```

2. **定位源文件**
```
找到: src/gromacs/pulling/
      src/gromacs/pulling/pull.cpp
      src/gromacs/pulling/pullutil.cpp
```

3. **查看实现细节**
```bash
# 查看伞状势的计算
vim src/gromacs/pulling/pull.cpp
# 搜索 "umbrella" 或 "harmonic"
```

4. **理解算法**
```cpp
// 伞状势公式: V = 0.5 * k * (r - r0)^2
force = -k * (distance - reference_distance);
```

---

## 四、典型问题的查找路径

### 问题 1: 不理解 sc-alpha 参数

**查找路径:**

1. **查看手册分析报告**
```bash
grep -i "sc-alpha" gromacs_manual_analysis.md
```

2. **定位章节**
```
找到: Chapter 5.8.4 - Soft-core Interactions
```

3. **查阅完整说明**
```bash
# 在线查看
firefox https://manual.gromacs.org/2026.1/reference-manual/special/free-energy-calculations.html#soft-core-interactions
```

4. **查看公式**
```
手册中的软核势公式:
V_soft = V_LJ * (α * λ^p * σ^6 + r^6)^(-1)
```

5. **查找推荐值**
```
手册建议:
- sc-alpha: 0.3-0.7 (典型值 0.5)
- sc-power: 1 或 2
- sc-sigma: 0.3 nm
```

### 问题 2: LINCS 警告

**查找路径:**

1. **搜索错误信息**
```bash
cd gromacs-2026.1/src
grep -r "LINCS WARNING" .
```

2. **找到源文件**
```
找到: src/gromacs/mdlib/lincs.cpp
```

3. **查看警告条件**
```cpp
if (bond_deviation > lincs_warnangle) {
    fprintf(stderr, "LINCS WARNING: bond %d rotated more than %g degrees\n", ...);
}
```

4. **查阅手册说明**
```
手册位置: Chapter 5.4.3 - Constraint Algorithms
在线: https://manual.gromacs.org/2026.1/reference-manual/algorithms/constraint-algorithms.html
```

5. **理解原因和解决方案**
```
原因: 约束键旋转角度过大,通常由于:
- 时间步长太大
- 初始结构不稳定
- 温度/压力耦合参数不当

解决方案:
- 减小 dt (0.002 → 0.001)
- 更严格的能量最小化
- 使用 constraints = all-bonds
```

### 问题 3: PMF 计算结果异常

**查找路径:**

1. **查阅理论章节**
```
手册位置: Chapter 5.8 - Free Energy Calculations
          Chapter 5.12 - Averages and Fluctuations
```

2. **查看 WHAM 算法**
```bash
# 查看 gmx wham 源码
vim gromacs-2026.1/src/gromacs/gmxana/gmx_wham.cpp
```

3. **理解误差来源**
```
手册说明:
- 统计误差: 采样不足
- 系统误差: 窗口覆盖不足
- 数值误差: 迭代不收敛
```

4. **查找最佳实践**
```
手册建议:
- 窗口重叠 > 30%
- 每窗口采样 > 5 ns
- Bootstrap 误差估计
```

### 问题 4: 自定义力场参数

**查找路径:**

1. **查阅力场章节**
```
手册位置: Chapter 5.5 - Interaction Functions and Force Fields
          Chapter 5.6 - Topology File Format
```

2. **查看力场文件格式**
```bash
# 查看示例力场
cat gromacs-2026.1/share/gromacs/top/amber99sb-ildn.ff/forcefield.itp
```

3. **查看参数定义**
```
[ atomtypes ]
; name  at.num   mass     charge  ptype  sigma      epsilon
  C      6      12.01000  0.0000  A      0.33996695 0.35982400
```

4. **查阅参数化指南**
```
手册位置: Chapter 4 - How-To Guides
          Section: Parameterization of New Molecules
在线: https://manual.gromacs.org/2026.1/how-to/topology.html
```

---

## 五、源码深度排查

### 何时需要查看源码

1. **手册说明不够详细**
2. **需要了解具体实现**
3. **怀疑存在 bug**
4. **需要修改或扩展功能**

### 源码结构

```
gromacs-2026.1/src/gromacs/
├── pulling/          # 拉力和伞状采样
├── mdlib/            # MD 核心算法
├── gmxana/           # 分析工具
├── gmxpreprocess/    # 预处理工具
├── listed_forces/    # 键合相互作用
├── ewald/            # 长程静电
├── freeenergy/       # 自由能计算
└── ...
```

### 查看源码的方法

**方法 1: 直接查看**
```bash
cd gromacs-2026.1/src/gromacs/pulling
vim pull.cpp
```

**方法 2: 搜索关键词**
```bash
cd gromacs-2026.1/src
grep -r "umbrella" . --include="*.cpp" --include="*.h"
```

**方法 3: 查看函数调用**
```bash
# 使用 cscope 或 ctags
cscope -R
# 或
ctags -R
vim -t function_name
```

### 理解代码的技巧

1. **从错误信息入手**
   - 搜索错误字符串
   - 找到 gmx_fatal() 或 gmx_error() 调用
   - 理解触发条件

2. **查看注释**
   - GROMACS 代码注释详细
   - 通常包含公式和参考文献

3. **查看测试用例**
   - `src/gromacs/*/tests/` 目录
   - 包含各种使用场景

4. **查看文档字符串**
   - Doxygen 格式的注释
   - 说明函数功能和参数

---

## 六、实战案例

### 案例 1: 理解 pull_coord1_k 的单位

**问题:** 不确定力常数的单位是什么

**查找过程:**

1. **查看手册**
```bash
grep -i "pull_coord1_k" gromacs_manual_analysis.md
```

2. **找到说明**
```
手册: Chapter 3.7 - MDP Options
参数: pull-coord1-k
单位: kJ mol^-1 nm^-2 (对于 umbrella 类型)
```

3. **验证源码**
```bash
cd gromacs-2026.1/src/gromacs/pulling
grep -n "pull_coord1_k" pull.cpp
```

4. **查看代码**
```cpp
// Line 456
real k = pull->coord[c].k;  // kJ/(mol*nm^2)
real force = -k * (distance - reference);  // kJ/(mol*nm)
```

5. **结论**
```
确认单位: kJ/(mol·nm²)
典型值: 1000-3000 kJ/(mol·nm²)
```

### 案例 2: 排查 WHAM 收敛问题

**问题:** WHAM 分析不收敛

**查找过程:**

1. **查看错误信息**
```
gmx wham: WARNING: WHAM did not converge after 10000 iterations
```

2. **查阅手册**
```
手册: Chapter 5.8.3 - WHAM Analysis
说明: 默认迭代 10000 次,容差 1e-6
```

3. **查看源码**
```bash
vim gromacs-2026.1/src/gromacs/gmxana/gmx_wham.cpp
# 搜索 "converge"
```

4. **找到收敛判据**
```cpp
// Line 1234
if (fabs(delta_F) < tolerance) {
    converged = TRUE;
}
```

5. **理解原因**
```
原因: 窗口重叠不足,导致自由能差异过大
解决: 增加窗口数量或延长采样时间
```

6. **调整参数**
```bash
# 增加迭代次数和放宽容差
gmx wham -it tpr_files.dat -if pullf_files.dat -o pmf.xvg -nBootstrap 20000 -tol 1e-5
```

---

## 七、建立个人知识库

### 记录查找过程

**创建笔记文件:**
```bash
mkdir -p ~/gromacs_notes
vim ~/gromacs_notes/umbrella_sampling.md
```

**记录内容:**
```markdown
# 伞状采样笔记

## 参数设置
- pull_coord1_k: 1000-3000 kJ/(mol·nm²)
  - 手册: Chapter 5.8.3
  - 源码: src/gromacs/pulling/pull.cpp:456

## 常见问题
- LINCS 警告: 减小 dt 到 0.001
  - 手册: Chapter 5.4.3
  - 解决日期: 2026-04-07

## 参考文献
- Kumar et al. (1992) J. Comput. Chem. 13, 1011
```

### 建立快速索引

**创建索引文件:**
```bash
vim ~/gromacs_notes/INDEX.md
```

**内容:**
```markdown
# GROMACS 快速索引

## 自由能计算
- 理论: 手册 5.8
- 软核: 手册 5.8.4
- WHAM: 手册 5.8.3
- 源码: src/gromacs/freeenergy/

## 拉力代码
- 参数: 手册 3.7
- 算法: 手册 5.8.2
- 源码: src/gromacs/pulling/

## 常见错误
- LINCS: 手册 5.4.3, 源码 src/gromacs/mdlib/lincs.cpp
- 盒子尺寸: 源码 src/gromacs/pulling/pull.cpp:234
```

---

## 八、获取帮助

### 官方资源

1. **GROMACS 论坛**
   - https://gromacs.bioexcel.eu/
   - 搜索已有问题
   - 发布新问题

2. **邮件列表**
   - gmx-users@gromacs.org
   - 订阅: https://mailman-1.sys.kth.se/mailman/listinfo/gromacs.org_gmx-users

3. **GitHub Issues**
   - https://github.com/gromacs/gromacs/issues
   - 报告 bug
   - 功能请求

### 提问技巧

**好的问题包含:**
1. GROMACS 版本
2. 完整的错误信息
3. 相关的 MDP 文件
4. 已尝试的解决方案
5. 手册章节引用

**示例:**
```
标题: WHAM 分析不收敛 (GROMACS 2026.1)

描述:
我在进行伞状采样的 WHAM 分析时遇到收敛问题。

环境:
- GROMACS 2026.1
- 21 个窗口,间距 0.1 nm
- 每窗口采样 5 ns

错误信息:
WARNING: WHAM did not converge after 10000 iterations

已尝试:
- 增加迭代次数到 20000 (-nBootstrap 20000)
- 放宽容差到 1e-5 (-tol 1e-5)
- 查阅手册 Chapter 5.8.3

附件:
- pull.mdp
- umbrella.mdp
- hist.xvg

请问可能是什么原因?
```

---

## 九、总结

### 查找流程图

```
遇到问题
    ↓
查看 troubleshoot 文档
    ↓
问题未解决?
    ↓
查看手册分析报告 (gromacs_manual_analysis.md)
    ↓
定位相关章节
    ↓
查阅完整手册 (PDF 或在线)
    ↓
仍未解决?
    ↓
查看源码 (src/gromacs/)
    ↓
理解实现细节
    ↓
仍未解决?
    ↓
搜索论坛/邮件列表
    ↓
发布问题 (附上详细信息)
```

### 关键原则

1. **先查文档,再看代码**
2. **记录查找过程**
3. **建立个人索引**
4. **善用搜索工具**
5. **理解原理,不只是解决问题**

---

**最后更新:** 2026-04-07
**维护者:** GROMACS Skills 2.0 项目
