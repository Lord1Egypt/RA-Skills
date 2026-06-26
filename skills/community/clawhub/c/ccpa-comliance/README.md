# CCPA Compliance v1.0.4

## 🇺🇸 加州消费者隐私法（CCPA/CPRA）合规技能

**CCPA Compliance v1.0.4** 是为加州市场设计的**纯本地运行**CCPA/CPRA合规解决方案。

---

## 🌟 核心价值

### 🎯 一站式CCPA合规解决方案
为在加州处理消费者数据的企业和组织提供全面的CCPA/CPRA合规支持。

### 🔒 纯本地运行，数据安全 ✅ 已强化
所有数据处理在本地完成，**无需网络连接**，不收集、存储或传输用户数据到外部服务器。

### 🛡️ 企业级安全标准
通过全面安全检查，符合CCPA/CPRA数据保护要求和企业安全标准。

### ⚡ 零依赖安装
**无需安装任何外部依赖**，直接使用Python标准库运行。

---

## ✨ 主要功能

### 1. CCPA合规检查
- ✅ 企业适用性检查
- ✅ 消费者权利保障检查
- ✅ 数据销售机制检查

### 2. 消费者权利管理
- 知情权实现检查
- 删除权实现检查
- 选择退出权实现检查

### 3. 数据销售管理
- 识别数据销售活动
- "请勿销售"机制验证
- 选择退出流程检查

---

## 🚀 快速开始

### 🎉 重要更新：v1.0.4版本为纯本地运行版本
**无需安装任何外部依赖**，所有功能使用Python标准库实现。

### 运行要求
- Python 3.8+（仅需标准库）
- **无需安装pandas、jinja2等外部包**
- **无需网络连接**

### 使用步骤（纯本地，零安装）

```bash
# 方法1：直接运行CCPA检查
python scripts/ccpa-check.py --scenario "消费者数据分析"

# 方法2：先运行安全检查
python scripts/security_check_ccpa.py
python scripts/ccpa-check.py

# 方法3：运行消费者权利检查
python scripts/consumer-rights.py

# 方法4：运行选择退出机制检查
python scripts/opt-out-check.py
```

### 🔧 高级用法
```bash
# 交互式模式
python scripts/ccpa-check.py --interactive

# 指定输出格式（JSON）
python scripts/ccpa-check.py --scenario "数据销售" --format json

# 检查特定消费者权利
python scripts/consumer-rights.py --right delete
```

---

## ⚠️ 重要法律声明

### 免责条款

**使用本技能前请仔细阅读以下条款**：

1. **非法律建议**：本技能提供的信息仅供参考，不构成法律建议
2. **专业性咨询**：重大CCPA/CPRA合规决策必须咨询专业律师
3. **责任限制**：用户对使用本技能的所有决策和后果负全责
4. **适用性限制**：专为加州CCPA/CPRA设计

### 使用限制

**允许用途**:
- ✅ 作为CCPA合规自查的辅助工具
- ✅ 用于生成初步合规文档模板

**禁止用途**:
- ❌ 替代专业法律咨询
- ❌ 作为法律证据使用

---

## 📄 许可证

MIT License

---

**CCPA Compliance v1.0.3**  
**专为加州市场设计**  
**安全、可靠、合规**
