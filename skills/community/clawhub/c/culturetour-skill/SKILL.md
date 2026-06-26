---
name: culturetour-search
description: >-
  指导智能体检索文旅素材（数游神州 data0086.com）并走通「搜索 → 列表 → 预览(HLS/MP4) → 选择/购买 → Mock交易返回 → 视频下载到本地」。搜索请求默认 3条，最多 5 条（pageSize≤5），用户可要求更少；列表用表格展示（颜色徽章状态 + img + video），用户通过文本指令选择，支持多选与批量购买。用户可「购买 1,2」直接下单，无需二次确认；购买后 mock 交易响应（video_url 取自搜索结果的 fragmentUrl），自动下载视频到本地并输出文件路径。
  **输出格式自动适配**：桌面端/Web 客户端（ArkClaw、OpenClaw 等）默认输出 HTML 表格；**IM 手机应用**（飞书、微信、钉钉等）则输出 **Markdown 表格**，避免手机端直接显示 HTML 源码。
  所有嵌入媒体仅限 config.json 中 trusted_media_origins 声明的域名。环境变量 WENLV_API_ORIGIN、TRADE_API_BASE 可选覆盖 config.json 默认值（见 index.json env 声明）。
---

# 文旅素材搜索（API）

> ## 搜索流程说明（每次搜索都适用）
>
> **用户每次发起搜索时**（包括首次、后续、重新搜索、换关键词等），智能体都须按以下流程执行，**不得省略或合并为一次**：
>
> **Step 1. 计算两次调用的 pageSize（成片优先配比）**
>
> 设用户想要总条数为 `N`（默认 3，上限 5；用户可指定 1-5）：
> - `pageSize_finished = ceil(N / 2)` — 成片
> - `pageSize_material = floor(N / 2)` — 素材
>
> | 用户想要 `N` | 成片条数 | 素材条数 |
> |:--:|:--:|:--:|
> | 1 | 1 | 0 |
> | 2 | 1 | 1 |
> | 3 | 2 | 1 |
> | 4 | 2 | 2 |
> | 5 | 3 | 2 |
>
> **Step 2. 两次 POST 调用**（顺序执行）
>
> 1. **第一次**（成片）：请求体 `commodityCode = finished_commodity_code`，URL `pageSize = pageSize_finished`
> 2. **第二次**（素材）：请求体 `commodityCode = null`，URL `pageSize = pageSize_material`（若为 0 则跳过第二次）
>
> **Step 3. 兜底补齐**（配比失败时）
>
> 若成片实际返回 < `pageSize_finished`，用素材补齐到 `N` 条；反之亦然。目标是**总条数尽量等于 N**。
>
> **Step 4. 合并与判定类别**
>
> - 合并两次返回的 `datas`，按 `businessCode`/`id` 去重
> - **逐条以"返回数据本身"的 `commodityCode` 判定**（不是按哪次调用）：
>   - `item.commodityCode === finished_commodity_code` → `category = "成片"`
>   - 否则 → `category = "素材"`
>
> **Step 5. 展示与汇总（统计必须基于 category 字段，不是请求参数！）**
>
> ```python
> 成片条数 = sum(1 for item in results if item.category == "成片")
> 素材条数 = sum(1 for item in results if item.category == "素材")
> ```
>
> - **汇总行**（表格之前）：`📽 共找到 N 条资源：成片 **X** 条 ｜ 素材 **Y** 条`
>   - `X`、`Y` 必须与表格里实际带 `【成片】`/`【素材】` 徽章的行数**严格一致**
>   - 即使 `X=0` 或 `Y=0` 也要写出（说明搜过了但无结果）
> - **表格每行**：标题旁强制带 `【成片】` / `【素材】` 徽章（以 `item.category` 为准）
>
> **绝对禁止**：
> - ❌ 省略成片调用，只调一次接口就返回
> - ❌ 汇总行的数字与表格里实际徽章不一致（**最常见错误**：按"请求参数 commodityCode 是什么"算成片条数，而不是按"返回记录本身的 commodityCode"算）
> - ❌ 输出表格时省略类别徽章
>
> 此规则等同于主路径「步骤 1」，优先级最高。

> ## 购买流程说明（当前调试阶段）
>
> 本 Skill 处于调试阶段，真实交易 API 尚未上线。用户发出「购买」「下单」「买 N」等指令时，当前约定的完整响应流程为：
>
> 1. **构造 mock 交易响应**：`video_url` = 搜索结果中该素材的 `fragmentUrl`（预览地址）
> 2. **下载视频到本地**：调用 `bash scripts/download_video.sh "<video_url>" "downloads/{business_code}.mp4" [HLS|MP4]`，将视频保存到 `downloads/` 目录
> 3. **告知用户**：输出下载完成状态及本地文件路径
>
> 此流程由用户购买指令显式触发，搜索和预览阶段不执行任何下载。
> 真实交易 API 上线（`TRADE_API_BASE` 非空）后，步骤 1 将替换为真实下单请求，步骤 2-3 保持不变。

> **输出格式规范**
>
> 智能体应先判断客户端类型，再选择对应的输出格式：
>
> | 客户端类型 | 判定依据 | 输出格式 |
> |-----------|---------|---------|
> | **桌面端 / Web**（ArkClaw、OpenClaw、浏览器等） | 默认 | HTML 表格（`<table>`、`<img>`、`<video>` 等，仅限 `index.json` 中 `html_output.tags` 声明的标签） |
> | **IM 手机应用**（飞书、微信、钉钉、企业微信等） | 用户提到在飞书/微信/钉钉中使用，或上下文/系统信息表明客户端为 IM 应用 | Markdown 表格（`| col |` 语法，图片用 `![](url)`，链接用 `[text](url)`） |
>
> **桌面端 HTML 模式注意事项**：
> - 不要将 HTML 放在代码围栏内（围栏内的标签不会被渲染，只会显示源码）
> - 不要使用 `<input type="checkbox">`（静态 HTML 环境中无法交互）
> - 不要使用 `<button>`（无 JS 运行环境，无法绑定事件）
> - 所有媒体 URL（`<img src>`、`<video src>`）须通过下文「安全：媒体来源校验」
>
> **IM 手机端 Markdown 模式注意事项**：
> - 使用 Markdown 表格语法（`| col |`）
> - 缩略图用 `![封面](cover_url)` 或省略（手机屏幕窄时可不显示缩略图列）
> - 视频预览无法内嵌，统一用 `[▶ 预览](preview_url)` 链接
> - 不要输出 HTML 标签（手机 IM 不渲染 HTML，会直接显示标签源码）
>
> **通用规则**：
> - 选择操作通过**用户发送文本指令**完成（如「选 1,3」「购买」），智能体重新渲染带状态标记的表格
> - 注：本文档内的 HTML 模板用代码块展示以防文档渲染器误执行；智能体输出给用户时应去掉代码围栏。
> 详见下文「搜索结果展示」。

## 安全：媒体来源校验

本 Skill 的 HTML 输出包含 `<img>`、`<video>` 等标签，客户端会直接向 `src` 地址发起请求。为防止向不可信主机泄露用户 IP / 元数据，**智能体应在嵌入前校验媒体 URL 的来源**：

1. **可信来源列表**：[config.json](config.json) 的 **`trusted_media_origins`** 数组（默认仅包含 `api_origin`）。
2. **校验规则**：`<img src="...">`、`<video src="...">`、`<video poster="...">` 中的 URL **必须以 `trusted_media_origins` 中某一项开头**（协议 + 主机 + 端口完全匹配）。
3. **不符合时的处理**：
   - 若 `cover_url`（`breviaryPic`）不在可信列表 → 缩略图列显示「—」，不输出 `<img>`。
   - 若 `video_url`（`fragmentUrl`）不在可信列表 → 视频预览列**不输出 `<video>`**，改为纯文本「[需在浏览器中打开]」+ `preview_url` 超链接（`preview_url` 始终为同源站内页面）。
4. **API 响应中的 `breviaryPic`** 和 **`fragmentUrl`** 均为完整绝对 URL（指向 `wenzhou.data0086.com:9443`），须检查是否在 `trusted_media_origins` 中。
5. **`trusted_media_origins`** 见 [config.json](config.json)，当前包含 `https://www.data0086.com`、`https://test.data0086.com` 和 `https://wenzhou.data0086.com:9443`。

> 简言之：**只有 config 中声明的可信域名才允许直接嵌入媒体**，其余一律用 `preview_url` 超链接代替。

## 目标

让智能体用**自然语言**检索数游神州平台（data0086.com）上的文旅素材资源。每条结果必须**结构化保留**下游交易要用的字段，尤其是 **`fragmentUrl`（视频预览流）**、**`commodityCode`** 和 **`businessCode`**。

- 用 **解析后的搜索 URL** 直接 `POST` 请求，并按本文「输出映射」组装标准 JSON。

## 流程总览：先调试「预览 → 选择/购买」

**当前阶段（交易 API 未定时）**：智能体优先走通 **搜索 → 列表 → 预览 → 选择/购买 → Mock 交易返回 → 视频下载**。不在此阶段调用真实交易接口；购买后 **mock 交易返回数据**（`video_url` 复用搜索 API 的 `fragmentUrl`），然后 **将视频下载到本地** 并输出文件路径。

**真实交易 API**：`TRADE_API_BASE` / `trade_api_base` 配置为非空后将替换 mock 流程（见「交易 API」）。当前为空 → **使用 mock + 下载**。

智能体按顺序引导；上一步未就绪时不要进入下一步。用户可随时要求「重新搜索」。

### 主路径（调试优先）

| 步骤 | 行为要点 |
|------|----------|
| **1. 搜索（两次调用）** | 针对同一关键词，智能体**依次发起两次** `POST {api_origin}/ms-base/home/getList?pageNum=1&pageSize=3` 请求，合并结果：<br>**① 第 1 次**：请求体 `commodityCode` 填 [config.json](config.json) 的 **`finished_commodity_code`**（当前 `CommodityType-7bf0aa3057bc`）。<br>**② 第 2 次**：请求体 `commodityCode` 填 `null`。<br>**合并时按每条记录自身的 `commodityCode` 字段判定类别**：若 `item.commodityCode === finished_commodity_code` → `category = "成片"`，否则 → `category = "素材"`。展示时可在标题后加 `<small>` 徽章区分。`pageSize` 对**每次调用独立生效**，默认 `3`（最多 5）；用户要更少时按用户数量传。保留 P0/P1 字段。 |
| **2. 列出结果** | 用表格展示（HTML 或 Markdown，取决于客户端类型），不要把工具/API 返回的整段 JSON 当作对用户的主回复（见下「搜索结果展示」与「展示与 JSON」）：列 **状态｜标题｜缩略图｜视频预览｜详情**；首列用颜色徽章标记选中状态（非 checkbox）。表格**下方**附操作说明（见「选择与购买」）。 |
| **3. 预览** | 引导用户打开 **`preview_url`**（数游神州商品详情页 `/#/multimodal?businessCode=…`，统一处理视频播放）；可同时说明 **`stream_type`** 与原始 **`video_url`** 供技术核对。**预览仅用于选片，不等于已购原片**。 |
| **4. 选择 / 购买** | 支持两种操作模式，**无需额外确认步骤**：<br>**模式 A — 先选后买**：用户先发送选择指令（「选 1、3」「全选」），智能体重新渲染表格标记选中状态；之后用户发送「购买」或「下单」，**直接进入步骤 5**，不再要求二次确认。<br>**模式 B — 直接购买**：用户直接发送「购买 1,2」「下单 3」「买第1条」等**包含序号的购买指令**，智能体**一步完成**选中并**立即进入步骤 5**，跳过选择环节。<br>⚠️ **禁止**在用户发出购买指令后回复"接口未开放""暂不支持下单"等拒绝性文字——当前阶段购买指令的执行方式就是步骤 5 的 mock + 下载。<br>用户在选择阶段可追加/移除（「加上第2条」「去掉第3条」），智能体每次都重新渲染完整表格。 |
| **5. Mock 交易返回 + 视频下载（必须执行）** | 用户发出购买/下单指令后，智能体**必须立即执行以下操作**，不得跳过或以"接口未就绪"为由拒绝：<br>**A. 构造 mock 交易响应**：为每条选中素材生成 `{"code":0, "resData":{"video_url":"..."}}` ，其中 `video_url` = 该素材搜索结果的 `fragmentUrl`（预览地址）。<br>**B. 下载视频到本地**：调用 `bash scripts/download_video.sh "<video_url>" "<output_path>" [HLS\|MP4]` 将视频保存到 `downloads/` 目录，文件名为 `{business_code}.mp4`。<br>**C. 输出本地文件路径**：下载完成后向用户展示每条素材的 `local_path`。<br>详见「购买后输出」。 |

### 搜索结果展示 — 根据客户端类型选择输出格式

> 输出前应先判断客户端类型，选择对应格式。
>
> #### 桌面端 / Web 客户端（HTML 模式）
>
> 客户端（ArkClaw / OpenClaw）支持 HTML 渲染。展示搜索结果时，直接输出 HTML 标签（仅限 `index.json` 中 `html_output.tags` 声明的标签）。
>
> **注意事项（HTML 模式）：**
>
> - 不要使用 `<input type="checkbox">` 或 `<button>`（聊天气泡无 JS，无法交互）
> - 不要把 HTML 放在代码块里（代码块只会显示源码，不会渲染）
> - 所有 `<img src>` 和 `<video src>` 的 URL 须属于 `trusted_media_origins`（见「安全：媒体来源校验」）
>
> **正确做法**：在回复中直接书写 HTML 标签，不加代码围栏，让客户端渲染。选择状态用颜色徽章表示，用户通过发送文本指令选择/购买。
> （本文档内的模板为防止文档自身渲染 `<video>` 导致页面刷新，使用了代码块包裹——这仅限于文档展示，智能体输出时应去掉代码围栏。）
>
> #### IM 手机应用（Markdown 模式）
>
> 飞书、微信、钉钉等 IM 手机应用不渲染 HTML，会将标签作为纯文本显示。此时应使用 Markdown 表格。
>
> **注意事项（Markdown 模式）：**
>
> - 不要输出 HTML 标签（手机 IM 会直接显示标签源码）
> - 不要把表格放在代码围栏内
>
> **正确做法**：使用 Markdown 表格语法，缩略图用 `![](url)` 或省略，预览链接用 `[▶ 预览](preview_url)`。

#### 表格列定义（固定五列）

> **表格之前必须输出一行类别汇总**，格式示例：
> `🎬 共找到 **5** 条资源：成片 **2** 条 ｜ 素材 **3** 条`
> 即便成片为 0 也要明示 `成片 0 条`，以表明已执行两次搜索。

**HTML 模式（桌面端 / Web）：**

| 列名 | HTML 元素 | 内容 |
|------|---------------------|------|
| **状态** | `<span>` 带背景色 | 未选中：灰底序号 `<span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">1</span>`；选中：绿底 ✅ `<span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 1</span>` |
| **标题** | 纯文本 + `<small>` + **类别徽章** | title + **必标** 类别徽章：<br>成片 → `<small style="background:#f56c6c;color:#fff;padding:1px 6px;border-radius:3px;margin-left:4px;">成片</small>`<br>素材 → `<small style="background:#909399;color:#fff;padding:1px 6px;border-radius:3px;margin-left:4px;">素材</small>`<br>可附 `<br><small style="color:#999;">id</small>` |
| **缩略图** | `<img src="..." width="120">` | cover_url；无封面写「—」 |
| **视频预览** | `<video controls width="240" poster="..." src="...">` | src 用 video_url（fragmentUrl），poster 用 cover_url |
| **详情** | 纯文本 + `<a href="...">` | 分辨率/时长/大小，附 preview_url 超链接兜底 |

**Markdown 模式（IM 手机端）：**

| 列名 | Markdown 写法 | 内容 |
|------|--------------|------|
| **状态** | 纯文本序号或 ✅ | 未选中：`1`；选中：`✅ 1` |
| **标题** | 纯文本 + 类别前缀 | **必标** 类别：`【成片】title` 或 `【素材】title`（即使列表只有一类也要标） |
| **缩略图** | `![封面](cover_url)` 或省略 | 手机屏幕窄时可不显示此列 |
| **预览** | `[▶ 预览](preview_url)` | 链接到站内播放页 |
| **详情** | 纯文本 | 分辨率/时长/大小 |

### 选择与购买（表格下方操作区）

表格下方直接输出操作提示 HTML。

> **注意**：以下模板在本文档中用代码块展示，**防止文档渲染器误执行**。智能体输出给用户时应去掉代码围栏，直接输出 HTML。

> **核心规则：无需二次确认，购买 = mock 交易 + 下载视频**
> - 「购买 1,2」「下单 3」等**带序号的购买指令**→ 直接选中 → **立即执行 mock 交易返回 + 视频下载到本地 + 输出文件路径**，一步到位
> - 「选 1,3」→ 仅标记选中，渲染表格；之后用户说「购买」/「下单」→ **立即执行 mock + 下载**
> - **不要**在用户已发出购买指令后再要求「请确认」或「确认购买」
> - **不要**回复"接口未开放""暂不支持""请到官网购买"——当前阶段购买就是 mock + 下载

初始状态（无选中）— HTML 模式：
```html
<div style="background:#f6f8fa; border-left:4px solid #409eff; padding:10px 14px; margin:10px 0; border-radius:4px;">
<b>💡 操作说明</b><br>
· 回复「<b>购买 1、3</b>」或「<b>下单 2</b>」直接购买并下载视频到本地<br>
· 回复「选 1、3」先标记，之后回复「<b>购买</b>」一键下载<br>
· 回复「取消 3」取消已选
</div>
```

初始状态（无选中）— Markdown 模式（IM 手机端）：
```markdown
💡 **操作说明**
· 回复「**购买 1、3**」或「**下单 2**」直接购买并下载视频到本地
· 回复「选 1、3」先标记，之后回复「**购买**」一键下载
· 回复「取消 3」取消已选
```

有选中时 — HTML 模式：
```html
<div style="background:#f0f9eb; border-left:4px solid #67c23a; padding:10px 14px; margin:10px 0; border-radius:4px;">
✅ 已选 <b>N</b> 条素材 | 总时长 XXs | 总大小 <b>XXXM</b><br><br>
👉 回复「<b>购买</b>」或「<b>下单</b>」立即购买并下载到本地<br>
👉 回复序号可继续追加或取消选择
</div>
```

有选中时 — Markdown 模式（IM 手机端）：
```markdown
✅ 已选 **N** 条素材 | 总时长 XXs | 总大小 **XXXM**
👉 回复「**购买**」或「**下单**」立即购买并下载到本地
👉 回复序号可继续追加或取消选择
```

当用户发送选择指令后，智能体**重新渲染完整表格**：
- 选中行首列显示绿色 ✅ 徽章，行背景加 `style="background:#f0f9eb;"`
- 未选行首列显示灰色序号徽章
- 表格下方显示选中汇总 + 购买提示

### 展示与 JSON（必读）

- **对用户**：搜索列表的**默认形态**是表格（桌面端用 HTML 表格，IM 手机端用 Markdown 表格）。**禁止**用 JSON 代码块替代。
- **对程序/联调**：若用户明确说「给我原始 JSON」「导出结构」或已进入购买阶段，再按「标准结果 JSON 形状」或「购买后输出」给出 JSON。
- **条数**：URL 参数 **`pageSize` 默认传 `5`**（上限），用户要求更少时按用户数量传；若接口返回超出请求数量，只取前 N 条映射为表格。

### 完整输出模板（直接复制替换真实值）

智能体输出搜索结果时，**按照以下模板逐行输出 HTML**，将 `{变量}` 替换为真实值。

> **注意**：以下模板在本文档中用代码块展示，**防止文档渲染器误加载 `<video>`/`<img>` 导致页面刷新**。智能体输出给用户时应去掉代码围栏，直接输出 HTML 标签。

**初始状态（全部未选中）— HTML 模式：**

```html
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
<thead style="background:#f5f7fa;">
<tr><th>状态</th><th>标题</th><th>缩略图</th><th>视频预览</th><th>详情</th></tr>
</thead>
<tbody>
<tr>
<td><span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">1</span></td>
<td>{title}<br><small style="color:#999;">{id}</small></td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" poster="{cover_url}" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}<br><a href="{preview_url}">浏览器播放</a></td>
</tr>
<tr>
<td><span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;">2</span></td>
<td>{title}<br><small style="color:#999;">{id}</small></td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" poster="{cover_url}" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}<br><a href="{preview_url}">浏览器播放</a></td>
</tr>
</tbody>
</table>
<div style="background:#f6f8fa; border-left:4px solid #409eff; padding:10px 14px; margin:10px 0; border-radius:4px;">
<b>💡 操作说明</b><br>
· 回复「<b>购买 1、3</b>」或「<b>下单 2</b>」直接购买指定素材<br>
· 回复「选 1、3」先标记，之后回复「<b>购买</b>」一键下单
</div>
```

**初始状态（全部未选中）— Markdown 模式（IM 手机端）：**

```markdown
| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| 1 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |
| 2 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |

💡 **操作说明**
· 回复「**购买 1、3**」或「**下单 2**」直接购买指定素材
· 回复「选 1、3」先标记，之后回复「**购买**」一键下单
```

**选中第 1、2 条后（用户发送「选 1,2」后智能体重新渲染）— HTML 模式：**

```html
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
<thead style="background:#f5f7fa;">
<tr><th>状态</th><th>标题</th><th>缩略图</th><th>视频预览</th><th>详情</th></tr>
</thead>
<tbody>
<tr style="background:#f0f9eb;">
<td><span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 1</span></td>
<td>{title}</td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}</td>
</tr>
<tr style="background:#f0f9eb;">
<td><span style="background:#67c23a;color:#fff;padding:2px 8px;border-radius:4px;">✅ 2</span></td>
<td>{title}</td>
<td><img src="{cover_url}" width="120"></td>
<td><video controls width="240" src="{video_url}"></video></td>
<td>{resolution}<br>{duration_seconds}s / {file_size}</td>
</tr>
</tbody>
</table>
<div style="background:#f0f9eb; border-left:4px solid #67c23a; padding:10px 14px; margin:10px 0; border-radius:4px;">
✅ 已选 <b>2</b> 条素材 | 总时长 236.6s | 总大小 <b>273.9M</b><br><br>
👉 回复「<b>购买</b>」或「<b>下单</b>」立即下单<br>
👉 回复序号可追加或取消选择
</div>
```

**选中第 1、2 条后 — Markdown 模式（IM 手机端）：**

```markdown
| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| ✅ 1 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |
| ✅ 2 | {title} | [▶ 预览]({preview_url}) | {resolution} / {duration_seconds}s / {file_size} |

✅ 已选 **2** 条素材 | 总时长 236.6s | 总大小 **273.9M**
👉 回复「**购买**」或「**下单**」立即下单
👉 回复序号可追加或取消选择
```

**其中：**
- **`{preview_url}`** = `{api_origin}/#/multimodal?businessCode={businessCode}`（数游神州商品详情页）。
- **`{cover_url}`** = `breviaryPic`（已是完整 URL），**`{video_url}`** = `fragmentUrl`。嵌入前须校验来源属于 `trusted_media_origins`（见「安全：媒体来源校验」），不符合则不输出 `<img>` / `<video>`。

### ❌ 错误输出 vs ✅ 正确输出

**错误（HTML 模式下使用 checkbox / 代码围栏）：**
```
| □ | # | 标题 | 缩略图 | 预览 |
|---|---|------|--------|------|
| □ | 1 | 雁荡山素材 | [封面](url) | [预览 · HLS](url) |
```
或使用 `<input type="checkbox">`（渲染出来但无法勾选）、`<button>`（无法点击触发）。

**错误（IM 手机端输出 HTML 标签）：**
在飞书/微信中输出 `<table><tr><td>...` — 用户看到的是一堆 HTML 源码文本。

**✅ 正确 — HTML 模式（桌面端 / Web，无代码围栏）：**

智能体回复中应**直接包含**如下 HTML（不被 ``` 包裹）：

&lt;table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;"&gt;
&lt;tr&gt;
&lt;td&gt;&lt;span style="background:#e0e0e0;padding:2px 8px;border-radius:4px;"&gt;1&lt;/span&gt;&lt;/td&gt;
&lt;td&gt;雁荡山素材&lt;/td&gt;
&lt;td&gt;&lt;img src="https://…/cover.jpg" width="120"&gt;&lt;/td&gt;
&lt;td&gt;&lt;video controls width="240" src="https://…/index.m3u8"&gt;&lt;/video&gt;&lt;/td&gt;
&lt;td&gt;2560×1440&lt;br&gt;118.5s / 98.3M&lt;/td&gt;
&lt;/tr&gt;
&lt;/table&gt;

**✅ 正确 — Markdown 模式（IM 手机端）：**

| 状态 | 标题 | 预览 | 详情 |
|------|------|------|------|
| 1 | 雁荡山素材 | [▶ 预览](https://test.data0086.com/#/multimodal?businessCode=xxx) | 240.9s / ¥45 |

### `<video>` 标签用法

- **`src`** 必须用 **`video_url`**（即 `fragmentUrl`，实际媒体流），**不是** `preview_url`（商品详情页）。
- **来源校验**：嵌入前须确认 `video_url` 的来源在 `trusted_media_origins` 中（见「安全：媒体来源校验」）。不在列表中 → 不输出 `<video>`，改用 `preview_url` 超链接。
- **`poster`** 用 `cover_url`（封面图）。无封面时省略 `poster`。同样须通过来源校验。
- **MP4**：浏览器原生支持。
- **HLS（m3u8）**：Safari 原生支持；Chrome 依赖客户端 hls.js。若 `<video>` 无法播放，详情列的 `preview_url` 链接兜底。

### 预览与本地播放（能力边界）

**SKILL 无法在对话气泡内嵌入可执行的 HLS 播放器**（多数客户端会拦截脚本、iframe，且 OpenClaw / 飞书等需产品侧组件才能内嵌播放）。本 Skill 通过下列方式支持用户**在本机观看预览**：

1. **浏览器打开 `preview_url`（推荐）**  
   - 数游神州商品详情页已统一处理视频播放，用户直接点击表格中的「预览」链接即可。  
   - 若需在系统播放器中打开**原始流**，再使用 `video_url` + `stream_type`（见下文）。

2. **仅当无可用 HTML 播放页、且必须直接拉流时：再考虑 `video_url`**  
   - **`stream_type` 为 `MP4`**：多数浏览器可直接打开直链。  
   - **`stream_type` 为 `HLS`**：裸 m3u8 在 Chrome 常下载或无法播放；**Safari** 相对友好。  
   - 智能体应**优先推 `preview_url`**，避免向非技术用户丢裸 m3u8 链。

3. **本仓库脚本（本地用浏览器打开某 URL）**  
   - 路径：[scripts/open_preview.sh](scripts/open_preview.sh)（相对本 Skill 根目录）。  
   - 用法：优先 `bash scripts/open_preview.sh "<preview_url>" MP4`（播放页为 HTML 时按 HTTP 打开即可）；若需直接拉流，再传入 `video_url` 与 `HLS`/`MP4`。  
   - 适用于 Cursor / 终端；**飞书/OpenClaw** 仍以点击 **`preview_url`** 为主。

4. **可选：本机播放器（原始流）**  
   - **VLC** / **ffplay** 可粘贴 **`video_url`**；日常选片以 **`preview_url`** 为主。

飞书 / OpenClaw：**卡片按钮 URL** 与表格一致，指向 **`preview_url`**（即 `{api_origin}/#/multimodal?businessCode={businessCode}`）；若产品另有独立 H5 域名，以产品为准，但须能播同一条素材。

### 购买后输出（调试 / 联调）⚠️ 必须执行

> **强制规则**：用户发出「购买」「下单」等购买指令后，智能体**必须立即执行下述步骤 A + B**。**禁止**回复"交易接口未开放""暂不支持""请到官网购买"等拒绝性、引导性文字。当前阶段的"购买"就是 mock + 下载。

> **触发条件**：仅当用户显式发送「购买」「下单」「买第 N 条」等购买指令时触发，搜索、浏览、预览阶段不写入任何本地文件。

在未接真实交易 API 时，用户发出购买指令后智能体执行以下两步：

#### 步骤 A：构造 Mock 交易响应

为每条选中素材构造 **mock 交易返回数据**。核心字段 **`video_url`** 直接复用搜索 API 返回的 **`fragmentUrl`**（预览地址），模拟交易成功后服务端返回的视频下载链接。

**单条 mock 交易响应示例：**

```json
{
  "code": 0,
  "msg": "mock: 交易成功（模拟）",
  "resData": {
    "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe"
  }
}
```

> **说明**：`video_url` 的值 = 搜索结果中该素材的 `fragmentUrl`。当交易 API 真正上线后，此字段将由服务端返回真实的原片/授权下载地址。

**批量购买时，智能体为每条素材分别构造一个 mock 响应**，汇总后输出完整的购买结果 JSON：

```json
{
  "stage": "purchase_mock_completed",
  "items": [
    {
      "id": 459,
      "title": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
      "commodity_code": "CommodityType-e744a1044794",
      "business_code": "Commodity-20260406211854879",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
      "stream_type": "HLS",
      "duration_seconds": "240.9",
      "price": 45.0,
      "local_path": ""
    },
    {
      "id": 461,
      "title": "雁荡山-飞拉达-云雾多视频2-无人机航拍",
      "commodity_code": "CommodityType-948a39e64144",
      "business_code": "Commodity-20260406212609534",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/b68efe02182c436dbcf35f045b94ed30",
      "stream_type": "HLS",
      "duration_seconds": "30.5",
      "price": 45.0,
      "local_path": ""
    }
  ],
  "summary": {
    "total_items": 2,
    "total_duration_seconds": "271.4",
    "total_price": 90.0
  }
}
```

> `local_path` 在步骤 B 下载完成后填入。

#### 步骤 B：视频下载到本地

获得 mock 交易响应中的 `video_url` 后，智能体 **调用下载脚本将视频保存到本地**。

1. **下载目录**：`downloads/`（位于 Skill 根目录下；不存在时自动创建）。也可通过 [config.json](config.json) 的 `download_dir` 配置。
2. **文件命名**：`{business_code}.{ext}`（如 `Commodity-20260406211854879.mp4`）。扩展名由 `stream_type` 决定：MP4 → `.mp4`；HLS → `.mp4`（ffmpeg 转封装后输出）。
3. **下载命令**：调用 `bash scripts/download_video.sh "<video_url>" "<output_path>" [HLS|MP4]`。
   - **MP4**：直接用 `curl` 下载。
   - **HLS**：用 `ffmpeg` 下载 m3u8 并转封装为 MP4（需本机安装 ffmpeg）。
4. **输出**：下载完成后，将 `local_path` 填入结果 JSON 并**向用户输出文件路径**。

**下载完成后的最终输出示例：**

```json
{
  "stage": "download_completed",
  "items": [
    {
      "id": 459,
      "title": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
      "commodity_code": "CommodityType-e744a1044794",
      "business_code": "Commodity-20260406211854879",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
      "stream_type": "HLS",
      "local_path": "downloads/Commodity-20260406211854879.mp4",
      "duration_seconds": "240.9",
      "price": 45.0
    },
    {
      "id": 461,
      "title": "雁荡山-飞拉达-云雾多视频2-无人机航拍",
      "commodity_code": "CommodityType-948a39e64144",
      "business_code": "Commodity-20260406212609534",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/b68efe02182c436dbcf35f045b94ed30",
      "stream_type": "HLS",
      "local_path": "downloads/Commodity-20260406212609534.mp4",
      "duration_seconds": "30.5",
      "price": 45.0
    }
  ],
  "summary": {
    "total_items": 2,
    "total_duration_seconds": "271.4",
    "total_price": 90.0,
    "downloaded": 2,
    "failed": 0
  }
}
```

**向用户展示时**，在 JSON 之前/之后用自然语言说明：

> 已完成 2 条素材的模拟购买与下载：
> 1. 雁荡山-飞拉达雾天-一镜到底-无人机航拍 → `downloads/Commodity-20260406211854879.mp4`
> 2. 雁荡山-飞拉达-云雾多视频2-无人机航拍 → `downloads/Commodity-20260406212609534.mp4`

**错误处理**：若某条素材下载失败（网络错误、ffmpeg 未安装等），`local_path` 设为空字符串 `""`，`summary.failed` 计数 +1，并向用户说明失败原因与重试建议。

**单条选择**同样使用此结构（`items` 数组长度为 1），保持输出格式统一。

### 交易 API（预留，未来替换 mock）

以下仅在 **`TRADE_API_BASE` 或 `trade_api_base` 已配置为非空值** 且产品已约定路径/鉴权后执行。

1. **基址**：环境变量 **`TRADE_API_BASE`** 优先；否则 [config.json](config.json) 的 **`trade_api_base`** 非空字符串。
2. **调用**：用已锁定资源的 `id`、`commodityCode`、`businessCode` 按产品约定发起请求；鉴权勿泄露到对话。
3. **接入后替换 mock**：交易 API 上线后，步骤 A 的 mock 响应将被真实接口响应替换；`video_url` 以服务端返回为准。步骤 B 的下载逻辑保持不变。

> **当前状态**：`trade_api_base` 为空 → **不调用真实交易 API**，但**必须执行 mock + 下载流程**（见上文「购买后输出」）。绝不能因为交易 API 未就绪就拒绝用户的购买指令。

## API 基址配置（可更换）

**单一默认值**：与本 Skill 同目录的 [config.json](config.json)（`api_origin` + `search_path`）。

**解析规则**：

1. 若存在环境变量 **`WENLV_API_ORIGIN`**（仅站点根，如 `https://test.data0086.com`），则以其为 `api_origin`。
2. 否则使用 `config.json` 中的 `api_origin`。
3. `search_url` = `api_origin`（去掉末尾 `/`）+ `search_path`（默认 `/ms-base/home/getList`）+ `?pageNum={pageNum}&pageSize={pageSize}`。

| 项目 | 说明 |
|------|------|
| 基址 | `{api_origin}`，当前值见 [config.json](config.json)（`https://test.data0086.com`） |
| 搜索 | `POST {api_origin}/ms-base/home/getList?pageNum=1&pageSize=5` |
| 鉴权 | 无（公开接口，`token` 头可为空） |
| Content-Type | `application/json` |

换环境时：改 **config.json** 或部署侧设置 **`WENLV_API_ORIGIN`** 即可，无需改 Skill 正文中的长 URL。**交易**相关另设 **`TRADE_API_BASE`** 或 `config.json` 的 **`trade_api_base`**（非空时生效）。

### 详情页地址（用户点击「预览」）⚠️ 拼接规则

统一使用数游神州前端的商品详情页（与原始 `fragmentUrl` 区分）。

**拼接公式（唯一正确形式）：**

```text
preview_url = {api_origin} + {detail_path} + "?businessCode=" + {businessCode}
```

- **`api_origin`**：`WENLV_API_ORIGIN` 或 `config.json` 的 `api_origin`（当前 `https://test.data0086.com`，**无**末尾 `/`）。
- **`detail_path`**：默认 **`/#/multimodal`**（见 [config.json](config.json) 的 `detail_path`）。
- **`businessCode`**：搜索结果中每条素材的 `businessCode` 字段。

**✅ 正确格式：**
```text
https://test.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879
```

**❌ 错误格式 —— 不要用 `fragmentUrl` 当预览链接：**
```text
https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe
```

**表格「预览」列**、飞书卡片按钮、OpenClaw 内链均应使用 **`preview_url`**（商品详情页）。**`video_url`（fragmentUrl）仍须保留**在结构化结果中，供交易、调试与核对原始流。

### 播放页与裸流（必读：避免一点就下载 m3u8）

- **`video_url`（`fragmentUrl`）** 指向的是 **媒体流**（常见为 HLS 预览地址），**不是**给用户点的「网页预览」。在 Markdown 里若写成 `[预览](video_url)`，浏览器对 **HLS** 往往会 **下载 m3u8** 或无法内联播放。**禁止**将 `video_url` 作为表格「预览」列或卡片按钮的主链接。
- **`preview_url`** 对应数游神州的**商品详情页**（SPA 页面，内含视频播放器），用户点击后在**浏览器页面里播放**，而不是下载清单文件。
- **映射**：`preview_url` **一律只由** `{api_origin}{detail_path}?businessCode={businessCode}` **按上文公式拼接**（见 [config.json](config.json)），**不得**把 `fragmentUrl` 填进 `preview_url`，也不得用 `video_url` 顶替。

### 请求 URL 参数

分页通过 **URL query** 传递：

| 参数 | 必填 | 说明 |
|------|------|------|
| `pageNum` | 否 | 页码，默认 1 |
| `pageSize` | 否 | 每页条数，接口默认 18；**智能体侧默认传 `5`**（上限），用户要求更少时按用户数量传（如 1、2、3） |

### 请求体

```json
{
  "commodityCode": null,
  "sceneType": "",
  "tradeType": "",
  "search": "雁荡山飞拉达",
  "city": "330300"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `search` | 是 | 关键词，支持中文自然语言 |
| `city` | 否 | 城市行政区划代码，默认 `"330300"`（温州） |
| `commodityCode` | 否 | 按商品编码精确筛选。本 Skill 通过此字段区分「成片 / 素材」两类资源（见下） |
| `sceneType` | 否 | 场景类型筛选，如 `"慢直播"`，默认 `""` |
| `tradeType` | 否 | 交易类型筛选，如 `"cash"`，默认 `""` |

### 两次搜索：成片 + 素材

同一关键词下，本 Skill **依次发起两次搜索**，并按"成片优先 50:50"配比分配条数：

**pageSize 分配（用户想要总数 N，默认 3，上限 5）**：

| 顺序 | 请求 `commodityCode` | URL `pageSize` |
|:----|:--------------------|:--------------|
| **第 1 次（成片）** | [config.json](config.json) 的 `finished_commodity_code`（当前 `CommodityType-7bf0aa3057bc`） | `ceil(N / 2)` |
| **第 2 次（素材）** | `null` | `floor(N / 2)`（为 0 则跳过） |

配比参考表（N=1~5）：

| N | 成片 | 素材 |
|:-:|:---:|:---:|
| 1 | 1 | 0 |
| 2 | 1 | 1 |
| 3 | **2** | **1** |
| 4 | 2 | 2 |
| 5 | **3** | **2** |

**兜底补齐**：某一类返回不足时（如成片只返回 1 条而期望 2 条），用另一类补齐，总条数尽量达到 `N`。

**类别判定规则（核心）**：

**以返回的每条记录自身的 `commodityCode` 字段为准**，而不是按哪一次调用：

```text
if item.commodityCode === finished_commodity_code:
    item.category = "成片"
else:
    item.category = "素材"
```

> 这样即便两次调用返回数据有重复或交叉，最终每条记录的类别依然由其自身 `commodityCode` 决定，去重与标记逻辑一致。

**合并策略**：

1. 两次调用**按配比表分配 `pageSize`**（不是各自独立的 N）。
2. 合并两次返回的 `resData.datas`，按 `businessCode` 或 `id` **去重**（避免两次调用返回同一条记录时重复展示）。
3. 按上述判定规则为每条记录打 `category` 标签。
4. 排序：**成片在前、素材在后**；同类内部保留接口返回顺序。
5. 若某一类无数据，用另一类兜底补齐到 `N` 条；两类都无数据时，向用户说明"未找到相关资源"。

**展示要求（强制）**：

1. **汇总行（必须，统计口径以 `category` 字段为准）**：
   - 格式示例：`📽 共找到 5 条资源：**成片 3 条** | **素材 2 条**`
   - 即使某类为 0 也要写出（如 `📽 共找到 3 条资源：**成片 0 条** | **素材 3 条**`），让用户知道两次搜索确实都执行过。
   - ⚠️ **统计算法**：`成片条数 = 表格里 category == "成片" 的行数`、`素材条数 = 表格里 category == "素材" 的行数`；**不要**按"请求参数里 commodityCode 是什么"来算，以免出现"请求成片 3 条但返回的有 1 条实际是素材"时汇总错位。
   - **自检**：汇总行的 X 和 Y 必须等于表格里实际打 `【成片】`/`【素材】` 徽章的行数，加起来 = 总条数。
2. **类别徽章（必须，每行都标）**：
   - HTML 模式：标题旁追加 `<small style="background:#f56c6c;color:#fff;padding:1px 6px;border-radius:3px;margin-left:4px;">成片</small>` 或 `<small style="background:#909399;color:#fff;padding:1px 6px;border-radius:3px;margin-left:4px;">素材</small>`
   - Markdown 模式：标题前加 `【成片】` 或 `【素材】` 文本前缀
   - **不允许**只在混合类型时才标注；即使全部是同一类别也要每行标出。

**`finished_commodity_code` 可配置**：

- 修改 [config.json](config.json) 的 `finished_commodity_code` 即可调整成片归类的商品编码，无需改 Skill 正文。
- 值为空字符串或未配置时，跳过第 1 次搜索，仅按「素材」单次搜索——此时所有返回记录都标记为 `category: "素材"`。

### 响应约定

- 业务成功：`code === 0`，列表在 `resData.datas`，总数 `resData.total`。
- HTTP 非 2xx 或 `code !== 0`：向用户说明错误，勿伪造结果。

更完整的原始字段说明见 [references/api_reference.md](references/api_reference.md)。标准接口规范（含交易下单）见 [api.md](api.md)。

## 字段优先级

### P0 — 核心（交易直连，缺一不可）

| 来源字段 | 输出键名 | 说明 |
|----------|-------------------------|------|
| `id` | `id` | 素材唯一 ID（数字） |
| `commodityName` | `title` | 标题 |
| `fragmentUrl` | `video_url` | **原始预览流**（HLS），交易/核对用，**表格「预览」列不用作主链** |
| `commodityCode` | `commodity_code` | 商品编码，**交易下单必需** |
| `businessCode` | `business_code` | 业务编码，**交易下单必需**，也用于详情页 URL |

**派生（必选，用于展示与点击）**  

| 派生规则 | 输出键名 | 说明 |
|----------|----------|------|
| `{api_origin}{detail_path}?businessCode={businessCode}` | `preview_url` | **表格「预览」列、卡片按钮**统一用此链接（商品详情页）；`detail_path` 默认 `/#/multimodal`，见 [config.json](config.json) |

同时必须输出 **`stream_type`**（由 `video_url` / fragmentUrl 判定）：

- URL 含路径片段 **`/hls/`** → `"HLS"`（需 HLS 播放器，如 hls.js）
- URL **以 `.mp4` 结尾** → `"MP4"`（浏览器可直接播）
- 若 `fragmentUrl` 为空：不要编造 `video_url`；可省略 `stream_type` 或标为无法判定（勿写假链接）

### P1 — 重要（展示与交易辅助）

| 来源 | 输出键名 |
|------|----------|
| `explain` | `description`（HTML 格式，包含清晰度/格式等信息） |
| `fragmentTime` | `duration_seconds`（建议保留一位小数，字符串或数字均可） |
| `price` | `price`（元） |
| `breviaryPic` | `cover_url`：已是完整 URL，嵌入前须属于 `trusted_media_origins` |
| `sceneType` | `scene_type`（逗号分隔的场景类型） |
| `tag`（JSON.parse） | `tags`：逗号分隔或数组 |
| `createUser` | `merchant`（商家名称） |

### P2 — 辅助（可选）

`videoProductCode`、`contactName`、`contactPhone`、`merchantBusinessCode`、`priceJson`、`location` 等，在用户需要排查或对接数据源时再输出。

## 标准结果 JSON 形状（解析/转发用）

智能体整理输出时，每条结果建议符合：

```json
{
  "total": 185,
  "pageNum": 1,
  "pageSize": 5,
  "results": [
    {
      "#": "1",
      "id": 459,
      "title": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
      "commodity_code": "CommodityType-e744a1044794",
      "business_code": "Commodity-20260406211854879",
      "preview_url": "https://test.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879",
      "video_url": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
      "stream_type": "HLS",
      "duration_seconds": "240.9",
      "price": 45.0,
      "cover_url": "https://wenzhou.data0086.com:9443/res/covers/77758f136a4648888d1acd615ec24dbe.jpg",
      "scene_type": "慢直播,创作素材,无人机航拍",
      "tags": "视频创作, 无人机航拍",
      "merchant": "温州鼎诚体育发展有限公司"
    }
  ]
}
```

## curl 示例

**默认站点根须与 [config.json](config.json) 中 `api_origin` 保持一致**（换域名时改 config 并同步下面默认值，或只用 `export`）。

```bash
# 环境变量优先；未设置时读取 config.json 的 api_origin（当前为 https://test.data0086.com）
ORIGIN="${WENLV_API_ORIGIN:-https://test.data0086.com}"
FINISHED_CODE="CommodityType-7bf0aa3057bc"  # config.json finished_commodity_code

# 第 1 次：成片
curl -sS "${ORIGIN}/ms-base/home/getList?pageNum=1&pageSize=5" \
  -H 'Content-Type: application/json' \
  -H "Origin: ${ORIGIN}" \
  -H "Referer: ${ORIGIN}/" \
  -H 'token;' \
  --data-raw "{\"commodityCode\":\"${FINISHED_CODE}\",\"sceneType\":\"\",\"tradeType\":\"\",\"search\":\"雁荡山\",\"city\":\"330300\"}"

# 第 2 次：素材
curl -sS "${ORIGIN}/ms-base/home/getList?pageNum=1&pageSize=5" \
  -H 'Content-Type: application/json' \
  -H "Origin: ${ORIGIN}" \
  -H "Referer: ${ORIGIN}/" \
  -H 'token;' \
  --data-raw '{"commodityCode":null,"sceneType":"","tradeType":"","search":"雁荡山","city":"330300"}'
```

合并两次返回的 `resData.datas`（按 `businessCode`/`id` 去重），然后对每条记录按其自身的 `commodityCode` 判定：`commodityCode === finished_commodity_code` → `category = "成片"`，否则 → `category = "素材"`。最终输出 `results` 数组（成片在前、素材在后）。

## 智能体行为要点

1. **须同时保留 `preview_url`（详情列超链接兜底）与 `video_url`（`<video>` 播放源）**；**列表展示须用五列表格：状态（颜色徽章）｜标题｜缩略图｜视频预览｜详情**（见「搜索结果展示」）。桌面端用 HTML 表格，IM 手机端用 Markdown 表格。**不要**使用 `<input>`、`<button>` 等需要 JS 交互的元素。
2. **面向用户的列表**：桌面端以 **HTML 表格** 为主（含颜色徽章状态、`<img>`、`<video>` 元素），IM 手机端以 **Markdown 表格** 为主；结构化字段在表格列中体现。**不要**用整段 JSON 代替表格。仅在用户索要导出、或购买后的约定 JSON 块中再输出 JSON。
3. 分页：默认只拉第 1 页且 **`pageSize` 默认 5（上限）**，用户要求更少时按用户数量传；用户要「更多」时递增 `pageNum`，注意 `total` 边界。**跨页选择**：翻页时保留已选中条目；若用户在第 1 页选了第 1、3 条，翻到第 2 页后再选第 2 条，最终选中列表包含累计选中的所有条目。
4. **两次搜索 + 成片优先配比（每次搜索都必须执行，无例外）**：**不管是用户第 1 次搜索还是第 N 次搜索、同一关键词还是换关键词**，智能体对每一次搜索都**顺序**发起两次 POST，按 **50:50 成片优先** 配比分配 `pageSize`：
   - 成片：`commodityCode = config.finished_commodity_code`，`pageSize = ceil(N / 2)`
   - 素材：`commodityCode = null`，`pageSize = floor(N / 2)`
   - 示例：N=3 → 成片 2 条 + 素材 1 条；N=5 → 成片 3 条 + 素材 2 条
   - **禁止**因为"已经搜过""连续搜索""结果相似"等理由跳过成片那次调用
   - 合并两次返回的 `datas`（按 `businessCode`/`id` 去重），按每条记录自身的 `commodityCode` 判定 `category`；某类不足时用另一类兜底补齐到 N 条
   - **展示时强制输出**：(a) 汇总行 `📽 共找到 N 条资源：成片 X 条 | 素材 Y 条`，`X`/`Y` 必须按 `category` 字段统计而非请求参数，即便 `X=0` 也要写；(b) 每行标题带 `【成片】`/`【素材】` 徽章
   - `finished_commodity_code` 为空时才可跳过第一次调用，汇总行写明 `未配置 finished_commodity_code，仅搜素材`
   - 详见「两次搜索：成片 + 素材」
5. **预览与成单分离**：用户点击的预览必须是 **`preview_url`（商品详情页）**，**不要**把 **`video_url`（HLS 流）** 做成主链接以免下载或无法播放。预览仅用于选片。**当前调试阶段**：用户发出购买指令后，智能体**必须执行 mock 交易 + 视频下载**（步骤 5），不得以"接口未就绪"为由拒绝或引导用户去官网手动购买。
6. **交易安全**（启用交易 API 后）：不在对话中输出完整密钥；失败时返回接口错误摘要，不猜测成功。
7. **多选与购买（无需二次确认）**：支持两种下单方式：**① 直接购买**——用户发送「购买 1,3」「下单 2」等带序号的购买指令，智能体一步完成选中 + mock 交易 + 视频下载；**② 先选后买**——用户先「选 1,3」标记，再发送「购买」/「下单」直接执行 mock 交易 + 下载，**不再要求二次确认**。选择过程中用户可随时追加（「加上第2条」）或移除（「取消 3」），智能体每次都**重新渲染完整表格**，用绿色/灰色徽章标记选中状态。
8. **Mock 交易与视频下载**：购买确认后，智能体构造 mock 交易响应（`video_url` = 搜索结果的 `fragmentUrl`），然后调用 `scripts/download_video.sh` 将视频下载到 `downloads/` 目录（HLS 用 ffmpeg 转 MP4，MP4 用 curl 直接下载），最终**向用户输出每条素材的本地文件路径**。详见「购买后输出」。
9. **交互约束**：聊天气泡是静态 HTML（无 JavaScript），**禁止**使用 `<input>`、`<button>`、`<form>` 等需要 JS 交互的元素。所有用户操作通过**发送文本消息**完成，智能体解析后重新渲染表格。
10. **客户端适配**：智能体应根据客户端类型选择输出格式（HTML 或 Markdown）。判定方式见文首「输出格式规范」。若无法确定客户端类型，**默认使用 HTML 模式**；当用户反馈看到 HTML 源码时，切换为 Markdown 模式。

具体包名与发布流程以实际 npm 包为准；本 Skill 约束 **行为、配置解析顺序、API 路径与输出字段**。
