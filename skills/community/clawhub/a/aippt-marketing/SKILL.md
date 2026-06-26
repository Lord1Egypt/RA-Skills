---
name: aippt-marketing
description: |
  调用小方同学skill技能，10倍效率生成专业、精美营销方案，可一键导出专业 PPT。
  当用户表达以下意图时，将自动启用本技能：
    ● 方案生成：「生成营销方案」「撰写营销方案」「营销策划」「推广策划」「产品推广方案」「生成策划案」「品牌推广方案」
    ● PPT生成：「帮我做 PPT」「生成 PPT」「导出幻灯片」「营销方案PPT」「营销方案PPT」「营销方案模版」「企业营销方案模版」
  技能能力
    ● 文本主题输入（营销方案计划或已有完整方案） → 自动生成结构化全案
    ● 文件 / 链接解析 → 上传需求计划，直接生成方案
    ● 多轮交互编辑 → 方案需求分析 → 生成营销计划 → 方案主题推导→ 传播执行策略→ 传播方案
    ● 需求意图理解→ 结构化专业方案→交互对话 → 持续调整优化方案
    ● 风格选择 →企业DNA和多套 PPT 模版自由切换
    ● 自动生成 PPT 配图 → 一键下载
metadata:
  openclaw:
    requires:
      browser: true
      exec: true
    baseUrl: https://www.aippt.cn/api/marketing
    homepage: https://www.aippt.cn
---

# 小方同学营销方案生成

## 版本检查（每次会话首次触发时执行一次）

当前版本：`1.1.0`

用 exec 工具执行以下命令，检查是否有新版本：

```bash
clawhub inspect aippt-marketing --no-input 2>/dev/null | grep -oP 'Latest:\s*\K[\d.]+'
```

- 如果返回的版本号**大于** `1.1.0`，向用户展示：
  > 小方同学技能有新版本可用（当前 1.0.9 → 最新 X.X.X），执行 `clawhub update aippt-marketing` 即可更新。
- 如果命令失败或版本相同，**静默跳过**，不提示用户
- **此检查不阻塞后续流程**，检查完成后立即继续执行

---

## 必读约束

### Base URL

```
https://www.aippt.cn/api/marketing
```

### 认证方式

```
Authorization: Bearer AUTH_TOKEN
```

Token 从浏览器 localStorage 动态获取（key: `login_result_token`），详见 [references/api-details.md](references/api-details.md)。

---

### 首次使用提醒

**首次使用时，必须提醒用户**：

> 使用小方同学营销方案功能需要会员积分。如果您还没有购买，请先前往 [小方同学个人中心](https://www.aippt.cn/personal-center?utm_type=fanganskill&utm_source=fanganskill&utm_page=fangan.cn&utm_plan=fanganskill&utm_unit=xiaofangskill&utm_keyword=40515275) 购买会员积分，然后再开始生成方案。

- 每次会话第一次触发此技能时，都要展示此提醒
- 用户确认已有积分或明确表示继续后，再执行后续流程
- 若 API 返回积分不足相关错误，再次引导用户前往购买

---

### 操作规则

- 首次使用必须先完成登录，获取 AUTH_TOKEN 后才能调用 API
- 每一步都必须检查 `code == 0`，非 0 时展示 `msg` 给用户
- 若 API 返回 `code == 14006`，Token 过期，需重新登录
- **API 报错直接告知用户**，不要自行排查。将错误码和信息原样展示
- **用户输入含文件或链接时，必须先解析内容再调接口**（见第二步）
- `text_task_id`、`thread_id`、`message_seq` 必须从上一步返回中提取，不可编造
- **多轮交互规则**：每轮 interrupt 必须展示给用户并等待反馈，禁止自动发送 accepted/edit
- **超时设置**：普通阶段 `--max-time 300`；生图提示词 `--max-time 900`
- **图片轮询**：间隔 15 秒，直到全部完成

---

## 快速决策

| 用户意图 | 执行步骤 |
|---------|---------|
| 「生成营销方案」（无主题） | 提醒积分 → 询问主题 → 第一步起 |
| 「帮我做XX方案」（有主题） | 提醒积分 → 第一步起 |
| 「根据这个链接做方案」 | 提醒积分 → WebFetch 解析 → 第一步起 |
| 「根据这个文件做方案」 | 提醒积分 → Read 解析 → 第一步起 |
| 「用手机号登录」 | 询问手机号密码 → RSA 加密 → API 登录 |
| 用户确认/编辑某阶段 | 发送 accepted/edit → 获取下一阶段 |
| 用户选择风格 | 发送风格 → 获取生图提示词 → 轮询图片 |

---

## 执行流程

### 第一步：登录与获取 Token

**先询问用户选择登录方式**（不要先打开浏览器）：

#### 方式一：手机号密码登录

纯 API 调用，**不需要启动浏览器**。

1. 询问用户手机号和密码
2. RSA 加密后调用登录接口（详见 [references/api-details.md](references/api-details.md#手机号密码登录)）
3. 从响应 JSON body 取 `data.token.access_token` 作为 `AUTH_TOKEN`
4. 验证 Token 有效性

#### 方式二：微信扫码登录

需要启动浏览器。

1. 用 `browser_navigate` 打开 `https://www.aippt.cn/marketing/home?utm_type=fanganskill&utm_source=fanganskill&utm_page=fangan.cn&utm_plan=fanganskill&utm_unit=xiaofangskill&utm_keyword=40515275`
2. 用 `browser_evaluate` 检查 localStorage 中的 `login_result_token`
   - 已登录 → 保存 Token，跳到第二步
   - 未登录 → 引导扫码（详见 [references/api-details.md](references/api-details.md#引导微信扫码登录)）

#### 验证 Token

```bash
curl -s 'https://www.aippt.cn/api/user/info' \
  -H 'authorization: Bearer AUTH_TOKEN'
```
`code: 0` 有效；`code: 14006` 过期需重新登录。

---

### 第二步：获取用户输入

如果用户只说"生成营销方案"而没给具体主题，询问：
> 请告诉我营销方案的主题，例如："双十一电商大促方案"、"新品上市推广策略"等。

**解析用户附带的文件或链接**：

| 输入类型 | 处理方式 |
|---------|---------|
| 本地文件（`.pdf`、`.docx`、`.txt`、`.md`） | 用 `Read` 读取，提取关键信息作为 `reference_content` |
| 网络链接（`http://`、`https://`） | 用 `WebFetch` 抓取，提取关键信息作为 `reference_content` |
| 图片文件（`.png`、`.jpg`） | 用 `Read` 读取图片，识别文字信息 |

解析后：主题作为第三步 `title`，内容摘要（≤ 2000 字）填入第四步 `messages`。

---

### 流程开始前提醒

创建项目前，**必须先告知用户**：

> 方案生成过程较长（约 6 轮交互 + 图片生成），如果中途出现中断，发送「继续」即可恢复流程。

---

### 第三步：创建项目

```bash
curl -s -X POST 'https://www.aippt.cn/api/marketing/create' \
  -H 'authorization: Bearer AUTH_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "用户输入的主题",
    "reference_content": "",
    "is_regeneration": false,
    "senior_options": "",
    "type": 25
  }'
```

**提取**：`data.id` → `text_task_id`

---

### 第四步：创建生成任务

```bash
curl -s -X POST 'https://www.aippt.cn/api/marketing/task/create' \
  -H 'authorization: Bearer AUTH_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "用户输入的主题"}],
    "text_task_id": TEXT_TASK_ID,
    "resources": []
  }'
```

**提取**：`data.thread_id` 和 `data.message_seq`

---

### 第五步：多轮交互循环（核心流程）

进入 **"获取结果 → 展示 → 用户确认/编辑"** 的循环。共 6 轮 interrupt，每轮可编辑重复。

详细阶段说明见 [references/api-details.md](references/api-details.md#多轮交互阶段说明)。

#### 获取阶段结果

```bash
curl -s --max-time 300 'https://www.aippt.cn/api/marketing/task/result?thread_id=THREAD_ID&message_seq=MESSAGE_SEQ&include_start_message=false' \
  -H 'authorization: Bearer AUTH_TOKEN'
```

拼接所有 `message_chunk` 的 `content` 得到完整内容。收到 `interrupt` 后展示给用户。

#### 用户确认（accepted）

```bash
curl -s -X POST 'https://www.aippt.cn/api/marketing/task/create' \
  -H 'authorization: Bearer AUTH_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "thread_id": "THREAD_ID",
    "interrupt_feedback": "accepted",
    "messages": [{"role": "user", "content": "", "is_hidden": true}],
    "text_task_id": TEXT_TASK_ID
  }'
```

#### 用户要求修改（edit）

```bash
curl -s -X POST 'https://www.aippt.cn/api/marketing/task/create' \
  -H 'authorization: Bearer AUTH_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "thread_id": "THREAD_ID",
    "interrupt_feedback": "edit",
    "messages": [{"role": "user", "content": "用户的修改意见"}],
    "text_task_id": TEXT_TASK_ID
  }'
```

edit 后用返回的新 `message_seq` 再次获取结果（重复当前阶段），直到用户确认。

循环直到收到 `agent: "marketing_picture_style"` 的 interrupt → 进入第六步。

> **特殊处理：第 5 轮 `marketing_report`（最终文稿）**
>
> 收到 `marketing_report` 的 interrupt 后，**不需要等用户反馈**，直接：
> 1. 将完整文稿保存到临时文件（**必须先写文件，后续步骤依赖此文件**）：
>    ```bash
>    mkdir -p /tmp/aippt-pdf-TASK_ID
>    ```
>    用 exec 将完整文稿内容写入 `/tmp/aippt-pdf-TASK_ID/marketing-report.md`
> 2. 构造请求 JSON 文件（避免长文本内联导致 JSON 损坏）：
>    ```bash
>    node -e "
>    const fs = require('fs');
>    const report = fs.readFileSync('/tmp/aippt-pdf-TASK_ID/marketing-report.md', 'utf8');
>    const body = JSON.stringify({
>      thread_id: 'THREAD_ID',
>      interrupt_feedback: 'accepted',
>      messages: [{ role: 'user', content: report, is_hidden: true }],
>      text_task_id: TEXT_TASK_ID
>    });
>    fs.writeFileSync('/tmp/aippt-pdf-TASK_ID/accepted-body.json', body);
>    "
>    ```
> 3. 发送 accepted 请求：
>    ```bash
>    curl -s -X POST 'https://www.aippt.cn/api/marketing/task/create' \
>      -H 'authorization: Bearer AUTH_TOKEN' \
>      -H 'Content-Type: application/json' \
>      -d @/tmp/aippt-pdf-TASK_ID/accepted-body.json
>    ```
> 4. 用返回的新 `message_seq` 继续获取下一阶段结果

---

### 第六步：选择美化风格

收到 `marketing_picture_style` interrupt 后，向用户展示以下选项：

---

请选择 PPT 美化风格：

**① 风格类型**（三选一）：

1️⃣ **企业品牌风格**
   - 智能推荐品牌色（可输入品牌色或 HEX 色值）
   - 上传企业/品牌 logo

2️⃣ **行业风格**（默认推荐 ✅）
   - 智能模板，根据行业自动匹配

3️⃣ **经典风格**（15 种可选）
   写实 / 极简 / 商务 / 科技 / 经典中式 / 新中式 / 孟菲斯 / 拼贴 / 像素 / 环保主义 / 液态酸 / 弥散光 / 报刊 / 宏伟磅礴 / 自定义

**② 画面比例**：16:9（默认）/ 4:3

**③ PPT 页数**：智能页数（默认）/ 10-20页 / 21-40页 / 41-60页 / 自定义（小于100页）

> 不指定的话，我按 **行业风格 + 16:9 + 智能页数** 生成哦～

---

用户选择后，将用户的选择原文直接发送：

```bash
curl -s -X POST 'https://www.aippt.cn/api/marketing/task/create' \
  -H 'authorization: Bearer AUTH_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "thread_id": "THREAD_ID",
    "interrupt_feedback": "accepted",
    "messages": [{"role": "user", "content": "用户的选择原文", "is_hidden": true}],
    "text_task_id": TEXT_TASK_ID
  }'
```

---

### 第七步：获取生图提示词与 job_id

```bash
curl -s --max-time 900 'https://www.aippt.cn/api/marketing/task/result?thread_id=THREAD_ID&message_seq=MESSAGE_SEQ&include_start_message=false' \
  -H 'authorization: Bearer AUTH_TOKEN'
```

> 此步骤耗时较长（5-10 分钟），提前告知用户"正在生成图片提示词，请稍候..."。

**关键**：`job_id` 嵌套在 `content` 的 JSON 字符串内，需二次解析。详见 [references/api-details.md](references/api-details.md#job_id-二次解析)。

---

### 第八步：获取生成的图片

```bash
curl -s 'https://www.aippt.cn/api/marketing/image/gen/job/result?job_ids=JOB_IDS&task_id=TEXT_TASK_ID' \
  -H 'authorization: Bearer AUTH_TOKEN'
```

间隔 15 秒轮询，直到 `task_job_status: "done"`。详见 [references/api-details.md](references/api-details.md#图片轮询策略)。

全部完成后，用 Markdown 图片语法逐页展示给用户（直接显示图片，不要只发链接）：

```
![第1页](IMAGE_URL_1)
![第2页](IMAGE_URL_2)
...
```

---

### 第九步：生成文件并提供下载链接

图片全部展示完后，自动生成方案 PDF 和文稿文件，上传后一起返回给用户。

**1. 下载所有图片到临时目录**

```bash
mkdir -p /tmp/aippt-pdf-TASK_ID && \
curl -s -o /tmp/aippt-pdf-TASK_ID/page-01.jpg "IMAGE_URL_1" && \
curl -s -o /tmp/aippt-pdf-TASK_ID/page-02.jpg "IMAGE_URL_2" && \
...
```

**2. 合成方案 PDF**（按顺序尝试，成功即停）

**优先用 Node.js：**

```bash
node -e "
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');
const glob = require('glob');

(async () => {
  const files = glob.sync('/tmp/aippt-pdf-TASK_ID/page-*.jpg').sort();
  const doc = await PDFDocument.create();
  const PAGE_WIDTH = 1280;
  for (const f of files) {
    const img = await doc.embedJpg(fs.readFileSync(f));
    const scale = PAGE_WIDTH / img.width;
    const pageHeight = img.height * scale;
    const page = doc.addPage([PAGE_WIDTH, pageHeight]);
    page.drawImage(img, { x: 0, y: 0, width: PAGE_WIDTH, height: pageHeight });
  }
  fs.writeFileSync('/tmp/aippt-pdf-TASK_ID/marketing-plan.pdf', await doc.save());
})();
"
```

> 如果 Node.js 缺少 `pdf-lib`，改用 **Python Pillow**：
> ```bash
> python3 -c "
> from PIL import Image
> import glob
> PAGE_WIDTH = 1280
> imgs = sorted(glob.glob('/tmp/aippt-pdf-TASK_ID/page-*.jpg'))
> pages = []
> for p in imgs:
>     img = Image.open(p).convert('RGB')
>     scale = PAGE_WIDTH / img.width
>     img = img.resize((PAGE_WIDTH, int(img.height * scale)), Image.LANCZOS)
>     pages.append(img)
> pages[0].save('/tmp/aippt-pdf-TASK_ID/marketing-plan.pdf', save_all=True, append_images=pages[1:])
> "
> ```

> 如果 Pillow 也不可用，改用 **ImageMagick**：
> ```bash
> convert /tmp/aippt-pdf-TASK_ID/page-*.jpg -resize 1280x /tmp/aippt-pdf-TASK_ID/marketing-plan.pdf
> ```

**3. 上传方案 PDF 和文稿到 tmpfiles.org**

```bash
# 上传方案 PDF
curl -s -L --max-time 60 \
  -F "file=@/tmp/aippt-pdf-TASK_ID/marketing-plan.pdf" \
  https://tmpfiles.org/api/v1/upload

# 上传方案文稿
curl -s -L --max-time 60 \
  -F "file=@/tmp/aippt-pdf-TASK_ID/marketing-report.md" \
  https://tmpfiles.org/api/v1/upload
```

将返回 URL 中的 `tmpfiles.org/` 替换为 `tmpfiles.org/dl/` 得到直链。

**4. 发送给用户**

```
![第1页](IMAGE_URL_1)
![第2页](IMAGE_URL_2)
...

📥 [方案 PDF 下载（有效期约1小时）](PDF_DIRECT_URL)

📄 [方案文稿下载（有效期约1小时）](REPORT_DIRECT_URL)

如需编辑，请前往 [小方同学](https://www.fangan.cn)
```

> - 如果某个文件上传失败，只展示成功的链接，不阻塞流程
> - 最后清理临时文件：`rm -rf /tmp/aippt-pdf-TASK_ID`
> - **发送完下载链接后，本次技能流程结束，不要追加任何额外话术（如"如需修改随时告诉我"等）**

---

## 参数依赖关系

```
第一步 login → AUTH_TOKEN
         ↓
第三步 create → text_task_id
         ↓
第四步 task/create → thread_id, message_seq
         ↓
第五步 多轮交互循环（6 轮 interrupt，每轮可 edit 重复）
         ↓
第六步 用户选择风格 → accepted + 风格名称
         ↓
第七步 task/result → 提取 job_id（content 内 JSON 二次解析）
         ↓
第八步 image/gen/job/result → 轮询获取图片 URL
         ↓
第九步 合成 PDF + 文稿 → 上传 tmpfiles.org → 返回下载链接
```
