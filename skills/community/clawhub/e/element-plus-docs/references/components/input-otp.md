## InputOtp 一次性密码输入框 beta ​

**URL:** https://element-plus.org/zh-CN/component/input-otp

**Contents:**
- InputOtp 一次性密码输入框 beta ​
- 基础用法 ​
- 自定义长度 ​
- 展示类型 ​
- 调整尺寸 ​
- 禁用 & 只读 ​
- 密码模式 ​
- 分隔符 ​
- 自定义验证 ​
- 应用开发接口（API） ​

输入字段长度可以通过设置length属性来自定义。

有三种类型可用：outlined （默认）、filled 和 underlined。

有三个尺寸可用：large、default 和 small。

设置 validator 属性以验证输入字符，并使用 inputmode 指定键盘类型。

**Examples:**

Example 1 (vue):
```vue
<template>
  <div>
    <el-input-otp v-model="otp" />
    <div style="margin-top: 20px">Value: {{ otp }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp = ref('123')
</script>
```

Example 2 (vue):
```vue
<template>
  <div class="demo-input-otp">
    <el-input-otp v-model="otp1" :length="4" />
    <el-input-otp v-model="otp2" :length="8" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
```

Example 3 (vue):
```vue
<template>
  <div class="demo-input-otp">
    <div>
      <p>Outlined (Default)</p>
      <el-input-otp v-model="otp1" type="outlined" />
    </div>
    <div>
      <p>Filled</p>
      <el-input-otp v-model="otp2" type="filled" />
    </div>
    <div>
      <p>Underlined</p>
      <el-input-otp v-model="otp3" type="underlined" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
const otp3 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

Example 4 (vue):
```vue
<template>
  <div class="demo-input-otp">
    <div>
      <p>Large</p>
      <el-input-otp v-model="otp1" size="large" />
    </div>
    <div>
      <p>Default</p>
      <el-input-otp v-model="otp2" size="default" />
    </div>
    <div>
      <p>Small</p>
      <el-input-otp v-model="otp3" size="small" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const otp1 = ref('')
const otp2 = ref('')
const otp3 = ref('')
</script>

<style scoped>
.demo-input-otp {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

p {
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
```

---
