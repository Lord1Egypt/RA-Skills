## Tour 漫游式引导 ​

**URL:** https://element-plus.org/zh-CN/component/tour

**Contents:**
- Tour 漫游式引导 ​
- 基础用法 ​
- 非模态 ​
- 位置 ​
- 自定义遮罩样式 ​
- 自定义指示器 ​
- 目标 ​
- Tour API ​
  - Tour Attributes ​
  - Tour slots ​

用于分步引导用户了解产品功能的气泡组件。 用来引导用户并介绍产品

使用:mask="false"可以将引导变为非模态， 同时为了强调引导本身，建议与 type="primary" 组合使用。

改变引导相对于目标的位置，共有 12 种位置可供选择。 当 target 为空时引导将会展示在正中央。

可以传入目标的各种类型的参数。 自2.5.2以来支持字符串和函数类型。

tour-step 组件上相同名称配置的优先级更高。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open">
    <el-tour-step :target="ref1?.$el" title="Upload File">
      <img
        style="width: 240px"
        src="https://element-plus.org/images/element-plus-logo.svg"
        alt="tour.png"
      />
      <div>Put you files here.</div>
    </el-tour-step>
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

Example 2 (vue):
```vue
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour v-model="open" type="primary" :mask="false">
    <el-tour-step
      :target="ref1?.$el"
      title="Upload File"
      description="Put you files here."
    />
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

Example 3 (vue):
```vue
<template>
  <el-button ref="btnRef" type="primary" @click="open = true">
    Begin Tour
  </el-button>

  <el-tour v-model="open">
    <el-tour-step
      title="Center"
      description="Displayed in the center of screen."
    />
    <el-tour-step
      title="Right"
      description="On the right of target."
      placement="right"
      :target="btnRef?.$el"
    />
    <el-tour-step
      title="Top"
      description="On the top of target."
      placement="top"
      :target="btnRef?.$el"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import type { ButtonInstance } from 'element-plus'

const btnRef = ref<ButtonInstance>()

const open = ref(false)
</script>
```

Example 4 (vue):
```vue
<template>
  <el-button type="primary" @click="open = true">Begin Tour</el-button>

  <el-divider />

  <el-space>
    <el-button ref="ref1">Upload</el-button>
    <el-button ref="ref2" type="primary">Save</el-button>
    <el-button ref="ref3" :icon="MoreFilled" />
  </el-space>

  <el-tour
    v-model="open"
    :mask="{
      style: {
        boxShadow: 'inset 0 0 15px #333',
      },
      color: 'rgba(80, 255, 255, .4)',
    }"
  >
    <el-tour-step :target="ref1?.$el" title="Upload File">
      <img
        src="https://element-plus.org/images/element-plus-logo.svg"
        alt="tour.png"
      />
      <div>Put you files here.</div>
    </el-tour-step>
    <el-tour-step
      :target="ref2?.$el"
      title="Save"
      description="Save your changes"
      :mask="{
        style: {
          boxShadow: 'inset 0 0 15px #fff',
        },
        color: 'rgba(40, 0, 255, .4)',
      }"
    />
    <el-tour-step
      :target="ref3?.$el"
      title="Other Actions"
      description="Click to see other"
      :mask="false"
    />
  </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MoreFilled } from '@element-plus/icons-vue'

import type { ButtonInstance } from 'element-plus'

const ref1 = ref<ButtonInstance>()
const ref2 = ref<ButtonInstance>()
const ref3 = ref<ButtonInstance>()

const open = ref(false)
</script>
```

---
