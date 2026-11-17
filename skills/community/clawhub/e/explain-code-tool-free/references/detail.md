# 详细参考 - explain-code-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (javascript)

```javascript
// 观察者模式实现

class YouTubeChannel {
  constructor(name) {
    this.name = name
    this.subscribers = []  // 订阅者列表
  }

  // 订阅(注册观察者)
  subscribe(observer) {
    this.subscribers.push(observer)
    console.log(`${observer.name} 订阅了 ${this.name}`)
  }

  // 取消订阅
  unsubscribe(observer) {
    this.subscribers = this.subscribers.filter(sub => sub !== observer)
    console.log(`${observer.name} 取消订阅了 ${this.name}`)
  }

  // 发布视频(通知所有观察者)
  publishVideo(title) {
    console.log(`\n${this.name} 发布了新视频: ${title}`)
    this.subscribers.forEach(sub => sub.update(this.name, title))
  }
}

// 观察者(订阅者)
class Subscriber {
  constructor(name) {
    this.name = name
  }

  update(channel, videoTitle) {
    console.log(`  ${this.name} 收到通知: ${channel} 发布了 "${videoTitle}"`)
  }
}

// 使用
const channel = new YouTubeChannel("技术频道")

const alice = new Subscriber("Alice")
const bob = new Subscriber("Bob")

channel.subscribe(alice)  // Alice 订阅了 技术频道
channel.subscribe(bob)    // Bob 订阅了 技术频道

channel.publishVideo("观察者模式教程")
// 技术频道 发布了新视频: 观察者模式教程
//   Alice 收到通知
//   Bob 收到通知

channel.unsubscribe(alice)  // Alice 取消订阅
channel.publishVideo("策略模式教程")
// 只有 Bob 收到通知
```

## 代码示例 ()

```
类比:这个函数像一个有记忆力的助手

- memoize 是一个"包装器",给任何函数加上记忆功能
- 就像你问助手一个问题:
  1. 助手先检查"记忆本"(cache)里有没有记过
  2. 如果有 → 直接告诉你答案(不用重新算)
  3. 如果没有 → 去算一遍,然后记在记忆本里

执行流程:
┌─────────────────────────────────────┐
│ memoize(expensiveFn)                │
│   ↓                                 │
│ 创建空缓存 cache = {}               │
│   ↓                                 │
│ 返回新函数(带记忆的版本)           │
└─────────────────────────────────────┘

调用时:
┌─────────────────────────────────────┐
│ memoizedFn(1, 2)                    │
│   ↓                                 │
│ key = "[1,2]"                       │
│   ↓                                 │
│ key 在 cache 里?                    │
│   ├─ 是 → 返回 cache["[1,2]"]      │
│   └─ 否 → 计算fn(1,2),存入cache   │
└─────────────────────────────────────┘

常见误区:
- 只对纯函数有效(相同输入相同输出)
- 缓存会占用内存,不适合大量不同参数
- JSON.stringify 不处理函数和循环引用
```

## 代码示例 (javascript)

```javascript
// 常见误区示例

// 误区1: == vs ===
console.log(0 == false)   // true (发生了类型转换)
console.log(0 === false)  // false (严格比较)
// 提示:永远使用 === 避免隐式类型转换

// 误区2: this 指向问题
const obj = {
    name: "张三",
    greet: function() {
        // 这里的 this 指向 obj
        console.log(this.name)
    }
}

const fn = obj.greet
fn()  // undefined! this 不再指向 obj
// 提示:this 的值取决于函数如何被调用,不是定义在哪

// 误区3: 异步循环
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 0)
}
// 输出: 3, 3, 3 (不是 0, 1, 2)
// 原因: var 是函数作用域,循环结束时 i=3
// 修复: 使用 let (块作用域)
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 0)
}
// 输出: 0, 1, 2
```

