# AI Agent 使用 Skills 的设计原则

**核心认知:** Skills 的用户是 AI Agent，不是人类

---

## 一、AI Agent 的特点

### 与人类用户的区别

| 维度 | 人类用户 | AI Agent |
|------|---------|----------|
| 学习能力 | 需要学习和理解 | 不需要"学习"，需要"事实" |
| 探索能力 | 可以浏览手册 | 不需要"浏览"，需要"提取" |
| 上下文 | 有限，需要简化 | 有限，需要精简 |
| 执行方式 | 手动执行命令 | 调用 Skills 脚本 |
| 错误处理 | 需要引导和教育 | 需要明确的条件判断 |

### AI Agent 的需求

1. **明确性** - 不要"可能"，要"是"
2. **可执行性** - 不要"建议"，要"命令"
3. **完整性** - 不要"参考"，要"包含"
4. **结构化** - 不要"文本"，要"数据"

---

## 二、错误处理的正确方式

### ❌ 错误示例 (面向人类)

```bash
ERROR-002: ACPYPE 未安装

原因: ACPYPE (小分子参数化工具) 未安装

解决方案:
方案 1: 安装 ACPYPE (推荐)
  conda install -c conda-forge acpype

方案 2: 使用在线工具
  - LigParGen: http://zarbi.chem.yale.edu/ligpargen/
  - 步骤: 上传配体 → 选择 GROMACS → 下载 .itp

方案 3: 手动准备
  准备 ligand.gro 和 ligand.itp 文件

📖 详细指南: troubleshoot/freeenergy-errors.md#error-002
```

**问题:**
- AI 不需要"推荐"，需要"判断条件"
- AI 不能"上传到网站"
- AI 不知道"手动准备"是什么意思

### ✅ 正确示例 (面向 AI)

```bash
ERROR-002: ACPYPE 未安装

检测结果:
  command: acpype
  status: not found
  required_for: ligand parameterization

自动修复:
  [1] 检查 conda 是否可用
      if command -v conda; then
          conda install -c conda-forge acpype -y
          exit_code: $?
      fi
  
  [2] 检查 pip 是否可用
      if command -v pip; then
          pip install acpype
          exit_code: $?
      fi
  
  [3] 如果都失败，检查是否有预准备的拓扑
      required_files:
        - ligand.gro (配体坐标)
        - ligand.itp (配体拓扑)
      
      if [ -f "ligand.gro" ] && [ -f "ligand.itp" ]; then
          echo "Using pre-prepared topology"
          continue_execution: true
      else
          echo "ERROR: Cannot proceed without ACPYPE or pre-prepared topology"
          exit 1
      fi

替代工具:
  - antechamber (AmberTools)
    check: command -v antechamber
    usage: antechamber -i ligand.mol2 -fi mol2 -o ligand.mol2 -fo mol2 -c bcc
  
  - obabel (Open Babel)
    check: command -v obabel
    usage: obabel ligand.sdf -O ligand.mol2 -h

手册事实 (供 AI 理解上下文):
  source: GROMACS Manual Chapter 5.6
  fact: "配体拓扑必须包含 [moleculetype], [atoms], [bonds] 等节"
  validation: gmx grompp -f test.mdp -c ligand.gro -p ligand.itp -o test.tpr
```

**优势:**
- AI 可以按顺序尝试自动修复
- 每个步骤都有明确的检查条件
- 提供了可验证的替代方案
- 包含了手册中的关键事实（而不是引用）

---

## 三、参数说明的正确方式

### ❌ 错误示例 (面向人类)

```bash
sc-alpha: 软核参数

📖 详细说明:
   手册: Chapter 5.8.4 - Soft-core Interactions
   公式: V_soft = V_LJ * (α * λ^p * σ^6 + r^6)^(-1)
   
   推荐值: 0.3-0.7 (典型值 0.5)
   
🔍 查看完整说明:
   grep -A 30 "Soft-core" gromacs_manual_analysis.md
```

**问题:**
- AI 不需要"查看"，需要"知道"
- AI 不需要"推荐"，需要"规则"

### ✅ 正确示例 (面向 AI)

```yaml
parameter: sc-alpha
type: float
unit: dimensionless
valid_range: [0.0, 1.0]
typical_range: [0.3, 0.7]
default: 0.5

purpose: |
  Controls the strength of soft-core potential in free energy calculations.
  Prevents singularities when particles appear/disappear.

formula: |
  V_soft = V_LJ * (alpha * lambda^p * sigma^6 + r^6)^(-1)
  where:
    - V_LJ: Lennard-Jones potential
    - lambda: coupling parameter (0-1)
    - p: sc-power (typically 1 or 2)
    - sigma: sc-sigma (typically 0.3 nm)

selection_rules:
  - if: system_has_charged_particles
    then: use_higher_value  # 0.5-0.7
    reason: "Stronger soft-core needed for Coulomb interactions"
  
  - if: system_has_large_molecules
    then: use_lower_value  # 0.3-0.5
    reason: "Avoid over-softening of large vdW interactions"
  
  - if: lambda_windows_fail
    then: increase_by: 0.1
    max: 0.7
    reason: "Increase soft-core to stabilize simulations"

related_parameters:
  - sc-power: "Exponent in soft-core formula"
  - sc-sigma: "Soft-core radius"
  - couple-lambda0: "Interactions at lambda=0"
  - couple-lambda1: "Interactions at lambda=1"

validation:
  - check: sc-alpha >= 0.0 && sc-alpha <= 1.0
    error: "sc-alpha must be between 0 and 1"
  
  - check: free-energy == yes
    error: "sc-alpha only valid when free-energy = yes"

manual_reference:
  chapter: "5.8.4"
  title: "Soft-core Interactions"
  page: 234
  key_facts:
    - "Soft-core prevents singularities at lambda=0 and lambda=1"
    - "Higher alpha = stronger soft-core = more stable but less accurate"
    - "Typical values: 0.5 for vdW, 0.5-0.7 for Coulomb"
```

**优势:**
- AI 可以直接解析 YAML
- 包含了选择规则（不是"推荐"）
- 提供了验证条件
- 手册事实已提取（不需要查阅）

---

## 四、Skills 脚本的正确设计

### ❌ 错误示例 (需要人类干预)

```bash
# 配体参数化
echo "使用 ACPYPE 生成 GAFF 参数..."

if ! command -v acpype &> /dev/null; then
    echo "WARNING: ACPYPE not found"
    echo "请安装 ACPYPE 或手动准备配体拓扑"
    echo "参考: troubleshoot/freeenergy-errors.md#error-002"
    exit 1
fi

# TODO: 实际的参数化步骤
```

**问题:**
- 遇到错误就退出
- 需要人类去"参考文档"
- TODO 意味着功能未完成

### ✅ 正确示例 (AI 可自主处理)

```bash
# 配体参数化 (自动尝试多种方案)
parameterize_ligand() {
    local ligand_file="$1"
    local output_dir="$2"
    
    # 方案 1: 检查是否已有拓扑
    if [ -f "${output_dir}/ligand.gro" ] && [ -f "${output_dir}/ligand.itp" ]; then
        echo "[INFO] Using existing topology files"
        return 0
    fi
    
    # 方案 2: 尝试 ACPYPE
    if command -v acpype &> /dev/null; then
        echo "[INFO] Parameterizing with ACPYPE..."
        acpype -i "$ligand_file" -n 0 -o gmx -d "$output_dir" &> acpype.log
        if [ $? -eq 0 ] && [ -f "${output_dir}/ligand.gro" ]; then
            echo "[SUCCESS] ACPYPE parameterization completed"
            return 0
        else
            echo "[WARN] ACPYPE failed, trying alternative..."
        fi
    fi
    
    # 方案 3: 尝试 antechamber (AmberTools)
    if command -v antechamber &> /dev/null; then
        echo "[INFO] Parameterizing with antechamber..."
        antechamber -i "$ligand_file" -fi mol2 -o ligand.mol2 -fo mol2 -c bcc -nc 0 &> antechamber.log
        if [ $? -eq 0 ]; then
            parmchk2 -i ligand.mol2 -f mol2 -o ligand.frcmod
            # 转换为 GROMACS 格式
            acpype -p ligand.prmtop -x ligand.inpcrd -d "$output_dir"
            if [ $? -eq 0 ]; then
                echo "[SUCCESS] antechamber parameterization completed"
                return 0
            fi
        fi
    fi
    
    # 方案 4: 提供明确的错误和解决方案
    cat << EOF
[ERROR] Ligand parameterization failed

All automatic methods failed:
  - ACPYPE: $(command -v acpype &> /dev/null && echo "available but failed" || echo "not installed")
  - antechamber: $(command -v antechamber &> /dev/null && echo "available but failed" || echo "not installed")

Required files not found:
  - ${output_dir}/ligand.gro
  - ${output_dir}/ligand.itp

AI Agent Action Required:
  1. Install parameterization tool:
     conda install -c conda-forge acpype
     OR
     conda install -c conda-forge ambertools
  
  2. OR prepare topology manually using online tools:
     - LigParGen: http://zarbi.chem.yale.edu/ligpargen/
     - ATB: https://atb.uq.edu.au/
     
     Then place files in: ${output_dir}/
  
  3. OR provide pre-parameterized files via --ligand-topology flag

Manual Reference (for context):
  GROMACS Manual Chapter 5.6: Topology File Format
  Required sections: [moleculetype], [atoms], [bonds], [angles], [dihedrals]

EOF
    return 1
}

# 调用参数化函数
if ! parameterize_ligand "$LIGAND" "$OUTPUT"; then
    echo "[FATAL] Cannot proceed without ligand topology"
    exit 1
fi
```

**优势:**
- AI 可以自动尝试多种方案
- 每个方案都有明确的成功/失败判断
- 失败时提供结构化的错误信息
- 包含了 AI 可以执行的具体操作
- 手册事实已内嵌（不需要查阅）

---

## 五、文档的正确组织

### ❌ 错误方式 (面向人类)

```
troubleshoot/freeenergy-errors.md (15 KB)
  - ERROR-001: 详细说明 + 多种方案 + 手册引用
  - ERROR-002: 详细说明 + 多种方案 + 手册引用
  - ...
  - FAQ
  - 参考资源
```

**问题:**
- AI 需要读取整个 15 KB 文档
- 大量人类导向的文本（"建议"、"推荐"、"参考"）
- 手册引用需要二次查找

### ✅ 正确方式 (面向 AI)

```
troubleshoot/
├── freeenergy-errors.yaml          # 结构化错误定义
├── freeenergy-params.yaml          # 参数规则库
└── freeenergy-manual-facts.yaml    # 手册关键事实提取
```

**freeenergy-errors.yaml:**
```yaml
errors:
  ERROR-002:
    name: "ACPYPE not installed"
    detection:
      command: "acpype"
      exit_code: 127
    
    auto_fix:
      - method: "conda_install"
        command: "conda install -c conda-forge acpype -y"
        check: "command -v acpype"
      
      - method: "pip_install"
        command: "pip install acpype"
        check: "command -v acpype"
    
    alternatives:
      - tool: "antechamber"
        check: "command -v antechamber"
        usage: "antechamber -i {input} -fi mol2 -o {output} -fo mol2 -c bcc"
      
      - tool: "pre_prepared"
        required_files:
          - "ligand.gro"
          - "ligand.itp"
        validation: "gmx grompp -f test.mdp -c ligand.gro -p ligand.itp -o test.tpr"
    
    manual_facts:
      source: "Chapter 5.6"
      key_points:
        - "Ligand topology must include [moleculetype], [atoms], [bonds]"
        - "Atom types must match force field"
        - "Total charge should be integer"
```

**优势:**
- AI 可以直接解析 YAML
- 结构化数据，易于程序化处理
- 包含了自动修复逻辑
- 手册事实已提取，无需二次查找

---

## 六、Skills 2.0 架构的改进方向

### 当前架构

```
SKILLS_INDEX.yaml (索引)
  ↓
scripts/freeenergy.sh (Bash 脚本)
  ↓
troubleshoot/freeenergy-errors.md (Markdown 文档)
```

### 改进后的架构

```
SKILLS_INDEX.yaml (索引)
  ↓
scripts/freeenergy.sh (增强的 Bash 脚本)
  ├── 内嵌自动修复逻辑
  ├── 结构化错误输出
  └── 调用 YAML 规则库
  ↓
rules/ (YAML 规则库)
  ├── errors.yaml (错误定义 + 自动修复)
  ├── params.yaml (参数规则 + 选择逻辑)
  └── manual-facts.yaml (手册关键事实)
```

### 关键改进

1. **自包含性**
   - 脚本内嵌常见错误的自动修复
   - 减少对外部文档的依赖

2. **结构化数据**
   - 用 YAML 替代 Markdown
   - AI 可以直接解析和使用

3. **手册事实提取**
   - 不是"引用手册"
   - 而是"提取关键事实并内嵌"

4. **可执行性优先**
   - 每个错误都有明确的修复步骤
   - 每个参数都有选择规则

---

## 七、总结

### 核心原则

1. **AI 不需要"学习"，需要"事实"**
   - 不要引用手册，要提取关键事实
   - 不要建议查阅，要直接包含

2. **AI 不需要"探索"，需要"答案"**
   - 不要多种可能，要明确判断
   - 不要开放式建议，要条件化规则

3. **AI 不需要"引导"，需要"执行"**
   - 不要教育性文本，要可执行命令
   - 不要人工干预，要自动修复

4. **AI 需要"结构化"，不需要"文本"**
   - 用 YAML/JSON，不用 Markdown
   - 用数据结构，不用自然语言

### 实施建议

**短期 (立即可做):**
- 在脚本中增加自动修复逻辑
- 在错误信息中包含手册关键事实
- 提供结构化的错误输出

**中期 (下一版本):**
- 创建 YAML 规则库
- 提取手册关键事实到 YAML
- 重构脚本以使用规则库

**长期 (未来方向):**
- 完全结构化的 Skills 定义
- AI 可以动态组合 Skills
- 自动从手册生成规则库

---

**创建时间:** 2026-04-07 09:35
**核心洞察:** Skills 的用户是 AI，不是人类
**设计原则:** 可执行 > 可读，结构化 > 文本化，事实 > 引用
