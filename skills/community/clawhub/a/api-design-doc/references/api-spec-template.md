### 接口编号（API-Id）**：顺序生成，格式为 API001-接口名称，如 API001-用户登录, API002-获取用户列表, ...
- **功能描述**：详细描述接口的功能和用途
- **入参**：参数类型和说明
  - `param1`: `type` - 参数1说明（必填/可选）
  - `param2`: `type` - 参数2说明（必填/可选）
- **返回参数**：返回值类型和说明
  - `field1`: `type` - 字段1说明
  - `field2`: `type` - 字段2说明
- **URL地址**：`/api/endpoint`
- **请求方式**：`GET/POST/PUT/DELETE`
- **接口 JSON 示例**：
```json
// 请求示例
{
  "param1": "value1",
  "param2": "value2"
}

// 响应示例
{
  "code": 0,
  "message": "success",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}