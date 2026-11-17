## Result 结果 ​

**URL:** https://element-plus.org/zh-CN/component/result

**Contents:**
- Result 结果 ​
- 基础用法 ​
- 自定义内容 ​
- API ​
  - Attributes ​
  - 插槽 ​
- 源代码 ​
- 贡献者 ​
  - Contents
    - 链接

Please follow the instructions

Please follow the instructions

Please follow the instructions

Please follow the instructions

Using slot as subtitle

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-row>
    <el-col :sm="12" :lg="6" :xl="4">
      <el-result
        icon="primary"
        title="Primary Tip"
        sub-title="Please follow the instructions"
      >
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6" :xl="4">
      <el-result
        icon="success"
        title="Success Tip"
        sub-title="Please follow the instructions"
      >
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6" :xl="4">
      <el-result
        icon="warning"
        title="Warning Tip"
        sub-title="Please follow the instructions"
      >
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6" :xl="4">
      <el-result
        icon="error"
        title="Error Tip"
        sub-title="Please follow the instructions"
      >
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6" :xl="4">
      <el-result icon="info" title="Info Tip">
        <template #sub-title>
          <p>Using slot as subtitle</p>
        </template>
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
  </el-row>
</template>

<script setup lang="ts"></script>
```

Example 2 (vue):
```vue
<template>
  <el-result title="404" sub-title="Sorry, request error">
    <template #icon>
      <el-image
        src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
      />
    </template>
    <template #extra>
      <el-button type="primary">Back</el-button>
    </template>
  </el-result>
</template>
```

---
