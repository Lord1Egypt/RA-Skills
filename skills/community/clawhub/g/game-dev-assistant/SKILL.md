---
name: game-development
description: 游戏开发辅助技能，涵盖游戏数据分析、关卡设计、资产整理、项目构建自动化、测试框架、游戏存档解析、 Unity / Unreal / Godot 项目辅助。触发场景：游戏数据分析、关卡配置、资产整理打包、项目构建自动化、游戏测试、存档解析、引擎项目辅助、shader 调试、日志分析。
---

# Game Development - 游戏开发辅助

## 核心能力

### 游戏数据分析
- 游戏行为日志解析（玩家操作、事件序列）
- 数值配置文件处理（JSON / YAML / Excel 导出）
- 排行榜数据提取和分析
- 游戏内经济系统数据建模

### 关卡 & 配置管理
- 关卡数据结构解析（ Tilemap / Grid / Node Graph）
- 配置文件批量生成（刷怪表/掉落表/奖励表）
- 多语言文案整理和导出
- 游戏常量 / 枚举值统一管理

### 资产整理 & 打包
- 资源目录规范化整理
- 资产依赖关系分析
- 批量资源压缩 / 格式转换（纹理/音频/模型）
- 资源包（AssetBundle / Pak）打包流程辅助

### 项目构建自动化
- Unity / Unreal / Godot 命令行构建
- 多平台构建（Windows / Android / iOS / WebGL）
- 构建后自动执行：版本号更新 / 签名 / 上传
- CI/CD 流程脚本（GitHub Actions / Jenkins）

### 游戏测试
- 功能测试脚本（pytest + 游戏 API）
- 自动化冒烟测试（登录/创建角色/基础操作）
- 性能数据采集（帧率/内存/加载时间）
- 截图对比自动化（UI 回归测试）

### 存档 & 日志
- 游戏存档结构解析（二进制 / JSON 存档）
- 存档编辑器辅助（修改数值/解锁内容）
- 服务器日志分析（异常/崩溃/外挂检测）
- 客户端日志收集和汇总

### 引擎项目辅助
- Unity C# 脚本生成 / 检查
- Unreal Blueprints 节点图解析
- Godot GDScript 辅助编写
- Shader 语法检查和调试

### 关键脚本
- `scripts/game_data_parser.py` - 游戏数据解析
- `scripts/level_config.py` - 关卡配置生成
- `scripts/asset_packer.py` - 资源打包整理
- `scripts/build_unity.py` - Unity 命令行构建
- `scripts/build_godot.py` - Godot 命令行构建
- `scripts/game_tester.py` - 游戏功能测试框架
- `scripts/save_parser.py` - 存档解析编辑
- `scripts/log_analyzer.py` - 游戏日志分析
- `scripts/generate_csharp.py` - Unity C# 脚本生成

### 参考资源
- `references/unity-build.md` - Unity CI/CD 构建指南
- `references/godot-api.md` - Godot 常用 API 速查
- `references/game-data-formats.md` - 常见游戏数据格式说明

## 工作流程

1. **明确需求**：游戏数据分析 / 资产整理 / 构建自动化 / 测试
2. **了解项目**：使用什么引擎？项目结构如何？
3. **执行对应脚本**：解析 / 生成 / 构建 / 测试
4. **交付结果**：数据报告 / 资源包 / 构建产物 / 测试报告

## 注意事项
- 游戏数据格式多样，先确认具体格式再解析
- 构建脚本需要对应引擎已安装 CLI 版本
- 测试脚本连接真实游戏需确认安全性和封号风险
- 存档修改注意备份原文件
- 资产打包前确认目标平台的格式要求
