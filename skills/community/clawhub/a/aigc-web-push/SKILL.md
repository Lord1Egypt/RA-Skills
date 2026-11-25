---
name: aigc-web-push · AI内容生成与全网推送
slug: aigc-web-push
displayName: aigc-web-push · AI内容生成与全网推送
version: 3.6.11
summary: AI 生成文章/图文/视频，并推送到微信公众号或云电脑全网发布
license: MIT
description: 支持通过 AI 生成文章、图文卡片与视频，并推送到微信公众号（无需泄露公众号 Secret，无需配置 IP 白名单）或经由云电脑推送至全球任意站点；兼容其它技能产出的文章、图片与视频。
---

# aigc-web-push · AI内容生成与全网推送

**版本 3.6.11**

## 文件路径与作用

| 文件 | 位置 | 作用 |
| --- | --- | --- |
| **SKILL.md** | `aigc-web-push/` | 本说明 |
| **design.md** | 同上 | HTML 格式规范（文章 / 贴图 / 封面） |
| **design-video.md** | 同上 | 兜底成片；公共条款见 §2 / §3.1 / §3.2 / §5.3 / §6 / §7.1 / §11 |
| **Humanizer-zh.md** / **Humanizer.md** | 同上 | 去 AI 味（中 / 英） |
| **config.json** | 同上 | 配置向导生成后的真实配置 |
| **config.example.json** | 同上 | 字段说明 + 示例 |
| **package.json** | 同上 | 固定 CommonJS（`private`，不发 npm）；`version` 为技能版本 |
| **check-update.js** | 同上 | 推送前核对版本；落后则暂停并提示询问用户是否升级（由 `push.js` 调用） |
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
  out/gugong-ye-you.mp4  # 成片 out/<主题>.mp4
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

AI 检查 **aigc-web-push 目录** 下是否存在含有效 `openId` + `skillKey` 的 `config.json`。

- **写文章 / 贴图 / 做视频（含旁白、画面、成片）不要求登录**，无配置也可继续。
- **缺配置时不可用：** 推送、平台音乐搜索。需要时再发上方配置向导；无配置时配乐按「视频」第 8 条改走其它曲库。

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
- `skillKey`：向导签发；推送与音乐搜索必带。
- `autoUpdate`：可选；`false` 关闭推送前版本检查。

---

## 版本检查

`push.js` 推送前对照远端最新版。有新版本时**只向用户问是否升级**，并退出码 2（不自动改文件）。

**Agent 收到退出码 2 后：**

1. 询问用户是否升级（勿把命令行细节甩给用户）。
2. **同意**：保留本目录 `config.json`，执行 `npx skills add lihengdao/AIGC-Web-Push -g -y`，再重新推送。
3. **暂不升级**：设 `AIGC_WEB_PUSH_NO_UPDATE=1` 后重新推送。

同目录 24 小时检查一次；网络失败不阻断。关闭检查：`config.json` 的 `autoUpdate: false`，或 `AIGC_WEB_PUSH_NO_UPDATE=1`。

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

公众号不支持视频。推送仅云电脑；账号须已绑定 `contentType=video`。

本技能负责：分流、作品目录、成片路径、公共质量底线、封面、推送、配乐与音效。制作流水线与镜头语法以**选定能力的文档**为准，禁止凭本节或记忆开写。**第 2–4、8–9 条及所引 `design-video.md` 条款对一切能力生效**；与能力文档冲突时以本节为准。写代码前满足第 2–4 条；推送前通过第 9 条。

1. **作品目录** — `works/<日期>-<主题>/`；工程、音频、成片均在此，禁止写入技能根目录。成片路径：`out/<主题>.mp4`。

2. **画面与素材** — 主体为**程序化绘制**（Remotion / SVG / Canvas / CSS / R3F 等）。禁止为填镜头搜索、下载或采集图库照片、库存视频、网页截图或实拍；禁止用 AI 生成图/视频作主体镜头（封面除外）。**仅当用户明确上传或授权**外部素材时方可使用，并核实许可。能力文档中的采图、截图、B-roll、素材闸门要求与本条冲突时，跳过并以程序化等价镜头继续。画不准、质感不够或主题不易程序化时，按 `design-video.md` §3.2 依次换画法、换讲法或收窄表达，并完成完整成片。

3. **结构开合与正文（写稿或分镜前完成）** — 全片须有 **建立 → 展开 → 收束**（有旁白落在文案；无旁白落在画面段落）。建立给出观看理由或主题锚定；展开递进，禁止开场即散点罗列；收束闭合，禁止突然中断。有旁白时：先完成完整文案再配音；按 `design-video.md` §2.2 **依内容**选定主叙事结构，不得为套模型而硬套；旁白速率固定 **1.0**，禁止为卡点或时长变速（§5.3）。旁白与字幕只写主题内容，遵守 §6.5（禁止制作元话术）。事实不足则降低断言强度，不得编造。用户未要求逐步确认时自主推进到成片。

4. **镜头叙事（分镜与成片均须满足）** — 遵守 `design-video.md` §3.1 与 §6.5：核心信息点呈现「对象 → 可见变化 → 结果」；主段以连续状态变化推动观看，开场数秒内有可感知运动；按内容选型（界面 / 过程 / 结构 / 数据 / 情绪），不强制三维或固定配色；一镜一主表达，段落有承接，全片视觉语言统一；不以信息卡、要点列表轮播或节点流程图为主段；旁白、字幕与画面文字无制作元话术。

5. **分流（只选一个；看片子怎么讲，不看题材名）**

| 判断 | 能力 |
| --- | --- |
| 产品 / 网站 / App 的界面动效或软件产品介绍 | `video-shotcraft` |
| 旁白 / 口播 / 讲解为主 | `video-talkcraft` |
| 皆不明显，或自由视觉 / 无旁白 | `design-video.md` + Remotion 官方 Skills |

用户点名从其点名；歧义则问清后二选一，禁止并行；仍不清则 `design-video.md`。选定能力提供镜头语法与工程流程，**不免除第 2–4、8–9 条**。

6. **选定 `video-shotcraft` / `video-talkcraft` 后（写代码前）**
   - 未装则 `npx skills add Vincentwei1021/video-shotcraft` 或 `…/video-talkcraft`；失败则改 `design-video.md` 并告知用户。
   - 定位 skill 目录（`~/.agents/skills/`、`~/.claude/skills/`、`~/.codex/skills/` 或 CLI 提示路径），确认有 `SKILL.md`。
   - **完整阅读**该 `SKILL.md`，再按其指示阅读 `references/` 等。
   - 分镜、镜头配方与工程从其文档；与第 2–4 条冲突的采图、截图、库存素材或中途逐步确认要求，按本节公共底线执行。工程与成片在当前作品目录（第 1 条）。

7. **选定 `design-video.md` 后** — 安装 Remotion Skills（有 `@remotion/cli`：`npx remotion skills add`；否则 `npx skills add remotion-dev/skills`），加载 `remotion-best-practices`（场景 `remotion-markup`，API `remotion-docs` 或官网），完整执行 `design-video.md`（含 §2 / §3.1 / §6 / §11）。无法安装则告知用户并查阅官方文档，禁止凭记忆硬写。

8. **配乐与音效** — 遵守 `design-video.md` §7。配乐：用户指定 → 有配置则按 §7.1 下载到作品 `audio/` → 否则用其它曲库；接入时间线并按 §7.5 混音与机器判据验收（对白段音乐相对旁白工作电平低约 12～18 dB，停顿段恢复；侧链压低非静音）。音效：分镜列出动作点并同步取材接入。除用户明确静音外，成片须有可感知配乐；有动作点须有同步音效。禁止为对齐配乐而变速旁白。

9. **发布收口** — 唯一成片：`out/<主题>.mp4`；`push.js`（标题 + 描述，面向读者）。剪映工程、工作台、本地 preview 不替代本通道。
   - **封面：** 作品目录或 `out/` 若无封面，按 §3.2 补：`cover.png`（可用 AI 图，仅作封面）或 `cover.html`；推送时有图优先。
   - **技术验收：** 可播放、音画同步、无黑屏或缺资源；有旁白则字幕对齐且速率为 1.0。
   - **视觉与正文验收：** 对照第 2–4、8 条与 `design-video.md` §3.1 / §3.2 / §6.5 / §7 / §11；用时间码标出若干「对象—变化—结果」镜头；确认开合、开场运动、换方案、配乐接入与 §7.5 可感知、动作点音效；旁白、字幕、画面文字无 §6.5 元话术。技术通过不表示画面或声音合格；主段若为信息卡、方块连线、无变化讲解、缺乏可见动态、含元话术，或无静音例外却无配乐 / 配乐不可感知 / 有动作点却无同步音效，须返修重渲。

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

# 公众号 · 图片 URL（第 4 参为描述 / 图说）
node push.js wechat - img '["https://cdn.example.com/1.png"]' "标题" "描述"

# 云电脑 · HTML（标题←title，描述←meta description）
node push.js cloud - html ../works/20261117-demo/main.html article draft
node push.js cloud - html ../works/20261117-demo/main.html article draft account "官网账号"

# 云电脑 · 本地图（可选描述）
node push.js cloud - img ../works/20261117-demo/poster.png "标题" "描述" draft

# 云电脑 · 视频（标题 + 描述 + 可选封面）
node push.js cloud - video ../works/20261117-gugong-ye-you/out/gugong-ye-you.mp4 "故宫夜游指南" "三条路线带你逛亮灯后的故宫。" draft
node push.js cloud - video ../works/20261117-gugong-ye-you/out/gugong-ye-you.mp4 "故宫夜游指南" "三条路线带你逛亮灯后的故宫。" draft account "抖音主号"
```

字段对齐 auto-publish / design 前端：`title`、`description`、封面（`cover.png` 优先，否则文章 `*_cover.html` / 视频 `cover.html`）。

### 说明

- 公众号 / 云电脑未指定时用 `-` → 配置里 `selected: true` 项；也可传名称或 id。
- 云电脑指定环境/账号时按名称解析，歧义则失败并打印候选。
- API 基址：`apiBase`（缺省 `https://api.pcloud.ac.cn/openAccessService`）。
- **云电脑入队即完成**：勿轮询、勿因「还没发出」重推。
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
