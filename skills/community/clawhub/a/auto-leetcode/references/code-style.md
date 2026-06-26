# 代码风格指南

## 通用原则

- 函数/类签名必须与 LeetCode 题目模板一致
- 使用中文注释解释关键逻辑和思路转折点
- 注释应解释"为什么"而非"做了什么"（代码本身已经说明了做了什么）
- 变量命名尽量贴合题目描述中的术语

## Python 特定

- 使用 `class Solution` + 实例方法
- 类型注解可选，但推荐在复杂函数上使用
- 使用 f-string 而非 % 或 .format()
- 优先使用 Python 内置函数和数据结构

## C++ 特定

- 使用 `class Solution` + public 方法
- 优先使用 STL 容器和算法
- 注意内存管理和生命周期

## Java 特定

- 使用 `class Solution` + public 方法
- 优先使用标准库集合类
- 注意类型装箱/拆箱

## JavaScript 特定

- 使用 `var {method_name} = function(...)` 风格（LeetCode 默认）
- 添加 JSDoc 注释标注参数和返回类型

## Go 特定

- 函数签名与 LeetCode 模板一致
- 注意 Go 的零值语义

## Rust 特定

- 使用 `impl Solution` + pub fn
- 注意所有权和借用规则