# 抖音自动运营 Skill 小白安装教程

这份教程给已经装好 OpenClaw、并且已经接好飞书机器人的客户使用。

## 你会得到什么

- 自动发布抖音：飞书发 `发布抖音`，按提示扫码、发视频或字段化任务。
- 获取数据生成分析：飞书发 `更新数据` 或 `数据报告`。
- 自动回复评论：飞书发 `自动回复评论`。
- 自动回复私信：飞书发 `自动回复私信`。
- 数字人自动化营销：飞书发 `生成人设`、`训练数字人`、`开启自动化营销`。
- 定时任务：默认每 30 分钟自动回复新评论/私信；开启自动化营销后，每天 07:30 自动生成视频，待你确认后发布。

## 第 1 步：安装基础环境

如果你的机器是 Ubuntu / WSL Ubuntu，先执行这一段：

```bash
sudo apt update
sudo apt install -y curl ca-certificates gnupg git

NODE_MAJOR="$(node -p 'Number(process.versions.node.split(".")[0])' 2>/dev/null || echo 0)"
if [ "$NODE_MAJOR" -lt 22 ]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt install -y nodejs
fi

if ! command -v google-chrome >/dev/null 2>&1 && ! command -v chromium >/dev/null 2>&1; then
  sudo snap install chromium --classic || sudo apt install -y chromium-browser
fi
```

如果你已经能运行 `node -v` 且主版本号是 22 或更高，并且电脑里有 Chrome / Edge / Chromium，可以跳过这一步。

如果浏览器没装，后面的自举脚本会再自动尝试安装一次；自动安装失败时，按终端提示执行手工安装命令即可。

## 第 2 步：安装 skill

推荐通过 ClawHub 安装到当前 OpenClaw workspace：

```bash
openclaw skills install douyin-upload-mcp-skill --force
cd ~/.openclaw/workspace/skills/douyin-upload-mcp-skill
```

如果你使用了 OpenClaw profile，例如 `openclaw --profile customer-a ...`，安装目录通常会变成：

```bash
~/.openclaw/workspace-customer-a/skills/douyin-upload-mcp-skill
```

最稳妥的方式是看安装命令输出里的 `Installing to ...` 或 `Installed ... -> ...`，然后 `cd` 到实际输出的目录。后续所有命令都在这个 skill 目录里执行。

注意：OpenClaw 2026.4.2 中不要执行 `openclaw skills install douyin-upload-mcp-skill --version 0.1.0`，这里的 `--version` 会被顶层命令吃掉，表现为只打印 OpenClaw 版本但没有安装。

如果是从 GitHub 手工安装，可以用：

```bash
mkdir -p ~/openclaw-skills
cd ~/openclaw-skills
git clone https://github.com/MrChenyh/douyin-upload-mcp-skill.git
cd douyin-upload-mcp-skill
```

## 第 3 步：生成本机配置模板并自举

```bash
npm install
cp references/skill-local-config.md .env.local 2>/dev/null || cp .env.example .env.local
node scripts/bootstrap-openclaw.js --apply
```

这一步会自动完成：

- 安装当前 skill 的 Node 依赖。
- 把随包的 `vendor/xiaoice-video-tool` 安装到 `~/自动营销/xiaoice-video-tool`。
- 如果小冰工具 `.env` 不存在，会从模板生成 `~/自动营销/xiaoice-video-tool/.env`。
- 检测浏览器；缺失时会尝试自动安装 Chromium/Chrome。
- 注册 OpenClaw MCP 工具。
- 启动抖音浏览器守护进程。
- 检查中文字体，避免浏览器截图中文变方块。
- 生成本机需要填写的配置模板。

这一步默认不会因为你还没填写密钥而中断。真正的在线验收放在配置填写完成之后执行。

## 第 3.5 步：填写配置文件

公开包不包含任何密钥。你需要在本机填写两个配置文件。

第一个是 skill 配置：

```bash
nano ~/.openclaw/workspace/skills/douyin-upload-mcp-skill/.env.local
```

如果是 profile 安装或 GitHub clone 安装，就进入实际安装/clone 出来的 skill 目录编辑 `.env.local`，不要固定套用上面的默认路径。

至少需要填写：

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

第二个是小冰一键成片工具配置：

```bash
nano ~/自动营销/xiaoice-video-tool/.env
```

至少需要填写：

```text
VIDEO_SERVICE_INTERNAL_TOKEN=请设置一个本机内部随机口令
VIDEO_SERVICE_ADMIN_TOKEN=请设置一个本机管理随机口令
VIDEO_SERVICE_CALLBACK_TOKEN=请设置一个回调随机口令
VIDEO_PROVIDER_API_BASE_URL=小冰一键成片API地址
VIDEO_PROVIDER_API_KEY=小冰一键成片API密钥
VIDEO_PROVIDER_VH_BIZ_ID=数字人模型ID
```

填写完成后运行验收：

```bash
node scripts/bootstrap-openclaw.js --apply
node scripts/preflight.js --online
node scripts/agent-ready.js
```

## 第 4 步：开启默认定时任务

```bash
node scripts/douyin-schedule-manager.js install-default
node scripts/douyin-schedule-manager.js status
```

默认任务：

- 每 30 分钟：检查新增未回复评论和未读私信，并按内容自动回复。
- 开启自动化营销后每天 07:30：自动生成视频，待你回复【确认发布】后发布。

## 第 5 步：在飞书里使用

常用指令：

```text
发布抖音
生成人设
训练数字人
开启自动化营销
更新数据
数据报告
自动回复
自动回复评论
自动回复私信
截图
定时任务
```

修改定时任务：

```text
修改定时任务 自动回复 30分钟
修改定时任务 自动化营销 07:30
关闭定时任务
开启定时任务
```

字段化发布任务格式：

```text
tags:#宠物险#保险
"封面图片": "https://example.com/cover.png"
标题："养宠不焦虑的秘诀？"
"视频地址": "https://example.com/video.mp4"
```

数字人训练材料格式：

```text
姓名：张三
照片：https://example.com/photo.jpg
性别：男
年龄：35
从业年限：8年
主营业务：...
核心优势：...
目标客户：...
个人特质：...
经验案例：...
IP核心诉求：...
禁忌与偏好：...
```

先发送上述信息生成人设，系统会返回账号定位方案并等待用户确认。用户回复 `确认人设` 后，系统会自动用已确认人设和本人照片请求 Coze 生成训练视频，并提交小冰质检和训练；客户已有数字人时也可以直接发送 `绑定数字人ID xxxxx`。默认 model id 只用于 demo、应急降级或稳定性 dry-run。

## 登录提醒

首次使用或登录失效时：

1. 飞书发 `发布抖音`。
2. 系统提示准备扫码后，回复 `发送二维码`。
3. 在电脑端飞书查看二维码，用手机抖音 App 扫码。
4. 扫码确认后回复 `已登录`。
5. 如果需要短信验证码，直接回复 6 位数字。

注意：抖音手机端通常不能直接扫描同一台手机相册里的二维码，所以建议在电脑端飞书查看二维码。

## 常见问题

### 飞书没反应

运行：

```bash
node scripts/openclaw-douyin-health.js --fix --restart-gateway
```

然后在飞书重新发送上一条指令。

### 浏览器没有打开或连接失败

运行：

```bash
node scripts/bootstrap-openclaw.js --apply
node scripts/openclaw-douyin-health.js --fix --restart-gateway
```

### 二维码过期

飞书回复：

```text
发送二维码
```

系统会重新获取最新二维码，不要使用旧图。

### 想看当前页面

飞书发送：

```text
截图
```

系统会把当前抖音页面截图发回飞书。

### 定时任务不确定有没有开启

飞书发送：

```text
定时任务
```

或命令行执行：

```bash
node scripts/douyin-schedule-manager.js status
```
