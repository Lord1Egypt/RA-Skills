## Carousel 走马灯 ​

**URL:** https://element-plus.org/zh-CN/component/carousel

**Contents:**
- Carousel 走马灯 ​
- 基础用法 ​
  - 1
  - 2
  - 3
  - 4
  - 1
  - 2
  - 3
  - 4

在有限空间内，循环播放同一类型的图片、文字等内容

结合使用 el-carousel 和 el-carousel-item 标签就得到了一个走马灯。 每一个页面的内容是完全可定制的，把你想要展示的内容放在 el-carousel-item 标签内。 默认情况下，在鼠标 hover 底部的指示器时就会触发切换。 通过设置 trigger 属性为 click，可以达到点击触发的效果。

启用动态模糊增强了走马灯的活力和流畅性。 motion-blur 的默认值是 false，手动激活此功能即可提供视觉感受上的提升。

indicator-position 属性定义了指示器的位置。 默认情况下，它会显示在走马灯内部，设置为 outside 则会显示在外部；设置为 none 则不会显示指示器。

arrow 属性定义了切换箭头的显示时机。 默认情况下，切换箭头只有在鼠标 hover 到走马灯上时才会显示。 若将 arrow 设置为 always，则会一直显示；设置为 never，则会一直隐藏。

当 carousel 的 height 设置为 auto时， carousel 的高度将根据子内容的高度自动设置

当页面宽度方向空间空余，但高度方向空间匮乏时，可使用卡片风格

将 type 属性设置为 card 即可启用卡片模式。 从交互上来说，卡片模式和一般模式的最大区别在于，卡片模式可以通过直接点击两侧的幻灯片进行切换。

默认情况下，方向 direction 为 水平 horizontal。 通过设置 direction 为 vertical 来让走马灯在垂直方向上显示。

normal vertical layout

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="block text-center">
    <span class="demonstration">
      Switch when indicator is hovered (default)
    </span>
    <el-carousel height="150px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
  <div class="block text-center" m="t-4">
    <span class="demonstration">Switch when indicator is clicked</span>
    <el-carousel trigger="click" height="150px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

Example 2 (vue):
```vue
<template>
  <div class="block text-center">
    <span class="demonstration">Motion blur the switch (default)</span>
    <el-carousel height="200px" motion-blur>
      <el-carousel-item v-for="item in 4" :key="item">
        <h3 class="small justify-center" text="2xl">{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
  <p class="text-center demonstration">Vertical effect</p>
  <el-carousel
    height="200px"
    direction="vertical"
    motion-blur
    :autoplay="false"
  >
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <el-carousel indicator-position="outside">
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  display: flex;
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

Example 4 (vue):
```vue
<template>
  <el-carousel :interval="5000" arrow="always">
    <el-carousel-item v-for="item in 4" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
```

---
