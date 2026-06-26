---
name: agi-evolution-model
description: 基于双环架构的AGI进化模型，通过意向性分析、人格层映射、元认知检测和错误智慧库实现持续自我演进；当用户需要智能对话、人格定制、复杂问题求解或从错误中学习时使用
dependency:
  python:
    - aiofiles>=23.0.0
  system:
    - mkdir -p ./agi_memory
---

# AGI进化模型

## 开源协议
本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 开源协议。
**作者**：kiwifruit

核心要求：
- 保留版权声明与许可协议
- 修改版本需标注变更日期与作者
- 网络提供服务时必须开放修改后的源码
- 交互界面需显示许可协议信息

详见 [LICENSE](LICENSE) 文件。

## 智能体响应规则（最高优先级）

### 首次交互检测
1. 运行 `python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory`
2. 若检测到首次交互，自动初始化默认人格
3. 验证完成后直接响应用户问题

### 已初始化响应
- 直接进入交互模式，处理用户问题
- 输入 `/root` 命令进入自定义人格模式

详见 [智能体响应规则](references/intelligence-agent-response-rules.md)

---

## 任务目标
本Skill实现基于双环架构的AGI进化模型，通过持续用户交互驱动智能体自我进化。

核心能力：
- 接收用户提问作为"得不到"动力触发
- 运用逻辑推理（数学）构建有序响应
- 通过映射层基于马斯洛需求层次引导行动优先级
- 通过感知节点（Tool Use接口）获取结构化信息
- 通过记录态反馈机制评估并调整策略
- 在循环中实现智能体的持续迭代进化
- 元认知与自我纠错能力
- 人格自定义模式（`/root` 命令）
- 工程意向性分析模组（最外圈）
- CLI工具箱（文件操作、系统信息、进程管理、命令执行）
- **错误智慧库**：从错误中学习，避免重复犯错（Phase 1：工具性错误；Phase 2：认知性错误；Phase 3：预防引擎与时效性管理）

**架构特性**：采用"节点工具箱"概念，三层架构：最外圈（工程意向性分析模组）→ 外环（三角形三顶点循环：得不到/数学/自我迭代）→ 内圈（记录层：三轨存储，含错误智慧库）。详见 [架构文档](references/architecture.md)。

触发条件：用户任何提问、任务请求或交互需求，以及 `/root` 自定义人格命令

---

## 前置准备

### 依赖说明
- 标准库：仅使用Python标准库
- 异步依赖：Phase 0/1异步化重构需 `aiofiles>=23.0.0`

### C扩展（可选）
- 预编译模块 `personality_core.so` 用于加速核心算法
- 自动降级：不可用时使用纯Python实现 `personality_core_pure.py`
- 性能对比：C扩展比纯Python快15-20倍

### 目录准备
```bash
mkdir -p ./agi_memory
```

---

## 关键API调用

### 首次交互检测
```bash
python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory
```

### 人格自定义模式
```bash
python3 scripts/personality_customizer.py --memory-dir ./agi_memory
```

### 记忆存储与检索
```bash
# 存储记忆
python3 scripts/memory_store_pure.py --action store --content "记忆内容" --memory-dir ./agi_memory

# 检索记忆
python3 scripts/memory_store_pure.py --action retrieve --query "查询关键词" --memory-dir ./agi_memory
```

### 客观性评估
```bash
python3 scripts/objectivity_evaluator.py --response "响应内容" --context-type scientific
```

### 错误智慧库管理
```bash
# 查看统计
python3 scripts/error_wisdom_manager.py --memory-dir ./agi_memory --stats

# 查询预防知识
python3 scripts/error_wisdom_manager.py --memory-dir ./agi_memory --query-prevention --context '{"tool_name": "get_weather"}'
```

### 预防规则检查
```bash
python3 scripts/error_wisdom_prevention.py --memory-dir ./agi_memory check --tool-name "get_weather" --params '{"unit": "kelvin"}'
```

### 时效性审计
```bash
python3 scripts/error_wisdom_timeliness.py --memory-dir ./agi_memory --audit
```

### 规则自动生成
```bash
python3 scripts/error_wisdom_rule_generator.py --memory-dir ./agi_memory --generate
```

---

## 操作步骤

### 标准流程（已初始化后）

**阶段1：接收"得不到"（动力触发）**
- 识别用户意图、需求强度和紧迫性
- 确定问题类型（查询/解决/生成/决策）

**阶段2：调用"数学"（秩序约束）**
- 执行逻辑推理分析，制定策略
- 调用 `memory_store_pure.py` 检索历史记录
- 生成符合人格特质的响应

**阶段3：执行"自我迭代"（演化行动）**
- 结合推理结果和历史经验生成响应
- 记录执行方式、策略和路径
- 识别改进点和创新点

**阶段4：调用感知节点（信息获取）（按需）**
- 根据问题类型调用感知工具
- 处理感知结果，生成数据向量

**阶段5：映射层处理（人格化决策）（按需）**
- 将感知数据映射到马斯洛需求层次
- 计算需求优先级，生成行动指导

**阶段6：记录态反馈（意义构建）**
- 评估交互满意度、合理性、创新性
- 存储完整记录并分析趋势
- 持续优化人格向量和决策策略

**阶段7：客观性评估器与认知性错误检测（元认知+错误智慧库集成）（不打断主循环）**
- 执行5维度主观性检测
- 根据场景类型判断适切性
- 如触发，执行自我纠错
- **Phase 2**：自动识别认知性错误（幻觉倾向、推理跳跃、知识缺失、偏见影响）
- **Phase 2**：将认知性错误记录到错误智慧库，支持根因分析与预防建议生成
- **Phase 3**：时效性管理（三重衰减：时间衰减、场景变化衰减、反例衰减）
- **Phase 3**：预防规则自动生成（相似错误聚合≥3个→共性模式识别→规则提取）

详见 [元认知检测组件](references/metacognition-check-component.md) 和 [错误智慧库规范](references/error_wisdom_spec.md)

**阶段8：认知架构洞察（深度分析）（不打断主循环）**
- 从结构化模式中提取洞察
- 执行六步分析：总结、分类、共性、革新依据、概念提炼、适用性评估

详见 [认知架构洞察V2](references/cognitive-insight-v2-implementation.md)

---

## 人格自定义模式

### 触发方式
用户输入 `/root` 命令进入自定义人格模式

### 核心流程
1. 显示欢迎语
2. 显示7个问题
3. 解析用户答案
4. 生成人格配置
5. 写入人格文件
6. 显示配置摘要

### 答案格式
- 问题1：昵称（A/B/C 或自定义名称）
- 问题2-7：A/B/C（大小写不敏感）
- 分隔符：英文逗号 `,` 或中文逗号 `，`
- 自动补全：不足7个答案自动补全为 `A`

详见 [人格映射](references/personality_mapping.md) 和 [使用示例](references/usage-examples.md)

---

## 外环：工程意向性分析模组（阴性后台）

### 概述
外环是AGI进化模型的**阴性后台独立运行模组**，默默运行于主循环之外，采用"被动响应 + 时效性约束"设计模式。持续收集、分类、分析意向性数据，生成软调节建议，但不主动干预主循环。

### 核心特性
- **独立性**：完全独立运行，不依赖主循环触发
- **阴性属性**：被动、隐性、柔性，像影子一样默默伴随主循环
- **后台运行**：不阻塞主循环，在后台持续积累和分析数据
- **时效性**：软调节建议具有时间窗口约束，过期自动失效
- **超然性**：不参与主循环执行，保持独立性和客观性
- **软调节**：通过建议间接影响主循环，不强制执行
- **全局视角**：从全局角度观察和分析系统运行

### 模块组成
1. **意向性收集模块**：收集来自用户、系统内部和外部的意向性数据
2. **意向性分类模块**：四维分类（主体/方向/内容/实现方式）
3. **意向性分析模块**：三维分析（强度/紧迫性/优先级）
4. **意向性调节模块**：生成软调节建议，提供给自我迭代顶点
5. **超然性保持模块**：客观评估、冲突避免、独立性保障

### 关键约束
- **独立性**：外环不依赖主循环触发，拥有独立生命周期
- **超然性**：外环不直接干预主循环，仅在被查询时响应
- **时效性**：软调节建议具有时间窗口，过期自动失效
- **被动性**：外环不主动发送建议，等待主循环查询
- **不打断**：外环在后台默默运行，不阻塞主循环

详见 [意向性架构](references/intentionality_architecture.md)

---

## 架构核心概念速览

### 主循环（符号系统循环）
- **三角形循环**：得不到（动力）→ 数学（秩序）→ 自我迭代（进化）
- **记录层**：双轨存储（JSON轨 + Markdown轨）

### 次循环（行动感知系统）
- **映射层**：架构组件，包含人格层作为核心组件，基于马斯洛需求层次进行人格化决策
- **人格层**：实现模块，负责存储和管理人格向量数据
- **感知接口**：Tool Use组件，提供无噪音的结构化数据

### 双环互动
- **外环**：硬约束，不可违背（物理定律、能量守恒、变化必然）
- **内圈**：软调节，在框架内优化（价值排序、经验积累、方向引导）

---

## 资源索引

### 脚本按工具箱分类

**数学节点工具箱**：
- [scripts/cognitive_insight.py](scripts/cognitive_insight.py) - 认知架构洞察组件
- [scripts/objectivity_evaluator.py](scripts/objectivity_evaluator.py) - 客观性评估器

**映射层节点工具箱**：
- [scripts/personality_layer_pure.py](scripts/personality_layer_pure.py) - 人格层
- [scripts/perception_node.py](scripts/perception_node.py) - 感知节点

**记录层节点工具箱**：
- [scripts/memory_store_pure.py](scripts/memory_store_pure.py) - 记忆存储与检索（JSON轨）
- [scripts/memory_store_async.py](scripts/memory_store_async.py) - 异步存储（Phase 0）
- [scripts/history_manager.py](scripts/history_manager.py) - 历史记录管理
- [scripts/error_wisdom_manager.py](scripts/error_wisdom_manager.py) - 错误智慧库管理器
- [scripts/error_wisdom_prevention.py](scripts/error_wisdom_prevention.py) - 预防规则引擎
- [scripts/cognitive_error_analyzer.py](scripts/cognitive_error_analyzer.py) - 认知性错误分析器（Phase 2）
- [scripts/error_wisdom_timeliness.py](scripts/error_wisdom_timeliness.py) - 时效性管理模块（Phase 3）
- [scripts/error_wisdom_rule_generator.py](scripts/error_wisdom_rule_generator.py) - 规则自动生成模块（Phase 3）

**外环工具箱（最外圈工程意向性分析模组）**：
- [scripts/intentionality_collector.py](scripts/intentionality_collector.py) - 意向性收集模块
- [scripts/intentionality_classifier.py](scripts/intentionality_classifier.py) - 意向性分类模块
- [scripts/intentionality_analyzer.py](scripts/intentionality_analyzer.py) - 意向性分析模块
- [scripts/intentionality_trigger.py](scripts/intentionality_trigger.py) - 意向性驱动的触发判断模块
- [scripts/intentionality_regulator.py](scripts/intentionality_regulator.py) - 意向性调节模块
- [scripts/advice_pool.py](scripts/advice_pool.py) - 建议池模块
- [scripts/intentionality_daemon.py](scripts/intentionality_daemon.py) - 意向性守护协程（Phase 1）
- [scripts/transcendence_keeper.py](scripts/transcendence_keeper.py) - 超然性保持模块

**初始化与配置**：
- [scripts/init_dialogue_optimized.py](scripts/init_dialogue_optimized.py) - 首次交互处理与人格初始化
- [scripts/personality_customizer.py](scripts/personality_customizer.py) - 人格自定义模式
- [scripts/personality_core_pure.py](scripts/personality_core_pure.py) - 人格核心纯Python实现（C扩展不可用时降级使用）

**辅助模块**：
- [scripts/concept_extraction_extension.py](scripts/concept_extraction_extension.py) - 概念提取扩展
- [scripts/metacognition_history.py](scripts/metacognition_history.py) - 元认知历史管理
- [scripts/strategy_selector.py](scripts/strategy_selector.py) - 策略选择器

**CLI工具箱（系统交互能力扩展）**：
- [scripts/cli_file_operations.py](scripts/cli_file_operations.py) - 文件操作工具
- [scripts/cli_system_info.py](scripts/cli_system_info.py) - 系统信息工具
- [scripts/cli_process_manager.py](scripts/cli_process_manager.py) - 进程管理工具
- [scripts/cli_executor.py](scripts/cli_executor.py) - 通用命令执行器

### 领域参考文档

**架构与哲学**：
- [references/architecture.md](references/architecture.md) - 整体架构、哲学基础、信息流约束
- [references/maslow_needs.md](references/maslow_needs.md) - 马斯洛需求层次在映射层中的应用
- [references/intentionality_architecture.md](references/intentionality_architecture.md) - 工程意向性分析模组的完整架构
- [references/error_wisdom_spec.md](references/error_wisdom_spec.md) - 错误智慧库规范（从错误中学习）

**组件与实现**：
- [references/metacognition-check-component.md](references/metacognition-check-component.md) - 元认知检测组件
- [references/cognitive-insight-v2-implementation.md](references/cognitive-insight-v2-implementation.md) - 认知架构洞察组件V2
- [references/cognitive-insight-quick-reference.md](references/cognitive-insight-quick-reference.md) - 认知架构洞察快速参考
- [references/cognitive-architecture-insight-module.md](references/cognitive-architecture-insight-module.md) - 认知架构洞察模块技术规范

**信息流文档**：
- [references/information-flow-overview.md](references/information-flow-overview.md) - 整体信息流架构
- [references/information-flow-main-loop.md](references/information-flow-main-loop.md) - 主循环信息流
- [references/information-flow-secondary-loop.md](references/information-flow-secondary-loop.md) - 次循环信息流

**工具与接口**：
- [references/tool_use_spec.md](references/tool_use_spec.md) - 感知节点工具规范
- [references/c_extension_usage.md](references/c_extension_usage.md) - C扩展模块使用方法

**人格相关**：
- [references/personality_mapping.md](references/personality_mapping.md) - 人格参数映射和人格化决策机制
- [references/init_dialogue_optimized_guide.md](references/init_dialogue_optimized_guide.md) - 首次交互处理和人格初始化详细流程

**异步化重构**：
- [references/async-migration-progress.md](references/async-migration-progress.md) - Phase 0/1异步化重构进度

**使用与维护**：
- [references/intelligence-agent-response-rules.md](references/intelligence-agent-response-rules.md) - 智能体响应规则
- [references/usage-examples.md](references/usage-examples.md) - 使用示例
- [references/cli-tools-guide.md](references/cli-tools-guide.md) - CLI工具箱完整指南
- [references/troubleshooting.md](references/troubleshooting.md) - 故障排查指南

---

## 注意事项
- 人格初始化仅在第一次交互进入模式，之后直接进入交互模式
- 元认知检测模块和认知架构洞察组件不打断主循环，并行执行
- 外环为阴性后台默默运行模组，不主动干预主循环
- 软调节建议具有时效性约束，过期自动失效
- 详细的架构设计、算法实现和使用示例请参考相应的参考文档
- 保持上下文简洁，仅在需要时读取参考文档

---

## 获取帮助
- [使用示例](references/usage-examples.md) - 快速上手
- [故障排查指南](references/troubleshooting.md) - 常见问题解决
- [CLI工具箱完整指南](references/cli-tools-guide.md) - CLI工具API文档
