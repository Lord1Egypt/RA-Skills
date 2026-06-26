# 文档规范

## 概述

本文档定义代码注释和项目文档编写标准。详细的 JSDoc/TSDoc 注释格式见 `coding.coding-style.md` 注释规范章节，API 文档格式见 `coding.api.md`。

## 代码注释原则

- 解释 **"为什么"** 而非 "是什么"
- 仅在复杂算法、业务规则、临时方案处添加注释
- 公共 API 必须包含参数说明和返回值说明
- 删除已失效的注释

## 项目文档要求

### README.md（必须）
```markdown
# 项目名称

## 简介
项目简要描述（1-3 句话）

## 技术栈
- 前端：Vue 3 + TypeScript + Pinia
- 后端：Spring Boot 3 + MyBatis-Plus

## 快速开始
安装、运行、构建步骤

## API 文档
接口文档链接或入口说明
```

### CHANGELOG.md（必须）
```markdown
## [1.2.0] - 2026-01-15

### 新增
- 功能描述

### 修复
- 修复描述
```

## 文档工具

| 语言 | 工具 | 说明 |
|------|------|------|
| TypeScript/JavaScript | JSDoc / TSDoc | 函数、类、模块注释 |
| Java | Javadoc | 方法、类注释 |
| Python | Sphinx / docstring | 模块、函数注释 |

> **上下文提示**：在编写文档时，建议同时加载：
> - `coding.coding-style.md` - 注释格式规范
> - `coding.api.md` - API 文档规范
