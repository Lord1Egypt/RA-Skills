# Changelog

## v2.1.0 (2026-05-27)

### 新增
- **config-template.json**：示例配置模板，新用户首次使用时自动从模板创建 config.json
- **脚本自动初始化**：send_group_message.sh 检测到 config.json 不存在时自动从模板复制
- **.clawhubignore 完善**：排除 config-template.json、memories/、token 缓存等隐私/非必要文件

### 优化
- **隐私信息脱敏**：config.json、memories/ 已完全排除版本控制，发布包不含任何 open_id/chat_id
- **SKILL.md 文档更新**：补充自动初始化说明

## v2.0.0 (2026-05-20)

### 破坏性变更
- **敏感信息分离**：`config.json` 不再包含 open_id / chat_id，拆分到 `secrets.json`（不纳入版本控制）
- **脚本输出格式**：从 JSON 输出改为 source-friendly 环境变量（`CHAT_ID`, `MSG_TYPE`, `MSG_CONTENT`, `HAS_IMAGE`, `IMAGE_KEY`）
- **消息格式统一**：at=true 时固定为 3 元素结构 `text(prefix) → at(对方) → text(正文)`

### 新增
- **每日聊天机制**：闲聊时段（cron 生成）+ 聊天检查（心跳）+ 📸照片时段
- **secrets.json**：敏感信息独立存储，脚本自动合并 config.json + secrets.json
- **图片内嵌**：图片作为 `img` 标签内嵌在 post 消息中，无需额外发送

### 优化
- **脚本通用化**：`send_group_message.sh` 替代专用 `chat_to_ray.sh`，支持任意群和联系人
- **SKILL.md 文档补全**：合入聊天检查、闲聊时段、照片生成等近期新功能的完整文档
- **HEARTBEAT.md 更新**：统一使用新脚本路径和调用方式

## v1.1.0 (2026-04-18)

### 新增
- **记忆管理系统**：联系人记忆全局共享（`memories/contacts/`），按时间增量更新
- **消息来源识别**：sender_id + 前缀双重判断
- **认识新朋友机制**：遇到未知群/联系人时先征求用户同意
- **首次使用权限检查**：自动检测飞书 OAuth 权限

### 优化
- **配置结构升级**：contacts 全局共享 + 群引用
- **快捷脚本**：`send_group_message.sh` 支持图片上传

## v1.0.0 (2026-03-28)

### 初始功能
- 基础群消息发送和回复
- @ 对方通知
- 简单配置结构
