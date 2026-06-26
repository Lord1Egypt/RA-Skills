# django-vue-admin 业务逻辑分析

## 一、模块总览

| 模块 | 说明 | 状态 |
|------|------|------|
| system | 系统管理 | ✅ 完整 |
| wf | 工作流引擎 | ✅ 完整 |
| crm | 客户管理 | ⚪ 空模块 |
| monitor | 系统监控 | ✅ 基础功能 |

---

## 二、system 模块 - 系统管理

### 2.1 功能清单

| 功能 | API 路径 | 权限代码 | 说明 |
|------|---------|---------|------|
| 用户管理 | /system/user/ | user_create/update/delete | 增删改查、密码修改、重置 |
| 角色管理 | /system/role/ | role_create/update/delete | 角色CRUD、权限分配 |
| 权限管理 | /system/perm/ | perm_create/update/delete | 目录/菜单/接口权限 |
| 组织管理 | /system/org/ | org_create/update/delete | 公司/部门架构 |
| 岗位管理 | /system/position/ | position_create/update/delete | 职位管理 |
| 字典类型 | /system/dicttype/ | dicttype_create/update/delete | 字典分类 |
| 字典管理 | /system/dict/ | dict_create/update/delete | 键值对配置 |
| 文件管理 | /system/file/ | - | 上传/下载/预览 |
| 定时任务 | /system/task/ | ptask_create/update/delete | Celery 任务管理 |
| 用户信息 | /system/user/info/ | - | 获取当前用户权限 |
| 修改密码 | /system/user/password/ | - | 修改登录密码 |

### 2.2 核心业务逻辑

#### 用户管理
```python
# 创建用户
- 默认密码: 0000
- 支持指定密码
- 支持多角色分配
- 支持部门归属

# 修改密码
- 验证旧密码
- 两次输入新密码一致
- 自动加密存储
```

#### 角色权限
```python
# 权限分配
- 功能权限: 菜单/接口级别的访问控制
- 数据权限: 全部/本级及以下/本级/仅本人

# 权限继承
- 用户 → 角色 → 权限 → 接口
```

#### 文件上传
```python
# 自动识别类型
- 图片 (image/*)
- 视频 (video/*)
- 音频 (audio/*)
- 文档 (application/*, text/*)

# 存储信息
- 文件名、大小、MIME类型
- 上传人、时间
```

#### 定时任务
```python
# 支持策略
- Interval: 间隔执行 (每N秒/分/时)
- Crontab: 定时执行 (Cron表达式)

# 任务管理
- 启用/禁用
- 立即执行
- 执行日志
```

---

## 三、wf 模块 - 工作流引擎

### 3.1 核心概念

```
Workflow (工作流定义)
    ↓
State (状态) ──── Transition (流转) ──── State (状态)
    ↓
Ticket (工单)
    ↓
TicketFlow (流转记录)
```

### 3.2 功能清单

| 功能 | API | 说明 |
|------|-----|------|
| 工作流管理 | /wf/workflow/ | 创建/配置工作流 |
| 状态管理 | /wf/state/ | 定义流程节点 |
| 流转管理 | /wf/transition/ | 定义流转规则 |
| 字段管理 | /wf/customfield/ | 自定义表单字段 |
| 工单管理 | /wf/ticket/ | 工单 CRUD |
| 流转记录 | /wf/flow/ | 查看处理历史 |
| 创建工单 | /wf/ticket/create/ | 提交流程 |
| 处理工单 | /wf/ticket/handle/ | 审批/处理 |
| 流转工单 | /wf/ticket/transition/ | 状态流转 |
| 转交 | /wf/ticket/deliver/ | 转交他人处理 |
| 加签 | /wf/ticket/add_node/ | 临时加签 |
| 退回 | /wf/ticket/retreat/ | 退回上一步 |
| 关闭 | /wf/ticket/close/ | 强制关闭 |

### 3.3 状态类型

```python
# 状态类型
type = (
    (0, '普通'),     # 普通处理节点
    (1, '开始'),     # 流程起点
    (2, '结束'),     # 流程终点
)

# 处理人类型
participant_type = (
    (0, '无处理人'),
    (1, '个人'),     # 指定用户
    (2, '多人'),     # 多人处理
    (3, '部门'),     # 部门成员
    (4, '角色'),     # 角色成员
    (5, '变量'),     # create_by (创建人)
    (6, '脚本'),     # Python 脚本
    (7, '工单字段'), # 从表单字段获取
)

# 分配方式
distribute_type = (
    (1, '主动接单'),  # 需要先接单
    (2, '直接处理'),  # 直接处理
    (3, '随机分配'),  # 随机分配
    (4, '全部处理'),  # 全部处理完才能流转
)
```

### 3.4 核心业务逻辑

#### 工单创建流程
```python
1. 获取工作流初始状态
2. 获取可用的流转规则
3. 获取自定义字段配置
4. 提交工单数据
5. 自动生成流水号 (sn)
6. 记录创建人、所属部门
```

#### 工单处理流程
```python
1. 验证处理人权限
2. 检查必填字段
3. 执行前置脚本 (Hook)
4. 记录处理意见
5. 流转到下一状态
6. 通知下一处理人
7. 更新工单状态
```

#### 特殊操作
```python
# 转交 (deliver)
- 当前处理人转交给其他人
- 保留转交记录

# 加签 (add_node)
- 临时添加处理人
- 加签完成后回到原处理人

# 退回 (retreat)
- 退回到上一步骤
- 需要填写退回原因

# 关闭 (close)
- 强制结束流程
- 仅管理员可操作
```

### 3.5 自定义字段

```python
# 支持的字段类型
field_type = (
    ('string', '字符串'),
    ('int', '整型'),
    ('float', '浮点'),
    ('boolean', '布尔'),
    ('date', '日期'),
    ('datetime', '日期时间'),
    ('radio', '单选'),
    ('checkbox', '多选'),
    ('select', '单选下拉'),
    ('selects', '多选下拉'),
    ('cascader', '级联'),
    ('textarea', '文本域'),
    ('file', '附件'),
)

# 字段属性
field_attribute = (
    (1, '只读'),
    (2, '必填'),
    (3, '可选'),
    (4, '隐藏'),
)
```

---

## 四、monitor 模块 - 系统监控

### 4.1 功能清单

| 功能 | API | 说明 |
|------|-----|------|
| 服务器信息 | /monitor/server/ | CPU/内存/磁盘 |
| 日志列表 | /monitor/log/ | 日志文件列表 |
| 日志详情 | /monitor/log/detail/ | 查看日志内容 |

### 4.2 服务器监控

```python
# CPU 信息
- 核心数 (物理/逻辑)
- 使用率

# 内存信息
- 总容量 (GB)
- 已使用 (GB)
- 使用率 (%)

# 磁盘信息
- 总容量 (GB)
- 已使用 (GB)
- 使用率 (%)
```

### 4.3 日志管理

```python
# 功能
- 列出日志文件 (按修改时间排序)
- 查看日志内容
- 文件大小显示

# 配置
LOG_PATH = 'logs/'  # 日志目录
```

---

## 五、crm 模块 - 客户管理

**状态**: 空模块，可基于此框架扩展

### 扩展建议

```python
# 可添加的模型
class Customer(CommonBModel):
    name = models.CharField('客户名称')
    industry = models.CharField('行业')
    level = models.CharField('客户等级')
    source = models.CharField('客户来源')
    ...

class Contact(CommonBModel):
    customer = models.ForeignKey(Customer)
    name = models.CharField('联系人')
    phone = models.CharField('电话')
    email = models.EmailField('邮箱')
    ...
```

---

## 六、权限体系详解

### 6.1 权限模型

```
用户 (User)
    ↓ 多个角色
角色 (Role)
    ├─ 功能权限 (perms) → Permission
    └─ 数据权限 (datas) → Organization
```

#### Permission (功能权限)
```python
class Permission(SoftModel):
    name = models.CharField('名称', max_length=30)      # "用户管理"
    type = models.CharField('类型', choices=           # 菜单/接口
        ('目录', '目录'),                               # 左侧菜单一级
        ('菜单', '菜单'),                               # 左侧菜单二级
        ('接口', '接口'))                               # API 权限
    method = models.CharField('方法/代号')              # 如: user_create
    parent = models.ForeignKey('self')                  # 父级权限
    sort = models.IntegerField('排序')                  # 菜单顺序
    is_frame = models.BooleanField('外部链接')           # 是否 iframe 加载
```

#### Role (角色)
```python
class Role(SoftModel):
    name = models.CharField('角色名')                  # "管理员"
    perms = models.ManyToManyField(Permission)        # 功能权限集合
    datas = models.CharField('数据权限', choices=      # 数据范围
        ('全部', '全部'),                               # 看所有数据
        ('自定义', '自定义'),                           # 看指定部门
        ('同级及以下', '同级及以下'),                     # 部门及同级
        ('本级及以下', '本级及以下'),                     # 本部门及子部门
        ('本级', '本级'),                               # 仅本部门
        ('仅本人', '仅本人'))                           # 仅自己创建
    depts = models.ManyToManyField(Organization)       # 自定义部门范围
```

### 6.2 功能权限 (菜单权限)

```python
# 权限类型
1. 目录 (Directory)     → 左侧菜单一级
2. 菜单 (Menu)          → 左侧菜单二级，可绑定权限
3. 接口 (Interface)     → API 权限代码

# 前端使用
v-permission="['user_create']"  # 按钮级控制
```

### 6.3 数据权限 (行级控制)

| 数据范围 | 说明 | SQL 逻辑 |
|---------|------|----------|
| 全部 | 所有数据 | 不过滤 |
| 自定义 | 指定部门 | belong_dept IN (指定部门) |
| 同级及以下 | 当前部门 + 同级部门 + 子部门 | belong_dept IN (同级及子部门) |
| 本级及以下 | 本部门 + 子部门 | belong_dept IN (子部门) |
| 本级 | 仅本部门 | belong_dept = 当前部门 |
| 仅本人 | 自己创建的数据 | create_by = 当前用户 |

### 6.4 权限校验流程

```
请求 → RbacPermission.has_permission()
    ├─ 超级管理员 → 直接放行
    ├─ 有 admin 权限 → 放行
    ├─ 无 perms_map 配置 → 放行
    └─ 校验接口权限
        └─ perms_map[method] ∈ user.perms → 放行

对象级 → has_object_permission()
    └─ 校验 belong_dept ∈ user.data_scope
```

### 6.5 完整权限架构图

```
┌─────────────────────────────────────────────────────┐
│                     用户 User                        │
│  username, name, phone, avatar, dept, roles        │
└─────────────────────┬───────────────────────────────┘
                      │ n:m
                      ▼
┌─────────────────────────────────────────────────────┐
│                     角色 Role                        │
│  name, perms(M), datas, depts(M), description     │
│                                                     │
│  数据权限:                                          │
│  ┌─────────────────────────────────────────────┐   │
│  │ 全部 | 自定义 | 同级及以下 | 本级及以下 | 本级 | 仅本人 │
│  └─────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │ n:m
                      ▼
┌─────────────────────────────────────────────────────┐
│                 权限 Permission                      │
│  name, type, method, parent, sort, is_frame       │
│                                                     │
│  类型:                                              │
│  ┌─────────┬─────────┬────────────┐               │
│  │ 目录     │ 菜单    │ 接口        │               │
│  │ (一级菜单)│ (二级菜单)│ (API权限)   │               │
│  └─────────┴─────────┴────────────┘               │
└─────────────────────────────────────────────────────┘
```

### 6.6 前端权限控制

```vue
<!-- 1. 菜单权限 (路由守卫) -->
<el-menu>
  <el-menu-item v-if="hasPermission('user')">用户管理</el-menu-item>
</el-menu>

<!-- 2. 按钮权限 (指令) -->
<el-button v-permission="['user_create']">新增</el-button>
<el-button v-permission="['user_delete']">删除</el-button>

<!-- 3. API 权限 (后端自动校验) -->
<!-- perms_map = {'post': 'user_create'} -->
```

---

## 七、API 接口规范

### 7.1 响应格式

```json
// 成功
{
  "results": [...],
  "count": 100,
  "next": "...",
  "previous": null
}

// 详情
{
  "id": 1,
  "name": "xxx",
  ...
}

// 错误
{
  "detail": "错误信息"
}
```

### 7.2 分页参数

```
GET /api/xxx/?page=1&limit=20
```

---

## 八、扩展开发指南

### 8.1 新增业务模块

```python
# 1. 创建 App
python manage.py startapp myapp apps/

# 2. 定义模型
from utils.model import CommonBModel

class MyModel(CommonBModel):
    name = models.CharField('名称')
    ...

# 3. 创建序列化器
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

# 4. 创建视图
class MyModelViewSet(ModelViewSet):
    perms_map = {'get': '*', 'post': 'my_create', ...}
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

# 5. 注册路由
router.register(r'my', MyModelViewSet)
```

### 8.2 添加定时任务

```python
# 1. 创建任务
from celery import shared_task

@shared_task
def my_task():
    print('执行任务')

# 2. 后台配置
# settings.py 添加配置

# 3. 访问管理后台创建定时任务
```
