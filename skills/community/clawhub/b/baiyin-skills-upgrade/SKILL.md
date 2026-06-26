---
name: baiyin-skills-upgrade
version: 1.0.0
description: |
  检查并更新本地 baiyin skills 到 SkillHub 中的最新版本。
  用于 `skill/` 目录下的百音技能在执行前做远程版本检查、按需升级、
  回滚失败更新，并在升级完成后继续原始技能任务。
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# /baiyin-skills-upgrade

检查并更新本地 `skill/` 目录下的 baiyin skills。

适用范围：

- `skill/baiyin-video-skill`
- `skill/baiyin-image-generate-skill`
- `skill/baiyin-music-generate`
- `skill/baiyin-voice-generate-skill`
- `skill/baiyin-cover-sing-skill`
- `skill/baiyin-cover-train-skill`
- `skill/baiyin-digital-human-lipsync`
- `skill/baiyin-track-separation-skill`

不处理当前升级 skill 自身目录 `skill/baiyin-upgrade`。

## 内联升级流程

当其他 baiyin skill 的启动前导检测到远程版本更新时，引用本节。

### 第 1 步：识别当前目标 skill

先确定当前要升级的是哪个本地 skill 目录。

规则：

- 如果当前 skill 已明确知道自己的目录，直接使用该目录
- 否则从当前执行上下文中定位 `skill/<slug>/SKILL.md`
- 目标目录必须位于项目根目录下的 `skill/` 中
- 如果目标目录是 `skill/baiyin-upgrade`，直接跳过，不要自升级

目标目录确认后，读取本地元数据：

```bash
LOCAL_META="<target_skill_dir>/_meta.json"
LOCAL_SKILL_MD="<target_skill_dir>/SKILL.md"
```

若 `_meta.json` 不存在，则视为无法进行远程比对，只继续当前 skill，不做升级。

### 第 2 步：读取本地版本信息

从 `_meta.json` 读取以下字段：

- `ownerId`
- `slug`
- `version`
- `publishedAt`

要求：

- `ownerId` 必须是 `baiyin`
- `slug` 必须与目录名一致
- 比较远程版本时，优先比较 `publishedAt`
- 若 `publishedAt` 相同，再比较 `version`

如果本地元数据损坏、缺字段或无法解析，告诉用户：

`当前 skill 的本地元数据不完整，跳过自动升级，继续执行当前任务。`

### 第 3 步：查询 SkillHub 远程版本

使用当前宿主环境已有的 SkillHub 查询能力读取远程 skill 元数据。

查询输入：

- `ownerId`
- `slug`

期望取得远程结果中的至少这些字段：

- `version`
- `publishedAt`
- `files` 或完整 skill 包内容

要求：

- 不要自行猜测其他 `ownerId`
- 不要把别的 skill 的返回结果套用到当前 skill
- 若当前环境已有 SkillHub 查询脚本、MCP、CLI 或 API 封装，优先使用现成能力
- 只有在宿主环境明确提供 SkillHub HTTP 接口说明时，才直接请求 HTTP；不要凭空编造 URL

如果查不到远程结果：

- 静默放弃升级
- 继续当前 skill 原任务

### 第 4 步：判断是否需要升级

仅在以下任一条件满足时才升级：

- 远程 `publishedAt` 大于本地 `publishedAt`
- 远程 `publishedAt` 相同，但远程 `version` 高于本地 `version`

如果远程没有更新：

- 直接继续当前 skill 原任务
- 不额外提示“已是最新版本”，除非用户显式调用 `/baiyin-skills-upgrade`

### 第 5 步：询问用户或自动升级

首先检查是否启用 baiyin skill 自动升级：

- 优先读取宿主环境已有的 baiyin skill 配置
- 如无专门配置，可读取环境变量 `BAIYIN_SKILL_AUTO_UPGRADE`

如果自动升级开启：

- 记录：`Auto-upgrading baiyin skill <slug> v{old} -> v{new}...`
- 跳过用户确认，直接进入第 6 步

否则，使用 `AskUserQuestion` 询问：

- 问题：`百音技能 <slug> 有新版本（当前 v{old}，最新 v{new}），现在更新吗？`
- 选项：
  - `Yes, upgrade now`
  - `Always keep baiyin skills up to date`
  - `Not now`
  - `Never ask again`

分支处理：

- 选择 `Yes, upgrade now`：进入第 6 步
- 选择 `Always keep baiyin skills up to date`：
  - 写入自动升级配置
  - 提示 `已开启 baiyin skills 自动升级。`
  - 进入第 6 步
- 选择 `Not now`：
  - 写入本地延后标记
  - 本次不再重复提醒
  - 继续当前 skill 原任务
- 选择 `Never ask again`：
  - 写入关闭更新检查配置
  - 继续当前 skill 原任务

### 第 6 步：备份本地 skill

升级前先备份当前目录：

```bash
BACKUP_DIR="<target_skill_dir>.bak"
```

规则：

- 若已存在旧备份目录，先删除该旧备份，再创建新备份
- 备份内容至少包含：
  - `SKILL.md`
  - `_meta.json`
  - `references/`
  - `scripts/`
  - `assets/`
  - 其他当前 skill 目录内文件

### 第 7 步：拉取并覆盖最新 skill 内容

从 SkillHub 取回远程 skill 的完整内容后，覆盖本地目标目录。

覆盖原则：

- 只更新当前 `<target_skill_dir>`，不要误改其他 skill
- 远程若包含 `SKILL.md`、`_meta.json`、`references/`、`scripts/`、`assets/`，按目录结构完整覆盖
- 远程若删除了某些旧文件，本地也应同步删除，避免保留陈旧资源
- 不要改动目标 skill 目录外的任何内容

如果宿主环境返回的是压缩包、文件列表或对象存储下载地址，都按“还原为 skill 目录完整快照”的结果处理。

### 第 8 步：校验更新结果

覆盖完成后至少检查：

- `<target_skill_dir>/SKILL.md` 存在且非空
- `<target_skill_dir>/_meta.json` 存在且可解析
- 新 `_meta.json` 的 `ownerId` 仍为 `baiyin`
- 新 `_meta.json` 的 `slug` 与目标目录匹配
- 新版本信息确实等于远程版本

如果当前 skill 自带 `scripts/`：

- 仅做轻量存在性检查
- 不要因为未知外部依赖而主动跑高风险脚本

### 第 9 步：失败回滚

在以下任一情况发生时，必须回滚：

- 远程文件获取失败
- 覆盖中断
- `SKILL.md` 丢失或为空
- `_meta.json` 不可解析
- 新 `slug` 或 `ownerId` 与目标 skill 不匹配

回滚动作：

- 删除当前损坏的新目录
- 用备份目录恢复原目录

回滚后提示用户：

`百音技能 <slug> 自动更新失败，已恢复到本地旧版本。`

然后继续当前 skill 原任务。

### 第 10 步：清理升级标记

升级成功后：

- 清理该 skill 的延后提醒状态
- 写入最近一次升级记录
- 删除本次备份目录

可记录的信息：

- `slug`
- `oldVersion`
- `newVersion`
- `oldPublishedAt`
- `newPublishedAt`
- `upgradedAt`

### 第 11 步：展示变更摘要

仅在确实完成升级后，向用户输出简短摘要：

```text
百音技能 <slug> 已更新：v{old} -> v{new}

已继续执行当前任务。
```

如果远程返回了更新说明，可补充 3-5 条高信号变更；否则不要编造更新内容。

### 第 12 步：继续原任务

升级流程完成后，回到原始 baiyin skill 的主流程继续执行。

要求：

- 不要让用户重复输入刚才已经给过的业务参数
- 不要在升级完成后停住等待，除非原任务本身需要用户继续选择
- 如果升级前已经进入某个交互步骤，升级后从该步骤继续

---

## 独立使用

当用户直接调用 `/baiyin-skills-upgrade` 时：

1. 先枚举 `skill/` 下全部 baiyin skills
2. 逐个读取 `_meta.json`
3. 逐个查询远程版本
4. 列出：
   - 可升级的 skill
   - 已是最新的 skill
   - 无法检查的 skill
5. 如果存在可升级项，再询问用户是否批量升级

批量升级要求：

- 默认只升级有更新的项
- 某个 skill 升级失败时，仅回滚该 skill
- 不影响其他 skill 继续升级
- 最终输出逐项结果摘要

批量模式输出格式：

```text
百音 skills 检查完成

可升级：
- baiyin-video-skill: v1.0.0 -> v1.1.0
- baiyin-image-generate-skill: v1.0 -> v1.1

已最新：
- baiyin-music-generate

检查失败：
- baiyin-track-separation-skill
```

## 回复规则

- 不要编造 SkillHub 接口地址、认证方式或返回结构
- 不要在无法确认远程内容时硬做覆盖
- 不要升级 `skill/baiyin-upgrade` 自身
- 不要改动 `skill/` 目录外文件
- 不要在升级失败后保留半更新状态
- 用户未显式调用升级 skill 时，若远程无更新，应静默继续原任务
