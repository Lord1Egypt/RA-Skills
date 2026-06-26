# GetCompareCommits

## 原始 Swagger
https://api.cnb.cool/#/operations/GetCompareCommits

## 接口描述
比较两个提交、分支或标签之间差异的接口。Compare two commits, branches, or tags.
## 接口权限
repo-code:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/git/compare/{base_head}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | 不带.git后缀的仓库名称。格式：`组织名称/仓库名称`|
| base_head | 字符串 | 是 | 用于Git比较操作的基准和头部分支或提交的SHA值。格式：`base...head`|
## 响应信息


**响应类型：** api.CompareResponse

**响应结构：**
```json
{
  "base_commit": {
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的作者信息。
    "commit": {
      "author": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的作者签名信息。
      "comment_count": 0, // 提交的评论数量。
      "committer": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的提交者签名信息。
      "message": "string", // 提交的消息内容。
      "tree": {
        "sha": "string" // 树对象的哈希值。
      }, // 提交对应的树对象信息。
      "verification": {
        "payload": "string", // 验证负载数据。
        "reason": "string", // 验证结果的原因。
        "signature": "string", // 签名信息。
        "verified": false, // 提交是否已验证。
        "verified_at": "string" // 验证时间。
      } // 提交的验证信息。
    }, // 提交的详细信息。
    "committer": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的提交者信息。
    "parents": [{
      "sha": "string" // 父提交的哈希值。
    }], // 父提交列表。
    "sha": "string" // 提交的哈希值。
  }, // 基准对比提交。
  "commits": [{
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的作者信息。
    "commit": {
      "author": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的作者签名信息。
      "comment_count": 0, // 提交的评论数量。
      "committer": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的提交者签名信息。
      "message": "string", // 提交的消息内容。
      "tree": {
        "sha": "string" // 树对象的哈希值。
      }, // 提交对应的树对象信息。
      "verification": {
        "payload": "string", // 验证负载数据。
        "reason": "string", // 验证结果的原因。
        "signature": "string", // 签名信息。
        "verified": false, // 提交是否已验证。
        "verified_at": "string" // 验证时间。
      } // 提交的验证信息。
    }, // 提交的详细信息。
    "committer": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的提交者信息。
    "parents": [{
      "sha": "string" // 父提交的哈希值。
    }], // 父提交列表。
    "sha": "string" // 提交的哈希值。
  }], // 提交列表。
  "files": [{
    "additions": 0, // 新增行数。
    "deletions": 0, // 删除行数。
    "mode": "string", // 文件权限模式。
    "name": "string", // 文件名。
    "patch": "string", // Git差异补丁内容。
    "path": "string", // 文件路径。
    "previous_filename": "string", // 重命名前的原文件名。
    "previous_mode": "string", // 重命名前的文件权限模式。
    "status": "string" // 文件变更状态。枚举值：`added`,`modified`,`deleted`,`renamed`,`copied`
  }], // 文件差异列表。
  "head_commit": {
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的作者信息。
    "commit": {
      "author": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的作者签名信息。
      "comment_count": 0, // 提交的评论数量。
      "committer": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的提交者签名信息。
      "message": "string", // 提交的消息内容。
      "tree": {
        "sha": "string" // 树对象的哈希值。
      }, // 提交对应的树对象信息。
      "verification": {
        "payload": "string", // 验证负载数据。
        "reason": "string", // 验证结果的原因。
        "signature": "string", // 签名信息。
        "verified": false, // 提交是否已验证。
        "verified_at": "string" // 验证时间。
      } // 提交的验证信息。
    }, // 提交的详细信息。
    "committer": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的提交者信息。
    "parents": [{
      "sha": "string" // 父提交的哈希值。
    }], // 父提交列表。
    "sha": "string" // 提交的哈希值。
  }, // 源分支最新提交。
  "merge_base_commit": {
    "author": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的作者信息。
    "commit": {
      "author": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的作者签名信息。
      "comment_count": 0, // 提交的评论数量。
      "committer": {
        "date": "string", // 签名时间。
        "email": "string", // 签名者邮箱。
        "name": "string" // 签名者姓名。
      }, // 提交的提交者签名信息。
      "message": "string", // 提交的消息内容。
      "tree": {
        "sha": "string" // 树对象的哈希值。
      }, // 提交对应的树对象信息。
      "verification": {
        "payload": "string", // 验证负载数据。
        "reason": "string", // 验证结果的原因。
        "signature": "string", // 签名信息。
        "verified": false, // 提交是否已验证。
        "verified_at": "string" // 验证时间。
      } // 提交的验证信息。
    }, // 提交的详细信息。
    "committer": {
      "avatar": "string", // 用户头像。
      "email": "string", // 用户邮箱。
      "freeze": false, // 是否冻结。
      "is_npc": false, // 是否是 NPC。
      "nickname": "string", // 昵称。
      "username": "string" // 用户名。
    }, // 提交的提交者信息。
    "parents": [{
      "sha": "string" // 父提交的哈希值。
    }], // 父提交列表。
    "sha": "string" // 提交的哈希值。
  }, // 共同祖先提交。
  "total_commits": 0 // 总提交数。
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/git/compare/{base_head}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
