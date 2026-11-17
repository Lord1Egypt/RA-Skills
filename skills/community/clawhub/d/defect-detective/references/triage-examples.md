# 分诊示例

三个完整案例，覆盖主路径与两条跳过分支。日常分诊按 SKILL.md 的规则执行即可；遇到分支判断或想对照输出格式时再读本文。

> 示例中的工单号、路径、报文与数据均为演示用途的虚构或脱敏内容，不代表任何真实系统或真实工单。

## 例 A：后端 API 错误 —— 查重命中（主路径）

**输入信号：**

```text
订单服务下单接口报错：
java.lang.NullPointerException
  at com.mystar.order.service.OrderService.submit(OrderService.java:142)
  at com.mystar.order.controller.OrderController.post(OrderController.java:88)
  at org.springframework.web.filter.OncePerRequestFilter.doFilter(...)
2026-11-12T14:32:11.204+08:00, requestId=req_8f3a2b, thread=http-nio-8080-exec-12
```

**步骤 1 — 指纹：** `NullPointerException · OrderService.submit / order · 下单接口`。剥离时间戳、requestId、线程名；Spring 堆栈帧视为框架帧不进指纹。

**步骤 2 — 降级查重（跨栈，未过滤组件）：**

- 第一级：`NullPointerException + OrderService + 下单` → 无结果
- 第二级：`NullPointerException + 订单服务` → 命中 TICKET-8842「下单偶发空指针」（open，相似度：高——指纹所含核心项[异常类型、模块/端点、消息特征]全命中；指纹无错误码，不参与判定）。指纹无错误码，L2 按流程规则以"异常类型 + 模块/端点"执行
- 第三级：未执行（第二级已命中，命中后停止降级）

**步骤 3 — 涉及层已知**（服务名 + 服务端堆栈），`git blame OrderService.java` 附近近期合并：PR-3021 三天前重构了优惠卷计算。

**步骤 4 — 归属：** 订单服务团队——依据：TICKET-8842 历史归属 + PR-3021 作者所在团队。

**报告（节选）：**

```text
缺陷：订单下单接口 NullPointerException
指纹：NullPointerException · OrderService.submit / order

已知问题？  可能
  - TICKET-8842  下单偶发空指针  (open, 高) — 指纹所含核心项全命中；"偶发"与本例"每次必现"待工程师复核

可能的归属团队：订单服务团队 — TICKET-8842 历史归属 + PR-3021 作者

近期可疑变更：
  - PR-3021  OrderService 优惠卷计算重构 — 命中区域三天前刚改

证据：
  - 搜索关键词：L1 "NullPointerException+OrderService+下单"（无结果）；L2 "NullPointerException+订单服务"（命中）
  - 搜索范围：跨栈
  - 代码关联：order 仓库 main 分支 blame

相关：同区域近 30 天另有 2 张已关闭的 NPE 工单，均不涉及下单路径

建议：链接到已有工单（TICKET-8842）
状态：完成
```

注意：相似度为"高"但"已知问题？"仍答"可能"——本例"每次必现"与工单描述"偶发"存在复现差异，留给工程师确认，不擅自合并。

## 例 B：前端展示问题 —— 跳过步骤 3（前端分支）

**输入信号：** "结账页面的优惠券列表在 Safari 上错位，按钮和输入框重叠，Chrome 正常。"

**步骤 1 — 指纹：** `样式错位 · checkout 优惠券列表 · Safari`。纯 UI 描述，无异常/错误码，指纹以区域 + 现象为主。

**步骤 2 — 降级查重：** 第一级 `Safari 样式错位 + 优惠券列表` → 命中 TICKET-9013（open，相似度：中——按 FAQ 口径，指纹所含核心项中模块/区域与现象命中，但消息特征存在差异：本例限 Safari，工单覆盖 Chrome 全系）。列为候选。

**步骤 3 — 跳过：** 前端渲染/样式异常且无后端线索 → 注明"前端展示问题，无后端代码可关联"。

**步骤 4 — 归属：** 前端 Web 团队——依据：TICKET-9013 的组件标签为 checkout-web。

**报告（节选）：**

```text
缺陷：Safari 结账页优惠券列表错位
指纹：样式错位 · checkout 优惠券列表 · Safari

已知问题？  可能（仅中相似候选）
  - TICKET-9013  Chromium 全系结账优惠券列表错位  (open, 中) — 模块/区域与现象命中，消息特征差异（本例限 Safari）

可能的归属团队：前端 Web 团队 — TICKET-9013 组件标签 checkout-web

近期可疑变更：不适用 — 前端展示问题，无后端代码可关联
相关：无

建议：需要更多信息 — 是否同因由工程师确认，不代为链接（中相似不足以支撑链接，见 FAQ 判定规则）
状态：完成
```

## 例 C：环境/配置类问题 —— 跳过步骤 3 + 无匹配建票（真实冒烟案例）

**输入信号：**

```text
环境：macOS + zsh，AI agent 运行在沙盒执行环境
现象：agent 写入 skill 文件失败：
  [Errno 13] Permission denied: '~/.trae-cn/skills/fast-commit/SKILL.md'
  os.makedirs('~/.trae-cn/skills/fast-commit') 同样 Permission denied
同一进程对项目目录的写入完全正常，只有写 ~/.trae-cn/skills/ 被拒。每次必现。
```

**步骤 1 — 指纹：** `Errno13/EPERM · ~/.trae-cn/skills/ · sandbox write（选择性拒绝）`。剥离用户名、skill 名。关键特征：选择性拒绝（同进程项目目录可写）→ 指向沙盒写权限策略而非文件系统损坏。

**步骤 2 — 降级查重（跨栈）：** 三级全部执行均无结果——可达的工单系统不覆盖此产品域。按 FAQ 规则如实标注：查不到 ≠ 一定是新问题。

**步骤 3 — 跳过：** 环境/配置类问题（沙盒策略、文件权限）→ 注明"无代码仓库可关联"。

**步骤 4 — 归属：** 平台沙盒策略团队——依据：路径属平台配置区 + 选择性拒绝由沙盒写权限策略控制（组件推断，无工单历史佐证，标注推断属性）。

**报告（节选）：**

```text
缺陷：沙盒环境写入 ~/.trae-cn/skills/ 报 EPERM，项目目录写入正常
指纹：Errno13/EPERM · ~/.trae-cn/skills/ · sandbox write

已知问题？  否（可达的工单系统中无匹配）

可能的归属团队：平台沙盒策略团队 — 路径属平台配置区 + 选择性拒绝由沙盒写策略控制

近期可疑变更：不适用 — 环境/配置类问题，无代码仓库可关联

证据：
  - 搜索关键词：L1 "EPERM+skills+Permission denied"；L2 "EPERM"；L3 "skill 写入"（均无结果）
  - 搜索范围：跨栈；可达的工单系统不覆盖此域
  - 代码关联：跳过

相关：无

建议：新建工单（可达工单系统不含此域，无法完全排除已知问题）
状态：完成

建票建议：
  标题：沙盒环境写入 ~/.trae-cn/skills/ 报 EPERM（项目目录写入正常）
  描述：Errno13/EPERM · ~/.trae-cn/skills/；每次必现；同进程项目目录写入正常，仅用户主目录配置区被拒
  建议归属：平台沙盒策略团队
```

注意证据字段如实写出"可达的工单系统不覆盖此域"——这是报告可信度的一部分，掩盖搜索局限才会误导建票决策。
