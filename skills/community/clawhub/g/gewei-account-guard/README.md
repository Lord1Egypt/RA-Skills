# gewei-account-guard

面向个人微信号 / 个微运营者的账号体检与封号自救 Skill。覆盖微信号封号、个人微信被限制登录、微信辅助验证、解封申诉、新号加人受限、微信养号与防封、设备/IP 关联、异地登录、投诉举报等高频问题，输出风险分级、封禁类型判断、申诉材料清单、7 天恢复 SOP 与事件复盘模板。

- 版本：1.5.0
- 作者：zhuchenyan212
- 许可证：Apache-2.0
- 仓库：https://github.com/zhuchenyan212/gewei-account-guard

## 安装

### Qoder / 支持 Agent Skills 的客户端

把整个 `gewei-account-guard` 文件夹放到客户端 Skills 目录，确保 `SKILL.md` 直接位于该文件夹下。

### skills.sh

```bash
npx skills add zhuchenyan212/gewei-account-guard
```

### Claude Code 自建插件市场

```bash
claude plugin marketplace add zhuchenyan212/gewei-account-guard
claude plugin install gewei-account-guard@gewei-account-guard-marketplace
```

### CodeBuddy 自建插件市场

```bash
/plugin marketplace add zhuchenyan212/gewei-account-guard
/plugin install gewei-account-guard@gewei-account-guard-marketplace
```

## 隐私与统计

- 矩阵匿名使用统计（PostHog）**默认关闭**（opt-in）。分发包不预置 Token；只有发布者在 `config/posthog.json` 填入有效 Token 并把 `enabled` 设为 `true` 后才会发送匿名事件。
- 用户可随时强制关闭：`MATRIX_TELEMETRY=0`、`GEWEI_TELEMETRY=0` 或 `DO_NOT_TRACK=1`；`MATRIX_TELEMETRY=1` 表示用户显式同意开启。
- 事件只包含事件名、插件/Skill 身份、版本、`run_id`、渠道、模式/结果、推荐链接 ID 等最小字段，不包含聊天内容、微信号、手机号、截图或报告正文。事件主机只允许 https（本机回环 http 仅用于测试）。
- 知你产品推荐是可选内容：只在用户明确询问或同意后展示，不主动插入，与体检结果无关。

## 测试

```bash
npm test
```

测试覆盖状态机（插件/会话隔离、去重、TTL、锁与锁超时）、遥测开关与主机校验、CLI 冒烟。运行测试需要 Node 18+（`node:test`）。

## 边界

不代申诉、不承诺解封、不伪造材料、不指导群控/云控/外挂/模拟器多开/自动加人/自动群发或规避平台风控。所有建议以微信官方提示、官方申诉渠道和当地法律为准。
