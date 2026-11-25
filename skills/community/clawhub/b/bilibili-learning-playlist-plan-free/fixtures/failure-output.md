# 离线失败分支实际结果

输入 [failure-private-unauthorized.json](failure-private-unauthorized.json) 是离线页面资料模拟，`collectionAccess` 明确为 `unauthorized`，表示私人收藏夹未获授权；不代表在线读取。

规划器以退出码非零停止，业务错误为：`私人收藏夹未授权：停止读取，未生成学习顺序或日程`。该分支在读取条目及校验标题前拦截，因此不会猜测内容，也不会生成学习顺序或日程。

说明：此 fixture 验证规划器对明确未授权状态的停止行为。线上登录、验证码和风控仍须由实际操作流程停止处理，未进行在线验收。
