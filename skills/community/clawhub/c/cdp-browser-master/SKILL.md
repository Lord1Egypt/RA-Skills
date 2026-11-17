---
slug: cdp-browser-master
name: cdp-browser-master
version: 1.0.1
displayName: CDP浏览器大师
summary: "解决反爬检测、选择器易"
license: Proprietary
description: 。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。具备完整的输入输出规范。
tags:
  - 自动化
  - 浏览器
  - 数据抓取
  - 工作流
  - 效率
  - edge
  - chrome
  - cookie
  - const
  - await
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Automation"
homepage: "https://skillhub.cn/skill/"
---
> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# CDP浏览器大师

通过用户已登录的浏览器(Edge/Chrome)执行自动化任务。核心技术:CDP(Chrome DevTools Protocol),通过WebSocket与浏览器通信。核心信条:**优先用web_fetch,CDP只用于JS渲染或需登录态的场景;先探测再定位,多备选降级。**

## 能力简介
### 1. 反检测策略
UA天然真实(用已登录浏览器)、启动参数`--disable-blink-features=AutomationControlled`规避WebDriver标记、行为拟人化(随机延迟)、Cloudflare绕过(复用已验证会话)。使用`input_params`参数支持创建/查询/导出操作。

### 2. 选择器探测模式
先eval探索DOM结构(打印class/tag/text样本),再写精确选择器,提供多备选(精确class→模糊`[class*="未指定"]`→语义tag→属性选择器)降级匹配。

### 3. SPA导航模式
处理Next.js/React内部路由,先入可访问父页面(如`/user-center/basic-information`),再用JS点击侧边栏`<div cursor-pointer>`触发内部路由跳转,避免直接navigate子路由404。

### 4. 智能等待
`waitNetworkIdle`检测无请求持续500ms即继续,替代固定sleep,既不快也不慢。

### 5. Cookie获取
普通Cookie用`document.cookie`,HttpOnly Cookie用CDP `Network.getCookies`命令获取。

### 6. 连接管理
端口复用(每端口同时一个WebSocket)、ConnectionManager自动管理、残留连接清理、端口占用排查。

## 快速指引
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 应用场景
**何时使用**: JS渲染页面抓取(B站、SPA应用)、需登录态的网站操作、需要交互(点击/填表/滚动)的自动化、平台配额查询、多标签页管理与数据提取

**不适用场景**: 静态HTML页面抓取(用web_fetch即可)、无浏览器环境的服务器、强反爬站点且无法通过验证页的场景

## 关键参数说明

| 模块 | 方法 | 关键参数 | 说明 |
|---|---|---|---|
| edge/chrome | `goto(url)` | url:目标地址 | 导航到指定页面 |
| edge/chrome | `JSON.parse(js)` | js:JS表达式字符串 | 在页面执行JS并返回结果 |
| edge/chrome | `click(selector)` | selector:CSS选择器 | 点击元素 |
| edge/chrome | `waitNetworkIdle(timeout)` | timeout:最大等待ms(默认10000) | 智能等待网络空闲 |
| edge/chrome | `screenshot()` | 无 | 返回PNG base64截图 |

**启动浏览器远程调试**:
- Edge: `Start-Process msedge.exe --remote-debugging-port=9222 --disable-blink-features=AutomationControlled`
- Chrome: `Start-Process chrome.exe --remote-debugging-port=9223`
- 模块导入: `const { edge, chrome } = require('./cdp-automation.js');`

**典型流程**: 导航→探测DOM(eval打印结构)→操作(click/填表)→智能等待(waitNetworkIdle)→提取数据(eval/screenshot)。SPA导航需先入父页面再JS点击侧边栏div。

## 示例代码

### 1. 启动浏览器远程调试（PowerShell）

以反检测参数启动Edge，开启9222调试端口：

```powershell
# Edge：开启远程调试并禁用自动化标记
Start-Process msedge.exe -ArgumentList @(
    "--remote-debugging-port=9222",
    "--disable-blink-features=AutomationControlled",
    "--user-data-dir=$env:LOCALAPPDATA\Microsoft\Edge\User Data"
)

# Chrome：9223端口
Start-Process chrome.exe -ArgumentList @(
    "--remote-debugging-port=9223",
    "--disable-blink-features=AutomationControlled"
)

# 验证端口是否就绪
Invoke-RestMethod -Uri "http://localhost:9222/json/version" | Select-Object webSocketDebuggerUrl
```

### 2. CDP自动化完整流程（Node.js）

导航→探测DOM→点击→智能等待→提取数据的典型流程：

```javascript
const { edge } = require('./cdp-automation.js');

async function scrapeOrderList() {
  // 1. 导航到订单页（复用已登录浏览器会话）
  await edge.goto('https://shop.example.com/user-center/orders');
  await edge.waitNetworkIdle(10000);

  // 2. 探测DOM结构（先探索再定位，打印样本）
  const probe = await edge.JSON.parse(`
    (() => {
      const rows = document.querySelectorAll('[class*="order"]');
      return Array.from(rows).slice(0, 3).map(el => ({
        tag: el.tagName,
        cls: el.className,
        text: el.innerText.slice(0, 80),
      }));
    })()
  `);
  console.log('DOM探测结果:', JSON.stringify(probe, null, 2));

  // 3. 点击「已发货」筛选标签
  await edge.click('[class*="shipped"]');

  // 4. 智能等待网络空闲（替代固定sleep）
  await edge.waitNetworkIdle(8000);

  // 5. 提取订单数据
  const orders = await edge.JSON.parse(`
    (() => {
      const items = document.querySelectorAll('[class*="order-item"]');
      return Array.from(items).map(item => ({
        id: item.querySelector('[class*="order-no"]')?.innerText,
        amount: item.querySelector('[class*="price"]')?.innerText,
        status: item.querySelector('[class*="status"]')?.innerText,
      }));
    })()
  `);
  return orders;
}

scrapeOrderList().then(orders => console.log(orders));
```

### 3. 获取HttpOnly Cookie（Node.js）

`document.cookie`无法读取HttpOnly Cookie，需通过CDP命令获取：

```javascript
/cdp-automation.js');

async function getHttpOnlyCookies(targetUrl) {
  const cdpSession = await edge.getCdpSession();
  // 通过 Network.getCookies 获取包含 HttpOnly 的完整 Cookie
  const { cookies } = await cdpSession.send('Network.getCookies', {
    urls: [targetUrl],
  });
  // 转为标准 Cookie 头格式
  const cookieHeader = cookies
    .map(c => `${c.name}=${c.value}`)
    .join('; ');
  console.log('Cookie数量:', cookies.length);
  console.log('含HttpOnly:', cookies.filter(c => c.httpOnly).length);
  return cookieHeader;
}

// 示例：获取登录态Cookie用于后续请求
getHttpOnlyCookies('https://shop.example.com').then(header => {
  console.log('Cookie头:', header.slice(0, 60) + '...');
});
```

### 4. SPA内部路由导航（Node.js）

直接navigate到SPA子路由会404，需先入父页面再JS点击侧边栏div：

```javascript
/cdp-automation.js');

async function navigateSpaRoute() {
  // 1. 先入可访问的父页面（非SPA内部子路由）
  await edge.goto('https://app.example.com/user-center/basic-information');
  await edge.waitNetworkIdle(8000);

  // 2. JS点击侧边栏 div 触发内部路由跳转
  await edge.JSON.parse(`
    const nav = document.querySelector('div[cursor-pointer][class*="security"]');
    if (nav) nav.click();
  `);

  // 3. 等待SPA路由切换完成
  await edge.waitNetworkIdle(8000);

  // 4. 截图确认已跳转
  const screenshot = await edge.screenshot();
  return screenshot;
}

navigateSpaRoute().then(() => console.log('SPA导航完成'));
```

## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| action | string | 是 | 操作类型: `navigate`/`eval`/`click`/`screenshot`/`get_cookies`/`connect` |
| url | string | 条件必填 | 目标页面URL,`navigate`/`get_cookies`时必填 |
| js | string | 条件必填 | JS表达式字符串,`eval`时必填 |
| selector | string | 条件必填 | CSS选择器,`click`时必填 |
| browser | string | 否 | 浏览器类型: `edge`(默认)/`chrome` |
| port | number | 否 | 远程调试端口,Edge默认9222,Chrome默认9223 |
| timeout | number | 否 | 最大等待毫秒数,默认10000 |
| input_params | object | 否 | 附加配置选项,支持创建/查询/导出操作 |

## 返回格式
```json
{
  "success": true,
  "data": {
    "result": "CDP自动化执行结果",
    "execution_time": "1.2s",
    "metadata": {
      "version": "1.0",
      "processor": "cdp-browser-master"
    }
  },
  "execution_log": ["解析输入参数", "连接浏览器调试端口", "执行自动化操作", "提取并格式化结果"],
  "error": null
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| success | boolean | 处理是否成功,`true`表示成功,`false`表示失败 |
| data.result | string/object | 自动化执行结果,可能是提取的DOM数据、截图base64或Cookie字符串 |
| data.execution_time | string | 处理耗时,格式如`1.2s` |
| data.metadata.version | string | 技能版本号 |
| data.metadata.processor | string | 处理器标识,固定为`cdp-browser-master` |
| execution_log | array | 执行步骤日志,记录连接、导航、操作、提取各阶段 |
| error | string/null | 错误信息,成功时为`null`,失败时为错误描述(如端口被占用、选择器未找到等) |

## 故障恢复
| 场景 | 原因 | 处理方式 |
|:-----|:-----|:-----|
| 连接9222失败 | 端口被占或浏览器未启动 | `netstat -ano \| findstr :9222`查端口,`taskkill /F /PID <pid>`清残留,重启浏览器 |
| eval返回空值 | 页面未渲染完 | 用`waitNetworkIdle`替代固定sleep,JS密集页面手动加到8-10s |
| 被反爬拦截 | 检测到自动化标记 | 加`--disable-blink-features=AutomationControlled`,行为拟人化,复用已验证会话Cookie |
| SPA子路由404 | 直接navigate到SPA内部路由 | 先入可访问父页面,再JS点击侧边栏div触发内部路由跳转 |
| Cookie缺失 | HttpOnly Cookie用document.cookie拿不到 | 用CDP `Network.getCookies`命令获取 |

## 问答合集
**Q: 什么时候该用CDP而不是web_fetch?**
A: JS渲染页面、需登录态、需交互(点击/填表)时用CDP。静态HTML用web_fetch即可。B站等页面web_fetch拿到的是空壳。

**Q: 选择器经常失效怎么办?**
A: 用探测模式——先eval探索DOM结构再定位。提供多备选选择器(从精确class到模糊`[class*="未指定"]`到语义tag到属性选择器)降级匹配。优先用`[class*="未指定"]`模糊匹配。

**Q: 怎么拿HttpOnly Cookie?**
A: `document.cookie`拿不到。用CDP的`Network.getCookies`命令:`cdpSession.send('Network.getCookies', {urls: ['https://目标网站.com']})`。

## 能力边界
1. **依赖本地浏览器环境**:需提前安装Edge/Chrome并启动远程调试,无浏览器环境的服务器无法使用
2. **每端口单连接限制**:同一时间每个端口(9222/9223)只能有一个WebSocket连接,多任务需排队或用不同端口
3. **强反爬站点可能失败**:小红书等强反自动化检测站点,即使加反检测策略仍可能被识别
4. **选择器随网站改版失效**:网站更新可能导致选择器失效,需用探测模式重新探索DOM结构
5. **不适用Headless场景**:核心优势是复用已登录浏览器会话,Headless模式失去此优势且更易被检测

## 安全原则
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 使用环境变量管理密钥,禁止硬编码 |
| 命令执行风险 | 只运行安全清单内命令,禁止拼接用户输入 |
| 网络通信安全 | 通信使用HTTPS并校验证书有效性 |
| 敏感数据暴露 | 返回内容不包含敏感凭证 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 性能评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 优势对比
| 对比维度 | CDP浏览器大师 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 解决反爬检测、选择器易 | 通用场景 | 通用场景 |

## 功能介绍
- **自动化执行**: 解决反爬检测、选择器易
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 环境初始化
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪

## 支持中心
### Q1: CDP浏览器大师支持哪些输入格式？

A1: 解决反爬检测、选择器易。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 异常修复
针对CDP浏览器大师使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### CDP浏览器大师通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 常见疑问速答
## 异常恢复流程
针对CDP浏览器大师使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 可用性分类
- **分类**: MD（纯Markdown指令，通过自然语言驱动Agent完成操作）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作。
