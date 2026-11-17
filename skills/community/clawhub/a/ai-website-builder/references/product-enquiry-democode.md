# 产品询盘完整示例代码

### 注意事项1：请务必保留此示例代码中的检验和提交表单的JS，否能表单可能无法提交
### 注意事项2：验证码输入框的样式要与表单中其它输入框的样式保持一至

## 使用说明

这是一份可复制后再按站点调整的完整 Twig 示例。它包含：

- URL 参数接收和单产品加载
- `FnGetOnePro` 产品数据注入
- `localStorage` 询盘车
- 产品列表渲染、数量修改和删除
- `EnquiryProduct` hidden 字段同步
- 自定义表单 FieldType 1 至 15，其中 13/14/15 按单行文本渲染
- 图片验证码、短信/邮箱验证码、地区三级联动和文件上传
- 基础自定义表单校验和 AJAX 提交
- `back`、`blank`、`popup` 三种打开方式

部署前必须替换：

1. `FnGetCustomForm(1516)` 中的示例表单 ID。请先调用 `get_enquiry_form_id` 获取真实 ID。
2. `/enquiry.html` 为站点实际询盘页地址。
3. 页头、页尾的实际模板引用方式。
4. 产品列表地址和站点 CSS 变量。

示例中的字段渲染和表单提交逻辑来源于 `customform-democode-base.md`。不要删除基础校验、上传和 AJAX 代码。

```twig
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>产品询盘</title>
  <style>
    /* 这里只提供布局骨架，实际项目应换成站点已有设计变量。 */
    :root {
      --primary: #1677ff;
      --surface: #ffffff;
      --border: #e5e7eb;
      --text: #1f2937;
      --muted: #6b7280;
      --radius: 8px;
    }
    * { box-sizing: border-box; }
    body { margin: 0; color: var(--text); font: 14px/1.6 Arial, "Microsoft YaHei", sans-serif; background: #f7f8fa; }
    img { max-width: 100%; display: block; }
    button, input, select, textarea { font: inherit; }
    button { cursor: pointer; }
    .enquiry-page { max-width: 1200px; margin: 0 auto; padding: 32px 16px; }
    .enquiry-layout { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; align-items: start; }
    .enquiry-products, .enquiry-form-wrap { padding: 24px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); }
    .enquiry-title, .title { margin: 0 0 20px; font-size: 20px; }
    .enquiry-empty, .form-empty { padding: 24px 0; color: var(--muted); text-align: center; }
    .enquiry-item { display: grid; grid-template-columns: 80px minmax(0, 1fr) auto; gap: 12px; padding: 16px 0; border-bottom: 1px solid var(--border); }
    .enquiry-item:first-child { padding-top: 0; }
    .ei-img { width: 80px; height: 80px; object-fit: cover; border-radius: 6px; background: #f1f5f9; }
    .ei-noimg { display: flex; align-items: center; justify-content: center; color: var(--muted); font-size: 12px; }
    .ei-name { font-weight: 600; overflow-wrap: anywhere; }
    .ei-sku { margin-top: 4px; color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
    .ei-num { display: flex; align-items: center; gap: 6px; margin-top: 10px; color: var(--muted); }
    .ei-num-input { width: 72px; padding: 4px 6px; border: 1px solid var(--border); border-radius: 4px; }
    .ei-del, .continue-btn { color: var(--primary); background: transparent; border: 0; }
    .form-fields-list { display: grid; gap: 16px; }
    .form-field-item { min-width: 0; }
    .field-label { margin: 0 0 6px; font-weight: 600; }
    .field-icon { display: inline-block; width: 16px; height: 16px; margin-right: 4px; vertical-align: -3px; object-fit: contain; }
    .required { margin-left: 4px; color: #dc2626; }
    .field-input, .radio-group, .checkbox-group, .file-operation, .verify-code-box, .static-text { margin: 0; }
    .form-input, .form-textarea, .form-select, .form-datetime, .sms-code, .email-code, .verify-input { width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 6px; background: #fff; }
    .form-textarea { min-height: 110px; resize: vertical; }
    .radio-group, .checkbox-group { display: flex; flex-wrap: wrap; gap: 10px 16px; }
    .radio-item, .checkbox-item { display: inline-flex; align-items: center; gap: 5px; }
    .area-select-group, .sms-validate-box, .email-validate-box, .verify-code-box { display: flex; flex-wrap: wrap; gap: 8px; }
    .area-select-group .form-select { flex: 1 1 140px; }
    .sms-validate-box { margin-top: 8px; }
    .email-validate-box { margin-top: 8px; }
    .sms-code, .email-code { flex: 1 1 160px; }
    .sms-btn, .upload-btn, .browse-file, .refresh-btn { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; padding: 0 12px; color: var(--primary); background: #fff; border: 1px solid var(--primary); border-radius: 6px; }
    .email-btn { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; padding: 0 12px; color: var(--primary); background: #fff; border: 1px solid var(--primary); border-radius: 6px; }
    .file-operation { display: flex; align-items: center; flex-wrap: wrap; gap: 10px; }
    .verify-img { width: 145px; height: 50px; object-fit: contain; border: 1px solid var(--border); }
    .upload-status { color: var(--muted); }
    .static-text { color: var(--muted); }
    .submit-btn-box { display: flex; justify-content: flex-end; gap: 12px; padding-top: 8px; }
    .submit-btn { min-height: 40px; padding: 0 22px; color: #fff; background: var(--primary); border: 1px solid var(--primary); border-radius: 6px; }
    .submit-btn:disabled { cursor: wait; opacity: .65; }
    @media (max-width: 768px) {
      .enquiry-layout { grid-template-columns: 1fr; }
      .enquiry-products, .enquiry-form-wrap { padding: 16px; }
    }
  </style>
</head>
<body>

{# -------------------- 1. 读取页面参数和产品 -------------------- #}
{% set fromParam = request.get.from|default('back') %}
{% set modeParam = request.get.mode|default('single') %}
{% set urlProduct = null %}
{% if modeParam == 'single' and request.get.pid %}
  {% set urlProduct = FnGetOnePro(request.get.pid) %}
{% endif %}

{# 独立页面显示站点页头；弹窗只显示询盘主体。按站点实际模板修改 include。 #}
{% if fromParam != 'popup' %}
  {# {% include 'site-header.twig' %} #}
{% endif %}

<main class="enquiry-page">
  <div class="enquiry-layout">
    <section class="enquiry-products" aria-labelledby="enquiryProductsTitle">
      <h1 class="enquiry-title" id="enquiryProductsTitle">询盘产品</h1>
      <div id="enquiryProductList" aria-live="polite">
        <p class="enquiry-empty" id="enquiryEmpty">暂无询盘产品</p>
      </div>
    </section>

    <section class="enquiry-form-wrap">
      {# 1516 只是占位值，部署前必须替换为 MCP 返回的真实表单 ID。 #}
      {% set form = FnGetCustomForm(1516) %}
      {% set formID = form.form.ID|default(0) %}

      {% if form and form.fields %}
      <form id="customForm{{ form.form.ID }}" action="{{ form.action }}" method="post" enctype="multipart/form-data">
        {# 这些字段是自定义表单 AJAX 提交协议的一部分，不能删除。 #}
        <input type="hidden" name="submitType" value="ajax">
        <input type="hidden" name="FormID" value="{{ form.form.ID }}">
        <input type="hidden" name="needValidateCode" value="{{ form.needValidateCode }}">
        <input type="hidden" name="submitChecksum" value="{{ form.submitChecksum }}">
        <input type="hidden" name="submitFrom" value="customhtml">

        {# 询盘新增业务字段，JS 会在初始化、修改列表和提交前同步它。 #}
        <input type="hidden" name="EnquiryProduct" id="EnquiryProductField" value="">

        {% if form.form.Name %}
          <h2 class="title">{{ form.form.Name }}</h2>
        {% endif %}

        <div class="form-fields-list">
          {% for field in form.fields %}
            {% if field.IsShow == 1 %}

              {% if field.FieldType == 1 or field.FieldType == 13 or field.FieldType == 14 or field.FieldType == 15 %}
              <div class="form-field-item">
                <p class="field-label">
                  {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" alt="">{% endif %}
                  {{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input">
                  <input type="text" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" placeholder="{{ field.Placeholder }}" class="form-input">
                  {% if field.ValidateType == 3 and field.IsSmsValidate == 1 %}
                  <span class="sms-validate-box">
                    <input class="sms-code" name="col{{ field.ID }}_vcode" placeholder="请输入验证码" required>
                    <button class="sms-btn" type="button">获取验证码</button>
                  </span>
                  {% endif %}
                  {% if field.ValidateType == 6 and field.IsEmailValidate == 1 %}
                  <span class="email-validate-box">
                    <input class="email-code" name="col{{ field.ID }}_vcode" placeholder="请输入验证码" required>
                    <button class="email-btn" type="button">获取验证码</button>
                  </span>
                  {% endif %}
                </p>
              </div>

              {% elseif field.FieldType == 2 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="field-input">
                  <textarea class="form-textarea" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" placeholder="{{ field.Placeholder }}" rows="5"></textarea>
                </p>
              </div>

              {% elseif field.FieldType == 3 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="radio-group">
                  {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
                  <label class="radio-item">
                    <input type="radio" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" value="{{ fieldValue }}">
                    <span>{{ fieldValue }}</span>
                  </label>
                  {% endfor %}
                </p>
              </div>

              {% elseif field.FieldType == 4 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="field-input">
                  <select name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" class="form-select">
                    <option value="">请选择</option>
                    {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}<option value="{{ fieldValue }}">{{ fieldValue }}</option>{% endfor %}
                  </select>
                </p>
              </div>

              {% elseif field.FieldType == 5 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="checkbox-group">
                  {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
                  <label class="checkbox-item">
                    <input type="checkbox" name="col{{ field.ID }}[]" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" value="{{ fieldValue }}">
                    <span>{{ fieldValue }}</span>
                  </label>
                  {% endfor %}
                </p>
              </div>

              {% elseif field.FieldType == 6 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="file-operation">
                  <label class="upload-btn" for="file{{ form.form.ID }}_{{ field.ID }}">选择图片</label>
                  <input type="file" accept="image/*" class="form-file" id="file{{ form.form.ID }}_{{ field.ID }}" name="file_{{ field.ID }}" style="display:none">
                  <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}">
              </div>

              {% elseif field.FieldType == 7 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="field-input area-select-group">
                  <select id="form{{ form.form.ID }}_selProvince{{ field.ID }}" name="selProvince" class="form-select area-province"><option value="">选择省份</option></select>
                  <select id="form{{ form.form.ID }}_selCity{{ field.ID }}" name="selCity" class="form-select area-city"><option value="">选择城市</option></select>
                  <select id="form{{ form.form.ID }}_selArea{{ field.ID }}" name="selArea" class="form-select area-county"><option value="">选择区县</option></select>
                  <input type="hidden" id="form{{ form.form.ID }}_region{{ field.ID }}" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" class="form-region">
                </p>
              </div>

              {% elseif field.FieldType == 8 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="field-input"><input type="text" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" placeholder="{{ field.Placeholder|default('请选择时间') }}" class="form-datetime"></p>
              </div>

              {% elseif field.FieldType == 9 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="file-operation">
                  <label class="browse-file" for="file_{{ field.ID }}">选择文件</label>
                  <input type="file" class="form-file-upload" id="file_{{ field.ID }}" name="file_{{ field.ID }}" style="display:none">
                  <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}">
              </div>

              {% elseif field.FieldType == 10 %}
              <div class="form-field-item">
                <p class="field-label">{{ field.Name }}{% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}</p>
                <p class="file-operation">
                  <label class="upload-btn" for="file_{{ field.ID }}">选择多张图片</label>
                  <input type="file" accept="image/*" multiple class="form-file-multi" id="file_{{ field.ID }}" name="file_{{ field.ID }}[]" style="display:none">
                  <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}">
              </div>

              {% elseif field.FieldType == 11 %}
              <div class="form-field-item">
                {% if field.IsShowTitle != 0 %}<p class="field-label">{{ field.Name }}</p>{% endif %}
                <p class="static-text">{{ field.FieldValues }}</p>
              </div>

	      {% elseif field.FieldType == 12 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input area-select-group">
                    <select 
                        id="form{{ form.form.ID }}_selGlobalCountry{{ field.ID }}" 
                        name="selGlobalCountry"
                        class="form-select area-province"
                    >
                        <option value="">select country</option>
                    </select>
                    <select 
                        id="form{{ form.form.ID }}_selLevelOneRegion{{ field.ID }}" 
                        name="selLevelOneRegion"
                        class="form-select area-city"
                    >
                        <option value="">please select province/state</option>
                    </select>
                    <select 
                        id="form{{ form.form.ID }}_selLevelTwoRegion{{ field.ID }}" 
                        name="selLevelTwoRegion"
                        class="form-select area-county"
                    >
                        <option value="">please select city</option>
                    </select>
                    <input 
                        type="hidden" 
                        id="form{{ form.form.ID }}_global_region{{ field.ID }}" 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}" 
                        validatetype="{{ field.ValidateType }}" 
                        class="form-region"
                    >
                </p>
            </div>

              {% endif %}

            {% endif %}
          {% endfor %}

          {% if form.needValidateCode == 1 %}
          <div class="form-field-item">
            <p class="field-label">验证码</p>
            <p class="verify-code-box">
              <input class="form-input verify-input" type="text" name="vCode" placeholder="点击获取验证码" chname="验证码" isrequire="1" fieldtype="1" validatetype="1">
              <img class="verify-img" style="display:none" src="" alt="验证码">
              <button type="button" class="refresh-btn" style="display:none">刷新验证码</button>
            </p>
          </div>
          {% endif %}

          <div class="form-field-item submit-btn-box">
            <input type="submit" class="submit-btn" value="提交询盘">
            <button type="button" class="continue-btn" id="continueBrowseBtn">继续浏览</button>
          </div>
        </div>
      </form>
      {% else %}
        <p class="form-empty">询盘表单不存在或没有可用字段</p>
      {% endif %}
    </section>
  </div>
</main>

{# 将服务端产品变成安全的 JS 对象，不能直接把名称拼接进 JS 字符串。 #}
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

<script>
(function () {
  'use strict';

  var STORAGE_KEY = 'enquiryCart';
  var fromParam = {{ fromParam|json_encode|raw }};
  var productList = document.getElementById('enquiryProductList');
  var emptyTip = document.getElementById('enquiryEmpty');
  var form = document.getElementById('customForm{{ formID }}');
  var enquiryField = document.getElementById('EnquiryProductField');

  function normalizeItem(item) {
    if (!item || !item.productID || !item.name) return null;
    var num = parseInt(item.num, 10);
    return {
      productID: String(item.productID),
      name: String(item.name),
      image: item.image ? String(item.image) : '',
      num: isFinite(num) && num > 0 ? String(num) : '1',
      skutext: item.skutext ? String(item.skutext) : ''
    };
  }

  function getCart() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      var cart = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(cart)) return [];
      return cart.map(normalizeItem).filter(function (item) { return item !== null; });
    } catch (error) {
      return [];
    }
  }

  function saveCart(cart) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
      return true;
    } catch (error) {
      alert('浏览器无法保存询盘产品，请检查隐私模式或 Storage 设置。');
      return false;
    }
  }

  function syncHiddenField(cart) {
    if (enquiryField) enquiryField.value = JSON.stringify(cart || getCart());
  }

  function addOrUpdateInitialItem() {
    var initial = normalizeItem(window.__INIT_ENQUIRY_ITEM__);
    if (!initial) return;

    var cart = getCart();
    var index = cart.findIndex(function (item) {
      return String(item.productID) === initial.productID;
    });
    if (index === -1) {
      cart.push(initial);
    } else {
      cart[index] = {
        productID: initial.productID,
        name: initial.name || cart[index].name,
        image: initial.image || cart[index].image,
        num: initial.num || cart[index].num,
        skutext: initial.skutext
      };
    }
    saveCart(cart);
  }

  function createProductRow(item, index) {
    var row = document.createElement('div');
    row.className = 'enquiry-item';

    if (item.image) {
      var image = document.createElement('img');
      image.className = 'ei-img';
      image.src = item.image;
      image.alt = item.name;
      row.appendChild(image);
    } else {
      var noImage = document.createElement('div');
      noImage.className = 'ei-img ei-noimg';
      noImage.textContent = '无图';
      row.appendChild(noImage);
    }

    var body = document.createElement('div');
    var name = document.createElement('div');
    name.className = 'ei-name';
    name.textContent = item.name;
    body.appendChild(name);

    if (item.skutext) {
      var sku = document.createElement('div');
      sku.className = 'ei-sku';
      sku.textContent = '规格：' + item.skutext;
      body.appendChild(sku);
    }

    var numberBox = document.createElement('label');
    numberBox.className = 'ei-num';
    numberBox.textContent = '数量：';
    var numberInput = document.createElement('input');
    numberInput.className = 'ei-num-input';
    numberInput.type = 'number';
    numberInput.min = '1';
    numberInput.value = item.num;
    numberInput.setAttribute('data-index', String(index));
    numberBox.appendChild(numberInput);
    body.appendChild(numberBox);
    row.appendChild(body);

    var deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.className = 'ei-del';
    deleteButton.textContent = '删除';
    deleteButton.setAttribute('data-index', String(index));
    row.appendChild(deleteButton);
    return row;
  }

  function renderProductList() {
    if (!productList) return;
    var cart = getCart();
    productList.querySelectorAll('.enquiry-item').forEach(function (node) { node.remove(); });

    if (!cart.length) {
      if (emptyTip) emptyTip.style.display = '';
      syncHiddenField([]);
      return;
    }

    if (emptyTip) emptyTip.style.display = 'none';
    cart.forEach(function (item, index) {
      productList.appendChild(createProductRow(item, index));
    });
    syncHiddenField(cart);

    productList.querySelectorAll('.ei-num-input').forEach(function (input) {
      input.addEventListener('change', function () {
        var cart = getCart();
        var index = Number(input.getAttribute('data-index'));
        if (!cart[index]) return;
        var value = parseInt(input.value, 10);
        cart[index].num = isFinite(value) && value > 0 ? String(value) : '1';
        saveCart(cart);
        renderProductList();
      });
    });

    productList.querySelectorAll('.ei-del').forEach(function (button) {
      button.addEventListener('click', function () {
        var cart = getCart();
        var index = Number(button.getAttribute('data-index'));
        if (index >= 0) cart.splice(index, 1);
        saveCart(cart);
        renderProductList();
      });
    });
  }

  function validateEnquiryProducts(cart) {
    var errors = [];
    if (!Array.isArray(cart) || cart.length === 0) {
      errors.push('请至少添加一件询盘产品后再提交');
      return errors;
    }
    cart.forEach(function (item, index) {
      if (!item.productID) errors.push('询盘产品第' + (index + 1) + '项缺少产品ID');
      if (!item.name) errors.push('询盘产品第' + (index + 1) + '项缺少产品名称');
      if (!item.num || !/^\d+$/.test(String(item.num)) || Number(item.num) <= 0) {
        errors.push('询盘产品第' + (index + 1) + '项数量必须大于0');
      }
    });
    return errors;
  }

  function validateBaseFields() {
    var errors = [];
    if (!form) return errors;

    form.querySelectorAll('[isrequire="1"]').forEach(function (field) {
      var fieldName = field.getAttribute('chname') || '该字段';
      if (field.type === 'hidden' && !field.name.includes('col')) return;

      if (field.type === 'checkbox' && field.name.includes('[]')) {
        if (!form.querySelector('input[name="' + field.name + '"]:checked')) errors.push('请至少选择一个' + fieldName);
        return;
      }
      if (field.type === 'radio') {
        if (!form.querySelector('input[name="' + field.name + '"]:checked')) errors.push('请选择' + fieldName);
        return;
      }
      if (field.type === 'file') {
        if (!field.value) errors.push('请上传' + fieldName);
        return;
      }
      if (!field.value || field.value.trim() === '') errors.push('请输入' + fieldName);
    });

    form.querySelectorAll('[fieldtype="6"], [fieldtype="9"], [fieldtype="10"]').forEach(function (field) {
      if (field.getAttribute('isrequire') === '1' && !field.value.trim()) {
        errors.push('请上传' + (field.getAttribute('chname') || '该文件'));
      }
    });

    form.querySelectorAll('[validatetype="2"]').forEach(function (field) {
      if (field.value && !/^[0-9]+$/.test(field.value.trim())) errors.push(field.getAttribute('chname') + '必须是数字');
    });
    form.querySelectorAll('[validatetype="3"]').forEach(function (field) {
      if (field.value && !/^1[3-9]\d{9}$/.test(field.value.trim())) errors.push(field.getAttribute('chname') + '格式不正确');
    });
    form.querySelectorAll('[validatetype="5"]').forEach(function (field) {
      if (field.value && !(/^(1[3-9]\d{9}|\d{3,4}-?\d{7,8})$/.test(field.value.trim()))) errors.push(field.getAttribute('chname') + '格式不正确');
    });
    form.querySelectorAll('[validatetype="6"]').forEach(function (field) {
      if (field.value && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(field.value.trim())) errors.push(field.getAttribute('chname') + '格式不正确');
    });
    form.querySelectorAll('[validatetype="7"]').forEach(function (field) {
      if (field.value && !/^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/.test(field.value.trim())) errors.push(field.getAttribute('chname') + '格式不正确');
    });
    return errors;
  }

  function appendFormData(formData) {
    form.querySelectorAll('input, select, textarea').forEach(function (element) {
      if (!element.name || element.type === 'file') return;
      if ((element.type === 'checkbox' || element.type === 'radio') && !element.checked) return;
      formData.append(element.name, element.value);
    });
  }

  function submitForm() {
    var cart = getCart();
    syncHiddenField(cart);
    var errors = validateEnquiryProducts(cart).concat(validateBaseFields());
    if (errors.length) {
      alert(errors.join('\n'));
      return;
    }

    var formData = new FormData();
    appendFormData(formData);
    var submitButton = form.querySelector('.submit-btn');
    var originalText = submitButton ? submitButton.value : '提交询盘';
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.value = '提交中...';
    }

    fetch(form.action || window.location.href, { method: 'POST', body: formData })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success) {
          alert(data.msg || data.message || '提交失败，请重试');
          return;
        }
        alert(data.msg || data.message || '提交成功！');
        localStorage.removeItem(STORAGE_KEY);
        form.reset();
        form.querySelectorAll('.upload-status').forEach(function (node) { node.textContent = ''; });
        renderProductList();
        form.querySelectorAll('select[id*="_selProvince"]').forEach(loadProvinces);
        form.querySelectorAll('select[id*="_selGlobalCountry"]').forEach(loadGlobalCountries);
      })
      .catch(function (error) {
        console.error('表单提交错误:', error);
        alert('网络错误，提交失败');
      })
      .finally(function () {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.value = originalText;
        }
      });
  }

  function loadProvinces(selectElement) {
    fetch('/index.php?c=Front/CustomForm&a=getRegion&type=prov')
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success || !data.data) return;
        selectElement.innerHTML = '<option value="">选择省份</option>';
        data.data.forEach(function (item) {
          var option = document.createElement('option');
          option.value = item.ID;
          option.textContent = item.Name;
          selectElement.appendChild(option);
        });
      })
      .catch(function (error) { console.error('加载省份失败:', error); });
  }

  function loadCities(provinceID, citySelect, areaSelect, regionInput) {
    fetch('/index.php?c=Front/CustomForm&a=getRegion&type=city&prov=' + encodeURIComponent(provinceID))
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success || !data.data) return;
        citySelect.innerHTML = '<option value="">选择城市</option>';
        areaSelect.innerHTML = '<option value="">选择区县</option>';
        regionInput.value = '';
        data.data.forEach(function (item) {
          var option = document.createElement('option');
          option.value = item.ID;
          option.textContent = item.Name;
          citySelect.appendChild(option);
        });
      })
      .catch(function (error) { console.error('加载城市失败:', error); });
  }

  function loadDistricts(provinceID, cityID, areaSelect, regionInput) {
    fetch('/index.php?c=Front/CustomForm&a=getRegion&type=district&prov=' + encodeURIComponent(provinceID) + '&city=' + encodeURIComponent(cityID))
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success || !data.data) return;
        areaSelect.innerHTML = '<option value="">选择区县</option>';
        regionInput.value = '';
        data.data.forEach(function (item) {
          var option = document.createElement('option');
          option.value = item.ID;
          option.textContent = item.Name;
          areaSelect.appendChild(option);
        });
      })
      .catch(function (error) { console.error('加载区县失败:', error); });
  }

  function bindRegions() {
    if (!form) return;
    form.querySelectorAll('select[id*="_selProvince"]').forEach(function (provinceSelect) {
      var fieldID = provinceSelect.id.replace(/.*selProvince/, '');
      var citySelect = document.getElementById('form{{ formID }}_selCity' + fieldID);
      var areaSelect = document.getElementById('form{{ formID }}_selArea' + fieldID);
      var regionInput = document.getElementById('form{{ formID }}_region' + fieldID);
      if (!citySelect || !areaSelect || !regionInput) return;

      loadProvinces(provinceSelect);
      provinceSelect.addEventListener('change', function () {
        if (!this.value) {
          citySelect.innerHTML = '<option value="">选择城市</option>';
          areaSelect.innerHTML = '<option value="">选择区县</option>';
          regionInput.value = '';
          return;
        }
        loadCities(this.value, citySelect, areaSelect, regionInput);
      });
      citySelect.addEventListener('change', function () {
        if (!this.value) {
          areaSelect.innerHTML = '<option value="">选择区县</option>';
          regionInput.value = '';
          return;
        }
        loadDistricts(provinceSelect.value, this.value, areaSelect, regionInput);
      });
      areaSelect.addEventListener('change', function () {
        var provinceName = provinceSelect.options[provinceSelect.selectedIndex].text;
        var cityName = citySelect.options[citySelect.selectedIndex].text;
        var areaName = areaSelect.options[areaSelect.selectedIndex].text;
        if (provinceSelect.value && citySelect.value && areaSelect.value) {
          regionInput.value = provinceName + '/' + cityName + '/' + areaName;
        } else {
          regionInput.value = '';
        }
      });
    });

    form.querySelectorAll('select[id*="_selGlobalCountry"]').forEach(function (countrySelect) {
      var fieldID = countrySelect.id.replace(/.*selGlobalCountry/, '');
      var levelOneSelect = document.getElementById('form{{ formID }}_selLevelOneRegion' + fieldID);
      var levelTwoSelect = document.getElementById('form{{ formID }}_selLevelTwoRegion' + fieldID);
      var globalRegionInput = document.getElementById('form{{ formID }}_global_region' + fieldID);
      if (!levelOneSelect || !levelTwoSelect || !globalRegionInput) return;

      loadGlobalCountries(countrySelect);
      countrySelect.addEventListener('change', function () {
        if (!this.value) {
          levelOneSelect.innerHTML = '<option value="">please select province/state</option>';
          levelTwoSelect.innerHTML = '<option value="">please select city</option>';
          globalRegionInput.value = '';
          return;
        }
        loadGlobalRegions(
          this.value,
          levelOneSelect,
          levelTwoSelect,
          globalRegionInput,
          'please select province/state',
          'please select city'
        );
      });
      levelOneSelect.addEventListener('change', function () {
        if (!this.value) {
          levelTwoSelect.innerHTML = '<option value="">please select city</option>';
          globalRegionInput.value = '';
          return;
        }
        loadGlobalRegions(
          this.value,
          levelTwoSelect,
          null,
          globalRegionInput,
          'please select city'
        );
      });
      levelTwoSelect.addEventListener('change', function () {
        var countryName = countrySelect.options[countrySelect.selectedIndex].text;
        var levelOneName = levelOneSelect.options[levelOneSelect.selectedIndex].text;
        var levelTwoName = levelTwoSelect.options[levelTwoSelect.selectedIndex].text;
        if (countrySelect.value && levelOneSelect.value && levelTwoSelect.value) {
          globalRegionInput.value = countryName + '/' + levelOneName + '/' + levelTwoName;
        } else {
          globalRegionInput.value = '';
        }
      });
    });
  }

  function loadGlobalCountries(selectElement) {
    fetch('/index.php?c=Front/CustomForm&a=getIntlRegion')
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success || !data.data) return;
        selectElement.innerHTML = '<option value="">select country</option>';
        data.data.forEach(function (item) {
          var option = document.createElement('option');
          option.value = item.ID;
          option.textContent = item.Name;
          selectElement.appendChild(option);
        });
      })
      .catch(function (error) { console.error('加载国家失败:', error); });
  }

  function loadGlobalRegions(parentID, targetSelect, childSelect, regionInput, targetPlaceholder, childPlaceholder) {
    fetch('/index.php?c=Front/CustomForm&a=getIntlRegion&parent_id=' + encodeURIComponent(parentID))
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.success || !data.data) return;
        targetSelect.innerHTML = '<option value="">' + targetPlaceholder + '</option>';
        if (childSelect) {
          childSelect.innerHTML = '<option value="">' + childPlaceholder + '</option>';
        }
        regionInput.value = '';
        data.data.forEach(function (item) {
          var option = document.createElement('option');
          option.value = item.ID;
          option.textContent = item.Name;
          targetSelect.appendChild(option);
        });
      })
      .catch(function (error) { console.error('加载国际地区失败:', error); });
  }

  function bindSmsButtons() {
    if (!form) return;
    form.querySelectorAll('.sms-btn').forEach(function (button) {
      button.addEventListener('click', function () {
        var box = button.closest('.sms-validate-box');
        var phoneInput = box ? box.previousElementSibling : null;
        if (!phoneInput || !/^1[3-9]\d{9}$/.test(phoneInput.value)) {
          alert('请先输入正确的手机号码');
          return;
        }
        var originalText = button.textContent;
        button.disabled = true;
        button.textContent = '发送中...';
        fetch('/index.php?c=Front/CustomForm&a=sendsmsvcode&mobile=' + encodeURIComponent(phoneInput.value))
          .then(function (response) { return response.json(); })
          .then(function (data) {
            if (!data.success) {
              alert(data.msg || data.message || '发送失败，请重试');
              button.disabled = false;
              button.textContent = originalText;
              return;
            }
            var seconds = 60;
            button.textContent = seconds + 's后重试';
            var timer = window.setInterval(function () {
              seconds -= 1;
              if (seconds <= 0) {
                window.clearInterval(timer);
                button.disabled = false;
                button.textContent = originalText;
              } else {
                button.textContent = seconds + 's后重试';
              }
            }, 1000);
          })
          .catch(function () {
            alert('网络错误，请重试');
            button.disabled = false;
            button.textContent = originalText;
          });
      });
    });
  }

  function bindEmailButtons() {
    if (!form) return;
    form.querySelectorAll('.email-btn').forEach(function (button) {
      button.addEventListener('click', function () {
        var box = button.closest('.email-validate-box');
        var emailInput = box ? box.previousElementSibling : null;
        var emailReg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailInput || !emailReg.test(emailInput.value)) {
          alert('请先输入正确的邮箱地址');
          return;
        }
        var originalText = button.textContent;
        button.disabled = true;
        button.textContent = '发送中...';
        fetch('/index.php?c=validatecode&a=sendEmailCode&email=' + encodeURIComponent(emailInput.value))
          .then(function (response) { return response.json(); })
          .then(function (data) {
            if (!data.success) {
              alert(data.msg || data.message || '发送失败，请重试');
              button.disabled = false;
              button.textContent = originalText;
              return;
            }
            var seconds = 60;
            button.textContent = seconds + 's后重试';
            var timer = window.setInterval(function () {
              seconds -= 1;
              if (seconds <= 0) {
                window.clearInterval(timer);
                button.disabled = false;
                button.textContent = originalText;
              } else {
                button.textContent = seconds + 's后重试';
              }
            }, 1000);
          })
          .catch(function () {
            alert('网络错误，请重试');
            button.disabled = false;
            button.textContent = originalText;
          });
      });
    });
  }

  function bindVerifyCode() {
    if (!form) return;
    var input = form.querySelector('.verify-input');
    var image = form.querySelector('.verify-img');
    var refresh = form.querySelector('.refresh-btn');
    if (!input || !image || !refresh) return;

    function getVerifyURL() {
      return '/index.php?c=validatecode&useCurve=1&useNoise=1&fontSize=32&imageW=290&imageH=100&t=' + Date.now();
    }
    input.addEventListener('click', function () {
      if (image.style.display === 'none') {
        image.src = getVerifyURL();
        image.style.display = 'block';
        refresh.style.display = 'inline-flex';
      }
    });
    refresh.addEventListener('click', function () { image.src = getVerifyURL(); });
  }

  function bindFileUpload() {
    if (!form) return;
    form.querySelectorAll('input[type="file"]').forEach(function (fileInput) {
      fileInput.addEventListener('change', function () {
        if (!fileInput.files || !fileInput.files.length) return;
        var fieldName = fileInput.name;
        var fieldID = fieldName.replace('file_', '').replace('[]', '');
        var hiddenInput = form.querySelector('input[name="col' + fieldID + '"]');
        var operation = fileInput.closest('.file-operation');
        var status = operation ? operation.querySelector('.upload-status') : null;
        if (!hiddenInput) return;

        var uploadData = new FormData();
        if (fieldName.includes('[]')) {
          Array.from(fileInput.files).forEach(function (file) { uploadData.append(fieldName, file); });
          uploadData.append('count', String(fileInput.files.length));
          if (status) status.textContent = '上传中 ' + fileInput.files.length + ' 个文件...';
        } else {
          uploadData.append(fieldName, fileInput.files[0]);
          if (status) status.textContent = '上传中...';
        }

        var action = fieldName.includes('[]')
          ? '/index.php?c=Front/CustomForm&a=uploadfiles'
          : '/index.php?c=Front/CustomForm&a=uploadfile';
        fetch(action, { method: 'POST', body: uploadData })
          .then(function (response) { return response.json(); })
          .then(function (data) {
            if (!data.success || !data.newfile) {
              if (status) status.textContent = '';
              alert(data.msg || data.message || '上传失败');
              return;
            }
            hiddenInput.value = data.newfile;
            var count = String(data.newfile).split(',').length;
            if (status) status.textContent = '已上传' + count + (count > 1 ? '个文件' : '个文件');
            fileInput.value = '';
          })
          .catch(function () {
            if (status) status.textContent = '';
            alert('网络错误，上传失败');
          });
      });
    });
  }

  function bindContinueButton() {
    var button = document.getElementById('continueBrowseBtn');
    if (!button) return;
    button.addEventListener('click', function () {
      var productURL = 'products.html';
      if (fromParam === 'popup') {
        window.close();
        window.setTimeout(function () {
          if (!window.closed) window.location.href = productURL;
        }, 100);
      } else if (fromParam === 'blank') {
        window.location.href = productURL;
      } else if (window.history.length > 1) {
        window.history.back();
      } else {
        window.location.href = productURL;
      }
    });
  }

  if (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      submitForm();
    });
  }

  addOrUpdateInitialItem();
  renderProductList();
  bindRegions();
  bindSmsButtons();
  bindEmailButtons();
  bindVerifyCode();
  bindFileUpload();
  bindContinueButton();
}());
</script>

{% if fromParam != 'popup' %}
  {# {% include 'site-footer.twig' %} #}
{% endif %}
</body>
</html>
```

## 代码关键点

### 1. 为什么产品要在 Twig 中加载

产品详情由 `FnGetOnePro` 在服务端读取，避免前端额外依赖一个未约定的产品详情接口。Twig 将必要字段编码后写入 `window.__INIT_ENQUIRY_ITEM__`，浏览器加载页面后再交给 Storage 逻辑处理。

### 2. 为什么不能只在页面加载时设置 `EnquiryProduct`

用户可能在页面上修改数量或删除产品。因此提交时必须重新读取 `localStorage`，重新序列化并覆盖 hidden 字段。示例中的 `submitForm()` 已执行这一步。

### 3. 为什么上传时不提交 file input

自定义表单上传接口会先把文件保存并返回路径。正式提交时只提交 `col{{ field.ID }}` hidden 字段，基础表单脚本也会跳过 `type=file`，避免重复上传。

### 4. 哪些代码不能删

- `submitType`、`FormID`、`needValidateCode`、`submitChecksum`、`submitFrom`
- `EnquiryProduct` hidden 字段
- 产品提交前校验
- 文件 hidden 字段校验
- 手机号、邮箱、数字、身份证校验
- 文件上传、短信、地区和图形验证码逻辑
- `fetch + FormData` AJAX 提交流程
