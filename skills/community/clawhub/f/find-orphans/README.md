# Find Orphans（孤儿文件清理）

查找项目中未被引用的文件、未使用的组件和无效代码，生成清理建议报告。

## What It Does

- 检测完全未引用的文件（孤儿文件）
- 识别导入但未使用的组件
- 发现定义但未调用的工具函数
- 分析路由未注册的页面组件
- 生成分级清理建议（高/中/低优先级）

## How to Use

在 Claude Code 中当用户说「清理无用代码」「查找孤儿文件」「删除未使用的文件」或需要清理历史遗留代码时，本 skill 会扫描项目并输出《孤儿文件清理报告》。

## Requirements

- 适用于前端项目（React/Vue/Angular 等）
- 支持 TypeScript/JavaScript 项目
- 需要 package.json 和明确的入口文件
