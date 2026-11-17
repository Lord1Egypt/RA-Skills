---
name: channels-video-publish
slug: channels-video-publish
displayName: 视频号自动发布
version: 1.2.1
description: 内容做好之后的视频号自动发布。成品视频 + 文案就绪后，一条命令完成上传、填短标题/描述、归入合集、声明原创、设定时发表；支持按天批量排期，一次配好让系列内容自动逐日发出。也能对账「哪些发了哪些没发」、给已排期内容改时间。当用户说「发视频号」「视频号发布」「上传视频号」「视频号定时发表」「视频号排期」「查一下哪些没发」「改一下发布时间」时使用。
agent_created: true
---

# 视频号自动发布

## 它接的是哪一段

**内容生产之后的那一段。**

你已经有成品 mp4 和写好的文案，接下来要在网页后台里做一堆重复动作：传文件、填短标题、写描述、选合集、勾原创、点日历设定时。这些动作每条视频都要重来一遍，跟内容质量毫无关系，但必须人肉完成。

本 skill 把这整段收敛成一条命令。

| 它负责 | 它不负责 |
|---|---|
| 上传成品视频 | 剪辑、合成、加字幕 |
| 填短标题、描述 | 写文案、想选题 |
| 归入合集 | 做封面、生成素材 |
| 声明原创 | 互动、评论、看数据 |
| 设定时 / 按天批量排期 | 删除已发布内容（不可逆，本 skill 不做） |
| 发完之后：对账、改期 | — |

## When to use

- 「把这条视频发到视频号」「视频号定时发 10-15 07:00」
- 「这十几条视频排一下，每天发一条」
- 「查一下视频号里哪些发了哪些没发」
- 「把已经排上的那条改到后天」

## 前置条件

1. Chrome 带远程调试端口、用独立 profile 启动（别污染常用浏览器）：
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --remote-debugging-port=9222 --user-data-dir=/Users/jx/ChromeAutomation &
   ```
   在该浏览器里**手动扫码登录**视频号助手。会话会过期，脚本退出码 3 会提示。
2. node 依赖 `ws`：`/Users/jx/.workbuddy/binaries/node/workspace/node_modules`
3. 跑之前必须清代理（否则 9222 流量被劫持到 80）：
   ```bash
   unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY NODE_OPTIONS
   export NO_PROXY='127.0.0.1,localhost'
   ```
   Bash 工具里需要 `dangerouslyDisableSandbox: true`。

## Workflow

### Step 1 — 确认输入

- 成品视频（mp4）、**短标题 ≤16 字**、描述、合集名（默认「怎么活得更好」）
- 目标日期：**必须 ≤ 今天+14 天**（视频号硬限制，脚本会自动校验并中止）

### Step 2 — 先用 dry-run 跑一遍

```bash
node scripts/cdp-publish.js --file /path/a.mp4 --title "标题" \
  --desc "描述" --album "怎么活得更好" --duration 516 --day 15 --hour 07 --dry-run
```

dry-run 会做完上传 + 填字段 + 保存草稿，**不点发表**。确认草稿箱里内容无误再正式跑。

### Step 3 — 正式发布

- 定时：去掉 `--dry-run`，带 `--day/--hour`（可加 `--month`）
- 即时发表：加 `--immediate`
- 批量：维护 episodes.json，用 `--episodes <文件> --ep <编号>`

### Step 4 — 核对

- 到草稿箱/发表记录核对日期时间与原创标记
- 核查原创：`node scripts/check-original.js`

## 批量排期（最常用的姿势）

做一个系列时，真正省时间的用法是**一次配好，按天自动发**：

```bash
# episodes.json 里放好每一期的 file / title / desc / day
node scripts/cdp-publish.js --episodes episodes.json --ep 24 --day 15 --hour 07
```

完成后视频号里会排成一列「将于 X 月 X 日 07:00 发表」，你不用再管它。
注意视频号定时**最远只能选 14 天后**，超窗脚本直接中止（退出码 4），所以批量要按滚动窗口分批排。

## 发完之后

- **对账**：`node scripts/list-all.js` — 一次拉全量列表（标题/时间/原创状态），
  和本地文件一比就知道哪些没发、哪条漏了原创
- **改期**：`node scripts/reschedule.js <ep> <月> <日> <时> [分]` —
  已排上定时但还没发的内容改时间，走「修改并重新发表」链路，不用删稿重传

## CLI

```
node scripts/cdp-publish.js --file <mp4> --title <短标题> [--desc <描述>]
       [--album <合集>] [--duration <秒>] [--day <日> --hour <时> [--minute <分>]]
       [--immediate] [--dry-run]
node scripts/cdp-publish.js --episodes episodes.json --ep 24 --day 15 --hour 07
node scripts/check-original.js [--all]
node scripts/list-all.js
node scripts/reschedule.js <ep> <月> <日> <时> [分]
```

退出码：`0` 成功｜`1` 失败｜`3` 登录态失效需重扫｜`4` 定时日期超窗口（**未发布**）

## 安全规则（不要跳过）

- 目标日超 14 天窗口 → **中止，不发布**（宁可少发不错发）
- 日期/时间回填校验不符 → 中止
- **原创声明必须真实点击**，不要只改 DOM 属性
- 删除已发布条目不可逆且丢播放/赞数据，**必须用户明确确认**（本 skill 不含删除动作）
- 已发布条目**不能补声明原创**；>6 个月的连修改都不行，只能删旧重发

## 已知限制

- ✅ 已跑通：上传、短标题、描述、合集、原创、定时发表、改期
- ⚠️ 时间面板的小时点选偶发失效 → 脚本已内置「校验 + 重试 + 面板自动重开」
- ⚠️ **合集计数只统计已发布视频**：合集管理页/下拉里显示「共 N 个内容」不含定时中的条目，
  「共 1 个内容」不代表定时稿没选上合集。验证定时稿的合集绑定：
  列表行悬浮「修改并重新发表」打开编辑页，看合集字段是否回显目标合集名。

> 视频号助手新版是 SPA，发布表单藏在 **0×0 的 iframe** 里，鼠标坐标点击全部失效，
> 这也是为什么必须用 CDP 直连而不是普通的浏览器自动化。全部踩坑记录在
> `references/troubleshooting.md`，**改脚本前先读它**。

## 相关

- **抖音**发布见 skill `douyin-video-publish`（同一套思路，但 DOM 结构完全不同，脚本不可互换）

## 创建新合集（发布页内可完成）

「添加到合集」下拉里自带「创建新合集」入口（`.create`），流程：
点下拉 → 点「创建新合集」→ 弹窗输入标题（**上限 10 字，创建后不可修改**）→ 点「创建」→
出现「已创建合集」提示 → 重新打开下拉选中新合集 → Escape 关闭。
参考实现：`macros/ch-ep01-publish.js` 第 4 节。立即发布 = radio 保持 value=0（不定时，默认值）。

## 文件

- `scripts/cdp-publish.js` — 主发布脚本（上传 / 填字段 / 合集 / 原创 / 定时 / 批量）
- `scripts/list-all.js` — 全量列表导出，用于对账「哪些发了哪些没发」
- `scripts/reschedule.js` — 改已排期条目的时间
- `scripts/check-original.js` — 原创声明状态核查
- `references/troubleshooting.md` — **踩坑清单，改代码前必读**
- `assets/episodes.example.json` — 批量排期配置模板

## 更新日志

### v1.2.1（2026-10-20）
- 🔴 定时/改期必须**回读校验日期**：只校验时间会静默按旧日期发出，
  `references/troubleshooting.md` 新增第 13 条（含防御代码）
- 新增第 14 条：已定时条目走「修改并重新发表」改期，比删了重传快且不产生重复条目
- 已知限制补充：合集计数只统计已发布视频，定时稿的合集绑定要看编辑页回显

### v1.2.0（2026-10-11）
- 定位重写：明确为「内容做好之后的发布环节」，主线是自动发布与批量排期，
  对账/改期降为发完之后的辅助能力
- 新增「它负责 / 不负责」边界表，避免被当成剪辑或文案工具调用
- 批量排期提升为独立章节（系列内容一次配好、按天自动发）

### v1.1.0（2026-10-10）
- 新增 `reschedule.js`：已排期未发布条目可直接改时间，不用删稿重传
- 新增 `list-all.js`：一次性拉全量列表，用于对账
- 时间面板 hour/minute 点选加「校验 + 重试 + 面板自动重开」，修掉偶发不生效
- 时间戳对账要用北京时区换算（`toISOString()` 是 UTC，差 8 小时）
