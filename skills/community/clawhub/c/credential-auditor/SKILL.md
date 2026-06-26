---
name: credential_auditor
description: 自动化凭证安全审计工具，支持设备默认密码匹配、密码字典生成和多协议暴力破解测试
metadata:
  openclaw:
    os: ["darwin", "linux", "windows"]
    requires:
      bins: ["python3"]
      config: []
---

# Credential Auditor - 凭证安全审计技能

## 技能概述

Credential Auditor 是为安全工程师设计的自动化凭证安全审计技能，帮助你在使用 OpenClaw 进行安全测试时，智能化地进行密码安全评估和漏洞检测。

## 核心能力

### 1. 设备默认密码智能匹配
- 自动识别设备类型（路由器、摄像头、服务器、网络设备）
- 匹配 20+ 主流品牌的默认凭证数据库
- 支持 500+ 设备默认密码快速查询
- 一键生成设备安全评估报告

### 2. 智能密码字典生成
- **规则驱动生成**：根据目标信息（公司名、年份、地点）智能生成定制密码
- **字典变异增强**：对现有字典进行 Leet Speak、大小写、数字后缀等变异
- **社会工程学分析**：基于个人信息（姓名、生日、公司）生成针对性密码
- **暴力枚举支持**：按字符集和长度范围生成全组合密码

### 3. 多协议安全测试
- 支持 SSH、RDP、FTP、HTTP/HTTPS、Telnet、SMB 等协议
- 多线程并发测试，提高审计效率
- 自动保存测试进度和结果
- 支持使用默认密码库进行快速测试

### 4. 专业工具集成
- 无缝集成 Hydra、Medusa、Ncrack 等专业工具
- 自动检测工具安装状态
- 统一命令接口，简化操作流程
- 结果自动解析和格式化

## 使用场景

### 场景1：设备安全基线检查
```
用户："帮我检查这个路由器的默认密码安全性，IP是192.168.1.1"
→ 自动识别设备类型
→ 查询默认密码库
→ 尝试默认凭证登录测试
→ 生成安全评估报告
```

### 场景2：企业密码策略审计
```
用户："为TechCorp公司生成一份密码安全测试字典"
→ 收集企业信息（公司名、年份、地点）
→ 应用密码生成规则
→ 生成定制化测试字典
→ 提供密码强度分析
```

### 场景3：渗透测试辅助
```
用户："测试目标服务器192.168.1.100的SSH密码强度"
→ 检查目标可达性
→ 选择合适的测试字典
→ 执行多线程密码测试
→ 生成测试报告和建议
```

## 工作流程

### 自动化决策逻辑

当用户提出安全测试需求时，技能会自动：

1. **识别测试类型**
   - 提到设备类型 → 使用默认密码匹配
   - 需要生成密码 → 使用字典生成器
   - 指定协议和目标 → 使用暴力破解工具
   - 需要高效测试 → 集成专业工具

2. **智能参数配置**
   - 自动选择合适的字典文件
   - 优化线程数和超时设置
   - 根据协议类型调整测试策略

3. **结果分析报告**
   - 统计测试成功率和失败率
   - 识别弱密码模式
   - 提供安全加固建议

## 使用示例

### 查询设备默认密码
```bash
# 列出所有支持的设备类型
python scripts/device_matcher.py --list-devices

# 查询路由器默认密码
python scripts/device_matcher.py --device-type router --brand Cisco

# 查询IP摄像头默认密码
python scripts/device_matcher.py --device-type camera --brand Hikvision
```

### 生成密码字典
```bash
# 基于规则生成
python scripts/wordlist_generator.py --rule-based \
  --target-info "company:TechCorp,year:2024,location:Beijing" \
  --output custom_wordlist.txt

# 社会工程学生成
python scripts/wordlist_generator.py --social-eng \
  --name "John" --birthday "1990-01-15" \
  --company "TechCorp" \
  --output social_wordlist.txt
```

### 执行安全测试
```bash
# SSH密码测试
python scripts/brute_force.py --protocol ssh \
  --target 192.168.1.100 --port 22 \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt

# 使用默认密码测试
python scripts/brute_force.py --protocol ssh \
  --target 192.168.1.1 \
  --use-default-passwords \
  --device-type router
```

### 工具集成
```bash
# 检查工具安装状态
python scripts/tool_integration.py --check-tools

# 使用Hydra进行测试
python scripts/tool_integration.py --tool hydra \
  --protocol ssh --target 192.168.1.100 \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt
```

## 数据资源

### 设备密码数据库
- `references/device_passwords.json` - 500+ 设备默认凭证
- 涵盖路由器、摄像头、服务器、网络设备等
- 支持 Cisco、Hikvision、Dahua、TP-Link 等主流品牌

### 密码生成规则
- `references/password_rules.json` - 智能密码生成规则
- 支持常见模式、变异规则、社会工程学规则
- 可自定义扩展规则库

### 协议配置
- `references/protocol_configs.json` - 协议测试参数配置
- 预设超时、线程数、重试策略
- 支持自定义协议参数

### 字典资源
- `references/usernames.txt` - 常用用户名字典
- `references/passlist.txt` - 通用密码字典

## 安全与合规

### ⚠️ 重要警告
- **仅用于授权测试**：此技能仅供合法的安全测试、教育和研究使用
- **遵守法律法规**：未经授权的密码破解行为是违法的
- **道德责任**：确保有明确的授权和合法的测试范围
- **数据保护**：不得在未经授权的情况下访问、修改或泄露他人数据

### 最佳实践
1. 获取书面授权后再进行测试
2. 在隔离环境中进行安全测试
3. 详细记录测试过程和结果
4. 及时报告发现的安全漏洞
5. 遵循负责任的漏洞披露原则

## 技能配置

### 环境要求
- Python 3.10+
- 必需依赖：paramiko, requests, colorama
- 可选工具：Hydra, Medusa, Ncrack

### 安装依赖
```bash
pip install paramiko requests colorama
```

### 安装可选工具
```bash
# macOS
brew install hydra medusa ncrack

# Ubuntu/Debian
sudo apt-get install hydra medusa ncrack

# Windows
# 从官方网站下载对应工具
```

## 输出格式

### 测试报告示例
```
========================================
凭证安全审计报告
========================================
目标: 192.168.1.100
协议: SSH
测试时间: 2026-03-30 11:00:00

测试统计:
- 总尝试次数: 1000
- 成功次数: 2
- 失败次数: 998
- 测试耗时: 120.5秒

发现的有效凭证:
1. admin:admin123
2. root:password

安全建议:
- 立即修改默认密码
- 启用账户锁定策略
- 实施密码复杂度要求
- 启用双因素认证
========================================
```

## 技能优势

### 智能化
- 自动识别测试场景
- 智能选择测试策略
- 自动优化测试参数

### 易用性
- 简单直观的命令接口
- 详细的帮助文档
- 丰富的使用示例

### 专业性
- 符合安全测试标准
- 完整的审计报告
- 专业的安全建议

### 可扩展
- 支持自定义规则
- 可添加新设备类型
- 支持新协议扩展

## 常见问题

### Q: 如何添加新的设备默认密码？
A: 编辑 `references/device_passwords.json`，按照现有格式添加新设备。

### Q: 如何自定义密码生成规则？
A: 编辑 `references/password_rules.json`，添加自定义规则和模式。

### Q: 测试速度太慢怎么办？
A: 增加线程数（`--threads`），或使用 Hydra 等专业工具。

### Q: 如何保护测试数据安全？
A: 所有测试数据仅保存在本地，建议测试完成后及时删除敏感数据。

## 更新日志

### v1.0.0 (2026-03-30)
- 初始版本发布
- 支持设备默认密码匹配
- 支持智能密码字典生成
- 支持多协议安全测试
- 集成专业安全工具

## 技术支持

- 技能文档：README.md
- 问题反馈：GitHub Issues
- 数据来源：https://github.com/jeanphorn/wordlist

---

**使用此技能即表示你同意遵守所有适用的法律法规，并仅在授权范围内进行安全测试。**
