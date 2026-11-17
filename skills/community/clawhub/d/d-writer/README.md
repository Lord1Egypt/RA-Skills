# Dragon Writer 🐉

一套**工具无关**（tool-neutral）的**长篇虚构小说写作工作流**，兼容各类 AI 编码 agent 使用。

Dragon Writer 把一部长篇拆成一份**可审计、可回滚、跨会话续写**的"文件圣经"，外加一份给作者自己看的**实时进度仪表盘**。**全程不靠记忆，靠文件**。

### ⑤ 写作仪表盘导览

`assets/dashboard.html` 打开即见 4 个标签页，运行时自会读取书源文件，永远反映最新内容。《霜寒之纪》示例：4/200 章、约 1265 字、5 份设定文件、7 位角色（4 主 3 次）。

**① 总览** —— 顶部一枚进度环（带过渡动画），环心大字标百分比，环侧列出"已完成 N / 目标 N 章""约 N 字 / 目标单章 N 字""更新于 …"。环下 6 张统计卡（总章节、目标章节、总字数、平均章字数、单章目标、状态）。其下四块：当前状态（地点/时间、主角、已知真相…）、当前焦点、最近章节（章/标题/角色/事件/心境五列逆序表）、审计漂移（已修复 / 已知漂移两节，按类型着色）、字数趋势（柱状图）。

**② 设定内容** —— 5 份设定文件（故事框架 / 卷纲 / 规则书 / 当前状态 / 风格指南）各一张可展开卡片，展开后原文 Markdown 渲染全文呈现，卡片旁显示字数与完成度。

**③ 人物关系** —— 左侧 `<canvas>` 力导向关系图：**滚轮缩放（0.25–3 倍）、拖拽空白平移、双击适应画布**，右上角 ＋/－/⛶/1:1 视图控制。主要角色圆形实心取主题强调色、次要角色方形虚边取灰色，节点尺寸随连线数略增；初始布局主要内圈、次要外圈。连线为二次曲线，中点药丸标签带碰撞检测不互相覆盖，缩小时自动隐藏次要角色名与边标签。悬停 / 点击节点高亮其直接关系，**右侧详情栏**（与画布等高、内部滚动）同步显示故事功能、欲望、恐惧、当前状态、弧线、秘密与全部关系。下方角色卡网格区分主配（靛蓝色条 +「主要」徽章 / 灰条 +「次要」徽章），支持搜索与层级筛选，点击卡片同样定位并高亮对应节点。

**④ 阅读章节** —— 左栏竖向目录（"第 N 回 · 标题"，当前章高亮），右栏 Serif 字体渲染的 Markdown 章节正文（h1/h2/h3、blockquote、table、code/pre、list 全套样式），章内搜索（Ctrl+F，高亮 + 计数 + 跳转），底栏"‹ 上一章 / 下一章 ›"导航 + "导出全本 TXT"按钮。

---

## 它能做什么

### 5+1 种工作流模式

| 模式 | 触发时机 | 做什么 |
| --- | --- | --- |
| **A · 新书** | 一句灵感 / 书名 / 题材 | 建目录、一口气产出全部基础文件骨架（意图 / 故事框架 / 卷纲 / 角色 / 规则 / 状态 / 钩子） |
| **B · 续写** | 书已存在，往下写 | 读工作集 → 写章节意图 → 起草 → **双层质量门禁**（10 项驻场初筛 + 43 个候选深化审计维度 · 审-改循环） → 落盘 |
| **C · 导入** | 手里有旧章节，缺状态文件 | 从旧章反推基础文件，回放导入章节，续写 |
| **D · 转向** | "换方向 / 下一章写 X" | 轻量调 `current_focus.md`，不改整份大纲 |
| **E · 改写 / 修复** | 重写某一章 | **三步回滚机械**：恢复快照 → 清后续产物 → 重写 → 再走双层质检 |
| **F · 仪表盘** | 看进度 / 关系 / 读章节 | 确保书文件夹下有模板，**双击 HTML 打开**，权限仍有效时自动重连（不承诺永久零交互） |
| **G · 合并审核** | 写完一章 / 连续写完多章后 | 把选定章节合并，子代理统一跑 43 维（时间线 / 设定冲突 / 伏笔 / 去 AI 味…），留痕审计漂移 |

### 双层质量门禁

写一章不是写完就定稿，而是过两层：

1. **驻场初筛（10 点）**——主角是否按动机行动、有没有人知道不该知道的、**空间是否一致、口袋里东西有没有无痕 ±1、常识是否合理、本章开场与上章末物理状态是否衔接**……直接、快速。
2. **43 个候选深化审计维度连续审计 + 审-改循环**——按体裁裁剪出本章节要跑的维度清单（仙侠默认 22–26 维），逐维出报告 → 修订 → **回头从第 1 维再过一遍**（防修 A 打坏 B） → 留痕审计漂移。详见 [`references/audit-dimensions.md`](references/audit-dimensions.md)。

### 写作仪表盘（双击即用）

`assets/dashboard.html` 是一份**运行时模板**，不嵌入任何数据。打开后通过 File System Access API 选择书文件夹（首次授权后 IndexedDB 持久化，权限有效时自动重连），运行时读源文件实时计算：

- 写作进度（进度环、字数、完成度）
- 设定内容全文（5 份设定文件可展开阅读，标注字数与完成度）
- 当前焦点卡片
- **人物关系图**（`<canvas>` 力导向图，缩放 / 平移 / 适应画布，悬停高亮邻居，角色卡区分主配）
- **章节阅读**（目录 + Markdown 渲染 + 章内搜索 + 上一章 / 下一章导航）
- 章节合并导出 TXT
- 审计漂移（已修复 / 已知漂移两节）

### 受保护上下文 vs 可压缩历史

- **静态基础**（premise / 世界法则 / 角色卡 / 规则书）→ 尽量不动。
- **运行时态**（当前状态 / 钩子 / 摘要 / 焦点 / **道具账本 / 空间锚点** / 审计漂移）→ 每章更新。
- **权威顺序**（冲突裁决） ：用户指令 ＞ 当前焦点 ＞ 意图 ＋ 规则 ＞ 状态 / 角色 / 钩子 ＞ 大纲 ＞ 旧摘要 ＞ 旧章节正文。

---

## 项目结构

```
dragon-writer/
  README.md                        # 本文件：总览 + 仪表盘截图（仅源码仓库保留，发布时排除）
  SKILL.md                         # 路由器：触发范围 + 核心规则 + 模式路由 + 自动更新
  _meta.json                       # Skill 元数据：版本号 + slug + 更新配置
  agents/
    openai.yaml                    # 平台 display_name / 默认提示
  references/
    file-contract.md               # 规范布局 + 文件职责 + 权威顺序 + 事务流程 + 快照契约 + Schema
    file-contract.json             # 机器可读文件契约（canonical + aliases + required + consumer）
    templates.md                   # 全部基础文件模板（含新增模板）
    audit-dimensions.md            # 43 维：判定规则 + 分级 + 体裁裁剪 + 四态结果 + 风险驱动 + 维度边界
    workflow.md                    # 路由到各模式文件
    workflow-new-book.md           # 模式 A：创建新书
    workflow-continue.md           # 模式 B：续写
    workflow-import.md             # 模式 C：导入并续写
    workflow-redirect.md           # 模式 D：转向
    workflow-rewrite.md            # 模式 E：改写 / 修复
    workflow-dashboard.md          # 模式 F：仪表盘
    workflow-combined-audit.md     # 模式 G：合并审核
  assets/
    dashboard.html                 # 运行时仪表盘模板（零嵌入数据，构建产物）
    book-skeleton/                 # 书籍骨架（init_book 直接复制）
  scripts/
    _contract.py                   # 共享契约加载器（canonical/aliases/字数/哈希）
    init_book.py                   # 创建新书（含完整示例骨架复制）
    validate_book.py               # 验证书籍完整性（账本一致性机器检查）
    rebuild_index.py               # 重建章节 index（真实字数）
    snapshot_book.py               # 创建 / 验证快照
    rollback_book.py               # 安全回滚
    select_audit.py                # 选择激活的审计维度
    auto_update.py                 # 自动更新检查 / 执行（CLI 优先，回退官方下载）
    build_dashboard.py             # 构建 self-contained dashboard（内联契约 + 质量检查）
    quality_check.py               # 静态质量检查（语法 / no-undef / CSP / 大小）
  tests/
    test_contract.py               # Python 文件契约测试
    test_validate_checks.py        # 账本一致性检查测试（别名/双卡/字数/证据/锚点/性别/维度列）
    test_auto_update.py            # 自动更新测试（版本比较/下载 URL/git 保护/CLI 参数）
    fixtures/
      standard-book/               # 标准书 fixture（通过全部验证）
      timeline-demo-book/          # 时间线演示书 fixture
    js/
      test_dashboard.js            # Dashboard 单元测试（纯函数逻辑）
      test_integration.js          # Dashboard 集成测试（HTML 结构 / ARIA / 函数存在性）
    artifacts/                     # 测试产物（build_size.json / quality_check.json）
  books/
    <book-id>/                     # 一本书
      book.json
      dashboard.html               # 模式 F 注入的模板（仅一份）
      chapters/{index.json, 0001_*.md}
      story/
        author_intent.md / current_focus.md / book_rules.md
        current_state.md / pending_hooks.md / chapter_summaries.md
        audit-drift.md / style_guide.md
        outline/{story_frame.md, volume_map.md}
        roles/{major, minor}/<name>.md
        runtime/{chapter-NNNN.intent.md, *.rewrite.md}
        snapshots/{0000..000N}/
```

> `roles/major/` 与 `roles/minor/` 兼容中文命名 `主要角色/` 与 `次要角色/`。

---

## 核心机制（续写必跑）

续写每章，`current_state.md` 是"硬账本"，下面两个表是本次优化的重点——**没有它们，口袋里东西数和房间门朝哪边都没有参照**：

### 道具账本 Prop Ledger
> `current_state.md` 的新章节，随身物件逐件登记。**数量与存在的变化必须由显式事件驱动**（获得 / 失去 / 消耗 / 赠予 / 被夺 / 碎裂），不可无痕 ±1。

| prop_id | 名称 | 类别 | 数量 | 归属角色 | 存放位置 | 状态 | 最近变化章 | 最近变化事件 |
| --- | --- | --- | ---: | --- | --- | --- | ---: | ---: |
| prop-001 | 回春丹 | 丹药 | 3 | 主角 | 储物袋乙格 | 完好 | 12 | 购买 |
| prop-002 | 青锋剑 | 法器 | 1 | 主角 | 背上剑鞘 | 完好 | 3 | 获赠（师尊） |

### 空间锚点 Spatial Anchors
> `current_state.md` 的新章节，每个反复出现的场景登记一次**固定布局**。后续同场景跨章描写均以此为准；物件位置变化必须有显式事件（拆建、战损、重新布置）。

| anchor_id | 场景名词 | 方位 / 格局 | 出入口 | 关键物件位置 | 建立章 |
| --- | --- | --- | --- | --- | ---: |
| sa-001 | 藏经阁三层 | 八角形中厅，八面经橱按八卦排列 | 西南角木梯 | 中厅八角石台（阵眼） | 7 |

两个表的详细列含义与治理规则见 [`references/templates.md`](references/templates.md)。

### 账本一致性校验（validate_book.py，落盘必跑）

每章落盘后运行 `python scripts/validate_book.py <book-dir>`，用**确定性机器检查**把"正文内部矛盾、账本与正文脱节、文件层分叉"拦在产出环节，而不是靠人工审计兜底：

| 检查 | 抓什么 | 级别 |
| --- | --- | --- |
| 规范名 / 别名并存 | `audit-drift.md` 与 `audit_drift.md` 双源 | error |
| 角色同名双卡 | 同一角色同时存在于 `major/` 与 `minor/`（晋升未清理） | error |
| wordCount 真值 | index 字数与正文重算值偏差 >5%（禁手写，须跑 `rebuild_index.py`） | error |
| 事实表证据链 | fact 的 `evidence` 引文必须在来源章正文命中（防捏造事实） | error |
| 道具 origin 漂移 | origin（来历）跨快照变化而未同步失效旧事实 | warning |
| canon 数字锚点自冲突 | 角色卡锚点表同事项多值无递增生效章 | warning |
| 性别称谓 lint | 女角色被"男的"、男角色被"女的"错称 | warning |
| 维度列一致性 | 角色卡时间线出现 book_rules 未声明的列（如仙侠题材的三围） | warning |
| book.json 生命周期 | status 陈旧 / updatedAt 落后 / skillVersion 不符 | warning |

配套的新 schema 字段：事实表 `evidence`（原文短引）、道具账本 `origin`（来历）、角色卡 `基本信息·性别` + `canon 数字锚点`、`book_rules`「物理数据维度」「逻辑数据维度」声明（时间线列按题材声明，未声明的列不出现）。

### 完整示例书骨架（book-skeleton）

`assets/book-skeleton/` 是一本**内部自洽的完整示例书**（《霜寒之纪》/陆恒），19 个文件全部有可抄的完整示例、**零空目录**：两个示例章节、三张角色卡（含性别 + 数字锚点 + 时间线）、事实表带证据、道具账本带来历、空间锚点带登记、intent 带"前章末状态续接 + 实际偏离记录"。`init_book.py` 建新书时直接复制，模型照此改写，不再凭空猜结构。

---

## 如何使用

### 触发 Dragon Writer

- "帮我写一本仙侠新书，叫《霜寒之纪》" → 模式 A
- "继续写《霜寒之纪》的下一章" → 模式 B
- "把这几章旧稿导入进去" → 模式 C
- "下一章要转到陆恒被追杀" → 模式 D
- "重写第 23 章" → 模式 E
- "看看《霜寒之纪》的进度" → 模式 F
- "把前 5 章合并统一审一遍" → 模式 G

### 打开写作仪表盘

```bash
# 进入某一本书，双击 dashboard.html
start books/<book-id>/dashboard.html       # Windows
open   books/<book-id>/dashboard.html       # macOS
xdg-open books/<book-id>/dashboard.html    # Linux
```

首次选择书文件夹并授权；以后打开，权限仍有效时自动重连（句柄记入 IndexedDB），永远显示最新内容（权限失效后需用户点击授权，不承诺永久零交互）。推荐 **Chrome / Edge**。

### 前置条件

- 一个读过 `references/file-contract.md` 的 LLM agent。
- 任意文件读写能力（Read / Write / Edit 或等价工具）。
- 浏览器支持 File System Access API（**Chrome / Edge 86+**；Safari / Firefox 走 `webkitdirectory` 兼容模式）。

---

## 文档导读

| 想读什么 | 去哪读 |
| --- | --- |
| 整体怎么用、质量门禁、各模式流程 | [SKILL.md](SKILL.md) |
| 每种模式的具体步骤 | [references/workflow.md](references/workflow.md) |
| 规范布局 + 文件职责 + 权威顺序 | [references/file-contract.md](references/file-contract.md) |
| 基础文件模板（新建 / 回填时照抄） | [references/templates.md](references/templates.md) |
| **43 个候选深化审计维度**的规则、分级、体裁裁剪 | [references/audit-dimensions.md](references/audit-dimensions.md) |
| 合并审核（模式 G）流程 | [references/workflow-combined-audit.md](references/workflow-combined-audit.md) |
| 仪表盘模板 | [assets/dashboard.html](assets/dashboard.html) |
| 仪表盘总览标签截图 | [references/tab-overview.png](references/tab-overview.png) |

### 自动更新

Skill 启动时自动检查更新（静默，错误自动跳过）：

```bash
# 检查更新（静默模式，启动时调用）
python scripts/auto_update.py check

# 查看版本状态
python scripts/auto_update.py status --verbose
```

版本控制逻辑：
- 本地版本存储在 `_meta.json` 的 `version` 字段
- 远程版本从 `https://api.skillhub.cn/api/v1/search?q=d-writer` 获取（slug=`d-writer`）
- 语义化版本对比（`x.y.z`）：本地 < 远程时执行更新
- 更新方式：优先 `skillhub` CLI，回退到直接下载 zip（官方端点 `https://api.skillhub.cn/api/v1/download?slug={slug}`）
- 任何错误均跳过，不中断 skill 运行
- **git 工作树保护**：安装目录是 git 工作树且有未提交改动时跳过覆盖（防抹掉源码工作），可用 `--force` 覆盖

### 发布新版（维护者）

改完代码后按以下步骤发版，否则已安装副本的自动更新永远拉不到新版本：

```bash
# 1) 升版本号：SKILL.md frontmatter 与 _meta.json 的 version 同步递增
# 2) 本地测试：python -m pytest tests/ -q
# 3) 从干净暂存副本发布（必须排除注册表禁止的文件类型）：
#    cp -r dragon-writer /tmp/publish-staging/d-writer
#    rm -f 暂存目录/.editorconfig 暂存目录/.gitattributes
#    rm -rf 暂存目录/.pytest_cache 暂存目录/__pycache__
#    rm -f 暂存目录/references/tab-*.png   # 注册表禁止 .png / .editorconfig / .gitattributes
#    skillhub publish /tmp/publish-staging/d-writer --version x.y.z --changelog "..."
# 4) 验证：skillhub verify d-writer@x.y.z 或检查 https://api.skillhub.cn/api/v1/skills/d-writer
#    确认 latestVersion 已指向新版本；若未更新，到 skillhub 控制台确认/激活该版本
# 5) git tag x.y.z 并推送
```

> 注册表文件类型白名单：发布时会拒绝 `.png`、`.editorconfig`、`.gitattributes` 等类型——这些只保留在源码仓库（仪表盘截图等），不进发布包。`publish` 目前不支持 `--namespace`/`--skillId` 链接既有技能，若发布后 `latestVersion` 未指向新版本，需到 skillhub 控制台处理。

### 运行测试

```bash
# Dashboard 单元测试（纯函数逻辑，30 项）
node tests/js/test_dashboard.js

# Dashboard 集成测试（HTML 结构 / ARIA / 函数存在性，38 项）
node tests/js/test_integration.js

# 构建 self-contained dashboard（内联契约 + 质量检查）
python scripts/build_dashboard.py

# 静态质量检查（语法 / no-undef / CSP / 大小，25 项）
python scripts/quality_check.py

# Python 全套测试（契约 + 账本一致性检查 + 自动更新，44 项）
python -m pytest tests/ -q

# 单独跑某一块
python -m pytest tests/test_contract.py -v        # 文件契约
python -m pytest tests/test_validate_checks.py -v # 账本一致性检查
python -m pytest tests/test_auto_update.py -v     # 自动更新
```

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)（若未随附 LICENSE 文件，默认按 MIT 许可条款授权：自由使用、修改、分发，但需保留原始许可声明，且作者不承担任何责任）。
