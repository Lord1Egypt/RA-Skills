# Follow ScoutX 定时任务稳定性优化

## Tasks

- [x] 增加 OpenClaw cron 投递诊断，识别 `--channel last` 等不稳定配置。
- [x] 让 `install-openclaw-cron --apply` 默认阻止不稳定的模糊投递，除非显式放行。
- [x] 增加 `--main-session-system-event`，用于当前聊天稳定投递。
- [x] 增加 `--replace-existing`，按 name 查找旧 job 并通过 id 删除后重装。
- [x] 将 mixed 默认递送改为单 cron job，digest 内部分区排版。
- [x] 增加按 delivery channel 的消息长度预检测与拆分，优先覆盖飞书。
- [x] 在 dry run / JSON 输出中暴露稳定性诊断，便于安装前排查。
- [x] 当 `delivery.channel=feishu` 时，禁止 `--main-session-system-event`，避免把当前聊天回传链路误当成飞书投递链路。
- [x] 强化 `prepare-digest` 与 prompts 的逐条输出约束，禁止把后续内容折叠成“更多动态/更多精选内容”。
- [x] 让脚本在初始化/安装时自动同步 bundled prompts，本地旧版本先备份，自定义 prompt 默认保留。
- [x] 修正主题过滤匹配：支持 `AI/人工智能` 这类复合关键词，并避免 `ai` 命中 `Miami` / `Fairuz` 这类误判。
- [x] 收紧包含过滤范围：正向主题匹配只看标题与摘要正文，不再因为 ScoutX 条目的 tag/频道元信息带 `AI` 就误放行。
- [x] 将验收规范写入 skill：验收时只认 `preview --json` / `deliver --json` 原始字段，禁止输出 `AI相关: ✅/⚠️/❌` 这类二次判断。
- [x] 增加 `preview --json` / `deliver --json` 的 `group_counts` 与 `errors` 字段，避免真实执行阶段静默降级后还要靠上层猜测。
- [x] 默认允许 partial digest，但必须显式返回 `status=partial`、`failed_source_types` 和 `errors`，避免把抓取故障伪装成过滤结果。
- [x] 修正中文投递链路：`zh-CN` / `bilingual` 且包含一手信息源时，OpenClaw 改走 `prepare-digest`，避免一手信息源保持英文原文。
- [x] 强化中文摘要约束：`zh-CN` 时，一手信息源的标题和摘要必须中文化，不能只翻译 section label。
- [x] 同步更新 `SKILL.md`、`README.md`、`AGENT.md`、`CLAUDE.md` 的安装建议。
- [x] 运行基础验证命令。

## Review

- 默认 `in_chat` 会解析成 `channel=last`，现在 dry run 会标记 `stable=false`，直接 apply 会被阻止。
- 显式 `--delivery-channel feishu --delivery-target ou_xxx` 会通过稳定性诊断，并保留 `--session isolated` 作为干净执行环境。
- 当前聊天使用 `--main-session-system-event` 生成 `--session main --system-event`，不再硬编码 target，也不依赖 `last`。
- OpenClaw cron 不按 name 更新；`--replace-existing` 会用 `list --json` 找到生成 job name 对应的 id，再调用 `cron rm <id>`。
- mixed 模式默认不再拆成两个 cron job，而是保留一个 job，在 digest 内部分一手信息源 / ScoutX 优质媒体两个 section。
- `deliver --json` 会提前按 channel 限制拆成多条消息块；cron prompt 改成逐块发送，飞书默认使用更保守的长度阈值。
- 飞书投递路径已经收口为显式 `announce + channel + to`；`main-session-system-event` 只保留给当前聊天，避免依赖 OpenClaw 主会话转发链路。
- 即使上层走 `prepare-digest` + LLM remix，prompt 和 output contract 现在也明确要求逐条编号输出，不能再把第 4 条以后合并成“更多…”。
- 本地 prompt 不再需要手动覆盖；脚本会自动同步内置 prompt 更新，并给旧文件留备份，避免线上环境长期吃旧模板。
- 主题过滤原来是纯子串匹配：`AI/人工智能` 会被当成一个整体导致漏匹配，单独的 `ai` 又会误伤 `Miami`、`Fairuz` 等词。现在改成“分隔符拆词 + AI 主题别名 + 短英文词边界匹配”。
- ScoutX 媒体条目之前还可能因为上游 tag/频道标签命中 `AI` 而被误放行；现在正向过滤只检查标题与摘要正文，排除词仍看全量文本。
- 验收链路之前会把原始结果改写成 `AI相关: ✅/⚠️/❌` 这类主观标签，容易误报；现在 skill 里明确要求验收只引用原始 JSON 字段。
- `deliver --json` 之前没有 `group_counts` 和 `errors`，导致“真实执行”阶段如果某个 feed 拉取失败或被降级，上层只能猜。现在直接把这些字段暴露出来。
- 之前只要某个选中 feed 抓取失败，脚本会用剩余 feed 继续出摘要，却没有明确标出 partial，造成 `first_party=0 / scoutx=10` 这类假象。现在继续允许降级，但会显式返回 `status=partial`、失败源和错误详情。
- `language=zh-CN` 之前只影响标题和标签，不影响一手信息源正文语言。现在 OpenClaw 生成 cron 命令时，会在中文/双语且启用一手源时切到 `prepare-digest`，让上层按 `config.language` 生成中文摘要。
- 仅仅把中文场景切到 `prepare-digest` 还不够；prompt、output contract 和 OpenClaw payload 也要明确要求“一手信息源标题 + 摘要中文化”，否则模型仍可能直接保留英文原文。
- `--allow-channel-last` 只作为已经验证平台能力后的逃生口，不再是默认路径。

# README 结构补强

## Tasks

- [x] 阅读当前 `README.md`、`SKILL.md`、`service.json` 和脚本入口，确认文档边界。
- [x] 参考 `alchaincyf/nuwa-skill` README 的结构优势，提炼适合 Follow ScoutX 的表达顺序。
- [x] 重写 README 顶部定位、效果示例、安装路径、定时投递和“背后的判断”段落。
- [x] 补充 CLI 能力、本地状态文件、仓库结构与服务提供方说明。

## Review

- 新版 README 从“是什么”改成“为什么要用 + 装完能得到什么”，更接近安装型 skill 的用户决策路径。
- 保留了当前项目已有的运维细节，但把其位置后移，避免用户一上来就陷入底层实现。
- 借鉴了 `nuwa-skill` 的叙事方式，但没有照搬“蒸馏人物”的故事，而是改成更贴合本项目的信息获取判断。
- 后续又补上了 `背后的故事` 和 `关于作者` 两节；前者用于承接项目动机，后者先保留占位结构，方便补真实信息。
- 顶部命名已切换为 `谛听.skill`，并补了 slogan；`Follow ScoutX` 暂时保留为仓库名与英文识别名，减少和现有目录、脚本、安装路径的割裂。
