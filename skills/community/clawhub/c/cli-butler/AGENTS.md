# cli-butler — 项目协作规范

- 需求真相源：`docs/REQUIREMENTS.md`；渠道模型口径：`docs/provenance.md`。改需求先改文档再动代码。
- 协作语言：简体中文；`SKILL.md` 与 README 面向开源，用英文。
- 技术约束：POSIX bash、零第三方依赖；单渠道探测失败不阻塞整体；危险操作默认 dry-run。
- 安全红线（不可协商）：渠道管理的二进制禁止直接 `rm`；launchd 停用须挪 plist；app 内嵌软链只备份挪链。
- 每次改动后跑 `tests/run.sh`；shellcheck 在 CI 跑，本地装了就一并跑。
- 提交信息用英文祈使句；一个功能一个 commit。
- 开源发布前：npm / GitHub / skills.sh 名字查重。

## 多 Agent 交接
- 开始时读取 HANDOVER.md 与对应任务记录，沿用原任务编号，登记负责人、目标和状态。
- 有进展、阻塞或用户新决定时更新任务记录；结束前补齐产物、证据、未完成项和下一步，在 HANDOVER.md 同步摘要和入口。
- 自动记录只反映会话状态。Agent 核对并填写业务结果；最终回复附记录路径，无法写入时标记「待同步」。
