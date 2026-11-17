## 自定义默认值 ​

**URL:** https://element-plus.org/zh-CN/guide/custom-defaults

**Contents:**
- 自定义默认值 ​
- 基础用法 ​
  - Contents
    - 链接
    - 社区

通过提前配置默认值，您可以减少重复的prop声明并保持模板更干净和更一致。

您可以使用组件提供的静态setPropsDefaults方法自定义组件的属性默认值。

请注意，默认自定义仅适用于声明式组件 并且 必须在组件初始化之前执行。

配置的默认值是全局的。 一旦设置，它们将应用于注册了该组件的所有Vue应用程序。

组件首次渲染后，其默认值将变为不可变，无法再更改。

不建议为其他组件内部使用的组件设置默认值。

**Examples:**

Example 1 (sql):
```sql
import { ElButton } from 'element-plus'

ElButton.setPropsDefaults({
  type: 'primary',
  size: 'small',
})
```

Example 2 (vue):
```vue
<template>
  <el-button>Hello</el-button>
  <el-button type="primary" size="small">Hello</el-button>
</template>
```

Example 3 (css):
```css
// 这将导致 el-autocomplete 组件的行为发生改变。
ElInput.setPropsDefaults({ maxlength: 1 })
```

---
