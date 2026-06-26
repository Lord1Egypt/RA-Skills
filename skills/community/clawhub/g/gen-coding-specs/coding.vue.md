# Vue.js 开发规范

## 概述
本文档定义 Vue.js 项目的开发规范，基于 **Vue 3 + TypeScript + Composition API** 技术栈，确保前端代码的一致性、可维护性和性能。

## 技术栈标准

- **框架**: Vue 3.x
- **语言**: TypeScript 4.x+
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router 4.x
- **UI组件库**: [项目指定组件库，如 Element Plus / Ant Design Vue]
- **CSS预处理器**: SCSS / Less

## 目录结构

```
src/
├── assets/             # 静态资源 (图片, 字体)
├── components/         # 公共组件 (基础组件)
│   ├── common/         # 通用组件
│   └── layout/         # 布局组件
├── composables/        # 组合式函数 (Hooks)
├── directives/         # 自定义指令
├── layouts/            # 布局页面
├── router/             # 路由配置
├── stores/             # Pinia 状态管理
├── styles/             # 全局样式
├── types/              # TypeScript 类型定义
├── utils/              # 工具函数
├── views/              # 页面组件
└── App.vue
└── main.ts
```

## 组件规范

### 1. 组件定义
统一使用 `<script setup lang="ts">` 语法。

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';
import type { User } from '@/types/user';

// Props 定义
interface Props {
  title: string;
  items?: User[];
}
const props = withDefaults(defineProps<Props>(), {
  items: () => []
});

// Emits 定义
const emit = defineEmits<{
  (e: 'update', id: number): void;
  (e: 'delete', id: number): void;
}>();

// 状态
const activeId = ref<number | null>(null);

// 计算属性
const hasItems = computed(() => props.items.length > 0);

// 方法
const handleUpdate = (id: number) => {
  activeId.value = id;
  emit('update', id);
};
</script>

<template>
  <div class="user-list">
    <h3>{{ title }}</h3>
    <ul v-if="hasItems">
      <li v-for="item in items" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>
```

### 2. 命名规范
- **文件命名**: 使用 **PascalCase** (如 `UserProfile.vue`)。
- **组件引用**: 使用 **PascalCase** (如 `<UserProfile />`)。
- **Props**: 声明时使用 camelCase，模板中使用 kebab-case。

### 3. 组件通信
- **父子组件**: 使用 `props` 和 `emit`。
- **跨层级**: 使用 `provide` / `inject` 或 Pinia。
- **避免**: 避免使用 `$parent` 或 `$refs` 进行数据传递。

## 状态管理 (Pinia)

### 1. Store 定义
使用 Setup Store 语法定义 Store。

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { getUserList } from '@/api/user';
import type { User } from '@/types/user';

export const useUserStore = defineStore('user', () => {
  // State
  const users = ref<User[]>([]);
  const loading = ref(false);

  // Getters
  const activeUsers = computed(() => users.value.filter(u => u.isActive));

  // Actions
  async function fetchUsers() {
    loading.value = true;
    try {
      users.value = await getUserList();
    } finally {
      loading.value = false;
    }
  }

  return { users, loading, activeUsers, fetchUsers };
});
```

### 2. Store 使用
```vue
<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
// 保持响应性解构
const { users, loading } = storeToRefs(userStore);
// 直接解构 Actions
const { fetchUsers } = userStore;
</script>
```

## 组合式函数 (Composables)

将可复用的逻辑提取为 Composable 函数，以此替代 Mixins。
命名约定：`useXxx`。

```typescript
// composables/usePagination.ts
import { ref, computed } from 'vue';

export function usePagination(callback: (page: number) => Promise<void>) {
  const currentPage = ref(1);
  const pageSize = ref(10);
  const total = ref(0);

  const handlePageChange = (page: number) => {
    currentPage.value = page;
    callback(page);
  };

  return {
    currentPage,
    pageSize,
    total,
    handlePageChange
  };
}
```

## 性能优化

1.  **按需引入**: 组件库和第三方库尽量按需引入。
2.  **异步组件**: 对于大型组件或路由页面，使用 `defineAsyncComponent` 或路由懒加载。
    ```typescript
    const UserDetail = () => import('@/views/UserDetail.vue');
    ```
3.  **计算属性缓存**: 若依赖未变化，计算属性不会重新计算，善用 `computed`。
4.  **v-show vs v-if**: 频繁切换显示状态使用 `v-show`，条件渲染使用 `v-if`。
5.  **Key 的使用**: `v-for` 循环必须绑定唯一的 `key`，避免使用 index。

## 风格指南

- **HTML 指令顺序**: `v-if` / `v-show` > `v-for` > `id` > `ref` > `key` > `v-model` > 其他属性 > 事件。
- **自闭合标签**: 内容为空的组件使用自闭合标签 `<MyComponent />`。
- **模板简洁**: 如果模板逻辑复杂，提取为计算属性。

---

> **上下文提示**：在开发 Vue 组件时，建议同时加载：
> - `coding.api.md` - 接口调用规范
> - `coding.coding-style.md` - 通用编码风格
