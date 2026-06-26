# 钉钉应用权限开通清单

## 📋 应用信息

- **AppKey**: 配置为环境变量 `DINGTALK_APP_KEY`
- **AppSecret**: 配置为环境变量 `DINGTALK_APP_SECRET`（⚠️ 绝不要明文写在代码或文档中）
- **应用类型**: 企业内部应用

> ⚠️ **安全提示**：AppKey 和 AppSecret 是敏感凭据，请通过环境变量或安全配置文件传入，切勿硬编码。本文件中的申请链接使用 `YOUR_APP_KEY` 占位符，请替换为你自己的 AppKey。

---

## ✅ 已开通权限（6个）

| 权限 | 用途 |
|------|------|
| 钉盘应用盘空间读 | 列出和查看空间信息 |
| 钉盘应用盘空间写 | 创建新空间 |
| 钉盘应用文件读 | 列出和查询文件 |
| 钉盘应用文件写 | 上传文件、写入文档 |
| 钉盘上传信息读 | 获取上传凭证 |
| 钉盘下载信息读 | 获取文件下载信息 |

---

## ❌ 待开通权限（4个）

### 🔴 高优先级（必须开通）

| # | 权限名称 | 权限标识 | 用途 | 一键申请链接 |
|---|---------|---------|------|-------------|
| 1 | 企业存储文件下载信息读 | 企业存储文件下载信息读权限 | 下载文件到本地（配合已开通的"钉盘下载信息读"使用） | [点击申请](https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23%E4%BC%81%E4%B8%9A%E5%AD%98%E5%82%A8%E6%96%87%E4%BB%B6%E4%B8%8B%E8%BD%BD%E4%BF%A1%E6%81%AF%E8%AF%BB%E6%9D%83%E9%99%90) |

### 🟡 中优先级（建议开通）

| # | 权限名称 | 权限标识 | 用途 | 一键申请链接 |
|---|---------|---------|------|-------------|
| 2 | 通讯录用户详情读 | qyapi_get_member | 获取用户手机号、邮箱等详细信息 | [点击申请](https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23qyapi_get_member) |
| 3 | 通讯录部门列表读 | qyapi_get_department_list | 获取组织架构部门列表 | [点击申请](https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23qyapi_get_department_list) |

### ⚪ 低优先级（可选）

| # | 权限名称 | 权限标识 | 用途 | 一键申请链接 |
|---|---------|---------|------|-------------|
| 4 | 企业钉盘基础权限 | qyapi_cspace_base | 旧版自定义空间API（新版API已覆盖大部分功能） | [点击申请](https://open-dev.dingtalk.com/appscope/apply?content=YOUR_APP_KEY%23qyapi_cspace_base) |

---

## 📝 开通步骤

### 方式一：一键申请（推荐）

1. 将链接中的 `YOUR_APP_KEY` 替换为你的实际 AppKey
2. 点击链接跳转到钉钉开放平台申请页面
3. 提交申请后等待管理员审批

### 方式二：手动搜索

1. 登录 [钉钉开放平台](https://open-dev.dingtalk.com/)
2. 进入 **应用开发** → 找到你的应用
3. 点击 **权限管理**
4. 在搜索框搜索权限名称（如"企业存储文件下载"）
5. 点击申请 → 管理员审批

---

## ⏱️ 生效时间

- 权限审批通过后 **5-10分钟** 内生效
- 如果测试仍提示权限不足，等待几分钟后重试

---

## 🧪 验证方法

权限开通后，可以运行以下测试验证：

```bash
# 获取token（使用你的环境变量）
APP_KEY="${DINGTALK_APP_KEY}"
APP_SECRET="${DINGTALK_APP_SECRET}"

TOKEN=$(curl -s -X POST 'https://api.dingtalk.com/v1.0/oauth2/accessToken' \
  -H 'Content-Type: application/json' \
  -d "{\"appKey\":\"$APP_KEY\",\"appSecret\":\"$APP_SECRET\"}" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['accessToken'])")

# 测试下载权限
curl -X POST "https://api.dingtalk.com/v1.0/storage/spaces/{spaceId}/dentries/{dentryId}/downloadInfos/query?unionId={unionId}" \
  -H "x-acs-dingtalk-access-token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"option": {"version": 1}}'
```

返回下载URL表示权限开通成功。

---

## 📞 联系信息

如有疑问，请联系应用开发者或参考：
- 钉钉开放平台文档：https://open.dingtalk.com/document/
- 钉盘API文档：https://open.dingtalk.com/document/development/knowledge-base-download-file

---

*最后更新：2026-04-12*