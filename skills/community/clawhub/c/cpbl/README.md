# CPBL Skill - 中華職棒資訊查詢 ⚾

查詢中華職棒 CPBL 即時比分 已完賽結果 賽程 戰績 球員數據 新聞與歷史資料

## v1.5.2 重點

- **Scrapling StealthyFetcher 正式取代 Camoufox**：維基館爬蟲全面改用 Scrapling 原生 API
  - `StealthyFetcher.fetch()` 一行搞定，不再需要手動管理 browser context
  - 支援 `StealthySession` 複用 browser，多頁面查詢更高效
  - CLI `scrapling extract stealthy-fetch --ai-targeted` 也可直接用
  - 文字提取改用 `page.css()[0].get_all_text()` 取代舊的 `inner_text()`
- **SKILL.md 加入安裝說明**：新增 `metadata.openclaw.requires` (uv, python3) 與 stealth browser 安裝步驟
- **移除 camoufox 直接依賴**：scrapling 內建 patchright stealth browser，不需要額外裝 camoufox
- **已驗證**：StealthyFetcher 成功抓取 twbsball (Anubis v1.25.0)，MVP 歷史頁 2233 字元完整取得

## v1.5.1 重點

- **Scrapling StealthyFetcher 取代 Camoufox**：維基館爬蟲改用 Scrapling 原生 API
  - `StealthyFetcher.fetch()` 一行搞定，不再需要手動管理 browser context
  - 支援 `StealthySession` 複用 browser，多頁面查詢更高效
  - CLI `scrapling extract stealthy-fetch` 也可直接用
- **移除 camoufox 直接依賴**：scrapling 內建 stealth browser，不需要額外裝 camoufox

## v1.5.0 重點

- **Scrapling 繞過 Anubis 防爬機制**：台灣棒球維基館 (twbsball) 自 2026-05 啟用 Anubis v1.25.0 Proof-of-Work + browser fingerprint 防護
  - `web_fetch`、`tavily_extract`、Playwright 全部被封鎖
  - Scrapling `StealthyFetcher` headless 模式即可成功繞過 PoW 挑戰
  - SKILL.md 新增 Scrapling 使用範例與注意事項
- **維基館查詢優先順序調整**：歷史/獎項資料改用 StealthyFetcher → web_search → 維基百科 → 手動查詢
- **依賴更新**：skill venv 已有 `scrapling[all]`（內含 stealth browser 引擎）

## v1.4.3 重點

- **Box Score 詳細數據**：已結束比賽現在會顯示完整投手與打者成績
  - 投手：局數(IP) 被安打(H) 自責分(ER) 三振(K) 四壞(BB) 被全壘打(HR) 中繼成功(H) 救援成功(SV) 最快球速
  - 打者：打數(AB) 安打(H) 打點(RBI) 全壘打(HR) 得分(R) 盜壘(SB) MVP標記
- **比賽狀態修正**：`getlive` 的 `GameStatus=3` 現在會正確覆蓋 `PresentStatus=2`，比賽不再卡在「比賽中」
- **比賽時長格式**：`032300` → `3h23m` 人類可讀格式
- **救援投手支援**：勝投/敗投/救援成功 全部顯示
- **中繼點/救援點**：投手摘要加入中繼成功(H) 與救援成功(SV) 標記
- **PR #3 合併**：N+1 query 優化、TTL 快取、CSRF token 累 HTTP 優先、平行 detail fetch

## v1.4.2 重點

- **戰績排名修復**：`cpbl_standings.py` 現在可正確解析官方 `/standings/seasonaction` 回傳的四張表
- **二軍代碼修正**：二軍查詢改用 `D` 避免沿用錯誤代碼
- **文件同步更新**：清掉舊的「只有表頭 沒資料」描述 避免誤導
- **主流程 smoke test 全過**：standings live schedule games stats 都已重新驗證

## v1.4.0 重點

- **即時局數顯示**：`cpbl_live.py` 現在能正確顯示比賽進行中的「第N局上/下半」
- **延賽自動偵測**：API 標記已結束但 0:0 無勝敗投 → 自動判為延賽 🌧️
- **API 延遲修正**：`PresentStatus=1`(未開打) 但已有非零比分 → 修正為比賽中
- 移除 `cpbl_news.py`（功能已被 `web_search` 取代）
- 移除 `lxml` 依賴 其餘腳本盡量維持輕量

## 功能

- 即時比分 `scripts/cpbl_live.py`
- 已完賽結果 `scripts/cpbl_games.py`
- 賽程查詢 `scripts/cpbl_schedule.py`
- 戰績排名 `scripts/cpbl_standings.py`
- 球員與排行榜數據 `scripts/cpbl_stats.py`
- 近期新聞 直接用 `web_search` 查 CPBL 官網新聞頁
- 歷史獎項與紀錄 Scrapling StealthyFetcher 查台灣棒球維基館（可繞過 Anubis 防爬）

## 資料來源

| 來源 | 用途 | 備註 |
|------|------|------|
| CPBL 官方站隱藏 API | 即時比分 比賽結果 賽程 戰績 球員數據 | 直接可用 |
| 台灣棒球維基館 | 年度獎項 歷史紀錄 球員生涯資料 | 需 Scrapling StealthyFetcher 繞過 Anubis |

## 快速開始

```bash
uv run scripts/cpbl_live.py --output text
uv run scripts/cpbl_games.py --date 2026-04-01 --output text
uv run scripts/cpbl_schedule.py --month 2026-04 --all
uv run scripts/cpbl_standings.py
uv run scripts/cpbl_stats.py --year 2025 --category batting --top 10
# 近期新聞請用 web_search 搜尋 CPBL 官網
```

### 查詢台灣棒球維基館（需 Scrapling StealthyFetcher）

**安裝（首次使用前）：**
```bash
# 1. 建立 venv 並安裝依賴（如果 .venv 不存在）
cd skills/cpbl && uv venv && uv pip install -e .
# 2. 安裝 stealth browser（Scrapling StealthyFetcher 需要）
.venv/bin/scrapling install --force
```

```python
# 在 CPBL skill venv 中執行
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    "https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員",
    headless=True,
    wait=10000,  # 等 Anubis PoW 挑戰完成
)
text = page.css("#mw-content-text")[0].get_all_text()
print(text)
```

多頁面查詢用 `StealthySession` 複用 browser：
```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True) as session:
    page1 = session.fetch("https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員")
    text1 = page1.css("#mw-content-text")[0].get_all_text()
```

## 授權

僅供學習與個人使用 請遵守 CPBL 官網與資料來源的使用條款