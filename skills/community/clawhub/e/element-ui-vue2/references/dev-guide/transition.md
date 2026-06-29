---
name: "transition"
description: "内置过渡动画 -- Element UI Vue2 桌面端组件。Invoke when user needs 内置过渡动画 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/transition"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/transition#nei-zhi-guo-du-dong-hua) 内置过渡动画

Element 内应用在部分组件的过渡动画，你也可以直接使用。在使用之前请阅读 [transition 组件文档](https://cn.vuejs.org/v2/api/#transition) 。

### [¶](https://element.eleme.cn/#/zh-CN/component/transition#fade-dan-ru-dan-chu) fade 淡入淡出

Click Me

.el-fade-in-linear

.el-fade-in

提供 `el-fade-in-linear` 和 `el-fade-in` 两种效果。

```
<template>
  <div>
    <el-button @click="show = !show">Click Me</el-button>

    <div style="display: flex; margin-top: 20px; height: 100px;">
      <transition name="el-fade-in-linear">
        <div v-show="show" class="transition-box">.el-fade-in-linear</div>
      </transition>
      <transition name="el-fade-in">
        <div v-show="show" class="transition-box">.el-fade-in</div>
      </transition>
    </div>
  </div>
</template>

<script>
    export default {
    data: () => ({
      show: true
    })
  }
</script>

<style>
  .transition-box {
    margin-bottom: 10px;
    width: 200px;
    height: 100px;
    border-radius: 4px;
    background-color: #409EFF;
    text-align: center;
    color: #fff;
    padding: 40px 20px;
    box-sizing: border-box;
    margin-right: 20px;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/transition#zoom-suo-fang) zoom 缩放

Click Me

.el-zoom-in-center

.el-zoom-in-top

.el-zoom-in-bottom

提供 `el-zoom-in-center`，`el-zoom-in-top` 和 `el-zoom-in-bottom` 三种效果。

```
<template>
  <div>
    <el-button @click="show2 = !show2">Click Me</el-button>

    <div style="display: flex; margin-top: 20px; height: 100px;">
      <transition name="el-zoom-in-center">
        <div v-show="show2" class="transition-box">.el-zoom-in-center</div>
      </transition>

      <transition name="el-zoom-in-top">
        <div v-show="show2" class="transition-box">.el-zoom-in-top</div>
      </transition>

      <transition name="el-zoom-in-bottom">
        <div v-show="show2" class="transition-box">.el-zoom-in-bottom</div>
      </transition>
    </div>
  </div>
</template>

<script>
    export default {
    data: () => ({
      show2: true
    })
  }
</script>

<style>
  .transition-box {
    margin-bottom: 10px;
    width: 200px;
    height: 100px;
    border-radius: 4px;
    background-color: #409EFF;
    text-align: center;
    color: #fff;
    padding: 40px 20px;
    box-sizing: border-box;
    margin-right: 20px;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/transition#collapse-zhan-kai-zhe-die) collapse 展开折叠

使用 `el-collapse-transition` 组件实现折叠展开效果。

Click Me

el-collapse-transition

el-collapse-transition

```
<template>
  <div>
    <el-button @click="show3 = !show3">Click Me</el-button>

    <div style="margin-top: 20px; height: 200px;">
      <el-collapse-transition>
        <div v-show="show3">
          <div class="transition-box">el-collapse-transition</div>
          <div class="transition-box">el-collapse-transition</div>
        </div>
      </el-collapse-transition>
    </div>
  </div>
</template>

<script>
    export default {
    data: () => ({
      show3: true
    })
  }
</script>

<style>
  .transition-box {
    margin-bottom: 10px;
    width: 200px;
    height: 100px;
    border-radius: 4px;
    background-color: #409EFF;
    text-align: center;
    color: #fff;
    padding: 40px 20px;
    box-sizing: border-box;
    margin-right: 20px;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/transition#an-xu-yin-ru) 按需引入

```js
// fade/zoom 等
import 'element-ui/lib/theme-chalk/base.css';
// collapse 展开折叠
import CollapseTransition from 'element-ui/lib/transitions/collapse-transition';
import Vue from 'vue'

Vue.component(CollapseTransition.name, CollapseTransition)
```

自定义主题 Layout 布局


