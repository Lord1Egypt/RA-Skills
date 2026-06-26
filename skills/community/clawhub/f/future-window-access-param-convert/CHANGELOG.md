# Changelog
All notable changes to the "cyberwin_hardwareaccess_param_convert" skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-11
### Added
- 初始版本发布，核心功能：替换文本模板中 @参数名@ 格式的占位符为智能门禁参数值
- 支持入参校验（templateText 非空字符串、paramData 非数组对象）
- 异常捕获机制，返回标准化成功/失败结果
- 适配 OpenClaw 平台技能规范，包含完整元信息、入参定义

### Changed
- 技能 ID 从 future_window_access_param_convert 统一修改为 cyberwin_hardwareaccess_param_convert
- 优化变量命名，提升代码可读性（如 模板文本/参数数据 注释）

### Fixed
- 无已知 bug，初始版本经入参边界测试验证

## [Unreleased]
### Planned
- 支持更多占位符格式（如 {{参数名}}）
- 新增批量模板替换功能
- 支持参数值为空时的自定义默认值配置