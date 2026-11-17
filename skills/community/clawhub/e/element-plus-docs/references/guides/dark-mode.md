## 暗黑模式 2.2.0 ​

**URL:** https://element-plus.org/zh-CN/guide/dark-mode

**Contents:**
- 暗黑模式 2.2.0 ​
- 如何启用？ ​
- 自定义变量 ​
  - 通过 CSS ​
  - 通过 SCSS ​
  - Contents
    - 链接
    - 社区

现在，Element Plus 终于支持了暗黑模式！

我们提取并整理了所有的设计变量，并通过 CSS Vars 技术实现动态更新主题。

首先你可以创建一个开关来控制 暗黑模式 的 class 类名。

如果您只需要暗色模式，只需在 html 上添加一个名为 dark 的类 。

如果您想动态切换，建议使用 useDark | VueUse。

也可以参考我们提供的 element-plus-vite-starter 模版 例子。

像这样，新建一个 styles/dark/css-vars.css文件:

在 Element Plus 的样式之后导入它

如果您使用 scss，您也可以导入 scss 文件来实现一样的效果

**Examples:**

Example 1 (html):
```html
<html class="dark">
  <head></head>
  <body></body>
</html>
```

Example 2 (python):
```python
// if you just want to import css
import 'element-plus/theme-chalk/dark/css-vars.css'
```

Example 3 (sass):
```sass
html.dark {
  /* 自定义深色背景颜色 */
  --el-bg-color: #626aef;
}
```

Example 4 (unknown):
```unknown
import 'element-plus/theme-chalk/dark/css-vars.css'
import './styles/dark/css-vars.css'
```

---
