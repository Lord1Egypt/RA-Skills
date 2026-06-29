# 权限说明（Permissions）

## 操作权限权重

本技能所有操作为 **LOW 权限**，无需用户确认：

| 操作 | 权限权重 | 说明 |
|------|---------|------|
| 读取 .drawio 文件 | LOW | 只读操作 |
| 生成/写入 .drawio 文件 | LOW | 产出物写入 workspace |
| 执行 Python 脚本（drawio_templates.py 等） | LOW | 本地代码执行 |
| 打开 draw.io 预览 | LOW | 本地应用启动 |
| 版本管理（init/save/restore） | LOW | 本地文件版本控制 |

## 敏感操作说明

本技能**不涉及**以下高风险操作：
- 网络请求（无 API 调用）
- 文件系统 outside workspace（只写 `{workspace}`）
- 敏感信息读写（不访问密钥、密码、token）
- Git 操作（不执行 push/pull/commit）

## 授权方式

采用 `unified` 模式（已在 SKILL.md frontmatter 声明 `permission_weight: LOW`），所有 LOW 权限操作自动执行，无需每次确认。
