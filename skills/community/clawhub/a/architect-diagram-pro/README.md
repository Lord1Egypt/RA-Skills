# 架构图生成 (architect-diagram-pro)

本地优先的架构图与结构图生成工具。纯本地渲染，无需云端、无需 node、无需 API Key。

## 功能特性

- **四层设计**：语义层 → 护栏层 → 模板层 → 生成层双轨
- **三不变式**：解引用一切 / 论证而非展示 / 一图一主题
- **双输出轨道**：自包含 HTML、内联 SVG，以及 Mermaid 代码块
- **内置护栏**：类型边界、文字避让（防压字）、Token 高效复用、渲染前自检与出错重试
- **零外部依赖**：不引入任何 CDN、外部字体或脚本；仅用系统字体栈，离线 / 国内环境可用

## 触发场景

当用户要求画架构图、系统图、模块图、流程图、时序图、状态机、网络拓扑图、ER 图、数据流图、微服务 / 云原生架构图、甘特图，或提到「画个图」「架构图」「系统图」「拓扑图」「时序图」「draw / diagram / flowchart / architecture」时触发。

## 支持的图类型

系统 / 微服务 / 分层架构图、网络拓扑图、业务流程图、数据流图、时序图、状态机图、ER 图 / 类图、甘特图。

## 暂不支持（遇到会先说明 + 原因 + 替代方案，再等确认）

统计图（饼 / 柱 / 折线）、3D / 地图、思维导图、PNG / PDF 直出、反向工程（由图生成代码）、实时数据接入。

## 输出形态

| 形态 | 适用场景 |
| --- | --- |
| 自包含 HTML | 概览 / 分享；暖色极简、系统字体、响应式 |
| 内联 SVG | 精细 / 多类型 / 对话直看 |
| Mermaid 代码块 | 进文档 |

## 包结构

```
architect-diagram-pro/
├── SKILL.md
├── README.md
├── assets/
│   └── template.html            # 暖色自包含 HTML 模板
└── references/
    ├── three-invariants.md       # 三不变式与展示意图边界
    ├── capability-matrix.md      # 类型边界 ✅/❌ 与硬规则
    ├── clarification-gate.md     # 澄清三问 + 确认门 + scenarios 高亮
    ├── svg-efficient-template.md # Token 高效 SVG 复用模板
    ├── arrow-text-clearance.md   # 文字避让规范
    ├── architecture-layout.md    # 分层架构布局规范
    ├── diagram-types.md          # 各类型：最佳实践 → 反模式 → 骨架
    ├── html-template-guide.md    # HTML 模板使用与扩展
    ├── self-check-and-errors.md  # 渲染前自检 + 四段式出错与重试
    └── faq.md                    # 范围与异常排查
```

## 工作流（概要）

1. **澄清**：意图 / 类型 / 输出形态不清时，用 ≤3 选项提问
2. **语义规划**：三不变式 + 坐标预演（Mental Sandbox）
3. **能力边界预检**：对照类型矩阵，❌ 区先说明不支持 + 原因 + 替代
4. **选轨道**：HTML / SVG / Mermaid
5. **生成**：多视图拆分前走确认门（scenarios 高亮优于复制多份图）
6. **自检与重试**：逐条核对强制规则，出错按「现象 → 原因 → 修复 → 重试校验」处理

## 使用说明

- 产物生成在当前工作区内，不要求联网鉴权或配置任何 API Key。
- 导出 PNG / PDF：HTML 请在浏览器「打印 / 另存为 PDF」或截图；SVG 可复制后自行保存。
- 节点建议 ≤20，超出先提议拆分或走 scenarios 高亮单条链路。
- 文件与专有名词先拍平为自包含语义再绘图，不只读词成框。
