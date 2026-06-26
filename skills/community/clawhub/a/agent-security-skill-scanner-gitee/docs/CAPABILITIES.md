# Agent Security Skill Scanner - 功能能力文档

> **版本**: v2.0.1  
> **最后更新**: 2026-03-14  
> **状态**: ✅ 生产就绪

---

## 零、Skill 基本信息

### 0.1 标识信息

| 字段 | 值 | 说明 |
|------|-----|------|
| **Skill 名称** | `agent-security-skill-scanner` | 官方标识名 |
| **中文名称** | 技能安全扫描器 | 中文别名 |
| **简称** | `skill-scanner` | 短别名 |
| **版本** | v2.0.1 | 当前版本 |
| **作者** | Security Team | 开发团队 |
| **许可** | MIT License | 开源协议 |
| **分类** | Security | 安全类 |

### 0.2 调用标识

```yaml
# OpenClaw Skill 调用
skill: agent-security-skill-scanner
version: ">=2.0.0"

# 命令行调用
python cli.py scan <target>

# Python API 调用
from cli import scan_skill
result = scan_skill(target)
```

### 0.3 多语言命名习惯

| 语言/框架 | 命名方式 | 示例 |
|-----------|---------|------|
| **Python** | snake_case | `agent_security_skill_scanner` |
| **JavaScript** | camelCase | `agentSecuritySkillScanner` |
| **Go** | PascalCase | `AgentSecuritySkillScanner` |
| **Rust** | snake_case | `agent_security_skill_scanner` |
| **Java** | PascalCase | `AgentSecuritySkillScanner` |
| **Shell** | kebab-case | `agent-security-skill-scanner` |
| **URL/Path** | kebab-case | `agent-security-skill-scanner` |

### 0.4 兼容性

| 平台/框架 | 版本要求 | 支持状态 |
|-----------|---------|---------|
| **OpenClaw** | ≥2.0.0 | ✅ 完全支持 |
| **Python** | ≥3.8 | ✅ 完全支持 |
| **Linux** | Any | ✅ 完全支持 |
| **macOS** | ≥10.15 | ✅ 完全支持 |
| **Windows** | ≥10 | ✅ 支持 (需 Python 环境) |
| **Docker** | Any | ✅ 支持 (容器化部署) |

---

## 一、核心能力概览

| 能力域 | 功能模块 | 代码量 | 成熟度 |
|--------|---------|--------|--------|
| **扫描引擎** | static_analyzer.py | ~400 行 | ✅ 成熟 |
| **扫描引擎** | dynamic_detector.py | ~415 行 | ✅ 成熟 |
| **扫描引擎** | risk_scanner.py | ~445 行 | ✅ 成熟 |
| **检测模块** | detectors/malware.py | ~120 行 | ✅ 成熟 |
| **检测模块** | detectors/metadata.py | ~305 行 | ✅ 成熟 |
| **优化系统** | parallel_scanner.py | ~200 行 | ✅ 成熟 |
| **优化系统** | rule_iterator.py | ~340 行 | ✅ 成熟 |
| **优化系统** | auto_iteration.py | ~350 行 | ✅ 成熟 |
| **报告系统** | reporters/report_generator.py | ~370 行 | ✅ 成熟 |
| **CLI 工具** | cli.py + scanner_cli.py | ~390 行 | ✅ 成熟 |

**总代码量**: ~3,335 行核心代码

---

## 二、详细功能清单

### 2.1 静态分析能力 (static_analyzer.py)

**功能概述**: 通过 AST 抽象语法树分析和正则模式匹配，对 Skill 代码进行静态扫描，识别潜在的安全风险。

| 功能 | 说明 | 检测模式 | 技术实现 |
|------|------|---------|---------|
| 危险函数检测 | 识别 eval/exec/system 等危险调用 | 15+ 模式 | AST + 正则 |
| 混淆代码识别 | Base64/十六进制/ROT13 编码检测 | 5+ 模式 | 熵值分析 |
| 硬编码凭据 | API Key/密码/Token/私钥检测 | 10+ 模式 | 模式匹配 |
| 敏感文件访问 | /etc/, ~/.ssh/, /proc/等路径检测 | 8+ 路径 | 路径匹配 |
| 网络请求分析 | 无限制网络调用、C2 通信检测 | 6+ 模式 | URL 分析 |
| 环境变量窃取 | os.environ 敏感变量访问 | 3+ 模式 | 变量追踪 |

**检测规则示例**:
```python
# 危险函数检测规则
DANGEROUS_FUNCTIONS = [
    ('eval', '代码执行风险'),
    ('exec', '代码执行风险'),
    ('compile', '动态编译风险'),
    ('__import__', '动态导入风险'),
    ('os.system', '系统命令风险'),
    ('subprocess.call', '子进程风险'),
]

# 敏感路径检测
SENSITIVE_PATHS = [
    '/etc/passwd',
    '/etc/shadow',
    '~/.ssh/id_rsa',
    '/proc/self/environ',
]
```

**性能指标**:
- 检出率：≥95%
- 误报率：≤3%
- 扫描速度：~2 秒/技能
- 内存占用：~50MB

---

### 2.2 动态检测能力 (dynamic_detector.py)

**功能概述**: 在隔离沙箱环境中执行代码，监控运行时行为，捕捉静态分析无法发现的隐蔽威胁。

| 功能 | 说明 | 检测能力 | 技术实现 |
|------|------|---------|---------|
| 运行时行为监控 | 追踪实际执行行为 | 进程、文件、网络 | syscall 追踪 |
| 沙箱执行分析 | 隔离环境测试 | 安全隔离 | Docker/namespace |
| 网络流量检测 | C2 通信、数据外传识别 | DNS/HTTP/HTTPS | 流量分析 |
| 文件操作审计 | 敏感文件读写修改 | 系统/用户文件 | inotify |
| 进程注入检测 | 异常进程行为识别 | 内存注入检测 | ptrace |

**适用场景**:
- 高风险技能深度分析
- 混淆代码行为验证
- 零日威胁检测

**安全隔离**:
- 网络隔离：禁止外联
- 文件系统：只读挂载
- 进程隔离：namespace 隔离

---

### 2.3 风险扫描能力 (risk_scanner.py)

**功能概述**: 综合静态分析和动态检测结果，生成量化风险评分和处置建议。

| 功能 | 分级/范围 | 说明 | 算法 |
|------|---------|------|------|
| 综合评分 | 0-100 分 | 量化风险等级 | 加权平均 |
| 五级分类 | CRITICAL/HIGH/MEDIUM/LOW/SAFE | 风险分级处置 | 阈值判定 |
| 处置建议 | REJECT/REVIEW/ALLOW | 自动化决策支持 | 规则引擎 |
| 趋势分析 | 历史对比 | 风险演变追踪 | 时间序列 |

**风险阈值**:
```
CRITICAL (严重): ≥80 分 → 立即拒绝，存在明确恶意行为
HIGH (高):    60-79 分 → 人工审查，高风险特征
MEDIUM (中):  40-59 分 → 标记观察，中等风险
LOW (低):     20-39 分 → 低风险，常规监控
SAFE (安全):  <20 分  → 通过，无明显风险
```

**评分算法**:
```python
risk_score = (
    static_analysis_score * 0.4 +    # 静态分析权重 40%
    dynamic_analysis_score * 0.4 +   # 动态检测权重 40%
    metadata_score * 0.2             # 元数据权重 20%
)
```

---

### 2.4 恶意代码检测 (detectors/malware.py)

**功能概述**: 基于特征码和行为模式的恶意代码识别引擎。

| 检测类型 | 模式数 | 典型示例 | 风险等级 |
|---------|--------|---------|---------|
| 代码执行 | 5+ | `eval()`, `exec()`, `compile()` | HIGH |
| 动态导入 | 3+ | `__import__()`, `importlib` | MEDIUM |
| 系统命令 | 4+ | `os.system()`, `subprocess` | HIGH |
| 混淆解码 | 6+ | `base64.b64decode()`, `binascii` | MEDIUM |
| 网络攻击 | 8+ | `requests.post()`, `urllib` | HIGH |
| 权限滥用 | 10+ | 敏感路径、提权操作 | CRITICAL |

**检测流程**:
```
1. 文件扫描 → 2. 模式匹配 → 3. 特征提取 → 4. 风险判定 → 5. 报告生成
```

---

### 2.5 元数据检测 (detectors/metadata.py)

**功能概述**: 检查 Skill 的元数据完整性、权限声明合规性、依赖安全性。

| 检测项 | 检查内容 | 合规标准 | 风险权重 |
|--------|---------|---------|---------|
| Skill 完整性 | SKILL.md, cli.py 等必需文件 | 100% 必需 | 10% |
| 权限审查 | 声明权限与实际使用一致性 | 最小权限原则 | 25% |
| 依赖分析 | 第三方包来源与风险 | 可信源优先 | 30% |
| 维护者验证 | 身份可信度、历史记录 | 可追溯 | 15% |
| 版本合规 | 语义化版本规范 | SemVer 2.0 | 10% |

**必需文件清单**:
- `SKILL.md` - Skill 定义文件
- `cli.py` - CLI 入口
- `README.md` - 使用说明
- `LICENSE` - 开源协议

---

### 2.6 并行扫描 (parallel_scanner.py)

**功能概述**: 利用多进程并行处理，大幅提升批量扫描效率。

| 功能 | 性能提升 | 适用场景 | 资源消耗 |
|------|---------|---------|---------|
| 多进程扫描 | 4-8x 加速 | 批量技能扫描 | CPU 多核 |
| 批量处理 | 支持 100+ 技能 | 技能市场审核 | 内存 ~128MB |
| 结果聚合 | 统一报告格式 | 集中审计 | 磁盘 <50MB |

**使用示例**:
```bash
# 并行扫描整个技能目录
python parallel_scanner.py scan-all ./skills/ --workers 4

# 指定并发数
python parallel_scanner.py scan-all ./skills/ --workers 8 --output report.json
```

---

### 2.7 规则迭代 (rule_iterator.py)

**功能概述**: 基于扫描结果和误报反馈，自动优化检测规则和阈值。

| 功能 | 说明 | 更新频率 | 学习方式 |
|------|------|---------|---------|
| 规则优化 | 自动调整检测阈值 | 每次扫描后 | 自适应 |
| 误报学习 | 基于白名单更新规则 | 手动触发 | 监督学习 |
| 新威胁适配 | 规则库自动扩充 | 每周更新 | 威胁情报 |

**规则版本管理**:
```
rules/
├── v1.0/  # 初始规则
├── v1.5/  # 动态检测规则
├── v2.0/  # 并行扫描规则
└── v2.0.1/ # 当前规则
```

---

### 2.8 自动迭代系统 (auto_iteration.py)

**功能概述**: 定时自动执行扫描任务，持续监控技能库安全状态。

| 功能 | 配置选项 | 默认值 | 说明 |
|------|---------|--------|------|
| 定时扫描 | 可配置周期 | 每 6 小时 | cron 表达式 |
| 自动报告 | HTML/JSON/Markdown | JSON | 输出格式 |
| 持续优化 | 规则自学习 | 启用 | 自动更新规则 |
| 告警通知 | 邮件/Webhook | 可选 | 高风险告警 |

**配置示例**:
```yaml
# config.yaml
schedule:
  enabled: true
  cron: "0 */6 * * *"  # 每 6 小时
  
report:
  format: json
  output_dir: ./reports/
  
alert:
  enabled: true
  threshold: 60  # HIGH 风险告警
  webhook: https://example.com/alert
```

---

## 三、性能指标

| 指标 | 目标 | 实测 | 测试环境 |
|------|------|------|---------|
| 单技能扫描时间 | ≤5 秒 | 2-3 秒 | 4 核 CPU, 8GB RAM |
| 批量扫描 (100 个) | ≤5 分钟 | 3-4 分钟 | 并行模式 |
| 内存占用 | ≤256MB | ~128MB | 峰值 |
| 检测率 | ≥92% | ~95% | 测试样本集 |
| 误报率 | ≤4% | ~3% | 测试样本集 |
| CPU 利用率 | ≤80% | ~60% | 多核并行 |

---

## 四、使用场景

### 4.1 技能市场审核 🔒
- ✅ 新技能上架前安全扫描
- ✅ 定期安全复审 (每季度)
- ✅ 用户举报响应处理

### 4.2 企业 Agent 治理 🏢
- ✅ 内部技能库安全审计
- ✅ 供应链安全检查
- ✅ 合规性验证 (等保/GDPR)

### 4.3 开发者自检 👨‍💻
- ✅ 发布前安全自测
- ✅ CI/CD 集成检查
- ✅ 代码质量持续提升

---

## 五、集成方式

### 5.1 CLI 命令行

```bash
# 单个技能扫描
python cli.py scan <skill_path>

# 批量扫描
python cli.py scan-all <skills_dir>

# JSON 格式输出
python cli.py scan <skill_path> --format json

# 详细模式
python cli.py scan <skill_path> --verbose

# 指定输出文件
python cli.py scan <skill_path> --output report.json
```

### 5.2 Python API

```python
from cli import scan_skill

# 扫描技能
result = scan_skill("path/to/skill")

# 获取评分
score = result['overall']['score']
level = result['overall']['level']

# 处置建议
if result['overall']['verdict'] == 'REJECT':
    print("⚠️ 此技能存在高风险，建议拒绝")
elif result['overall']['verdict'] == 'REVIEW':
    print("⚡ 此技能需要人工审查")
else:
    print("✅ 此技能通过安全检查")
```

### 5.3 定时任务

```bash
# 添加到 crontab (每 6 小时扫描一次)
0 */6 * * * cd /path/to/scanner && python auto_iteration.py

#  systemd 服务
[Unit]
Description=Skill Security Scanner
[Service]
ExecStart=/usr/bin/python3 /path/to/auto_iteration.py
[Install]
WantedBy=multi-user.target
```

---

## 六、检测规则库

| 规则类别 | 规则数 | 覆盖范围 | 优先级 |
|---------|--------|---------|--------|
| 恶意代码 | 25+ | 代码执行、命令注入 | P0 |
| 权限滥用 | 20+ | 文件、网络、系统调用 | P0 |
| 数据泄露 | 15+ | 敏感数据外传 | P1 |
| 混淆隐藏 | 10+ | 编码、加密、隐藏 | P1 |
| 依赖风险 | 30+ | 恶意 npm/Python 包 | P2 |

**总计**: 100+ 检测规则

---

## 七、白名单机制

| 类型 | 说明 | 配置方式 |
|------|------|---------|
| 本地白名单 | 项目级豁免 | `data/whitelist/local.json` |
| 公共白名单 | 官方可信技能 | 定期同步更新 |
| 模式白名单 | 规则级豁免 | 配置文件指定 |
| 哈希白名单 | 文件级豁免 | SHA256 哈希匹配 |

---

## 八、报告输出

| 格式 | 用途 | 大小 | 示例 |
|------|------|------|------|
| JSON | 机器处理、API 集成 | ~5KB | `report.json` |
| HTML | 人工审查、可视化 | ~50KB | `report.html` |
| Markdown | 文档归档、Git 提交 | ~10KB | `report.md` |
| 文本 | 终端快速查看 | ~2KB | 终端输出 |

---

## 九、版本演进

| 版本 | 发布日期 | 核心能力 | 状态 |
|------|---------|---------|------|
| v1.0 | 2026-02-15 | 基础静态分析 | 已归档 |
| v1.5 | 2026-02-28 | 动态检测、白名单 | 已归档 |
| v2.0 | 2026-03-10 | 并行扫描、自动迭代 | 稳定 |
| v2.0.1 | 2026-03-14 | 完整功能集、文档完善 | **当前** |

---

## 十、技术栈

| 项目 | 规格 |
|------|------|
| **语言** | Python 3.8+ |
| **依赖** | 标准库为主，最小化外部依赖 |
| **兼容** | OpenClaw 2.0+ |
| **许可** | MIT License |
| **架构** | 模块化、可扩展 |

---

## 十一、限制与注意事项

### 11.1 已知限制
- 动态检测需要额外权限 (sandbox 环境)
- 某些高级混淆代码可能无法完全识别
- 大规模批量扫描需要足够内存 (建议≥512MB)

### 11.2 最佳实践
- 定期更新检测规则库 (建议每周)
- 结合人工审查使用 (高风险技能)
- 启用并行扫描提升性能 (批量场景)

### 11.3 故障排除
| 问题 | 解决方案 |
|------|---------|
| 扫描超时 | 增加 `--timeout` 参数 |
| 误报过多 | 更新白名单 `local.json` |
| 性能问题 | 启用并行扫描 `--workers 4` |

---

## 十二、相关资源

| 资源 | 链接 |
|------|------|
| Gitee 仓库 | https://gitee.com/caidongyun/agent-security-skill-scanner |
| 问题反馈 | Gitee Issues |
| 更新日志 | release/RELEASE.md |
| 安装指南 | install.sh |
| 功能文档 | docs/CAPABILITIES.md |

---

*文档生成：2026-03-14 | 版本：v2.0.1 | 状态：生产就绪*
