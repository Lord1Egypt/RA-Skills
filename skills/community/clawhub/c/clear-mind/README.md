# Clear-Mind Skill

## Project Introduction

Clear-Mind is an agent memory file maintenance and optimization system designed specifically for managing AI assistant's MEMORY.md files. As your AI agent (openclaw) is used longer, a large number of invalid files accumulate in the memory file (memory.md), causing the agent to become increasingly stupid and enter a brain fog state. This skill is the agent's meditation moment. Its core functions include:

- **Factual Information Migration**: Migrates specific factual information (such as project details, portfolio, historical events, etc.) from MEMORY.md to a dedicated facts/ directory
- **Core Rules Preservation**: Ensures core behavioral rules, capability definitions, and tool descriptions remain in MEMORY.md
- **Quick Index Construction**: Maintains a Quick Index table for easy navigation between core agent memory files and fact files
- **Security Verification Mechanism**: Ensures the safety and accuracy of the migration process through multiple verification steps and user confirmation

## Applicable Scenarios

Use the Clear-Mind skill when:

- MEMORY.md accumulates a large amount of factual information (such as project details, technical details, etc.)
- Regular agent memory file cleanup and maintenance is needed
- You want to optimize the agent memory file structure to improve AI assistant performance and reliability

## Update Notes

### 2026-03-14 Update

**Major Improvements**:

1. **Enhanced Safety and Controllability**
   - Added clear classification guidelines to clearly define what content must remain in MEMORY.md
   - Added the safety principle of "When in doubt, keep in MEMORY.md"
   - Implemented strict content classification standards

2. **Optimized Workflow**
   - Added migration plan creation step
   - Added user verification step to obtain explicit confirmation before migration
   - Strengthened content analysis and classification process

3. **Improved Verification Mechanism**
   - Implemented comprehensive verification process, including content integrity check and safety verification
   - Added user review step to ensure users understand all changes
   - Added final safety check to ensure core information is not affected

4. **Added Safety Metrics**
   - Defined key safety metrics to ensure 100% of core behavioral rules, capability definitions, tool descriptions, and installed skills information are preserved
   - Clarified success criteria, emphasizing the removal of factual bloat while preserving core capabilities

## Directory Structure

```
clear-mind/
├── SKILL.md          # Skill definition and workflow
├── README.md         # Project introduction and update notes
└── .gitignore        # Git ignore file configuration
```

## Usage Method

1. Activate the Clear-Mind skill when factual information accumulates in MEMORY.md
2. The system will analyze the current agent memory file status and create a migration plan
3. You need to confirm the migration plan before the system executes it
4. After migration completion, the system will perform comprehensive verification and report results to you
5. You can quickly access information migrated to the facts/ directory through the Quick Index

## Safety Measures

Clear-Mind skill has multiple safety mechanisms:

- **Conservative Migration Strategy**: When in doubt, keep information in MEMORY.md
- **User Confirmation**: Obtain explicit user approval at key steps
- **Comprehensive Verification**: Ensure core rules and capabilities are not affected
- **Rollback Mechanism**: Provide complete rollback capability to restore previous states when needed

These measures ensure that Clear-Mind skill optimizes agent memory files without affecting the core functions and capabilities of the AI assistant.

# Clear-Mind Skill

## 项目介绍

Clear-Mind是一个agent记忆文件维护和优化系统，专为管理AI助手的MEMORY.md文件而设计。当你的AI agent（openclaw）使用越久，会有大量无效文件堆积在记忆文件（memory.md）中，造成agent越来越笨，进入脑雾状态。这个skill是agent的冥想时刻。它的核心功能是：

- **事实性信息迁移**：将具体的事实性信息（如项目详情、投资组合、历史事件等）从MEMORY.md迁移到专门的facts/目录
- **核心规则保留**：确保核心行为规则、能力定义和工具描述等重要信息保留在MEMORY.md中
- **快速索引构建**：维护Quick Index表，方便在核心agent记忆文件和事实文件之间快速导航
- **安全验证机制**：通过多重验证步骤和用户确认，确保迁移过程的安全性和准确性

## 适用场景

当以下情况发生时，应该使用Clear-Mind技能：

- MEMORY.md中积累了大量事实性信息（如项目详情、技术细节等）
- 需要定期进行agent记忆文件清理和维护
- 希望优化agent记忆文件结构，提高AI助手的性能和可靠性

## 更新说明

### 2026-03-14 更新

**主要改进**：

1. **增强安全性和可控性**
   - 添加了明确的分类指南，清晰界定哪些内容必须保留在MEMORY.md中
   - 增加了"当不确定时，保留在MEMORY.md中"的安全原则
   - 实现了严格的内容分类标准

2. **优化工作流程**
   - 添加了迁移计划创建步骤
   - 增加了用户验证环节，在迁移前获得明确确认
   - 强化了内容分析和分类流程

3. **完善验证机制**
   - 实现了全面的验证流程，包括内容完整性检查和安全验证
   - 添加了用户审查步骤，确保用户了解所有更改
   - 增加了最终安全检查，确保核心信息未受影响

4. **添加安全指标**
   - 定义了关键安全指标，确保100%的核心行为规则、能力定义、工具描述和已安装技能信息得到保留
   - 明确了成功标准，强调移除事实性信息膨胀的同时保留核心能力

## 目录结构

```
clear-mind/
├── SKILL.md          # 技能定义和工作流程
├── README.md         # 项目介绍和更新说明
└── .gitignore        # Git忽略文件配置
```

## 使用方法

1. 当MEMORY.md中积累了事实性信息时，激活Clear-Mind技能
2. 系统会分析当前agent记忆文件状态，创建迁移计划
3. 您需要确认迁移计划，系统才会执行迁移
4. 迁移完成后，系统会进行全面验证并向您报告结果
5. 您可以通过Quick Index快速访问迁移到facts/目录的信息

## 安全保障

Clear-Mind技能设计了多重安全保障机制：

- **保守迁移策略**：当不确定时，保留信息在MEMORY.md中
- **用户确认**：在关键步骤获得用户明确批准
- **全面验证**：确保核心规则和能力未受影响
- **回滚机制**：提供完整的回滚能力，在需要时恢复之前的状态

这些措施确保了Clear-Mind技能在优化agent记忆文件的同时，不会影响AI助手的核心功能和能力。