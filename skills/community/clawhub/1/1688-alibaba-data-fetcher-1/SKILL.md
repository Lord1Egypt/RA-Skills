---
name: "1688-alibaba-data-fetcher"
description: "1688卖家工作台数据抓取：原生聊天用MEDIA、飞书必须用message；登录必须同回合内持续poll。"
---

# 1688卖家工作台 — 1688 Data Claw 插件 数据抓取

> 适用系统：Linux (Ubuntu 24.04) / Windows 10/11
> 插件：1688 Data Claw v1.0.0（自研 Chrome 扩展，content script 自动采集 + 外部 API 获取）

## ⚠️ 执行规则（最高优先级）

**本 skill 所有操作必须通过 skill 文件夹内预装的脚本完成，禁止自行编写代码。**
**工作流程中避免输出思考、执行过程、输出目前执行到了哪一步，只输出给用户的登录二维码图片、报告、首次安装后的提示等必要内容** 
1. **先看目录**：每次执行前，先 `ls $SKILL_DIR/scripts/` 确认可用脚本
2. **只用脚本，不写代码**：数据采集用 `fetch_data.py`，报告生成用 `generate_report_v3.py`，飞书推送用 `push_feishu_post.py`，浏览器管理用 `start-browser.sh/.ps1`。**禁止在 chat 中拼接 Python/JS 代码来替代脚本，如果脚本运行有问题再考虑阅读并修复问题**
3. **脚本路径始终相对于 `$SKILL_DIR`**：`cd $SKILL_DIR && python3 scripts/xxx.py`（Windows 用 `.\python3.cmd` 替代 `python3`）
4. **数据来源只能是插件**：报告生成脚本只读取 `fetch_data.py` 产出的 JSON，禁止自己调用 API 或猜测数据
5. **🔒 报告数据只读**：报告 7 段数据（商品/流量/交易/新老客/新灯塔/流量渠道/关键词）由 `generate_report_v3.py` 生成，**模型绝对禁止修改、删减、重写、替换、添加**。模型仅可修改 `## ⚠数据诊断` 与 `## ✅明日工作清单` 段落
6. **违反上述规则的操作无效**，必须按脚本流程重新执行

---

## ⚠️ Windows 浏览器隔离（必读）

**Windows 上必须使用独立 Chromium 便携版，与用户日常 Chrome 完全隔离。**

| 隔离层级 | 说明 |
|---|---|
| **独立可执行文件** | 从 skill 预打包的 Chromium 压缩包解压到专用目录 |
| **独立 user-data-dir** | 不共享用户的 cookies、密码、会话、扩展 |
| **独立 CDP 端口** | `9222`，避免与用户 Chrome DevTools 冲突 |
| **禁用同步** | `--disable-sync` |
| **禁用后台服务** | 关闭组件更新、崩溃报告等 |

**`executablePath` 指向独立 Chromium，`user-data-dir` 指向独立目录。**

**⚠️ 三层强制验证（缺一不可）：** 1) CDP 9222 端口有响应；2) `$USER_DATA/.openclaw_browser_marker` 标记文件存在；3) 进程参数 `--user-data-dir` 指向独立目录（Linux: `/tmp/chromium`，Windows: `C:\isolated-profiles\1688-agent`）。任何一层不通过 → 视为非独立 Chromium → 拒绝连接。**任何时候都禁止连接用户 Chrome。**

## 触发条件

用户提到以下关键词时使用本 skill，**先 `ls $SKILL_DIR/scripts/` 查看可用脚本**：
- 1688 数据抓取、1688 店铺数据、1688 诊断
- 1688 Data Claw、数据采集
- 飞书推送 1688 报告
- 1688 登录二维码
- 登录

## 一、初始化

> **路径约定：** `$SKILL_DIR` = 本 SKILL.md 所在目录。`$SKILL_DIR/..` 为 workspace 目录（报告输出位置）。**Python 脚本内置跨平台支持（`platform.system()` 自动检测 Linux/Windows）。**

### 1.1 固定路径（主会话和定时任务必须使用相同实例）

| 项目 | Linux | Windows |
|------|-------|--------|
| **浏览器可执行文件** | `$SKILL_DIR/chromium/chrome-linux64/chrome` | `$SKILL_DIR/chromium/chrome-win64/chrome.exe` |
| **用户数据目录** | `/tmp/chromium` | `C:\isolated-profiles\1688-agent` |
| **插件目录** | `$SKILL_DIR/plugin`（随 skill 打包） | 同 |
| **CDP 端口** | `9222` | `9222` |
| **虚拟显示** | `Xvfb :99` | 不需要 |
| **输出目录** | `$SKILL_DIR` | `$SKILL_DIR` |
| **飞书 chat_id / 凭证** | 从 `scripts/env.sh` 读取 | 从 `scripts/env.ps1` 读取 |

**关键规则：** 1) 启动前先检查 CDP 9222（Linux `curl`，Windows `curl.exe` 避免 PowerShell 别名冲突）；2) **绝不 kill 任何进程**；3) 用预打包的 Chromium（Snap 版不稳定）；4) 凭证从 env 文件读取，禁止硬编码。

### 1.2 脚本目录

| 脚本 | 平台 | 用途 |
|------|------|------|
| `setup.sh` / `setup.ps1` | Linux / Windows | 一键初始化：依赖 + Chromium + 嵌入式 Python + 目录。**首次部署**执行一次 |
| `start-browser.sh` / `start-browser.ps1` | Linux / Windows | 启动/复用独立 Chromium（三层验证） |
| `fetch_data.py` | 跨平台 | 一键采集 → 保存 JSON。Windows 用 `python3.cmd` |
| `generate_report_v3.py` | 跨平台 | **当前默认**：Markdown 表格版日报 |
| `generate_report_v2.py` / `generate_report.py` | 跨平台 | 旧版（v2紧凑/v1表格），已弃用保留供参考 |
| `push_feishu_post.py` | 跨平台 | 飞书推送：直接调飞书 `im/v1/messages` API 用 `post`+`md`，正确渲染表格 |
| `login.py` | 跨平台 | 一键登录：清Cookie→扫码→等待 |
| `cdp_client.py` | 跨平台 | CDP 客户端模块 |
| `python3.cmd` | Windows | 嵌入式 Python 3.12 启动器 |

### 1.3 一键初始化（首次部署执行一次）

```bash
# Linux
./scripts/setup.sh
# Windows
.\scripts\setup.ps1
```

**Chromium 下载源：** npmmirror（淘宝，国内 ~4.5MB/s），自动回退 Google 官方源。

### 1.4 启动浏览器（仅在 CDP 9222 无响应时执行）

```bash
./scripts/start-browser.sh         # Linux
.\scripts\start-browser.ps1        # Windows
```

逻辑：检查端口 → 已运行则三层验证 → 通过跳过/未通过拒绝（不杀进程）→ 未运行则启动独立 Chromium（`--load-extension` + 独立 `--user-data-dir` + `--disable-sync`）。**绝不连接用户 Chrome。**

### 1.5 插件位置（随 skill 打包在 `plugin/`）

```
plugin/
├── manifest.json       # 固定 ID: ekmgnempbbamlmaolijdfjakeopniion
├── background.js       # Service Worker - 数据汇总 + API
├── content.js          # Content Script - 自动采集
├── md5.js              # MTOP 签名
├── popup.html/js
├── openclaw-bridge.js
└── icons/
```

### 1.6 配置飞书通知

> v3 推送链路：app_id + app_secret + chat_id，不依赖 OpenClaw `message` 工具或 lark-cli。

**步骤 1：向用户获取三项凭证**

| 项目 | 获取方式 |
|------|----------|
| App ID（`cli_` 开头） | 飞书开发者后台 → 应用 → 凭证 |
| App Secret | 同上 |
| Chat ID（`oc_` 开头） | 用户提供目标群聊会话 ID |

**步骤 2（可选）：OpenClaw Gateway 绑定飞书 channel**（仅在需要在 chat 内接收消息时保留）

```bash
openclaw plugins install @openclaw/feishu
openclaw gateway restart
```

**步骤 3：把三项凭证写入 env 文件**

`scripts/env.sh`（Linux） / `scripts/env.ps1`（Windows）：

```bash
export FEISHU_APP_ID="cli_xxxxxxxx"
export FEISHU_APP_SECRET="***"
export FEISHU_CHAT_ID="oc_xxxxxxxx"
```

```powershell
$script:FEISHU_APP_ID = "cli_xxxxxxxx"
$script:FEISHU_APP_SECRET = "***"
$script:FEISHU_CHAT_ID = "oc_xxxxxxxx"
```

**步骤 4：验证推送链路**

```bash
# 验证 token
python3 scripts/push_feishu_post.py --check
# Windows: cd $SKILL_DIR; .\python3.cmd scripts/push_feishu_post.py --check

# 发送测试报告
python3 scripts/push_feishu_post.py $SKILL_DIR/1688_daily_report_v3.md
```

成功 → 飞书目标群收到 Markdown 卡片，输出 `✅ 发送成功，message_id: om_xxxxx`。失败检查：`FEISHU_APP_ID/SECRET/CHAT_ID`、应用是否已发布、`im:message:send_as_bot` 权限、IP 白名单。

---

## 二、数据抓取方案（1688 Data Claw 插件）

**通过 CDP 连接浏览器，在页面上下文执行 JS，调 `chrome.runtime.sendMessage` 外部消息 API 获取插件采集的数据。** 数据由插件自动采集，模型**禁止自行调用 API 或猜测**。

**固定扩展 ID：** `ekmgnempbbamlmaolijdfjakeopniion`

**采集页面：**

| 页面 | URL | 采集内容 |
|------|-----|----------|
| **工作台** | `work.1688.com` | 旺旺响应率、咨询满意度、物流指标、品质退款率、新灯塔评分 |
| **生意参谋** | `sycm.1688.com` | 店铺排名、商品概况、流量、询盘、交易、近7天流量来源/关键词 |

content script 在导航完成后自动采集，等待 5-8s 即可通过 `fetch_claw_data(mode='full')` 获取。详见预装的 `scripts/cdp_client.py`。

**API Mode：** `full`（全部）/ `sycm`（仅生意参谋）/ `work`（仅工作台）/ `summary`（汇总）。

---

## 三、数据结构（插件采集，禁止自己拿）

### 3.1 生意参谋（sycm）

```json
{
  "_pageType": "sycm",
  "companyName": "店铺名", "category": "主营类目", "subCategory": "子类目",
  "identity": "svip", "isSvip": true,

  "rankTrend": {
    "lastDate": "YYYY-MM-DD", "rank": 5, "layer": 3,
    "cateLevel1": "...", "cateLevel2": "...",
    "payAmt": 12345.67,
    "rawDates": [...], "rawRanks": [...], "rawPayAmt": [...]
  },

  "itemOverview": { /* 在线/动销/UV/PV */
    "statDate": "YYYY-MM-DD", "itemCnt": 100, "pullSalesItemCnt": 50,
    "uv": 200, "payItemQty": 8, "hasVisitorItemCnt": 30, "itemPv": 500
  },

  "flowStats": { /* 总展现/PV/UV/点击/跳失/无线 */
    "statDate": "YYYY-MM-DD", "revealCnt": 1000, "pv": 500, "uv": 200,
    "clickRate": 0.5, "avgPvs": 2.5, "bounceRate": 0.3,
    "payByrCnt": 10, "payAmt": 5000,
    "mobileUv": 120, "mobilePv": 300, "mobileShare": 0.6
  },

  "inquiry": { /* 询盘、旺旺分 */
    "statDate": "YYYY-MM-DD", "effectiveInQUsers": 8, "wangInQUsers": 8,
    "effectInQCnt": 8, "wangInQCnt": 6, "repeatRate": 0.25,
    "scorefh": 4.5, "scorehm": 4.2, "scorexy": 4.8
  },

  "trade": { /* 交易：金额/买家/订单/退款/客单价 */
    "statDate": "YYYY-MM-DD",
    "payAmt": 5000, "payByrCnt": 10, "payNewByrCnt": 3, "payOldByrCnt": 7,
    "payItemQty": 20, "payMordCnt": 15, "payRate": 0.05,
    "perByrAmt": 500,
    "crtOrdItmQty": 8, "crtByrCnt": 5, "crtOrdAmt": 800,
    "rfdSucAmt": 200, "refundRate": 0.04,
    "newBuyerAmt": 1500, "newBuyerShare": 0.30,
    "oldBuyerShare": 0.70, "oldBuyerPerAmt": 500
  },

  "tradeRecent7": {
    "dateRange": "YYYY-MM-DD|YYYY-MM-DD",
    "payAmt": 35000, "payByrCnt": 70,
    "payNewByrCnt": 20, "payOldByrCnt": 50,
    "payRate": 0.06, "perByrAmt": 500,
    "rfdSucAmt": 800, "refundRate": 0.023
  },

  "flowSourceRecent7": {
    "dateRange": "YYYY-MM-DD|YYYY-MM-DD",
    "sources": [
      {"name": "搜索", "myUv": 50, "goodUv": 249, "outerId": "search", "outerLevel": "1", "parentOuterId": ""},
      {"name": "自然搜索", "myUv": 30, "goodUv": 150, "outerId": "search_natural", "outerLevel": "2", "parentOuterId": "search"}
    ],
    "totalMyUv": 103, "totalGoodUv": 758
  },

  "keywordsRecent7": {
    "dateRange": "YYYY-MM-DD|YYYY-MM-DD",
    "keywords": [
      {"keyword": "...", "keywordRevealCnt": 82, "uv": 3, "pv": 6,
       "leadPayAmt": 0, "leadPayByrCnt": 0, "leadCrtByrCnt": 0,
       "clickRate": 0.036, "webClickRate": 0.032, "webPayRate": 0.01,
       "revealItem": 9, "bestOrder": 1, "avgOrder": 1,
       "webSearchIndex": 6014, "webSupplyAndDemandIndex": 120, "referencePrice": 25.00}
    ],
    "totalKeywordReveal": 1000, "totalLeadPayAmt": 0, "recordCount": 10
  }
}
```

### 3.2 工作台（work）

```json
{
  "_pageType": "work",

  "wwResponse": {"score": 95.0, "name": "3分钟响应率", "time": "06.17"},
  "wwSatisfaction": {"score": 98.0, "name": "咨询满意度"},

  "lgt48hGotRate": {"score": 98.5, "name": "48H揽收率"},
  "lgtFulfillRate": {"score": 98.5, "name": "履约率"},
  "lgtPlanAccRate": {"score": 76.5, "name": "物流时效达成率"},
  "lgt72hReceiveRate": {"score": 65.7, "name": "72H支签率"},
  "lgtFulfillDzRate": {"score": 100, "name": "定制品履约率"},
  "lgtRfdFhRate": {"score": 0, "name": "物流发货退款率"},

  "qualityRfdRate": {"score": 0, "name": "品质退款率"},
  "qualityBadRate": {"score": 0, "name": "商品品质差评率"},

  "nlhScore": {"score": "3.3", "name": "新灯塔分", "title": "差", "copyWriting": "落后78%同行"},
  "qualityScore": {"score": "5.0", "name": "商品体验", "proportionSuffix": "15%"},
  "refundScore": {"score": "1.7", "name": "售后体验", "proportionSuffix": "30%"},
  "lgtScore": {"score": "2.4", "name": "物流体验", "proportionSuffix": "35%"},
  "wwScore": {"score": "5.0", "name": "咨询体验", "proportionSuffix": "20%"},
  "starScore": {"score": "4.0", "name": "星级"},
  "cateLvl1Name": "宠物及园艺"
}
```

> JSON 字段保留了 1688 后端原始响应（`raw` / `allRaw` / `mobileRaw` / `rawUser` / `rawDiamond` 等），正常报告生成可忽略，使用上层解析字段即可。

---

## 四、工作流程

### 4.1 整体流程

**重要：登录流程仅在用户明确要求时执行。** 默认直接跳过登录，导航到工作台和生意参谋抓取数据。

```
初始化 → python3 scripts/fetch_data.py
       → python3 scripts/generate_report_v3.py
       → 模型填入「数据诊断 + 明日工作清单」
       → python3 scripts/push_feishu_post.py
```

### 4.2 步骤详解

执行前先 `ls $SKILL_DIR/scripts/`。

#### Step 1：一键抓取数据

```bash
cd $SKILL_DIR && python3 scripts/fetch_data.py /tmp/1688_raw_data.json
# Windows
cd $SKILL_DIR; .\python3.cmd scripts/fetch_data.py $env:TEMP/1688_raw_data.json
```

脚本自动：检查浏览器 → 导航工作台(5s) → 导航生意参谋(8s) → 获取插件数据 → 保存 JSON。退出码：`0`=成功，`1`=需登录（执行 4.3），`2`=采集失败。

> `fetch_data.py` 已内置跨平台支持：Linux 自动调 `bash start-browser.sh`，Windows 自动调 `powershell start-browser.ps1`。Windows 嵌入式 Python 通过 `python3.cmd` 调用，无系统环境变量。

#### Step 2：生成报告（v3）

```bash
python3 scripts/generate_report_v3.py /tmp/1688_raw_data.json
# Windows
cd $SKILL_DIR; .\python3.cmd scripts/generate_report_v3.py $env:TEMP/1688_raw_data.json
```

脚本生成 7 段数据表格 + 2 段占位符（`## ⚠数据诊断` 与 `## ✅明日工作清单`）到 `1688_daily_report_v3.md`。

**⚠️ 模型必须完成 Step 2.5：** 读取报告文件，**仅替换 `[模型生成]` 占位符**为诊断内容。

**🔒 绝对禁止修改前 7 段：** 模型只能修改 2 个占位符段落，**禁止修改/删减/重写/替换/添加/调整格式前 7 段任何数据**，前 7 段必须与脚本输出完全一致。审阅仅用于确认无空值/乱码。

**🔒 占位符段落也不得压缩。**

内容要求：
1. 数据异常点（≤150字）
2. 渠道优化方向
3. 关键词优化动作
4. 今日重点工作（3-5条）

**v3 报告结构：**

| 章节 | 数据来源 |
|------|----------|
| 标题 `# 📊1688运营日报｜YYYY-MM-DD` | 今日日期 |
| 头部：店铺/类目/层级排名 | sycm.companyName / rankTrend / category |
| 📦商品基础 | sycm.itemOverview |
| 📈流量数据 | sycm.flowStats + inquiry |
| 💰交易售后 | sycm.trade |
| 👥新老客结构 | sycm.trade（计算复购率、客单价） |
| ⭐新灯塔履约 | work |
| 🛤TOP8流量渠道 | sycm.flowSourceRecent7 |
| 🔎TOP10关键词 | sycm.keywordsRecent7 |
| ⚠数据诊断 | **模型生成** |
| ✅今日工作清单 | **模型生成** |

**⚠️ 关键规则：**
- **数据只能来自插件采集结果**，禁止自行调用 API 或猜测
- 插件未采集字段标注"—（插件未采集）"
- 报告生成后必须由模型审阅，确认无空值/乱码
- **🔒 模型只能修改 `## ⚠数据诊断` 与 `## ✅明日工作清单` 段落**
- **🔒 推送必须使用报告文件原文，一字不改**（禁止合并行、压缩格式、删换行、调整分隔符、改写）。模型只能决定推不推，不能决定推什么版本
- 返回给用户聊天的必须是完整的报告文件内容

#### Step 3：推送飞书（直接调飞书 open API，post+md 渲染表格）

**核心实现：`scripts/push_feishu_post.py`** —— 直接调飞书 `im/v1/messages` API 用 `msg_type: "post"` + `content.md` 标签，飞书原生支持 GFM 表格渲染。

**为什么不用 OpenClaw `message` 工具：** 1) OpenClaw `message` 对 Feishu 走 text 类型，不支持表格（渲染为 plaintext 代码块）；2) interactive card 跨端一致性差；3) 直接 API 更稳定，跨 PC/Mobile/iPad 渲染一致。

**推送命令：**

```bash
python3 scripts/push_feishu_post.py /path/to/1688_daily_report_v3.md
# Windows
cd $SKILL_DIR; .\python3.cmd scripts/push_feishu_post.py 1688_daily_report_v3.md

python3 scripts/push_feishu_post.py --check     # 仅验证 token
```

**凭证来源：** `scripts/env.ps1`/`env.sh` 的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_CHAT_ID`（`oc_` 开头）。CLI 第二参数可覆盖 chat_id：

```bash
python3 scripts/push_feishu_post.py report.md oc_xxxxxxxx
```

**Token 缓存：** 首次调用通过 `auth/v3/tenant_access_token/internal` 拿 token（有效期 2h），缓存到 `scripts/.feishu_token.json`，过期前 60s 自动续。**与 OpenClaw `channels.feishu` 独立**。

**🔒 推送铁律：**
1. 只读 `$SKILL_DIR/1688_daily_report_v3.md` 文件内容
2. 原样发送，**禁止合并行/压缩格式/删换行/调整分隔符/改写措辞**
3. 模型只能决定推送时机，不能决定推送版本
4. 超长先询问用户，禁止自行压缩
5. 只含文件原文，禁止附加任何额外文字

### 4.3 登录流程（v6：进程永不退出）

**⚠️ 登录必须通过脚本执行，禁止自行编写登录代码。**

**启动命令（单次启动，单进程长轮询）：**

```bash
cd $SKILL_DIR && python3 scripts/login.py           # Linux
cd $SKILL_DIR; .\python3.cmd scripts\login.py       # Windows
# 限时（默认无限）
cd $SKILL_DIR && python3 scripts/login.py --max-time 1800
```

**⚡ OpenClaw exec 参数：** `background=true, timeout=0或留空`。**错误示例：** `timeout=30, yieldMs=20000`（进程被立刻杀死）。

**⛔ v6 硬约束：**

1. **进程永不退出**：v6 起 `login.py` 内部循环 "等待 → 超时 → 自动 refresh → 再等待"，**除非登录成功或达到 `--max-time` 上限，绝不 sys.exit**。模型侧**只需 exec 一次 + 后续多次 poll**，无需循环 re-exec。
2. **`--wait-timeout` 默认 100s，硬区间 90s–110s**（脚本双向钳制）。1688 服务端二维码静态有效期约 120s，100±10s 是安全刷新窗口。
3. **`--max-time` 默认 0=无限**。仅在用户明确说"限时"时才设。

**输出标记（v6）：**

| 标记 | 含义 | 是否退出 |
|---|---|---|
| `[QR_UPDATED]` | 二维码已生成/刷新 | 否 |
| `[LOGIN_SUCCESS]` | 登录成功 | ✅ sys.exit(0) |
| `[TIMEOUT]` | 单次等待超时 | ❌ 脚本继续，自动 refresh |
| `[MAX_TIME_REACHED]` | 总等待超时 | ✅ sys.exit(1) |

---

#### 🟦 图片发送铁律（按当前渠道选择发送方式，不可互换）

**核心规则：** 二维码图片的发送方式**严格依赖当前对话的渠道**，两种方式**不可互换、不可降级**：

| 当前渠道 | 发送方式 | 原因 |
|---|---|---|
| **原生聊天**（`inbound_meta.channel != "feishu"`，如 Telegram / Discord / Signal / iMessage） | 最终回复用 `MEDIA:<绝对路径>` **单独一行**附图 | OpenClaw 会把 `MEDIA:` 解析为原生聊天的媒体附件 |
| **飞书渠道**（`inbound_meta.channel == "feishu"`，direct 或 group） | **必须**调 `message` 工具：`action=send`, `channel=feishu`, `target=<chat_id>`, `media=<绝对路径>` | 飞书渠道下 `MEDIA:` **不会**被渲染为图片附件（只显示为纯文本路径） |

**错误示例：**
- 在飞书对话里写 `MEDIA:C:\...\1688_qrcode.png` → 用户看不到图，只看到一串路径文本
- 在原生聊天调用 `message` 工具 → 该工具是飞书专用，原生渠道会失败

**同步推送到 FEISHU_CHAT_ID 群聊：**

| 场景 | 是否再调 message 推群聊 |
|---|---|
| 当前聊天 == FEISHU_CHAT_ID 群聊（用户直接在配置群发起登录） | **跳过**（避免同群双发） |
| 当前聊天 ≠ FEISHU_CHAT_ID（飞书 direct 非 FEISHU_CHAT_ID，或原生聊天） | **再调一次** message 推群聊，保证 FEISHU_CHAT_ID 配置群也能看到二维码 |

---

#### 🟦 持续 poll 铁律（必须同一回合内多次轮询）

**核心规则：** v6 脚本永不退出、模型侧**必须在同一回合内**反复 `process poll` 直到 `[LOGIN_SUCCESS]` 或 `[MAX_TIME_REACHED]`，**禁止**"发完图就觉得回合结束"。

**执行清单：**

1. `exec` 启动 `login.py`（`background=true`, `timeout=0或留空`）
2. `process poll` 检测到 `[QR_UPDATED]` → 按"图片发送铁律"发图（原生 `MEDIA:` / 飞书 `message`），按"群聊同步推送"决定是否再推 `FEISHU_CHAT_ID`
3. `process poll`（`timeout=30000`）→ 检查返回：
   - **新 `[QR_UPDATED]`**：回到第 2 步重新发图
   - **`[LOGIN_SUCCESS]`**：成功通知，按用户要求继续
   - **`[MAX_TIME_REACHED]`**：报告状态，问用户"续 / 重新发起"
   - **只有轮询心跳**（`等待登录中... Ns / 100s`）：继续 `process poll`，再等 30s
4. 重复第 3 步直到终止标记出现
5. **登录成功前禁止标 In Progress 完成、禁止说"已完成"/"我先等一下"**

**为什么必须同一回合内持续 poll：**
- v6 脚本永不退出，中途"等用户指令"会让用户必须发消息你才会继续轮询，但用户能做的就是等你——死锁
- 每个 `[QR_UPDATED]` 间隔最多 100s。如果不持续 poll，新二维码生成后没人发给用户，用户扫的就是失效码
- `process poll` 单次 timeout 最大 30s。一个回合内连续调多次即可覆盖（100s 需要 4 次 30s）

---

**⛔ 模型执行规则 v6（必须 100% 遵守）：**

```
┌─────────────────────────────────────────────────────────┐
│  模型登录监控（v6：单进程长轮询 + 渠道分流）             │
│                                                          │
│  1. exec login.py                                        │
│     （background=true，timeout=0 或留空）                │
│  2. process poll → 检测 [QR_UPDATED]                     │
│                                                          │
│     【图片发送铁律】                                      │
│     ├─ 当前渠道 != "feishu"（原生聊天）                  │
│     │   → 最终回复用 MEDIA:<绝对路径> 单独一行附图        │
│     └─ 当前渠道 == "feishu"（飞书聊天）                  │
│         → 调 message 工具发图（必须；禁止 MEDIA:）        │
│                                                          │
│     【群聊同步推送】                                      │
│     ├─ 当前聊天 == FEISHU_CHAT_ID → 跳过                 │
│     └─ 当前聊天 != FEISHU_CHAT_ID → message 推群聊        │
│                                                          │
│  3. process poll（30s/次）→ 检查                          │
│     ├─ 新 [QR_UPDATED]：回到第 2 步                       │
│     ├─ [LOGIN_SUCCESS]：成功通知，按要求继续             │
│     ├─ [MAX_TIME_REACHED]：报告状态，问用户下一步         │
│     └─ 只有心跳日志：继续 process poll（不要等用户）      │
│  4. 终止条件出现前，禁止标完成、禁止说"已完成"            │
└─────────────────────────────────────────────────────────┘
```

**⛔ 禁止行为清单（违反 → 流程无效）：**

| ❌ 禁止 | ✅ 应该 |
|---|---|
| 飞书渠道聊天用 `MEDIA:` 发图 | 飞书渠道**必须**用 `message` 工具显式发送；`MEDIA:` 在飞书渠道下不会渲染为图片附件，只显示为纯文本路径（**实测已确认**） |
| 原生聊天调用 `message` 工具 | 原生聊天只在最终回复用 `MEDIA:<绝对路径>` 单独一行附图；`message` 是飞书专用 |
| 只推当前聊天、漏推飞书群聊；或被问到才补推 | 同一回合检测到 `[QR_UPDATED]` 后连续两步：① 按渠道发当前聊天（飞书 `message` / 原生 `MEDIA:`），② 判断是否再 `message` 推 `FEISHU_CHAT_ID`（当前聊天 == `FEISHU_CHAT_ID` 时跳过） |
| 同一回合发完图就停下来等用户指令 | 同一回合内**反复** `process poll`（timeout=30000），直到 `[LOGIN_SUCCESS]` 或 `[MAX_TIME_REACHED]`，中途新 `[QR_UPDATED]` 必须立即重新发图 |
| 写"登录失败"、"请稍后再试"、"我先等一下" | 进程没退出就是还在等；只有进程退出码 = 1 才是 `[MAX_TIME_REACHED]`，那也只能"报告状态，问下一步" |
| 把二维码图片和文字提示合在同一回复、用 `**MEDIA:...**` 加粗 | 飞书渠道下图片走 `message` 工具附加（与文字消息分两条）；原生渠道下 `MEDIA:` 单独一行（必须先于任何文字） |
| `--wait-timeout` 设 < 90s 或 > 110s；`--max-time` 默认设上限 | 默认 100s / 0=无限；只在用户明确指示时调 |
| 登录成功前调 `create_goal status=complete`、说"已完成" | 在检测到 `[LOGIN_SUCCESS]` 之前，进程仍在运行，任务**未完成** |

---

**底层原理（为何这样设计）：**

- 进程**永不退出** + `[QR_UPDATED]` 多次触发 = 模型只需 poll 一次，"提前结束"在物理上不可能
- **渠道-发送方式铁律**：原生聊天用 `MEDIA:`（最终回复附图）；飞书渠道用 `message` 工具。这两种方式**不可互换**：`MEDIA:` 在飞书渠道显示为纯文本路径，不会渲染为图片附件（**实测已确认**）；`message` 工具是飞书专用通道，原生聊天用会失败
- **持续 poll 铁律**：v6 脚本永不退出，如果模型发完图就停，用户必须发消息你才会继续轮询，但用户能做的就是等——形成死锁。每个 `[QR_UPDATED]` 间隔最多 100s，必须**同一回合内**连续 `process poll`（≤30s/次）才能把新二维码及时发给用户，否则用户扫的永远是过期码
- **双发铁律**把"推送飞书群聊"和"推送当前聊天"绑成同一触发条件，模型无法遗漏

**脚本执行流程（v6 循环版）：**

```
首次准备：检查浏览器 → 清Cookie+导航+切换扫码登录+截码 → 输出首次 [QR_UPDATED]
主循环（永不退出）：
  等待 wait_timeout 秒（每秒检查 URL，跳 work.1688.com 即登录成功）
  登录成功 → [LOGIN_SUCCESS] → sys.exit(0)
  单次超时 → [TIMEOUT]（不退出）
  检查 max-time：超出 → [MAX_TIME_REACHED] → sys.exit(1)；未超 → refresh + 输出新 [QR_UPDATED] → 回到等待
```

**参数：**

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--output PATH` | `$SKILL_DIR/1688_qrcode.png` | 二维码输出路径 |
| `--wait-timeout N` | 100 | 单次超时秒数，**硬区间 90–110s**（1688 二维码静态有效期约 120s） |
| `--max-time M` | 0=无限 | 总等待超时秒数。0 表示永不退出 |
| `--refresh` | — | 刷新模式：跳过 Cookie 清除和导航 |

**⚠️ 为什么 wait_timeout 不能自由设：** 1688 二维码静态有效期约 120s。太大（>120s）→ 用户扫到失效码；太小（<60s）→ 频繁 reload + 增加风控概率。90–110s 留 10–30s 给"打开 App → 扫码 → 确认"链路。

---

## 五、定时任务

```json
{
  "job": {
    "name": "1688-daily-report-v3",
    "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
    "sessionTarget": "isolated",
    "payload": {
      "kind": "agentTurn",
      "message": "使用 1688-alibaba-data-fetcher skill 生成 v3 报告（generate_report_v3.py），填入数据诊断与明日工作清单，再用 push_feishu_post.py 推送到 env 里的 FEISHU_CHAT_ID。报告源数据默认 $env:TEMP/1688_raw_data.json（Windows）或 /tmp/1688_raw_data.json（Linux）。",
      "timeoutSeconds": 300
    }
  }
}
```

> v3 推送通过 agent 内部调 `push_feishu_post.py` 完成，`chat_id` 从 `scripts/env.ps1` 的 `FEISHU_CHAT_ID` 读取。禁止在 cron 任务中硬编码其他 chat_id。

---

## 六、故障排查

| 问题 | 解决方案 |
|------|----------|
| 插件数据为空 | 增加等待时间（5→10s）；刷新重试 |
| `chrome.runtime.sendMessage` 超时 | 检查 CDP targets 列表确认扩展 ID 存在 |
| CDP 端口不可用 | 检查 `ps aux | grep chrome`；端口被占用则手动处理（脚本不杀进程） |
| 插件未加载 | 确认用 Chromium（非 Chrome）；检查插件目录路径 |
| 登录页无二维码 | 切到"扫码登录"标签 |
| 二维码显示过期 | 刷新页面 + 重新截取 |
| **飞书推送失败** | 1) `push_feishu_post.py --check`；2) 查 env 凭证；3) `FEISHU_CHAT_ID` 以 `oc_` 开头；4) 应用已发布 + 有 `im:message:send_as_bot` 权限 |
| **飞书表格渲染为 plaintext** | 误用了 `message` 工具 text 通道。改用 `push_feishu_post.py`（msg_type=post） |
| Cookie 失效 | 重新扫码登录 |
| **登录流程 model 端"提前结束"** | 必须**同一回合内**持续 `process poll`（≤30s/次），直到 `[LOGIN_SUCCESS]` 或 `[MAX_TIME_REACHED]` |
| **登录流程 model 在飞书渠道用 `MEDIA:` 发图** | 飞书渠道下 `MEDIA:` 只显示为纯文本路径，不会渲染为图片附件。改用 `message` 工具显式发送 |

## 七、注意事项

1. **登录流程仅在用户明确要求时执行**
2. **⚠️ 推送前必须模型确认**：检查报告内容无 undefined/空值/乱码
3. **插件 content script 自动采集**：导航到目标页面后等待 5-8 秒即可获取数据
4. **扩展 ID 固定**：`ekmgnempbbamlmaolijdfjakeopniion`
5. **Cookie 有效期**：约 6 天，建议每 5-6 天重新扫码登录
6. **Chromium 必须**：Google Chrome 禁止 `--load-extension`
7. **飞书渠道下图片附件必须用 `message` 工具**：`action=send, channel=feishu, media=<绝对路径>` —— `MEDIA:` 在飞书渠道不会渲染为图片附件
8. **飞书推送通道（v3 默认）**：`scripts/push_feishu_post.py` 直接调飞书 `im/v1/messages` API 用 `post`+`md` 标签，正确渲染 markdown 表格。**不依赖** `message` 工具或 `lark-cli`
9. **凭证唯一来源**：`scripts/env.ps1`/`env.sh` 的 `FEISHU_APP_ID`/`FEISHU_APP_SECRET`/`FEISHU_CHAT_ID`。禁止硬编码其他值
10. **旧版脚本**：`generate_report_v2.py`（紧凑）、`generate_report.py`（v1）保留供参考
11. **报告源数据默认路径**：`$env:TEMP/1688_raw_data.json`（Windows）/ `/tmp/1688_raw_data.json`（Linux）
12. **登录流程必须在同一回合内反复轮询**：v6 脚本永不退出，模型必须连续 `process poll` 直到 `[LOGIN_SUCCESS]` 或 `[MAX_TIME_REACHED]`，中途发完图就停会死锁 + 用户扫到失效码
