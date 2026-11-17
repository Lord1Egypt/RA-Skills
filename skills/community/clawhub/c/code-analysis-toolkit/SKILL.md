---
slug: "code-analysis-toolkit"
name: "code-analysis-toolkit"
version: 1.0.1
displayName: "代码分析工具包专业版"
summary: "企业级Git历史分析,支持团队复盘、同意管理、趋势追踪与多格式报告"
license: "Proprietary"
edition: "pro"
description: |-
  面向团队与企业的高级 Git 历史分析工具,在免费版基础上扩展团队复盘、同意管理、趋势追踪等能力。核心能力:
  - 团队复盘分析(需全员同意)
  - 同意管理与审计追踪
  - 多仓库批量扫描与聚合报告
  - 历史趋势追踪与基线对比
  - 匿名化输出与隐私保护

  适用场景:
  - 团队迭代复盘与改进
  - 多仓库代码质量审计
  - 代码质量趋势追踪

  差异化:
  - 兼容免费版全部能力,无缝升级
  - 支持团队复盘与同意管理
  - 提供趋势追踪与基线对比
  - 优先技术支持与更新通道
tags:
  - 代码分析
  - Git历史
  - 企业级
  - 团队复盘
  - 趋势追踪
tools:
  - read
  - exec
homepage: "https://skillhub.cn"
# 定价元数据
suggested_price: "19.9 CNY/per_use"
pricing_tier: "L2-标准级"
pricing_model: "per_use"

---
# 代码分析工具包专业版

## 付费版专享能力

| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 代码分析工具包专业版企业级Git历史分析 | 不支持 | 支持 |
| 代码分析工具包专业版同意管理 | 不支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |

## 核心能力

### 1. 团队复盘分析(需全员同意)
支持全员同意的团队复盘,输出匿名化/聚合结果:

```bash
# 团队复盘(必须全员同意)
python -m src.main --i-have-consent \
  --multi-author-team-retro \
  --consented-author "Alice <alice@example.com>" \
  --consented-author "Bob <bob@example.com>" \
  --consented-author "Carol <carol@example.com>" \
  -r /path/to/team-repo \
  -f markdown -o team-retro.md
```

重要约束:

| 规则 | 说明 |
|:-----|:-----|
| 必须全员同意 | 每个被分析的成员都必须明确同意 |
| 双步选择 | 需同时指定 `--multi-author-team-retro` 和 `--consented-author` |
| 无排行榜 | 不生成排名表或跨作者对比表 |
| 匿名化选项 | 可输出匿名化结果 |
| 审计追踪 | 记录同意时间与范围 |

**输入**: 用户提供团队复盘分析(需全员同意)所需的指令和必要参数.
### 2. 同意管理
```json
{
  "consent_management": {
    "enabled": true,
    "consent_log": ".code-analysis/consent-log.json",
    "require_explicit": true,
    "consent_expiry_days": 90,
    "revocation_supported": true
  }
}
```

同意记录包含:

| 字段 | 说明 |
|---:|---:|
| 作者 | 被分析的 Git 作者 |
| 同意时间 | 明确同意的时间戳 |
| 分析范围 | 被授权分析的数据范围 |
| 过期时间 | 同意有效期 |
| 撤回状态 | 是否已撤回同意 |

**输入**: 用户提供同意管理所需的指令和必要参数.
**输出**: 返回同意管理的处理结果,包含执行状态码、结果数据和执行日志.
### 3. 多仓库批量扫描
```bash
# 批量扫描多个仓库
python -m src.main --i-have-consent \
  -r /path/to/projects \
  --scan-all \
  -f markdown -o batch-report.md
# ...
# 每个仓库单独分析,合并为聚合报告
```

**输入**: 用户提供多仓库批量扫描所需的指令和必要参数.
**输出**: 返回多仓库批量扫描的处理结果,包含执行状态码、结果数据和执行日志。- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `多仓库批量扫描` 选项

### 4. 历史趋势追踪
```bash
# 对比历史基线
python -m src.main --i-have-consent \
  -r /path/to/repo \
  --compare-baseline .code-analysis/baselines/q1-baseline.json \
  -f markdown -o trend-report.md
```

趋势追踪维度:

| 维度 | 追踪指标 | 说明 |
|:---:|:---:|:---:|
| 提交纪律 | 提交频率变化 | 与基线对比的增减 |
| 代码质量 | Bug 修复率趋势 | 是否在改善 |
| 测试覆盖 | 测试文件变更率 | 测试投入趋势 |
| 提交规范 | 规范符合度变化 | 规范采纳趋势 |

**输入**: 用户提供历史趋势追踪所需的指令和必要参数.
**处理**: 解析历史趋势追踪的输入参数,执行核心处理逻辑,返回结构化结果和执行状态.
**输出**: 返回历史趋势追踪的处理结果,包含执行状态码、结果数据和执行日志.
### 5. 匿名化输出
```bash
# 匿名化团队报告
python -m src.main --i-have-consent \
  --multi-author-team-retro \
  --consented-author "Alice <alice@example.com>" \
  --consented-author "Bob <bob@example.com>" \
  -r /path/to/repo \
  --anonymize \
  -f markdown -o anonymous-retro.md
```

匿名化规则:

| 处理项 | 方式 |
|:------|------:|
| 作者名 | 替换为"开发者 A/B/C" |
| 邮箱 | 完全移除 |
| 提交哈希 | 保留(用于引用) |
| 文件路径 | 保留(技术分析需要) |

**输入**: 用户提供匿名化输出所需的指令和必要参数.
**输出**: 返回匿名化输出的处理结果,包含执行状态码、结果数据和执行日志.
#
## 适用场景

### 场景一: 团队迭代复盘
迭代结束后,团队全员同意做复盘分析.
```bash
# 团队复盘(全员已同意)
python -m src.main --i-have-consent \
  --multi-author-team-retro \
  --consented-author "Alice <alice@example.com>" \
  --consented-author "Bob <bob@example.com>" \
  --consented-author "Carol <carol@example.com>" \
  -r /path/to/sprint-repo \
  -s 2026-04-01 -u 2026-06-30 \
  --anonymize \
  -f markdown -o sprint-23-retro.md
```

输出示例:

```text
团队迭代复盘报告 - Sprint 23
=====================================
# ...
使用须知:
- 本报告描述 Git 历史,不描述个人能力
- 代码审查、设计、指导等贡献不可见
- 结果仅供团队复盘讨论,不用于任何 HR 决策
# ...
匿名化说明:
- 开发者已替换为 A/B/C
- 所有分析均基于全员同意
# ...
团队聚合统计:
- 总提交数: 342
- 活跃开发者: 3 人
- 平均提交大小: 28 行
- 测试文件变更占比: 25%
# ...
各维度观察(匿名):
开发者 A: 提交频率稳定,测试覆盖率高
开发者 B: 提交较大,建议拆分小提交
开发者 C: Bug 修复占比低,代码质量稳定
# ...
团队改进建议(讨论提示):
- 考虑统一提交消息规范
- 测试文件变更占比可提升
- 建议定期做小提交
# ...
注意: 以上为讨论提示,非评判结论
```

### 场景二: 多仓库代码质量审计
对企业多个仓库做批量质量审计.
```bash
# 批量扫描
python -m src.main --i-have-consent \
  -r /path/to/projects \
  --scan-all \
  -f markdown -o quality-audit.md
# ...
# 对比基线
python -m src.main --i-have-consent \
  -r /path/to/projects \
  --scan-all \
  --compare-baseline .code-analysis/baselines/q1-baseline.json \
  -f markdown -o trend-audit.md
```

### 场景三: 代码质量趋势追踪
建立质量基线,定期追踪改进趋势.
```bash
# 建立基线
python -m src.main --i-have-consent \
  -r /path/to/repo \
  --save-baseline .code-analysis/baselines/q2-baseline.json
# ...
# 季度对比
python -m src.main --i-have-consent \
  -r /path/to/repo \
  -s 2026-07-01 -u 2026-09-30 \
  --compare-baseline .code-analysis/baselines/q2-baseline.json \
  -f markdown -o q3-trend.md
```

趋势报告示例:

```text
代码质量趋势报告 - Q3 vs Q2
=====================================
# ...
提交纪律:
- 提交频率: +12% (提升)
- 消息长度: +8 字符 (改善)
- 规范符合: 72% → 85% (显著提升)
# ...
代码质量:
- Bug 修复率: 18% → 15% (改善)
- 回退率: 3% → 2% (改善)
- 测试变更: 22% → 28% (提升)
# ...
结论:
本季度代码质量指标整体改善
建议: 继续保持提交规范,进一步提升测试覆盖
```

## 使用流程

### 优秀步: 初始化配置
```bash
mkdir -p .code-analysis/{baselines,reports,consent}
# ...
cat > .code-analysis/config.json << 'EOF'
{
  "edition": "pro",
  "consent_management": {
    "enabled": true,
    "consent_log": ".code-analysis/consent/consent-log.json",
    "require_explicit": true,
    "consent_expiry_days": 90
  },
  "batch": {
    "scan_all": true,
    "max_depth": 5
  },
  "trend": {
    "baseline_dir": ".code-analysis/baselines/",
    "auto_compare": true
  },
  "privacy": {
    "anonymize_default": false,
    "local_only": true
  }
}
EOF
```

### 第二步: 记录团队同意
```bash
# 记录同意(团队复盘前)
请记录以下成员的分析同意:
- Alice <alice@example.com> - 同意,有效期 90 天
- Bob <bob@example.com> - 同意,有效期 90 天
- Carol <carol@example.com> - 同意,有效期 90 天
分析范围: Sprint 23 期间的提交历史
```

### 第三步: 执行团队复盘
```bash
# 团队复盘分析
python -m src.main --i-have-consent \
  --multi-author-team-retro \
  --consented-author "Alice <alice@example.com>" \
  --consented-author "Bob <bob@example.com>" \
  --consented-author "Carol <carol@example.com>" \
  -r /path/to/repo \
  --anonymize \
  -f markdown -o team-retro.md
```

#
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---:|:---|---:|---:|
| content | string | 否 | code-analysis-toolkit处理的内容输入 |, 默认: 全部维度 |
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
|:------:|--------|:-------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8 或更高版本
- **Git**: 已安装且待分析仓库存在

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|----|:--:|---:|----|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| gitpython | Python 库 | 必需 | `pip install gitpython` |
| pydriller | Python 库 | 必需 | `pip install pydriller` |
| radon | Python 库 | 必需 | `pip install radon` |
| tabulate | Python 库 | 必需 | `pip install tabulate` |
| jinja2 | Python 库 | 必需 | `pip install jinja2` |
| click | Python 库 | 必需 | `pip install click` |
| reportlab | Python 库 | PDF 必需 | `pip install reportlab` |
| weasyprint(可选) | Python 库 | PDF 推荐 | `pip install weasyprint` |
| concurrent-futures | Python 标准库 | 批量扫描 | Python 自带 |

### API Key 配置
- 本工具完全在本地运行,无需外部 API Key
- 分析过程不传输数据到外部服务器

### 可用性分类
- **分类**: MD+EXEC+SCRIPT+AUDIT(Markdown 指令 + 命令行执行 + Python 分析脚本 + 审计日志)
- **说明**: 通过自然语言指令驱动 Agent 执行 Git 历史分析,支持团队复盘与趋势追踪
- **离线可用**: 是,完全在本地运行,不传输数据

## 案例展示

### 企业级配置
```json
{
  "edition": "pro",
  "organization": {
    "name": "开发团队",
    "team_members": [
      {"name": "Alice", "email": "alice@example.com"},
      {"name": "Bob", "email": "bob@example.com"}
    ]
  },
  "consent_management": {
    "enabled": true,
    "consent_log": ".code-analysis/consent/consent-log.json",
    "require_explicit": true,
    "consent_expiry_days": 90,
    "revocation_supported": true
  },
  "batch": {
    "scan_all": true,
    "max_depth": 5,
    "concurrent": 3
  },
  "trend": {
    "baseline_dir": ".code-analysis/baselines/",
    "auto_compare": true,
    "retention_baselines": 365
  },
  "privacy": {
    "anonymize_default": false,
    "local_only": true,
    "no_external_transmission": true
  },
  "audit": {
    "enabled": true,
    "log_dir": ".code-analysis/audit/",
    "retention_days": 365
  }
}
```

### 同意管理配置
```json
{
  "consent_log": {
    "format": "json",
    "fields": [
      "author_name",
      "author_email",
      "consent_timestamp",
      "analysis_scope",
      "expiry_date",
      "revoked": false,
      "revoked_date": null
    ]
  }
}
```

## 常见问题

### Q1: 专业版是否兼容免费版的报告格式?
完全兼容。专业版使用相同的分析维度与报告格式,免费版的报告可直接在专业版中对比.
### Q2: 团队复盘需要每个人的同意吗?
是的。每个被分析的 Git 作者都必须明确同意。缺少任何一人的同意,该作者的数据不会被分析.
### Q3: 同意记录如何管理?
同意记录存储在 `.code-analysis/consent/consent-log.json` 中,包含同意时间、范围、有效期等。支持随时撤回.
### Q4: 匿名化报告还能用于技术分析吗?
可以。匿名化只替换作者名和邮箱,保留提交哈希和文件路径,技术分析不受影响.
### Q5: 趋势对比的基线如何建立?
在首次分析时使用 `--save-baseline` 参数保存基线,之后可使用 `--compare-baseline` 与基线对比.
### Q6: 如何获得优先技术支持?
专业版用户可通过专属通道提交问题,通常 1 个工作日内响应.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|-------|-------|-------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | ，请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

