# 浏览器原理面试题库

## 初级

### 题目1：简述浏览器渲染流程
**考察点：** 关键渲染路径、DOM/CSSOM 构建、渲染树

**参考答案：**
浏览器渲染流程（关键渲染路径）：

1. **解析 HTML** → 构建 DOM 树
2. **解析 CSS** → 构建 CSSOM 树
3. **合并** DOM + CSSOM → 渲染树（Render Tree，只含可见节点）
4. **布局（Layout/Reflow）**：计算每个节点的几何信息（位置、尺寸）
5. **绘制（Paint）**：将节点绘制成像素
6. **合成（Composite）**：将多个图层合并输出到屏幕

```
HTML → DOM
             ↘
              Render Tree → Layout → Paint → Composite
             ↗
CSS  → CSSOM
```

优化建议：
- 将 CSS 放在 `<head>`，JS 放在 `</body>` 前（或加 `defer`/`async`）
- 避免 JS 阻塞解析（`defer` 异步加载，不阻塞，按顺序执行）

---

### 题目2：什么是重排（Reflow）和重绘（Repaint）？如何减少？
**考察点：** 触发条件、性能影响、优化手段

**参考答案：**
- **重排（Reflow）**：元素的几何属性变化，需重新计算布局，代价高
- **重绘（Repaint）**：外观变化但不影响布局（如颜色），代价低
- **重排一定触发重绘，重绘不一定重排**

触发重排的操作：
```javascript
// 读取布局属性会强制同步布局（强制重排）
const h = element.offsetHeight;   // 读
element.style.height = h + 'px';  // 写 → 重排

// 优化：批量读，批量写
const h1 = el1.offsetHeight;
const h2 = el2.offsetHeight;      // 先全部读
el1.style.height = h1 + 'px';
el2.style.height = h2 + 'px';    // 再全部写
```

减少重排的方法：
```javascript
// 1. 使用 DocumentFragment 批量操作 DOM
const frag = document.createDocumentFragment();
items.forEach(item => frag.appendChild(createEl(item)));
container.appendChild(frag);

// 2. 使用 CSS transform 代替 top/left（不触发重排）
el.style.transform = 'translateX(100px)'; // ✅
el.style.left = '100px';                  // ❌
```

---

### 题目3：什么是事件循环（Event Loop）？宏任务和微任务的区别？
**考察点：** 调用栈、任务队列、执行顺序

**参考答案：**
JS 是单线程的，通过事件循环处理异步任务。

执行顺序：同步代码 → 微任务队列（全部清空）→ 宏任务（一个）→ 微任务 → 宏任务 ...

- **宏任务（MacroTask）**：`setTimeout`、`setInterval`、I/O、UI渲染
- **微任务（MicroTask）**：`Promise.then`、`queueMicrotask`、`MutationObserver`

```javascript
console.log('1');                     // 同步

setTimeout(() => console.log('2'));   // 宏任务

Promise.resolve().then(() => {
  console.log('3');                   // 微任务
  Promise.resolve().then(() => console.log('4')); // 微任务
});

console.log('5');                     // 同步

// 输出顺序：1 → 5 → 3 → 4 → 2
```

---

## 中级

### 题目4：V8 垃圾回收机制是什么？分代回收如何工作？
**考察点：** 新生代/老生代、Scavenge、Mark-Sweep、内存泄漏

**参考答案：**
V8 使用**分代垃圾回收**，将堆内存分为新生代和老生代：

**新生代（Young Generation）**：存放短命对象，空间小（约1-8MB）
- 使用 **Scavenge 算法**（复制算法）：将存活对象复制到另一半空间，效率高

**老生代（Old Generation）**：存放长命对象，空间大
- 使用 **Mark-Sweep（标记清除）**：标记可达对象，清除未标记的
- 使用 **Mark-Compact（标记整理）**：整理碎片

**晋升条件**：新生代对象经历 2 次 Scavenge 后晋升到老生代

```javascript
// 常见内存泄漏场景
// 1. 意外全局变量
function leak() {
  leakedVar = 'I am global'; // 忘写 let/const/var
}

// 2. 未清除的定时器
const timer = setInterval(() => { /* ... */ }, 1000);
// 记得 clearInterval(timer)

// 3. 闭包引用大对象
function createLeak() {
  const bigData = new Array(1e6).fill('*');
  return () => bigData[0]; // bigData 无法被回收
}
```

---

### 题目5：`requestAnimationFrame` 和 `setTimeout` 在动画中的区别？
**考察点：** 渲染时机、掉帧、性能

**参考答案：**
```javascript
// setTimeout：不精确，可能在一帧内多次触发或跳帧
let pos = 0;
function animate() {
  pos += 2;
  el.style.left = pos + 'px';
  setTimeout(animate, 16); // ❌ 16ms 不精确
}

// requestAnimationFrame：与浏览器刷新率同步（通常60fps=16.7ms）
function animate(timestamp) {
  pos += 2;
  el.style.transform = `translateX(${pos}px)`;
  requestAnimationFrame(animate); // ✅ 下一帧执行
}
requestAnimationFrame(animate);

// 取消动画
const rafId = requestAnimationFrame(animate);
cancelAnimationFrame(rafId);
```

`rAF` 优势：
- 浏览器隐藏标签页时自动暂停，节省资源
- 在每帧渲染前执行，避免丢帧
- 与显示器刷新率同步

---

### 题目6：Web Workers 是什么？如何与主线程通信？
**考察点：** 多线程、postMessage、使用场景

**参考答案：**
Web Workers 让 JS 在**独立线程**中运行，不阻塞主线程（UI线程）。

```javascript
// main.js - 主线程
const worker = new Worker('worker.js');

// 向 Worker 发消息
worker.postMessage({ data: largeArray, type: 'SORT' });

// 接收 Worker 消息
worker.onmessage = (e) => {
  console.log('排序结果:', e.data);
};

// 错误处理
worker.onerror = (err) => console.error(err);

// 终止 Worker
worker.terminate();
```

```javascript
// worker.js - Worker 线程
self.onmessage = (e) => {
  const { data, type } = e.data;
  if (type === 'SORT') {
    const sorted = data.sort((a, b) => a - b); // 耗时操作
    self.postMessage(sorted); // 返回结果
  }
};
```

**限制：** 无法访问 DOM、`window`、`document`；可使用 `fetch`、`XMLHttpRequest`、`IndexedDB`。

---

## 高级

### 题目7：浏览器的合成层（Compositing Layer）是什么？如何利用 GPU 加速？
**考察点：** 图层提升、will-change、避免过度使用

**参考答案：**
浏览器会将部分元素提升为独立的合成层，由 GPU 合成，跳过 Layout 和 Paint，性能极高。

触发合成层的条件：
- `transform: translateZ(0)` 或 `translate3d`
- `will-change: transform`（现代推荐方式）
- `opacity < 1`（配合 transition）
- `video`、`canvas`、`iframe`

```css
/* 触发 GPU 加速 */
.animated-element {
  will-change: transform; /* 提前声明，浏览器预优化 */
}

/* 不推荐的 hack */
.old-hack {
  transform: translateZ(0); /* 曾经的方法，现在用 will-change */
}

/* 动画完成后移除，避免内存占用 */
```
```javascript
el.addEventListener('animationend', () => {
  el.style.willChange = 'auto'; // 释放合成层
});
```

**注意：** 合成层占用显存，过多会导致内存压力，不要滥用。

---

### 题目8：详细描述从输入 URL 到页面显示的完整过程
**考察点：** 网络请求、DNS、TCP、渲染、完整链路

**参考答案：**
1. **URL 解析**：解析协议、域名、路径
2. **DNS 查询**：本地缓存 → 系统缓存 → DNS 服务器 → 根域名服务器
3. **TCP 连接**：三次握手建立连接（HTTPS 还有 TLS 握手）
4. **发送 HTTP 请求**：请求头/体
5. **服务器响应**：返回 HTML
6. **浏览器解析渲染**：DOM → CSSOM → Render Tree → Layout → Paint → Composite
7. **加载子资源**：CSS、JS、图片（并行加载）
8. **JS 执行**：可能修改 DOM，触发重排重绘
9. **DOMContentLoaded**：DOM 解析完成
10. **load 事件**：所有资源加载完成

```javascript
// 性能监控关键时间点
performance.timing.domContentLoadedEventEnd
  - performance.timing.navigationStart; // DCL 时间

window.addEventListener('load', () => {
  const [entry] = performance.getEntriesByType('navigation');
  console.log('Total load time:', entry.loadEventEnd);
});
```

---

### 题目9：浏览器缓存策略（强缓存 vs 协商缓存）详解
**考察点：** Cache-Control、ETag、Last-Modified、缓存决策流程

**参考答案：**
```
请求资源
  ↓
有缓存？
  ├── 否 → 发请求 → 缓存响应
  └── 是 → 强缓存是否过期？
              ├── 未过期 → 直接用缓存（200 from cache）
              └── 过期 → 发协商请求（带 ETag/Last-Modified）
                          ├── 资源未变 → 304 Not Modified，用缓存
                          └── 资源已变 → 200，返回新资源
```

```http
# 强缓存：不请求服务器
Cache-Control: max-age=31536000, immutable   # 1年
Expires: Wed, 21 Oct 2026 07:28:00 GMT       # 旧方式

# 协商缓存：请求服务器验证
ETag: "abc123"                              # 内容哈希
Last-Modified: Tue, 22 Feb 2022 22:00:00 GMT

# 请求头（协商）
If-None-Match: "abc123"
If-Modified-Since: Tue, 22 Feb 2022 22:00:00 GMT
```

最佳实践：
- HTML：`no-cache`（每次协商）
- CSS/JS：`max-age=1年` + 文件名加 hash（如 `app.3f8a2b.js`）
- 图片：`max-age=1周` 或更长
