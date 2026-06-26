# django-vue-admin 代码生成器

一键生成完整的 django-vue-admin 风格项目代码。

## 功能

用户告诉 Skill 要创建的模块，Skill 自动生成：
- Django Model
- Django Serializer
- Django ViewSet
- Django URL
- Vue 页面
- Vue API

## 自动读取模板文档

Skill 内置以下模板文档，会自动读取用于代码生成：

| 文档 | 用途 |
|------|------|
| `templates/CORE_MODULES.md` | 核心模块完整代码（用户/角色/组织/权限/字典/文件） |
| `templates/BUSINESS_LOGIC.md` | 业务逻辑参考（用户/权限/工作流） |
| `templates/LOGIC_FLOW.md` | 流程逻辑（登录/权限校验/数据权限） |
| `templates/FIELD_TEMPLATE.md` | 字段模板（常用字段组合） |

**Skill 会根据用户描述的模块，自动：**
1. 读取 FIELD_TEMPLATE.md 获取字段定义
2. 读取 BUSINESS_LOGIC.md 获取业务逻辑模式
3. 读取 LOGIC_FLOW.md 获取流程逻辑
4. 生成完整的 CRUD 代码

---

# 使用方式

## 示例对话

**用户**: 创建一个产品管理模块，包含名称、价格、库存、分类字段

**Skill**: 自动生成以下代码：

```python
# apps/product/models.py
class Product(CommonBModel):
    name = models.CharField('产品名称', max_length=200)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    stock = models.IntegerField('库存', default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='分类')
    status = models.BooleanField('状态', default=True)
    ...
```

用户直接复制到项目中即可使用。

---

# 代码生成器

## 内置模板

### 1. Model 模板

```python
from django.db import models
from utils.model import CommonBModel

class Product(CommonBModel):
    """产品"""
    name = models.CharField('产品名称', max_length=200)
    code = models.CharField('产品编码', max_length=50, unique=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    stock = models.IntegerField('库存', default=0)
    status = models.BooleanField('状态', default=True)
    description = models.TextField('描述', blank=True)
    
    # 关联字段
    category = models.ForeignKey('Category', on_delete=models.CASCADE, 
                                verbose_name='分类', related_name='products')
    
    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['-create_time']
    
    def __str__(self):
        return self.name
```

### 2. Serializer 模板

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('category', 'create_by', 'belong_dept')

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'price', 'stock', 'status', 'description']
```

### 3. ViewSet 模板

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer
from utils.permission import RbacPermission

class ProductViewSet(ModelViewSet):
    """产品管理"""
    perms_map = {
        'get': '*',
        'post': 'product_create',
        'put': 'product_update',
        'delete': 'product_delete',
    }
    permission_classes = [IsAuthenticated, RbacPermission]
    queryset = Product.objects.all()
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    filterset_fields = ['category', 'status']
    ordering = ['-create_time']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductSerializer
        return ProductCreateSerializer
    
    def get_queryset(self):
        from utils.queryset import get_data_scope
        return get_data_scope(self.request.user, super().get_queryset())
```

### 4. URL 模板

```python
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
urlpatterns = router.urls
```

### 5. Vue API 模板

```javascript
export function getProductList(params) {
  return request({ url: '/myapp/product/', method: 'get', params })
}
export function getProduct(id) {
  return request({ url: `/myapp/product/${id}/`, method: 'get' })
}
export function createProduct(data) {
  return request({ url: '/myapp/product/', method: 'post', data })
}
export function updateProduct(id, data) {
  return request({ url: `/myapp/product/${id}/`, method: 'put', data })
}
export function deleteProduct(id) {
  return request({ url: `/myapp/product/${id}/`, method: 'delete' })
}
```

### 6. Vue 页面模板

```vue
<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="名称" style="width: 200px" @keyup.enter.native="handleFilter" />
      <el-button type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleCreate" v-permission="['product_create']">新增</el-button>
    </div>

    <el-table v-loading="listLoading" :data="list" border stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="price" label="价格" width="100">
        <template slot-scope="{row}">¥{{ row.price }}</template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template slot-scope="{row}">
          <el-tag :type="row.status ? 'success' : 'danger'">{{ row.status ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template slot-scope="{row}">
          <el-button type="text" @click="handleUpdate(row)" v-permission="['product_update']">编辑</el-button>
          <el-button type="text" @click="handleDelete(row)" v-permission="['product_delete']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="600px">
      <el-form ref="dataForm" :model="temp" :rules="rules" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="temp.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="temp.stock" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="temp.status" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getProductList, createProduct, updateProduct, deleteProduct } from '@/api/myapp'

export default {
  components: { Pagination },
  data() {
    return {
      list: [], total: 0, listLoading: true,
      listQuery: { page: 1, limit: 20, name: '' },
      dialogFormVisible: false, dialogStatus: '',
      textMap: { update: '编辑', create: '新增' },
      temp: { id: undefined, name: '', price: 0, stock: 0, status: true },
      rules: { name: [{ required: true, message: '必填', trigger: 'blur' }] }
    }
  },
  created() { this.getList() },
  methods: {
    getList() {
      this.listLoading = true
      getProductList(this.listQuery).then(res => {
        this.list = res.results || res
        this.total = res.count || this.list.length
        this.listLoading = false
      })
    },
    handleFilter() { this.listQuery.page = 1; this.getList() },
    handleCreate() {
      this.temp = { id: undefined, name: '', price: 0, stock: 0, status: true }
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs.dataForm.validate(valid => {
        if (valid) {
          createProduct(this.temp).then(() => { this.dialogFormVisible = false; this.getList() })
        }
      })
    },
    updateData() {
      this.$refs.dataForm.validate(valid => {
        if (valid) {
          updateProduct(this.temp.id, this.temp).then(() => { this.dialogFormVisible = false; this.getList() })
        }
      })
    },
    handleDelete(row) {
      this.$confirm('确认删除?').then(() => { deleteProduct(row.id).then(() => this.getList()) })
    }
  }
}
</script>
```

---

# 字段类型映射

## Django → Vue

| Django 字段 | Vue 组件 |
|------------|----------|
| CharField | el-input |
| TextField | el-input (type=textarea) |
| IntegerField | el-input-number |
| DecimalField | el-input-number |
| BooleanField | el-switch |
| ForeignKey | el-select |
| DateField | el-date-picker |
| DateTimeField | el-date-picker (type=datetime) |
| ImageField | el-upload |
| FileField | el-upload |

---

# 生成流程

当用户说"创建一个产品模块"时：

1. **解析需求**
   - 模块名: Product
   - 字段: name, price, stock, status

2. **生成后端代码**
   - apps/myapp/models.py
   - apps/myapp/serializers.py
   - apps/myapp/views.py
   - apps/myapp/urls.py

3. **生成前端代码**
   - src/api/myapp.js
   - src/views/myapp/product.vue

4. **输出代码**
   - 用户直接复制使用

---

# 快速参考

## 常用字段

```python
# 基础
name = models.CharField('名称', max_length=100)
code = models.CharField('编码', max_length=50, unique=True)
description = models.TextField('描述', blank=True)
status = models.BooleanField('状态', default=True)
sort = models.IntegerField('排序', default=0)

# 数值
price = models.DecimalField('价格', max_digits=10, decimal_places=2)
quantity = models.IntegerField('数量', default=0)

# 关联
category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='分类')
user = models.ForeignKey('system.User', on_delete=models.SET_NULL, null=True, verbose_name='用户')

# 文件
image = models.ImageField('图片', upload_to='images/', null=True, blank=True)
file = models.FileField('附件', upload_to='files/', null=True, blank=True)

# 时间
start_date = models.DateField('开始日期', null=True, blank=True)
expire_time = models.DateTimeField('过期时间', null=True, blank=True)
```

## 项目启动

```bash
# 克隆
git clone https://github.com/caoqianming/django-vue-admin.git myproject
cd myproject/server

# 环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置
cp server/conf_e.py server/conf.py

# 数据库
python manage.py migrate
python manage.py loaddata db.json

# 运行
python manage.py runserver 0.0.0.0:8000

# 前端
cd ../client
npm install
npm run dev
```
