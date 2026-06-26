# Vue.js 最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Vue 3 核心特性

### 1.1 Composition API

**核心优势：**
- 逻辑组织更灵活
- 代码复用性强
- TypeScript支持更好
- 更容易测试

**基本用法：**

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// 响应式状态
const count = ref(0);

// 计算属性
const doubleCount = computed(() => count.value * 2);

// 生命周期钩子
onMounted(() => {
  console.log('Component mounted');
});

// 方法
const increment = () => {
  count.value++;
};
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

---

### 1.2 Script Setup

**优势：**
- 更简洁的语法
- 自动暴露变量和方法
- 更好的TypeScript支持
- 减少样板代码

**使用示例：**

```vue
<script setup lang="ts">
// 自动导入
import { ref } from 'vue';

// 自动暴露给模板
const message = ref('Hello Vue 3');

// 自动暴露方法
const greet = () => {
  console.log(message.value);
};
</script>

<template>
  <div>
    <p>{{ message }}</p>
    <button @click="greet">Greet</button>
  </div>
</template>
```

---

## 二、组件设计最佳实践

### 2.1 组件拆分原则

**建议：**
- 单一职责：每个组件只负责一个功能
- 合理大小：组件代码不超过200行
- 可复用性：设计通用组件
- 清晰命名：使用语义化的组件名称

**示例：**

```
components/
├── Button.vue         # 通用按钮
├── Card.vue           # 卡片组件
├── Input.vue          # 输入框
└── UserList/
    ├── UserList.vue   # 列表容器
    └── UserItem.vue   # 列表项
```

---

### 2.2 Props 设计

**最佳实践：**
- 使用TypeScript类型定义
- 设置默认值
- 验证props
- 使用解构和默认值

**示例：**

```vue
<script setup lang="ts">
interface Props {
  title: string;
  description?: string;
  count?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  description: '',
  count: 0,
  disabled: false
});
</script>
```

---

### 2.3 Emits 设计

**最佳实践：**
- 定义emit类型
- 使用kebab-case命名
- 传递必要的参数

**示例：**

```vue
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update:count', value: number): void;
  (e: 'submit', formData: Record<string, any>): void;
}>();

const handleSubmit = () => {
  emit('submit', { name: 'John' });
};
</script>
```

---

## 三、状态管理

### 3.1 Pinia

**优势：**
- 轻量
- TypeScript支持
- 模块化设计
- 更好的开发体验

**基本用法：**

```typescript
// stores/counter.ts
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0);
  
  function increment() {
    count.value++;
  }
  
  function decrement() {
    count.value--;
  }
  
  return {
    count,
    increment,
    decrement
  };
});

// 在组件中使用
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
store.increment();
```

---

### 3.2 状态管理最佳实践

**建议：**
- 状态集中管理
- 模块化设计
- 合理的状态结构
- 异步操作处理

---

## 四、性能优化

### 4.1 响应式优化

**技巧：**
- 使用 `shallowRef` 和 `shallowReactive` 处理大型对象
- 使用 `markRaw` 跳过响应式转换
- 合理使用 `computed` 缓存计算结果
- 避免在模板中执行复杂计算

**示例：**

```vue
<script setup>
import { shallowRef, markRaw } from 'vue';

// 大型对象使用shallowRef
const largeObject = shallowRef({ /* 大型数据 */ });

// 不需要响应式的对象
const nonReactive = markRaw({ /* 数据 */ });
</script>
```

---

### 4.2 渲染优化

**技巧：**
- 使用 `v-memo` 缓存渲染结果
- 合理使用 `v-if` 和 `v-show`
- 避免不必要的组件渲染
- 使用虚拟滚动处理长列表

**示例：**

```vue
<template>
  <!-- 缓存渲染结果 -->
  <div v-memo="[value]">
    {{ expensiveComputation(value) }}
  </div>
  
  <!-- 长列表虚拟滚动 -->
  <virtual-list
    :data-key="'id'"
    :data-sources="items"
    :data-component="Item"
    :estimate-size="50"
  />
</template>
```

---

### 4.3 构建优化

**建议：**
- 代码分割
- 树摇
- 按需加载
- 资源优化

**配置示例：**

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'pinia'],
          router: ['vue-router']
        }
      }
    }
  }
});
```

---

## 五、路由管理

### 5.1 Vue Router 4

**核心特性：**
- 组合式API支持
- 动态路由
- 嵌套路由
- 导航守卫

**基本配置：**

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/about',
    component: () => import('@/views/About.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
```

---

### 5.2 路由最佳实践

**建议：**
- 懒加载路由组件
- 合理的路由结构
- 导航守卫使用
- 路由元信息

---

## 六、表单处理

### 6.1 表单最佳实践

**建议：**
- 使用 `v-model` 双向绑定
- 表单验证
- 错误处理
- 防抖处理

**示例：**

```vue
<script setup>
import { ref, computed } from 'vue';

const form = ref({
  name: '',
  email: ''
});

const errors = computed(() => {
  const result = {};
  if (!form.value.name) result.name = 'Name is required';
  if (!form.value.email) result.email = 'Email is required';
  return result;
});

const isValid = computed(() => Object.keys(errors.value).length === 0);

const handleSubmit = () => {
  if (isValid.value) {
    // 提交逻辑
  }
};
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label>Name</label>
      <input v-model="form.name" />
      <span v-if="errors.name">{{ errors.name }}</span>
    </div>
    <div>
      <label>Email</label>
      <input v-model="form.email" type="email" />
      <span v-if="errors.email">{{ errors.email }}</span>
    </div>
    <button type="submit" :disabled="!isValid">Submit</button>
  </form>
</template>
```

---

## 七、测试策略

### 7.1 单元测试

**工具：**
- Vitest
- Vue Test Utils

**示例：**

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '@/components/Button.vue';

describe('Button', () => {
  it('renders correctly', () => {
    const wrapper = mount(Button, {
      props: {
        label: 'Click me'
      }
    });
    expect(wrapper.text()).toContain('Click me');
  });
  
  it('emits click event', async () => {
    const wrapper = mount(Button, {
      props: {
        label: 'Click me'
      }
    });
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toBeTruthy();
  });
});
```

---

### 7.2 E2E测试

**工具：**
- Cypress
- Playwright

---

## 八、项目结构

### 8.1 推荐结构

```
src/
├── assets/          # 静态资源
├── components/      # 通用组件
├── composables/     # 组合式函数
├── views/           # 页面组件
├── stores/          # Pinia 状态管理
├── router/          # 路由配置
├── services/        # API 服务
├── utils/           # 工具函数
├── types/           # TypeScript 类型
├── App.vue          # 根组件
└── main.ts          # 入口文件
```

---

## 九、TypeScript 最佳实践

### 9.1 类型定义

**建议：**
- 为props定义接口
- 为store定义类型
- 为API响应定义类型
- 使用泛型增强类型安全性

**示例：**

```typescript
// types/user.ts
export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

// components/UserCard.vue
<script setup lang="ts">
import type { User } from '@/types/user';

const props = defineProps<{
  user: User;
}>();
</script>
```

---

### 9.2 类型工具

**常用类型：**
- `Partial<T>` - 部分属性可选
- `Required<T>` - 所有属性必填
- `Pick<T, K>` - 选择部分属性
- `Omit<T, K>` - 排除部分属性
- `Record<K, T>` - 键值对类型

---

## 十、部署与CI/CD

### 10.1 部署策略

**建议：**
- 静态站点生成(SSG)
- 服务端渲染(SSR)
- 容器化部署
- CDN加速

### 10.2 CI/CD配置

**示例：**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## 十一、常见问题与解决方案

### 11.1 性能问题

**问题：** 页面渲染缓慢
**解决方案：**
- 使用虚拟滚动
- 优化组件渲染
- 减少不必要的计算
- 使用缓存

### 11.2 内存泄漏

**问题：** 组件卸载后内存未释放
**解决方案：**
- 清理事件监听器
- 取消异步操作
- 清理定时器

### 11.3 状态管理混乱

**问题：** 状态分散，难以管理
**解决方案：**
- 使用Pinia集中管理状态
- 合理的状态结构设计
- 模块化状态管理

---

## 十二、最佳实践总结

1. **使用Composition API**：更好的逻辑组织和代码复用
2. **TypeScript优先**：类型安全，更好的开发体验
3. **组件化设计**：单一职责，可复用性
4. **性能优化**：响应式优化，渲染优化
5. **状态管理**：Pinia轻量高效
6. **路由管理**：懒加载，合理结构
7. **表单处理**：验证，错误处理
8. **测试策略**：单元测试，E2E测试
9. **项目结构**：清晰，模块化
10. **部署优化**：CI/CD，性能优化

---

## 相关资源

- [Vue 3 官方文档](https://vuejs.org/docs)
- [Vue Router 官方文档](https://router.vuejs.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [Vue Test Utils 文档](https://test-utils.vuejs.org/)

