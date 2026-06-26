# follow-builders-sidecar

`follow-builders-sidecar` 是原版
[`follow-builders`](https://github.com/zarazhangrui/follow-builders) 的
OpenClaw 外置增强层。它不会去改原 skill 目录，也不依赖作者接受 PR；
它只负责“接管调度与投递”，内容仍然来自上游公开 feed。

## 效果展示

这张图就是 sidecar 想交付出来的效果：不是只把 digest 发出去，而是把上游信息整理成更适合在飞书群里阅读、转发和点开的消息卡片。

![飞书卡片预览](https://raw.githubusercontent.com/AMortalsOdyssey/follow-builders-sidecar/main/assets/feishu-card-preview.jpeg)

- 支持把卡片发送到可配置的飞书群聊
- 头像使用真实来源，不再是占位图
- 姓名和身份信息都可以点击跳转回对应主页
- 同一位 builder 的多条消息可以在一张卡片里分段展示
- 每条内容都保留原文跳转入口
- 低价值、低信号推文会先过滤，减少噪声
- 转发 / quote tweet 会补读原帖上下文
- podcast 链接会修复到具体单集或视频页，而不是只落到主页

## 相对原版新增的能力

- 独立的 hourly OpenClaw cron
- 按本地时区判断“当天是否有上游更新”
- `daily` / `weekly` 成功一次即停止当天/当周重复推送
- 原版 cron 如果被重新启用，sidecar 下次运行会自动 disable
- quote tweet 内容补全
- podcast 单集真实链接修复
- 低价值内容过滤
- 模型输出校验、repair pass、程序化 fallback
- 默认 OpenClaw 渠道投递
- 可选 Feishu interactive card 投递
- 自定义 Feishu 应用缺少图片上传 scope 时，回退默认账号上传头像

## 目录说明

- `assets/feishu-card-preview.jpeg`：飞书卡片效果展示
- `SKILL.md`：OpenClaw companion skill
- `scripts/sidecar-setup.js`：首次 takeover
- `scripts/sidecar-configure.js`：后续配置修改
- `scripts/sidecar-status.js`：查看当前状态
- `scripts/sidecar-rollback.js`：回滚并可选恢复原 job
- `scripts/run-sidecar.js`：每小时运行的主入口

## 本地配置目录

sidecar 自己的配置和状态都写在：

- `~/.follow-builders-sidecar/config.json`
- `~/.follow-builders-sidecar/state.json`
- 仅在直连 Feishu 应用模式下写 `~/.follow-builders-sidecar/credentials.json`

原版 `~/.follow-builders/config.json` 只会在 takeover 时导入一次。
接管完成后，以 sidecar 配置为准。

## 接管流程

```bash
cd scripts
npm install
node sidecar-setup.js
```

如果要启用 Feishu 卡片投递，安装 / takeover 时需要先二选一：

- `openclaw_account`：复用 OpenClaw 已配置好的 Feishu 应用
- `direct_credentials`：给 sidecar 单独配置一套本地 Feishu `appId` / `appSecret` / `chatId`

接管会做这些事：

1. 一次性导入原 skill 配置
2. 查找原版 OpenClaw digest cron
3. 记录原 job id
4. disable 原 job
5. 创建 sidecar 自己的 hourly cron
6. 写入 sidecar config/state

## 投递方式

### 默认：`openclaw_announce`

默认会沿用原 job 的：

- `channel`
- `to`
- 可选 `accountId`

sidecar 运行时会主动调用 `openclaw message send` 发消息，而不是依赖
cron job 的“最后一句回复”来投递。

### 可选：`feishu_card`

Feishu 卡片投递支持两种模式：

- `openclaw_account`：复用 OpenClaw 已配置的 Feishu account，再配一个目标群聊 `chatId`
- `direct_credentials`：把 sidecar 自己用的 Feishu `appId` / `appSecret` / `chatId` 写入本地 `~/.follow-builders-sidecar/credentials.json`

如果发送应用没有图片上传 scope，会自动回退到默认 Feishu account 上传头像。

## 运行语义

- sidecar 默认每小时检查一次
- 上游是否更新，以 GitHub 上 feed 相关 commit 的时间为准
- commit 时间会先转换到 sidecar `timezone`
- 只有 commit 的本地日期与“今天”相同，才算有效更新
- `daily`：本地当天最多成功发送一次
- `weekly`：只在配置的 `weeklyDay` 允许发送，且当周最多成功一次
- 同一天即使上游连更多次，只要已经成功推送过一次，就不再重复推送

如果用户想改触发时段，直接改 sidecar 自己的 cron 即可。sidecar 不会再去同步原 skill 的 `deliveryTime`。

## 常用命令

```bash
node scripts/sidecar-status.js
node scripts/sidecar-configure.js --driver feishu_card --feishu-account follow_builders_group --feishu-chat-id oc_xxx
node scripts/sidecar-configure.js --driver feishu_card --feishu-mode direct_credentials --feishu-app-id cli_xxx --feishu-app-secret secret_xxx --feishu-chat-id oc_xxx
node scripts/run-sidecar.js --skip-delivery
node scripts/sidecar-rollback.js --reenable-original
```

## 备注

- v1 只支持 OpenClaw
- v1 不修改上游 `follow-builders` 仓库
- 上游 freshness 判断依据是 GitHub commit 时间，不是本地文件 mtime

## 协议

MIT，见 [LICENSE](LICENSE)。
