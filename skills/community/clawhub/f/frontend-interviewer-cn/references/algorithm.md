# 前端算法高频题

## 初级

### 1. 手写防抖（debounce）和节流（throttle）

**考察点**：闭包、定时器、性能优化

```js
// 防抖：最后一次触发后 delay ms 执行
function debounce(fn, delay) {
  let timer = null
  return function (...args) {
    clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 节流：每 interval ms 最多执行一次
function throttle(fn, interval) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= interval) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

// 使用场景
const onSearch = debounce((val) => fetchSearch(val), 300)  // 搜索输入
const onScroll = throttle(() => checkPosition(), 100)       // 滚动监听
```

---

### 2. 数组去重（多种方式）

**考察点**：数据结构、ES6

```js
const arr = [1, 2, 2, 3, 3, 4]

// 方式1：Set（最简洁）
const unique1 = [...new Set(arr)]

// 方式2：filter + indexOf
const unique2 = arr.filter((v, i) => arr.indexOf(v) === i)

// 方式3：reduce
const unique3 = arr.reduce((acc, v) => acc.includes(v) ? acc : [...acc, v], [])

// 对象数组按属性去重
const users = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }, { id: 1, name: 'A' }]
const uniqueUsers = [...new Map(users.map(u => [u.id, u])).values()]
```

---

### 3. 手写深拷贝

**考察点**：递归、数据类型判断

```js
function deepClone(target, map = new WeakMap()) {
  // 处理基本类型和 null
  if (target === null || typeof target !== 'object') return target
  
  // 处理循环引用
  if (map.has(target)) return map.get(target)
  
  // 处理特殊对象
  if (target instanceof Date) return new Date(target)
  if (target instanceof RegExp) return new RegExp(target)
  
  // 处理数组和普通对象
  const clone = Array.isArray(target) ? [] : {}
  map.set(target, clone)
  
  for (const key of Reflect.ownKeys(target)) {
    clone[key] = deepClone(target[key], map)
  }
  return clone
}

// 测试循环引用
const obj = { a: 1, b: { c: 2 } }
obj.self = obj
const cloned = deepClone(obj)  // 不会栈溢出
```

---

## 中级

### 4. 实现 LRU 缓存

**考察点**：Map、数据结构设计

```js
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity
    this.cache = new Map()  // Map 保持插入顺序
  }

  get(key) {
    if (!this.cache.has(key)) return -1
    // 移到最近使用：删除再重新插入
    const val = this.cache.get(key)
    this.cache.delete(key)
    this.cache.set(key, val)
    return val
  }

  put(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key)
    } else if (this.cache.size >= this.capacity) {
      // 删除最久未使用（Map 第一个元素）
      this.cache.delete(this.cache.keys().next().value)
    }
    this.cache.set(key, value)
  }
}

// 测试
const lru = new LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
lru.get(1)    // 1，1 变为最近使用
lru.put(3, 3) // 淘汰 2
lru.get(2)    // -1，已淘汰
```

---

### 5. 手写 Promise.all 和 Promise.race

**考察点**：Promise、异步编程

```js
// Promise.all：全部成功才 resolve，任一失败就 reject
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = []
    let count = 0
    if (promises.length === 0) return resolve([])
    
    promises.forEach((p, i) => {
      Promise.resolve(p).then(val => {
        results[i] = val
        if (++count === promises.length) resolve(results)
      }).catch(reject)
    })
  })
}

// Promise.race：第一个完成（无论成功失败）就结束
function promiseRace(promises) {
  return new Promise((resolve, reject) => {
    promises.forEach(p => Promise.resolve(p).then(resolve).catch(reject))
  })
}

// Promise.allSettled：等全部完成，无论成败
function promiseAllSettled(promises) {
  return Promise.all(promises.map(p =>
    Promise.resolve(p)
      .then(value => ({ status: 'fulfilled', value }))
      .catch(reason => ({ status: 'rejected', reason }))
  ))
}
```

---

## 高级

### 6. 二叉树遍历（递归 + 迭代）

**考察点**：树、递归、栈

```js
// 前序遍历：根-左-右
function preorder(root) {
  if (!root) return []
  // 递归
  return [root.val, ...preorder(root.left), ...preorder(root.right)]
  
  // 迭代
  const res = [], stack = [root]
  while (stack.length) {
    const node = stack.pop()
    res.push(node.val)
    if (node.right) stack.push(node.right) // 先压右
    if (node.left) stack.push(node.left)   // 再压左
  }
  return res
}

// 层序遍历（BFS）
function levelOrder(root) {
  if (!root) return []
  const res = [], queue = [root]
  while (queue.length) {
    const level = []
    const size = queue.length
    for (let i = 0; i < size; i++) {
      const node = queue.shift()
      level.push(node.val)
      if (node.left) queue.push(node.left)
      if (node.right) queue.push(node.right)
    }
    res.push(level)
  }
  return res
}
```

---

### 7. 实现函数柯里化（curry）

**考察点**：闭包、函数式编程

```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args)
    }
    return function (...args2) {
      return curried.apply(this, args.concat(args2))
    }
  }
}

// 使用
const add = curry((a, b, c) => a + b + c)
add(1)(2)(3)   // 6
add(1, 2)(3)   // 6
add(1)(2, 3)   // 6

// 无限柯里化（累加）
function infiniteCurry(fn) {
  const args = []
  return function inner(...newArgs) {
    if (newArgs.length === 0) return fn(...args)
    args.push(...newArgs)
    return inner
  }
}

const sum = infiniteCurry((...args) => args.reduce((a, b) => a + b, 0))
sum(1)(2)(3)() // 6
```

---

### 8. 实现 EventEmitter（发布订阅）

**考察点**：设计模式、事件系统

```js
class EventEmitter {
  constructor() {
    this.events = {}
  }

  on(event, listener) {
    if (!this.events[event]) this.events[event] = []
    this.events[event].push(listener)
    return this
  }

  once(event, listener) {
    const wrapper = (...args) => {
      listener(...args)
      this.off(event, wrapper)
    }
    wrapper._original = listener
    return this.on(event, wrapper)
  }

  emit(event, ...args) {
    const listeners = this.events[event] || []
    listeners.slice().forEach(fn => fn(...args))
    return this
  }

  off(event, listener) {
    if (!this.events[event]) return this
    this.events[event] = this.events[event].filter(
      fn => fn !== listener && fn._original !== listener
    )
    return this
  }
}

// 使用
const emitter = new EventEmitter()
emitter.on('data', (d) => console.log('received:', d))
emitter.once('connect', () => console.log('connected!'))
emitter.emit('data', { id: 1 })
emitter.emit('connect') // 触发一次后自动移除
```
