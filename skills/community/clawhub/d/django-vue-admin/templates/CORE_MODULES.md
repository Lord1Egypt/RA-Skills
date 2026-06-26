# django-vue-admin 核心模块完整代码

基于 django-vue-admin 项目的完整实现，包含所有业务逻辑。

---

## 一、Model 定义

### 1.1 系统模型完整代码

```python
# apps/system/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.model import SoftModel
from simple_history.models import HistoricalRecords


class Position(SoftModel):
    """岗位"""
    name = models.CharField('名称', max_length=32, unique=True)
    description = models.CharField('描述', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = '职位/岗位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Permission(SoftModel):
    """功能权限:目录,菜单,接口"""
    menu_type_choices = (
        ('目录', '目录'),
        ('菜单', '菜单'),
        ('接口', '接口')
    )
    name = models.CharField('名称', max_length=30)
    type = models.CharField('类型', max_length=20, choices=menu_type_choices, default='接口')
    is_frame = models.BooleanField('外部链接', default=False)
    sort = models.IntegerField('排序标记', default=1)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父')
    method = models.CharField('方法/代号', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = '功能权限表'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name


class Organization(SoftModel):
    """组织架构"""
    organization_type_choices = (
        ('公司', '公司'),
        ('部门', '部门')
    )
    name = models.CharField('名称', max_length=60)
    type = models.CharField('类型', max_length=20, choices=organization_type_choices, default='部门')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父')

    class Meta:
        verbose_name = '组织架构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(SoftModel):
    """角色"""
    data_type_choices = (
        ('全部', '全部'),
        ('自定义', '自定义'),
        ('同级及以下', '同级及以下'),
        ('本级及以下', '本级及以下'),
        ('本级', '本级'),
        ('仅本人', '仅本人')
    )
    name = models.CharField('角色', max_length=32, unique=True)
    perms = models.ManyToManyField(Permission, blank=True, verbose_name='功能权限')
    datas = models.CharField('数据权限', max_length=50, choices=data_type_choices, default='本级及以下')
    depts = models.ManyToManyField(Organization, blank=True, verbose_name='权限范围', related_name='roles')
    description = models.CharField('描述', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class User(AbstractUser):
    """用户"""
    name = models.CharField('姓名', max_length=20, null=True, blank=True)
    phone = models.CharField('手机号', max_length=11, null=True, blank=True, unique=True)
    avatar = models.CharField('头像', max_length=100, default='/media/default/avatar.png', null=True, blank=True)
    dept = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='组织')
    position = models.ManyToManyField(Position, blank=True, verbose_name='岗位')
    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级主管')
    roles = models.ManyToManyField(Role, blank=True, verbose_name='角色')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username


class DictType(SoftModel):
    """数据字典类型"""
    name = models.CharField('名称', max_length=30)
    code = models.CharField('代号', max_length=30, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父')

    class Meta:
        verbose_name = '字典类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Dict(SoftModel):
    """数据字典"""
    name = models.CharField('名称', max_length=60)
    code = models.CharField('编号', max_length=30, null=True, blank=True)
    description = models.TextField('描述', blank=True, null=True)
    type = models.ForeignKey(DictType, on_delete=models.CASCADE, verbose_name='类型')
    sort = models.IntegerField('排序', default=1)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父')
    is_used = models.BooleanField('是否有效', default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = '字典'
        verbose_name_plural = verbose_name
        unique_together = ('name', 'is_used', 'type')

    def __str__(self):
        return self.name


class CommonAModel(SoftModel):
    """业务用基本表A - 包含创建人/更新人"""
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='创建人', related_name='%(class)s_create_by')
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='最后编辑人', related_name='%(class)s_update_by')

    class Meta:
        abstract = True


class CommonBModel(SoftModel):
    """业务用基本表B - 包含创建人/更新人/所属部门"""
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='创建人', related_name='%(class)s_create_by')
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 verbose_name='最后编辑人', related_name='%(class)s_update_by')
    belong_dept = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, 
                                   verbose_name='所属部门', related_name='%(class)s_belong_dept')

    class Meta:
        abstract = True


class File(CommonAModel):
    """文件存储表"""
    name = models.CharField('名称', max_length=100, null=True, blank=True)
    size = models.IntegerField('文件大小', default=1, null=True, blank=True)
    file = models.FileField('文件', upload_to='%Y/%m/%d/')
    type_choices = (
        ('文档', '文档'),
        ('视频', '视频'),
        ('音频', '音频'),
        ('图片', '图片'),
        ('其它', '其它')
    )
    mime = models.CharField('文件格式', max_length=120, null=True, blank=True)
    type = models.CharField('文件类型', max_length=50, choices=type_choices, default='文档')
    path = models.CharField('地址', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = '文件库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
```

---

## 二、权限校验类

### 2.1 功能权限校验

```python
# apps/system/permission.py
from django.core.cache import cache
from rest_framework.permissions import BasePermission
from utils.queryset import get_child_queryset2
from .models import Organization, Permission
from django.db.models import Q


def get_permission_list(user):
    """获取权限列表,可用redis存取"""
    if user.is_superuser:
        perms_list = ['admin']
    else:
        perms = Permission.objects.none()
        roles = user.roles.all()
        if roles:
            for i in roles:
                perms = perms | i.perms.all()
        perms_list = perms.values_list('method', flat=True)
        perms_list = list(set(perms_list))
    cache.set(user.username + '__perms', perms_list, 60*60)
    return perms_list


class RbacPermission(BasePermission):
    """基于角色的权限校验类"""

    def has_permission(self, request, view):
        if not request.user:
            perms = ['visitor']
        else:
            perms = cache.get(request.user.username + '__perms')
        if not perms:
            perms = get_permission_list(request.user)
        if perms:
            if 'admin' in perms:
                return True
            elif not hasattr(view, 'perms_map'):
                return True
            else:
                perms_map = view.perms_map
                _method = request._request.method.lower()
                if perms_map:
                    for key in perms_map:
                        if key == _method or key == '*':
                            if perms_map[key] in perms or perms_map[key] == '*':
                                return True
                return False
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if hasattr(obj, 'belong_dept'):
            has_obj_perm(request.user, obj)
        return True


def has_obj_perm(user, obj):
    """数据权限控权"""
    roles = user.roles
    data_range = roles.values_list('datas', flat=True)
    if '全部' in data_range:
        return True
    elif '自定义' in data_range:
        depts = Organization.objects.filter(roles__in=roles)
        if obj.belong_dept not in depts:
            return False
    elif '同级及以下' in data_range:
        if user.dept.parent:
            belong_depts = get_child_queryset2(user.dept.parent)
            if obj.belong_dept not in belong_depts:
                return False
    elif '本级及以下' in data_range:
        belong_depts = get_child_queryset2(user.dept)
        if obj.belong_dept not in belong_depts:
            return False
    elif '本级' in data_range:
        if obj.belong_dept is not user.dept:
            return False
    return True
```

### 2.2 数据权限过滤器

```python
# apps/system/permission_data.py
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.generics import GenericAPIView
from apps.system.mixins import CreateUpdateModelBMixin
from apps.system.models import Organization
from utils.queryset import get_child_queryset2


class RbacFilterSet(CreateUpdateModelBMixin, object):
    """
    数据权限控权返回的queryset
    在必须的View下继承
    """
    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)
        
        if self.request.user.is_superuser:
            return queryset

        if hasattr(queryset.model, 'belong_dept'):
            user = self.request.user
            roles = user.roles
            data_range = roles.values_list('datas', flat=True)
            
            if '全部' in data_range:
                return queryset
            elif '自定义' in data_range:
                return queryset.filter(belong_dept__roles__in=roles)
            elif '同级及以下' in data_range:
                if user.dept.parent:
                    belong_depts = get_child_queryset2(user.dept.parent)
                    return queryset.filter(belong_dept__in=belong_depts)
            elif '本级及以下' in data_range:
                belong_depts = get_child_queryset2(user.dept)
                return queryset.filter(belong_dept__in=belong_depts)
            elif '本级' in data_range:
                return queryset.filter(belong_dept=user.dept)
            elif '仅本人' in data_range:
                return queryset.filter(Q(create_by=user) | Q(update_by=user))
        return queryset


def rbac_filter_queryset(user, queryset):
    """数据权限控权方法"""
    if user.is_superuser:
        return queryset

    roles = user.roles
    data_range = roles.values_list('datas', flat=True)
    
    if hasattr(queryset.model, 'belong_dept'):
        if '全部' in data_range:
            return queryset
        elif '自定义' in data_range:
            if roles.depts.exists():
                return queryset.filter(belong_dept__in=roles.depts)
        elif '同级及以下' in data_range:
            if user.dept.parent:
                belong_depts = get_child_queryset2(user.dept.parent)
                return queryset.filter(belong_dept__in=belong_depts)
        elif '本级及以下' in data_range:
            belong_depts = get_child_queryset2(user.dept)
            return queryset.filter(belong_dept__in=belong_depts)
        elif '本级' in data_range:
            return queryset.filter(belong_dept=user.dept)
        elif '仅本人' in data_range:
            return queryset.filter(Q(create_by=user) | Q(update_by=user))
    return queryset
```

---

## 三、认证后端

### 3.1 自定义认证 (支持用户名/手机/邮箱)

```python
# apps/system/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(
                Q(username=username) | Q(phone=username) | Q(email=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
```

---

## 四、信号处理

### 4.1 角色变更时自动更新权限缓存

```python
# apps/system/signals.py
from django.db.models.signals import m2m_changed
from .models import Role, Permission, User
from django.dispatch import receiver
from django.core.cache import cache
from .permission import get_permission_list


@receiver(m2m_changed, sender=User.roles.through)
def update_perms_cache_user(sender, instance, action, **kwargs):
    """变更用户角色时动态更新权限缓存"""
    if action in ['post_remove', 'post_add']:
        if cache.get(instance.username+'__perms', None):
            get_permission_list(instance)
```

---

## 五、ViewSet 完整实现

### 5.1 用户管理 ViewSet

```python
# apps/system/views.py - UserViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

from .models import User, Organization
from .serializers import UserListSerializer, UserCreateSerializer, UserModifySerializer
from .filters import UserFilter
from .mixins import OptimizationMixin
from .permission import RbacPermission, get_permission_list


class UserViewSet(OptimizationMixin, ModelViewSet):
    """用户管理"""
    perms_map = {
        'get': '*',
        'post': 'user_create',
        'put': 'user_update',
        'delete': 'user_delete',
    }
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filterset_class = UserFilter
    search_fields = ['username', 'name', 'phone', 'email']
    ordering_fields = ['-id']

    def perform_destroy(self, instance):
        if instance.is_superuser:
            raise ValidationError('不能删除超级用户')
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)
        # 按部门过滤
        dept = self.request.query_params.get('dept', None)
        if dept:
            from utils.queryset import get_child_queryset2
            deptqueryset = get_child_queryset2(Organization.objects.get(pk=dept))
            queryset = queryset.filter(dept__in=deptqueryset)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserModifySerializer
        elif self.action == 'list':
            return UserListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        password = request.data.get('password', '0000')
        if password:
            password = make_password(password)
        else:
            password = make_password('0000')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=password)
        return Response(serializer.data)

    @action(methods=['put'], detail=False, url_path='password')
    def password(self, request, pk=None):
        """修改密码"""
        user = request.user
        old_password = request.data.get('old_password')
        if check_password(old_password, user.password):
            new_password1 = request.data.get('new_password1')
            new_password2 = request.data.get('new_password2')
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return Response('密码修改成功!')
            else:
                return Response('新密码两次输入不一致!', status=400)
        else:
            return Response('旧密码错误!', status=400)

    @action(methods=['get'], detail=False, url_path='info')
    def info(self, request, pk=None):
        """获取当前用户信息"""
        user = request.user
        perms = get_permission_list(user)
        return Response({
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'roles': user.roles.values_list('name', flat=True),
            'avatar': user.avatar,
            'perms': perms,
        })
```

### 5.2 角色管理 ViewSet

```python
class RoleViewSet(OptimizationMixin, ModelViewSet):
    """角色管理"""
    perms_map = {
        'get': '*',
        'post': 'role_create',
        'put': 'role_update',
        'delete': 'role_delete',
    }
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name']
    ordering_fields = ['id']
```

---

## 六、Mixins

### 6.1 创建/更新自动填充

```python
# apps/system/mixins.py
from django.db.models.query import QuerySet


class CreateUpdateModelAMixin:
    """业务用基本表A用"""
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class CreateUpdateModelBMixin:
    """业务用基本表B用"""
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user, belong_dept=self.request.user.dept)
    
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class CreateUpdateCustomMixin:
    """整合版 - 自动判断"""
    def perform_create(self, serializer):
        if hasattr(self.queryset.model, 'belong_dept'):
            serializer.save(create_by=self.request.user, belong_dept=self.request.user.dept)
        else:
            serializer.save(create_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)


class OptimizationMixin:
    """性能优化 - eager loading"""
    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
```

---

## 七、工具函数

### 7.1 部门层级获取

```python
# utils/queryset.py
from django.db import models
from django.apps import apps


def get_child_queryset2(obj, hasParent=True):
    """获取所有子部门"""
    cls = type(obj)
    queryset = cls.objects.none()
    fatherQueryset = cls.objects.filter(pk=obj.id)
    if hasParent:
        queryset = queryset | fatherQueryset
    child_queryset = cls.objects.filter(parent=obj)
    while child_queryset:
        queryset = queryset | child_queryset
        child_queryset = cls.objects.filter(parent__in=child_queryset)
    return queryset


def get_parent_queryset(obj, hasSelf=True):
    """获取所有上级部门"""
    cls = type(obj)
    ids = []
    if hasSelf:
        ids.append(obj.id)
    while obj.parent:
        obj = obj.parent
        ids.append(obj.id)
    return cls.objects.filter(id__in=ids)
```

---

## 八、过滤器

### 8.1 用户过滤器

```python
# apps/system/filters.py
from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'name': ['exact', 'contains'],
            'is_active': ['exact'],
        }
```

---

## 九、初始权限数据

### 9.1 权限数据示例

```python
# 权限数据结构
permissions = [
    # 系统管理
    {'name': '系统管理', 'type': '目录', 'sort': 1},
    {'name': '用户管理', 'type': '菜单', 'parent': None, 'path': '/system/user', 'component': 'system/user'},
    {'name': '用户列表', 'type': '接口', 'method': 'user_list'},
    {'name': '用户创建', 'type': '接口', 'method': 'user_create'},
    {'name': '用户修改', 'type': '接口', 'method': 'user_update'},
    {'name': '用户删除', 'type': '接口', 'method': 'user_delete'},
    {'name': '角色管理', 'type': '菜单'},
    {'name': '组织管理', 'type': '菜单'},
    {'name': '权限管理', 'type': '菜单'},
    # 工作流
    {'name': '工作流', 'type': '目录', 'sort': 2},
    {'name': '工单管理', 'type': '菜单'},
    # 监控
    {'name': '系统监控', 'type': '目录', 'sort': 3},
]
```

---

## 十、配置

### 10.1 Django 设置

```python
# settings.py

# 认证后端
AUTHENTICATION_BACKENDS = [
    'apps.system.authentication.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 自定义用户模型
AUTH_USER_MODEL = 'system.User'
```

### 10.2 URL 配置

```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 系统
    path('api/system/', include('apps.system.urls')),
]
```

---

## 十一、API 接口汇总

| 模块 | 接口 | 权限 | 说明 |
|------|------|------|------|
| 用户 | GET /api/system/user/ | * | 用户列表 |
| | POST /api/system/user/ | user_create | 创建用户 |
| | GET /api/system/user/{id}/ | * | 用户详情 |
| | PUT /api/system/user/{id}/ | user_update | 更新用户 |
| | DELETE /api/system/user/{id}/ | user_delete | 删除用户 |
| | GET /api/system/user/info/ | - | 当前用户信息 |
| | PUT /api/system/user/password/ | - | 修改密码 |
| 角色 | GET /api/system/role/ | * | 角色列表 |
| | POST /api/system/role/ | role_create | 创建角色 |
| 组织 | GET /api/system/organization/ | * | 组织列表 |
| 权限 | GET /api/system/permission/ | * | 权限列表 |
| 登录 | POST /api/token/ | - | 获取Token |
| | POST /api/token/refresh/ | - | 刷新Token |
