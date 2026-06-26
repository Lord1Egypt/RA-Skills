#!/usr/bin/env node
/**
 * HTML 表单生成器 HTML Form Generator 📜
 * 
 * 将字段定义/JSON Schema 转换为 Bootstrap 5 或 Tailwind CSS 格式的 HTML 表单
 */

const fs = require('fs');
const path = require('path');

/**
 * 解析字段定义字符串
 */
function parseFieldDefinition(fieldString) {
  // 格式："field_name:type [required] [options=value1|value2|...] [min/max/step] [placeholder]"
  const parts = fieldString.split(/[\s]+/);
  
  let fieldName = '';
  let fieldType = 'text';
  let required = false;
  let options = [];
  let minMaxStep = {};
  let placeholder = '';
  
  parts[0] && (fieldName = parts[0]);
  if (parts[1]) {
    // 识别类型：text, email, number, password, tel, url, date, datetime-local, select, radio, checkbox, file, textarea
    const typeMatch = parts[1].match(/^([a-zA-Z-]+)(?:\(([^)]+)\))?$/);
    if (typeMatch) {
      fieldType = typeMatch[1];
      minMaxStep.value = typeMatch[2]; // 如 number(5,2)
    } else {
      // 可能是值或选项，看是否包含 pipe
      const hasPipe = parts[1].includes('|');
      if (hasPipe) {
        options.push(...parts[1].split('|').map(opt => opt.trim()));
      } else {
        placeholder = parts[1]; // 当作占位符
      }
    }
  }
  
  return { fieldName, fieldType, required, options, minMaxStep, placeholder };
}

/**
 * 生成 Bootstrap 5 HTML 表单字段
 */
function generateBootstrapField(field) {
  let inputClass = 'form-control';
  let fieldHtml = '';
  
  if (field.fieldType === 'textarea') {
    fieldHtml = `<textarea class="form-control ${field.required ? '' : 'is-invalid'}`} 
      placeholder="${field.placeholder || ''}"
      rows="4"
      name="${field.fieldName}">${field.value || ''}</textarea>`;
  } else if (field.fieldType === 'select') {
    let optionsHtml = field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('');
    fieldHtml = `<select class="form-select ${field.required ? '' : 'is-invalid'}`} 
      name="${field.fieldName}"
      required="${field.required || ''}">
      ${optionsHtml}
    </select>`;
  } else if (field.fieldType === 'radio') {
    fieldHtml = field.options.map((opt, idx) => 
      `<div class="form-check">
        <input class="form-check-input" type="radio" name="${field.fieldName}" value="${opt}" id="rf_${field.fieldName}_${idx}">
        <label class="form-check-label" for="rf_${field.fieldName}_${idx}">${opt}</label>
      </div>`
    ).join('');
  } else if (field.fieldType === 'checkbox') {
    fieldHtml = `<input type="checkbox" class="form-check-input ${field.required ? '' : 'is-invalid'}`} 
      name="${field.fieldName}" 
      id="rf_${field.fieldName}_0">
      <label class="form-check-label" for="rf_${field.fieldName}_0">${field.placeholder || field.options[0] || ''}</label>`;
  } else if (field.fieldType === 'file') {
    fieldHtml = `<input type="file" class="form-control ${field.required ? '' : 'is-invalid'}`} 
      name="${field.fieldName}"
      accept="${field.accept || '*.*'}"` + (field.maxSize ? `max-size="${field.maxSize}"` : '') + (field.maxFiles ? `multiple="${field.maxFiles >= 1}"` : '') + `/>`;
  } else {
    fieldHtml = `<input type="${field.fieldType}" class="form-control ${field.required ? '' : 'is-invalid'}`} 
      name="${field.fieldName}"
      placeholder="${field.placeholder || ''}"
      value="${field.value || ''}"
      required="${field.required || ''}"${field.minMaxStep.min ? ` min="${field.minMaxStep.min}"` : ''}${field.minMaxStep.max ? ` max="${field.minMaxStep.max}"` : ''}${field.minMaxStep.step ? ` step="${field.minMaxStep.step}"` : ''}${field.minLength ? ` minlength="${field.minLength}"` : ''}${field.maxLength ? ` maxlength="${field.maxLength}"` : ''}"${field.autocomplete ? ` autocomplete="${field.autocomplete}"` : ''}">`;
  }
  
  return fieldHtml;
}

/**
 * 生成完整的 Bootstrap 5 HTML 表单
 */
function generateBootstrapForm(fields, formTitle = '', options = {}) {
  const containerClass = options.container || 'container mt-4';
  const cardClass = options.card ? 'card shadow-sm' : '';
  
  let html = `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>${formTitle || '表单'}</title>\n  <!-- Bootstrap 5 CSS -->\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">\n  <style>\n    .needs-validation:not([class*=\`invalid\`]) { \n      justify-content: space-between; \n    }\n    .needs-validation:valid { \n      background-color: #d4edda;\n      border-color: #c3e6cb;\n    }\n  </style>\n</head>\n<body>\n  <div class="${containerClass}">\n    ${formTitle ? `\n      <h1 class="mb-4">${formTitle}</h1>\n    ` : ''}\n    
    <form class="${cardClass}" novalidate>
      ${fields.map(f => `<div class="mb-3">\n        <label for="rf_${f.fieldName}" class="form-label${f.required ? ' required' : ''}">${f.placeholder || f.fieldName}${f.required ? '*' : ''}</label>\n        ${generateBootstrapField(f)}\n      </div>`).join('')}\n      
      <button type="submit" class="btn btn-primary mt-3">提交</button>\n    </form>\n  </div>\n\n  <!-- Bootstrap JS Bundle -->\n  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>\n  \n  <script>\n    (function() {
      "use strict";\n      // Prevent form submission if there are validation errors\n      var form = document.querySelector("form");\n      form.addEventListener("submit", function(event) {\n        if (!form.checkValidity()) {\n          event.preventDefault();\n          event.stopPropagation();\n        }\n        form.classList.add("was-validated");\n      });\n    })();\n  </script>\n</body>\n</html>`;
  
  return html;
}

/**
 * 从 JSON Schema 生成 HTML 表单
 */
function generateFromSchema(schema, options = {}) {
  const fields = [];
  const formTitle = schema.title || '表单';
  
  // 遍历 properties
  if (schema.properties) {
    for (const [fieldName, fieldSchema] of Object.entries(schema.properties)) {
      const fieldDef = parseFieldDefinition(fieldName);
      
      // 覆盖属性（从 schema 中获取更详细的类型信息）
      if (fieldSchema.type) {
        fieldDef.fieldType = fieldSchema.type;
      }
      if (fieldSchema.required && fieldSchema.required.includes(fieldName)) {
        fieldDef.required = true;
      }
      if (fieldSchema.default !== undefined) {
        fieldDef.value = fieldSchema.default;
      }
      if (fieldSchema.placeholder) {
        fieldDef.placeholder = fieldSchema.placeholder;
      }
      
      // 处理 minimum/maximum/exclusiveMinimum/exclusiveMaximum
      if (fieldSchema.minimum !== undefined) fieldDef.minMaxStep.min = fieldSchema.minimum;
      if (fieldSchema.maximum !== undefined) fieldDef.minMaxStep.max = fieldSchema.maximum;
      if (fieldSchema.exclusiveMinimum !== undefined) fieldDef.minMaxStep.min = fieldSchema.exclusiveMinimum;
      if (fieldSchema.exclusiveMaximum !== undefined) fieldDef.minMaxStep.max = fieldSchema.exclusiveMaximum;
      
      // 处理 pattern（正则验证）
      if (fieldSchema.pattern) {
        fieldDef.pattern = fieldSchema.pattern;
      }
      
      // 处理 enum（select 或 radio 选项）
      if (Array.isArray(fieldSchema.enum)) {
        fieldDef.fieldType = 'select';
        fieldDef.options = fieldSchema.enum;
      } else if (fieldSchema['x-radio'] === true) {
        fieldDef.fieldType = 'radio';
        if (!fieldDef.options && Array.isArray(fieldSchema.enum)) {
          fieldDef.options = fieldSchema.enum;
        }
      }
      
      fields.push(fieldDef);
    }
  }
  
  // 处理 required 数组（在 schema.required 中）
  const requiredFields = schema.required || [];
  fields.forEach(f => {
    if (requiredFields.includes(f.fieldName)) {
      f.required = true;
    }
  });
  
  return generateBootstrapForm(fields, formTitle, options);
}

/**
 * 将字段定义字符串数组转换为表单
 */
function generateFromFieldDefinitions(fieldDefs, title) {
  const fields = fieldDefs.map(define => parseFieldDefinition(define));
  return generateBootstrapForm(fields, title || '表单');
}

// CLI 使用示例
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help')) {
    console.log(`
HTML 表单生成器 v1.0

用法:
  # 从字段定义字符串数组生成表单
  node html_form_generator.js --fields "name:text,age:number,city:select(Beijing|Shanghai|Guangzhou)" \
    --title "用户信息" \
    --output form.html
  
  # 从 JSON Schema 生成表单
  node html_form_generator.js --schema schema.json --framework bootstrap
  
  # 直接输出到 stdout
  node html_form_generator.js <field_definitions>

选项:
  --fields       字段定义字符串（多个用,分隔）
  --schema       JSON Schema 文件路径
  --title        表单标题（可选）
  --output       输出文件路径（可选，默认输出到 stdout）
  --framework    Bootstrap|Tailwind（默认：Bootstrap）
  --min/max      number 字段的最小/最大值
  --step         number 字段的步长
  --placeholder  输入框占位符文本
  --help         显示此帮助信息

示例:
  node html_form_generator.js --fields "name:text,age:number(50)" \
    --title "员工登记"
    `);
    process.exit(0);
  }
}

main().catch(console.error);
