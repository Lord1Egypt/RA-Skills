---
name: feishu-scheduler
description: "飞书一句话智能排期与日程协调助手，基于事件驱动架构"
---


# 📅 飞书智能排期助手 (Feishu Scheduler)

## 技能描述 (Skill Description)
这是专门用于 OpenClaw Agent 下发的飞书环境专属 AI 工具（Skill）。
它使大语言模型具备处理**“长程协调”、“涉及多位群内飞书用户”**复杂会议预约场景的能力。
主要能力有：计算多人的日历闲忙交集、发送附带时间选项的飞书交互式卡片、以及在成员意见不合时，作为 Webhook 中控台提供实时冲突情报通知 Agent 进行多轮自动斡旋处理。

## 🤖 运行时指令：Agent 执行策略 (Execution Strategy)
作为挂载此 Skill 的 Agent，处理用户的排期请求时，需要严格遵循以下工作流机制（请阅读你的系统提示词）：

### 1. 意图解析与信息补足
- 对话用户输入：“帮我约刘总开个需求会”。
- Agent 必须检查是否满足：【参会人群（包含用户本人或其上级）】、【期望的时间范围（几号到几号，如没有则默认下周）】、【预计会议时长（单位分钟，如半小时或一小时）】。
- 如果信息不全，Agent 要利用大模型的自然语言主动**拒绝工具调用**，改口礼貌询问用户要求的内容。

### 2. 日历交集计算器 (`POST /api/claw/calc-free-time`)
- 向端点传入所需属性：`userIds`, `startTimeIso`, `endTimeIso`, `durationMinutes`。
- 获取返回结果中提供的最近 3-5 个**完全交集长短的空闲时间段 (Free Time)**。
- 只有成功拿到选项列表（也就是时间不冲突）时，才可进入第三步。如果拿到的数组为空（没有任何共同闲时），将原因转化成友好长句推还给请求用户。

### 3. 主动发包：排期卡片派发 (`POST /api/claw/dispatch-cards`)
- Agent 根据上一步拿出的可选时间，加上排期会议的话题，组合成一段 **“富有情商和商务礼仪”** 的导语作为发包请求内容（如：“诸位大佬，刚跟李总沟通过看啥时间定方案比较好，礼拜四十点这个点您看行吗？”）。
- 将该 `agentMessage` 传入卡片下发 API。
- API 响应 `SessionID` 给 Agent。**注意：收到 SessionID 意味着此任务挂起，当前 Agent 不需要再主动采取任何行动，请结束当前进程不要死等。**

### 4. 冲突判定与反弹接力 (Webhook 触发机制)
- 会话对象可能在这张“确认时间选项卡片”中出现意见不合或全点“此时均冲突”。
- Webhook 服务器 (`/api/feishu/card-webhook`) 会持续跟踪和监控所有人的投递票选比例，若出现异常分歧，Webhook 会把当前进展（包括具体的谁没投、谁选择了什么时间）组织成结构体，并带上同一 `SessionID` 去**主动反向触发 (Wake up)** 给我们的 Agent。
- Agent 在被异常唤醒之时，能够读取并判断：“噢，刘总说周三有事，周四行”，这要求 Agent 再一次使用大模型的推算能力和对话补全能力执行，带着全新计算好的时间槽二次调用**第三步 (步骤3 发派卡片)**，继续向各方斡旋，直至全部投票意见统一。

---

## 📂 微服务结构说明 (Architecture Info)

> 目录已经过符合 Miaoda 规范和 OpenClawHub 打包分发处理：

- **`index.js`**: 提供给 Agent 声明内主动发起交互动作的三组 API，以及直接供飞书开发者后台端点消费的 Webhook `/api/feishu/card-webhook` 入口。
- **`feishuService.js`**: 包含所有包含 Feishu Open API 网关交互的核心认证 (TenantAccessToken Cache)、区间合并算法、卡片 Message Card DOM 构建和真实创建日历日程模块 (`createMeeting`)。
- **`dbStore.js`**: 依赖 Node.js 文件系统读写的轻量级事务/会话记录模块，实现各端异步状态管理的防丢落地与挂起机制追踪。
- **`openapi.yaml`**: OpenClaw 一键导入时的标准大模型能力边界规范元数据定义文件。
- **`_meta.json`**: Clawhub 及第三方 Agent UI 解析插件包属性的专用格式声明包。
