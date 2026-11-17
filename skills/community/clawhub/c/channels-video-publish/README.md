# channels-video-publish · 视频号自动发布

**内容做好之后，把它发出去的这一段。**

你的成品视频和文案已经就绪，接下来要在网页后台里重复这些动作：传文件、填短标题、
写描述、选合集、勾原创、点日历设定时。每条视频都要重来一遍，跟内容质量毫无关系，
但必须人肉完成。

这个 skill 把整段收敛成一条命令，并且支持**按天批量排期**：一次配好，让系列内容
自己一天一天往下发。

支持 WorkBuddy / QClaw / ima / Claude Code / Cursor。

## 它做什么

```bash
node scripts/cdp-publish.js --file output.mp4 --title "短标题" \
  --desc "描述" --album "怎么活得更好" --duration 516 --day 15 --hour 07
```

一条命令完成：上传视频 → 填短标题 → 写描述 → 归入合集 → 声明原创 → 设定时 → 发表。

批量排期（做系列内容时最省时间的用法）：

```bash
node scripts/cdp-publish.js --episodes episodes.json --ep 24 --day 15 --hour 07
```

排完之后视频号里会挂着一列「将于 X 月 X 日 07:00 发表」，不用再管。

| 负责 | 不负责 |
|---|---|
| 上传成品视频 | 剪辑、合成、加字幕 |
| 填短标题、描述 | 写文案、想选题 |
| 归入合集 | 做封面、生成素材 |
| 声明原创 | 互动、评论、看数据 |
| 设定时 / 按天批量排期 | 删除已发布内容（不可逆，本 skill 不做） |
| 发完之后：对账、改期 | — |

## 为什么自己写脚本很麻烦

视频号助手新版是 SPA，**真正的发布表单藏在一个宽高为 0×0 的 iframe 里**：

- 鼠标坐标点击全部失效 → 只能用合成 DOM 事件或直接走 CDP
- 表单 iframe 的 URL 是 `empty.html` → 靠 URL 匹配定位的老脚本全废
- file chooser 在 0×0 iframe 里根本不触发 → 必须 `objectId` + `DOM.setFileInputFiles`
- ant-design / weui 组件基本只认真实点击事件 → DOM 层 `element.click()` 大面积无效

每一个都能耗掉一小时。全部解法固化在 `references/troubleshooting.md`。

## 安装

把整个目录放到 skills 目录下即可：

```
~/.workbuddy/skills/channels-video-publish/     # WorkBuddy
~/.claude/skills/channels-video-publish/        # Claude Code
```

依赖：`ws`（`npm i ws`）。

## 前置条件

1. 带远程调试端口启动 Chrome（用独立 profile，别污染常用浏览器）：

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir=/Users/jx/ChromeAutomation &
```

在该浏览器里**手动扫码登录**视频号助手。会话会过期，脚本会以退出码 3 提示。

2. 跑之前清代理（否则 9222 的流量会被劫持到 80）：

```bash
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY NODE_OPTIONS
export NO_PROXY='127.0.0.1,localhost'
```

## 用法

```bash
# 定时发表（10-15 07:00）
node scripts/cdp-publish.js --file video.mp4 --title "短标题" \
  --desc "描述" --album "合集名" --duration 516 --day 15 --hour 07

# 即时发表（不定时）
node scripts/cdp-publish.js --file video.mp4 --title "短标题" --immediate

# 演练：上传+填字段+存草稿，但不点发表
node scripts/cdp-publish.js --file video.mp4 --title "短标题" --dry-run

# 批量排期
node scripts/cdp-publish.js --episodes episodes.json --ep 24 --day 15 --hour 07

# 发完之后：对账 / 改期
node scripts/list-all.js                        # 哪些发了、哪些没发
node scripts/reschedule.js 24 10 16 07 00       # 把已排期的改到 10-16 07:00
```

### 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 失败 |
| 3 | 登录态失效，需重新扫码 |
| 4 | 定时日期超出 14 天窗口（**未发布**） |

## 安全设计

- 视频号定时**最远只能选未来 14 天**。脚本会提前校验，超窗直接中止，绝不误发
- 日期 / 时间回填会二次校验，不符预期就停
- 原创声明必须真实点击，不允许只改 DOM 属性
- 本 skill **不含任何删除动作** —— 删除已发布内容不可逆且会丢播放/赞数据

## 已知限制

- ✅ 已跑通：上传、短标题、描述、合集、原创、定时发表、改期
- ⚠️ 时间面板的小时点选偶发失效 → 脚本已内置「校验 + 重试 + 面板自动重开」

详见 `references/troubleshooting.md`。

## License

MIT
