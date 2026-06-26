# 变更日志

## [1.0.0] - 2025-04-10

### 新增
- 初始版本发布
- 支持 1 种 OCR 识别类型：定额发票
- 从 `.env` 文件读取 API Key
- 友好的配置检测和 Token 过期提示
- 输出识别结果为 JSON 格式

## [1.0.1] - 2025-04-13

### 优化
- update channelTag

## [1.0.2] - 2025-04-15

### 优化
- update ClawHub 的安全扫描

## [1.0.3] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V1

## [1.0.4] - 2025-04-16

### 修复
- 修正 skill.yaml 中的 homepage 为可验证地址
- 替换 README 为简洁版本，移除内部 GitLab 链接
- 删除 SKILL.md 中误导性的身份证/通用OCR示例
- 增加隐私安全警告
- 保留 API 返回的 confidence 字段