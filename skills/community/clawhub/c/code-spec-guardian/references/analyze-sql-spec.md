# SQL/数据库规范分析指引 | SQL Spec Analyzer

> 指导 AI 分析项目 SQL/数据库规范，提取 `sql-spec.md` 规范。

## 分析流程

1. **先读 `references/sql-spec.md`** 了解条目编号
2. **读 `project_context.json`** 获取语言和框架信息；用 `exec` 搜索 ORM 模型文件和 migration 文件（如 `Get-ChildItem -Path . -Recurse -Include *.prisma,*.sql` 或 `find . -name 'migration*'`），用 `read` 读关键文件
3. **读关键文件**：ORM 配置文件、migration 文件、model 定义文件
4. **写入 `.code-spec/sql-spec.md`**

## 各条目分析要点

### 命名规范 [SQL-01 ~ SQL-04]

#### [SQL-01] 表命名
- 读 migration 文件中的 CREATE TABLE 语句
- 复数/单数、snake_case、前缀/后缀约定
- 关联表命名（如 user_role）

#### [SQL-02] 字段命名
- 从 ORM model 定义提取字段名
- snake_case 还是 camelCase
- 是否使用保留字作为字段名

#### [SQL-03] 索引命名
- 主键命名（pk_xxx）
- 唯一索引（uk_xxx）、普通索引（idx_xxx）
- 外键索引命名

#### [SQL-04] 外键命名
- 外键约束名格式（fk_xxx_xxx）

### 字段规范 [SQL-05 ~ SQL-08]

#### [SQL-05] 主键设计
- 类型：自增 INT / BIGINT / UUID / cuid / Snowflake
- 自增主键起步值
- 是否使用复合主键

#### [SQL-06] 时间字段
- 命名：created_at vs createTime
- 类型：datetime / timestamp / bigint
- 是否有自动更新（updated_at / ON UPDATE CURRENT_TIMESTAMP）

#### [SQL-07] 软删除
- 字段名：deleted_at / is_deleted / status
- 类型：datetime vs tinyint
- ORM 查询中软删除过滤方式

#### [SQL-08] 字段类型选择
- VARCHAR 长度偏好（255/191/64 等模式）
- 金额用 DECIMAL 还是 INT（分）
- JSON/Text 字段使用
- ENUM vs SMALLINT 状态字段

### 索引与关联 [SQL-09 ~ SQL-11]

#### [SQL-09] 索引创建原则
- 高频查询字段索引
- 外键是否自动加索引
- 是否使用了全文索引

#### [SQL-10] 联合索引
- 是否有联合索引
- 联合索引的字段顺序约定

#### [SQL-11] 模型关联
- ORM 关联定义：belongsTo / hasMany / belongsToMany
- 关联命名约定
- 中间表命名

### ORM 规范 [SQL-12 ~ SQL-15]

#### [SQL-12] ORM 框架
- 从 `project_context.json` → `frameworks` 检查是否有 Prisma/TypeORM/Sequelize/GORM/Django ORM 等
- 用 `exec` 搜索 ORM 配置文件（如 `prisma/schema.prisma`、`ormconfig.json`、`datasource` 配置）
- 用 `read` 读 ORM 配置文件确认版本
- TypeORM/Prisma/Sequelize/Drizzle/Mongoose/Django ORM 版本

#### [SQL-13] Model 定义风格
- Prisma schema 组织方式（单文件还是多文件）
- Entity class 还是 schema-first
- Model 文件组织方式

#### [SQL-14] 查询写法
- Query Builder vs Raw SQL 使用比例
- WHERE 条件写法约定
- 排序/分页写法

#### [SQL-15] 连接池配置
- 数据库连接配置中的 pool 参数
- 最大/最小连接数

### 迁移规范 [SQL-16 ~ SQL-17]

#### [SQL-16] 迁移脚本命名
- migration 文件命名格式
- 时间戳 vs 序号

#### [SQL-17] 迁移脚本编写
- 是否必须同时有 up 和 down
- 模块化迁移还是一个文件
- seed 数据管理

### 特殊场景 [SQL-18 ~ SQL-19]

#### [SQL-18] 树形结构
- parent_id 自关联 / ltree / nested set
- 查询方法封装

#### [SQL-19] 读写分离
- 是否有多数据源配置
- 读写路由逻辑
