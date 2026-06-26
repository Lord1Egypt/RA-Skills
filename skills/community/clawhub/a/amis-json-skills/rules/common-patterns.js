/**
 * amis 常见错误模式库
 * 包含错误模式检测和自动修复建议
 */

const errorPatterns = [
  {
    pattern: /missing.*type/i,
    message: '组件缺少type字段',
    fix: '添加 "type": "组件类型"',
    example: '{ "type": "page" }'
  },
  {
    pattern: /missing.*name.*form/i,
    message: 'Form控件缺少name字段',
    fix: '为表单控件添加唯一的name属性',
    example: '{ "type": "text", "name": "username" }'
  },
  {
    pattern: /missing.*api.*crud/i,
    message: 'CRUD缺少api配置',
    fix: '添加api地址用于数据获取',
    example: '{ "api": "/api/data" }'
  },
  {
    pattern: /missing.*columns.*crud/i,
    message: 'CRUD缺少columns配置',
    fix: '添加columns定义表格列',
    example: '{ "columns": [{ "name": "id", "label": "ID" }] }'
  },
  {
    pattern: /invalid.*json/i,
    message: 'JSON格式错误',
    fix: '检查JSON语法，确保引号和括号匹配',
    example: '{"key": "value"}'
  }
];

const warningPatterns = [
  {
    pattern: /button.*without.*action/i,
    message: 'Button未设置操作类型',
    suggestion: '建议设置actionType: dialog/ajax/url/reload等'
  },
  {
    pattern: /form.*without.*api/i,
    message: 'Form未设置提交API',
    suggestion: '建议设置api用于数据提交'
  },
  {
    pattern: /crud.*without.*operation/i,
    message: 'CRUD缺少操作列',
    suggestion: '建议添加type: operation的列用于操作按钮'
  },
  {
    pattern: /dialog.*without.*title/i,
    message: 'Dialog未设置标题',
    suggestion: '建议设置title便于用户理解'
  },
  {
    pattern: /missing.*label.*button/i,
    message: 'Button未设置label',
    suggestion: '建议设置label或icon便于识别'
  }
];

const infoPatterns = [
  {
    pattern: /form.*horizontal/i,
    message: '表单使用横向模式',
    suggestion: '移动端可考虑使用responsive适配'
  },
  {
    pattern: /crud.*table/i,
    message: 'CRUD使用表格模式',
    suggestion: '移动端可考虑使用list或cards模式'
  },
  {
    pattern: /without.*loading/i,
    message: '建议添加loading状态',
    suggestion: '对于异步操作，建议添加loading配置提升用户体验'
  },
  {
    pattern: /without.*description/i,
    message: '建议添加字段说明',
    suggestion: '添加description属性帮助用户理解'
  }
];

function detectErrorPatterns(schemaString) {
  const results = [];
  const schemaStr = JSON.stringify(schemaString);

  errorPatterns.forEach(item => {
    if (item.pattern.test(schemaStr)) {
      results.push({
        type: 'error',
        message: item.message,
        fix: item.fix,
        example: item.example
      });
    }
  });

  return results;
}

function detectWarningPatterns(schemaString) {
  const results = [];
  const schemaStr = JSON.stringify(schemaString);

  warningPatterns.forEach(item => {
    if (item.pattern.test(schemaStr)) {
      results.push({
        type: 'warning',
        message: item.message,
        suggestion: item.suggestion
      });
    }
  });

  return results;
}

function detectInfoPatterns(schemaString) {
  const results = [];
  const schemaStr = JSON.stringify(schemaString);

  infoPatterns.forEach(item => {
    if (item.pattern.test(schemaStr)) {
      results.push({
        type: 'info',
        message: item.message,
        suggestion: item.suggestion
      });
    }
  });

  return results;
}

function getSuggestions(schema) {
  const suggestions = [];

  // 检查移动端适配
  if (schema.type === 'form' && schema.mode === 'horizontal') {
    suggestions.push('移动端适配：可考虑添加responsive配置');
  }

  if (schema.type === 'crud' && schema.mode === 'table') {
    suggestions.push('移动端适配：可考虑添加mobile条件切换为list模式');
  }

  // 检查数据加载
  if (schema.type === 'crud' && !schema.loadDataOnce && !schema.api) {
    suggestions.push('大数据量场景建议考虑loadDataOnce或分页配置');
  }

  // 检查权限控制
  if (schema.type === 'button' && !schema.hiddenOn && !schema.disabled) {
    suggestions.push('建议根据权限配置hiddenOn或disabled属性');
  }

  return suggestions;
}

// 导出函数
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    errorPatterns,
    warningPatterns,
    infoPatterns,
    detectErrorPatterns,
    detectWarningPatterns,
    detectInfoPatterns,
    getSuggestions
  };
}
