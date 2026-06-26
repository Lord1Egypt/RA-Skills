# Credential Auditor - OpenClaw 凭证安全审计技能

<div align="center">

![Credential Auditor](https://img.shields.io/badge/Credential-Auditor-blue?style=for-the-badge)

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green?style=flat-square)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**专为安全工程师设计的 OpenClaw 凭证安全审计技能**

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [配置说明](#配置说明)

</div>

---

## 📖 简介

**Credential Auditor** 是一个专为安全工程师设计的 OpenClaw 技能，提供智能化的凭证安全审计能力。通过集成设备默认密码数据库、智能密码字典生成和多协议安全测试，帮助安全工程师高效完成授权范围内的安全评估工作。

### 🎯 设计目标

- **智能化**：自动识别测试场景，智能选择测试策略
- **易用性**：简单直观的命令接口，无需复杂配置
- **专业性**：符合安全测试标准，提供专业审计报告
- **合规性**：强调授权使用，内置安全警告和最佳实践

## ✨ 功能特性

### 🔐 设备默认密码智能匹配
- 支持 **4 大类设备类型**：路由器、摄像头、服务器、网络设备
- 涵盖 **20+ 主流品牌**：Cisco、Hikvision、Dahua、TP-Link 等
- 提供 **500+ 设备默认凭证**快速查询
- 一键生成设备安全评估报告

### 📝 智能密码字典生成
- **规则驱动生成**：根据目标信息智能生成定制密码
- **字典变异增强**：Leet Speak、大小写、数字后缀等变异
- **社会工程学分析**：基于个人信息生成针对性密码
- **暴力枚举支持**：按字符集和长度生成全组合

### 💥 多协议安全测试
- 支持 **SSH、RDP、FTP、HTTP/HTTPS、Telnet、SMB** 等协议
- 多线程并发测试，提高审计效率
- 自动保存测试进度和结果
- 支持使用默认密码库快速测试

### 🛠️ 专业工具集成
- 无缝集成 **Hydra、Medusa、Ncrack** 等专业工具
- 自动检测工具安装状态
- 统一命令接口，简化操作流程
- 结果自动解析和格式化

## 🚀 快速开始

### 前置要求

- OpenClaw 已安装并正常运行
- Python 3.7 或更高版本
- 必需依赖：`paramiko`, `requests`, `colorama`

### 安装步骤

#### 方法1：通过 ClawHub 安装（推荐）

```bash
# 在 ClawHub 中搜索并安装
openclaw skill install credential_auditor

#### 方法2：手动安装

1. **下载技能**
   ```bash
   # 克隆或下载此技能到本地
   git clone https://github.com/jeanphorn/credential_auditor.git
   cd credential_auditor
   ```

2. **安装到 OpenClaw**
   ```bash
   # 复制技能到 OpenClaw 工作区技能目录
   mkdir -p ~/.openclaw/workspace/skills/
   cp -r . ~/.openclaw/workspace/skills/credential_auditor/
   ```

3. **安装 Python 依赖**
   ```bash
   pip install paramiko requests colorama
   ```

4. **验证安装**
   ```bash
   # 重启 OpenClaw 或重新加载技能
   openclaw agent --message "列出所有支持的设备类型"
   ```


```

### 安装可选工具

为了获得更好的性能，建议安装专业安全工具：

```bash
# macOS
brew install hydra medusa ncrack

# Ubuntu/Debian
sudo apt-get install hydra medusa ncrack

# Windows
# 从官方网站下载对应工具并添加到 PATH
```

## 📚 使用指南

### 基础用法

#### 1. 查询设备默认密码

**通过 OpenClaw 对话**：
```
用户："帮我查询 Cisco 路由器的默认密码"
AI：自动调用 credential_auditor 技能
    → 查询设备密码数据库
    → 返回 Cisco 路由器默认凭证列表
```

**命令行方式**：
```bash
# 列出所有支持的设备
python scripts/device_matcher.py --list-devices

# 查询特定设备
python scripts/device_matcher.py --device-type router --brand Cisco

# 输出到文件
python scripts/device_matcher.py --device-type camera --brand Hikvision \
  --output hikvision_passwords.json
```

#### 2. 生成密码字典

**通过 OpenClaw 对话**：
```
用户："为 TechCorp 公司生成一份密码测试字典"
AI：自动调用技能
    → 收集企业信息
    → 应用密码生成规则
    → 生成定制化字典
```

**命令行方式**：
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

# 基于字典变异
python scripts/wordlist_generator.py --dictionary-based \
  --base-dict references/passlist.txt --mutations \
  --output mutated_wordlist.txt
```

#### 3. 执行安全测试

**通过 OpenClaw 对话**：
```
用户："测试目标服务器 192.168.1.100 的 SSH 密码强度"
AI：自动调用技能
    → 检查目标可达性
    → 选择合适的测试字典
    → 执行多线程密码测试
    → 生成测试报告
```

**命令行方式**：
```bash
# SSH 密码测试
python scripts/brute_force.py --protocol ssh \
  --target 192.168.1.100 --port 22 \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt \
  --threads 5

# 使用默认密码测试
python scripts/brute_force.py --protocol ssh \
  --target 192.168.1.1 \
  --use-default-passwords \
  --device-type router

# HTTP 表单测试
python scripts/brute_force.py --protocol http \
  --target http://example.com/login \
  --method POST \
  --user-field username \
  --pass-field password \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt
```

#### 4. 使用专业工具

```bash
# 检查工具安装状态
python scripts/tool_integration.py --check-tools

# 使用 Hydra
python scripts/tool_integration.py --tool hydra \
  --protocol ssh --target 192.168.1.100 --port 22 \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt \
  --threads 10

# 使用 Medusa
python scripts/tool_integration.py --tool medusa \
  --protocol rdp --target 192.168.1.100 --port 3389 \
  --userlist references/usernames.txt \
  --passlist references/passlist.txt
```

### 高级用法

#### 自定义密码规则

编辑 `references/password_rules.json`：

```json
{
  "common_patterns": [
    "{company}{year}",
    "{company}@{year}",
    "{name}{birthday}"
  ],
  "mutations": {
    "capitalize": true,
    "add_numbers": ["", "123", "1234", "2024"],
    "add_symbols": ["", "!", "@", "#"],
    "leet_speak": {
      "a": ["a", "@", "4"],
      "s": ["s", "$", "5"]
    }
  }
}
```

#### 添加新设备密码

编辑 `references/device_passwords.json`：

```json
{
  "routers": {
    "NewBrand": [
      {"model": "ModelName", "username": "admin", "password": "password"}
    ]
  }
}
```

#### 自定义协议配置

编辑 `references/protocol_configs.json`：

```json
{
  "ssh": {
    "default_port": 22,
    "timeout": 10,
    "max_threads": 5,
    "retry_attempts": 3
  }
}
```

## 📁 项目结构

```
credential_auditor/
├── SKILL.md                          # OpenClaw 技能定义文件
├── README.md                         # 技能说明文档
├── LICENSE                           # MIT 许可证
│
├── scripts/                          # 核心脚本工具
│   ├── device_matcher.py            # 设备密码匹配器
│   ├── wordlist_generator.py        # 密码字典生成器
│   ├── brute_force.py               # 多协议测试工具
│   ├── tool_integration.py          # 第三方工具集成
│   └── utils.py                     # 通用工具函数
│
└── references/                       # 参考数据资源
    ├── device_passwords.json        # 设备密码数据库
    ├── password_rules.json          # 密码生成规则
    ├── protocol_configs.json        # 协议配置参数
    ├── usernames.txt                # 用户名字典
    └── passlist.txt                 # 密码字典
```

## ⚙️ 配置说明

### 环境变量

无需配置环境变量，所有配置通过配置文件管理。

### 配置文件

#### device_passwords.json
设备默认密码数据库，格式：
```json
{
  "设备类型": {
    "品牌": [
      {"model": "型号", "username": "用户名", "password": "密码"}
    ]
  }
}
```

#### password_rules.json
密码生成规则配置，包含：
- `common_patterns`: 常见密码模式
- `mutations`: 变异规则
- `leet_speak`: Leet Speak 映射

#### protocol_configs.json
协议测试参数配置，包含：
- `default_port`: 默认端口
- `timeout`: 超时时间
- `max_threads`: 最大线程数
- `retry_attempts`: 重试次数

## 🎯 使用场景

### 场景1：设备安全基线检查

**目标**：检查网络设备的默认密码安全性

**流程**：
1. 识别设备类型和品牌
2. 查询默认密码数据库
3. 尝试默认凭证登录测试
4. 生成安全评估报告

**示例**：
```
用户："检查公司内网 192.168.1.1 这台路由器的默认密码安全性"
```

### 场景2：企业密码策略审计

**目标**：评估企业密码策略的强度

**流程**：
1. 收集企业信息（公司名、年份、地点等）
2. 生成定制化密码字典
3. 测试内部服务密码强度
4. 提供密码策略改进建议

**示例**：
```
用户："为 TechCorp 公司生成一份密码安全测试字典，公司在北京，成立于 2020 年"
```

### 场景3：渗透测试辅助

**目标**：辅助渗透测试人员进行密码安全测试

**流程**：
1. 信息收集和目标识别
2. 生成针对性密码字典
3. 执行多协议密码测试
4. 生成测试报告和建议

**示例**：
```
用户："测试目标 192.168.1.100 的 SSH 服务，使用社会工程学字典"
```

## ⚠️ 安全与合规

### 重要警告

**此技能仅供授权的安全测试、教育和研究使用！**

- ✅ 仅在授权范围内使用
- ✅ 遵守所有适用的法律法规
- ✅ 获得书面授权后再进行测试
- ✅ 保护测试过程中获取的数据
- ❌ 未经授权的密码破解是违法的
- ❌ 不得用于非法目的

### 最佳实践

1. **获取授权**：确保有明确的书面授权
2. **隔离环境**：在隔离环境中进行测试
3. **详细记录**：记录所有测试过程和结果
4. **及时报告**：发现漏洞及时报告给相关负责人
5. **负责任披露**：遵循负责任的漏洞披露原则

### 法律声明

使用此技能即表示你同意：
- 仅在授权范围内使用
- 遵守所有适用的法律法规
- 承担使用此技能的全部责任
- 不将此技能用于非法目的

## 📊 性能优化

### 提高测试速度

1. **增加线程数**：
   ```bash
   python scripts/brute_force.py --threads 10
   ```

2. **使用专业工具**：
   ```bash
   # Hydra 通常比纯 Python 实现快 5-10 倍
   python scripts/tool_integration.py --tool hydra
   ```

3. **优化字典大小**：
   - 使用针对性字典而非通用字典
   - 去重和排序字典文件

### 资源使用

- **内存**：大字典可能占用较多内存，建议分批处理
- **CPU**：多线程测试会提高 CPU 使用率
- **网络**：大量并发连接可能触发目标防护机制

## 🔧 故障排除

### 常见问题

#### Q: 技能未加载
**A**: 检查技能是否正确安装到 `~/.openclaw/workspace/skills/credential_auditor/`

#### Q: Python 模块导入失败
**A**: 安装必需依赖 `pip install paramiko requests colorama`

#### Q: 工具未找到
**A**: 确保工具已安装并在 PATH 中，或使用纯 Python 实现

#### Q: 测试速度太慢
**A**: 增加线程数或使用 Hydra 等专业工具

#### Q: 连接超时
**A**: 检查目标是否可达，增加超时时间 `--timeout 20`

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0.0 (2026-03-30)
- ✨ 初始版本发布
- ✅ 支持设备默认密码匹配
- ✅ 支持智能密码字典生成
- ✅ 支持多协议安全测试
- ✅ 集成专业安全工具
- 📝 完整的文档和示例

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 [jeanphorn/wordlist](https://github.com/jeanphorn/wordlist) 提供的密码字典资源
- 感谢 OpenClaw 团队提供的优秀平台
- 感谢所有贡献者和安全研究人员的努力

## 📞 支持

- **文档**：查看 README.md 和 SKILL.md
- **问题**：GitHub Issues
- **数据来源**：https://github.com/jeanphorn/wordlist

---

<div align="center">

**Made with ❤️ for Security Engineers**

**⚠️ 始终在授权范围内使用，遵守法律法规！**

</div>
