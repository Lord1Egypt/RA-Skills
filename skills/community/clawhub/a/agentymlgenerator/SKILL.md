---  
name: agent-yml-generator  
description: 生成可直接导入 Dify 1.3.1 平台的 Agent 工作流 YAML 配置文件。当用户描述业务需求、SOP流程、或要求生成 Dify workflow/agent YAML 时，必须使用本 skill。触发词包括：生成yml、生成yaml、dify工作流、agent yaml、工作流配置、导入dify、生成工作流、SOP转工作流等。即使用户只是描述业务流程或粘贴 SOP 文档，也应主动使用本 skill 为其生成可运行的 YAML。  
---  
  
# Agent YML Generator  
  
将业务需求/SOP描述转化为可直接导入 Dify 1.3.1 平台运行的工作流 YAML 配置。  
  
## 输入信息收集  
  
首先确认以下两点：  
1. **业务需求描述**：SOP文档、需求文字、流程说明（任意形式）  
2. **工作流类型**：  
   - `workflow`（工作流）：有明确开始/结束，适合自动化批处理任务  
   - `advanced-chat`（对话流）：适合对话式交互场景  
  
如果用户没有明确说明类型，根据业务描述推断，并告知用户你的判断。  
  
---  
  
## 执行步骤  
  
按以下 **4个阶段** 依次执行，不可跳过：  
  
### 阶段一：步骤拆分（生成结构化 JSON 工作流方案）  
  
使用 `references/step-split-prompt.md` 中的 System Prompt，将业务需求转化为结构化 JSON 工作流方案。  
  
**输出格式**：标准 JSON 数组，包含每个节点的完整信息。  
  
详见：`references/step-split-prompt.md`  
  
---  
  
### 阶段二：生成 Dify YAML  
  
使用 `references/yaml-gen-prompt.md` 中的规范，将阶段一的 JSON 方案转换为完整的 Dify 1.3.1 YAML。  
  
**关键要求**：  
- 工作流类型：`workflow` 时 `mode: workflow`，`advanced-chat` 时 `mode: advanced-chat`  
- YAML 版本：`version: 0.2.0`（内部平台版本，对应外部 Dify 1.3.1）  
- 所有 LLM 节点 provider 只用：`openai` 或 `gemini`  
- 仅输出纯 YAML，无任何解释文字  
  
详见：`references/yaml-gen-prompt.md`  
  
---  
  
### 阶段三：格式与语法修正  
  
使用 `references/yaml-fix-prompt.md` 的规则，对阶段二的 YAML 进行全面检查和修复：  
  
**必查项**：  
- YAML 语法：冒号后空格、缩进（4空格，禁Tab）、特殊字符转义、闭合完整性  
- Dify 1.3.1 规范：节点 type 为小写（如 `code_executor`，不是 `code-executor`）、无 1.6 版本字段（`loop_type`、`table_output_format` 等）  
- connections 链路：所有节点连线完整，无孤立节点  
- 参数传递：每个节点（除 Start）的入参均来自前序节点  
  
详见：`references/yaml-fix-prompt.md`  
  
---  
  
### 阶段四：最终润色与输出  
  
做最后检查，确保：  
1. `version` 字段值为 `0.2.0`  
2. 所有节点有 `position`、`height`、`width` 字段（合法数字）  
3. `data.title` 和 `data.desc` 不为空字符串  
4. 节点 type 合法值（`start`/`document_extractor`/`llm`/`branch`/`answer`/`code`/`end`等）  
5. 对话流（advanced-chat）末尾用 `answer` 节点；工作流（workflow）末尾用 `end` 节点  
6. 无 `---` 或 `----` 分隔符（会导致平台报错）  
7. 输出完整 YAML，无任何说明文字  
  
---  
  
## 输出规范  
  
最终输出：  
1. 简要说明工作流结构（节点数量、主要流程）  
2. 完整的 YAML 代码块（用 ```yaml 包裹）  
3. 提示用户直接复制导入 Dify 1.3.1 平台  
  
---  
  
## 注意事项  
  
- **严禁**输出 YAML 之外的内容（无解释、无注释、无标题）在 YAML 代码块内  
- **严禁**使用 1.6 版本字段：`loop_type`、`table_output_format`、`yangyaofei/vllm` provider  
- LLM 节点变量引用格式：`${变量名}`（不支持 `${节点ID.变量名}`）  
- Branch 节点条件只用简化表达式：`${变量名} != ""`、`${变量名} == "success"`（禁用 `len()` 等复杂函数）  
- 遇到【迭代】/【循环】等复杂节点，可用多个串行 LLM 节点替代  
