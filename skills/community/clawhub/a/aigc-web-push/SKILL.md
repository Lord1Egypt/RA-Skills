---
name: aigc-web-push · AI内容生成与全网推送
description: 支持通过 AI 生成文章、图文卡片与视频，并推送到微信公众号（无需泄露公众号 Secret，无需配置 IP 白名单）或经由云电脑推送至全球任意站点；兼容其它技能产出的文章、图片与视频。
---

# aigc-web-push · AI内容生成与全网推送

## 文件路径与作用

| 文件 | 位置 | 作用 |
| --- | --- | --- |
| **SKILL.md** | `aigc-web-push/` | 本说明 |
| **design.md** | 同上 | HTML 格式规范（文章 / 贴图 / 封面） |
| **remotion-video.md** | 同上 | Remotion 视频成片规范 |
| **Humanizer-zh.md** / **Humanizer.md** | 同上 | 去 AI 味（中 / 英） |
| **config.json** | 同上 | 配置向导生成后的真实配置 |
| **config.example.json** | 同上 | 字段说明 + 示例 |
| **package.json** | 同上 | 固定 CommonJS（`private`，不发 npm）；`version` 与 ClawHub 对齐 |
| **check-update.js** | 同上 | 推送前核对 / 自升级（由 `push.js` 调用） |
| **push.js** | 同上 | 统一推送入口（公众号 / 云电脑） |
| **push-to-wechat-mp.js** | 同上 | 公众号推送实现 |
| **push-to-cloud.js** | 同上 | 云电脑推送实现（本地媒体上传、按名解析目标） |

---

## 作品目录（强制）

**技能目录只放技能与配置；每条作品必须有独立工作文件夹。**  
禁止把 HTML、封面、Remotion 工程、TTS、音乐、成片堆在 `aigc-web-push/` 根目录或用户仓库根目录。

### 位置

在用户当前工作区（或用户指定的内容根）下：

```text
works/<YYYYMMDD>-<短主题>/
```

命名：日期 + 短横线 + 简短主题（可用拼音或英文）；用户指定名称时以用户为准。同主题改稿用子目录 `v2/`，不要覆盖上一版。

### 目录内容

**文章 / 贴图：**

```text
works/20261117-gugong-ye-you/
  main.html
  main_cover.html      # 可选；与主 HTML 同目录，主文件名 + _cover.html
  cover.png            # 可选封面图（有则优先于 HTML）
```

**视频：**

```text
works/20261117-gugong-ye-you/
  remotion/            # Remotion 工程
  audio/               # TTS、音乐、音效
  out/aigc-video.mp4   # 成片
  cover.html           # 可选封面 HTML；也可放在 out/ 下
  cover.png            # 可选封面图（有则优先；作品目录或 out/）
```

### 规则

1. 收到新创作任务后，**先建作品目录**，再在该目录内生成全部产出。
2. `config.json`、技能 Markdown、推送脚本永远留在 `aigc-web-push/`，不要复制进作品目录。
3. 推送时在技能目录执行 `node push.js …`，媒体参数传入作品文件的路径（相对技能目录或绝对路径）。
4. 封面只在**作品目录内**与主文件配对查找；技能根目录不放作品封面。

---

## 第一步：配置向导

| 项 | 内容 |
| --- | --- |
| **配置向导地址** | [https://design.pcloud.ac.cn/aigc-web-push.html](https://design.pcloud.ac.cn/aigc-web-push.html) |
| **流程** | AI 发向导给**当前操作用户** → 已在 design 登录则直接继续，否则微信扫码 → 选默认公众号 / 默认云电脑 → 用户复制发给 **自己的** AI |

AI 检查 **aigc-web-push 目录** 下是否存在 `config.json`。如果不存在，则无法使用本技能，AI 需要发送配置向导地址给用户完成配置。

**说明：**

- **微信公众号**：本人号 + 企业显式授权号 + 企业管理员可见的本企号；点选一项为默认（`selected: true`）。没有可跳过，配置里不写 `accounts`。新号才扫码授权并填写 AppID / sn。
- **云电脑**：同上口径列出可用机并写入 `instances`。没有机器也可生成配置（省略 `instances`）。点选的那一台是默认（`selected: true`）。
- **不预选环境 / 账号**：向导只授权通道。推送时再按对话指定「某环境 / 某账号 / 某云电脑」；配置里 `defaultTargetScope` 固定为 `all`。

**多人 / 企业（必读）：**

| 规则 | 说明 |
| --- | --- |
| 一人一配置 | `openId` + `skillKey` 绑定**扫码人**。同事各走各的向导；**禁止**把别人的 `config.json` 拷给 Agent |
| 重新扫码 | 会轮换 `skillKey`，旧配置立刻失效 |
| 企业资源授权 | 在 Design「我的 → 团队」由 **所有者/管理员** 授权云电脑/公众号；本向导不能替人授权 |
| 角色 | 管理员可见本企高敏资源；编辑仅能用已授权资源；**只读不能推**高敏资源 |
| 计费 | 在团推送扣**企业钱包** Token |

**云电脑相关管理（不在本技能目录内操作）：**

| 事项 | 在哪里做 |
| --- | --- |
| 开通 / 开关机 / 销毁云电脑 | [云电脑管理](https://design.pcloud.ac.cn/#/manage?tab=server) |
| 在云电脑上绑定站点账号（文章 / 贴图 / 视频等） | 同上：进入对应云电脑控制台完成登录与账号绑定 |
| 授权同事用某台机 / 某个公众号 | Design「我的 → 团队」 |
| 选默认公众号 / 默认云电脑写入 `config.json` | 本技能配置向导（须本人登录） |

向导**不能**开通机器，也**不能**代绑站点账号或代授企业权限。没有公众号或云电脑也可以先生成配置；要用哪条通道，再补对应的号或机器。

---

## 第二步：配置文件

AI 将配置向导得到的配置参数保存为 **aigc-web-push 目录** 下的 `config.json`，编码 **UTF-8**。

```bash
cat > config.json << 'EOF'
{ … 粘贴配置向导 JSON … }
EOF
```

`config.json` 字段：

- `accounts`：有公众号才写入；`selected: true` 为默认（至多一项）。
- `instances`：有云电脑才写入；`selected: true` 为默认（至多一项）。
- `defaultTargetScope`：向导固定为 `all`；推送时可用 CLI 覆盖为 `environment` / `account`。
- `skillKey`：向导签发；推送与 `remotion-video.md` 中音乐搜索等需鉴权接口必带。
- `autoUpdate`：可选；`false` 关闭推送前自动升级。

---

## 自动升级

`push.js` 推送前对照 [ClawHub](https://clawhub.ai/lihengdao/aigc-web-push) 最新版；落后则升级技能文件并继续推送（**保留 `config.json`**）。同目录 24 小时检查一次。网络失败不阻断推送。

关闭：`config.json` 设 `"autoUpdate": false`，或环境变量 `AIGC_WEB_PUSH_NO_UPDATE=1`。

手动：`npx clawhub update aigc-web-push` 或 `npx skills update aigc-web-push`。

---

## 第三步：写内容

先按「作品目录」建好文件夹，再创作。

### 文章 / 贴图（HTML）

1. 阅读 `design.md`；文本文章按 `Humanizer-zh.md`（中文）或 `Humanizer.md`（英文）去 AI 味。
2. 在作品目录生成 `main.html`（文件名可自定）：
   - **文章**：默认宽度 677px
   - **贴图**：默认宽度 375px，固定分页比例（默认 3:4）；同作品内所有 `.pagination` 高度一致。推公众号时后台会把 HTML 转成图片。
3. 无内嵌图片时，按 `design.md`「封面 HTML」在**同一作品目录**生成 `main_cover.html`（主文件名 + `_cover.html`）；若已有封面图，文件名固定为 `cover.png`（有则优先）。

贴图版式取向见 `design.md`「版式取向」。

### 视频（Remotion）

必须按 `remotion-video.md` 成片，再推云电脑。公众号不支持视频；云电脑须已绑定 `contentType=video` 的账号。

1. 在作品目录内创建 `remotion/` 等子目录，**不要**把 Remotion 工程建在技能根目录。
2. 准备 Remotion Agent Skills 后编码：
   - 已有 Remotion / `@remotion/cli`：`npx remotion skills add`
   - 尚未安装 Remotion：`npx skills add remotion-dev/skills`
   - 加载 `remotion-best-practices`；写场景加载 `remotion-markup`；查 API 用 `remotion-docs` 或官网文档。
   - 无法安装时告知用户并查官方文档，禁止凭记忆硬写。
3. 流程：旁白文案 → 锁定 TTS → 字词级对齐 → 字幕 → 分镜 → Remotion → 渲染 → 验收。
4. 成片：`works/.../out/aigc-video.mp4`；可选 `cover.html` / `video_cover.html`，或封面图 `cover.png`（作品目录或 `out/`；有图优先）。

---

## 第四步：推送

在 **aigc-web-push 目录**执行 `push.js`；通道为 `wechat` 或 `cloud`。下方路径示例假设作品目录相对技能目录为 `../works/20261117-demo/`（按实际路径调整）。

### 对话路由

| 用户说法 | Agent 行为 |
| --- | --- |
| 未指定目标 | 默认公众号或默认云电脑；云电脑 `targetScope=all` |
| 「发到 xx 公众号」 | `wechat` 首参用公众号 **名称** 或 AppID（`config.accounts`） |
| 「发到 xx 云电脑」 | `cloud` 首参用机名或 id（`config.instances`） |
| 「发到 xx 环境」 | `resolve`（`prefer=environment`）或 `… environment "名称"` |
| 「发到 xx 账号 / 视频账号」 | `resolve`（视频用 `categoryId=video`，`prefer=account`）或 `… account "名称"` |
| 歧义 / 未匹配 | 列出 candidates 或名称冲突列表，禁止擅自推送 |
| 视频 + 公众号 | 说明不支持，改云电脑 |

```bash
cd aigc-web-push
node push.js cloud - list-targets video
node push.js cloud - resolve video "抖音主号" account
node push.js cloud - resolve article "Chrome-工作" environment
```

`resolve` 唯一命中返回可推送参数；不唯一时退出码 3 并打印候选。

### 推送目标（云电脑）

| `targetScope` | 含义 | 附加参数 |
| --- | --- | --- |
| `all`（默认） | 该机全部匹配且启用的账号 | 无 |
| `environment` | 指定浏览器环境 | id 或名称 |
| `account` | 指定发布账号 | id 或名称 |

多机时仅支持 `all`。

### 命令示例

```bash
cd aigc-web-push

# 公众号 · HTML（- = 默认号；也可用名称或 AppID）
node push.js wechat - html ../works/20261117-demo/main.html
node push.js wechat "我的订阅号" html ../works/20261117-demo/main.html

# 公众号 · 图片 URL
node push.js wechat - img '["https://cdn.example.com/1.png"]' "标题" "正文"

# 云电脑 · HTML
node push.js cloud - html ../works/20261117-demo/main.html article draft
node push.js cloud - html ../works/20261117-demo/main.html article draft account "官网账号"

# 云电脑 · 本地图
node push.js cloud - img ../works/20261117-demo/poster.png "标题" draft

# 云电脑 · 视频
node push.js cloud - video ../works/20261117-demo/out/aigc-video.mp4 "标题" draft
node push.js cloud - video ../works/20261117-demo/out/aigc-video.mp4 "标题" draft account "抖音主号"
```

封面：推送时自动附带。封面图固定为 `cover.png`（有则优先）；否则文章用同目录 `*_cover.html`，视频用 `cover.html` / `video_cover.html`。

### 说明

- 公众号未指定时用 `-` / `default` → `accounts` 中 `selected: true`；也可传名称或 AppID。
- 云电脑未指定时用 `-` → `instances` 中 `selected: true`；也可传机名或 id。
- 云电脑指定环境/账号时，末参的 id 与名称一律经 `resolveCloudPublishTarget` 解析，歧义则失败并打印候选。
- API：`apiBase`（缺省 `https://api.pcloud.ac.cn/openAccessService`）。公众号 `sendToWechat`；云电脑 `sendToCloud`；列目标 `listCloudPublishTargets`；按名解析 `resolveCloudPublishTarget`；上传 `prepareMediaUpload`。
- **云电脑入队即完成**：勿轮询站点结果、勿因「还没发出」而重推。
- **公众号超时**：可视为已受理，勿狂推；请用户看服务通知或草稿箱。

## 其它功能

### 清空草稿箱

POST `https://api.pcloud.ac.cn/openAccessService`：

```json
{
  "action": "cleanupDrafts",
  "openId": "",
  "skillKey": "",
  "appId": ""
}
```

超时可视为已成功；请用户在公众号草稿箱确认。
