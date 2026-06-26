# 代码探索策略

本文档指导如何针对不同类型的项目读取代码、提取功能信息。核心原则：**不要逐行阅读，要找高信息密度的位置**。

---

## 一、项目类型识别信号

在根目录执行 `list_dir` 或 `ls`，根据文件特征判断项目类型：

| 发现的文件/目录 | 项目类型 | 后续读取策略 |
|--------------|---------|------------|
| `package.json` + `src/` + `components/` | Web 前端（React/Vue/Angular） | → 读导航/路由 + 页面组件 + i18n |
| `go.mod` / `pom.xml` / `*.csproj` / `Cargo.toml` | 后端服务 | → 读路由定义 + 控制器 + 数据模型 |
| `package.json` + `server.js` / `app.js` | Node.js 后端 | → 读 Express/Koa/Fastify 路由 |
| `requirements.txt` + `manage.py` | Django Web 应用 | → 读 urls.py + views.py + models.py |
| `*.xcodeproj` / `*.pbxproj` | iOS 原生应用 | → 读 Storyboard/SwiftUI View + ViewController |
| `AndroidManifest.xml` | Android 原生应用 | → 读 Activity/Fragment + XML 布局 |
| `pubspec.yaml` | Flutter 跨端应用 | → 读 lib/screens/ + lib/models/ |
| `*.sln` + `*.xaml` | WPF/WinForms 桌面 | → 读 XAML 页面 + ViewModel + 菜单资源 |
| `CMakeLists.txt` / `*.pro` | Qt/C++ 桌面 | → 读 .ui 文件 + MainWindow + 菜单定义 |
| `electron.js` / `main.js` + `renderer/` | Electron 桌面 | → 读 IPC 频道定义 + renderer 页面 |
| 以上多种并存 | 多端项目 | → 分别处理各端，最后合并成统一手册 |

---

## 二、各类项目的高信息密度位置

### Web 全栈项目

```
高价值位置（优先读）：
├── 路由/导航定义    → 功能清单的骨架
├── i18n 中文文件   → 所有 UI 文案（不要读组件里的硬编码字符串，读这里更快）
├── 数据模型/Schema  → 字段含义、业务实体
├── 权限配置文件     → 哪些功能对哪些角色开放
├── 核心 Service 层  → 业务规则、副作用
└── 枚举/常量文件    → 状态值、选项列表的含义

低价值位置（能不读就不读）：
├── 样式文件（*.css/*.scss）
├── 测试文件（*.test.*/*.spec.*）
├── 构建配置（webpack.config.js、vite.config.ts 等）
└── 第三方库代码（node_modules/）
```

### 纯后端服务（Go/Java/Python/C# 等）

```
高价值位置：
├── 路由注册文件      → 完整的接口列表 = 功能清单
├── 中间件/拦截器     → 权限规则、全局行为
├── 数据模型/ORM 实体 → 字段含义、约束
├── 业务逻辑层        → 核心算法、状态机、计算公式
├── 配置结构体        → 可配置项清单
└── 错误码定义文件    → 业务异常边界

可能有价值：
├── 数据库迁移文件    → 字段变更历史，推断设计演进
└── 注释/Swagger 注解 → 字段说明（比代码更接近业务语言）
```

### 桌面应用（WPF/Qt/Electron）

```
高价值位置：
├── 主窗口/菜单定义   → 功能导航结构
├── UI 资源文件       → 按钮文字、对话框标题（.resx/.strings/.ts）
├── ViewModel/Presenter → 界面逻辑、字段绑定
├── 命令注册表        → 用户可触发的所有操作
└── 设置/配置模型     → 系统可配置项

特别注意：
├── 桌面应用往往没有 i18n 文件，字符串直接写在资源文件或代码里
└── 找到菜单定义文件后，其层级结构直接对应文档的章节结构
```

### 移动端（iOS/Android/Flutter）

```
高价值位置：
├── 导航/路由定义     → 页面清单（Flutter: GoRouter; iOS: Coordinator; Android: Navigation Graph）
├── 字符串资源        → strings.xml / Localizable.strings / .arb 文件
├── 数据模型          → 业务实体
├── ViewModel/BLoC    → 界面行为逻辑
└── 权限声明文件      → AndroidManifest.xml / Info.plist 中的权限声明
```

---

## 三、可以写脚本辅助提取的场景

当代码量较大（>50 个文件）时，不要逐个手读，考虑写脚本：

### 脚本 A：提取所有路由/功能入口
```bash
# Go (Gin)
grep -rn "router\.\(GET\|POST\|PUT\|DELETE\|PATCH\)" --include="*.go" | grep -v "_test.go"

# Python (Django)
grep -rn "path\|re_path\|url(" --include="urls.py"

# Node.js (Express)
grep -rn "app\.\(get\|post\|put\|delete\|patch\)\|router\." --include="*.js" --include="*.ts"

# Java (Spring)
grep -rn "@RequestMapping\|@GetMapping\|@PostMapping" --include="*.java"
```

### 脚本 B：提取所有中文字符串（用于推断功能名称）
```bash
# 通用（搜索中文字符）
grep -rPn "[\x{4e00}-\x{9fff}]" --include="*.json" --include="*.ts" --include="*.go" | head -100

# 专找 i18n 文件
find . -name "*.json" | xargs grep -Pl "[\x{4e00}-\x{9fff}]" 2>/dev/null
find . -name "zh*.json" -o -name "*zh.json" -o -name "*.strings" 2>/dev/null
```

### 脚本 C：统计各目录代码量（判断哪里是核心）
```bash
# 各目录文件数
find . -type f -name "*.go" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -20

# 各文件行数（最大的往往是核心业务逻辑）
find . -type f \( -name "*.go" -o -name "*.ts" -o -name "*.py" \) | xargs wc -l | sort -rn | head -20
```

### 脚本 D：提取数据模型字段
```bash
# Go struct
grep -rn "^\s\+\w\+ \+\w\+.*\`" --include="*.go" | grep -v "_test.go"

# TypeScript interface/type
grep -A 30 "^interface \|^type .*{" --include="*.ts" -rn

# Python dataclass/model
grep -rn "^\s\+\w\+: " --include="*.py" | grep -v "def \|import "
```

### 脚本 E：提取权限/角色枚举
```bash
grep -rn "role\|Role\|permission\|Permission\|admin\|Admin" --include="*.go" --include="*.ts" --include="*.py" | grep -i "const\|enum\|iota\|=.*\"" | head -30
```

---

## 四、遇到看不懂的代码时

**优先策略（从快到慢）**：

1. **找注释**：函数/类的 doc comment 是最快的语义来源
2. **找调用方**：`grep -rn "functionName"` 看谁在调用，上下文能告诉你它的用途
3. **找测试**：`*_test.*` 文件里的测试用例通常有最清晰的行为描述
4. **找枚举值的使用**：枚举值在 `switch/if` 里的处理逻辑会告诉你每个值的含义
5. **找数据库迁移**：迁移文件的注释往往解释了字段为什么存在
6. **最后再读代码**：理解不了就标注"待确认"，不要猜测业务含义

---

## 五、多端项目的处理方式

如果项目包含前端 + 后端（或更多端），不要混在一起读：

1. **分端建立功能清单**：前端的菜单/路由 vs 后端的接口列表 → 对比找到对应关系
2. **以用户视角合并**：最终文档按用户操作路径组织，不按"前端章/后端章"拆分
3. **冲突时优先 UI 文案**：UI 上显示的文字最接近用户认知，以此命名功能
4. **纯后端项目**：没有界面，按接口分组（而非菜单）组织章节，关注参数含义和状态变化
