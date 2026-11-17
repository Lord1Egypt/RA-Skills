# 写操作与同步规则

## 真实写操作

以下动作会修改真实 Doxent 数据：
- create
- update
- delete
- move
- rename
- complete
- uncomplete
- 会创建或落真实记录的 upload

## 确认规则

在执行高风险动作前，必须确认：
- 对象标识
- 对象名称
- 对象类型
- 影响范围

这条规则适用于 delete、move、rename、complete、uncomplete 以及类似的直接状态变更动作。

## 同步规则

- 当底层流程要求写后同步时，真实写操作成功后再调用 `/open-model/sync`。
- 纯读取操作不要调用 `/open-model/sync`。
- 对用户说明结果时，要明确 sync 只表示“已触发同步流程”，不代表远端已经完成最终可见。
