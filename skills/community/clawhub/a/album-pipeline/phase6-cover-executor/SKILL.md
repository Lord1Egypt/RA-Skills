# Phase 6.4.6 — Cover Executor Skill

> 使用 MiniMax CLI `mmx image generate` 批量生成专辑封面图和单曲封面图。

---

## 触发

phase6-cover-prompt-generator 完成后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6.4.5 | `generate/covers/prompts/album-cover-prompt{1,2,3}.txt` | 专辑封面 3 个 Prompt 版本 |
| Phase 6.4.5 | `generate/covers/prompts/T{N}-曲名-cover-prompt{1,2,3}.txt` | 单曲封面 Prompt（每首歌 3 个版本） |
| Phase 6.4.5 | `generate/covers/prompts/index.json` | Prompt 索引 |

---

## 执行

### ⚠️ 修改范围
- **读取**：`generate/covers/prompts/*.txt`、`generate/covers/prompts/index.json`
- **写入**：`generate/covers/album-cover-p{1,2,3}.png`、`generate/covers/tracks/T{N}-曲名-p{1,2,3}.png`
- **禁止**：修改 Prompt 源文件

### 并行策略

**专辑封面 + N 首单曲封面 = 1 + N×3 个并行生成任务**。

- 专辑封面 3 个版本可并行发起
- 每首歌的单曲封面 3 个版本可并行发起
- 不同歌曲之间可并行发起

⚠️ **限流处理**：MiniMax image-01 有 API rate limit。如遇 429 响应，降级为串行生成，每张完成后间隔 3-5 秒再发起下一张。

### CLI 命令模板

**专辑封面：**

```bash
# 版本 1 — 概念忠实型
mmx image generate \
  --prompt "$(cat generate/covers/prompts/album-cover-prompt1.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers \
  --out-prefix album-cover-p1

# 版本 2 — 情绪氛围型
mmx image generate \
  --prompt "$(cat generate/covers/prompts/album-cover-prompt2.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers \
  --out-prefix album-cover-p2

# 版本 3 — 极简符号型
mmx image generate \
  --prompt "$(cat generate/covers/prompts/album-cover-prompt3.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers \
  --out-prefix album-cover-p3
```

**单曲封面（以 T1-出发 为例）：**

```bash
mmx image generate \
  --prompt "$(cat generate/covers/prompts/T1-出发-cover-prompt1.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers/tracks \
  --out-prefix T1-出发-p1

mmx image generate \
  --prompt "$(cat generate/covers/prompts/T1-出发-cover-prompt2.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers/tracks \
  --out-prefix T1-出发-p2

mmx image generate \
  --prompt "$(cat generate/covers/prompts/T1-出发-cover-prompt3.txt)" \
  --width 2048 --height 2048 \
  --out-dir generate/covers/tracks \
  --out-prefix T1-出发-p3
```

### CLI 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--prompt` | 从对应 promptN.txt 读取 | 主描述 |
| `--width` | 2048 | 最大分辨率（image-01 支持上限） |
| `--height` | 2048 | 正方形封面 |
| `--out-dir` | `generate/covers` 或 `generate/covers/tracks` | 输出目录 |
| `--out-prefix` | `album-cover-pN` 或 `T{N}-曲名-pN` | 输出文件名前缀 |

### 产物管理

```
generate/covers/
├── album-cover-p1.png              ← 版本 1：概念忠实型
├── album-cover-p2.png              ← 版本 2：情绪氛围型
├── album-cover-p3.png              ← 版本 3：极简符号型
├── prompts/                        ← Prompt 源文件
│   ├── album-cover-prompt{1,2,3}.txt
│   ├── T{N}-曲名-cover-prompt{1,2,3}.txt
│   └── index.json
└── tracks/
    ├── T1-曲名-p1.png              ← T1 版本 1
    ├── T1-曲名-p2.png              ← T1 版本 2
    ├── T1-曲名-p3.png              ← T1 版本 3
    ├── T2-曲名-p1.png
    ├── ...
    └── TN-曲名-p3.png              ← TN 版本 3
```

### 质量检查

生成完成后对每张封面图做基本检查：
1. 文件存在且非空（≥ 50KB）
2. 图片为正方形（2048×2048 或接近比例）
3. 格式为 PNG

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | 专辑封面 3 张已生成 | album-cover-p1/p2/p3.png 存在 |
| 2 | 单曲封面全部已生成 | N 首歌 × 3 张 = 全部产物文件存在 |
| 3 | 文件可正常打开 | 非损坏图片，文件大小 ≥ 50KB |
| 4 | 产物目录结构正确 | covers/ + covers/tracks/ 按约定命名 |
| 5 | 原始 Prompt 未污染 | 未修改 `generate/covers/prompts/` 中的文件 |
| 6 | 生成日志已保存 | 记录每张生成耗时/模型版本/Prompt 来源 |

全部 ✅ → 返回 Phase 6 主流程，进入 phase6-promo-video-executor
