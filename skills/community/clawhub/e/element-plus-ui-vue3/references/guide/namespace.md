---
name: "namespace"
description: "自定义命名空间 -- Element Plus Vue3 桌面端组件。Invoke when user needs 自定义命名空间 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/namespace.html"
---

---

## 自定义命名空间 2.2.0 [​](#自定义命名空间)

TIP

我们提供了 [element-plus-vite-starter 模版](https://github.com/element-plus/element-plus-vite-starter)。 查看代码了解使用方法。

Element Plus 提供的默认命名空间为 `el`。 在特殊情况下，我们需要自定义命名空间。

由于我们使用 sass 书写样式，如果您需要自定义所有命名空间， 我们假定用户使用了 sass 书写样式。

您必须同时设置 `ElConfigProvider` 和 scss `$namespace`。

### 设置 `ElConfigProvider` [​](#设置-elconfigprovider)

使用 `ElConfigProvider` 包装您的根组件。

App.vue

vue

```
<template>
  <el-config-provider namespace="ep">
    <!-- ... -->
  </el-config-provider>
</template>
```

### 设置 SCSS 和 CSS 变量 [​](#设置-scss-和-css-变量)

创建 `styles/element/index.scss`：

styles/element/index.scss

scss

```
// we can add this to custom namespace, default is 'el'
@forward 'element-plus/theme-chalk/src/mixins/config.scss' with (
  $namespace: 'ep'
);
// ...
```

在 `vite.config.ts` 中导入 `styles/element/index.scss`：

> Webpack也是如此，它需要在 `preprocessorOptions` 中设置。

vite.config.ts

ts

```
import { defineConfig } from 'vite'
// https://vitejs.dev/config/
export default defineConfig({
  // ...
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "~/styles/element/index.scss" as *;`,
      },
    },
  },
  // ...
})
```

就这么简单。

[暗黑模式](https://element-plus.org/zh-CN/guide/dark-mode)

[自定义默认值](https://element-plus.org/zh-CN/guide/custom-defaults)


