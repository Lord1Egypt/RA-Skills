// Adapt response/status fields to the real HTTP contract. No network or module calls.
function main({response, error, configured}) {
  if (configured === false) return {state:"not_configured", text:"接口未配置，未执行请求"};
  if (String(error || "").trim()) return {state:"request_error", text:"请求失败，请查看脱敏运行记录"};
  if (response && typeof response === "object" && Number(response.statusCode) >= 400)
    return {state:"request_error", text:"请求失败，请查看脱敏运行记录"};
  if (response == null || response === "" || (Array.isArray(response) && response.length === 0))
    return {state:"empty", text:"请求已返回空结果"};
  return {state:"received", text:"接口已返回，待按业务契约解析"};
}
