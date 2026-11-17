---
name: agent-security-audit
description: AI Agent安全审计工具。扫描Skill/Agent代码中的敏感信息泄露、API密钥暴露、注入风险、权限问题、数据安全漏洞，AI智能分析给出修复建议。适用于开发者发布前安全自检、代码安全review。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - DEEPSEEK_API_KEY
---

# AI Agent 安全审计工具

AI Agent和Skill代码安全审计利器，一键扫描安全漏洞，AI智能分析给出可落地的修复方案。帮你在发布前堵住安全漏洞，避免密钥泄露、注入攻击、数据泄露等风险。

## When to Use

- Skill发布前做安全自检
- 第三方Skill安装前安全审查
- 代码仓库定期安全巡检
- AI Agent项目安全评估
- 排查代码中的敏感信息泄露
- 合规审计和安全加固

## Core Rules

1. 静态扫描 + AI深度分析双层检测机制
2. 支持单文件和整个目录递归扫描
3. 覆盖20+种常见安全漏洞类型
4. 按严重程度分级：严重/高危/中危/低危
5. 输出清晰的修复建议和代码示例
6. 支持JSON和文本两种报告格式

## Quick Start

```bash
# 扫描单个文件
python3 {baseDir}/scripts/audit.py path/to/your/skill.py

# 扫描整个Skill目录
python3 {baseDir}/scripts/audit.py path/to/skill/directory

# 只看严重和高危问题
python3 {baseDir}/scripts/audit.py ./ --severity high

# 输出JSON格式报告
python3 {baseDir}/scripts/audit.py ./ --format json -o report.json

# 跳过AI分析（快速扫描）
python3 {baseDir}/scripts/audit.py ./ --no-ai
```

## Input Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| target | string | 是 | 要扫描的文件或目录路径 |
| --no-ai | flag | 否 | 跳过AI深度分析，只做静态扫描 |
| --format | string | 否 | 输出格式：text/json，默认text |
| -o, --output | string | 否 | 输出报告文件路径 |
| --severity | string | 否 | 过滤级别：critical/high/medium/low/all，默认all |
| --api-key | string | 否 | DeepSeek API Key，也可通过环境变量设置 |
| --base-url | string | 否 | DeepSeek API Base URL |

## Detection Capabilities

### 🔴 敏感信息泄露检测
- API密钥（OpenAI/DeepSeek/AWS/GitHub等格式）
- 密码和凭证
- 私钥文件
- JWT令牌
- 数据库连接串
- 手机号、身份证号等个人信息

### 🟠 注入攻击检测
- 命令注入（os.system/subprocess shell=True）
- 代码注入（eval/exec）
- SQL注入（字符串拼接SQL）
- 路径遍历漏洞
- 不安全的反序列化（pickle）

### 🟡 权限与配置风险
- 硬编码管理员凭证
- 不安全的文件权限（777）
- 调试模式开启
- CORS通配符配置
- HTTPS证书校验关闭

### 🤖 AI Agent 特有风险
- 提示注入漏洞
- 工具滥用风险
- 数据泄露风险
- 越权操作风险
- 输出过滤缺失

## Output Format

扫描报告包含：

1. **风险概览** - 各严重级别问题数量统计
2. **总体风险评级** - 严重/高/中/低
3. **问题明细** - 按严重程度排序，包含文件、行号、代码、描述
4. **AI深度分析** - 智能风险评估、修复方案、加固建议

## Advanced Usage

### CI/CD 集成

```bash
# 在CI流水线中使用，发现严重问题时失败退出
python3 {baseDir}/scripts/audit.py ./src --severity critical
if [ $? -ne 0 ]; then
  echo "❌ 发现严重安全问题，构建终止！"
  exit 1
fi
```

### 定期安全巡检

```bash
# 生成每日安全报告
python3 {baseDir}/scripts/audit.py /path/to/project -o reports/audit_$(date +%Y%m%d).json
```

### 批量审查多个Skill

```bash
for skill in ./skills/*/; do
  name=$(basename "$skill")
  echo "扫描: $name"
  python3 {baseDir}/scripts/audit.py "$skill" --no-ai -o "reports/${name}_audit.txt"
done
```

## API Configuration

需要配置DeepSeek API密钥（用于AI深度分析）：
- 环境变量：`DEEPSEEK_API_KEY`
- 可选：`DEEPSEEK_BASE_URL`（自定义API地址）

静态扫描无需API Key，只有AI深度分析需要。

## References

- `references/owasp_top10.md` - OWASP Top 10安全风险
- `references/security_checklist.md` - AI Agent安全检查清单
- `references/fix_examples.md` - 常见漏洞修复示例代码

## Limitations

- 静态扫描基于正则匹配，可能存在误报和漏报
- AI分析仅供参考，关键问题建议人工复核
- 不支持二进制文件和编译后代码扫描
- 不支持动态运行时漏洞检测
