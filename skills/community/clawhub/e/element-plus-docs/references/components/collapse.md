## Collapse 折叠面板 ​

**URL:** https://element-plus.org/zh-CN/component/collapse

**Contents:**
- Collapse 折叠面板 ​
- 基础用法 ​
- 手风琴效果 ​
- 自定义面板标题 ​
- 自定义图标 2.8.3 ​
- 自定义图标位置 2.9.10 ​
- 阻止折叠 2.9.11 ​
- Collapse API ​
  - Collapse Attributes ​
  - Collapse Events ​

通过 accordion 属性来设置是否以手风琴模式显示。

除了可以通过 title 属性以外，还可以通过具名 slot 来实现自定义面板的标题内容，以实现增加图标等效果。

从版本 2.9.10开始， title 插槽提供一个 isActive 属性，显示当前折叠项是否活跃。

除了使用 icon 属性外，您还可以自定义面板项目图标，从而添加自定义内容。

使用 expand-icon-position 属性，您可以自定义图标位置。

设置 beforeChange 属性，若返回 false 或者返回 Promise 且被 reject ，则停止切换。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advice about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CollapseModelValue } from 'element-plus'

const activeNames = ref(['1'])
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}
</script>
```

Example 2 (vue):
```vue
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeName = ref('1')
</script>
```

Example 3 (vue):
```vue
<template>
  <div class="demo-collapse">
    <el-collapse accordion>
      <el-collapse-item name="1">
        <template #title="{ isActive }">
          <div :class="['title-wrapper', { 'is-active': isActive }]">
            Consistency
            <el-icon class="header-icon">
              <info-filled />
            </el-icon>
          </div>
        </template>
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { InfoFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.title-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
}

.title-wrapper.is-active {
  color: var(--el-color-primary);
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="Consistency" name="1" :icon="CaretRight">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <template #icon="{ isActive }">
          <span class="icon-ele">
            {{ isActive ? 'Expanded' : 'Collapsed' }}
          </span>
        </template>
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CaretRight } from '@element-plus/icons-vue'

import type { CollapseModelValue } from 'element-plus'

const activeNames = ref(['1'])
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}
</script>

<style scoped>
.icon-ele {
  margin: 0 8px 0 auto;
  color: #409eff;
}
</style>
```

---
