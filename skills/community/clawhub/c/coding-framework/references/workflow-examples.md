# 工作流示例

> coding-framework 的常见使用场景和工作流示例。

## 模式 1：快速编码

### 场景：用户要求写一个简单的 HTTP 服务

```
用户：用 Python 写一个 HTTP 服务，返回 JSON 格式的当前时间

coding-framework 处理流程：
1. 应用 Ponytail 决策阶梯
   - 需要存在吗？→ 是，用户明确要求
   - 代码库已有？→ 检查... 无
   - 标准库能做？→ 是！http.server + json + datetime
   - 停止在第 3 级
2. 输出最简实现
3. 标注：skipped: 路由框架/中间件/日志, add when 需要多端点或认证时
```

### 场景：用户要求重构一个模块

```
用户：重构 src/payment.py，代码太乱了

coding-framework 处理流程：
1. 评估复杂度 → 需要读取文件 + 分析 + 重写 → 复杂任务
2. spawn coding-agent（code-reviewer 先审查）
3. 根据审查结果制定重构计划
4. 如果重构涉及多轮改进 → 切换到迭代模式
```

## 模式 2：代理审查

### 场景：用户提交代码审查请求

```
用户：审查 src/api/ 目录的代码

coding-framework 处理流程：
1. 解析目标：src/api/ 目录
2. 分析代码特征 → 涉及 API 端点、认证、数据库操作
3. 自动选择代理：
   - code-reviewer（代码质量）
   - security-auditor（API 安全）
   - performance-analyst（N+1 查询检测）
4. 运行 review-orchestrator.py --auto-select
5. 并行 spawn 3 个子代理
6. 收集结果 → 置信度过滤 → 冲突解决
7. 生成汇总报告
```

### 场景：只做安全审查

```
用户：检查这段代码有没有安全漏洞

coding-framework 处理流程：
1. 识别：安全审查请求
2. 选择代理：security-auditor
3. spawn 单个子代理
4. 扫描 25 种安全模式
5. 输出安全审计报告
```

## 模式 3：迭代改进

### 场景：性能优化

```
用户：这个接口响应太慢了，帮我优化

coding-framework 处理流程：
1. 初始化迭代循环
   python scripts/loop-controller.py init \
     --name "optimize-api" \
     --mode adaptive \
     --max 10 \
     --patience 3
2. 第 1 轮：性能分析 → 发现 N+1 查询
3. 修复 N+1 → 更新状态
4. 第 2 轮：再次分析 → 发现缺少索引
5. 添加索引 → 更新状态
6. 第 3 轮：再次分析 → 无明显改进
7. 第 4 轮：仍无改进 → patience 触发 → 停止
8. 输出优化报告
```

### 场景：测试修复

```
用户：测试一直失败，帮我修到全部通过

coding-framework 处理流程：
1. 初始化迭代循环
   python scripts/loop-controller.py init \
     --name "fix-tests" \
     --mode max \
     --max 15 \
     --condition "regex:All tests passed"
2. 循环：运行测试 → 分析失败 → 修复 → 验证
3. 匹配完成条件 → 退出循环
```

## 模式 4：安全守卫

### 场景：用户执行危险命令

```
用户执行：rm -rf /tmp/build

coding-framework 处理流程：
1. PreExec hook 触发
2. pre-exec-check.sh 扫描命令
3. 匹配规则：dangerous-commands (critical)
4. 决策：block
5. 输出：
   {
     "decision": "block",
     "message": "命令被规则 'dangerous-commands' 阻止",
     "matched_rules": ["dangerous-commands"]
   }
6. 报告用户，建议替代方案：trash /tmp/build
```

### 场景：正常命令执行

```
用户执行：python test_main.py

coding-framework 处理流程：
1. PreExec hook 触发
2. pre-exec-check.sh 扫描命令
3. 无匹配规则
4. 决策：allow
5. 命令执行
6. PostExec hook 记录日志
```

## 组合工作流

### 场景：完整的编码 + 审查 + 优化流程

```
1. 快速编码（模式 1）
   → 写代码，应用 Ponytail 阶梯

2. 代理审查（模式 2）
   → 并行审查：code-reviewer + security-auditor
   → 发现问题 → 修复

3. 迭代改进（模式 3）
   → 性能优化循环
   → 直到满足条件

4. 安全守卫（模式 4）
   → 全程保护，每次 exec 前检查
```

## 自定义工作流

用户可以根据需要组合不同模式：

```
用户：帮我写一个新 API，写完做安全审查，然后优化性能

coding-framework：
1. 模式 1 → 写代码
2. 模式 2 → 安全审查（security-auditor）
3. 模式 3 → 性能优化迭代
4. 模式 4 → 全程安全守卫
```
