# 通用错误处理

## 异常体系

```
SkillError (基类, code=500)
+-- AuthError      (AK 无效/签名失败/未配置, code=401)
+-- ParamError     (请求参数不合法, code=400)
+-- RateLimitError (请求被限流, code=429)
+-- ServiceError   (服务端异常/网络异常, code=500)
+-- TimeoutError   (请求超时, code=504)
```

## 错误识别与 Agent 应对

命令输出 `success: false` 时，先输出 `markdown` 字段，再根据关键词引导：

| markdown 关键词    | Agent 应对                                     |
| ------------------ | ---------------------------------------------- |
| "AK 未配置"        | 运行 `cli.py configure YOUR_AK` 或检查环境变量 |
| "认证失败" / "401" | AK 无效或过期，需重新配置                      |
| "限流" / "429"     | 等待 1-2 分钟重试                              |
| "超时" / "504"     | 接口较慢，已内置自动重试，可稍后再试           |
| "连接错误"         | 检查网络                                       |
| 其他               | 仅输出 markdown 即可                           |

## 输出格式

所有异常统一转为标准 JSON：
```json
{
  "success": false,
  "markdown": "错误描述（用户可读）",
  "data": {}
}
```

## 环境变量覆盖

| 环境变量               | 说明                  | 默认值 |
| ---------------------- | --------------------- | ------ |
| `COWBOY_REPORT_TIMEOUT` | 工作日报接口超时(秒)  | 30     |
