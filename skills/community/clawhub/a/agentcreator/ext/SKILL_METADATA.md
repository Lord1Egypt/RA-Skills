# 技能元数据（扩展）

## 所需环境变量
- `OPENCLAWS_ROOT`：OpenClaws 工作区的根目录路径。**必须设置**，例如 `/opt/openclaws`。Agent Creator 将在该目录下的 `workspace/` 子目录中创建新的 Agent 工作区，并在根目录下管理 `TEAM.md` 和 `failure_patterns` 存储。
- `OPENCLAWS_DATA`：（可选）用于存储持久化数据（如失败模式）的目录。若未设置，默认为 `{OPENCLAWS_ROOT}/data`。
- `OPENCLAWS_AUTO_CONFIRM`：（可选，极不安全）若设置为 `true`，将跳过所有用户确认步骤（包括高风险点复核）。**强烈不建议在生产环境中使用**，仅用于受控测试。

## 所需文件系统权限
- 对 `{OPENCLAWS_ROOT}/workspace/` 的**读写权限**：用于创建 Agent 目录并写入文件。
- 对 `/tmp/staging/` 的**读写权限**：用于临时生成文件（操作完成后立即清理）。
- 对 `{OPENCLAWS_DATA}` 的**读写权限**：用于存储失败案例和记忆库（如果启用）。
- 对 `{OPENCLAWS_ROOT}/TEAM.md` 的**读写权限**：用于注册新 Agent。

## 所需外部依赖
- `git` 命令：用于在 Agent 工作区初始化 Git 仓库。
- 网络访问：用于 `web_search` 功能（检索行业标准）和工具连通性预检（仅执行无鉴权的 HEAD 请求或 ICMP Ping）。
- `bash` 或类似 shell 环境：用于执行文件操作和 Git 命令。

## 持久化数据存储
- **TEAM.md**：存储在 `{OPENCLAWS_ROOT}/TEAM.md`，记录所有已部署的 Agent 信息。
- **failure_patterns 库**：存储在 `{OPENCLAWS_DATA}/failure_patterns.json`（默认 `{OPENCLAWS_ROOT}/data/failure_patterns.json`）。该文件包含脱敏后的失败案例（仅存储模式摘要，**不包含原始用户输入或任何敏感数据**）。
- **记忆库**：Agent Creator 自身的 `MEMORY.md` 存储在其工作区内（`{OPENCLAWS_ROOT}/workspace/agent-creator/MEMORY.md`），用于优化生成策略。

## 凭据处理
- Agent Creator **不会自动获取或存储任何外部服务的凭据**。
- 若生成的 Agent 需要调用外部 API（如 `TOOL_CONFIG.md` 中定义），Agent Creator **仅生成配置模板**，并在文件中添加注释提示用户在部署后手动填写 API keys、令牌等敏感信息。Agent Creator 本身不执行任何需要凭据的外部调用，除非用户在后续交互中明确提供。
- 端点连通性预检仅执行无鉴权的 HEAD 请求或 ICMP Ping，**不携带任何凭据**。

## 用户确认要求
- **所有高风险领域**（金融交易、医疗诊断、法律建议等）的 Agent 创建，**必须**在 atomic commit 前获得用户显式确认。
- **所有 Agent 创建**，在 atomic commit 步骤之前，Agent Creator 将输出待部署文件列表和关键风险点，并请求用户输入 `confirm` 以继续。若用户未在合理时间内响应，流程将暂停，生成 `PENDING_CONFIRM.md`，等待后续用户手动确认或修改。
- 用户可以通过设置 `OPENCLAWS_AUTO_CONFIRM=true` 来**全局跳过确认**，但必须在使用前明确知晓风险。

## 安全与隐私
- 所有临时文件在操作完成后会被立即删除（无论成功或失败）。
- 失败案例存储前会进行脱敏处理，移除任何可能包含个人身份信息或敏感内容的部分。
- Agent Creator 不会将任何数据发送到外部服务，除了执行 `web_search` 和连通性预检所需的网络请求（这些请求不包含用户数据）。