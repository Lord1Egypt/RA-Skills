# Django Model 字段模板 (基于 django-vue-admin 项目分析)

## 一、通用业务字段模板

### 1.1 基础业务模型 (CommonBModel)

适用于大多数业务表，包含完整的数据权限字段：

```python
from django.db import models
from utils.model import CommonBModel

class MyModel(CommonBModel):
    """
    业务模型 - 继承 CommonBModel
    包含: create_time, update_time, is_deleted, create_by, update_by, belong_dept
    """
    # ===== 业务字段 =====
    name = models.CharField('名称', max_length=100)
    code = models.CharField('编码', max_length=50, unique=True)
    status = models.BooleanField('状态', default=True)
    sort = models.IntegerField('排序', default=0)
    description = models.TextField('描述', blank=True)
    
    # ===== 关联字段 =====
    category = models.ForeignKey('Category', on_delete=models.CASCADE, 
                                verbose_name='分类', related_name='models')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                              null=True, blank=True, verbose_name='父级')
    
    # ===== 特殊字段 =====
    # 金额/数量
    price = models.DecimalField('价格', max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField('数量', default=0)
    
    # 富文本/文件
    content = models.TextField('内容', blank=True)
    image = models.ImageField('图片', upload_to='images/', null=True, blank=True)
    file = models.FileField('附件', upload_to='files/', null=True, blank=True)
    
    # JSON 扩展
    extra = models.JSONField('扩展信息', default=dict, blank=True)
    
    class Meta:
        verbose_name = '业务名称'
        verbose_name_plural = verbose_name
        ordering = ['sort', '-create_time']
    
    def __str__(self):
        return self.name
```

### 1.2 简单业务模型 (CommonAModel)

适用于不需要部门数据权限的表：

```python
from utils.model import CommonAModel

class MyModel(CommonAModel):
    """简单业务模型 - 继承 CommonAModel"""
    name = models.CharField('名称', max_length=100)
    # 包含: create_time, update_time, is_deleted, create_by, update_by
```

---

## 二、字段类型速查表

### 2.1 常用字段

| 字段类型 | 用途 | 示例 |
|---------|------|------|
| CharField | 短文本 | `name = models.CharField('名称', max_length=100)` |
| TextField | 长文本 | `description = models.TextField('描述', blank=True)` |
| IntegerField | 整数 | `quantity = models.IntegerField('数量', default=0)` |
| DecimalField | 金额 | `price = models.DecimalField('价格', max_digits=10, decimal_places=2)` |
| BooleanField | 布尔 | `status = models.BooleanField('状态', default=True)` |
| DateField | 日期 | `start_date = models.DateField('开始日期', null=True, blank=True)` |
| DateTimeField | 日期时间 | `create_time = models.DateTimeField('创建时间', auto_now_add=True)` |
| JSONField | JSON 数据 | `extra = models.JSONField('扩展', default=dict, blank=True)` |
| ImageField | 图片 | `image = models.ImageField('图片', upload_to='images/%Y/%m/')` |
| FileField | 文件 | `file = models.FileField('附件', upload_to='files/%Y/%m/')` |

### 2.2 关系字段

| 字段类型 | 用途 | 示例 |
|---------|------|------|
| ForeignKey | 外键(一对多) | `category = models.ForeignKey('Category', on_delete=models.CASCADE)` |
| ManyToManyField | 多对多 | `roles = models.ManyToManyField('Role', blank=True)` |
| OneToOneField | 一对一 | `profile = models.OneToOneField('Profile', on_delete=models.CASCADE)` |
| ForeignKey('self') | 自关联 | `parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)` |

### 2.3 字段选项

```python
# 常用选项
name = models.CharField(
    '名称',                    # verbose_name
    max_length=100,            # 最大长度
    unique=True,               # 唯一
    null=True,                 # 数据库允许NULL
    blank=True,                # 表单允许空
    default='',                # 默认值
    choices=[('a', 'A'), ('b', 'B')],  # 选项
    verbose_name='名称',       # 中文名
    help_text='帮助文本',      # 帮助提示
)
```

---

## 三、常用业务字段组合

### 3.1 基础信息

```python
# 基础信息
name = models.CharField('名称', max_length=100)
code = models.CharField('编码', max_length=50, unique=True)
description = models.TextField('描述', blank=True)
sort = models.IntegerField('排序', default=0)
status = models.BooleanField('状态', default=True)
is_used = models.BooleanField('是否启用', default=True)
```

### 3.2 组织架构

```python
# 组织关联
dept = models.ForeignKey('Organization', on_delete=models.SET_NULL, 
                        null=True, blank=True, verbose_name='所属部门')
company = models.ForeignKey('Organization', on_delete=models.SET_NULL,
                           null=True, blank=True, verbose_name='所属公司',
                           related_name='xxx_company')
```

### 3.3 人员关联

```python
# 人员关联
create_by = models.ForeignKey('system.User', on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='创建人',
                             related_name='%(class)s_created')
update_by = models.ForeignKey('system.User', on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='更新人',
                             related_name='%(class)s_updated')
leader = models.ForeignKey('system.User', on_delete=models.SET_NULL,
                          null=True, blank=True, verbose_name='负责人')
```

### 3.4 分类/层级

```python
# 分类层级
category = models.ForeignKey('Category', on_delete=models.CASCADE,
                           verbose_name='分类', related_name='items')
parent = models.ForeignKey('self', on_delete=models.CASCADE,
                          null=True, blank=True, verbose_name='父级',
                          related_name='children')
level = models.IntegerField('层级', default=1)
path = models.CharField('路径', max_length=500, default='', blank=True)
```

### 3.5 金额/统计

```python
# 金额相关
price = models.DecimalField('价格', max_digits=10, decimal_places=2, default=0)
amount = models.DecimalField('金额', max_digits=15, decimal_places=2, default=0)
cost = models.DecimalField('成本', max_digits=10, decimal_places=2, default=0)

# 数量相关
quantity = models.IntegerField('数量', default=0)
stock = models.IntegerField('库存', default=0)
count = models.IntegerField('次数', default=0)
```

### 3.6 文件/图片

```python
# 文件
image = models.ImageField('图片', upload_to='images/%Y/%m/', null=True, blank=True)
avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
file = models.FileField('附件', upload_to='files/%Y/%m/', null=True, blank=True)
url = models.CharField('链接', max_length=500, blank=True)
```

### 3.7 时间相关

```python
# 时间
start_date = models.DateField('开始日期', null=True, blank=True)
end_date = models.DateField('结束日期', null=True, blank=True)
expire_time = models.DateTimeField('过期时间', null=True, blank=True)
```

### 3.8 审批/状态

```python
# 审批流程
workflow = models.ForeignKey('wf.Workflow', on_delete=models.CASCADE,
                            null=True, blank=True, verbose_name='工作流')
state = models.CharField('状态', max_length=20, default='draft',
                        choices=[('draft', '草稿'), ('pending', '待审批'), ('approved', '已批准'), ('rejected', '已拒绝')])
```

### 3.9 扩展字段

```python
# JSON 扩展
extra = models.JSONField('扩展信息', default=dict, blank=True)
config = models.JSONField('配置', default=dict, blank=True)
tags = models.JSONField('标签', default=list, blank=True)
```

---

## 四、完整示例

### 4.1 产品模型

```python
class Product(CommonBModel):
    """产品"""
    name = models.CharField('产品名称', max_length=200)
    code = models.CharField('产品编码', max_length=50, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                               verbose_name='产品分类', related_name='products')
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='品牌')
    price = models.DecimalField('销售价', max_digits=10, decimal_places=2)
    cost = models.DecimalField('成本价', max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField('库存', default=0)
    image = models.ImageField('产品图片', upload_to='products/', null=True, blank=True)
    description = models.TextField('产品描述', blank=True)
    specs = models.JSONField('规格参数', default=dict, blank=True)
    status = models.BooleanField('上架状态', default=True)
    sort = models.IntegerField('排序', default=0)
    
    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.name
```

### 4.2 订单模型

```python
class Order(CommonBModel):
    """订单"""
    order_no = models.CharField('订单号', max_length=50, unique=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,
                               verbose_name='客户', related_name='orders')
    total_amount = models.DecimalField('订单金额', max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField('实付金额', max_digits=12, decimal_places=2, default=0)
    status = models.CharField('订单状态', max_length=20, 
                             choices=[('pending', '待支付'), ('paid', '已支付'), 
                                     ('shipped', '已发货'), ('completed', '已完成'), 
                                     ('cancelled', '已取消')],
                             default='pending')
    pay_time = models.DateTimeField('支付时间', null=True, blank=True)
    ship_time = models.DateTimeField('发货时间', null=True, blank=True)
    remark = models.CharField('备注', max_length=500, blank=True)
    
    class Meta:
        verbose_name = '订单'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.order_no
```

---

## 五、前端字段映射

| Django 字段 | 前端组件 | 说明 |
|------------|---------|------|
| CharField(choices) | el-select | 下拉选择 |
| BooleanField | el-switch | 开关 |
| IntegerField/DecimalField | el-input-number | 数字输入 |
| TextField | el-input(type=textarea) | 文本域 |
| DateField | el-date-picker | 日期选择 |
| DateTimeField | el-date-picker(type=datetime) | 日期时间 |
| ImageField | el-upload | 图片上传 |
| FileField | el-upload | 文件上传 |
| ForeignKey | el-select + remote | 下拉选择 |
| ManyToManyField | el-select(multiple) | 多选 |
| JSONField | 自定义组件 | JSON 编辑器 |
