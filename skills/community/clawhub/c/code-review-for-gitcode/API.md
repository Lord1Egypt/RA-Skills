# GitCode PR 评论 API 文档

当需要向 PR 添加评论时，参考此文档。

## 提交 PR 评论

### API 端点

```
POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments
```

### 请求参数

#### Path Parameters

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| owner | string | 是 | 仓库所属空间地址（组织或个人） |
| repo | string | 是 | 仓库路径 |
| number | integer | 是 | PR 序号 |

#### Query Parameters

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| access_token | string | 是 | 用户授权码（GitCode Token） |

#### Request Body (application/json)

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| body | string | 是 | 评论内容 |
| path | string | 否 | 文件的相对路径（行级评论必需） |
| position | integer | 否 | 代码所在行数（行级评论必需） |

### 请求示例

```bash
curl -X POST \
  "https://api.gitcode.com/api/v5/repos/Ascend/msinsight/pulls/275/comments?access_token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "【review】可维护性问题。代码中存在硬编码值。建议提取为常量。",
    "path": "src/components/Table.tsx",
    "position": 42
  }'
```

### Python 示例

```python
import urllib.request
import json

def post_pr_comment(owner, repo, pr_number, token, body, path=None, position=None):
    url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    
    data = {
        "access_token": token,
        "body": body
    }
    
    if path:
        data["path"] = path
    if position:
        data["position"] = position
    
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

# 使用示例
result = post_pr_comment(
    owner="Ascend",
    repo="msinsight",
    pr_number=275,
    token="your_token_here",
    body="【review】可维护性问题。代码中存在硬编码值。",
    path="src/components/Table.tsx",
    position=42
)
print(f"Comment posted: {result['id']}")
```

### 响应示例 (200 OK)

```json
{
  "id": "28ede3cc57e10bddef15971f0c55bc6c12998bd7",
  "body": "【review】可维护性问题...",
  "path": "src/components/Table.tsx",
  "position": 42,
  "user": {
    "login": "username",
    "id": 12345
  },
  "created_at": "2026-03-10T12:00:00Z"
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权（Token 无效） |
| 404 | PR 不存在 |
| 422 | 验证失败（如行号超出范围） |

### 注意事项

1. **Token 权限**: 需要 `repo` 或 `public_repo` 权限
2. **行号**: `position` 是 diff 中的行号，不是文件绝对行号
3. **路径**: `path` 必须是 PR 中变更的文件路径
4. **评论类型**:
   - 提供 `path` 和 `position`: 行级评论（代码审查）
   - 不提供: PR 级评论（普通评论）

### 获取 PR Diff 行号

如需确定正确的 `position`，先获取 PR diff:

```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/diff"
```

Diff 中的 `@@` 标记包含行号信息。
