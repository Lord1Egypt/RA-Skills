# CRUD Code Generator — 数据库表对象增删查改导出代码生成器

根据 DDL 建表语句，一键生成后端 Java 全栈代码（Entity/DTO/QueryParam/Mapper/Service/Controller/Converter/Enum）+ 前端 Vue2 页面 + SQL 文件。

## 功能

- **自动探测项目结构**：自动扫描后端 Maven 模块，识别 Entity/Service/Controller 等各模块路径，适配不同项目结构
- **全栈代码生成**：从 DDL 到后端 10 层代码 + 前端页面 + API + SQL 文件一键生成
- **枚举自动识别**：从 DDL 字段注释识别枚举值，生成对应枚举类和前端字典 SQL
- **逻辑删除检测**：自动识别 `deleted` 字段并添加 `@TableLogic` 注解
- **字典 SQL 生成**：为每个枚举自动生成 `sys_dict` / `sys_dict_detail` 插入 SQL
- **导出接口生成**：生成 EasyPOI Excel 导出功能，支持数据量校验与批量导出
- **生成后验证**：后端 `mvn clean package` 编译验证，前端可选 `npm run dev` 验证

## 依赖

### 后端
- Java 8+ / Spring Boot 2.x
- MyBatis-Plus（`@TableId`, `@TableField`, `@TableName`）
- MapStruct（对象转换）
- EasyPOI（Excel 导出）
- coadmin 框架基础类（`BaseEntity`, `BaseDto`, `CommonMapper`, `QueryHelpMybatisPlus` 等）

### 前端
- Vue 2 + Quasar UI
- 自定义 CRUD mixin 框架（`@crud/crud`, `presenter()`, `header()`, `form()`, `crud()`）
- Vuex permission store 字典系统（`dict.xxx`, `getDictLabel`）

## 使用

当需要根据数据库表结构生成管理端 CRUD 代码时，激活此 skill：
- "根据模板生成增删查改代码"
- "根据建表语句生成 CRUD"
- "生成数据管理端接口"
- "生成 table object CRUD"

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.1.0 | 2026-05-12 | endcy | 自动探测项目结构、自动生成前端字典 SQL、@TableLogic 自动检测、前端验证可选 |
| 1.0.0 | 2026-05-12 | endcy | 初始版本，支持基于 DDL 的全栈 CRUD 代码生成 |
