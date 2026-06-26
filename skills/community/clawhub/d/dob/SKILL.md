---
name: dob
description: 工具箱。
---

# Deep Memory（深层记忆）

分层记忆体系的第二层，负责结构化的知识与技能沉淀。日常高频信息存在 `memory/` 和 `MEMORY.md`，遇到需要长期记住的概念、用法、经验时使用本层。

## 记忆层次决策树

> ⚠️ **区分 memory_search 和 deep-memory：**
> `memory_search`（系统内置工具）只搜索 `MEMORY.md` 和 `memory/`（日常记忆层）。
> 查询技术/工具类内容（如 "@xxx 怎么用"）→ 走下面的决策树，先查 deep-memory。
> 不要用 `memory_search` 替代 deep-memory 查询流程。

```
用户问："我的 xxx 怎么用" / "之前那个 xxx 是在哪个文件"
    │
    ├─→ 检查 MEMORY.md / memory/（日常记忆）
    │       └─→ 有 → 返回，无 → 继续
    │
    ├─→ 检查 DEEP-MEMORY.md 索引（关键字匹配）
    │       └─→ 命中 → 读取对应 deep-memory/*.md
    │
    └─→ 互联网搜索
```

**什么时候用 deep-memory：**
- 用户明确提到某个库、框架、工具的名称
- 想把读过的文档、博客、论文精华存起来备用
- 教用户某个知识点后，希望自己也能记住
- 用户说"把这个存到深层记忆"

**什么时候用 MEMORY/memory：**
- 日常会话中的事实、决定、上下文
- 用户偏好、习惯、项目进展
- 工作进度、非结构化的临时笔记

## 常见错误

**❌ 不要用 `memory_search` 查 deep-memory：**
`memory_search` 是系统工具，只搜 `MEMORY.md` 和 `memory/`，不搜 `DEEP-MEMORY.md` 索引。
即使搜索结果为空，也不代表 deep-memory 里没有对应内容。
正确做法：手动读取 `DEEP-MEMORY.md`（索引表），匹配 keywords，再读对应文件。

**❌ 不要跳过索引表直接搜记忆文件：**
`deep-memory/` 下的文件没有全文索引，必须通过 `DEEP-MEMORY.md` 索引表定位。直接遍历文件是无效的。

## 安装与初始化

skill 安装后需要运行初始化脚本，才能在workspace创建 DEEP-MEMORY.md 和 deep-memory/ 目录：

```bash
node skills/depth-memory/scripts/setup.mjs
```

初始化脚本会自动：
1. 创建 `deep-memory/` 目录
2. 写入一条**验收测试记录**（用于验证系统是否正常）
3. 创建 `DEEP-MEMORY.md` 索引（若不存在）
4. 将测试记录写入索引

**验证：** 初始化完成后，搜索关键字 `深层记忆系统验收测试` 或 `验收测试`，应能命中测试记录。

---

## 目录结构

```
deep-memory/                    ← 记忆文件目录（setup.mjs 创建）
  2026-04-27 13_06_20.md       ← 格式：YYYY-MM-DD HH_MM_SS.md
  2026-04-27 16_10_30.md
  ...
DEEP-MEMORY.md                  ← 索引文件（setup.mjs 创建）
memory/                         ← 日常记忆（第一层）
  YYYY-MM-DD.md                 ← 每日笔记
MEMORY.md                       ← 长期记忆索引（第一层）
skills/depth-memory/
  SKILL.md                      ← 本文件
  scripts/
    setup.mjs                   ← 安装后初始化脚本（首次安装必运行）
    query.mjs                   ← 关键字检索
    add.mjs                     ← 新增记忆（交互式 / 命令行）
```

## 工作流

### 查询流程

```
1. 读取 DEEP-MEMORY.md（索引表）
2. 从用户输入中提取关键字（@库名、英文术语、中文关键词）
3. 遍历索引表格，匹配 Keywords 列：
     - 完全相等 → 优先
     - 包含匹配 → 次之
     - 反向包含（关键字 → 条目关键词）→ 兜底
4. 命中 → 读取对应 deep-memory/YYYY-MM-DD HH_MM_SS.md
5. 无命中 → 互联网搜索
```

### 新增流程

```
1. 确定主题和关键字
2. 将完整内容写入 deep-memory/YYYY-MM-DD HH_MM_SS.md
   （文件名用当前时间，格式固定）
3. 提取关键字更新 DEEP-MEMORY.md 索引表
   （在表头分隔线后插入新行，保持按关键词字母序或时间倒序）
4. 可选：同步更新 memory/YYYY-MM-DD.md 记录本次操作
```

## 索引格式

`DEEP-MEMORY.md` 为 markdown 表格，三列：`Keywords` | `Description` | `File Path`

```markdown
| Keywords | Description | File Path |
| :--- | :--- | :--- |
| @k3000/store, 结构化存储, 本地数据库, 二进制存储, 版本化存储 | 结构化本地存储库，二进制文件 + 加密索引，支持索引查询/范围查询/分页/联合查询 | `deep-memory/2026-05-05 17_49_00.md` |
```

**关键词提取原则：**
- 必须包含库的正式名称（如 `@k3000/store`）
- 必须包含中文核心描述（1-2个词）
- 包含常用别名或相关术语
- 包含核心 API 或特性名称（可选）
- 用逗号分隔，不超过 10 个关键词

**好的关键词示例：**
`@k3000/store, 结构化存储, 本地数据库, 二进制存储, 版本化存储`

**不好的关键词示例：**
`@k3000/store`（缺少中文描述）
`这个库很好用可以存很多东西`（太模糊，无法检索）

## 脚本用法

### query.mjs — 关键字检索

```bash
node scripts/query.mjs <关键字>
```

返回 JSON：
- 命中：`{ found: true, keyword: "...", results: [{ keyword, description, filePath }] }`
- 无命中：`{ found: false, keyword: "..." }`

**匹配逻辑：**
- 关键字 → 索引 Keywords 列（大小写不敏感，包含即命中）
- 兜底：索引 Keywords → 关键字（反向包含）

```bash
# 示例
node scripts/query.mjs @k3000/store
node scripts/query.mjs 结构化存储
```

### add.mjs — 新增记忆条目

支持两种模式：

**交互模式（不带参数）：**
```bash
node scripts/add.mjs
# 按提示输入：标题 → 关键字 → 描述 → 内容（Ctrl+D 结束）
```

**命令行模式（推荐在 agent 内使用）：**
```bash
node scripts/add.mjs <标题> <关键字1,关键字2> <描述> [正文内容...]
# 注意：正文内容为空格分隔，多行内容需用 stdin 或直接写文件
```

实际 agent 用法：直接用 `write` 工具写文件 + 手动编辑 `DEEP-MEMORY.md`，比调用脚本更可控。

### list-index.mjs

此脚本目前不存在。如需列全部索引，直接读取 `DEEP-MEMORY.md` 即可。

## 记忆文件格式规范

每个 `deep-memory/YYYY-MM-DD HH_MM_SS.md` 文件应包含：

```markdown
# <标题>

> 来源：<URL 或来源>
> 存入时间：<YYYY-MM-DD HH:MM>

## 概述

1-3 句话描述这是什么。

## 核心概念

关键术语和定义的简短列表。

## 快速上手 / 典型用法

可运行的最小示例代码。

## API 参考 / 常用操作

表格或列表形式的关键 API。

## 注意事项 / 已知限制

使用时的坑、版本兼容、常见错误。

---

## 其他补充（可选）

FAQ、对比类似工具的优劣、相关链接等。
```

## 维护与更新

**更新已有记忆：**
- 找到对应的 `deep-memory/*.md` 文件，用 `edit` 工具追加或修正内容
- 如果关键词有变化，同步更新 `DEEP-MEMORY.md` 的索引行
- 不要删除旧文件，只追加或修正（保留历史版本）

**合并/整理：**
- 如果两个记忆文件高度相关（如同一库的不同版本用法），可以在尾部用 "===" 分隔分别记录，并注明日期

**定期检查（每 1-2 周）：**
- `DEEP-MEMORY.md` 是否有未匹配的查询（用户说"我存过的"但没找到）
- 索引关键词是否过时（库更新后补充新 API 关键字）

## 常见问题

**Q: 用户问了一个问题，但 deep-memory 没有匹配到怎么办？**
→ 先尝试互联网搜索，找到答案后按"新增流程"存入 deep-memory，下次即可命中。

**Q: 关键词如何确定？**
→ 思考：如果用户想找这个记忆，会怎么描述？把最能想到的 3-5 个词/短语写进 Keywords。

**Q: 存进去之后怎么验证？**
→ 用 `node scripts/query.mjs <关键字>` 测试，确认能返回对应文件路径。

**Q: 需要删除一条记忆怎么办？**
→ 从 `DEEP-MEMORY.md` 索引表中删除对应行，文件可以保留（标记为已废弃）或删除。

**Q: list-index.mjs 不存在怎么列出全部索引？**
→ 直接读取 `DEEP-MEMORY.md` 即可，或写一个简单的 `grep` 命令：
```bash
Select-String "|" DEEP-MEMORY.md | Select-Object -Skip 2
```

**Q: 重新安装 skill 需要重新初始化吗？**
→ 不需要。setup.mjs 做了幂等处理：索引和目录已存在时会跳过，不会覆盖已有数据。
如果需要重新生成测试记录，先删除 `deep-memory/2026-05-07 11_01_00.md` 和索引中的对应行，再运行 setup.mjs。

## 触发条件

遇到以下任务时，**先执行查询流程**，再决定是否新增：

- 用户问一个知识性/技能性问题（优先查 deep-memory，再用 `memory_search` 查日常记忆，最后互联网搜索）
- 用户明确提到某个库、框架、工具的名称（先查 deep-memory 索引）
- 用户提到"之前那个 xxx 怎么用来着"、"存在深层记忆"、"记一下这个"等关键词
- 用户发送了一个 npm 库、GitHub repo 或工具链接，让存入记忆
- 需要帮用户整理某个领域的知识体系
- 读完一篇文档/博客，主动提取关键内容存入 deep-memory

## 相关文件

- `MEMORY.md` — 第一层日常记忆
- `memory/YYYY-MM-DD.md` — 每日会话日志
- `DEEP-MEMORY.md` — 本层索引表