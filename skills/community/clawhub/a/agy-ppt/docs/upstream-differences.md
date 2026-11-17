# Upstream Differences：codex-ppt-skill 與 agy-ppt

本文件說明上游 [`ningzimu/codex-ppt-skill`](https://github.com/ningzimu/codex-ppt-skill)
與本專案 `agy-ppt` 的差異。目的是讓使用者清楚知道兩者各自的行為與設計選擇，
並公平描述 upstream，不使用貶低性措辭。

`agy-ppt` 是 standalone repository，不包含（vendor）完整 upstream checkout，也不使用
Git submodule。upstream 只在真的需要其未修改原始實作時，由
`scripts/codex_ppt_dependency.py` 解析為 external runtime dependency（詳見
[codex-ppt Dependency](../../README.md#codex-ppt-dependency)）。`agy-ppt` 本身內含
衍生自 upstream 並改作的實作（見下方第 6 節）。

## 1. 定位差異

| | upstream behavior | agy-ppt behavior |
| --- | --- | --- |
| 執行模型 | 單一 skill，由呼叫它的 agent（Codex/Claude/其他）直接驅動整個流程 | AGY（唯一 orchestrator / state owner）、明確指派的 Codex Production Engineering Worker 或 Kiro（engineering）、Codex Slide Image Worker（slide-image）分工 |
| 呼叫對象 | 直接呼叫 skill 內的腳本完成生成、組裝 | AGY 呼叫 worker，worker 完成後把結果交回 AGY，worker 之間不互相呼叫（`AGY -> worker -> AGY`） |
| 主要使用情境 | 單次或少量互動式生成一份 PPT | 需要跨 process resume、故障恢復、可稽核 state 的多頁 deck 生成 |
| 發佈方式 | 單一 repository，直接包含完整 skill 實作 | Standalone repository；upstream 實作不 vendor，只在需要時作為 external runtime dependency 解析 |

這是 design choice 的差異，不代表其中一種取代另一種：upstream 的直接驅動模型對單次
互動式使用仍然完全可用。

## 2. 圖片生成 backend

| | upstream behavior | agy-ppt behavior |
| --- | --- | --- |
| 預設 backend | `scripts/image_gen.py` + `image_providers/`（`openai_compatible.py`、`atlascloud.py`），需要 `OPENAI_API_KEY` 或相容的 API base URL | `scripts/codex_image_adapter.py`，透過已登入的 Codex CLI 訂閱 session 呼叫內建 `image_gen` 工具，不使用 API key |
| API key 是否為必要路徑 | 是，這是 upstream 的主要生成路徑 | 否；`codex_image_adapter.py` 會從子行程環境變數中移除 API-key 類變數，內建工具不可用時回報 `IMAGE_BACKEND_UNAVAILABLE`，不會自動改用付費 API |
| 是否保留 upstream 的 API 路徑 | -- | 是，`scripts/image_gen.py` 與 `scripts/image_providers/` 是衍生自 upstream 並改作的實作，位於 `skills/agy-ppt/scripts/`，供需要 API-key 路徑的使用者自行選用；但 agy-ppt 的正式 workflow 預設路徑是 Codex CLI 訂閱 session |

## 3. State 與流程控制

| | upstream behavior | agy-ppt behavior |
| --- | --- | --- |
| 進度追蹤 | `slide_jobs.json` + `slide_run_state.json`（`scripts/slide_run_state.py`），記錄 dispatch/完成狀態 | 新增 `project_state.py`：deck 級 phase state machine、每頁 slide state machine、generation 計數器、attempt 歷史、resume/recovery、worker-result 驗證，皆為 AGY-only 寫入 |
| 是否取代 upstream 的檔案 | -- | 不取代；`prepare_slide_prompts.py` 產出的 `prompts/slide_XX.json`、`slide_jobs.json` 仍是 prompt 與 dispatch 記錄的 source of truth，`project_state.py` 是額外疊加的控制層，引用而非複製這些檔案 |
| 中斷恢復 | 由呼叫端自行判斷 `slide_run_state.json` 決定是否續跑 | `project_state.py` 提供 deterministic 的 `recover_interrupted()`：沒有 completed result + 已驗證 artifact 就不視為成功 |
| 重複 generic 失敗的處理 | 由呼叫端自行決定是否重試 | AGY 端提供最多一次 immediate retry 的政策方法（`consecutive_failure_streak` / `may_retry_immediately` / `block_after_repeated_failure`），第二次連續同錯誤即 block 專案而非無限重試 |

## 4. 工程 worker 整合

| | upstream behavior | agy-ppt behavior |
| --- | --- | --- |
| 程式修改/除錯 | 由呼叫 skill 的 agent 自行處理 | 可由明確指派的 Codex Production Engineering Worker 或既有 Kiro ACP 路徑執行；結果一律回交 AGY，worker 不可自行推進簡報 workflow |
| Kiro 是否可呼叫 Codex | 不適用（upstream 無此分工） | 明確禁止：Kiro 不得呼叫 Codex，Codex 不得呼叫 Kiro，任一 worker 不得代替 AGY 決定下一步 |

## 5. 測試與恢復驗證

| | upstream behavior | agy-ppt behavior |
| --- | --- | --- |
| 自動化測試 | 未附帶 deterministic fault-injection 測試套件 | 新增 `tests/recovery/`（deterministic fault injection，不消耗額度）與 `tests/integration/test_phase9_live_*.py`（opt-in，消耗訂閱額度）等測試 |
| 額度消耗測試策略 | 不適用 | 一般 unit tests 與 `run_recovery_tests.py` 皆為 deterministic、不呼叫真實 Codex；live 測試需明確設定環境變數（如 `AGY_PPT_LIVE_RECOVERY=1`）才會執行 |
| Dependency resolver 測試 | 不適用 | `tests/test_codex_ppt_dependency.py`：全部使用暫存本機 Git repository，不使用真實 GitHub network |

## 6. 衍生自 upstream 並改作的部分

以下實作衍生自 upstream 設計，並整合進 `agy-ppt` 的 orchestration 模型：

- PPTX 組裝邏輯（`scripts/assemble_ppt.py`：讀取 `origin_image/slide_XX.png`、依頁碼排序、寫入 speaker notes）
- Slide prompt 準備流程（`scripts/prepare_slide_prompts.py`）
- 綠幕去除工具（`scripts/remove_chroma_key.py`）
- 風格庫（`references/*.md`）與其使用方式

## 7. External Runtime Dependency

`agy-ppt` 不 vendor 完整 upstream checkout。當某個功能真的需要 upstream 未修改的
原始實作時，由 `scripts/codex_ppt_dependency.py` 在需要的當下解析／下載：

- upstream URL 固定為 `https://github.com/ningzimu/codex-ppt-skill.git`
- 「latest」deterministic 定義為 `main` 分支目前的 HEAD commit
- 快取位置在本 repository 之外的 OS 應用程式快取目錄，也不在 Global AGY Skill
  安裝位置或任何簡報 workspace 之內
- upstream 暫時無法連線時，若已有快取則重用並印出警告（非 API fallback）；若沒有
  快取則回報明確的 `CODEX_PPT_DEPENDENCY_UNAVAILABLE` 錯誤

詳見根目錄 [`README.md`](../../README.md#codex-ppt-dependency) 的
「codex-ppt Dependency」章節，以及 `scripts/codex_ppt_dependency.py` 的模組文件。

## 8. 免責聲明

agy-ppt is not affiliated with or endorsed by the upstream author.

本文件與 agy-ppt 專案不宣稱取得 upstream 作者的背書或正式合作關係，亦不主張 upstream
原始工作為 agy-ppt 的原創成果。完整授權與來源歸屬請見根目錄 `LICENSE` 與
`THIRD_PARTY_NOTICES.md`。
