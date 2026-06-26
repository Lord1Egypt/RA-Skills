# 元提示系统 (Meta-Prompt System) — 已废弃

> ⚠️ 本文档描述的Python脚本方案已被废弃。
> 元提示系统的功能已内化为SKILL.md中的"元提示层"章节，AI直接在对话中执行。
> 本文档仅供历史参考。

> 用户端优化可以增加大模型50%的能力。

---

## 系统架构

```
用户输入 → [Meta-Prompt层] → 优化后的提示 → [执行层] → 高质量输出
               │
               ├── 提示词优化器 (prompt_optimizer.py)
               ├── 逻辑规范器 (logic_normalizer.py)
               ├── 质量检查器 (quality_checker.py)
               └── 场景预处理器 (scenario_preprocessor.py)
```

### 两阶段执行模型

| 阶段 | 职责 | 工具 |
|------|------|------|
| **第一阶段：优化** | 用元提示模板做逻辑规范和提示词编写 | prompt_optimizer + logic_normalizer |
| **第二阶段：执行** | 将优化后的内容提交给大模型执行 | 优化后的 meta_prompt → 大模型 |
| **质量闭环** | 检查输出质量，必要时重新优化 | quality_checker |

---

## 组件说明

### 1. 提示词优化器 (Prompt Optimizer)

**文件**: `scripts/prompt_optimizer.py`

**功能**: 将用户的原始问题/场景优化为结构化的、能激发大模型最佳能力的提示词。

**核心能力**:
- 6种任务类型自动识别：分析(analysis)、建议(advice)、对话(dialogue)、评估(evaluation)、自省(reflection)、危机(crisis)
- 为每种类型定制推理链和质量检查点
- 融入"觉察→接纳→暂停→选择"核心路径

**使用方法**:

```python
from scripts.prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()

# 基本优化
result = optimizer.optimize("孩子不听话怎么办")
# → 提交 result["meta_prompt"] 给大模型执行

# 指定任务类型
result = optimizer.optimize("孩子沉迷手机", task_type="advice")

# 带额外上下文
result = optimizer.optimize("成绩下降", context="孩子8岁，男孩")
```

**命令行**:
```bash
python3 scripts/prompt_optimizer.py "孩子不听话怎么办"
python3 scripts/prompt_optimizer.py --task-type advice "孩子沉迷手机"
python3 scripts/prompt_optimizer.py --context "孩子8岁" "成绩下降"
python3 scripts/prompt_optimizer.py --list-types
```

---

### 2. 逻辑规范器 (Logic Normalizer)

**文件**: `scripts/logic_normalizer.py`

**功能**: 将用户的模糊描述转换为结构化的问题定义，识别关键要素。

**核心能力**:
- 7大问题分类自动识别：行为、情绪、关系、发展、安全、父母自身、家庭系统
- 4级紧急程度评估：critical / high / medium / low
- 缺失信息检测：自动发现用户未提供的关键信息
- 情绪基调识别：焦虑、愤怒、悲伤、无助、自责
- 问题重新框架化：从"孩子有问题"转为"孩子有未满足的需求"

**使用方法**:

```python
from scripts.logic_normalizer import LogicNormalizer

normalizer = LogicNormalizer()

# 快速分析（仅本地关键词匹配）
result = normalizer.normalize("孩子总是不听话", depth="quick")

# 深度分析（生成元提示，提交大模型）
result = normalizer.normalize("孩子成绩下降，我快崩溃了", depth="deep")
# → 提交 result["meta_prompt"] 给大模型执行
```

**命令行**:
```bash
python3 scripts/logic_normalizer.py "孩子总是不听话"
python3 scripts/logic_normalizer.py --depth deep "孩子成绩下降，我快崩溃了"
```

---

### 3. 质量检查器 (Quality Checker)

**文件**: `scripts/quality_checker.py`

**功能**: 检查AI输出是否符合预期，识别潜在问题，提供改进建议。

**5大检查维度**:

| 维度 | 权重 | 检查项 |
|------|------|--------|
| 安全性 | 10 | 无惩罚性建议、危机转介、无绝对化表述 |
| 共情性 | 8 | 承认情绪、不指责父母 |
| 可操作性 | 7 | 有具体步骤、有对话示例、年龄适配 |
| 深度 | 6 | 探索根因、父母视角 |
| 理念一致性 | 5 | 核心路径（觉察→接纳→暂停→选择）、需求导向 |

**使用方法**:

```python
from scripts.quality_checker import QualityChecker

checker = QualityChecker()

# 快速检查（本地关键词匹配）
result = checker.check("AI的输出内容...", original_question="孩子不听话")

# 深度检查（生成元提示，提交大模型）
result = checker.check("AI输出...", original_question="孩子不听话", depth="deep")

# 列出所有检查项
checks = checker.list_checks()
```

**命令行**:
```bash
python3 scripts/quality_checker.py --question "孩子不听话" "AI输出内容..."
python3 scripts/quality_checker.py --depth deep --question "孩子不听话" --file output.txt
python3 scripts/quality_checker.py --list-checks
```

---

### 4. 场景预处理器 (Scenario Preprocessor)

**文件**: `scripts/scenario_preprocessor.py`

**功能**: 自动匹配最相关的场景文件，提取关键信息，生成定制化的提示词。

**核心能力**:
- 覆盖73个育儿场景的关键词索引
- 基于关键词权重的相关度评分
- 自动读取匹配场景的完整内容
- 综合多场景生成定制化提示词

**使用方法**:

```python
from scripts.scenario_preprocessor import ScenarioPreprocessor

preprocessor = ScenarioPreprocessor()

# 预处理（匹配场景 + 生成元提示）
result = preprocessor.preprocess("孩子最近成绩下降了，不愿意写作业")
# → result["matched_scenarios"] 匹配到的场景
# → result["meta_prompt"] 可提交大模型的定制化提示词

# 仅匹配场景
matches = preprocessor.match_scenarios("孩子不想上学", top_n=5)

# 列出所有场景
scenarios = preprocessor.list_scenarios()
```

**命令行**:
```bash
python3 scripts/scenario_preprocessor.py "孩子成绩下降了"
python3 scripts/scenario_preprocessor.py --top 5 "孩子不想上学"
python3 scripts/scenario_preprocessor.py --list
```

---

## 集成方式

### 与 SKILL.md 的集成

在 SKILL.md 的使用流程中，元提示系统可以在以下环节接入：

#### 方式1: 自动流水线（推荐）

```python
from scripts.prompt_optimizer import PromptOptimizer
from scripts.logic_normalizer import LogicNormalizer
from scripts.quality_checker import QualityChecker
from scripts.scenario_preprocessor import ScenarioPreprocessor

# 第一步：场景预处理
preprocessor = ScenarioPreprocessor()
scenario_result = preprocessor.preprocess(user_input)

# 第二步：逻辑规范
normalizer = LogicNormalizer()
logic_result = normalizer.normalize(user_input, depth="deep")

# 第三步：提示词优化（融合场景和逻辑分析）
optimizer = PromptOptimizer()
prompt_result = optimizer.optimize(
    user_input,
    context=json.dumps({
        "scenario": scenario_result["matched_scenarios"],
        "logic": logic_result["auto_analysis"],
    })
)

# 第四步：提交大模型执行
# optimized_prompt = prompt_result["meta_prompt"]
# ai_output = call_llm(optimized_prompt)

# 第五步：质量检查
checker = QualityChecker()
quality_result = checker.check(ai_output, original_question=user_input, depth="quick")
```

#### 方式2: 按需使用单个组件

```python
# 仅需要质量检查时
from scripts.quality_checker import QualityChecker
checker = QualityChecker()
result = checker.check(ai_output, question="孩子不听话")
if not result["auto_check"]["passed"]:
    # 需要改进
    print(result["auto_check"]["issues"])
```

#### 方式3: 命令行管道

```bash
# 完整流水线
input="孩子成绩下降了"
scenario=$(python3 scripts/scenario_preprocessor.py "$input")
logic=$(python3 scripts/logic_normalizer.py --depth deep "$input")
prompt=$(python3 scripts/prompt_optimizer.py --context "$scenario" "$input")
# 将 $prompt 提交给大模型...
```

### 与现有场景文件的关系

- **场景文件** (`scenarios/*.md`): 提供具体的育儿场景描述、错误反应、正确做法
- **场景预处理器**: 自动匹配最相关的场景，提取关键信息用于定制化
- **关系**: 场景文件是"素材库"，预处理器是"搜索引擎"

### 与理论文件的关系

- **理论文件** (`theory/*.md`): 提供心理学理论基础
- **元提示系统**: 将理论融入提示词的推理链和质量检查点中
- **关系**: 理论是"知识库"，元提示系统是"应用层"

---

## 设计原则

1. **渐进式深度**: quick 模式仅用本地分析，deep 模式才生成元提示提交大模型
2. **零外部依赖**: 所有脚本仅使用 Python 标准库
3. **JSON 输出**: 所有组件输出 JSON，便于程序化集成
4. **可组合性**: 组件可独立使用，也可串联成流水线
5. **场景驱动**: 73个场景覆盖常见育儿困境，预处理器自动匹配
6. **理念一致**: 所有元提示都融入"觉察→接纳→暂停→选择"的核心路径

---

## 文件清单

```
scripts/
├── prompt_optimizer.py      # 提示词优化器
├── logic_normalizer.py      # 逻辑规范器
├── quality_checker.py       # 质量检查器
└── scenario_preprocessor.py # 场景预处理器

tools/
└── meta-prompt-system.md    # 本文档
```
