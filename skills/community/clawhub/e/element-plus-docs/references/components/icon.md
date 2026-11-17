## Icon 图标 ​

**URL:** https://element-plus.org/zh-CN/component/icon

**Contents:**
- Icon 图标 ​
- 使用图标 ​
- 安装 ​
  - 使用包管理器 ​
- 选择一个你喜欢的包管理器 ​
  - 注册所有图标 ​
  - 浏览器直接引入 ​
  - 自动导入 ​
- 基础用法 ​
- 结合 el-icon 使用 ​

Element Plus 提供了一套常用的图标集合。

如果你想像用例一样直接使用，你需要全局注册组件，才能够直接在项目里使用。

如若需要查看所有可用的 SVG 图标请查阅 @element-plus/[email protected]@element-plus/icons-vue@latest 和有关 Icon Collection 的源码 element-plus-icons

您需要从 @element-plus/icons-vue 中导入所有图标并进行全局注册。

直接通过浏览器的 HTML 标签导入 Element Plus，然后就可以使用全局变量 ElementPlusIconsVue了。

根据不同的 CDN 提供商有不同的引入方式， 根据不同的 CDN 提供商有不同的引入方式， 我们在这里以 unpkg 和 jsDelivr 举例。 你也可以使用其它的 CDN 供应商。

我们建议使用 CDN 引入 Element Plus 的用户在链接地址上锁定版本，以免将来 Element Plus 升级时受到非兼容性更新的影响。 锁定版本的方法请查看 unpkg.com。

使用 unplugin-icons 和 unplugin-auto-import 从 iconify 中自动导入任何图标集。 您可以参考此模板。

由于 HTML 标准已经定义了一个名为 menu 的标签，如果你注册的 Menu 无法正常工作，则需要使用别名来渲染图标。

el-icon 为原始的 SVG 图标提供额外的属性，细节如下。

通过添加额外的类名 is-loading，你的图标就可以在 2 秒内旋转 360 度，当然你也可以自己改写想要的动画。

只要你安装了 @element-plus/icons-vue，就可以在任意版本里使用 SVG 图标。

**Examples:**

Example 1 (elixir):
```elixir
$ npm install @element-plus/icons-vue
```

Example 2 (elixir):
```elixir
$ yarn add @element-plus/icons-vue
```

Example 3 (elixir):
```elixir
$ pnpm install @element-plus/icons-vue
```

Example 4 (typescript):
```typescript
// main.ts

// 如果您正在使用CDN引入，请删除下面一行。
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
```

---
