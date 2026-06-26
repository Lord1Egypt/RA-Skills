# 页面模板

## 目录

- 列表页模板
- 表单页模板
- 详情页模板
- Dashboard 页模板
- 空状态页模板
- 路由注册模板

## 列表页模板

```vue
<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import {
    FormInstance,
    Modal,
    Notification,
    Message,
  } from '@arco-design/web-vue';

  interface {{Entity}}DTO {
    id: number;
    // TODO: 根据业务定义字段
  }

  type FilterType = {
    // TODO: 根据业务定义筛选字段
  };

  const MOCK_DATA: {{Entity}}DTO[] = [
    // TODO: 填充 mock 数据，至少 5 条
  ];

  const mockFetch = (params: any): Promise<{ code: number; data: { list: {{Entity}}DTO[]; count: number } }> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const start = (params.page - 1) * params.limit;
        const list = MOCK_DATA.slice(start, start + params.limit);
        resolve({ code: 0, data: { list, count: MOCK_DATA.length } });
      }, 300);
    });
  };

  const filterFormRef = ref<FormInstance>();
  const data = ref<{{Entity}}DTO[]>([]);

  const req = ref({
    loading: false,
    data: {
      // 筛选字段初始值
    } as FilterType,
    pagination: {
      current: 1,
      pageSize: 10,
      total: 0,
    },
  });

  const columns = [
    // { title: '字段名', dataIndex: 'field', width: 150 },
    // { title: '操作', slotName: 'action', width: 200, fixed: 'right' as const },
  ];

  const editModal = ref({
    visible: false,
    itemId: 0,
    isEdit: false,
  });

  const getList = () => {
    req.value.loading = true;
    const params = {
      page: req.value.pagination.current,
      limit: req.value.pagination.pageSize,
      // ...筛选参数
    };

    // TODO: 替换为真实 API 调用
    mockFetch(params)
      .then((res) => {
        if (res.code !== 0) {
          Modal.confirm({ title: '请求失败', content: '加载数据失败' });
          return;
        }
        data.value = res.data.list;
        req.value.pagination.total = res.data.count;
      })
      .finally(() => {
        req.value.loading = false;
      });
  };

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

  const handleAdd = () => {
    editModal.value.itemId = 0;
    editModal.value.isEdit = false;
    editModal.value.visible = true;
  };

  const handleEdit = (record: {{Entity}}DTO) => {
    editModal.value.itemId = record.id;
    editModal.value.isEdit = true;
    editModal.value.visible = true;
  };

  const handleDelete = (record: {{Entity}}DTO) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该记录吗？此操作不可恢复！',
      onOk: () => {
        // TODO: 替换为真实 API 调用
        Notification.success('删除成功');
        getList();
      },
    });
  };

  const handleEditModalClose = (shouldRefresh: boolean) => {
    editModal.value.visible = false;
    editModal.value.itemId = 0;
    editModal.value.isEdit = false;
    if (shouldRefresh) {
      getList();
    }
  };

  onMounted(() => {
    getList();
  });
</script>

<template>
  <a-space class="page-container" direction="vertical" fill>
    <div class="toolbar">
      <a-row :gutter="[24, 24]" style="margin: auto; width: 100%">
        <a-col :span="24">
          <a-form :model="req.data" layout="vertical" ref="filterFormRef">
            <a-row :gutter="16">
              <a-col :span="6">
                <a-form-item field="fieldName" label="字段名">
                  <a-input
                    v-model="req.data.fieldName"
                    placeholder="请输入"
                    allow-clear
                  />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
        <a-col :span="24">
          <a-space>
            <a-button type="primary" @click="handleSearch">搜索</a-button>
            <a-button @click="handleReset">重置</a-button>
            <a-divider direction="vertical" />
            <a-button type="primary" @click="handleAdd">新增</a-button>
          </a-space>
        </a-col>
      </a-row>
    </div>

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
      <template #action="{ record }">
        <a-space>
          <a-button type="primary" size="small" @click="handleEdit(record)">
            编辑
          </a-button>
          <a-button
            type="outline"
            status="danger"
            size="small"
            @click="handleDelete(record)"
          >
            删除
          </a-button>
        </a-space>
      </template>
    </a-table>

    <a-modal
      v-if="editModal.visible"
      draggable
      :align-center="false"
      :top="60"
      :mask-closable="false"
      width="700px"
      :footer="false"
      v-model:visible="editModal.visible"
      @cancel="handleEditModalClose(false)"
    >
      <template #title>
        {{ editModal.isEdit ? '编辑' : '新增' }}
      </template>
      <div style="padding: 20px">编辑表单区域</div>
    </a-modal>
  </a-space>
</template>

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

## 表单页模板

```vue
<script setup lang="ts">
  import { ref, computed } from 'vue';
  import { FormInstance, Notification } from '@arco-design/web-vue';

  interface FormData {
    // TODO: 根据业务定义字段
  }

  interface Props {
    itemId?: number;
    isEdit: boolean;
  }

  interface Emits {
    (e: 'close', shouldRefresh: boolean): void;
  }

  const props = defineProps<Props>();
  const emit = defineEmits<Emits>();

  const formRef = ref<FormInstance>();
  const loading = ref(false);

  const formData = ref<FormData>({
    // TODO: 初始值
  });

  const rules = computed(() => ({
    // fieldName: [{ required: true, message: '请输入字段名' }],
  }));

  const handleSubmit = async () => {
    try {
      const valid = await formRef.value?.validate();
      if (valid) return;

      loading.value = true;
      // TODO: 替换为真实 API 调用
      await new Promise((resolve) => setTimeout(resolve, 500));
      Notification.success(props.isEdit ? '编辑成功' : '新增成功');
      emit('close', true);
    } catch (error) {
      Notification.error('操作失败');
    } finally {
      loading.value = false;
    }
  };

  const handleCancel = () => {
    emit('close', false);
  };
</script>

<template>
  <a-spin :loading="loading">
    <a-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      layout="vertical"
      auto-label-width
    >
      <a-divider orientation="left">基本信息</a-divider>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item field="fieldName" label="字段名">
            <a-input v-model="formData.fieldName" placeholder="请输入" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-divider />
      <a-space>
        <a-button type="primary" :loading="loading" @click="handleSubmit">
          {{ isEdit ? '保存' : '提交' }}
        </a-button>
        <a-button @click="handleCancel">取消</a-button>
      </a-space>
    </a-form>
  </a-spin>
</template>
```

## 详情页模板

```vue
<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { Notification } from '@arco-design/web-vue';

  interface {{Entity}}DetailDTO {
    id: number;
    // TODO: 根据业务定义字段
  }

  const MOCK_DETAIL: {{Entity}}DetailDTO = {
    id: 1,
    // TODO: 填充 mock 详情数据
  };

  const loading = ref(false);
  const detail = ref<{{Entity}}DetailDTO | null>(null);

  const loadDetail = async () => {
    loading.value = true;
    try {
      // TODO: 替换为真实 API 调用
      await new Promise((resolve) => setTimeout(resolve, 300));
      detail.value = MOCK_DETAIL;
    } catch (error) {
      Notification.error('加载详情失败');
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    loadDetail();
  });
</script>

<template>
  <a-spin :loading="loading" style="width: 100%">
    <a-space direction="vertical" fill style="padding: 16px" v-if="detail">
      <a-page-header :title="'详情'" @back="$router.back()">
        <template #extra>
          <a-space>
            <a-button type="primary">编辑</a-button>
          </a-space>
        </template>
      </a-page-header>

      <a-card title="基本信息" :bordered="false">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="ID">{{ detail.id }}</a-descriptions-item>
        </a-descriptions>
      </a-card>
    </a-space>
  </a-spin>
</template>
```

## Dashboard 页模板

```vue
<script setup lang="ts">
  import { ref, onMounted } from 'vue';

  const MOCK_STATS = {
    total: 1256,
    today: 42,
    active: 890,
    pending: 23,
  };

  const MOCK_CHART_DATA = {
    xAxis: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    series: [120, 200, 150, 80, 70, 110, 130],
  };

  const loading = ref(false);
  const stats = ref(MOCK_STATS);
  const chartData = ref(MOCK_CHART_DATA);

  onMounted(() => {
    // TODO: 替换为真实 API 调用
  });
</script>

<template>
  <div style="padding: 16px">
    <a-row :gutter="16" style="margin-bottom: 16px">
      <a-col :span="6">
        <a-card :bordered="false">
          <a-statistic title="总数" :value="stats.total" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false">
          <a-statistic title="今日新增" :value="stats.today" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false">
          <a-statistic title="活跃" :value="stats.active" />
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card :bordered="false">
          <a-statistic title="待处理" :value="stats.pending" />
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16">
      <a-col :span="16">
        <a-card title="趋势图" :bordered="false">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: var(--color-text-3)">
            图表区域 (使用 vue-echarts 或 Chart 组件)
          </div>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="分布" :bordered="false">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: var(--color-text-3)">
            饼图区域
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>
```

## 空状态页模板

```vue
<template>
  <div style="padding: 16px">
    <a-card :bordered="false">
      <a-empty style="padding: 80px 0">
        <template #image>
          <icon-file style="font-size: 48px; color: var(--color-text-3)" />
        </template>
        暂无数据，请先创建
        <template #extra>
          <a-button type="primary" @click="handleCreate">
            立即创建
          </a-button>
        </template>
      </a-empty>
    </a-card>
  </div>
</template>

<script setup lang="ts">
  const handleCreate = () => {
    // TODO: 跳转到创建页面或打开弹窗
  };
</script>
```

## 路由注册模板

```typescript
import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const MODULE_NAME: AppRouteRecordRaw = {
  path: '/{module-name}',
  name: '{moduleName}',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.{moduleName}',
    requiresAuth: true,
    icon: 'icon-apps',
    order: 10,
  },
  children: [
    {
      path: 'list',
      name: '{ModuleName}List',
      component: () => import('@/views/{module-name}/index.vue'),
      meta: {
        locale: 'menu.{moduleName}.list',
        requiresAuth: true,
        roles: ['*'],
      },
    },
  ],
};

export default MODULE_NAME;
```
