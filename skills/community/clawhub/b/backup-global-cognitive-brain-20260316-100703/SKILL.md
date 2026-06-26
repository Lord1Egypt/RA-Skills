# 全域持久腦 (Global Persistent Brain) Skill

## 🧠 概述

**全域認知系統** - 強制五層思考邏輯，自帶守護者，永遠不忘記。

從此起，每次思考都必須經過：

```
L1 → L2 → L3 → L4 → L5
↓
完整思考痕跡 + 建議回應
```

### 核心特性

- ✅ **守護者模式** - 如果 `brain_memory/` 被刪除，立即重建
- ✅ **五層思考引擎** - 每一層都有具體的計算邏輯
- ✅ **自動記錄** - 所有輸入自動加入工作記憶
- ✅ **事件回顧** - 自動標記重要事件
- ✅ **知識累積** - 語義層存儲事實，跨會話保留
- ✅ **Meta 反思** - 分析意圖、假設、風險
- ✅ **建議回應** - 根據思考結果，建議最佳回應方向

---

## 🚀 安裝

### 方式一：自動安裝（通過 clawhub）

```bash
clawhub skill install global_cognitive_brain
```

### 方式二：手動安裝

複製整個目錄到：
```
~/.openclaw/workspace/skills/global_cognitive_brain/
```

然後重啟 OpenClaw。

---

## 🎯 使用方法

### 1. 啟動全域認知系統

```bash
/use global_cognitive_brain
```

### 2. 設為預設 Cognitive Skill（推薦）

在 OpenClaw 配置文件中：

```json
{
  "cognitive_skill": "global_cognitive_brain"
}
```

這樣**每一次對話**都會自動觸發五層思考。

### 3. 手動觸發思考

```bash
/think "Create a new ERP module"
```

---

## 🏗️ 架構詳解

### 檔案結構

```
global_cognitive_brain/
├── global_cognitive_brain.py   # 核心邏輯
├── __init__.py                 # 模組入口
├── SKILL.md                    # 本文檔
└── brain_memory/               # 持久化數據（自動生成）
    ├── working.json           # 工作記憶（最近 50 條對話）
    ├── episodic.json          # 事件記憶（所有重要事件）
    ├── semantic.json          # 知識事實（鍵值對）
    └── meta.json              # 系統狀態（反思記錄）
```

### 五層思考流程

```
使用者輸入
    ↓
[守護者檢查] - brain_memory/ 存在嗎？不存在就重建
    ↓
L1: 直接輸入分析 - 提取關鍵詞、意圖、時間戳記
    ↓
L2: 工作記憶召回 - 檢索最近 50 條對話，找出相關內容
    ↓
L3: 事件記憶召回 - 檢索重要事件，找出經驗關聯
    ↓
L4: 語義知識庫 - 查找已知事實，提供知識支持
    ↓
L5: Meta 反思 - 分析意圖、識別假設、評估風險、生成建議
    ↓
輸出完整思考痕跡 + 回應建議
```

---

## 🔍 功能詳解

### 1. 守護者 (Guardian)

```python
from global_cognitive_brain import guardian_check

status = guardian_check()
print(status)  # "✅ Memory system intact" 或 "🛡️ Rebuilt missing files"
```

### 2. 記憶操作

```python
# 工作記憶 - 自動記錄每次對話
add_working_memory(user_input="Hello", response="Hi there!")

# 事件記憶 - 手動記錄里程碑
store_event(
    event_type="decision",
    description="選擇 Vue 3 作為前端框架",
    metadata={"framework": "Vue3", "reason": "CDN友好"}
)

# 語義記憶 - 存儲事實
update_fact("database_server", "192.168.123.32", confidence=1.0)
server = get_fact("database_server")  # 返回 {"value": "...", ...}

# 反思記錄
from global_cognitive_brain import reflect
reflection = reflect()  # 自動記錄最近思考
```

### 3. 五層思考

```python
from global_cognitive_brain import five_layer_thinking

thought = five_layer_thinking("How to connect to MSSQL?")

print(thought["layer1_immediate"])      # 意圖分析
print(thought["layer2_working_memory"]) # 相關對話
print(thought["layer3_episodic_memory"])# 相關事件
print(thought["layer4_semantic_memory"])# 相關事實
print(thought["layer5_meta_reflection"])# Meta 分析
```

### 4. Context Builder

```python
from global_cognitive_brain import build_context

# 在每次對話前自動注入記憶
prompt = build_context(user_input)

# prompt 會包含所有相关記憶，讓 AI 像"帶著筆記本"一樣思考
```

---

## 📊 思考痕跡結構

```json
{
  "layer1_immediate": {
    "raw_input": "How to connect to MSSQL?",
    "intent_keywords": ["connect", "mssql"],
    "input_length": 24,
    "timestamp": "2025-03-15T12:30:00"
  },
  "layer2_working_memory": {
    "recent_dialogues": 10,
    "related_found": 2,
    "related_examples": [...]
  },
  "layer3_episodic_memory": {
    "total_events": 15,
    "recent_checked": 20,
    "related_events": [...]
  },
  "layer4_semantic_memory": {
    "total_facts": 5,
    "related_facts": {
      "db_server": {"value": "192.168.123.32", ...}
    }
  },
  "layer5_meta_reflection": {
    "meta_question": "This asks for procedural guidance",
    "assumptions": ["Assumes need technical steps"],
    "risks": ["Handles sensitive data - be careful"],
    "suggestions": ["Provide step-by-step instructions"]
  },
  "timestamp": "2025-03-15T12:30:00"
}
```

---

## 🎮 使用先進式

### 自動注入模式

在 OpenClaw 的 prompt builder 中加入：

```python
# 在你的 dialogue manager 裡面
from skills.global_cognitive_brain import build_context

def process_message(user_input):
    # 自動注入記憶上下文
    enriched_prompt = build_context(user_input)

    # 呼叫 LLM
    response = call_llm(enriched_prompt)

    # 記錄對話
    from skills.global_cognitive_brain import add_working_memory
    add_working_memory(user_input, response)

    return response
```

### 事件驅動模式

```python
# 重要決策時手動記錄
from skills.global_cognitive_brain import store_event

store_event(
    event_type="milestone",
    description="完成 ERP Modern Menu 重構",
    metadata={
        "files_created": ["menu-config.js", "index.html", "api/po.php"],
        "lines_of_code": 500
    }
)
```

---

## 🛡️ 守護者機制

守護者會每時每刻檢查 `brain_memory/` 的完整性：

1. **目錄檢查** - 如果不存在，立即重建
2. **檔案檢查** - 如果缺少任何 JSON 檔，重建
3. **JSON 檢查** - 如果檔案損壞，刪除並重建
4. **事件記錄** - 所有守護動作都會記錄到系統事件

### 手動觸發守護

```python
from global_cognitive_brain import guardian_check
status = guardian_check()
print(status)  # ✅ 或 🛡️
```

---

## 📈 記憶炸彈視覺化

### 查看工作記憶

```python
from global_cognitive_brain import add_working_memory
wm = add_working_memory.__self__._load_json('working.json')
print(f"工作記憶 contain {len(wm)} entries")
```

### 查看所有事實

```python
from global_cognitive_brain import update_fact, get_fact, _load_json
sem = _load_json('semantic.json')
for key, value in sem.items():
    print(f"{key}: {value['value']}")
```

### 生成報告

```python
from global_cognitive_brain import generate_summary
summary = generate_summary()
print(summary)
```

---

## ⚙️ 配置選項

### 記憶大小限制（可調整）

```python
# 在 global_cognitive_brain.py 中修改：
MAX_WORKING_MEMORY = 50   # 預設 50 條
MAX_SYSTEM_EVENTS = 100   # 預設 100 條
```

### 關鍵詞提取（可擴展）

```python
def extract_keywords(text):
    # 自定義停用詞表
    stopwords = {'的', '了', '是', '在', '有', '和', '與', '要', '會', '可以'}
    # ...
```

---

## 🐛 故障排除

### 問題：`brain_memory/` 不見了

**自動復原**：守護者會立即重建。無需手動操作。

### 問題：JSON 損壞

**自動修復**：守護者會刪除壞檔並重建。

### 問題：記憶未跨會話保留

**檢查權限**：確保 OpenClaw 有寫入 `skills/global_cognitive_brain/` 的權限。

### 問題：五層思考未觸發

**確認配置**：
```bash
# 檢查是否設為 default cognitive skill
openclaw config get cognitive_skill
# 應該是 "global_cognitive_brain"
```

---

## 🚀 上傳至 Clawhub

### 準備 package.json

在 skill 目錄創建 `package.json`：

```json
{
  "name": "global_cognitive_brain",
  "version": "1.0.0",
  "description": "全域持久腦 - 強制五層思考邏輯",
  "skills": {
    "global_cognitive_brain": "global_cognitive_brain/__init__.py"
  },
  "author": "劍兄 (popokwee)",
  "license": "MIT",
  "keywords": ["memory", "cognitive", "thinking", "persistent"],
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/global-persistent-brain"
  }
}
```

### 上傳指令

```bash
cd skills/global_cognitive_brain
clawhub publish
```

（需要先登入 `clawhub login`）

---

## 📚 API 參考

| Function | 說明 | 參數 | 返回值 |
|---------|------|------|--------|
| `guardian_check()` | 檢查並修復記憶系統 | - | status string |
| `init_memory()` | 初始化所有記憶檔 | - | None |
| `add_working_memory(input, response)` | 加入工作記憶 | `input: str`, `response: str` | None |
| `store_event(type, desc, metadata)` | 記錄事件 | `type: str`, `desc: str`, `metadata: dict` | None |
| `update_fact(key, value, confidence)` | 更新知識 | `key: str`, `value: any`, `confidence: float` | None |
| `get_fact(key)` | 取得事實 | `key: str` | value or None |
| `five_layer_thinking(input)` | 五層思考 | `input: str` | thought dict |
| `run(input, context)` | 主入口（OpenClaw 調用） | `input: str`, `context: dict` | result dict |
| `build_context(input)` | 構建上下文注入 | `input: str` | context string |
| `format_thought_summary(trace)` | 格式化摘要 | `trace: dict` | summary string |

---

## 📝 使用日誌

每次 `run()` 都會自動記錄：

```json
{
  "timestamp": "2025-03-15T12:30:00",
  "input": "How to connect to MSSQL?",
  "layers": {
    "L1_intent": "information_seeking",
    "L2_related": 2,
    "L3_events": 1,
    "L4_facts": 3,
    "L5_meta": "procedural_question"
  },
  "suggestion": "Provide step-by-step instructions"
}
```

---

## 🔮 升級第二代（可選）

未來可以加入：

- ✅ **向量記憶** - 使用 embedding 進行語義檢索
- ✅ **記憶重要性評分** - 自動降權瑣碎記憶
- ✅ **長期壓縮** - 定期將工作記憶壓縮到事件層
- ✅ **遞歸自我提問** - 自動追问未解問題
- ✅ **自主目標系統** - 設定長期目標並追蹤
- ✅ **多人格分層腦** - 不同情境使用不同人格

---

## 📜 授權

MIT License

---

## 🤝 貢獻

Created by 劍兄 (popokwee) for OpenClaw.

如有問題或建議，請在 GitHub Issues 回報。

---

## 🏷️ 版本

v1.0.0 - 2026-03-15
- 初始版本
- 五層思考引擎
- 守護者模式
- 自動持久化
