# scam-radar（防割雷达）安装说明

## 这是什么

理财防割韭菜识别助手：对话式十问采集可疑理财营销（老师荐股/带单、9 元理财课、保本高息、
陌生理财 App）的特征，命中即给官方持牌查验路径与报案止付路径。

**立場**：中立买方——只教通用识别特征 + 官方查验入口 + 列命中事实；
**绝不**替用户给「某产品/课程/平台是骗局」的定性判断，不荐股、不代操作、不承诺追回。

## 安装

把整个 `scam-radar/` 文件夹复制到 Agent 平台的技能目录（如 `~/.workbuddy/skills/`），
或在平台上按「上传 skill 包」的标准流程导入 `scam-radar-<版本>.zip`。

## 依赖

- 无第三方依赖。`scripts/radar_check.py` 纯 Python 标准库，Python 3.8+ 直接可跑。
- 不接任何行情/交易接口，输入数据本地处理。

## 触发方式

对 Agent 说：
- 「帮我查查这个股票群靠不靠谱」
- 「有人推荐我一个理财课/理财 App，帮我过一遍」

## 文件说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 技能主文件（安全红线、五特征、工作流、联动关系） |
| `references/interview.md` | 十问剧本（AI 执行入口） |
| `references/case_material.md` | 实证教材（公开报道套路拆解） |
| `references/check_entrances.md` | 官方查验入口详解 |
| `references/dialog_flows.md` | 三对话流话术 + 拒绝话术库 |
| `scripts/radar_check.py` | 特征自检脚本（case.json / --scenario / --demo） |
| `CHANGELOG.md` | 版本记录 |
| `tests/` | 开发用快照与治理工具（发布包不含，可删） |
