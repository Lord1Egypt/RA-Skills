# 视频号自动发布 · 踩坑清单

这份是**干活前必读**。每一条都是实际调试中撞出来的，跳过必重踩。

---

## 1. 为什么不用 playwright

Chrome 153 下 `playwright.chromium.connectOverCDP()` 握手会**卡死不返回**。
改用 `ws` 直连 browser endpoint（`/json/version` 的 `webSocketDebuggerUrl`），
自己发 `Target.createTarget` / `attachToTarget` / `Runtime.evaluate`。

## 2. Host 头必须带 `:9222`（最容易浪费一小时的一条）

Chrome 是**按请求的 Host 头**生成 `webSocketDebuggerUrl` 的。
发 `Host: 127.0.0.1` 会拿到 `ws://127.0.0.1/devtools/...`（没有端口）→ ws 去连 80 → `ECONNREFUSED`。
curl 能连上是因为它发的是 `Host: 127.0.0.1:9222`。

```js
http.get({ host: '127.0.0.1', port: 9222, path, headers: { Host: '127.0.0.1:9222' } })
```

## 3. sessionId 与 flatten

- 浏览器级命令的 `sessionId` 必须是**字符串或省略**，传 `null` 会被拒：
  `Message may have string 'sessionId' property`
- `Target.attachToTarget` 必须 `flatten: true`，否则子帧走另一个 session，报
  `Session with given id not found`

## 4. 后台标签不布局

后台 tab 的元素 `getBoundingClientRect()` 全是 0、`offsetParent` 为 null，点击静默失效。
必须 `Target.activateTarget` 把标签提到前台。

## 5. 新 UI：发布表单藏在 0×0 的 iframe 里（最关键）

`https://channels.weixin.qq.com/platform/post/create` 现在是一个「视频号助手」hub
（左侧导航：首页/内容管理/视频/图文/音乐/音频/草稿箱…），
**真正的发布表单在一个 `src=empty.html` 的 iframe 的 contentDocument 里**。

- 靠 iframe URL 匹配定位已经失效（旧的是 `/micro/content/post/create`，现在是 `empty.html`）
- 该 iframe **宽高为 0×0** → 真实鼠标坐标完全失效，只能用合成 DOM 事件
  （`el.click()`、native value setter + `dispatchEvent`）
- 定位方式改为**运行时探测**：哪个 iframe 的 contentDocument 里有 `input[type=file]`，哪个就是表单

```js
const FIND_FORM = `(function(){var fs=Array.from(document.querySelectorAll('iframe'));
for(var i=0;i<fs.length;i++){var d=null;try{d=fs[i].contentDocument;}catch(e){}
if(d&&d.querySelector('input[type=file]'))return fs[i];}return null;})()`;
```

## 6. 绝不缓存 executionContextId

监听 `Runtime.executionContextCreated` 把 contextId 存起来复用，会在页面重绘后失效，报：

```
Cannot find context with specified id  /  Invalid parameters
```

**正确做法**：`Runtime.evaluate` **不带 contextId**（Chrome 默认用顶层框架），
全程从顶层经 `iframe.contentDocument` 操作表单（同源，可读写、能触发 React 事件）。

## 7. 文件上传别指望 file chooser

0×0 的 iframe 里调 `input.click()` **不会**触发文件选择框，`Page.fileChooserOpened` 永远不来。

正确做法：用 `Runtime.evaluate`（**不要** returnByValue）拿到 input 的 `objectId`，
再 `DOM.setFileInputFiles({ objectId, files: [...] })`：

```js
const r = await send(ps, 'Runtime.evaluate', { expression: '...return input...' }); // 无 returnByValue
await send(ps, 'DOM.setFileInputFiles', { objectId: r.result.objectId, files: [filePath] });
```

这招实测稳定（ep24 100MB+ 一次成功）。

## 8. 运行环境（本机）

```bash
# Chrome 需带远程调试端口启动（独立 profile，别污染常用浏览器）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir=/Users/jx/ChromeAutomation &

# 跑脚本前必须清代理，否则 :9222 的流量会被沙箱/代理劫持到 :80
unset http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY NODE_OPTIONS
export NO_PROXY='127.0.0.1,localhost'
# node 用受管版本（版本号会变，别写死，先列出来再取）
NODE=$(ls -d /Users/jx/.workbuddy/binaries/node/versions/*/bin/node | head -1)
NODE_PATH=/Users/jx/.workbuddy/binaries/node/workspace/node_modules $NODE cdp-publish.js ...
```

Bash 工具里跑需要 `dangerouslyDisableSandbox: true`（沙箱会把 9222 流量劫持）。

## 9. 定时窗口：最远 14 天

视频号定时发表只能选**未来 14 天内**的日期。超出会选不中（不会报错，只是点不动）。
脚本已内置校验：目标日距今 >14 天直接以退出码 4 中止，**绝不误发**。

批量排期策略：按「今天 +14 天」滚动窗口**分批**做，不能一次排到底。

## 10. 原创声明的规则（业务红线）

- 原创**只能在发布时声明**；已发布条目没有补声明入口
- 超过 6 个月的条目，连「修改并重新发表」都没有 → 只能**删旧重发**
- 删旧会丢失已有播放/点赞数据，**不可逆**，必须用户明确确认
- 重复内容重发，原创审核可能判「非首发/重复」不通过

核查原创状态：`node check-original.js`（走 `post_list` 接口读 `originalInfo.isDeclared`）

## 11. 列表接口（原创核查用）

```
POST https://channels.weixin.qq.com/micro/content/cgi-bin/mmfinderassistant-bin/post/post_list
```

`pageSize` 改 100 可一次拉全部（默认 20）。字段：`objectId` / `createTime`(unix) /
`readCount` / `likeCount` / `originalInfo.isDeclared` / `status`。
**没有视频时长字段**（只有 `avgPlayTimeSec` 平均播放时长），所以不能靠时长反查源文件。

## 12. 当前已知卡点（未完全打通）

- ✅ 已验证：表单定位、文件上传、短标题、描述、合集选择
- ⚠️ **未验证**：定时日历面板展开（`.weui-desktop-picker__dd` 在 0×0 iframe 里不吃合成 click）、
  原创声明弹窗闭环、最终「发表」按钮的弹窗链
- 即发表（不定时）可绕过日历面板；若定时必须，需先修日历面板展开

修改日历相关逻辑时，先把 `references/` 里这份清单读一遍再动手。

## 13. 定时发布必须「回读校验日期」+「回读校验时间」

发布/改期脚本最容易出的**静默失败**：日期点选偶发不生效，但日志里后续步骤全部成功，
结果视频按**旧日期**排出去。真实案例：一批 10 条里有 2 条日期没改成功，直到拉服务端
`post_list` 对账才发现。

**防御写法（必须在点「发表」之前）**：

```js
const readDate = () => frame.evaluate(() => {
  const it = Array.from(document.querySelectorAll('.form-item'))
    .find(x => (x.querySelector('.label') || {}).textContent?.trim().startsWith('发表时间'));
  if (!it) return null;
  const inp = Array.from(it.querySelectorAll('input')).find(i => /^\d{4}-\d{1,2}-\d{1,2}/.test(i.value));
  return inp ? inp.value : null;   // ⚠️ 值形如 "2026-11-01 07:00"，带时间！
});
const normDate = (v) => {           // ⚠️ 别用 split('-')，末段 "01 07:00" 会变 NaN
  const m = String(v || '').match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])].join('-') : '';
};
// 不匹配就重开面板 → 重新翻月 → 重新点日，最多 5 次；仍不匹配直接 exit(1)，不要带病发布
```

时间同理（`input` 值 /^HH:mm/），已内置重试；日期同理处理。

**批量脚本的日期起点**：分多批跑时，起始日期必须显式传参并用 `DRY=1` 预演
（默认值会让第二批整体错位一天，造成同一天两条）。

## 14. 已定时条目的「改期」比「删了重传」划算

列表行悬浮 →「修改并重新发表」打开的编辑页会**保留**封面、标题、描述、合集、原创勾选、
定时模式，只改日期时间即可，约 30s/条；重新上传约 45s/条且会产生重复条目需要清理。
