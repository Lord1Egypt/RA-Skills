# Go 语言代码片段

## 1. 基础语法

### 1.1 基本数据类型

```go
// 基本数据类型
var i int = 42
var f float64 = 3.14
var b bool = true
var s string = "Hello"

// 简短变量声明
j := 100
k := "World"

// 常量
const PI = 3.14159
const (n = 5
    m = 10)

// 类型转换
x := int(3.14) // 3
y := float64(42) // 42.0
z := string(65) // "A"
```

### 1.2 控制流

```go
// if 语句
if x > 0 {
    fmt.Println("x is positive")
} else if x < 0 {
    fmt.Println("x is negative")
} else {
    fmt.Println("x is zero")
}

// for 循环
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// while 循环
j := 0
for j < 10 {
    fmt.Println(j)
    j++
}

// 无限循环
for {
    fmt.Println("Loop forever")
    break
}

// switch 语句
switch day {
case "Monday":
    fmt.Println("Start of week")
case "Friday":
    fmt.Println("End of week")
default:
    fmt.Println("Midweek")
}
```

## 2. 函数

### 2.1 函数定义

```go
// 基本函数
func add(a, b int) int {
    return a + b
}

// 多返回值
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// 命名返回值
func calculate(a, b int) (sum, product int) {
    sum = a + b
    product = a * b
    return // 裸返回
}

// 可变参数
func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

// 函数作为参数
func apply(op func(int, int) int, a, b int) int {
    return op(a, b)
}

// 匿名函数
func() {
    fmt.Println("Anonymous function")
}()

// 闭包
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}
```

### 2.2 结构体和方法

```go
// 结构体定义
type Person struct {
    Name string
    Age  int
}

// 结构体方法
func (p Person) Greet() string {
    return fmt.Sprintf("Hello, my name is %s and I'm %d years old", p.Name, p.Age)
}

// 指针接收器
func (p *Person) Birthday() {
    p.Age++
}

// 构造函数
func NewPerson(name string, age int) *Person {
    return &Person{Name: name, Age: age}
}

// 结构体嵌入
type Employee struct {
    Person
    Position string
    Salary   float64
}

func (e Employee) Greet() string {
    return fmt.Sprintf("%s and I work as a %s", e.Person.Greet(), e.Position)
}
```

## 3. 接口

```go
// 接口定义
type Logger interface {
    Log(message string)
}

// 实现接口
type ConsoleLogger struct{}

func (cl ConsoleLogger) Log(message string) {
    fmt.Println("LOG:", message)
}

type FileLogger struct {
    File *os.File
}

func (fl FileLogger) Log(message string) {
    fmt.Fprintln(fl.File, "LOG:", message)
}

// 接口作为参数
func LogMessage(logger Logger, message string) {
    logger.Log(message)
}

// 空接口
func PrintValue(v interface{}) {
    switch v.(type) {
    case int:
        fmt.Println("Integer:", v)
    case string:
        fmt.Println("String:", v)
    default:
        fmt.Println("Unknown type")
    }
}
```

## 4. 并发编程

### 4.1 Goroutines

```go
// 启动多个 goroutine
func main() {
    for i := 0; i < 5; i++ {
        go func(i int) {
            fmt.Println("Goroutine", i)
        }(i)
    }
    time.Sleep(1 * time.Second)
}

// 使用 sync.WaitGroup
func main() {
    var wg sync.WaitGroup
    
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            fmt.Println("Goroutine", i)
        }(i)
    }
    
    wg.Wait()
    fmt.Println("All goroutines completed")
}
```

### 4.2 Channels

```go
// 基本 channel
func main() {
    ch := make(chan string)
    
    go func() {
        ch <- "Hello from goroutine"
    }()
    
    message := <-ch
    fmt.Println(message)
}

// 带缓冲的 channel
func main() {
    ch := make(chan int, 3)
    
    ch <- 1
    ch <- 2
    ch <- 3
    
    fmt.Println(<-ch) // 1
    fmt.Println(<-ch) // 2
    fmt.Println(<-ch) // 3
}

// 关闭 channel
func main() {
    ch := make(chan int)
    
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)
    }()
    
    for value := range ch {
        fmt.Println(value)
    }
}

// 单向 channel
func send(ch chan<- int) {
    ch <- 42
}

func receive(ch <-chan int) {
    fmt.Println(<-ch)
}
```

### 4.3 互斥锁

```go
// 使用互斥锁
var (
    counter int
    mu      sync.Mutex
)

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}

func getCounter() int {
    mu.Lock()
    defer mu.Unlock()
    return counter
}

// 使用读写锁
var rwmu sync.RWMutex

func readCounter() int {
    rwmu.RLock()
    defer rwmu.RUnlock()
    return counter
}

func writeCounter(val int) {
    rwmu.Lock()
    defer rwmu.Unlock()
    counter = val
}
```

## 5. 错误处理

```go
// 基本错误处理
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// 自定义错误
type AppError struct {
    Code    int
    Message string
}

func (e *AppError) Error() string {
    return e.Message
}

func processRequest() error {
    return &AppError{Code: 400, Message: "Bad request"}
}

// 错误包装
func readFile(filename string) error {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        return fmt.Errorf("failed to read file: %w", err)
    }
    // process data
    return nil
}

// 错误检查
func main() {
    if err := readFile("test.txt"); err != nil {
        var appErr *AppError
        if errors.As(err, &appErr) {
            fmt.Printf("App error: %d - %s\n", appErr.Code, appErr.Message)
        } else {
            fmt.Printf("Generic error: %v\n", err)
        }
    }
}
```

## 6. 文件操作

```go
// 读取文件
func readFile(filename string) error {
    data, err := ioutil.ReadFile(filename)
    if err != nil {
        return err
    }
    fmt.Println(string(data))
    return nil
}

// 写入文件
func writeFile(filename, content string) error {
    err := ioutil.WriteFile(filename, []byte(content), 0644)
    if err != nil {
        return err
    }
    return nil
}

// 逐行读取
func readLines(filename string) error {
    file, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer file.Close()
    
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }
    
    return scanner.Err()
}

// 文件信息
func fileInfo(filename string) error {
    info, err := os.Stat(filename)
    if err != nil {
        return err
    }
    
    fmt.Printf("Name: %s\n", info.Name())
    fmt.Printf("Size: %d bytes\n", info.Size())
    fmt.Printf("Mode: %v\n", info.Mode())
    fmt.Printf("ModTime: %v\n", info.ModTime())
    fmt.Printf("IsDir: %v\n", info.IsDir())
    
    return nil
}
```

## 7. HTTP 服务器

```go
// 基本 HTTP 服务器
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello, World!")
    })
    
    http.HandleFunc("/api", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{
            "message": "Hello from API",
        })
    })
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

// 自定义 HTTP 处理器
type MyHandler struct{}

func (h *MyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello from MyHandler")
}

func main() {
    http.Handle("/", &MyHandler{})
    log.Fatal(http.ListenAndServe(":8080", nil))
}

// 路由
func main() {
    mux := http.NewServeMux()
    
    mux.HandleFunc("/", homeHandler)
    mux.HandleFunc("/about", aboutHandler)
    mux.HandleFunc("/api", apiHandler)
    
    log.Fatal(http.ListenAndServe(":8080", mux))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Home Page")
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "About Page")
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "message": "API Response",
    })
}
```

## 8. 数据库操作

### 8.1 SQLite

```go
import (
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
)

func sqliteExample() error {
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        return err
    }
    defer db.Close()
    
    // 创建表
    _, err = db.Exec(`CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)`)
    if err != nil {
        return err
    }
    
    // 插入数据
    _, err = db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "John", 30)
    if err != nil {
        return err
    }
    
    // 查询数据
    rows, err := db.Query("SELECT id, name, age FROM users")
    if err != nil {
        return err
    }
    defer rows.Close()
    
    for rows.Next() {
        var id int
        var name string
        var age int
        if err := rows.Scan(&id, &name, &age); err != nil {
            return err
        }
        fmt.Printf("ID: %d, Name: %s, Age: %d\n", id, name, age)
    }
    
    return rows.Err()
}
```

### 8.2 PostgreSQL

```go
import (
    "database/sql"
    _ "github.com/lib/pq"
)

func postgresExample() error {
    connStr := "host=localhost port=5432 user=postgres password=secret dbname=mydb sslmode=disable"
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return err
    }
    defer db.Close()
    
    // 测试连接
    if err := db.Ping(); err != nil {
        return err
    }
    
    // 创建表
    _, err = db.Exec(`CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, age INTEGER)`)
    if err != nil {
        return err
    }
    
    // 插入数据
    _, err = db.Exec("INSERT INTO users (name, age) VALUES ($1, $2)", "John", 30)
    if err != nil {
        return err
    }
    
    // 查询数据
    rows, err := db.Query("SELECT id, name, age FROM users")
    if err != nil {
        return err
    }
    defer rows.Close()
    
    for rows.Next() {
        var id int
        var name string
        var age int
        if err := rows.Scan(&id, &name, &age); err != nil {
            return err
        }
        fmt.Printf("ID: %d, Name: %s, Age: %d\n", id, name, age)
    }
    
    return rows.Err()
}
```

### 8.3 MongoDB

```go
import (
    "context"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

func mongoExample() error {
    // 连接 MongoDB
    client, err := mongo.Connect(context.Background(), options.Client().ApplyURI("mongodb://localhost:27017"))
    if err != nil {
        return err
    }
    defer client.Disconnect(context.Background())
    
    // 获取数据库和集合
    db := client.Database("mydb")
    coll := db.Collection("users")
    
    // 插入文档
    user := map[string]interface{}{
        "name": "John",
        "age":  30,
    }
    _, err = coll.InsertOne(context.Background(), user)
    if err != nil {
        return err
    }
    
    // 查询文档
    cursor, err := coll.Find(context.Background(), map[string]interface{}{})
    if err != nil {
        return err
    }
    defer cursor.Close(context.Background())
    
    for cursor.Next(context.Background()) {
        var result map[string]interface{}
        if err := cursor.Decode(&result); err != nil {
            return err
        }
        fmt.Println(result)
    }
    
    return cursor.Err()
}
```

## 9. JSON 处理

```go
// JSON 序列化
func jsonMarshal() error {
    type User struct {
        Name string `json:"name"`
        Age  int    `json:"age"`
    }
    
    user := User{Name: "John", Age: 30}
    data, err := json.Marshal(user)
    if err != nil {
        return err
    }
    fmt.Println(string(data)) // {"name":"John","age":30}
    return nil
}

// JSON 反序列化
func jsonUnmarshal() error {
    type User struct {
        Name string `json:"name"`
        Age  int    `json:"age"`
    }
    
    data := []byte(`{"name":"John","age":30}`)
    var user User
    if err := json.Unmarshal(data, &user); err != nil {
        return err
    }
    fmt.Printf("Name: %s, Age: %d\n", user.Name, user.Age)
    return nil
}

// 处理 JSON 文件
func jsonFile() error {
    type User struct {
        Name string `json:"name"`
        Age  int    `json:"age"`
    }
    
    // 读取 JSON 文件
    data, err := ioutil.ReadFile("users.json")
    if err != nil {
        return err
    }
    
    var users []User
    if err := json.Unmarshal(data, &users); err != nil {
        return err
    }
    
    // 处理数据
    for _, user := range users {
        fmt.Printf("Name: %s, Age: %d\n", user.Name, user.Age)
    }
    
    return nil
}
```

## 10. 命令行工具

```go
// 基本命令行参数
func main() {
    args := os.Args[1:]
    for _, arg := range args {
        fmt.Println(arg)
    }
}

// 使用 flag 包
func main() {
    var name string
    var age int
    var verbose bool
    
    flag.StringVar(&name, "name", "World", "Name to greet")
    flag.IntVar(&age, "age", 18, "Age of person")
    flag.BoolVar(&verbose, "verbose", false, "Enable verbose mode")
    flag.Parse()
    
    if verbose {
        fmt.Printf("Greeting %s who is %d years old\n", name, age)
    }
    fmt.Printf("Hello, %s!\n", name)
}

// 子命令
func main() {
    rootCmd := &cobra.Command{
        Use:   "myapp",
        Short: "My application",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("Hello from root command")
        },
    }
    
    addCmd := &cobra.Command{
        Use:   "add",
        Short: "Add two numbers",
        Run: func(cmd *cobra.Command, args []string) {
            a, _ := strconv.Atoi(args[0])
            b, _ := strconv.Atoi(args[1])
            fmt.Printf("%d + %d = %d\n", a, b, a+b)
        },
    }
    
    rootCmd.AddCommand(addCmd)
    rootCmd.Execute()
}
```

## 11. 性能优化

### 11.1 内存优化

```go
// 预分配切片容量
func preallocateSlice() {
    // 不好的做法
    s := []int{}
    for i := 0; i < 1000; i++ {
        s = append(s, i)
    }
    
    // 好的做法
    s := make([]int, 0, 1000)
    for i := 0; i < 1000; i++ {
        s = append(s, i)
    }
}

// 避免字符串拼接
func stringConcat() {
    // 不好的做法
    result := ""
    for i := 0; i < 1000; i++ {
        result += "hello"
    }
    
    // 好的做法
    var builder strings.Builder
    for i := 0; i < 1000; i++ {
        builder.WriteString("hello")
    }
    result := builder.String()
}

// 使用对象池
var bufferPool = sync.Pool{
    New: func() interface{} {
        return &bytes.Buffer{}
    },
}

func processData(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    buf.Reset()
    
    // 使用 buffer
    buf.Write(data)
    
    // 处理完成后归还
    bufferPool.Put(buf)
}
```

### 11.2 并发优化

```go
// 工作池
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
    
    // 发送 10 个任务
    for j := 1; j <= 10; j++ {
        jobs <- j
    }
    close(jobs)
    
    // 收集结果
    for a := 1; a <= 10; a++ {
        <-results
    }
}

// 使用 sync.Map
var m sync.Map

func concurrentMap() {
    // 存储值
    m.Store("key1", "value1")
    m.Store("key2", "value2")
    
    // 加载值
    if value, ok := m.Load("key1"); ok {
        fmt.Println(value)
    }
    
    // 删除值
    m.Delete("key1")
    
    // 遍历
    m.Range(func(key, value interface{}) bool {
        fmt.Printf("%v: %v\n", key, value)
        return true
    })
}
```

## 12. 测试

### 12.1 单元测试

```go
// user_test.go
package main

import "testing"

func TestAdd(t *testing.T) {
    result := add(2, 3)
    expected := 5
    if result != expected {
        t.Errorf("add(2, 3) = %d; want %d", result, expected)
    }
}

func TestDivide(t *testing.T) {
    tests := []struct {
        name     string
        a        float64
        b        float64
        expected float64
        hasError bool
    }{
        {"positive numbers", 10, 2, 5, false},
        {"negative numbers", -10, 2, -5, false},
        {"division by zero", 10, 0, 0, true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := divide(tt.a, tt.b)
            if (err != nil) != tt.hasError {
                t.Errorf("divide(%f, %f) error = %v, hasError %v", tt.a, tt.b, err, tt.hasError)
                return
            }
            if !tt.hasError && result != tt.expected {
                t.Errorf("divide(%f, %f) = %f, want %f", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### 12.2 基准测试

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        add(2, 3)
    }
}

func BenchmarkConcatStrings(b *testing.B) {
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        result := ""
        for j := 0; j < 100; j++ {
            result += "hello"
        }
    }
}

func BenchmarkBuilderStrings(b *testing.B) {
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        var builder strings.Builder
        for j := 0; j < 100; j++ {
            builder.WriteString("hello")
        }
        _ = builder.String()
    }
}
```

## 13. 部署

### 13.1 Docker

```dockerfile
# Dockerfile
FROM golang:1.20-alpine AS builder

WORKDIR /app
COPY . .

RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
```

### 13.2 Kubernetes

```yaml
# deployment.yaml
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
        - name: ENVIRONMENT
          value: "production"

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 14. 实用工具

### 14.1 时间处理

```go
// 时间格式化
func formatTime() {
    now := time.Now()
    
    // 格式化时间
    fmt.Println(now.Format("2006-01-02 15:04:05"))
    
    // 解析时间
    layout := "2006-01-02"
    date, err := time.Parse(layout, "2023-10-01")
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(date)
    
    // 时间计算
    tomorrow := now.Add(24 * time.Hour)
    lastWeek := now.AddDate(0, 0, -7)
    fmt.Println(tomorrow)
    fmt.Println(lastWeek)
}

// 定时器
func timerExample() {
    // 一次性定时器
    timer := time.NewTimer(2 * time.Second)
    <-timer.C
    fmt.Println("Timer fired")
    
    // 周期性定时器
    ticker := time.NewTicker(1 * time.Second)
    go func() {
        for range ticker.C {
            fmt.Println("Ticker fired")
        }
    }()
    
    time.Sleep(5 * time.Second)
    ticker.Stop()
    fmt.Println("Ticker stopped")
}
```

### 14.2 网络操作

```go
// HTTP 客户端
func httpClient() error {
    client := &http.Client{Timeout: 10 * time.Second}
    
    // GET 请求
    resp, err := client.Get("https://api.example.com")
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return err
    }
    fmt.Println(string(body))
    
    // POST 请求
    jsonData := []byte(`{"name": "John", "age": 30}`)
    resp, err = client.Post("https://api.example.com", "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    body, err = ioutil.ReadAll(resp.Body)
    if err != nil {
        return err
    }
    fmt.Println(string(body))
    
    return nil
}

// TCP 服务器
func tcpServer() error {
    listener, err := net.Listen("tcp", ":8080")
    if err != nil {
        return err
    }
    defer listener.Close()
    
    for {
        conn, err := listener.Accept()
        if err != nil {
            return err
        }
        
        go func(c net.Conn) {
            defer c.Close()
            
            // 读取数据
            buf := make([]byte, 1024)
            n, err := c.Read(buf)
            if err != nil {
                fmt.Println(err)
                return
            }
            
            // 发送响应
            c.Write([]byte("Hello from TCP server\n"))
            c.Write(buf[:n])
        }(conn)
    }
}
```

*本代码片段库将持续更新，以反映 Go 语言的最新最佳实践和特性。*