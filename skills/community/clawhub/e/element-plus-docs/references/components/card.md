## Card 卡片 ​

**URL:** https://element-plus.org/zh-CN/component/card

**Contents:**
- Card 卡片 ​
- 基础用法 ​
- 简单卡片 ​
- 有图片内容的卡片 ​
- 带有阴影效果的卡片 ​
- API ​
  - Attributes ​
  - Slots ​
- 源代码 ​
- 贡献者 ​

Card 组件由 header body 和 footer组成。 header 和 footer是可选的，其内容取决于一个具名的 slot。

配置 body-style 属性来自定义 body 部分的样式。

通过 shadow 属性设置卡片阴影出现的时机。 该属性的值可以是：always、hover 或 never。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-card style="max-width: 480px">
    <template #header>
      <div class="card-header">
        <span>Card name</span>
      </div>
    </template>
    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
    <template #footer>Footer content</template>
  </el-card>
</template>
```

Example 2 (vue):
```vue
<template>
  <el-card style="max-width: 480px">
    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
  </el-card>
</template>
```

Example 3 (vue):
```vue
<template>
  <el-card style="max-width: 480px">
    <template #header>Yummy hamburger</template>
    <img
      src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
      style="width: 100%"
    />
  </el-card>
</template>
```

Example 4 (vue):
```vue
<template>
  <div class="flex flex-wrap gap-4">
    <el-card style="width: 480px" shadow="always">Always</el-card>
    <el-card style="width: 480px" shadow="hover">Hover</el-card>
    <el-card style="width: 480px" shadow="never">Never</el-card>
  </div>
</template>
```

---
