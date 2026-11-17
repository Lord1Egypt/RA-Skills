# AI 通识课资深专家 V6.0（工作流引擎版）

> 🎓 最全面的 AI 通识课教学技能，涵盖 A→G 七大模块、p5.js 课件/游戏、交互式备课、AI 学习评估、协作备课。**V6.0 升级为自动化智能化工作流引擎**：一句话需求即自动跑完「意图→计划→生成→验证→组装→分发→报告→回流」全流程。

## 版本历史

| 版本 | 日期 | 主要变化 |
|------|------|----------|
| V3 | 早期 | 基础课件 + 备课工作流 |
| V4 | 中期 | 游戏化学习 + 交互式问答 |
| V4.3 | 2026-08-05 | 4 格式 zip 打包 + 商用生产级 8 维度 |
| **V5** | **2026-08-14** | **六大能力 + F/G 新模块 + 离线支持 + 协作备课** |
| **V5.5** | **2026-08-25** | **E·N 院校适配 + F/G 课件游戏适配 + WorkBuddy 适配 + 互动控件门控 + meta.json** |
| **V6.0** | **2026-08-26** | **⭐ 工作流引擎：8 阶段管线 + Playwright 控件自动实测闭环 + 智能闭环(评估→补学) + 跨时间运营流 + 原生分发自动化 + 第 13 维工作流门控** |

## ⭐ 六大核心能力

| 能力 | 触发词 | 产出 |
|------|--------|------|
| 能力一 课件 | 「课件」「演示」「教学」 | p5.js 单文件 HTML 互动课件 |
| 能力二 游戏 | 「游戏」「闯关」「冒险」 | p5.js 单文件 HTML 沉浸式游戏 |
| 能力三 备课 | 「备课」「教案」「word/ppt」 | 4 格式文档 + zip 一键打包 |
| **能力四 评估** ⭐ | 「测评」「练习题」「测验」 | 自适应测评 + 薄弱点诊断报告 |
| **能力五 推荐** ⭐ | 「学习路径」「课程规划」 | 个性化课程推荐 + 学习计划 |
| **能力六 协作** ⭐ | 「团队备课」「多人编辑」 | 协作备课室 + 版本管理 |

## 课程模块（A→G）

### 通用基座层
- **A** 认知基础（AI 进化、AI 是什么、协作哲学）
- **B** 工具操作（TRAE IDE、SOLO）
- **C** 方法论（Prompt、需求拆解、验证闭环、多 Agent、飞轮）
- **D** 通用实练（数据分析、Vibe Coding）

### 专业应用层
- **E** 跨学科适配

### 新增层（V5）
- **F** 安全与伦理（AI 安全、数据隐私、偏见公平、伦理责任）
- **G** 最新发展（大模型跃升、AI Agent、前沿应用）

## 🚀 V6.0 工作流引擎（核心升级）

不再「按需零散调用」，而是统一编排成可恢复、可验证、跨时间的工作流：

- **8 阶段管线**：`INTENT → PLAN → BUILD → VERIFY → ASSEMBLE → DELIVER → REPORT → LEARN`
- **自动化验证闭环**：`assets/playwright-control-test-harness.js` 自动枚举并触发课件/游戏的全部互动控件，捕获报错，生成→实测→修复(≤3)→复测
- **智能闭环**：评估薄弱点自动回流为补学课件/路径；课程推荐自动转可执行周计划（写入备忘录/日历）
- **原生分发自动化**：按意图自动接 IMA 知识库 / 腾讯文档 / 设备侧（闹钟·日历·备忘录·分享）
- **跨时间运营流**：`references/automation-ops.md` — 4 周上手自动驾驶 / 每日 AI 速递 / 考前复习提醒 / 教研组周报
- **长任务可恢复**：`assets/workflow-state-template.json` 状态骨架，断点续跑
- **随技能样例库**：`examples/` 收纳 11 个已通过 VERIFY 门控的真实可运行样例（覆盖六大能力 + A→G 全模块含 E·N），按能力分目录、语义化命名，入口 `examples/INDEX.md` — 可作教学演示、生成模板与回归基线
- 详见 `references/workflow-orchestrator.md`（引擎中枢）与 `references/skill-analysis-v6.md`（升级依据）

## 技术特性

| 特性 | 说明 |
|------|------|
| p5.js 2.x | 2D/3D 互动课件与游戏 |
| 离线支持 | Service Worker + IndexedDB |
| 文档生成 | Excel + Word + PPT + PDF + ZIP |
| 评估系统 | 自适应测评 + 薄弱点诊断 + 补学回流 |
| 协作系统 | 腾讯文档实时协作 + 版本管理 + 批注 |
| 工作流引擎 | 8 阶段管线 + Playwright 自动实测 + 可恢复状态 |
| 商用标准 | 13 维度 SLA/门控 + 15 项 QA 门控 + 工作流编排门控 |

## 文件结构

```
ai-literacy-expert-v5/
├── SKILL.md                              # 核心技能定义（V6.0 工作流引擎版）
├── README.md                             # 本文件
├── meta.json                             # 技能元数据（v6.0.0）
├── assets/                               # 可复用自动化资产
│   ├── playwright-control-test-harness.js  # VERIFY 阶段：控件自动实测
│   └── workflow-state-template.json        # 长任务可恢复状态骨架
├── examples/                             # ⭐ 随技能分发的「模块×能力」样例库（11 个已验证产物）
│   ├── INDEX.md                          # 模块×能力矩阵 + 样例清单
│   ├── courseware/  game/  lesson/  assessment/  recommend/  collaboration/
│   └── （按能力分目录，详见 examples/INDEX.md）
├── references/
    ├── workflow-orchestrator.md         # ⭐ V6.0 工作流编排引擎（中枢）
    ├── automation-ops.md                 # ⭐ V6.0 跨时间运营流
    ├── skill-analysis-v6.md              # ⭐ V5.5→V6.0 深度分析与依据
    ├── workbuddy-adaptation.md           # WorkBuddy 适配总纲
    ├── module-e-bnbu-sai.md              # E·N BNBU/SAI 院校子模块
    ├── assessment-guide.md               # AI 学习评估师指南
    ├── recommendation-engine.md          # 智能推荐引擎指南
    ├── collaboration-guide.md            # 协作备课室指南
    ├── commercial-production-standards.md # 商用生产级标准（含 §11 控件测试）
    ├── p5js-courseware-guide.md          # 课件开发指南
    ├── p5js-game-design-guide.md         # 游戏开发指南
    ├── offline-support-guide.md          # 离线支持指南
    ├── interactive-lesson-builder-guide.md  # 交互式备课指南
    ├── module-a-cognition.md … module-g-latest-developments.md  # A→G 模块内容
    └── audit-report.md                   # V4.3→V5 审核报告
```

## 快速开始

### 生成课件
```
用户：做一个关于"Prompt 优化"的互动课件
AI：[生成 p5.js 单文件 HTML 课件]
```

### 生成游戏
```
用户：设计一个"Prompt 大冒险"游戏
AI：[生成 p5.js 单文件 HTML 闯关游戏]
```

### 生成备课包
```
用户：帮我备一节"AI 是什么"的课，受众是高中生
AI：[5 阶段对话] → [生成 4 格式文档 + zip 打包]
```

### 测评学习效果
```
用户：测评一下我 C 模块的学习效果
AI：[生成 20 道自适应测评题] → [评分 + 薄弱点诊断 + PDF 报告]
```

### 推荐学习路径
```
用户：我是零基础，想系统学习 AI，应该从哪里开始？
AI：[分析目标 + 生成个性化学习路径图]
```

### 团队协作备课
```
用户：创建一个"初中 AI 课"协作备课室
AI：[创建协作空间] → [邀请成员] → [分工编辑] → [版本管理]
```

### 🚀 工作流自动化（V6.0）
```
用户：给 BNBU 新生做 4 周 AI 上手包，自动推进
AI：[INTENT 路由 ops] → [PLAN 4 周路径] → [BUILD 每周课件+游戏+自测]
   → [VERIFY Playwright 自动实测全部控件] → [ASSEMBLE zip+SHA]
   → [DELIVER 日历排课+闹钟+IMA 落库+腾讯文档周包]
   → [REPORT 工作流状态报告] → [LEARN 结课测评回流]
```

### 一键跑完整链路
```
用户：把"C1 Prompt"做成课件，自动测完直接存 IMA
AI：走 8 阶段管线，VERIFY 阶段自动实测 → 全过 → 存 IMA 知识库 → 附门控结果块
```

## 离线使用

V5 支持完全离线使用：

1. **首次加载**：自动缓存所有核心资源
2. **离线使用**：断网后仍可使用已缓存功能
3. **自动同步**：联网后自动同步离线期间的数据

## 与旧版本兼容

| 版本 | 状态 | 说明 |
|------|------|------|
| V3 | ✅ 保留 | 完全兼容 |
| V4 | ✅ 保留 | V5 完全兼容 V4 |
| V4.3 | ✅ 保留 | V5 完全兼容 V4.3 |
| V5 / V5.5 / V6.0 | ✅ 同注册 id | V6.0 完全兼容 V5 全部能力，并叠加工作流引擎 |

## 质量保证

每个交付物必须通过：
- **15 项 QA 门控**（V4.3 的 12 项 + V5 新增 3 项）
- **13 维度商用标准 / 强制门控**（含 V6.0 第 13 维「工作流编排门控」与第 12 维「互动控件全测」——后者由 Playwright 自动实测）
- **8 阶段工作流管线完整跑通** + 工作流状态报告
- **教学准确性验证**

## 联系方式

如有问题或建议，请联系技能维护团队。
