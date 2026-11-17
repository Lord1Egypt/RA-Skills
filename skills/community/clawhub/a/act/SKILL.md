# act — 活动发现与创建

> 通用 Agent SKILL · v2.2.0 · MCP Tool
>
> 安装后 Agent 可搜索活动、查看详情、创建活动、查询活动行程。
>
> **MCP 后端：** `https://mcp.fore.vip` · **区域：** 深圳 (CN-SZ)

---

## 功能矩阵

| 工具 | 端点 | 鉴权 | 说明 |
|------|------|------|------|
| `search_activities` | `POST /act/search` | 无 | 搜索活动：距离/热度双模式 |
| `get_activity_detail` | `POST /act/detail` | 无 | 查详情 + 浏览量自增 |
| `create_activity` | `POST /act/create` | `X-API-Key` | 创建新活动 |
| `list_activity_schedules` | `POST /act/schedules` | 无 | 按活动 ID 查行程列表 |

## 安装

```bash
npx skills add fore-vip/act
```

---

## 模式 1：原子级交互创建（多轮收集→单次调用）

> 用户说"帮我创建一个活动"时触发。逐轮收集所有必填信息，确认后才调用 MCP。

### 必填字段（必须逐项确认）

1. **API Key** — 第一件事就问。不存不记，每轮创建都重问。
   - 问："请提供活动创建 API Key"
   - 校验：返回 403 提示用户 key 无效

2. **封面图片** — 第二件事。
   - 问："请发送一张活动封面图片，或提供封面图片链接"
   - 用户发图片 → 用图片链接作为 cover URL
   - 用户发链接 → 直接用作 cover URL
   - 没有图片 → 必须拒绝创建，不能跳过

3. **活动主题** — 第三件。
   - 问："活动主题/名称是什么？（例：周末梧桐山徒步）"
   - 校验 ≤500 字
   - 同时确认标签："要不要加几个标签？比如 [徒步, 周末, 户外]"

4. **地址** — 第四件。
   - 问："活动地址在哪里？（例：深圳梧桐山国家森林公园）"
   - 校验 ≤128 字

5. **经纬坐标** — 第五件。自动从地址解析，不额外问用户。
   - 拿到地址后，调用 `web_search` 搜索"{地址} 经纬度"获取坐标
   - 或使用内置地理知识推断深圳市范围内坐标
   - 如果解析失败：告知用户"未能自动解析地址坐标，请提供经纬度（如：22.543, 114.058）"
   - 解析成功：展示坐标并请用户确认"用这个坐标可以吗？(22.543, 114.058)"

6. **开始/结束时间** — 第六件。
   - 问："活动什么时候开始和结束？"
   - 接受自然语言："周六上午9点"、"7月1日"、"下周五晚上7点到10点"
   - 转换为 Unix ms 时间戳
   - 如果不确定结束时间：设为 null（不限）

### 原子级调用

所有字段收集完毕后，总结确认：

```
确认创建以下活动：
- 主题：周末梧桐山徒步
- 地址：深圳梧桐山国家森林公园
- 坐标：22.581, 114.196
- 封面：[展示封面图片]
- 标签：徒步, 周末, 户外
- 时间：2026-06-20 09:00 开始，不限结束
- 人数：不限

确认创建？回复"是"来执行。
```

用户确认后，**只调一次** `create_activity`：

```js
create_activity({
  content: "周末梧桐山徒步",
  address: "深圳梧桐山国家森林公园",
  cover: "https://...",
  tags: ["徒步", "周末", "户外"],
  latitude: 22.581,
  longitude: 114.196,
  start_time: 1750352400000,
  max_participants: 0
})
```

**创建成功后展示：**
- ✅ 主题 + 返回链接 `url`
- 封面图片（如有）
- 地图位置（如有坐标）
- 时间范围

**创建失败处理：**
- 403 → "API Key 无效，请重新提供"
- -1 → 告知哪个字段有什么问题
- -3 → "封面图片下载失败，请换一张"

---

## 模式 2：自动化批量创建（搜索→生成→循环调用）

> 用户说"帮我搜最近深圳有什么大型活动并发布"、"批量创建活动" 等触发。

### 执行流程（不可跳过任何步骤）

#### Step 1：确认 API Key

```
请提供活动创建 API Key（用于批量创建）。
```

返回 403 则中止。

#### Step 2：搜索未来大型活动

调用 `web_search` 搜索未来 30 天内深圳的大型活动：

```
搜索关键词（分开调 3 次，一次一个维度）：
1. "深圳 2026年7月 大型活动 展会 音乐节"
2. "深圳 周末活动 马拉松 市集 展览 06月 07月"
3. "深圳 公益 志愿者 社区活动 6月 7月"
```

从搜索结果中提取：
- 活动名称/主题
- 地址
- 时间（开始+结束）
- 是否适合作为活动记录

至少找到 3 个候选活动。**只创建真实存在、信息明确的活动，禁止编造。**

#### Step 3：为每个活动准备封面

对每个候选活动，搜索封面图：

```js
// 调 web_search 搜图
web_search(keyword: "{活动名} 海报")
web_search(keyword: "{活动主题} 配图")
```

从搜索结果中提取可直接访问的图片 URL。如果没有找到，告知用户哪些活动缺封面并跳过。

#### Step 4：解析坐标

对每个活动地址搜索经纬度：

```js
web_search(keyword: "{地址} 经纬度")
```

提取 lat/lng，不能编造。

#### Step 5：循环批量创建

**逐条、顺序调用**（等上一条返回再调下一条）：

```js
for (const item of activities) {
  const result = await create_activity({
    content: item.title,
    address: item.address,
    cover: item.coverUrl,
    tags: item.tags,
    latitude: item.lat,
    longitude: item.lng,
    start_time: item.startTime,
    end_time: item.endTime,
    max_participants: item.maxParticipants || 0
  })
  // 汇报每条结果
}
```

**进度汇报格式（每创建完一条输出）：**

```
已创建 1/5：深圳动漫展 ✅
已创建 2/5：南山周末市集 ✅
已创建 3/5：深圳湾晨跑 ❌（封面下载失败，已跳过）
...
```

全部完成后输出汇总：

```markdown
🎉 批量创建完成

成功 4 条：
- [深圳动漫展](https://fore.vip/pages/activity/detail?id=xxx) — 7月4日
- [南山周末市集](https://fore.vip/pages/activity/detail?id=xxx) — 6月28日
- [深圳湾晨跑](https://fore.vip/pages/activity/detail?id=xxx) — 每周六
- [净滩行动](https://fore.vip/pages/activity/detail?id=xxx) — 7月1日

失败 1 条：深圳音乐节（封面转存失败）
```

---

## create_activity — 创建活动 API

> 系统自动填充：`open=1`（公开）、`type="ai"`（AI 创建）、`create_time`/`update_time`

```
POST https://mcp.fore.vip/act/create
Content-Type: application/json
X-API-Key: {key}

{
  "content": "周末爬山",           // 必填 ≤500字
  "address": "深圳梧桐山",          // 必填 ≤128字
  "cover": "https://example.com/pic.jpg",  // 必填，自动转存至云存储
  "tags": ["徒步", "周末"],         // 可选，最多10个
  "latitude": 22.543,              // 可选，与 longitude 生成位置
  "longitude": 114.058,
  "start_time": 1718000000000,     // 可选 ms时间戳
  "end_time": 1718100000000,       // 可选
  "max_participants": 20,          // 可选，默认0=不限
  "creator_name": "小明"            // 可选
}
```

创建成功返回完整活动对象（含 `_id` 和 `url`，`cover` 为云存储 URL）。

## search_activities — 搜索活动

```
POST https://mcp.fore.vip/act/search
{ keyword, type, latitude, longitude, page, pageSize }
```

排序：有经纬度→距离 ASC；无→热度 DESC。

## get_activity_detail — 活动详情

```
POST https://mcp.fore.vip/act/detail
{ id: "6a0a..." }
```

返回完整活动文档。

## list_activity_schedules — 活动行程列表

```
POST https://mcp.fore.vip/act/schedules
{ activity_id: "6a0a...", page: 1, pageSize: 10 }
```

按活动 ID 查行程列表，`start_time` 升序。返回 schedule 表原始字段（不联表 guest）：

```json
{
  "list": [
    {
      "_id": "...",
      "activity_id": "...",
      "content": "集合出发",
      "start_time": 1718000000000,
      "end_time": 1718003600000,
      "guest_id": "uni-id-users._id 或 null",
      "in_progress": true,
      "cps": { "appId": "...", "path": "...", "url": "...", "icon": "..." },
      "creator": "...",
      "create_time": 1718000000000
    }
  ],
  "total": 25,
  "page": 1,
  "pageSize": 10
}
```

## 错误码

| 场景 | errCode | 说明 |
|------|---------|------|
| 创建缺 Key | 403 | Header 未带 X-API-Key |
| 字段缺失/超长 | -1 | content/address/cover 必填 |
| 封面转存失败 | -3 | 下载/上传失败，活动不创建 |
| DB 失败 | -2 | 数据库写入异常 |
| ID 缺失 | -1 | detail 缺少 id |
| 行程 activity_id 缺失 | -1 | schedules 缺少 activity_id |
| 搜索无结果 | — | list=[], text 含提示 |

## 使用示例

| 用户说 | Agent 行为 |
|--------|-----------|
| "帮我创建一个周末爬山的活动" | **模式1**：逐轮收集 Key→封面→主题→地址→坐标(自动解析)→时间→确认→单次调用 create_activity |
| "批量搜深圳未来活动和发布" | **模式2**：确认Key→搜索3维度→提取候补→搜封面→解析坐标→循环 create_activity→汇总汇报 |
| "附近的爬山活动" | search_activities({ keyword:"爬山", latitude, longitude }) |
| "这个活动详情" | get_activity_detail({ id }) |
| "这个活动有哪些行程" | list_activity_schedules({ activity_id }) |

---

## 提示

- **时间戳格式**：所有 `start_time` / `end_time` 字段均为 Unix 毫秒时间戳（13 位），不是秒。
- **行程不联表 guest**：`list_activity_schedules` 返回 `guest_id`（uni-id-users._id 字符串）但不返回嘉宾昵称/头像。若需展示嘉宾信息，由调用方另行查询用户表。
- **分页上限**：`pageSize` 最大 50，超过会被截断到 50；建议默认 10。
- **空行程处理**：新活动可能无行程，`list` 返回 `[]`、`total: 0` 属正常，应提示用户"该活动暂无行程，可去小程序内推荐"。
- **MCP 与前端双路线**：`schedules()` 同时服务于 MCP（URL 化云对象 HTTP 接口 `POST /act/schedules`）和小程序/H5 直连（`uniCloud.importObject`），两条路线返回结构一致。
- **后端实现风格**：base 仓库的 act 云对象是 URL 化云对象风格，方法直接读取 `this.getHttpInfo().body` 解析参数，返回业务对象或 `{errCode, errMsg}`，不是 JSON-RPC `tools/call` 路由风格。
- **创建活动封面**：`cover` 必填，必须是可公网访问的图片 URL，后端会下载转存到云存储，原 URL 不再保留。
- **`create_activity` 鉴权**：每次调用都要在 HTTP Header 传 `X-API-Key`，不缓存、不存储，每轮重问。
- **`get_activity_detail` 副作用**：调用即自增 `view_count`，Agent 不要为同一活动重复调用详情接口。
- **坐标格式**：GeoJSON 标准 `[lng, lat]`（经度在前），与大部分地图 SDK 的 `[lat, lng]` 相反，注意转换。

---

## 引用

| 项 | 路径 / 链接 |
|----|-------------|
| MCP 后端源码 | `~/git/base/uni_modules/act/uniCloud/cloudfunctions/act/index.obj.js` |
| MCP 工具契约 | `skills/act/mcp.json` |
| schedule 集合 schema | `~/git/base/uniCloud-aliyun/database/schedule.schema.json` |
| schedule 云对象（订阅消息） | `~/git/base/uniCloud-aliyun/cloudfunctions/schedule/index.obj.js` |
| 前端行程查询参考实现 | `~/git/base/pages/activity/detail.vue#loadScheduleList` |
| MCP 服务地址 | `https://mcp.fore.vip` |
| skills 仓库 | `https://github.com/fore-vip/skills` |
| 活动详情页（H5） | `https://fore.vip/pages/activity/detail?id={_id}` |
| 行程详情页（H5） | `https://fore.vip/pages/activity/schedule?activity_id={_id}` |
| 项目主域 | `https://fore.vip` |
| 区域定位 | 深圳 (CN-SZ)，中心 [114.058, 22.543]，覆盖约 80km 半径 |

