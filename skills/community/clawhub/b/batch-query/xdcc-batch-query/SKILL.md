---
name: xdcc-batch-query
version: 2.0.0
display_name: 小递查查批量快递查询
display_name_en: Xdcc Batch Express Query
description: 小递查查（xdccy.com）批量快递物流查询技能，面向客户开箱即用。当用户需要注册小递查查账号并批量查询快递、或已注册后批量查物流/导出报表时使用。内置「无障碍注册引导」（自动拉起浏览器、页面分步横幅、自动填表，仅需客户完成短信验证码与滑块两步安全校验），注册后自动获取 API Key 并写入凭据，立即进入并发批量查询、聚合统计与多格式导出（JSON/CSV/TXT）。遇到无法自动解决的问题，统一给出会话内的自助排查步骤。
description_zh: 小递查查批量快递查询，面向客户闭环：注册引导（仅短信码+滑块需人工）→自动获取API Key→并发批量查询+聚合统计+CSV/JSON/TXT导出。无障碍引导、兜底排查。
description_en: Customer-ready batch express tracking for xdccy.com. Guided self-service onboarding (register → fetch API key → batch query) with accessible in-page instructions and official customer-service fallback.
agent_created: true
---

# 小递查查批量快递查询（客户版 · 完整闭环）

## 这个技能解决什么

让**零基础客户**也能在对话里完成：

> **注册小递查查账号 → 自动获取 API Key → 批量查询快递物流 → 导出报表**

全程只需客户在弹出的浏览器里做两件安全校验（短信验证码、滑块验证），其余由技能自动完成。
任何卡点都收敛为可执行的自助排查步骤，不会让客户卡死。

## 何时使用（触发词）

- "帮我注册小递查查并批量查快递" / "新客户批量查快递"
- "小递查查批量查询" / "批量查快递单号" / "查一批运单号"
- "把这批快递导成 Excel / CSV" / "生成快递查询报表"
- "统计这批件有多少签收了、多少超时了"
- 用户提供一批运单号，且当前无小递查查凭据

**不适用于**：下单寄件、运费计算、清关申报（需其他 API）。

## 核心能力

1. **无障碍注册引导**（`guided_register.py`）：自动打开浏览器、注入页面分步横幅、自动填手机号/密码；客户只需完成「短信验证码 + 滑块验证」两步；随后自动调 `GetUserApiKey` 取密钥并写入凭据文件。
2. **凭据自动映射**：`GetUserApiKey` 返回的 `PlatformID / UserID / UserApiKey` 自动映射为批量查询所需的 `PLATFORM_ID / MEMBER_ID / API_KEY`（已实测确认 `MemberID = UserID`）。
3. **并发批量查询**（`batch_query.py`）：默认并发 5（文档声明无频率限制），调用官方 API 基址下的 `/IsvApi/GetXdccTrackInfoV2` 与 `/UserInfo/GetUserApiKey`（基址见 `scripts/batch_query.py`、`scripts/get_user_apikey.py` 的常量，技能包内不做其他外链）。
4. **三种输入**：批量文件（每行 `NO` 或 `NO,TEL`）、内联单号（`--nos`）、手机号映射表 CSV（`--telmap`）。
5. **Tel 缺失预警**：按单号字母前缀识别快递公司（顺丰/中通/申通/圆通/韵达/百世/极兔/EMS），对 API 强制要求手机号后四位（Tel）却没提供的单号，查询前打印中文预警并给出补法，避免跑完一批全是 400 才发现。
   > 纯数字单号没有可靠前缀规律可依，不做推断，只由用户提供 Tel 或 `--tel` 统一兜底。
6. **聚合统计**：状态分布、超时单量、签收时效均值/峰值、快递公司分布、失败清单。
7. **多格式导出**：JSON / CSV（`utf-8-sig`，Excel 直开）/ 可读 TXT 报告。
8. **零三方依赖**：仅 Python 标准库（查询引擎）；注册引导依赖 Playwright（客户机缺失时提示安装）。

## 完整闭环工作流（Agent 编排）

```
客户说「我要批量查快递」/ 提供一批单号
        ↓
【第 1 步】检查凭据（~/.workbuddy/xdcc-credentials.env 是否存在且可用）
        ↓
   有凭据 ───────────────┐
        ↓ 无凭据          │
【第 2 步】注册引导        │
  引导客户给「手机号+密码」 │
  → 调 onboard.py 自动拉起浏览器引导注册
  → 客户完成 短信码 + 滑块
  → 自动 GetUserApiKey → 写凭据 → 试跑校验
        ↓                │
   凭据就绪 ◄─────────────┘
        ↓
【第 3 步】批量查询
  onboard.py 直接复用凭据跑 batch_query（或单独跑 batch_query.py）
        ↓
【第 4 步】聚合统计 + 导出 JSON/CSV/TXT + 用 present_files 呈现
```

### 操作要点（对 Agent）

1. **优先用 `onboard.py` 做闭环**：一条命令即可「确保凭据（缺则引导注册）→ 校验 → 批量查询」。
   ```bash
   # 客户首次使用（需客户提供手机号+密码，这是注册必需）
   python onboard.py --phone <客户手机号> --password <客户密码> --file 订单.txt --output 结果

   # 客户已有账号/凭据，仅查询
   python onboard.py --file 订单.txt --output 结果

   # 仅校验凭据是否可用
   python onboard.py --validate-only
   ```
2. **注册必须客户提供手机号+密码**：这两项是安全注册所需，技能无法代填（也不应代客户设置密码，存在合规风险）。用自然语言向客户索取即可。
3. **两步人工校验务必说清楚**：拉起浏览器后，明确告诉客户——「请点获取验证码、收短信填码、完成滑块、点注册，剩下的助手会自动完成」。页面顶部会有同款中文横幅引导。
4. **顺丰/中通必填手机号后四位**：缺 Tel 时 API 报 400。技能会在查询前自动预警缺 Tel 的单号（`find_missing_tel`），补法用 `--telmap`（推荐）或 `--tel` 或单号行内 `NO,TEL`。
5. **任何失败都要落到会话内兜底**：凭据校验失败、注册超时、接口 500 等，统一打印 `common.cs_hint()` 的三步自助排查（核对凭据键 → `--validate-only` 复核 → 报错原文发回会话）。技能包内不含任何外部联系渠道。

## 兜底与自助排查（会话内完成）

技能包内**不内置任何外部联系渠道**：不写第三方即时通讯账号、电子邮箱、电话、
外部站点地址，也不夹带任何推广。任何失败都收敛到 `common.cs_hint()` 的三步自助排查：

1. 核对凭据文件三个键是否齐全（`XDCC_PLATFORM_ID` / `XDCC_MEMBER_ID` / `XDCC_API_KEY`）
2. 单独执行 `onboard.py --validate-only` 复核当前凭据是否仍有效
3. 把报错原文发回会话，由助手带着上下文继续协助处理

> 若部署方需要接入自有支持入口，请自行扩展 `scripts/common.py` 的 `cs_hint()`，
> 不要把这些账号写回到本技能包内。

## 签名生成（遵循官方 §2.2.2）

```
原始RequestData(JSON) + APIKey → MD5(32位hex) → Base64(对hex串编码) → URL(UTF-8)编码 → DataSign
```
代码见 `scripts/batch_query.py:generate_data_sign()`。已用官方示例校验通过。

## 响应字段速查

| 分组 | 字段 | 用途 |
|---|---|---|
| 状态 | `State`, `StateDesc` | 3=已签收，其余按文本归类 |
| 时间 | `Pickup_Time`, `Dispatch_Time`, `SignFor_Time` | 揽收/派件/签收 |
| 城市/人员 | `Pickup_City`, `Delivery_City`, `Delivery_Courier(_Phone)` | 路线/派送员 |
| 时效(分) | `FirstIssue_TimeSpan` … `SignFor_TimeSpan`（6个） | 时效统计 |
| 超时 | `*_TimeOut`（7个，0/1） | 节点超时标记 |
| 轨迹 | `TraceList[]`（倒序）, `LastTrace`, `Count` | 最新轨迹 |

完整字段与状态码见 `references/api_reference.md`；客户上手见 `references/onboarding_guide.md`。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 全部成功 |
| 1 | 部分失败 / 新凭据校验未通过（已产出结果或已提示客服） |
| 2 | 参数错误（缺凭据且无手机号/密码 / 未解析到单号） |

## 资源

### scripts/
- `onboard.py` — **闭环编排器（首选）**：确保凭据（缺则引导注册）→ 校验 → 批量查询并导出。支持 `--phone/--password`（注册引导）、`--file/--nos/--telmap/--tel`（查询）、`--validate-only`。
- `guided_register.py` — 无障碍注册引导向导（人在环）：浏览器分步横幅 + 自动填表 + 轮询 token + GetUserApiKey + 写凭据 + 校验。Playwright 缺失时在**运行期**返回错误码 2（不中断进程），浏览器优先探测本机 Chrome（`CHROME_PATH` / PATH / 各系统通用路径），不做硬编码路径。
- `get_user_apikey.py` — 用 `auth` token 调 `GetUserApiKey` 取密钥（被引导向导复用）。
- `batch_query.py` — 批量查询引擎（并发/解析/Tel 预警/聚合/导出）。
- `common.py` — 共用：兜底排查文案 `cs_hint()`（会话内，零外部账号）、凭据映射 `map_apikey_to_creds()`、凭据读写（Unix 下收紧为 600）、`validate_track_creds()` 供 onboard 与引导向导共用一份校验实现。
- `selftest.py` — 纯静态自检（零网络），含缺 Tel 预警、CLI 友好报错，以及「技能包零外部联系渠道」合规扫描用例。
- `package.py` — 打包器：把本目录打成一层结构的 zip（自动排除 `.git` / `.workbuddy` / `__pycache__` 等开发期目录），默认输出 `dist/xdcc-batch-query-<version>.zip`。

### references/
- `api_reference.md` — 完整 API 参考（接口字段与状态码）。
- `onboarding_guide.md` — 客户分步上手指南 + FAQ + 自助排查清单。
- `SECURITY_AUDIT.md` — 安全审计与发布合规自查记录（含合规整改前后对照表）。

### 打包与验收

```bash
python scripts/selftest.py     # 先过自检（77 项，含合规扫描）
python scripts/package.py      # 产出 dist/xdcc-batch-query-2.0.0.zip
```

zip 内顶层为一层目录 `xdcc-batch-query/`，解压后即为完整技能包，可直接提审或部署。

---

**安全与合规提醒**
- PlatformID / APIKey 是商业凭据，写入 `~/.workbuddy/xdcc-credentials.env`，**勿硬编码进代码或公开文档**。
- Tel 仅用手机号后 4 位，勿主动索取完整手机号；注册密码由客户提供，技能不替客户设定密码。
- 注册的「短信验证码 + 滑块验证」是安全校验，必须由客户本人完成，技能不绕过。
- **发布合规**：本技能包不含任何第三方推广内容，也不内置外部联系渠道（即时通讯账号、电子邮箱、电话、外部站点地址一律不予写入）；第三方页面注入的仅是无品牌标识的纯操作提示条，不做满幅铺排。
