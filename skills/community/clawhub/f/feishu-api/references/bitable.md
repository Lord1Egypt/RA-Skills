# 多维表格（Bitable）API

## 资源结构

```
多维表格 App (app_token)
└── 表 (table_id)
    ├── 字段 (field_id)
    └── 记录 (record_id)
```

获取 app_token 和 table_id：
- URL: `https://xxx.feishu.cn/base/{app_token}?table={table_id}`
- app_token: `base` 后第一段
- table_id: `table=` 参数值

## 字段类型

| type | 类型 | 说明 |
|------|------|------|
| 1 | Text | 文本 |
| 2 | Number | 数字 |
| 3 | SingleSelect | 单选 |
| 4 | MultiSelect | 多选 |
| 5 | DateTime | 日期时间 |
| 7 | Checkbox | 复选框 |
| 11 | User | 用户 |
| 13 | Phone | 电话 |
| 15 | URL | 链接 |
| 17 | Attachment | 附件 |
| 18 | SingleLink | 单向链接 |
| 19 | Lookup | 查找 |
| 20 | Formula | 公式 |
| 21 | DuplexLink | 双向链接 |
| 22 | Location | 地理位置 |
| 23 | GroupChat | 群组 |
| 1001 | CreatedTime | 创建时间 |
| 1002 | ModifiedTime | 修改时间 |
| 1003 | CreatedUser | 创建人 |
| 1004 | ModifiedUser | 修改人 |
| 1005 | AutoNumber | 自动编号 |

## 记录操作

### 批量创建记录

```
POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create
```

```python
payload = {
    'records': [
        {
            'fields': {
                '文本字段名': '值',
                '数字': 123,
                '单选': '选项1',
                '多选': ['选项1', '选项2'],
                '用户': [{'id': 'ou_xxx'}],
                '链接': {'text': '显示文本', 'link': 'https://...'}
            }
        }
    ]
}
# 响应
{'code': 0, 'data': {'records': [{'record_id': 'recxxx', ...}]}}
```

### 批量删除记录

```
POST /bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete
```

```python
payload = {'records': ['recxxx1', 'recxxx2', ...]}
# 建议每批不超过 50 条
```

### 更新记录

```
PUT /bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
```

```python
payload = {'fields': {'字段名': '新值'}}
```

### 查询记录

```
GET /bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=100
```

## 字段操作

### 创建字段

```
POST /bitable/v1/apps/{app_token}/tables/{table_id}/fields
```

```python
payload = {
    'field_name': '新字段',
    'type': 1,  # 字段类型
    'property': {}  # 类型相关属性
}
```

### 批量创建字段

```
POST /bitable/v1/apps/{app_token}/tables/{table_id}/fields/batch_create
```

```python
payload = {
    'fields': [
        {'field_name': '字段1', 'type': 1},
        {'field_name': '字段2', 'type': 2}
    ]
}
```

## 常用字段格式

### 用户类型

```python
{'id': 'ou_xxx'}  # 单个用户
[{'id': 'ou_xxx'}, {'id': 'ou_yyy'}]  # 多个用户
```

### 日期时间

```python
# 毫秒时间戳
1699999999000
```

### 链接

```python
{'text': '链接文字', 'link': 'https://example.com'}
```

## 注意事项

1. **批量限制**：每批最多 50 条记录
2. **频率限制**：每秒 10 请求
3. **字段名匹配**：创建/更新时字段名必须与飞书表中的名称完全一致
4. **必填字段**：主键字段必须提供