# Wiki 读取规则

Wiki 只补充商家背景，不替代店铺体检接口数据。

- `WikiNav` / `WikiRead` 是当前会话提供的模型工具，不是本 skill 的 CLI 命令；没有 `WikiNav` 时跳过 Wiki，不要用 CLI、Bash 或猜文件路径替代。有 `WikiNav` 但没有 `WikiRead` 时，只使用可靠的页卡摘要，不尝试调用不存在的工具。
- 调用时传 `skillName="1688-shop-health-check"`。
- 店铺路由用 `loginId`，不用 `shopId` / userId，也不得把 `loginId` 写入 query。仅当工具参数中提供 `loginId` 时才传入目标店铺的 `loginId`；单店工具没有该参数时省略，使用当前店铺。
- 每店只调用一次 `WikiNav(query="店铺", skillName="1688-shop-health-check")`；工具提供 `loginId` 参数时增加目标店铺的 `loginId`。不改写 query 二次搜索，不翻页续查。
- 只使用属于目标店铺的店铺、品牌、工厂、经营定位或服务体系页面；客户实体、单个商品和平台知识不能代表店铺整体背景。
- 如果 `WikiNav` 提示目标 `loginId` 未找到、已查询默认店或当前店，立即丢弃该次结果，不调用 `WikiRead`，也不得把回落店铺的内容用于目标店铺。
- 如果 `WikiNav` 页卡的标题、摘要和章节已足够形成可靠的商家背景，直接整理摘要并停止，不调用 `WikiRead`。
- 只有页卡摘要不足时才读取正文：每店最多选择 3 个最相关页面，在同一轮调用 `WikiRead`；`page/path` 必须沿用 `WikiNav` 返回的信息。仅当 `WikiRead` 参数中提供 `loginId` 时才沿用对应页卡的 `loginId`，不得自行编写路径或路由值。
- 不要把 A 店 Wiki 用到 B 店；路由或页面归属不确定就跳过。
- 经营指标、销量、转化率、价格、评价、违规、履约等量化事实，以 CLI / 接口数据为准。
- Wiki 只能影响背景解释和建议措辞，不能单独制造诊断结论。
