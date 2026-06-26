# Go 语言最佳实践

## 1. 概述

Go 语言是一种开源的编程语言，它使构建简单、可靠和高效的软件变得容易。本指南涵盖了 Go 语言的最佳实践和推荐的编码标准。

## 2. 代码风格

### 2.1 命名规范

```go
// 包名：小写，简短，不使用下划线
package main

// 变量和函数：驼峰命名法
var userName string
func getUserInfo() {
}

// 常量：大写，使用下划线分隔
const MaxRetries = 3

// 结构体：首字母大写表示可导出
type User struct {
    Name string
    Age  int
}

// 接口：首字母大写表示可导出
interface Logger {
    Log(message string)
}
```

### 2.2 代码格式化

- 使用 `gofmt` 或 `go fmt` 自动格式化代码
- 行宽限制为 100 字符
- 缩进使用制表符（tab）

## 3. 包管理

### 3.1 Go Modules

```bash
# 初始化模块
go mod init example.com/project

# 添加依赖
go get github.com/gin-gonic/gin

# 整理依赖
go mod tidy
```

### 3.2 依赖版本管理

- 使用语义化版本控制
- 在 go.mod 文件中明确指定依赖版本
- 定期更新依赖以获取安全补丁

## 4. 错误处理

### 4.1 错误返回

```go
// 正确的错误处理方式
func getUser(id int) (User, error) {
    if id <= 0 {
        return User{}, errors.New("invalid user id")
    }
    // 业务逻辑
    return User{ID: id, Name: "John"}, nil
}

// 调用时处理错误
user, err := getUser(1)
if err != nil {
    log.Printf("Error getting user: %v", err)
    return
}
```

### 4.2 自定义错误

```go
// 自定义错误类型
type AppError struct {
    Code    int
    Message string
}

func (e *AppError) Error() string {
    return e.Message
}

// 使用自定义错误
func processRequest() error {
    return &AppError{Code: 400, Message: "Bad request"}
}
```

## 5. 并发编程

### 5.1 Goroutines

```go
// 启动 goroutine
func main() {
    go processTask()
    // 主协程继续执行
    time.Sleep(1 * time.Second)
}

func processTask() {
    fmt.Println("Processing task in goroutine")
}
```

### 5.2 Channels

```go
// 使用 channel 进行通信
func main() {
    ch := make(chan int)
    
    go func() {
        ch <- 42 // 发送数据到 channel
    }()
    
    value := <-ch // 从 channel 接收数据
    fmt.Println(value)
}

// 带缓冲的 channel
ch := make(chan int, 10)
```

### 5.3 WaitGroups

```go
// 使用 WaitGroup 等待多个 goroutine 完成
func main() {
    var wg sync.WaitGroup
    
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            fmt.Printf("Task %d completed\n", i)
        }(i)
    }
    
    wg.Wait() // 等待所有任务完成
    fmt.Println("All tasks completed")
}
```

## 6. 内存管理

### 6.1 切片

```go
// 切片的正确使用
func processSlice() {
    // 预分配容量
    slice := make([]int, 0, 100)
    
    for i := 0; i < 100; i++ {
        slice = append(slice, i)
    }
}

// 避免切片陷阱
func sliceTrap() {
    data := []int{1, 2, 3, 4, 5}
    slice := data[0:2] // 共享底层数组
    
    slice[0] = 100 // 会修改原数组
    fmt.Println(data) // [100 2 3 4 5]
}
```

### 6.2 映射

```go
// 映射的正确使用
func processMap() {
    // 预分配容量
    m := make(map[string]int, 100)
    
    m["key1"] = 1
    m["key2"] = 2
    
    // 检查键是否存在
    if value, exists := m["key1"]; exists {
        fmt.Println(value)
    }
}
```

## 7. 测试

### 7.1 单元测试

```go
// user_test.go
package main

import "testing"

func TestGetUser(t *testing.T) {
    user, err := getUser(1)
    if err != nil {
        t.Errorf("getUser(1) returned error: %v", err)
    }
    if user.ID != 1 {
        t.Errorf("Expected user ID 1, got %d", user.ID)
    }
}
```

### 7.2 基准测试

```go
func BenchmarkGetUser(b *testing.B) {
    for i := 0; i < b.N; i++ {
        getUser(1)
    }
}
```

## 8. 性能优化

### 8.1 减少内存分配

```go
// 避免频繁的字符串拼接
func concatStrings() string {
    var builder strings.Builder
    for i := 0; i < 1000; i++ {
        builder.WriteString("hello")
    }
    return builder.String()
}

// 使用对象池
var userPool = sync.Pool{
    New: func() interface{} {
        return &User{}
    },
}

func getUserFromPool() *User {
    return userPool.Get().(*User)
}

func returnToPool(user *User) {
    // 重置对象
    *user = User{}
    userPool.Put(user)
}
```

### 8.2 并发优化

```go
// 使用工作池
func workerPool() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // 启动 4 个工作协程
    for w := 1; w <= 4; w++ {
        go func(id int) {
            for job := range jobs {
                results <- job * 2
            }
        }(w)
    }
    
    // 发送任务
    for j := 1; j <= 10; j++ {
        jobs <- j
    }
    close(jobs)
    
    // 收集结果
    for a := 1; a <= 10; a++ {
        <-results
    }
}
```

## 9. 标准库使用

### 9.1 常用包

```go
// 导入常用包
import (
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
    "encoding/json"
    "sync"
)

// HTTP 服务器
func startServer() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello, World!")
    })
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

// JSON 处理
func jsonExample() {
    data := map[string]interface{}{
        "name": "John",
        "age":  30,
    }
    
    jsonData, err := json.Marshal(data)
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Println(string(jsonData))
}
```

## 10. 项目结构

### 10.1 推荐结构

```
myproject/
├── cmd/
│   └── server/
│       └── main.go        # 应用入口
├── internal/
│   ├── api/              # API 处理
│   ├── config/           # 配置
│   ├── model/            # 数据模型
│   ├── repository/       # 数据访问
│   └── service/          # 业务逻辑
├── pkg/                  # 可导出的包
│   ├── utils/            # 工具函数
│   └── logger/           # 日志工具
├── go.mod                # 依赖管理
└── README.md             # 项目说明
```

### 10.2 配置管理

```go
// config/config.go
package config

import (
    "os"
    "strconv"
)

type Config struct {
    Port    int
    DatabaseURL string
}

func Load() *Config {
    port, _ := strconv.Atoi(getEnv("PORT", "8080"))
    
    return &Config{
        Port:        port,
        DatabaseURL: getEnv("DATABASE_URL", "postgres://localhost:5432/mydb"),
    }
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}
```

## 11. 部署

### 11.1 Docker 部署

```dockerfile
# Dockerfile
FROM golang:1.20-alpine AS builder

WORKDIR /app
COPY . .

RUN go mod download
RUN go build -o server ./cmd/server

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
```

### 11.2 云部署

```yaml
# Kubernetes 部署配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: PORT
          value: "8080"
        - name: DATABASE_URL
          value: "postgres://db:5432/mydb"
```

## 12. 安全性

### 12.1 常见安全问题

- **SQL 注入**：使用参数化查询
- **跨站脚本 (XSS)**：对输入进行验证和转义
- **跨站请求伪造 (CSRF)**：使用 CSRF 令牌
- **敏感信息泄露**：不在代码中硬编码敏感信息
- **认证和授权**：使用安全的认证机制

### 12.2 安全最佳实践

```go
// 安全的 SQL 查询
func getUser(db *sql.DB, id int) (User, error) {
    var user User
    err := db.QueryRow("SELECT id, name FROM users WHERE id = $1", id).Scan(&user.ID, &user.Name)
    return user, err
}

// 密码哈希
func hashPassword(password string) (string, error) {
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
    return string(bytes), err
}

func checkPasswordHash(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}
```

## 13. 监控和日志

### 13.1 日志记录

```go
// 日志配置
func setupLogger() {
    log.SetOutput(os.Stdout)
    log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
}

// 结构化日志
import "github.com/rs/zerolog/log"

func structuredLog() {
    log.Info().
        Str("module", "auth").
        Str("user", "john").
        Int("status", 200).
        Msg("User logged in")
}
```

### 13.2 监控

```go
// 健康检查
func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

// 性能监控
import "github.com/prometheus/client_golang/prometheus"

var (
    requestsTotal = prometheus.NewCounter(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
    )
)

func init() {
    prometheus.MustRegister(requestsTotal)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    requestsTotal.Inc()
    // 处理请求
}
```

## 14. 最佳实践总结

1. **代码风格**：使用 `gofmt` 保持一致的代码风格
2. **错误处理**：显式处理错误，不要忽略
3. **并发**：合理使用 goroutines 和 channels
4. **内存管理**：注意切片和映射的使用，避免内存泄漏
5. **测试**：编写单元测试和基准测试
6. **性能**：关注内存分配和并发优化
7. **安全性**：防范常见安全问题
8. **项目结构**：遵循推荐的项目结构
9. **监控**：实现健康检查和性能监控
10. **文档**：为代码添加清晰的注释和文档

*本指南将持续更新，以反映 Go 语言的最新最佳实践和特性。*