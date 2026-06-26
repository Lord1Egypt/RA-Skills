# 错误处理

## 常见错误及解决方案

### 401 Unauthorized

**原因**：Token 无效或过期。

**解决**：
1. 检查环境变量：`echo $TEAMBITION_USER_TOKEN`
2. 检查 `user-token.json` 是否存在且格式正确：`{"userToken": "your_token"}`
3. 重新获取 Token

---

### 403 Forbidden

**原因**：Token 有效但无权限访问该资源。

**解决**：
- 确认 Token 对应的用户有权限访问该项目/任务
- 确认任务/项目 ID 正确

---

### 404 Not Found

**原因**：资源不存在或 ID 错误。

**解决**：
- 检查任务/项目 ID 是否正确（24 位 hex 字符串）
- 确认资源未被删除或归档

---

### 成员搜索返回多个结果

**现象**：`call_api.search_member('张三')` 打印候选列表并退出。

**解决**：使用更精确的关键词，如工号、邮箱前缀：
```bash
uv run scripts/query_members.py --keyword 'zhangsan@company.com'
```

---

### 日期格式错误

**现象**：API 返回日期相关错误。

**解决**：
- `create_task.py` 和 `update_task.py` 已内置时区转换，直接传东八区时间即可
- 格式：`2026-04-01` 或 `2026-04-01T23:59:59`
- 不要手动传 UTC 时间（会被再次转换导致偏差）

---

### TQL 语法错误

**现象**：查询返回空结果或 API 报错。

**解决**：
- 字符串值必须用单引号：`projectId = 'xxx'`（不是双引号）
- 时间函数：`startOf(d)`、`endOf(w)` 等（参考 `references/tql.md`）
- 不要猜测 TQL 语法，严格参考 `references/tql.md`

---

### 自定义字段更新失败

**现象**：更新自定义字段时 API 报错。

**解决**：
- 更新时使用 `customfieldId`，不是 `cfId`（查询返回的是 `cfId`）
- 不需要 `type` 字段
- `value` 数组中的对象必须包含 `id` 字段（即使为空字符串 `""`）

---

### 脚本找不到 Token

**现象**：`❌ 无法获取 User Token`

**解决**：
```bash
# 方式 1：环境变量
export TEAMBITION_USER_TOKEN="your_token_here"

# 方式 2：配置文件（在 teambition/ 目录下创建）
echo '{"userToken": "your_token_here"}' > user-token.json
```
