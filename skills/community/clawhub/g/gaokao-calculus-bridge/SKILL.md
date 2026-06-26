---
name: gaokao-calculus-bridge
description: 桥接2026高考数学改革与高等数学教育，培养真实世界问题解决能力。当用户需要情境化数学建模、跨学科应用、或从刷题模式转向素养培养时触发。
version: 1.0.0
author: daigxok
license: MIT
platforms: [macos, linux, windows]
metadata:
  openclaw:
    emoji: "🎓"
    homepage: "https://clawhub.ai/daigxok/gaokao-calculus-bridge"
    always: false
    skillKey: "gaokao-bridge"
    requires:
      bins: ["python3", "node"]
      env: ["OPENAI_API_KEY"]
      config: ["~/.openclaw/skills/gaokao-calculus-bridge/config.yaml"]
    primaryEnv: "OPENAI_API_KEY"
    install:
      - id: "python-deps"
        kind: "pip"
        packages: ["numpy", "matplotlib", "sympy", "pandas", "scipy"]
        label: "Install Python dependencies"
    config:
      - key: "difficulty_level"
        description: "默认难度级别 (high_school/college/bridge)"
        default: "bridge"
        prompt: "Select default difficulty level"
      - key: "domain_focus"
        description: "关注领域 (physics/cs/economics/biology/general)"
        default: "general"
        prompt: "Select domain focus for real-world cases"
---

# 高考-高数衔接智慧课程 (Gaokao-Calculus Bridge)

## When to Use

**触发条件**（满足任一即激活）：
- 用户提及"2026高考数学改革"、"情境化命题"、"真实世界问题"
- 用户需要从高中刷题模式过渡到大学数学学习
- 用户需要解决跨学科数学建模问题（AI/物理/经济/生物背景）
- 用户遇到长题干数学题，需要信息提取与建模指导
- 用户希望培养"数学翻译"能力（现实→数学语言）
- 用户需要设计项目式、探究式数学学习任务

**不触发条件**：
- 纯计算题求解（使用计算工具Skill）
- 标准定理证明（使用推导动画Skill）
- 单纯的概念查询（使用概念可视化Skill）

## Quick Reference

| 命令/请求 | 功能 |
|-----------|------|
| "分析2026高考改革要求" | 输出改革核心要点与应对策略 |
| "生成情境化题目 [领域]" | 生成指定领域的真实世界数学问题 |
| "建立概念映射 [高中概念] → [大学概念]" | 展示知识衔接路径 |
| "开始项目式学习 [主题]" | 启动完整PBL学习流程 |
| "分析长题干题目 [粘贴题目]" | 信息提取与建模指导 |
| "推荐学习路径 [当前水平]" | 生成个性化学习方案 |

## Core Workflows

### Workflow 1: 高考改革要点解析

**当用户询问2026高考数学改革时执行：**

1. **输出改革三重内核**（引用references/gaokao_2026_reform.md）：
   - 科技是背景板，建模是考点
   - 阅读能力是数学的新底盘
   - 从"深挖洞"到"广积粮"的策略转变

2. **能力对标分析**：
   - 高考要求 → 大学数学能力 → 本Skill培养方案
   - 使用脚本：`python3 scripts/concept_mapper.py --mode=ability`

3. **提供即时行动建议**：
   - 若用户是高中生：推荐"情境化解题训练"
   - 若用户是大学生：推荐"真实建模项目"
   - 若用户是教师：推荐"课程设计方案"

### Workflow 2: 情境化题目生成

**当用户需要真实世界数学问题时执行：**

1. **确定情境领域**（根据config.domain_focus或用户输入）：
   - 科技前沿：AI/量子计算/碳中和/脑机接口
   - 工程应用：电路优化/结构力学/信号处理
   - 社会经济：金融/人口/资源分配
   - 自然科学：生物种群/流行病/物理场

2. **运行生成脚本**：
   ```bash
   python3 scripts/problem_generator.py \
     --domain "${DOMAIN}" \
     --difficulty "${DIFFICULTY}" \
     --topic "${MATH_TOPIC}" \
     --output-format markdown
   ```

3. **题目结构要求**（必须包含）：
   - **背景段**：300-400字真实情境描述（含科技/人文元素）
   - **信息层**：嵌入关键参数、变量、约束条件（需提取）
   - **问题链**：从具体到抽象的分层设问
   - **建模提示**：引导学生完成"翻译"的关键问题

4. **示例输出格式**：
   ```markdown
   ## 情境：[领域名称]

   【背景】[真实世界描述，含专业术语]

   【信息提取】
   - 关键变量：[列表]
   - 约束条件：[列表]
   - 目标：[优化/预测/证明]

   【数学建模】
   请将上述情境转化为数学问题：[提示]

   【问题】
   (1) [基础计算]
   (2) [模型建立]
   (3) [拓展分析]
   ```

### Workflow 3: 长题干解析与建模

**当用户提供长题干题目时执行：**

1. **信息提取阶段**：
   - 使用脚本：`python3 scripts/model_extractor.py --text="${USER_INPUT}"`
   - 提取：关键参数、隐含条件、逻辑关系、问题意图

2. **结构化分析**：
   ```markdown
   ### 题目解构报告

   **原始字数**：XXX字
   **核心信息**：XX个参数，XX个约束

   **信息图谱**：
   [变量A] → [关系] → [变量B]

   **建模路径**：
   现实概念 [术语] → 数学抽象 [概念] → 工具选择 [方法]
   ```

3. **分步引导策略**：
   - 第一步：翻译（圈画关键信息）
   - 第二步：建模（建立变量关系）
   - 第三步：求解（选择数学工具）
   - 第四步：验证（回归现实情境）

### Workflow 4: 概念映射与衔接

**当用户需要理解高中到大学的知识跃迁时执行：**

1. **运行映射脚本**：
   ```bash
   python3 scripts/concept_mapper.py \
     --from "${HIGH_SCHOOL_CONCEPT}" \
     --to "${COLLEGE_CONCEPT}" \
     --visualization true
   ```

2. **输出衔接方案**：
   - 高中基础：[知识点+典型题型]
   - 大学拓展：[理论深化+应用场景]
   - 鸿沟识别：[常见认知断层]
   - 过渡练习：[桥接性题目]

3. **可视化展示**：
   - 知识图谱（文本形式）
   - 难度梯度曲线
   - 典型错误预警

### Workflow 5: 项目式学习(PBL)设计

**当用户需要完整的学习项目时执行：**

1. **项目启动**（使用templates/project_guide.md）：
   - 真实问题选择（来自references/real_world_cases.md）
   - 学习目标设定（知识+能力+素养）
   - 角色分配（数学家/工程师/数据分析师）

2. **阶段推进**：
   - **阶段1：问题解构**（1-2课时）
     - 背景调研、信息收集、问题定义
   - **阶段2：模型构建**（2-3课时）
     - 假设简化、变量选择、方程建立
   - **阶段3：求解验证**（2课时）
     - 数学求解、结果解释、模型检验
   - **阶段4：成果展示**（1课时）
     - 报告撰写、同伴评议、反思提升

3. **评价量规**：
   - 情境理解准确度（30%）
   - 模型合理性（30%）
   - 数学工具运用（25%）
   - 创新性与表达（15%）

### Workflow 6: 自适应学习路径

**当用户需要个性化学习方案时执行：**

1. **诊断评估**：
   - 当前水平测试（高考真题情境题）
   - 薄弱环节识别（信息提取/建模/计算/跨学科）
   - 学习目标确认（应试/能力提升/竞赛/科研）

2. **路径生成**（运行脚本）：
   ```bash
   python3 scripts/learning_path_advisor.py \
     --assessment "${ASSESSMENT_RESULT}" \
     --goal "${LEARNING_GOAL}" \
     --duration "${TIME_FRAME}"
   ```

3. **输出内容**：
   - 周计划（情境化题目+阅读材料+建模练习）
   - 资源推荐（跨学科阅读清单+工具教程）
   - 里程碑检测（阶段性能力自评）

## Integration with Existing Skills

**本Skill与已有高数Skill的协同**：

| 本Skill输出 | 衔接Skill | 使用场景 |
|-------------|-----------|----------|
| 情境化题目（需可视化） | `calculus-concept-visualizer` | 抽象概念动态演示 |
| 复杂推导过程 | `derivation-animation-skill` | 分步推导动画生成 |
| 建模错误分析 | `error-analysis-skill` | 错题归因与针对性训练 |
| 跨学科数据 | `calculus-resource-harvester` | 真实数据采集与验证 |

**调用示例**：
```
用户："生成一道AI优化情境的数学题并可视化"

执行流程：
1. gaokao-calculus-bridge 生成题目（Workflow 2）
2. 检测到"梯度下降"概念 → 调用 calculus-concept-visualizer 生成3D可视化
3. 整合输出：情境描述 + 交互式GeoGebra嵌入 + 分步建模指导
```

## Pitfalls & Warnings

**常见失败模式**：

1. **情境过载**：
   - 问题：背景描述过于复杂，学生困于术语理解
   - 解决：提供"术语速查表"，区分"需理解的背景"与"可剥离的噪音"

2. **建模跳跃**：
   - 问题：从现实到数学的跨越过大，学生无从入手
   - 解决：提供"脚手架"——中间变量设定、简化假设提示、类比案例

3. **跨学科恐惧**：
   - 问题：学生因不熟悉专业领域而产生认知恐惧
   - 解决：强调"背景只是背景板"，提供领域无关的通用建模框架

4. **评价偏差**：
   - 问题：过度关注数学解的正确性，忽视建模过程
   - 解决：使用本Skill提供的评价量规，平衡过程与结果

## Verification

**验证Skill正常工作**：

1. **基础测试**：
   ```
   输入："2026高考数学改革考什么？"
   预期输出：包含"情境化建模、深度阅读、广度积累"三要点
   ```

2. **生成测试**：
   ```
   输入："生成一道碳中和情境的微积分题"
   预期输出：包含背景描述、信息提取层、分层问题的完整题目
   ```

3. **映射测试**：
   ```
   输入："映射 高中导数 → 大学微分学"
   预期输出：知识衔接路径+典型断层+过渡练习
   ```

**故障排查**：
- 若脚本运行失败：检查Python依赖是否安装（`pip install -r requirements.txt`）
- 若API调用失败：检查OPENAI_API_KEY环境变量
- 若输出格式异常：检查config.yaml中的difficulty_level设置

## References

**详细文档请查阅references/目录**：
- `gaokao_2026_reform.md`：改革政策原文与解读
- `real_world_cases.md`：分类真实世界案例库
- `modeling_templates.md`：通用数学建模模板
- `interdisciplinary_models.md`：跨学科模型速查

**脚本使用文档**：
- 运行`python3 scripts/<script>.py --help`查看参数说明
- 所有脚本支持`--output-format json`用于程序化调用
