---
name: "avatar"
description: "Avatar 头像 -- Element UI Vue2 桌面端组件。Invoke when user needs Avatar 头像 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/avatar"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/avatar#avatar-tou-xiang) Avatar 头像

用图标、图片或者字符的形式展示用户或事物信息。

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#ji-ben-yong-fa) 基本用法

通过 `shape` 和 `size` 设置头像的形状和大小。

circle

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

![](https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png)

square

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

![](https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png)

```
<template>
  <el-row class="demo-avatar demo-basic">
    <el-col :span="12">
      <div class="sub-title">circle</div>
      <div class="demo-basic--circle">
        <div class="block"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
        <div class="block" v-for="size in sizeList" :key="size">
          <el-avatar :size="size" :src="circleUrl"></el-avatar>
        </div>
      </div>
    </el-col>
    <el-col :span="12">
      <div class="sub-title">square</div>
      <div class="demo-basic--circle">
        <div class="block"><el-avatar shape="square" :size="50" :src="squareUrl"></el-avatar></div>
        <div class="block" v-for="size in sizeList" :key="size">
          <el-avatar shape="square" :size="size" :src="squareUrl"></el-avatar>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
<script>
  export default {
    data () {
      return {
        circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
        squareUrl: "https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png",
        sizeList: ["large", "medium", "small"]
      }
    }
  }
</script>

```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#zhan-shi-lei-xing) 展示类型

支持三种类型：图标、图片和字符

![](https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png)

user

```
<template>
  <div class="demo-type">
    <div>
      <el-avatar icon="el-icon-user-solid"></el-avatar>
    </div>
    <div>
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
    </div>
    <div>
      <el-avatar> user </el-avatar>
    </div>
  </div>
</template>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#tu-pian-jia-zai-shi-bai-de-fallback-xing-wei) 图片加载失败的 fallback 行为

当展示类型为图片的时候，图片加载失败的 fallback 行为

![](https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png)

```
<template>
  <div class="demo-type">
    <el-avatar :size="60" src="https://empty" @error="errorHandler">
      <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
    </el-avatar>
  </div>
</template>
<script>
  export default {
    methods: {
      errorHandler() {
        return true
      }
    }
  }
</script>

```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#tu-pian-ru-he-gua-ying-rong-qi-kuang) 图片如何适应容器框

当展示类型为图片的时候，使用 `fit` 属性定义图片如何适应容器框，同原生 [object-fit](https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit)。

fill ![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

contain ![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

cover ![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

none ![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

scale-down ![](https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg)

```
<template>
  <div class="demo-fit">
    <div class="block" v-for="fit in fits" :key="fit">
        <span class="title">{{ fit }}</span>
        <el-avatar shape="square" :size="100" :fit="fit" :src="url"></el-avatar>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        fits: ['fill', 'contain', 'cover', 'none', 'scale-down'],
        url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
      }
    }
  }
</script>

```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| icon | 设置头像的图标类型，参考 Icon 组件 | string |  |  |
| size | 设置头像的大小 | number/string | number / large / medium / small | large |
| shape | 设置头像的形状 | string | circle / square | circle |
| src | 图片头像的资源地址 | string |  |  |
| srcSet | 以逗号分隔的一个或多个字符串列表表明一系列用户代理使用的可能的图像 | string |  |  |
| alt | 描述图像的替换文本 | string |  |  |
| fit | 当展示类型为图片的时候，设置图片如何适应容器框 | string | fill / contain / cover / none / scale-down | cover |

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| error | 图片类头像加载失败的回调， 返回 false 会关闭组件默认的 fallback 行为 | (e: Event) |

### [¶](https://element.eleme.cn/#/zh-CN/component/avatar#slot) Slot

| 名称 | 说明 |
| --- | --- |
| default | 自定义头像展示内容 |

Badge 标记 Skeleton 骨架屏


