# 前端框架最佳实践总结

> 整理日期：2026-05-25
> 归属：full-stack-architect技能

---

## 一、Vue 3 最佳实践

### 1.1 项目结构

**推荐结构：**

```
src/
├── assets/            # 静态资源
├── components/        # 通用组件
├── composables/       # 组合式函数
├── directives/        # 自定义指令
├── layouts/           # 布局组件
├── pages/             # 页面组件
├── router/            # 路由配置
├── stores/            # 状态管理
├── utils/             # 工具函数
├── services/          # API服务
├── App.vue            # 根组件
└── main.js            # 入口文件
```

**命名规范：**
- 组件：PascalCase（UserProfile.vue）
- 文件夹：kebab-case（user-profile）
- 变量：camelCase
- 常量：UPPERCASE
- 组合式函数：use前缀（useAuth.js）

---

### 1.2 Composition API

**最佳实践：**
- 使用 `setup()` 函数或 `<script setup>`
- 合理组织组合式函数
- 使用 `ref` 和 `reactive` 管理状态
- 利用 `watch` 和 `computed` 响应式数据
- 生命周期钩子函数使用

**示例：**

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 响应式状态
const count = ref(0)
const message = ref('Hello Vue 3')

// 计算属性
const doubledCount = computed(() => count.value * 2)

// 方法
const increment = () => {
  count.value++
}

// 生命周期
onMounted(() => {
  console.log('Component mounted')
})

// 路由
const router = useRouter()
const navigateToAbout = () => {
  router.push('/about')
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubledCount }}</p>
    <button @click="increment">Increment</button>
    <button @click="navigateToAbout">Go to About</button>
  </div>
</template>
```

**组合式函数示例：**

```javascript
// composables/useAuth.js
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export function useAuth() {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const router = useRouter()

  const login = async (credentials) => {
    // 登录逻辑
    user.value = { id: 1, name: 'John' }
  }

  const logout = () => {
    user.value = null
    router.push('/login')
  }

  return {
    user,
    isAuthenticated,
    login,
    logout
  }
}

// 使用
<script setup>
import { useAuth } from '@/composables/useAuth'

const { user, isAuthenticated, login, logout } = useAuth()
</script>
```

---

### 1.3 响应式系统

**ref vs reactive：**
- **ref**：适用于基本类型和对象
- **reactive**：适用于对象
- **最佳实践**：优先使用 ref，保持一致性

**示例：**

```javascript
// ref 示例
import { ref } from 'vue'

const count = ref(0)
const user = ref({ name: 'John', age: 30 })

// 修改
count.value++
user.value.name = 'Jane'

// reactive 示例
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  user: { name: 'John', age: 30 }
})

// 修改
state.count++
state.user.name = 'Jane'
```

**响应式深度：**
- `reactive` 默认深度响应
- `ref` 对于对象也是深度响应
- 使用 `shallowRef` 和 `shallowReactive` 浅响应

---

### 1.4 状态管理

**Pinia 最佳实践：**
- 模块化 store
- 使用 composition API
- 类型安全
- 持久化存储

**示例：**

```javascript
// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    loading: false
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.user,
    userName: (state) => state.user?.name || 'Guest'
  },
  
  actions: {
    async login(credentials) {
      this.loading = true
      try {
        // 登录逻辑
        this.user = { id: 1, name: 'John' }
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
    }
  }
})

// 使用
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const handleLogin = async () => {
  await userStore.login({ email: 'test@example.com', password: 'password' })
}
</script>
```

---

### 1.5 路由

**Vue Router 4 最佳实践：**
- 动态路由
- 嵌套路由
- 路由守卫
- 懒加载

**示例：**

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/pages/About.vue')
  },
  {
    path: '/user/:id',
    name: 'User',
    component: () => import('@/pages/User.vue'),
    props: true
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = !!localStorage.getItem('token')
  
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

---

### 1.6 性能优化

**最佳实践：**
- 使用 `v-memo` 缓存渲染结果
- 合理使用 `v-if` 和 `v-show`
- 组件懒加载
- 虚拟滚动
- 避免不必要的响应式

**示例：**

```vue
<!-- v-memo 示例 -->
<div v-for="item in items" :key="item.id" v-memo="[item.id, item.name]">
  {{ item.name }}
</div>

<!-- 组件懒加载 -->
<template>
  <div>
    <button @click="showComponent = true">Show Component</button>
    <component v-if="showComponent" :is="LazyComponent" />
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue'

const showComponent = ref(false)
const LazyComponent = defineAsyncComponent(() => import('./HeavyComponent.vue'))
</script>

<!-- 虚拟滚动 -->
<template>
  <VirtualList
    :data-key="'id'"
    :data-sources="items"
    :data-component="ItemComponent"
    :estimate-size="50"
  />
</template>
```

---

## 二、Svelte 最佳实践

### 2.1 项目结构

**推荐结构：**

```
src/
├── assets/            # 静态资源
├── components/        # 组件
├── stores/            # 状态管理
├── utils/             # 工具函数
├── services/          # API服务
├── routes/            # 路由（SvelteKit）
├── lib/               # 通用库
├── App.svelte         # 根组件
└── main.js            # 入口文件
```

**命名规范：**
- 组件：PascalCase（UserProfile.svelte）
- 文件夹：kebab-case（user-profile）
- 变量：camelCase
- 常量：UPPERCASE

---

### 2.2 响应式系统

**最佳实践：**
- 使用 `let` 声明响应式变量
- 利用 `$:` 反应式语句
- 合理使用 `reactive` 和 `readonly`
- 避免不必要的计算

**示例：**

```svelte
<script>
  let count = 0
  let name = 'Svelte'
  
  // 反应式语句
  $: doubled = count * 2
  $: message = `Hello ${name}!`
  $: if (count > 10) {
    console.log('Count is greater than 10')
  }
  
  function increment() {
    count++
  }
</script>

<div>
  <h1>{message}</h1>
  <p>Count: {count}</p>
  <p>Doubled: {doubled}</p>
  <button on:click={increment}>Increment</button>
  <input bind:value={name} placeholder="Enter name" />
</div>
```

---

### 2.3 组件通信

**最佳实践：**
- 使用 props 传递数据
- 使用 events 触发操作
- 使用 context API 共享状态
- 使用 stores 全局状态管理

**示例：**

```svelte
<!-- Parent.svelte -->
<script>
  import Child from './Child.svelte'
  let count = 0
  
  function handleIncrement() {
    count++
  }
</script>

<div>
  <h2>Parent: {count}</h2>
  <Child bind:count on:reset={() => count = 0} />
</div>

<!-- Child.svelte -->
<script>
  export let count
  import { createEventDispatcher } from 'svelte'
  const dispatch = createEventDispatcher()
  
  function reset() {
    dispatch('reset')
  }
</script>

<div>
  <h3>Child: {count}</h3>
  <button on:click={() => count++}>Increment</button>
  <button on:click={reset}>Reset</button>
</div>
```

---

### 2.4 状态管理

**Svelte Stores 最佳实践：**
- 使用 `writable` 可写存储
- 使用 `readable` 只读存储
- 使用 `derived` 派生存储
- 合理使用存储订阅

**示例：**

```javascript
// stores/counter.js
import { writable, derived } from 'svelte/store'

export const count = writable(0)

export const doubled = derived(count, $count => $count * 2)

export const actions = {
  increment: () => count.update(n => n + 1),
  decrement: () => count.update(n => n - 1),
  reset: () => count.set(0)
}

// 使用
<script>
  import { count, doubled, actions } from './stores/counter'
</script>

<div>
  <p>Count: {$count}</p>
  <p>Doubled: {$doubled}</p>
  <button on:click={actions.increment}>Increment</button>
  <button on:click={actions.decrement}>Decrement</button>
  <button on:click={actions.reset}>Reset</button>
</div>
```

---

### 2.5 生命周期

**Svelte 生命周期函数：**
- `onMount`：组件挂载后
- `onDestroy`：组件销毁前
- `beforeUpdate`：更新前
- `afterUpdate`：更新后
- `tick`：下一次更新后

**示例：**

```svelte
<script>
  import { onMount, onDestroy, beforeUpdate, afterUpdate, tick } from 'svelte'
  let count = 0
  let element
  
  onMount(() => {
    console.log('Component mounted')
    const interval = setInterval(() => {
      count++
    }, 1000)
    
    return () => {
      clearInterval(interval)
      console.log('Component cleanup')
    }
  })
  
  beforeUpdate(() => {
    console.log('Before update')
  })
  
  afterUpdate(async () => {
    console.log('After update')
    await tick()
    console.log('After tick')
  })
  
  onDestroy(() => {
    console.log('Component destroyed')
  })
</script>

<div bind:this={element}>
  <p>Count: {count}</p>
</div>
```

---

### 2.6 性能优化

**最佳实践：**
- 使用 `#key` 指令优化列表
- 避免不必要的重渲染
- 合理使用 `$$invalidate`
- 组件懒加载
- 虚拟滚动

**示例：**

```svelte
<!-- #key 指令 -->
{#each items as item (item.id)}
  <div>{item.name}</div>
{/each}

<!-- 组件懒加载 -->
<script>
  import { onMount } from 'svelte'
  let HeavyComponent
  
  onMount(async () => {
    const module = await import('./HeavyComponent.svelte')
    HeavyComponent = module.default
  })
</script>

{#if HeavyComponent}
  <svelte:component this={HeavyComponent} />
{/if}

<!-- 虚拟滚动 -->
<script>
  import VirtualList from 'svelte-virtual-list'
  let items = Array.from({ length: 10000 }, (_, i) => ({ id: i, name: `Item ${i}` }))
</script>

<VirtualList
  items={items}
  let:item
  height={400}
  itemHeight={50}
>
  <div>{item.name}</div>
</VirtualList>
```

---

## 三、Solid.js 最佳实践

### 3.1 项目结构

**推荐结构：**

```
src/
├── assets/            # 静态资源
├── components/        # 组件
├── hooks/             # 自定义钩子
├── stores/            # 状态管理
├── utils/             # 工具函数
├── services/          # API服务
├── routes/            # 路由
├── App.jsx            # 根组件
└── index.jsx          # 入口文件
```

**命名规范：**
- 组件：PascalCase（UserProfile.jsx）
- 文件夹：kebab-case（user-profile）
- 变量：camelCase
- 常量：UPPERCASE
- 钩子：use前缀（useAuth.js）

---

### 3.2 响应式系统

**最佳实践：**
- 使用 `createSignal` 创建响应式状态
- 使用 `createMemo` 缓存计算
- 使用 `createEffect` 副作用
- 合理使用 `batch` 批量更新

**示例：**

```jsx
import { createSignal, createMemo, createEffect, batch } from 'solid-js'

function Counter() {
  const [count, setCount] = createSignal(0)
  const [name, setName] = createSignal('Solid')
  
  // 计算属性
  const doubled = createMemo(() => count() * 2)
  
  // 副作用
  createEffect(() => {
    console.log(`Count changed to: ${count()}`)
  })
  
  const increment = () => {
    setCount(c => c + 1)
  }
  
  const updateBoth = () => {
    batch(() => {
      setCount(c => c + 1)
      setName('Solid.js')
    })
  }
  
  return (
    <div>
      <h1>Hello {name()}</h1>
      <p>Count: {count()}</p>
      <p>Doubled: {doubled()}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={updateBoth}>Update Both</button>
    </div>
  )
}

export default Counter
```

---

### 3.3 组件

**最佳实践：**
- 使用函数组件
- 合理使用 `props`
- 利用 `children` 插槽
- 组件懒加载

**示例：**

```jsx
// Parent.jsx
import Child from './Child'

function Parent() {
  return (
    <div>
      <Child title="Hello">
        <p>This is a slot</p>
      </Child>
    </div>
  )
}

// Child.jsx
function Child(props) {
  return (
    <div>
      <h2>{props.title}</h2>
      {props.children}
    </div>
  )
}

export default Child

// 懒加载
import { lazy } from 'solid-js'

const HeavyComponent = lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <div>
      <HeavyComponent />
    </div>
  )
}
```

---

### 3.4 状态管理

**Solid Stores 最佳实践：**
- 使用 `createStore` 创建状态
- 利用 `produce` 更新状态
- 合理使用选择器
- 模块化状态

**示例：**

```jsx
import { createStore, produce } from 'solid-js/store'

// 创建 store
const [state, setState] = createStore({
  user: null,
  products: [],
  cart: []
})

// 更新状态
const addToCart = (product) => {
  setState('cart', produce(cart => {
    cart.push(product)
  }))
}

const updateUser = (user) => {
  setState('user', user)
}

// 使用
function Cart() {
  return (
    <div>
      <h2>Cart ({state.cart.length} items)</h2>
      {state.cart.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  )
}

export default Cart
```

---

### 3.5 路由

**Solid Router 最佳实践：**
- 动态路由
- 嵌套路由
- 路由守卫
- 懒加载

**示例：**

```jsx
import { render } from 'solid-js/web'
import { Router, Routes, Route, Link, useParams, useNavigate } from '@solidjs/router'

function Home() {
  return <h1>Home</h1>
}

function About() {
  return <h1>About</h1>
}

function User() {
  const params = useParams()
  return <h1>User: {params.id}</h1>
}

function App() {
  const navigate = useNavigate()
  
  return (
    <Router>
      <nav>
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Link href="/user/1">User 1</Link>
        <button onClick={() => navigate('/')}>Go Home</button>
      </nav>
      <Routes>
        <Route path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/user/:id" component={User} />
      </Routes>
    </Router>
  )
}

render(() => <App />, document.getElementById('root'))
```

---

## 四、前端框架通用最佳实践

### 4.1 代码组织

**最佳实践：**
- 模块化组织代码
- 合理使用文件夹结构
- 统一命名规范
- 代码拆分和懒加载
- 避免代码重复

**示例：**

```
// 好的组织方式
components/
├── Button/           # 按钮组件
│   ├── Button.jsx
│   ├── Button.css
│   └── index.js
├── Card/             # 卡片组件
│   ├── Card.jsx
│   ├── Card.css
│   └── index.js
└── index.js          # 导出所有组件

// 统一导出
export { default as Button } from './Button'
export { default as Card } from './Card'

// 使用
import { Button, Card } from '@/components'
```

---

### 4.2 性能优化

**通用最佳实践：**
- 组件懒加载
- 虚拟滚动
- 防抖和节流
- 缓存计算结果
- 减少不必要的渲染
- 优化图片加载

**示例：**

```javascript
// 防抖
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 节流
function throttle(func, limit) {
  let inThrottle
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// 图片懒加载
const LazyImage = ({ src, alt }) => {
  const [loaded, setLoaded] = useState(false)
  
  return (
    <div style={{ position: 'relative', width: '100%', paddingBottom: '56.25%' }}>
      {!loaded && <div style={{ position: 'absolute', inset: 0, backgroundColor: '#f0f0f0' }} />}
      <img
        src={src}
        alt={alt}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          opacity: loaded ? 1 : 0,
          transition: 'opacity 0.3s'
        }}
        onLoad={() => setLoaded(true)}
      />
    </div>
  )
}
```

---

### 4.3 可访问性

**最佳实践：**
- 使用语义化 HTML
- 提供 alt 文本
- 键盘导航支持
- 适当的颜色对比度
- 屏幕阅读器支持
- ARIA 标签

**示例：**

```jsx
// 语义化 HTML
function Navbar() {
  return (
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  )
}

// 表单可访问性
function LoginForm() {
  return (
    <form>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" aria-required="true" />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" aria-required="true" />
      </div>
      <button type="submit">Login</button>
    </form>
  )
}

// ARIA 标签
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null
  
  return (
    <div 
      role="dialog" 
      aria-modal="true" 
      aria-labelledby="modal-title"
      style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)' }}
    >
      <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: 'white', padding: '20px' }}>
        <h2 id="modal-title">Modal Title</h2>
        {children}
        <button onClick={onClose} aria-label="Close modal">Close</button>
      </div>
    </div>
  )
}
```

---

### 4.4 国际化

**最佳实践：**
- 使用 i18n 库
- 分离翻译文件
- 支持 RTL 语言
- 日期和时间本地化
- 数字和货币本地化

**示例：**

```javascript
// 使用 i18next
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  en: {
    translation: {
      welcome: 'Welcome',
      about: 'About',
      contact: 'Contact'
    }
  },
  zh: {
    translation: {
      welcome: '欢迎',
      about: '关于',
      contact: '联系我们'
    }
  }
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })

// 使用
import { useTranslation } from 'react-i18next'

function Header() {
  const { t, i18n } = useTranslation()
  
  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng)
  }
  
  return (
    <header>
      <h1>{t('welcome')}</h1>
      <nav>
        <a href="/">{t('welcome')}</a>
        <a href="/about">{t('about')}</a>
        <a href="/contact">{t('contact')}</a>
      </nav>
      <div>
        <button onClick={() => changeLanguage('en')}>English</button>
        <button onClick={() => changeLanguage('zh')}>中文</button>
      </div>
    </header>
  )
}
```

---

### 4.5 测试

**最佳实践：**
- 单元测试
- 集成测试
- E2E 测试
- 测试覆盖率
- 自动化测试

**示例：**

```javascript
// React 测试 (Jest + React Testing Library)
import { render, screen, fireEvent } from '@testing-library/react'
import Counter from './Counter'

test('renders counter component', () => {
  render(<Counter />)
  expect(screen.getByText(/Count:/)).toBeInTheDocument()
})

test('increments counter when button is clicked', () => {
  render(<Counter />)
  const incrementButton = screen.getByText('Increment')
  const countElement = screen.getByText(/Count:/)
  
  fireEvent.click(incrementButton)
  expect(countElement).toHaveTextContent('Count: 1')
})

// Vue 测试 (Vitest)
import { mount } from '@vue/test-utils'
import Counter from './Counter.vue'

test('renders counter component', () => {
  const wrapper = mount(Counter)
  expect(wrapper.text()).toContain('Count: 0')
})

test('increments counter when button is clicked', async () => {
  const wrapper = mount(Counter)
  const button = wrapper.find('button')
  
  await button.trigger('click')
  expect(wrapper.text()).toContain('Count: 1')
})
```

---

## 五、最佳实践总结

1. **项目结构**：清晰的目录结构和命名规范
2. **响应式系统**：合理使用框架的响应式特性
3. **组件设计**：可复用、可维护的组件
4. **状态管理**：选择合适的状态管理方案
5. **路由**：合理的路由设计和守卫
6. **性能优化**：懒加载、虚拟滚动、缓存等
7. **可访问性**：语义化 HTML、键盘导航等
8. **国际化**：支持多语言
9. **测试**：单元测试、集成测试
10. **代码质量**：代码规范、注释、文档

---

## 相关资源

- [Vue 3 官方文档](https://vuejs.org/guide/introduction.html)
- [Svelte 官方文档](https://svelte.dev/docs)
- [Solid.js 官方文档](https://www.solidjs.com/docs/latest)
- [Vue Router 官方文档](https://router.vuejs.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Solid Router 官方文档](https://github.com/solidjs/solid-router)
- [i18next 官方文档](https://www.i18next.com/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest 官方文档](https://vitest.dev/)

