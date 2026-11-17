## Space 间距 ​

**URL:** https://element-plus.org/zh-CN/component/space

**Contents:**
- Space 间距 ​
- 基础用法 ​
- 垂直布局 ​
- 控制间距的大小 ​
- 自定义 Size ​
- 自动换行 ​
- 行间分隔符 ​
- 字母数字类型分隔符 ​
- 分隔符还可以是 VNode 类型 ​
- 对齐方式 ​

虽然我们拥有 Divider 组件，但很多时候我们需要不是一个被 Divider 组件 分割开的页面结构，因此我们会重复的使用很多的 Divider 组件，这在我们的开发效率上造成了一定的困扰。 间距组件就是为了解决这种困扰应运而生的。

最基础的用法，通过这个组件来给组件之间提供统一的间距。

使用 direction 来控制布局的方式, 背后实际上是利用了 flex-direction 来控制.

你可以使用内置的尺寸 small、default、large 来设置大小，这些尺寸分别对应 8px、12px、16px。 默认的间距大小为 small，也就是 8px。

您也可以通过自定义的 size 来控制大小， 参见下一个部分。

很多时候，内建的大小不满足设计师的要求，我们可以通过传入自己定义的大小 (数值类型) 来设置。

不要让 ElSpace 与使用依赖父元素百分比宽度（或高度）的元素一起使用（例如 ElSlider），这样会造成光标不同步。

在 **水平 (horizontal) ** 模式下，通过使用 wrap（布尔类型）来控制自动换行行为。

有时候，仅仅在行间加空白并不能满足我们的日常需求，此时分隔符 (spacer) 就可以发挥非常好的作用了。

设置该值可以调整所有子节点在容器内的对齐方式，可设置的值与 align-items 一致。

通过 fill**（布尔类型）**参数，您可以控制子节点是否自动填充容器。

下面的例子中，当设置为 fill 时，子节点的宽度会自动适配容器的宽度。

也可以使用 fillRatio 参数，自定义填充的比例， 默认值为 100，代表基于父容器宽度的 100% 进行填充

需要注意的是，水平布局和垂直布局的表现形式稍有不同，具体的效果可以查看下面的例子

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-space wrap>
    <el-card v-for="i in 3" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>
```

Example 2 (vue):
```vue
<template>
  <el-space direction="vertical">
    <el-card v-for="i in 2" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>
```

Example 3 (vue):
```vue
<template>
  <el-space direction="vertical" alignment="start" :size="30">
    <el-radio-group v-model="size">
      <el-radio value="large">Large</el-radio>
      <el-radio value="default">Default</el-radio>
      <el-radio value="small">Small</el-radio>
    </el-radio-group>

    <el-space wrap :size="size">
      <el-card v-for="i in 3" :key="i" class="box-card" style="width: 250px">
        <template #header>
          <div class="card-header">
            <span>Card name</span>
            <el-button class="button" text>Operation button</el-button>
          </div>
        </template>
        <div v-for="o in 4" :key="o" class="text item">
          {{ 'List item ' + o }}
        </div>
      </el-card>
    </el-space>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { ComponentSize } from 'element-plus'

const size = ref<ComponentSize>('default')
</script>
```

Example 4 (vue):
```vue
<template>
  <el-slider v-model="size" />
  <el-space wrap :size="size">
    <el-card v-for="i in 2" :key="i" class="box-card" style="width: 250px">
      <template #header>
        <div class="card-header">
          <span>Card name</span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      <div v-for="o in 4" :key="o" class="text item">
        {{ 'List item ' + o }}
      </div>
    </el-card>
  </el-space>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const size = ref(20)
</script>
```

---
