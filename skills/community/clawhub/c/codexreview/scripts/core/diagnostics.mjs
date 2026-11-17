import os from "node:os";

export function createDiagnostic(code, level, message, action, detail = "") {
  return {
    code,
    level,
    message,
    action,
    ...(detail ? { detail: redactHome(detail) } : {}),
  };
}

export function redactHome(value) {
  const text = String(value || "");
  const home = os.homedir();
  return home && text.startsWith(home) ? `~${text.slice(home.length)}` : text;
}

export function userError(message, action, detail = "") {
  const error = new Error(message);
  error.userMessage = message;
  error.userAction = action;
  error.userDetail = detail;
  return error;
}

export function formatUserError(error, prefix = "无法完成操作") {
  const message = error?.userMessage || error?.message || "发生未知错误";
  const action = error?.userAction || "请检查输入后重试。";
  const detail = error?.userDetail ? `\n详情：${redactHome(error.userDetail)}` : "";
  return `${prefix}：${message}\n建议：${action}${detail}`;
}
