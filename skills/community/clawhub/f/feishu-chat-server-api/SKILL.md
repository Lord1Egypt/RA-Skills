---
name: feishu-chat-server-api
description: Manage Feishu group chats through Feishu server APIs, including create, get details, list members, add members, remove members, and disband chats.
metadata: {"openclaw":{"emoji":"💬","homepage":"https://github.com/wodenwang/feishu-extension-skills","os":["darwin","linux"],"requires":{"bins":["uv"]},"install":[{"id":"brew-uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)","os":["darwin"]}]}}
---

# Feishu Chat Server API

这个 skill 负责飞书群组管理相关能力，当前覆盖以下 action：

- `feishu-chat-create`
- `feishu-chat-get`
- `feishu-chat-members-list`
- `feishu-chat-member-add`
- `feishu-chat-member-remove`
- `feishu-chat-disband`

## 何时使用

当用户请求与飞书群组本身相关的操作时使用这个 skill，例如：

- 创建一个新群
- 查看某个群的详情
- 列出群成员
- 往群里加人
- 从群里移人
- 解散群

如果用户请求的是消息发送、卡片、文档、多维表格、审批等能力，不要用这个 skill，应该路由到对应模块级 skill。

## 路由规则

根据用户意图选择具体 action：

- 创建群：`feishu-chat-create`
- 获取群详情：`feishu-chat-get`
- 获取群成员列表：`feishu-chat-members-list`
- 拉人入群：`feishu-chat-member-add`
- 移出群成员：`feishu-chat-member-remove`
- 解散群：`feishu-chat-disband`

不要把“移除一个成员”和“解散整个群”混淆。

## 通用输入

凭证优先级如下：

1. action 显式传入 `app_id` / `app_secret`
2. 当前工作目录下的 `.local/feishu-extension-skills.json`
3. 环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`

如果这 3 层都没有命中，调用会失败。

也可以在调用命令里通过 `--config-file /path/to/file.json` 显式指定本地配置文件路径。

群相关 action 还需要按场景提供：

- `chat_id`
- `name`
- `user_id_list`
- `member_id`

约束：

- 只接受飞书 `user_id` 或 `open_id`
- 不要自行猜测邮箱、手机号、姓名对应的用户 ID

## 调用命令

统一调用入口：

```bash
uvx --from git+https://github.com/wodenwang/feishu-extension-skills.git feishu-extension-skills invoke <action> --args-json '<json>'
```

ClawHub 安装：

```bash
clawhub install feishu-chat-server-api
```

本地配置文件示例：

```json
{
  "app_id": "cli_xxx",
  "app_secret": "sec_xxx"
}
```

示例：

```bash
uvx --from git+https://github.com/wodenwang/feishu-extension-skills.git feishu-extension-skills invoke feishu-chat-create --args-json '{"app_id":"cli_xxx","app_secret":"sec_xxx","name":"项目临时群","user_id_list":["ou_xxx","ou_yyy"]}'
```

```bash
uvx --from git+https://github.com/wodenwang/feishu-extension-skills.git feishu-extension-skills invoke feishu-chat-member-add --args-json '{"app_id":"cli_xxx","app_secret":"sec_xxx","chat_id":"oc_xxx","user_id_list":["ou_xxx"]}'
```

## 当前未覆盖

这个 skill 当前还没有封装以下群治理接口：

- 更新群信息
- 更新群发言权限
- 获取群成员发言权限
- 更新群置顶 / 撤销群置顶
- 获取用户或机器人所在的群列表
- 搜索可见群列表
- 获取群分享链接
