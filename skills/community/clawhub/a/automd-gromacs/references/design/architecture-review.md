# GROMACS Skills 2.0 架构重新审视

**核心发现:** 当前架构已经很接近 AI-friendly 设计，但需要进一步优化

---

## 一、当前架构的优势

### ✅ 已经做对的事情

1. **轻量级三层架构**
   ```
   SKILLS_INDEX.yaml (索引) - 结构化 ✅
     ↓
   scripts/*.sh (可执行脚本) - 直接运行 ✅
     ↓
   troubleshoot/*-errors.md (故障排查) - 按需加载 ✅
   ```

2. **脚本的自包含性**
   - 所有参数都有默认值
   - 错误检查完善
   - 可以直接执行

3. **节省 60% 上下文**
   - AI 只需读取索引 + 脚本
   - 不需要读取冗长的 SKILL.md

### ⚠️ 需要改进的地方

1. **错误处理不够自动化**
   - 遇到错误就退出
   - 需要人工干预

2. **手册知识未内嵌**
   - 参数说明在注释中，但不够结构化
   - 关键事实散落在 troubleshoot 文档中

3. **规则未显式化**
   - 参数选择逻辑隐藏在代码中
   - AI 难以理解"为什么这样设置"

---

## 二、改进方案

### 方案 A: 最小改动 (推荐)

**目标:** 在现有架构上增强，不破坏已有设计

**改动:**

1. **增强脚本的自动修复能力**
   ```bash
   # 当前
   if ! command -v acpype; then
       echo "ERROR: ACPYPE not found"
       exit 1
   fi
   
   # 改进后
   if ! command -v acpype; then
       echo "[WARN] ACPYPE not found, attempting auto-install..."
       if command -v conda; then
           conda install -c conda-forge acpype -y
       elif command -v pip; then
           pip install acpype
       else
           echo "[ERROR] Cannot auto-install ACPYPE"
           echo "Required: conda or pip"
           exit 1
       fi
   fi
   ```

2. **在脚本中内嵌关键手册事实**
   ```bash
   # 在脚本开头添加
   # ============================================
   # 参数说明 (来自 GROMACS Manual Chapter 5.8.4)
   # ============================================
   # sc-alpha: 软核参数 (0.3-0.7, 典型值 0.5)
   #   - 控制软核势强度
   #   - 防止 lambda=0/1 时的奇点
   #   - 公式: V_soft = V_LJ * (α*λ^p*σ^6 + r^6)^(-1)
   #   - 选择规则:
   #     * 带电粒子系统: 使用 0.5-0.7
   #     * 大分子系统: 使用 0.3-0.5
   #     * 模拟不稳定: 增加 0.1 (最大 0.7)
   ```

3. **提供结构化的错误输出**
   ```bash
   # 当前
   echo "ERROR: Ligand parameterization failed"
   exit 1
   
   # 改进后
   cat << 'EOF' | tee error_report.json
   {
     "error_code": "ERROR-003",
     "error_name": "Ligand parameterization failed",
     "detection": {
       "command": "acpype",
       "exit_code": 1,
       "log_file": "acpype.log"
     },
     "attempted_fixes": [
       {"method": "acpype", "status": "failed"},
       {"method": "antechamber", "status": "not_available"}
     ],
     "required_action": {
       "install_tool": "conda install -c conda-forge acpype",
       "or_prepare_files": ["ligand.gro", "ligand.itp"],
       "validation": "gmx grompp -f test.mdp -c ligand.gro -p ligand.itp"
     },
     "manual_reference": {
       "chapter": "5.6",
       "key_fact": "Ligand topology must include [moleculetype], [atoms], [bonds]"
     }
   }
   EOF
   exit 1
   ```

### 方案 B: 中等改动

**目标:** 添加 YAML 规则库，但保持脚本为主

**新增文件:**
```
gromacs-skills-2.0/
├── rules/
│   ├── freeenergy-params.yaml    # 参数规则
│   ├── freeenergy-errors.yaml    # 错误定义
│   └── manual-facts.yaml         # 手册事实
└── scripts/
    └── utils/
        └── rule_parser.sh        # YAML 解析器
```

**使用方式:**
```bash
# 在脚本中调用
source scripts/utils/rule_parser.sh

# 读取参数规则
SC_ALPHA=$(get_param_value "sc-alpha" "default")
SC_ALPHA_RANGE=$(get_param_value "sc-alpha" "typical_range")

# 读取错误定义
AUTO_FIX=$(get_error_autofix "ERROR-002")
```

### 方案 C: 大改动 (不推荐)

**目标:** 完全结构化，脚本变成规则执行器

**问题:**
- 破坏现有架构
- 增加复杂度
- 不符合"轻量级"原则

---

## 三、推荐实施路径

### 阶段 1: 立即改进 (1-2 小时)

**目标:** 增强现有脚本的自动修复能力

**任务:**
1. 为 freeenergy.sh 添加自动安装 ACPYPE 的逻辑
2. 为 ligand.sh 添加多工具尝试逻辑
3. 为 membrane.sh 添加依赖检查和提示

**示例:**
```bash
# 在每个脚本的开头添加
auto_install_dependencies() {
    local missing_tools=()
    
    # 检查必需工具
    if ! command -v acpype &> /dev/null; then
        missing_tools+=("acpype")
    fi
    
    # 尝试自动安装
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo "[INFO] Missing tools: ${missing_tools[*]}"
        echo "[INFO] Attempting auto-install..."
        
        for tool in "${missing_tools[@]}"; do
            if command -v conda &> /dev/null; then
                conda install -c conda-forge "$tool" -y
            elif command -v pip &> /dev/null; then
                pip install "$tool"
            fi
        done
    fi
}

# 在脚本开始时调用
auto_install_dependencies
```

### 阶段 2: 内嵌手册事实 (2-3 小时)

**目标:** 将关键手册事实提取并内嵌到脚本注释中

**任务:**
1. 从 gromacs_manual_analysis.md 提取关键事实
2. 以结构化注释的形式添加到脚本中
3. 包含参数说明、选择规则、验证方法

**示例:**
```bash
# ============================================
# 参数配置 (基于 GROMACS Manual Chapter 5.8)
# ============================================

# λ 窗口分布 (Manual 5.8.3)
# - 推荐: 端点密集分布
# - 原因: 端点附近 dH/dλ 变化剧烈
# - 最佳实践: 0.0, 0.05, 0.1, 0.2, ..., 0.8, 0.9, 0.95, 1.0
LAMBDA_VALUES=(0.0 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.95 1.0)

# 软核参数 (Manual 5.8.4)
# - sc-alpha: 0.5 (范围 0.3-0.7)
#   * 带电系统: 0.5-0.7
#   * 大分子: 0.3-0.5
# - sc-power: 1 (或 2)
# - sc-sigma: 0.3 nm
SC_ALPHA=0.5
SC_POWER=1
SC_SIGMA=0.3

# cutoff 距离 (Manual 3.7)
# - 推荐: 1.2 nm (最小 1.0 nm)
# - 原因: 确保长程相互作用准确
RCOULOMB=1.2
RVDW=1.2
```

### 阶段 3: 结构化错误输出 (1-2 小时)

**目标:** 让错误信息对 AI 更友好

**任务:**
1. 统一错误输出格式
2. 包含自动修复尝试记录
3. 提供明确的下一步操作

**示例:**
```bash
report_error() {
    local error_code="$1"
    local error_name="$2"
    local details="$3"
    
    cat << EOF
╔════════════════════════════════════════════════════════════════╗
║ ERROR REPORT                                                   ║
╠════════════════════════════════════════════════════════════════╣
║ Code: $error_code
║ Name: $error_name
║ 
║ Details:
║ $details
║ 
║ Auto-fix attempts:
$(print_autofix_attempts)
║ 
║ Required action:
$(print_required_action "$error_code")
║ 
║ Manual reference:
$(print_manual_reference "$error_code")
╚════════════════════════════════════════════════════════════════╝
EOF
}
```

---

## 四、具体改进示例

### 示例 1: freeenergy.sh 的配体参数化部分

**当前代码:**
```bash
# TODO: 实际的参数化步骤
# acpype -i $LIGAND -n 0 -o gmx
# 生成 ligand.itp 和 ligand.gro
```

**改进后:**
```bash
# ============================================
# 配体参数化 (Manual Chapter 5.6)
# ============================================
# 目标: 生成 ligand.gro 和 ligand.itp
# 方法: 优先 ACPYPE, 备选 antechamber
# 验证: gmx grompp 测试拓扑正确性

parameterize_ligand() {
    local input="$1"
    local output_dir="$2"
    
    echo "[1/4] Checking existing topology..."
    if [ -f "$output_dir/ligand.gro" ] && [ -f "$output_dir/ligand.itp" ]; then
        echo "  ✓ Found existing topology"
        return 0
    fi
    
    echo "[2/4] Attempting ACPYPE..."
    if command -v acpype &> /dev/null; then
        acpype -i "$input" -n 0 -o gmx -d "$output_dir" &> acpype.log
        if [ $? -eq 0 ]; then
            echo "  ✓ ACPYPE succeeded"
            return 0
        else
            echo "  ✗ ACPYPE failed (see acpype.log)"
        fi
    else
        echo "  - ACPYPE not available"
        # 尝试自动安装
        if command -v conda &> /dev/null; then
            echo "  → Installing ACPYPE via conda..."
            conda install -c conda-forge acpype -y &> conda_install.log
            if command -v acpype &> /dev/null; then
                acpype -i "$input" -n 0 -o gmx -d "$output_dir" &> acpype.log
                if [ $? -eq 0 ]; then
                    echo "  ✓ ACPYPE installed and succeeded"
                    return 0
                fi
            fi
        fi
    fi
    
    echo "[3/4] Attempting antechamber..."
    if command -v antechamber &> /dev/null; then
        antechamber -i "$input" -fi mol2 -o ligand.mol2 -fo mol2 -c bcc -nc 0 &> antechamber.log
        if [ $? -eq 0 ]; then
            parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod
            # 转换为 GROMACS 格式 (需要 acpype 或 ParmEd)
            echo "  ✓ antechamber succeeded (conversion needed)"
            # TODO: 添加转换逻辑
        fi
    else
        echo "  - antechamber not available"
    fi
    
    echo "[4/4] All methods failed"
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║ ERROR-003: Ligand Parameterization Failed                     ║
╠════════════════════════════════════════════════════════════════╣
║ Attempted methods:
║   - ACPYPE: not available or failed
║   - antechamber: not available or failed
║ 
║ Required action (choose one):
║ 
║ Option 1: Install ACPYPE
║   conda install -c conda-forge acpype
║ 
║ Option 2: Install AmberTools
║   conda install -c conda-forge ambertools
║ 
║ Option 3: Use online tool
║   - LigParGen: http://zarbi.chem.yale.edu/ligpargen/
║   - ATB: https://atb.uq.edu.au/
║   Then place ligand.gro and ligand.itp in: $output_dir/
║ 
║ Option 4: Provide pre-parameterized files
║   --ligand-gro <file> --ligand-itp <file>
║ 
║ Manual reference:
║   Chapter 5.6: Topology File Format
║   Required sections: [moleculetype], [atoms], [bonds]
║   Validation: gmx grompp -f test.mdp -c ligand.gro -p ligand.itp
╚════════════════════════════════════════════════════════════════╝
EOF
    return 1
}

# 调用
if ! parameterize_ligand "$LIGAND" "$OUTPUT"; then
    exit 1
fi
```

---

## 五、总结

### 核心洞察

**当前架构已经很好，只需增强:**
1. ✅ 轻量级三层架构 - 保持
2. ✅ 可执行脚本 - 保持
3. ⚠️ 自动修复能力 - 增强
4. ⚠️ 手册事实内嵌 - 增强
5. ⚠️ 结构化错误输出 - 增强

### 实施优先级

**P0 (立即):**
- 增强脚本的自动修复能力
- 添加依赖自动安装逻辑

**P1 (本周):**
- 内嵌手册关键事实到脚本注释
- 统一错误输出格式

**P2 (下周):**
- 创建 YAML 规则库 (可选)
- 提供辅助工具脚本

### 不要做的事

❌ 不要完全重构架构
❌ 不要引入过多抽象层
❌ 不要破坏"轻量级"原则
❌ 不要让 AI 去"学习"手册

### 要做的事

✅ 让脚本更智能 (自动修复)
✅ 让错误更明确 (结构化输出)
✅ 让知识更内嵌 (手册事实)
✅ 让 AI 更自主 (减少人工干预)

---

**创建时间:** 2026-04-07 09:40
**状态:** ✅ 改进方案已明确
**下一步:** 实施阶段 1 (自动修复增强)
