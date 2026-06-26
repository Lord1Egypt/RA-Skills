# Multi-Agent Collaboration Protocol

## Hierarchy Pattern

```
Adam (人类决策者)
  │
  ├── 小咪 (System Brain / 指挥官)
  │     │
  │     ├── sains-crm (商机管理)
  │     ├── Jarvis Invest (投资交易)
  │     ├── marketing-growth (获客增长)
  │     ├── personal-cfo (财务分析)
  │     ├── 休眠修炼 (技术进化)
  │     ├── phd-revision (论文修改)
  │     ├── family-guardian (家庭守护)
  │     └── agent-army (多Agent调度)
  │
  └── main (通用备用)
```

## Collaboration Rules

### 1. 单一沟通口
- Adam 只与小咪对话
- 所有 Agent 通过小咪接收指令和上报结果
- 小咪是唯一的"对外接口"

### 2. 升级机制
```
Agent 发现问题 → 评估影响级别
  ├── 低影响 → 自行处理，事后报告
  ├── 中影响 → 上报小咪，小咪决定是否转 Adam
  └── 高影响 → 立即上报小咪 → 通知 Adam
```

### 3. 冲突解决
- 同级别 Agent 之间冲突 → 小咪仲裁
- 跨域资源竞争 → 小咪协调
- 任务优先级冲突 → Adam 拍板

### 4. SOUL.md 协作字段
每个 SOUL.md 必须包含：

```markdown
## 与上级的协作协议
- 直接上级：小咪
- 日常汇报：每5分钟/每小时/完成后
- 升级触发：[什么情况下需要上报]
- 决策权限：[可以自主决定的范围]
```

## Validation Checklist

Run `soul-check.py` to verify:
- [ ] All agents have SOUL.md at root level
- [ ] SOUL.md contains all required sections
- [ ] Collaboration protocol defined
- [ ] Personality assigned (not "generic")
- [ ] Escalation rules clear
