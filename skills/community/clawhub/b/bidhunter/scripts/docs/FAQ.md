# BidHunter 常见问题（FAQ）

> 检索方式：`python3 faq.py <关键词>` 或 `python3 bidhunter.py faq <关键词>`。
> 每个问题含关键词标签，命中任一即返回。

## Q: 为什么判读结果里很多"需确认"？
关键词: 需确认 不确定 没匹配 漏标
A: "需确认"表示标题未命中任何主体能力词。常见原因：
1. 你的 `qual_rules.json` 的 `entities` 能力词没覆盖该标的范围 → 按营业执照补充能力词。
2. 标题里能力词被边界感知规则挡掉（如"电气设备"里的"电气"因前有 CJK 字被挡）→ 属于正常防误匹配，可在标题里出现能力词词首时正常命中。
3. 实在吃不准就人工看一眼，并在报告底部用"反馈 #序号 准确/有误 原因"告诉我们，帮你优化规则。

## Q: 推送失败了怎么办 / 怎么查推送记录？
关键词: 推送 失败 收不到 钉钉 企微 邮件 历史
A: 先运行诊断 `python3 doctor.py` 看 E005。查历史与重试：
- `python3 push_manager.py history` 看 30 天推送记录
- `python3 push_manager.py stats` 看统计
- `python3 push_manager.py retry-failed` 重发失败项
- `python3 push_manager.py health-check` 看连续失败告警
首次配置通道请用 `python3 config_wizard.py`，未通过连通性测试不会写入。

## Q: 怎么配置资质规则（不会写代码）？
关键词: 配置 规则 资质 能力词 不会 新手 怎么填
A: 两种方式：
1. 规则编辑器（推荐，零代码）：`python3 bidhunter.py rules edit` → 浏览器打开 http://localhost:8080 图形化编辑并保存。
2. 行业模板起步：复制 `scripts/samples/` 下对应行业的模板，按营业执照改 `entities`/`red_alerts`。
改完跑 `python3 qual_check.py --validate-rules qual_rules.json` 做健康检查。

## Q: 支持哪些招投标平台？怎么加新平台？
关键词: 平台 平台列表 新增平台 采集 数据源 支持
A: 当前支持已在 `references/platforms.md` 列明的央企/公共资源平台（如 cnooc/sinopec/petrochina/cnpc 等）。新增平台：参考 `references/platforms.md` 的"自定义数据源"章节，把平台采集参数加入 `bid_monitor.sh` 的适配器；也可在 ClawHub/SkillHub 反馈你需要的平台，我们按优先级扩展（v1.5 已增补平台覆盖）。

## Q: 报告里出现的"评分"是什么意思？
关键词: 评分 分数 匹配度 强烈推荐 建议跟 优先级
A: v1.5 新增资质匹配度评分（0-100），帮你在可投标里排优先级：
- 能力词命中数（≤40）+ 重点地区（≤20）+ 行业偏好（≤15）+ 预算区间（≤15）
- 等级：强烈推荐(≥80) / 建议跟(≥55) / 可投一般 / 需确认 / 不可投
评分仅供参考，最终仍以人工研判为准。

## Q: 投标日历/开标倒计时怎么用？
关键词: 日历 倒计时 开标 截止 提醒 漏跟
A: `python3 bidhunter.py calendar` 或 `calendar.py <qual文件> --days 30` 看未来窗口内的开标/截止日。加 `--remind` 可对临近截止（默认 48h 内）的标自动推送提醒（需先配置推送通道）。
注意：多数平台 list 接口无截止日字段，日历日期从标题解析，未含明确日期的标会归入"待核实截止日"。

## Q: AI 速读/投标建议要额外付费吗？
关键词: AI 速读 投标建议 费用 花钱 MiniMax API Key 配置
A: 不额外购买服务器。AI 速读/风险识别/投标建议调用你自己的 MiniMax API（doubao/MiniMax 等），仅消耗你的 API 余额。配置：`~/.config/bidhunter/ai.json` 写入 `{"api_key":"...","group_id":"..."}`。未配置时 AI 功能自动跳过，不影响基础采集研判。

## Q: 多维筛选（金额/地区/行业）怎么用？
关键词: 筛选 金额 预算 地区 行业 订阅 过滤
A: 在 `qual_rules.json` 设置 `region_priority.high`（重点地区）、`industry_categories`+`industry_priority`（行业）、`budget_priority`（预算区间）。运行时可加过滤：
`python3 filter_multi.py qual_xxx.jsonl --min 500000 --max 20000000 --region 天津 --industry 智能设备`

## Q: SkillHub / ClawHub 上怎么搜不到或装不上？
关键词: SkillHub ClawHub 安装 搜不到 面板 技能市场 上架
A: 两端都要发布才覆盖。ClawHub 为 openclaw 命令行生态（自助发布免审核）；SkillHub 是 WorkBuddy 技能面板数据源（需官方审核，审核通过后点"上架"才在面板可见）。若面板搜不到，通常是 SkillHub 还在审核中或未点"上架"。

## Q: 我的数据会外传吗？
关键词: 隐私 数据 外传 安全 保密
A: 采集仅取公开招投标公告；资质规则、推送配置存在你本机（`~/.config/bidhunter/`、skill 内 `bid_cache/`）。AI 速读会把公告/招标文件文本发往你配置的 MiniMax API 做解析，不会进入任何 BidHunter 云端（我们无云端）。不外传任何私有信息。

## Q: 运行报 Python 错误 / 模块找不到？
关键词: 报错 错误 python 模块 找不到 环境
A: `python3 --version` 需 ≥3.8。所有脚本仅用标准库，无需 pip 安装。若报错，运行 `python3 doctor.py` 获取带错误码（E001~E005 / W001~W004）的诊断与下一步。
