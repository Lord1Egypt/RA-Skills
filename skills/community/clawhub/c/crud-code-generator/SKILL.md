---
name: crud-code-generator
description: Use when generating CRUD code (create, read, update, delete, export) for database table objects across Java/Spring Boot backend and Vue2 frontend projects, based on DDL SQL. Activates when user asks to generate CRUD code, create data management endpoints, or scaffold admin pages from table definitions.
---

# crud-code-generator — 数据库表对象增删查改导出代码生成器

> 根据 DDL 建表语句，一键生成后端 Java 全栈代码（Entity/DTO/QueryParam/Mapper/Service/Controller/Converter/Enum）+ 前端 Vue2 页面 + SQL 文件

## 激活条件

当用户提到以下任一内容时激活：
- "根据模板生成增删查改代码"
- "根据建表语句生成 CRUD"
- "生成数据管理端接口"
- "生成 table object CRUD"
- 提供 DDL SQL 并要求生成对应管理代码

## 核心原则

**先确认后生成** — 在生成代码前，必须确认以下信息：
1. DDL 建表语句或 SQL 文件路径
2. 后端工程主路径
3. 是否需要生成前端代码及前端工程主路径（可选）
4. 表中文注释（用于生成 Controller 的 Swagger 注解和前端页面标题）

**生成后验证** — 后端执行 `mvn clean package`，前端提示用户是否验证 `npm run dev`。

## Step 0-A: 自动探测项目结构

在生成代码前，必须先探测后端工程目录结构，自动适配不同的项目模块名。

### 探测步骤

1. **扫描后端工程根目录下的所有 Maven 模块**:
```bash
# 找到所有包含 pom.xml 的子模块
find {backend-root} -maxdepth 2 -name "pom.xml" -not -path "*/target/*"
```

2. **识别模块用途** — 通过以下方式判断各模块的角色：
   - 查找已有 Entity 类所在目录 → 确认为 domain 模块
   - 查找已有 Service/ServiceMapper/Converter 类所在目录 → 确认为 core/service 模块
   - 查找已有 Controller 类所在目录 → 确认为 admin/controller 模块

3. **记录各模块的包路径**:
   - Entity 包路径（如 `com.infypower.fycev.domain`）
   - DTO/QueryParam 包路径（如 `com.infypower.fycev.service.dto`）
   - Enum 包路径（如 `com.infypower.enums`）
   - Service 接口包路径（如 `com.infypower.fycev.service`）
   - ServiceImpl 包路径（如 `com.infypower.fycev.service.impl`）
   - Converter 包路径（如 `com.infypower.fycev.service.converter`）
   - Mapper 包路径（如 `com.infypower.fycev.service.mapper`）
   - Mapper XML 路径（如 `ces-core/src/main/resources/mapper/`）
   - Controller 包路径（如 `com.infypower.fycev.rest`）

4. **探测前端结构**:
   - 检查 `{frontend-root}/src/components/CRUD/crud.js` 是否存在 → 确认使用 CRUD mixin
   - 检查已有 API 文件路径（如 `src/api/ces/`）→ 确认 API 文件存放目录
   - 检查已有页面路径（如 `src/pages/ces/`）→ 确认页面组件存放目录

### 探测失败处理

如果无法自动识别某个模块路径：
1. 向用户展示已识别的部分
2. 询问用户确认未识别部分的路径，给出示例选项
3. 得到用户确认后再继续生成

## Step 0-B: 确认输入信息

```
需要用户确认：
1. DDL 建表语句（直接粘贴 或 提供 SQL 文件路径）
2. 后端工程主路径（自动探测失败时需确认）
3. 是否生成前端代码？如果是，提供前端工程主路径（自动探测失败时需确认）
4. 表业务中文名称（用于 Controller 注解和页面标题，可从 DDL COMMENT 提取）
```

## Step 1: 解析 DDL

从 DDL 中提取以下信息：

| 提取项 | 来源 |
|--------|------|
| 表名 | `CREATE TABLE xxx` |
| 表注释 | `COMMENT = 'xxx'` |
| 字段列表 | 字段名、类型、注释、是否 NOT NULL、默认值 |
| 主键 | `PRIMARY KEY` 或 `id BIGINT` |
| 索引/唯一约束 | `INDEX` / `UNIQUE KEY` |
| 逻辑删除字段 | `deleted` 字段 → 自动添加 `@TableLogic` |

### 字段类型映射规则

| SQL 类型 | Java Entity 类型 | DTO 类型 | 说明 |
|----------|-----------------|---------|------|
| BIGINT / BIGINT UNSIGNED | Long | Long (@JsonSerialize ToStringSerializer) | ID 字段需要 ToStringSerializer 防止 JS 精度丢失 |
| INT / TINYINT (枚举用途) | 自定义 Enum | 自定义 Enum | 需要生成对应枚举类，见字段注释枚举值定义 |
| TINYINT (0/1 二值) | Boolean | Boolean | 如 status=0/1 映射为 Boolean，Excel 导出用 `replace = {"启用_true", "禁用_false"}` |
| VARCHAR / CHAR | String | String (@NotBlank/@Size) | 需要加校验注解 |
| TEXT | String | String | |
| DATETIME / TIMESTAMP | Date | Date | java.util.Date |
| TIME | java.sql.Time | java.sql.Time | |
| DECIMAL / NUMERIC | BigDecimal | BigDecimal | |
| JSON | String | String | 以 JSON 字符串处理 |
| DOUBLE / FLOAT | Double | Double | |

### 逻辑删除字段检测

如果 DDL 中包含 `deleted` 字段（注释含"逻辑删除"或默认值为 0），在 Entity 中添加：
```java
@ApiModelProperty("逻辑删除：0=未删除, 1=已删除")
@TableLogic
private Integer deleted;
```

### Query 字段选择

仅将以下字段加入 QueryParam：
- 业务上可能用于筛选的字段（如 operatorId、status、类型字段）
- 时间字段生成范围查询（字段名 + `Ge` + `_suffix Le`，使用 `@Query(type = Query.Type.GREATER_THAN_EQ)`）
- 字符串字段用 LIKE 查询（`@Query(type = Query.Type.INNER_LIKE)`）

### 枚举字段判断

- 如果字段类型为 `TINYINT` 且注释中包含多个枚举值描述（如 `1=xxx, 2=yyy`），需要生成对应枚举类
- 如果字段类型为 `TINYINT` 且注释仅为 `0=禁用, 1=启用` 等二值描述，映射为 `Boolean`，不生成枚举
- 如果已有相同含义的枚举（如 `CommonEffectiveStatusEnum`），直接复用不生成

## Step 2: 生成后端代码

**重要**：使用 Step 0-A 探测到的实际路径，而非硬编码路径。

按以下顺序生成文件，每个文件参考模板见 [references/java-templates.md](references/java-templates.md)：

1. **Enum 枚举类**（如果有 tinyint 等枚举字段）
2. **Entity 实体类**
3. **DTO 数据传输对象**
4. **QueryParam 查询条件对象**
5. **Mapper 接口**
6. **Mapper XML**
7. **Converter（MapStruct）**
8. **Service 接口**
9. **ServiceImpl 实现类**
10. **Controller 控制器**

### 命名转换规则

- 表名 `ces_xxx_yyy_zzz` → 类名 `XxxYyyZzz`（去掉 `ces_` 前缀，大写驼峰）
- 如果表名没有 `ces_` 前缀，直接转换为大写驼峰
- Controller 类名: `XxxYyyZzzController`
- Service 接口: `XxxYyyZzzService`
- ServiceImpl: `XxxYyyZzzServiceImpl`
- DTO: `XxxYyyZzzDTO`
- QueryParam: `XxxYyyZzzQueryParam`
- Converter: `XxxYyyZzzConverter`
- Mapper: `XxxYyyZzzMapper`
- URL 路径: `/api/ces/xxx-yyy-zzz`（中划线分隔，保持表名前缀 `ces_` 后面的部分）
- 权限前缀: `xxxYyyZzz:list` / `xxxYyyZzz:add` / `xxxYyyZzz:edit` / `xxxYyyZzz:del`

### QueryParam 必须包含枚举 import

如果 QueryParam 中引用了枚举类型，必须添加对应 import：
```java
import com.infypower.enums.XxxStatusEnum;
```

### ServiceImpl 必须包含 List import

```java
import java.util.List;
import java.util.Set;
```

## Step 3: 生成 SQL 文件

在 `sql/{year}/{month}/` 目录下创建两个 SQL 文件：

**DDL 文件**: `{日期}-ddl-{表名}.sql` — 包含完整建表语句

**DML 文件**: `{日期}-dml-{表名}.sql` — 包含菜单权限 SQL，模板见 [references/sql-templates.md](references/sql-templates.md)

## Step 4: 生成前端代码（如果用户要求）

### 4-A: 前端字典配置

如果后端生成了新的枚举类，需要在前端对应字典文件中添加字典配置。

1. **查找前端字典配置文件** — 通常在 `src/store/modules/permission.js` 或 `src/utils/dict.js` 或类似的字典配置文件中
2. **添加字典项** — 根据枚举的 code/desc 值生成对应的字典配置：

```js
// 示例：在权限/字典 store 中添加
{ name: 'ces_xxx_status', items: [
  { label: '禁用', value: '0' },
  { label: '启用', value: '1' }
]}
```

如果无法自动识别字典配置文件路径，告知用户需要手动添加，并给出具体的字典配置代码片段。

### 4-B: 页面和 API 文件

1. **API 文件** `{frontend-root}/src/api/ces/{page-name}.js`
2. **页面组件** `{frontend-root}/src/pages/ces/{page-name}/index.vue`

模板参考 [references/vue-templates.md](references/vue-templates.md)。

**页面名称转换**:
- 表名 `ces_xxx_yyy_zzz` → 页面目录 `xxx-yyy-zzz`
- API 文件 `xxx-yyy-zzz.js`

## Step 5: 验证

### 后端验证（必须）

```bash
cd {backend-root}
mvn clean package -q
```

### 前端验证（可选，提示用户）

生成前端代码后，询问用户：
> 前端代码已生成。是否需要验证前端编译？可以执行 `npm run dev` 检查是否有编译错误。

如果用户确认需要验证：
```bash
cd {frontend-root}
npm run dev
```
等待编译完成（Vite/Webpack 显示 "ready in xxx ms" 或类似成功信息），确认无 ERROR 后停止 dev server。

## Step 6: 输出报告

生成完成后，输出文件清单：

```
已生成以下文件：

后端:
  [Enum]      {实际路径}/enums/XxxStatusEnum.java（如有）
  [Entity]    {实际路径}/domain/XxxYyyZzz.java
  [DTO]       {实际路径}/dto/XxxYyyZzzDTO.java
  [QueryParam] {实际路径}/dto/XxxYyyZzzQueryParam.java
  [Mapper]    {实际路径}/mapper/XxxYyyZzzMapper.java
  [MapperXML] {实际路径}/resources/mapper/XxxYyyZzzMapper.xml
  [Converter] {实际路径}/converter/XxxYyyZzzConverter.java
  [Service]   {实际路径}/service/XxxYyyZzzService.java
  [ServiceImpl] {实际路径}/impl/XxxYyyZzzServiceImpl.java
  [Controller] {实际路径}/rest/XxxYyyZzzController.java

SQL:
  [DDL]       sql/2026/202605/ddl-日期-表名.sql
  [DML]       sql/2026/202605/dml-日期-表名.sql

前端:
  [Dict]      字典配置代码（如已自动添加 / 提示手动添加）
  [Page]      src/pages/ces/xxx-yyy-zzz/index.vue
  [API]       src/api/ces/xxx-yyy-zzz.js

验证:
  后端 mvn clean package: ✅ 通过 / ❌ 失败（原因）
  前端 npm run dev: 用户未验证 / ✅ 通过 / ❌ 失败（原因）
```

## Java 代码模板关键要点

详见 [references/java-templates.md](references/java-templates.md)，以下为核心要点：

### Entity 模板要点

- 每个字段加 `@ApiModelProperty("字段注释")`
- `id`: `@TableId(type = IdType.ASSIGN_ID)` + `@TableField(fill = FieldFill.INSERT)`
- `createTime` / `createUser`: `@TableField(fill = FieldFill.INSERT)`
- `updateTime` / `updateUser`: `@TableField(fill = FieldFill.UPDATE)`
- `deleted`: `@TableLogic`（如果 DDL 有逻辑删除字段）

### DTO 模板要点

- Long 类型字段必须加 `@JsonSerialize(using = ToStringSerializer.class)`
- 非空字段加 `@NotNull`，字符串加 `@NotBlank` / `@Size(max = N)`
- 类级别加 `@JsonInclude(JsonInclude.Include.NON_NULL)`
- 需要导出的字段加 `@Excel(name = "列名", suffix = SUFFIX)`

### QueryParam 模板要点

- **必须添加枚举类型的 import**（如果引用了枚举字段）
- 字符串筛选: `@Query(type = Query.Type.INNER_LIKE)`
- 精确匹配: `@Query`
- 范围查询: `@Query(type = Query.Type.GREATER_THAN_EQ)` 字段名加 `Ge` 后缀

### ServiceImpl 模板要点

- `// @CacheConfig(cacheNames = XxxYyyService.CACHE_KEY)` 保留注释
- **必须包含 `import java.util.List;`**
- 标准 CRUD 方法: `pageByQueryParam`, `listByQueryParam`, `countByQueryParam`, `getById`, `insert`, `updateById`, `removeByIds`

### Controller 模板要点

- 包含 `@UniformAPI`、`@Log`、`@ApiOperation`、`@PreAuthorize` 注解
- 导出方法 `download` 参考已有 Controller 实现

### Enum 模板要点

- `@EnumValue` + `@JsonValue` + `@JSONField` + `@JsonCreator` 四注解
- 检查是否可以复用已有枚举（如 `CommonEffectiveStatusEnum`）

## 前端代码模板关键要点

详见 [references/vue-templates.md](references/vue-templates.md)，以下为核心要点：

### 字段类型 → 组件映射

| 字段类型 | 搜索栏组件 | 表格列 format |
|----------|-----------|--------------|
| String | `<co-input>` | 无 |
| Long (ID关联) | `<co-input>` | `getOperatorName(val)` / `getUsername(val)` |
| Enum | `<co-select>` with `dict.xxx` | `getDictLabel('dict_key', val)` |
| Boolean | `<co-toggle toggle-indeterminate>` | `val ? i18n.t('yes') : i18n.t('no')` |
| Date | `<co-date-select range>` | `formatTime(val)` |

### 字典配置

每个枚举字段在前端需要对应的字典数据支持：
- 在 Vuex `permission.dict` 中添加 `{name: 'ces_xxx_enum', items: [...]}`
- 或在前端字典配置文件中注册
- 如果无法自动添加，提示用户手动添加

## 常见问题排查

### 编译错误: QueryParam 中枚举类找不到

```
原因: QueryParam 缺少枚举类型的 import
解决: 添加 import com.infypower.enums.XxxStatusEnum;
```

### 编译错误: ServiceImpl 中 List 找不到

```
原因: ServiceImpl 缺少 java.util.List import
解决: 添加 import java.util.List;
```

### 前端字典未定义

```
原因: 前端 Vuex permission.store 中未注册对应字典
解决: 在权限字典配置中添加枚举对应的 dict 数据，或使用 getDictLabel('dict_key', val)
```

## 生成规则检查清单

生成每个文件后，检查：

- [ ] Entity 类有 `@TableName`、`@TableId(type=ASSIGN_ID)`、`@TableField(fill=...)` 注解
- [ ] Entity 中 deleted 字段有 `@TableLogic` 注解（如果 DDL 有逻辑删除字段）
- [ ] DTO 类 Long 字段有 `@JsonSerialize(using=ToStringSerializer.class)`
- [ ] DTO 类有 `@JsonInclude(NON_NULL)` 和字段校验注解
- [ ] QueryParam 使用 `@Query` 注解，筛选字段合理
- [ ] QueryParam 包含所有枚举类型的 import
- [ ] Mapper 接口 extends `CommonMapper<Entity>`，有 `@Repository`
- [ ] Mapper XML 有正确的 namespace 声明
- [ ] Converter 使用 MapStruct `@Mapper(componentModel="spring")`
- [ ] ServiceImpl 有 `@CacheConfig` 注释保留（`//` 状态）
- [ ] ServiceImpl 包含 `import java.util.List;`
- [ ] Controller 每个方法有 `@Log`、`@ApiOperation`、`@PreAuthorize` 注解
- [ ] Controller 导出方法有 `@UniformAPI(enable = false)`
- [ ] 枚举类有 `@EnumValue`、`@JsonValue`、`@JsonCreator` 注解
- [ ] SQL 文件放在 `sql/{year}/{month}/` 目录
- [ ] 前端 API 路径与 Controller `@RequestMapping` 匹配
- [ ] 前端 columns 包含所有需要展示的字段
- [ ] 前端权限与 Controller `@PreAuthorize` 权限一致
- [ ] 前端字典配置已添加（或已提示用户手动添加）

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.1.0 | 2026-05-12 | endcy | 自动探测项目结构、自动生成前端字典 SQL、@TableLogic 自动检测、前端验证可选 |
| 1.0.0 | 2026-05-12 | endcy | 初始版本，支持基于 DDL 的全栈 CRUD 代码生成 |
