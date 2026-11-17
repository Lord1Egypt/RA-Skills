# DeepSeek Harness 平台全景（2026-08 蒸馏自 666 文档，已与运行实例核对）

> 定位：DSH 是开源 **Coding Agent 运行框架**，核心设计是"**一切皆插件**"——基于 Cordis 元框架，
> 从模型适配器、工具注册、会话日志到 **Agent Loop 本身**都是可替换/可扩展的插件。
> 被喻为"Agent 时代的安卓系统"：既提供"开车"（直接当助手用），更提供"造车"（组装定制 Agent）。

## 1. 平台定位脑图

```
DeepSeek Harness（DSH）
│  = 开源 Coding Agent 运行框架 · "一切皆插件"
│
├─ 底座：Cordis 元框架（vendor/cordis v4）
│    ├─ 时空可组合性（副作用可撤销 + 依赖反应式）
│    ├─ 无特权核心（Agent Loop 也是插件）
│    └─ 自进化（Agent 动态生成工具并热装载，可精确撤回）
│
├─ 四种 Agent 预设（Profile）
│    ├─ 标准模式  standard  — 完整编码 Agent（文件/Shell/检索/Skills/计划/目标/子代理/工作流）
│    ├─ PTC 模式   code      — 标准 + Code Mode SDK（模型用 TS 程序组合多步操作）
│    ├─ 创造模式   cordis    — 会话内动态生成/热加载/调试插件卡片（极客玩法）
│    └─ 极简模式   minimal   — 仅 bash + str_replace_editor 双工具（基准测试）
│
├─ 工程化能力
│    ├─ 长程任务（自主 分析→规划→编码→并发→测试→清理 闭环）
│    ├─ 主动交互（指令不明确时拉起提问 + 建议选项）
│    └─ 透明监控（Trajectory 事件级回放 / Token 仪表盘 / 沙箱授权）
│
└─ 生态（社区插件）
     ├─ 技能类：dsh-code-review（审 PR）/ dsh-find-simplifications / dsh-doc-standards
     ├─ 界面类：dsh-cc-tui（终端 TUI）/ dsh-agent-teams（子代理协作面板）
     ├─ 增强类：ModLens（读图）/ ModSearch（搜索精读）
     └─ 自动化：dsh-automation（定时/固定间隔任务）
```

## 2. 四种预设模式（实测核对）

| 模式 | preset id | 定位 | 对应能力 |
|---|---|---|---|
| 标准模式 | `standard` | 完整编码 Agent | 文件编辑/Shell/网页检索/Skills/计划/目标/子代理/工作流 |
| PTC 模式 | `code` | 标准 + Code Mode SDK | 模型写 TS 程序组合多步操作（`order: 2`） |
| 创造模式 | `cordis` | 会话内动态插件创作 | 动态生成/热加载/预览调试插件卡片（`order` 最高） |
| 极简模式 | `minimal` | 基准测试 | 仅 bash + str_replace_editor 双工具 |

> 666 文档的"PTC 模式"即 preset `code`；"创造模式（Creator）"即 preset `cordis`（本技能运行的模式）。
> 模式选择 = 会话侧工具集差异，**不影响宿主组合装配**（见 [mental-models.md](mental-models.md) 第 3 节）。

## 3. 插件构建两条路径（与 deployment-overview 呼应）

```
路径 A：创造模式动态生成（最快，临时）
  会话内下指令 → 模型调 cordis_define 注册 → 即时渲染预览
  → 会话结束销毁 → 调试满意后手动导出源码（TS/YAML）落盘

路径 B：本地 Skill/插件文件（可复用，持久）
  本地建目录写 SKILL.md/代码 → 配置/命令行加载 → 重启后依然有效
  → 正式化走 cordis.patch.yml 装配 + npm pack（见 [deployment-overview.md](../50-ship/deployment-overview.md)）
```

- 路径 A = 动态插件（⑤，进程内临时）；路径 B = 声明式装配（②，持久）——两路径对应六形态中的两个。
- **导出源码**是路径 A → B 的桥梁：动态调试满意后，把代码固化进磁盘插件。

## 4. 环境要求与安全边界（实操硬约束）

| 项 | 要求 |
|---|---|
| Node.js 版本 | **≥ 22.19.0 或 ≥ 24.0.0**（否则动态注册可能失败） |
| 模型建议 | 创造模式插件开发优先 DeepSeek-V4-Pro（逻辑编排更强） |
| 调试工具 | `dsh --profile creator --dump-config` 打印完整插件加载树（排查挂载/依赖缺失） |
| 安全 | 创造模式是**高信任开发模式**（执行模型生成的代码）——仅在受信任 Workspace 操作 |

> 注：Node 版本下限以官方发布为准，本机实测 Node v22.20 动态注册正常。

## 5. 生态演进背景

- Cordis 理念源于 DeepSeek × 北大论文《一套处理时空可组合性的编程范式》（Spatiotemporal Composability）。
- 已在 **Koishi 聊天机器人框架**生产验证 4 年（4000+ 社区插件）；DSH 是 Koishi-Cordis 的升级版，扩展到自进化 Agent 基础设施。
- 对插件开发者的意义：DSH 插件 = Cordis 插件包（工具 + 事件 + UI 组件），技能全部规范直接适用。
