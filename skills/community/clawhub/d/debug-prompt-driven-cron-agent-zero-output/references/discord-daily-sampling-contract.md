# Discord 日报/复盘任务的采样实现契约

## 目的

当日报、复盘、统计类任务依赖 Discord 数据时，若不把“样本源”和“匹配规则”写成固定实现，极易出现：

- 当天明明有消息，结果却全 0；
- 只统计到 thread reply，漏掉主频道起帖；
- 只看文本，漏掉结构化 mention/reply；
- snowflake 精度或类型比较错误；
- 时间窗边界偏移导致跨天漏样本。

本文给出一份适合固定成脚本/工具链的最小实现契约。

---

## 一、必须明确的样本源

如果目标是统计“某用户本人发言 + @该用户 + 回复该用户”的 Discord 活动，则样本源至少应包含：

1. **parent channel 主频道消息**
2. **主频道中创建 thread 的 starter message**
3. **这些 thread 的 replies**

否则最常见的漏扫就是：

- 主频道开帖消息未统计；
- 只扫 thread 内消息，没扫 parent channel；
- 只扫主频道，没展开 thread reply。

---

## 二、推荐的固定扫描顺序

建议不要让模型自由决定“怎么扫”，而是固定为：

1. 读取目标 parent channel 在时间窗内的主频道消息；
2. 从这些消息中识别 thread starter / thread 入口；
3. 读取这些 thread 的 replies；
4. 对主频道消息与 thread replies 统一执行筛选；
5. 输出样本明细与统计结果。

可简化为：

```text
scan parent messages
→ collect thread starters / thread ids
→ scan thread replies
→ merge messages
→ filter by author / mention / reply
→ produce report
```

---

## 三、匹配规则应写死为结构化判断

### 1. 本人发言

应以结构化作者字段判断：

```ts
message.author?.id === TARGET_USER_ID
```

不要依赖：

- 用户名
- 昵称
- display name
- 文本中自称

---

### 2. @ 提及目标用户

优先使用结构化 `mentions`：

```ts
message.mentions?.some(m => m.id === TARGET_USER_ID)
```

正文中的 `<@...>`、`<@!...>` 形式只能作为兜底补充，不应作为主判断依据。

原因：

- 文本可能被转义或裁剪；
- 不同来源数据未必保留原始 mention 文本；
- 结构化字段更稳定。

---

### 3. 回复目标用户

应优先检查 reply 结构，而不是仅凭文本语气推断。

推荐判断思路：

- `message_reference.message_id` 存在，说明它是回复；
- 若可获取 `referenced_message.author.id`，则以该字段判断被回复对象是否为目标用户；
- 如数据源不直接返回被回复消息作者，则需要补查被引用消息。

可表达为：

```ts
const isReplyToTarget =
  !!message.message_reference?.message_id &&
  referencedMessage?.author?.id === TARGET_USER_ID
```

---

## 四、Discord snowflake 一律按字符串处理

Discord ID 是 snowflake，务必统一按字符串比较：

```ts
const TARGET_USER_ID = "1478785297784373490"
message.author?.id === TARGET_USER_ID
```

不要写成：

```ts
Number(message.author?.id) === 1478785297784373490
```

原因：

- 大整数在某些环境中可能发生精度问题；
- 数据源字段通常本身就是字符串；
- 字符串比较最稳妥、最一致。

建议约束：

- 禁止 `Number(id)` 参与业务匹配；
- 禁止把 snowflake 当普通数值主键处理；
- 所有 channel/user/message/thread ID 统一以 string 存储和比较。

---

## 五、时间窗必须落成固定函数

如果业务定义是“Asia/Shanghai 的昨日 00:00:00 ~ 23:59:59.999”，就不要在 prompt 中模糊表达，而应生成固定时间边界。

建议输出明确的起止：

- `YYYY-MM-DD 00:00:00+08:00`
- `YYYY-MM-DD 23:59:59.999+08:00`

核心要求：

1. 先在目标时区求“昨日”；
2. 再生成起止边界；
3. 所有查询统一复用同一时间窗；
4. 审计日志中落盘最终起止值。

否则容易出现：

- 服务器时区与业务时区不一致；
- UTC 换算导致跨天；
- 当日凌晨消息被算到前一天或后一天。

---

## 六、分页与覆盖面必须显式约束

如果没有分页策略，模型或脚本可能只读到很少一部分消息，导致“看起来成功，实际漏样本”。

实现时应明确：

- 每个 channel / thread 的分页方式；
- 每页大小；
- 停止条件；
- 只在时间窗内截断，而不是随意按条数截断。

至少要保证：

- 主频道不会只取前 N 条就停止；
- thread replies 不会因为默认 limit 太小而漏后续内容；
- 时间窗边界内的消息全部有机会被扫描。

---

## 七、推荐的筛选输出结构

建议每次运行都产出可审计的中间结果，而不仅是最终日报文本。

最少记录：

- 扫描的 guild/channel/thread ID
- 时间窗起止
- 主频道扫描消息数
- thread starter 命中数
- thread replies 扫描数
- 本人发言命中数
- mention 命中数
- reply 命中数
- 最终纳入样本的消息 ID 列表

这样当结果为 0 时，可以快速判断：

- 是没扫到；
- 是扫到了但筛选条件没命中；
- 还是命中了但下游整理没写出来。

---

## 八、最小规则清单

可直接作为实现验收 checklist：

- [ ] 明确扫描 parent channel 主消息
- [ ] 明确纳入 thread starter message
- [ ] 明确扫描 thread replies
- [ ] author 匹配使用 `author.id === TARGET_USER_ID`
- [ ] mention 匹配优先使用 `mentions[].id`
- [ ] reply 匹配基于 `message_reference` 与被回复消息作者
- [ ] 所有 snowflake 按 string 处理
- [ ] 时间窗按业务时区生成固定起止
- [ ] 查询具备分页能力
- [ ] 检索阶段落盘审计日志

---

## 九、一个推荐结论模板

当任务结果全 0 时，如果审计日志显示：

- 主频道扫描数为 0，或
- thread starter 命中数为 0，或
- thread replies 未扫描，

则优先判断为：

> 上游采样链路存在漏扫，不能将“0 结果”解释为“当天无活动”。

只有在以下都已被证实后，才适合下结论“当天确实无样本”：

- 主频道已完整扫描；
- thread starter 已纳入；
- thread replies 已扫描；
- author / mention / reply 规则已按结构化字段执行；
- 时间窗正确；
- 分页覆盖完整。