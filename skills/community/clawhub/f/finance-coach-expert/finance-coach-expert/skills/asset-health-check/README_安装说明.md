# asset-health-check（资产体检）安装说明

## 这是什么

家庭资产体检计算器：对话式采集资产/负债（用户零格式门槛，AI 代填），
本地静态计算净资产、四桶占比、应急金月数、权益占比、集中度、保障覆盖，
输出一张 Markdown 体检卡。

**立场**：诊断书——只报「事实 + 中性经验区间 + 信息缺口」；
**不**荐股/给买卖点位/代操作/下「偏高/偏低」判断，不接行情 API。

## 安装

把整个 `asset-health-check/` 文件夹复制到 Agent 平台的技能目录（如 `~/.workbuddy/skills/`），
或在平台上按「上传 skill 包」的标准流程导入 `asset-health-check-<版本>.zip`。

## 依赖

- 无第三方依赖。`scripts/health_check.py` 纯 Python 标准库，Python 3.8+ 直接可跑。
- 数据全程本地处理、不出本机；用户可全程不登录任何平台。
- 采集的脱敏规范：绝不需要账号/证件号/手机号等敏感信息。

## 触发方式

对 Agent 说：
- 「帮我做一次家庭资产体检」
- 「看看我现在有多少钱，钱都放在哪类里」

## 文件说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 技能主文件（安全红线、工作流、官方自查入口、联动） |
| `references/interview.md` | 对话式采集剧本（AI 执行入口） |
| `references/data_format.md` | 输入 JSON/CSV 字段说明 + 脱敏规范 |
| `references/health_card_template.md` | 体检卡输出结构模板（红线说明） |
| `references/dual_audience.md` | L1/L2 双人群分层逻辑 |
| `scripts/health_check.py` | 体检计算脚本（--input/--output/--demo/--compare） |
| `CHANGELOG.md` | 版本记录 |
| `tests/` | 开发用快照与治理工具（发布包不含，可删） |
