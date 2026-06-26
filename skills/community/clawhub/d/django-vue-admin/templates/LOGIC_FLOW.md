# django-vue-admin 深度业务逻辑分析

## 一、用户认证流程

### 1.1 登录流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         用户登录流程                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐    ┌─────────────┐    ┌──────────────────┐            │
│  │  用户输入  │───▶│ 前端验证    │───▶│ 提交 username    │            │
│  │ 用户名/密码 │    │ (表单校验)   │    │  password       │            │
│  └──────────┘    └─────────────┘    └────────┬─────────┘            │
│                                               │                      │
│                                               ▼                      │
│                                    ┌─────────────────────┐           │
│                                    │   POST /api/token/  │           │
│                                    │   用户名 + 密码     │           │
│                                    └──────────┬──────────┘           │
│                                               │                      │
│                                               ▼                      │
│                                    ┌─────────────────────┐           │
│                                    │  CustomBackend      │           │
│                                    │  authenticate()     │           │
│                                    └──────────┬──────────┘           │
│                                               │                      │
│                                               ▼                      │
│                                    ┌─────────────────────┐           │
│                                    │  查询用户 (3种方式)  │           │
│                                    │  1. username       │           │
│                                    │  2. phone          │           │
│                                    │  3. email          │           │
│                                    └──────────┬──────────┘           │
│                                               │                      │
│                    ┌──────────────────────────┼──────────────────┐   │
│                    │                          ▼                  │   │
│                    │               ┌─────────────────────┐   │   │
│                    │               │  check_password()   │   │   │
│                    │               │  密码校验           │   │   │
│                    │               └──────────┬──────────┘   │   │
│                    │                          │              │   │
│              ┌────┴────┐              ┌─────┴─────┐      │   │
│              │  失败   │              │  成功      │      │   │
│              └────┬────┘              └─────┬─────┘      │   │
│                   │                         │            │   │
│                   ▼                         ▼            │   │
│           ┌────────────┐          ┌──────────────┐     │   │
│           │ 返回错误   │          │ JWT Token    │     │   │
│           │ 401       │          │ Access +     │     │   │
│           └───────────┘          │ Refresh      │     │   │
│                                 └──────────────┘     │   │
│                                                       │   │
└───────────────────────────────────────────────────────┴───┘
```

### 1.2 认证后端代码

```python
# apps/system/authentication.py

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 支持 3 种方式登录
        user = UserModel._default_manager.get(
            Q(username=username) | Q(phone=username) | Q(email=username))
        
        # 校验密码
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
```

### 1.3 JWT Token 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/token/` | POST | 获取 Token (用户名+密码) |
| `/api/token/refresh/` | POST | 刷新 Token |
| `/api/token/black/` | GET | 退出登录 (Token 加入黑名单) |

```javascript
// 前端登录请求
POST /api/token/
{
  "username": "admin",
  "password": "admin"
}

// 响应
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 二、请求处理流程

### 2.1 完整请求流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        请求处理流程                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐                                                         │
│  │  请求入口  │  POST /api/system/user/                                │
│  └────┬─────┘                                                         │
│       │                                                                │
│       ▼                                                                │
│  ┌──────────────┐                                                      │
│  │  JWT 认证   │  解析 Header: Authorization: Bearer <token>          │
│  │  验证 Token │                                                      │
│  └──────┬───────┘                                                      │
│         │                                                              │
│    ┌────┴────┐                                                        │
│    │  Token   │                                                        │
│    │  无效    │──────────────────▶ 401 Unauthorized                    │
│    └────┬────┘                                                        │
│         │ 有效                                                         │
│         ▼                                                              │
│  ┌──────────────┐                                                      │
│  │ 获取用户信息  │  request.user = User.objects.get(id=token.user_id)  │
│  │ 加载角色权限  │                                                      │
│  └──────┬───────┘                                                      │
│         │                                                              │
│         ▼                                                              │
│  ┌──────────────┐                                                      │
│  │ RbacPermission │ 权限校验                                            │
│  │ has_permission() │                                                   │
│  └──────┬───────┘                                                      │
│         │                                                              │
│    ┌────┴────┐                                                        │
│    │  有权限   │                                                        │
│    └────┬────┘                                                        │
│         │                                                              │
│         ▼                                                              │
│  ┌──────────────┐                                                      │
│  │ ViewSet 处理 │  ModelViewSet CRUD 操作                              │
│  └──────┬───────┘                                                      │
│         │                                                              │
│         ▼                                                              │
│  ┌──────────────┐                                                      │
│  │ 数据权限过滤  │  get_queryset() → 过滤 belong_dept                  │
│  └──────┬───────┘                                                      │
│         │                                                              │
│         ▼                                                              │
│  ┌──────────────┐                                                      │
│  │ 返回响应     │  JSON 数据                                           │
│  └──────────────┘                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 三、权限校验逻辑

### 3.1 功能权限校验

```python
# utils/permission.py

class RbacPermission(BasePermission):
    def has_permission(self, request, view):
        # 1. 获取用户
        user = request.user
        if not user:
            return False
            
        # 2. 超级管理员直接放行
        if user.is_superuser:
            return True
        
        # 3. 获取缓存的权限列表
        perms = cache.get(f'{user.username}__perms')
        if not perms:
            # 从数据库加载
            perms = get_permission_list(user)
        
        # 4. admin 权限放行所有
        if 'admin' in perms:
            return True
        
        # 5. 检查 ViewSet 的 perms_map
        if not hasattr(view, 'perms_map'):
            return True  # 无权限配置，放行
        
        # 6. 获取接口需要的权限
        method = request._request.method.lower()  # get/post/put/delete
        required_perm = view.perms_map.get(method, '')
        
        # 7. * 表示所有人可访问
        if required_perm == '*':
            return True
        
        # 8. 检查用户是否有此权限
        return required_perm in perms
```

### 3.2 权限代码配置

```python
# 在 ViewSet 中配置权限映射
class UserViewSet(ModelViewSet):
    perms_map = {
        'get': '*',                  # 所有人可访问 (需登录)
        'post': 'user_create',       # 需要 user_create 权限
        'put': 'user_update',
        'delete': 'user_delete',
    }
```

### 3.3 权限获取流程

```python
def get_permission_list(user):
    """获取用户权限列表"""
    if user.is_superuser:
        return ['admin']
    
    # 从角色中聚合权限
    perms = Permission.objects.none()
    for role in user.roles.all():
        perms = perms | role.perms.all()
    
    # 提取权限代码
    perms_list = perms.values_list('method', flat=True)
    perms_list = list(set(perms_list))
    
    # 缓存 1 小时
    cache.set(f'{user.username}__perms', perms_list, 3600)
    
    return perms_list
```

---

## 四、数据权限过滤

### 4.1 数据权限过滤流程

```python
# ViewSet 中的 get_queryset()

def get_queryset(self):
    queryset = super().get_queryset()
    user = self.request.user
    
    # 超级管理员看全部
    if user.is_superuser:
        return queryset
    
    # 获取用户角色数据权限
    roles = user.roles.all()
    data_ranges = set(roles.values_list('datas', flat=True))
    
    # 全部数据
    if '全部' in data_ranges:
        return queryset
    
    # 构建过滤条件
    q = Q()
    
    if '本级及以下' in data_ranges and user.dept:
        # 获取本部门及所有子部门
        depts = get_child_queryset2(user.dept)
        q |= Q(belong_dept__in=depts)
    
    if '本级' in data_ranges and user.dept:
        q |= Q(belong_dept=user.dept)
    
    if '仅本人' in data_ranges:
        q |= Q(create_by=user)
    
    return queryset.filter(q)
```

### 4.2 部门层级获取

```python
def get_child_queryset2(obj):
    """递归获取所有子部门"""
    queryset = type(obj).objects.none()
    fatherQueryset = type(obj).objects.filter(pk=obj.id)
    
    queryset = queryset | fatherQueryset  # 包含自己
    
    # 递归获取子部门
    child_queryset = type(obj).objects.filter(parent=obj)
    while child_queryset:
        queryset = queryset | child_queryset
        child_queryset = type(obj).objects.filter(parent__in=child_queryset)
    
    return queryset
```

---

## 五、自动填充字段

### 5.1 创建/更新自动填充

```python
# 使用 Mixin 自动填充审计字段

class CreateUpdateCustomMixin:
    def perform_create(self, serializer):
        # 如果模型有 belong_dept 字段，自动填充
        if hasattr(self.queryset.model, 'belong_dept'):
            serializer.save(
                create_by=self.request.user,
                belong_dept=self.request.user.dept
            )
        else:
            serializer.save(create_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)
```

### 5.2 使用方式

```python
class ProductViewSet(CreateUpdateCustomMixin, ModelViewSet):
    # 创建时自动填充: create_by, belong_dept
    # 更新时自动填充: update_by
    pass
```

---

## 六、前端权限控制

### 6.1 用户信息获取

```javascript
// GET /api/system/user/info/
{
  "id": 1,
  "username": "admin",
  "name": "管理员",
  "roles": ["管理员"],
  "avatar": "/media/xxx.png",
  "perms": ["admin", "user_create", "user_update", ...]
}
```

### 6.2 权限指令

```javascript
// v-permission 指令
Vue.directive('permission', {
  inserted(el, binding) {
    const perms = store.getters.permissions
    const required = binding.value[0]
    
    if (!perms.includes(required)) {
      el.parentNode.removeChild(el)  // 无权限则移除元素
    }
  }
})
```

### 6.3 前端使用

```vue
<!-- 菜单 -->
<el-menu-item v-if="hasPermission('user')">用户管理</el-menu-item>

<!-- 按钮 -->
<el-button v-permission="['user_create']">新增</el-button>
<el-button v-permission="['user_update']">编辑</el-button>
<el-button v-permission="['user_delete']">删除</el-button>
```

---

## 七、完整的认证授权流程图

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          完整请求生命周期                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. 请求发起                                                               │
│     ┌─────────────────────────────────────┐                                │
│     │ GET /api/system/user/               │                                │
│     │ Authorization: Bearer eyJhbGci...    │                                │
│     └─────────────────────────────────────┘                                │
│                        │                                                    │
│                        ▼                                                    │
│  2. JWT 认证                                                              │
│     ┌─────────────────────────────────────┐                                │
│     │ TokenObtainPairView → authenticate() │                                │
│     │ • 解析 Token                                                 │
│     │ • 获取用户 ID                                                │
│     │ • 加载用户信息 → request.user                               │
│     └─────────────────────────────────────┘                                │
│                        │                                                    │
│                        ▼                                                    │
│  3. 权限校验                                                              │
│     ┌─────────────────────────────────────┐                                │
│     │ RbacPermission.has_permission()     │                                │
│     │ • 检查 is_superuser                                         │
│     │ • 检查 admin 权限                                           │
│     │ • 读取 perms_map                                            │
│     │ • 校验接口权限 (GET → user_list)                           │
│     └─────────────────────────────────────┘                                │
│                        │                                                    │
│                        ▼                                                    │
│  4. 数据过滤                                                              │
│     ┌─────────────────────────────────────┐                                │
│     │ get_queryset()                      │                                │
│     │ • 获取用户角色数据权限 (本级及以下)                         │
│     │ • 获取用户部门及子部门                                      │
│     │ • 过滤: belong_dept IN (子部门)                           │
│     └─────────────────────────────────────┘                                │
│                        │                                                    │
│                        ▼                                                    │
│  5. 业务处理                                                              │
│     ┌─────────────────────────────────────┐                                │
│     │ ModelViewSet.list()                  │                                │
│     │ • 查询数据库                                                │
│     │ • 分页                                                      │
│     │ • 序列化返回                                               │
│     └─────────────────────────────────────┘                                │
│                        │                                                    │
│                        ▼                                                    │
│  6. 响应                                                                  │
│     ┌─────────────────────────────────────┐                                │
│     │ HTTP 200 OK                         │                                │
│     │ {                                                           │
│     │   "results": [...],                                         │
│     │   "count": 100                                             │
│     │ }                                                           │
│     └─────────────────────────────────────┘                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 八、核心数据流

### 8.1 用户 → 角色 → 权限

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │     │    Role     │     │ Permission  │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id          │     │ id          │     │ id          │
│ username    │────▶│ name        │     │ name        │
│ name        │     │ perms  ◀────┼─────│ method      │ ← 接口权限码
│ phone       │     │ datas       │     │ type        │ ← 目录/菜单/接口
│ email       │     │ depts       │     │ parent      │
│ dept ───────┼────▶│             │     │             │
│ roles ◀─────┘     │             │     │             │
│             │     └─────────────┘     └─────────────┘
└─────────────┘
     │
     │
     ▼
┌─────────────┐
│Organization │
├─────────────┤
│ id          │
│ name        │ ← 部门名称
│ type        │ ← 公司/部门
│ parent      │ ← 上级部门
└─────────────┘
```

### 8.2 权限校验数据流

```
请求: GET /api/system/user/123/

1. Token 解析
   token.user_id → 1

2. 用户加载
   User.objects.get(id=1)
   → { id: 1, username: 'admin', dept_id: 5, roles: [1, 2] }

3. 角色加载
   Role.objects.filter(id__in=[1,2])
   → [
       { name: '管理员', perms: [1,2,3], datas: '全部' },
       { name: '员工', perms: [4,5], datas: '仅本人' }
     ]

4. 权限聚合
   Permission.objects.filter(id__in=[1,2,3,4,5])
   → ['admin', 'user_list', 'user_create', 'user_update', 'user_delete']

5. 数据权限
   数据范围取并集: ['全部']  → 不过滤

6. 响应
   返回用户 123 的完整数据
```

---

## 九、关键配置

### 9.1 Django REST Framework 配置

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

### 9.2 SimpleJWT 配置

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

## 十、常见场景

### 10.1 新建用户

```
1. 管理员创建用户
   POST /api/system/user/
   { username, name, password, dept, roles: [2,3] }

2. 密码加密存储
   make_password(password) → 加密后的 hash

3. 角色关联保存
   User.roles.set([2, 3])

4. 响应
   返回用户信息 (密码已加密)
```

### 10.2 用户修改密码

```
1. 用户修改密码
   PUT /api/system/user/password/
   { old_password, new_password1, new_password2 }

2. 验证旧密码
   check_password(old_password, user.password)

3. 设置新密码
   user.set_password(new_password)
   user.save()
```

### 10.3 数据权限场景

```
场景: 部门经理只能看本部门数据

1. 创建角色 "部门经理"
   - 功能权限: user_list, user_view
   - 数据权限: 本级及以下

2. 用户归属
   - 张三 (dept: 销售部)

3. 查询用户列表
   - 张三查询时
   - 获取销售部及子部门
   - SELECT * FROM user WHERE dept_id IN (5, 6, 7)
   - 只能看到本部门及下属部门的人
```
