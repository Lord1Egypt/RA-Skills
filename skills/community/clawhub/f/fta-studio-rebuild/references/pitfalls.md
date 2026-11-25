# 已踩过的坑（按症状查）

遇到"改了没生效""点了没反应""找不到文件"这类现象，先按下表核对，不要凭直觉改代码。

---

## 1. 双击节点不折叠 / 点击类交互失效

**症状**：绑定 `dblclick` 后，真实双击毫无反应，但单测"通过"。

**根因**：`pointerdown` 处理器里调用了 `render()`，而 `render()` 执行 `svg.innerHTML = ''` 重建 DOM → 第一次点击的元素被销毁 → 第二次点击落在新元素上 → 浏览器判定两次点击不在同一元素 → **原生 `dblclick` 不触发**。

**修复**：在 `pointerdown` 里自己判定（同 id + 420ms 内），见 `frontend.md` §4。

**测试陷阱**：`element.dispatchEvent(new MouseEvent('dblclick'))` 会绕过真实点击序列，**必然假通过**。必须用 CDP：
```js
await cdp.send('Input.dispatchMouseEvent', { type:'mousePressed',  x, y, button:'left', clickCount:1 });
await cdp.send('Input.dispatchMouseEvent', { type:'mouseReleased', x, y, button:'left', clickCount:1 });
await cdp.send('Input.dispatchMouseEvent', { type:'mousePressed',  x, y, button:'left', clickCount:2 });
await cdp.send('Input.dispatchMouseEvent', { type:'mouseReleased', x, y, button:'left', clickCount:2 });
```

---

## 2. 双击 .bat 满屏 `'o.'` `'m'` `'ershell'` 不是内部或外部命令

**根因**：`.bat` 用了 **LF** 换行（编辑器/写文件工具默认 LF），cmd.exe 要求 **CRLF**，于是按错误字节边界切行，把 `echo.`、`powershell` 劈成碎片。

**修复**：统一规范化为 ASCII + CRLF，见 `windows-packaging.md` §1。

---

## 3. 报 `Node.js runtime not found`（Node 明明装了）

两个原因叠加：

1. `dir /b /s "...\versions\*\node.exe"` —— `dir` 的通配符**只能放路径最后一段**，放中间静默返回空，又被 `2>nul` 吞掉。
2. 双击启动时 **PATH 里没有 node**（托管运行时只注入 WorkBuddy 自己的进程）。

**修复**：四段式发现（枚举版本目录 → PATH → 显式路径 → 常见安装位置），见 `windows-packaging.md` §2。

---

## 4. 只画出一个事件，其余节点不显示；选中/右键全失效

**症状**：顶事件下方有箭头，但箭头末端没有方框，也点不中。

**根因**：`render()` 里把**几何描述对象**当成 DOM 元素用了：

```js
const shape = eventShapePath(n.type, w, h);   // { kind, d }
const shapeEl = el('path', {...}, g);         // 真正的 SVG 元素
shape.addEventListener('pointerdown', ...);   // ❌ TypeError
```

异常让 `render()` 在**画完第一个节点后中断**：连线在前一轮循环已画完（所以有箭头），门在节点循环之后（所以没有门），三个事件监听就在崩的那一行（所以点不中）。

**修复**：绑到 `shapeEl`。**判断依据**：打开 DevTools 看 Console 是否有红色异常 —— 这类"渲染到一半"的现象基本都是异常中断。

---

## 5. 复制到桌面后打不开（`ERR_CONNECTION_REFUSED`）

**根因**：`cd /d "%~dp0"` + 相对路径 `src\launch.mjs`。文件在桌面时 `%~dp0` = 桌面，`src\launch.mjs` 不存在 → node 秒退 → 端口无人监听。

**修复**：显式拼接 `%~dp0app\src\launch.mjs`，或多路径探测（同目录优先，其次固定项目路径）。

**排查口诀**：`ERR_CONNECTION_REFUSED` = **端口没有监听**（服务没跑）；代理问题是超时/代理错误，两者别混。

---

## 6. 改了代码但页面没变

**根因**：静态资源没有版本号，且服务端没下发 `Cache-Control`，浏览器用缓存。

**修复**：`app.js?v=NN` 每次改动递增 **且** 服务端加 `no-store, must-revalidate`。

---

## 7. 关掉黑窗口服务就没了 / 端口从 8777 一路蔓延到 8778、8779

**根因**：前台运行 + 没有单实例识别，反复双击就不断开新端口，旧标签页指向已死端口。

**修复**：
- 分离式后台启动（关窗不停服务）
- 启动前先探测 `/api/capabilities`，若已是自己则**复用**而不是新开
- 端口被占用时顺延，并把**实际端口**打印出来

---

## 8. 折叠顶事件无效（徽标出现但节点一个不少）

**根因**：`computeLayout` 里写了 `n.collapsed && n.id !== rootId`，把根节点排除在折叠之外。

**修复**：去掉 `!== rootId` 判断。改完用真实双击验证节点数变化（12 → 1）。

---

## 9. 用户说"改了没生效"，其实跑的是安装副本

**症状**：代码明明改了、`present_files` 打开的样例也是新效果，但用户截图还是旧界面（旧文案、旧行为）。

**根因**：用户在跑 `%LOCALAPPDATA%\FTA Studio\app`（便携安装副本），而你改的是项目源码目录。两者完全独立。

**修复**（每次改完必做）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill>/scripts/sync-installed.ps1 `
  -SourceDir <项目目录> -Restart
```

验证要点：`app.js` 的字节数/内容包含新符号、`index.html` 里的 `?v=NN` 已递增、服务已重启。**不要**只靠"我本地跑通了"。

---

## 10. 多个分页点全被切到同一页

**症状**：设了"制动回路失效"和"踏板行程传递失效"两个分页点，两页都跑到第 2 页；用户期望第 2 页、第 3 页。

**根因**：旧 `paginateBanded` 用"前沿推进"，把本页命中的所有分页点合并成一个 `nextFrontier`，于是它们共用一个下一页。

**修复**：改成递归 `expandPage(tops, contFrom)` —— 每个分页点各自递归开一页；同页多个分页点按 **DFS 先序**排序后依次开页；`continuedFrom` 记为真正的父页号。见 `SKILL.md` §4。

**回归断言**：双分页点必须得到 3 页，且 P2/P3 的 `continuedFrom === 1`。

---

## 11. 重构分页后 A4 虚线标注全没了

**症状**：分页页数、页顶事件都对，但导出图里虚线框旁边的「⤓ 分页 → 第 N 页」不见了。

**根因**：重写 `expandPage` 时漏了 `page.breakNodes = [...new Set(hitBreaks)]`——页对象初始化成 `breakNodes: []` 后就再没赋值，`buildBandedView` 的 `breakMarkerIds` 因此恒为空。

**教训**：页对象的每个字段在重构时都要确认"谁写、谁读"。**页数对 ≠ 记号对**，两者要分别断言。

---

## 12. A4 页码标注统一写成了 `p.index + 1`

**症状**：第 1 页有两个分页点分别指向第 2、3 页，但两个标注都印成「→ 第 2 页」。

**根因**：`renderA4HTML` 里按"下一页 = index+1"的假设生成标注；一个分页点独占一页时才成立。

**修复**：先建 `pageOfId`（遍历所有页累积，后面的页覆盖前面的），再逐分页点查真实目标页；页顶承接事件的来源页用 `page.continuedFrom`。

---

## 13. PowerShell 工具里"服务启动后立刻就没了"

**症状**：上一条命令 `Start-Process` 起了服务，下一条命令 `Invoke-WebRequest` 直接 `ECONNREFUSED`。

**根因**：工具调用结束时回收它 spawn 的后台进程。

**对策**：
- **"启动服务 + 验证"必须写在同一条命令里**；
- `Start-Process -WorkingDirectory` 已指向 `app` 目录时，参数写 `src\cli.mjs`，**不能**再带 `app\` 前缀（否则秒退）；
- 无头浏览器脚本偶尔 `exit -1` 且无输出 → 是 Chrome 启动时序问题，直接重跑。

---

## 14. 沙箱拒绝删除临时目录

**症状**：CDP 脚本里的 `fs.rmSync('D:\\tmp\\xxx-profile', { recursive: true })` 被沙箱/用户拒绝，整条命令不执行。

**对策**：用带时间戳的一次性 profile 目录（`` `D:\\tmp\\cdp-${Date.now()}` ``），**不做删除**，让系统自己回收。别在自动化脚本里写递归删除。

---

## 通用排查顺序

1. 浏览器 Console 有没有红色异常？（有 → 先修异常，八成是渲染中断）
2. 端口有没有在监听？（`netstat -ano | findstr :8777`）
3. 拿到的 HTML/JS 是不是新版本？（`curl` 看 `?v=`）
4. **用户跑的是不是你改的那一份？**（见第 9 条：源码 vs `%LOCALAPPDATA%\FTA Studio`）
5. 分页类问题：页数对但记号不对 → 查 `page.breakNodes` 有没有赋值（第 11 条）；页码错 → 查是不是偷懒用了 `index+1`（第 12 条）
6. 只有在真实交互下才复现的问题 → 用 CDP 真实鼠标事件复测，不要用 `dispatchEvent`
7. 改完必须跑：`run-tests.mjs` + `test-new-features.mjs` + `_jump.mjs` + 浏览器验证
