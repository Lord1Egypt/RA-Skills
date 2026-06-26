# 纯 Prompt 驱动的 cron agentTurn 任务：可审证据与证据边界

## 适用场景

当一个定时任务在 cron 中配置为 `payload.kind: "agentTurn"`，且 `payload.message` 是一段自然语言 prompt 时，排查“任务成功但产物为空”类问题时，需要先明确：

- 哪些信息可以从配置和 run 记录中直接证明；
- 哪些信息**不能**从这些文件中推出；
- 哪些结论只能作为“高概率推断”，不能当成源码级事实。

---

## 一、`jobs.json` 能证明什么

典型可直接确认的信息包括：

- job 标识与名称
- 调度表达式 `schedule.expr`
- 调度时区 `schedule.tz`
- 执行类型 `payload.kind`
- 交给 agent 的原始 prompt 文本 `payload.message`

如果看到：

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "你是“小笔（Writer）”执行每日复盘整理..."
  }
}
```

则可直接得出：

1. 这是 **agentTurn 任务**，不是显式 shell / JS / TS 脚本任务；
2. 当前最直接可审的“实现入口”就是这段 prompt；
3. prompt 中写明的内容，只能证明“业务口径被声明过”，**不能自动等价于“有固定代码严格执行”**。

---

## 二、`jobs.json` 不能证明什么

即使 prompt 写了类似：

- 仅处理某个 guild
- 仅统计某个用户本人发言
- 包含 @该用户 / 回复该用户
- 时间窗为昨日（某时区）

也**不能**仅凭 prompt 证明以下实现细节已经被固定：

- 具体调用了哪种 Discord 读取 API
- 是否扫描 parent channel 主频道消息
- 是否扫描 thread starter message
- 是否扫描 thread replies
- mention 是否基于结构化 `mentions[].id` 判断
- reply 是否基于 `message_reference` / `referenced_message.author.id` 判断
- 是否做分页
- limit 多大
- 是否按字符串比较 snowflake ID
- 是否真的按指定时区构造查询边界

结论：

> prompt 只定义了“想要什么结果”，不等于定义了“如何机械地取数”。

---

## 三、run 记录能证明什么

对于 cron run 记录（如 `.jsonl`），通常可以直接确认：

- 某次任务确实被触发
- `runAtMs`
- `status`（例如 `ok`）
- 使用的模型
- 使用的 provider

如果 run 记录显示：

- `status: "ok"`

则只能说明：

- 任务没有明显 crash；
- 没有以显式失败态结束；
- 可能没有 timeout。

---

## 四、run 记录不能证明什么

`status: "ok"` **不能**证明：

- 检索覆盖面正确；
- 目标频道确实被扫到；
- threads 确实被扫到；
- 主频道消息确实被纳入；
- 筛选条件实现无误；
- 空结果就一定代表“当天真的没数据”。

如果 run 记录没有同时落盘以下内容：

- 扫描了哪些 channel/thread
- 拉取了多少消息
- 命中了哪些消息 ID
- 使用了哪些查询参数
- 各筛选阶段的命中数

那么 run 记录对“为什么结果为 0”只能提供**成功执行**这一层证明，不能提供**采样正确**这一层证明。

---

## 五、如何判断“源码缺失”已足以影响排查结论

如果你已经：

- 找到 cron job 配置；
- 找到 run 记录；
- 找到最终产物；
- 但在 workspace / skills / scripts / templates 中找不到对应实现文件；

则应把结论切换为：

> 当前任务是“纯 prompt 驱动”，真实读取行为缺乏固定实现证据。

这类任务里，很多关键动作可能由模型在运行时临场决定，例如：

- 先看哪个频道；
- 是否展开 thread；
- 是否只看一层消息；
- 是否跳过 starter；
- 是否只凭文本而不查结构化字段。

因此，后续排查重点应转向：

1. 产物是否明确写成“未检索到样本”；
2. 外部事实是否证明当天明明有数据；
3. 是否存在高风险漏扫点（主频道、thread starter、thread replies、reply 结构、mention 结构等）。

---

## 六、证据强度分级建议

排查时建议给结论标注强度：

### A. 可直接证实

来自文件或日志的明确事实，例如：

- job 是 `agentTurn`
- schedule 是 `0 5 * * *`
- tz 是 `Asia/Shanghai`
- 产物写了“未检索到符合筛选条件的记录”
- run 状态是 `ok`

### B. 高概率推断

由多份证据交叉支持，但缺少源码或 API 日志闭环，例如：

- 更像是采样漏扫，而不是分类清零
- 主频道消息可能未被纳入
- thread starter 可能未被统计

### C. 当前无法证实

没有源码、没有检索明细日志时，不应说死的内容，例如：

- 运行时一定用了某个 Discord API
- 一定按字符串比较了 snowflake
- 一定正确处理了回复链
- 一定按时区边界查询

---

## 七、对未来同类任务的落盘建议

为了避免以后只能“反推”，建议让任务在运行时至少记录：

- 实际扫描的 guild/channel/thread ID
- 主频道扫描消息数
- thread starter 命中数
- thread replies 扫描数
- author 命中数
- mention 命中数
- reply 命中数
- 最终纳入样本的消息 ID 列表
- 使用的时间窗起止（带时区）

这样才能把：

- “任务成功执行”
- “任务正确取数”
- “任务正确分类”

这三层问题拆开审计。