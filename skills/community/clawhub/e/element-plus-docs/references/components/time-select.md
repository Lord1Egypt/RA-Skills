## TimeSelect 时间选择 ​

**URL:** https://element-plus.org/zh-CN/component/time-select

**Contents:**
- TimeSelect 时间选择 ​
- 固定时间点 ​
- 时间格式 ​
- 固定时间范围 ​
- API ​
  - Attributes ​
  - Events ​
  - Exposes ​
- 源代码 ​
- 贡献者 ​

使用 el-time-select 标签，然后通过start、end和step指定起始时间，结束时间和步长。

使用 format 属性来控制时间格式 (小时以及分钟)。

在 这里 查看 Day.js 支持的 format 参数。

如果先选中了开始（或结束）时间，则结束（或开始）时间的状态也将会随之改变。

**Examples:**

Example 1 (vue):
```vue
<template>
  <el-time-select
    v-model="value"
    style="width: 240px"
    start="08:30"
    step="00:15"
    end="18:30"
    placeholder="Select time"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
</script>
```

Example 2 (vue):
```vue
<template>
  <el-time-select
    v-model="value"
    style="width: 240px"
    start="00:00"
    step="00:30"
    end="23:59"
    placeholder="Select time"
    format="hh:mm A"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
</script>
```

Example 3 (vue):
```vue
<template>
  <div class="demo-time-range flex flex-wrap gap-4">
    <el-time-select
      v-model="startTime"
      style="width: 240px"
      :max-time="endTime"
      placeholder="Start time"
      start="08:30"
      step="00:15"
      end="18:30"
    />
    <el-time-select
      v-model="endTime"
      style="width: 240px"
      :min-time="startTime"
      placeholder="End time"
      start="08:30"
      step="00:15"
      end="18:30"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const startTime = ref('')
const endTime = ref('')
</script>
```

---
