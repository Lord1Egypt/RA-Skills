# Phase 6 — Promotional Writer Skill

> 制作宣传文档，从模板填充专辑信息，生成多渠道宣传物料。

---

## 触发

phase6-album-overview-updater 完成后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 1 | `docs/album-overview.md` | 专辑核心概念/叙事轴/曲目定位 |
| Phase 2 | `songs/T{N}-曲名.md` | 每首歌的封面高光文案、市场评估 |
| Phase 6 | `templates/promotional-materials.md` | 宣传文档模板 |

---

## 执行

### ⚠️ 修改范围
- **读取**：`docs/album-overview.md`、`songs/T{N}-曲名.md`、`templates/promotional-materials.md`
- **写入**：`docs/promotional-materials.md`
- **禁止**：修改模板文件或 `songs/`/`generate/` 中的任何文件

### 宣传文档结构

从模板 `templates/promotional-materials.md` 初始化，填充以下内容：

1. **一句话专辑概念**：从 Phase 1 核心传播概念提取
2. **专辑简介（~300 字）**：综合专辑概述 + 叙事轴 + 目标听众
3. **核心宣传语（3 条）**：从核心悖论/高光文案/传播概念衍生
4. **各曲高光文案**：从 `songs/T{N}-曲名.md` 提取「封面高光文案」区块
5. **Social Media 文案**：
   - 微博：140 字以内
   - 小红书：200-300 字 + 话题标签
   - 微信推文标题：× 3 个备选
6. **制作信息**：
   - AI 生成工具（MiniMax music-2.6）
   - 规模（N 首歌 × 2 语言 × 3 Prompt = X 首生成物）
   - 输出标准（320kbps/44.1kHz/-14 LUFS）
7. **潜在争议点与回应预案**：
   - AI 生成音乐的争议
   - 叙事策略：协作非替代

### 制作信息格式

```markdown
## 制作信息

- **音乐生成**：MiniMax music-2.6
- **生成规模**：N 首 × 2 语言 × 3 Prompt 版本 = X 首生成物，选定 2N 首
- **输出标准**：MP3 320kbps / 44.1kHz / -14 LUFS
- **叙事策略**：不隐藏 AI 生成事实，将其转化为专辑最诚实的隐喻
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 一句话概念明确 | ≤ 30 字符，可独立传播 |
| 2 | 专辑简介完整 | ~300 字，涵盖核心概念 + 叙事轴 + 目标听众 |
| 3 | 3 条宣传语差异化 | 分别从悖论/高光/传播角度切入 |
| 4 | 各曲高光文案齐全 | N 首歌，每首一句话 |
| 5 | Social Media 文案齐全 | 微博/小红书/微信推文标题 × 3 |
| 6 | 制作信息准确 | 工具/规模/标准数据正确 |
| 7 | 争议预案完整 | ≥ 1 个争议点 + 回应策略 |

全部 ✅ → 进入下一步（phase6-artist-story-writer）
