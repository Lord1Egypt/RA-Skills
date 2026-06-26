# AtomGit API 快速参考

> **API 版本**: v5  
> **Base URL**: `https://api.atomgit.com/api/v5`

---

## 🔐 认证

```bash
# 方式 1: Authorization Header (推荐)
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.atomgit.com/api/v5/user

# 方式 2: PRIVATE-TOKEN Header
curl -H "PRIVATE-TOKEN: YOUR_TOKEN" https://api.atomgit.com/api/v5/user

# 方式 3: URL 参数
curl "https://api.atomgit.com/api/v5/user?access_token=YOUR_TOKEN"
```

---

## 📊 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | GET/PUT/DELETE 成功 |
| 201 Created | POST 成功，资源已创建 |
| 204 No Content | 成功，无返回内容 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未认证 |
| 403 Forbidden | 无权限 |
| 404 Not Found | 资源不存在 |
| 429 Too Many Requests | 超限 (50/分，5000/小时) |
| 500 Server Error | 服务器错误 |

---

## 👤 Users (用户)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/user` | GET | 当前用户信息 |
| `/user/repos` | GET | 用户仓库列表 |
| `/users/:username` | GET | 指定用户信息 |
| `/users/:username/repos` | GET | 用户公开仓库 |
| `/user/starred` | GET | Star 的仓库 |
| `/user/subscriptions` | GET | Watch 的仓库 |
| `/users/:username/events` | GET | 用户动态 |

---

## 📁 Repositories (仓库)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/repos/:owner/:repo` | GET | 仓库详情 |
| `/repos/:owner/:repo/git/trees/:ref` | GET | 文件树 |
| `/search/repositories` | GET | 搜索仓库 |

---

## 🔀 Pull Requests (合并请求)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/repos/:owner/:repo/pulls` | GET | PR 列表 |
| `/repos/:owner/:repo/pulls/:number` | GET | PR 详情 |
| `/repos/:owner/:repo/pulls/:number/files` | GET | 变更文件 |
| `/repos/:owner/:repo/pulls/:number/commits` | GET | 提交记录 |
| `/repos/:owner/:repo/pulls/:number/comments` | POST | 添加评论 |
| `/repos/:owner/:repo/pulls/:number/merge` | PUT | 合并 PR |

---

## 📝 Issues (问题)

| 端点 | 方法 | 说明 |
|------|------|------|
| `/repos/:owner/:repo/issues` | GET | Issue 列表 |
| `/repos/:owner/:repo/issues/:number` | GET | Issue 详情 |
| `/repos/:owner/:repo/issues` | POST | 创建 Issue |
| `/repos/:owner/:repo/issues/:number` | PUT | 更新 Issue |
| `/repos/:owner/:repo/issues/:number/comments` | GET/POST | 评论 |

---

## 💡 使用示例

### 获取用户信息
```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.atomgit.com/api/v5/user
```

### 获取仓库列表
```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.atomgit.com/api/v5/user/repos
```

### 获取 PR 列表
```bash
curl -H "Authorization: Bearer TOKEN" \
  "https://api.atomgit.com/api/v5/repos/owner/repo/pulls?state=open"
```

### 合并 PR
```bash
curl -X PUT -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"merge_commit_message":"Merged"}' \
  "https://api.atomgit.com/api/v5/repos/owner/repo/pulls/3/merge"
```

---

## 📚 完整文档

- **官方 API 文档**: https://docs.atomgit.com/docs/apis/
- **技能命令参考**: [commands.md](commands.md)
- **使用指南**: [README.md](README.md)

---

*最后更新：2026-03-25*
