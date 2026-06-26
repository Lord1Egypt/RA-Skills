# ASF V4.0 Skill - 手动发布指南

**原因**: clawhub CLI 登录状态可能未正确传递

---

## 方法 1: 使用完整路径发布

```bash
# 1. 确认登录
clawhub whoami

# 2. 如果显示未登录，重新登录
clawhub login

# 3. 使用完整路径发布
clawhub publish /root/.openclaw/workspace-main/skills/asf-v4 \
  --name "ASF V4.0 工业化增强" \
  --version "1.0.0" \
  --tags "governance,optimization,security,economics,veto,ownership,kpi,budget" \
  --changelog "初始发布 - 8 Tools + 6 Commands + Memory/Agent/Security 集成 + 性能基准 + 安全审计 100%"
```

---

## 方法 2: 使用 slug 发布

```bash
clawhub publish asf-v4 \
  --slug "asf-v4" \
  --name "ASF V4.0 工业化增强" \
  --version "1.0.0" \
  --tags "governance,optimization,security,economics,veto,ownership,kpi,budget"
```

---

## 方法 3: Web 界面发布

### 步骤 1: 访问 ClawHub

打开浏览器访问：https://clawhub.ai

### 步骤 2: 登录

使用你的账号登录。

### 步骤 3: 创建新技能

1. 点击 "Create Skill" 或 "发布技能"
2. 填写技能信息:
   - **Name**: ASF V4.0 工业化增强
   - **Slug**: asf-v4
   - **Version**: 1.0.0
   - **Description**: ASF V4.0 工业化增强模块 - 治理门禁 + 成本模型 + 安全优化
   - **Tags**: governance, optimization, security, economics, veto, ownership, kpi, budget
   - **Category**: governance
   - **License**: MIT

### 步骤 4: 上传文件

打包技能文件:

```bash
cd /root/.openclaw/workspace-main/skills
tar -czf asf-v4-1.0.0.tar.gz asf-v4/
```

上传 `asf-v4-1.0.0.tar.gz` 到 ClawHub。

### 步骤 5: 填写技能介绍

复制以下内容到技能介绍框:

```markdown
# ASF V4.0 工业化增强

ASF V4.0 工业化增强模块，提供企业级治理门禁、成本模型优化和安全在线优化能力。

## 核心功能

### 🛡️ 治理门禁
- 硬/软否决权执行
- Ownership 证明生成
- Veto 规则检查

### 📊 经济学优化
- 经济学评分计算
- 接口预算计算
- 返工风险预测

### 🔥 热契约分析
- 契约耦合度检测
- 角色数量收敛
- 冲突解决

### 🔄 安全优化
- 旋钮限制
- 自动回滚
- 冷却机制

## 可用工具 (8 个)

1. **veto-check** - 硬/软否决权检查
2. **ownership-proof** - Ownership 证明生成
3. **economics-score** - 经济学评分计算
4. **interface-budget** - 接口预算计算
5. **rework-risk** - 返工风险预测
6. **hot-contract** - 热契约分析
7. **conflict-resolve** - 冲突解决
8. **safe-optimize** - 安全在线优化

## 可用命令 (6 个)

- `asf:status` - 检查技能状态
- `asf:veto` - 运行否决检查
- `asf:proof` - 生成所有权证明
- `asf:score` - 计算经济学评分
- `asf:risk` - 预测返工风险
- `asf:hot-contracts` - 分析热契约

## 性能指标

- 总吞吐量：>40,000 ops/sec
- P95 延迟：<30ms
- 内存占用：<5MB
- CPU 影响：<2%

## 安全审计

- 审计分数：100%
- 检查项目：23 项全部通过

## 安装

```bash
clawhub install asf-v4
```

## 启用

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "enabled": ["asf-v4"]
  }
}
```

## 许可证

MIT License
```

### 步骤 6: 提交审核

点击 "Publish" 或 "提交" 按钮。

---

## 方法 4: 使用 API 发布

```bash
# 获取 API Token (从 ClawHub 设置页面)
export CLAWHUB_TOKEN="your-api-token"

# 使用 curl 发布
curl -X POST https://clawhub.ai/api/skills \
  -H "Authorization: Bearer $CLAWHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ASF V4.0 工业化增强",
    "slug": "asf-v4",
    "version": "1.0.0",
    "description": "ASF V4.0 工业化增强模块 - 治理门禁 + 成本模型 + 安全优化",
    "tags": ["governance", "optimization", "security", "economics", "veto", "ownership", "kpi", "budget"],
    "category": "governance",
    "license": "MIT",
    "repository": "https://github.com/openclaw/openclaw",
    "main": "index.ts"
  }'
```

---

## 验证发布

### 方法 1: CLI 验证

```bash
clawhub search asf-v4
```

### 方法 2: Web 验证

访问：https://clawhub.ai/skills/asf-v4

### 方法 3: 安装测试

```bash
clawhub install asf-v4
```

---

## 故障排除

### 问题 1: "Not logged in"

**解决**:
```bash
# 清除旧登录
clawhub logout

# 重新登录
clawhub login

# 验证登录
clawhub whoami
```

### 问题 2: "Path must be a folder"

**解决**:
```bash
# 使用绝对路径
clawhub publish /root/.openclaw/workspace-main/skills/asf-v4
```

### 问题 3: "Skill already exists"

**解决**:
```bash
# 更新版本
# 修改 package.json 和 skill.yaml 中的 version 为 1.0.1
# 然后发布
clawhub publish asf-v4 --version "1.0.1" --changelog "更新说明"
```

### 问题 4: 发布超时

**解决**:
```bash
# 压缩文件后上传
cd /root/.openclaw/workspace-main/skills
tar -czf asf-v4.tar.gz asf-v4/
# 然后通过 Web 界面上传
```

---

## 发布后检查清单

- [ ] 技能页面可访问
- [ ] 技能介绍正确显示
- [ ] Tools 列表完整 (8 个)
- [ ] Commands 列表完整 (6 个)
- [ ] 性能指标显示
- [ ] 安全审计分数显示
- [ ] 安装命令可用
- [ ] 文档链接正确

---

## 分享技能

发布成功后，分享链接:

```
https://clawhub.ai/skills/asf-v4
```

社交媒体文案:

```
🎉 发布了新技能 "ASF V4.0 工业化增强" 到 @ClawHub!

包含 8 个 Tools 和 6 个 Commands:
🛡️ 治理门禁 (veto-check, ownership-proof)
📊 经济学优化 (economics-score, interface-budget)
🔥 热契约分析 (hot-contract)
🔄 安全优化 (safe-optimize)

性能：>40,000 ops/sec
安全：100% 审计通过

立即安装：clawhub install asf-v4

#OpenClaw #ClawHub #ASF #Governance #Optimization
```

---

**选择最适合你的发布方法执行发布！**
