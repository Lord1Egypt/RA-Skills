---
slug: "code-analyze"
name: "code-analyze"
version: 1.0.1
displayName: "代码分析工具专业版"
summary: "企业级多领域结构化分析,支持批量分析、团队协作、自定义框架与优先级支持"
license: "Proprietary"
edition: "pro"
description: |-
  面向团队与企业的高级结构化分析工具,在免费版基础上扩展批量分析、协作评审、自定义框架等能力。核心能力:
  - 多领域深度分析(代码、数据、文本、决策、可视化、架构)
  - 批量文件分析与聚合报告生成
  - 团队协作评审与多视角交叉验证
  - 自定义分析框架与模板管理
  - 历史分析存档与趋势追踪

  适用场景:
  - 企业代码库批量安全审查
  - 架构决策多视角评审
  - 团队复盘与改进追踪

  差异化:
  - 兼容免费版全部框架,无缝升级
  - 支持自定义分析维度与权重配置
  - 提供团队协作与历史追踪能力
  - 优先...
tags:
  - 开发工具
  - 代码分析
  - 企业级
  - 批量分析
  - 团队协作
tools:
  - read
  - exec
homepage: "https://skillhub.cn"
# 定价元数据
suggested_price: "29.9 CNY/per_use"
pricing_tier: "L3-专业级"
pricing_model: "per_use"

---
# 代码分析工具专业版

## 付费版专享能力

| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 代码分析工具专业版业级多领域结构化分析 | 不支持 | 支持 |
| 代码分析工具专业版支持批量分析 | 不支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |

## 核心能力

### 1. 六大领域深度分析
| 领域 | 分析重点 | 重点关注项 |
|:-----|:-----|:-----|
| 代码 | 生产故障、死代码 | 风格问题不等于缺陷 |
| 数据 | 粒度、缺失值、异常值 | 混合类型、分母缺失 |
| 文本 | 论点、证据强度 | 无来源的断言 |
| 决策 | 未列选项、可逆性 | 现状偏误 |
| 可视化 | 主导性、一致性 | 平台约定差异 |
| 架构 | 耦合度、扩展性 | 单点故障、技术债 |

**输入**: 用户提供六大领域深度分析所需的指令和必要参数.
**输出**: 返回六大领域深度分析的处理结果,包含执行状态码、结果数据和执行日志.
### 2. 批量分析与聚合报告
支持对整个目录或代码库进行批量分析,自动生成聚合报告:

```bash
# 批量分析整个模块
请对 src/payment/ 目录下所有 Python 文件执行安全分析
框架: MECE
输出: 聚合报告,按风险等级排序
```

**输入**: 用户提供批量分析与聚合报告所需的指令和必要参数.
### 3. 多视角交叉验证
同一输入由不同角色视角分析,交叉验证结论:

| 视角 | 关注维度 |
|---:|---:|
| 安全视角 | 漏洞、注入、权限 |
| 性能视角 | 复杂度、瓶颈、资源 |
| 可维护视角 | 耦合、命名、文档 |
| 业务视角 | 需求覆盖、边界条件 |

**输出**: 返回多视角交叉验证的处理结果,包含执行状态码、结果数据和执行日志.
### 4. 自定义分析框架
支持注册自定义分析框架,通过模板文件管理:

```json
{
  "framework_name": "安全合规审查",
  "dimensions": [
    "数据保护",
    "访问控制",
    "审计日志",
    "合规要求"
  ],
  "weights": {
    "数据保护": 0.4,
    "访问控制": 0.3,
    "审计日志": 0.2,
    "合规要求": 0.1
  },
  "thresholds": {
    "critical": 0.8,
    "warning": 0.6
  }
}
```

**输入**: 用户提供自定义分析框架所需的指令和必要参数.
**输出**: 返回自定义分析框架的处理结果,包含执行状态码、结果数据和执行日志。- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `自定义分析框架` 选项

### 5. 历史存档与趋势追踪
每次分析自动存档,支持按时间线追踪变化趋势:

```bash
# 查看历史分析
请列出过去 30 天针对 src/auth/ 模块的分析记录
对比: 安全风险分数变化趋势
```

**输入**: 用户提供历史存档与趋势追踪所需的指令和必要参数.
**输出**: 返回历史存档与趋势追踪的处理结果,包含执行状态码、结果数据和执行日志.
#
## 适用场景

### 场景一: 企业代码库批量安全审查

安全团队对整个服务做批量审查,生成聚合报告并分发给相关团队.
```bash
# 批量安全审查
请对 services/ 目录执行批量安全审查
分析维度: 注入风险、认证缺陷、敏感信息泄露、依赖漏洞
输出格式: 聚合报告 + 按服务分组的详细清单
优先级: 红色(立即修复) / 黄色(本周修复) / 白色(排期修复)
```

输出结构示例:

```text
批量安全审查报告 - services/
=====================================
# ...
红色 关键(3项):
1. [order-service] SQL 拼接存在注入风险 [来自输入 handler.py:45]
2. [auth-service] JWT 密钥硬编码 [来自输入 config.py:12]
3. [payment-service] 未验证回调签名 [来自输入 webhook.py:89]
# ...
黄色 重要(7项):
- [user-service] 密码强度未校验 [推断]
- ...
# ...
聚合统计:
- 审查文件: 156 个
- 发现问题: 24 项
- 红色占比: 12.5%
- 建议优先处理: order-service, auth-service
```

### 场景二: 架构决策多视角评审

对架构方案做四视角交叉评审,确保决策全面.
```bash
# 架构方案评审
请对以下微服务拆分方案做多视角评审:
方案: 按业务域拆分订单、用户、支付三个服务
视角: 安全 / 性能 / 可维护 / 业务
框架: MECE + 预演失败
```

### 场景三: 团队复盘与改进追踪

迭代结束后,对代码质量做复盘分析并追踪改进趋势.
```bash
# 迭代复盘分析
请对本次迭代(Sprint 23)的代码提交做复盘分析
分析维度: 提交规范、测试覆盖、重构比例、缺陷修复率
对比: 与 Sprint 22 的变化趋势
输出: 复盘报告 + 改进建议清单
```

## 使用流程

### 优秀步: 初始化工作区

```bash
# 创建分析工作区
mkdir -p .code-analyze/{reports,frameworks,history}
# ...
# 初始化配置
cat > .code-analyze/config.json << 'EOF'
{
  "edition": "pro",
  "default_framework": "MECE",
  "batch_limit": 200,
  "cross_validation": true,
  "auto_archive": true,
  "history_retention_days": 90
}
EOF
```

### 第二步: 注册自定义框架(可选)

```bash
# 在 frameworks 目录创建自定义框架
cat > .code-analyze/frameworks/security-review.json << 'EOF'
{
  "framework_name": "安全合规审查",
  "dimensions": ["数据保护", "访问控制", "审计日志"],
  "weights": {"数据保护": 0.5, "访问控制": 0.3, "审计日志": 0.2}
}
EOF
```

### 第三步: 执行批量分析

```bash
# 批量分析命令
请对 src/ 目录执行批量安全分析
配置: .code-analyze/config.json
框架: security-review
输出: .code-analyze/reports/security-$(date +%Y%m%d).md
```

### 第四步: 查看聚合报告

```bash
# 查看最新报告
请展示 .code-analyze/reports/ 下最新一份分析报告的摘要
包含: 红色问题数、黄色问题数、涉及模块、趋势对比
```

#
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|:---:|:---:|:---:|:---:|
| content | string | 否 | code-analyze处理的内容输入 |, 默认: 全部维度 |
| strict_level | string | 否 | 审查严格度, 可选: strict/normal/loose, 默认: normal |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_grade": "A",
    "total_score": 92,
    "max_score": 100,
    "summary": "处理完成",
    "details": [
      {
        "item": "代码风格",
        "status": "pass",
        "score": 95,
        "comment": "符合规范"
      },
      {
        "item": "安全合规",
        "status": "warn",
        "score": 80,
        "comment": "符合规范"
      }
    ],
    "improvements": [
      {
        "priority": "high",
        "suggestion": "建议优化",
        "expected_gain": "+5分"
      },
      {
        "priority": "medium",
        "suggestion": "建议优化",
        "expected_gain": "+3分"
      }
    ]
  },
  "error": null
}
```

## 异常处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 

## 依赖说明

### 运行环境

- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Python 3.8+(批量分析脚本,可选)

### 依赖说明(补充)

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 批量分析必需 | python.org |
| jq | CLI 工具 | 否 | 系统包管理器 |
| ripgrep | CLI 工具 | 批量扫描推荐 | 系统包管理器 |

### API Key 配置

- 本工具基于 Markdown 指令驱动,无需额外 API Key
- 批量分析若调用外部 LLM API,需配置对应 Key:

```bash
# 可选: 批量分析使用的外部 LLM Key(如非 Agent 内置)
export ANALYZE_LLM_API_KEY="your-api-key"
export ANALYZE_LLM_ENDPOINT="https://api.example.com/v1"
```

### 可用性分类

- **分类**: MD+EXEC+SCRIPT(Markdown 指令 + 命令行执行 + 可选 Python 脚本)
- **说明**: 核心分析通过自然语言指令驱动 Agent 执行,批量分析可通过 Python 脚本加速
- **离线可用**: 核心分析完全离线;批量分析脚本可选调用外部 API

## 案例展示

### 企业级配置

```json
{
  "edition": "pro",
  "organization": {
    "name": "技术团队",
    "default_reviewers": ["security-team", "arch-team"]
  },
  "analysis": {
    "default_framework": "MECE",
    "cross_validation_roles": ["security", "performance", "maintainability"],
    "batch_concurrency": 5,
    "max_file_size_mb": 10
  },
  "archive": {
    "enabled": true,
    "retention_days": 180,
    "storage": "local",
    "path": ".code-analyze/history"
  },
  "notification": {
    "on_critical": true,
    "channels": ["email", "webhook"]
  }
}
```

### 团队协作配置

```json
{
  "collaboration": {
    "shared_frameworks": true,
    "review_workflow": "round-robin",
    "min_reviewers": 2,
    "conflict_resolution": "senior-decides"
  }
}
```

## 常见问题

### Q1: 专业版是否兼容免费版的分析结果?

完全兼容。专业版输出的报告格式与免费版一致,免费版创建的分析可直接在专业版中打开和继续编辑.
### Q2: 批量分析有文件数量上限吗?

默认单次批量上限 200 个文件,可通过配置文件调整。超大批量建议分模块执行,避免单次分析时间过长.
### Q3: 自定义框架如何与内置框架混用?

在分析指令中指定即可,框架名称对应 frameworks 目录下的文件名:

```bash
# 混用框架
请用 security-review 框架分析 src/auth/,用 MECE 框架分析 src/utils/
```

### Q4: 历史分析数据存储在哪里?

默认存储在项目根目录的 `.code-analyze/history/` 下,可配置为其他本地路径。数据不出本机.
### Q5: 团队协作如何同步框架?

将 `.code-analyze/frameworks/` 目录纳入版本控制,团队成员拉取后即可共享自定义框架.
### Q6: 如何获得优先技术支持?

专业版用户可通过专属通道提交问题,通常 1 个工作日内响应.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:---------:|-----------|:----------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | ，请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

