---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_09278516731111f1986d525400d9a7a1
    ReservedCode1: AUyjUecqI66yaX1fOVDYxe6vVotA/3ZVz8n1xiDUPsF0yn8bSU87tChbRWJbKaT4o0ts4UZi9AJxRZmU5xkrCe94WjQvbkm9P+NkDeQYhiWERjqQ16SexUNWfh7s9DpScskLGTHTfwmekpbdxo+Kzwr+yaVdMYBtG/coirfZjkZbgN5v0w7nm7fzR84=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_09278516731111f1986d525400d9a7a1
    ReservedCode2: AUyjUecqI66yaX1fOVDYxe6vVotA/3ZVz8n1xiDUPsF0yn8bSU87tChbRWJbKaT4o0ts4UZi9AJxRZmU5xkrCe94WjQvbkm9P+NkDeQYhiWERjqQ16SexUNWfh7s9DpScskLGTHTfwmekpbdxo+Kzwr+yaVdMYBtG/coirfZjkZbgN5v0w7nm7fzR84=
---

# 飞书机器人创建概要

## 核心步骤

1. 登录飞书开放平台，创建企业自建应用
2. 为应用添加机器人能力
3. 开通消息读写相关权限
4. 开启长连接接收事件（关键步骤，默认关闭）
5. 记录应用凭证
6. 发布应用并过审
7. 将机器人加入目标群聊

## 关键注意

- 长连接接收事件开关默认关闭，必须手动打开
- 权限开通后需重新发布应用才生效
- 群信息需在手机飞书 App 获取，网页后台不显示

> 配置模板与分步操作（每步带期望日志）见部署文档：https://www.jinengpu.chat/feishu-multi-agent-detail.html
*（内容由AI生成，仅供参考）*
