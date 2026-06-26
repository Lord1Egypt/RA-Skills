# CEO决策助手 v2.8 安装指南

## 产品简介

CEO决策助手是一套专为中国CEO设计的AI协作体系，融合龙虾2.0主脑+子代理架构，开箱即用。

## 功能特性

- ✅ 6大代理矩阵，各司其职
- ✅ 6大定时简报，自动推送飞书
- ✅ 永久记忆系统，个性化学习
- ✅ 决策分级管理，P0-P3清晰处理
- ✅ 每日自动优化，持续进化

## 安装前提

- OpenClaw 已安装（≥2026.4.0）
- 飞书企业自建应用（App ID + App Secret）
- MiniMax API Key（或使用Qwen替代）

## 安装步骤（5分钟）

### Step 1：获取飞书凭证

1. 登录[飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置机器人能力

### Step 2：配置文件

```bash
# 克隆技能
npx clawhub@latest install ceo-ai-assistant

# 或手动下载到 skills 目录
```

### Step 3：配置飞书

编辑 `openclaw.json`，添加飞书配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "domain": "feishu",
      "accounts": {
        "main": {
          "appId": "你的APP_ID",
          "appSecret": "你的APP_SECRET",
          "dmPolicy": "allowlist",
          "allowFrom": ["你的用户ID"]
        }
      }
    }
  }
}
```

### Step 4：重启服务

```bash
openclaw gateway restart
```

### Step 5：验证安装

```bash
openclaw status
```

看到 Gateway running 即成功。

## 使用指南

### 基础指令

- "检查健康" - 系统健康检查
- "查看代理" - 各代理连接状态
- "安装技能" - 安装新技能
- "精简技能" - 移除冗余技能

### 主脑协作

- 看到"主脑"二字 → 我直接执行
- 没有"主脑"二字 → 我安排子代理执行

### 决策分级

| 等级 | 使用场景 |
|------|---------|
| P0 | 紧急情况，直接执行 |
| P1 | 次日简报中标注⏳ |
| P2 | 周例会讨论 |
| P3 | 月度复盘 |

## 定时任务说明

| 时间 | 任务 | 推送 |
|------|------|------|
| 7:50 | CEO早晨简报 | 飞书 |
| 8:00/18:00 | 超级检索日报 | 飞书 |
| 周一9:00 | 周度部门例会 | 飞书 |
| 21:00 | 日度汇总简报 | 飞书 |
| 20:00 | 知识库自动更新 | 自动 |
| 周五17:00 | 周度复盘 | 飞书 |

## 故障排除

### 飞书无法连接

1. 检查 appId/appSecret 是否正确
2. 检查机器人是否已启用
3. 检查是否已添加应用权限

### 定时任务不执行

1. 检查 cron 状态：`openclaw cron status`
2. 检查 Gateway 是否运行
3. 查看任务日志

### 模型响应慢

- MiniMax M2.7：带推理，速度慢但思考深
- Qwen3.5+：无推理，速度快

可按需切换默认模型。

## 技术支持

- 问题反馈：ClawHub 评论区
- 更新订阅：clawhub sync ceo-ai-assistant
- 文档：CEO决策协作体系v2.8.md

---

版本：v2.8.0 | 更新：2026-04-25
