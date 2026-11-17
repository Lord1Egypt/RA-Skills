# Go 规范分析指引 | Go Analyzer

> 覆盖 Go 项目的语言特有规范。以 Effective Go 为基础 + 项目实际约定。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读 `go.mod`（或从 `project_context.json` → `configs` 中获取片段）
3. 追加写入 `.code-spec/go-style.md`（Go 特有条目，不要写入 code-style.md）

## Go 特有分析维度

### 命名

- **包名**：全小写、单数、简短无下划线
- **导出标识符**：首字母大写
- **私有标识符**：首字母小写
- **接口**：单方法接口 `-er` 后缀（Reader/Writer），多方法接口用名词
- **Getter/Setter**：`Get` 前缀？（Go 惯例不推荐 `GetXxx`）
- **变量**：驼峰命名，缩写全大写（ID/URL/HTTP/JSON）

### 包组织

- 项目根目录 vs `cmd/` / `internal/` / `pkg/` 分层
- 标准项目布局：`cmd/` `internal/` `pkg/` `api/` `configs/` `scripts/`
- 是否有 internal 包限制外部导入
- 循环依赖检测：是否通过接口解耦

### 错误处理

- `if err != nil` 模式
- 错误包装：`fmt.Errorf("xxx: %w", err)` vs `errors.Wrap`
- 自定义错误类型
- panic vs error 使用边界
- 错误包（`pkg/errors` / `github.com/pkg/errors`）使用

### 代码风格

- **格式化**：`gofmt` / `goimports` 是否强制
- **import 分组**：标准库 → 第三方 → 本地（`goimports` 自动处理）
- **变量声明**：`:=` short declaration vs `var` 使用场景
- **零值利用**：是否充分利用零值初始化
- **make vs new** 使用
- **切片 vs 数组** 使用场景

### 并发

- goroutine 使用模式：`go func()` 匿名 vs 命名函数
- channel：buffered vs unbuffered
- `sync.WaitGroup` / `sync.Mutex` / `sync.RWMutex` 使用
- `context.Context` 传递和取消
- `errgroup` 使用

### 接口

- 小接口（1-3 方法）约定
- 接口定义位置：使用方定义（consumer side）
- 空接口 `interface{}` vs `any` 使用
- 类型断言 vs type switch

### 项目结构

- **HTTP 服务**：Gin / Echo / Fiber / net/http 标准库
  - router → handler → service → repository 分层
  - middleware 链组织
  - 路由分组
- **配置**：viper 使用、config struct 定义
- **依赖注入**：wire / dig / 手动注入

### 依赖管理

- go.mod 中的模块路径和版本
- require / replace / exclude 指令
- 依赖分组（直接依赖 vs indirect）

### 测试

- `*_test.go` 命名
- Table-driven tests 使用
- testify 库使用
- `TestMain` 使用
- mock：gomock / testify mock
- 基准测试 `BenchmarkXxx` 约定
- 测试覆盖率要求

### 数据库

- **GORM**：
  - Model 定义：gorm tag 约定
  - 查询链式调用风格
  - 事务处理方式
  - 连接池配置
- **sqlx / database/sql**：
  - 查询构建方式
  - 扫描约定

### 工具链

- golangci-lint 配置（`.golangci.yml`）
- Makefile 中的构建目标
- 代码生成：`go generate` 使用
- Wire 依赖注入生成
- Swag 文档生成
