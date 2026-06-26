# claude-wechat-bridge-with-files

让 OpenClaw / Claude Code（CLI）通过微信 ClawBot 收发消息的桥接配置 skill，**带图片 / 文件 / 语音 / 视频补丁 + 主动发送**。

基于第三方 npm 包 [`claude-wechat-channel`](https://www.npmjs.com/package/claude-wechat-channel)（fengliu222 维护）+ 微信官方 ClawBot 接口。原版只透传文本、且只能「响应」，本 skill 在它之上加了两块：

**① 媒体补丁**（给 `monitor.js`，收方向）：

- 收图片 → 落 `~/.wechat-claude/media/`，在消息里注入 `[图片: <绝对路径>]`
- 收文件（PDF / DOCX / ...）→ 同上，注入 `[文件: <绝对路径>]`
- 收语音 → `[语音文件: <绝对路径>]`
- 收视频 → `[视频: <绝对路径>]`

Claude 拿到路径后用 Read tool 直接读：图片靠多模态看，PDF 用 `pypdf` 抽文本。

**② 主动发送 `wsend.js`**（v1.2.0 新增，发方向）：

官方 `reply` 工具只能「响应」——必须用户先发消息、Claude 才能回。`wsend.js` 扒了底层 ilink 接口后发现
`POST /ilink/bot/sendmessage` 接受不带 `context_token` 的纯文本，于是直接复用账号凭证打这个接口，
**让 Claude 无需用户先发消息就能主动推消息到微信**：

```bash
node wsend.js "长任务跑完了，结果在桌面 result.html"
node wsend.js - < message.txt          # 长文走 stdin
node wsend.js --to <userId> "文字"      # 指定接收人
```

已验证（2026-06-02）：零入站、纯主动，用户手机微信实收。典型用途：长任务主动汇报、定时把结果推给你。

## 装一下

1. 把整个 repo 拖到 `~/.claw/skills/claude-wechat-bridge/`
2. 按 [`SKILL.md`](./SKILL.md) 走完 1-4 步装好原版 bridge
3. 第 5 步装图片文件补丁：
   ```bash
   bash ~/.claw/skills/claude-wechat-bridge/apply-media-patch.sh
   pkill -f claude-wechat-channel
   ```
4. 主动发送开箱即用（绑定登录后凭证已在 `~/.wechat-claude/`）：
   ```bash
   node ~/.claw/skills/claude-wechat-bridge/wsend.js "wsend 自测 ✅"
   ```

## 适用

- 需要在不在电脑前的时候继续给 Claude 喂任务（语音、截图、PDF、文件）
- 让 Claude 处理一份手机微信里收到的 BP / 报告 / 名片
- **长任务主动汇报**：AI 在电脑跑批量活，跑完 / 卡住时主动用微信通知你
- ClawBot loop 类长任务的人机互动

## 不适用 / 限制

- **主动发纯文本** 已打通（`wsend.js`，已验证）；**主动发图片 / 文件** 暂未验证（媒体走 getuploadurl，可能仍依赖入站 context_token）
- macOS / Linux / Windows 都行，Mac 测过最多
- 必须电脑常开

## License

MIT
