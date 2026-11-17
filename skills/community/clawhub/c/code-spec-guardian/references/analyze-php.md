# PHP 规范分析指引 | PHP Analyzer

> 覆盖 PHP 项目的语言特有规范。以项目实际配置为准。

## 分析流程

1. 读 `references/analyze-code-style.md` 中的通用部分
2. 用 `read` 读 `composer.json` 获取依赖和 autoload 配置
3. 追加写入 `.code-spec/php-style.md`（PHP 特有条目，不要写入 code-style.md）

## PHP 特有分析维度

### 命名
- **变量/函数**：camelCase vs snake_case（PSR-1 要求 camelCase）
- **类**：PascalCase（PSR-1 强制）
- **常量**：UPPER_CASE（PSR-1 强制）
- **命名空间**：`Vendor\Project\Module`（PSR-4 autoload）

### 代码风格
- **缩进**：4 空格（PSR-12）
- **大括号**：类/方法次行，控制结构同行（PSR-12）
- **引号**：单引号 vs 双引号使用场景
- **PHP 标签**：`<?php` vs `<?=` vs 短标签
- **行宽**：PSR-12 建议 120 字符

### 框架特定
- **Laravel**：Artisan 命令、Eloquent Model、Migration、Middleware、Service Provider、Form Request 验证
- **Symfony**：Bundle 组织、Service 配置、Controller 写法、Doctrine ORM
- **CodeIgniter**：Controller 继承、Model 写法、路由配置

### 工具链
- **Linter**：PHP_CodeSniffer (phpcs/phpcbf) 配置
- **Formatter**：PHP-CS-Fixer 配置
- **静态分析**：Psalm / PHPStan 级别
- **测试**：PHPUnit，测试目录和命名

### 包管理
- composer.json 依赖管理
- autoload PSR-4 vs classmap
- require vs require-dev
