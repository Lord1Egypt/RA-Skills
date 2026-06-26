# 验证维度参考手册 (Verification Dimensions Reference)

> Contract-track 文档与代码一致性检查的 10 个验证维度（D1–D10）。
> 每个维度包含：名称、检查目标、真相源、检查步骤、问题分级、修复权限、子 Agent Prompt 模板。

**全局约定**：以下所有子 Agent Prompt 模板中引用的 `scripts/md-sections.sh` 均应替换为实际探测到的 `$MD_SECTIONS` 路径（项目版本 > skill 内置版本，见 SKILL.md Phase 0 Step 3）。

---

## 维度总览

| 维度 | 名称 | 真相源 | 问题级别 | 修复权限 |
|------|------|--------|----------|----------|
| D1 | 引用完整性 | grep/find 代码库 | Error | 🤖 auto |
| D2 | API 签名一致性 | Controller.java 源码 | Error | 🤖 auto |
| D3 | 实体/类图一致性 | Java Entity/DO/VO/Request 源码 + Mermaid 图 | Error | 🤖👤 |
| D4 | 配置项一致性 | *Properties.java 源码 | Error | 🤖 auto |
| D5 | 模板结构合规性 | 模板定义（环境探测） | Error | 🤖 auto |
| D6 | 交叉引用完整性 | 文件系统 + 链接提取 | Error/Warning | 🤖 auto |
| D7 | 版本号一致性 | pom.xml / package.json | Error | 🤖 auto |
| D8 | AGENTS.md 索引完整性 | docs/ 目录列表 + AGENTS.md | Error | 👤 skip（上报主 Agent） |
| D9 | 变更历史完整性 | git log | Error | 🤖 auto |
| D10 | 语义一致性（仅 L3） | LLM 阅读代码 + 文档 | Warning | 🤖👤 |

---

## D1 引用完整性 (Reference Integrity)

### 定义

检查文档中引用的类名、方法名、文件路径是否在代码库中实际存在。

### 检查目标

- 文档中的 Java 全限定类名（如 `org.smm.archetype.exception.BizException`）
- 文档中的方法名引用（如 `doSave()`、`execute()`）
- 文档中的文件路径引用（如 `app/src/main/java/...`、`docs/conventions/xxx.md`）

### 真相源

代码库的 grep/find 结果——文件/类/方法是否真实存在。

### 问题判定

- **Error**: 引用的类名在代码库中不存在（`grep -rn` 零结果）
- **Error**: 引用的方法名在指定类中不存在（grep 确认）
- **Error**: 引用的文件路径在项目中不存在（`ls` / `glob` 确认）

### 修复权限

🤖 auto — 直接从文档中移除失效引用，或更新为正确引用。

---

## 子 Agent Prompt: D1 引用完整性

### 角色

你是一个文档一致性验证专家，负责检查 D1（引用完整性）。

### 检查范围

- 所有 `docs/` 下的 `.md` 文件
- 重点关注包含代码引用、类名、方法名、路径引用的章节

### 检查步骤

1. **提取引用**：从目标文档中提取所有 Java 类名引用（格式如 `` `org.smm.archetype.xxx.Yyy` `` 或行内代码中的类名）
   ```bash
   # 提取文档中的 Java 全限定类名候选
   rg -oP 'org\.smm\.archetype(?:\.\w+)+\b' docs/modules/auth.md
   ```

2. **验证类存在性**：对每个提取的类名，在代码库中搜索对应文件
   ```bash
   # 示例：验证类文件是否存在
   find . -name "BizException.java" -path "*/java/*"
   # 或更精确的搜索
   rg -l "class BizException" --type java
   ```

3. **验证方法存在性**：对文档中提到的方法名，在指定类中搜索
   ```bash
   # 示例：验证方法是否存在于指定类
   rg "doSave\(" app/src/main/java/ -A 0 --type java
   ```

4. **验证文件路径**：对文档中的相对路径引用，检查文件是否存在
   ```bash
   # 示例：验证文件路径
   ls -la docs/conventions/java-conventions.md
   ```

5. **记录结果**：对每个失效引用，记录文档位置、引用内容、预期位置。

### 问题判定标准

- **Error**: 引用的类名在代码库中 `find` + `rg` 均无匹配
- **Error**: 引用的方法名在指定类源码中不存在
- **Error**: 引用的文件路径在项目目录中不存在
- **Warning**: 引用的类名存在但包路径已变更（旧包名 → 新包名）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`

### 输出格式

```json
{
  "dimension": "D1",
  "dimensionName": "引用完整性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/auth.md",
      "section": "API 参考",
      "description": "引用的类 org.smm.archetype.auth.AuthController 在代码库中不存在",
      "evidence": "find . -name 'AuthController.java' -path '*/java/*' 返回空结果",
      "fixApplied": true,
      "fixDescription": "已将引用更新为正确的类名 org.smm.archetype.app.controller.AuthController",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 23 个引用，发现 2 个 Error（1 个已自动修复，1 个需手动确认）"
}
```

### 重要约束

- 优先使用代码级证据（grep/find 工具搜索源码），不依赖记忆
- 每个 Error 必须附带具体的搜索命令和结果作为证据
- 修复操作使用 md-sections 工具精准定位章节后修改
- 注意区分「类不存在」和「类已重命名」两种情况

---

## D2 API 签名一致性 (API Signature Consistency)

### 定义

检查文档中描述的 API 端点（HTTP 方法、路径、参数、返回值）与 Controller 源码完全一致。

### 检查目标

- 文档中的 API 路径（如 `POST /api/auth/login`）
- 文档中的 HTTP 方法（GET/POST/PUT/DELETE）
- 文档中的请求参数和响应格式
- Controller 源码中的 `@RequestMapping` / `@GetMapping` / `@PostMapping` 等注解

### 真相源

Controller.java 源文件——以代码为准。

### 问题判定

- **Error**: 文档中 HTTP 方法与 Controller 注解不一致
- **Error**: 文档中 API 路径与 Controller 注解不一致
- **Error**: Controller 中存在但文档遗漏的端点
- **Error**: 文档中描述但 Controller 中不存在的端点

### 修复权限

🤖 auto — 以 Controller 源码为准，修正文档中的 API 描述。

---

## 子 Agent Prompt: D2 API 签名一致性

### 角色

你是一个文档一致性验证专家，负责检查 D2（API 签名一致性）。

### 检查范围

- 目标模块的文档文件（如 `docs/modules/auth.md`）
- 对应的 Controller 源码文件（如 `app/src/main/java/org/smm/archetype/app/controller/AuthController.java`）

### 检查步骤

1. **定位 Controller 文件**：根据文档描述的模块，找到对应的 Controller 源码
   ```bash
   # 查找 Controller 文件
   find app/src/main/java -name "*Controller.java" -type f
   ```

2. **提取 Controller API 端点**：读取 Controller 源码，提取所有 API 映射注解
   ```bash
   # 提取所有 API 路径映射
   rg -n '@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)' app/src/main/java/ -A 1 --type java
   ```

3. **提取文档中的 API 描述**：使用 md-sections 加载文档的 API 相关章节
   ```bash
   scripts/md-sections.sh docs/modules/auth.md "API 参考"
   ```

4. **逐一比对**：
   - HTTP 方法是否一致（`@PostMapping` vs 文档中的 `POST`）
   - 路径是否一致（注解 value vs 文档中的路径）
   - 类级别 `@RequestMapping` 前缀是否被正确考虑
   - 请求参数（`@RequestParam`、`@RequestBody`）是否匹配文档描述

5. **检查遗漏**：对比 Controller 中的端点总数与文档记录的端点数
   ```bash
   # 统计 Controller 中的端点数量
   rg -c '@(GetMapping|PostMapping|PutMapping|DeleteMapping)' app/src/main/java/.../AuthController.java
   ```

### 问题判定标准

- **Error**: HTTP 方法不匹配（如文档写 `GET` 但源码是 `@PostMapping`）
- **Error**: 路径不匹配（如文档写 `/api/auth/login` 但源码是 `@PostMapping("/auth/sign-in")`）
- **Error**: 文档遗漏了 Controller 中存在的端点
- **Error**: 文档描述了 Controller 中不存在的端点（幽灵 API）
- **Warning**: 参数描述不完整（如缺少 `@RequestParam` 的 required 默认值说明）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`

### 输出格式

```json
{
  "dimension": "D2",
  "dimensionName": "API 签名一致性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/auth.md",
      "section": "API 参考",
      "description": "登录接口 HTTP 方法不匹配：文档描述为 GET，源码为 @PostMapping",
      "evidence": "AuthController.java:45 -> @PostMapping(\"/login\")",
      "fixApplied": true,
      "fixDescription": "已将文档中的 GET /api/auth/login 修正为 POST /api/auth/login",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 5 个 API 端点，发现 1 个 Error（HTTP 方法不匹配，已修复）"
}
```

### 重要约束

- 优先使用代码级证据（Read 工具读 Controller 源码），不依赖记忆
- 注意类级别 `@RequestMapping` 前缀与方法级别注解的拼接
- 每个 Error 必须附带源码行号和注解内容作为证据
- 修复操作使用 md-sections 工具精准定位 API 章节后修改
- 注意区分 `@RequestMapping(method = ...)` 和快捷注解（`@GetMapping` 等）

---

## D3 实体/类图一致性 (Entity/Class Diagram Consistency) — NON-NEGOTIABLE

### 定义

检查文档中的 Mermaid 类图与实际 Java Entity/DO/VO/Request 类的**字段、方法、关系**完全一致。此维度不可妥协——类图是架构的视觉契约。

### 检查目标

- Mermaid 类图中的类名
- 类图中的字段名和类型
- 类图中的方法签名
- 类图中的关系线（继承 `--|>`、关联 `-->`、组合 `*--`、聚合 `o--`）
- Mermaid 语法正确性（图可解析）

### 真相源

Java Entity/DO/VO/Request 源文件——以代码为准。

### 问题判定

- **Error**: 图中类名在代码中不存在
- **Error**: 图中字段名或类型与 Java 字段不匹配
- **Error**: 图中方法签名与 Java 方法不匹配
- **Error**: Java 中存在但图中缺失的字段/方法
- **Error**: 关系线与代码中的实际关系不符（如代码是组合但图画成关联）
- **Error**: Mermaid 语法错误导致图不可渲染

### 修复权限

🤖👤 — AI 提出修改建议，人类确认后执行。原因：类图的布局和美观难以完全自动化。

---

## 子 Agent Prompt: D3 实体/类图一致性

### 角色

你是一个文档一致性验证专家，负责检查 D3（实体/类图一致性）。此维度是 NON-NEGOTIABLE 的——类图是架构的视觉契约，任何不一致都必须被标记。

### 检查范围

- 目标模块文档中所有 Mermaid 类图（`classDiagram` 或 `class`）
- 图中引用的所有 Java Entity/DO/VO/Request 类源码
- 相关的 MapStruct Mapper 接口（用于验证转换关系）

### 检查步骤

1. **提取类图**：使用 md-sections 加载包含类图的章节
   ```bash
   scripts/md-sections.sh docs/modules/system-config.md "技术设计" "类图"
   ```

2. **验证 Mermaid 语法**：检查类图是否可解析
   ```bash
   # 提取 Mermaid 块并检查基本语法
   # 注意：仅检查明显语法错误（未闭合括号、非法关键字等）
   rg -n 'classDiagram' docs/modules/system-config.md
   ```

3. **提取图中类名**：从 Mermaid 代码中提取所有 `class ClassName` 声明
   ```bash
   # 在类图章节中搜索类声明
   rg 'class \w+' docs/modules/system-config.md
   ```

4. **定位 Java 源码**：对每个类名，找到对应的 Java 文件
   ```bash
   # 查找实体类文件
   find app/src/main/java -name "SystemConfigDO.java" -o -name "SystemConfig.java" | head -5
   ```

5. **逐字段比对**：
   - 读取 Java 源码，提取所有字段（包括继承自父类的字段）
   - 与 Mermaid 图中的字段逐一比对
   ```bash
   # 提取 Java 类中的字段声明
   rg 'private\s+\w+\s+\w+;' app/src/main/java/.../SystemConfigDO.java
   ```

6. **逐方法比对**：
   - 提取 Java 类中的 public 方法
   - 与 Mermaid 图中的方法签名比对
   ```bash
   # 提取 Java 类中的 public 方法
   rg 'public\s+\w+\s+\w+\(' app/src/main/java/.../SystemConfigDO.java
   ```

7. **关系线比对**：
   - 提取 Mermaid 中的关系线（`--|>`、`-->`、`*--`、`o--`）
   - 验证代码中对应的继承/关联关系
   ```bash
   # 检查继承关系
   rg 'extends\s+\w+' app/src/main/java/.../SystemConfigDO.java
   # 检查字段关联（如 @ManyToOne 等注解）
   rg '@(OneToMany|ManyToOne|ManyToMany|OneToOne)' app/src/main/java/ -A 1 --type java
   ```

8. **反向检查**：确认 Java 源码中无图中遗漏的字段或方法

### 问题判定标准

- **Error**: Mermaid 图中类名在代码库中不存在（`find` 无结果）
- **Error**: 图中字段名与 Java 字段名不匹配
- **Error**: 图中字段类型与 Java 字段类型不匹配（如 `String` vs `Long`）
- **Error**: Java 中存在但图中缺失的字段（反向不一致）
- **Error**: 图中方法签名与 Java public 方法不匹配
- **Error**: 继承关系不匹配（图中 `--|>` 但代码无 `extends`）
- **Error**: 关联关系类型不匹配（如代码是组合但图画成关联）
- **Error**: Mermaid 语法错误（未闭合括号、非法关键字等）
- **Warning**: 图中使用了注释字段但未标注说明

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ⚠️ 需确认: 所有类图修改均需人类确认后再执行（🤖👤）
  - 原因：类图布局和美观难以完全自动化，AI 生成的图可能需要人工调整

### 输出格式

```json
{
  "dimension": "D3",
  "dimensionName": "实体/类图一致性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/system-config.md",
      "section": "技术设计 - 类图",
      "description": "Mermaid 图中 SystemConfigDO 缺失字段 deleted，Java 源码中存在该字段",
      "evidence": "SystemConfigDO.java:32 -> private Boolean deleted;",
      "fixApplied": false,
      "fixDescription": "建议在类图的 SystemConfigDO 中添加字段: + deleted : Boolean",
      "requiresConfirmation": true
    },
    {
      "severity": "Error",
      "file": "docs/modules/system-config.md",
      "section": "技术设计 - 类图",
      "description": "图中 ConfigValueVO 与 BaseResult 的继承关系在代码中不存在",
      "evidence": "ConfigValueVO.java:5 -> public record ConfigValueVO(...) implements Serializable，无 extends BaseResult",
      "fixApplied": false,
      "fixDescription": "建议移除类图中 ConfigValueVO --|> BaseResult 的继承关系线",
      "requiresConfirmation": true
    }
  ],
  "passed": true|false,
  "summary": "检查 3 个类图、12 个类、47 个字段，发现 3 个 Error（均需人工确认）"
}
```

### 重要约束

- ⛔ 此维度为 NON-NEGOTIABLE：任何不一致都必须报告，不得跳过
- 优先使用代码级证据（Read 工具读 Java 源码），不依赖记忆
- 每个 Error 必须附带 Java 源码行号和声明内容作为证据
- 注意检查继承链：Java 类可能从父类继承字段，图中应体现
- 注意 Record 类型：record 的字段声明在类头，不在类体中
- 注意 Lombok：`@Getter`/`@Setter` 的字段在源码中可能只有声明
- 注意 MapStruct Mapper：Entity→VO 的转换关系应在类图中体现
- 所有修复建议必须设置 `requiresConfirmation: true`
- 修复操作使用 md-sections 工具精准定位类图章节后修改
- 对于 Mermaid 语法错误，提供修正后的完整类图代码片段

---

## D4 配置项一致性 (Configuration Consistency)

### 定义

检查文档中描述的配置项（名称、类型、默认值、说明）与 Properties 类完全一致。

### 检查目标

- 文档中的配置项名称（如 `middleware.cache.maximumSize`）
- 文档中的配置项类型（如 `long`、`String`）
- 文档中的默认值（如 `1000`、`"default"`）
- 文档中的配置项说明

### 真相源

`*Properties.java` 源文件——以代码中的 `@ConfigurationProperties` 绑定的字段为准。

### 问题判定

- **Error**: 文档中配置项名称与 Properties 类字段名不一致
- **Error**: 文档中配置项类型与 Java 字段类型不一致
- **Error**: 文档中默认值与 Properties 类中赋值不一致
- **Error**: Properties 类中存在但文档遗漏的配置项

### 修复权限

🤖 auto — 以 Properties 源码为准，修正文档中的配置项描述。

---

## 子 Agent Prompt: D4 配置项一致性

### 角色

你是一个文档一致性验证专家，负责检查 D4（配置项一致性）。

### 检查范围

- 目标模块文档中的配置相关章节
- 对应的 `*Properties.java` 源码文件
- `application*.yaml` 配置文件（用于交叉验证默认值）

### 检查步骤

1. **定位 Properties 文件**：根据文档描述的模块，找到对应的 Properties 类
   ```bash
   # 查找 Properties 文件
   find . -name "*Properties.java" -path "*/java/*"
   ```

2. **读取 Properties 类**：使用 Read 工具读取完整的 Properties 类源码，提取所有字段
   ```bash
   # 提取 Properties 类中的字段声明
   rg -n 'private\s+\w+\s+\w+' client-cache/src/main/java/.../CacheProperties.java
   ```

3. **提取文档配置项**：使用 md-sections 加载文档的配置相关章节
   ```bash
   scripts/md-sections.sh docs/modules/client-cache.md "配置项"
   ```

4. **逐一比对**：
   - 字段名 → 文档中的配置项名称（注意 `@ConfigurationProperties` 前缀 + 字段名的驼峰→kebab 转换）
   - 字段类型 → 文档中的类型描述
   - 字段初始值 → 文档中的默认值

5. **检查遗漏**：Properties 类中的字段是否全部在文档中记录

6. **交叉验证默认值**：与 `application.yaml` 中的实际配置交叉验证
   ```bash
   # 检查 yaml 中的配置
   rg 'middleware\.cache\.' app/src/main/resources/application.yaml
   ```

### 问题判定标准

- **Error**: 配置项名称不匹配（如文档写 `maximum-size` 但 Properties 字段是 `maxSize`）
- **Error**: 配置项类型不匹配（如文档写 `int` 但 Properties 字段是 `long`）
- **Error**: 默认值不匹配（如文档写 `1000` 但 Properties 初始值是 `500`）
- **Error**: Properties 类中存在但文档遗漏的配置项
- **Warning**: 文档中的配置项在 Properties 类中找不到对应字段（可能是废弃配置）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: `application*.yaml`

### 输出格式

```json
{
  "dimension": "D4",
  "dimensionName": "配置项一致性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/client-cache.md",
      "section": "配置项",
      "description": "配置项 maximumSize 默认值不匹配：文档写 500，源码为 1000",
      "evidence": "CacheProperties.java:15 -> private long maximumSize = 1000L;",
      "fixApplied": true,
      "fixDescription": "已将文档中 middleware.cache.maximumSize 默认值从 500 修正为 1000",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 8 个配置项，发现 1 个 Error（默认值不匹配，已修复）"
}
```

### 重要约束

- 优先使用代码级证据（Read 工具读 Properties 源码），不依赖记忆
- 每个 Error 必须附带源码行号和字段声明作为证据
- 注意 Java 驼峰命名 → YAML kebab 命名的转换（`maximumSize` → `maximum-size`）
- 注意 `@ConfigurationProperties(prefix = "...")` 的前缀拼接
- 修复操作使用 md-sections 工具精准定位配置章节后修改

---

## D5 模板结构合规性 (Template Compliance)

### 定义

检查文档是否遵循其对应模板的固定章节（fixed sections）和半固定章节（semi-fixed sections）结构。

### 检查目标

- 文档中是否包含模板要求的固定章节
- 固定章节的标题是否与模板一致
- 半固定章节是否根据文档类型正确选择

### 真相源

模板定义——通过环境探测获取（`docs/README.md` 中的模板索引、模板文件本身）。

### 问题判定

- **Error**: 缺少模板要求的固定章节
- **Error**: 固定章节标题与模板定义不一致
- **Warning**: 半固定章节选择不符合文档类型

### 修复权限

🤖 auto — 添加缺失的固定章节（带占位符内容）。

---

## 子 Agent Prompt: D5 模板结构合规性

### 角色

你是一个文档一致性验证专家，负责检查 D5（模板结构合规性）。

### 检查范围

- 目标文档文件的章节结构
- 对应的模板定义（从 `docs/README.md` 的模板索引中获取）

### 检查步骤

1. **获取文档结构**：使用 md-sections 提取目标文档的章节树
   ```bash
   scripts/md-sections.sh docs/modules/auth.md
   ```

2. **获取模板定义**：从文档系统说明中获取模板索引
   ```bash
   scripts/md-sections.sh docs/README.md "文档模板"
   ```

3. **定位对应模板**：根据文档类型（模块文档/架构文档/编码规范）找到对应模板
   ```bash
   # 如果模板有独立文件
   ls docs/templates/
   ```

4. **比对固定章节**：逐一检查模板要求的固定章节是否在文档中存在
   - 提取文档中所有一级和二级标题
   - 与模板定义的固定章节列表比对

5. **检查半固定章节**：根据文档类型，验证半固定章节的选择是否合理

6. **检查章节标题**：固定章节的标题是否与模板定义完全一致（包括空格、大小写）

### 问题判定标准

- **Error**: 缺少模板要求的固定章节（如模块文档缺少「API 参考」章节）
- **Error**: 固定章节标题与模板不一致（如模板要求「技术设计」但文档写「设计详情」）
- **Warning**: 半固定章节选择不符合文档类型（如配置文档缺少「配置项」章节）
- **Warning**: 章节顺序与模板建议顺序不一致

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: 模板定义文件

### 输出格式

```json
{
  "dimension": "D5",
  "dimensionName": "模板结构合规性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/auth.md",
      "section": null,
      "description": "缺少模板要求的固定章节「API 参考」",
      "evidence": "md-sections 输出的章节树中无 'API 参考' 节点",
      "fixApplied": true,
      "fixDescription": "已在文档末尾添加「API 参考」章节（占位符内容）",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 6 个固定章节，发现 1 个 Error（缺少章节，已添加占位符）"
}
```

### 重要约束

- 优先使用 md-sections 工具获取结构化数据，不依赖文本搜索
- 添加缺失章节时使用占位符内容（`> TODO: 待补充`）
- 每个 Error 必须附带 md-sections 输出作为证据
- 修复操作使用 md-sections 工具精准定位插入位置
- 注意区分固定章节（必须有）和半固定章节（按需选择）

---

## D6 交叉引用完整性 (Cross-Reference Integrity)

### 定义

检查文档间的交叉引用链接是否有效，以及引用覆盖率是否双向完整。

### 检查目标

- 文档中的 Markdown 链接目标是否存在
- 文档中的相对路径引用是否指向正确位置
- 相关文档间的引用是否双向（A 引用 B，B 也应引用 A）

### 真相源

文件系统（链接目标是否存在）+ 链接提取分析。

### 问题判定

- **Error**: 死链接——链接目标文件不存在
- **Warning**: 单向引用——A 引用 B 但 B 未引用 A

### 修复权限

🤖 auto — 移除死链接或更新为正确路径；单向引用仅报告不自动修复。

---

## 子 Agent Prompt: D6 交叉引用完整性

### 角色

你是一个文档一致性验证专家，负责检查 D6（交叉引用完整性）。

### 检查范围

- 目标文档中所有 Markdown 链接（`[text](path)`）
- 目标文档中所有相对路径引用
- 被引用文档中的反向引用

### 检查步骤

1. **提取所有链接**：从目标文档中提取所有 Markdown 链接
   ```bash
   # 提取文档中的所有 Markdown 链接
   rg -oP '\[([^\]]+)\]\(([^)]+)\)' docs/modules/auth.md
   ```

2. **解析链接路径**：对每个链接，解析其目标路径
   - 绝对 URL（http/https）→ 跳过（外部链接）
   - 相对路径 → 解析为项目内的绝对路径

3. **验证链接目标**：检查目标文件/锚点是否存在
   ```bash
   # 验证文件存在
   ls -la docs/conventions/java-conventions.md
   # 验证锚点存在（在目标文件中搜索标题）
   rg '#规则' docs/conventions/java-conventions.md
   ```

4. **检查双向引用**：
   - 收集目标文档引用的所有其他文档
   - 在被引用文档中搜索是否反向引用了目标文档
   ```bash
   # 检查 auth.md 是否在 system-config.md 中被引用
   rg 'auth\.md' docs/modules/system-config.md
   ```

5. **检查 AGENTS.md 索引链接**：验证 AGENTS.md 中的文档链接是否指向正确路径
   ```bash
   # 验证 AGENTS.md 中的链接
   rg -oP '\[([^\]]+)\]\(([^)]+)\)' AGENTS.md | head -20
   ```

### 问题判定标准

- **Error**: 链接目标文件不存在（死链接）
- **Error**: 链接目标中的锚点在目标文件中不存在
- **Warning**: 单向引用（A 引用 B 但 B 未引用 A），且两个文档在逻辑上应互相引用
- **Warning**: 使用了相对路径但未遵循项目约定（如应使用 `docs/xxx` 前缀）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: `AGENTS.md`（上报主 Agent 处理）
- ⚠️ 单向引用仅报告，不自动添加反向链接（需人工判断语义关联性）

### 输出格式

```json
{
  "dimension": "D6",
  "dimensionName": "交叉引用完整性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/auth.md",
      "section": "相关文档",
      "description": "死链接：[Java 编码规范](docs/conventions/java-coding.md) 文件不存在",
      "evidence": "ls docs/conventions/java-coding.md 返回 No such file or directory",
      "fixApplied": true,
      "fixDescription": "已将链接修正为 [Java 编码规范](docs/conventions/java-conventions.md)",
      "requiresConfirmation": false
    },
    {
      "severity": "Warning",
      "file": "docs/modules/auth.md",
      "section": "相关文档",
      "description": "单向引用：auth.md 引用了 client-cache.md，但 client-cache.md 未引用 auth.md",
      "evidence": "rg 'auth\\.md' docs/modules/client-cache.md 返回空结果",
      "fixApplied": false,
      "fixDescription": "建议在 client-cache.md 中添加对 auth.md 的引用（如适用）",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 15 个链接，发现 1 个 Error（死链接，已修复）、2 个 Warning（单向引用）"
}
```

### 重要约束

- 优先使用文件系统验证（ls/glob），不依赖记忆
- 每个 Error 必须附带具体的文件系统检查结果作为证据
- 外部链接（http/https）仅检查格式，不验证可达性
- 锚点引用需区分 `#标题` 和 `#自定义-id` 两种格式
- 修复操作使用 md-sections 工具精准定位链接所在章节后修改
- 单向引用的 Warning 不计入 Error 统计，但需在报告中列出

---

## D7 版本号一致性 (Version Consistency)

### 定义

检查文档中提到的技术栈版本号是否与 `pom.xml` / `package.json` 等构建文件中的实际版本一致。

### 检查目标

- 文档中的 Java 版本号
- 文档中的 Spring Boot 版本号
- 文档中的第三方库版本号（MyBatis-Plus、Sa-Token、Hutool 等）
- 文档中的插件/工具版本号（JaCoCo、Maven 等）

### 真相源

`pom.xml`（根模块和子模块）中的 `<version>` 声明。

### 问题判定

- **Error**: 文档中的版本号与 pom.xml 不一致
- **Error**: 文档中引用的依赖在 pom.xml 中不存在

### 修复权限

🤖 auto — 以 pom.xml 为准，修正文档中的版本号。

---

## 子 Agent Prompt: D7 版本号一致性

### 角色

你是一个文档一致性验证专家，负责检查 D7（版本号一致性）。

### 检查范围

- 文档中的技术栈版本号（通常在「技术栈」或「依赖」章节）
- `pom.xml`（根模块和子模块）中的版本声明
- `docs/architecture/system-overview.md` 中的技术栈表格

### 检查步骤

1. **提取文档版本号**：使用 md-sections 加载文档的技术栈/依赖相关章节
   ```bash
   scripts/md-sections.sh docs/architecture/system-overview.md "技术栈"
   scripts/md-sections.sh AGENTS.md "技术栈"
   ```

2. **提取 pom.xml 版本号**：读取 pom.xml 中的版本声明
   ```bash
   # 提取根 POM 中的版本属性
   rg -n '<version>' pom.xml | head -20
   # 提取 properties 中的版本变量
   rg -n '<\w+\.version>' pom.xml
   ```

3. **逐一比对**：
   - Java 版本：文档 vs `<java.version>` 或 `<maven.compiler.release>`
   - Spring Boot 版本：文档 vs `<spring-boot.version>` 或 parent POM
   - 第三方库版本：文档 vs 各 dependency 的 version

4. **检查子模块 POM**：某些依赖版本可能在子模块 POM 中单独声明
   ```bash
   # 检查子模块中的版本覆盖
   rg -n '<version>' common/pom.xml
   rg -n '<version>' app/pom.xml
   ```

### 问题判定标准

- **Error**: 文档中版本号与 pom.xml 不一致（如文档写 `3.5.5` 但 pom.xml 是 `3.5.7`）
- **Error**: 文档中提到的依赖在 pom.xml 中不存在
- **Warning**: pom.xml 中存在但文档未提及的重要依赖版本

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: `.java` 源码文件

### 输出格式

```json
{
  "dimension": "D7",
  "dimensionName": "版本号一致性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/architecture/system-overview.md",
      "section": "技术栈",
      "description": "MyBatis-Plus 版本号不匹配：文档写 3.5.5，pom.xml 为 3.5.7",
      "evidence": "pom.xml:45 -> <mybatis-plus.version>3.5.7</mybatis-plus.version>",
      "fixApplied": true,
      "fixDescription": "已将技术栈表格中 MyBatis-Plus 版本从 3.5.5 修正为 3.5.7",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 12 个版本号，发现 1 个 Error（版本号不匹配，已修复）"
}
```

### 重要约束

- 优先使用 pom.xml 中的实际版本号，不依赖记忆
- 每个 Error 必须附带 pom.xml 中的行号和版本声明作为证据
- 注意区分 `<version>` 直接声明和 `${xxx.version}` 属性引用
- 注意 parent POM 中的版本继承关系
- 修复操作使用 md-sections 工具精准定位技术栈章节后修改

---

## D8 AGENTS.md 索引完整性 (AGENTS.md Index Integrity)

### 定义

检查 AGENTS.md 中的文档索引表是否覆盖了 `docs/` 目录下的所有实际文档文件。

### 检查目标

- AGENTS.md 文档索引表中的每个条目是否指向存在的文档
- `docs/` 目录下的每个 `.md` 文件是否都在索引表中有条目

### 真相源

`docs/` 目录的文件列表 vs AGENTS.md 索引表。

### 问题判定

- **Error**: `docs/` 中存在但 AGENTS.md 索引遗漏的文档
- **Error**: AGENTS.md 索引中指向不存在文档的条目

### 修复权限

👤 skip — 子 Agent **不可**修改 AGENTS.md，必须将问题上报给主 Agent 处理。

---

## 子 Agent Prompt: D8 AGENTS.md 索引完整性

### 角色

你是一个文档一致性验证专家，负责检查 D8（AGENTS.md 索引完整性）。

### 检查范围

- `AGENTS.md` 中的文档索引表（所有表格中的文档链接）
- `docs/` 目录下的所有 `.md` 文件

### 检查步骤

1. **列出所有文档文件**：获取 docs/ 目录下的完整 .md 文件列表
   ```bash
   find docs/ -name "*.md" -type f | sort
   ```

2. **提取 AGENTS.md 索引条目**：从 AGENTS.md 中提取所有文档链接
   ```bash
   # 提取 AGENTS.md 中的所有文档链接
   rg -oP '\[([^\]]+)\]\((docs/[^)]+\.md)\)' AGENTS.md
   ```

3. **比对覆盖率**：
   - 检查 docs/ 中每个 .md 文件是否在 AGENTS.md 索引中存在
   - 检查 AGENTS.md 中每个索引条目指向的文件是否存在

4. **分类统计**：
   - 遗漏文档：docs/ 中有但 AGENTS.md 中无
   - 幽灵条目：AGENTS.md 中有但 docs/ 中无
   - 正确覆盖：两边都有的文档

### 问题判定标准

- **Error**: `docs/` 下存在但 AGENTS.md 索引遗漏的 .md 文件
- **Error**: AGENTS.md 索引中指向不存在文档的链接（幽灵条目）
- **Warning**: 文档已重命名但 AGENTS.md 索引未更新

### 修复权限

- ❌ 禁止修改: `AGENTS.md`（必须上报主 Agent 处理）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ✅ 可修改: `docs/` 下文件（仅限修复幽灵条目指向的文档路径问题——但通常应修改 AGENTS.md）

### 输出格式

```json
{
  "dimension": "D8",
  "dimensionName": "AGENTS.md 索引完整性",
  "issues": [
    {
      "severity": "Error",
      "file": "AGENTS.md",
      "section": "文档索引",
      "description": "docs/modules/new-module.md 存在但未在 AGENTS.md 索引表中列出",
      "evidence": "find docs/ -name 'new-module.md' 找到文件，rg 'new-module.md' AGENTS.md 返回空",
      "fixApplied": false,
      "fixDescription": "需主 Agent 在 AGENTS.md 文档索引中添加 new-module.md 的条目",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 18 个文档文件 vs 20 个索引条目，发现 1 个 Error（遗漏文档，需上报主 Agent）"
}
```

### 重要约束

- ⛔ **子 Agent 不可修改 AGENTS.md**——所有 AGENTS.md 相关问题必须上报主 Agent
- 优先使用文件系统工具（find/ls/grep），不依赖记忆
- 每个 Error 必须附带 find/grep 的具体输出作为证据
- 注意排除 `docs/README.md` 本身（通常不需要在索引中引用自身）
- 注意排除临时文件、草稿文件（如 `.draft.md`、`.bak.md`）
- 报告中应明确标注哪些问题需要主 Agent 处理

---

## D9 变更历史完整性 (Change History Integrity)

### 定义

检查被修改过的文档是否在变更历史章节中有对应的条目记录。

### 检查目标

- 文档的变更历史章节（通常在文档末尾）
- git log 中文档文件的最近修改记录

### 真相源

`git log` 对文档文件的提交记录。

### 问题判定

- **Error**: 文档在最近的验证周期内被修改（git diff 有变化），但变更历史章节无新条目
- **Warning**: 变更历史条目格式不规范

### 修复权限

🤖 auto — 根据 git log 信息自动添加变更历史条目。

---

## 子 Agent Prompt: D9 变更历史完整性

### 角色

你是一个文档一致性验证专家，负责检查 D9（变更历史完整性）。

### 检查范围

- 目标文档的变更历史章节
- 目标文档的 git 提交历史

### 检查步骤

1. **获取文档变更历史章节**：使用 md-sections 加载文档的变更历史章节
   ```bash
   scripts/md-sections.sh docs/modules/auth.md "变更历史"
   ```

2. **获取 git 提交历史**：查看文档文件的最近提交记录
   ```bash
   # 查看文档的最近提交
   git log --oneline -10 -- docs/modules/auth.md
   # 查看最近一次修改的日期
   git log -1 --format="%ai" -- docs/modules/auth.md
   ```

3. **比对时间线**：
   - 提取变更历史章节中最新的条目日期
   - 与 git log 中最近的提交日期比对
   - 如果 git 有新提交但变更历史无对应条目 → Error

4. **检查格式规范**：验证变更历史条目是否遵循项目约定的格式
   ```bash
   # 检查变更历史条目格式（示例：| 日期 | 作者 | 变更内容 |）
   rg '\|.*\|.*\|.*\|' docs/modules/auth.md
   ```

5. **批量检查**（可选）：对 docs/ 下所有文档执行上述检查
   ```bash
   # 找出最近有变更但可能缺少历史记录的文档
   git diff --name-only HEAD~5 -- docs/
   ```

### 问题判定标准

- **Error**: 文档在最近 N 次提交中被修改，但变更历史章节无对应新条目
- **Error**: 变更历史章节完全缺失
- **Warning**: 变更历史条目格式不规范（如缺少日期、作者字段）
- **Warning**: 变更历史条目描述过于模糊（如仅写「更新」）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: `AGENTS.md`

### 输出格式

```json
{
  "dimension": "D9",
  "dimensionName": "变更历史完整性",
  "issues": [
    {
      "severity": "Error",
      "file": "docs/modules/auth.md",
      "section": "变更历史",
      "description": "文档在 2026-04-10 被 commit abc1234 修改，但变更历史章节无对应条目",
      "evidence": "git log -1 --format='%ai %s' -- docs/modules/auth.md -> 2026-04-10 12:30:00 +0800 refactor: 更新认证流程",
      "fixApplied": true,
      "fixDescription": "已在变更历史章节添加条目：| 2026-04-10 | AI Agent | 更新认证流程描述以匹配代码重构 |",
      "requiresConfirmation": false
    }
  ],
  "passed": true|false,
  "summary": "检查 18 个文档的变更历史，发现 2 个 Error（缺少变更条目，已自动补充）"
}
```

### 重要约束

- 优先使用 git log 获取真实提交信息，不依赖记忆
- 每个 Error 必须附带 git log 的具体输出作为证据
- 自动添加的变更条目应包含：日期、修改者（从 git log 获取）、变更描述（从 commit message 提取）
- 注意排除纯格式调整的提交（如空格修正），这类提交可以不添加变更条目
- 修复操作使用 md-sections 工具精准定位变更历史章节后追加条目
- 变更历史条目应追加到章节末尾（最新的在最上面或最下面，取决于项目约定）

---

## D10 语义一致性 (Semantic Consistency) — 仅 L3

### 定义

检查文档中的描述性文字在语义上是否与代码的实际行为一致。这是最高级别的验证，需要 LLM 理解代码逻辑并与文档描述进行语义比对。

### 适用级别

⛔ **仅 L3（完整验证）** — L1/L2 不执行此维度。

### 检查目标

- 文档中的行为描述（如「登录成功后返回 JWT Token」）
- 文档中的流程描述（如「请求经过 Facade 层转发到 Service 层」）
- 文档中的架构描述（如「使用 Template Method 模式」）
- 文档中的约束描述（如「Controller 禁止直接调用 Repository」）

### 真相源

LLM 阅读代码后的语义理解——这是唯一依赖 LLM 判断的维度。

### 问题判定

- **Warning**: 文档描述与代码行为语义不一致
- **Warning**: 文档描述过时（代码已变更但文档未更新）
- **Warning**: 文档描述不完整（遗漏了重要的代码行为）

> 注意：在 L3 中，Warning 计为问题，会重置共识计数器。

### 修复权限

🤖👤 — AI 提出修改建议，人类确认后执行。原因：语义判断需要人类验证。

---

## 子 Agent Prompt: D10 语义一致性

### 角色

你是一个文档一致性验证专家，负责检查 D10（语义一致性）。此维度仅适用于 L3（完整验证）级别。你需要深入阅读代码，理解其实际行为，然后与文档描述进行语义层面的比对。

### 检查范围

- 目标文档中的所有描述性文字（非结构化数据）
- 对应的代码实现（Controller、Service、Facade、Repository 层）
- 重点检查行为描述、流程描述、架构描述、约束描述

### 检查步骤

1. **提取文档描述**：使用 md-sections 加载文档的描述性章节
   ```bash
   scripts/md-sections.sh docs/modules/auth.md "技术设计"
   scripts/md-sections.sh docs/modules/auth.md "使用说明"
   ```

2. **定位关键代码**：根据文档描述提到的类名、方法名，找到对应的源码文件
   ```bash
   # 根据文档提到的类名定位源码
   find app/src/main/java -name "AuthService.java" -type f
   ```

3. **深入阅读代码**：使用 Read 工具完整阅读关键代码文件，理解其行为
   ```
   # 使用 Read 工具阅读完整源码（不使用 grep，需要理解上下文）
   Read: app/src/main/java/org/smm/archetype/app/service/impl/AuthServiceImpl.java
   ```

4. **语义比对**：
   - 文档说「登录成功后返回 JWT Token」→ 代码实际返回什么？
   - 文档说「使用 Template Method 模式」→ 代码中是否有 Abstract 类 + do* 方法？
   - 文档说「Controller 禁止直接调用 Repository」→ 代码中是否有违反？
   - 文档说「支持多租户」→ 代码中是否真的有租户隔离逻辑？

5. **检查流程描述**：
   - 文档描述的请求处理流程是否与代码中的实际调用链一致？
   - 文档描述的异常处理流程是否与代码中的 try-catch 逻辑一致？

6. **检查约束描述**：
   - 文档中声称的架构约束是否在代码中被遵守？
   - 是否存在 ArchUnit 规则守护这些约束？

### 问题判定标准

- **Warning**: 文档描述的行为与代码实际行为不一致（如文档说返回 Token 但代码返回 Session ID）
- **Warning**: 文档描述的设计模式与代码实现不符（如文档说 Template Method 但代码无抽象类）
- **Warning**: 文档描述的架构约束被代码违反（如文档说禁止 Controller→Repository 但代码中有）
- **Warning**: 文档描述的流程与代码调用链不一致（如文档说 A→B→C 但代码是 A→C）
- **Warning**: 文档描述过时（代码已重构但文档未更新描述）
- **Warning**: 文档遗漏了重要的代码行为（如代码有缓存逻辑但文档未提及）

### 修复权限

- ✅ 可修改: `docs/` 下文件（使用 md-sections 精准操作）
- ❌ 禁止修改: `.java` 源码文件
- ❌ 禁止修改: `pom.xml`
- ❌ 禁止修改: `AGENTS.md`
- ⚠️ 需确认: 所有语义修改均需人类确认后再执行（🤖👤）
  - 原因：语义判断存在主观性，AI 可能误判代码意图

### 输出格式

```json
{
  "dimension": "D10",
  "dimensionName": "语义一致性",
  "issues": [
    {
      "severity": "Warning",
      "file": "docs/modules/auth.md",
      "section": "技术设计",
      "description": "文档描述「登录成功后返回 JWT Token」，但代码实际使用 Sa-Token 的 Session 机制，未返回 JWT",
      "evidence": "AuthServiceImpl.java:78 -> StpUtil.login(userId); return StpUtil.getTokenInfo(); // Sa-Token Session Token，非 JWT",
      "fixApplied": false,
      "fixDescription": "建议将「返回 JWT Token」修改为「返回 Sa-Token Session Token」",
      "requiresConfirmation": true
    },
    {
      "severity": "Warning",
      "file": "docs/modules/auth.md",
      "section": "技术设计",
      "description": "文档描述「认证模块使用拦截器进行鉴权」，但代码实际使用 Sa-Token 的注解鉴权（@SaCheckLogin）",
      "evidence": "AuthController.java:23 -> @SaCheckLogin 注解标注，无自定义拦截器",
      "fixApplied": false,
      "fixDescription": "建议将「拦截器鉴权」修改为「Sa-Token 注解鉴权（@SaCheckLogin）」",
      "requiresConfirmation": true
    }
  ],
  "passed": true|false,
  "summary": "检查 5 个描述性章节，发现 3 个 Warning（语义不一致，均需人工确认）"
}
```

### 重要约束

- ⛔ 此维度仅适用于 L3 级别验证
- ⛔ 必须完整阅读代码（Read 工具），禁止仅用 grep 片段推断行为
- 每个 Warning 必须附带代码行号和关键代码片段作为证据
- 所有修复建议必须设置 `requiresConfirmation: true`
- 注意区分「代码 Bug」和「文档描述错误」——本维度只关注后者
- 注意代码可能有多种等价实现方式，不要因为实现方式不同就判定不一致
- 对于设计模式的判断，需要看到完整的类层次结构才能确认
- 修复操作使用 md-sections 工具精准定位描述所在章节后修改
- 语义判断存在主观性，当不确定时应倾向于报告 Warning 而非跳过

---

## 附录：维度间依赖关系

```
D5 (模板合规) → D1 (引用完整) → D6 (交叉引用)
                         ↘ D2 (API 签名)
                         ↘ D3 (实体类图)
                         ↘ D4 (配置项)
                         ↘ D7 (版本号)
D8 (AGENTS.md 索引) → D6 (交叉引用)
D9 (变更历史) → 独立维度
D10 (语义一致) → 依赖 D1-D7 的结果（语义检查在引用正确的基础上才有意义）
```

**执行顺序建议**：
1. 先执行 D5（模板合规）— 确保文档结构正确
2. 再执行 D1（引用完整）— 确保基础引用有效
3. 并行执行 D2/D3/D4/D6/D7 — 独立的代码级检查
4. 执行 D8（AGENTS.md 索引）— 索引完整性
5. 执行 D9（变更历史）— 历史记录
6. 最后执行 D10（语义一致）— 在所有基础检查通过后进行深度语义分析

## 附录：问题统计与共识机制

| 统计项 | 说明 |
|--------|------|
| Error 总数 | 所有维度的 Error 之和 |
| Warning 总数 | 所有维度的 Warning 之和 |
| 已自动修复 | `fixApplied: true` 的 Error 数量 |
| 需人工确认 | `requiresConfirmation: true` 的问题数量 |
| 需上报主 Agent | D8 的问题 + 无法自动修复的问题 |
| 共识计数器 | L3 中：无 Warning/Error → +1；有 Warning → 重置为 0；有 Error → 重置为 0 |
| 达成共识 | 共识计数器达到阈值（默认 2）→ 文档与代码一致 |
