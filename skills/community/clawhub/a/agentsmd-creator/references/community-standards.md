# 社区编码规范标准

各语言主流社区编码规范，用于新项目中生成默认编码规范引用。

## 默认社区语言栈标准

| 语言 | 规范名称 | 链接 |
|------|----------|------|
| Python | Google Python Style Guide | https://google.github.io/styleguide/pyguide.html |
| JavaScript/TypeScript | Airbnb JavaScript Style Guide | https://github.com/airbnb/javascript |
| JavaScript/TypeScript | Google JavaScript Style Guide | https://google.github.io/styleguide/jsguide.html |
| Java | Alibaba Java Coding Guidelines (P3C) | https://github.com/alibaba/p3c |
| Go | Effective Go | https://go.dev/doc/effective_go |
| C++ | Google C++ Style Guide | https://google.github.io/styleguide/cppguide.html |
| C# | Microsoft .NET Naming Conventions | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/ |

## 使用规则

- **已有项目（≥ 10 文件）**：从代码中分析实际编码规范，写入 `docs/CODING_STYLE.md`
- **新项目（< 10 文件）**：使用上表对应语言的社区规范作为默认标准
