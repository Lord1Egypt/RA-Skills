# 🎉 Credential Auditor - OpenClaw 技能！

## 📦 项目信息

**技能名称**: `credential_auditor` (凭证审计器)  
**项目位置**: `~/Desktop/credential_auditor/`  
**创建时间**: 2026-03-30  
**状态**: ✅ 已完成并验证通过

## 🎯 技能定位

**Credential Auditor** 是一个专为安全工程师设计的 OpenClaw 技能，提供智能化的凭证安全审计能力。

### 目标用户
- 安全工程师
- 渗透测试人员
- 安全审计人员
- 安全研究人员

### 核心价值
- **智能化**：自动识别测试场景，智能选择测试策略
- **易用性**：简单直观的命令接口，无需复杂配置
- **专业性**：符合安全测试标准，提供专业审计报告
- **合规性**：强调授权使用，内置安全警告和最佳实践

## ✨ 核心功能

### 1. 设备默认密码智能匹配 🔐
- 支持 **4 大类设备类型**：路由器、摄像头、服务器、网络设备
- 涵盖 **20+ 主流品牌**
- 提供 **500+ 设备默认凭证**
- 一键生成设备安全评估报告

### 2. 智能密码字典生成 📝
- 规则驱动生成
- 字典变异增强
- 社会工程学分析
- 暴力枚举支持

### 3. 多协议安全测试 💥
- 支持 SSH、RDP、FTP、HTTP/HTTPS、Telnet、SMB
- 多线程并发测试
- 自动保存测试进度和结果

### 4. 专业工具集成 🛠️
- 无缝集成 Hydra、Medusa、Ncrack
- 自动检测工具安装状态
- 统一命令接口

## 📁 项目结构

```
credential_auditor/
├── SKILL.md                          # ✅ OpenClaw 技能定义文件（符合官方格式）
├── README.md                         # ✅ 完整使用指南
├── INSTALL.md                        # ✅ 安装说明
├── LICENSE                           # ✅ MIT 许可证
│
├── scripts/                          # ✅ 核心脚本工具
│   ├── device_matcher.py            # 设备密码匹配器
│   ├── wordlist_generator.py        # 密码字典生成器
│   ├── brute_force.py               # 多协议测试工具
│   └── tool_integration.py          # 第三方工具集成
│
└── references/                       # ✅ 参考数据资源
    ├── device_passwords.json        # 设备密码数据库
    ├── password_rules.json          # 密码生成规则
    ├── protocol_configs.json        # 协议配置参数
    ├── usernames.txt                # 用户名字典
    └── passlist.txt                 # 密码字典
```

## ✅ 符合 OpenClaw 格式要求

### YAML Frontmatter 格式 ✅
```yaml
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
```

### 技能目录结构 ✅
- ✅ 包含必需的 `SKILL.md` 文件
- ✅ YAML frontmatter 格式正确
- ✅ Markdown 正文包含详细指令
- ✅ 支持多操作系统
- ✅ 定义了必需的二进制文件

### 功能验证 ✅
- ✅ 设备匹配器测试通过
- ✅ 密码生成器测试通过
- ✅ 所有脚本可正常运行

## 🚀 安装使用

### 快速安装

```bash
# 1. 进入项目目录

# 2. 安装到 OpenClaw
mkdir -p ~/.openclaw/workspace/skills/
cp -r . ~/.openclaw/workspace/skills/credential_auditor/

# 3. 安装 Python 依赖
pip install paramiko requests colorama

# 4. 重启 OpenClaw 并测试
```

### 使用示例

#### 通过 OpenClaw 对话
```
用户："帮我查询 Cisco 路由器的默认密码"
AI：自动调用 credential_auditor 技能
    → 查询设备密码数据库
    → 返回 Cisco 路由器默认凭证列表
```

#### 命令行方式
```bash
# 查询设备默认密码
python scripts/device_matcher.py --device-type router --brand Cisco

# 生成密码字典
python scripts/wordlist_generator.py --rule-based \
  --target-info "company:TechCorp,year:2024"
```

## 📊 项目统计

- **总文件数**: 12 个核心文件
- **代码行数**: 1000+
- **文档字数**: 5000+
- **支持协议**: 6 种
- **设备类型**: 4 大类
- **品牌数量**: 20+
- **默认密码**: 500+

## ⚠️ 安全与合规

### 重要警告
- ✅ 仅在授权范围内使用
- ✅ 遵守所有法律法规
- ✅ 获得书面授权后再测试
- ✅ 保护测试过程中获取的数据

### 法律声明
此技能仅供合法的安全测试、教育和研究使用。未经授权的密码破解行为是违法的。

## 📖 文档导航

### 用户文档
- **README.md** - 完整使用指南
- **INSTALL.md** - 详细安装说明
- **SKILL.md** - 技能详细说明

### 开发文档
- **LICENSE** - MIT 许可证
- **references/** - 配置文件和数据

## 🎓 学习路径

### 初级：基础使用
1. 阅读 `INSTALL.md` 安装技能
2. 阅读 `README.md` 了解功能
3. 尝试查询设备默认密码
4. 尝试生成密码字典

### 中级：实际应用
1. 为目标设备生成定制密码字典
2. 执行授权的安全测试
3. 分析测试结果
4. 编写安全报告

### 高级：工具集成
1. 安装 Hydra、Medusa 等专业工具
2. 使用工具集成功能
3. 自定义密码规则
4. 扩展设备数据库

```

## 📞 技术支持

- **文档**: README.md, INSTALL.md, SKILL.md
- **问题反馈**: GitHub Issues
- **数据来源**: https://github.com/jeanphorn/wordlist

## 🎉 项目亮点

### 1. 符合 OpenClaw 官方标准
- ✅ 标准的 YAML frontmatter
- ✅ 规范的目录结构
- ✅ 完整的技能说明

### 2. 专业的安全工具
- ✅ 面向安全工程师设计
- ✅ 强调授权使用和合规性
- ✅ 提供专业的审计报告

### 3. 易于使用
- ✅ 简单的安装流程
- ✅ 详细的使用文档
- ✅ 丰富的使用示例

### 4. 可扩展
- ✅ 支持自定义规则
- ✅ 可添加新设备类型
- ✅ 支持新协议扩展

---

## ✅ 验证清单

- [x] 技能名称符合 OpenClaw 规范（snake_case）
- [x] SKILL.md 包含正确的 YAML frontmatter
- [x] 所有必需字段都已填写
- [x] 技能功能已测试通过
- [x] 文档完整且清晰
- [x] 包含安全警告和法律声明
- [x] 提供安装和使用说明
- [x] 代码可正常运行

---


**⚠️ 记住：始终在授权范围内使用，遵守法律法规！**
