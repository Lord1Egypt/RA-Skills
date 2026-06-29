---
name: "theming"
description: "主题指南 -- Element Plus Vue3 桌面端组件。Invoke when user needs 主题指南 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/theming.html"
---

---

# 自定义主题 [​](#自定义主题)

Element Plus 默认提供一套主题，CSS 命名采用 BEM 的风格，方便使用者覆盖样式。 但是如果需要大规模替换样式，例如： 将主题颜色从蓝色改为橙色或绿色，也许一个个将其覆盖起来不是一个好主意。

我们提供四种方法来改变样式变量。

## 更换主题色 [​](#更换主题色)

以下是自定义主题的一些例子。

-   全部导入：[element-plus-vite-starter](https://github.com/element-plus/element-plus-vite-starter)
-   按需导入：[unplugin-element-plus/examples/vite](https://github.com/element-plus/unplugin-element-plus)

### 通过 SCSS 变量 [​](#通过-scss-变量)

`theme-chalk` 使用SCSS编写而成。 你可以在 [`packages/theme-chalk/src/common/var.scss`](https://github.com/element-plus/element-plus/blob/dev/packages/theme-chalk/src/common/var.scss) 文件中查找SCSS变量。

WARNING

我们使用 sass 模块（[sass:map](https://sass-lang.com/documentation/values/maps)...）和 `@use` 来重构所有的 SCSS 变量。 通过对所有 SCSS 变量使用 `@use`，解决了由 `@import` 造成的重复输出问题。

> [介绍Sass 模块 | CSS-TRICKS](https://css-tricks.com/introducing-sass-modules/)

例如，我们使用 `$colors` 作为 map 来保存不同类型的颜色。

`$notification` 是所有 `notification` 组件的变量的映射。

今后，我们将为每个组件自定义的变量编写文档。 你也可以直接查看源代码 [var.scss](https://github.com/element-plus/element-plus/blob/dev/packages/theme-chalk/src/common/var.scss)。

scss

```
$colors: () !default;
$colors: map.deep-merge(
  (
    'white': #ffffff,
    'black': #000000,
    'primary': (
      'base': #409eff,
    ),
    'success': (
      'base': #67c23a,
    ),
    'warning': (
      'base': #e6a23c,
    ),
    'danger': (
      'base': #f56c6c,
    ),
    'error': (
      'base': #f56c6c,
    ),
    'info': (
      'base': #909399,
    ),
  ),
  $colors
);
```

### 如何覆盖它？ [​](#如何覆盖它)

如果您的项目也使用了 SCSS，可以直接修改 Element Plus 的样式变量。 新建一个样式文件，例如 `styles/element/index.scss`：

WARNING

您应该使用 `@use 'xxx.scss' as *;` 代替 `@import 'xxx.scss';`。

因为 sass 团队说他们最终会删除 `@import` 语法。

> [Sass: @use](https://sass-lang.com/documentation/at-rules/use) vs [Sass: @import](https://sass-lang.com/documentation/at-rules/import)

styles/element/index.scss

scss

```
/* just override what you need */
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $colors: (
    'primary': (
      'base': green,
    ),
  )
);

// If you just import on demand, you can ignore the following content.
// 如果你想导入所有样式:
// @use "element-plus/theme-chalk/src/index.scss" as *;
```

然后在你的项目入口文件中，导入这个样式文件以替换 Element Plus 内置的 CSS：

TIP

在 element-plus scss 文件之前导入`element/index.scss`以避免 sass 混合变量的问题，因为我们需要通过你的自定义变量生成 light-x。

创建一个 `element/index.scss` 文件来合并你的变量和 element-plus 的变量。 （如果你在 TypeScript 中导入了它们，他们将不会被合并）

TIP

除此以外，你应该将你的 scss 文件与 element 变量的 scss 文件区分开来。 如果将它们混合在一起，`element-plus` 每次热更新都需要编译大量的 scss 文件，这将会导致编译速度变慢。

main.ts

ts

```
import { createApp } from 'vue'
import './styles/element/index.scss'
import ElementPlus from 'element-plus'
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus)
```

如果你正在使用vite，并且你想在按需导入时自定义主题。

使用 `scss.additionalData` 来编译所有应用 scss 变量的组件。

vite.config.ts

ts

```
import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// 也可以使用 unplugin-vue-components
// import Components from 'unplugin-vue-components/vite'
// import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
// 或使用 unplugin-element-plus
import ElementPlus from 'unplugin-element-plus/vite'

export default defineConfig({
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "~/styles/element/index.scss" as *;`,
      },
    },
  },
  plugins: [
    vue(),
    // 使用 unplugin-vue-components
    // Components({
    //   resolvers: [
    //     ElementPlusResolver({
    //       importStyle: "sass",
    //       // directives: true,
    //       // version: "2.1.5",
    //     }),
    //   ],
    // }),
    // 或使用 unplugin-element-plus
    ElementPlus({
      useSource: true,
    }),
  ],
})
```

如果您正在使用 webpack，并且需要在按需导入时自定义主题。

webpack.config.js

js

```
// 使用 unplugin-element-plus

import ElementPlus from 'unplugin-element-plus/webpack'

export default defineConfig({
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@use "~/styles/element/index.scss" as *;`,
      },
    },
  },
  plugins: [
    ElementPlus({
      useSource: true,
    }),
  ],
})
```

### 通过 CSS 变量设置 [​](#通过-css-变量设置)

CSS 变量是一个非常有用的功能，几乎所有浏览器都支持。 （IE：啊这？)

> 从 [使用CSS自定义属性(变量) | MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) 了解更多信息

我们用 css 变量来重构了几乎所有组件的样式系统。

TIP

它兼容 SCSS 变量系统。 我们使用 SCSS 的函数自动生成需要用到的 css 变量。

这意味着你可以动态地改变组件内的个别变量，以便更好地自定义组件样式，而不需要修改 SCSS 文件重新编译一次。

> 之后，每个组件的 css 变量名称和作用将被写入到对应的组件文档中。

就像这样：

css

```
:root {
  --el-color-primary: green;
}
```

如果你只想自定义一个特定的组件，只需为某些组件单独添加内联样式。

html

```
<el-tag style="--el-tag-bg-color: red">Tag</el-tag>
```

出于性能原因，更加推荐你在类名下添加自定义 css 变量，而不是在全局的 `:root` 下。

css

```
.custom-class {
  --el-tag-bg-color: red;
}
```

如果您想要通过 js 控制 css 变量，可以这样做：

ts

```
// document.documentElement 是全局变量时
const el = document.documentElement
// const el = document.getElementById('xxx')

// 获取 css 变量
getComputedStyle(el).getPropertyValue(`--el-color-primary`)

// 设置 css 变量
el.style.setProperty('--el-color-primary', 'red')
```

如果你想要更优雅的方式，请看这里。 [useCssVar | VueUse](https://vueuse.org/core/usecssvar/)

[从 Element UI 升级](https://element-plus.org/zh-CN/guide/migration)

[暗黑模式](https://element-plus.org/zh-CN/guide/dark-mode)


