## 安装 ​

**URL:** https://element-plus.org/zh-CN/guide/installation

**Contents:**
- 安装 ​
- 兼容性2.5.0 ​
  - Sass ​
  - 版本 ​
- 使用包管理器 ​
- 浏览器直接引入 ​
- Hello World ​
  - Contents
    - 链接
    - 社区

Element Plus 支持最近两个版本的浏览器。

如果您需要支持旧版本的浏览器，请自行添加 Babel 和相应的 Polyfill 。

由于 Vue 3 不再支持 IE11，Element Plus 也不再支持 IE 浏览器。

在2.8.5及以后的版本, Sass 的最低支持版本为 1.79.0.

如果您的终端提示 legacy JS API Deprecation Warning，您可以在 vite.config.ts 中配置以下代码：

Element Plus 目前还处于快速开发迭代中。

此外，在dev 分支上的每个提交和 PR 都将被发布到 pkg.pr.new，如果您想要使用一些未发布的内容，您可以参考 这里。

我们建议使用包管理器（NPM、Yarn、PNPM）安装 Element Plus， 这样您就可以使用诸如 Vite 和 Webpack 之类的打包工具。

如果你的网络环境不佳，推荐使用 cnpm 或使用 npmmirror

直接通过浏览器的 HTML 标签导入 Element Plus，然后就可以使用全局变量 ElementPlus 了。

根据不同的 CDN 提供商有不同的引入方式， 我们在这里以 unpkg 和 jsDelivr 举例。 你也可以使用其它的 CDN 供应商。

我们建议使用 CDN 引入 Element Plus 的用户在链接地址上锁定版本，以免将来 Element Plus 升级时受到非兼容性更新的影响。 锁定版本的方法请查看 unpkg.com。

由于原生的 HTML 解析行为的限制，单个闭合标签可能会导致一些例外情况，所以请使用双封闭标签， 参考

通过 CDN 的方式我们可以很容易地使用 Element Plus 写出一个 Hello world 页面。 在线演示

如果是通过包管理器安装，并希望配合打包工具使用，请阅读下一节：快速上手。

**Examples:**

Example 1 (lua):
```lua
import { defineConfig } from 'vite'
// https://vitejs.dev/config/
export default defineConfig({
  // ...
  css: {
    preprocessorOptions: {
      scss: { api: 'modern-compiler' },
    },
  },
  // ...
})
```

Example 2 (unknown):
```unknown
$ npm install element-plus --save
```

Example 3 (unknown):
```unknown
$ yarn add element-plus
```

Example 4 (unknown):
```unknown
$ pnpm install element-plus
```

---
