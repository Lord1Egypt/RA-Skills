# Vue.js 代码片段

## 1. 基础组件模板

### 1.1 单文件组件 (SFC)

```vue
<template>
  <div class="component-container">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <button @click="handleClick">点击我</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 定义 props
const props = defineProps<{
  title: string
  description?: string
}>()

// 定义 emits
const emit = defineEmits<{
  (e: 'click', payload: { timestamp: number }): void
}>()

// 响应式数据
const count = ref(0)

// 计算属性
const doubleCount = computed(() => count.value * 2)

// 方法
const handleClick = () => {
  count.value++
  emit('click', { timestamp: Date.now() })
}
</script>

<style scoped>
.component-container {
  padding: 20px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
}

button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #35495e;
}
</style>
```

### 1.2 组合式API 逻辑复用

```vue
<template>
  <div>
    <h2>计数器: {{ count }}</h2>
    <button @click="increment">增加</button>
    <button @click="decrement">减少</button>
  </div>
</template>

<script setup lang="ts">
import { useCounter } from './composables/useCounter'

const { count, increment, decrement } = useCounter(0)
</script>
```

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initialValue: number = 0) {
  const count = ref(initialValue)
  
  const increment = () => {
    count.value++
  }
  
  const decrement = () => {
    count.value--
  }
  
  const reset = () => {
    count.value = initialValue
  }
  
  const doubleCount = computed(() => count.value * 2)
  
  return {
    count,
    increment,
    decrement,
    reset,
    doubleCount
  }
}
```

## 2. 状态管理

### 2.1 Pinia 存储

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Pinia Counter'
  }),
  getters: {
    doubleCount: (state) => state.count * 2,
    greet: (state) => `Hello, ${state.name}!`
  },
  actions: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    },
    reset() {
      this.count = 0
    },
    setName(name: string) {
      this.name = name
    }
  }
})
```

### 2.2 组件中使用 Pinia

```vue
<template>
  <div>
    <h2>{{ store.name }}</h2>
    <p>计数: {{ store.count }}</p>
    <p>双倍计数: {{ store.doubleCount }}</p>
    <button @click="store.increment">增加</button>
    <button @click="store.decrement">减少</button>
    <button @click="store.reset">重置</button>
  </div>
</template>

<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>
```

## 3. 路由

### 3.1 路由配置

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // 懒加载
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/user/:id',
      name: 'user',
      component: () => import('../views/UserView.vue'),
      props: true
    }
  ]
})

export default router
```

### 3.2 组件中使用路由

```vue
<template>
  <div>
    <h2>用户详情</h2>
    <p>用户ID: {{ id }}</p>
    <router-link to="/">返回首页</router-link>
    <button @click="goBack">返回</button>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const id = route.params.id

const goBack = () => {
  router.back()
}
</script>
```

## 4. API 调用

### 4.1 基本 API 调用

```typescript
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 统一错误处理
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api
```

### 4.2 组件中使用 API

```vue
<template>
  <div>
    <h2>用户列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">错误: {{ error }}</div>
    <ul v-else>
      <li v-for="user in users" :key="user.id">
        {{ user.name }} - {{ user.email }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const users = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    users.value = await api.get('/users')
  } catch (err) {
    error.value = '获取用户列表失败'
  } finally {
    loading.value = false
  }
})
</script>
```

## 5. 表单处理

### 5.1 基本表单

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="name">姓名:</label>
      <input 
        type="text" 
        id="name" 
        v-model="form.name"
        required
      />
    </div>
    <div>
      <label for="email">邮箱:</label>
      <input 
        type="email" 
        id="email" 
        v-model="form.email"
        required
      />
    </div>
    <button type="submit">提交</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface FormData {
  name: string
  email: string
}

const form = ref<FormData>({
  name: '',
  email: ''
})

const handleSubmit = () => {
  console.log('表单数据:', form.value)
  // 在这里处理表单提交逻辑
}
</script>
```

### 5.2 表单验证

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <div>
      <label for="name">姓名:</label>
      <input 
        type="text" 
        id="name" 
        v-model="form.name"
      />
      <div v-if="errors.name" class="error">
        {{ errors.name }}
      </div>
    </div>
    <div>
      <label for="email">邮箱:</label>
      <input 
        type="email" 
        id="email" 
        v-model="form.email"
      />
      <div v-if="errors.email" class="error">
        {{ errors.email }}
      </div>
    </div>
    <button type="submit">提交</button>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface FormData {
  name: string
  email: string
}

interface Errors {
  name: string | ''
  email: string | ''
}

const form = ref<FormData>({
  name: '',
  email: ''
})

const errors = reactive<Errors>({
  name: '',
  email: ''
})

const validateForm = (): boolean => {
  let isValid = true
  
  // 重置错误
  errors.name = ''
  errors.email = ''
  
  // 验证姓名
  if (!form.value.name.trim()) {
    errors.name = '姓名不能为空'
    isValid = false
  }
  
  // 验证邮箱
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.value.email.trim()) {
    errors.email = '邮箱不能为空'
    isValid = false
  } else if (!emailRegex.test(form.value.email)) {
    errors.email = '请输入有效的邮箱地址'
    isValid = false
  }
  
  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    console.log('表单数据:', form.value)
    // 在这里处理表单提交逻辑
  }
}
</script>

<style scoped>
.error {
  color: red;
  font-size: 12px;
  margin-top: 4px;
}
</style>
```

## 6. 动画和过渡

### 6.1 基本过渡

```vue
<template>
  <div>
    <button @click="show = !show">
      {{ show ? '隐藏' : '显示' }}
    </button>
    <transition name="fade">
      <div v-if="show" class="box">
        这是一个过渡动画
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.box {
  width: 200px;
  height: 200px;
  background-color: #42b983;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

### 6.2 列表过渡

```vue
<template>
  <div>
    <button @click="addItem">添加项目</button>
    <button @click="removeItem">移除项目</button>
    <transition-group name="list" tag="ul">
      <li v-for="(item, index) in items" :key="item.id">
        {{ item.text }}
      </li>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Item {
  id: number
  text: string
}

const items = ref<Item[]>([
  { id: 1, text: '项目 1' },
  { id: 2, text: '项目 2' },
  { id: 3, text: '项目 3' }
])

let nextId = 4

const addItem = () => {
  items.value.push({
    id: nextId++,
    text: `项目 ${nextId - 1}`
  })
}

const removeItem = () => {
  items.value.pop()
}
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 10px;
  margin: 5px 0;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
```

## 7. 生命周期钩子

```vue
<template>
  <div>
    <h2>生命周期钩子示例</h2>
    <p>当前计数: {{ count }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

const count = ref(0)

// 组件挂载前
onBeforeMount(() => {
  console.log('组件挂载前')
})

// 组件挂载后
onMounted(() => {
  console.log('组件挂载后')
  // 可以在这里初始化数据、绑定事件等
  const interval = setInterval(() => {
    count.value++
  }, 1000)
  
  // 清理函数
  return () => {
    clearInterval(interval)
  }
})

// 组件更新前
onBeforeUpdate(() => {
  console.log('组件更新前')
})

// 组件更新后
onUpdated(() => {
  console.log('组件更新后')
})

// 组件卸载前
onBeforeUnmount(() => {
  console.log('组件卸载前')
})

// 组件卸载后
onUnmounted(() => {
  console.log('组件卸载后')
  // 可以在这里清理定时器、事件监听器等
})
</script>
```

## 8. 组合式API 高级用法

### 8.1 依赖注入

```vue
<template>
  <div>
    <h2>依赖注入示例</h2>
    <ChildComponent />
  </div>
</template>

<script setup lang="ts">
import { provide } from 'vue'
import ChildComponent from './ChildComponent.vue'

// 提供依赖
provide('message', 'Hello from parent')
provide('user', {
  name: 'John',
  age: 30
})
</script>
```

```vue
<template>
  <div>
    <h3>子组件</h3>
    <p>{{ message }}</p>
    <p>用户: {{ user.name }}, {{ user.age }}岁</p>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'

// 注入依赖
const message = inject('message', '默认消息')
const user = inject('user', { name: 'Guest', age: 0 })
</script>
```

### 8.2 响应式工具

```typescript
// composables/useDebounce.ts
import { ref, watch } from 'vue'

export function useDebounce<T>(value: T, delay: number = 300) {
  const debouncedValue = ref(value)
  let timeoutId: ReturnType<typeof setTimeout>
  
  watch(
    () => value,
    (newValue) => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => {
        debouncedValue.value = newValue
      }, delay)
    }
  )
  
  return debouncedValue
}
```

```vue
<template>
  <div>
    <input 
      type="text" 
      v-model="inputValue"
      placeholder="输入搜索内容"
    />
    <p>防抖后的值: {{ debouncedValue }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDebounce } from './composables/useDebounce'

const inputValue = ref('')
const debouncedValue = useDebounce(inputValue, 500)
</script>
```

## 9. 性能优化

### 9.1 使用 `v-memo`

```vue
<template>
  <div>
    <h2>使用 v-memo 优化性能</h2>
    <div v-for="item in items" :key="item.id" v-memo="[item.value]">
      <div>{{ item.name }}</div>
      <div>{{ item.value }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Item {
  id: number
  name: string
  value: number
}

const items = ref<Item[]>([
  { id: 1, name: '项目 1', value: 10 },
  { id: 2, name: '项目 2', value: 20 },
  { id: 3, name: '项目 3', value: 30 }
])
</script>
```

### 9.2 虚拟滚动

```vue
<template>
  <div class="virtual-list" ref="container">
    <div 
      class="virtual-list-container"
      :style="{ height: totalHeight + 'px' }"
    >
      <div 
        class="virtual-list-content"
        :style="{ transform: `translateY(${offset}px)` }"
      >
        <div 
          v-for="item in visibleItems" 
          :key="item.id"
          class="virtual-list-item"
        >
          {{ item.text }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Item {
  id: number
  text: string
}

const container = ref<HTMLElement | null>(null)
const items = ref<Item[]>([])
const itemHeight = 50
const visibleCount = 10

// 生成大量数据
for (let i = 1; i <= 1000; i++) {
  items.value.push({ id: i, text: `项目 ${i}` })
}

const totalHeight = computed(() => items.value.length * itemHeight)
const startIndex = ref(0)
const endIndex = ref(Math.min(visibleCount, items.value.length))

const visibleItems = computed(() => {
  return items.value.slice(startIndex.value, endIndex.value)
})

const offset = computed(() => startIndex.value * itemHeight)

const handleScroll = () => {
  if (!container.value) return
  
  const scrollTop = container.value.scrollTop
  const newStartIndex = Math.floor(scrollTop / itemHeight)
  const newEndIndex = Math.min(newStartIndex + visibleCount, items.value.length)
  
  startIndex.value = newStartIndex
  endIndex.value = newEndIndex
}

onMounted(() => {
  if (container.value) {
    container.value.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  if (container.value) {
    container.value.removeEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
.virtual-list {
  width: 300px;
  height: 500px;
  border: 1px solid #eaeaea;
  overflow-y: auto;
}

.virtual-list-container {
  position: relative;
  width: 100%;
}

.virtual-list-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}

.virtual-list-item {
  height: 48px;
  line-height: 48px;
  padding: 0 16px;
  border-bottom: 1px solid #eaeaea;
}
</style>
```

## 10. 测试

### 10.1 组件测试

```typescript
// tests/components/HelloWorld.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HelloWorld from '@/components/HelloWorld.vue'

describe('HelloWorld', () => {
  it('renders properly', () => {
    const wrapper = mount(HelloWorld, {
      props: {
        msg: 'Hello Vitest'
      }
    })
    expect(wrapper.text()).toContain('Hello Vitest')
  })
  
  it('emits click event when button is clicked', () => {
    const wrapper = mount(HelloWorld)
    const button = wrapper.find('button')
    button.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

## 11. 部署

### 11.1 Vite 构建配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    minify: 'terser',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['axios']
        }
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
})
```

### 11.2 Docker 部署

```dockerfile
# Dockerfile
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

*本代码片段库将持续更新，以反映 Vue.js 的最新最佳实践和特性。*