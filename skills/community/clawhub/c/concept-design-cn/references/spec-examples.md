# 概念与同步示例

以下为[工具编码](tool-encoding.md)的工程示例；概念与同步按[规格记法](spec-notation.md)编写。
以下接口和业务规则为教学设定，产品需求须另行确认。
表中列出验收与反例检查，不代表已执行的测试结果。

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

```markdown
# concept Todo
coverage: complete
## purpose
记住未完成工作，并区分已完成工作。
## state
tasks: set Task
text: Task -> Text
done: set Task
Task 是不复用的局部身份；Text 是任意字符串，允许空文本。
初始 tasks 与 done 为空。
text 定义域恰为 tasks，每任务恰有一个 Text；done 是 tasks 的子集。
Missing 是表示未知任务的单例错误。
## actions
add [text: Text] => [task: Task]
  requires true
  ensures 创建并返回一个新鲜 t；tasks = 旧 tasks union {t}；
          text = 旧 text 加 (t, 输入 text)；done 不变
// 保留身份与文本，支持重新打开。
complete [task: Task] => []
  requires task 属于 tasks
  ensures done = 旧 done union {task}；其余状态不变
complete [task: Task] => [error: Missing]
  requires task 不属于 tasks
  ensures 返回 Missing；状态不变
reopen [task: Task] => []
  requires task 属于 tasks
  ensures done = 旧 done minus {task}；其余状态不变
reopen [task: Task] => [error: Missing]
  requires task 不属于 tasks
  ensures 返回 Missing；状态不变
## operational principle
after add [text: "报告"] => [task: t]，待办包含 t；
then complete [task: t] => [] 后待办不含 t；
then reopen [task: t] => [] 后恢复同一 t 与文本。
## queries
_pending [] => [task: Task; text: Text]
  恰返回 tasks minus done，每任务一行并附文本；
  空状态返回零行；无顺序；不产生完成记录

## 执行约束
- 完成：声明的结果与局部状态效果可被后续查询观察后，动作才完成。
- 并发：每次状态变更原子保持已声明不变量。
- 失败/重复：沿用上述动作分支；重复 add 创建不同任务。
- 时限/恢复：未声明时限要求；持久化与重启恢复不在本例范围。
```

| 从全新状态验收 | 可观察结果 |
| --- | --- |
| add("报告") 后 _pending | 恰含返回的任务与输入文本。 |
| add 得到 t；complete(t) 后 reopen(t)，每次均查询 | t 先消失，再以原文本出现。 |
| add 得到 t；complete(t) 两次，再 reopen(t) 两次 | 重复调用成功，不增加重复任务或其他变化。 |
| complete(unknown) 或 reopen(unknown) | Missing，状态不变。 |
| add 前 _pending | 零行，无错误。 |

## 局部订位模型

本片段仅覆盖选定时段的成功或冲突。

```markdown
# concept Reserving [U, S]
coverage: partial
## purpose
为用户保留未来使用资源时段的承诺。
## state
reservations: set Reservation
user: Reservation -> U
slot: Reservation -> S
status: Reservation -> Status
Reservation 是局部身份；Status = booked | canceled | granted。
Conflict 是表示时段已有 booked 预约的单例错误。
初始 reservations 为空。
每项预约恰有一个 user、slot 和 status。
每个 S 最多有一个 booked 预约；不假定 S 的字段。
从空状态 reserve [user: u1; slot: s1] => [reservation: r1] 后：
{ reservation: r1, user: u1, slot: s1, status: booked }
每行是一项当前预约，以 reservation 为身份；字段对应同名关系。
## actions
reserve [user: U; slot: S] => [reservation: Reservation]
  requires slot 无 booked 预约
  ensures 原子创建并返回新鲜 r，设为输入 user/slot 和 booked；
          r 加入 reservations；已有事实不变
reserve [user: U; slot: S] => [error: Conflict]
  requires slot 有 booked 预约
  ensures 返回 Conflict；状态不变
cancel [reservation: Reservation] => []
  requires 预约为 booked
  ensures 仅将状态改为 canceled
grant [reservation: Reservation] => []
  requires 预约为 booked；到场条件未决
  ensures 仅将状态改为 granted
## operational principle
after reserve [user: u; slot: s] => [reservation: r]，
then 未取消且满足到场条件时 grant [reservation: r] => []，兑现承诺。

## 执行约束
- 完成：reserve 完成时具有已声明的预约或 Conflict 结果及状态效果。
- 并发：同一时段无 booked 预约的检查与新预约创建原子执行。
- 失败/重复：reserve 沿用声明的分支；重试身份与 cancel/grant 拒绝行为仍未决。
- 时限/恢复：到场条件、时限与重启恢复仍未决。
```

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

```markdown
# app Reservations
include Availability [VenueId]
include Reserving [UserId, Availability.Slot]
include Requesting

### 发起预约
sync reserve
when { Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request] }
then { Reserving/reserve: [user: ?user; slot: ?slot] }

// 预约结果不含 request，入口完成记录提供响应所需的请求身份。
### 返回预约结果
sync accepted
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [reservation: ?reservation]
}
then { Requesting/respond: [request: ?request; reservation: ?reservation] }

### 返回预约冲突
sync rejected
when {
  Requesting/reserve: [user: ?user; slot: ?slot] => [request: ?request]
  Reserving/reserve: [user: ?user; slot: ?slot] => [error: ?error]
}
then { Requesting/respond: [request: ?request; error: ?error] }

## 执行约束
- flow/关联：每个 Requesting/reserve 开启独立 flow，仅含一次尝试；重复尝试须关联发生记录。
- 读取/顺序：选定时段来自入口；_find 是读取，不满足 when。
- 结果：accepted/rejected 在该 flow 中匹配入口与预约完成记录，并沿用其 RequestId 响应。响应投递失败的处理仍未决。
- 时限/恢复：时限、重试与重启恢复仍未决。
```

| 验收或反例 | 可观察结果 |
| --- | --- |
| 预约空闲时段，再在其 booked 期间发起另一个请求 | 首个请求得到预约，第二个得到 Conflict，已有事实不变。 |
| 入口与预约完成记录来自不同 flow | 不用另一 flow 的结果响应当前请求。 |
| _find 返回零个或多个候选 | 规则不等待该查询，也不隐含预约其结果；候选选择须由产品需求确定。 |
| 移除 Availability 却保留 Availability.Slot | 子集不可用；须将 S 改绑为独立提供的 SlotId，并更新入口与规则。 |

发现时段的需求才支持纳入 Availability，类型绑定本身不够。
已知时段产品可能只需 Reserving。
到场输入/时限、cancel/grant 拒绝条件、认证、场所检查、并发撤下、
显示、取消入口和故障处理仍未决。
offered 可在 reserve 前变化，不能代替写入时检查不变量。
到场与 grant 定义并检查后，才能确认目的达成。

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

```markdown
# app ExternalLogin
include Web
include OAuthAuthentication [Credential]
include ExternalIdentity
include Profile [ExternalIdentity.Identity]
include Session [ExternalIdentity.Identity]

### 验证登录凭证
sync VerifyLogin
when { Web/login: [credential: ?credential] => [request: ?request] }
then { OAuthAuthentication/verify: [credential: ?credential] }

### 登记已验证的外部身份
sync RecordVerifiedIdentity
when {
  OAuthAuthentication/verify: []
    => [valid: true; namespace: ?namespace; subject: ?subject]
}
then { ExternalIdentity/record: [namespace: ?namespace; subject: ?subject] }

### 设置资料并创建会话
sync PrepareLogin
when {
  OAuthAuthentication/verify: [] => [valid: true; displayName: ?displayName]
  ExternalIdentity/record: [] => [identity: ?identity]
}
then {
  Profile/set: [identity: ?identity; displayName: ?displayName]
  Session/open: [identity: ?identity]
}

### 汇合完成结果并读取响应数据
sync CompleteLogin
when {
  Web/login: [] => [request: ?request]
  Profile/set: [identity: ?identity] => [identity: ?identity]
  Session/open: [identity: ?identity] => [session: ?session]
}
where {
  Profile: { ?identity displayName: ?displayName }
  Session: { ?session identity: ?identity; token: ?token }
}
then {
  Web/respond: [request: ?request; identity: ?identity; session: ?session;
                displayName: ?displayName; token: ?token]
}

### 拒绝无效凭证
sync RefuseLogin
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [valid: false]
}
then { Web/respond: [request: ?request; error: "InvalidCredentials"] }

### 返回验证错误
sync ReportVerificationError
when {
  Web/login: [] => [request: ?request]
  OAuthAuthentication/verify: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

### 返回会话错误
sync ReportSessionError
when {
  Web/login: [] => [request: ?request]
  Session/open: [] => [error: ?error]
}
then { Web/respond: [request: ?request; error: ?error] }

## 执行约束
- flow/关联：每个 Web/login 开启独立 flow，仅有一次验证尝试。该 flow 内其余动作各调用至多一次；重复尝试须关联发生记录。
- 读取/顺序：动作可同步或异步执行，CompleteLogin 匹配已完成的 Profile/set 与 Session/open。声明的成功状态效果可查询后才产生完成记录。本例假定所读资料与会话在完成至响应之间不被其他 flow 改写。
- 结果：在动作按所列分支完成且匹配规则最终执行的前提下，每个请求恰有一次响应。会话失败保留已完成的身份/资料效果。错误响应不等待资料完成，也不隐含取消其在途调用。
- 时限/恢复：时限、重试与重启恢复仍未决。
```

RecordVerifiedIdentity 与 PrepareLogin 从同一验证完成记录读取不同字段，匹配不会消耗该记录。
沿 PrepareLogin 的两个调用，核对 CompleteLogin 中的完成模式与公开状态读取。

| 验收场景 | 可观察结果 |
| --- | --- |
| 验证有效，资料与会话均完成 | 返回该请求的身份、资料与会话；响应一次。 |
| 验证返回 false | 返回 InvalidCredentials；不登记身份、设置资料或创建会话。 |
| 验证返回错误 | 原请求收到该错误；不发起后续业务动作。 |
| 会话创建失败 | 返回 SessionError，保留已完成的身份与资料效果；在途资料调用仍可能完成。 |
| 只有资料完成 | 会话仍在途时，不返回成功。 |
| 只有会话完成 | 资料仍在途时，不返回成功。 |
| 同一身份在另一 flow 中有会话完成记录 | 该记录不能满足 CompleteLogin，也不能提供当前请求的会话。 |

### 按查询行展开调用

本片段从 Posting/delete 成功完成开始，不包含删除入口及拒绝响应。
Posting/delete 接收 `[post: PostId]`，成功返回 `[post: PostId]`，失败返回 `[error: DeleteError]`。
Commenting[P] 的公开关系 `target: CommentId -> P` 为每条现存评论关联一个目标。
`remove [comment: CommentId] => [removed: boolean]` 删除指定评论及其 target 关系，返回 true；其余状态不变。
评论不存在时返回 false，状态不变。

```markdown
# app Discussion
include Posting
include Commenting [Posting.PostId]

### 删除目标文章的现存评论
sync RemovePostComments
when { Posting/delete: [] => [post: ?post] }
where { Commenting: { ?comment target: ?post } }
then { Commenting/remove: [comment: ?comment] }

## 执行约束
- flow/关联：发出的 remove 调用沿用 Posting/delete 成功发生记录的 flow。
- 读取/顺序：Posting/delete 完成后，规则才读取求值时的评论。
- 结果：每条匹配行发出一次 remove，零行不调用；评论在 remove 前被删除时，返回声明的 false 结果。
- 时限/恢复：并发新增、其他删除失败、时限、重试与重启恢复仍未决。
```

| 验收场景 | 可观察结果 |
| --- | --- |
| 查询无匹配评论 | 不调用 remove。 |
| 查询有多条匹配评论 | 每行发起一次 remove，其他文章的评论不受影响。 |
| 匹配评论在调用前已被删除 | remove 返回 false，状态不变。 |
| Posting/delete 返回错误 | 该完成记录不触发 remove；删除拒绝响应在本片段范围外。 |
