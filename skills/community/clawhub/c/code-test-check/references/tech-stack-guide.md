# 源码搜索指引（通用）

本文件指导如何在**用户指定的后端与前端源码**中精准定位功能实现。本技能不预设具体项目，以下路径均以第 0 步确认的源码根目录为准（下文用 `<后端根>`、`<前端根>` 代指）。

## 一、工具使用策略

### 1. SearchCodebase（语义搜索，首选定位工具）
- 用于"按功能意图找代码"，不依赖精确关键词
- **必须指定 target_directories**，分别搜索后端和前端（用第 0 步确认的根目录）：
  - 后端：`target_directories: ["<后端根>"]`
  - 前端：`target_directories: ["<前端根>"]`
- 查询要写完整自然语言问题，一次只问一个：
  - ✅ "XX审批通过的接口实现在哪里"
  - ❌ "审批"（太模糊）
- 忽略依赖与构建产物目录：`vendor`、`node_modules`、`runtime`、`dist`、`target`、`build` 等

### 2. Grep（精确文本匹配，确认工具）
- 用于按已知标识符（方法名、路由、字段、中文文案）精确定位
- 常用模式：
  - 路由路径：`Grep pattern="xx/approve" path="<后端根>"`
  - 方法名：`Grep pattern="function approve"` 或 `def approve` / `approve(`（按语言调整）
  - 中文文案（前端按钮/提示）：`Grep pattern="审批通过"`
  - 字段名：`Grep pattern="approve_status"`
- 善用 glob 过滤：按语言/框架的文件后缀过滤，如 `*.php`、`*.java`、`*.py`、`*.{vue,js,ts}`、`*.{tsx,jsx}`

### 3. Glob（按文件名查找）
- 定位控制器/模型/页面/接口定义文件（文件名按实际命名约定调整）：
  - `Glob pattern="**/*Controller*.java" path="<后端根>"`
  - `Glob pattern="**/views/**" path="<前端根>/src"`

### 4. Read（阅读代码验证逻辑）
- 命中后必须 Read 读取关键行段，确认实现逻辑而非仅关键词命中
- 优先只读必要行范围（offset + limit），避免读取超大文件

## 二、项目结构识别（第 0 步探测参考）

若用户未说明目录结构，用 `Glob`/`LS` 浏览根目录，按下表识别框架特征目录，推断技术栈与分层。

### 常见后端框架目录锚点（参考，不穷尽）

| 框架/语言 | 路由 | 控制器/处理 | 模型/实体 | 常量/枚举 |
|-----------|------|------------|----------|----------|
| ThinkPHP (PHP) | `app/*/route/` | `app/*/controllers/` | `app/common/models/`、`app/common/` | `app/common/constant/` |
| Laravel (PHP) | `routes/` | `app/Http/Controllers/` | `app/Models/` | `app/Enums/`、`config/` |
| Spring Boot (Java) | `@RequestMapping` 注解 | `@RestController` 类（`controller/`） | `entity/`、`model/`、`mapper/` | `enums/`、`constant/` |
| Django (Python) | `urls.py` | `views.py` | `models.py` | `constants.py` |
| Express/Koa (Node) | `routes/`、`app.js` | `controllers/`、`handlers/` | `models/` | `constants/`、`config/` |
| Gin (Go) | `router.go`、`*.go` 路由注册 | `handler/`、`controller/` | `model/`、`entity/` | `const/`、`constant/` |

### 常见前端框架目录锚点（参考，不穷尽）

| 框架 | 接口定义 | 页面视图 | 组件 | 路由 |
|------|---------|---------|------|------|
| Vue (Element Plus/Ant 等) | `src/api/` | `src/views/` | `src/components/` | `src/router/` |
| React | `src/api/`、`src/services/` | `src/pages/`、`src/views/` | `src/components/` | `src/router/`、`App.tsx` |
| 小程序(Taro/原生) | `src/api/`、`service/` | `src/pages/`、`pages/` | `src/components/`、`components/` | `app.config.*` |

> ⚠️ 以上仅为探测参考，实际以用户项目为准。探测完成后整理为「目录锚点表」并让用户确认。

## 三、后端验证要点（通用）

- **接口存在性**：先查路由是否定义了该路径（路由文件或路由注解）
- **参数校验**：查控制器/处理方法中的 validate / 参数获取逻辑
- **业务逻辑**：查处理方法体 + 调用的 Model/Service 方法
- **状态流转**：查常量/枚举定义 + 更新状态的代码
- **权限控制**：查中间件、拦截器、权限校验注解/装饰器

**后端搜索示例（路径用第 0 步确认的实际根目录替换）：**
```
# 1. 找路由（按框架调整，路由文件或注解）
Grep pattern="xxReport/approve" path="<后端根>" -n

# 2. 找处理方法（按语言调整函数定义语法）
Grep pattern="function approve|def approve|approve\(" glob="*.{php,py,java,go}" path="<后端根>"

# 3. 语义搜索定位实现
SearchCodebase information_request="XX审批通过的完整业务逻辑实现"
           target_directories=["<后端根>"]
```

## 四、前端验证要点（通用）

- **接口调用**：查前端接口定义模块中是否定义了对应接口方法
- **UI 元素**：查视图文件中的按钮、表单、列表（按中文文案或组件属性搜索）
- **交互逻辑**：查视图文件中的事件绑定（如 `@click`、`@change`、`onClick`）、方法定义
- **状态展示**：查条件渲染（如 `v-if`、`v-show`、`&&`、三元）、状态映射
- **字段绑定**：查表单绑定（如 `v-model`、`value`）、表格列字段绑定

**前端搜索示例（路径用第 0 步确认的实际根目录替换）：**
```
# 1. 找接口定义
Grep pattern="approve" glob="*.{js,ts}" path="<前端根>/src"

# 2. 找页面（按中文文案）
Grep pattern="审批通过" glob="*.{vue,jsx,tsx}" path="<前端根>/src"

# 3. 语义搜索
SearchCodebase information_request="XX审批页面的实现"
           target_directories=["<前端根>"]
```

## 五、常见误判与规避

| 误判类型 | 表现 | 规避方法 |
|---------|------|---------|
| 关键词假阳性 | 文案命中但实为注释/死代码 | Read 读取上下文，确认代码在执行路径上 |
| 空实现 | 方法存在但只有空体或 TODO | Read 读取方法体，确认有实际逻辑 |
| 注释代码 | 被注释掉的实现 | 检查 `//`、`/* */`、`<!-- -->`、`#` 注释 |
| 旧版残留 | 历史代码未被清理 | 结合路由/调用链确认是否在用 |
| 动态调用 | 方法名拼接、反射调用 | 用 Grep 搜索调用处，追溯动态方法名 |

## 六、无法静态判定的情况

以下情况需在报告中明确标注为"静态分析无法确认"，建议结合运行时测试：
- 基于数据库配置/开关的动态行为
- 权限/角色控制的可见性
- 异步队列、定时任务的执行
- 第三方服务调用的实际响应
