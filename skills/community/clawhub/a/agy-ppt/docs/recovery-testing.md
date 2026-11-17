# Recovery Testing：Fault Injection 與 Deterministic Recovery（Phase 9）

本文件說明 Phase 9 建立的自動化故障注入（fault injection）與恢復測試工具。

目的是能用**單一命令**回答一個問題：

> 這條 workflow 在各種 worker / backend / assembly 故障下，state 是否仍然正確、
> 可恢復、不會假裝成功？

Phase 9 只新增測試工具，**不修改** production workflow。以下元件在本階段視為
frozen，只被測試「使用」，不被修改：

- Kiro ACP Bridge（`scripts/kiro_acp_bridge.py`）
- Codex Image Adapter（`scripts/codex_image_adapter.py`）
- Project State Infrastructure（`scripts/project_state.py`、`scripts/validate_project.py`）
- upstream assembly（`scripts/assemble_ppt.py` 等）

## 1. 檔案位置

```
skills/agy-ppt/
├── scripts/run_recovery_tests.py          # 自動化 runner（單一命令）
├── scripts/run_live_recovery_tests.py     # Phase 9B~9D live runner（opt-in）
├── tests/helpers/
│   ├── fake_image_worker.py               # 可控制結果的假 image worker
│   ├── fake_assembly.py                   # 可控制失敗次數的假 assembly
│   ├── recovery_deck.py                   # 共用 harness（AGY 視角）
│   ├── live_recovery.py                   # Phase 9B~9D live harness（ledger / role process / kill scope）
│   └── fault_matrix.py                    # table-driven fault matrix 載入與斷言
├── tests/recovery/
│   ├── fault_matrix.json                  # fault -> 期待 state 對照表
│   ├── test_generation_failure.py         # Scenario 1
│   ├── test_backend_unavailable.py        # Scenario 2
│   ├── test_artifact_ambiguous.py         # Scenario 3
│   ├── test_invalid_output.py             # Scenario 4
│   ├── test_interrupted_generation.py     # Scenario 5
│   ├── test_qa_regeneration.py            # Scenario 6
│   ├── test_assembly_failure.py           # Scenario 7
│   └── test_resume_idempotency.py         # Scenario 8
└── tests/integration/
    ├── test_recovery_live.py                   # Live A / Live B（opt-in，會消耗額度）
    ├── test_phase9_live_resume.py              # 9B partial resume（兩個真實 process）
    ├── test_phase9_live_regenerate.py          # 9B regenerate（generation 1 -> 2）
    ├── test_phase9_live_interruption.py        # 9C process interruption（double opt-in）
    └── test_phase9_live_assembly_recovery.py   # 9D assembly recovery（不呼叫 Codex）
```

## 2. Mock vs Live（額度政策）

| | mock / recovery suite | live suite |
| --- | --- | --- |
| 位置 | `tests/recovery/` | `tests/integration/test_recovery_live.py`、`tests/integration/test_phase9_live_*.py` |
| 呼叫真實 Codex / Kiro / `image_gen` | **不會** | 會（僅 Codex 內建 `image_gen`；9D 完全不呼叫） |
| 消耗訂閱額度 | **不會** | 會（Live A 預設 1 turn、Live B 2 turns、9B resume 3 turns、9B regenerate 2 turns、9C ≤ 2 turns、9D 0 turns） |
| 預設是否執行 | 是 | **否**，需 `AGY_PPT_LIVE_RECOVERY=1`（9C 另需 `AGY_PPT_LIVE_RECOVERY_INTERRUPT=1`） |
| 決定論 | 完全 deterministic | 依賴真實 runtime |

mock 端有兩層保證，確保不可能偷偷打到真實 backend：

1. 故障全部由 `FakeImageWorker` / `FakeAssembly` 在記憶體與 temp 目錄產生。
2. 每個 recovery test 在 `setUp` 會把 `subprocess.Popen/run/call/check_call/check_output`
   換成會直接讓測試失敗的 guard（`ExternalProcessSpawned`）。任何試圖 spawn
   process 的行為都會被抓到，也不會有 API key 被讀取。

## 3. Fake Image Worker

`tests/helpers/fake_image_worker.py` 回傳與真實 adapter **相同**的 result contract
（`agy-ppt/codex-image-adapter-result/1`），因此 `record_worker_result()` 會用同一套
驗證邏輯處理它。

每頁可用 `SlidePlan` 腳本化：

| 欄位 | 意義 |
| --- | --- |
| `fault` | 要注入哪一種故障（見下表） |
| `succeed_on` | 第幾次 generation 才成功（`succeed_on=2` → 第 1 次故障、第 2 次成功） |
| `create_artifact` | 成功的那一輪是否真的寫出 artifact（`False` 可模擬「回報成功但檔案不在」） |
| `fault_artifact` | 故障 / 中斷的那一輪是否仍在 output path 留下 artifact |
| `ambiguous_count` | ambiguous 時留下幾個候選 artifact |
| `invalid_artifact` | 寫出非影像 payload |
| `output_dir` | 輸出目錄（預設 `origin_image`） |

支援的故障：

| fault | 行為 |
| --- | --- |
| `success` | completed + 合法 PNG |
| `IMAGE_GENERATION_FAILED` | error，無 artifact |
| `IMAGE_BACKEND_UNAVAILABLE` | error，內建 `image_gen` 不可用（永不 fallback 付費 API） |
| `IMAGE_ARTIFACT_AMBIGUOUS` | error，diagnostics 保留 ≥2 個 candidates |
| `IMAGE_ARTIFACT_NOT_FOUND` | error，找不到 artifact |
| `IMAGE_OUTPUT_INVALID` | error，產出不是可讀影像（被 quarantine，不進 output path） |
| `CODEX_TIMEOUT` | error，render turn 超時 |
| `interrupted` | **丟出 `FakeWorkerInterrupted`**，AGY 收不到任何 result |

`worker.calls` 記錄每一次 render turn，用來證明「已完成的 slide 沒有被重生」。

## 4. Fake Assembly

`tests/helpers/fake_assembly.py` 模擬 assembly 的 contract，但不 import
`python-pptx`、不重生任何 slide image：

- `fail_times=N`：前 N 次 assembly 失敗（`ASSEMBLY_FAILED`），之後成功
- 失敗時**不寫出任何 deck 檔案**（不留半成品）
- qa_passed 的 slide 缺圖時回報 `ASSEMBLY_INPUT_MISSING`，不會默默組裝
- 每次 run 會記錄讀到的 image digest，用來證明兩次 assembly 之間圖片沒被改動
- `fix()` 模擬「assembly 問題修好了」

## 5. Fault Matrix（table-driven）

`tests/recovery/fault_matrix.json` 是 fault → 期待 state 的對照表，避免在四個檔案
裡重複同樣的斷言程式碼。`helpers/fault_matrix.attach_matrix_tests()` 會為每一列
自動產生一個獨立測試（各自有獨立 workspace 與 state 檔）。

| fault | matrix `expected` | 記錄後 slide state | AGY 動作 | 最終 slide state |
| --- | --- | --- | --- | --- |
| `IMAGE_GENERATION_FAILED` | `generation_failed` | `generation_failed` | 可 retry | `generation_failed` → `ready` |
| `CODEX_TIMEOUT` | `generation_failed` | `generation_failed` | 可 retry | `generation_failed` → `ready` |
| `IMAGE_BACKEND_UNAVAILABLE` | `blocked` | `generation_failed` | 標記 blocked | `blocked`（記得 `phase_before_block`） |
| `IMAGE_ARTIFACT_AMBIGUOUS` | `not_generated` | `generation_failed` | 可 retry | `generation_failed` → `ready` |
| `IMAGE_OUTPUT_INVALID` | `not_generated` | `generation_failed` | 可 retry | `generation_failed` → `ready` |

每一列共同驗證：

- worker error_code 被保留（result、attempt、slide `blocker` 三處一致）
- 不進入 `generated`、不寫入合法 `image_path`
- 判定結果在 reload 之後仍然存在
- retry 只能由 AGY 明確發動（沒有任何 auto-retry）

## 6. 八個 Recovery Scenario 與期待 state

| # | 檔案 | 情境 | 主要期待 |
| --- | --- | --- | --- |
| 1 | `test_generation_failure.py` | slide_01/02 成功、slide_03 `IMAGE_GENERATION_FAILED` | 01/02 維持 `generated`（generation 不變）；03 = `generation_failed`；04 仍 `planned` 不被誤標完成；AGY `generation_failed → ready` 後第 2 次成功，`generation = 2`、`attempts = 2` |
| 2 | `test_backend_unavailable.py` | 內建 `image_gen` 不可用 | 不得 `generated`；slide 與 project 進入合法 `blocked` 並記住 `phase_before_block`；state reload 後完整保留；backend 恢復後可 resume，已完成 slide 不重生、image bytes 不變 |
| 3 | `test_artifact_ambiguous.py` | 多個候選 artifact | 不自行選 artifact（`origin_image/` 不會多出檔案）；不進 `generated`；diagnostics 保留全部 candidates 並可 reload；AGY 可重新派發 generation |
| 4 | `test_invalid_output.py` | 產出不是合法影像 | 無效 artifact 不進 `generated`；`image_path` 不被記成合法 final output；用 production `sniff_image()` 確認 payload 真的無效；output path 上的既有垃圾檔不被採用；retry 後才有合法圖 |
| 5 | `test_interrupted_generation.py` | 中斷在 `generating` | 沒有 completed attempt → `generation_failed`；有 completed attempt 但 artifact 不存在 → `generation_failed`；有 artifact 但沒有 recorded result → 仍 `generation_failed`（不猜成功）；completed attempt + verified artifact → 可 deterministic 恢復為 `generated`；recovery 不動其他 slide、不推進 phase、可重複執行 |
| 6 | `test_qa_regeneration.py` | gen1 成功 → AGY `qa_failed` → `ready` → gen2 成功 → `qa_passed` | `generation = 2`、`attempts = 2`；attempt 1 不消失也不被覆寫；visual QA 判斷只有 AGY 能做（`by="codex"` 會被拒絕）；其他 slide 狀態與圖片位元不變 |
| 7 | `test_assembly_failure.py` | 全部 `qa_passed`，assembly 第一次失敗 | 不重生 slide image（worker call 數與 digest 不變）；`qa_passed` 不消失；project 不得回到 `slide_generation` / `visual_qa`；失敗不留半成品 deck；若 blocked，resume 只能回到 `assembly`；修好後只重跑 assembly，第二次成功 → slide `assembled`、project `complete` |
| 8 | `test_resume_idempotency.py` | 重複記錄 / 重複 resume | 相同 idempotency key 重複記錄：不 +generation、不 +attempts、不重複 history、不會反轉已做的 QA；無 key 的重複記錄會被拒絕而不是重複計數；resume 只派發未完成 slide；第二次 resume 不派發任何 worker；`complete` 專案重複 resume 完全不呼叫 worker；phase 不會重複推進；reload → save → reload 無漂移 |

## 7. 如何執行 Phase 9

單一命令（deterministic，不消耗額度）：

```bash
python3 skills/agy-ppt/scripts/run_recovery_tests.py
```

輸出：

```text
Phase 9 Recovery Test
PASS generation failure
PASS backend unavailable
PASS artifact ambiguous
PASS invalid artifact
PASS interrupted generation
PASS QA regeneration
PASS assembly failure
PASS resume/idempotency

8/8 PASS
```

exit code：全過 `0`；任一 scenario 失敗 `1`（參數錯誤 `2`）。

其他用法：

```bash
# 每個 scenario 顯示測試數與耗時
python3 skills/agy-ppt/scripts/run_recovery_tests.py -v

# 只跑單一 scenario
python3 skills/agy-ppt/scripts/run_recovery_tests.py --scenario test_assembly_failure

# 機器可讀報告
python3 skills/agy-ppt/scripts/run_recovery_tests.py --json recovery-report.json

# 列出 scenario
python3 skills/agy-ppt/scripts/run_recovery_tests.py --list
```

recovery suite 也會被既有的全量 unit test 指令自動收錄：

```bash
python3 -m unittest discover -s skills/agy-ppt/tests -t skills/agy-ppt/tests -p "test_*.py"
```

## 8. Live Tests（opt-in，會消耗訂閱額度）

預設不執行。只有明確 opt-in 才會呼叫真實 Codex：

```bash
AGY_PPT_LIVE_RECOVERY=1 python3 -m unittest discover \
    -s skills/agy-ppt/tests/integration -t skills/agy-ppt/tests/integration -v

# 或直接執行
python3 skills/agy-ppt/tests/integration/test_recovery_live.py
```

| 環境變數 | 預設 | 說明 |
| --- | --- | --- |
| `AGY_PPT_LIVE_RECOVERY` | 未設定 | `=1` 才啟用 live scenario |
| `AGY_PPT_LIVE_RECOVERY_SLIDES` | `1` | Live A 真實生成幾頁 |
| `AGY_PPT_LIVE_RECOVERY_TIMEOUT` | `420` | 單次 render turn 逾時秒數 |

- **Live A**：真實生成少量 slide 後 reload state，驗證已完成 slide 不重生
  （resume 不會派發它們、image bytes 不變、`generation` 保持 1）。
- **Live B**：真實生成一頁 → AGY 判定 `qa_failed` → 真實 regenerate，驗證
  `generation = 2`、`attempts = 2`、attempt 1 未被覆寫。

Live 測試只寫入 `<repo>/.agy-ppt-integration/live-recovery/`，teardown 會刪除。
若當前 runtime 沒有內建 `image_gen`（回報 `IMAGE_BACKEND_UNAVAILABLE`），視為
runtime capability blocker 而 skip，不是程式錯誤，也不會 fallback 付費 API。

## 8B. Phase 9B~9D Live Failure & Recovery（opt-in，會消耗訂閱額度）

Phase 9A 用 fake worker 證明 deterministic recovery；Phase 9B~9D 用**真實 runtime**
再證明一次。單一命令：

```bash
AGY_PPT_LIVE_RECOVERY=1 python3 skills/agy-ppt/scripts/run_live_recovery_tests.py

# 額外執行 process interruption（會真的 kill 一個真實 Codex generation）
AGY_PPT_LIVE_RECOVERY=1 AGY_PPT_LIVE_RECOVERY_INTERRUPT=1 \
    python3 skills/agy-ppt/scripts/run_live_recovery_tests.py
```

輸出：

```text
Phase 9B-9D Live Failure & Recovery
PASS partial resume
PASS regenerate
SKIPPED process interruption (…AGY_PPT_LIVE_RECOVERY_INTERRUPT=1…)
PASS assembly recovery

codex real invocations: 5
duplicate invocations: 0
api fallback count: 0

3 PASS, 0 FAIL, 1 SKIPPED of 4 scenarios
```

exit code：任一 required scenario `FAIL`、出現 duplicate invocation、或出現 API
fallback 都是非 0；runtime capability blocker 造成的 `SKIPPED` 不算失敗。

| scenario | 檔案 | 真實 render turn | 主要期待 |
| --- | --- | --- | --- |
| 9B partial resume | `test_phase9_live_resume.py` | 3 | Process A 建立 3 頁 disposable project、真實生成 slide_01/02 並記為 `qa_passed` 後**完全退出**；Process B 是全新 process，只從磁碟讀 state，必須跳過 slide_01/02、只真實生成 slide_03。最終 `slide_01/02/03` 各 1 次 invocation、duplicate = 0、generation 均為 1、已完成圖片 bytes 不變 |
| 9B regenerate | `test_phase9_live_regenerate.py` | 2 | 真實 generation 1 → 測試控制器明確判 `qa_failed`（理由固定 `Phase 9B regeneration state test`）→ `ready` → 真實 regenerate 為 generation 2 → `qa_passed`。`generation = 2`、`attempts = 2`、Codex invocation = 2、兩次 attempt metadata 都保留、最終 image 真實可讀、`backend = codex_builtin_imagegen`、`api_fallback_used = false` |
| 9C process interruption | `test_phase9_live_interruption.py` | ≤ 2 | 真實 Codex generation 被中斷後，由全新 process 重讀 state；沒有 completed result + verified artifact 就必須 `generating → generation_failed`（不猜成功）；再由測試控制器 `generation_failed → ready → generation 2`，第二次成功後 `qa_passed` |
| 9D assembly recovery | `test_phase9_live_assembly_recovery.py` | 0 | 不呼叫 Codex；用測試 PNG 讓所有 slide 在 `qa_passed`，先用安全可預測的 invalid assembly input 讓真實 `assemble_ppt.py` 失敗。slides 不倒退、generation 不增加、attempts 不增加、Codex invocation = 0、失敗不留半成品 deck；修正 input 後只重跑 assembly，slides → `assembled`、project → `complete` |

### `codex_invocations.jsonl`

`tests/helpers/live_recovery.py` 的 `InvocationLedger` 是跨 process 的 append-only
帳本：**只有真正準備呼叫 Codex 的那一刻**才寫入一行 `codex_invocation`，turn 回來
後再寫一行 `codex_result`。因此

- resume 跳過的 slide 完全不會留下任何一行（這就是 partial resume 的證據）；
- 被 kill 掉的 turn 只會有 `codex_invocation`、沒有 `codex_result`；
- duplicate invocation 的定義是「同一個 slide + 同一個 generation 被呼叫超過一次」，
  所以 regenerate（generation 2）永遠不算 duplicate。

### Process interruption 的 kill 範圍（安全性）

9C **不使用** `killall codex`，也不搜尋 process table：

1. 產生 generation 的 child process 會先安裝一個「只觀察、不改行為」的
   `subprocess.Popen` tracker，把自己啟動的每個 PID / process group 寫進
   `tracked_child_processes.jsonl`；
2. 控制端只會 kill：自己啟動的那個 Python child PID，以及帳本裡記錄到的
   Codex process group（adapter 使用 `start_new_session=True`，該 process 是自己
   group 的 leader，所以 kill 這個 group 不可能碰到別人的 Codex session）；
3. 永遠不會 signal 自己的 process group、`pid <= 1`、或任何沒有被記錄過的 group；
4. 若中斷視窗沒抓到（例如 turn 太快就結束），scenario 會 `SKIPPED`（inconclusive）
   而不是 FAIL，並且仍然會把 tracked 的 Codex child 收乾淨。

### 環境變數

| 環境變數 | 預設 | 說明 |
| --- | --- | --- |
| `AGY_PPT_LIVE_RECOVERY` | 未設定 | `=1` 才執行 resume / regenerate / assembly recovery |
| `AGY_PPT_LIVE_RECOVERY_INTERRUPT` | 未設定 | 再加 `=1` 才執行 process interruption |
| `AGY_PPT_LIVE_RECOVERY_TIMEOUT` | `420` | 單次 render turn 逾時秒數 |
| `AGY_PPT_LIVE_RECOVERY_INTERRUPT_WAIT` | `90` | 等待 tracked Codex child 出現的秒數 |
| `AGY_PPT_LIVE_RECOVERY_INTERRUPT_DELAY` | `5` | 觀察到 child 之後、動手中斷前的等待秒數 |
| `AGY_PPT_LIVE_RECOVERY_LEDGER` | 未設定 | 自訂 `codex_invocations.jsonl` 路徑（runner 會自動設一個共用檔） |
| `AGY_PPT_LIVE_RECOVERY_KEEP` | 未設定 | `=1` 保留 `.agy-ppt-integration/` 下的產出以便 debug |
| `AGY_PPT_LIVE_ASSEMBLY_PYTHON` | 未設定 | 指定執行 `assemble_ppt.py` 的 interpreter（預設找 runtime venv） |

所有 9B~9D 產出只寫入 `<repo>/.agy-ppt-integration/<scenario>/`，結束後 best-effort
刪除。9D 需要 `python-pptx`：測試**不會安裝任何 dependency**，找不到可用 interpreter
時視為 capability blocker 而 `SKIPPED`。

## 9. 本階段不做

- parallel generation（仍是 `sequential_only`）
- 修改任何 frozen production component
- 新增 queue
- 修改 Codex prompt
- 使用 API key
