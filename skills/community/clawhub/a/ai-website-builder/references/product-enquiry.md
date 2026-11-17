# 产品询盘页面（Product Enquiry）说明

## 一、功能概述

产品询盘页用于让访客提交一个或多个产品的询价、采购或咨询信息。页面由两个不可缺少的部分组成：

1. **询盘产品列表**：展示当前准备询盘的产品，支持修改数量、查看规格和删除产品。
2. **自定义询盘表单**：通过 `FnGetCustomForm(表单ID)` 加载后台配置的联系人、电话、邮箱、备注、附件等字段。

两部分通过固定字段 `EnquiryProduct` 连接。提交时，产品列表被序列化为 JSON 字符串，与自定义表单的其它字段一起提交给后台。

完整可复制代码见：[`product-enquiry-democode.md`](product-enquiry-democode.md)。

自定义表单的字段类型、上传、短信/邮箱验证码、地区联动、图形验证码和 AJAX 提交逻辑必须以 [`customform-democode-base.md`](customform-democode-base.md) 为基础。询盘页只增加产品列表和 `EnquiryProduct` 业务逻辑，不要删除基础示例中的校验和提交代码。

## 二、部署前准备

### 1. 获取真实的自定义表单 ID

询盘表单必须先在后台创建，然后在开发或部署时调用 MCP 工具获取当前站点的真实表单 ID：

```text
MCP: get_enquiry_form_id
```

返回的整数用于：

```twig
{% set form = FnGetCustomForm(真实表单ID) %}
```

不同站点的表单 ID 可能不同。文档和完整示例中的数字只能作为占位值，不能直接部署。若工具返回为空，先在后台创建名称明确的“产品询盘”自定义表单。

### 2. 需要按站点替换的内容

- `FnGetCustomForm(...)` 中的表单 ID。
- 询盘页实际 URL，例如 `/enquiry.html`。
- 站点页头、页尾的实际模板引用方式。
- 站点已有的 CSS 变量和基础组件类名。

## 三、接收 URL 参数

所有产品详情页、产品列表页和询盘车入口都应使用统一参数打开询盘页，不要分别定义私有参数。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `pid` | 产品 ID。`mode=single` 时使用 | 无 |
| `num` | 初始询盘数量 | `1` |
| `skutext` | 已选规格文本，例如 `颜色:红色;尺寸:XL` | 空字符串 |
| `mode` | `single` 表示处理 URL 中的单个产品；`cart` 表示直接读取询盘车 | `single` |
| `from` | `back` 原窗口返回；`blank` 新窗口打开；`popup` 弹窗打开 | `back` |

示例：

```text
/enquiry.html?pid=123&num=2&skutext=%E9%A2%9C%E8%89%B2%3A%E7%BA%A2%E8%89%B2%3B%E5%B0%BA%E5%AF%B8%3AXL&mode=single&from=back
```

模板中通过 `request.get` 读取：

```twig
{% set pid = request.get.pid %}
{% set mode = request.get.mode|default('single') %}
{% set fromParam = request.get.from|default('back') %}
```

参数编码由打开询盘页的统一 JavaScript 函数完成。浏览器的 `URLSearchParams.get()` 已经返回解码后的值，读取 `skutext` 后不要再次调用 `decodeURIComponent`，否则中文或 `%` 可能被错误处理。

推荐的统一入口：

```javascript
function openEnquiry(opts) {
  opts = opts || {};
  var mode = opts.mode || 'single';
  var from = opts.from || 'back';
  var params = [];

  if (mode === 'single' && opts.pid) {
    params.push('pid=' + encodeURIComponent(String(opts.pid)));
  }
  params.push('num=' + encodeURIComponent(String(opts.num || 1)));
  if (opts.skutext) {
    params.push('skutext=' + encodeURIComponent(String(opts.skutext)));
  }
  params.push('mode=' + encodeURIComponent(mode));
  params.push('from=' + encodeURIComponent(from));

  var url = '/enquiry.html?' + params.join('&');
  if (from === 'popup') {
    var width = 900;
    var height = 720;
    var left = Math.max(0, (screen.width - width) / 2);
    var top = Math.max(0, (screen.height - height) / 2);
    window.open(url, 'enquiryPopup', 'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top);
  } else if (from === 'blank') {
    window.open(url, '_blank');
  } else {
    window.location.href = url;
  }
}
```

调用示例：

```html
<button type="button" onclick="openEnquiry({pid: 123})">立即询盘</button>
<button type="button" onclick="openEnquiry({pid: 123, from: 'popup'})">弹窗询盘</button>
<button type="button" onclick="openEnquiry({mode: 'cart', from: 'blank'})">批量询盘</button>
```

## 四、加载产品数据

### 1. 单产品模式

当 `mode=single` 且存在 `pid` 时，模板服务端调用：

```twig
{% set urlProduct = null %}
{% if request.get.pid %}
  {% set urlProduct = FnGetOnePro(request.get.pid) %}
{% endif %}
```

常用字段：

| 字段 | 用途 |
|------|------|
| `ProductID` | 唯一产品 ID |
| `Name` | 产品名称 |
| `ImgBig` | 默认大图 |
| `ImgSmall` | 默认小图，可作为图片回退 |

产品不存在时不要生成产品项，也不要写入 Storage。页面应显示“产品不存在”或空询盘列表状态。

### 2. 从 Twig 注入 JavaScript

产品名称、图片、规格等内容不能直接拼接进 JavaScript 字符串。使用 `json_encode|raw` 注入：

```twig
{% if urlProduct and urlProduct.ProductID %}
<script>
window.__INIT_ENQUIRY_ITEM__ = {
  productID: {{ urlProduct.ProductID|json_encode|raw }},
  name: {{ urlProduct.Name|json_encode|raw }},
  image: {{ (urlProduct.ImgBig|default(urlProduct.ImgSmall|default('')))|json_encode|raw }},
  num: {{ (request.get.num|default('1'))|json_encode|raw }},
  skutext: {{ (request.get.skutext|default(''))|json_encode|raw }}
};
</script>
{% endif %}
```

这样可以正确处理中文、引号、换行和特殊字符。

### 3. 批量询盘模式

当 `mode=cart` 时不需要再次调用 `FnGetOnePro`。页面直接读取浏览器中的 `enquiryCart`，并渲染已有产品。

## 五、`EnquiryProduct` 数据结构

提交字段名固定为 `EnquiryProduct`，字段值是 JSON 数组的字符串：

```json
[
  {
    "name": "产品名称",
    "image": "/comdata/站点ID/product/example.jpg",
    "productID": "123",
    "num": "2",
    "skutext": "颜色:红色;尺寸:XL"
  }
]
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 产品名称 |
| `image` | 否 | 产品图片路径，通常取 `ImgBig` |
| `productID` | 是 | 产品 ID，作为去重和后台关联依据 |
| `num` | 否 | 正数数量，缺省时使用 `1` |
| `skutext` | 否 | 已选规格文本，没有规格时为空字符串 |

模板中必须增加：

```html
<input type="hidden" name="EnquiryProduct" id="EnquiryProductField" value="">
```

`EnquiryProduct` 是业务必填字段。提交前必须解析 JSON，并确认它是非空数组；每一项至少要有 `productID`、`name` 和大于 0 的 `num`。

## 六、写入和维护 Storage

统一使用：

```javascript
var STORAGE_KEY = 'enquiryCart';
```

建议封装读写函数并处理隐私模式、浏览器禁用 Storage 或数据损坏：

```javascript
function getCart() {
  try {
    var value = localStorage.getItem(STORAGE_KEY);
    var cart = value ? JSON.parse(value) : [];
    return Array.isArray(cart) ? cart : [];
  } catch (error) {
    return [];
  }
}

function saveCart(cart) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    return true;
  } catch (error) {
    return false;
  }
}
```

初始化规则：

1. `mode=single` 且有有效初始产品时，读取当前询盘车。
2. 以字符串形式比较 `productID`，避免数字和字符串导致重复。
3. 已存在同一产品时更新数量、规格、名称和图片，不重复追加。
4. 不存在时追加新项。
5. `mode=cart` 不追加 URL 产品，只渲染现有询盘车。

每次数量修改、删除产品或重新渲染列表后，都要把最新数组同步到 `EnquiryProduct` hidden 字段。

提交成功后清空：

```javascript
localStorage.removeItem(STORAGE_KEY);
```

提交失败或网络异常时不要清空，避免用户重新填写产品。

## 七、渲染产品列表

产品列表由 JavaScript 从 Storage 动态生成，至少展示：

- 图片
- 产品名称
- 规格文本
- 数量输入框
- 删除按钮

推荐使用 DOM API 创建元素，并通过 `textContent`、`setAttribute` 设置动态值，不要把产品名称、规格和图片地址直接拼接到 `innerHTML`。数量修改时应将非法值归一化为 `1`，再保存并重新渲染。删除后重新读取 Storage，删除对应索引，再同步 hidden 字段。

空列表时显示提示，并在提交校验中阻止空询盘。

完整的产品列表实现见 [`product-enquiry-democode.md`](product-enquiry-democode.md) 中“询盘车 Storage 和产品列表”部分。

## 八、渲染自定义表单

表单来源：

```twig
{% set form = FnGetCustomForm(真实表单ID) %}
```

表单必须保留这些隐藏字段：

```html
<input type="hidden" name="submitType" value="ajax">
<input type="hidden" name="FormID" value="{{ form.form.ID }}">
<input type="hidden" name="needValidateCode" value="{{ form.needValidateCode }}">
<input type="hidden" name="submitChecksum" value="{{ form.submitChecksum }}">
<input type="hidden" name="submitFrom" value="customhtml">
<input type="hidden" name="EnquiryProduct" id="EnquiryProductField" value="">
```

字段 `name` 必须继续使用基础示例约定：

- 普通字段：`col{{ field.ID }}`
- 多选字段：`col{{ field.ID }}[]`
- 上传文件：`file_{{ field.ID }}` 或 `file_{{ field.ID }}[]`
- 短信/邮箱验证码：`col{{ field.ID }}_vcode`

只渲染 `field.IsShow == 1` 的字段，并保留 FieldType 1 至 15 的处理。其中 FieldType 13（公司名）、14（姓名）、15（邮箱）虽然具有明确业务语义，实际均按单行文本控件渲染。邮箱字段满足 `ValidateType=6 && IsEmailValidate=1` 时，必须显示邮箱验证码输入框并调用邮箱验证码接口。上传字段必须使用 hidden 字段保存上传接口返回的路径，表单提交时不重复提交原始 file input。

完整字段循环、图形验证码、短信/邮箱验证码、地区和上传实现位于 [`product-enquiry-democode.md`](product-enquiry-democode.md)。

## 九、提交表单

提交事件的正确顺序：

1. 阻止默认提交。
2. 重新读取 `enquiryCart`，不要只相信上一次渲染时的 hidden 值。
3. 将最新数组序列化并写入 `EnquiryProduct`。
4. 校验 `EnquiryProduct` 是非空数组。
5. 校验产品 ID、名称和数量。
6. 执行基础自定义表单的必填、格式、单选、多选和文件 hidden 字段校验。
7. 使用 `fetch + FormData` 提交，跳过 `type=file`，只提交已上传文件路径。
8. 禁用提交按钮，防止重复提交。
9. 根据 JSON 响应显示成功或失败信息。
10. 成功后清空询盘车、重置表单、清理上传状态并重新初始化地区选择；失败时保留数据。

表单必须使用：

```html
<form method="post" enctype="multipart/form-data">
```

并携带：

```html
<input type="hidden" name="submitType" value="ajax">
```

不要改为 GET、整页跳转或另写一套 XMLHttpRequest 提交流程。基础示例中的完整校验和 AJAX 逻辑不能删除，只能在提交校验前增加询盘产品校验。

## 十、页面联动与继续浏览

### `from=back`

默认原窗口打开。页面包含站点页头和页尾，点击“继续浏览”优先执行 `history.back()`；没有可返回历史时跳转产品列表页。

### `from=blank`

新窗口打开。页面包含站点页头和页尾，点击“继续浏览”跳转产品列表地址。

### `from=popup`

弹窗打开。页面只渲染询盘主体，不重复输出页头和页尾。点击“继续浏览”尝试 `window.close()`；浏览器禁止脚本关闭窗口时，应提供产品列表跳转或提示作为兜底。

页头页尾是否渲染只能在询盘模板中根据 `request.get.from` 判断一次，入口页面不要各自复制这套逻辑。

## 十一、样式约定

询盘页应复用站点已有的字体、颜色、按钮、输入框、边框和响应式断点。完整示例只提供布局骨架：桌面端左右分栏，移动端上下排列。

用户提供的深色绿金设计可以作为视觉参考，但不应覆盖站点既有设计系统，也不应作为所有站点的强制配色。

## 十二、模板编辑器兼容约定

高级数据接口文档和基础表单示例中的编辑器约定同样适用于询盘页：

1. Twig 标签不能放在 `<html>` 标签之前。
2. 不要在 HTML 标签属性中放置 `{% if %}`、`{% for %}` 等逻辑控制标签。
3. 需要编辑器保留的 Twig 逻辑可使用 `<!---->` 包裹。
4. `<title>` 内不要使用 Twig 逻辑标签。
5. HTML 属性必须保持规范，标签必须正确闭合。
6. 不要为了减少代码而删掉基础示例中的校验脚本。

## 十三、常见问题与排错

### 表单不存在

检查后台是否创建产品询盘表单，以及是否已通过 `get_enquiry_form_id` 获取并替换真实 ID。

### 产品没有进入询盘车

检查 `pid` 是否存在、`FnGetOnePro(pid)` 是否返回有效 `ProductID`，以及浏览器是否允许 `localStorage`。

### 产品重复

确保比较前统一使用 `String(productID)`，并按 `productID` 去重，而不是使用产品名称或数组索引。

### 产品列表有数据但提交为空

提交前重新执行 `getCart()`，将 JSON 写入 `EnquiryProduct`。不要只在页面初次渲染时设置 hidden 字段。

### 文件上传后仍提示必填

检查上传接口是否成功返回 `newfile`，以及返回值是否写入对应的 `col{{ field.ID }}` hidden 字段。

### 多文件上传失败

类型 10 必须调用 `uploadfiles`，所有文件使用相同的 `file_XXX[]` 参数，并额外提交 `count`。

### AJAX 返回解析失败

检查表单 `action`、`submitType=ajax`、`submitChecksum` 和站点接口响应。不要把 HTML 错误页当作 JSON 处理。

## 十四、参考文件

- 完整询盘示例：[`product-enquiry-democode.md`](product-enquiry-democode.md)
- 自定义表单基础示例：[`customform-democode-base.md`](customform-democode-base.md)
- 高级数据接口说明：[`advanced-data-interface.md`](advanced-data-interface.md)
