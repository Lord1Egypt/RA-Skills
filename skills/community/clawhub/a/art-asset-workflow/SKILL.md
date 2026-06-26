---
name: art-asset-workflow
version: 1.0.0
description: "美术素材生成完整工作流指引。生成游戏 UI 图标、角色概念图、运营海报等素材时使用。包含工具链说明、尺寸选择、提示词规范、工作流步骤。细节工具用法见对应子技能：codex-imggen（生图）、sprite-tools（切图/抠图）。"
metadata: {"openclaw":{"emoji":"🎮","requires":{"anyBins":["codex"]}}}
---

# 美术素材生成工作流

## 工具链

```
生图（AI）→ 拆图 → 抠图 → 独立素材 → Unity/美术流程
   ↓           ↓         ↓
codex-imggen  sprite-tools  sprite-tools
```

> ⏱️ **注意**：Codex CLI 生图约需 30~90 秒，调用时 exec timeout 应设不低于 **180 秒**，避免 agent 误判失败。

## 尺寸选择

| 需求 | 推荐工具 | 推荐尺寸 |
|------|---------|---------|
| **游戏 UI 图标**（批量） | Codex CLI | `1K` 方图 或 `1536x1024` 横版，**白色背景**，3x2 布局 |
| **单张素材**（角色/概念） | Codex CLI | `1K` / `1536x1024` / `9:16`，**白色背景** |
| **单张素材**（角色/概念） | Codex CLI | `1K` / `1536x1024` / `9:16` |
| **运营海报/带文字** | 官方 API（gpt-image-2）| `1024x1536` / `1024x1024` |
| **高精度素材** | 官方 API | `2048x2048` / `3840x2160` |
| **抠图后处理** | PIL/numpy | 保持原尺寸 |

⚠️ **Codex CLI 尺寸限制**：最大输出 ~1.57MP（1254×1254 级别），4K/FHD/720p 都会降级，不要用这些标识。

✅ **安全尺寸**：`1K` → 1254×1254，`1536x1024` → 精确 1536×1024，`9:16` → 941×1672

✅ **官方 API gpt-image-2** 支持精确 2048×2048、3840×2160、2160×3840（需要用户自建 API Key）

## 提示词规范

### 批量游戏 UI 图标（白色背景）
```bash
bash ~/.openclaw/skills/codex-imggen/scripts/batch_generate.sh \
  "flat vector art style, white background (#ffffff), each icon approximately 256x256 pixels, consistent 2px gold (#d4af37) border, same lighting angle, centered subjects" \
  6 \
  /tmp/icons/
```
> 布局：1024×1536 输出 → 3x2（2列3行），每格 512×512

### 单张素材
```bash
bash ~/.openclaw/skills/codex-imggen/scripts/generate.sh \
  "A medieval sword with golden blade on white background (#ffffff), flat vector art style" \
  /tmp/art/
```

### 带尺寸控制的单张（1K 方图）
```bash
bash ~/.openclaw/skills/codex-imggen/scripts/gen_size.sh \
  "1K" \
  "A ruby gem on white background, flat vector art style" \
  /tmp/art/
```

### 官方 API（需要用户自建 API Key）
```python
from openai import OpenAI
client = OpenAI()

result = client.images.generate(
    model="gpt-image-2",
    prompt="游戏角色概念图：手持法杖的法师，深色披风，魔法光效，Unity 风格",
    size="1024x1536",
    quality="high"
)
```

## 工作流步骤

### Step 1：生成
根据需求选择：
- **批量图标** → Codex `batch_generate.sh`（一次出 6 个风格一致的元素）
- **单张素材** → Codex `generate.sh` 或 `gen_size.sh`
- **高精度/带文字/运营图** → 官方 gpt-image-2 API

### Step 2：拆分 + 抠图（一键完成）
推荐用 `batch_split.sh`，自动完成：背景透明化 → 网格拆分 → alpha 抠图
```bash
# 1024x1536 输出 → 3x2 layout（2列3行）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/batch.png 3x2 /tmp/icons/

# 1536x1024 输出 → 2x3 layout（3列2行）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/batch.png 2x3 /tmp/icons/
```

### Step 3：验证图片
**生成后必须验证**，用图像理解工具检查是否有明显问题：
- 元素完整性（没有缺失或被截断）
- 风格一致性（背景色、边框、光影是否统一）
- 内容正确性（图标/道具与预期是否匹配）

```bash
# 批量生成后验证整张
mmx vision describe /tmp/batch.png "检查这张游戏UI素材图：元素是否完整、风格是否一致、背景是否为白色、有无明显错误"

# 单张素材验证
mmx vision describe /tmp/art/output.png "这是一张游戏素材，描述画面内容并指出是否有明显问题"
```

如发现问题，记录问题类型并决定是否重新生成或调整提示词。

## 提示词技巧

### 应该写什么
- 明确风格描述（flat vector / pixel art / realistic）
- 指定配色（#hex 色值比文字描述更准）
- 统一光影角度、边框厚度、内边距
- 说明背景要求（**white background #ffffff** 而非 transparent / dark）
- 列出具体元素清单

### 避免什么
- 不要用 "high quality"、"4K"、"professional"（模型无法执行这些元指令）
- 不要同时指定多个冲突风格
- 不要让模型自己决定布局（明确说 "in a grid" 或 "single image"）

### 批量风格固定技巧
在 `batch_generate.sh` 的风格提示词里写通用的共享特征（背景色、边框、金色），在元素列表里写每个图标的具体内容。

## 质量档位选择

| 档位 | 用途 | 时延 |
|------|------|------|
| low | 快速预览 | 低 |
| medium | 预览确认 | 中 |
| high | 最终交付 | 高 |

先用低档预览，确认后再高档输出（官方 API）。

## 官方 API vs Codex CLI

| | Codex CLI | 官方 API |
|--|----------|---------|
| 尺寸 | ~1.57MP 封顶 | 最高 3840×2160 |
| 成本 | Plus 订阅 | 按次付费 |
| 文本渲染 | 一般 | 强（支持中文） |
| 批次生成 | 支持（batch 模式） | 单张为主 |
| 背景透明 | 需后处理 | gpt-image-1.5 支持 |
| 适用场景 | 游戏 UI 批量素材 | 高精度/运营图/编辑 |

## 子技能索引

| 技能 | 用途 |
|------|------|
| `codex-imggen` | Codex CLI 生图（尺寸控制、batch 模式） |
| `sprite-tools` | 切图+抠图（**batch_split** 一键完成，或 grid_splitter + alpha_trim 分步） |