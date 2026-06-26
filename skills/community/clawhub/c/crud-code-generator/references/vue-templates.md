# Vue 前端代码模板参考

> 模板中的 `xxx-yyy` 替换为中划线分隔的页面名称，`xxxYyy` 替换为小写驼峰，`XxxYyy` 替换为大写驼峰，`表中文字名` 替换为表注释。

---

## 0. 前端字典说明

> 字典数据由后端 `sys_dict` / `sys_dict_detail` 表管理，通过 API `getDictMapAll` 加载到 Vuex `permission.dict` 中。

### 字典来源

前端页面使用的字典数据来自后端数据库：
- `sys_dict` — 字典类型表
- `sys_dict_detail` — 字典明细表
- 前端通过 `getDictMapAll()` API 加载所有字典数据到 Vuex store

### 生成字典 SQL

为每个新生成的枚举类，在 DML SQL 文件中添加对应的 `sys_dict` / `sys_dict_detail` 插入语句。参见 [sql-templates.md](sql-templates.md) 第 3 节。

### 前端使用方式

```js
// co-select 下拉选项
:options="dict.ces_xxx_enum"

// 表格列格式化显示
format: val => getDictLabel('ces_xxx_enum', val)

// 表单只读字段显示
:value="getDictLabel('ces_xxx_enum', form.enumField)"
```

### 命名约定

- 字典 key 格式: `ces_{枚举名小写下划线}`
- 如枚举名 `XxxStatusEnum` → `ces_xxx_status`
- 字典 value 使用枚举的 code 值（字符串形式）
- 布尔类型字段不需要字典，前端用 `i18n.t('enable')` / `i18n.t('disable')` 显示

---

## 1. API 文件模板
