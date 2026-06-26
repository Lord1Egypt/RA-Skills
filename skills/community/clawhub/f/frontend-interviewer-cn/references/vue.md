# Vue 深度面试题库

## 目录
- [初级](#初级)
- [中级](#中级)
- [高级](#高级)
- [专家](#专家)

---

## 初级

### V-J-01 Vue 2 vs Vue 3 核心区别
**难度：** 初级

| 特性 | Vue 2 | Vue 3 |
|------|-------|-------|
| 响应式 | `Object.defineProperty` | `Proxy` |
| API 风格 | Options API | Composition API（兼容 Options） |
| 根节点 | 单根节点 | 多根节点（Fragment） |
| 生命周期 | `beforeCreate/created/...` | `setup()` 替代前两者 |
| TypeScript | 二等公民 | 一等公民 |
| 性能 | — | 更快的渲染，更小的包体积 |
| Tree Shaking | 有限 | 完全支持 |

---

### V-J-02 v-show vs v-if
**难度：** 初级

- `v-if`：条件为 false 时，完全不渲染 DOM，有销毁/重建开销
- `v-show`：始终渲染，通过 `display: none` 切换，切换开销低
- **选择**：频繁切换用 v-show；初始条件不可能为真用 v-if

---

## 中级

### V-M-01 Vue 3 响应式原理深度解析
**难度：** 中级/高级  
**考察点：** Proxy、依赖收集

**核心：基于 Proxy + Reflect**

```javascript
// 简化版响应式实现
function reactive(obj) {
  return new Proxy(obj, {
    get(target, key, receiver) {
      track(target, key);  // 依赖收集
      const res = Reflect.get(target, key, receiver);
      // 深度响应式
      return typeof res === 'object' ? reactive(res) : res;
    },
    set(target, key, value, receiver) {
      const res = Reflect.set(target, key, value, receiver);
      trigger(target, key);  // 触发更新
      return res;
    },
    deleteProperty(target, key) {
      const res = Reflect.deleteProperty(target, key);
      trigger(target, key);
      return res;
    }
  });
}

// 依赖收集核心
const targetMap = new WeakMap();
let activeEffect = null;

function track(target, key) {
  if (!activeEffect) return;
  let depsMap = targetMap.get(target);
  if (!depsMap) targetMap.set(target, depsMap = new Map());
  let dep = depsMap.get(key);
  if (!dep) depsMap.set(key, dep = new Set());
  dep.add(activeEffect);
}

function trigger(target, key) {
  const depsMap = targetMap.get(target);
  depsMap?.get(key)?.forEach(effect => effect());
}
```

**Vue 2 响应式的局限（为什么 Vue 3 使用 Proxy）：**
- `Object.defineProperty` 无法检测**新增/删除属性**（需要 `Vue.set/Vue.delete`）
- 无法检测**数组索引修改**和 `length` 变化（Vue 2 对数组方法做了 hack）
- Proxy 可拦截所有操作（包括 `in`、`delete`、迭代等）

---

### V-M-02 Composition API 核心
**难度：** 中级

**`ref` vs `reactive`：**
```javascript
// ref - 包装任意值为响应式，通过 .value 访问
const count = ref(0);
count.value++; // 修改
// 模板中自动解包：{{ count }}（不需要 .value）

// reactive - 对象/数组的深度响应式
const state = reactive({ name: 'Vue', version: 3 });
state.name = 'Vue3'; // 直接修改

// shallowRef / shallowReactive - 浅层响应式（性能优化）
const data = shallowRef({ list: [] });
data.value = { list: [1, 2] }; // 触发更新
data.value.list.push(3);       // 不触发更新

// toRefs - 解构 reactive 时保持响应性
const { name, version } = toRefs(state);
```

**computed 与 watch：**
```javascript
// computed - 有缓存，依赖不变不重算
const doubled = computed(() => count.value * 2);

// watchEffect - 自动追踪依赖
const stop = watchEffect(() => {
  console.log(count.value); // 依赖 count
});
stop(); // 停止监听

// watch - 显式指定依赖，可获取新旧值
watch(
  () => state.name,
  (newVal, oldVal) => { console.log(newVal, oldVal); },
  { immediate: true, deep: true, flush: 'post' }
);
```

---

### V-M-03 虚拟 DOM 与 Diff 算法（Vue 3）
**难度：** 中级/高级

**Vue 3 Diff 优化（相比 Vue 2）：**

1. **静态提升（Static Hoisting）**：静态节点只创建一次，复用 VNode 引用
2. **补丁标志（Patch Flags）**：编译时标记哪些属性是动态的，运行时跳过静态比对
3. **块树（Block Tree）**：将动态节点收集到 Block 的 dynamicChildren 数组，Diff 只对比动态节点
4. **最长递增子序列（LIS）**：用于最小化 DOM 移动操作

```javascript
// 补丁标志示例（编译器生成）
createVNode("div", { class: "container" }, [
  createVNode("span", null, name, PatchFlags.TEXT), // 动态文本
  createVNode("div", { id: dynamicId }, null, PatchFlags.PROPS, ["id"]) // 动态属性
])
```

**Vue 3 Diff 流程（有 key 的列表）：**
1. 头头对比，相同则 patch 并移动指针
2. 尾尾对比，相同则 patch 并移动指针
3. 旧节点遍历完：挂载剩余新节点
4. 新节点遍历完：卸载剩余旧节点
5. 乱序处理：建立 key → index Map，使用 LIS 最小化移动

---

## 高级

### V-S-01 Vue 3 编译器优化原理
**难度：** 高级

**模板编译阶段：**
```
源码模板
  ↓ Parse（解析）
  AST（抽象语法树）
  ↓ Transform（转换/优化）
  优化后 AST（静态分析、提升、Block 收集）
  ↓ Generate（代码生成）
  渲染函数
```

**关键优化：**
- `v-if` 和 `v-for` 创建 Block 节点
- 静态子树提升（`hoistStatic`）
- 事件监听缓存（`cacheHandlers`）

---

### V-S-02 Pinia vs Vuex
**难度：** 高级

| 特性 | Vuex 4 | Pinia |
|------|--------|-------|
| TypeScript | 需要大量类型声明 | 原生支持，自动推导 |
| 模块 | `modules`（嵌套命名空间） | 多个独立 store |
| Mutations | 必须 | 不需要（直接修改 state） |
| DevTools | 支持 | 支持（更好） |
| SSR | 手动处理 | 内置支持 |
| 插件 | store plugins | store plugins |

**Pinia 示例：**
```javascript
// 定义 store
const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const isLoggedIn = computed(() => !!user.value);
  
  async function login(credentials) {
    user.value = await api.login(credentials);
  }
  
  return { user, isLoggedIn, login };
});

// 使用
const userStore = useUserStore();
userStore.login({ ... });
```

---

## 专家

### V-E-01 Vue 3 渲染器与自定义渲染器
**难度：** 专家

```javascript
// 自定义渲染器（平台无关的 Vue 3）
import { createRenderer } from '@vue/runtime-core';

const { createApp } = createRenderer({
  // 创建元素
  createElement(type) { return canvas.createElement(type); },
  // 插入元素
  insert(el, parent, anchor) { parent.insertBefore(el, anchor); },
  // 设置文本
  setElementText(el, text) { el.textContent = text; },
  // 属性 patch
  patchProp(el, key, prevValue, nextValue) {
    el[key] = nextValue;
  },
  // 创建文本节点
  createText(text) { return { type: 'text', text }; },
  // 其他必要操作...
});

// 可以渲染到 Canvas、Native、WebGL 等任意平台
```

**追问：** Vue 3 如何实现跨平台渲染？（运行时核心与平台无关，通过注入平台特定的 DOM 操作实现）
