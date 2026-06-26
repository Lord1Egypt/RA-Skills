# Smart Commit — 测试用例

> 版本: v1.0.0 | 更新: 2026-05-21

## 测试用例 1：简单 bug 修复

**输入 diff：**
```diff
--- a/src/api/user.go
+++ b/src/api/user.go
@@ -45,7 +45,7 @@ func GetUser(id int) (*User, error) {
-    result, err := db.Query("SELECT * FROM users WHERE id = ?", id)
+    result, err := db.Query("SELECT id, name, email FROM users WHERE id = ?", id)
```

**期望输出类型：** `fix`
**期望 scope：** `api` 或 `user`
**期望关键词：** SQL、查询、select、字段

**参考输出：**
```
fix(api): specify fields in user query to avoid unnecessary data fetch

Using SELECT * may cause issues when table schema changes.
Explicitly select only needed columns for stability.
```

---

## 测试用例 2：新功能

**输入描述：**
> 我刚加了一个微信登录功能，用 OAuth2.0，用户点击微信图标后跳转微信授权，回调后自动创建或关联账号。涉及文件：auth/wechat.go, routes/auth.go, middleware/session.go

**期望输出类型：** `feat`
**期望 scope：** `auth`
**期望包含：** OAuth2、微信登录、回调

**参考输出：**
```
feat(auth): add WeChat OAuth2 login support

Implement WeChat OAuth2.0 authorization flow:
- Add WeChat login button on login page
- Handle OAuth callback and auto-create/link accounts
- Update session middleware to support WeChat auth
```

---

## 测试用例 3：重构

**输入 diff 摘要：**
> 把 utils.go 里散落的 5 个日期格式化函数合并成一个 formatDate()，所有调用方已更新。功能完全不变。

**期望输出类型：** `refactor`
**期望 scope：** `utils`

**参考输出：**
```
refactor(utils): consolidate date formatting functions into formatDate()

Merge 5 scattered date formatting helpers into a single unified function.
No behavioral changes.
```

---

## 测试用例 4：BREAKING CHANGE

**输入描述：**
> 修改了 UserResponse 结构体，把 username 改成了 userName（驼峰），同时删除了废弃的 nickname 字段。所有 API 返回都变了。

**期望输出类型：** `feat` 或 `fix` + `BREAKING CHANGE`
**期望 scope：** `api`

**参考输出：**
```
feat(api): standardize UserResponse field naming to camelCase

BREAKING CHANGE: UserResponse.username renamed to userName.
UserResponse.nickname field removed (deprecated since v2.1).
Update all clients to use new field names.

Migration: rename username → userName, remove nickname usage.
```

---

## 测试用例 5：PR 描述

**输入 commits：**
- feat(search): add full-text search with Elasticsearch
- fix(search): handle empty query gracefully
- test(search): add integration tests for search API
- docs(search): add search API documentation
- chore(deps): add elasticsearch-go client

**期望输出：** 完整 PR 描述，按功能分组

**参考输出：**
```markdown
## 📌 变更摘要
集成 Elasticsearch 实现全文搜索功能，支持中文分词和模糊匹配。

## 🔧 主要变更
- **[新功能]** 实现 Elasticsearch 全文搜索 API
- **[修复]** 空查询参数的错误处理
- **[测试]** 搜索 API 集成测试
- **[文档]** 搜索 API 使用文档
- **[依赖]** 新增 elasticsearch-go 客户端

## 📁 影响范围
- `search/` — 新模块，核心搜索逻辑
- `routes/api.go` — 新增搜索路由
- `go.mod` — 新增依赖

## ⚠️ 风险评估
🟡 中 — 新模块，不影响现有功能，但需要 Elasticsearch 基础设施支持

## ✅ 测试建议
- [ ] 验证中文搜索分词效果
- [ ] 测试空查询和特殊字符
- [ ] 检查搜索响应时间（< 200ms）
- [ ] 确认 Elasticsearch 连接池配置
```

---

## 测试用例 6：Release Notes

**输入 commits（v1.2.0 到 v1.3.0）：**
- feat(auth): add WeChat OAuth2 login
- feat(dashboard): add real-time notification widget
- fix(api): handle null response from payment gateway
- fix(upload): fix file size validation for large files
- refactor(utils): consolidate date formatting
- chore(deps): upgrade to Go 1.23
- docs(readme): update installation guide

**参考输出：**
```markdown
## [1.3.0] - 2026-05-21

### ✨ 新功能
- **微信登录** — 支持 WeChat OAuth2.0 授权登录
- **实时通知** — 仪表盘新增实时通知小组件

### 🐛 修复
- 修复支付网关返回空响应时的崩溃问题
- 修复大文件上传时文件大小校验不正确的问题

### 🔧 其他改进
- 合并日期格式化工具函数，减少代码重复
- 升级 Go 版本至 1.23
- 更新安装文档
```

---

## 测试用例 7：中文项目

**输入 diff：**
```diff
--- a/src/订单服务.java
+++ b/src/订单服务.java
+    public void 取消订单(String orderId) {
+        订单 order = 订单仓库.查找(orderId);
+        if (order.是否可取消()) {
+            order.设置状态(订单状态.已取消);
+            退款服务.发起退款(order.get支付Id());
+        }
+    }
```

**期望输出：** 中文 commit message

**参考输出：**
```
feat(订单): 新增订单取消功能

支持用户取消未发货订单，自动触发退款流程。
取消前校验订单状态，仅允许取消待发货状态的订单。
```

---

## 测试用例 8：快速模式

**用户输入：** "帮我写个 commit message，刚改了登录页面的样式"

**期望输出：** 简洁的 2-3 个选项，不啰嗦

**参考输出：**
```
选择一个：

1. style(login): update login page layout and styling
2. style(ui): redesign login page visual appearance
3. feat(login): refresh login page design

建议选 1（纯样式变更用 style）
```

---

## 评分标准

| 维度 | 满分 | 标准 |
|------|------|------|
| type 准确性 | 25 | 是否正确识别变更类型 |
| scope 合理性 | 20 | 范围不过宽不过窄 |
| subject 清晰度 | 25 | 一眼看懂做了什么 |
| body 价值 | 15 | 是否解释了"为什么" |
| 风格一致性 | 15 | 中英文、格式符合规范 |
