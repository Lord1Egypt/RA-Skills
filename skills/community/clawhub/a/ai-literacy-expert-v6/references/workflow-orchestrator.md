# 自动化智能化工作流编排引擎（V6.0 核心）

> 本文件是 V6.0 的「中枢神经」。它把 V5.5 的六个独立能力 + A→G 七模块 + E·N 院校子模块 + WorkBuddy 适配层，**统一编排成一条可恢复、可验证、跨时间的工作流管线**。
>
> **设计哲学**：V5.5 是「高质量提示词 + 知识库」（告诉 AI *怎么做*）；V6.0 是「**工作流引擎**」（替 AI *把步骤串起来、把验证自动化、把分发接上、把学习回流*）。你只需要说一句话，引擎自动跑完 INTENT→PLAN→BUILD→VERIFY→ASSEMBLE→DELIVER→REPORT→LEARN。

---

## 0. 何时用本引擎

- 用户一句话需求（如「给 BNBU 新生做 4 周 AI 上手包」）→ 走**请求驱动**工作流。
- 时间到了（如每周一 9 点）→ 走**时间驱动**运营流（见 `automation-ops.md`）。
- 长任务（如整套 20+ 课备课包）→ 启用**状态持久化**可断点续跑。

> 凡涉及「生成课件/游戏」，`VERIFY` 阶段**强制**调用 `assets/playwright-control-test-harness.js` 自动实测，未过不得进入 `DELIVER`。

---

## 1. 八大阶段通用管线（所有能力的骨架）

```
┌─────────────────────────────────────────────────────────────────────┐
│  INTENT → PLAN → BUILD → VERIFY → ASSEMBLE → DELIVER → REPORT → LEARN │
└─────────────────────────────────────────────────────────────────────┘
        ▲                                  │                         │
        └──────── 自动修复闭环(≤3) ─────────┘                         │
        └──────── 评估→补学回流(LEARN) ───────────────────────────────┘
```

### 阶段 1 · INTENT（意图识别）
**目标**：把自然语言 → 结构化意图对象 `Intent`。
**自动决策**（命中即路由，不追问）：
```javascript
Intent = {
  ability:   'courseware'|'game'|'lesson'|'assessment'|'recommend'|'collab'|'ops',
  modules:   ['A2','C1', ...],          // 从触发词/上下文解析
  audience:  '中学生'|'大学生'|'教师'|'企业'|'BNBU新生'|...,
  difficulty:1..5,
  workbuddy: { ima:bool, doc:bool, alarm:bool, calendar:bool, memo:bool, share:bool },
  context:   {...}                       // 课程代码/专业/博智坊期数等
}
```
**完成判据**：`ability` 已确定。`ability` 模糊 → **只追问 1 次**（「你想做课件、游戏、还是备课包？」），其余字段用智能缺省（见 §3）。

### 阶段 2 · PLAN（计划拆解）
**目标**：选 runbook（§4）+ 拆 stage + 建状态文件（见 `assets/workflow-state-template.json`）。
**自动决策**：缺参数一律智能缺省（不阻塞）：受众默认「大学生」、难度默认 2、题量默认 20、粒度默认「单元」。
**完成判据**：计划可读、含 checkpoint 列表、状态文件已写。

### 阶段 3 · BUILD（生成）
**目标**：调对应 reference 生成产物。
- 课件/游戏 → `p5js-courseware-guide.md` / `p5js-game-design-guide.md`
- 备课 → `interactive-lesson-builder-guide.md`（5 阶段，参数智能预填）
- 评估 → `assessment-guide.md`
- 推荐 → `recommendation-engine.md`
- 协作 → `collaboration-guide.md` + WorkBuddy 腾讯文档
- 院校 → `module-e-bnbu-sai.md`
**失败处理**：生成失败 → 重试 1 次；仍失败 → 回退到更简方案并告警。

### 阶段 4 · VERIFY（自动验证闭环）⭐ 最关键升级
**目标**：用 `assets/playwright-control-test-harness.js` **自动实测全部互动控件**，门控不过禁提交。
```
BUILD 产物 → 跑 harness → 全过? ──是──→ ASSEMBLE
                    │否
                    ├─ 自动读报告 → 定位缺陷控件 → 修复代码
                    └─ 复测 → 计数(≤3) → 仍不过则降级/告警并附报告
```
**自动决策**：缺陷自动修复（改 HTML/JS 后复测），预算 3 次；超过则**禁止提交**，把已测结果与修复建议随交付物说明。
**完成判据**：门控结果块「全部通过 / 修复后通过」。

### 阶段 5 · ASSEMBLE（组装打包）
**目标**：拼齐交付物五件套——产物 + README + 版本号 + SHA256 + 离线缓存清单；课件/游戏/备课包可 `zip`。
**完成判据**：单 HTML ≤ 200KB（备课 ≤ 500KB）、含 CDN 降级链、含门控结果块。

### 阶段 6 · DELIVER（原生分发）⭐ WorkBuddy 自动化
**目标**：按 `Intent.workbuddy` 自动接原生动作（见 `workbuddy-adaptation.md`）：
- `ima:true` → 保存到 IMA 知识库（先确认授权）
- `doc:true` → 存/建腾讯文档（协作备课、评估、报告）
- `alarm/calendar/memo` → 设备侧能力（复习提醒/课程表/学习计划）
- `share:true` → 系统分享面板分发
- 默认 → WorkBuddy 预览面板直开 + 本地文件
**失败处理**：未授权 → 引导授权后重试；分享失败 → 降级为「给链接+说明」。

### 阶段 7 · REPORT（报告留痕）
**目标**：生成**工作流状态报告**（模板见 §6）+ 门控结果块，附在交付物末尾。
**内容**：意图快照、各阶段耗时、验证结果、分发去向、可追溯 ID。

### 阶段 8 · LEARN（回流优化）⭐ 闭环
**目标**：把本次结果变成下一次的输入。
- **评估→补学回路**：若本次为「评估」，解析薄弱点 → 自动生成「补学课件/路径」建议（触发新一轮 INTENT，但标注 `auto:true` 降打扰）。
- **推荐→计划回路**：推荐结果自动转「可执行周计划」并写入备忘录/日历（能力五 × 设备侧）。
- **反馈沉淀**：用户采纳/修改反馈写入状态，优化下次路由与缺省。

---

## 2. 意图分类器（自动路由表）

| 信号（触发词/上下文） | ability | 常见 modules | 默认 workbuddy |
|----------------------|---------|--------------|----------------|
| 课件/演示/可视化/教具 | courseware | 解析自需求 | 预览+IMA |
| 游戏/闯关/冒险/玩中学 | game | A/B/C/D | 预览+IMA |
| 备课/教案/题目/备课包/word/ppt/excel/pdf | lesson | 多选 | 腾讯文档 |
| 测评/测验/评估/薄弱点/学习报告 | assessment | 已完成模块 | IMA+闹钟 |
| 设计课程/推荐路径/学习规划/周计划 | recommend | 图谱推导 | 备忘录+日历 |
| 团队备课/协作/版本/批注 | collab | 指定范围 | 腾讯文档+分享 |
| 4周上手/博智坊/SAI新生/每日速递/考前提醒/周报 | ops | E·N 相关 | 全量设备侧 |
| BNBU/SAI/专业代码(BA/GD/AI/FIN…) | 同上 + context.bnbu=true | E·N | 预览+IMA+腾讯文档 |

**歧义消解**：单信号明确 → 直接路由；多信号 → 取最强信号 + 主动澄清 1 次；无任何信号 → 视为 `courseware`（默认教具）。

---

## 3. 智能缺省（让「少问多办」成立）

| 参数 | 缺省 | 依据 |
|------|------|------|
| audience | 大学生 | 历史最常用 |
| difficulty | 2（中等） | 覆盖最广 |
| question_count | 20 | 约 30 分钟 |
| granularity | 单元（2–4 课） | 备课甜点 |
| workbuddy | 预览+本地 | 最安全，不越权 |
| time_available | 每天 1h | 推荐引擎默认 |

> 缺省不等于瞎猜：在 `PLAN` 阶段向用户**展示**已采用的缺省，用户可一键改。只在「信息严重不足且影响方向」时才追问。

---

## 4. 六能力 runbook（执行清单）

### Runbook A · 课件（courseware）
```
INTENT(ability=courseware) → PLAN(选模块/受众/难度)
→ BUILD(p5js-courseware-guide §二：单HTML+说明+实验指南+探索任务)
→ VERIFY(harness 控件实测, ≤3 修复)
→ ASSEMBLE(README+版本+SHA256+离线清单)
→ DELIVER(预览 / IMA)
→ REPORT(门控结果块) → LEARN(可沉淀为 IMA 素材)
```

### Runbook B · 游戏（game）
同 A，差异：`BUILD` 用 `p5js-game-design-guide.md`；`VERIFY` 额外跑 **canvas 烟雾测试**（按键/点击中心/状态推进，捕获崩溃）；`REPORT` 含状态机巡检结论。

### Runbook C · 备课（lesson）
```
INTENT(ability=lesson) → PLAN(智能预填受众/模块/粒度缺省)
→ BUILD(5阶段: 仅缺省未覆盖项才问; 生成教案+题库+PPT大纲)
→ ASSEMBLE(4格式 HTML + JSZip 一键包)
→ VERIFY(文档按钮/下载控件实测)
→ DELIVER(腾讯文档云端 + 分享教研组)
→ REPORT → LEARN(可转评估验证)
```

### Runbook D · 评估（assessment）
```
INTENT(ability=assessment) → PLAN(模块/难度/题量缺省)
→ BUILD(题组 JSON + 单HTML作答+IndexedDB进度)
→ VERIFY(评分逻辑/题型切换实测)
→ DELIVER(报告存 IMA / 腾讯文档 + 设考前复习闹钟)
→ REPORT(薄弱点诊断)
→ LEARN(⭐ 薄弱点→自动生成补学课件/路径建议, 触发新一轮 INTENT auto:true)
```

### Runbook E · 推荐（recommend）
```
INTENT(ability=recommend) → PLAN(目标/基础/时间缺省)
→ BUILD(知识图谱推导路径+大纲+里程碑)
→ DELIVER(⭐ 路径→备忘录学习计划 + 日历周计划)
→ REPORT → LEARN(完成度可回灌优化图谱权重)
```

### Runbook F · 协作（collab）
```
INTENT(ability=collab) → PLAN(范围/成员/角色缺省)
→ BUILD(腾讯文档备课室+IMA共享素材+批注结构)
→ DELIVER(分享链接 + 日历排评审会 + 备忘录待办)
→ REPORT(协作状态) → LEARN(版本沉淀复用)
```

---

## 5. 子 Agent 编排（WorkBuddy 多 Agent 复用）

长任务/批量任务用 WorkBuddy 子 Agent 并行加速（见 `workbuddy-adaptation.md` §1 智能体协作）：
- **builder**（fork 主上下文）：并行生成多模块课件。
- **tester**：专职跑 `playwright-control-test-harness.js`，与主生成解耦，避免上下文污染。
- **packager**：专职 zip + SHA256 + 离线清单。
- **deliverer**：专职 WorkBuddy 原生分发（IMA/腾讯文档/设备侧）。

> 编排铁律：**tester 必须独立**——生成者不自己测自己，保证 §11 门控客观。

---

## 6. 工作流状态报告模板（REPORT 阶段输出）

```markdown
# 工作流状态报告 · {能力名} · {timestamp}
- 意图快照：{Intent JSON 摘要}
- 管线：INTENT✅ PLAN✅ BUILD✅ VERIFY✅ ASSEMBLE✅ DELIVER✅ REPORT✅ LEARN✅
- 验证：控件 N 个，通过 M，修复后通过 K，未过 0
- 分发：IMA✅ / 腾讯文档✅ / 闹钟⏸(未授权) / 分享✅
- 产物：{file} · SHA256 {hash} · {size}KB
- 回流：{LEARN 结论，如「薄弱点 C3 → 已生成补学课件建议」}
- 可追溯 ID：{uuid}
```

---

## 7. 可观测性（对齐商用标准 §5）

每阶段向状态文件追加一条结构化日志：
```javascript
{ ts, stage:'VERIFY', ability:'courseware', module:'C1',
  detail:{ controls:12, pass:11, fixed:1 }, durationMs:8421, errors:[] }
```
长任务据此可断点续跑：`PLAN` 阶段先读已有状态，跳过已完成 stage。

---

## 8. 与既有门控的关系

本引擎**不替代**商用生产标准 12 维度门控，而是把门控「**自动化执行**」：
- 维度 1–8、9–11 → 在对应 stage 自动检查并写入状态报告。
- **维度 12（互动控件全测）** → 由 `VERIFY` 阶段的 `playwright-control-test-harness.js` 自动执行，结果即门控结果块。
- 任一门控不过 → 管线在对应 stage 熔断，禁止进入 `DELIVER`。

> 一句话总结 V6.0：**把 V5.5 的「质量清单」变成「自动跑的质量流水线」**。
