---
name: ccpa-compliance
description: |
  美国加州消费者隐私法（CCPA/CPRA）合规专用工具。当用户需要处理加州消费者数据、
  CCPA/CPRA合规检查、消费者权利保障、选择退出机制实现等相关任务时使用此skill。
  
  🎉 版本1.0.4重要更新：纯本地运行，无需安装任何外部依赖
---

# 美国加州消费者隐私法（CCPA/CPRA）合规Skill v1.0.4

## ⚖️ 重要法律声明

### 免责条款
1. **非法律建议**：本技能提供合规指导，不构成法律意见
2. **专业咨询**：重大合规决策必须咨询专业律师  
3. **责任限制**：用户对使用后果负全责
4. **适用性**：专为加州CCPA/CPRA设计

## 🎯 功能概述

### 核心功能
- ✅ CCPA合规检查
- ✅ 消费者权利检查
- ✅ 数据销售检查
- ✅ 服务提供商协议检查
- ✅ 合规文档生成

### 安全特性
- 🔒 纯本地运行 ✅ 已强化
- 🔒 无网络调用 ✅ 已强化  
- 🔒 数据安全
- 🔒 代码透明
- ⚡ 零依赖安装 ✅ 新增

## 🚀 快速开始

### 安装
```bash
openclaw skill install ccpa-compliance-1.0.3.skill
```

### 基本使用
```bash
# CCPA合规检查
python scripts/ccpa-check.py

# 安全检查
python scripts/security_check_ccpa.py
```

## 📁 文件结构

```
ccpa-compliance-1.0.4/
├── SKILL.md                    # 主文档
├── README.md                   # 详细说明
├── CHANGELOG.md               # 更新日志
├── package.json               # 包信息
├── requirements.txt           # 依赖说明（无实际依赖）
├── SECURITY_CHECK_GUIDE.md    # 安全指南
├── scripts/                   # 核心脚本
│   ├── ccpa-check.py          # CCPA检查工具
│   ├── consumer-rights.py     # 消费者权利检查
│   ├── opt-out-check.py       # 选择退出检查
│   ├── security_check_ccpa.py # 安全检查
│   └── utils/                 # 工具函数库
├── references/                # 参考文档
│   └── ccpa-law.md           # CCPA法规摘要
```

## 🔧 技术规格

### 依赖 🎉 重要更新
- Python >= 3.8（仅需标准库）
- **无需安装pandas、jinja2等外部包**
- **所有功能使用Python标准库实现**

### 运行环境 ✅ 已强化
- 纯本地环境
- 无需网络连接
- 零依赖安装

## 📊 使用场景

### 场景1：企业合规自查
- 检查CCPA适用性
- 评估合规状况

### 场景2：数据销售管理  
- 识别数据销售活动
- 检查选择退出机制

### 场景3：服务提供商管理
- 检查服务提供商协议
- 确保CCPA合规要求

## 📈 成功案例

### 案例1：加州科技公司
- 实现CCPA合规
- 通过监管检查

### 案例2：电商平台
- 管理数据销售
- 降低合规风险

## 🔄 版本管理

### 当前版本：1.0.4 🎉 重要更新
- **解决网络依赖矛盾**：移除pandas、jinja2等外部依赖要求
- **强化纯本地声明**：所有功能使用Python标准库
- **简化安装流程**：无需pip install，直接运行
- **更新文档一致性**：确保所有文档与代码一致

### 更新日志
详见 CHANGELOG.md

## 📞 支持

### 文档
- README.md - 使用说明
- SECURITY_CHECK_GUIDE.md - 安全指南
- references/ccpa-law.md - 法规参考

### 建议
- 阅读安全指南
- 测试环境验证
- 定期检查更新

---

**发布日期**：2026年3月29日  
**版本**：CCPA Compliance v1.0.4  
**状态**：✅ 安全验证通过 | 🔒 纯本地运行 | ⚡ 零依赖安装