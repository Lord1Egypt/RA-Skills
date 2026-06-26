# JavaScript 核心面试题库

## 目录
- [初级题目](#初级)
- [中级题目](#中级)
- [高级题目](#高级)
- [专家题目](#专家)
- [代码手写题](#代码手写题)

---

## 初级

### JS-J-01 什么是闭包？
**难度：** 初级  
**考察点：** 作用域、词法环境

**标准答案要点：**
- 闭包是函数与其词法作用域（Lexical Environment）的组合
- 内部函数可以访问外部函数的变量，即使外部函数已经执行完毕
- 经典应用：数据私有化、函数工厂、防抖节流

**代码示例：**
```javascript
function counter() {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}
const c = counter();
c.increment(); // 1
c.increment(); // 2
```

**追问：**
1. 闭包可能导致什么问题？如何避免？（内存泄漏：变量无法被 GC，循环中使用 let 替代 var）
2. `for` 循环中 `var` 和 `let` 的闭包行为差异？

---

### JS-J-02 `==` 和 `===` 的区别
**难度：** 初级  
**考察点：** 类型转换、隐式强制转换

**标准答案要点：**
- `===` 严格相等：不进行类型转换，类型和值都必须相同
- `==` 宽松相等：会进行类型强制转换（ToNumber、ToPrimitive）
- 典型陷阱：`null == undefined` 为 `true`，`null === undefined` 为 `false`

**追问：** `[] == false` 为什么是 `true`？（ToPrimitive → "" → 0，Boolean → 0，0 == 0）

---

### JS-J-03 `var`、`let`、`const` 的区别
**难度：** 初级  
**考察点：** 变量声明、作用域、提升

| 特性 | var | let | const |
|------|-----|-----|-------|
| 作用域 | 函数作用域 | 块作用域 | 块作用域 |
| 变量提升 | 提升（undefined） | 存在但 TDZ | 存在但 TDZ |
| 重复声明 | 允许 | 不允许 | 不允许 |
| 重新赋值 | 允许 | 允许 | 不允许 |
| 挂载到 window | 是 | 否 | 否 |

**TDZ（Temporal Dead Zone）：** let/const 声明前访问会抛出 `ReferenceError`

---

### JS-J-04 什么是事件冒泡和事件捕获？
**难度：** 初级  
**考察点：** 事件模型、DOM

**标准答案要点：**
- **捕获阶段**：事件从 window → document → ... → 目标元素
- **目标阶段**：事件到达目标元素
- **冒泡阶段**：事件从目标元素 → ... → window
- `addEventListener` 第三个参数 `true` 为捕获，`false`（默认）为冒泡
- `stopPropagation()` 阻止传播；`stopImmediatePropagation()` 还阻止同元素其他监听器
- `preventDefault()` 阻止默认行为

**追问：** 事件委托的原理和优势？（利用冒泡，减少事件绑定数量，动态元素也适用）

---

## 中级

### JS-M-01 详解 JavaScript 事件循环（Event Loop）
**难度：** 中级  
**考察点：** 异步机制、宏任务/微任务

**标准答案要点：**

执行顺序：
1. 同步代码（Call Stack）
2. 清空微任务队列（Microtask Queue）：`Promise.then`、`MutationObserver`、`queueMicrotask`
3. 取一个宏任务（Macrotask/Task Queue）：`setTimeout`、`setInterval`、`I/O`、`MessageChannel`
4. 重复 2-3

```javascript
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
// 输出：1 4 3 2
```

**追问：**
1. `queueMicrotask` vs `Promise.resolve().then` 的区别？（功能相同，queueMicrotask 更语义化）
2. Node.js 中的 `process.nextTick` 和 Promise 的优先级？（nextTick 优先）
3. `requestAnimationFrame` 属于宏任务还是微任务？（宏任务，在下一帧渲染前执行）

---

### JS-M-02 Promise 深度解析
**难度：** 中级  
**考察点：** 异步编程、错误处理

**核心知识点：**
- Promise 的三种状态：Pending → Fulfilled / Rejected（不可逆）
- `.then()` 返回新的 Promise，支持链式调用
- `.catch()` 等价于 `.then(null, rejection)`
- Promise 错误不被捕获不会崩溃（静默失败），但现代浏览器会在 console 报 `UnhandledPromiseRejection`

**Promise.xxx 对比：**
```javascript
// Promise.all - 全部成功才成功，一个失败立即失败
Promise.all([p1, p2, p3])

// Promise.allSettled - 等所有完成，返回每个结果（含状态）
Promise.allSettled([p1, p2, p3])

// Promise.race - 第一个完成（无论成败）
Promise.race([p1, p2, p3])

// Promise.any - 第一个成功；全部失败才失败（AggregateError）
Promise.any([p1, p2, p3])
```

**手写 Promise（面试高频）：**
```javascript
class MyPromise {
  constructor(executor) {
    this.state = 'pending';
    this.value = undefined;
    this.callbacks = [];
    
    const resolve = (value) => {
      if (this.state !== 'pending') return;
      this.state = 'fulfilled';
      this.value = value;
      this.callbacks.forEach(cb => cb.onFulfilled(value));
    };
    
    const reject = (reason) => {
      if (this.state !== 'pending') return;
      this.state = 'rejected';
      this.value = reason;
      this.callbacks.forEach(cb => cb.onRejected(reason));
    };
    
    try {
      executor(resolve, reject);
    } catch (e) {
      reject(e);
    }
  }
  
  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handle = (fn, value) => {
        try {
          const result = fn ? fn(value) : value;
          result instanceof MyPromise ? result.then(resolve, reject) : resolve(result);
        } catch (e) {
          reject(e);
        }
      };
      
      if (this.state === 'fulfilled') handle(onFulfilled, this.value);
      else if (this.state === 'rejected') handle(onRejected, this.value);
      else this.callbacks.push({
        onFulfilled: v => handle(onFulfilled, v),
        onRejected: r => handle(onRejected, r)
      });
    });
  }
}
```

---

### JS-M-03 原型链与继承
**难度：** 中级  
**考察点：** OOP、原型机制

**核心要点：**
- 每个对象有 `[[Prototype]]`（通过 `__proto__` 访问，或 `Object.getPrototypeOf()`）
- 函数有 `prototype` 属性，`new` 操作时赋值给实例的 `[[Prototype]]`
- 原型链终止于 `Object.prototype.__proto__ === null`

```javascript
function Animal(name) { this.name = name; }
Animal.prototype.speak = function() { return `${this.name} speaks`; };

function Dog(name) { Animal.call(this, name); }
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.bark = function() { return 'Woof!'; };

const d = new Dog('Rex');
d instanceof Dog;    // true
d instanceof Animal; // true
```

**`new` 操作符的步骤：**
1. 创建空对象
2. 设置 `__proto__` = 构造函数的 `prototype`
3. 执行构造函数（`this` 指向新对象）
4. 若构造函数返回对象，则返回该对象；否则返回新对象

**追问：** `class` 语法糖与原型继承的本质关系？（class 本质是基于原型的语法糖，`extends` 会设置原型链）

---

### JS-M-04 `this` 指向详解
**难度：** 中级  
**考察点：** 执行上下文

| 场景 | this 指向 |
|------|----------|
| 全局函数调用 | `window`（严格模式为 `undefined`） |
| 方法调用 | 调用该方法的对象 |
| `new` 调用 | 新创建的对象 |
| `call/apply/bind` | 第一个参数指定的对象 |
| 箭头函数 | 词法作用域（外层 this） |
| 事件处理器 | 绑定元素（除非箭头函数） |

**常见陷阱：**
```javascript
const obj = {
  name: 'test',
  greet: function() {
    setTimeout(function() {
      console.log(this.name); // undefined (this = window)
    }, 0);
    setTimeout(() => {
      console.log(this.name); // 'test' (箭头函数捕获外层 this)
    }, 0);
  }
};
```

---

## 高级

### JS-S-01 JavaScript 内存管理与垃圾回收
**难度：** 高级  
**考察点：** 运行时、性能

**V8 内存结构：**
- **新生代（Young Generation）**：存活时间短的对象，使用 Scavenge 算法（Semi-Space），From/To 区交替
- **老生代（Old Generation）**：存活时间长的对象，使用标记-清除（Mark-Sweep）+ 标记-整理（Mark-Compact）
- **大对象空间**：单独管理，不进入正常 GC 流程

**常见内存泄漏场景：**
1. 意外的全局变量（未声明变量）
2. 未清理的定时器 / 事件监听器
3. 闭包持有大量数据
4. 已移除 DOM 节点的引用仍在 JS 中

**WeakMap/WeakSet 的价值：** 弱引用不阻止 GC，适合缓存 DOM 节点引用

---

### JS-S-02 ES6+ 高级特性深度解析
**难度：** 高级

**Generator 函数：**
```javascript
function* idGenerator() {
  let id = 1;
  while (true) yield id++;
}

// 协程实现异步（co 库原理）
function* fetchUser(id) {
  const user = yield fetch(`/user/${id}`);
  const posts = yield fetch(`/posts?userId=${user.id}`);
  return posts;
}
```

**Proxy 与 Reflect：**
```javascript
const handler = {
  get(target, prop, receiver) {
    console.log(`Getting ${prop}`);
    return Reflect.get(target, prop, receiver);
  },
  set(target, prop, value, receiver) {
    console.log(`Setting ${prop} = ${value}`);
    return Reflect.set(target, prop, value, receiver);
  }
};
const p = new Proxy({}, handler);
// Vue 3 响应式系统的核心基础
```

---

## 专家

### JS-E-01 JavaScript 引擎优化
**难度：** 专家  
**考察点：** JIT 编译、性能优化

**V8 优化关键：**
- **隐藏类（Hidden Classes）**：V8 为相同属性顺序的对象创建相同 Hidden Class，实现属性访问优化
- **内联缓存（Inline Cache）**：缓存属性访问的位置信息，避免重复查找
- **JIT 编译**：热点代码由 Ignition（解释器）→ Turbofan（优化编译器）

**反优化（Deoptimization）触发条件：**
- 对象属性动态增减（破坏 Hidden Class）
- 函数参数类型变化（影响 IC）
- `arguments` 对象使用
- `try-catch` 内的代码（部分情况）

**追问：** 如何通过 Chrome DevTools 检测 V8 反优化？（`--trace-deopt` 或 Performance 面板）

---

## 代码手写题

### 防抖（Debounce）
```javascript
function debounce(fn, delay, immediate = false) {
  let timer = null;
  return function(...args) {
    const callNow = immediate && !timer;
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (!immediate) fn.apply(this, args);
    }, delay);
    if (callNow) fn.apply(this, args);
  };
}
```

### 节流（Throttle）
```javascript
function throttle(fn, interval) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
}
```

### 深拷贝（Deep Clone）
```javascript
function deepClone(obj, map = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (map.has(obj)) return map.get(obj); // 处理循环引用
  
  const clone = Array.isArray(obj) ? [] : {};
  map.set(obj, clone);
  
  for (const key of Reflect.ownKeys(obj)) {
    clone[key] = deepClone(obj[key], map);
  }
  return clone;
}
```

### 柯里化（Curry）
```javascript
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}
```

### 发布订阅（EventEmitter）
```javascript
class EventEmitter {
  constructor() { this.events = {}; }
  
  on(event, fn) {
    (this.events[event] ??= []).push(fn);
    return this;
  }
  
  once(event, fn) {
    const wrapper = (...args) => { fn(...args); this.off(event, wrapper); };
    return this.on(event, wrapper);
  }
  
  emit(event, ...args) {
    this.events[event]?.forEach(fn => fn(...args));
    return this;
  }
  
  off(event, fn) {
    this.events[event] = this.events[event]?.filter(f => f !== fn);
    return this;
  }
}
```
