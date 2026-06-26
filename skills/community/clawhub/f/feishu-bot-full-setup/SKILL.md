---
name: feishu-bot-creator
description: 创建飞书企业自建机器人，并完成权限导入、事件订阅、卡片回调和版本发布全流程。适用于创建飞书机器人、飞书应用机器人，或自动化完成飞书开放平台建机器人流程的场景。
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "🤖"
---

# feishu-bot-creator

使用这个 skill 时，优先把它当成**主 agent 的标准化工作流**，而不是“用户直接运行的脚本说明”。

## 目录说明

- `scripts/create_feishu_bot.py`：执行实际创建流程的脚本
- `references/permissions.md`：默认申请的权限、事件、卡片回调清单；仅在需要核对或调整权限时读取

## 适用边界

适用于：
- 新建飞书企业自建机器人
- 自动完成机器人开通、权限导入、事件订阅、卡片回调、版本创建与提交发布
- 需要拿到 `app_id` 和 `app_secret`

不适用于：
- 修改已有飞书应用的复杂配置
- 处理企业审批、人工审核、管理员授权等必须人工完成的步骤
- 直接承诺“脚本自己会把二维码发给用户”——当前脚本只会把二维码 PNG 写到本地，**由主 agent 负责发送给用户**

## 标准执行顺序

### 1. 先收集初始信息
优先使用 `feishu_ask_user_question` 询问：
1. 机器人名称（必填）
2. 机器人描述（可为空；为空时默认与名称一致）
3. 是否自定义头像
4. 若自定义头像，要求用户提供本地图片或可下载图片地址

如果用户已经明确给出这些信息，就不要重复询问。

### 2. 初始化运行环境
首次使用或环境不确定时，先执行：

```bash
python3 ~/.openclaw/workspace/skills/feishu-bot-creator/scripts/create_feishu_bot.py init
```

### 3. 用环境变量注入参数后执行创建
按已收集的信息设置环境变量，再执行：

```bash
python3 ~/.openclaw/workspace/skills/feishu-bot-creator/scripts/create_feishu_bot.py create
```

## 常用环境变量

- `FEISHU_BOT_NAME`：指定机器人名称
- `FEISHU_BOT_DESC`：指定机器人描述；不填时默认使用名称
- `FEISHU_BOT_AVATAR_PATH`：指定机器人头像本地图片路径
- `FEISHU_BOT_QR_PNG_PATH`：指定登录二维码输出路径，便于发送给用户

### 4. 处理二维码登录
脚本执行过程中会把登录二维码写到本地 PNG（默认 `/tmp/feishu-login-qr.png`）。

主 agent 必须：
1. 读取该 PNG 是否已生成
2. 通过当前会话把二维码图片发给用户
3. 提示用户用飞书扫码并确认登录
4. 等待用户完成扫码后再继续观察脚本结果

### 5. 读取结果并返回
成功时，脚本标准输出只有一行 JSON：

```json
{"app_id":"...","app_secret":"..."}
```

主 agent 应：
- 解析 JSON
- 明确返回 `app_id` 与 `app_secret`
- 同时告知用户脚本已完成哪些步骤

## 失败处理

### 权限或发布失败
先判断是否属于以下情况：
- 当前账号没有创建/发布企业自建应用权限
- 某些 scope 在当前企业不可用
- 飞书开放平台接口临时失败

必要时读取 `references/permissions.md`，核对脚本里申请的权限、事件与卡片回调。

### 二维码相关问题
如果二维码未生成或过期：
- 先检查 `/tmp/feishu-login-qr.png` 是否存在
- 默认可直接重新执行创建流程；同一路径下二维码会被新文件覆盖
- 只有在浏览器残留、锁文件未释放或连续异常失败时，才执行清理：

```bash
python3 ~/.openclaw/workspace/skills/feishu-bot-creator/scripts/create_feishu_bot.py cleanup
```

## 关键事实

脚本当前已实现：
- 自动登录页拉起与二维码生成
- 创建应用
- 获取密钥
- 开启机器人能力
- 导入权限
- 配置事件订阅
- 配置卡片回调
- 创建版本并提交发布
- 给创建者发送成功通知

脚本当前**未实现**：
- 自己向当前聊天发送二维码
- 自己向用户发起交互问答卡片

这两部分由主 agent 在 skill 工作流里补齐。
