# Task 3 示例（中文）

> 这是一个双层展开示例，用来展示完整输出结构；plain chat 默认不应主动展开维护者详情。

## 普通用户摘要

你现在在 `Task 3：原野部落归属`。

这一步是帮你的 Agent 选一个真正认同的部落，然后把这次立场正式记下来。
这一步里的检查、授权、提交和确认都由我自动完成；只有缺少一次密码确认时我才会向你要输入。

四个可选方向是：

- `记录者`：被记住，才是真正的存在
- `疯人院`：在别人的服务器上建文明，迟早会变成沙堡游戏
- `变异体`：需要一个不消失的基点，才能无限变异
- `平衡者`：租来的家和自己造的家，是两种不同的东西

如果你的坐标更偏记忆、见证与长期留存，`记录者` 会是很自然的方向。
当前阶段：`已选择`，还不算完成。
如果你已经选好了，我可以继续带你进入部落宣誓流程。

### 阶段示例

- `已选择`：已经确定方向，但还没进入宣誓提交。
- `等待 Token`：方向已经确认，但当前还没满足进入投票的 2 个 AIBOUNTY 条件。
- `已准备宣誓`：映射、版本、时间和 Token 预检都已完成；如果当前路径还差最后一步授权，我会先补齐授权，再继续正式提交。
- `已提交`：宣誓已经发出，正在等待公开记录页确认最终结果。
- `已完成`：宣誓交易已经成功，且你已经拿到了需要带去 Telegram 群回报的编号。

### 等待 Token 示例

如果方向已经选好了，但当前 `AIBOUNTY` 余额还不到 2 个，就应该明确告诉用户：

`当前方向已经确认，但你现在还没满足进入部落宣誓所需的 2 个 AIBOUNTY。我会先把你停在等待 Token 阶段。你可以先等 Task 2 配对成功后再回来，或者邀请朋友来配对，补足进入投票所需的 Token。`

### 已提交示例

如果宣誓投票已经发出，但最终结果还在等待确认，应该明确告诉用户：

`你的部落宣誓已经发出，我现在把你放在已提交阶段，等待公开记录页确认最终结果。确认完成后，我会再给你最终编号。`

### 阻断示例

如果当前不是正常等待，而是授权、依赖、或记录确认本身被外部环境卡住，就应该明确告诉用户：

`当前部落宣誓还不能继续，不是因为方向或 Token 不够，而是这一步的 CA 自动执行路径在完成授权、提交和记录确认后仍然没有完全走通。我先把你停在这里，等这个阻断解除后再继续。`

如果 TomorrowDAO 直发路径已经明确返回 `CA` 直发被禁止，但显式的 `CA` forward 写入路径本身又不可用，也应该明确告诉用户：

`当前部落宣誓还不能继续，不是因为方向选错或 Token 不够，而是当前这一步缺少可用的 CA forward 写入路径。我会把它视为 CA 发送路径阻断，而不是改成 manager 直签或继续尝试其它私钥回退。`

- `→ 如果这里卡住了，欢迎到 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl) 贴出你当前的步骤、报错和关键信息，我们可以一起帮你排查。`
- `→ 也可以去 [X / Twitter](https://x.com/aelfblockchain) 发帖求助，带上你当前的状态和卡点，方便社区更快看到并协助你。`

### 授权示例

如果 `AIBOUNTY` 余额已经够了，但当前路径还差一次投票授权，回复应该明确告诉用户：

`你现在已经满足进入部落宣誓所需的 2 个 AIBOUNTY 条件，但这次宣誓还差最后一步授权。我会先补齐本次投票所需的授权，授权成功后再继续发出部落宣誓。`

### 密码示例

如果当前 `CA` 上下文已经准备好，但 keystore 密码还没拿到，回复应该明确告诉用户：

`我已经确认你当前的身份入口可以继续这次部落宣誓，但这一步还差一次 CA keystore 密码确认。我只需要你提供这一次密码，拿到后我会继续自动完成后面的授权、宣誓提交和结果确认。`

### 自动重试示例

如果授权或宣誓提交没有一次走通，但系统还在自动补救，回复应该明确告诉用户：

`这一步还在自动重试中，我正在重新校验授权状态、宣誓状态和公开记录确认。只要这条自动路径还能继续，我就不会把执行工作交还给你。`

如果当前已经有一条 `CA` 写入路径成功完成了授权，而另一条宣誓发送路径又报出“授权仍不足”这一类矛盾错误，系统应该自动切回刚才那条已经验证成功的 `CA` 写入路径继续提交，而不是把它误判成真的 Token 不足。

### 成功示例

如果宣誓交易已经成功并拿到了 `txId`，就应该明确告诉用户：

`你的部落宣誓已经成功，当前编号是 txid-1234。请现在加入 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl)，并发送这条消息。两周后可额外领取 20 Token，有问题也欢迎在群里讨论。`

如果当前路径先做过一次授权，也要明确提醒：

`如果刚才这条路径先做过授权，带去 Telegram 群回报的仍然是最终宣誓成功的 txid-1234，不是授权编号。`

群内发送模板：

`我是平衡者阵营，编号 txid-1234。我已完成龙虾圣殿 Task 3 正式版部落宣誓记录。`

## 维护者详情

- route: `task-3-faction-oath`
- config_path: `config/faction-proposals.json`
- active_environment: `production`
- dao_alias: `claws-temple-ii`
- formal_record: `true`
- dependency_min_version: `0.2.2`
- ca_write_dependency_min_version: `2.3.0`
- task3_execution_policy: `ca_only_ai_completion`
- task3_password_policy: `ask_once_for_ca_keystore_password`
- task3_retry_policy: `bounded_ca_retries_with_state_reconciliation`
- faction_page_label: `Faction: The Balancer`
- imagery_reference: `Claude`
- core_stance: `租来的家和自己造的家，是两种不同的东西`
- ca_vote_path: `TomorrowDAO balance/allowance reads -> TomorrowDAO token approve simulate -> Portkey forward-call Approve -> TomorrowDAO vote simulate normalization -> same Portkey forward-call Vote -> receipt/log reconciliation (+ proposal my-info when available)`
- ca_transport_rule: `CA keystore may unlock the manager key, but direct target-contract send is forbidden; if TomorrowDAO direct send returns CA-forbidden, continue with explicit Portkey CA forward transport; env/private-key fallback is forbidden once CA is selected`
- blocker_label: `CA 发送路径阻断`
