# API命名规范

本规范定义了API接口、参数、字段等的命名规则，确保API的一致性和可读性。

## URL路径命名

### 基本规则

- 使用小写字母
- 使用连字符（-）分隔单词
- 使用复数形式表示资源集合
- 使用名词而非动词

### 示例

```
✅ 正确：
GET /api/users
GET /api/user-orders
POST /api/products

❌ 错误：
GET /api/getUsers
GET /api/userOrders
POST /api/createProduct
```

### RESTful风格

- `GET /api/users` - 获取用户列表
- `GET /api/users/{id}` - 获取单个用户
- `POST /api/users` - 创建用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

## 参数命名

### 查询参数

- 使用小写字母
- 使用下划线（_）分隔单词
- 使用驼峰命名法（camelCase）作为备选方案

```
✅ 正确：
GET /api/users?page_num=1&page_size=10
GET /api/users?userName=test

❌ 错误：
GET /api/users?PageNum=1&PageSize=10
GET /api/users?user_name=test
```

### 路径参数

- 使用小写字母
- 使用下划线（_）分隔单词

```
✅ 正确：
GET /api/users/{user_id}
GET /api/orders/{order_id}

❌ 错误：
GET /api/users/{userId}
GET /api/orders/{orderId}
```

## 请求体参数命名

- 使用驼峰命名法（camelCase）
- 布尔类型使用 `is` 或 `has` 前缀

```json
{
  "userName": "test",
  "userAge": 25,
  "isActive": true,
  "hasPermission": false
}
```

## 响应字段命名

- 使用驼峰命名法（camelCase）
- 布尔类型使用 `is` 或 `has` 前缀

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "userId": 123,
    "userName": "test",
    "isActive": true,
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

## 常见字段命名

| 用途           | 命名示例                     |
| -------------- | ---------------------------- |
| ID             | `userId`, `orderId`, `id`    |
| 名称           | `userName`, `productName`    |
| 创建时间       | `createdAt`, `createTime`    |
| 更新时间       | `updatedAt`, `updateTime`    |
| 状态           | `status`, `isActive`         |
| 数量           | `count`, `total`, `quantity` |
| 页码           | `pageNum`, `pageNo`          |
| 每页数量       | `pageSize`, `limit`          |
| 排序字段       | `sortBy`, `orderBy`          |
| 排序方向       | `sortOrder`, `order`         |

## 版本控制

- 在URL中包含版本号
- 使用 `v1`, `v2` 等格式

```
/api/v1/users
/api/v2/users