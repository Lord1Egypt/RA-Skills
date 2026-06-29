---
name: "installation"
description: "安装 -- Element UI Vue2 桌面端组件。Invoke when user needs 安装 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/installation"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/installation#an-zhuang) 安装

### [¶](https://element.eleme.cn/#/zh-CN/component/installation#npm-an-zhuang) npm 安装

推荐使用 npm 的方式安装，它能更好地和 [webpack](https://webpack.js.org/) 打包工具配合使用。

```shell
npm i element-ui -S
```

### [¶](https://element.eleme.cn/#/zh-CN/component/installation#cdn) CDN

目前可以通过 [unpkg.com/element-ui](https://unpkg.com/element-ui/) 获取到最新版本的资源，在页面上引入 js 和 css 文件即可开始使用。

```html
<!-- 引入样式 -->
<link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
<!-- 引入组件库 -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
```

我们建议使用 CDN 引入 Element 的用户在链接地址上锁定版本，以免将来 Element 升级时受到非兼容性更新的影响。锁定版本的方法请查看 [unpkg.com](https://unpkg.com/)。

### [¶](https://element.eleme.cn/#/zh-CN/component/installation#hello-world) Hello world

通过 CDN 的方式我们可以很容易地使用 Element 写出一个 Hello world 页面。[在线演示](https://codepen.io/bofeng/pen/poaEmJY)

如果是通过 npm 安装，并希望配合 webpack 使用，请阅读下一节：[快速上手](https://element.eleme.cn/#/zh-CN/component/quickstart)。

更新日志 快速上手


