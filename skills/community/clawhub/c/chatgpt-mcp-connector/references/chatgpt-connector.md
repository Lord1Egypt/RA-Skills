# ChatGPT 连接器与授权（阶段 6）

> 阶段 6 = 在 ChatGPT 建自定义连接器并完成 OAuth 授权。
> 主流程见 SKILL.md；本文件是完整细节。

> 🤖 **本阶段默认由 agent 用 `browser-harness` 驱动浏览器自动完成** ——
> 开开发者模式、建连接器、填 Owner password 授权，全部由 agent 执行，
> **不需要用户自己填表**。完整可执行步骤见下文「🤖 自动化执行」一节。
>
> 只有两件事必须停下来交给用户：
> ① **首次**允许 Chrome 远程调试（一次性点击，之后 daemon 复用那条连接）；
> ② ChatGPT **未登录**时由用户登录（登录墙 —— 密码 / MFA / 账号选择一律不得代填）。
>
> 若环境里没有 browser-harness（或用户明确要求自己动手），走下文「完整步骤（人工兜底路径）」。

## 两条路径怎么选

| 情形 | 走哪条 |
| --- | --- |
| 默认 | **🤖 自动化执行** —— agent 用 browser-harness 全程操作 |
| 没装 browser-harness、或安装/连接修不好 | 人工兜底路径（把值列清楚，让用户自己填） |
| 用户明确说「我自己来」 | 人工兜底路径 |
| 自动化中途撞上登录墙 / MFA / consent | **停下**，切人工完成那一步，再回到自动化 |

## ⚠️ 铁律：Settings 只开开发者模式，连接器必须在「插件」页建

这两处表单字段长得**一模一样**（名称 / 描述 / URL / OAuth 三选项），走错了提交就报
`Something went wrong. If this issue persists please contact us through our help center.`
**绝大多数这个报错都是入口走错**，不是服务端问题。

## 🤖 自动化执行（browser-harness）

**默认路径。** agent 自己驱动浏览器把 A–F 六步跑完，用户只在两处被叫到（A 的首次点击、B 的登录墙）。

调用形态（heredoc，helpers 已预导入）：

```bash
browser-harness <<'PY'
print(page_info())
PY
```

### A. 前置：确认能连上浏览器（唯一必点一次的地方）

```bash
browser-harness --doctor
```

看两行就够：

- `[ok] chrome running` —— 浏览器在跑
- `active browser connections` —— **为 0 说明还没建立连接**，通常就是远程调试没开

没开时 harness 会打开 `chrome://inspect/#remote-debugging`，此时**停下来请用户**勾选
"Allow remote debugging for this browser instance" 并点 Allow。

> 🙋 **需要你操作**：浏览器刚打开一个调试设置页，请勾选「Allow remote debugging for this browser instance」
> 并点 Allow，然后告诉我。这一步**只需要做一次**。

⚠️ **不要在循环里重试**：Chrome 对每个新连接都弹一个新对话框，反复重试等于反复骚扰用户。
daemon 会长期持有那条连接，所以这个点击是一次性的。

`Browser Use cloud auth` 那行报 FAIL 是**正常的**，本地 Chrome 用不到云端浏览器。

### B. 登录墙自检（第二处可能要叫用户）

```python
new_tab("https://chatgpt.com/")
wait_for_load()
print(page_info())
```

落到登录页而不是 ChatGPT 主界面 → **停下来问用户**。
browser-harness 的规则是「登录墙必须停」：唯一例外是 Chrome **已登录**时可以直接走 SSO，
但**密码、MFA、consent、账号选择一律不得代填**。

> 🙋 **需要你操作**：ChatGPT 当前未登录，请在浏览器里登录后告诉我，我接着往下走。

### C. 打开开发者模式（只需一次，之后可跳过）

设置 → 账户安全与登录 → 开发者模式。
开完**回读一次开关状态**再继续 —— 视觉上「点到了」不等于「开上了」。

### D. 建连接器

**用深链接直达新插件弹窗**，省掉在列表页找按钮那一步：

```python
new_tab("https://chatgpt.com/plugins#settings/Connectors?create-connector=true&redirectAfter=%2Fplugins")
wait_for_load()
```

⚠️ 反例：`goto_url` 直达 `/plugins/plugin_xxx` 这类 SPA 详情页**渲染不出内容**，
必须回列表页用坐标点击走客户端路由。

填表字段：

| 字段 | 选择器 / 值 |
| --- | --- |
| 名称 | `input[name=custom-connector-name]` → 自定义名（如 `DevSpace`） |
| 描述 | `input[name=custom-connector-description]`（可选） |
| 连接方式 | 选 **服务器 URL**（不是「隧道」） |
| 服务器 URL | `input[name=custom-connector-url]` → `https://<隧道域名>/mcp`，**必须带 `/mcp`** |
| 身份验证 | `select` → **`OAUTH`**（另两个：`无身份验证` / `混合`） |
| 确认框 | **必须勾选**，否则 `创建` 永远是 disabled |

> 🔎 **提交前的自检信号（很值钱）**：填完 URL 后，「高级 OAuth 设置」按钮的文案会从
> 「输入有效的 MCP 服务器 URL 以查看已发现的 OAuth 设置」（disabled）
> 变成「**查看已发现的 OAuth 设置**」（enabled）—— 这说明 OAuth 发现成功。
> **文案没变就别点创建**：那意味着 URL 少了 `/mcp`、隧道不通或服务没起，先修再提交。
> 这一步能在**提交之前**拦下绝大多数 `Something went wrong`。

React 受控输入必须走原生 setter + 派发事件，直接 `el.value = v` **无效**：

```python
js("""
const set = (sel, v) => {
  const el = document.querySelector(sel);
  if (!el) return 'MISS ' + sel;
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  setter.call(el, v);
  el.dispatchEvent(new Event('input',  { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
  return 'OK ' + sel;
};
window.__r = [
  set('input[name=custom-connector-name]', 'DevSpace'),
  set('input[name=custom-connector-url]',  'https://<隧道域名>/mcp'),
];
""")
print(js("JSON.stringify(window.__r)"))
```

（写法上用 `js("""...""")` 而不是 f-string，免得 JS 里的花括号要和 Python 转义打架；
需要注入 Python 变量时再单独拼接。）

点「创建」→ **等 ≥6 秒**再判定：提交是异步的，弹窗稍后才关，**等不够会误判成失败**。

```python
click_at_xy(x, y)      # 坐标点「创建」
import time; time.sleep(6)
print(page_info())
```

### E. OAuth 授权

提交后 ChatGPT 自动跳到 `https://<隧道域名>/authorize?...&redirect_uri=https://chatgpt.com/connector/oauth/...`
—— **域名从 chatgpt.com 变成了隧道域名**，这是个关键转折点。

Owner password 就地读取、就地填入，**全程不 print**：

```python
import json, os, pathlib

cfg_dir = pathlib.Path(os.environ.get('DEVSPACE_CONFIG_DIR') or (pathlib.Path.home() / '.devspace'))
auth = json.loads((cfg_dir / 'auth.json').read_text(encoding='utf-8'))
token = auth.get('ownerToken') or auth.get('owner_token')
assert isinstance(token, str) and token, 'auth.json 里没有 ownerToken，先跑 devspace-bootstrap check'

# token 只出现在这一条 IIFE 表达式里，不 print、不写日志、不进命令行参数
result = js(
    "(() => {"
    "  const el = document.querySelector('input[type=password]');"
    "  if (!el) return 'MISS password input';"
    "  const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;"
    "  s.call(el, TOKEN);"
    "  el.dispatchEvent(new Event('input',  { bubbles: true }));"
    "  el.dispatchEvent(new Event('change', { bubbles: true }));"
    "  return 'OK len=' + el.value.length;"     # 只回长度，绝不回值
    "})()".replace('TOKEN', json.dumps(token))
)
print(result)      # 期望 OK len=43
```

> 🔐 三条硬约束（写进代码里，不靠自觉）：
> 1. **绝不 print / 回显 / 写日志**这个值 —— 回读校验只回**长度**（本机应为 `43`）；
> 2. **绝不当命令行参数传**（会进 shell 历史与进程列表）—— 在同一段 heredoc 里就地读、就地填；
> 3. **绝不让用户把它贴进聊天** —— 人工路径同样禁止这一点。

Windows 上路径是 `%USERPROFILE%\.devspace\auth.json`；`DEVSPACE_CONFIG_DIR` 可覆盖配置目录。
（实测 `~/.devspace/auth.json` 是 `{"ownerToken": "<43 字符>"}`，`config.json` 同目录；
`~/.local/share/devspace/` 放的是 `devspace.sqlite*` 状态库，别找错地方。）

然后点 `Authorize DevSpace`。

### F. 验证

服务端日志见下节「成功判据」。UI 侧插件页「已安装」应出现 `DevSpace`。

**这一阶段有两个必须用日志、不能只看 UI 的判据**：

- `userAgent: openai-mcp/1.0.0` + `200` + `mcp_session_created` → 连接真的建立了
- `tool_call ... success:true` → ChatGPT 真的在读写你本机文件

### 通用技巧与坑（自动化适用）

- **每次 `browser-harness` 调用都会重置当前标签页** → 每个脚本开头必须重新选标签：

  ```python
  for t in list_tabs():
      if <匹配条件>: switch_tab(t["targetId"]); break
  ```

  注意授权流程会把标签页从 `chatgpt.com` **导航到隧道域名**，
  所以匹配条件**不能写死 `chatgpt.com`**，否则会误操作成别的标签页。
- **点击一律用坐标 `click_at_xy()`，不要用 JS `.click()`** —— JS 点击对 ChatGPT 的 React
  按钮经常无效；坐标点击能正确触发（勾选 checkbox、提交都能 work）。
- **坐标怎么拿**：优先 DOM 枚举（`js(...)` 扫 `button,a,[role=button]` 拿 `getBoundingClientRect`），
  比 AX 树稳 —— `DOM.getBoxModel` 用 AX 给的 `backendNodeId` 会报 `Invalid parameters`。
  （browser-harness 的通用建议是优先用 AX 树，但对 ChatGPT 这套 UI 实测 DOM 枚举更可靠。）
- **坐标超出视口**（`y > ph`）会点空：先 `el.scrollIntoView({block:'center'})` 再重新量。
- **想看前端到底发没发请求**：给页面 `window.fetch` 打桩记录到 `window.__netlog`，
  比只看服务端日志更快定位。
- **别用 `goto_url` 走 SPA 内部路由**（见 D 步的反例）。
- 每次填完/点完，都要用一次 `js(...)` 或 `page_info()` **回读**确认，不要假设操作生效了。

## 完整步骤（人工兜底路径）

1. 设置 → **账户安全与登录** → 打开 **开发者模式**（只需一次）
2. 打开 `https://chatgpt.com/plugins`
3. 点右上角 **`创建应用`** 按钮（aria-label=`创建应用`；1904 宽视口下约 `(1448, 135)`）
4. 提交后 URL 变为
   `https://chatgpt.com/plugins#settings/Connectors?create-connector=true&redirectAfter=%2Fplugins`
   —— 这个深链接可当作「直接打开新插件弹窗」的快捷入口
5. 「新插件」弹窗填表：

   | 字段 | 值 |
   | --- | --- |
   | `input[name=custom-connector-name]` | 自定义名字，如 `DevSpace` |
   | `input[name=custom-connector-description]` | 任意描述（可选） |
   | 连接方式 | 选 **`服务器 URL`**（另一个是 `隧道`） |
   | `input[name=custom-connector-url]` | `https://<域名>/mcp`，**必须带 `/mcp`** |
   | 身份验证 `select` | 保持 **`OAUTH`**（另两个：`无身份验证` / `混合`） |
   | checkbox | **必须勾选「我了解并希望继续」，否则 `创建` 永远 disabled** |

6. **可视信号**：填完 URL 后，`高级 OAuth 设置` 按钮文案从
   「输入有效的 MCP 服务器 URL 以查看已发现的 OAuth 设置」（disabled）
   变成「**查看已发现的 OAuth 设置**」（enabled）→ OAuth 发现成功。
7. 点 `创建` → **等 ≥6 秒**（提交异步，弹窗随后才关；等不够会误判为失败）
8. ChatGPT 自动跳 `/authorize?...&redirect_uri=https://chatgpt.com/connector/oauth/...`
   → 填 **Owner password**（`~/.devspace/auth.json` 的 `ownerToken`，字段名 `owner_token`）
   → 点 `Authorize DevSpace`

   > 🔐 **Owner password 的两条底线**（人工路径与自动化路径都适用）：
   > ① **绝对不要让用户把它贴进聊天/日志** —— 需要时只告诉他「去 `~/.devspace/auth.json` 里看」；
   > ② 走自动化时由 agent **就地读取 auth.json 并直接填入表单**，不 print、不回显、
   >    不作为命令行参数传递（会进 shell 历史与进程列表）。

9. 302 回跳 `https://chatgpt.com/connector/oauth/<id>?code=...&state=...` → 完成

## 成功判据（服务端日志，`userAgent` 是关键区分字段）

```
POST /mcp  → 401   Python/3.14 aiohttp       ← OpenAI 后端预检，读 WWW-Authenticate
GET  /     → 200   aiohttp                   ← oauth-protected-resource/mcp
GET  /     → 200   aiohttp                   ← oauth-authorization-server
POST /     → 201   aiohttp                   ← ★ DCR 动态客户端注册成功（219 字节）
POST /     → 302   Chrome                    ← ★ Owner 密码通过，带 code 重定向
POST /mcp  → 200   openai-mcp/1.0.0          ← ★ 正式客户端建立 MCP 会话
mcp_session_created  sessionIdPrefix ...
```

**最终判据：`userAgent: openai-mcp/1.0.0` + `200` + `mcp_session_created`。**
随后会出现真实业务日志，例如：

```
{"event":"tool_call","tool":"read","workspaceId":"ws_a16dfaff82","path":"crates/core/src/...","success":true}
```

**认这个才是真通了** —— 说明 ChatGPT 真的在读写你本机文件。

UI 侧：插件页「已安装」出现 `DevSpace`，详情页显示 `在聊天中试用 / 版本 x.y.z`。

> 日志中间件的 `path` 字段对 well-known 路由记录**不准**（返回 200 的正确 JSON 却记成 `GET /`），
> 排查时别只信这个字段。

## 在对话里用它

新开一个对话，从工具菜单挂上 DevSpace，然后给**绝对路径**（别让它猜）：

```
用 DevSpace 打开本地工作区：D:\projects\my-app\<项目名>          （Windows）
用 DevSpace 打开本地工作区：/home/you/projects/my-app/<项目名>    （macOS / Linux）

只读，不要改文件、不要跑有副作用的命令。
先读根目录的 AGENTS.md / CLAUDE.md（如果存在），然后告诉我：
1. 技术栈；2. 启动与测试命令；3. 当前 git 状态；4. 你实际读了哪些文件。
```

> 路径必须是**本机原生写法**：Windows 用反斜杠（`D:\...`），macOS / Linux 用正斜杠（`/home/...`）。
>
> ⚠️ **不要给 `/mnt/c/...` 这类 WSL 路径**。DevSpace 是 Windows 进程，它把开头的 `/` 当成**当前盘**的根，
> 于是 `/mnt/f/projectL` 被解析成 `C:\mnt\f\projectL` → 报
> `Path is outside allowed roots: /mnt/f/projectL`（报错回显的是**原始输入**，不是解析结果，很容易看歪）。
> 这种路径通常是从 WSL 里的 `pwd -P` / `git rev-parse --show-toplevel` 抄来的 ——
> **取路径要在 PowerShell / cmd 里取**，别在 WSL 里取。
>
> ⚠️ **junction / symlink 会把路径"换个地方"**。若 `F:\chatgpt_work\projectL` 是指向 `F:\projectL` 的 junction：
> 交**逻辑路径** → 字符串比较通过（白名单看着"在根内"，其实读写的是根外）；
> 交**真实路径** → 被拒（`F:\projectL` 不在白名单里）。
> 想把真实路径也用起来，就把它一起加进 `allowedRoots`。先 `realpath` 看一眼目标落在哪。

同一会话内 `open_workspace` 返回的 `workspace_id` 要一直复用；
白名单内可以自由切换/打开多个 workspace（各有独立 `workspace_id`）。

## 收尾

- **`devspace serve` 必须常驻**；agent 会话结束后需在终端手动起。
  开机自启按平台选：Windows 用任务计划程序 / `nssm`，macOS 用 `launchd`（`~/Library/LaunchAgents/*.plist`），
  Linux 用 `systemd`（user 或 system unit）。启动命令一律指向**绝对路径的 `dist/cli.js`**：
  `node "$(npm root -g)/@waishnav/devspace/dist/cli.js" serve`（三平台通用）。
- 用完关公网入口：`tailscale funnel reset`。
- ChatGPT 侧：连接器详情页可以 **Refresh** 重新拉取工具列表；改完 URL 记得 Refresh + 新开对话。
- 插件建好了但新对话里看不到工具 → 打开连接详情 → **Refresh** → 再新开一个对话。
