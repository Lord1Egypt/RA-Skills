---
name: "dark-mode"
description: "暗黑模式指南 -- Element Plus Vue3 桌面端组件。Invoke when user needs 暗黑模式指南 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/dark-mode.html"
---

---

# 暗黑模式 2.2.0 [​](#暗黑模式)

现在，Element Plus 终于支持了暗黑模式！

我们提取并整理了所有的设计变量，并通过 CSS Vars 技术实现动态更新主题。

## 如何启用？ [​](#如何启用)

首先你可以创建一个开关来控制 `暗黑模式` 的 class 类名。

> 如果您只需要暗色模式，只需在 html 上添加一个名为 `dark` 的类 。

html

```
<html class="dark">
  <head></head>
  <body></body>
</html>
```

> 如果您想动态切换，建议使用 [useDark | VueUse](https://vueuse.org/core/useDark/)。

只需要如下在项目入口文件修改一行代码：

main.ts

ts

```
// if you just want to import css
import 'element-plus/theme-chalk/dark/css-vars.css'
```

> 也可以参考我们提供的 [element-plus-vite-starter 模版](https://github.com/element-plus/element-plus-vite-starter) 例子。

## 自定义变量 [​](#自定义变量)

### 通过 CSS [​](#通过-css)

直接覆盖对应的 css 变量即可

像这样，新建一个 `styles/dark/css-vars.css`文件:

css

```
html.dark {
  /* 自定义深色背景颜色 */
  --el-bg-color: #626aef;
}
```

在 Element Plus 的样式之后导入它

main.ts

ts

```
import 'element-plus/theme-chalk/dark/css-vars.css'
import './styles/dark/css-vars.css'
```

### 通过 SCSS [​](#通过-scss)

如果您使用 scss，您也可以导入 scss 文件来实现一样的效果

> 您可以参考 [自定义主题](https://element-plus.org/zh-CN/guide/theming) 获取更多信息。

styles/element/index.scss

scss

```
/*just override what you need*/
@forward 'element-plus/theme-chalk/src/dark/var.scss' with (
  $bg-color: (
    'page': #0a0a0a,
    '': #626aef,
    'overlay': #1d1e1f,
  )
);
```

main.ts

ts

```
import './styles/element/index.scss'

// or just want to import scss?
// import 'element-plus/theme-chalk/src/dark/css-vars.scss'
```

[主题](https://element-plus.org/zh-CN/guide/theming)

[自定义命名空间](https://element-plus.org/zh-CN/guide/namespace)


