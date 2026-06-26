# Auto Model Router

> 智能模型路由：根據工作類型自動選擇最適合的模型

## 功能

- ✅ 自動識別8大工作範疇
- ✅ 智能分配模型（用家只需提供1-N個模型）
- ✅ 突發任務自動分派子Agent
- ✅ 支援國際/國內模型套餐
- ✅ 未知任務/模型自動Fallabck

## 安裝

```bash
npx clawhub install auto-model-router
```

## 首次配置

```bash
/model-router setup
```

系統會引導你：
1. 選擇套餐（Plan A 國際 / Plan B 國內）
2. 輸入你現有的模型
3. 系統自動分配到8個範疇

## 快速開始

### 示例：用家只有3個模型

```
/model-router setup
> 選擇套餐：Plan A
> 輸入模型：Claude Opus, GPT-4.5, GPT-4o

系統自動分配：
高邏輯推理 → Claude Opus
代碼生成 → GPT-4.5
創意寫作 → GPT-4o
資訊閱讀 → Claude Opus (擴展)
...
```

## 工作範疇

| # | 範疇 | 描述 |
|---|------|------|
| 1 | 高邏輯推理 | 分析、策劃、策略、評估 |
| 2 | 代碼生成 | 編程、debug、重構 |
| 3 | 創意寫作 | 故事、文案、劇本 |
| 4 | 資訊閱讀 | 總結、翻譯、問答 |
| 5 | 簡單重複 | 格式化、批量、轉換 |
| 6 | 圖片理解 | 截圖分析、OCR |
| 7 | 圖片生成 | 海報、設計、插畫 |
| 8 | 影片/音頻 | 剪輯、字幕 |

## 命令

| 命令 | 描述 |
|------|------|
| `/model-router setup` | 配置嚮導 |
| `/model-router plan A` | 切換到套餐A |
| `/model-router plan B` | 切換到套餐B |
| `/model-router list` | 查看當前配置 |
| `/model-router reset` | 重置配置 |

## 文件結構

```
auto-model-router/
├── SKILL.md              # 主要規格文檔
├── README.md             # 本文件
├── config/
│   ├── default.json     # 預設配置
│   ├── plan-a.json      # 國際模型套餐
│   └── plan-b.json      # 國內模型套餐
└── task-rules.json       # 分類規則
```

## License

MIT
