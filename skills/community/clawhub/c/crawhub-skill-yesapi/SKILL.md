--- name: yesapi description: YesApi果创云低代码平台接口封装，支持表单结构和数据操作 version: 1.0.0 homepage: https://api.yesapi.net/ user-invocable: true metadata: {"requires": {"env": ["YESAPI_APP_KEY", "YESAPI_DOMAIN", "YESAPI_SIGN"]}, "tags": ["api", "lowcode", "yesapi", "form", "database"]} ---

# YesApi 果创云低代码平台 Skill

本技能提供对 YesApi 果创云低代码平台的完整接口封装，支持表单结构管理和数据操作。

## 配置要求

在使用前需要配置以下环境变量：

- `YESAPI_APP_KEY`: 你的果创云应用密钥
- `YESAPI_DOMAIN`: 果创云API域名（默认：https://api.yesapi.net）
- `YESAPI_SIGN`: 静态签名密钥

## 功能特性

### 1. 表单结构管理
- 获取表单模型列表
- 创建表单模型
- 更新表单结构
- 删除表单模型

### 2. 表单数据操作
- 通用数据查询（支持分页、过滤、排序）
- 数据新增
- 数据更新
- 数据删除
- 批量更新
- 批量删除

## 使用方法

### 获取表单列表
```
获取我的表单模型列表
```

### 查询表单数据
```
查询表单 [表单名] 的数据，限制10条记录
```

### 创建新数据
```
向表单 [表单名] 添加新数据：{"field1": "value1", "field2": "value2"}
```

### 更新数据
```
更新表单 [表单名] 中ID为 [记录ID] 的数据：{"field1": "new_value"}
```

### 删除数据
```
删除表单 [表单名] 中ID为 [记录ID] 的记录
```

### 批量更新数据
```
批量更新表单 [表单名] 中满足条件的数据：{"field1": "new_value"}，指定条件where：[["字段名", "比较符", "比较值"]]
```

### 批量删除数据
```
批量删除表单 [表单名] 中满足条件的记录，指定条件where：[["字段名", "比较符", "比较值"]]
```

## API 接口封装

### 表单结构接口
基于 `App.Platform_MyModels` 接口封装：
- `get_models()`: 获取模型列表
- `create_model(model_name)`: 创建新模型
- `delete_model(model_name)`: 删除模型
- `add_model_new_field(model_name, field_data)`: 为模型添加新字段

### 表单数据接口
基于 `App.Table` 系列接口封装：
- `query_data(model_name, params)`: 查询数据
- `insert_data(model_name, data)`: 插入数据
- `update_data(model_name, id, data)`: 更新数据
- `delete_data(model_name, id)`: 删除数据
- `batch_update(model_name, where, data)`: 批量更新数据
- `batch_delete(model_name, where)`: 批量删除数据

## 错误处理

所有API调用都会返回详细的错误信息，包括：
- HTTP状态码
- 错误代码
- 错误消息
- 建议解决方案

## 最佳实践

1. **配置管理**: 建议使用环境变量管理敏感信息
2. **错误重试**: 网络请求支持自动重试机制
3. **数据验证**: 在发送数据前进行本地验证
4. **日志记录**: 重要操作会记录详细日志

## 技术实现

- 使用 Python 的 `requests` 库进行HTTP请求
- 支持异步操作提高性能
- 内置签名算法确保API安全
- 完整的类型提示支持

## 依赖项

- Python 3.8+
- requests >= 2.28.0
- pydantic >= 1.10.0
- python-dotenv >= 0.19.0

## 许可证

MIT License
