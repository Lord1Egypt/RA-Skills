# 变更日志

## [1.0.0] - 2025-04-10

### 新增
- 初始版本发布
- 支持 1 种 OCR 识别类型：出生医学证明
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

## [1.0.5] - 2026-08-12

### 安全修复
- 收紧 skill.yaml 与 SKILL.md 描述，移除通用 OCR 表述，仅保留出生医学证明识别场景
- skill.yaml 新增 permissions 声明，显式列出读取本地文件、网络传输、脚本执行权限
- main.py 对 ocrType 增加白名单校验，仅允许 `BIRTH_CERTIFICATE`
- README.md 与 SKILL.md 补充隐私、数据外传、用户授权、数据保留等安全警告

## [1.0.4] - 2026-07-02

### 优化
- update ClawHub 的安全扫描V2

