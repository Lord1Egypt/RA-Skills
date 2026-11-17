## Config Provider 全局配置 ​

**URL:** https://element-plus.org/zh-CN/component/config-provider

**Contents:**
- Config Provider 全局配置 ​
- i18n 配置 ​
- 对按钮进行配置 ​
- 对链接进行配置2.9.11 ​
- 对 Card 进行配置 2.10.5 ​
- 对 Dialog 进行配置 2.10.7 ​
- 对消息进行配置 ​
- 空值配置2.7.0 ​
- 表格配置 2.13.3 ​
- 实验性功能 ​

Config Provider 被用来提供全局的配置选项，让你的配置能够在全局都能够被访问到。

通过 Config Provider 来配置多语言，让你的应用可以随时切换语言。

设置 empty-values 来配置组件的默认空值。 默认值是 ['', null, undefined]。 如果认为空字符串不是一个空值，可以设置成 [undefined, null]。

设置 value-on-clear 以设置清空选项的值。 组件默认值是 undefined。 在日期组件中是 null。 如果想设置成 undefined，请使用 () => undefined。

在本节中，您可以学习如何使用 Config Provider 来提供实验性功能。 现在，我们还没有添加任何实验性功能，但在未来的规划中，我们将添加一些实验性功能。 您可以使用此配置来管理这些功能。

**Examples:**

Example 1 (jsx):
```jsx
<template>
  <div>
    <el-button mb-2 @click="toggle">Switch Language</el-button>
    <br />

    <el-config-provider :locale="locale">
      <el-table mb-1 :data="[]" />
      <el-pagination :total="100" />
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'

const language = ref('zh-cn')
const locale = computed(() => (language.value === 'zh-cn' ? zhCn : en))

const toggle = () => {
  language.value = language.value === 'zh-cn' ? 'en' : 'zh-cn'
}
</script>
```

Example 2 (vue):
```vue
<template>
  <div>
    <div>
      <el-checkbox v-model="config.autoInsertSpace">
        autoInsertSpace
      </el-checkbox>
      <el-checkbox v-model="config.plain"> plain </el-checkbox>
      <el-checkbox v-model="config.round"> round </el-checkbox>
      <el-checkbox v-model="config.dashed"> dashed </el-checkbox>
      <el-checkbox v-model="config.text"> text </el-checkbox>
      <el-select v-model="config.type" class="ml-5" style="max-width: 150px">
        <el-option
          v-for="type in buttonTypes.filter(Boolean)"
          :key="type"
          :value="type"
        />
      </el-select>
    </div>
    <el-divider />
    <el-config-provider :button="config">
      <el-button>中文</el-button>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { buttonTypes } from 'element-plus'

import type { ButtonConfigContext } from 'element-plus'

const config = reactive<ButtonConfigContext>({
  autoInsertSpace: true,
  type: 'default',
  plain: true,
  round: true,
  text: false,
  dashed: false,
})
</script>
```

Example 3 (vue):
```vue
<template>
  <div>
    <div class="flex gap-4">
      <div class="flex flex-col basis-150px gap-1">
        <span>Type:</span>
        <el-select v-model="config.type">
          <el-option v-for="type in linkTypes" :key="type" :value="type" />
        </el-select>
      </div>
      <div class="flex flex-col basis-150px gap-1">
        <span>Underline:</span>
        <el-select v-model="config.underline">
          <el-option
            v-for="type in underlineOptions"
            :key="type"
            :value="type"
          />
        </el-select>
      </div>
    </div>
    <el-divider />
    <el-config-provider :link="config">
      <el-link>Link desu!</el-link>
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

import type { LinkConfigContext } from 'element-plus'

const linkTypes = ['primary', 'success', 'warning', 'info', 'danger', 'default']
const underlineOptions = ['always', 'never', 'hover']

const config = reactive<LinkConfigContext>({
  type: 'success',
  underline: 'always',
})
</script>
```

Example 4 (vue):
```vue
<script lang="ts" setup>
import { reactive } from 'vue'

import type { CardConfigContext } from 'element-plus'

const config = reactive<CardConfigContext>({
  shadow: 'always',
})
</script>

<template>
  Shadow:
  <div class="flex flex-col justify-center">
    <el-radio-group v-model="config.shadow">
      <el-radio value="always">always</el-radio>
      <el-radio value="hover">hover</el-radio>
      <el-radio value="never">never</el-radio>
    </el-radio-group>
    <el-divider />
    <el-config-provider :card="config">
      <el-card>Card desu!</el-card>
    </el-config-provider>
  </div>
</template>
```

---
