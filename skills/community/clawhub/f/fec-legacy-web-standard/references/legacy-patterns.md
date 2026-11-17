# Traditional front-end maintenance mode

## Namespace

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

## Events and DOM

- Event triggering elements use `.js-*` classes, separated from style classes.
- Cache frequently used selectors.
- Batch DOM manipulation with `DocumentFragment` or one-time insertion.
- Unbind the event or call the plug-in destroy when the page is unloaded or the module is destroyed.

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
      showError("Network error, please try again later");
    })
    .always(function () {
      hideLoading();
    });
}
```

## XSS escaping

```javascript
$(".username").text(userData.name);

function escapeHtml(str) {
  var div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}
```

## File organization

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

## Checklist

- No global variables leaked.
- Events are bound to reasonable containers.
- Ajax handling loading/error/empty.
- User input is escaped.
- No third-party library or framework dependencies have been expanded.
