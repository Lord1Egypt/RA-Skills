## v0.1.4 (2026-10-02)

- 链接口径统一：_meta payment_link 改为官方详情页（购买动作在详情页完成），包内不出现支付直链

# Changelog

## v0.1.3 (2026-09-30)

- 核心原理重构为双路线结构（路线A 直连互@ / 路线B Gateway 路由），去除单路线断言
- 移除旧的转化说明页（转化内容移至落地页）
- 获取链接统一为官方 jinengpu 渠道，旧第三方铺子链接废弃
- 兼容清单统一为 8 框架（OpenClaw/AutoClaw/WorkBuddy/CherryStudio/DeepSeek Harness/Pi/Claude Code/Codex）
- 修正失真的 API 额度断言，改为准确的频控分级描述
- 版本号统一 0.1.x 单轨；README 与 SKILL.md 去重（README 收敛为摘要页）
- 新增 128 字符摘要与口语搜索关键词（Agent互相@ / agent to agent chat / bot relay 等）

## v0.1.2 (2026-09-30)

- SKILL.md 基础环境表补 WorkBuddy 兼容声明（三 skill 话术一致性）

## v0.1.1 (2026-09-29)

- Add MIT LICENSE to repository root
- Refresh README with install instructions (ClawHub search + git clone)
- Repository housekeeping; no changes to skill logic or scripts

AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_37fda03b731011f1b2f55254006c9bbf
    ReservedCode1: ptKI4uTV4VXl3W7ZV24wEWzlu6NeoRFLEAdhdH5XdKM/QVPeAxk2slWRDGpKgUul9mfg0Mb58sAk4Cb1j1aDEw1+zyn9l9lXrW33B8eyDrRcNbUPvqesY3wL2gIKQkzN3QNR2AxdPUNZCxnqb+MrmBYZwQC4NSalpGHP9yoGkWr8J8yDiI5of0v36lw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_37fda03b731011f1b2f55254006c9bbf
    ReservedCode2: ptKI4uTV4VXl3W7ZV24wEWzlu6NeoRFLEAdhdH5XdKM/QVPeAxk2slWRDGpKgUul9mfg0Mb58sAk4Cb1j1aDEw1+zyn9l9lXrW33B8eyDrRcNbUPvqesY3wL2gIKQkzN3QNR2AxdPUNZCxnqb+MrmBYZwQC4NSalpGHP9yoGkWr8J8yDiI5of0v36lw=
