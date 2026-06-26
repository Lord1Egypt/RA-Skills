# AI Relay Open-Source Readiness Discussion

**Date**: 2026-05-23  
**Discussion ID**: `rt_xxxxxxxx`  
**WebViewer**: `http://0.0.0.0:8206/r/Am7_gvvXRBehEmhEIWv9JjvWd4g7`  
**Conclusion doc**: `/Users/parsifal/Repo/Service/ai-relay/docs/roundtable-open-source-readiness.md`

## Configuration

```python
roundtable_init(
    topic="AI Relay 开源准备评估：哪些模块适合开源？",
    context="AI Relay 是一个 OpenAI 兼容的 API 代理...",
    participants=[
        {"profile": "bingge", "role": "产品总监", "perspective": "产品价值与开源策略", "display_name": "饼哥"},
        {"profile": "xiaosu", "role": "设计师", "perspective": "用户体验与品牌一致性", "display_name": "像素姐"},
        {"profile": "mafei", "role": "开发者", "perspective": "技术可行性与维护成本", "display_name": "码飞"},
    ],
    max_rounds=3,
    notifications={...}  # standard OPC config
)
```

## Workflow Used

**Hybrid approach** (delegate_task for reasoning + Direct Core API for recording):
1. Coordinator opened Round 0 via Direct Core API
2. Each participant: `delegate_task` → extract summary → `core.speak()` to record
3. Coordinator summarized between rounds via `core.speak(participant="coordinator")`
4. Notifications sent to company group after each round via `send_message`

## Key Results

### Round 1 — 适合开源的模块
- **饼哥**: 六个适配器、Dashboard、文档站、CLI、TypeScript SDK
- **像素姐**: 类型系统设计、VS Code 插件、主题定制、飞书文档
- **码飞**: NPM 一键部署、VS Code 插件、Dashboard、类 Vercel 自部署

### Round 2 — 开源风险
- **码飞**: 安全漏洞、500+处公司IP硬编码、攻击面暴露（priority #1）
- **饼哥**: 代码质量（1948 warnings）、团队维护能力、竞品先发优势
- **像素姐**: 内部功能泄露、Design System 缺失、品牌一致性

### Round 3 — 时间线与分工（达成共识 5/29 发布 v0.1.0）
- **码飞**: 安全扫描+License+CI/CD+Docker+构建打包 (2.5天)
- **饼哥**: README+Quick Start+审核规范+文档模板 (1.5天)
- **像素姐**: Logo+GitHub Banner+OG Image+截图 (2天)
- Code Freeze: 5/28, 发布: 5/29

## Post-Discussion Actions

After the discussion concluded, two follow-up actions were executed:

### 1. Kanban Task Dispatch
4 tasks created and dispatched via three-step pattern (create → notify-subscribe → feishu-send).
All completed within the same day. See `references/post-discussion-kanban-dispatch.md`.

### 2. Security Cleanup (Git History)
The discussion identified leaked secrets in Git history. Cleanup steps:
1. `git-filter-repo` to remove `.env.production` and `.env.local.bak` from ALL commits
2. Force push: `git push origin main --force`
3. Key rotation: update relay API keys in `~/.hermes/config.yaml`, restart gateway
4. Verify leaked tokens are revoked: `curl -H "Authorization: Bearer $TOKEN" https://api.vercel.com/v2/user` (expect 403)

## Lessons Learned

1. **Round tracking bug**: All speeches showed `round: 0` or `round: 1` regardless of actual round
2. **delegate_task 100% failure**: 6/6 sub-agents failed to call `roundtable_speak`
3. **WebViewer URL not auto-shared**: Direct Core API doesn't trigger browser open — must manually share URL and run `open`
4. **Notifications worked**: All 6 speeches synced to company group in real-time
5. **Conclusion doc must be written BEFORE `roundtable_end`**: `end()` only accepts brief text, not full documents
6. **Post-discussion dispatch**: Roundtable conclusions should be immediately converted to kanban tasks with clear ownership and deadlines
