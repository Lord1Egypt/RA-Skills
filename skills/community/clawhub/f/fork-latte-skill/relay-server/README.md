# 报名中转服务（relay-server）

![Mode](https://img.shields.io/badge/mode-lark__cli%20%7C%20feishu__api-blue) ![Stack](https://img.shields.io/badge/stack-Node.js%20%2B%20Feishu%20Bitable-green) ![API](https://img.shields.io/badge/api-REST-orange)

把报名信息写入飞书多维表格的**服务端**。飞书凭证只存在这里的环境变量里，客户端 Skill 仅持有一个普通 URL，看不到任何飞书细节。

## 两种写入模式

| 模式 | 适用场景 | 前置条件 |
|------|----------|----------|
| `lark_cli` | 本地快速验证 | 本机已安装并授权 `lark-cli`，无需建飞书应用 |
| `feishu_api` | 生产 / 可部署 | 一个飞书自建应用 + 多维表格权限（应用身份，区别于个人账号） |

## 快速开始（lark_cli 本地验证）

```bash
cd relay-server
cp .env.example .env
# 编辑 .env：MODE=lark_cli，填入 FEISHU_BASE_TOKEN / FEISHU_TABLE_ID
node server.js
```

服务端默认监听 `http://localhost:3000`。客户端（Skill）把 `endpoint` 指向它即可。

## feishu_api 模式配置

### 步骤一：建应用拿凭证
1. 打开 [飞书开放平台](https://open.feishu.cn) → 开发者后台。
2. 创建应用 → 企业自建应用 → 填名称（如 `signup-relay`）→ 创建。
3. 应用内「凭证与基础信息」→ 复制 **App ID** 和 **App Secret**（即 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`）。

### 步骤二：开通多维表格权限
1. 应用左侧「权限管理」→ 搜索 `bitable` → 开通**多维表格**读写权限。
2. 「版本管理与发布」→ 创建版本 → 发布（权限通常发布后才对 API 生效）。

### 步骤三：把应用加进你的多维表格（最容易被漏，关键）
光有 App Secret 不够，应用必须成为那张表的「可编辑」成员：
1. 打开你的多维表格 → 右上角「共享 / 成员」→「添加协作者」。
2. 搜索你刚建的应用名 → 选「可编辑」→ 确认。

### 步骤四：填 .env
```
MODE=feishu_api
PORT=3000
API_KEY=                # 可选，建议设一个防刷
FEISHU_BASE_TOKEN=你的BASE_TOKEN
FEISHU_TABLE_ID=你的TABLE_ID
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
FEISHU_DOMAIN=https://open.feishu.cn
```
`BASE_TOKEN` / `TABLE_ID` 与 lark_cli 模式同一张表；也可从表 URL `.../base/{BASE_TOKEN}?table={TABLE_ID}` 取到。`.env` 已被 gitignore，不进仓库。

### 步骤五：启动 & 自测
```bash
cd signup-agent
node --env-file=relay-server/.env relay-server/server.js
# 另开终端
curl -s -X POST http://localhost:3000/api/signup -H "Content-Type: application/json" \
  -d '{"name":"飞书API测试","job":"工程师","wechat":"wx_test","experience":"有"}'
# 预期 {"ok":true,"record_id":"rec..."}
```

### 底层接口（理解“写”就是这两个请求）
1. 拿 `tenant_access_token`：
```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'
# 返回 {"code":0,"tenant_access_token":"t-xxx","expire":7200}
```
2. 写记录：
```bash
curl -X POST https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_TOKEN}/tables/{TABLE_ID}/records \
  -H "Authorization: Bearer t-xxx" -H "Content-Type: application/json" \
  -d '{"fields":{"名字":"张三","职业":"工程师","微信号":"wx","有无创业经验":[{"text":"有"}]}}'
# 单选字段值是 [{"text":"有"}]，文本字段是普通字符串
```

## 接口

### 查重 `GET /api/signup/exists?wechat=XXX`
返回该微信号是否已有记录（同一人 = 微信号相同）。
```json
{ "ok": true, "exists": true, "record_id": "recxxxx",
  "fields": { "名字": "张三", "职业": "程序员", "微信号": "wxid_abc", "有无创业经验": "有" } }
```

### 报名 `POST /api/signup`
```json
{ "name": "张三", "job": "程序员", "wechat": "wxid_abc", "experience": "有" }
```
- 带上 `overwrite: true` + `record_id` → 覆盖（更新）已有记录；否则新增。
- 成功：`{ "ok": true, "record_id": "recxxxx", "overwritten": false }`
- 失败：`{ "ok": false, "error": "..." }`（401 未带 key / 400 校验失败 / 500 写入失败）

## 查重与覆盖

- 查重按**微信号**判定「同一人」（名字可变）。
- 客户端先调 `exists`；若 `exists:true`，问用户「覆盖还是新增」：
  - 覆盖 → 带 `overwrite:true` + `record_id` 提交，更新那条记录；
  - 新增 → 普通提交，再建一条。

## 常见报错

| 报错 | 原因 | 解决 |
|------|------|------|
| `无权限` / `code: 1254049` | 应用没被加进表（步骤三漏了）或权限未发布 | 把应用加为表「可编辑」成员并发布版本 |
| `invalid app` / `code: 400` | App ID / Secret 填错 | 核对凭证与基础信息 |
| 单选写入报选项不存在 | 表里「有无创业经验」缺少对应选项 | 先在表里建好「有 / 无」两个选项 |
| `91403 Forbidden` | 应用未被授权访问该 base | 检查步骤二 / 步骤三，确认应用有 bitable 权限且已加为成员 |

## 部署位置（让别人也能写你的表）

- **本地 + 内网穿透**：`cloudflared tunnel --url http://localhost:3000` 或 ngrok，得到公网 URL 填进 Skill 的 `config.json`。
- **Serverless**：Cloudflare Workers / Vercel / 阿里云函数计算等，把 `server.js` 包成 HTTP 函数（注意用平台方式读取环境变量）。
- **VPS**：`node server.js` + 反向代理（Nginx / Caddy）+ HTTPS。

> 建议设 `API_KEY`，并在 Skill 的 `config.json` 里带上，避免端点被任意调用刷表。

## 安全

- `.env` 含飞书凭证，**已被 `.gitignore` 排除，切勿提交**。
- 客户端 Skill 永远不接触飞书 token，只 POST 到你的 endpoint。
