# aios-call-app-service

这是一个面向 AIOS / OpenClaw / Forguncy 场景的业务调用技能，用于处理依赖实时业务数据、系统接口、绑定配置或业务动作的请求。

## 适用场景

- 查询实时业务数据
- 调用本体中定义的业务命令
- 使用绑定接口读取系统数据
- 需要基于真实系统返回结果继续分析
- 用户要求直接在系统中执行操作

## 调用原则

- 先读取 `AIOS_ONTOLOGY_DIR`
- 再确认应用、命令、参数结构和枚举映射
- 统一通过 `aios-apps-invoke-cli` 发起调用
- 当前 CLI 只支持 `provider=hzg`
- 当前会话标识使用 `SessionId`
- 调用 `aios-apps-invoke-cli` 时：
  - `-p` 对应 `provider`
  - `-s` 对应 `SessionId`
- `binding` 参数优先从 `binding-*.md` 的 `CandidatesBindings`、`TableBindings`、`DataSourceBindings` 文档生成兼容 schema
- `servercommand` 参数严格按 ontology 的 `Input Arguments` 生成

## 相关文档

- 主说明见 `SKILL.md`
- 调用细则见 `references/invoke-rules.md`
- 数据处理规则见 `references/data-processing.md`
