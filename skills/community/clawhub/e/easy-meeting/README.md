# Feishu Scheduler Skill for OpenClaw

这是一个针对 OpenClaw 平台设计的飞书 (Feishu) 日程排期与卡片交互的后台服务。
它可以被 OpenClaw Agent 调用来拉取指定一群人的“共同空闲时间”，并通过飞书发送“交互式卡片”供群负责人点击确认时间。

---

## 🚀 项目结构

- \`index.js\` - Express 服务端入口，暴露 OpenClaw 的调用 API，以及飞书的卡片回调 Webhook。
- \`feishuService.js\` - 核心飞书 API 封装层，负责缓存 Token、查询 FreeBusy、发送交互式卡片 (Interactive Message Card)。
- \`.env.example\` - 配置飞书核心凭证的环境变量模板。
- \`package.json\` - 依赖定义。

---

## 🛠️ 安装与配置

### 1. 飞书开放平台准备
1. 访问并登录 [飞书开放平台](https://open.feishu.cn/app/)。
2. **创建自建应用**。
3. 从“凭证与基础信息”中提取 \`App ID\` 和 \`App Secret\`。
4. 在“权限管理”中，申请以下权限并发布新版本使其生效：
   - 获取日历及日程信息 (获取空闲状态必须)
   - 以应用身份发送消息 (发送群卡片必须)

### 2. 本地初始化
复制环境变量模板，并填入你自己飞书应用的 ID 和 Secret：

\`\`\`bash
cp .env.example .env
\`\`\`

然后在项目根目录执行：

\`\`\`bash
npm install
npm run dev
\`\`\`

服务默认会运行在本地 \`http://localhost:3000\`。

---

## 📡 接口说明与集成 (OpenClaw) 

该服务暴露了两个核心路由接口：

### 1. 接受 Agent/OpenClaw 的排期请求
**POST** \`/api/claw/schedule\`

当 Agent/OpenClaw 通过 Workflow 决定为几个骨干安排会议前，它会发起此 HTTP POST 请求。

**Body 参数要求 (JSON):**
\`\`\`json
{
  "managerUserId": "ou_3333333333",          // 点击定夺按钮的负责人飞书 user_id
  "userIds": ["ou_1111111111", "ou_2222222"], // 需要查询闲忙的所有参会者飞书 user_id 数组
  "startTimeIso": "2023-10-31T09:00:00+08:00",// 约束下限时间 (ISO 8601格式)
  "endTimeIso": "2023-10-31T18:00:00+08:00"   // 约束上限时间
}
\`\`\`

### 2. 飞书卡片行为回调 (Webhook)
**POST** \`/api/feishu/card-callback\`

这个是你需要反向配置到 **“飞书开发者后台 -> 事件订阅 / 接收消息”** 中的公网 URL 地址。
如果要在本地测试，你需要用内网穿透工具（例如 ngrok 或者 cpolar）。
  
当负责人在飞书内点击了：\`[10:00 - 10:30]\` 的按钮，飞书会把信息 POST 传递回这个接口，从而让服务实现真正的建日程功能。
  
---

## 📚 开发注意与补充

1. **多时区问题**: \`feishuService.js\` 中全部依据带有时区 (\`+08:00\`) 的 ISO8601 长字符串处理。
2. **错误处理**: 如果参会者满负荷没有空隙，服务会响应 \`success: false\` 和 \`未找到空闲时段\`。
3. **真实落盘/预定**: 当前 \`index.js\` 的 \`card-callback\` 只打印了用户选择了哪个时间，没有实质去调用建日程接口 (Create Calendar Event)。你可以基于此结构在回调里接入进一步的数据库落盘或触发子 Agent 去真实预定会议室。
