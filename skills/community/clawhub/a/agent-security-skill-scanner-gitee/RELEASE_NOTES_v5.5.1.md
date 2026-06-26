# Agent Security Scanner v5.5.1 发布说明

**发布日期**: 2026-04-10  
**版本**: v5.5.1  
**类型**: 紧急修复 (Bug Fix)  
**依据**: ClawHub 官方安全扫描反馈

---

## 🔍 修复背景

ClawHub 官方安全扫描发现以下问题：

### 高优先级问题

1. **环境变量未声明** 🔴
   - SKILL.md 要求导出 LLM_API_KEY 等环境变量
   - 但技能元数据声明为 0 个必需环境变量
   - 风险：用户可能意外泄露敏感信息

2. **持久化行为未声明** 🔴
   - 指导用户启动后台守护进程
   - 未声明持久化权限和网络调用
   - 风险：技能可能在未告知用户的情况下持久运行

### 中优先级问题

3. **声明不一致** 🟡
   - SKILL.md 和 package.json 引用不同仓库 URL
   - 风险：用户可能混淆官方仓库

4. **安装路径不明确** 🟡
   - 多个安装路径和仓库 URL
   - 风险：用户可能安装到非官方版本

5. **Unicode 控制字符** 🟡
   - SKILL.md 包含 Unicode 控制字符
   - 风险：可能隐藏恶意指令

6. **网络调用未审查** 🟡
   - 代码可能发起网络调用，但未审查
   - 风险：可能泄露敏感数据

---

## ✅ 修复内容

### 1. 环境变量声明 ✅

**修复**: 在 SKILL.md 中声明所有环境变量

```yaml
必需环境变量：无
可选环境变量:
  - LLM_API_KEY (LLM API 密钥，建议隔离使用)
  - LLM_API_URL (LLM API 地址，优先本地模型)
  - FEISHU_WEBHOOK (飞书告警 Webhook)
  - ALERT_EMAIL (告警邮箱)
  - ENABLE_LLM_ANALYSIS (启用 LLM 分析，默认 false)
```

**安全提示**:
- ⚠️ 不要使用生产环境的 API 密钥
- ⚠️ 优先使用本地/离线模型
- ⚠️ 在隔离环境测试后再启用

### 2. 持久化行为声明 ✅

**修复**: 在 SKILL.md 中声明所有持久化行为

```yaml
后台守护进程:
  启用：可选 (默认 false)
  命令：nohup python3 lingshun_scanner_daemon.py &
  注意：可能发起网络调用

定时任务:
  启用：可选 (默认 false)
  命令：crontab -e 配置
  注意：定期执行扫描

网络调用:
  启用：可选 (默认 false)
  目的地：用户配置的 LLM_API_URL/FEISHU_WEBHOOK
  注意：所有网络调用都是可选的
```

### 3. 双仓库源声明 ✅

**修复**: 明确声明双仓库源策略

```yaml
主仓库 (Gitee):
  URL: https://gitee.com/caidongyun/agent-security-skill-scanner
  适用：中国大陆用户
  优势：访问速度快

镜像仓库 (GitHub):
  URL: https://github.com/caidongyun/agent-security-skill-scanner
  适用：海外用户
  优势：访问稳定

选择建议:
  - 中国大陆：优先 Gitee
  - 海外：优先 GitHub
  - 网络问题：切换仓库源
```

### 4. 统一仓库 URL ✅

**修复**: 统一所有文档中的仓库 URL

```
统一为:
  - Gitee: https://gitee.com/caidongyun/agent-security-skill-scanner
  - GitHub: https://github.com/caidongyun/agent-security-skill-scanner
```

### 5. 清理 Unicode 字符 ✅

**修复**: 清理 SKILL.md 中的 Unicode 控制字符

```bash
# 检查命令
od -c SKILL.md | grep '\\\\'

# 清理后
无隐藏字符 ✅
```

### 6. 网络调用审查 ✅

**修复**: 审查并声明所有网络调用

```yaml
网络调用点:
  - LLM API 调用 (可选，用户配置 URL)
  - 飞书 Webhook 通知 (可选，用户配置)
  - 邮件告警 (可选，用户配置)

审查结果:
  - 所有网络调用都是可选的 ✅
  - 目的地由用户配置 ✅
  - 代码可审查 ✅
```

---

## 📦 新增功能

### CLI 工具 (v5.5)

```bash
# 安装
chmod +x asc-scan
sudo ln -sf $(pwd)/asc-scan /usr/local/bin/asc-scan

# 使用
asc-scan agent-reach
asc-scan ./suspicious.py
asc-scan ./suspicious.py --verbose
```

### 智能识别

```yaml
支持的目标类型:
  - ClawHub 技能
  - 本地 Skill
  - 单文件 (.py/.js/.go 等)
  - 配置文件 (.yaml/.yml/.json)
  - NPM 包 (即将支持)
  - GitHub 仓库 (即将支持)
```

### 分层输出

```yaml
默认模式:
  - 风险等级 (🟢/🟡/🔴)
  - 关键问题 (最多 3 条)
  - 明确建议 (安装/谨慎/拒绝)

高级模式 (--verbose):
  - 完整扫描结果
  - 多扫描器对比
  - 详细修复建议

JSON 输出 (--json):
  - 结构化数据
  - 便于程序处理
```

---

## 📊 变更统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **修复问题** | 6 个 | ClawHub 官方发现 |
| **新增文件** | 5 个 | CLI/文档/规范 |
| **修改文件** | 1 个 | SKILL.md |
| **新增代码** | ~400 行 | asc-scan CLI |
| **新增文档** | ~15KB | 使用说明/规范 |

---

## ⚠️ 兼容性说明

### 向后兼容

```yaml
✅ Python API: 完全兼容
✅ 现有规则：完全兼容
✅ 现有测试：完全兼容
✅ 配置文件：完全兼容
```

### 新增依赖

```yaml
可选依赖:
  - 无 (CLI 工具无额外依赖)

必需依赖:
  - Python 3.6+
  - PyYAML
```

---

## 🧪 测试验证

### 已通过测试

```yaml
✅ CLI 版本检查
✅ CLI 帮助信息
✅ 扫描单文件
✅ 扫描 YAML 配置
✅ 良性文件识别
✅ 详细模式输出
✅ JSON 输出
```

### 待验证

```yaml
⏳ ClawHub 官方重新扫描
⏳ 安装流程测试
⏳ 用户反馈收集
```

---

## 📝 升级指南

### 从 v5.5 升级

```bash
# 拉取最新代码
git pull

# 验证版本
./asc-scan --version
# 应显示：v5.5.1
```

### 从旧版本升级

```bash
# 重新克隆
git clone https://gitee.com/caidongyun/agent-security-skill-scanner.git
cd agent-security-skill-scanner/release/v5.1.0

# 安装 CLI
chmod +x asc-scan
sudo ln -sf $(pwd)/asc-scan /usr/local/bin/asc-scan
```

---

## 🎯 下一步计划

### v5.6 (按需迭代)

```yaml
计划功能:
  - NPM 包扫描支持
  - GitHub 仓库扫描支持
  - 外部链接检测增强
  - 批量扫描优化

时间：2026-04 下旬
```

### v6.0 (重大更新)

```yaml
计划功能:
  - 运行时保护
  - 交互式模式
  - 企业功能
  - 其他 Skill 市场支持

时间：2026-05 下旬
```

---

## 📞 反馈渠道

### 报告问题

- Gitee Issues: https://gitee.com/caidongyun/agent-security-skill-scanner/issues
- GitHub Issues: https://github.com/caidongyun/agent-security-skill-scanner/issues

### 安全审计

如需第三方安全审计，请联系：agent-security@example.com

---

## 📋 检查清单

### 发布前检查

```yaml
✅ 所有环境变量已声明
✅ 所有持久化行为已声明
✅ 双仓库源已声明
✅ Unicode 字符已清理
✅ 网络调用已审查
✅ SKILL.md 已更新
✅ Release Notes 已创建
✅ CLI 工具已测试
```

### 发布后验证

```yaml
⏳ ClawHub 官方重新扫描
⏳ 用户反馈收集
⏳ 误报/漏报监控
⏳ 性能监控
```

---

**发布状态**: ✅ 准备就绪  
**ClawHub 扫描**: ⏳ 待重新验证  
**用户反馈**: ⏳ 待收集
