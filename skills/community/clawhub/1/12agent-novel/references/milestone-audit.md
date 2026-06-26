# Milestone Audit（全书锚定审计，每20章触发）

\u003e 目标：弥补现有系统"章节级防漂移"的结构性缺口。每完成第20、40、60...章时，触发一次跨全书视角的一致性审计，识别渐进漂移。

---

## 一、触发条件

满足以下任一条件时触发：
- `lastClosedChapter` 为 20 的倍数（第20、40、60章...）
- 用户手动发送"里程碑审计" / "全书审计"
- resume-protocol 检查发现 `lastMilestoneAuditChapter` 落后当前章超过 20 章

\u003e 触发优先级高于普通章节推进：自动推进循环中，若触发里程碑审计，需先完成审计再继续推进。

---

## 二、审计内容

调用 FinalReviewer，执行以下五项全书级检查：

### 检查项 A：角色一致性（渐进 OOC 检测）
- 对比角色圣经（`characters/protagonist.md` + `characters/characters.md`）与最近 5 章原文
- 重点识别：语气漂移、决策逻辑变化、核心性格弱化
- **特别关注**：早期设定的"Signature 标签"是否仍在正文中有所体现

### 检查项 B：伏笔健康度
- 读取 `references/plot-tracker.md`，列出所有"已埋设未回收"的伏笔
- 对照当前章节进度，标记"超期未回收"的伏笔（埋设超过 15 章未回收）
- 对照最近 10 章正文，检查是否有实际回收但 tracker 未更新的情况

### 检查项 C：大纲偏离度
- 对比 `outline/outline.md`（三幕结构 / 核心转折点）与实际已写章节进度
- 标记：当前实际进度是否在大纲预期的轨道上
- 若已发生合理的创作性偏离，记录偏离内容供 Coordinator 决策是否更新大纲

### 检查项 D：势力/世界观自洽性
- 对照 `worldbuilding/world.md` 的势力格局，检查最近 10 章中势力行为是否合理
- 重点：力量体系等级是否被突破；地理/时间线是否出现矛盾

### 检查项 E：节奏与结构健康度
- 对照大纲的幕结构，评估当前节奏是否符合预期
- 识别：是否存在连续 5 章以上的"铺垫过密"或"推进过快"异常

---

## 三、调用方式

```javascript
sessions_spawn({
  task: `${read("references/agent-final-reviewer.md")}

【本次任务】
执行第 ${auditChapter} 章里程碑全书锚定审计。

【输入材料】
- 角色圣经: ${read("characters/protagonist.md")} + ${read("characters/characters.md")}
- 世界观: ${read("worldbuilding/world.md")}
- 全书大纲: ${read("outline/outline.md")}
- 伏笔追踪表: ${read("references/plot-tracker.md")}
- 滚动摘要（全部）: ${read("references/rolling-summary.md")}
- 最近5章原文: ${recentChapters}

【检查项】
A. 角色一致性（渐进 OOC）
B. 伏笔健康度（超期未回收 / tracker 漏更新）
C. 大纲偏离度
D. 势力/世界观自洽性
E. 节奏与结构健康度

【输出要求】
每项给出：状态（正常/警告/严重）+ 具体问题描述 + 修复建议
最后给出综合评级（绿色/黄色/红色）和优先处理建议`,
  label: "milestone-audit-ch" + auditChapter,
  model: readConfig("meta/config.md", "finalReviewer"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 1200
})
```

---

## 四、审计结果处理

| 综合评级 | 处理方式 |
|---------|----------|
| 🟢 绿色（无严重问题） | 记录报告，继续推进 |
| 🟡 黄色（有警告项） | 向用户展示警告，确认后继续；Coordinator 标记待观察项 |
| 🔴 红色（有严重问题） | **暂停自动推进**，向用户报告，等待修复指令 |

审计报告写入：`archive/milestone-audit/audit-ch{NNN}.md`

---

## 五、状态记录

审计完成后更新 `meta/workflow-state.json`：

```json
{
  "milestoneAudit": {
    "lastMilestoneAuditChapter": 20,
    "lastAuditResult": "green",
    "pendingWarnings": [],
    "nextAuditChapter": 40
  }
}
```

---

## 六、与现有机制的关系

| 机制 | 范围 | 频率 | 目标 |
|------|------|------|------|
| OOCGuardian | 单章 | 每4章/条件触发 | 当章 OOC |
| FinalReviewer | 单章 | 重点章节 | 当章终审 |
| ReaderSimulator | 最近5章 | 每5章 | 读者体验 |
| **MilestoneAudit** | **全书** | **每20章** | **渐进漂移** |

\u003e Milestone Audit 是唯一具备全书视角的审计机制，专门针对上述四种机制无法覆盖的跨章漂移。
