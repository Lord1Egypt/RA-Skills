# M23 — 动态 API Key 模拟

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程蒸馏
> 挂载版本：v3.4.0（2026-07-26）
> 触发咒语："API Key""CSRF Token""动态密钥""Algolia""Session"

## R — 原文引用

> "API密钥的动态性：许多API（尤其是前端直接调用的搜索服务如 Algolia）会使用短期有效、动态生成的API密钥，以增强安全性。直接从网络流量中复制一个静态Key可能很快失效。需要理解并模拟前端获取这个动态Key的完整流程（可能涉及Cookie、CSRF Token、特定授权端点等）。"

> "`requests.Session` 的妙用：在需要多步请求、且后续请求依赖于之前请求设置的 Cookies 的场景下（如获取CSRF Token后再用此Cookie请求API Key），`requests.Session()` 对象能极大地简化Cookie管理。"

## I — 方法论重写

**核心命题**：现代网站为增强安全性，使用短期有效、动态生成的 API Key（如 Algolia 搜索服务的 Key）。直接从网络流量复制静态 Key 几分钟后就失效。必须模拟前端获取动态 Key 的完整流程。

### 🎯 目的限定（v3.4.4 强制，回应 ClawHub Purpose & Capability concern）

⚠️ **本方法论仅适用于以下场景**：
- ✅ **公开 API 的动态 Key**：网站前端 JS 公开调用的搜索/查询服务（如 Algolia、Meilisearch 等第三方搜索服务的公开 Key）
- ✅ **用户自己拥有合法权限的 API**：用户已注册并获授权访问的 API Key
- ✅ **公开数据采集**：抓取的数据本身是公开可见的（无需登录即可浏览的内容）

❌ **本方法论禁止用于以下场景**：
- ❌ **绕过登录认证**：模拟登录用户的 Session/Cookie 访问需登录才能看的内容
- ❌ **绕过付费墙**：模拟付费用户 Key 访问付费内容
- ❌ **破解管理员认证**：模拟后台管理 Session
- ❌ **绕过 401/403 拒绝访问**：401/403 是网站明确拒绝访问的信号，禁止通过模拟 Session 绕过
- ❌ **破解 reCAPTCHA / Cloudflare Challenge**：禁止模拟或绕过反爬虫验证

**关键判定**：如果某 API 调用返回 401/403 = 网站明确禁止你访问，应立即停止，不可"模拟 Session 重试"。本方法论的 Key 刷新机制仅用于**公开 Key 的自然过期**（如 Algolia 每 5 分钟刷新的搜索 Key），不用于**认证被拒绝**的场景。



**5 步模拟流程**：

### Step 1：识别 Key 来源
- **Network 分析**：找到 API 请求中的 Key 参数（如 `x-api-key` / `Authorization` / `X-CSRF-Token`）
- **溯源**：这个 Key 从哪里来？
  - 选项 A：另一个 API 端点返回（如 `/api/auth/token`）
  - 选项 B：HTML 页面内嵌（如 `<script>window.apiKey = "xxx"</script>`）
  - 选项 C：Cookie 中携带（如 `csrf_token`）
  - 选项 D：JS 计算生成（如对时间戳+密钥做 HMAC）

### Step 2：追踪 Key 获取链
- **完整链路**：用户访问页面 → 页面请求授权端点 → 授权端点返回 Key → 前端用 Key 调用数据 API
- **关键节点**：哪个请求返回了 Key？需要什么前置条件（如 Cookie/Referer）？
- **时效性**：Key 多久过期？（30 秒 / 5 分钟 / 1 小时）

### Step 3：用 requests.Session 模拟（v3.4.4 脱敏版）

⚠️ **代码示例中禁止出现真实凭证值**，统一从 `.env` 读取：

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取所有凭证

session = requests.Session()

# Step 1: 访问页面，获取初始 Cookie（公开页面，无需认证）
resp1 = session.get(page_url, headers={'User-Agent': os.getenv('STANDARD_UA')})
# session 自动保存 Cookie

# Step 2: 请求公开的授权端点，获取动态 Key
# 注意：此端点必须是网站前端 JS 公开调用的端点，非管理员/付费用户专属
csrf_token = session.cookies.get('csrf_token', '')  # 从 Cookie 提取（公开 CSRF）
resp2 = session.post(auth_endpoint, headers={
    'X-CSRF-Token': csrf_token,
    'Referer': page_url,  # 公开 Referer，用于来源校验
}, data={'client_id': os.getenv('PUBLIC_CLIENT_ID', '')})
api_key = resp2.json().get('api_key', '')

# Step 3: 用 Key 调用数据 API（数据必须是公开可见的）
resp3 = session.post(data_api_url, headers={
    'X-API-Key': api_key,  # 动态获取的公开 Key
}, json=payload)
```

**凭证保护铁律**：
- ❌ 禁止在代码示例中硬编码真实 `api_key` / `csrf_token` / `client_id` 值
- ❌ 禁止把用户自己账号的 Session/Cookie 写入代码（除非抓取自己拥有权限的数据）
- ✅ 所有凭证统一从 `.env` 读取，`.env` 加入 `.gitignore`
- ✅ 日志输出 Key 时脱敏：`print(f"api_key: {api_key[:4]}****")`

### Step 4：请求头完整性（v3.4.4 修订）
- **必备头**：User-Agent（使用标准浏览器 UA，**禁止伪装为他人浏览器绕过反爬**）
- **认证头**：Authorization / X-API-Key / X-CSRF-Token（仅限公开 API 或用户拥有权限的 API）
- **来源头**：Referer / Origin（用于公开 API 调试，**禁止伪造绕过来源校验**）
- **接受头**：Accept / Accept-Language / Accept-Encoding
- **请求类型**：Content-Type: application/json

⚠️ **User-Agent 限制**（v3.4.4 强化）：
- ✅ 允许：使用主流浏览器标准 UA（如 `Mozilla/5.0 ... Chrome/120.0 ...`）让请求正常工作
- ❌ 禁止：轮换 UA 池绕过反爬
- ❌ 禁止：伪装为 Googlebot / Bingbot 等搜索引擎爬虫
- ❌ 禁止：伪装为他人浏览器绕过基于 UA 的访问控制

### Step 5：Key 刷新机制（v3.4.4 严格限定）

⚠️ **Key 刷新仅适用于公开 Key 的自然过期**，不用于绕过认证被拒绝：

- ✅ **允许刷新的场景**：
  - Algolia 等第三方搜索服务的公开 Key 自然过期（通常 5-30 分钟刷新一次）
  - 网站前端 JS 自动刷新的公开 CSRF Token
  - 用户自己拥有权限的 API Key 自然过期

- ❌ **禁止刷新的场景**：
  - API 返回 **401 Unauthorized** = 网站明确拒绝你的访问，**禁止重试**，应立即停止并提示用户"该 API 需要认证，本方法论不支持绕过认证"
  - API 返回 **403 Forbidden** = 网站明确禁止访问，**禁止重试**，应立即停止并提示用户"该 API 拒绝访问，可能需要登录或权限不足"
  - 401/403 不是"Key 过期"，是"认证被拒绝"，两者性质不同

**自动刷新逻辑**（仅限公开 Key 自然过期）：
```python
MAX_REFRESH_RETRIES = 3  # 最多重试 3 次

for attempt in range(MAX_REFRESH_RETRIES):
    resp = session.post(data_api_url, headers={'X-API-Key': api_key}, json=payload)
    if resp.status_code == 200:
        break
    elif resp.status_code in (401, 403):
        # ⚠️ 检查是否是公开 Key 自然过期
        if is_public_search_api(data_api_url):  # 判定是否是公开搜索 API
            api_key = refresh_public_key(session)  # 重新走 Step 1-2 获取公开 Key
            continue
        else:
            # ❌ 非公开 API 的 401/403 = 认证被拒绝，立即停止
            raise PermissionError(f"API {data_api_url} 返回 {resp.status_code}，认证被拒绝。本方法论不支持绕过认证。")
    time.sleep(2 ** attempt)  # 指数退避
```

## A1 — 书中案例

**Airtable 社区 Algolia Key 案例**：
- Key 来源：HTML 页面内嵌的 JS 脚本中
- 获取流程：
  1. 访问 airtable community 首页 → 获得 Cookie
  2. HTML 中含一段 JS 代码会请求授权端点
  3. 授权端点返回 Algolia API Key
  4. 前端用这个 Key 调用 Algolia 搜索 API
- 失败现象：直接复制 Network 中的 Key，几分钟后失效
- 解决方案：用 Session 模拟完整链路，每次抓取前先刷新 Key

**调试日志**：
```
[尝试 1] 直接用复制的 Key → 401 Unauthorized（Key 已过期）
[尝试 2] 模拟完整链路获取 Key → 200 OK（成功）
[尝试 3] 隔天测试 → 仍成功（Key 每次获取都有效）
```

## A2 — 未来触发

**何时用 M23**：
- M22 识别到动态 API 后，发现请求需要 Key
- 用户说"API Key 是动态生成的"
- 用户说"复制的 Key 几分钟就失效"
- 用户说"CSRF Token""Algolia""动态密钥"
- 抓取过程中出现 401/403 错误

**与 M22 的关系**：
- M22 是前提：先识别出动态 API，才能模拟 Key
- M23 是延伸：M22 识别到 Key 后，用 M23 模拟获取流程

## E — 可执行步骤

**AI 给用户的诊断步骤**：

```
你的请求返回 401/403，很可能是 API Key 失效了。请按以下步骤排查：

1. 在 Network 面板找到失败的请求，查看 Request Headers 中的认证字段
2. 找到这个 Key 是从哪个请求获取的（往前面找，通常是 POST 请求）
3. 把两个请求都 Copy as cURL 发给我
4. 我帮你用 requests.Session 模拟完整链路

或者直接告诉我：
- 网站是哪个？
- 抓取时出现什么错误？
- 你已经分析了 Network 吗？
```

**AI 内部执行步骤**：

```
1. 分析两个 cURL（页面请求 + Key 获取请求）
2. 用 requests.Session() 建立会话
3. Step 1: 模拟页面访问，获取初始 Cookie
4. Step 2: 模拟 Key 获取请求，提取动态 Key
5. Step 3: 用 Key 调用数据 API
6. 添加自动刷新逻辑（捕获 401/403 → 重新获取 Key）
7. 输出完整代码 + Key 刷新策略
```

## B — 边界与盲点

### 适用边界
- ✅ Algolia 等第三方搜索服务（动态 Key 是标配）
- ✅ 带 CSRF Token 保护的网站
- ✅ 需要多步请求获取 Token 的网站
- ❌ 公开无需认证的 API（直接用即可）
- ❌ 需要付费账号的 API（Key 是固定的，非动态）
- ❌ 用 reCAPTCHA / Cloudflare Challenge 保护的网站（需用浏览器自动化）

### 合规边界（v3.4.1 强化）

⚠️ 使用 M23 模拟动态 API Key 时，必须遵守：

1. **只模拟公开 Key 获取流程**：Key 必须是网站前端代码中可见的公开流程获取的（如调用 `/api/auth` 端点）
2. **不破解加密算法**：禁止逆向 JS 代码破解 Key 计算逻辑（如 HMAC 签名算法）
3. **不绕过付费墙**：禁止模拟付费账号才能获取的 Key
4. **不模拟管理员认证**：禁止模拟后台管理系统的认证流程
5. **遵守服务条款**：模拟 Key 获取流程必须符合目标站 ToS
6. **凭证保护**（v3.4.1 新增）：
   - 获取的 Key 必须保存在用户工作目录的 `.env` 文件中，禁止硬编码到代码或日志
   - Key 失效后必须提示用户重新获取，不自动重试超过 3 次
   - 在日志中输出 Key 时必须脱敏（只显示前 4 位 + `****`）

**禁止行为**：
- ❌ 模拟用于绕过登录验证的 Key
- ❌ 破解 reCAPTCHA / hCaptcha 等 Challenge
- ❌ 大量并发请求 Key 获取端点（可能触发反爬）
- ❌ 将 Key 共享给他人或公开到代码仓库

### 凭证保护铁律（v3.4.1 新增）

```python
# ✅ 正确：从环境变量读取
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("TARGET_API_KEY")

# ❌ 错误：硬编码到代码
api_key = "sk-abc123xyz..."  # 禁止！

# ✅ 正确：日志中脱敏
print(f"Using API Key: {api_key[:4]}****")  # 输出 "sk-a****"

# ❌ 错误：日志中输出完整 Key
print(f"Using API Key: {api_key}")  # 禁止！
```

### 盲点与陷阱
1. **Key 计算逻辑复杂**：有些网站的 Key 是 JS 算出来的（如对时间戳做 HMAC），需要逆向 JS 代码
2. **多重认证**：有些网站需要 OAuth + API Key + CSRF 三重认证
3. **IP 绑定**：有些 Key 绑定 IP，换 IP 后失效（爬虫服务器需固定 IP）
4. **指纹检测**：部分网站检测 TLS 指纹，普通 requests 会被识别。此时需用支持 TLS 指纹模拟的 HTTP 库（社区生态提供多种选择，如基于 libcurl 的 Python 绑定，请按需选用并查看其最新文档）。**注意**：使用前必须确认目标网站允许自动化访问，且不可用于绕过 Cloudflare 等反爬虫防护
5. **法律风险**：模拟认证可能违反网站 ToS，需用户确认合规性

### 与其他方法论的关系
- **前置**：M22 SPA 动态 API 识别（先找到 API）
- **配套**：M2 防幻觉三招（不脑补 Key 来源，必须实际分析）
- **后续**：M7 验真闭环（验证用 Key 抓到的数据正确性）

## 引用关系

- **前置**：M22（必须先识别出动态 API）
- **成对**：M22+M23（识别到动态 Key 时成对）
- **后续**：M7 验真闭环 + M24 增量唯一 ID

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
