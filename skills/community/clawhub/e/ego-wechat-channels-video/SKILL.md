---
slug: ego-wechat-channels-video
displayName: Ego WeChat Channels Video
summary: "Publish a WeChat Channels video draft with Ego Lite via ego-browser — login-check first (sessions expire fast), upload video, fill description/short title/topics/location/cover, save draft only. So..."
license: MIT
homepage: https://github.com/terryso/ego-skills/tree/main/skills/wechat-channels-video
name: wechat-channels-video
description: Publish a WeChat Channels video draft with Ego Lite via ego-browser — login-check first (sessions expire fast), upload video, fill description/short title/topics/location/cover, save draft only. Soft-fails if Channels is logged out and tells the human to scan QR inside Ego. Personal use. Use when the user asks to post to 视频号 / Channels assistant.
metadata:
  version: "0.2.1"
  requires:
    bins:
      - ego-browser
      - node
  ego:
    min_skill_guide: "2.1.0"
version: "0.2.1"
---

# wechat-channels-video

用 Ego Lite 会话在 [视频号助手](https://channels.weixin.qq.com) **保存视频草稿**。不点「发表」（扫码发表留给人）。

Save a WeChat Channels **draft** through Ego Lite. Never click Publish — QR publish is human-only.

## 先装 Ego

先装 **Ego Lite**，保证 `ego-browser` 在 `PATH`。缺失则 soft-fail / 告知用户去装，**不要**硬调浏览器。

## 每次发布前：登录闸门（必做）

视频号登录态**过期很快**。Agent **在上传或填表之前**必须跑：

```bash
node scripts/check-login.mjs
# 需要把窗口留给人扫码时：
node scripts/check-login.mjs --keep
```

| 退出码 | 含义 | Agent 做什么 |
|--------|------|----------------|
| `0` | 已登录 | 把 `login_tip` 告诉用户，继续流程 |
| `2` | 未登录 / 无 ego-browser | 展示 `how_to_login` / `how_to_login_zh`，**停**。请人在 Ego 扫码后再跑 check-login |
| `1` | 其它错误 | 报告 JSON `error`，不要假装已发布 |

详见 `references/login.md`。不要另做 cookie-healthcheck 技能。

## 输入（通用，无本机产品路径）

调用方提供视频与文案字段，见 `references/inputs.md`。本技能**不**写死任何 `~/…` 业务目录。

最少需要：本机 `video` 路径、`description`、`short_title`。可选：`tags`、`cover`、位置/原创/活动。

## CLI 薄脚本（稳定部分）

`ego-browser nodejs` 不转发 shell argv；`check-login` 已用临时 entry + `ego-browser nodejs -e` 包好。

```bash
# 仓库根目录
node skills/wechat-channels-video/scripts/check-login.mjs
node skills/wechat-channels-video/scripts/check-login.mjs --keep
node skills/wechat-channels-video/scripts/serve-file.mjs --file /absolute/path/to/video.mp4 --port 18765

# 已安装的技能目录里也可以用相对路径
node scripts/check-login.mjs
node scripts/serve-file.mjs --file /absolute/path/to/video.mp4 --port 18765
```

- **check-login**：唯一登录硬闸门；结束默认 `finish({ keep: [] })`（`--keep` 除外）。
- **serve-file**：给页面 `fetch` 用的本机 CORS 文件服务；打印 `{ url, bytes, port }`，SIGINT 结束。大视频不要 base64。

**不**把整段发表 UI 打成一个巨型脚本：wujie、坐标点击、封面 `waitForFileChooser` 需要 Agent 看 snapshot/截图。脚本负责可判定的登录与传文件；表单仍按下面 Agent 步骤。

## ego-browser API 速查

每次 `ego-browser nodejs` 是新进程；TaskSpace / Page 跨调用持久，JS 变量不持久。

| API | 说明 |
| --- | --- |
| `taskSpace(name\|id)` | 一个用户目标一个 space；记下 `spaceId` 复用 |
| `task.page("p1")` | 首屏用 goto 复用，别乱开页 |
| `page.snapshot()` | 观察（能看穿 open shadow）；**点击**在 wujie 内常被拦截 |
| `page.evaluate(fn, arg)` | 只收**一个** JSON 可序列化参数（长文案走这里） |
| `page.mouse.click(x, y)` | wujie 内弹层常用 |
| `page.waitForFileChooser()` | 封面唯一稳妥上传路径 |
| `task.handOff()` | 交给人扫码发表 / 当面登录 |
| `task.finish({ keep: [] })` | 收尾关 space；需人接着看时用 handOff，不要长期占机器 |

**关键**：snapshot 看得见 wujie shadow；ref/text 点击会报 intercepts pointer events。wujie 内动作用 `evaluate` 里 `.click()` 或坐标 `mouse.click`。

## Agent 流程（登录通过之后）

### 0. 路由到发表页

**不要**直接 goto `/platform/post/create`（懒加载白屏）。走 UI：

`首页 → 左栏「内容管理」→「视频」→ 右侧「发表视频」`

就绪：wujie 内文案出现「视频描述」「短标题」，且有隐藏 `input[type=file][accept*="video"]` 与「保存草稿」。

```js
const state = await page.evaluate(() => {
  const app = document.querySelector('wujie-app');
  if (!app?.shadowRoot) return { wujie: false };
  const t = app.shadowRoot.textContent || '';
  return {
    wujie: true,
    hasDesc: t.includes('视频描述'),
    hasShort: t.includes('短标题'),
    hasUpload: !!app.shadowRoot.querySelector('input[type=file][accept*="video"]'),
    hasSave: t.includes('保存草稿'),
  };
});
```

### 1. 上传视频

先起 `serve-file`（端口默认 18765），再在页面里 fetch + DataTransfer 注入隐藏 file input（视频组件未做 isTrusted 加固；封面做了）：

```js
const r = await page.evaluate(async (p) => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const input = root.querySelector('input[type=file][accept*="video"]');
  const resp = await fetch(p.url);
  const dt = new DataTransfer();
  dt.items.add(new File([await resp.blob()], p.name, { type: 'video/mp4' }));
  input.files = dt.files;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
  return 'injected ' + dt.files[0].size;
}, { url: 'http://127.0.0.1:18765/video.mp4', name: 'video.mp4' });
```

验证只看 DOM：出现「转发/赞/评论」预览卡、进度稳定 100%。`performance` resource **抓不到**上传 POST。上传中途不要填表；wujie 短暂 null 时等一会再探，**不要刷新**。

### 1.5 检查点：先存草稿

上传完成后**立刻**点一次「保存草稿」，再填描述/短标题/位置，最后再存。避免中途翻车重传大文件。

### 2. 描述 + 话题

描述是 `.input-editor`（非 contenteditable）。`execCommand`；文案从 evaluate 第二参数传入：

```js
await page.evaluate((p) => {
  const ed = document.querySelector('wujie-app').shadowRoot.querySelector('.input-editor');
  ed.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  document.execCommand('insertText', false, p.desc);
}, { desc });
await page.evaluate((p) => {
  const ed = document.querySelector('wujie-app').shadowRoot.querySelector('.input-editor');
  ed.focus();
  document.execCommand('insertParagraph');
  document.execCommand('insertText', false, p.tags);
  ed.blur();
}, { tags });
```

### 3. 短标题

真 `<input>`，必须 native setter；验证读 `input.value`（innerText 不含 input 值）。

**服务端硬限制**（实测多期，触发即红字警告，保存被拒）：

- **≤16 字**：超长直接拒（17 字实测被拒）。
- **符号白名单**：只有书名号、引号、冒号、加号、问号、百分号、摄氏度。
  - 全角逗号「，」→ 换空格（如「烂推荐看够了，自己搭一个」→「烂推荐看够了 自己搭一个」）。
  - 小数点会触发「特殊字符」警告：版本号里的 `6.1` 这类写法要改说法规避。
  - `|`、`#`、`@` 都不行：自带标题里的分隔符取主句（如「标题文字|栏目#066」→「标题文字」）。

填完后检查输入框下方有没有红字警告；有就改写后再保存。

### 4. 位置

默认常带城市。稳妥：`mouse.click` 打开 → snapshot/截图 → 点「不显示位置」→ **回读字段**确认。evaluate 坐标可能点到隐藏层。

### 5. 保存草稿（终点）

点「保存草稿」。成功信号：「已保存」+ 底部按钮变灰。再 goto 草稿箱核对。**草稿箱可见前不要离开编辑器**。

可选：声明原创、活动搜索（native setter 写搜索词；搜不到就「不参与活动」）。

#### 声明原创

真 checkbox（授权钥匙串行）。勾选后弹协议层：勾「我已阅读并同意…」→ 点层内「声明原创」确认按钮。两步都要坐标点击并回读 `input[type=checkbox].checked` 确认。

#### 活动搜索弹层

- 打开弹层点「不参与活动」字段；**弹层可能不弹**（点击被吞），探测 `input[placeholder*="搜索活动"]` 失败就重试 2–3 次。
- 搜索词用 **native setter + input/change 事件**（`keyboard.insertText` 间歇性失效）；**二次搜索前先清空**——native setter 是覆盖，但焦点点击后残留词会被追加成「AI科普AI科普」。
- 列表渲染后**截图引导点击**：弹层行序和 y 坐标每期都可能变（还见过偏移一行的渲染 bug），按截图上的可见坐标点，点完**回读活动字段**确认选中项。点错行（相邻活动）若主题也合适可接受，不必强改。
- 视口尺寸变化会让「滚到顶部再点开」的既有坐标失效——每次都要重新探测触发器坐标。

### 6. 封面（可选）

唯一稳妥：`waitForFileChooser()` + 可信点击「上传封面」+ `chooser.setFiles(<绝对路径>)`。合成 `input.files` / OS 文件框方案已实测失败。确认按钮转圈结束、预览不再回退默认帧后再存草稿。

### 7. 收尾

- 停掉 `serve-file`（释放端口）。
- 需要人发表：草稿箱 `handOff()`。
- 否则 `finish({ keep: [] })`，**不要**长期占 space。

## 避坑清单

1. wujie shadow：查询从 `wujie-app.shadowRoot` 起。
2. 直链 create 白屏：必须 UI 路径进入发表页。
3. wujie 内 ref/text 点击被拦截 → evaluate 或坐标点击。
4. 长文案只经 evaluate 参数传入。
5. 描述用 execCommand；短标题用 native setter。
6. 位置两段式坐标 + 回读验证。
7. 封面只能 waitForFileChooser。
8. 上传验证只看 DOM；上传后先存草稿。
9. 草稿落盘前不导航离开。
10. 登录页「加载失败」是红鲱鱼；handOff 让人扫码。
11. **每次发布前 check-login**；exit 2 必须停。
12. 发表是人工终点；本技能只到草稿。
13. 短标题 ≤16 字 + 符号白名单（见 §3）；触发红字就改写，别硬保存。
14. 原创两段式（勾选 + 协议层确认），活动弹层截图引导 + 回读（见 §5）；「已保存」标签偶尔错过时机，草稿箱核对是最终事实。

## 测试

```bash
npm test
```
