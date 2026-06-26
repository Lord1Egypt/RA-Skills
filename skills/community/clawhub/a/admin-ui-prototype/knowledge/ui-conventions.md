# Admin-UI 页面规范

本文档提炼自 admin-ui 项目代码，定义页面原型生成的 UI 规范。

## 技术栈

- Vue 3 + TypeScript (strict mode)
- Arco Design Vue (`@arco-design/web-vue`)
- Pinia 状态管理
- LESS 预处理器
- Vite 构建

## 页面类型

### 1. 列表页（最常用）

结构：搜索栏 → 操作栏 → 数据表格 → CRUD 弹窗

```
<a-space direction="vertical" fill>
  ├── 搜索区域 (<a-form> + <a-row :gutter="16">)
  │     └── 筛选字段 (<a-col :span="6"> + <a-form-item>)
  ├── 操作栏 (<a-space> 包含搜索/重置/新增按钮)
  ├── 数据表格 (<a-table> + columns + pagination)
  └── 弹窗组件 (<a-modal> + 子组件)
</a-space>
```

### 2. 表单页

结构：分区表单 + 验证规则 + 提交/取消

```
<a-spin :loading="loading">
  <a-form :model="formData" :rules="rules" layout="vertical">
    ├── 分区标题 (<a-divider orientation="left">)
    ├── 字段行 (<a-row :gutter="16">)
    │     └── 字段列 (<a-col :span="12"> + <a-form-item>)
    └── 操作按钮 (<a-space>)
  </a-form>
</a-spin>
```

### 3. 详情页

结构：标题栏 + 描述列表 + 状态标签 + 操作按钮

```
<a-space direction="vertical" fill>
  ├── 标题栏 (<a-page-header>)
  ├── 基本信息 (<a-card> + <a-descriptions :column="2" bordered>)
  ├── 关联数据 (<a-card> + <a-table>)
  └── 操作按钮 (<a-space>)
</a-space>
```

### 4. Dashboard 页

结构：统计卡片 + 筛选器 + 图表区域

```
<div class="container">
  ├── 统计卡片 (<a-row :gutter="16"> + <a-col> + <a-statistic>)
  ├── 筛选工具栏
  └── 图表区域 (<a-row :gutter="16"> + <a-card> + Chart 组件)
</div>
```

### 5. 空状态页

结构：居中引导 + 操作入口

```
<a-card>
  <a-empty>
    ├── 描述文案
    └── 操作按钮 (<a-button type="primary">)
  </a-empty>
</a-card>
```

---

## Script 规范

### 基本结构

```typescript
<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { FormInstance, Modal, Notification, Message } from '@arco-design/web-vue';

  // 1. 类型定义
  interface ItemDTO {
    id: number;
    name: string;
    status: number;
    // ...
  }

  type FilterType = {
    name: string;
    status: string;
  };

  // 2. 响应式状态
  const filterFormRef = ref<FormInstance>();
  const data = ref<ItemDTO[]>([]);

  const req = ref({
    loading: false,
    data: {
      name: '',
      status: '',
    } as FilterType,
    pagination: {
      current: 1,
      pageSize: 10,
      total: 0,
    },
  });

  // 3. 表格列定义
  const columns = [
    { title: '名称', dataIndex: 'name', width: 150 },
    { title: '状态', slotName: 'status', width: 80 },
    { title: '操作', slotName: 'action', width: 200, fixed: 'right' as const },
  ];

  // 4. 弹窗状态
  const editModal = ref({
    visible: false,
    itemId: 0,
    isEdit: false,
  });

  // 5. 数据加载
  const getList = () => {
    req.value.loading = true;
    // API 调用...
  };

  // 6. 事件处理
  const handleSearch = () => {
    req.value.pagination.current = 1;
    getList();
  };

  const handleReset = () => {
    filterFormRef.value?.resetFields();
    req.value.pagination.current = 1;
    getList();
  };

  const setPageChange = (val: number) => {
    req.value.pagination.current = val;
    getList();
  };

  const setSizeChange = (val: number) => {
    req.value.pagination.pageSize = val;
    req.value.pagination.current = 1;
    getList();
  };

  // 7. 生命周期
  onMounted(() => {
    getList();
  });
</script>
```

### 命名约定

| 类别 | 命名 | 示例 |
|---|---|---|
| DTO 类型 | PascalCase + DTO | `SupplierDTO` |
| 筛选类型 | FilterType (type alias) | `type FilterType = { ... }` |
| 事件处理 | handle + 动词 | `handleEdit`, `handleDelete` |
| 数据加载 | get/load + 名词 | `getList`, `loadDictionary` |
| 分页处理 | setPageChange / setSizeChange | 固定命名 |
| 弹窗状态 | xxxModal | `editModal`, `secretModal` |

### 弹窗通信模式

```typescript
// 父组件
const editModal = ref({ visible: false, itemId: 0, isEdit: false });

const handleModalClose = (shouldRefresh: boolean) => {
  editModal.value.visible = false;
  editModal.value.itemId = 0;
  editModal.value.isEdit = false;
  if (shouldRefresh) getList();
};

// 子组件 Props & Emits
interface Props { itemId?: number; isEdit: boolean; }
interface Emits { (e: 'close', shouldRefresh: boolean): void; }
```

---

## Template 规范

### 搜索栏

```vue
<a-form :model="req.data" layout="vertical" ref="filterFormRef">
  <a-row :gutter="16">
    <a-col :span="6">
      <a-form-item field="name" label="名称">
        <a-input v-model="req.data.name" placeholder="请输入名称" allow-clear />
      </a-form-item>
    </a-col>
    <a-col :span="6">
      <a-form-item field="status" label="状态">
        <a-select v-model="req.data.status" placeholder="请选择状态" allow-clear :options="statusOptions" />
      </a-form-item>
    </a-col>
  </a-row>
</a-form>
```

### 操作栏

```vue
<a-space>
  <a-button type="primary" @click="handleSearch">搜索</a-button>
  <a-button @click="handleReset">重置</a-button>
  <a-divider direction="vertical" />
  <a-button type="primary" @click="handleAdd">新增</a-button>
</a-space>
```

### 数据表格

```vue
<a-table
  row-key="id"
  :columns="columns"
  :loading="req.loading"
  :data="data"
  :pagination="req.pagination"
  :scroll="{ x: 1200 }"
  @page-change="setPageChange"
  @page-size-change="setSizeChange"
>
  <template #status="{ record }">
    <a-tag :color="record.status === 1 ? 'green' : 'red'">
      {{ record.status === 1 ? '启用' : '禁用' }}
    </a-tag>
  </template>
  <template #action="{ record }">
    <a-space>
      <a-button type="primary" size="small" @click="handleEdit(record)">编辑</a-button>
      <a-button type="outline" status="danger" size="small" @click="handleDelete(record)">删除</a-button>
    </a-space>
  </template>
</a-table>
```

### 弹窗

```vue
<a-modal
  v-if="editModal.visible"
  draggable
  :align-center="false"
  :top="60"
  :mask-closable="false"
  width="700px"
  :footer="false"
  v-model:visible="editModal.visible"
  @cancel="handleModalClose(false)"
>
  <template #title>{{ editModal.isEdit ? '编辑' : '新增' }}</template>
  <EditComponent :item-id="editModal.itemId" :is-edit="editModal.isEdit" @close="handleModalClose" />
</a-modal>
```

---

## Style 规范

### 基本结构

```less
<style scoped lang="less">
  .page-container {
    padding: 16px;

    .toolbar {
      background: var(--color-bg-2);
      padding: 8px 16px 0 16px;
    }
  }
</style>
```

### 设计 Token

| Token | 用途 |
|---|---|
| `var(--color-bg-1)` | 页面背景 |
| `var(--color-bg-2)` | 卡片/工具栏背景 |
| `var(--color-text-1)` | 主要文本 |
| `var(--color-text-2)` | 次要文本 |
| `var(--color-text-3)` | 辅助文本 |
| `var(--color-border)` | 边框颜色 |
| `var(--color-border-2)` | 次要边框 |
| `var(--color-fill-2)` | 内容区背景 |

### 间距系统

基于 4px 网格：`4px`, `8px`, `12px`, `16px`, `20px`, `24px`

- 页面 padding: `16px`
- 卡片内 padding: `20px`
- 表单行 gutter: `16`
- 组件间距: `8px` ~ `16px`

### 响应式断点

- 移动端: `< 992px`（菜单折叠为抽屉）

---

## 反馈组件使用

```typescript
// 成功提示
Notification.success('操作成功');

// 错误提示
Notification.error(res.msg || '操作失败');

// 短消息
Message.success('已复制到剪贴板');
Message.error('复制失败');

// 确认对话框
Modal.confirm({
  title: '确认删除',
  content: `确定要删除"${record.name}"吗？此操作不可恢复！`,
  onOk: () => { /* 执行删除 */ },
});
```

---

## Arco Design 常用组件速查

| 组件 | 用途 | 常用 Props |
|---|---|---|
| `a-table` | 数据表格 | row-key, columns, data, pagination, loading, scroll |
| `a-form` | 表单 | model, rules, layout="vertical" |
| `a-form-item` | 表单项 | field, label, rules |
| `a-input` | 输入框 | v-model, placeholder, allow-clear |
| `a-select` | 下拉选择 | v-model, options, placeholder, allow-clear |
| `a-button` | 按钮 | type(primary/outline/text), status(danger/warning), size(small/mini) |
| `a-tag` | 标签 | color(green/red/blue/arcoblue) |
| `a-modal` | 弹窗 | v-model:visible, draggable, width, footer |
| `a-space` | 间距容器 | direction(vertical/horizontal), fill |
| `a-row/a-col` | 栅格 | gutter, span |
| `a-spin` | 加载遮罩 | loading |
| `a-switch` | 开关 | model-value, @change |
| `a-descriptions` | 描述列表 | column, bordered, size |
| `a-divider` | 分割线 | orientation("left"), direction("vertical") |
| `a-alert` | 提示信息 | type(info/warning/error/success) |
| `a-statistic` | 统计数值 | title, value, prefix |
| `a-card` | 卡片容器 | bordered, title |
| `a-tabs/a-tab-pane` | 标签页 | default-active-key, title |
| `a-dropdown/a-doption` | 下拉菜单 | @click |
| `a-tooltip` | 文字提示 | content |
| `a-empty` | 空状态 | description |
