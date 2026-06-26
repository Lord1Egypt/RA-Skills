# 传统前端维护模式

## 命名空间

```javascript
var App = App || {};
App.UserModule = (function ($) {
  "use strict";

  function init() {
    bindEvents();
    loadData();
  }

  function bindEvents() {
    $(document).on("click", ".js-submit-btn", handleSubmit);
  }

  return { init: init };
})(jQuery);
```

## 事件与 DOM

- 事件触发元素用 `.js-*` class，与样式 class 分离。
- 缓存频繁使用的选择器。
- 批量 DOM 操作用 `DocumentFragment` 或一次性插入。
- 页面卸载或模块销毁时解绑事件或调用插件 destroy。

## Ajax

```javascript
function fetchUserList(params) {
  return $.ajax({
    url: "/api/v1/users",
    method: "GET",
    data: params,
    dataType: "json",
  })
    .done(function (res) {
      if (res.code === 0) renderList(res.data);
      else showError(res.message);
    })
    .fail(function () {
      showError("网络错误，请稍后重试");
    })
    .always(function () {
      hideLoading();
    });
}
```

## XSS 转义

```javascript
$(".username").text(userData.name);

function escapeHtml(str) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}
```

## 文件组织

```text
project/
├── css/
│   ├── common.css
│   └── pages/user-list.css
├── js/
│   ├── lib/jquery.min.js
│   ├── common/utils.js
│   └── pages/user-list.js
└── pages/
```

## 检查清单

- 没有全局变量泄漏。
- 事件绑定在合理容器上。
- Ajax 处理 loading/error/empty。
- 用户输入已转义。
- 未扩大第三方库或框架依赖。
