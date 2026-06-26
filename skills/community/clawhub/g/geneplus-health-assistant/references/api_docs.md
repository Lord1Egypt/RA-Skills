# API文档参考

## 接口信息

### 基础配置

| 配置项 | 值 |
|-------|-----|
| Base URL | `https://ydai.jinbaisen.com/api/v1` |
| API Key | `fastgpt-aIOCbwavMirdBk08oHQyDxudE56DBnksVXUL4m8c50CuPnTNGqK5yX7Ykm` |
| Model | `cyzh-cfc` |

### 请求参数

```json
{
  "model": "cyzh-cfc",
  "messages": [
    {"role": "system", "content": "系统提示"},
    {"role": "user", "content": "用户输入"},
    {"role": "assistant", "content": "助手回复"}
  ],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### 响应格式

流式响应 (SSE格式)：
```
data: {"choices":[{"delta":{"content":"内容片段"}}]}
data: [DONE]
```

## 信息收集要求

### 必填信息

1. **基础人口学特征**
   - 姓名
   - 年龄
   - 生理性别
   - 常住地域
   - 职业

2. **健康病史信息**
   - 既往病史
   - 家族遗传史
   - 生活方式与行为暴露（吸烟、饮酒、熬夜等）

3. **用药与特殊状态**
   - 当前用药史
   - 过敏史
   - 女性特殊状态（备孕、孕期、哺乳期等）

### 关键信息

4. **检验单据文本**
   - 体检报告
   - 化验单
   - 检验单数据

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 请求超时 | 提示"云端健康计算引擎暂时未响应，请稍后再试或重新发送您的数据" |
| API错误 | 提示具体错误信息，建议重新发送数据 |
| 网络异常 | 提示检查网络连接后重试 |
