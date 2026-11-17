# Skill Handoff: 数字内容资源入库流程（content-to-asset-ingest）

> 本文件由 workflow-structurer 的五阶段渐进式澄清协议生成。
> Phase 1 目标澄清 → Phase 2 步骤骨架 → Phase 3 逐步骤下钻（输入/输出/职责/风险/校验/规则）→ Phase 4 汇总确认 → Phase 5 handoff 摘要。

## Goal
把一份可用的数字内容，按标准结构打包并稳定地发布到 ClawHub 资源中心，使其可被检索、可被安装。

## Trigger Phrases
- "把这份内容入库 / 发布到资源中心"
- "整理一个可发布的 skill 资产"
- "content-to-asset ingest"
- "帮我把成果沉淀到 ClawHub"

## Steps

### Step 1: 内容就绪与校验（Prepare & Validate）

**Input:**
- 一份待入库的数字内容（Markdown / 文本文件）
- 一个拟用的 slug（kebab-case，全局唯一）

**Output:**
- 一份本地校验通过、形状符合"可发布 skill"的目录

**Responsibilities:**
- 确认内容非空、可读、无占位符；确认目录含 SKILL.md 与 references/。

**Risks:**
- 内容是空文件或含 TODO；缺 SKILL.md 导致 publish 被拒；slug 与他人冲突。

**Validation:**
- `ls -R collab-asset` 能看到 SKILL.md 与至少一个 references/*.md；`test -s collab-asset/SKILL.md` 通过。

**Rules:**
- SKILL.md 必须含 frontmatter（name + description）。
- slug 必须 kebab-case 且事先用 search 确认未被占用。

### Step 2: 本地打包（Package）

**Input:**
- Step 1 通过的目录与元数据（name、tags、topics）

**Output:**
- 形状规范的发布目录：collab-asset/ 下含 SKILL.md 与 references/DESCRIPTION.md

**Responsibilities:**
- 把上游流程产物（handoff）写入 references/DESCRIPTION.md，保证描述质量。

**Risks:**
- DESCRIPTION.md 为空导致入库后无检索价值；标签/主题拼写错误。

**Validation:**
- `wc -l collab-asset/references/DESCRIPTION.md` > 0；文件 UTF-8 无乱码。

**Rules:**
- DESCRIPTION.md 不能为空；name/topics 不能为空字符串。

### Step 3: 预览发布（Dry-run publish）

**Input:**
- 打包好的目录 + 元数据 flag

**Output:**
- 一次不触网的发布预览结果（校验结构与元数据）

**Responsibilities:**
- 运行 `clawhub publish ... --dry-run`，确认无报错、元数据预览正确。

**Risks:**
- 跳过 dry-run 直接发布导致脏数据上线；未登录导致鉴权失败。

**Validation:**
- 命令退出码为 0；输出里 name/slug/tags 与预期一致。

**Rules:**
- 正式发布前必须先有一次成功的 dry-run；`clawhub whoami` 必须返回有效账号。

### Step 4: 正式入库（Publish）

**Input:**
- dry-run 通过的同一条命令（去掉 --dry-run）

**Output:**
- ClawHub 资源中心出现该条目（可能有审核延迟）

**Responsibilities:**
- 执行正式 publish，记录返回的版本号/日志。

**Risks:**
- 网络抖动导致重复发布；审核未过被驳回；slug 临时被抢注。

**Validation:**
- 命令退出码为 0 且返回成功信息。

**Rules:**
- 同一 slug 发布失败后不要无限重试；间隔后退避。

### Step 5: 入库核验（Verify）

**Input:**
- 已发布的 slug

**Output:**
- 可被 `clawhub search` 检索到的确认

**Responsibilities:**
- 用 search 验证成果可见；必要时等待审核通过后再查。

**Risks:**
- 误以为失败而重复发布；忽略审核延迟导致反复操作。

**Validation:**
- `clawhub search <slug>` 返回该条目。

**Rules:**
- 新条目可能有短暂审核/索引延迟，至少等待一次再下结论。

## Key Rules
- 不跳步：先准备/打包 → dry-run → publish → verify。
- 发布前必须 `clawhub whoami` 有效 + 一次成功 dry-run。
- slug 全局唯一且 kebab-case；DESCRIPTION.md 不能为空。
- 新条目检索不到时先考虑审核延迟，不要重复发布。

## Key Risks
- 缺 SKILL.md 或 frontmatter → publish 被拒。
- slug 冲突 / 重复发布。
- 跳过 dry-run 把脏数据推上线。
- 把审核延迟误判为失败。

## Validation Summary
- 本地：`ls -R` 结构正确、SKILL.md 非空、DESCRIPTION.md 非空。
- 远端：dry-run 退出码 0 → publish 退出码 0 → `clawhub search <slug>` 命中。

## Suggested Skill Name
content-to-asset-ingest
