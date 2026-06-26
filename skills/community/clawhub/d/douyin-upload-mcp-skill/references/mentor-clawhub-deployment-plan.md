# 抖音自动化营销 Skill ClawHub 部署方案

## 1. 结论

当前采用 **ClawHub + 本机 env 配置 + bootstrap 自举** 的部署方式。

ClawHub 负责分发：

- 抖音自动化营销 skill 文档和脚本
- OpenClaw MCP server
- 浏览器 daemon
- 小冰一键成片工具代码
- 安装说明和配置模板

目标机器负责本地配置：

- 飞书 app / 会话 ID
- 模型 API key
- 小冰一键成片 API key
- Coze / 数字人训练 API key
- 抖音首次扫码登录

密钥和登录态不上传 GitHub/ClawHub。

## 2. 部署包

已发布：

- GitHub: `https://github.com/MrChenyh/douyin-upload-mcp-skill`
- ClawHub: `douyin-upload-mcp-skill@0.1.8`

包内包含：

- `SKILL.md`
- `references/customer-install-guide.md`
- `references/skill-local-config.md`
- `references/xiaoice-service-config.md`
- `scripts/bootstrap-openclaw.js`
- `scripts/preflight.js`
- `scripts/agent-ready.js`
- `vendor/xiaoice-video-tool`

包内不包含：

- `.env` / `.env.local`
- API key / 飞书 secret / 小冰 key
- 抖音 Cookie / 浏览器 profile
- OpenClaw 会话历史
- `node_modules`
- 浏览器安装包

## 3. 安装步骤

目标机器进入 Ubuntu / WSL Ubuntu 后执行：

```bash
openclaw skills install douyin-upload-mcp-skill --force
cd ~/.openclaw/workspace/skills/douyin-upload-mcp-skill
```

如果使用 OpenClaw profile：

```bash
openclaw --profile customer-a skills install douyin-upload-mcp-skill --force
```

则目录通常是：

```bash
~/.openclaw/workspace-customer-a/skills/douyin-upload-mcp-skill
```

实际以安装命令输出的 `Installing to ...` 或 `Installed ... -> ...` 为准。

## 4. 自举配置

在 skill 目录执行：

```bash
npm ci
cp references/skill-local-config.md .env.local 2>/dev/null || cp .env.example .env.local
node scripts/bootstrap-openclaw.js --apply
```

自举会完成：

- 安装 Node 依赖
- 安装小冰工具到 `~/自动营销/xiaoice-video-tool`
- 生成小冰工具 `.env` 模板
- 检测浏览器
- 注册 OpenClaw MCP
- 启动 `douyin-skill-supervisor.service`
- 启动抖音浏览器 daemon

## 5. 需要填写的配置

编辑 skill 配置：

```bash
nano .env.local
```

至少填写：

```text
FEISHU_APP_ID=
FEISHU_APP_SECRET=
DOUYIN_FEISHU_RECEIVE_ID=
DOUYIN_FEISHU_RECEIVE_ID_TYPE=chat_id
DOUYIN_PERSONA_API_KEY=
DOUYIN_NEXT_VIDEO_PLAN_API_KEY=
DOUYIN_DATA_REPORT_API_KEY=
DOUYIN_AUTO_REPLY_API_KEY=
DIGITAL_HUMAN_COZE_TOKEN=
DIGITAL_HUMAN_TRAINING_API_KEY=
```

编辑小冰工具配置：

```bash
nano ~/自动营销/xiaoice-video-tool/.env
```

至少填写：

```text
VIDEO_SERVICE_INTERNAL_TOKEN=本机内部随机口令
VIDEO_SERVICE_ADMIN_TOKEN=本机管理随机口令
VIDEO_SERVICE_CALLBACK_TOKEN=回调随机口令
VIDEO_PROVIDER_API_BASE_URL=小冰一键成片 API 地址
VIDEO_PROVIDER_API_KEY=小冰一键成片 API key
VIDEO_PROVIDER_VH_BIZ_ID=数字人模型 ID
```

## 6. 验收命令

配置填完后运行：

```bash
node scripts/bootstrap-openclaw.js --apply
node scripts/preflight.js --online
node scripts/agent-ready.js
```

`preflight --online` 全绿后，认为环境配置完成。

## 7. 真实业务验收

飞书侧测试：

```text
发布抖音
数据报告
自动回复评论
自动回复私信
定时任务
```

首次发布需要用户扫码抖音，可能需要短信验证码或安全验证。

## 8. 已完成实测

已用纯净 OpenClaw profile 验证：

- ClawHub 可安装 `douyin-upload-mcp-skill@0.1.5+`
- OpenClaw `skills check` 可识别为 ready
- 配置模板随包保留
- 小冰工具随包保留
- `npm ci` 成功
- `bootstrap` 成功
- 小冰 `.env` 自动生成
- MCP 注册成功
- supervisor 和 daemon 启动成功

剩余必须人工完成：

- 填写目标机器 env
- 飞书授权/会话 ID 配置
- 小冰/Coze/API key 配置
- 抖音首次扫码登录

## 9. 边界

ClawHub 安装只负责把 skill 下载到 OpenClaw workspace，不会自动执行 `npm ci`、不会填密钥、不会迁移抖音登录态。

如果客户完全不会命令行，可以让 OpenClaw agent 按本文命令代执行；如果希望用户零命令行安装，则需要改用 WSL 镜像交付方案。
