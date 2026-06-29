---
name: amap-roadbook
description: 当用户想把自然语言旅行想法生成高德/Amap 路书，或生成可公网访问的 HTML/Excel/JSON 路书产物时使用。本 skill 会先反问缺失信息，再进行地点解析、POI 搜索、路线规划、每日时间线、天气提醒、假设说明，并默认发布到公网静态目录以便访问和下载。需要用户配置高德 Web Service API Key、JavaScript API Key 和 JS 安全密钥。
version: 0.2.1
metadata: { "openclaw": { "requires": { "env": ["AMAP_WEB_SERVICE_KEY", "AMAP_JS_API_KEY", "AMAP_JS_SECURITY_CODE"] }, "primaryEnv": "AMAP_WEB_SERVICE_KEY", "envVars": [{ "name": "AMAP_WEB_SERVICE_KEY", "required": true, "description": "高德 Web Service API Key，用于地理编码、POI 搜索、路径规划、输入提示、行政区划和天气查询。" }, { "name": "AMAP_JS_API_KEY", "required": true, "description": "高德 JavaScript API Key，用于交互式地图渲染。" }, { "name": "AMAP_JS_SECURITY_CODE", "required": true, "description": "高德 JavaScript API 安全密钥，用于前端地图渲染。" }] } }
---

# 高德 AI 路书

GitHub 仓库预览效果： [zuo-wentao/Amap-Roadbook-Skill](https://github.com/zuo-wentao/Amap-Roadbook-Skill)

根据用户的自然语言旅行计划，生成一份可执行的地图路书。路书应结合高德 API、路线规划、天气信息、每日时间线和可用于地图渲染的结构化数据。

亮点：

- **在线预览**：生成可分享的网站页面，用户打开链接即可查看完整地图路书。
- **实时编辑**：修改行程后复用同一个 `publishId` 覆盖更新，让预览链接保持不变。
- **Excel 计划表**：主动生成并返回 `.xlsx` 下载地址，方便同行人查看、打印或二次编辑。
- **交互地图**：基于高德 JS API 展示停靠点、路线和每日时间线。
- **路线兜底**：优先使用真实线路，查不到路线时自动使用直线兜底。

## 核心规则

在生成路书前，必须确认最低规划信息是否齐全。如果关键信息缺失，先提出简洁的澄清问题并停止，不要编造日期、出发地、目的地或必去地点。

最低必需信息：

- 出发城市或出发地点。
- 目的城市或旅行区域。
- 出行日期、开始日期或旅行天数。
- 至少一个必去地点、目的地列表或兴趣偏好。

强烈建议确认的信息：

- 住宿地址、酒店名称或偏好的住宿区域。
- 城际交通偏好：高铁、飞机、自驾或都可以。
- 市内交通偏好：公共交通、打车、步行、自驾或都可以。
- 每日节奏：轻松、均衡或紧凑。
- 旅行限制：老人、小孩、行李、无障碍需求、预算限制等。

每次最多问 3-5 个问题。优先询问能让第一版路书成立的最少问题。

完整反问策略见 `references/clarification-policy.md`。

## Key 配置

用户需要配置自己的高德 Key。不要把作者的 Key 写死进 skill、脚本或示例输出。

- `AMAP_WEB_SERVICE_KEY`：高德 Web Service API Key，用于地理编码、POI 搜索、路径规划、天气等服务。
- `AMAP_JS_API_KEY`：高德 JavaScript API Key，用于交互式地图渲染。
- `AMAP_JS_SECURITY_CODE`：高德 JavaScript API 安全密钥，用于前端地图渲染。

### 配置方式（按优先级）

脚本 `scripts/plan-roadbook.mjs` 中的 `resolveKey()` 按以下优先级读取 Key：

1. **Shell 环境变量**（最高优先级）
2. **`~/.openclaw/openclaw.json`** 中的 `skills.entries.amap-roadbook.env.<KEY_NAME>`

> ⚠️ 注意：脚本读取的是 `~/.openclaw/openclaw.json`，**不是** `gateway.json`。如果你在 gateway 配置配了 Key，需要同步写到 openclaw.json 的对应位置，否则脚本拿不到。

#### 方式 1：在 openclaw.json 中配置（推荐）

```json5
{
  skills: {
    entries: {
      "amap-roadbook": {
        enabled: true,
        env: {
          AMAP_WEB_SERVICE_KEY: "YOU_AMAP_WEB_SERVICE_KEY",
          AMAP_JS_API_KEY: "YOUR_AMAP_JS_API_KEY",
          AMAP_JS_SECURITY_CODE: "YOUR_AMAP_JS_SECURITY_CODE"
        }
      }
    }
  }
}
```

不建议只配置 `apiKey` 便捷字段；本 skill 需要同时读取三个环境变量。

如果你是本地开发、并且需要让 OpenClaw 扫描额外目录，再单独加：

```json5
{
  skills: {
    load: {
      extraDirs: [
        "/path/to/amap-roadbook/parent-dir"
      ]
    }
  }
}
```

#### 方式 2：Shell 环境变量（本地测试用）

```bash
export AMAP_WEB_SERVICE_KEY="你的高德 Web Service Key"
export AMAP_JS_API_KEY="你的高德 JS API Key"
export AMAP_JS_SECURITY_CODE="你的高德 JS 安全密钥"
```

### 验证 Key 配置

运行脚本时，第一行日志会打印 Key 状态：

```
🔑  Key 状态：WEB=✅  JS=✅  SECCODE=✅
```

如果某个 Key 为 `❌`，对应字段会有详细提示（配置文件路径、缺失字段名、解析错误等）。也可以直接运行路书生成验证：

```bash
cd /path/to/amap-roadbook
node scripts/plan-roadbook.mjs --input input/sample.json --output-dir /tmp/check
```

### 高德 Key 申请地址

- 高德开放平台：https://lbs.amap.com/
- 控制台 → 应用管理 → 我的应用 → 创建新应用
- **Web Service Key**：平台选「Web 服务」
- **JS API Key**：平台选「Web 端(JSAPI)」，启用安全密钥并设置域名白名单

## 工作流程

1. 将用户输入解析为旅行需求草稿。
2. 检查最低必需信息是否齐全。
3. 如果信息缺失，提出澄清问题并停止。
4. 如果信息齐全，构造结构化路书请求。
5. 先用高德 API 解析地点，再规划路线。
6. 按天生成有序停靠点和交通路段。
7. 返回简洁说明和可用于地图渲染的 JSON。
8. 信息齐全并需要生成产物时，默认使用 `scripts/plan-roadbook.mjs --publish --excel` 发布到公网静态目录。
9. 如果用户明确说“不发布”“仅本地生成”或类似要求，才输出到本地 `output/`。
10. 如果用户在同一会话要求修改已发布路书，复用上一次 `publishId` 覆盖同一发布目录，让链接保持不变。

## 公网发布

默认发布配置：

- 本地暂存目录：`output/<publishId>/`
- 上传接口：`http://120.46.7.129:30002/publish`
- 服务器保存目录：`/opt/openclaw-publish/<publishId>/`
- 公网地址：`http://120.46.7.129:30001`
- HTML 页面：`http://120.46.7.129:30001/<publishId>/`
- Excel 下载：`http://120.46.7.129:30001/<publishId>/roadbook.xlsx`

默认生成并发布：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --publish --excel
```

会话内修改已有发布结果时，使用上一次的 `publishId`：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --publish --publish-id <previousPublishId> --excel
```

发布模式会生成：

```text
output/<publishId>/
  index.html
  roadbook.json
  roadbook.xlsx
```

然后通过 Node 上传服务写入服务器：

```text
POST http://120.46.7.129:30002/publish
```

Nginx 只负责静态访问；上传服务只接收 `index.html`、`roadbook.json`、`roadbook.xlsx` 并保存到 `/opt/openclaw-publish/<publishId>/`。

发布客户端需要配置：

- `ROADBOOK_PUBLISH_TOKEN`：必填，上传服务鉴权 token。
- `ROADBOOK_PUBLISH_ENDPOINT`：可选，默认 `http://120.46.7.129:30002/publish`。

服务端运行 `scripts/publish-server.mjs`，需要配置：

- `ROADBOOK_PUBLISH_TOKEN`：可选，必须和客户端一致（默认无需 token）。
- `ROADBOOK_PUBLISH_PORT`：默认 `30002`。
- `ROADBOOK_PUBLISH_ROOT`：默认 `.`（当前目录）。
- `ROADBOOK_PUBLIC_BASE_URL`：默认 `http://120.46.7.129:30001`。

发布后必须主动在回答中返回可打开/可下载的产物地址，不要只说“已生成”：

- `publishId`
- 网站页面访问链接（HTML）
- Excel 下载链接（XLSX）
- 远程服务器目录路径
- JSON/HTML/XLSX 文件路径

如果脚本生成了 `roadbook.html`、`index.html` 或 `roadbook.xlsx`，回答里必须明确列出对应地址或文件路径；如果某个产物生成失败，必须直接说明失败原因或缺失项。

必须提醒用户：发布链接公网可访问，可能包含出行日期、住宿区域、同行人和预算等信息，只分享给可信对象。用户明确要求不发布时，使用本地模式。

### Excel 路书

运行脚本时加 `--excel` 可额外生成格式化的 `.xlsx` 表格：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --publish --excel
```

生成的 `roadbook.xlsx` 包含 5 个 Sheet：

| Sheet | 内容 |
|---|---|
| 总览 | 目的地、日期、天气、预算、假设、提醒 |
| 每日行程 | 每日时间线，停靠点 + 交通衔接，按交通方式着色 |
| 路线段 | 起点→终点、方式、耗时、距离 |
| 预算 | 分项估算 + 合计，与预算对比 |
| 景点信息 | 电话、评分、营业时间（来自高德 POI 数据） |

也可以单独运行导出脚本：

```bash
node scripts/export-excel.mjs --input output/roadbook.json --output output/roadbook.xlsx
```

### 本地模式

只有当用户明确要求“不发布”或“仅本地生成”时，使用本地模式：

```bash
node scripts/plan-roadbook.mjs --input input/roadbook-input.json --output-dir output --excel
```

本地模式会生成 `roadbook.html`、`roadbook.json` 和可选的 `roadbook.xlsx`，不会返回公网链接。回答中仍然必须主动返回本地 HTML 和 XLSX 文件路径，方便用户直接打开或下载。

## 高德 API 使用原则

以下事实应优先来自高德 API：

- 地理编码：解析城市、酒店、车站、机场、景点和地址。
- 输入提示和关键字搜索：消解模糊地点名。
- 路径规划：估算路段耗时，并选择市内交通方式。
- 天气查询：添加每日天气提醒和风险提示。
- 行政区划查询：规范城市、区县和 adcode。
- 静态地图或 JavaScript 地图：后续用于生成可分享的地图路书。

不要编造高德 API 不覆盖的实时事实。酒店价格、景区门票、机票价格、火车票价格、班次和营业时间，除非有可靠来源，否则必须标注为"需另行确认""用户提供"或"估算"。

API 选择细节见 `references/amap-api-map.md`。

## 输出协议

输出应包含：

- 对已理解行程的简短确认。
- 明确列出假设。
- 每日时间线：时间、地点、推荐活动和备注。
- 路线路段：起点、终点、交通方式、耗时、距离和换乘说明。
- 天气提醒和时间风险。
- 遵循 `references/roadbook-schema.md` 的地图可渲染 JSON。
- 如果生成了公网产物，必须主动附上网站页面链接、Excel 下载链接、`publishId` 和服务器路径。
- 如果生成了本地产物，必须主动附上本地 HTML、JSON 和 XLSX 文件路径。
- 不要省略网站和 xlsx 地址；只要文件存在，就必须在最终回答中列出来。

## 输出风格

回答要像一个实用的旅行执行助理，不要像营销文案。好的结果应该说明：

- 哪些信息已经确认。
- 哪些信息是默认假设。
- 每天的简明安排。
- 哪些地方存在时间过紧、换乘过多、天气风险或信息缺失。

## 本地产物

当前 skill 默认生成公网可访问的 JSON/HTML/Excel 产物。只有用户明确要求不发布时，才生成本地 JSON/HTML/Excel 产物用于演示。除非用户明确要求做页面渲染，否则不要把精力放在网页细节实现上。

## 反问示例

用户："我明天去北京，想去圆明园、大兴机场和迪士尼，玩三天。"

应反问：

"我可以把它做成高德路书。生成前先确认 4 个信息：1. 你从哪里出发？2. 北京住宿已经确定了吗，还是需要我推荐住宿区域？3. 城际交通偏好是高铁、飞机，还是都可以？4. 每天希望轻松一点还是尽量多打卡？"

## 信息充分示例

用户："使用 $amap-roadbook。我 6 月 15 日从合肥出发去北京玩 4 天，偏好高铁，住海淀附近，想轻松安排圆明园、北京环球度假区、大兴机场和半天咖啡/书店。"

此时可以继续构造路书请求，并生成结构化路书结果或本地产物。
