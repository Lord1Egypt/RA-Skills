#!/usr/bin/env node
/**
 * 表单验证器 Form Validator 📜
 * 
 * 实现实时客户端验证、错误提示和渐进式增强
 */

const fs = require('fs');

/**
 * 验证器工厂 - 根据字段类型创建验证函数
 */
function createValidator(fieldDefinition) {
  const validators = {};
  
  // 必填验证
  validators.required = (value) => !['', null, undefined].includes(value);
  
  // 文本验证（最小/最大长度）
  if (fieldDefinition.minLength !== undefined) {
    validators.minLength = (value) => value.length >= fieldDefinition.minLength;
  }
  
  if (fieldDefinition.maxLength !== undefined) {
    validators.maxLength = (value) => value.length <= fieldDefinition.maxLength;
  }
  
  // email 验证（正则）
  if (fieldDefinition.fieldType === 'email') {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    validators.emailFormat = (value) => emailRegex.test(value);
  }
  
  // 电话号码验证
  if (fieldDefinition.fieldType === 'tel') {
    const phoneRegex = /^1[3-9]\d{9}$/; // 中国大陆手机号
    validators.phoneFormat = (value) => phoneRegex.test(value);
  }
  
  // number 验证（最小/最大/步长）
  if (fieldDefinition.fieldType === 'number') {
    if (fieldDefinition.minimum !== undefined) {
      validators.minValue = (value) => value >= fieldDefinition.minimum;
    }
    
    if (fieldDefinition.maximum !== undefined) {
      validators.maxValue = (value) => value <= fieldDefinition.maximum;
    }
    
    // 步长验证（值应该是 step 的倍数）
    if (fieldDefinition.step !== undefined) {
      validators.stepValidation = (value) => {
        const remainder = Math.abs(value - Math.round(value / fieldDefinition.step) * fieldDefinition.step);
        return remainder < Number.EPSILON;
      };
    }
  }
  
  // select 验证（从选项列表中）
  if (fieldDefinition.fieldType === 'select' && fieldDefinition.options) {
    validators.inOptions = (value) => fieldDefinition.options.includes(value);
  }
  
  // 文件上传验证
  if (fieldDefinition.fieldType === 'file') {
    const fileValidators = {};
    
    // 文件大小限制
    if (fieldDefinition.maxSize !== undefined) {
      const maxSizeBytes = parseInt(fieldDefinition.maxSize);
      fileValidators.fileSizeLimit = (file) => file.size <= maxSizeBytes;
    }
    
    // 文件类型限制（扩展名）
    if (fieldDefinition.accept) {
      const allowedExtensions = fieldDefinition.accept.split(',').map(ext => ext.trim().toLowerCase());
      const fileValidator = (file) => {
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        return allowedExtensions.includes(extension);
      };
      
      fileValidators.allowedExtension = fileValidator;
    }
    
    return { required: validators.required, ...fileValidators };
  }
  
  // 自定义验证（异步 API 调用）
  if (fieldDefinition.api) {
    async function apiValidation(value) {
      // TODO: 实际实现时调用 API 验证用户名/邮箱是否已存在
      return true; // 默认返回 true
    }
    
    validators.apiCheck = apiValidation;
  }
  
  return validators;
}

/**
 * 生成实时验证逻辑的 JavaScript 代码片段
 */
function generateRealtimeValidationCode(fields) {
  const fieldObjects = fields.map(f => ({
    id: `rf_${f.fieldName}`,
    name: f.fieldName,
    type: f.fieldType,
    validators: createValidator(f),
    required: f.required || false,
    placeholder: f.placeholder || ''
  }));
  
  const errorMessages = {};
  fieldObjects.forEach(field => {
    if (field.validators.required) errorMessages[`${field.name}_required`] = `请输入${field.placeholder || field.fieldName}`;
    if (field.validators.minLength) errorMessages[`${field.name}_minlength`] = `长度至少为 ${field.validators.minLength} 个字符`;
    if (field.validators.maxLength) errorMessages[`${field.name}_maxlength`] = `长度不能超过 ${field.validators.maxLength} 个字符`;
    if (field.validators.emailFormat) errorMessages[`${field.name}_email`] = '请输入有效的邮箱地址';
    if (field.validators.phoneFormat) errorMessages[`${field.name}_phone`] = '请输入有效的电话号码';
    if (field.validators.minValue) errorMessages[`${field.name}_minvalue`] = `最小值为 ${field.validators.minValue}`;
    if (field.validators.maxValue) errorMessages[`${field.name}_maxvalue`] = `最大值为 ${field.validators.maxValue}`;
    if (field.validators.inOptions) errorMessages[`${field.name}_options`] = '请从列表中选择';
  });
  
  let validationCode = `// 实时验证逻辑\n`;\n` +
    `\nclass RealtimeValidator {\n`;
  
  fieldObjects.forEach((field, idx) => {
    const id = field.id;
    const name = field.name;
    
    validationCode += `  ${id}_validator = {${"\n"`};
    validationCode += `    id: '${id}',${"\n"`};
    validationCode += `    name: '${name}',${"\n"`;
    validationCode += `    required: ${field.required},${"\n"`};
    validationCode += `    errorElement: document.getElementById('${id}'),`;
    validationCode += `\n`;\n` +
    `  };\n`;
  });
  
  validationCode += `\n  // 监听输入事件\n`;\n` +
    `  fieldObjects.forEach(field => {\n`;\n` +
    `    const id = field.id;\n`;\n` +
    `    const errorElement = document.getElementById(id);\n`;\n` +
    `    const parent = errorElement.parentElement;\n`;\n` +
    `    const input = field.type === 'textarea' ? errorElement : errorElement.querySelector('input');\n`;\n` +
    `\n`;
    validationCode += `    // 输入时清除错误\n`;\n` +
    `    if (input) {\n`;\n` +
    `      input.addEventListener('input', () => {\n`;\n` +
    `        parent.classList.remove('is-invalid');\n`;\n` +
    `        parent.classList.add('is-valid');\n`;\n` +
    `      });\n`;\n` +
    `    }\n`;\n` +
    `\n`;
    validationCode += `    // 失焦时验证\n`;\n` +
    `    if (input) {\n`;\n` +
    `      input.addEventListener('blur', () => {\n`;\n` +
    `        const value = input.value.trim();\n`;\n` +
    `        validateField(field, value);\n`;\n` +
    `      });\n`;\n` +
    `    }\n`;\n` +
    `\n`;
    validationCode += `    if (field.type === 'select') {\n`;\n` +
    `      input = errorElement.querySelector('option'); // 处理 select\n`;\n` +
    `      input.addEventListener('change', () => {\n`;\n` +
    `        validateField(field, input.value);\n`;\n` +
    `      });\n`;\n` +
    `    }\n`;\n` +
    `\n`;
    validationCode += `    if (field.type === 'checkbox') {\n`;\n` +
    `      const checkbox = errorElement.querySelector('input[type="checkbox"]');\n`;\n` +
    `      checkbox.addEventListener('change', () => {\n`;\n` +
    `        validateField(field, checkbox.checked);\n`;\n` +
    `      });\n`;\n` +
    `    }\n`;\n` +
    `\n`;
    validationCode += `    if (field.type === 'file') {\n`;\n` +
    `      const fileInput = errorElement.querySelector('input[type="file"]');\n`;\n` +
    `      fileInput.addEventListener('change', () => {\n`;\n` +
    `        validateFileUpload(field, fileInput.files[0]);\n`;\n` +
    `      });\n`;\n` +
    `    }\n`;\n` +
    `\n`;
    validationCode += `  });\n`;
  
  validationCode += `\n  // 验证单个字段\n`;\n` +
    `  function validateField(field, value) {\n`;\n` +
    `    const errorElement = field.errorElement || document.getElementById(field.id);\n`;\n` +
    `    const parent = errorElement.parentElement;\n`;\n` +
    `\n`;
    validationCode += `    if (!field.required && !['', null, undefined].includes(value)) {\n`;\n` +
    `      // 非必填字段且有值则视为有效\n`;\n` +
    `      parent.classList.remove('is-invalid');\n`;\n` +
    `      return true;\n`;\n` +
    `    }\n`;
  
  // 添加所有验证器
  fieldObjects.forEach(field => {
    for (const [validatorName, validator] of Object.entries(field.validators)) {
      if (validator !== validators.required) {
        validationCode += `    \n`;
        validationCode += `    if (${validatorName}(value)) {\n`;
        validationCode += `      parent.classList.remove('is-invalid');\n`;
        validationCode += `      parent.classList.add('is-valid');\n`;
        validationCode += `      return true;\n`;
        validationCode += `    }\n`;
        validationCode += `  } else {\n`;
        validationCode += `    parent.classList.remove('is-valid');\n`;
        validationCode += `    parent.classList.add('is-invalid');\n`;
        validationCode += `    // TODO: 显示错误信息\n`;
      }
    }
  });
  
  validationCode += `    return false;\n`;\n` +
    `  }\n`;\n` +
    `\n`;
  validationCode += `  // 验证文件上传\n`;\n` +
    `  function validateFileUpload(field, file) {\n`;\n` +
    `    if (!file) return true; // 空文件视为有效（用户未选择）\n`;\n` +
    `\n`;
  validationCode += `    const errorElement = field.errorElement || document.getElementById(field.id);\n`;\n` +
    `    const parent = errorElement.parentElement;\n`;\n` +
    `\n`;
    validationCode += `    // TODO: 添加文件大小/类型验证\n`;\n` +
    `    return true; \n`;\n` +
    `  }\n`;\n` +
    `\n`;
    validationCode += `  // 暴露到 window（供表单脚本调用）\n`;\n` +
    `  window.RealtimeValidator = this;\n`;
  
  return validationCode;
}

/**
 * 生成完整的验证器脚本和 HTML
 */
function generateCompleteFormWithValidation(htmlContent, fields) {
  const validationScript = generateRealtimeValidationCode(fields);
  
  // 将验证逻辑注入到 HTML 中
  const completeHtml = htmlContent + `</body>\n\n`;\n` +
    `${validationScript}\n`;\n` +
    `<script>\n`;\n` +
    `// 暴露到全局，供表单脚本调用\n`;\n` +
    `window.RealtimeValidator = new RealtimeValidator();\n`;\n` +
    `</script>\n`;\n` +
    `<!-- Bootstrap Validation CSS -->\n`;\n` +
    `<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">\n`;\n` +
    `<!-- 验证逻辑注入完成 -->\n`;
  
  return completeHtml;
}

// CLI 使用示例
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help')) {
    console.log(`
表单验证器 v1.0

用法:
  # 生成验证逻辑
  node validator.js --fields "name:text,minLength=3,maxLength=50,email=email,phone=tel" \
    --output validation_logic.js
  
  # 将验证逻辑注入到已有 HTML
  node validator.js --inject-file form.html --fields "..." \
    --output form_validated.html

选项:
  --fields       字段定义（同 html_form_generator.js）
  --inject-file  要注入验证逻辑的 HTML 文件路径
  --output       输出文件路径（可选，默认输出到 stdout）
  --help         显示此帮助信息
    `);
    process.exit(0);
  }
}

main().catch(console.error);
