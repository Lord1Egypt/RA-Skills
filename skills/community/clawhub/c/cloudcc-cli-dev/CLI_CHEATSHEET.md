## CLI 入口速查（本仓库已定义）

`package.json` 中定义的 bin：

- `cc`：主入口（支持 `create` / `get` / `pull` / `publish` / `doc` 等）
- `cloudccCreate`：创建模板项目（内部调用 `src/project/create.js`）
- `cloudccBuild`：组件发布/构建相关（内部调用 `src/plugin/publish.js`）

---

## 常用 CLI 命令速查（按开发流程分组）

### 项目与文档

```bash
# 版本
cc -v

# 创建模板项目
cc create project <projectName>

# 输出项目文档（纯 CLI 文档）
cc doc project overview
cc doc project key-guide
```

### 对象与字段

```bash
# 创建自定义对象
cc create object <projectPath> <label>

# 查询对象列表（输出 JSON）
# type 可选：standard / custom / both（默认：both）
cc get object <projectPath> [type]

# 查询对象字段（输出 JSON）
cc get fields <projectPath> <objprefix>

# 创建字段（字段类型决定参数个数）
cc create fields <projectPath> <fieldType> <objid> <nameLabel> [ptext|lookupObj]
```

### 菜单与应用

```bash
# 创建菜单（标签页）
cc create menu <type> <projectPath> <resourceId> <tabName> [tabStyle] [mobileimg] [cloudccservicetab]

# 创建应用
cc create application <projectPath> <appName> <appCode> [menuIds]
```

### 自定义类（classes）

```bash
cc create classes <ClassName>
cc pull classes <ClassName>
cc publish classes <ClassName>
```

### 定时类（schedule）

```bash
cc create schedule <ScheduleName>
cc pull schedule <ScheduleName>
cc publish schedule <ScheduleName>
```

### 触发器（triggers）

```bash
# 创建：参数是一个 JSON（需 encodeURI 后作为单个参数传入）
cc create triggers <encodedJson>

# 拉取/发布：namePath 形如 objectName/triggerName
cc pull triggers <namePath>
cc publish triggers <namePath>
```

### 自定义组件（plugin / plugins）

```bash
# 创建（生成到 plugins/<pluginName>/）
cc create plugin <pluginName>

# 发布（编译并上传）
cc publish plugin <pluginName>
```

