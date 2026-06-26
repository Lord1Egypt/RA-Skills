# Session Cache（会话级固定层缓存策略）

> 目标：减少主控每章重复读取固定层文件的 token 消耗。固定层内容在同一会话内只需读取一次，后续章节复用缓存，直至发生触发刷新的事件。

---

## 一、哪些内容属于固定层（可缓存）

| 文件 | 缓存条件 | 刷新条件 |
|------|----------|----------|
| `worldbuilding/world.md` | Phase 2 开始后首次读取 | 用户执行"补设定" / Phase 3 世界观变更 |
| `characters/protagonist.md` | Phase 2 开始后首次读取 | 用户执行"修改角色" / 角色弧光重大变更 |
| `characters/characters.md` | Phase 2 开始后首次读取 | 新增/修改角色 |
| `outline/outline.md` | Phase 2 开始后首次读取 | 用户执行"修改大纲" |
| `references/iron-rules.md` | 会话开始时读取一次 | 永不刷新（铁律不可变） |

> **不可缓存的内容（每章必须重新读取）：**
> - `meta/workflow-state.json`
> - `meta/metadata.json`
> - `meta/style-anchor.md`（每章全文喂入 MainWriter，需保持最新）
> - `outline/chapter-outline.md`（当前章节细纲）
> - `references/rolling-summary.md`（每5章更新）
> - tracker 三件套（每章更新）

---

## 二、缓存初始化时机

**Phase 2 首次进入时（执行恢复协议之后）**，Coordinator 执行一次性固定层读取：

```
1. 读取 worldbuilding/world.md → 提取世界观摘要（≤1500字）
2. 读取 characters/protagonist.md + characters/characters.md → 提取角色圣经摘要（≤2000字）
3. 读取 outline/outline.md → 全书大纲（≤3000字）
4. 读取 references/iron-rules.md

以上内容在本会话内视为"已加载"，后续章节直接复用，不重复读取文件。
```

> 注意：此处"缓存"是指 Coordinator 在同一会话的 context 中已持有这些内容，不是指写入任何中间文件。会话重启后需重新加载。

---

## 三、刷新触发条件

出现以下任一情况时，Coordinator 必须重新读取对应文件并更新缓存内容：

| 触发事件 | 需刷新的缓存项 |
|---------|---------------|
| 用户执行"补设定" / 修改世界观 | `world.md` 摘要 |
| 用户执行"修改角色" | `protagonist.md` + `characters.md` 摘要 |
| 用户执行"修改大纲" | `outline.md` |
| Phase 3 任何结构性修改 | 视修改范围刷新对应项 |
| 会话中断后恢复（resumeRequired = true） | 全部重新加载 |

---

## 四、对主控压力的影响

| 场景 | 不使用缓存 | 使用缓存 | 节省 |
|------|-----------|---------|------|
| 写第 20-30 章（10章） | 每章读 4 个固定层文件 × 10 = 40次读取 | 会话开始时读 1 次 | ~39 次固定层文件读取 |
| 自动推进 8 章 | 同上规模 | 同上 | 显著减少 context 填充量 |

---

## 五、使用规范

- Coordinator 在每章 Step 1（写前核查）中，使用缓存的固定层摘要，而非重新读取原始文件
- 若 Coordinator 不确定缓存是否有效（如用户提到修改了某文档），**优先刷新后继续**，不要使用可能过期的缓存
- 缓存内容仅在 Coordinator 主控会话内有效，子 Agent 的输入仍需 Coordinator 主动传入
