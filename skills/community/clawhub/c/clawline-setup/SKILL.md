# ClawLine Setup

通过对话一键安装并配置 ClawLine 手机 App 与 OpenClaw 的连接，无需任何命令行操作。

## 能做什么

安装此 Skill 后，直接在任意聊天窗口对 OpenClaw 说自然语言即可完成全部配置：

- **安装 ClawLine**：检查并自动安装 ClawLine Channel Plugin
- **绑定手机**：提供 UUID 后立即写入配置并重启网关
- **随时重新绑定**：说出新 UUID 即可覆盖旧配对
- **查看状态**：随时查询连接状态和实例信息
- **断开连接**：清除配对信息

## 使用示例

```
你：帮我安装 ClawLine
AI：✅ ClawLine Channel Plugin 安装成功。
    下一步需要绑定你的手机：
    1. 打开 ClawLine App
    2. 进入"添加实例"页面
    3. 给实例命名（如"我的电脑"）
    4. 复制页面显示的 UUID
    复制后直接告诉我即可。

你：ClawLine 的 UUID 是 a1b2c3d4-e5f6-7890-abcd-ef1234567890
AI：✅ UUID 已更新。网关重启后，请在 App 的"实例管理"→ 待确认列表中确认配对即可。
```

## 安装方式

此 Skill 由 clawhub 通过以下命令自动安装：

```bash
openclaw plugins install @openclawline/clawline-setup
```

## 触发关键词

| 说什么 | 触发的操作 |
|--------|-----------|
| 帮我安装 ClawLine | 检查并安装 Channel Plugin |
| 安装 ClawLine | 同上 |
| ClawLine 的 UUID 是 xxxx | 设置/更新连接 UUID |
| ClawLine 连接状态 | 查看当前配置 |
| 断开 ClawLine | 清除配对信息 |

## 相关链接

- GitHub：https://github.com/qtx0213/clawline
- ClawLine App：https://openclawline.com
- npm 包：https://www.npmjs.com/package/@openclawline/clawline-setup
