## 自定义表单示例代码-基础版
### 注意事项1：因为前端的HTML编辑器会用 new DOMParser().parseFromString() 处理最终的代码，注意 html tag 的属性要规范，避免在标签属性中使用 {%if%} {%for%}等逻辑控制代码
### 注意事项2：请务必保留此示例代码中的检验和提交表单的JS，否能表单可能无法提交
### 注意事项3：验证码输入框的样式要与表单中其它输入框的样式保持一至

{# 获取表单，1516为表单的ID，请根据具体情况替换为你真实的表单ID #}
{% set form = FnGetCustomForm(1516) %}

{# 检查表单是否存在 #}
{% if form and form.fields %}
<form id="customForm{{ form.form.ID}}" action="{{ form.action }}" method="post" class="Form-containt" enctype="multipart/form-data">
    {# 隐藏字段 #}
    <input type="hidden" name="submitType" value="ajax" />
    <input type="hidden" name="FormID" value="{{ form.form.ID }}">
    <input type="hidden" name="needValidateCode" value="{{ form.needValidateCode }}">
    <input type="hidden" name="submitChecksum" value="{{ form.submitChecksum }}">
    <input type="hidden" name="submitFrom" value="customhtml">
    {# 表单标题 #}
    {% if form.form.Name %}
    <h3 class="title">{{ form.form.Name }}</h3>
    {% endif %}
    
    <div class="form-fields-list">
        {% for field in form.fields %}
            {# 只显示启用的字段 #}
            {% if field.IsShow == 1 %}
            
            {# 类型1/13/14/15: 单行文本类（通用文本/公司名/姓名/邮箱） #}
            {% if field.FieldType == 1 or field.FieldType == 13 or field.FieldType == 14 or field.FieldType == 15 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input">
                    <input 
                        type="text" 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}"  
                        validatetype="{{ field.ValidateType }}"
                        placeholder="{{ field.Placeholder }}"
                        class="form-input"
                    >
                    {# 手机号字段且开启短信验证时，显示验证码输入框和发送按钮 #}
                    {% if field.ValidateType == 3 and field.IsSmsValidate == 1 %}
                    <span class="sms-validate-box">
                        <input 
                            class="sms-code" 
                            name="col{{ field.ID }}_vcode" 
                            placeholder="请输入验证码" 
                            required
                        >
                        <button class="sms-btn" type="button">获取验证码</button>
                    </span>
                    {% endif %}
                    {# 邮箱字段且开启邮箱真实性验证时，显示验证码输入框和发送按钮 #}
                    {% if field.ValidateType == 6 and field.IsEmailValidate == 1 %}
                    <span class="email-validate-box">
                        <input
                            class="email-code"
                            name="col{{ field.ID }}_vcode"
                            placeholder="请输入验证码"
                            required
                        >
                        <button class="email-btn" type="button">获取验证码</button>
                    </span>
                    {% endif %}
                </p>
            </div>
            
            {# 类型2: 多行文本 #}
            {% elseif field.FieldType == 2 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input">
                    <textarea 
                        class="form-textarea" 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}" 
                        validatetype="{{ field.ValidateType }}"
                        placeholder="{{ field.Placeholder }}"
                        rows="5"
                    ></textarea>
                </p>
            </div>
            
            {# 类型3: 单选框 #}
            {% elseif field.FieldType == 3 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="radio-group">
                    {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
                    <label class="radio-item">
                        <input 
                            type="radio" 
                            class="form-radio" 
                            name="col{{ field.ID }}" 
                            chname="{{ field.Name }}" 
                            isrequire="{{ field.IsRequire }}" 
                            fieldtype="{{ field.FieldType }}" 
                            validatetype="{{ field.ValidateType }}" 
                            value="{{ fieldValue }}"
                        >
                        <span>{{ fieldValue }}</span>
                    </label>
                    {% endfor %}
                </p>
            </div>
            
            {# 类型4: 下拉选择 #}
            {% elseif field.FieldType == 4 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input">
                    <select 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}" 
                        validatetype="{{ field.ValidateType }}"
                        class="form-select"
                    >
                        <option value="">请选择</option>
                        {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
                        <option value="{{ fieldValue }}">{{ fieldValue }}</option>
                        {% endfor %}
                    </select>
                </p>
            </div>
            
            {# 类型5: 多选框 #}
            {% elseif field.FieldType == 5 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="checkbox-group">
                    {% for fieldValue in FnGetFieldValuesArray(field.FieldValues) %}
                    <label class="checkbox-item">
                        <input 
                            type="checkbox" 
                            class="form-checkbox" 
                            name="col{{ field.ID }}[]" 
                            chname="{{ field.Name }}" 
                            isrequire="{{ field.IsRequire }}" 
                            fieldtype="{{ field.FieldType }}" 
                            validatetype="{{ field.ValidateType }}" 
                            value="{{ fieldValue }}"
                        >
                        <span>{{ fieldValue }}</span>
                    </label>
                    {% endfor %}
                </p>
            </div>
            
            {# 类型6: 图片上传 #}
            {% elseif field.FieldType == 6 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="file-operation">
                    <label class="upload-btn" for="file{{ form.form.ID}}_{{ field.ID }}">
                        <span class="icon-add">+</span>
                    </label>
                    <input 
                        type="file" 
                        accept="image/*" 
                        class="form-file" 
                        id="file{{ form.form.ID}}_{{ field.ID }}" 
                        name="file_{{ field.ID}}"
                        style="display:none"
                    />
                    <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" />
            </div>
            
            {# 类型7: 中国国内地区选择 #}
            {% elseif field.FieldType == 7 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input area-select-group">
                    <select 
                        id="form{{ form.form.ID }}_selProvince{{ field.ID }}" 
                        name="selProvince"
                        class="form-select area-province"
                    >
                        <option value="">选择省份</option>
                    </select>
                    <select 
                        id="form{{ form.form.ID }}_selCity{{ field.ID }}" 
                        name="selCity"
                        class="form-select area-city"
                    >
                        <option value="">选择城市</option>
                    </select>
                    <select 
                        id="form{{ form.form.ID }}_selArea{{ field.ID }}" 
                        name="selArea"
                        class="form-select area-county"
                    >
                        <option value="">选择区县</option>
                    </select>
                    <input 
                        type="hidden" 
                        id="form{{ form.form.ID }}_region{{ field.ID }}" 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}" 
                        validatetype="{{ field.ValidateType }}" 
                        class="form-region"
                    >
                </p>
            </div>
            
            {# 类型8: 时间选择 #}
            {% elseif field.FieldType == 8 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="field-input">
                    <input 
                        type="text" 
                        name="col{{ field.ID }}" 
                        chname="{{ field.Name }}" 
                        isrequire="{{ field.IsRequire }}" 
                        fieldtype="{{ field.FieldType }}" 
                        validatetype="{{ field.ValidateType }}"
                        placeholder="请选择时间"
                        class="form-datetime"
                    />
                </p>
            </div>
            
            {# 类型9: 文件上传 #}
            {% elseif field.FieldType == 9 %}
            <div class="form-field-item">
                <p class="field-label">
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="file-operation">
                    <label class="browse-file" for="file_{{ field.ID }}">
                        {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                        浏览文件
                    </label>
                    <input 
                        type="file" 
                        class="form-file-upload" 
                        id="file_{{ field.ID }}" 
                        name="file_{{ field.ID}}"
                        style="display:none"
                    />
                    <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" />
            </div>
            
            {# 类型10: 多图上传 #}
            {% elseif field.FieldType == 10 %}
            <div class="form-field-item">
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                <p class="file-operation multi-images">
                    <label class="upload-btn-multi" for="file_{{ field.ID }}">
                        <span class="icon-add">+</span>
                    </label>
                    <input 
                        type="file" 
                        accept="image/*" 
                        multiple 
                        class="form-file-multi" 
                        id="file_{{ field.ID }}" 
                        name="file_{{ field.ID }}[]"
                        style="display:none"
                    />
                    <span class="upload-status"></span>
                </p>
                <input type="hidden" name="col{{ field.ID }}" chname="{{ field.Name }}" isrequire="{{ field.IsRequire }}" fieldtype="{{ field.FieldType }}" validatetype="{{ field.ValidateType }}" />
            </div>
            
            {# 类型11: 静态文本 #}
            {% elseif field.FieldType == 11 %}
            <div class="form-field-item">
                {% if field.IsShowTitle != 0 %}
                <p class="field-label">
                    {% if field.Icon %}<img class="field-icon" src="{{ field.Icon }}" />{% endif %}
                    {{ field.Name }}
                    {% if field.IsRequire == 1 %}<span class="required">*</span>{% endif %}
                </p>
                {% endif %}
                <p class="static-text">
                    <span>{{ field.FieldValues }}</span>
                </p>
            </div>

	    {# 类型12: 国际地区选择 #}
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
        
        {# 验证码(如果需要) #}
        {% if form.needValidateCode == 1 %}
        <div class="form-field-item">
            <p class="field-label">验证码</p>
            <p class="verify-code-box">
                <input class="verify-input form-input" type="text" name="vCode" placeholder="点击获取验证码" chname="验证码" isrequire="1" fieldtype="1" validatetype="1" />
                <img class="verify-img" style="display:none" src="">
                <span class="refresh-btn" style="display:none">刷新验证码</span>
            </p>
        </div>
        {% endif %}
        
        {# 提交按钮 #}
        {% if form.action %}
        <div class="form-field-item submit-btn-box">
            <input type="submit" class="submit-btn" value="提交"/>
        </div>
        {% endif %}
	<script>
	function syncRequired{{ form.form.ID }}(checkboxes) {
	  const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
	  checkboxes.forEach(cb => {
	    // 有任意一个被选中 → 全部去掉 required
	    // 一个都没选 → 全部恢复 required
	    cb.required = !anyChecked;
	  });
	}
	document.querySelectorAll(
	  'input[isrequire="1"], select[isrequire="1"], textarea[isrequire="1"]'
	).forEach(el => {
	  el.setAttribute('required', 'required');
	  if (el.type == 'checkbox') {
		let checkboxes = document.querySelectorAll('input[name="'+el.name+'"]');
		checkboxes.forEach(cb => {
		  cb.addEventListener('change', syncRequired{{ form.form.ID }}.bind(null, checkboxes));
		});
	  }
	});
	</script>
    
    {# 表单验证脚本 #}
    <script>
    (function() {
        var form = document.getElementById('customForm{{ form.form.ID}}');
        if (!form) return;
        
        // 表单提交验证
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // 阻止默认提交
            
            var errors = [];
            
            // 1. 验证所有必填字段
            var requiredFields = form.querySelectorAll('[isrequire="1"]');
            requiredFields.forEach(function(field) {
                var fieldName = field.getAttribute('chname') || '该字段';
                
                // 跳过静态文本和隐藏字段
                if (field.type === 'hidden' && !field.name.includes('col')) return;
                
                // 多选框特殊处理：至少选中一个
                if (field.type === 'checkbox' && field.name.includes('[]')) {
                    var groupName = field.name;
                    var checkedBoxes = form.querySelectorAll('input[name="' + groupName + '"]:checked');
                    if (checkedBoxes.length === 0) {
                        errors.push('请至少选择一个' + fieldName);
                    }
                    return;
                }
                
                // 单选框特殊处理：至少选中一个
                if (field.type === 'radio') {
                    var radioName = field.name;
                    var checkedRadio = form.querySelector('input[name="' + radioName + '"]:checked');
                    if (!checkedRadio) {
                        errors.push('请选择' + fieldName);
                    }
                    return;
                }
                
                // 文件上传特殊处理
                if (field.type === 'file') {
                    if (!field.value || field.value === '') {
                        errors.push('请上传' + fieldName);
                    }
                    return;
                }
                
                // 普通输入框、文本域、下拉框验证
                if (!field.value || field.value.trim() === '') {
                    errors.push('请输入' + fieldName);
                }
            });
            
            // 2. 验证文件上传字段（检查hidden input的值）
            var fileFields = form.querySelectorAll('[fieldtype="6"], [fieldtype="9"], [fieldtype="10"]');
            fileFields.forEach(function(hiddenField) {
                if (hiddenField.getAttribute('isrequire') === '1') {
                    var fieldName = hiddenField.getAttribute('chname') || '该字段';
                    if (!hiddenField.value || hiddenField.value.trim() === '') {
                        errors.push('请上传' + fieldName);
                    }
                }
            });
            
            // 3. 验证手机号格式（ValidateType=3）
            var phoneFields = form.querySelectorAll('[validatetype="3"]');
            phoneFields.forEach(function(field) {
                if (field.value && field.value.trim() !== '') {
                    var phoneReg = /^1[3-9]\d{9}$/;
                    if (!phoneReg.test(field.value)) {
                        errors.push(field.getAttribute('chname') + '格式不正确');
                    }
                }
            });
            
            // 4. 验证邮箱格式（ValidateType=6）
            var emailFields = form.querySelectorAll('[validatetype="6"]');
            emailFields.forEach(function(field) {
                if (field.value && field.value.trim() !== '') {
                    var emailReg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                    if (!emailReg.test(field.value)) {
                        errors.push(field.getAttribute('chname') + '格式不正确');
                    }
                }
            });
            
            // 5. 验证数字格式（ValidateType=2）
            var numberFields = form.querySelectorAll('[validatetype="2"]');
            numberFields.forEach(function(field) {
                if (field.value && field.value.trim() !== '') {
                    var numberReg = /^[0-9]+$/;
                    if (!numberReg.test(field.value)) {
                        errors.push(field.getAttribute('chname') + '必须是数字');
                    }
                }
            });
            
            // 6. 验证身份证号（ValidateType=7）
            var idCardFields = form.querySelectorAll('[validatetype="7"]');
            idCardFields.forEach(function(field) {
                if (field.value && field.value.trim() !== '') {
                    var idCardReg = /^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
                    if (!idCardReg.test(field.value)) {
                        errors.push(field.getAttribute('chname') + '格式不正确');
                    }
                }
            });
            
            // 如果有错误，显示错误信息
            if (errors.length > 0) {
                alert(errors.join(','));
                return false;
            }
            
            // 验证通过，使用AJAX提交表单
            var formData = new FormData();
            
            // 遍历表单所有元素，排除file类型的input
            var formElements = form.querySelectorAll('input, select, textarea');
            formElements.forEach(function(element) {
                // 跳过file类型的input（因为文件已经提前上传）
                if (element.type === 'file') {
                    return;
                }
                
                // 跳过没有name属性的元素
                if (!element.name) {
                    return;
                }
                
                // 处理checkbox和radio（只添加选中的）
                if (element.type === 'checkbox' || element.type === 'radio') {
                    if (element.checked) {
                        formData.append(element.name, element.value);
                    }
                    return;
                }
                
                // 其他元素直接添加
                formData.append(element.name, element.value);
            });
            
            var submitBtn = form.querySelector('.submit-btn');
            var originalText = submitBtn ? submitBtn.value : '提交';
            
            // 禁用提交按钮，防止重复提交
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.value = '提交中...';
            }
            
            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (data.success) {
                    alert(data.msg || '提交成功！');
                    // 提交成功后重置表单
                    form.reset();
                    
                    // 清空所有上传状态显示
                    var uploadStatuses = form.querySelectorAll('.upload-status');
                    uploadStatuses.forEach(function(status) {
                        status.textContent = '';
                    });
                    
                    // 重新加载地区选择（如果需要）
                    var provinceSelects = form.querySelectorAll('select[id*="_selProvince"]');
                    provinceSelects.forEach(function(sel) {
                        loadProvinces(sel);
                    });
                    var globalCountrySelects = form.querySelectorAll('select[id*="_selGlobalCountry"]');
                    globalCountrySelects.forEach(function(sel) {
                        loadGlobalCountries(sel);
                    });
                } else {
                    alert(data.msg || '提交失败，请重试');
                }
            })
            .catch(function(error) {
                alert('网络错误，提交失败');
                console.error('表单提交错误:', error);
            })
            .finally(function() {
                // 恢复提交按钮状态
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.value = originalText;
                }
            });
            
            return false;
        });
        
        // 短信验证码按钮点击事件
        var smsButtons = form.querySelectorAll('.sms-btn');
        smsButtons.forEach(function(btn) {
            btn.addEventListener('click', function() {
                // 查找对应的手机号输入框
                var smsBox = this.closest('.sms-validate-box');
                if (!smsBox) return;
                
                var phoneInput = smsBox.previousElementSibling;
                if (!phoneInput || !phoneInput.value) {
                    alert('请先输入手机号码');
                    return;
                }
                
                // 验证手机号格式
                var phoneReg = /^1[3-9]\d{9}$/;
                if (!phoneReg.test(phoneInput.value)) {
                    alert('手机号码格式不正确');
                    return;
                }
                
                // 调用短信接口发送验证码
                var mobile = phoneInput.value;
                var smsUrl = '/index.php?c=Front/CustomForm&a=sendsmsvcode&mobile=' + encodeURIComponent(mobile);
                
                // 显示加载状态
                var originalText = this.textContent;
                this.disabled = true;
                this.textContent = '发送中...';
                
                fetch(smsUrl)
                    .then(function(response) { return response.json(); })
                    .then(function(data) {
                        if (data.success) {
                            alert('验证码已发送到 ' + mobile);
                            
                            // 倒计时60秒
                            var countdown = 60;
                            btn.textContent = countdown + 's后重试';
                            
                            var timer = setInterval(function() {
                                countdown--;
                                if (countdown <= 0) {
                                    clearInterval(timer);
                                    btn.disabled = false;
                                    btn.textContent = '获取验证码';
                                } else {
                                    btn.textContent = countdown + 's后重试';
                                }
                            }, 1000);
                        } else {
                            alert(data.msg || '发送失败，请重试');
                            btn.disabled = false;
                            btn.textContent = originalText;
                        }
                    })
                    .catch(function(error) {
                        alert('网络错误，请重试');
                        btn.disabled = false;
                        btn.textContent = originalText;
                        console.error('短信发送错误:', error);
                    });
            });
        });

        // 邮箱验证码按钮点击事件
        var emailButtons = form.querySelectorAll('.email-btn');
        emailButtons.forEach(function(btn) {
            btn.addEventListener('click', function() {
                // 查找对应的邮箱输入框
                var emailBox = this.closest('.email-validate-box');
                if (!emailBox) return;

                var emailInput = emailBox.previousElementSibling;
                if (!emailInput || !emailInput.value) {
                    alert('请先输入邮箱地址');
                    return;
                }

                // 验证邮箱格式
                var emailReg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (!emailReg.test(emailInput.value)) {
                    alert('邮箱地址格式不正确');
                    return;
                }

                // 调用邮箱验证码接口发送验证码
                var email = emailInput.value;
                var emailUrl = '/index.php?c=validatecode&a=sendEmailCode&email=' + encodeURIComponent(email);

                // 显示加载状态
                var originalText = this.textContent;
                this.disabled = true;
                this.textContent = '发送中...';

                fetch(emailUrl)
                    .then(function(response) { return response.json(); })
                    .then(function(data) {
                        if (data.success) {
                            alert('验证码已发送到 ' + email);

                            // 倒计时60秒
                            var countdown = 60;
                            btn.textContent = countdown + 's后重试';

                            var timer = setInterval(function() {
                                countdown--;
                                if (countdown <= 0) {
                                    clearInterval(timer);
                                    btn.disabled = false;
                                    btn.textContent = '获取验证码';
                                } else {
                                    btn.textContent = countdown + 's后重试';
                                }
                            }, 1000);
                        } else {
                            alert(data.msg || '发送失败，请重试');
                            btn.disabled = false;
                            btn.textContent = originalText;
                        }
                    })
                    .catch(function(error) {
                        alert('网络错误，请重试');
                        btn.disabled = false;
                        btn.textContent = originalText;
                        console.error('邮箱验证码发送错误:', error);
                    });
            });
        });
        
        // 中国国内地区选择三级联动（如果存在地区选择字段）
        var provinceSelects = form.querySelectorAll('select[id*="_selProvince"]');
        provinceSelects.forEach(function(provinceSel) {
            var fieldId = provinceSel.id.replace(/.*selProvince/, '');
            var citySel = document.getElementById('form{{ form.form.ID }}_selCity' + fieldId);
            var areaSel = document.getElementById('form{{ form.form.ID }}_selArea' + fieldId);
            var regionInput = document.getElementById('form{{ form.form.ID }}_region' + fieldId);
            
            if (!citySel || !areaSel || !regionInput) return;
            
            // 初始化：加载省份列表
            loadProvinces(provinceSel);
            
            // 省份变化时加载城市
            provinceSel.addEventListener('change', function() {
                var provinceID = this.value;
                if (!provinceID) {
                    citySel.innerHTML = '<option value="">选择城市</option>';
                    areaSel.innerHTML = '<option value="">选择区县</option>';
                    regionInput.value = '';
                    return;
                }
                
                // 根据省份ID加载城市列表
                loadCities(provinceID, citySel, areaSel, regionInput);
            });
            
            // 城市变化时加载区县
            citySel.addEventListener('change', function() {
                var provinceID = provinceSel.value;
                var cityID = this.value;
                if (!cityID) {
                    areaSel.innerHTML = '<option value="">选择区县</option>';
                    regionInput.value = '';
                    return;
                }
                
                // 根据省市ID加载区县列表
                loadDistricts(provinceID, cityID, areaSel, regionInput);
            });
            
            // 区县变化时更新隐藏字段（存储名称而非ID）
            areaSel.addEventListener('change', function() {
                var provinceName = provinceSel.options[provinceSel.selectedIndex].text;
                var cityName = citySel.options[citySel.selectedIndex].text;
                var areaName = this.options[this.selectedIndex].text;
                
                if (provinceName && cityName && areaName && 
                    provinceName !== '选择省份' && cityName !== '选择城市' && areaName !== '选择区县') {
                    regionInput.value = provinceName + '/' + cityName + '/' + areaName;
                } else {
                    regionInput.value = '';
                }
            });
        });

        // 国际地区选择三级联动（如果存在国际地区选择字段）
        var globalCountrySelects = form.querySelectorAll('select[id*="_selGlobalCountry"]');
        globalCountrySelects.forEach(function(countrySel) {
            var fieldId = countrySel.id.replace(/.*selGlobalCountry/, '');
            var levelOneSel = document.getElementById('form{{ form.form.ID }}_selLevelOneRegion' + fieldId);
            var levelTwoSel = document.getElementById('form{{ form.form.ID }}_selLevelTwoRegion' + fieldId);
            var globalRegionInput = document.getElementById('form{{ form.form.ID }}_global_region' + fieldId);

            if (!levelOneSel || !levelTwoSel || !globalRegionInput) return;

            // 初始化：加载国家列表
            loadGlobalCountries(countrySel);

            // 国家变化时加载一级行政区域
            countrySel.addEventListener('change', function() {
                var countryID = this.value;
                if (!countryID) {
                    levelOneSel.innerHTML = '<option value="">please select province/state</option>';
                    levelTwoSel.innerHTML = '<option value="">please select city</option>';
                    globalRegionInput.value = '';
                    return;
                }

                loadGlobalRegions(countryID, levelOneSel, levelTwoSel, globalRegionInput, 'please select province/state', 'please select city');
            });

            // 一级行政区域变化时加载二级行政区域
            levelOneSel.addEventListener('change', function() {
                var levelOneID = this.value;
                if (!levelOneID) {
                    levelTwoSel.innerHTML = '<option value="">please select city</option>';
                    globalRegionInput.value = '';
                    return;
                }

                loadGlobalRegions(levelOneID, levelTwoSel, null, globalRegionInput, 'please select city');
            });

            // 二级行政区域变化时更新隐藏字段（存储名称而非ID）
            levelTwoSel.addEventListener('change', function() {
                var countryName = countrySel.options[countrySel.selectedIndex].text;
                var levelOneName = levelOneSel.options[levelOneSel.selectedIndex].text;
                var levelTwoName = this.options[this.selectedIndex].text;

                if (countrySel.value && levelOneSel.value && levelTwoSel.value) {
                    globalRegionInput.value = countryName + '/' + levelOneName + '/' + levelTwoName;
                } else {
                    globalRegionInput.value = '';
                }
            });
        });
        
        // 加载省份列表
        function loadProvinces(selectElement) {
            fetch('/index.php?c=Front/CustomForm&a=getRegion&type=prov')
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.data) {
                        selectElement.innerHTML = '<option value="">选择省份</option>';
                        data.data.forEach(function(province) {
                            var option = document.createElement('option');
                            option.value = province.ID;
                            option.textContent = province.Name;
                            selectElement.appendChild(option);
                        });
                    }
                })
                .catch(function(error) {
                    console.error('加载省份失败:', error);
                });
        }
        
        // 加载城市列表
        function loadCities(provinceID, citySelect, areaSelect, regionInput) {
            fetch('/index.php?c=Front/CustomForm&a=getRegion&type=city&prov=' + provinceID)
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.data) {
                        citySelect.innerHTML = '<option value="">选择城市</option>';
                        areaSelect.innerHTML = '<option value="">选择区县</option>';
                        regionInput.value = '';
                        
                        data.data.forEach(function(city) {
                            var option = document.createElement('option');
                            option.value = city.ID;
                            option.textContent = city.Name;
                            citySelect.appendChild(option);
                        });
                    }
                })
                .catch(function(error) {
                    console.error('加载城市失败:', error);
                });
        }
        
        // 加载区县列表
        function loadDistricts(provinceID, cityID, areaSelect, regionInput) {
            fetch('/index.php?c=Front/CustomForm&a=getRegion&type=district&prov=' + provinceID + '&city=' + cityID)
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.data) {
                        areaSelect.innerHTML = '<option value="">选择区县</option>';
                        regionInput.value = '';
                        
                        data.data.forEach(function(district) {
                            var option = document.createElement('option');
                            option.value = district.ID;
                            option.textContent = district.Name;
                            areaSelect.appendChild(option);
                        });
                    }
                })
                .catch(function(error) {
                    console.error('加载区县失败:', error);
                });
        }

        // 加载国家列表
        function loadGlobalCountries(selectElement) {
            fetch('/index.php?c=Front/CustomForm&a=getIntlRegion')
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.data) {
                        selectElement.innerHTML = '<option value="">select country</option>';
                        data.data.forEach(function(country) {
                            var option = document.createElement('option');
                            option.value = country.ID;
                            option.textContent = country.Name;
                            selectElement.appendChild(option);
                        });
                    }
                })
                .catch(function(error) {
                    console.error('加载国家失败:', error);
                });
        }

        // 加载国际地区的一级或二级行政区域
        function loadGlobalRegions(parentID, targetSelect, childSelect, regionInput, targetPlaceholder, childPlaceholder) {
            fetch('/index.php?c=Front/CustomForm&a=getIntlRegion&parent_id=' + encodeURIComponent(parentID))
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.data) {
                        targetSelect.innerHTML = '<option value="">' + targetPlaceholder + '</option>';
                        if (childSelect) {
                            childSelect.innerHTML = '<option value="">' + childPlaceholder + '</option>';
                        }
                        regionInput.value = '';

                        data.data.forEach(function(region) {
                            var option = document.createElement('option');
                            option.value = region.ID;
                            option.textContent = region.Name;
                            targetSelect.appendChild(option);
                        });
                    }
                })
                .catch(function(error) {
                    console.error('加载国际地区失败:', error);
                });
        }
        
        // 图片验证码加载和刷新
        var verifyImg = form.querySelector('.verify-img');
        var refreshBtn = form.querySelector('.refresh-btn');
        var verifyInput = form.querySelector('.verify-input');
        
        if (verifyImg && refreshBtn && verifyInput) {
            // 生成验证码URL
            function getVerifyCodeUrl() {
                return '/index.php?c=validatecode&useCurve=1&useNoise=1&fontSize=32&imageW=290&imageH=100&t=' + new Date().getTime();
            }
            
            // 点击输入框显示验证码
            verifyInput.addEventListener('click', function() {
                if (verifyImg.style.display === 'none') {
                    verifyImg.src = getVerifyCodeUrl();
                    verifyImg.style.display = 'block';
                    refreshBtn.style.display = 'inline';
                }
            });
            
            // 点击刷新按钮刷新验证码
            refreshBtn.addEventListener('click', function() {
                verifyImg.src = getVerifyCodeUrl();
            });
        }
        
        // 监听文件选择变化，执行上传
        var fileInputs = form.querySelectorAll('input[type="file"]');
        fileInputs.forEach(function(fileInput) {
            fileInput.addEventListener('change', function() {
                if (!this.files || this.files.length === 0) return;
                
                var fieldName = this.name; // file_{{ field.ID }} 或 file_{{ field.ID }}[]
                var fieldId = fieldName.replace('file_', '').replace('file', '').replace('[]', '');
                
                // 找到对应的hidden input
                var hiddenInput = form.querySelector('input[name="col' + fieldId + '"]');
                if (!hiddenInput) {
                    console.error('未找到对应的隐藏字段: col' + fieldId);
                    return;
                }
                
                // 获取上传状态显示区域
                var uploadStatus = this.closest('.file-operation').querySelector('.upload-status');
                
                // 创建FormData
                var formData = new FormData();
                
                // 多文件上传：一次性将所有文件添加到formData
                if (fieldName.includes('[]')) {
                    Array.from(this.files).forEach(function(file) {
                        formData.append(fieldName, file); // 都使用相同的参数名 file_XXX[]
                    });
                    
                    // 添加文件数量参数
                    formData.append('count', this.files.length);
                    
                    if (uploadStatus) {
                        uploadStatus.textContent = '上传中 ' + this.files.length + '个文件...';
                    }
                } else {
                    // 单文件上传
                    formData.append(fieldName, this.files[0]);
                    
                    if (uploadStatus) {
                        uploadStatus.textContent = '上传中...';
                    }
                }
                
                // 调用上传接口（一次请求）
                // 根据是否为多文件选择不同的接口地址
                var uploadUrl = fieldName.includes('[]') 
                    ? '/index.php?c=Front/CustomForm&a=uploadfiles' 
                    : '/index.php?c=Front/CustomForm&a=uploadfile';
                
                fetch(uploadUrl, {
                    method: 'POST',
                    body: formData
                })
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success && data.newfile) {
                        // 后端返回的newfile已经是逗号分隔的字符串
                        hiddenInput.value = data.newfile;
                        
                        // 解析文件数量用于显示
                        var fileCount = data.newfile.split(',').length;
                        if (uploadStatus) {
                            uploadStatus.textContent = '已上传' + fileCount + (fileCount > 1 ? '个文件' : '张');
                        }
                        
                        // 清空file input，允许重复上传
                        fileInput.value = '';
                    } else {
                        alert(data.msg || '上传失败');
                        if (uploadStatus) {
                            uploadStatus.textContent = '';
                        }
                    }
                })
                .catch(function(error) {
                    alert('网络错误，上传失败');
                    if (uploadStatus) {
                        uploadStatus.textContent = '';
                    }
                    console.error('文件上传错误:', error);
                });
            });
        });
    })();
    </script>
</form>
{% else %}
    <p>表单不存在或没有可用字段</p>
{% endif %}
