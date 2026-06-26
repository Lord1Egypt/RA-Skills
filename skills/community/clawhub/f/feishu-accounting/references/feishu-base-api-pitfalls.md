# 飞书 base/v3 API 踩坑记录

## 1. Record 创建：不加 `fields` 包装

```python
# ✅ 正确（base/v3 API 直接平铺字段）
payload = {
    "月份": "2026-05",
    "分类": "餐饮",
    "金额": 23.40,
    "文本": "2026-05-15 13:11午饭",
}

# ❌ 错误（这是其他飞书 API 的格式，base/v3 不支持）
payload = {
    "fields": {
        "月份": "2026-05",
        ...
    }
}
```

错误响应：`"Record write payload must not be wrapped in 'fields'."`

## 2. Tenant Token 分页上限只有 ~20 条

`page_size=100` 参数在 Tenant Token 下实际只返回 20 条（实测验证），`has_more` 正常指示。

**正确翻页写法：**

```python
offset = 0
while True:
    url = f"/records?page_size=100&offset={offset}"
    # ... 请求 ...
    records = data["data"]["data"]
    if not records:
        break
    for rec in records:
        process(rec)
    offset += len(records)  # 按实际返回数累加，而非固定步长
```

**错误写法（会漏数据）：**
```python
offset += 100  # ❌ 实际只返回 20 条，offset=100 跳过了 21-100
```

## 3. 字段创建后需等待缓存生效

创建字段后立即更新选项（UPDATE field）需要加 `time.sleep(1)`，否则飞书返回 400。

```python
def update_field_options(...):
    time.sleep(1)  # 等待字段创建缓存生效
    # 然后才能 PUT 更新选项
```

## 4. 地址恢复与字段映射

```
创建多维表格: data["base_token"]        # 不是 data["base"]["token"]
创建数据表:   data["id"]                # 不是 data["table_id"]
创建字段:     data["id"]                # 不是 data["field"]["id"]
更新字段:     用 PUT                     # 不是 PATCH
```

每次写字段前，建议调 `GET /fields` 确认字段顺序和 ID，不要靠记忆写死 index。

## 5. `.env` 加载：用直接赋值覆盖父 shell 变量

```python
# ❌ 错误：setdefault 不覆盖已存在的环境变量
# 如果父 shell 已有 FEISHU_APP_ID（旧应用的），.env 的值会被忽略
os.environ.setdefault(k.strip(), v.strip())

# ✅ 正确：直接赋值，.env 始终优先
os.environ[k.strip()] = v.strip()
```
