# ASF V4.0 Skill - 生产环境部署指南

**版本**: 1.0.0  
**日期**: 2026-03-29  
**状态**: ✅ 本地部署完成

---

## 📦 部署状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **openclaw.json** | ✅ 已配置 | 移除了无效的插件配置 |
| **Gateway** | ✅ 运行中 | ws://127.0.0.1:18789 |
| **技能文件** | ✅ 已就绪 | `/root/.openclaw/workspace-main/skills/asf-v4/` |
| **ClawHub 发布** | ⏸️ 暂停 | 发布包已准备 (`/tmp/asf-v4-1.0.0.tar.gz`) |

---

## 🔧 本地使用方法

### 方法 1: 通过 tools.alsoAllow 启用

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "tools": {
    "profile": "coding",
    "alsoAllow": [
      "coding_agent",
      "session_logs",
      "asf-v4"
    ]
  }
}
```

然后重启 Gateway:

```bash
openclaw gateway restart
```

### 方法 2: 作为本地技能加载

在 agent 会话中直接导入:

```typescript
import { asf_v4 } from '/root/.openclaw/workspace-main/skills/asf-v4/index.ts';

// 使用工具
const result = await asf_v4.tools['veto-check']({ changes, approvals });
```

### 方法 3: 创建本地技能链接

```bash
# 创建技能符号链接到 OpenClaw 技能目录
ln -s /root/.openclaw/workspace-main/skills/asf-v4 ~/.openclaw/skills/asf-v4

# 在 openclaw.json 中配置
{
  "skills": {
    "local": ["asf-v4"]
  }
}
```

---

## 🚀 使用示例

### 示例 1: Veto 检查

```typescript
const vetoResult = await tools['asf-v4:veto-check']({
  changes: [
    { resourceType: 'contract', resourcePath: '/orders', action: 'update' }
  ],
  approvals: [
    { authority: 'architect', scope: 'contract:OpenAPI:*', status: 'approved' }
  ]
});

console.log(vetoResult.passed); // true/false
```

### 示例 2: Ownership 证明

```typescript
const proof = await tools['asf-v4:ownership-proof']({
  resources: [
    { type: 'contract', path: '/orders#POST', format: 'openapi' }
  ],
  roles: [
    { id: 'backend-team' },
    { id: 'architect' }
  ]
});

console.log(proof.valid); // true/false
```

### 示例 3: 经济学评分

```typescript
const score = await tools['asf-v4:economics-score']({
  assignment: { taskToRole: { 'task-1': 'role-1', 'task-2': 'role-2' } },
  dag: { tasks: [...], edges: [...] },
  roles: [
    { id: 'role-1', economics: { costPerTask: 1.0 } }
  ]
});

console.log(score.totalScore); // -1 to 1
```

---

## 📊 性能基准

运行基准测试:

```bash
cd /root/.openclaw/workspace-main/skills/asf-v4
npx ts-node benchmarks/performance-benchmark.ts
```

**预期结果**:
- Veto Enforcement: >6,000 ops/sec
- Ownership Proof: >3,500 ops/sec
- Economics Score: >2,200 ops/sec
- Memory Write: >12,500 ops/sec
- Memory Read: >8,300 ops/sec
- Agent Status: >11,000 ops/sec

---

## 🔒 安全审计

运行安全审计:

```bash
cd /root/.openclaw/workspace-main/skills/asf-v4
bash scripts/security-audit.sh
```

**预期结果**: 100% 通过 (23/23 项)

---

## 📋 配置说明

### vetoRules 配置

```yaml
# config/asf-v4.config.yaml
veto:
  mode: default  # default | strict | custom
  rules:
    - authority: architect
      mode: hard
      scopeSelector: 'contract:OpenAPI:*'
```

### economicsWeights 配置

```yaml
economics:
  scoreWeights:
    interfaceCost: -0.30
    bottleneck: -0.20
    skillMatch: 0.20
    parallelismGain: 0.15
    reworkRisk: -0.15
```

### safeOptimizer 配置

```yaml
optimizer:
  enabled: true
  cooldownMs: 1800000  # 30 分钟
  failureThreshold: 2
```

---

## 🐛 故障排除

### 问题 1: 工具无法访问

**解决**:
```bash
# 检查 Gateway 状态
openclaw status

# 重启 Gateway
openclaw gateway restart

# 检查技能文件
ls -la /root/.openclaw/workspace-main/skills/asf-v4/
```

### 问题 2: 性能低下

**解决**:
```bash
# 运行基准测试
npx ts-node benchmarks/performance-benchmark.ts

# 检查内存使用
cat /proc/$(pgrep -f openclaw)/status | grep VmRSS
```

### 问题 3: 安全审计失败

**解决**:
```bash
# 运行安全审计
bash scripts/security-audit.sh

# 查看失败项
cat scripts/security-audit.sh | grep -A5 "FAIL"
```

---

## 📦 ClawHub 发布 (可选)

如需发布到 ClawHub:

1. 访问：https://clawhub.ai/create
2. 上传：`/tmp/asf-v4-1.0.0.tar.gz`
3. 填写技能信息 (见 `QUICK-WEB-PUBLISH.md`)
4. 点击发布

---

## 📚 相关文档

- `README.md` - 使用指南
- `PHASE-{1,2,3}-COMPLETE.md` - 实现报告
- `QUICK-WEB-PUBLISH.md` - Web 发布指南
- `skills/asf-v4/` - 技能源代码

---

**本地部署完成** · 可以开始使用 asf-v4 技能
