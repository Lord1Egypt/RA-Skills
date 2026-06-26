# API设计规范参考

本文档提供RESTful API设计的标准规范，用于技术文档生成时的参考。

## 设计原则

### 1. RESTful原则
- **资源导向**：API围绕资源设计，而非操作
- **统一接口**：使用标准HTTP方法
- **无状态**：每个请求包含所有必要信息
- **可缓存**：适当使用缓存头
- **分层系统**：客户端不依赖直接连接
- **按需代码**：可选支持客户端代码扩展

### 2. 版本管理
- URL路径包含版本：`/api/v1/resource`
- 使用Accept头：`Accept: application/vnd.company.v1+json`
- **推荐**：URL路径版本控制，简单明确

### 3. 安全原则
- 所有API强制HTTPS
- 身份验证和授权分离
- 输入验证和输出过滤
- 速率限制和配额管理

## API结构规范

### 1. 资源命名
- 使用名词复数形式：`/users` 而非 `/user`
- 小写字母，单词间用连字符：`/user-roles`
- 避免动词：使用HTTP方法表示操作

### 2. HTTP方法使用
| 方法 | 用途 | 幂等性 | 安全性 |
|------|------|--------|--------|
| GET | 获取资源 | 是 | 是 |
| POST | 创建资源 | 否 | 否 |
| PUT | 全量更新资源 | 是 | 否 |
| PATCH | 部分更新资源 | 否 | 否 |
| DELETE | 删除资源 | 是 | 否 |

### 3. 端点设计示例
```
# 资源集合操作
GET    /api/v1/users          # 获取用户列表
POST   /api/v1/users          # 创建新用户

# 单个资源操作
GET    /api/v1/users/{id}     # 获取指定用户
PUT    /api/v1/users/{id}     # 全量更新用户
PATCH  /api/v1/users/{id}     # 部分更新用户
DELETE /api/v1/users/{id}     # 删除用户

# 子资源操作
GET    /api/v1/users/{id}/orders      # 获取用户的订单
POST   /api/v1/users/{id}/orders      # 为用户创建订单
GET    /api/v1/users/{id}/orders/{orderId}  # 获取用户特定订单
```

## 请求与响应规范

### 1. 请求头标准
```http
# 必需头
Content-Type: application/json
Authorization: Bearer {token}
Accept: application/json

# 推荐头
X-Request-ID: {uuid}          # 请求跟踪
X-Client-Version: 1.0.0       # 客户端版本
X-Device-Info: {device_info}  # 设备信息
```

### 2. 请求参数类型
| 参数位置 | 用途 | 示例 |
|----------|------|------|
| 路径参数 | 资源标识 | `/users/{id}` |
| 查询参数 | 筛选、排序、分页 | `?page=1&size=10` |
| 请求体 | 创建/更新数据 | JSON对象 |
| 请求头 | 元数据、认证 | `Authorization` |

### 3. 响应格式标准

#### 成功响应 (HTTP 2xx)
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 业务数据
  },
  "meta": {
    // 分页、时间戳等元数据
  }
}
```

#### 分页响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],        // 当前页数据
    "total": 100,          // 总记录数
    "page": 1,             // 当前页码
    "size": 10,            // 每页大小
    "pages": 10            // 总页数
  }
}
```

#### 错误响应 (HTTP 4xx/5xx)
```json
{
  "code": 400,
  "message": "参数验证失败",
  "errors": [
    {
      "field": "username",
      "code": "REQUIRED",
      "message": "用户名不能为空"
    },
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "邮箱格式不正确"
    }
  ],
  "request_id": "req_123456",
  "timestamp": "2026-04-21T10:00:00Z"
}
```

### 4. HTTP状态码使用
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | 成功获取或更新资源 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 成功但无返回内容 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或认证失败 |
| 403 | Forbidden | 无访问权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建） |
| 422 | Unprocessable Entity | 业务逻辑验证失败 |
| 429 | Too Many Requests | 请求过于频繁 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务暂时不可用 |

## 分页、排序和筛选

### 1. 分页参数
```http
GET /api/v1/users?page=1&size=10
```
- `page`: 页码（从1开始）
- `size`: 每页记录数（默认10，最大100）
- **注意**: 避免使用 `limit` 和 `offset`，语义不如 `page` 和 `size` 明确

### 2. 排序参数
```http
GET /api/v1/users?sort=created_at:desc,username:asc
```
格式：`字段名:方向`
- 方向：`asc`（升序）或 `desc`（降序）
- 多个排序字段用逗号分隔

### 3. 筛选参数
```http
GET /api/v1/users?status=active&role=admin&created_after=2026-01-01
```
- 使用查询参数进行筛选
- 支持范围查询：`created_after`、`created_before`
- 支持部分匹配：`name_like=john`
- 支持IN查询：`status=active,inactive`

## 业务逻辑伪代码规范

### 1. 标准结构
```python
def api_endpoint(request):
    """
    函数文档字符串：描述接口功能
    
    Args:
        request: 请求对象，包含参数、用户信息等
        
    Returns:
        响应数据或错误
        
    Raises:
        可能抛出的异常
    """
    
    # 1. 参数验证
    validate_request(request)
    
    # 2. 权限检查
    check_permission(request.user)
    
    # 3. 业务逻辑处理
    result = process_business_logic(request)
    
    # 4. 数据持久化
    save_to_database(result)
    
    # 5. 返回响应
    return format_response(result)
```

### 2. CRUD操作模板

#### 创建资源
```python
def create_resource(request):
    # 1. 解析请求数据
    data = parse_request_body(request)
    
    # 2. 验证数据完整性
    errors = validate_create_data(data)
    if errors:
        return validation_error_response(errors)
    
    # 3. 检查唯一性约束
    if resource_exists(data['unique_field']):
        return conflict_error('资源已存在')
    
    # 4. 业务逻辑处理
    processed_data = apply_business_rules(data)
    
    # 5. 创建资源
    resource = Resource.create(**processed_data)
    
    # 6. 触发后续操作（异步）
    trigger_async_tasks(resource)
    
    # 7. 返回创建结果
    return created_response(resource.to_dict())
```

#### 获取资源列表
```python
def list_resources(request):
    # 1. 解析查询参数
    page = request.query.get('page', 1)
    size = request.query.get('size', 10)
    filters = extract_filters(request.query)
    
    # 2. 构建查询
    query = Resource.query.filter_by(is_deleted=False)
    
    # 3. 应用筛选条件
    if filters:
        query = apply_filters(query, filters)
    
    # 4. 应用排序
    sort_fields = parse_sort_fields(request.query.get('sort'))
    if sort_fields:
        query = apply_sorting(query, sort_fields)
    
    # 5. 执行分页查询
    total = query.count()
    items = query.paginate(page, size).all()
    
    # 6. 格式化数据
    formatted_items = [item.to_summary_dict() for item in items]
    
    # 7. 返回分页结果
    return paginated_response(formatted_items, total, page, size)
```

#### 更新资源
```python
def update_resource(request, resource_id):
    # 1. 查找资源
    resource = Resource.find_or_404(resource_id)
    
    # 2. 权限验证（资源级权限）
    if not can_edit_resource(request.user, resource):
        return forbidden_error('无权修改此资源')
    
    # 3. 解析更新数据
    update_data = parse_request_body(request)
    
    # 4. 验证更新数据
    errors = validate_update_data(update_data, resource)
    if errors:
        return validation_error_response(errors)
    
    # 5. 应用更新
    before_update = resource.to_dict()
    resource.update(**update_data)
    after_update = resource.to_dict()
    
    # 6. 记录变更日志
    log_change(request.user, 'update', before_update, after_update)
    
    # 7. 返回更新结果
    return success_response(resource.to_dict())
```

#### 删除资源
```python
def delete_resource(request, resource_id):
    # 1. 查找资源
    resource = Resource.find_or_404(resource_id)
    
    # 2. 权限验证（删除权限）
    if not can_delete_resource(request.user, resource):
        return forbidden_error('无权删除此资源')
    
    # 3. 检查关联约束
    if has_dependent_resources(resource):
        return conflict_error('存在关联资源，无法删除')
    
    # 4. 执行软删除（或物理删除）
    resource.mark_as_deleted()
    # 或: resource.delete()
    
    # 5. 清理关联数据
    cleanup_related_data(resource)
    
    # 6. 返回成功响应（无内容）
    return no_content_response()
```

### 3. 复杂业务逻辑示例

#### 订单创建流程
```python
def create_order(request):
    """
    创建订单的完整流程
    
    业务规则：
    1. 验证用户账户状态
    2. 检查商品库存
    3. 计算价格和优惠
    4. 扣减库存
    5. 创建订单记录
    6. 扣款或生成待支付订单
    7. 发送订单确认通知
    """
    
    # 1. 验证用户和权限
    user = get_current_user(request)
    if not user.is_active:
        return bad_request('用户账户已冻结')
    
    # 2. 解析订单数据
    order_data = request.json
    items = order_data['items']
    
    # 3. 检查商品库存（事务性）
    with transaction.atomic():
        # 锁定库存记录
        product_stocks = ProductStock.select_for_update().filter(
            product_id__in=[item['product_id'] for item in items]
        )
        
        # 验证库存充足
        for item in items:
            stock = next(s for s in product_stocks if s.product_id == item['product_id'])
            if stock.quantity < item['quantity']:
                return insufficient_stock_error(stock.product.name)
        
        # 4. 计算订单金额
        order_amount = calculate_order_amount(items, user)
        
        # 5. 扣减库存
        for item in items:
            stock = next(s for s in product_stocks if s.product_id == item['product_id'])
            stock.quantity -= item['quantity']
            stock.save()
        
        # 6. 创建订单
        order = Order.create(
            user_id=user.id,
            amount=order_amount,
            status='pending_payment',
            items=items
        )
        
        # 7. 记录库存变更日志
        log_inventory_changes(order, product_stocks)
    
    # 8. 异步处理后续操作
    async_tasks = [
        send_order_confirmation_email(order),
        update_user_purchase_stats(user),
        trigger_inventory_replenishment_check(product_stocks)
    ]
    execute_async_tasks(async_tasks)
    
    # 9. 返回订单信息
    return created_response(order.to_detail_dict())
```

## 数据库设计参考

### 1. 表设计规范
```sql
-- 基础表结构模板
CREATE TABLE table_name (
    id VARCHAR(36) PRIMARY KEY DEFAULT UUID(),  -- 主键使用UUID
    -- 业务字段
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    -- 元数据字段
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(36) NOT NULL,
    updated_by VARCHAR(36),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP,
    deleted_by VARCHAR(36),
    -- 约束
    UNIQUE KEY uk_name (name),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2. 关联关系设计
```sql
-- 一对一关系
ALTER TABLE profile 
    ADD CONSTRAINT fk_profile_user 
    FOREIGN KEY (user_id) REFERENCES users(id) 
    ON DELETE CASCADE;

-- 一对多关系  
ALTER TABLE orders
    ADD CONSTRAINT fk_order_user
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT;

-- 多对多关系（中间表）
CREATE TABLE user_roles (
    id VARCHAR(36) PRIMARY KEY DEFAULT UUID(),
    user_id VARCHAR(36) NOT NULL,
    role_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_role (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
```

## 错误处理规范

### 1. 错误代码定义
```json
{
  "code": "VALIDATION_ERROR",
  "message": "参数验证失败",
  "details": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "邮箱格式不正确"
    }
  ]
}
```

### 2. 常见错误代码
| 错误代码 | HTTP状态码 | 含义 |
|----------|------------|------|
| `VALIDATION_ERROR` | 400 | 参数验证失败 |
| `AUTHENTICATION_FAILED` | 401 | 认证失败 |
| `PERMISSION_DENIED` | 403 | 权限不足 |
| `RESOURCE_NOT_FOUND` | 404 | 资源不存在 |
| `RESOURCE_CONFLICT` | 409 | 资源冲突 |
| `RATE_LIMIT_EXCEEDED` | 429 | 请求频率超限 |
| `INTERNAL_ERROR` | 500 | 服务器内部错误 |
| `SERVICE_UNAVAILABLE` | 503 | 服务不可用 |

## 性能优化建议

### 1. 数据库优化
- 合理使用索引（查询字段、排序字段）
- 避免N+1查询问题（使用JOIN或批量查询）
- 分页查询使用游标分页（Cursor-based Pagination）替代偏移分页

### 2. 缓存策略
```python
# Redis缓存示例
CACHE_KEYS = {
    'user': 'user:{id}',
    'user_products': 'user:{id}:products',
    'product_detail': 'product:{id}:detail'
}

# 缓存读取策略
def get_user_with_cache(user_id):
    cache_key = CACHE_KEYS['user'].format(id=user_id)
    cached_data = redis.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    # 缓存未命中，查询数据库
    user = User.get(user_id)
    if user:
        # 设置缓存，过期时间30分钟
        redis.setex(cache_key, 1800, json.dumps(user.to_dict()))
    
    return user
```

### 3. 异步处理
- 耗时操作异步执行（邮件发送、文件处理等）
- 使用消息队列解耦服务
- 实现重试和死信队列机制

## 文档要求

在技术文档中描述API时，应为每个接口提供：

1. **接口基本信息**：URL、方法、功能描述
2. **请求参数**：路径参数、查询参数、请求体
3. **响应格式**：成功响应、错误响应
4. **业务逻辑**：详细处理步骤（伪代码）
5. **权限要求**：需要的角色和权限
6. **性能考虑**：缓存、索引、异步处理建议
7. **错误处理**：可能出现的错误和应对措施

确保描述准确完整，便于大模型理解和实现。