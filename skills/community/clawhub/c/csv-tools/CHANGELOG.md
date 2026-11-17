# Csv Tools — 更新日志

## [1.1.0] - 2026-07-19

### Security Fix (post-release patch)
- 替换 `eval()` 为安全的 `_safe_math()` 表达式计算器（修复 Dangerous Code Execution 安全标记）
- SKILL.md权限声明补充：添加 Constraints 列、Permission Boundaries、Explicit Denied 扩展
- 触发关键词收窄：所有关键词加 CSV 前缀，新增 Do NOT use when 和 Usage Boundaries
- 新实现使用 shunting-yard 算法，仅允许数字和 +-*/()


## [1.1.0] - 2026-07-19

### 新增
- **stats 命令**: 列级统计 — sum/avg/min/max/std/中位数/唯一值/最常见值
- **columns 命令**: 列操作 — 重命名、选择、添加计算列(支持简单算术表达式)
- **detect 命令**: 数据类型自动检测 — 整数/浮点数/日期/布尔/文本识别
- **profile 命令**: 数据画像 — 缺失率可视化条形图、唯一值比例、最常见值
- **sample 命令**: 随机抽样 — head/tail/random/systematic 四种方式

### 变更
- validate 命令: 新增对 sentinel 值(N/A, NULL, NaN)的检测；无输出文件时默认显示前20条问题
- split 命令: 输出路径逻辑优化，自动处理 .csv 后缀
- preview 命令: 超过20列时提示"more"，显示行数位置

## [1.0.0] - 2026-07-19

### 新增
- 首次发布
- CSV 工具集 — 预览、筛选、排序、合并、分割、去重、验证
