# Agent Fact Check Verify

**語言切換 / Language Switcher**：
**中文（目前）** | [English](docs/README.en.md) | [Español](docs/README.es.md) | [العربية](docs/README.ar.md)

版本：**1.0.5**  
作者：**Allen Niu**  
授權：**MIT**

`agent-fact-check-verify` 是面向 AI Agent 的嚴謹資訊查核技能。它的核心是「可重現的規則化判定流程」：先把輸入拆成可驗證 claim，再做多來源交叉查證（官方、主流媒體、事實查核站、社群訊號），最後用內部固定規則完成判定；對外只輸出中立、整合式結論，不暴露內部評分細節。

---

## 1. 設計目標與專業原則

本技能要解決的不是「寫一段看起來像查核的文字」，而是建立可審計、可追溯、可重跑的查核流程。

- **可重現**：相同 evidence 輸入，判定結果一致。
- **可追溯**：每個結論可以回到對應來源連結。
- **可審計**：內部規則固定，不允許任意自由心證打分。
- **中立表達**：對使用者輸出不帶立場、不做情緒化語言。
- **成本受控**：每個 claim 設定搜索預算與停止條件，避免無限擴搜。

---

## 2. 功能範圍（做什麼 / 不做什麼）

### 觸發詞（建議）

使用者輸入包含「查證」「核實」「核實這個」「是真的嗎」「是否正確」時，應優先啟用本 skill。

### 2.1 會做的

1. 從長文本拆出多個可驗證 claim。
2. 將 claim 分類為 statistical / causal / attribution / event / prediction / opinion / satire。
3. 按固定三輪策略查證：官方與一手 → 主流交叉 → 反證與闢謠。
4. 內部使用規則化判定（0–100）做 `true/uncertain/false` 帶狀決策。
5. 對使用者輸出整合式回覆（不顯示分數與機制）。

### 2.2 不會做的

1. 不把主觀價值判斷（純 opinion）硬判真偽。
2. 不把社群聲量當主證據。
3. 不輸出政治立場或說服性語言。
4. 不保證覆蓋付費牆、私有資料、封閉社群訊息。

---

## 3. 專案結構

```text
agent-fact-check-verify/
├── SKILL.md
├── LICENSE
├── README.md                    # 中文預設
├── scripts/
│   └── factcheck_engine.py      # extract / score / compose
├── references/
│   ├── scoring-rubric.md        # 內部規則摘要
│   └── source-policy.md         # 來源政策與優先級
└── docs/
    ├── README.en.md
    ├── README.es.md
    └── README.ar.md
```

---

## 4. 安裝與環境要求

### 4.1 基本需求

- Python 3.10+
- 可用搜尋能力（由 Agent 工具提供）
- 能讀寫工作目錄

### 4.2 快速檢查

```bash
python3 scripts/factcheck_engine.py --help
```

若顯示 `extract|score|compose` 三個子命令，即可使用。

---

## 5. 可選 CLI 與 Cookie 類別（重點）

以下 CLI 為**可選**，未安裝不影響主流程；若有安裝，X/Reddit 查核精度與速度通常更好。

- X CLI：<https://github.com/jackwener/twitter-cli>
- Reddit CLI：<https://github.com/jackwener/rdt-cli>

### 5.1 twitter-cli（Cookie 方式）

常見 cookie 類別：

- **必要登入類**：`auth_token`, `ct0`
- **會話/客戶端輔助**：`guest_id`, `kdt`
- **其他常見欄位**：`twid`, `lang`

實務建議：

- cookie 檔放在本機受限權限位置（例如 600）。
- 嚴禁提交到 Git。
- 定期輪替 cookie，失效即更新。

### 5.2 rdt-cli（Cookie 方式）

常見 cookie/會話類別：

- **會話主鍵**：`reddit_session`
- **裝置/追蹤**：`loid`, `session_tracker`
- **其他可能授權欄位**：`token_v2`（依工具版本可能不同）

實務建議：

- 使用低權限帳號做查核用途。
- cookie 失效時更新，不要在共享環境明文存放。

---

## 6. 執行流程（建議標準作業）

### Step A：抽取 claim

```bash
python3 scripts/factcheck_engine.py extract \
  --text "輸入待查文字" \
  --output claims.json
```

輸出每個 claim 的 `id / type / query`，供後續查證。

### Step B：三輪查證（由 Agent 執行）

1. **官方一手**：先找政府、官方公告、原始文件。
2. **主流交叉**：至少兩個獨立主流來源互證。
3. **反證搜尋**：主動搜索 debunk / false / misleading。

建議每 claim 搜索上限 6 次（每輪 2 次），避免失控。另可額外做 X(Twitter) 多次查核（建議 3 次），僅作社群佐證，且不改動官方/主流/反證三輪的既有次數。

### Step C：內部判定

```bash
python3 scripts/factcheck_engine.py score \
  --input evidence.json \
  --output scored.json
```

### Step D：輸出對使用者回覆

```bash
python3 scripts/factcheck_engine.py compose \
  --input scored.json \
  --output reply.txt
```

---

## 7. evidence.json 欄位規範（詳細）

每個 claim 建議包含：

- `claim`: 原始 claim 文本
- `type`: claim 類型
- `evidence.official_count`: 官方/一手來源數
- `evidence.mainstream_count`: 主流媒體來源數
- `evidence.independent_count`: 獨立來源數（去重後）
- `evidence.factcheck_true`: 是否有權威 fact-check 判真
- `evidence.factcheck_false`: 是否有權威 fact-check 判假
- `evidence.authority_rebuttal`: 是否被權威來源直接反駁
- `evidence.outdated_presented_current`: 過時資訊被當現況
- `evidence.source_chain_hops`: 來源轉述層級
- `evidence.core_contradiction`: 核心事實衝突
- `evidence.has_timestamp`: 是否有可驗證時間戳
- `evidence.strong_social_debunk`: 社群是否存在強反證
- `evidence.out_of_context`: 內容是否斷章取義
- `evidence.headline_mismatch`: 標題與正文是否不一致
- `evidence.missing_data_citation`: 是否缺少關鍵數據來源
- `evidence.fact_opinion_mixed`: 事實與觀點是否混寫

---

## 8. 對使用者輸出規範（硬性）

對外一律使用整合格式，**不得逐條顯示 claim**。固定輸出四段：

1. **是否正確（簡答）**：`正確 / 錯誤 / 部分正確 / 證據不足`（擇一）+ 一句簡答。  
2. **此事的真實情形**：整合後說明，不列 claim-by-claim。  
3. **結論**：給最終判斷與必要提醒。  
4. **相關連結（最多五個）**：最多 5 條，依優先級排序：官方/原始來源 > 高可信主流 > 補充佐證。  

另外：
- 不顯示內部分數。
- 不顯示評分機制。
- 永遠附上限制聲明：

`⚠️ 本查核基於公開可得資訊，無法涵蓋未公開或付費牆後的內容。`

---

## 9. 邊界案例處理

- **Prediction**：不做真偽裁定，只回覆可查詢到的預測來源結果。
- **Opinion**：標記為觀點陳述，不進入真偽判定。
- **Satire**：明確標示為諷刺/虛構來源。
- **資訊不足**：回覆「目前無法確認」，避免過度判斷。

---

## 10. 風險與限制

1. 公開資料不代表完整真相，尤其是封閉系統或內部文件。
2. 即時事件可能在分鐘級更新，需注意時效。
3. 社群平台容易混入未驗證傳言，只能作輔助訊號。
4. 個別官方來源可能有機構立場，需交叉來源平衡。

---

## 11. 多語文件

- English: `docs/README.en.md`
- Español: `docs/README.es.md`
- العربية: `docs/README.ar.md`



## 12. 搜尋優先與 Fallback（v1.0.5）

- 強制 Tavily 優先：有 `TAVILY_API_KEY` 且可用時，先用 Tavily。
- 僅在 key 缺失、401/403、429/額度不足、連續 timeout 時，才退回預設搜尋。
- fallback 不中斷流程，需註記該輪為 fallback。

### 來源配比
- Tavily/一般搜尋：50%
- Reddit CLI：10%
- Twitter CLI：40%

### CLI 不可用時重分配
- 無 Reddit：+7% 給 Tavily、+3% 給可信度交叉驗證。
- 無 Twitter：+28% 給 Tavily、+12% 給可信度交叉驗證。
- Reddit 與 Twitter 都無：Tavily 85% + 可信度交叉驗證 15%。

### 搜尋次數提升
- CLI 皆可用：10 次
- 缺 1 個 CLI：12 次
- 缺 2 個 CLI：14 次

### 最低呼叫次數（10 次基準）
- Tavily：至少 5 次
- Twitter CLI：至少 4 次
- Reddit CLI：至少 1 次

> 規則：最低次數是強制門檻，不得只象徵性各呼叫 1 次。若 CLI 不可用，其最低次數需依既有重分配規則轉為 Tavily 與可信度交叉驗證追加查詢。

## 13. Claim Core First（避免誤判）

核實時先判斷「核心主張」再判斷細節，避免把非核心描述誤當主要錯誤。

- 第一層（最高）：核心事實（事件有無、對象、方向）。
- 第二層（中）：關鍵條件（時間/地點等，僅在會改變真假時加權）。
- 第三層（低）：表述細節（快訊語氣、措辭），原則不得單獨翻盤。



## 14. 判定寬嚴校準（降低過嚴誤判）

- 核心原則：**核心事實寬容、關鍵誤導嚴格**。
- 判定順序：先看是否造成使用者誤導，再看細節是否完美。

### 四級判定
- **正確**：核心事實成立，關鍵條件無實質偏差。
- **部分正確**：核心成立但存在過時、脈絡不足、措辭誇張、次要偏差。
- **錯誤**：核心不成立，或關鍵條件錯到改變結論。
- **證據不足**：公開資訊不足以支持或反駁核心。

### 防過嚴規則
- 非核心瑕疵（快訊語氣、標題強度、非關鍵時間差）不得單獨導致「錯誤」。
- 核心成立時，預設落在「部分正確」，除非關鍵條件確實翻轉結論。



## 15. 評分、審核與寬鬆政策（持續優化）

- 新增「誤導風險分層」：高 / 中 / 低。
- 判定預設先落在「部分正確」，僅在核心不成立或關鍵條件改變決策時判「錯誤」。

### 翻盤檢查
- 若判錯主因是快訊語氣、標題強度、非關鍵時間差，需二次檢查是否真的改變結論。
- 若不改變，應降為「部分正確」。

### 不可寬鬆清單（維持嚴格）
- 公共安全
- 醫療風險
- 金融/詐騙
- 官方政策生效時間與適用條件
