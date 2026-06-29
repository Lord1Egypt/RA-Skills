---
name: doc-compare-craft
version: 1.0.0
description: 双文档输入+智能差异分析，生成并排/内联/红线标注等交互式对比HTML
author: wuwenbin-beijing-st
homepage: https://github.com/wwbwin/clawhub-skills
tags: [visualization, html, tool]
---

# 【简介】

文档修改后的比对是团队协作中的高频痛点。Word 的修订模式在多轮修改后臃肿难读，逐行肉眼比对效率低下，合同、方案、条款的变更差异缺少直观展示。每次版本迭代，团队成员都要花大量时间搞清楚"到底改了什么"。

本 Skill 通过双文档输入 + 智能差异分析 + 交互式对比页面，提供行级 / 词级的变更检测。支持并排对比、内联高亮、合并视图、法律红线标注等多种模式，让每次文档变更都一目了然。

---

# Doc Compare Craft — 文档对比工具 Skill

> 对比两个版本的文档，生成高亮差异的交互式对比页面。
>
> 作者：wuwenbin-beijing-st

## 使用说明

运行此 Skill 后，按以下步骤操作：

1. **粘贴旧版文档**：先输入旧版本的完整文本
2. **粘贴新版文档**：再输入新版本的完整文本
3. **选择对比模式**：从映射表中选择适合的对比方式
4. **选择配色方案**：选择差异高亮配色
5. **生成对比页面**：输出交互式单文件 HTML

### 输入格式建议

- 直接粘贴文本内容（支持中英文混合）
- 对于较长文档，分段落标记方便定位
- 法律文档建议使用 legal-redline 模式

## 场景-模式映射表

| 文档类型 | 推荐模式 | 特点 |
|---------|---------|------|
| 合同/协议 | legal-redline（法律红线） | 逐词对比，法律术语高亮，批注式标注 |
| 技术方案 | side-by-side（并排对比） | 左右对照，段落级差异 |
| 代码/脚本 | word-level（词级精细） | 逐词差异，适合代码审查 |
| 报告/文章 | inline（内联高亮） | 新版中直接标注增删改 |
| 规范/标准 | unified（合并视图） | 统一视图上下文，适合逐行审查 |
| 任意文档 | summary-only（仅摘要） | 仅输出变更摘要，适合快速了解改动 |
| 章节重组 | structural（结构变更） | 检测章节移动、增删、重命名 |

## 配色方案库

### 差异高亮色（默认）
- **新增**（绿色）：`#34d399` bg / `#065f46` text
- **删除**（红色）：`#fca5a5` bg / `#991b1b` text
- **修改**（黄色）：`#fde68a` bg / `#92400e` text
- **移动**（蓝色）：`#93c5fd` bg / `#1e40af` text

### 4 套主题配色

#### 1. 简洁白
```
--bg: #ffffff
--text: #1f2937
--added-bg: #d1fae5
--removed-bg: #fee2e2
--modified-bg: #fef3c7
--moved-bg: #dbeafe
```

#### 2. 护眼暗色
```
--bg: #1e293b
--text: #e2e8f0
--added-bg: #064e3b
--removed-bg: #7f1d1d
--modified-bg: #78350f
--moved-bg: #1e3a5f
```

#### 3. 温和米色
```
--bg: #fefcf6
--text: #3a3a3a
--added-bg: #d4edda
--removed-bg: #f8d7da
--modified-bg: #fff3cd
--moved-bg: #d6f0fc
```

#### 4. 法律正式
```
--bg: #f8f9fa
--text: #18181b
--added-bg: #bbf7d0
--removed-bg: #fecaca
--modified-bg: #fde68a
--moved-bg: #bfdbfe
--strikethrough: #dc2626
```

## 交互增强包列表

### 基础交互
- 视图切换（并排/内联/合并）
- 跳转到下一处差异
- 差异计数统计
- 逐段展开/折叠

### 高级交互
- 过滤变更类型（只显示新增/只显示删除）
- 导出补丁（diff 格式）
- 复制差异片段
- 关键词搜索定位
- 打印优化视图

## 限制说明

- **单文件 HTML**：所有输出均为单一 HTML 文件，CSS 和 JS 全部内联
- **零外部依赖**：不加载任何 CDN 资源、字体、图标库
- **差异算法**：纯 JS 实现的简化版 Myers 差异算法
- **系统字体栈**：font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif
- **浏览器兼容**：Chrome/Firefox/Safari/Edge 最新两版
- **响应式布局**：桌面和移动端均可正常浏览

## 命令定义

### `/doc-compare`
主入口命令。输入旧版和新版两份文档，选择对比模式后生成差异对比页面。

### `/doc-redline`
法律文档专用红线模式。针对合同、协议等法律文档，使用逐词对比 + 法律批注标注。

## 文件结构

```
skills/doc-compare-craft/
├── SKILL.md
├── patterns/
│   ├── side-by-side.json    # 并排对比
│   ├── inline.json          # 内联高亮
│   ├── unified.json         # 合并视图
│   ├── word-level.json      # 词级精细对比
│   ├── legal-redline.json   # 法律红线标注
│   ├── summary-only.json    # 仅变更摘要
│   └── structural.json      # 结构变更对比
└── templates/
    ├── base.html
    ├── side-by-side.html
    ├── inline.html
    ├── unified.html
    ├── word-level.html
    ├── legal-redline.html
    ├── summary-only.html
    └── structural.html
```
