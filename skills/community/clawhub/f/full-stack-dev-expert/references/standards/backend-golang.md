# Golang 编码规范（后端工程师实现必读）

适用：Go 1.22+。目标：惯用（idiomatic）优先，反对把 Java/Python 习惯带进 Go。

## 1. 工程结构

```
<repo>/
├── cmd/<app>/main.go        # 入口：只做装配（配置、依赖注入、启动），薄
├── internal/                # 私有代码，编译器强制不可被外部引用
│   ├── handler/             # HTTP 路由层：参数校验 + 调 service
│   ├── service/             # 业务层
│   ├── repository/          # 数据访问（database/sql + pgx / sqlx）
│   └── domain/              # 领域类型（实体、值对象、业务错误）
├── pkg/                     # 确认可被外部复用的库（没有就别建）
├── api/                     # OpenAPI/契约文件
└── migrations/
```

路由库 chi 或 gin（ADR 二选一全项目统一）；依赖注入手动 wire，不引框架。

## 2. 错误处理

- 错误是值：每层 `if err != nil` 显式处理，禁止 `_` 丢弃错误。
- 包装：`fmt.Errorf("create order %d: %w", id, err)`；判断用 `errors.Is/As`，
  禁止字符串匹配错误内容。
- 业务错误定义在 domain：哨兵错误（`var ErrOrderNotFound = errors.New(...)`）+
  `errors.Is` 映射 HTTP 状态码（统一错误响应出口）。
- panic 只用于不可恢复的程序性错误；HTTP handler 的 panic 由 recovery 中间件兜底转 500。

## 3. 并发纪律

- context.Context 一律第一个参数，透传取消与超时；禁止 `context.Background()` 在请求路径中途替换。
- goroutine 生命周期必须可归束：`errgroup.Group`（并发+错误聚合）/ `sync.WaitGroup`；
  泄漏 goroutine 是缺陷（`goleak` 测试）。
- channel 归属清晰：谁创建谁关闭；只发送方用 `chan<-`，只接收方用 `<-chan` 窄化。
- 共享可变状态：`sync.Mutex` 保护或改为 message passing；map 并发写必须加锁。
- `time.Sleep` 不用于同步生产代码，只用于退避重试（`x/exp/backoff` 或手写退避）。

## 4. 数据库与事务

- 驱动 pgx（PostgreSQL）/ go-sql-driver（MySQL）；连接池参数外置
  （MaxOpen/MaxIdle/ConnMaxLifetime）。
- 查询一律参数化占位符，禁止 fmt 拼 SQL；复杂查询集中 repository 可审查。
- 事务：`db.BeginTx` + defer rollback 模式，事务闭包收敛在 repository/service；
  事务内禁止 HTTP 调用。
- 扫描到显式结构体（禁止 map[string]any 透传到 handler）。

## 5. 接口与设计

- 接口定义在消费方（Go 惯例），小接口（1-3 方法）；不预先为"可替换"发明接口。
- 结构体校验：`go-playground/validator` 标签 + handler 统一校验入口。
- 零值可用：结构体默认零值即合法状态（`NewXxx` 构造器保不变量）。

## 6. 测试

- 表驱动测试（table-driven）为默认形态；`t.Run` 子测试名描述 场景+期望。
- httptest 走 HTTP 层集成测试；repository 用真实测试库（dockertest/testcontainers）。
- goleak 检查并发泄漏；测试不依赖执行顺序与共享状态。

## 7. 质量命令

```bash
go build ./... && go vet ./...
staticcheck ./...            # 引入后无 ERROR
go test ./... -race -count=1
```

提交前全过；`-race` 是强制项。
