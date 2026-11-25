# 概念与同步示例

以下为[工具编码](tool-encoding.md)的工程示例；概念与同步按[规格记法](spec-notation.md)编写。
以下接口和业务规则为教学设定，产品需求须另行确认。
表中列出验收与反例检查，不代表已执行的测试结果。
每个场景的规格是 `assets/examples/` 下的独立文件，只读取当前需要的场景；文件可直接交给 `concept_lint.py` 检查。

## 场景索引

| 场景 | 学习重点 | 范围 |
| --- | --- | --- |
| [待办](#完整待办) | 状态不变量、动作契约、拒绝与重复调用 | 完整的本地任务行为，无需同步。 |
| [订位](#局部订位模型) | 类型绑定、请求关联、成功/冲突与可用子集 | 局部模型；到场与目的达成仍有缺口。 |
| [外部身份登录](#外部身份登录) | 共用完成记录、无先后约束的调用及其汇合、状态读取、错误分支与 flow 隔离 | 仅列所需接口；时限、重试与恢复未决。 |
| [评论清理](#按查询行展开调用) | 查询零行/多行与删除竞态 | 从文章删除成功开始；并发新增评论未决。 |

## 完整待办

可信调用者在本地添加、完成和重新打开任务，只需一份 CONCEPT，无需 SYNCS。
删除、排序、界面、外部入口、授权和持久化不在本例范围。

规格：[assets/examples/todo.concept.md](../assets/examples/todo.concept.md)

| 从全新状态验收 | 可观察结果 |
| --- | --- |
| add("报告") 前后各查询 _pending | 先为零行且无错误，后恰含返回的任务与输入文本。 |
| add 得到 t；complete(t) 两次，再 reopen(t) 两次，每次均查询 | t 先消失，再以原文本出现；重复调用成功，不增加重复任务或其他变化。 |
| complete(unknown) 或 reopen(unknown) | Missing，状态不变。 |

## 局部订位模型

本片段仅覆盖选定时段的成功或冲突。

规格：[assets/examples/reservation.concept.md](../assets/examples/reservation.concept.md)

Availability[V] 拥有局部 Slot 身份，不读取 Reserving，通过以下接口提供可选时段：

- `venue: Slot -> V` 为每个时段关联恰一个场所。
- `offered: set Slot` 是现有时段的子集。
- `_find [venue: V] => [slot: Slot]` 返回全部匹配的 offered 时段，每项一行；无匹配为零行，不产生完成记录。

应用入口契约：

```markdown
Requesting/reserve: [user: UserId; slot: Availability.Slot] => [request: RequestId]
Requesting/respond: [request: RequestId; reservation: Reserving.Reservation] => []
Requesting/respond: [request: RequestId; error: Conflict] => []
```

规格：[assets/examples/reservation.syncs.md](../assets/examples/reservation.syncs.md)

| 验收或反例 | 可观察结果 |
| --- | --- |
| 预约空闲时段，再在其 booked 期间发起另一个请求 | 首个请求得到预约，第二个得到 Conflict，已有事实不变。 |
| 入口与预约完成记录来自不同 flow | 不用另一 flow 的结果响应当前请求。 |
| _find 返回零个或多个候选 | 规则不等待该查询，也不隐含预约其结果；候选选择须由产品需求确定。 |
| 移除 Availability 却保留 Availability.Slot | 子集不可用；须将 S 改绑为独立提供的 SlotId，并更新入口与规则。 |

发现时段的需求才支持纳入 Availability，类型绑定本身不够；已知时段的产品可能只需 Reserving。
offered 可在 reserve 前变化，不能代替写入时检查不变量。
未决：到场输入/时限与 grant 的定义（定义并检查后才能确认目的达成）、cancel/grant 拒绝条件、认证、场所检查、并发撤下、显示、取消入口和故障处理。

## 同步场景

### 外部身份登录

验证通过后先登记身份，再发起资料设置和会话创建，二者无先后约束。
两者均完成后才返回成功。
Credential 是不透明凭证值，Text 是字符串。
Identity 指 ExternalIdentity.Identity，SessionId 指 Session.SessionId。
Web 分配 RequestId；LoginError 包含 InvalidCredentials、VerificationError 与 SessionError。

所需接口片段：

| 动作 | 结果与效果 |
| --- | --- |
| `Web/login [credential: Credential]` | 返回新鲜的 `[request: RequestId]`，开启 flow。 |
| `OAuthAuthentication/verify [credential: Credential]` | 返回 `[valid: true; namespace: Text; subject: Text; displayName: Text]`、`[valid: false]` 或 `[error: VerificationError]`；公开状态不变。 |
| `ExternalIdentity/record [namespace: Text; subject: Text]` | 返回 `[identity: Identity]`；同一 namespace/subject 对应同一身份，无记录时创建；其余状态不变。 |
| `Profile/set [identity: Identity; displayName: Text]` | 返回 `[identity: Identity]`；仅设置该身份的 displayName。 |
| `Session/open [identity: Identity]` | 成功创建新鲜 session，关联 identity 和 token，返回 `[session: SessionId]`，其余状态不变；失败返回 `[error: SessionError]`，状态不变。 |
| `Web/respond [request: RequestId; identity: Identity; session: SessionId; displayName: Text; token: Text]` | 返回 `[]`，向该请求写出登录结果。 |
| `Web/respond [request: RequestId; error: LoginError]` | 返回 `[]`，向该请求写出错误。 |

Profile 的公开关系 `displayName: Identity -> Text` 对每个已设置身份恰有一值。
Session 的公开关系 `identity: SessionId -> Identity` 和 `token: SessionId -> Text` 对每个 session 各有一值。

规格：[assets/examples/login.syncs.md](../assets/examples/login.syncs.md)

RecordVerifiedIdentity 与 PrepareLogin 从同一验证完成记录读取不同字段，匹配不会消耗该记录。
沿 PrepareLogin 的两个调用，核对 CompleteLogin 中的完成模式与公开状态读取。

| 验收场景 | 可观察结果 |
| --- | --- |
| 验证有效，资料与会话均完成 | 返回该请求的身份、资料与会话；响应一次。 |
| 验证返回 false | 返回 InvalidCredentials；不登记身份、设置资料或创建会话。 |
| 验证返回错误 | 原请求收到该错误；不发起后续业务动作。 |
| 会话创建失败 | 返回 SessionError，保留已完成的身份与资料效果；在途资料调用仍可能完成。 |
| 资料与会话只完成其一 | 另一项仍在途时，不返回成功。 |
| 同一身份在另一 flow 中有会话完成记录 | 该记录不能满足 CompleteLogin，也不能提供当前请求的会话。 |

### 按查询行展开调用

本片段从 Posting/delete 成功完成开始，不包含删除入口及拒绝响应。
Posting/delete 接收 `[post: PostId]`，成功返回 `[post: PostId]`，失败返回 `[error: DeleteError]`。
Commenting[P] 的公开关系 `target: CommentId -> P` 为每条现存评论关联一个目标。
`remove [comment: CommentId] => [removed: boolean]` 删除指定评论及其 target 关系，返回 true；其余状态不变。
评论不存在时返回 false，状态不变。

规格：[assets/examples/comment-cleanup.syncs.md](../assets/examples/comment-cleanup.syncs.md)

| 验收场景 | 可观察结果 |
| --- | --- |
| 查询无匹配评论 | 不调用 remove。 |
| 查询有多条匹配评论 | 每行发起一次 remove，其他文章的评论不受影响。 |
| 匹配评论在调用前已被删除 | remove 返回 false，状态不变。 |
| Posting/delete 返回错误 | 该完成记录不触发 remove；删除拒绝响应在本片段范围外。 |
