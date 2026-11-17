## Loading 加载 ​

**URL:** https://element-plus.org/zh-CN/component/loading

**Contents:**
- Loading 加载 ​
- 区域加载 ​
- 自定义加载中组件内容 ​
- 让加载组件铺满整个屏幕 ​
- 以服务的方式来调用 ​
- 应用程序上下文 2.9.10 ​
- API ​
  - 配置项 ​
  - 指令 ​
- 源代码 ​

在需要的时候展示加载动画，防止页面失去响应提高用户体验（例如表格）。

Element Plus 提供了两种调用 Loading 的方法：指令和服务。 对于自定义指令 v-loading，只需要绑定 boolean 值即可。 默认状况下，Loading 遮罩会插入到绑定元素的子节点。 通过添加 body 修饰符，可以使遮罩插入至 Dom 中的 body 上。

你可以自定义加载中组件的文字，图标，以及背景颜色。

在绑定了v-loading指令的元素上添加element-loading-text属性，其值会被渲染为加载文案，并显示在加载图标的下方。 类似地，element-loading-spinner、element-loading-background 和 element-loading-svg 属性分别用来设定 svg 图标、背景色值、加载图标。

虽然 element-loading-spinner / element-loading-svg 属性支持传入的 HTML 片段，但是动态在网站上渲染任意的 HTML 是非常危险的，因为很容易导致 XSS 攻击。 请确保 element-loading-spinner / element-loading-svg的内容是可信的， 不要将用户提交的内容赋值给 element-loading-spinner / element-loading-svg 属性。

当使用指令方式时，全屏遮罩需要添加fullscreen修饰符（遮罩会插入至 body 上） 此时若需要锁定屏幕的滚动，可以使用lock修饰符； 当使用服务方式时，遮罩默认即为全屏，无需额外设置。

Loading 还可以以服务的方式调用。 你可以像这样引入 Loading 服务：

其中options参数为 Loading 的配置项，具体见下表。 LoadingService 会返回一个 Loading 实例，可通过调用该实例的 close 方法来关闭它：

需要注意的是，以服务的方式调用的全屏 Loading 是单例的。 若在前一个全屏 Loading 关闭前再次调用全屏 Loading，并不会创建一个新的 Loading 实例，而是返回现有全屏 Loading 的实例：

此时调用它们中任意一个的 close 方法都能关闭这个全屏 Loading。

如果完整引入了 Element Plus，那么 app.config.globalProperties 上会有一个全局方法$loading， 它的调用方式为：this.$loading(options)，同样会返回一个 Loading 实例。

现在 Loading 接受一条 context 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Loading 中，这将允许你继承应用程序的所有属性。

如果您全局注册了 ELLoading 组件，它将自动继承应用的上下文环境。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-table v-loading="loading" :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(true)

const tableData = [
  {
    date: '2016-05-02',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]
</script>

<style>
body {
  margin: 0;
}
.example-showcase .el-loading-mask {
  z-index: 9;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <el-table
    v-loading="loading"
    element-loading-text="Loading..."
    :element-loading-spinner="svg"
    element-loading-svg-view-box="-10, -10, 50, 50"
    element-loading-background="rgba(122, 122, 122, 0.8)"
    :data="tableData"
    style="width: 100%"
  >
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
  <el-table
    v-loading="loading"
    :element-loading-svg="svg"
    class="custom-loading-svg"
    element-loading-svg-view-box="-10, -10, 50, 50"
    :data="tableData"
    style="width: 100%"
  >
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" />
  </el-table>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const loading = ref(true)
const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `
const tableData = [
  {
    date: '2016-05-02',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]
</script>

<style>
.example-showcase .el-loading-mask {
  z-index: 9;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-button
    v-loading.fullscreen.lock="fullscreenLoading"
    type="primary"
    @click="openFullScreen1"
  >
    As a directive
  </el-button>
  <el-button type="primary" @click="openFullScreen2"> As a service </el-button>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElLoading } from 'element-plus'

const fullscreenLoading = ref(false)
const openFullScreen1 = () => {
  fullscreenLoading.value = true
  setTimeout(() => {
    fullscreenLoading.value = false
  }, 2000)
}

const openFullScreen2 = () => {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  setTimeout(() => {
    loading.close()
  }, 2000)
}
</script>
```

Example 4 (sql):
```sql
import { ElLoading } from 'element-plus'
```

---
