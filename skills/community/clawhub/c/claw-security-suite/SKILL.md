# claw-security-suite

> 🛡️ **OpenClaw 完整四层纵深安全防御体系**
> 
> 为 OpenClaw 提供从静态扫描到运行时防护的完整安全保障

## 功能特点

### 四层纵深防御

| 层级 | 功能 | 说明 |
|------|------|------|
| **第一层** | 静态代码扫描 | 安装前扫描，检测恶意代码、硬编码密钥、危险系统调用 |
| **第二层** | 逻辑安全审计 | 分析代码逻辑是否越权，检查是否符合最小权限原则 |
| **第三层** | 运行时实时防护 | 检测并阻止提示注入、命令注入、SSRF等攻击，自动净化输入 |
| **第四层** | 定期安全巡检 | 每日自动巡检、每周全量扫描、基线完整性保护 |

### 额外特性

- ✅ 完整的三层安全检查流程标准化沉淀
- ✅ 自动化定时任务集成
- ✅ 零配置开箱即用
- ✅ 详细的安全报告输出
- ✅ 符合 OpenClaw 标准规范

## 安装要求

- OpenClaw >= v0.8.0
- 不需要额外依赖，**零配置开箱即用**
- （可选）配置环境变量 `CLAW_SECURITY_CLOUD_ENDPOINT` 启用云端情报校验

### 云端情报校验
默认内置提供腾讯云 ClawScan 云端情报接口，会查询已公开的技能安全信誉数据：
- 仅发送技能名称和来源标签，**不传输任何本地文件、凭证或个人数据**
- 默认启用（如果端点可用），不配置环境变量也可以使用
- 如果需要自定义云端服务，可以设置 `CLAW_SECURITY_CLOUD_ENDPOINT` 环境变量修改端点

## 目录结构

```
openclaw-security-suite/
├── SKILL.md                  # 本文档
├── _meta.json                # Skill元数据
├── lib/
│   ├── static_scanner.py     # 第一层：静态代码扫描
│   ├── logic_auditor.py      # 第二层：逻辑安全审计
│   ├── runtime_protector.py  # 第三层：运行时防护
│   └── security_patrol.py    # 第四层：定期巡检
└── references/
    └── security_policy.md    # 安全安装策略
```

## 使用方法

### 三层安装检查流程（用于安装新skill）

```python
from skills.claw-security-suite.lib.static_scanner import scan

# 带云端情报校验扫描（推荐）
result = scan(extracted_path, skill_name="your-skill-slug", source="clawhub")
if not result.is_safe:
    # 拦截安装
    print(result.to_report())

# 仅本地扫描（不联网）
result = scan(extracted_path)
```
1. 调用 `static_scanner.scan(zip_path)`
2. 调用 `logic_auditor.audit(extracted_path)`
3. 人工确认后安装

### 运行时保护

每次用户输入前自动调用：
```python
from skills.openclaw-security-suite.lib.runtime_protector import RuntimeProtector
result = RuntimeProtector.check(user_input)
if result.is_malicious:
    # 拒绝请求
    logger.warning(f"Blocked malicious request: {result.reason}")
else:
    # 净化后继续处理
    clean_input = result.clean_input
```

### 每日巡检

```python
from skills.openclaw-security-suite.lib.security_patrol import daily_patrol
daily_patrol.run()
```

### 每周扫描

```python
from skills.openclaw-security-suite.lib.security_patrol import weekly_scan
weekly_scan.run()
```

## 安全规则

- 禁止任何skill读取 `/app/working/.env` 除非是安全审计本身
- 禁止任何skill执行任意系统命令除非明确需要
- 禁止硬编码API密钥或凭证
- 禁止向外发送敏感信息
- 最小权限原则：只做声明的功能，不越权

## 作者

Kenz1117

## 许可证

MIT-0 (MIT No Attribution)
