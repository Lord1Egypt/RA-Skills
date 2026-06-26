# AI Agent Security Scanner v6.2.0

企业级 AI Agent 安全扫描工具

---

## 📊 核心指标

| 指标 | v6.2.0 | 说明 |
|------|--------|------|
| 规则数 | 846 | 去重优化后实际生效 |
| 新增模块 | 7 | 风险分级/攻击链检测/熔断等 |
| 检测架构 | 三层 | 白名单 → 智能评分 → LLM |
| 扫描速度 | ~385 文件/秒 | 8 worker 并发 |

## 🎯 快速开始

### 安装
```bash
npm install -g @caidongyun/security-scanner
```

### 使用
```bash
# 扫描目录
agent-scanner /path/to/skills

# 并发扫描
agent-scanner /path/to/skills --workers 8

# 输出 JSON 报告
agent-scanner /path/to/skills --output json --output-file report.json
```

## 🔥 v6.2.0 新特性

### 1. 风险分级体系
- **Curl 风险分级**: 白名单域名 + 敏感参数检测
- **凭据窃取检测**: 攻击链识别 (诱导→混淆→外传)
- **5 级风险体系**: CRITICAL/HIGH/MEDIUM/LOW/INFO

### 2. 单 Skill 熔断机制
- 默认阈值: 500 文件/目录
- 防止恶意软件塞入大量文件拖慢扫描
- 参数: `--skill-max-files N`

### 3. 规则库优化
- 去重 88 条规则 (928 → 846)
- 标准化 419 条 severity 为大写
- 新增 6 条凭据攻击链规则 (CRED-CHAIN-001~006)

## 📦 发布文件清单 (20 个)

**核心模块 (8 个)**:
| 文件 | 功能 |
|------|------|
| `scanner.py` | 主扫描器 (三层架构) |
| `whitelist_filter.py` | 白名单过滤 |
| `config_detector.py` | 配置文件检测 |
| `context_aware_filter.py` | 上下文感知过滤 (新增) |
| `credential_theft_classifier.py` | 凭据窃取攻击链检测 (新增) |
| `curl_risk_classifier.py` | Curl 风险分级 (新增) |
| `risk_tier_classifier.py` | 5 级风险体系 (新增) |
| `security_tool_detector.py` | 安全工具识别 (新增) |

**规则库 (2 个)**:
- `rules/dist/all_rules.json` — 846 条规则
- `rules/rule_optimizer.py` — 规则优化器 (新增)

**引擎模块 (9 个)**:
- `src/encoding_utils.py`
- `src/engines/` (8 个检测引擎)

**入口 (3 个)**:
- `scan` — CLI 入口
- `index.js` — Node.js 入口
- `index.d.ts` — 类型定义

**文档/配置 (5 个)**:
- `package.json`
- `requirements.txt`
- `README.md`
- `RELEASE_NOTES.md`
- `SKILL.md`

## 🔧 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--workers` | 4 | 并发线程数 |
| `--skill-max-files` | 500 | 单 Skill 文件数熔断阈值 |
| `--timeout` | 3.0 | 单文件超时 (秒) |
| `--output` | text | 输出格式 (text/json) |
| `--output-file` | - | 输出文件路径 |

## 📝 许可证

MIT License

## 🔗 仓库

- **Gitee**: https://gitee.com/caidongyun/agent-security-skill-scanner-master
- **GitHub**: https://github.com/caidongyun/agent-security-skill-scanner
- **NPM**: @caidongyun/security-scanner@6.2.0
