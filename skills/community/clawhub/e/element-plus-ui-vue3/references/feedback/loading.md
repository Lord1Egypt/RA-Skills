---
name: "loading"
description: "Loading 加载 -- Element Plus Vue3 桌面端组件。Invoke when user needs Loading 加载 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/loading.html"
---

---

# Loading 加载 [​](#loading-加载)

更新日志待解决

12

加载数据时显示动效。

## 区域加载 [​](#区域加载)

在需要的时候展示加载动画，防止页面失去响应提高用户体验（例如表格）。

Element Plus 提供了两种调用 Loading 的方法：指令和服务。 对于自定义指令 `v-loading`，只需要绑定 `boolean` 值即可。 默认状况下，Loading 遮罩会插入到绑定元素的子节点。 通过添加 `body` 修饰符，可以使遮罩插入至 Dom 中的 body 上。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_1_column_1" width="180"><col name="el-table_1_column_2" width="180"><col name="el-table_1_column_3" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_1_column_1 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_1_column_2 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_1_column_3 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGUgdi1sb2FkaW5nPVwibG9hZGluZ1wiIDpkYXRhPVwidGFibGVEYXRhXCIgc3R5bGU9XCJ3aWR0aDogMTAwJVwiPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGxvYWRpbmcgPSByZWYodHJ1ZSlcblxuY29uc3QgdGFibGVEYXRhID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdKb2huIFNtaXRoJyxcbiAgICBhZGRyZXNzOiAnTm8uMTUxOCwgIEppbnNoYWppYW5nIFJvYWQsIFB1dHVvIERpc3RyaWN0JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnSm9obiBTbWl0aCcsXG4gICAgYWRkcmVzczogJ05vLjE1MTgsICBKaW5zaGFqaWFuZyBSb2FkLCBQdXR1byBEaXN0cmljdCcsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ0pvaG4gU21pdGgnLFxuICAgIGFkZHJlc3M6ICdOby4xNTE4LCAgSmluc2hhamlhbmcgUm9hZCwgUHV0dW8gRGlzdHJpY3QnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbmJvZHkge1xuICBtYXJnaW46IDA7XG59XG4uZXhhbXBsZS1zaG93Y2FzZSAuZWwtbG9hZGluZy1tYXNrIHtcbiAgei1pbmRleDogOTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/loading/basic.vue)_

vue

```
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

隐藏源代码

## 自定义加载中组件内容 [​](#自定义加载中组件内容)

你可以自定义加载中组件的文字，图标，以及背景颜色。

在绑定了`v-loading`指令的元素上添加`element-loading-text`属性，其值会被渲染为加载文案，并显示在加载图标的下方。 类似地，`element-loading-spinner`、`element-loading-background` 和 `element-loading-svg` 属性分别用来设定 svg 图标、背景色值、加载图标。

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_2_column_4" width="180"><col name="el-table_2_column_5" width="180"><col name="el-table_2_column_6" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_2_column_4 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_2_column_5 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_2_column_6 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr></tbody></table>

Loading...

|
Date

 |

Name

 |

Address

 |
| --- | --- | --- |

<table class="el-table__body" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 893px;"><colgroup><col name="el-table_3_column_7" width="180"><col name="el-table_3_column_8" width="180"><col name="el-table_3_column_9" width="533"></colgroup><tbody tabindex="-1"><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-02</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-04</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr><tr style="" class="el-table__row"><td colspan="1" rowspan="1" class="el-table_3_column_7 el-table__cell"><div class="cell">2016-05-01</div></td><td colspan="1" rowspan="1" class="el-table_3_column_8 el-table__cell"><div class="cell">John Smith</div></td><td colspan="1" rowspan="1" class="el-table_3_column_9 el-table__cell"><div class="cell">No.1518, Jinshajiang Road, Putuo District</div></td></tr></tbody></table>

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdGFibGVcbiAgICB2LWxvYWRpbmc9XCJsb2FkaW5nXCJcbiAgICBlbGVtZW50LWxvYWRpbmctdGV4dD1cIkxvYWRpbmcuLi5cIlxuICAgIDplbGVtZW50LWxvYWRpbmctc3Bpbm5lcj1cInN2Z1wiXG4gICAgZWxlbWVudC1sb2FkaW5nLXN2Zy12aWV3LWJveD1cIi0xMCwgLTEwLCA1MCwgNTBcIlxuICAgIGVsZW1lbnQtbG9hZGluZy1iYWNrZ3JvdW5kPVwicmdiYSgxMjIsIDEyMiwgMTIyLCAwLjgpXCJcbiAgICA6ZGF0YT1cInRhYmxlRGF0YVwiXG4gICAgc3R5bGU9XCJ3aWR0aDogMTAwJVwiXG4gID5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJkYXRlXCIgbGFiZWw9XCJEYXRlXCIgd2lkdGg9XCIxODBcIiAvPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cIm5hbWVcIiBsYWJlbD1cIk5hbWVcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwiYWRkcmVzc1wiIGxhYmVsPVwiQWRkcmVzc1wiIC8+XG4gIDwvZWwtdGFibGU+XG4gIDxlbC10YWJsZVxuICAgIHYtbG9hZGluZz1cImxvYWRpbmdcIlxuICAgIDplbGVtZW50LWxvYWRpbmctc3ZnPVwic3ZnXCJcbiAgICBjbGFzcz1cImN1c3RvbS1sb2FkaW5nLXN2Z1wiXG4gICAgZWxlbWVudC1sb2FkaW5nLXN2Zy12aWV3LWJveD1cIi0xMCwgLTEwLCA1MCwgNTBcIlxuICAgIDpkYXRhPVwidGFibGVEYXRhXCJcbiAgICBzdHlsZT1cIndpZHRoOiAxMDAlXCJcbiAgPlxuICAgIDxlbC10YWJsZS1jb2x1bW4gcHJvcD1cImRhdGVcIiBsYWJlbD1cIkRhdGVcIiB3aWR0aD1cIjE4MFwiIC8+XG4gICAgPGVsLXRhYmxlLWNvbHVtbiBwcm9wPVwibmFtZVwiIGxhYmVsPVwiTmFtZVwiIHdpZHRoPVwiMTgwXCIgLz5cbiAgICA8ZWwtdGFibGUtY29sdW1uIHByb3A9XCJhZGRyZXNzXCIgbGFiZWw9XCJBZGRyZXNzXCIgLz5cbiAgPC9lbC10YWJsZT5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGxvYWRpbmcgPSByZWYodHJ1ZSlcbmNvbnN0IHN2ZyA9IGBcbiAgICAgICAgPHBhdGggY2xhc3M9XCJwYXRoXCIgZD1cIlxuICAgICAgICAgIE0gMzAgMTVcbiAgICAgICAgICBMIDI4IDE3XG4gICAgICAgICAgTSAyNS42MSAyNS42MVxuICAgICAgICAgIEEgMTUgMTUsIDAsIDAsIDEsIDE1IDMwXG4gICAgICAgICAgQSAxNSAxNSwgMCwgMSwgMSwgMjcuOTkgNy41XG4gICAgICAgICAgTCAxNSAxNVxuICAgICAgICBcIiBzdHlsZT1cInN0cm9rZS13aWR0aDogNHB4OyBmaWxsOiByZ2JhKDAsIDAsIDAsIDApXCIvPlxuICAgICAgYFxuY29uc3QgdGFibGVEYXRhID0gW1xuICB7XG4gICAgZGF0ZTogJzIwMTYtMDUtMDInLFxuICAgIG5hbWU6ICdKb2huIFNtaXRoJyxcbiAgICBhZGRyZXNzOiAnTm8uMTUxOCwgIEppbnNoYWppYW5nIFJvYWQsIFB1dHVvIERpc3RyaWN0JyxcbiAgfSxcbiAge1xuICAgIGRhdGU6ICcyMDE2LTA1LTA0JyxcbiAgICBuYW1lOiAnSm9obiBTbWl0aCcsXG4gICAgYWRkcmVzczogJ05vLjE1MTgsICBKaW5zaGFqaWFuZyBSb2FkLCBQdXR1byBEaXN0cmljdCcsXG4gIH0sXG4gIHtcbiAgICBkYXRlOiAnMjAxNi0wNS0wMScsXG4gICAgbmFtZTogJ0pvaG4gU21pdGgnLFxuICAgIGFkZHJlc3M6ICdOby4xNTE4LCAgSmluc2hhamlhbmcgUm9hZCwgUHV0dW8gRGlzdHJpY3QnLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbi5leGFtcGxlLXNob3djYXNlIC5lbC1sb2FkaW5nLW1hc2sge1xuICB6LWluZGV4OiA5O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/loading/customization.vue)_

vue

```
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

隐藏源代码

WARNING

虽然 `element-loading-spinner / element-loading-svg` 属性支持传入的 HTML 片段，但是动态在网站上渲染任意的 HTML 是非常危险的，因为很容易导致 [XSS 攻击](https://en.wikipedia.org/wiki/Cross-site_scripting)。 请确保 `element-loading-spinner / element-loading-svg`的内容是可信的， **不要**将用户提交的内容赋值给 `element-loading-spinner / element-loading-svg` 属性。

## 让加载组件铺满整个屏幕 [​](#让加载组件铺满整个屏幕)

加载数据时显示全屏动画。

当使用指令方式时，全屏遮罩需要添加`fullscreen`修饰符（遮罩会插入至 body 上） 此时若需要锁定屏幕的滚动，可以使用`lock`修饰符； 当使用服务方式时，遮罩默认即为全屏，无需额外设置。

As a directive As a service

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtYnV0dG9uXG4gICAgdi1sb2FkaW5nLmZ1bGxzY3JlZW4ubG9jaz1cImZ1bGxzY3JlZW5Mb2FkaW5nXCJcbiAgICB0eXBlPVwicHJpbWFyeVwiXG4gICAgQGNsaWNrPVwib3BlbkZ1bGxTY3JlZW4xXCJcbiAgPlxuICAgIEFzIGEgZGlyZWN0aXZlXG4gIDwvZWwtYnV0dG9uPlxuICA8ZWwtYnV0dG9uIHR5cGU9XCJwcmltYXJ5XCIgQGNsaWNrPVwib3BlbkZ1bGxTY3JlZW4yXCI+IEFzIGEgc2VydmljZSA8L2VsLWJ1dHRvbj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyBFbExvYWRpbmcgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGZ1bGxzY3JlZW5Mb2FkaW5nID0gcmVmKGZhbHNlKVxuY29uc3Qgb3BlbkZ1bGxTY3JlZW4xID0gKCkgPT4ge1xuICBmdWxsc2NyZWVuTG9hZGluZy52YWx1ZSA9IHRydWVcbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgZnVsbHNjcmVlbkxvYWRpbmcudmFsdWUgPSBmYWxzZVxuICB9LCAyMDAwKVxufVxuXG5jb25zdCBvcGVuRnVsbFNjcmVlbjIgPSAoKSA9PiB7XG4gIGNvbnN0IGxvYWRpbmcgPSBFbExvYWRpbmcuc2VydmljZSh7XG4gICAgbG9jazogdHJ1ZSxcbiAgICB0ZXh0OiAnTG9hZGluZycsXG4gICAgYmFja2dyb3VuZDogJ3JnYmEoMCwgMCwgMCwgMC43KScsXG4gIH0pXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGxvYWRpbmcuY2xvc2UoKVxuICB9LCAyMDAwKVxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/loading/fullscreen.vue)_

vue

```
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

隐藏源代码

## 以服务的方式来调用 [​](#以服务的方式来调用)

Loading 还可以以服务的方式调用。 你可以像这样引入 Loading 服务：

ts

```
import { ElLoading } from 'element-plus'
```

在你需要的时候通过下面的方式调用：

ts

```
ElLoading.service(options)
```

其中`options`参数为 Loading 的配置项，具体见下表。 `LoadingService` 会返回一个 Loading 实例，可通过调用该实例的 `close` 方法来关闭它：

ts

```
const loadingInstance = ElLoading.service(options)
nextTick(() => {
  // Loading should be closed asynchronously
  loadingInstance.close()
})
```

需要注意的是，以服务的方式调用的全屏 Loading 是单例的。 若在前一个全屏 Loading 关闭前再次调用全屏 Loading，并不会创建一个新的 Loading 实例，而是返回现有全屏 Loading 的实例：

ts

```
const loadingInstance1 = ElLoading.service({ fullscreen: true })
const loadingInstance2 = ElLoading.service({ fullscreen: true })
console.log(loadingInstance1 === loadingInstance2) // true
```

此时调用它们中任意一个的 `close` 方法都能关闭这个全屏 Loading。

如果完整引入了 Element Plus，那么 `app.config.globalProperties` 上会有一个全局方法`$loading`， 它的调用方式为：`this.$loading(options)`，同样会返回一个 Loading 实例。

## 应用程序上下文 2.9.10 [​](#应用程序上下文)

现在 Loading 接受一条 `context` 作为消息构造器的第二个参数，允许你将当前应用的上下文注入到 Loading 中，这将允许你继承应用程序的所有属性。

你可以像这样使用它：

TIP

如果您全局注册了 ELLoading 组件，它将自动继承应用的上下文环境。

ts

```
import { getCurrentInstance } from 'vue'
import { ElLoading } from 'element-plus'

// in your setup method
const { appContext } = getCurrentInstance()!
ElLoading.service({}, appContext)
```

## API [​](#api)

### 配置项 [​](#配置项)

| 名称 | 说明 | 类型 | 默认 |
| --- | --- | --- | --- |
| target | Loading 需要覆盖的 DOM 节点。 可传入一个 DOM 对象或字符串； 若传入字符串，则会将其作为参数传入 `document.querySelector`以获取到对应 DOM 节点 | `string` / `HTMLElement` | document.body |
| body | 同 `v-loading` 指令中的 `body` 修饰符 | `boolean` | false |
| fullscreen | 同 `v-loading` 指令中的 `fullscreen` 修饰符 | `boolean` | true |
| lock | 同 `v-loading` 指令中的 `lock` 修饰符 | `boolean` | false |
| text | 显示在加载图标下方的加载文案 | `string` / `VNode` / `array` | — |
| spinner | 自定义加载图标类名 | `string` | — |
| background | 遮罩背景色 | `string` | — |
| customClass | Loading 的自定义类名 | `string` | — |
| svg | 自定义 SVG 元素覆盖默认加载器 | `string` | — |
| svgViewBox | 设置用于加载 svg 元素的 viewBox 属性 | `string` | — |
| beforeClose 2.7.8 | Loading 关闭之前执行的函数。 如果此函数返回 false ，关闭过程将被中止。 反之，loading 将被关闭。 | `Function` | — |
| closed 2.7.8 | Loading 完全关闭后触发的函数 | `Function` | — |

### 指令 [​](#指令)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| v-loading | 是否显示动画 | `boolean` / `LoadingOptions` |
| element-loading-text | 显示在加载图标下方的加载文案 | `string` |
| element-loading-spinner | 自定义加载图标 | `string` |
| element-loading-svg | 自定义加载图标 (与 element-loading-spinner 相同) | `string` |
| element-loading-svg-view-box | 设置用于加载 svg 元素的 viewBox 属性 | `string` |
| element-loading-background | 背景遮罩的颜色 | `string` |
| element-loading-custom-class | loading 的自定义类名 | `string` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/loading) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/loading.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/loading.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/69580637?v=4&size=64)](https://github.com/jevin98)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/130739557?v=4&size=64)](https://github.com/pan2-2)[![](https://avatars.githubusercontent.com/u/25472916?v=4&size=64)](https://github.com/wiidede)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/20919760?v=4&size=64)](https://github.com/zcmk123)[![](https://avatars.githubusercontent.com/u/134276765?v=4&size=64)](https://github.com/zwgwf)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/25458528?v=4&size=64)](https://github.com/weidehai)[![](https://avatars.githubusercontent.com/u/16174159?v=4&size=64)](https://github.com/anguiao)[![](https://avatars.githubusercontent.com/u/2755933?v=4&size=64)](https://github.com/BiosSun)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/33176053?v=4&size=64)](https://github.com/Ryan2128)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)

[Drawer 抽屉](https://element-plus.org/zh-CN/component/drawer)

[Message 消息提示](https://element-plus.org/zh-CN/component/message)


