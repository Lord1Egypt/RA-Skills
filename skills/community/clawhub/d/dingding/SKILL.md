---
name: "钉钉"
version: "2.0.0"
description: "钉钉群机器人工具与开放平台开发指南。Use for: (1) 用附带的零依赖 CLI 向钉钉群发通知——文本/markdown/链接卡片，支持加签安全模式和@人, (2) CI/监控/日报等自动化通知场景, (3) 钉钉开放平台 API（token/审批/通讯录）开发指导。DingTalk group-robot CLI (zero-dependency, HMAC-signed webhook) plus Open Platform development guide."
tags: ["dingtalk", "dingding", "bot", "webhook", "enterprise", "cli"]
author: "ClawSkills Team"
category: "enterprise"
---

# 钉钉 Skill

附带零依赖 CLI（`scripts/dingbot.py`，仅 Python 标准库），agent 可直接
向钉钉群发通知——这是 agent 自动化里最高频的钉钉需求：任务完成、
构建结果、监控告警、定时日报，一条命令送达。

## 快速开始

```bash
# 群设置 → 智能群助手 → 添加机器人 → 自定义。安全设置选"加签"
export DING_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=xxx'
export DING_SECRET='SECxxxxxx'   # 加签密钥；用关键词/IP模式则不设

python3 scripts/dingbot.py text "部署完成 ✅" @all
python3 scripts/dingbot.py markdown "巡检日报" report.md
python3 scripts/dingbot.py link "新版本发布" "点击查看详情" https://example.com
```

脚本行为声明：仅请求 `oapi.dingtalk.com`；`markdown` 命令的第二参数
若是本地文件路径则读取该文件，其余不读写本地文件。

## 命令手册

| 命令 | 作用 |
|------|------|
| `text <内容> [@手机号,手机号\|@all]` | 文本消息，可@指定成员或所有人 |
| `markdown <标题> <md文件或内容>` | markdown 消息（标题显示在会话列表） |
| `link <标题> <正文> <跳转URL> [图片URL]` | 链接卡片 |

加签算法已内置：`sign = base64(hmac_sha256(secret, "{毫秒时间戳}\n{secret}"))`
再 urlencode 拼进 URL——手写这个签名是接钉钉机器人最常见的翻车点。

## Agent 典型用法

1. **CI/CD 通知**：构建、测试、部署完成后 `text` 一条结果到项目群
2. **监控告警**：脚本巡检发现异常 → `markdown` 发结构化告警
   （标题带级别 emoji，正文列指标）
3. **定时日报**：cron 任务生成 md 报告 → `markdown` 推送
4. **@ 精确提醒**：告警 @值班人手机号 而不是打扰全群

## 实战要点与错误码（实测）

| errcode | 含义 | 处理 |
|---------|------|------|
| 300005 | token 不存在 | webhook URL 拼错或机器人被移除 |
| 310000 | 安全设置校验失败 | 关键词模式=内容必须含设定词；加签模式=检查 DING_SECRET；IP模式=出口IP不在白名单 |
| 130101 | 发送太快被限流 | 每机器人 **20 条/分钟**，超限封 10 分钟 |

- 安全模式三选一（关键词/加签/IP 白名单），**推荐加签**：关键词模式
  会强迫每条消息都带那个词，IP 模式对动态出口不友好
- markdown 支持的语法是子集：标题/引用/加粗/链接/图片/有序无序列表，
  **不支持表格**——需要表格就发正文截图或链接卡片
- @手机号 只在 `text` 类型生效；markdown 里 @ 需正文含 `@手机号` 且
  at 字段同时传（本脚本 text 已封装）

## 开放平台开发速查（服务端 API）

- 旧版域名 `oapi.dingtalk.com`（gettoken 参数式），新版 `api.dingtalk.com`
  （token 放 Header `x-acs-dingtalk-access-token`），新旧接口长期并存
- access_token：`GET /gettoken?appkey=&appsecret=`，有效期 7200 秒，
  必须中心化缓存
- 常用能力：工作通知（`/topapi/message/corpconversation/asendv2`）、
  审批实例、通讯录、考勤打卡数据。参数以 open.dingtalk.com 文档为准
- 企业内部应用最简单（免审核）；第三方应用要走应用市场审核

## 本 skill 不做什么

- 不含钉钉个人号自动化（协议逆向属封号高危区）
- Stream 模式回调、AI 助理（钉钉 AI PaaS）等新能力未覆盖，
  以官方文档 open.dingtalk.com 为准
- 群发通知打扰面大，@all 使用前 agent 应向用户确认
