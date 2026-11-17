# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-12

### Changed
- **calculator 能力升级 v2（科学计算 + 安全白名单）**
  - C 扩展 `core_perception_node`：弃用裸 `builtins.eval`，改为纯 C 递归下降白名单表达式求值器
    - 新增科学函数：sqrt/cbrt/sin/cos/tan/asin/acos/atan/sinh/cosh/tanh/asinh/acosh/atanh/
      exp/expm1/log/log2/log10/log1p/floor/ceil/trunc/degrees/radians/erf/erfc/gamma/lgamma
      （单参）+ pow/atan2/hypot/fmod/copysign/remainder/log(x,base)/min/max（双参）
    - 新增常量：pi/e/tau/inf/nan
    - 运算语义对齐 Python：负数取模（5 % -2 == -1）、地板除（-7 // 2 == -4）、
      幂右结合（3 ** 2 ** 2 == 81）、-2 ** 2 == -4、round half-to-even
    - 整数值返回 int（2 ** 10 -> 1024），其余返回 float
  - Python 兜底 `perception_node._safe_calc`：AST 白名单校验 + math 受限命名空间
    （清空 `__builtins__`），函数/常量集与 C 扩展对齐
  - 安全：两层均拒绝 `__import__`/`().__class__`/`open`/`lambda`/`exec`/属性访问/
    容器/任意未登记标识符；除法/取模除零报 CALC_ERROR
- **修复 calculator 缓存键缺陷**：ToolConfig 缺失 `cache_key_params=["expression"]`，
  导致所有表达式共用同一缓存键（`md5("calculator:{}")`），不同表达式互相串结果；
  现按 expression 区分缓存

### Files
- `so333/core_perception_node.c`（源码，v2 求值器）
- `so333/core_perception_node.c.bak-20260812` / `.pyd.bak-20260812` / `.so.bak-20260812`（旧版备份，工作空间）
- `scripts/core_perception_node.pyd` / `.so`（重新编译，Windows MinGW + WSL gcc；运行目录仅保留编译产物）
- `scripts/perception_node.py`（`_safe_calc` + calculator 分支 + ToolConfig 缓存键）

## [1.0.0] - 2026-07-15

### Added
- 三层架构（最外圈→外环→内圈）
  - 最外圈：工程意向性分析模组（阴性后台）
  - 外环：三角形顶点循环（得不到→数学→自我迭代）
  - 内圈：记录层（三轨存储）
- 三轨存储（JSON + Markdown + 错误智慧库）
  - JSON轨：结构化记录
  - Markdown轨：自我叙事
  - 错误智慧库轨：从错误中学习
- 五维智力模型
  - 算法智力（Algorithmic Intelligence）
  - 叙事智力（Narrative Intelligence）
  - 系统智力（System Intelligence）
  - 执行智力（Executive Intelligence）
  - 元智力（Meta Intelligence）
- 错误智慧库三阶段机制
  - Phase 1：工具性错误
  - Phase 2：认知性错误
  - Phase 3：预防引擎与时效性管理
- 人格层映射
  - 大五人格（OCEAN）
  - 马斯洛需求层次
- 元认知检测
  - 客观性评估器
  - 认知性错误检测
- 意向性分析模组
  - 意向性收集器
  - 意向性分类器
  - 意向性分析器
  - 触发判断器
  - 意向性调节器
  - 建议池
- 认知洞察模块
  - 认知洞察V2
  - 概念提取扩展
- C扩展模块
  - personality_core.so
  - core_perception_node.so
- 统一日志管理模块
- 参数校验框架
- 版本控制文件（VERSION, CHANGELOG.md）

### Changed
- 记录层从双轨存储升级为三轨存储
- 错误智慧库从被动纠错升级为主动预防
- 五维智力模型支持升维思考

### Fixed
- 修复 advice_pool.py 建议查询bug
- 修复多个模块API不匹配问题
- 修复参数校验不足问题

### Security
- 添加参数校验框架
- 添加统一日志管理
- 添加trace_id追踪

## [0.9.0] - 2026-04-11

### Added
- 五维智力模型基础实现
- 错误智慧库Phase 1/2/3
- 认知性错误检测与集成
- 时效性管理模块
- 预防规则引擎

### Changed
- 记录层从三轨存储升级为四轨存储（新增五维智力分支）
- 认知架构洞察升级为六步分析

## [0.8.0] - 2026-04-05

### Added
- 错误智慧库基础实现
- 客观性评估器
- 认知性错误分析器
- 错误智慧库管理器
- 预防规则引擎
- 时效性管理模块

### Changed
- 记录层从双轨存储升级为三轨存储（新增错误智慧库轨）
- description更新：新增"错误智慧库"和"从错误中学习"

## [0.7.0] - 2026-04-05

### Added
- narrative.md双轨存储功能
- 同步版本（memory_store_pure.py）
- 异步版本（memory_store_async.py）
- C扩展模块（personality_core.so, core_perception_node.so）

### Changed
- 记录层从单轨存储升级为双轨存储（JSON + Markdown）

## [0.6.0] - 2026-03-15

### Added
- 基础记录层实现
- JSON存储
- 人格层映射
- 意向性分析基础功能

---

## 版本说明

### 版本号规则
- **主版本号（MAJOR）**：不兼容的API变更
- **次版本号（MINOR）**：向下兼容的功能新增
- **修订号（PATCH）**：向下兼容的问题修正

### 变更类型
- **Added**：新增功能
- **Changed**：功能变更
- **Deprecated**：即将废弃的功能
- **Removed**：已移除的功能
- **Fixed**：问题修正
- **Security**：安全相关修复

---

**最后更新**: 2026-07-15  
**维护者**: AGI Evolution Team
