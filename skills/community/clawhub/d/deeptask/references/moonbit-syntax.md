# MoonBit 语法速查表

## 类型定义

### 结构体（推荐）
```moonbit
✅ struct Todo {
  id: Int,
  title: String,
  completed: Bool,
}
```

### 废弃语法（不要用）
```moonbit
❌ type Todo {
  id: Int,
  title: String,
}
```

---

## 枚举定义

### 正确语法
```moonbit
✅ enum Command {
  Add(String),
  List,
  Complete(Int),
  Delete(Int),
}
```

### 废弃语法
```moonbit
❌ type Command {
  Add(String),
  List,
}
```

---

## 字符串操作

### 字符串拼接
```moonbit
✅ String.concat(a, b, c)
✅ a + b + c  // 需要导入 operator
❌ a ++ b ++ c  // 未定义
```

### 字符串格式化
```moonbit
✅ String.concat("ID: ", Int.to_string(id))
```

---

## 标准库导入

### 使用 prelude
```moonbit
✅ use prelude/List
✅ use prelude/Option
✅ use prelude/Int
✅ use prelude/String
```

### 直接使用（需要导入）
```moonbit
✅ List.map(todos, fn(t) { ... })
✅ Option.map(opt, fn(x) { ... })
```

---

## 主函数定义

### 正确语法
```moonbit
✅ fn main {
  println("hello")
}
```

### 错误语法
```moonbit
❌ pub fn main() -> Unit {
  println("hello")
}
```

---

## 模块引用

### 正确使用
```moonbit
✅ use todo
✅ todo.make_todo(1, "task")
```

---

## FFI 限制

### wasm-gc 后端不支持
```moonbit
❌ extern "c" {
  fn read_file(path: String) -> String
}
```

### 解决方案
- 使用 JavaScript 后端
- 或使用内置 IO 模块

---

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `type X is undefined` | 未导入 prelude | `use prelude/X` |
| `operator ++ is unbound` | 字符串拼接错误 | 使用 `String.concat` |
| `Missing main function` | main 函数语法错误 | 使用 `fn main { }` |
| `extern "C" is unsupported` | wasm-gc 不支持 FFI | 换 JavaScript 后端 |
| `deprecated_syntax` | 使用废弃 type 语法 | 改用 `struct` 或 `enum` |

---

## 项目结构

```
project/
├── moon.mod.json    # 模块定义
├── src/
│   └── pkg/
│       ├── moon.pkg.json  # 包配置
│       └── main.mbt       # 源代码
```

### moon.mod.json
```json
{
  "name": "my-project",
  "version": "0.1.0"
}
```

### moon.pkg.json
```json
{
  "is-main": true,
  "import": []
}
```

---

## 快速测试

```bash
# 创建测试项目
mkdir /tmp/moon-test && cd /tmp/moon-test
echo '{"name":"test","version":"0.1.0"}' > moon.mod.json
mkdir src/test_pkg
echo '{"is-main":true}' > src/test_pkg/moon.pkg.json
echo 'fn main { println("hello") }' > src/test_pkg/main.mbt

# 验证编译
moon build

# 运行
moon run .
```
