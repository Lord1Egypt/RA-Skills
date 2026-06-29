---
name: "quickstart"
description: "快速开始 -- Element Plus Vue3 桌面端组件。Invoke when user needs 快速开始 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/quickstart.html"
---

---

# 快速开始 [​](#快速开始)

本节将介绍如何在项目中使用 Element Plus。

## 用法 [​](#用法)

### 完整引入 [​](#完整引入)

如果你对打包后的文件大小不是很在乎，那么使用完整导入会更方便。

main.ts

ts

```
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

const app = createApp(App)

app.use(ElementPlus)
app.mount('#app')
```

#### Volar 支持 [​](#volar-支持)

如果您使用 Volar，请在 `tsconfig.json` 中通过 `compilerOptions.type` 指定全局组件类型。

tsconfig.json

json

```
{
  "compilerOptions": {
    // ...
    "types": ["element-plus/global"]
  }
}
```

### 按需导入 [​](#按需导入)

您需要使用额外的插件来导入要使用的组件。

#### 自动导入 推荐 [​](#自动导入-推荐)

首先你需要安装`unplugin-vue-components` 和 `unplugin-auto-import`这两款插件

npmyarnpnpm

shell

```
$ npm install -D unplugin-vue-components unplugin-auto-import
```

shell

```
$ yarn add -D unplugin-vue-components unplugin-auto-import
```

shell

```
$ pnpm install -D unplugin-vue-components unplugin-auto-import
```

然后把下列代码插入到你的 `Vite` 或 `Webpack` 的配置文件中

vite.config.tswebpack.config.js

ts

```
import { defineConfig } from 'vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  // ...
  plugins: [
    // ...
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
})
```

js

```
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')

module.exports = {
  // ...
  plugins: [
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
}
```

想了解更多打包 ([Rollup](https://rollupjs.org/), [Vue CLI](https://cli.vuejs.org/)) 和配置工具，请参考 [unplugin-vue-components](https://github.com/antfu/unplugin-vue-components#installation) 和 [unplugin-auto-import](https://github.com/antfu/unplugin-auto-import#install)。

#### Nuxt [​](#nuxt)

对于 Nuxt 用户，只需要安装 `@element-plus/nuxt` 即可。

npmyarnpnpm

shell

```
$ npm install -D @element-plus/nuxt
```

shell

```
$ yarn add -D @element-plus/nuxt
```

shell

```
$ pnpm install -D @element-plus/nuxt
```

然后将下面的代码写入你的配置文件.

nuxt.config.ts

ts

```
export default defineNuxtConfig({
  modules: ['@element-plus/nuxt'],
})
```

配置文档参考 [docs](https://github.com/element-plus/element-plus-nuxt#readme).

### 手动导入 [​](#手动导入)

Element Plus 提供了基于 ES Module 的开箱即用的 [Tree Shaking](https://webpack.js.org/guides/tree-shaking/) 功能。

但你需要安装 [unplugin-element-plus](https://github.com/element-plus/unplugin-element-plus) 来导入样式。 配置文档参考 [docs](https://github.com/element-plus/unplugin-element-plus#readme).

App.vue

vue

```
<template>
  <el-button>I am ElButton</el-button>
</template>

<script setup lang="ts">
import { ElButton } from 'element-plus'
</script>
```

vite.config.ts

ts

```
import { defineConfig } from 'vite'
import ElementPlus from 'unplugin-element-plus/vite'

export default defineConfig({
  // ...
  plugins: [ElementPlus()],
})
```

## 快捷搭建项目模板 [​](#快捷搭建项目模板)

我们提供了 [Vite 模板](https://github.com/element-plus/element-plus-vite-starter)。

对于Nuxt 用户，我们有一个 [Nuxt 模板](https://github.com/element-plus/element-plus-nuxt-starter)。

对于 Laravel 用户，我们也准备了 [Laravel 模板](https://github.com/element-plus/element-plus-in-laravel-starter)。

## 全局配置 [​](#全局配置)

在引入 ElementPlus 时，可以传入一个包含 `size` 和 `zIndex` 属性的全局配置对象。 `size` 用于设置表单组件的默认尺寸，`zIndex` 用于设置弹出组件的层级，`zIndex` 的默认值为 `2000`。

完整引入：

main.ts

ts

```
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })
```

按需引入:

App.vue

vue

```
<template>
  <el-config-provider :size="size" :z-index="zIndex">
    <app />
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'

const zIndex = 3000
const size = 'small'
</script>
```

## 使用 Nuxt.js [​](#使用-nuxt-js)

您也可以使用 [Nuxt.js](https://nuxt.com/): 更多详情请参考 [Element Plus Nuxt.js 初始化模板](https://github.com/element-plus/element-plus-nuxt-starter)。

## 开始使用 [​](#开始使用)

现在你可以启动项目了。 对于每个组件的用法，请参考单个组件对应的文档。

[安装](https://element-plus.org/zh-CN/guide/installation)

[国际化](https://element-plus.org/zh-CN/guide/i18n)


