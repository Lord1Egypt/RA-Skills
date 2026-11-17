## Skeleton 骨架屏 ​

**URL:** https://element-plus.org/zh-CN/component/skeleton

**Contents:**
- Skeleton 骨架屏 ​
- 基础用法 ​
- 更多参数 ​
- 动画效果 ​
- 自定义样式 ​
- 加载状态 ​
- 渲染多条数据 ​
- 防止渲染抖动 ​
- 初始渲染加载 2.8.8 ​
- 切换显示/隐藏时避免渲染抖动 2.8.8 ​

在需要等待加载内容的位置设置一个骨架屏，某些场景下比 Loading 的视觉效果更好。

可以配置骨架屏段落数量，以便更接近真实渲染效果。显示的数量会比传入的数量多 1，首行会被渲染一个长度 33% 的段首。

我们提供了一个开关标志，表明是否显示加载动画， 调用 animated 如果真是这样，所有的 el-skeleton 的子节点将显示动画。

Element Plus 提供的排版模式有时候并不满足要求，当您想要用自己定义的模板时，可以通过一个具名 Slot template 来自己设定模板。

我们提供了不同的模板单元可供使用，具体可选值请看 API 详细描述。 另外，在构建您自己自定义的骨架时，您应该尽可能更接近于真正的DOM。 避免DOM因高度差而发生抖动。

当 Loading 结束之后，我们往往需要显示真实的 UI， 可以通过 loading 属性的值来控制是否显示加载后的 DOM。 也可以通过具名插槽 default 来构建 loading 结束之后需要展示的真实 DOM 元素结构。

大多时候, 骨架屏都被用来渲染列表, 当我们需要在从服务器获取数据的时候来渲染一个假的 UI。 利用 count 这个属性就能控制渲染多少条假的数据在页面上

我们不推荐在浏览器中渲染过多的虚假 UI 元素，这样会消耗更多时间销毁骨架元素，从而引起性能问题。 为了用户体验，请尽量将 count 值保持在小一点的数值。

有的时候，API 的请求回来的特别快，往往骨架占位刚刚被渲染，真实的数据就已经回来了，用户的界面会突然一闪， 此时为了避免这种情况，就需要通过 throttle 属性来避免这个问题。

2.8.8版本里， throtle 属性支持两个值： number 和 object。 当通过 number时，它相当于 {leading: xxx}，控制骨架屏幕显示的节奏。 当然，您也可以通过传递 {trailing: xxx} 来控制骨架屏消失的节奏。

当初始值为 loading: true 时，您可以设置 throttle: {initVal: true, leading: xxx} 来控制初始骨架屏的即时显示，而无需进行节流。

您可以设置 throttle: {initVal: true, leading: xxx, trailing: xxx}，以控制骨架效果的初始显示，并使切换加载状态时骨架效果的过渡更加平滑。

有时，当加载状态切换显示或隐藏时，您可能希望业务组件的渲染更加平滑。 您可以设置 throttle: {leading: xxx, trailing: xxx} 来控制渲染抖动。

**Examples:**

Example 1 (jsx):
```jsx
<template>
  <el-skeleton />
  <br />
  <el-skeleton style="--el-skeleton-circle-size: 100px">
    <template #template>
      <el-skeleton-item variant="circle" />
    </template>
  </el-skeleton>
</template>
```

Example 2 (typescript):
```typescript
<template>
  <el-skeleton :rows="5" />
</template>
```

Example 3 (typescript):
```typescript
<template>
  <el-skeleton :rows="5" animated />
</template>
```

Example 4 (vue):
```vue
<template>
  <el-skeleton style="width: 240px">
    <template #template>
      <el-skeleton-item variant="image" style="width: 240px; height: 240px" />
      <div style="padding: 14px">
        <el-skeleton-item variant="p" style="width: 50%" />
        <div
          style="
            display: flex;
            align-items: center;
            justify-items: space-between;
          "
        >
          <el-skeleton-item variant="text" style="margin-right: 16px" />
          <el-skeleton-item variant="text" style="width: 30%" />
        </div>
      </div>
    </template>
  </el-skeleton>
</template>
```

---
