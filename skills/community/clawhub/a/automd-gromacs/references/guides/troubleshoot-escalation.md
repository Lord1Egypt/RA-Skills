# 故障排查升级机制

**目标:** 当 Skills 无法解决问题时，自动引导用户查阅手册和源码

---

## 机制设计

### 三级故障排查体系

```
Level 1: Skills 内置解决方案
    ↓ (未解决)
Level 2: 手册章节引用
    ↓ (未解决)
Level 3: 源码深度排查
```

---

## Level 1: Skills 内置解决方案

**覆盖范围:** 80% 的常见问题

**特点:**
- 快速诊断
- 直接给出解决方案
- 包含可执行命令

**示例:**
```bash
ERROR-001: GROMACS 未安装

解决方案:
source /usr/local/gromacs/bin/GMXRC
```

---

## Level 2: 手册章节引用

**触发条件:**
- Level 1 方案无效
- 需要理解参数含义
- 需要调整高级参数

**引导方式:**

### 方式 1: 直接章节链接

在错误信息中添加:

```bash
ERROR-007: 自由能误差过大

当前误差: ± 2.3 kJ/mol (± 0.55 kcal/mol)
建议阈值: < 1.0 kcal/mol

📖 深入了解:
   手册章节: Chapter 5.8.3 - BAR Method
   本地路径: /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md
   在线链接: https://manual.gromacs.org/2026.1/reference-manual/special/free-energy-calculations.html#bar

   关键内容:
   - 误差来源分析
   - 采样时间建议
   - λ 分布优化
   - Bootstrap 误差估计

🔍 快速查找:
   grep -A 20 "BAR Method" /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md
```

### 方式 2: 参数说明引用

```bash
ERROR-005: λ 窗口模拟崩溃

可能原因: 软核参数不当

当前设置:
  sc-alpha = 0.5
  sc-power = 1
  sc-sigma = 0.3

📖 参数详解:
   手册章节: Chapter 5.8.4 - Soft-core Interactions
   参数说明: https://manual.gromacs.org/2026.1/user-guide/mdp-options.html#free-energy-calculations

   软核势公式:
   V_soft = V_LJ * (α * λ^p * σ^6 + r^6)^(-1)

   推荐值范围:
   - sc-alpha: 0.3-0.7 (控制软核强度)
   - sc-power: 1 或 2 (控制 λ 依赖性)
   - sc-sigma: 0.25-0.35 nm (控制软核半径)

🔍 查看完整说明:
   cat /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md | grep -A 50 "Soft-core"
```

### 方式 3: 最佳实践引用

```bash
ERROR-008: dH/dλ 重叠不足

当前重叠: < 0.03 (窗口 5-6)
建议重叠: > 0.03

📖 最佳实践:
   手册章节: Chapter 5.8 - Free Energy Calculations
   论文参考: Klimovich et al. (2015) J. Comput. Aided Mol. Des. 29, 397

   推荐设置:
   - 窗口间距: 0.05-0.1 nm
   - 窗口重叠: 30-50%
   - 采样时间: 5-10 ns/窗口
   - λ 分布: 端点密集

🔍 查看详细建议:
   手册位置: Section 5.8.5 - Best Practices
   本地查找: grep -A 30 "Best Practices" gromacs_manual_analysis.md
```

---

## Level 3: 源码深度排查

**触发条件:**
- Level 2 仍无法解决
- 需要理解算法实现
- 怀疑存在 bug
- 需要自定义功能

**引导方式:**

### 方式 1: 错误源码定位

```bash
ERROR-002: 拉力模拟失败

错误信息:
Fatal error:
Distance between pull groups 1 and 2 (5.234 nm) is larger than 0.49 times the box size (10.0 nm)

📖 手册说明:
   Chapter 5.8.2 - Pull Code
   限制原因: 避免 PBC 问题

💻 源码定位:
   文件: src/gromacs/pulling/pull.cpp
   行号: 234
   函数: check_pull_coords()

   查看方法:
   cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src/gromacs/pulling
   vim +234 pull.cpp

   关键代码:
   ```cpp
   if (distance > 0.49 * box_size) {
       gmx_fatal("Distance between pull groups %d and %d (%.3f nm) "
                 "is larger than 0.49 times the box size (%.1f nm)",
                 pull->coord[c].group[0], pull->coord[c].group[1],
                 distance, box_size);
   }
   ```

   理解:
   - 0.49 是硬编码的安全系数
   - 防止拉力组通过 PBC 相互作用
   - 解决方案: 增大盒子或减小拉力距离

🔍 搜索相关代码:
   cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src
   grep -rn "0.49 times the box size" .
```

### 方式 2: 算法实现查看

```bash
ERROR-006: WHAM 分析失败

问题: 不理解 WHAM 的收敛判据

📖 手册说明:
   Chapter 5.8.3 - WHAM Analysis
   算法: 加权直方图分析方法

💻 源码实现:
   文件: src/gromacs/gmxana/gmx_wham.cpp
   函数: do_wham()

   查看方法:
   cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src/gromacs/gmxana
   vim gmx_wham.cpp
   # 搜索 "/converge"

   关键代码:
   ```cpp
   // Line 1234
   for (iter = 0; iter < max_iterations; iter++) {
       // 计算自由能
       calc_free_energy(pmf, hist, ...);
       
       // 检查收敛
       delta_F = fabs(pmf[i] - pmf_old[i]);
       if (delta_F < tolerance) {
           converged = TRUE;
           break;
       }
   }
   ```

   理解:
   - 迭代计算 PMF
   - 收敛判据: |ΔF| < tolerance
   - 默认: tolerance = 1e-6, max_iterations = 10000

🔍 查看完整算法:
   vim +1200 gmx_wham.cpp
   # 阅读 do_wham() 函数
```

### 方式 3: 参数默认值查找

```bash
问题: 不确定 pull_coord1_k 的默认值

📖 手册说明:
   Chapter 3.7 - MDP Options
   说明: 未明确给出默认值

💻 源码查找:
   文件: src/gromacs/pulling/pull.cpp
   函数: init_pull_coord()

   查看方法:
   cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src/gromacs/pulling
   grep -n "pull_coord.*k" pull.cpp

   关键代码:
   ```cpp
   // Line 567
   pull->coord[c].k = 0.0;  // 默认值
   
   // Line 890
   if (pull->coord[c].eType == epullUMBRELLA) {
       if (pull->coord[c].k == 0.0) {
           gmx_fatal("pull-coord%d-k must be set for umbrella pulling", c+1);
       }
   }
   ```

   理解:
   - 默认值为 0.0
   - 对于 umbrella 类型,必须显式设置
   - 典型值: 1000-3000 kJ/(mol·nm²)

🔍 查找所有默认值:
   grep -n "pull->coord.*=" pull.cpp | grep "0.0\|NULL\|FALSE"
```

---

## 自动化引导脚本

### 脚本 1: 错误信息解析器

```bash
#!/bin/bash
# 文件: scripts/utils/error_parser.sh
# 功能: 解析 GROMACS 错误信息并提供手册引用

ERROR_MSG="$1"

# 提取关键词
if [[ "$ERROR_MSG" =~ "LINCS" ]]; then
    echo "📖 相关手册:"
    echo "   Chapter 5.4.3 - Constraint Algorithms"
    echo "   https://manual.gromacs.org/2026.1/reference-manual/algorithms/constraint-algorithms.html"
    echo ""
    echo "💻 源码位置:"
    echo "   src/gromacs/mdlib/lincs.cpp"
    echo ""
    echo "🔍 快速查找:"
    echo "   grep -A 20 'LINCS' /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md"

elif [[ "$ERROR_MSG" =~ "pull groups" ]]; then
    echo "📖 相关手册:"
    echo "   Chapter 5.8.2 - Pull Code"
    echo "   https://manual.gromacs.org/2026.1/reference-manual/special/pull.html"
    echo ""
    echo "💻 源码位置:"
    echo "   src/gromacs/pulling/pull.cpp"
    echo ""
    echo "🔍 快速查找:"
    echo "   grep -A 30 'Pull Code' /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md"

elif [[ "$ERROR_MSG" =~ "WHAM" ]]; then
    echo "📖 相关手册:"
    echo "   Chapter 5.8.3 - WHAM Analysis"
    echo "   https://manual.gromacs.org/2026.1/reference-manual/special/free-energy-calculations.html#wham"
    echo ""
    echo "💻 源码位置:"
    echo "   src/gromacs/gmxana/gmx_wham.cpp"
    echo ""
    echo "🔍 快速查找:"
    echo "   grep -A 40 'WHAM' /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md"

else
    echo "📖 通用手册索引:"
    echo "   /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md"
    echo ""
    echo "💻 源码搜索:"
    echo "   cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src"
    echo "   grep -r \"$ERROR_MSG\" ."
fi
```

### 脚本 2: 参数查找器

```bash
#!/bin/bash
# 文件: scripts/utils/param_finder.sh
# 功能: 查找 MDP 参数的手册说明和源码定义

PARAM="$1"

echo "🔍 查找参数: $PARAM"
echo ""

# 在手册分析中搜索
echo "📖 手册说明:"
grep -i -A 5 "$PARAM" /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md | head -20
echo ""

# 在源码中搜索
echo "💻 源码定义:"
cd /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src
grep -rn "$PARAM" . --include="*.cpp" --include="*.h" | head -10
echo ""

# 在示例 MDP 中搜索
echo "📝 示例用法:"
find . -name "*.mdp" | xargs grep -h "$PARAM" | head -5
```

---

## 集成到 Skills

### 在脚本中添加引导

**修改示例 (freeenergy.sh):**

```bash
# 原代码
if [ ! -f "$COMPLEX" ]; then
    echo "ERROR: Complex file not found: $COMPLEX"
    exit 1
fi

# 改进后
if [ ! -f "$COMPLEX" ]; then
    echo "ERROR: Complex file not found: $COMPLEX"
    echo ""
    echo "📖 系统准备指南:"
    echo "   手册: Chapter 3.3 - System Preparation"
    echo "   本地: /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md"
    echo ""
    echo "🔍 快速查找:"
    echo "   grep -A 30 'System Preparation' gromacs_manual_analysis.md"
    exit 1
fi
```

### 在 troubleshoot 文档中添加引导

**修改示例 (freeenergy-errors.md):**

```markdown
## ERROR-007: 自由能误差过大

### 症状
...

### 解决方案
...

### 📖 深入学习

如果上述方案仍无法解决问题,建议查阅:

**手册章节:**
- Chapter 5.8.3 - BAR Method
- Chapter 5.12 - Averages and Fluctuations

**本地查找:**
```bash
# 查看手册分析
grep -A 50 "BAR Method" /root/.openclaw/workspace/gromacs-resources/gromacs_manual_analysis.md

# 查看完整手册
evince /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/share/gromacs/manual/gromacs.pdf
```

**源码查看:**
```bash
# 查看 BAR 实现
vim /root/.openclaw/workspace/gromacs-resources/gromacs-2026.1/src/gromacs/gmxana/gmx_bar.cpp
```

**在线资源:**
- 官方手册: https://manual.gromacs.org/2026.1/reference-manual/special/free-energy-calculations.html#bar
- 论文: Bennett (1976) J. Comput. Phys. 22, 245
```

---

## 用户反馈机制

### 记录查找路径

**⚠️ 隐私提示：日志功能默认关闭，避免记录用户行为模式。**
**如需启用排错日志分析，设 `AUTOMD_TROUBLESHOOT_LOG=1`。**

**创建日志文件（仅当启用时）:**
```bash
if [[ "${AUTOMD_TROUBLESHOOT_LOG:-0}" == "1" ]]; then
    mkdir -p ./automd-troubleshoot-log
fi
```

**记录查找过程（仅当启用时）:**
```bash
# 日志默认存于当前工作目录，而非 ~/.gromacs_troubleshoot_log
# 这样用户可以看见和控制
log_troubleshoot() {
    if [[ "${AUTOMD_TROUBLESHOOT_LOG:-0}" != "1" ]]; then
        return 0
    fi
    local error_code="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    mkdir -p ./automd-troubleshoot-log
    echo "[$timestamp] ERROR-$error_code: User consulted manual" >> ./automd-troubleshoot-log/access.log
}
```

### 收集常见问题

**分析日志（仅当用户主动启用）:**
```bash
# 统计最常见的错误
cat ./automd-troubleshoot-log/access.log | awk '{print $3}' | sort | uniq -c | sort -rn
```

**改进 Skills:**
- 将高频问题的解决方案添加到 Level 1
- 完善相关的 troubleshoot 文档

---

## 总结

### 三级体系优势

1. **Level 1 (Skills)**: 快速解决 80% 问题
2. **Level 2 (手册)**: 深入理解 15% 问题
3. **Level 3 (源码)**: 终极解决 5% 问题

### 关键设计原则

1. **渐进式引导**: 从简单到复杂
2. **具体化引用**: 给出精确的章节和行号
3. **可执行命令**: 提供直接可用的查找命令
4. **多种资源**: 本地 + 在线 + 源码
5. **记录反馈**: 持续改进

---

**最后更新:** 2026-04-07
**维护者:** GROMACS Skills 2.0 项目
