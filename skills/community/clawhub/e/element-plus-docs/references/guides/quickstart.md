## 快速开始 ​

**URL:** https://element-plus.org/zh-CN/guide/quickstart

**Contents:**
- 快速开始 ​
- 用法 ​
  - 完整引入 ​
    - Volar 支持 ​
  - 按需导入 ​
    - 自动导入 推荐 ​
    - Nuxt ​
  - 手动导入 ​
- 快捷搭建项目模板 ​
- 全局配置 ​

本节将介绍如何在项目中使用 Element Plus。

如果你对打包后的文件大小不是很在乎，那么使用完整导入会更方便。

如果您使用 Volar，请在 tsconfig.json 中通过 compilerOptions.type 指定全局组件类型。

首先你需要安装unplugin-vue-components 和 unplugin-auto-import这两款插件

然后把下列代码插入到你的 Vite 或 Webpack 的配置文件中

想了解更多打包 (Rollup, Vue CLI) 和配置工具，请参考 unplugin-vue-components 和 unplugin-auto-import。

对于 Nuxt 用户，只需要安装 @element-plus/nuxt 即可。

Element Plus 提供了基于 ES Module 的开箱即用的 Tree Shaking 功能。

但你需要安装 unplugin-element-plus 来导入样式。 配置文档参考 docs.

对于Nuxt 用户，我们有一个 Nuxt 模板。

对于 Laravel 用户，我们也准备了 Laravel 模板。

在引入 ElementPlus 时，可以传入一个包含 size 和 zIndex 属性的全局配置对象。 size 用于设置表单组件的默认尺寸，zIndex 用于设置弹出组件的层级，zIndex 的默认值为 2000。

您也可以使用 Nuxt.js: 更多详情请参考 Element Plus Nuxt.js 初始化模板。

现在你可以启动项目了。 对于每个组件的用法，请参考单个组件对应的文档。

**Examples:**

Example 1 (sql):
```sql
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

const app = createApp(App)

app.use(ElementPlus)
app.mount('#app')
```

Example 2 (json):
```json
{
  "compilerOptions": {
    // ...
    "types": ["element-plus/global"]
  }
}
```

Example 3 (unknown):
```unknown
$ npm install -D unplugin-vue-components unplugin-auto-import
```

Example 4 (unknown):
```unknown
$ yarn add -D unplugin-vue-components unplugin-auto-import
```

---
