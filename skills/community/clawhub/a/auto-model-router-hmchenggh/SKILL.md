---
name: auto-model-router
description: Auto Model Router - Automatically select the best model based on task complexity for OpenClaw agents
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: []
      config: []
    homepage: https://github.com/HMCHENGGH/auto-model-router
---

# Auto Model Router Skill

> 智能模型路由：根據工作類型自動選擇最適合的模型

## 概述

Auto Model Router 係一個 OpenClaw Skill，自動根據用戶輸入的工作類型，選擇最適合的模型處理。

### 核心功能

- **任務分類引擎**：自動識別8大工作範疇
- **模型智能分配**：用戶只需提供1-N個模型，系統自動補全剩餘範疇
- **Multi-Agent 分派**：突發任務自動分派子 Agent 處理
- **雙套餐支援**：Plan A（國際模型）/ Plan B（國內模型）

---

## 八大工作範疇

| # | 範疇 | 輸入特徵 | 輸出特徵 | 關鍵詞 |
|---|------|----------|----------|--------|
| 1 | 高邏輯推理 | 分析需求、策略問題 | 計劃、報告、評估 | 分析、評估、比較、推理、策略、規劃 |
| 2 | 代碼生成 | 技術需求、功能描述 | 可執行代碼 | 函數、代碼、編程、debug、重構 |
| 3 | 創意寫作 | 創作需求 | 故事、文案、劇本 | 寫、創作、故事、編劇、文案 |
| 4 | 資訊閱讀 | 文檔、文章、連結 | 摘要、翻譯、問答 | 總結、摘要、翻譯、閱讀、解釋 |
| 5 | 簡單重複 | 格式化需求 | 轉換結果 | 格式化、批量、轉換、整理 |
| 6 | 圖片理解 | 圖片 + 文字 | 圖片分析 | 截圖、圖片、分析、識別、OCR |
| 7 | 圖片生成 | 文字描述 | 圖片 | 生成圖片、海報、設計 |
| 8 | 影片/音頻 | 影片/音頻 + 文字 | 分析或生成 | 影片、音頻、剪輯、字幕 |

---

## 模型套餐

### Plan A：國際模型

| # | 範疇 | 模型 A | 模型 B |
|---|------|--------|--------|
| 1 | 高邏輯推理 | Claude Opus 4 | DeepSeek R1 |
| 2 | 代碼生成 | GPT-4.5 | Claude Sonnet 4 |
| 3 | 創意寫作 | GPT-4o | MiniMax 2.7 |
| 4 | 資訊閱讀 | Claude Haiku | Gemini Flash |
| 5 | 簡單重複 | Gemini Flash-Lite | GPT-4o-mini |
| 6 | 圖片理解 | Claude Sonnet 4 | Gemini 2.0 |
| 7 | 圖片生成 | DALL-E 3 | Stable Diffusion |
| 8 | 影片/音頻 | GPT-4o | Gemini 2.0 |

### Plan B：國內模型

| # | 範疇 | 模型 A | 模型 B |
|---|------|--------|--------|
| 1 | 高邏輯推理 | DeepSeek R1 | GLM-5 |
| 2 | 代碼生成 | GLM-5 | Kimi K2 |
| 3 | 創意寫作 | MiniMax M2.5 | 文心一言 5.0 |
| 4 | 資訊閱讀 | MiniMax-01 | GLM-4-Long |
| 5 | 簡單重複 | GLM-4-Flash | DeepSeek V3 |
| 6 | 圖片理解 | MiniMax-VL-01 | GLM-4.6V |
| 7 | 圖片生成 | 騰訊混元-Image | 豆包Seed |
| 8 | 影片/音頻 | Vidu Q3 | 可靈 2.6 |

---

## 配置流程

### 首次使用

```
用戶輸入：「/model-router setup」
系統自動引導：
  1. 選擇套餐 [Plan A / Plan B / 自定義]
  2. 輸入可用模型
  3. 系統智能分配
  4. 保存配置
  5. 自動重載 OpenClaw
```

### 智能分配邏輯

當用戶提供的模型少於8個時，系統自動：

1. **直接匹配**：最符合該範疇的模型
2. **系列擴展**：同系列模型跨範疇使用
3. **能力估算**：選擇最接近能力需求的模型

#### 示例：用戶提供5個模型

```
用戶輸入：Claude Opus, GPT-4.5, GPT-4o, Claude Haiku, Gemini Flash-Lite

系統自動分配：
  高邏輯推理 → Claude Opus ✅
  代碼生成 → GPT-4.5 ✅
  創意寫作 → GPT-4o ✅
  資訊閱讀 → Claude Haiku ✅
  簡單重複 → Gemini Flash-Lite ✅
  圖片理解 → Claude Opus (擴展)
  圖片生成 → GPT-4o (擴展)
  影片/音頻 → GPT-4o (擴展)
```

---

## 任務分類引擎

### 分類演算法

```
輸入：用戶工作描述
    ↓
┌─────────────────────────────────┐
│  第一層：意圖檢測               │
│  • 動詞分析                     │
│  • 名詞分析                     │
│  • 輸出期望                     │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  第二層：關鍵詞匹配             │
│  • 匹配8大範疇關鍵詞           │
│  • 計算相似度                   │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  第三層：分類結果               │
│  • 主分類                       │
│  • 次分類（混合任務）          │
│  • 置信度                       │
└─────────────────────────────────┘
```

### 混合任務處理

當工作涉及多個範疇時：

```
任務：「分析數據後寫報告」
    ↓
主分類：高邏輯推理（分析）
次分類：創意寫作（報告）
    ↓
執行：高邏輯模型 → 創意寫作模型
```

---

## 突發任務處理

### 機制：Sub-Agent 分派

```
主任務執行中（高邏輯推理）
    ↓
突發任務：「幫我翻譯這份文件」
    ↓
系統自動：
  1. 保存主任務狀態
  2. 生成翻譯子 Agent
  3. 使用資訊閱讀模型翻譯
  4. 完成後返回結果
  5. 恢復主任務
```

### 配置

```json
{
  "subagents": {
    "translator": {
      "model": "minimax-01",
      "task_type": "info_reading"
    },
    "image_generator": {
      "model": "hunyuan-image",
      "task_type": "image_generation"
    },
    "video_agent": {
      "model": "vidu-q3",
      "task_type": "video_audio"
    }
  }
}
```

---

## 未知範疇 Fallback

### 當遇到未定義的工作類型時

```
未知工作：「語音識別」
    ↓
┌─────────────────────────────────┐
│  能力評估                       │
│  語音 → 文字 → 處理           │
│  最接近：資訊閱讀              │
└─────────────────────────────────┘
    ↓
映射到：資訊閱讀範疇
    ↓
使用該範疇配置的模型
```

### 預設映射表

| 未知範疇 | 映射到 | 理由 |
|----------|--------|------|
| 語音識別 | 資訊閱讀 | 音頻→文字→處理 |
| 語音合成 | 創意寫作 | 文字→語音創作 |
| 3D建模 | 圖片生成 | 空間理解類似 |
| 數據分析 | 高邏輯推理 | 需要分析推理 |
| 搜索研究 | 資訊閱讀 | 信息檢索整理 |

### 完全無法識別時

```
使用：高邏輯推理模型（預設fallback）
提示：「已為此任務分配高邏輯推理模型」
可選：用戶確認或修改
```

---

## 未知模型處理

### 當用戶輸入不在預設列表的模型

```
用戶輸入：「我用 XYZ 模型」
    ↓
┌─────────────────────────────────┐
│  查詢模型能力                   │
│  • 本地數據庫                   │
│  • API 識別                     │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Fallback 規則                   │
│  • 通用/無描述 → 高邏輯推理    │
│  • 強調創意 → 創意寫作          │
│  • 強調速度/平 → 簡單重複       │
│  • 強調翻譯/長文本 → 資訊閱讀 │
│  • 強調編程 → 代碼生成          │
└─────────────────────────────────┘
```

---

## 配置檔案

### 位置

```
~/.openclaw/skills/auto-model-router/
├── SKILL.md              # 本文件
├── config/
│   ├── default.json      # 預設配置
│   ├── plan-a.json       # Plan A 配置
│   ├── plan-b.json       # Plan B 配置
│   └── user.json         # 用戶自定義
└── task-rules.json       # 分類規則
```

### 配置格式

```json
{
  "version": "1.0",
  "plan": "A",
  "task_models": {
    "high_logic": "anthropic/claude-opus-4",
    "code_generation": "openai/gpt-4.5",
    "creative_writing": "openai/gpt-4o",
    "info_reading": "anthropic/claude-haiku",
    "simple_repeat": "google/gemini-flash-lite",
    "image_understanding": "anthropic/claude-sonnet-4",
    "image_generation": "stability/stable-diffusion",
    "video_audio": "openai/gpt-4o"
  },
  "subagents": {
    "enabled": true,
    "pool": ["translator", "image_generator", "video_agent"]
  },
  "fallback": {
    "unknown_task": "high_logic",
    "unknown_model": "high_logic"
  }
}
```

---

## 命令

| 命令 | 描述 |
|------|------|
| `/model-router setup` | 開始配置嚮導 |
| `/model-router plan [A/B/custom]` | 選擇套餐 |
| `/model-router list` | 列出當前配置 |
| `/model-router update <範疇> <模型>` | 更新特定範疇 |
| `/model-router reset` | 重置為預設 |

---

## 使用範例

### 示例 1：完整配置

```
用戶：/model-router setup
系統：選擇套餐 [1] Plan A (國際) [2] Plan B (國內) [3] 自定義
用戶：1
系統：請輸入你可用的模型（用逗號分隔）
用戶：Claude Opus, GPT-4.5, GPT-4o
系統：智能分配完成：
  高邏輯推理 → Claude Opus
  代碼生成 → GPT-4.5
  創意寫作 → GPT-4o
  資訊閱讀 → Claude Opus (擴展)
  簡單重複 → GPT-4.5 (擴展)
  圖片理解 → Claude Opus (擴展)
  圖片生成 → GPT-4o (擴展)
  影片/音頻 → GPT-4o (擴展)
系統：配置已保存。是否重載 OpenClaw？[Y/N]
```

### 示例 2：突發任務

```
主任務：策劃年度報告
使用的模型：DeepSeek R1（高邏輯）

突發：翻譯英文文件
系統：自動切換到 MiniMax-01（資訊閱讀）
翻譯完成，自動切換回 DeepSeek R1
繼續策劃報告
```

---

## 常見問題

### Q1：轉模型時需要問用戶嗎？
**不需要**。系統自動切換，通過 OpenClaw per-job model override 實現。

### Q2：如果提供的模型數量為0？
**使用預設套餐**：直接套用 Plan A 或 Plan B。

### Q3：如何處理完全未知的任務？
**使用高邏輯推理模型作為 fallback**，並提示用戶確認。

### Q4：支援多少個模型？
**理論上無限**。系統自動根據能力分配到8個範疇。

---

## 更新日誌

| 版本 | 日期 | 更新內容 |
|------|------|----------|
| 1.0 | 2026-04-05 | 初始版本 |

---

## 貢獻

歡迎提交 Issue 和 Pull Request！
