# Changelog

所有显著的变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-03-02

### 新增

- 初始版本发布
- 支持 .xls、.xlsx、.xlsm、.xltx、.xltm 格式
- 使用 python-calamine 作为主要解析引擎
- 自动降级到 xlrd/openpyxl 作为备选
- 自动安装依赖功能
- 结构化数据输出
- 文本格式转换
- 命令行支持

### 特性

- 高性能Excel解析，基于Rust实现
- 多工作表支持
- 跨平台兼容（Windows、Linux、macOS）
- 智能引擎选择
- 完善的错误处理

## [Unreleased]

### 计划

- [ ] 支持更多Excel格式
- [ ] 添加数据验证功能
- [ ] 支持公式计算
- [ ] 添加单元格格式信息
- [ ] 支持图片提取
