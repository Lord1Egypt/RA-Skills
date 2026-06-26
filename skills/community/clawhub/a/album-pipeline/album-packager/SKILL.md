# Album Packager — 发布物料打包 Skill

> Phase 6 总入口。编排 6 个子模块：专辑统筹更新 → 宣传文档 → 艺人说 → 封面概念 → 平台检查 → 最终打包。

---

## 核心原则

1. **绝对文件契约**：所有输入/输出严格遵循 `FILE_CONTRACTS.md`，不得偏离
2. **子 agent 强制分离**：6 个子模块各为独立的 `sessions_spawn` 调用，按 6.1→6.6 顺序串行执行，不得合并为单个 agent
3. **主 agent 只编排**：主 agent 负责启动/等待/判断完成，不直接撰写任何文档

---

## 子模块索引

| 子模块 | 路径 | 说明 |
|--------|------|------|
| Phase 6.1 | `phase6-album-overview-updater/SKILL.md` | 专辑统筹文档更新（评分转换/曲目单补全） |
| Phase 6.2 | `phase6-promotional-writer/SKILL.md` | 宣传文档（一句话概念/简介/社交文案/制作信息） |
| Phase 6.3 | `phase6-artist-story-writer/SKILL.md` | 艺人说文案（中文长版/英文长版/短版/金句） |
| Phase 6.4 | `phase6-cover-designer/SKILL.md` | 封面概念方案（≥3 方向/配色/应用场景） |
| Phase 6.5 | `phase6-platform-checker/SKILL.md` | 平台适配检查（网易云/QQ 音乐） |
| Phase 6.6 | `phase6-packager/SKILL.md` | 最终打包（zip + 上传清单） |

**执行顺序**：6.1 → 6.2 → 6.3 → 6.4 → 6.5 → 6.6（串行依赖）

---

## 启动前提示（用户心理预期管理）

**⚠️ 飞书推送机制关键：消息在 turn 结束后才推送。必须先输出提示文本，然后 spawn 子 agent，最后 `sessions_yield`。**

**正确流程：**
1. 主 agent 输出提示：
   > 🪚 Phase 6 发布物料打包已启动。6 个子模块串行（专辑统筹 → 宣传文档 → 艺人说 → 封面 → 平台检查 → 打包）。预计约 **30-45 分钟** 完成。完成后我会主动通知你，无需等待。
2. 按顺序 spawn 子 agent（6.1 → 6.2 → 6.3 → 6.4 → 6.5 → 6.6）
3. `sessions_yield` 结束当前 turn

---

## 触发

Phase 5 完成后，用户指令：
- 「打包发布物料」
- 「Phase 6」
- 「album packaging」

---

## 输入

- `docs/album-overview.md`（Phase 1 骨架，需补充完整）
- `songs/TN-*.md`（每首歌的封面高光文案、市场评估）
- `generate/cn_320k/` 和 `generate/en_320k/` 最终曲目（用于制作信息）
- `assets/` 封面概念图

---

## 执行

### ⚠️ 修改范围
- **读取**：`docs/album-overview.md`、`songs/TN-*.md`、`generate/cn_320k/`、`generate/en_320k/`、`assets/`
- **写入**：`docs/` 下的新文档文件 + 压缩包
- **禁止**：修改 `songs/` 或 `generate/` 目录中的任何文件

### 1. 专辑统筹文档（`docs/album-overview.md`）

补充完整：
- ✅ 专辑概述（Phase 1 已有）
- ✅ 曲目单（含最终时长/选定 Take）
- ✅ 英文专辑信息（Album Name / Description / Creator's Note）
- ✅ Track One-Liners（每首歌一句话介绍）
- ✅ 评分总览（Phase 2 的 5 维度评分表：韵律/市场/结构/哲学/编排）
  - 同时将 Phase 1 原始 4 维度评分保留为「## Phase 1 概念评分」历史参考子区块
- ⏳ 待办事项更新

### 2. 宣传文档（`docs/promotional-materials.md`）

从模板 `templates/promotional-materials.md` 初始化，填充：
- 一句话专辑概念
- 专辑简介（~300 字）
- 核心宣传语（3 条）
- 各曲高光文案（从 `songs/TN-*.md` 提取封面高光文案）
- Social Media 文案（微博 140 字/小红书 200-300 字/微信推文标题 ×3）
- 制作信息（AI 工具/规模/输出标准）
- 潜在争议点与回应预案

### 3. 艺人说文案

从模板 `templates/artist-story.md` 初始化，生成：
- `docs/artist-story-cn.md` — 中文长版（~1800 字）
- `docs/artist-story-en.md` — 英文长版（~1400 词）
- `docs/artist-story-short.md` — 中英文短版（各 ~400 字/词）
- `docs/artist-story-quotes.md` — 金句提取（5 条中英对照）

**叙事策略**：不隐藏 AI 生成事实，将其转化为专辑最诚实的隐喻。

### 4. 封面方案（`docs/cover-concept.md`）

从模板 `templates/cover-concept.md` 初始化，填充：
- ≥ 3 个视觉方向（含概念描述）
- 配色方案（含 HEX 色值）
- 每首歌的封面概念
- 应用场景（流媒体/实体/社交/MV + 尺寸要求）

### 5. 平台适配检查

检查最终产物是否符合目标平台要求：

| 检查项 | 网易云 | QQ 音乐 |
|--------|--------|--------|
| 格式 | MP3 320kbps ✅ | FLAC 优先，MP3 320kbps ✅ |
| 采样率 | 44.1kHz ✅ | 44.1kHz ✅ |
| 响度 | -14 LUFS ✅ | -14 LUFS ✅ |
| 最短时长 | ≥ 60 秒 | ≥ 60 秒 |
| 最长时长 | ≤ 6 分钟 | ≤ 6 分钟 |
| 最低曲目数 | 3 首 | 3 首 |
| 必填信息 | 专辑名/曲目/艺人 | 专辑名/曲目/艺人 |

生成 `docs/platform-check.txt`：
```
网易云音乐: ✅ 全部通过
QQ 音乐: ✅ 全部通过
```

### 6. 打包

```bash
cd <project-root>
zip -r <专辑名>-宣传物料.zip \
  docs/album-overview.md \
  docs/promotional-materials.md \
  docs/cover-concept.md \
  docs/artist-story-cn.md \
  docs/artist-story-en.md \
  docs/artist-story-short.md \
  docs/artist-story-quotes.md \
  docs/platform-check.txt
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | album-overview 完整 | 曲目单 + 评分总览 + 英文信息 + Track One-Liners |
| 2 | 艺人说 4 文件 | 中文长版 + 英文长版 + 中英短版 + 金句 |
| 3 | 宣传文档 | 一句话概念 + 300 字简介 + 各曲高光 + 社交媒体文案 + 制作信息 + 争议预案 |
| 4 | 封面方案 | ≥ 3 个视觉方向 + 配色（HEX）+ 应用场景 |
| 5 | 制作信息准确 | 标注 AI 生成工具、规模、输出标准 |
| 6 | 平台适配检查 | 网易云/QQ 音乐各项要求全 ✅，`docs/platform-check.txt` 已生成 |
| 7 | zip 内容完整 | 压缩包包含全部 8 个文档文件（含 platform-check.txt） |
| 8 | zip 打包 | 全部文档文件已打包为 <专辑名>-宣传物料.zip |

---

## 输出文件契约

严格遵循 `FILE_CONTRACTS.md` 中 Phase 6 契约。

---

## 最终交付物

| 文件/目录 | 内容 |
|-----------|------|
| `docs/album-overview.md` | 专辑统筹文档（完整） |
| `docs/promotional-materials.md` | 宣传文档 |
| `docs/artist-story-*.md` | 艺人说文案（4 文件） |
| `docs/cover-concept.md` | 封面概念 |
| `generate/cn_320k/` | 中文最终音频（N 首） |
| `generate/en_320k/` | 英文最终音频（N 首） |
| `*.zip` | 宣传物料压缩包 |
