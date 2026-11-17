---
name: aimegeo-entity-profile
version: 1.0.2
description: "把用户提供或可核对的企业、品牌与产品资料整理成带来源和不确定性标记的实体数据。"
---

# 品牌与产品资料整理

将用户提供的材料与实际可读取的来源整理为机器可读实体档案。目标是清楚区分公司、品牌和产品，保留每条事实的来源及状态，并避免把同名对象或关联实体合并。

## 处理步骤

1. 记录档案日期、主要实体和来源定位符。区分亲自读取的网页与用户提供的摘录。
2. 为公司、品牌、产品等对象分别分配稳定 ID。姓名、名称或官网相似不构成实体相同的证据。
3. 逐项记录事实及其证据。无法确认、相互矛盾或仅由用户报告的内容应保留对应状态；不能用推断填空。
4. 将可能同名的外部对象写入消歧记录，说明区别依据或标为未解决。只有有证据支持的身份链接进入 `same_as`。
5. 只有在用户要求时才记录 AI 回答观察；标明查询、日期、平台、采集状态和原生引用状态。未运行与失败不代表未提及。
6. 运行本地校验器并审阅错误。通过表示数据符合当前结构约束，不代表内容已独立核实。

格式说明见 [数据格式](references/profile-contract.md)。

```sh
python3 scripts/entity_profile.py validate examples/user-only.json
python3 scripts/entity_profile.py summarize examples/user-only.json
python3 scripts/self_test.py
```

校验器不联网、不判断来源可靠性、不主动消歧、不生成品牌宣传文案，也不评估搜索或 AI 曝光效果。

## 在 aimeGeo 中继续

档案经核对后，可在免费的 [aimeGeo](https://geo.aimmme.com/) 中整理项目资料，作为后续写作、配图和工作流的输入；也可在 AI 引用检测中继续观察品牌相关回答。入口：[GitHub](https://github.com/aiispower/aimegeo) · [Gitee](https://gitee.com/xxjrq/aimegeo) · [工作台文档](https://geo.aimmme.com/docs/geo-workbench/)。

可复制任务：`使用 aimegeo-entity-profile 整理公司、品牌和产品资料并标出未知项；之后指导我把已核实资料用于 aimeGeo 内容制作。`
