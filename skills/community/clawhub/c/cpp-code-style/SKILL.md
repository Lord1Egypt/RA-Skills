---
name: C++/CPP Code Style
description: C++/CPP代码都用这个coding style, code style, 代码风格，写代码之前阅读下面规则
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["g++", "gcc"]},"os":["linux","darwin","win32"]}}
---

# Google C++ Style Guide

写代码严格按照下面规则。
注意：external,3rdparty,.gitignore里面的文件都不在该规则范围内。

## 关键规则

### 1. 命名规范

- **文件名**: `snake_case.hpp`, `snake_case.cpp`
- **类名**: `CamelCase`
- **函数名**: `camelCase`（小驼峰，首字母小写）
- **变量名**: `snake_case`
- **类成员变量**: `m_camelCase`（m_前缀 + 小驼峰），不要m_camelCase_
- **常量**: `kCamelCase`（全局常量用 `g_CamelCase`）
- **命名空间**: `snake_case`

### 2. 缩进和格式

- **缩进**: 2 个空格，不使用 Tab
- **行宽**: 80 字符（软限制）
- **大括号**: 函数和类的开始大括号在新行，控制流语句的大括号在同一行
- **行尾空格**: 去掉行尾空格

```cpp
class Foo : public Bar {
 public:
  void Method() {
    if (condition) {
      DoSomething();
    }
  }
};
```

### 3. 空格

- 二元和三元操作符周围有空格
- 函数参数列表的第一个左括号紧贴函数名
- 返回类型和函数名之间有一个空格
- 指针/引用符号贴在类型上，而不是变量名

```cpp
// 正确
int* ptr;
int& ref;
void Func(int param1, int param2) { ... }

// 类成员变量
class MyClass {
 public:
  void myMethod() {
    m_counter = 0;  // m_ 前缀
    int local_var = 0;  // 局部变量用 snake_case
  }

 private:
  int m_counter;  // 成员变量 m_ + camelCase
};

// 错误
int *ptr;
int &ref;
void Func( int param1, int param2 ) { ... }
class MyClass {
  int counter;  // 缺少 m_ 前缀
};
```

### 4. 头文件保护

```cpp
#pragma once
// 或者
#ifndef _FILE_NAME_H_
#define _FILE_NAME_H_

// ... code ...

#endif  // _FILE_NAME_H_
```

### 5. 命名空间

- 不使用 `using namespace` 污染全局命名空间
- 使用 `namespace foo {` 和 `}  // namespace foo` 的格式
- 文件作用域的 `namespace` 声明后跟一对空大括号

```cpp
namespace litho {
namespace geo {

class Point { ... };

}  // namespace geo
}  // namespace litho
```

### 6. 注释

- 使用英文注释
- 使用 `//` 单行注释
- 使用 `/* */` 多行注释（仅当需要块注释时）
- 函数和类的文档使用 `/** ... */` 格式

```cpp
// 单行注释

/*
 * 多行注释
 */

/**
 * 函数描述
 * @param x 参数描述
 * @return 返回值描述
 */
```

### 7. 其他重要规则

- **私有成员**: 在 `private:` 之前声明公有的
- **内联函数**: 定义在头文件中
- **虚拟函数**: 声明为 `virtual`，在定义中不使用 `virtual` 关键字
- **常量成员**: 使用 `constexpr` 而不是 `const`
- **字符串字面量**: 使用 `// NOLINT` 关闭特定的 lint 警告（如果需要）
- **CMakefile**：不要用绝对路径和中文注释
- **CopyRight**： 使用当前年份，如2026
- **template**： template在class和function上一行
- **类成员变量**： 需要初始化
- **include顺序**：标准库 → 第三方库 → 项目头文件

## 工具

### clang-format

项目已配置 `.clang-format` 文件，使用 Google 风格。
检查`.clang-format` 文件是否符合上述规则，不符合修改`.clang-format` 文件。

格式化文件：
```bash
clang-format -i src/geo/*.hpp tests/*.cpp
```

## 参考

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [A C++ Guide](https://www.google-styleguide.com/)
