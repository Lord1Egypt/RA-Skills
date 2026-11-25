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
