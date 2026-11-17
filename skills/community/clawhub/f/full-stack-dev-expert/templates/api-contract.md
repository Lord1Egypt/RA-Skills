# API 契约（api-contract）

> 产出者：架构师（草案）→ 冻结 → 后端实现、前端对接、测试验证的唯一依据。
> 归档：`docs/api-contract.md`。遵循 `standards/api-design.md`。

- **契约版本**：v1
- **状态**：草案 / 冻结（<日期>）
- **Base URL**：`/api/v1`
- **认证**：`Authorization: Bearer <token>`（公开接口显式标注）

## 端点目录

| 方法 | 路径 | 说明 | 认证 |
|---|---|---|---|
| POST | /auth/login | 登录换 token | 公开 |

---

## <方法> <路径> —— <一句话说明>

- **用途**：
- **请求**：

```json
{ "field": "类型 — 说明 — 校验规则" }
```

- **响应 200/201**：

```json
{ "data": {} }
```

- **错误**：

| 状态码 | code | message | 场景 |
|---|---|---|---|
| 422 | FIELD_INVALID | | |

- **示例**（可复制粘贴，含认证头）：

```bash
curl -X POST "$BASE/api/v1/..." -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{}'
```

---

## 全局约定

- 错误结构、分页、排序、过滤、幂等键：见 `standards/api-design.md`，本契约只记差异。
