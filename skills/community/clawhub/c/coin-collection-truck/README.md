# Hong Kong Coin Collection Truck (香港收銀車) Agent Skill

[English](#english) | [繁體中文](#繁體中文) | [简体中文](#简体中文)

---

<a id="english"></a>
## 🇬🇧 English

### Overview
This repository contains an AI Agent Skill designed to query the official schedule and locations of the Hong Kong Monetary Authority's Coin Collection Fleet (收銀車). The fleet consists of two trucks ("Truck 1" and "Truck 2") that travel across different districts in Hong Kong to collect coins from the public.

By installing this skill, your AI agent can understand natural language queries about the coin trucks and provide accurate, up-to-date information including locations, schedules, and service suspensions.

### Features
*   **Natural Language Queries:** Ask questions like *"Where are the coin trucks today?"* or *"When will the truck visit Sha Tin?"*
*   **Date & District Filtering:** Query by specific dates, relative dates (today/tomorrow), or specific Hong Kong districts.
*   **Upcoming Schedules:** Check the schedule for the next 7 days (or any specified number of days).
*   **Suspension Awareness:** Automatically detects and warns users about service suspension dates (暫停日期).
*   **Map Integration:** Provides direct Google Maps links using precise latitude and longitude coordinates.

### Skill Anatomy
The skill is structured according to the standard agent skill anatomy:
*   `SKILL.md`: The core instruction file containing metadata and guidelines for the AI agent.
*   `scripts/query_coin_truck.py`: A robust Python script that parses the JSON database and handles complex date/location logic.
*   `references/coin_collection_truck_hk.json`: The local JSON database containing the official schedule and coordinates.
*   `assets/`: Contains official logos for visual branding in agent responses.

### Usage Examples
Once installed, you can ask your agent:
*   *"Where is today's coin truck?"*
*   *"Show me the coin truck schedule for Yuen Long."*
*   *"Is Truck 1 operating on March 20th?"*
*   *"What are the upcoming coin truck locations for the next 3 days?"*

---

<a id="繁體中文"></a>
## 🇭🇰 繁體中文

### 簡介
本儲存庫包含一個專為查詢香港金融管理局「收銀車」日程及位置而設的 AI 代理技能 (Agent Skill)。收銀車車隊由兩輛貨車（「收銀車1號」及「收銀車2號」）組成，輪流在全港各區為市民提供硬幣收集服務。

安裝此技能後，您的 AI 代理將能夠理解有關收銀車的自然語言查詢，並提供準確、最新的資訊，包括位置、服務時間及暫停服務安排。

### 功能特色
*   **自然語言查詢：** 支援如「今日收銀車喺邊？」或「收銀車幾時會去沙田？」等日常提問。
*   **日期及地區篩選：** 可按特定日期、相對日期（今日/聽日）或香港特定地區進行查詢。
*   **未來日程：** 輕鬆查看未來 7 天（或自訂天數）的收銀車日程。
*   **暫停服務提示：** 自動偵測並提醒用戶有關「暫停日期」的安排，避免白走一趟。
*   **地圖整合：** 利用精確的經緯度數據，直接提供 Google Maps 連結，方便導航。

### 技能結構
本技能按照標準的代理技能結構編寫：
*   `SKILL.md`：核心指令文件，包含供 AI 代理讀取的元數據 (Metadata) 及操作指南。
*   `scripts/query_coin_truck.py`：強大的 Python 腳本，負責解析 JSON 數據庫並處理複雜的日期與位置邏輯。
*   `references/coin_collection_truck_hk.json`：本地 JSON 數據庫，包含官方日程及坐標。
*   `assets/`：包含官方標誌，供代理在回覆時作視覺展示之用。

### 使用範例
安裝後，您可以向 AI 代理提問：
*   「今日收銀車喺邊度？」
*   「俾元朗區嘅收銀車時間表我睇。」
*   「3月20號收銀車1號有冇開？」
*   「未來三日收銀車會去邊幾區？」

---

<a id="简体中文"></a>
## 🇨🇳 简体中文

### 简介
本仓库包含一个专为查询香港金融管理局“收银车”日程及位置而设计的 AI 代理技能 (Agent Skill)。收银车车队由两辆货车（“收银车1号”及“收银车2号”）组成，轮流在全港各区为市民提供硬币收集服务。

安装此技能后，您的 AI 代理将能够理解有关收银车的自然语言查询，并提供准确、最新的信息，包括位置、服务时间及暂停服务安排。

### 功能特色
*   **自然语言查询：** 支持如“今天收银车在哪里？”或“收银车什么时候会去沙田？”等日常提问。
*   **日期及地区筛选：** 可按特定日期、相对日期（今天/明天）或香港特定地区进行查询。
*   **未来日程：** 轻松查看未来 7 天（或自定义天数）的收银车日程。
*   **暂停服务提示：** 自动检测并提醒用户有关“暂停日期”的安排，避免白跑一趟。
*   **地图整合：** 利用精确的经纬度数据，直接提供 Google Maps 链接，方便导航。

### 技能结构
本技能按照标准的代理技能结构编写：
*   `SKILL.md`：核心指令文件，包含供 AI 代理读取的元数据 (Metadata) 及操作指南。
*   `scripts/query_coin_truck.py`：强大的 Python 脚本，负责解析 JSON 数据库并处理复杂的日期与位置逻辑。
*   `references/coin_collection_truck_hk.json`：本地 JSON 数据库，包含官方日程及坐标。
*   `assets/`：包含官方标志，供代理在回复时作视觉展示之用。

### 使用示例
安装后，您可以向 AI 代理提问：
*   “今天收银车在哪里？”
*   “给我看元朗区的收银车时间表。”
*   “3月20号收银车1号有营业吗？”
*   “未来三天收银车会去哪些区？”
