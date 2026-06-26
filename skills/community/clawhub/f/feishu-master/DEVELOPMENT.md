# Feishu Skill Development Guide

本文档说明如何开发和维护 Feishu Skill。

## 目录结构

```
feishu-master/
├── SKILL.md                   # 用户文档 (主入口)
├── DEVELOPMENT.md             # 本文档 - 开发规范
├── scripts/
│   ├── __init__.py            # Python 包初始化
│   ├── get_token.py           # Token 获取与缓存
│   ├── script_index.json      # 脚本索引文件
│   ├── .gitignore             # 忽略敏感文件
│   ├── [api_scripts]/         # API 脚本 (按需添加)
│   └── env/
│       ├── .gitkeep           # 保持目录结构
│       ├── app.example.json   # 应用配置模板
│       ├── app.json           # 应用配置 (用户填写，不提交)
│       └── token_cache.json   # Token 缓存 (自动生成，不提交)
└── references/
    ├── README.md              # 文档说明
    ├── .gitkeep               # 保持目录结构
    ├── feishu_api.md          # API 摘要参考
    └── doc_urls.txt           # API 文档 URL 集合
```

## 脚本开发标准

### 1. Docstring 规范

每个脚本必须有完整的 docstring，包含以下部分：

```python
"""
[简要功能描述，一行]

[详细功能说明，描述脚本的作用和适用场景]

Usage:
    python3 script.py <param1> <param2> [options]

Parameters:
    param1: 参数说明 (类型、取值范围等)
    param2: 参数说明

Options:
    --option-name: 选项说明
    --page-size: 每页数量 (default: 20)
    --help, -h: 显示帮助信息

Output:
    JSON 格式输出:
    {
      "code": 0,
      "msg": "success",
      "data": { ... }
    }

Error Codes:
    0: 成功
    1: 参数错误
    2: API 调用失败

References:
    飞书 API 文档: https://open.feishu.cn/document/...
"""
```

### 2. Help 支持

必须支持 `--help` 和 `-h` 参数，打印 docstring：

```python
def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return
    # ... 其他逻辑
```

### 3. Token 使用规范

必须通过 `get_token.py` 获取 token，不要在脚本中重复实现：

```python
def get_token():
    """获取飞书 token"""
    result = subprocess.run(
        [sys.executable, str(TOKEN_SCRIPT)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()
```

### 4. JSON 输出格式

所有脚本必须输出标准 JSON 格式结果：

```python
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 5. 错误处理

- API 调用失败时返回标准错误响应
- 提供友好的错误提示
- 使用 `sys.exit(1)` 表示错误退出

### 6. 导入模块

```python
import sys
import json
import subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests 库未安装，请运行: pip install requests", file=sys.stderr)
    sys.exit(1)
```

## 索引维护规范

### 添加新脚本到 script_index.json

每个新脚本必须添加到 `scripts/script_index.json`：

```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T12:00:00Z",
  "scripts": [
    {
      "name": "script_name",
      "description": "脚本功能描述（中文）",
      "usage_hint": "python3 script_name.py <param1> <param2>",
      "added_date": "2026-02-12",
      "tags": ["tag1", "tag2", "tag3"]
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 脚本名称，使用下划线命名法（同时也是脚本文件名） |
| `description` | string | 是 | 功能描述，简明易懂 |
| `usage_hint` | string | 是 | 使用提示，格式如 `python3 script.py <param>` |
| `added_date` | string | 是 | 添加日期，ISO 格式 `YYYY-MM-DD` |
| `tags` | array | 是 | 标签数组，用于搜索匹配 |

### tags 推荐命名

- **功能类型**: `group`, `user`, `message`, `file`, `calendar`
- **操作类型**: `list`, `get`, `create`, `update`, `delete`, `send`
- **其他**: `member`, `info`, `upload`, `download`

## Token 使用规范

### 规范要点

1. 所有 API 脚本必须使用 `get_token.py` 获取 token
2. 不要在 API 脚本中重复实现 token 获取逻辑
3. Token 缓存机制由 `get_token.py` 统一管理
4. Token 有效期为 2 小时，提前 5 分钟自动刷新

### 错误代码

常见错误：
- `99991663`: 无效的 tenant_access_token（配置错误）
- `99991668`: tenant_access_token 已过期（缓存刷新问题）

## 测试流程

### 开发测试

1. **本地测试脚本**
   ```bash
   python3 scripts/get_token.py --check  # 验证 token
   python3 scripts/your_script.py --help
   python3 scripts/your_script.py <params>
   ```

2. **检查 JSON 输出格式**
   ```bash
   python3 scripts/your_script.py <params> | python3 -m json.tool
   ```

3. **更新索引文件**
   ```bash
   # 手动更新 script_index.json 或编写脚本自动更新
   ```

### 测试应用

建议使用测试应用进行开发：
- 在飞书开放平台创建测试应用
- 获取 test app_id 和 test app_secret
- 使用测试群组和数据避免影响正式环境

## 文档更新流程

### 1. 新 API URL 记录

添加 API 文档 URL 到 `references/doc_urls.txt`：

```txt
## 用户
- 获取用户信息: https://open.feishu.cn/document/server-docs/contact-v3/user/get_user
```

### 2. API 摘要更新

如果 API 是常用 API，更新 `references/feishu_api.md`：

```markdown
### 用户 API

#### 获取用户信息

- **Endpoint**: `GET /open-apis/contact/v3/users/:user_id`
- **用途**: ...
```

### 3. last_updated 更新

每次更新 `script_index.json` 时，更新 `last_updated` 字段：

```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T15:30:00Z",
  ...
}
```

## Context7 使用指南

### 查询 API 文档

当需要实现新 API 时，使用 Context7 查询最新文档：

```
Library: open.feishu.cn / larksuite
Query: "如何获取用户详细信息"
```

### 获取代码示例

```
Library: open.feishu.cn / larksuite
Query: "get user info python example"
```

## 版本管理

### 版本号规范

遵循语义化版本 `MAJOR.MINOR.PATCH`：
- `MAJOR`: 不兼容的 API 变更
- `MINOR`: 向后兼容的功能性新增
- `PATCH`: 向后兼容的问题修正

当前版本：`1.0.0`

### 更新记录

在 SKILL.md 或脚本 docstring 中记录重要变更。

## 最佳实践

### 1. 代码风格

- 使用 4 空格缩进
- 单行宽度不超过 120 字符
- 函数名使用 snake_case
- 常量名使用 UPPER_CASE

### 2. 性能考虑

- 重用 token 减少不必要的请求
- 合理设置超时时间（建议 10-30 秒）
- 处理分页数据时避免一次性获取所有数据

### 3. 安全性

- 不要将敏感信息（app_id, app_secret, token）提交到版本控制
- 使用 .gitignore 保护敏感文件
- token 只有 2 小时有效期，已过期的 token 会自动刷新

### 4. 用户体验

- 提供清晰的错误提示
- 支持 `--help` 查看使用说明
- 输出格式一致（JSON）

## 故障排查

### 常见问题

**问题**: `Error: 配置文件不存在 scripts/env/app.json`
- **解决**: 创建 `scripts/env/app.json` 并填入 app_id 和 app_secret

**问题**: `Error: requests 库未安装`
- **解决**: 运行 `pip install requests`

**问题**: API 返回错误码 `99991663`
- **解决**: 检查 `scripts/env/app.json` 中的 app_id 和 app_secret 是否正确

**问题**: API 返回错误码 `99991668`
- **解决**: 删除 `scripts/env/token_cache.json` 强制刷新 token

## 参考资料

- [飞书开放平台](https://open.feishu.cn/)
- [飞书 API 文档](https://open.feishu.cn/document/server-docs/)
- [飞书错误码](https://open.feishu.cn/document/server-docs/api-call/error-code)
- SKILL.md - 用户文档