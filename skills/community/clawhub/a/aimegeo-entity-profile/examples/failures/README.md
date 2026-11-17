# 失败与部分完成样例

所有文件均为离线演示资料。它们用于说明数据边界，不是查询结果。

## 将公司官网误设为产品 sameAs

```sh
python3 scripts/entity_profile.py validate examples/failures/mixed-identity.json
```

实际预期：退出 2，返回 `same_as_cross_entity`，路径 `$.entities[1].same_as[0]`；完整响应见 [expected-error.json](expected-error.json)。该错误档案将 `https://qinghe-tools.example/` 放入软件 same_as，而它已明确属于公司主体。开发关系不等于身份相同。

修正：删除错误 same_as，保留软件 → 公司的 developed_by 关系，得到[成功档案](../qinghe/品牌实体档案.json)。不要将公司改为产品别名来绕过。

## 只有用户任务也能部分完成

[user-only.json](../user-only.json) 仅根据“青禾科技有限公司的产品叫青禾工具，英文 Qinghe Tools”建立两个主体，名称标 reported、其他事实标 unknown。未提供官网、未断定是软件，未将“公司的产品”扩大为开发或所有权关系。

```sh
python3 scripts/entity_profile.py validate examples/user-only.json
python3 scripts/entity_profile.py schema examples/user-only.json
```

第一条退出 0：可以交付有出处的部分档案。第二条退出 2，错误 `schema_identity_unverified`：缺已支持的官网与规范身份，暂不可转换 Schema。下一步只需询问官网网址或产品页摘录；不用先申请百科或接入 API。

自测还覆盖出处缺失、无关主体证据、无原文引文、错误关系方向、未知日期被填值、冲突日期、未采集引用写成零、模拟混入分母、JSON 损坏等边界，见 [self_test.py](../../scripts/self_test.py)。
