/**
 * amis JSON Schema 校验器
 * 功能：检查配置的正确性，输出error/warning/info级别警告
 */

function validateAmisSchema(schema) {
  const result = {
    valid: true,
    errors: [],
    warnings: [],
    suggestions: [],
  };

  if (!schema || typeof schema !== "object") {
    result.valid = false;
    result.errors.push({
      type: "error",
      message: "Schema必须是有效的JSON对象",
    });
    return result;
  }

  // 检查根节点必须有type
  if (!schema.type) {
    result.errors.push({ type: "error", message: "缺少必填字段：type" });
    result.valid = false;
  }

  // 校验Page组件
  if (schema.type === "page") {
    validatePage(schema, result);
  }

  // 校验Form组件
  if (schema.type === "form") {
    validateForm(schema, result);
  }

  // 校验CRUD组件
  if (schema.type === "crud") {
    validateCrud(schema, result);
  }

  // 校验Dialog组件
  if (schema.type === "dialog" || schema.type === "drawer") {
    validateDialog(schema, result);
  }

  // 校验Button组件
  if (schema.type === "button") {
    validateButton(schema, result);
  }

  // 校验Wizard组件
  if (schema.type === "wizard") {
    validateWizard(schema, result);
  }

  // 检查API配置
  validateApiConfig(schema, result);

  // 检查事件动作配置
  validateEventActions(schema, result);

  // 集成通用模式告警检测
  if (typeof require !== "undefined") {
    try {
      const commonPatterns = require("./common-patterns");
      const errs = commonPatterns.detectErrorPatterns(schema);
      const warns = commonPatterns.detectWarningPatterns(schema);
      const infos = commonPatterns.detectInfoPatterns(schema);
      const suggests = commonPatterns.getSuggestions(schema);

      errs.forEach((e) => result.errors.push(e));
      warns.forEach((w) => result.warnings.push(w));
      infos.forEach((i) => result.suggestions.push(i));
      suggests.forEach((s) =>
        result.suggestions.push({ type: "suggestion", message: s }),
      );
    } catch (e) {
      // ignore
    }
  }

  return result;
}

function validatePage(schema, result) {
  if (!schema.body) {
    result.warnings.push({ type: "warning", message: "Page建议设置body属性" });
  }
}

function validateForm(schema, result) {
  if (!schema.controls && !schema.body) {
    result.errors.push({
      type: "error",
      message: "Form建议设置body以替代旧版的controls",
    });
    result.valid = false;
  }

  const formItems = schema.body || schema.controls;

  if (formItems && Array.isArray(formItems)) {
    formItems.forEach((control, index) => {
      if (
        control.type &&
        control.type !== "button" &&
        control.type !== "submit" &&
        control.type !== "reset"
      ) {
        if (!control.name) {
          result.warnings.push({
            type: "warning",
            message: `表单项[${index}] 建议设置name字段`,
          });
        }
      }
    });
  }

  if (!schema.api && !schema.initApi) {
    result.warnings.push({
      type: "warning",
      message: "Form建议设置api用于数据提交",
    });
  }
}

function validateCrud(schema, result) {
  if (!schema.api) {
    result.errors.push({ type: "error", message: "CRUD必须设置api" });
    result.valid = false;
  }

  if (!schema.columns) {
    result.errors.push({ type: "error", message: "CRUD必须设置columns" });
    result.valid = false;
  }

  if (schema.columns && Array.isArray(schema.columns)) {
    const hasOperation = schema.columns.some((col) => col.type === "operation");
    if (!hasOperation) {
      result.suggestions.push({
        type: "info",
        message: "CRUD建议添加operation列用于操作按钮",
      });
    }
  }
}

function validateDialog(schema, result) {
  if (!schema.body) {
    result.errors.push({ type: "error", message: "Dialog必须设置body" });
    result.valid = false;
  }

  if (!schema.title) {
    result.warnings.push({ type: "warning", message: "Dialog建议设置title" });
  }
}

function validateButton(schema, result) {
  if (!schema.label && !schema.icon) {
    result.warnings.push({
      type: "warning",
      message: "Button建议设置label或icon",
    });
  }

  if (!schema.actionType && !schema.onEvent) {
    result.warnings.push({
      type: "warning",
      message: "Button建议设置actionType或onEvent",
    });
  }
}

function validateWizard(schema, result) {
  if (!schema.steps || !Array.isArray(schema.steps)) {
    result.errors.push({ type: "error", message: "Wizard必须设置steps数组" });
    result.valid = false;
  }

  if (schema.steps) {
    schema.steps.forEach((step, index) => {
      if (!step.title) {
        result.warnings.push({
          type: "warning",
          message: `steps[${index}] 建议设置title`,
        });
      }
      if (!step.controls && !step.body) {
        result.warnings.push({
          type: "warning",
          message: `steps[${index}] 建议设置controls或body`,
        });
      }
    });
  }

  if (!schema.api) {
    result.warnings.push({
      type: "warning",
      message: "Wizard建议设置api用于最终提交",
    });
  }
}

function validateApiConfig(schema, result) {
  const api = schema.api;
  if (!api) return;

  if (typeof api === "string") {
    if (!api.match(/^(get|post|put|delete):/i) && !api.startsWith("/")) {
      result.warnings.push({
        type: "warning",
        message: "API地址建议以/开头或包含HTTP方法",
      });
    }
  } else if (typeof api === "object") {
    if (!api.url) {
      result.errors.push({ type: "error", message: "API配置缺少url字段" });
      result.valid = false;
    }
    if (!api.method) {
      result.warnings.push({
        type: "warning",
        message: "API配置建议设置method",
      });
    }
  }
}

function validateEventActions(schema, result) {
  if (!schema.onEvent) return;

  for (const [eventName, eventConfig] of Object.entries(schema.onEvent)) {
    if (!eventConfig.actions) {
      result.warnings.push({
        type: "warning",
        message: `onEvent.${eventName} 建议设置actions`,
      });
      continue;
    }

    eventConfig.actions.forEach((action, index) => {
      if (!action.actionType) {
        result.warnings.push({
          type: "warning",
          message: `onEvent.${eventName}.actions[${index}] 建议设置actionType`,
        });
      }
    });
  }
}

// 导出校验函数
if (typeof module !== "undefined" && module.exports) {
  module.exports = { validateAmisSchema };
}
