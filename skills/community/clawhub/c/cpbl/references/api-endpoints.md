# CPBL API Endpoints 偵查結果

## 已確認的 AJAX Endpoints

### 1. 戰績查詢
- **Endpoint:** `/standings/seasonaction`
- **方法:** POST
- **必要 Headers:**
  - `RequestVerificationToken`: 從頁面提取的 CSRF token
  - `X-Requested-With`: XMLHttpRequest
- **參數:**
  - `year`: 年份 (e.g., 2025)
- **回傳:** HTML 片段（包含球隊對戰戰績、團隊投球成績、團隊打擊成績、團隊守備成績等 4 個表格）
- **狀態:** ✅ 已驗證可用 (2026-03-20 20:46)
- **備註:** 不是 JSON API，需用 BeautifulSoup 解析 HTML

### 2. 賽程選項
- **Endpoint:** `/schedule/getoptsaction`
- **方法:** POST
- **必要 Headers:**
  - `RequestVerificationToken`: CSRF token
- **參數:**
  - `kindCode`: 賽事類型代碼
  - `year`: 年份
- **狀態:** ❌ 測試時返回 500 錯誤，需要更多參數

### 3. 統計數據
- **Endpoint:** `/stats/toplistaction`
- **方法:** POST
- **必要 Headers:**
  - `RequestVerificationToken`: CSRF token
  - `X-Requested-With`: XMLHttpRequest
- **參數:**
  - `year`: 年份 (e.g., 2025)
  - `kindCode`: A=一軍, W=二軍
- **回傳:** HTML 片段（包含 TopFiveList，顯示各項數據排行榜）
- **狀態:** ✅ 已驗證可用 (2026-03-20 20:47)
- **備註:** 不是 JSON API，需用 BeautifulSoup 解析 HTML

## CSRF Token 取得方式

從頁面 HTML 中提取：
```python
import re
import requests

# 取得頁面
response = requests.get('https://www.cpbl.com.tw/standings/season')
html = response.text

# 提取 token
match = re.search(r"RequestVerificationToken:\s*'([^']+)'", html)
token = match.group(1) if match else None
```

## 頁面結構分析

### 戰績頁面 (/standings/season)
- 使用 AJAX 載入資料
- 包含 4 個表格：
  1. 球隊對戰戰績
  2. 團隊投球成績
  3. 團隊打擊成績
  4. 團隊守備成績

### 賽程頁面 (/schedule)
- 使用 AJAX 動態載入
- 有日期選擇器
- 可能需要 JavaScript 渲染才能看到完整資料

## 技術難題

1. **AJAX + HTML 片段回傳:** CPBL 使用大量 AJAX，而且不是回 JSON，要自己解析 HTML 表格
2. **CSRF 保護:** 每個請求都需要有效的 CSRF token
3. **沒有公開 JSON API:** 所有資料都以 HTML 片段形式返回
4. **部分 endpoints 仍不穩:** 某些 endpoints 的參數名稱、回傳結構或可用性仍不穩定

## 備用資料源

### 1. 野球革命 (rebas.tw)
- 網址: https://www.rebas.tw/first-base-CPBL
- 需要啟用 JavaScript
- 可能有較友善的 API

### 2. Yahoo 運動
- 網址: https://tw.sports.yahoo.com/cpbl/
- 有新聞和基本資訊
- 可能需要爬蟲

### 3. ETtoday 運動雲
- 台灣體育新聞網站
- 可能有 CPBL 相關數據

### 4. 運動視界
- 運動新聞和分析
- 可能有額外資訊

## 建議的實作策略

### 方案 A: 直接打 AJAX endpoint 並解析 HTML（推薦）
- 優點: 速度較快 且已驗證 `/standings/seasonaction` 可直接取得四張表資料
- 缺點: 需要處理 CSRF 與欄位變動
- 作法: 
  1. 先取得有效 token
  2. POST AJAX endpoint
  3. 用 BeautifulSoup 解析 HTML 表格

### 方案 B: 直接打 AJAX Endpoints
- 優點: 速度較快
- 缺點: 需要正確的參數和 token
- 作法:
  1. 提取 CSRF token
  2. 模擬 AJAX 請求
  3. 解析返回的 HTML 片段

### 方案 C: 混合方案
- 優先使用 AJAX endpoints
- 失敗時改用 HTML 解析
- 最後嘗試備用資料源

## 下一步偵查

1. 用 scrapling dynamic mode 測試完整渲染
2. 嘗試找出賽程和統計的實際資料 endpoints
3. 測試備用資料源的可用性
4. 建立錯誤處理和 fallback 機制

## 更新日誌

- **2026-03-20 19:26**: 初始偵查完成，發現基本 endpoints 結構
- **2026-04-04 23:49**: 重新驗證 `/standings/seasonaction` 可回傳完整四張表資料 舊的「只有表頭」判斷已失效
