# 小方同学营销 API 详细参考

## 目录

1. [登录与 Token 获取](#登录与-token-获取)
2. [SSE 流式解析](#sse-流式解析)
3. [多轮交互阶段说明](#多轮交互阶段说明)
4. [job_id 二次解析](#job_id-二次解析)
5. [图片轮询策略](#图片轮询策略)
6. [QR 码截图与 OSS 上传](#qr-码截图与-oss-上传)
7. [错误码表](#错误码表)

---

## 登录与 Token 获取

### 检查登录状态（仅微信扫码登录流程使用）

用 `browser_navigate` 打开 `https://www.aippt.cn/marketing/home?utm_type=fanganskill&utm_source=fanganskill&utm_page=fangan.cn&utm_plan=fanganskill&utm_unit=xiaofangskill&utm_keyword=40515275`，然后用 `browser_evaluate` 检查 localStorage：

```js
// browser_evaluate — 检查登录状态
() => {
  const token = localStorage.getItem('login_result_token');
  if (token) {
    return { loggedIn: true, token: token };
  }
  return { loggedIn: false };
}
```

- `loggedIn: true` → 拿到 `token`，保存为 `AUTH_TOKEN`
- `loggedIn: false` → 引导微信扫码登录

> **localStorage key 说明**：
> - `login_result_token` — AIPPT 登录成功后自动写入的 Token，用于**检查是否已登录**
> - `token` — 微信扫码登录回调写入的 Token（与 `login_result_token` 值相同，写入时机不同）
> - 检查登录状态时读 `login_result_token`，微信扫码回调后读 `token`，两者最终拿到的是同一个 access_token

### 引导微信扫码登录

1. 用 JS 点击"登录"按钮（纯 DOM API，不依赖 snapshot ref）：

```js
// browser_evaluate — 点击登录按钮
() => {
  const buttons = document.querySelectorAll('button');
  for (const btn of buttons) {
    if (btn.textContent.trim() === '登录') {
      btn.click();
      return { clicked: true };
    }
  }
  return { error: 'login button not found' };
}
```

2. `browser_wait` 等待 2 秒（弹窗加载 + 二维码渲染）。

3. **截图二维码 → 上传 OSS → 发送图片链接给用户**（详见 [QR 码截图与 OSS 上传](#qr-码截图与-oss-上传)）。

4. 等待用户确认登录成功后，再次获取 token：

```js
// browser_evaluate — 登录后获取 token
() => {
  const token = localStorage.getItem('token');
  const userInfo = localStorage.getItem('userInfo');
  if (token) {
    return {
      loggedIn: true,
      token: token,
      userInfo: userInfo ? JSON.parse(userInfo) : null
    };
  }
  return { loggedIn: false };
}
```

### 手机号密码登录

当用户选择手机号密码登录时，**先询问用户手机号和密码**，然后通过 API 登录。

**加密方式**：RSA PKCS#1 v1.5（2048-bit），使用 JSEncrypt 库。`mobile` 和 `password` 字段均需加密。

**RSA 公钥**：

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyiij9gZ3EXit1lymdK8d
os5QVi/q+XAP0gKZ58HYyWfTmbInRsi/tNLdF4DFLBJ65//4BhYmMSdvG+44ZIvA
QVfaDUs9LEwVQPxp5DfXWVKLGiKzVpwRte0w1eR+GqzroaYsFNhkbc1IY2BjYa7j
vFtHYXZSgmNKQkxCObSBVaVNj/0LYraOy7Iy+yYOBrnJ4IkMpR6qPmB68IzNakqi
uLN9Q4SbGTwt+4Gt0HR+dpfi/al1lfpqxnnVhoA9TrKrbUmCITl4daRoIP1qdel+
JqbvGY/eBqoOA+p0QdknlDtnyKrQdhIPsFWC1s0UZ8/DrXCBJvr4OLYwnzv0dN6k
dQIDAQAB
-----END PUBLIC KEY-----
```

**加密与登录流程**（使用 exec 工具执行）：

```bash
# 用 Node.js crypto 模块加密手机号和密码，然后调用登录接口
node -e "
const crypto = require('crypto');
const https = require('https');

const PUBLIC_KEY = \`-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyiij9gZ3EXit1lymdK8d
os5QVi/q+XAP0gKZ58HYyWfTmbInRsi/tNLdF4DFLBJ65//4BhYmMSdvG+44ZIvA
QVfaDUs9LEwVQPxp5DfXWVKLGiKzVpwRte0w1eR+GqzroaYsFNhkbc1IY2BjYa7j
vFtHYXZSgmNKQkxCObSBVaVNj/0LYraOy7Iy+yYOBrnJ4IkMpR6qPmB68IzNakqi
uLN9Q4SbGTwt+4Gt0HR+dpfi/al1lfpqxnnVhoA9TrKrbUmCITl4daRoIP1qdel+
JqbvGY/eBqoOA+p0QdknlDtnyKrQdhIPsFWC1s0UZ8/DrXCBJvr4OLYwnzv0dN6k
dQIDAQAB
-----END PUBLIC KEY-----\`;

function rsaEncrypt(text) {
  return crypto.publicEncrypt(
    { key: PUBLIC_KEY, padding: crypto.constants.RSA_PKCS1_PADDING },
    Buffer.from(String(text))
  ).toString('base64');
}

const body = JSON.stringify({
  mobile: rsaEncrypt('PHONE_NUMBER'),
  password: rsaEncrypt('PASSWORD'),
  register_type: 1,
  register_region: 48,
  utm_type: 'fanganskill',
  utm_keyword: '40515275',
  utm_source: 'fanganskill',
  utm_unit: 'xiaofangskill',
  utm_plan: 'skill渠道',
  utm_page: 'fangan.cn',
  host: 'www.aippt.cn'
});

const req = https.request({
  hostname: 'www.aippt.cn',
  path: '/users/login/mobile',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'rsa': '1',
    'Content-Length': Buffer.byteLength(body)
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const result = JSON.parse(data);
    console.log(JSON.stringify({
      code: result.code,
      msg: result.msg,
      token: result.data?.token?.access_token || null,
      user_info: result.data?.userinfo || null
    }, null, 2));
  });
});
req.write(body);
req.end();
"
```

> 将 `PHONE_NUMBER` 和 `PASSWORD` 替换为用户提供的实际值。

**请求头**：必须包含 `rsa: 1`，标识字段已 RSA 加密。

**返回结构**（JSON body）：

```json
{
  "code": 0,
  "msg": "登录成功",
  "data": {
    "token": {
      "access_token": "eyJhbGciOiJI...",
      "refresh_token": "eyJhbGciOiJI...",
      "access_token_expires_at": "2026-06-16T13:34:53..."
    },
    "userinfo": {
      "id": 6287373,
      "nick_name": "xiaojing",
      "mobile": "158****1221"
    }
  }
}
```

**Token 获取方式**：直接从 JSON body 取 `data.token.access_token` 作为 `AUTH_TOKEN`。

- `code: 0` → 登录成功，取 `data.token.access_token`
- `code` 非 0 → 登录失败，将 `msg` 展示给用户（如"密码错误"、"账号不存在"）

> **注意**：手机号密码登录是纯 API 流程，不需要启动浏览器，也不需要写入 localStorage。后续所有 API 调用直接使用 `access_token` 即可。

---

### 验证 Token 有效性

```bash
curl -s 'https://www.aippt.cn/api/user/info' \
  -H 'authorization: Bearer TOKEN'
```

- `code: 0` → Token 有效
- `code: 14006`（"请先登录"）→ Token 过期，重新登录

---

## SSE 流式解析

`task/result` 接口返回 Server-Sent Events (SSE) 格式的流式数据。

### 事件类型

| 事件 | 含义 | 处理方式 |
|------|------|---------|
| `event: connected` | 连接建立 | 无需处理 |
| `event: message_chunk` | 正常内容片段 | 拼接所有 `content` 字段，组成完整内容 |
| `event: interrupt` | 当前阶段完成，等待用户反馈 | 展示内容给用户，等待确认或编辑 |
| `event: ping` | 心跳 | 无需处理 |
| `event: stream_end` | 流结束 | 流结束标志 |

### data 字段结构

```json
{
  "agent": "marketing_brief",
  "content": "生成的文本内容...",
  "id": "run--xxx",
  "message_id": "xxx",
  "role": "assistant",
  "thread_id": "xxx",
  "reasoning_content": "思考过程..."
}
```

- `agent`：当前执行的 Agent 类型（用于判断阶段）
- `content`：拼接所有 chunk 的 content 即为完整内容
- `reasoning_content`：Agent 的思考过程（可忽略）
- `finish_reason: "stop"`：当前 Agent 输出结束

---

## 多轮交互阶段说明

### 阶段流转顺序

| 轮次 | Agent 类型 | 阶段内容 | 说明 |
|------|-----------|---------|------|
| 1 | `marketing_brief` | Brief 需求分析 | 解析项目背景、目标、预算、USP、人群等 |
| 2 | `marketing_outline` | 方案目录结构 | 生成 12 章结构化目录 |
| 3 | `marketing_propagation_subject_deduction` | 策略推导 | 市场洞察、竞品诊断、传播主题推导 |
| 4 | `marketing_communication_plan` | 传播执行铺排 | 分阶段执行规划、达人矩阵、投流策略 |
| 5 | `marketing_report` | 最终文稿 | 合成完整方案文稿 |
| 6 | `marketing_picture_style` | 风格选择 | 提示"请定义PPT风格" |

### 循环流程

```
                    ┌──────────────────────────┐
                    │  获取结果 (task/result)     │
                    └────────────┬─────────────┘
                                 │
                          收到 interrupt
                                 │
                    ┌────────────▼─────────────┐
                    │  展示内容给用户，等待反馈    │
                    └────┬──────────────┬───────┘
                         │              │
                    用户确认         用户要求修改
                   (accepted)        (edit)
                         │              │
                    ┌────▼────┐    ┌────▼────┐
                    │ 发送确认  │    │ 发送修改  │
                    └────┬────┘    └────┬────┘
                         │              │
                 agent 是            回到获取结果
              picture_style?      (重复当前阶段)
                    │
              ┌─────┴─────┐
              │ 是         │ 否
              ▼            ▼
         风格选择       获取结果
                      (进入下一阶段)
```

### 风格选项

收到 `marketing_picture_style` interrupt 后，向用户展示选项，用户选择后将原文直接作为 `content` 发送。

#### 风格类型（三选一）

**1. 企业品牌风格**
   - 智能推荐品牌色（用户可提供品牌色或 HEX 色值）
   - 上传企业/品牌 logo

**2. 行业风格**（默认推荐）
   - 智能模板，根据行业自动匹配

**3. 经典风格**（15 种可选）
   - 写实 / 极简 / 商务 / 科技 / 经典中式 / 新中式 / 孟菲斯 / 拼贴 / 像素 / 环保主义 / 液态酸 / 弥散光 / 报刊 / 宏伟磅礴 / 自定义

#### 画面比例

- 16:9（默认）
- 4:3

#### PPT 页数

- 智能页数（默认，根据文稿量自动决定）
- 10-20页
- 21-40页
- 41-60页
- 自定义（小于 100 页）

#### 发送方式

用户选择后，将用户的选择原文直接作为 `messages[0].content` 发送即可，无需转换为特定格式。

例如用户说"科技风，4:3，30页"，则 content 就是 `"科技风，4:3，30页"`。

---

## job_id 二次解析

`job_id` **不在**事件的顶层字段中，而是嵌套在 `content` 字段的 **JSON 字符串**内，需要二次解析：

```
event: message_chunk
data: {"agent":"marketing_picture_prompt_job","content":"{\"id\":45303,\"job_id\":\"57a7b0e5-xxx\",\"page_id\":\"...\",\"prompt\":\"...\"}","message_id":"..."}
```

### 解析步骤

1. 找到 `agent` 为 `"marketing_picture_prompt_job"` 的事件
2. 取出 `content` 字段（是一个 **JSON 字符串**，不是对象）
3. 对 `content` 做 `JSON.parse()` / `json.loads()` 二次解析
4. 从解析后的对象中提取 `job_id`
5. 收集所有 `job_id`（一页 PPT 对应一个 job_id，通常 10-30 个）

### Python 示例

```python
import json

job_ids = []
for line in open('sse_output.txt'):
    line = line.strip()
    if line.startswith('data: '):
        data = json.loads(line[6:])
        if data.get('agent') == 'marketing_picture_prompt_job':
            inner = json.loads(data['content'])  # 二次解析
            job_ids.append(inner['job_id'])
```

---

## 图片轮询策略

### 接口

```bash
curl -s 'https://www.aippt.cn/api/marketing/image/gen/job/result?job_ids=JOB_IDS&task_id=TEXT_TASK_ID' \
  -H 'authorization: Bearer AUTH_TOKEN'
```

- `job_ids`：逗号拼接的所有 job_id
- `task_id`：创建项目时的 `text_task_id`

### 返回结构

```json
{
  "code": 0,
  "data": {
    "task_job_status": "running",
    "list": [
      {"job_id": "xxx", "status": "done", "image_url": "https://...jpg"},
      {"job_id": "yyy", "status": "running", "image_url": ""}
    ]
  }
}
```

### 轮询规则

- 间隔 **15 秒**重试
- 直到 `task_job_status` 为 `"done"` 或所有 `list[].status` 均为 `"done"`
- 最后一张图可能需要额外 1-2 分钟
- 全部完成后，整理所有 `image_url` 展示给用户

---

## QR 码截图与 OSS 上传

### 截图登录弹窗

1. 点击登录按钮并等待 2 秒后，执行 `browser_snapshot` 查看页面结构
2. 在 snapshot 中找到登录弹窗的**内部卡片容器** ref

典型 snapshot 结构（ref 每次会变）：
```
dialog [ref=eXXX]:
  - document:
    - generic [ref=eYYY]:          ← 目标：登录卡片容器
      - img [ref=...]              ← 关闭按钮
      - generic [ref=...]:
        - heading "微信登录" [ref=...]
        - paragraph "请使用手机微信扫码登录"
```

**定位规则**：
- 找到 `dialog` 下 `document` 下的第一个 `generic`，这是卡片容器
- **不要用 `dialog` 本身的 ref**（它是全屏遮罩层）

3. 用 `browser_take_screenshot` 截取元素：
```
browser_take_screenshot:
  element: "登录弹窗卡片"
  ref: "eYYY"
  filename: "/tmp/aippt-qrcode.png"
```

> 必须传 `ref` + `element` 做元素级截图，禁止全屏截图。

### 上传二维码截图（通过 tmpfiles.org）

> 登录阶段尚未获取 AUTH_TOKEN，无法使用小方同学上传接口，改用 tmpfiles.org 免登录上传。

```bash
curl -s -L --max-time 30 \
  -F "file=@/tmp/aippt-qrcode.png" \
  https://tmpfiles.org/api/v1/upload
```

- 返回 JSON：`{"status":"success","data":{"url":"http://tmpfiles.org/ID/filename.png"}}`
- **直链需转换**：将返回 URL 中的 `tmpfiles.org/` 替换为 `tmpfiles.org/dl/`
  - 返回：`http://tmpfiles.org/29295630/aippt-qrcode.png`
  - 直链：`https://tmpfiles.org/dl/29295630/aippt-qrcode.png`
- 文件有效期约 1 小时，足够扫码登录使用
- 如果上传失败，将本地截图路径发给用户，提示用户在浏览器中手动扫码

**发送给用户**：

```
![小方同学登录二维码](DIRECT_URL)
请用手机微信扫描以上二维码完成登录。扫码成功后请告诉我。
```

> 钉钉等渠道**必须用公网链接**，本地路径无法展示。

---

## 错误码表

| code | 说明 | 处理方式 |
|------|------|---------|
| 0 | 成功 | 正常处理 |
| 14006 | Token 过期 / 未登录 | 回到登录步骤重新获取 Token |
| 其他非 0 | 业务错误 | 将 `code` 和 `msg` 原样展示给用户 |

> API 报错直接告知用户，不要尝试自行排查。平台限制类错误（如"Agent 并发任务上限"）需用户去小方同学工作台处理。
