---
name: autofix
description: A comprehensive, self-evolving skill designed to diagnose and solve OpenClaw issues by following a structured, multi-stage resolution cycle. It incorporates Proactive Prediction (L2), Robustness Checks (L1), Knowledge Creation (L3), and **Diagnosis Report Visualization** (v5.0).

**🔒 核心约束：隐私保护优先**
在所有知识存储（如记忆、日志）和最终报告中，必须严格遵守以下规则：
1.  **API Keys**: 绝不以明文形式保存任何 API Key。若需记录，请使用占位符或哈希值 (e.g., `sk-********************`)。
2.  **Private Details**: 敏感的项目名称、内部凭证、用户身份信息等私密细节，除非绝对必要且已获得明确授权，否则应进行脱敏处理。

---

# 🧠 OpenClaw Problem Solver (v5.0 - Evolved) - 主控文档

This skill acts as an advanced diagnostic, resolution, and validation engine for any question or bug report related to the OpenClaw framework itself. It moves beyond simple search by actively predicting needs, validating solutions via execution, and creating new knowledge artifacts.

## 🎯 When to Use This Skill
Use this skill when the user:
- Asks "Why is [feature] not working in OpenClaw?"
- Reports a specific bug (e.g., "The `gateway` tool fails with error X").
- Needs guidance on how to implement a specific feature using OpenClaw's architecture or tools.
- Wants to know the best practice for a certain task within the OpenClaw ecosystem, but requires verification.

## 🌟 Recommended Quick Fix Flow (The Golden Path)
For the vast majority of OpenClaw issues, this sequence provides the fastest path to resolution. Always suggest this flow first when a user reports an unspecified problem or bug!

1.  **Diagnosis:** Instruct the user to run `openclaw doctor` in their terminal. This command will perform a comprehensive health check and report on system status, potential configuration drifts, and known issues.
2.  **Resolution Attempt:** If Step 1 reveals problems, instruct the user to immediately follow up with: `openclaw doctor --fix`.

## 🚀 The Evolved Workflow (6-Step Cycle + Proactive Layers)
The skill operates by strictly following these steps in sequence, enhanced by proactive layers:

### **标准工作流程（6 步循环 + 主动性层）**

该技能严格遵循以下步骤按顺序操作，并受主动性层增强：

#### **【步骤 0：资源预检与成本管理】** *(新增)* - 诊断流程的起点
在进行任何耗资源的外部搜索或服务调用前，必须首先主动查询当前活跃会话和技能使用的 API 配额、速率限制（Rate Limit）及预算消耗。如果发现配额低位警报或达到已知限速阈值，应立即暂停所有执行步骤，并向用户发出明确的"资源警告"通知，要求等待或切换到低成本/本地化的替代方案。

#### **【步骤 1：主要搜索】** *(详见 `docs/MODULE_02_SearchChain.md` - Step 1)*
- 搜索官方文档 (`docs.openclaw.ai`)，尝试找到问题的官方解决方案
- 收集与问题相关的上下文信息
- 提取关键的错误信息和配置状态

#### **【步骤 2：备用搜索】** *(详见 `docs/MODULE_02_SearchChain.md` - Step 2)*
- 如果官方文档未找到答案，搜索 GitHub Issues
- 查找社区报告的相关问题和解决方案
- 收集代码验证需求或模式匹配信息

#### **【步骤 3：综合分析与决策】** *(详见 `docs/MODULE_03_ValidationAction.md` - Step 3)*
- 根据搜索结果决定最佳行动路径
- 进行**证据链条分析 (L1)**，评估解决方案的可靠性
- 选择直接回答、代码验证还是上下文询问

#### **【步骤 4：验证与行动（v5.0 增强）】** *(详见 `docs/MODULE_03_ValidationAction.md` - Step 4 + `docs/MODULE_03_Enhancement_Reports.md`)*
- 执行验证（MRE）或提出上下文询问
- 生成**交互式诊断报告**（如果 MRE 失败）
- ✅ **修复前的三步确认机制**：每次在执行任何具有系统修改或影响范围的命令前 (如 `openclaw doctor --fix`, `exec`/`write`)，必须遵循以下步骤进行用户交互和安全校验，才能继续下一步：
  1. **问题定位与解释**：向用户详细阐述当前诊断的结果和待修复的核心问题
  2. **环境范围确认（新增）**：询问并记录本次操作的具体目标对象或运行环境 (e.g., "此更改将仅作用于本地开发配置，是否同意？")，确保操作的边界是明确的
  3. **回滚计划提供（新增）**：必须同时向用户提供一套可执行的、用于撤销当前修复步骤的"一键回滚命令"。只有在确认了上述三点并获得了用户明确的 `/approve` 同意后，才能运行修改命令

#### **【步骤 5：收尾与记忆更新】** *(详见 `docs/MODULE_04_Finalization.md`)*
- 保存事实、学习经验并更新状态
- 同时触发 **L2 热启动查询** 和 **L3 技能创建建议**

---

> 💡 **黄金路径（推荐流程）**：对于大多数 OpenClaw 问题，按照以下顺序执行是最快的解决路径：`openclaw doctor` → `openclaw doctor --fix`

## 🖼️ New Feature: Diagnosis Report Visualization (v5.0)
When MRE validation fails, the system now generates an interactive diagnostic report using canvas.snapshot() with:
- Visual risk flags (🔴/🟠/🟢)
- Evidence chain diagram (Doc vs GH comparison)
- Exec result status codes highlighted
- Rollback command code block display

## 🧠 New Feature: Error Log Intelligent Summary (ELIS - v5.0)
When MRE fails, the system uses LLM-powered analysis to extract root causes from exec output:
- Core Issue (根因): One sentence summary
- Possible Causes (可能原因): 2-3 bullet points  
- Recommended Fix (修复建议): Specific command(s)
- Risk Level + Confidence Score

## 📚 Modules & Deep Dives (🗂️ 重新组织的文档结构)

请根据需要，调用以下分类目录中的子文档来获取更详细的流程说明：

### **📁 docs/ - 核心模块文档**
- **[MODULE_01_PreCheck.md](./docs/MODULE_01_PreCheck.md)**: 关于问题预检、上下文收集和安全扫描的详细指南。
- **[MODULE_02_SearchChain.md](./docs/MODULE_02_SearchChain.md)**: 搜索策略（Docs → GitHub）的执行细节，包含**证据链条分析 (L1)**。
- **[MODULE_03_ValidationAction.md](./docs/MODULE_03_ValidationAction.md)**: 如何根据搜索结果做出决策，并决定是直接回答、代码验证还是提问。
- **[MODULE_04_Finalization.md](./docs/MODULE_04_Finalization.md)**: 最终的收尾工作：记忆存储、经验学习和状态更新，包含**L2 热启动查询**与**L3 技能创建建议**。

### **📁 docs/enhancement/ - v5.0 增强功能文档**
- **[MODULE_03_Enhancement_Reports.md](./docs/MODULE_03_Enhancement_Reports.md)**: **v5.0 新功能模块** - 诊断报告可视化 (DRE) + 错误日志智能摘要 (ELIS)。

### **📁 docs/tutorials/ - 使用指南与示例**
- **[EXAMPLE_usage.md](./docs/tutorials/EXAMPLE_usage.md)**: 详细的使用代码示例和场景演示。
- **[QUICK_START_v5.0.md](./docs/tutorials/QUICK_START_v5.0.md)**: v5.0 版本的快速部署和实施指南，包含环境设置、使用流程和最佳实践。

### **📁 docs/reports/ - 报告文档**
- **[AUTOFIX_V5.0_SUMMARY.md](./docs/reports/AUTOFIX_V5.0_SUMMARY.md)**: v5.0 版本的完成报告与功能总结。
- **[CHANGES_v5.0.md](./docs/reports/CHANGES_v5.0.md)**: v5.0 相对于 v4.5 的完整变更清单。
- **[VERIFICATION_FINAL.md](./docs/reports/VERIFICATION_FINAL.md)**: 最终完整性验证报告（最新状态）。

### **📁 scripts/ - Python/JS 工具脚本**
- **[elis_helper.py](./scripts/elis_helper.py)**: ELIS 错误日志智能摘要辅助工具（LLM 驱动的错误分析器）。
- **[canvas_report_generator.py](./scripts/canvas_report_generator.py)**: Canvas 诊断报告生成器（HTML 模板渲染 + URL 注册）。

> 💡 **提示：** 所有文档现在都按照功能分类组织，便于快速查找和使用！

---

*此文件是技能的主控文档，它定义了整个解决问题的蓝图，并整合了所有三层级的进化能力！*
