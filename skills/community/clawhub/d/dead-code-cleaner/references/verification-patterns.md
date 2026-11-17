# 验证模式参考

## 语言参考模式表

| 语言 | import 声明 | 动态加载 | 模板/标签引用 | 反射/运行时 |
|------|------------|---------|-------------|-----------|
| JS/TS (Node) | `from '...'`, `require('...')` | `import()` | N/A | `eval`, `Function()` |
| JS/TS (Vue) | `from '...'`, `require('...')` | `import()` | `<kebab>`, `<Pascal>`, `components:{}` | `eval` |
| JS/TS (React) | `from '...'`, `require('...')` | `import()`, `React.lazy()` | `<Pascal>`, JSX | `eval` |
| Python | `import X`, `from X import Y` | `__import__()`, `importlib` | N/A | `getattr`, `eval`, `exec` |
| Java | `import X` | `Class.forName()` | 注解引用 | Reflection API |
| Go | `import "X"` | `plugin.Open()` | N/A | `reflect` |
| Rust | `use X`, `mod X` | N/A | N/A | N/A |
| C/C++ | `#include "X"` | `dlopen()` | N/A | N/A |
| PHP | `use ...`, `require`, `include` | `class_exists()`, `autoload` | N/A | `ReflectionClass`, `call_user_func()` |
| C# | `using` | `Assembly.Load()`, `Activator.CreateInstance()` | N/A | `typeof()`, `System.Reflection` |

参数说明：
- `{rel_path}`：文件相对于源码根目录的路径，不含扩展名
- `{basename}`：文件名，不含扩展名
- `{PascalCase}`：basename 转 PascalCase
- `{kebab-case}`：basename 转 kebab-case
- `{camelCase}`：basename 转 camelCase


## 通用验证层（表外语言）

对于不在上表中的语言（如 Ruby、Swift、Kotlin、Scala、Dart、Elixir、Zig 等），codebase-memory-mcp 的图谱索引仍然有效——阶段 1 的孤立节点检测对所有语言一视同仁。进入阶段 2 时，使用以下通用验证层：

### L-grep-fallback：文件名全文搜索（替代 L-import-abs）

在整个项目中搜索对候选文件名的任何文本引用：
```bash
rg -l "{basename}" <repo-path> --type-not sql --type-not json --type-not yaml --type-not svg --type-not png
```
如果命中数 > 0，逐条核实是否为有效代码引用（排除同名异文件、注释/文档引用、配置文件中的同名键值）。

### L-import-rel：相对路径导入

与其他语言相同，搜索 `./` 和 `../` 模式。此层语言无关，始终执行。
```bash
rg -l "from ['"]\.\.?/.*{basename}['"]" <repo-path>
# 或通用模式（覆盖更多语言的 import 语法）
rg -l "['"]\.\.?/.*{basename}['"]" <repo-path>
```

### L-dynamic：动态加载

标记 N/A，同时将文件标记为「需人工复核」。表外语的动态加载模式差异太大（Ruby 的 `require`、Swift 的 `NSClassFromString` 等），无法可靠自动化。

### L-cross：跨项目/跨仓库引用

与其他语言相同。此层语言无关，始终执行。

### L-template-tag / L-component-reg

标记 N/A（非前端框架语言通常无此模式）。

### L-reflection：反射/运行时引用

标记 N/A，同时将文件标记为「需人工复核」。

### L-config-ref：配置文件引用

与其他语言相同。搜索配置文件（.yaml、.json、.xml、.properties、.toml）中的 `{basename}` 或 `{rel_path}`。此层语言无关，始终执行。

### 判定规则

表外语言的文件判定：
- L-grep-fallback 或 L-import-rel 或 L-cross 或 L-config-ref 命中有效引用 → ALIVE
- 以上四层均无命中 → DEAD
- 「需人工复核」标记（来自 L-dynamic / L-reflection）不影响判定，但文件在最终报告的「建议人工复核」章节中单独列出


## 阶段 2 验证层（表内语言精确模式）

以下为语言参考模式表中各语言对应的精确 `rg` 验证命令。对候选集中每个文件 F，根据其语言执行该语言对应的所有验证层。不适用的层跳过（标记 N/A）。

### Webpack/Vite 别名解析（JS/TS 前端项目前置步骤）

JS/TS 前端项目普遍使用路径别名（`@/`、`~/`、自定义 alias 等），使 `rg` 的裸 basename 搜索无法直接匹配。在运行 L-import-abs 之前：

1. 从构建配置中提取别名映射：
```bash
# webpack: 搜索 resolve.alias
rg "alias\s*:" webpack/ -A 50 2>/dev/null || rg "alias\s*:" vite.config.* -A 20
# 或直接查找常见的 webpack/vite 配置文件
rg "alias" webpack.config.* vite.config.* -A 5
```

2. 构建别名→路径映射表：
```
@ → src/
@components → src/components/
~ → src/
```

3. 在 L-import-abs 搜索时，对每个别名生成对应的搜索模式：
```bash
rel_path="views/my-service/foo"  # 文件在源码目录下的相对路径
rg -l "from ['"]@/${rel_path}['"]" <source-dir>/  # alias @/
```

### L-import-abs：绝对路径/别名路径导入

- JS/TS/Vue: 必须同时搜索两种模式以覆盖别名路径和非别名路径：
  - 模式 A（别名路径）：`rg -l "from ['"]@/{rel_path}['"]" <source-dir>/`
  - 模式 B（安全网）：`rg -l "from ['"].*{basename}['"]" <source-dir>/`
  - Shell 转义说明：外层用双引号时，内部双引号写 `"`，单引号无需转义
- Python: `rg "from {module_path} import|import {module_path}"`
- Java: `rg "import {package_path}"`
- Go: `rg "\"{module_path}\""`
- PHP: `rg "use .*{basename}|require.*{basename}|include.*{basename}"`
- C#: `rg "using .*{basename}|using static .*{basename}"`
- Rust: `rg "use {module_path}"`


### 同名校验（当 basename 在项目中出现多次时必做）

当候选文件 `{basename}` 在 `src/` 中存在多个同名文件时（可通过 `find <source-dir> -name "{basename}.*" | wc -l` 检测），仅靠 L-import-abs 模式 B 和 L-template-tag 的裸 basename 匹配无法区分引用的是哪一个同名文件。必须执行精确路径反查：

1. **检测同名文件数量**：
   ```bash
   find <source-dir> -name "{basename}.*" | wc -l
   ```
   若结果 ≤ 1，跳过此步骤。

2. **精确路径反查**（当同名文件 ≥ 2 时）：

   a. 对 L-import-abs 模式 B 的每个命中，替换为精确路径匹配：
   ```bash
   # 精确匹配：仅匹配包含正确路径的 import
   rg -l "from ['"].*{parent_dir}/{basename}['"]" <source-dir>/
   ```
   其中 `{parent_dir}` 为候选文件的直接父目录名（如 `baseline-check`）。仅此精确匹配的结果计入有效命中。

   b. 对 L-template-tag 的每个命中，确认该标签使用者与被引用文件在同一 `{parent_dir}` 子目录下：
   ```bash
   # 找到包含 kebab-case 标签的文件，检查是否在正确的目录路径下
   rg -l "<{kebab-case}[>\s/]" <source-dir>/ | xargs dirname | grep "/{parent_dir}/"
   ```
   若标签使用者和被引用文件不在同一个 `{parent_dir}` 子目录下，该命中为误报。

   c. 对 L-component-reg 的命中同样执行精确路径验证。

3. **判定**：仅精确路径匹配的结果计入有效命中。裸 basename 匹配结果在同名文件存在时不可信。

### L-import-rel：相对路径导入

- 覆盖 `./` 和 `../` 两种模式
- **搜索范围：整个源码目录（通常为 `src/`、`app/`、`lib/` 等，根据项目结构确定）**（而非仅 F 所在目录）。因为 `import X from './foo'` 可以出现在与 F 同目录的任意文件中，限制范围会导致漏检
- 搜索模式：
  ```bash
  # 模式 A：同目录相对导入
  rg -l "from ['"]\./{basename}['"]" <source-dir>/
  # 模式 B：安全网——任意包含 basename 的 import
  rg -l "from ['"].*{basename}['"]" <source-dir>/
  ```
- PHP: 搜索 `require` / `include` 中的相对路径：
  ```bash
  rg -l "(require|include|require_once|include_once)\s*['"]\.\.?/.*{basename}['"]" <source-dir>
  ```
- C#: 搜索 `.csproj` / `.sln` 中的项目引用（C# 源码文件间不通过路径直接引用，而是通过项目引用）。对 C# 候选文件，改为检查其所在 `.csproj` 是否被其他项目引用：
  ```bash
  rg -l "{basename}" **/*.csproj **/*.sln
  ```

**正则转义陷阱**：当文件名含点号时（如 `strategy.const.js`、`foo.bar.ts`），`rg` 正则中的 `.` 是通配符，会匹配任意字符。`rg "strategy.const"` 会误匹配 `strategyXconst`。必须写为 `rg "strategy\.const"` 才能精确匹配字面量点号。此问题会导致假阴性——文件实际有引用但被正则漏掉。

**示例**：对 `src/views/pages/general-settings/_components_/login-page-modify.vue`
```bash
rg -l "from ['"]\./login-page-modify['"]" src/
# 匹配: src/views/pages/general-settings/_components_/logo-settings.vue
rg -l "from ['"].*login-page-modify['"]" src/
# 匹配: 同上 + 任何其他形式的 import
```

### L-dynamic：动态加载

- JS/TS:
  ```bash
  # 标准动态导入
  rg "import\(['"`].*{basename}['"`]" <source-dir>/
  # Webpack require.context（动态批量加载目录下模块）
  rg "require\.context\(.*{basename}" <source-dir>/
  # Module Federation 远程模块加载
  rg "loadRemoteModule\(.*{basename}" <source-dir>/
  # Web Worker / Service Worker
  rg "new Worker\(['"`].*{basename}['"`]" <source-dir>/
  ```
- Python: `rg "__import__.*{basename}|importlib.*{basename}"`
- Java: `rg "Class\.forName.*{basename}|reflect.*{basename}"`
- PHP: `rg "class_exists.*{basename}|spl_autoload|new \\$"`
- C#: `rg "Assembly\.Load|Activator\.CreateInstance|Type\.GetType"`
- Go: `rg "plugin\.Open.*{basename}"`

### L-cross：跨项目/跨仓库引用

- 搜索范围：整个 monorepo / workspace，排除当前项目
- 搜索模式：`{rel_path}` + `{basename}` 精确匹配

### L-template-tag（前端框架）

- Vue: `<{kebab-case}>`, `<{PascalCase}>`
- React: JSX 中的 `<{PascalCase}>`
- Angular: `<{selector}>`

**注释排除（必做）**：前端框架的模板中，组件标签可能被 HTML 注释包裹（`<!-- <Component /> -->`）。`rg` 的字符串匹配无法区分注释与有效标签，因此必须执行两步验证：

```bash
# 步骤 1：找到所有包含组件标签的行
rg -n "<{kebab-case}|<{PascalCase}" <source-dir>/ --no-ignore

# 步骤 2：排除被 HTML 注释包裹的命中（管道过滤）
rg -n "<{kebab-case}|<{PascalCase}" <source-dir>/ --no-ignore | grep -v "<!--.*<"
```

仅步骤 2 的结果中余下的命中才是有效引用。如果步骤 1 有命中但步骤 2 为空的，该层标记为 0（无有效命中），并在报告中注明"命中均为注释"。

### L-component-reg（前端框架）

- Vue: `components: { {PascalCase} }`
- React: 无需额外检查（import 即注册）
- Angular: `declarations: [{PascalCase}]`

### L-reflection（后端语言）

- Python: `getattr(.*{basename})|eval(.*{basename})`
- Java: `Class\.forName|Method\.invoke`
- PHP: `ReflectionClass|new Reflection|call_user_func`
- C#: `typeof\(|\.GetType\(\)|System\.Reflection|MethodInfo`
- Go: `reflect\.`

### L-config-ref：配置文件引用

- 搜索配置文件（.yaml、.yml、.json、.xml、.toml、.properties、.ini）中的 `{basename}` 或 `{rel_path}`

---


### L-export-dead：导出级死代码检测（对应阶段 4.2d）

当候选文件 F 被标记为 DEAD，但其依赖的目标文件 T 因仍有其他消费者而标记为 ALIVE 时，对 F 从 T 导入的每个具名导出执行消费者精确搜索。仅当某个导出在项目中无任何活代码消费者时，才标记为 DEAD_EXPORT。

- **JS/TS/Vue**：
  ```bash
  # 搜索其他文件是否从 T 导入了具名导出 e
  rg -l "import\s*\{[^}]*\b{export_name}\b[^}]*\}\s*from\s*['\"].*{T_rel_path}['\"]" <source-dir>/
  ```
- **Python**：
  ```bash
  rg "from {module_path} import .*\b{export_name}\b"
  ```
- **Java**：
  ```bash
  rg "import static {package_path}\.{export_name}"
  # 同时覆盖通配符静态导入（如 `import static com.example.Foo.*`），通配符导入消费了该类的所有静态成员：
  rg "import static {package_path}\.\*"
  ```
- **Go**：不适用。Go 的导出以首字母大小写隐式区分，import 语句中不列出具名导出。
- **PHP**：
  ```bash
  rg 'use .*\\{export_name}' <source-dir>/
  ```
- **C#**：
  ```bash
  rg "using static .*{basename}\.{export_name}"
  ```
- **Rust**：
  ```bash
  rg "use {module_path}::{export_name}"
  ```

**判定**：若 e 的消费者仅来自 DEAD 集合（包括已删除的 F）→ 标记 DEAD_EXPORT，进入阶段 6.2 清理。

**默认导出排除**：`export default` 不适用此层——默认导出等同于整个文件，已在文件级检查中处理。

**重导出追踪**：若 T 本身是重导出文件（`export { X } from './actual-source'`），需递归追溯至 X 的最终定义文件，在最终定义文件中检查 X 的其他消费者。


## 交叉验证规则（对应 SKILL.md 阶段 3）

对每层命中：

1. **子串误匹配**：如 `vul-list` 包含 `ul-list`——用 `grep -v "vul-list"` 排除
2. **同名异文件**：如 `a/foo.vue` 被误判为引用了 `b/foo.vue`。此问题主要在阶段 2 的「同名校验」步骤中解决——当检测到同名文件时，必须用精确路径反查替换裸 basename 匹配。阶段 3 交叉验证时再次确认：逐一检查每个命中的 import/标签路径，确保其引用的文件路径与候选文件完全一致，排除指向同名异文件的所有命中。
3. **注释/文档引用**：注释或文档中的引用不是代码引用

标记规则：
- 任一层的任一命中经核实为**有效引用** → ALIVE，退出
- 所有层均无命中或所有命中均为误报 → DEAD

---

## 资源文件扩展名（对应 SKILL.md 阶段 6）

- **代码**：.vue .js .ts .jsx .tsx .py .java .go .rs .php .cs .c .cpp .h .rb .swift .kt .scala 等。以阶段 0 识别到的扩展名为准。
- **样式**：.scss .css .less .styl
- **资源**：.svg .png .jpg .gif .ico .woff .ttf .pdf

资源检查方法：在整个项目中 `rg` 搜索资源文件名。若仅被 DEAD 文件引用，标记 DEAD。
