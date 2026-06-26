# 安全工具说明

本目录包含 07-互联网访问技能的所有安全工具。

## 🔐 工具列表

### 1. encrypt_cookies.py - Cookie 加密工具

**功能**：使用 AES-256-GCM 加密存储敏感 Cookie

**使用方法**：
```bash
# 导入并加密 Cookie
python encrypt_cookies.py import --file cookies.json

# 解密查看
python encrypt_cookies.py decrypt --password "your-password"

# 轮换密钥（建议每月）
python encrypt_cookies.py rotate

# 检查 Cookie 年龄
python encrypt_cookies.py check
```

**安全特性**：
- AES-256-GCM 加密
- PBKDF2 密钥派生
- 密码或密钥文件双重支持
- 自动清理明文文件

---

### 2. audit_monitor.py - 审计监控工具

**功能**：实时监控、日志分析、威胁检测

**使用方法**：
```bash
# 生成安全报告
python audit_monitor.py report --days 7

# 实时监控（检测异常）
python audit_monitor.py monitor

# 扫描历史日志
python audit_monitor.py scan
```

**监控内容**：
- 异常高频请求
- 认证失败检测
- 数据大量下载
- SQL 注入、XSS 等攻击模式

---

### 3. dependency_check.py - 依赖安全检查

**功能**：检查已知漏洞、版本过时、供应链安全

**使用方法**：
```bash
# 完整检查
python dependency_check.py full

# 建立依赖基线
python dependency_check.py baseline

# 对比变更
python dependency_check.py diff
```

**检查项**：
- 已知 CVE 漏洞
- 过时的依赖包
- 可疑的包名
- 依赖树深度

---

## 🛡️ 安全最佳实践

### 日常维护

```bash
# 每周运行
python audit_monitor.py report --days 7

# 每月运行
python encrypt_cookies.py rotate
python dependency_check.py full
```

### 应急响应

**发现 Cookie 泄露**：
```bash
# 1. 撤销平台授权
# 2. 删除本地 Cookie
rm ~/.config/agent-reach/cookies.enc

# 3. 重新获取并加密
python encrypt_cookies.py import --file new_cookies.json
```

**发现依赖漏洞**：
```bash
# 1. 更新受影响的包
pip install --upgrade <package-name>

# 2. 重新检查
python dependency_check.py full

# 3. 重建基线
python dependency_check.py baseline
```

---

## 📋 安全检查清单

### ✅ 安装后
- [ ] Cookie 已加密
- [ ] 文件权限正确 (600)
- [ ] 依赖基线已建立
- [ ] 初始审计报告已生成

### ✅ 日常
- [ ] 每周查看审计日志
- [ ] 检查依赖更新
- [ ] 监控异常活动

### ✅ 每月
- [ ] 轮换 Cookie 密钥
- [ ] 更新依赖包
- [ ] 重新建立基线
- [ ] 检查文件权限

---

## 🔒 文件权限

确保敏感文件权限为 600：
```bash
chmod 600 ~/.config/agent-reach/cookies.enc
chmod 600 ~/.config/agent-reach/.key
chmod 600 ~/.config/agent-reach/security_config.yaml
```

---

## 📊 安全报告示例

```
============================================================
Agent Reach 安全审计报告
时间范围: 最近 7 天
============================================================

📊 总体统计
  总事件数: 1523
  失败请求: 3

🚨 事件按严重程度分布
  WARNING:    12 ████
  INFO:     1508 ████████████████████████████████████

🌐 平台访问统计
  github          :  234 次
  youtube         :   45 次
  twitter         :   12 次

💡 安全建议
  - 定期轮换 Cookie（建议每月一次）
  - 使用 agent-check 进行日常检查

============================================================
```

---

**版本**: 1.0
**更新**: 2025-02-27
