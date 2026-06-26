# SQL 模板参考

> 模板中的 `ces_xxx_yyy` 替换为实际表名，`表中文字名` 替换为表注释。

---

## 1. DDL 模板

**路径**: `sql/{year}/{month}/ddl-YYYYMMDD-表名.sql`

```sql
-- 建表语句由 DDL 原文件提供，直接复制原始 CREATE TABLE 语句
-- 以下仅为格式参考

DROP TABLE IF EXISTS ces_xxx_yyy;
CREATE TABLE ces_xxx_yyy (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    operator_id         BIGINT UNSIGNED NOT NULL COMMENT '运营商ID',
    -- ... 其他字段按原始 DDL
    create_user         BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '创建人',
    create_time         DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_user         BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '更新人',
    update_time         DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='表中文字名';
```

**注意**: DDL 文件内容应直接取自用户提供的原始 SQL，无需修改。如果表名已有完整建表语句，直接使用该语句。

---

## 2. DML 模板（菜单权限）

**路径**: `sql/{year}/{month}/dml-YYYYMMDD-表名.sql`

```sql
-- 菜单权限 SQL
-- 注意：以下 SQL 中的 pid 需要根据实际父菜单 ID 调整

-- 查询权限
SET @lastId = (SELECT id FROM sys_menu WHERE title = '表中文字名');

-- 如果父菜单不存在，需要先创建父菜单
-- INSERT INTO sys_menu (id, pid, sub_count, type, title, title_letter, title_en, sort, i_frame, `cache`, hidden, permission)
-- VALUES ((SELECT MAX(id) + 1 FROM sys_menu), 0, 4, 1, '表中文字名', '', 'xxxYyy', 1, 0, 0, 0, '');

-- 子菜单权限
INSERT INTO sys_menu (pid, sub_count, `type`, title, title_letter, title_en, sort, i_frame, `cache`, hidden, permission)
VALUES (@lastId, 0, 2, '查看', '', 'view', 10, 0, 0, 0, 'xxxYyy:list');

INSERT INTO sys_menu (pid, sub_count, `type`, title, title_letter, title_en, sort, i_frame, `cache`, hidden, permission)
VALUES (@lastId, 0, 2, '新增', '', 'add', 20, 0, 0, 0, 'xxxYyy:add');

INSERT INTO sys_menu (pid, sub_count, `type`, title, title_letter, title_en, sort, i_frame, `cache`, hidden, permission)
VALUES (@lastId, 0, 2, '修改', '', 'edit', 30, 0, 0, 0, 'xxxYyy:edit');

INSERT INTO sys_menu (pid, sub_count, `type`, title, title_letter, title_en, sort, i_frame, `cache`, hidden, permission)
VALUES (@lastId, 0, 2, '删除', '', 'delete', 40, 0, 0, 0, 'xxxYyy:del');
```

**要点**:
- `pid` 必须引用已存在的父菜单 ID
- `permission` 字段格式: `xxxYyy:action`（小写驼峰 + 冒号 + 操作）
- `type = 1` 表示菜单，`type = 2` 表示权限按钮
- `sort` 控制显示顺序

---

## 3. 数据字典 SQL（必须为每个新枚举生成）

为每个新生成的枚举类添加字典 SQL：

```sql
-- 字典数据：ces_xxx_enum（对应 XxxEnum）
INSERT INTO sys_dict (name, description) VALUES ('ces_xxx_enum', '枚举描述');
SET @xxxDictId = (SELECT id FROM sys_dict WHERE name = 'ces_xxx_enum');
INSERT INTO sys_dict_detail (dict_id, label, label_letter, value, sort)
VALUES (@xxxDictId, '描述1', 'MS1', '0', 1);
INSERT INTO sys_dict_detail (dict_id, label, label_letter, value, sort)
VALUES (@xxxDictId, '描述2', 'MS2', '1', 2);
```

**要点**:
- 字典 name 格式: `ces_{枚举名小写下划线}`，如 `XxxStatusEnum` → `ces_xxx_status`
- `value` 使用枚举的 code 值（字符串形式）
- `label_letter` 使用拼音首字母缩写（如 `PTKF` = 普通客服）
- 如果枚举值较多，按 sort 顺序逐条插入
- 布尔类型（Boolean）字段不需要字典，前端直接用 `i18n.t('yes')` / `i18n.t('no')` 显示
