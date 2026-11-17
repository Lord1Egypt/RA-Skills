# Rust 规范分析指引 | Rust Analyzer

> 覆盖 Rust 项目的语言特有规范。以项目实际配置为准。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读 `Cargo.toml` 获取依赖和 edition
3. 追加写入 `.code-spec/rust-style.md`（Rust 特有条目，不要写入 code-style.md）

## Rust 特有分析维度

### 命名
- **类型/Trait/Enum**：PascalCase（Rust 惯例强制）
- **函数/变量/模块**：snake_case（Rust 惯例强制）
- **常量/静态变量**：UPPER_SNAKE_CASE
- **生命周期**：`'a` / `'ctx` 短命名

### 代码风格
- **缩进**：4 空格
- **引号**：`"` vs `r#"raw"#` 使用场景
- **分号**：必须（表达式 vs 语句的区别）
- **match 臂**：`=>` 对齐
- **rustfmt**：是否配置了自定义格式化规则

### 错误处理
- `Result<T, E>` vs `Option<T>` 使用模式
- `?` 操作符普及率
- `unwrap()` / `expect()` 使用边界（测试 vs 生产）
- 自定义错误类型：`thiserror` vs `anyhow` vs 手动 enum
- `panic!` 使用场景

### 所有权与借用
- 引用 vs Clone 的使用倾向
- 生命周期标注的使用频率
- `Cow<'_, T>` 使用场景
- `Arc<Mutex<T>>` / `Rc<RefCell<T>>` 使用模式

### 模块组织
- `mod.rs` vs `module_name.rs` 文件组织
- `pub` 可见性管理
- `use` 语句组织：标准库 → 第三方 → crate 内部
- re-export 模式（`pub use`）

### 异步
- `tokio` vs `async-std` vs `smol`
- `.await` 位置（行尾 vs 行首）
- `Spawn` vs `join!` vs `select!` 使用
- `Send + Sync` 约束处理

### 工具链
- **edition**：2021 / 2018 / 2015
- **clippy**：是否配置了自定义 lint 规则
- **rustfmt**：rustfmt.toml 配置
- **测试**：`#[test]` / `#[cfg(test)]` 模块组织，`#[tokio::test]` 异步测试

### 依赖管理
- Cargo.toml 的 `[dependencies]` vs `[dev-dependencies]` vs `[build-dependencies]`
- features 启用方式
- workspace 多 crate 管理
