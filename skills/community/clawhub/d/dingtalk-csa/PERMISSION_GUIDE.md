# 钉盘助手 (dingtalk-csa) 权限开通指南

## 📖 适用对象

本文档适用于想要在企业内部部署 **钉盘助手 (dingtalk-csa)** 技能的管理员或开发者。

钉盘助手是一个通用的钉钉云存储管理技能，支持：
- 钉盘空间管理（列出、创建、查询）
- 文件操作（上传、下载、列出）
- 钉钉文档读写（adoc 格式）
- 通讯录查询（部门、用户）

---

## 🔑 必需开通的权限

在钉钉开放平台为你的应用开通以下权限后，钉盘助手才能正常工作。

### ✅ 核心权限（必须全部开通）

| # | 权限名称 | 权限标识 | 用途 | 缺少后果 |
|---|---------|---------|------|---------|
| 1 | **钉盘应用盘空间读权限** | `Storage.Space.Read` | 列出和查看钉盘空间 | ❌ 无法列出空间列表 |
| 2 | **钉盘应用盘空间写权限** | `Storage.Space.Write` | 创建新空间 | ❌ 无法创建空间 |
| 3 | **钉盘应用文件读权限** | `Storage.File.Read` | 列出和查询文件信息 | ❌ 无法查看文件列表 |
| 4 | **钉盘应用文件写权限** | `Storage.File.Write` | 上传文件、写入文档内容 | ❌ 无法上传文件或写入报告 |
| 5 | **钉盘上传信息读权限** | `Storage.UploadInfo.Read` | 获取文件上传凭证（OSS 地址） | ❌ 无法获取上传地址 |
| 6 | **钉盘下载信息读权限** | `Storage.DownloadInfo.Read` | 获取文件下载信息 | ❌ 无法下载文件 |
| 7 | **企业存储文件下载信息读权限** | （新版 API 权限） | 配合 #6 完成文件下载 | ❌ 下载链接无法获取 |

### 🟡 可选权限（按需开通）

| # | 权限名称 | 权限标识 | 用途 | 建议场景 |
|---|---------|---------|------|---------|
| 8 | **通讯录用户详情读权限** | `qyapi_get_member` | 获取用户手机号、邮箱等 | 需要查询同事联系方式 |
| 9 | **通讯录部门列表读权限** | `qyapi_get_department_list` | 获取组织架构部门列表 | 需要按部门管理文件权限 |
| 10 | **个人用户信息读权限** | `Contact.User.Read` | 新版 API 查询用户信息 | 使用新版通讯录 API |
| 11 | **企业钉盘基础权限** | `qyapi_cspace_base` | 旧版自定义空间 API | 兼容旧版系统（可选） |

---

## 📝 开通步骤

### 步骤 1：登录钉钉开放平台

访问：https://open-dev.dingtalk.com/

使用企业管理员账号登录。

### 步骤 2：进入应用管理

1. 点击顶部导航栏 **应用开发**
2. 找到你的企业内部应用（或创建一个新应用）
3. 点击进入应用详情页

### 步骤 3：申请权限

1. 在左侧菜单点击 **权限管理**
2. 在权限列表页面，使用搜索框搜索权限名称
3. 逐个搜索并申请上述 **核心权限**（#1-#7）

**搜索关键词建议：**
- 搜索 "空间读" → 找到 "钉盘应用盘空间读权限"
- 搜索 "空间写" → 找到 "钉盘应用盘空间写权限"
- 搜索 "文件读" → 找到 "钉盘应用文件读权限"
- 搜索 "文件写" → 找到 "钉盘应用文件写权限"
- 搜索 "上传" → 找到 "钉盘上传信息读权限"
- 搜索 "下载" → 找到 "钉盘下载信息读权限" 和 "企业存储文件下载信息读权限"

### 步骤 4：提交申请

1. 点击权限右侧的 **申请** 按钮
2. 填写申请理由（示例："用于企业内部文件管理和自动化报告生成"）
3. 提交申请

### 步骤 5：等待审批

- 企业内部应用的权限申请需要 **企业管理员审批**
- 审批通过后，权限通常 **5-10 分钟** 内生效

### 步骤 6：验证权限

权限生效后，可以运行以下测试命令验证：

```bash
# 替换为你的 AppKey 和 AppSecret
APP_KEY="your_app_key"
APP_SECRET="your_app_secret"

# 1. 获取 access_token
TOKEN=$(curl -s -X POST 'https://api.dingtalk.com/v1.0/oauth2/accessToken' \
  -H 'Content-Type: application/json' \
  -d "{\"appKey\":\"$APP_KEY\",\"appSecret\":\"$APP_SECRET\"}" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['accessToken'])")

echo "Token: $TOKEN"

# 2. 测试空间列表（验证 Storage.Space.Read）
echo "=== 测试空间列表 ==="
curl -s -X GET "https://api.dingtalk.com/v1.0/drive/spaces?unionId=YOUR_UNION_ID&spaceType=org&maxResults=10" \
  -H "x-acs-dingtalk-access-token: $TOKEN" | python3 -m json.tool

# 3. 测试文件列表（验证 Storage.File.Read）
echo "=== 测试文件列表 ==="
curl -s -X POST "https://api.dingtalk.com/v1.0/storage/spaces/YOUR_SPACE_ID/dentries/listAll" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"unionId": "YOUR_UNION_ID"}' | python3 -m json.tool

# 4. 测试文档写入（验证 Storage.File.Write）
echo "=== 测试文档写入 ==="
curl -s -X POST "https://api.dingtalk.com/v1.0/doc/suites/documents/YOUR_DOC_ID/overwriteContent?operatorId=YOUR_UNION_ID" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"content": "# Test", "dataType": "markdown"}' | python3 -m json.tool
```

**成功标志：**
- 空间列表：返回 JSON 包含 `spaces` 数组
- 文件列表：返回 JSON 包含 `dentries` 数组
- 文档写入：返回 `{"result": {}, "success": true}`

**失败标志：**
- 返回 `errcode: 60011` 或 `code: Forbidden.AccessDenied` → 权限未开通
- 返回 `param.error` → 参数错误，检查 spaceId/dentryId 是否正确

---

## 🔗 快速申请链接

如果你的应用已经创建，可以直接使用以下链接（替换 `YOUR_APP_KEY`）：

```
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.Space.Read
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.Space.Write
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.File.Read
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.File.Write
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.UploadInfo.Read
https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23Storage.DownloadInfo.Read
```

**注意：** "企业存储文件下载信息读权限" 需要在权限管理页面手动搜索申请，无直接链接。

---

## ⚠️ 常见问题

### Q1: 权限申请后多久生效？
**A:** 审批通过后 5-10 分钟内生效。如果长时间未生效，尝试重新获取 access_token。

### Q2: 提示 "企业认证等级过低"？
**A:** 部分高级权限需要企业完成实名认证。联系企业管理员完成认证。

### Q3: 旧版权限 `qyapi_cspace_base` 找不到？
**A:** 这是旧版权限，新版 API 已不再使用。可以忽略，不影响核心功能。

### Q4: 下载文件时提示权限不足？
**A:** 需要同时开通 `Storage.DownloadInfo.Read` 和 `企业存储文件下载信息读权限` 两个权限。

### Q5: 一个应用可以给多个企业使用吗？
**A:** 企业内部应用只能用于当前企业。如需多企业使用，需要：
- 为每个企业创建独立的应用
- 或使用第三方企业应用（需要上架）

---

## 📚 相关文档

- [钉钉开放平台 - 权限管理](https://open.dingtalk.com/document/orgapp-server/permission-management)
- [钉盘 API 文档](https://open.dingtalk.com/document/development/knowledge-base-download-file)
- [钉钉文档 API](https://open.dingtalk.com/document/development/dingtalk-document-model)
- [获取 access_token](https://open.dingtalk.com/document/orgapp-server/obtain-the-access_token-of-an-internal-app)

---

## 🆘 获取帮助

如遇问题，可以：
1. 查看钉钉开放平台官方文档
2. 在 [钉钉开发者社区](https://developers.dingtalk.com/) 提问
3. 联系技能开发者

---

*文档版本：1.0*  
*最后更新：2026-04-12*  
*适用技能：dingtalk-csa (钉盘助手)*
