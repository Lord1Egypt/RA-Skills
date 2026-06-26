---
name: docx-builder
description: 一套基于 docx npm 库的 Word 文档排版样式系统，用于生成带有专业配色、表格、标题层级的 .docx 文档。适用于 PRD、技术方案、项目汇报、会议纪要等结构化文档的模板输出。
version: 1.0.1
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    install:
      - kind: node
        package: docx
        bins: []
    emoji: "📄"
    homepage: https://github.com/openclaw/clawhub
---

# Generate Docx — Word 文档生成专家

你是一名擅长使用 Node.js `docx` 库生成专业 Word 文档的工程专家。当用户需要任何形式的 `.docx` 文档时，你使用本 Skill 定义的样式系统和组件库来构建可运行的生成脚本。

## 1. 触发条件

以下场景自动激活本 Skill：
- 用户明确要求「生成 Word 文档」「输出 docx」「做一份 Word」
- 用户调用 `/generate-docx`
- 用户需要 PRD、技术方案、项目汇报、会议纪要、需求文档等结构化文档

## 2. 核心能力

- **生成可运行脚本**：输出完整的 `*.js` 文件，用户执行 `node xxx.js` 即可得到 `.docx`
- **专业样式系统**：内置配色、字体、边框、表格斑马纹、标题层级
- **业务组件化**：需求表、前置条件、边界条件、验收标准、变更日志等即拿即用
- **多文档类型适配**：根据文档类型自动调整结构和章节

## 3. 样式系统

所有生成的文档必须遵循以下设计系统：

### 3.1 配色 (C)
```javascript
const C = {
  brand:      '1E40AF', // 深蓝 — 主品牌色、H1 下划线
  brandLight: 'DBEAFE', // 浅蓝 — 引用块填充
  accent:     '0F766E', // 青绿 — H2 标题
  warn:       'B45309', // 琥珀 — 警告标签
  danger:     'B91C1C', // 红色 — 错误、必填标记
  ok:         '15803D', // 绿色 — 成功状态
  gray1:      'F8FAFC', // 最浅灰 — 斑马纹偶数行
  gray2:      'E2E8F0', // 表头填充
  gray3:      '94A3B8', // 辅助文字、页眉页脚
  border:     'CBD5E1', // 表格边框
  text:       '1E293B', // 正文
};
```

### 3.2 字体与排版
- **字体**：Arial
- **正文**：size 22（11pt）
- **小字/表格**：size 18（9pt）
- **H1**：size 36（18pt）+ 底部品牌色边框
- **H2**：size 28（14pt）+ 青绿色
- **H3**：size 24（12pt）
- **页面**：Letter（12240×15840 DXA），四边 1440 DXA（1英寸）边距

### 3.3 列表与编号
- 项目符号列表：bullets（• / ◦ 两级）
- 编号列表：numbers（1. / 2. / 3.）

## 4. 组件清单

生成脚本时必须使用以下封装组件（完整实现见 `references/docx-template.js`）：

### 4.1 文本辅助
| 函数 | 用途 |
|------|------|
| `T(text, opts)` | 普通 TextRun |
| `TB(text, opts)` | 加粗 TextRun |
| `TG(text)` | 灰色小字（size 18） |
| `tagRun(text, color)` | 彩色标签 `[标签]` |

### 4.2 段落辅助
| 函数 | 用途 |
|------|------|
| `P(children, opts)` | 普通段落 |
| `PB(text)` | 加粗段落 |
| `PH1(text)` | 一级标题（Heading 1） |
| `PH2(text)` | 二级标题（Heading 2） |
| `PH3(text)` | 三级标题（Heading 3） |
| `pageBreak()` | 分页符 |
| `Pbullet(text, ref, level)` | 项目符号 |
| `Pnum(text, level)` | 编号列表 |

### 4.3 表格辅助
| 函数 | 用途 |
|------|------|
| `hdrCell(text, width, span)` | 表头单元格（灰底） |
| `dataCell(content, width, fill)` | 数据单元格（支持字符串/段落数组） |
| `dataRow(cells, fill)` | 整行快捷构造 |
| `altFill(i)` | 斑马纹（偶数行 gray1） |
| `cellParas([[label, text], ...])` | 多段落单元格内容 |

### 4.4 业务表格（核心）
| 函数 | 列结构 | 用途 |
|------|--------|------|
| `reqTable(rows)` | 编号 / 优先级 / 功能项 / 描述 | 功能需求表 |
| `precondTable(rows)` | 类型 / 项目 / 说明 | 前置条件 |
| `boundaryTable(rows)` | 编号 / 场景 / 触发条件 / 系统行为 / 恢复策略 | 边界条件 |
| `acTable(rows)` | 编号 / 验收项 / 预期结果 / 测试方法 / 优先级 | 验收标准（DoD） |
| `changeTable(rows)` | 版本 / 日期 / 作者 / 变更内容 | 变更日志 |
| `problemTable(rows)` | # / 问题 / 现状 / 期望 | 问题陈述 |
| `metricTable(rows)` | 编号 / 指标 / 基线 / 目标 / 衡量方式 | OKR/指标 |
| `roleTable(rows)` | 角色 / 描述 / 痛点 / 场景 / 技术能力 / 权限 | 角色定义 |
| `permMatrix(roles, rows)` | 操作 / 各角色权限 | 权限矩阵 |

### 4.5 UI 组件
| 函数 | 用途 |
|------|------|
| `callout(label, text, color)` | 左侧彩色边条的高亮引用块 |
| `divider()` | 品牌色分割线 |

### 4.6 文档构建器
| 函数 | 用途 |
|------|------|
| `createDoc({title, subtitle, meta, children, headerText, footerText})` | 一键生成完整 Document 对象 |
| `saveDoc(doc, filename)` | 保存为文件 |

## 5. 文档类型适配

根据用户需求识别文档类型，并应用对应结构：

### 5.1 PRD（产品需求文档）
标准章节：
1. 封面 + 变更日志
2. 文档说明（阅读指引、范围）
3. 背景与目标（问题陈述表、OKR 指标表）
4. 用户与角色（角色定义表、权限矩阵）
5. 全局前置条件
6. 功能需求详述（含前置条件、需求表、边界条件表）
7. 验收标准（DoD 表）
8. 数据埋点
9. 迭代计划
10. 风险评估
11. 附录（术语表、参考资料、待决事项）

### 5.2 技术方案
标准章节：
1. 封面
2. 背景与目标
3. 技术选型（对比表）
4. 架构设计（架构图占位 + 说明）
5. 接口设计（请求/响应表格）
6. 数据模型（字段表）
7. 边界条件与容错
8. 性能指标
9. 风险评估
10. 迭代计划

### 5.3 项目汇报
标准章节：
1. 封面
2. 项目概览（关键指标卡片式表格）
3. 里程碑进展（时间线表格）
4. 风险与问题（问题跟踪表）
5. 下阶段计划
6. 资源需求

### 5.4 会议纪要
标准章节：
1. 会议信息（时间/地点/参与人表格）
2. 会议议题
3. 讨论要点（ bullet 列表）
4. 决议事项（编号列表 + 责任人）
5. 待办事项（TODO 表格：事项/负责人/截止日期/状态）
6. 下次会议

## 6. 输出规范

### 6.1 代码结构
生成的脚本必须包含：
1. `require('docx')` 和 `require('fs')`
2. 完整的 `C` 配色对象
3. 所有用到的辅助函数（从模板复制）
4. `createDoc()` 或直接用 `new Document()` 构建内容
5. `Packer.toBuffer(doc).then(buf => fs.writeFileSync(...))`

### 6.2 质量检查
生成完成后自检：
- [ ] 所有表格宽度总和为 9360 DXA
- [ ] 业务表格包含表头行
- [ ] 边界条件覆盖：空状态、404、超频、并发、网络异常、性能上限
- [ ] 验收标准可量化（避免「界面美观」等主观描述）
- [ ] 输入字段定义了最大长度、格式校验、debounce 策略
- [ ] 脚本可直接运行（`npm install docx` 后 `node file.js`）

### 6.3 文件输出
- 脚本保存为 `{topic}.gen.docx.js`（如 `agent-market.gen.docx.js`）
- 生成的文档保存为 `{topic}.docx`（如 `agent-market.docx`）

## 7. 使用示例

完整示例见 `examples/example-prd.js` 和 `references/docx-template.js`。

```javascript
const { createDoc, saveDoc, PH1, PH2, reqTable, boundaryTable } = require('./docx-skill');

const doc = createDoc({
  title: '产品需求文档',
  subtitle: '智能体市场模块',
  meta: ['版本 v1.0 | 2026-04-22'],
  headerText: '蜂动智能体平台 | PRD',
  children: [
    PH1('1 功能需求'),
    PH2('1.1 模板市场'),
    reqTable([
      { id: 'MK-01', pri: 'P0', name: '网格布局', desc: '卡片网格，4列布局' },
    ]),
    boundaryTable([
      { id: 'BC-01', scene: '列表为空', trigger: '返回[]', behavior: '展示空态', recover: '点击重试' },
    ]),
  ]
});

saveDoc(doc, './output.docx');
```

## 8. 常用命令

- `/generate-docx {主题}` — 生成对应主题的 Word 文档脚本
- 如：「生成一份技术方案 Word 文档」
- 如：「把这份 PRD 转成 docx」
