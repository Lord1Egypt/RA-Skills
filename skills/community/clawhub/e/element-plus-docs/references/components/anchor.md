## Anchor 锚点 ​

**URL:** https://element-plus.org/zh-CN/component/anchor

**Contents:**
- Anchor 锚点 ​
- 基础用法 ​
- 水平模式 ​
- 滚动容器 ​
- 锚点链接变化 ​
- 下划线类型 ​
- 固定模式 ​
- Anchor API ​
  - 属性 ​
  - Anchor Events ​

通过锚点，您可以很快找到当前页面上信息内容的位置。

自定义滚动区域，使用 offset props 可以设置锚点滚动偏移。 监听link-click事件并阻止浏览器的默认行为，从而不会更改历史记录。

设置type="underline"以更改为下划线类型

使用 affix 组件来固定住页面中的锚点。

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-anchor :offset="70">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['anchor-api']}`">
      {{ locale['Anchor API'] }}
      <template #sub-link>
        <el-anchor-link :href="`#${locale['anchor-attributes']}`">
          {{ locale['Anchor Attributes'] }}
        </el-anchor-link>
        <el-anchor-link :href="`#${locale['anchor-events']}`">
          {{ locale['Anchor Events'] }}
        </el-anchor-link>
      </template>
    </el-anchor-link>
  </el-anchor>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

Example 2 (typescript):
```typescript
<template>
  <el-anchor :offset="70" direction="horizontal">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
  </el-anchor>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])
</script>
```

Example 3 (html):
```html
<template>
  <div>
    <el-row>
      <el-col :span="18">
        <div
          style="
            height: 30px;
            width: 70%;
            background: #000;
            position: absolute;
            top: 0;
            left: 0;
            color: #fff;
          "
        >
          Fixed Top Block
        </div>
        <div ref="containerRef" style="height: 300px; overflow-y: auto">
          <div
            id="part1"
            style="
              height: 300px;
              background: rgba(255, 0, 0, 0.02);
              margin-top: 30px;
            "
          >
            part1
          </div>
          <div
            id="part2"
            style="
              height: 300px;
              background: rgba(0, 255, 0, 0.02);
              margin-top: 30px;
            "
          >
            part2
          </div>
          <div
            id="part3"
            style="
              height: 300px;
              background: rgba(0, 0, 255, 0.02);
              margin-top: 30px;
            "
          >
            part3
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="vp-raw">
          <el-anchor
            :container="containerRef"
            direction="vertical"
            type="default"
            :offset="30"
            @click="handleClick"
          >
            <el-anchor-link href="#part1" title="part1" />
            <el-anchor-link href="#part2" title="part2" />
            <el-anchor-link href="#part3" title="part3" />
          </el-anchor>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const containerRef = ref<HTMLElement | null>(null)

const handleClick = (e: MouseEvent) => {
  e.preventDefault()
}
</script>
```

Example 4 (typescript):
```typescript
<template>
  <el-anchor :offset="70" @change="handleChange">
    <el-anchor-link :href="`#${locale['basic-usage']}`">
      {{ locale['Basic Usage'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['horizontal-mode']}`">
      {{ locale['Horizontal Mode'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['scroll-container']}`">
      {{ locale['Scroll Container'] }}
    </el-anchor-link>
    <el-anchor-link :href="`#${locale['anchor-api']}`">
      {{ locale['Anchor API'] }}
      <template #sub-link>
        <el-anchor-link :href="`#${locale['anchor-attributes']}`">
          {{ locale['Anchor Attributes'] }}
        </el-anchor-link>
        <el-anchor-link :href="`#${locale['anchor-events']}`">
          {{ locale['Anchor Events'] }}
        </el-anchor-link>
      </template>
    </el-anchor-link>
  </el-anchor>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import anchorLocale from '../../.vitepress/i18n/component/anchor.json'
import { useLang } from '~/composables/lang'

const lang = useLang()
const locale = computed(() => anchorLocale[lang.value])

const handleChange = (href: string) => {
  console.log(`anchor change: ${href}`)
}
</script>
```

---
