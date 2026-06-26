# Create Discord Ticket Skill

## 描述
此技能允许机器人在 Discord 服务器中为用户创建一个专用的私密频道（Ticket）。

## 使用场景
1. **自动修复失败**：当 `auto_repair_transaction` 无法解决交易卡住问题时。
2. **复杂技术错误**：遇到 `nonce_error` 或 `Computed Result Error` 需要人工干预时。
3. **隐私保护**：当需要用户提供详细的转账记录、截图或其他敏感信息时。

## 约束
- 只能在用户提出明确的业务故障且无法自动解决时调用。
- 调用前需告知用户：“我将为您开启一个私密频道以保护您的隐私”。

## 参数说明
- `username`: 用户的 Discord 昵称（用于命名频道）。
- `userId`: 用户的 Discord 唯一 ID（用于设置频道访问权限）。
- `issue`: 简短的问题描述（如 "AOX_STUCK"）。