# 上下文分层与收益口径

## 六类源与三层的对应

分层看的是"什么时候进上下文"，不是文件类型。同一个文件在不同 Agent 上可能落在不同层，先判层再动手。

| 源 | 常见层 | 判断依据 |
| --- | --- | --- |
| 规则（指令、约束） | Hot | 每次对话都在，改一个字就影响每轮 |
| 记忆（摘要、画像、注入块） | Hot | 启动即注入；服务端注入的部分本地可能无文件 |
| 技能清单（name + description + 触发词） | Hot | 每轮随工具列表一起发 |
| 技能正文、参考、子项 | Warm | 命中触发词或路由才加载 |
| 工具 schema（MCP / 插件暴露面） | Hot | 随工具清单注入，未连接 server 的不计 |
| 固定注入的模板与检查清单 | Hot 或 Warm | 看是每轮发还是按需读 |
| 会话、备份、日志、缓存、旧插件 | Cold | 从不进上下文，只占磁盘 |

## Hot

每轮或每次模型调用都会进入上下文的对象。典型包括常驻规则、Skill 列表元数据、工具 schema、固定注入片段。

可用的改进方式：压缩已验证的描述、删除已证明无效的常驻重复、减少不必要的工具暴露。Hot 的改动最容易影响行为，必须跑触发和常用任务回归。

## Warm

只有触发词、路由或任务条件成立时才加载的对象。典型包括 Skill 正文、参考文档、模板和脚本说明。

可用的改进方式：保留最小入口，把低频细节移到有明确读取条件的文件。只有在原本会加载的内容确实不再加载时，才产生 Token 收益。

## Cold

只占磁盘、不进入模型上下文的对象。典型包括旧会话归档、备份、缓存和历史包。

Cold 操作的价值是磁盘、备份时间和可管理性。它的 Token 收益固定为 0。将 Cold 释放空间写成 Token 节省属于口径错误。

## 记录模板

每条候选至少记录：

```json
{
  "id": "candidate-001",
  "layer": "hot|warm|cold",
  "observed_tokens": null,
  "estimated_tokens": 0,
  "load_frequency": null,
  "disk_bytes": 0,
  "evidence": "measured|estimated|unknown",
  "risk": "R0|R1|R2|R3",
  "action": "report-only|compress|move-to-warm|quarantine|archive|disable-optional-plugin",
  "rollback": "transaction-id-or-plan"
}
```

`observed_tokens` 只能来自现有用量事实源。`estimated_tokens` 必须带估算方法；两者不能相加成一个“实测值”。

## 报告口径

- Token 收益：写明时间窗口、来源、实测/估算。
- 磁盘收益：写明原始字节、处理后字节、净变化。
- 能力证据：写明触发集、任务集、引用检查和回滚结果。
- 未确认项：单独列出，不能计算进总收益。
