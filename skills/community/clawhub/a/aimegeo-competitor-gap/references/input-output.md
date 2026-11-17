# 输入与输出

Python 3.10+ 标准库，无 pip 安装要求。命令从技能目录运行，快照路径相对于输入 JSON 所在目录；脚本可由绝对路径调用，不依赖当前工作目录。快照必须位于输入目录内，不能通过绝对路径或 `..` 逃逸；跨目录的用户资料先复制到本次输入目录再引用。

```bash
python3 scripts/compare_pages.py --input examples/comparison.json --out /tmp/competitor-gap-demo
python3 scripts/compare_pages.py --input examples/failure-input.json --out /tmp/competitor-gap-failure
```

实际选项只有 `--input`、`--out`、`--fetch` 和 `--help`。可选 `--fetch` 仅 GET 明确给定且没有 snapshot 的 URL，使用 10 秒超时，响应最多 3 MiB；可跟随服务端重定向，记录 final_url。同页 URL 去片段、保留查询串，在单次运行中缓存，失败也缓存。同一 URL 出现冲突采集记录则拒绝输入，避免比较不同版本。不会自动读取 robots、llms、关于页、站点地图或页面外链，也不执行 JavaScript。

## 比较文件字段

完整可运行文件见 [comparison.json](../examples/comparison.json)。顶层字段：

| 字段 | 要求与含义 |
| --- | --- |
| comparison.question | 必填，说明用户要解决的问题 |
| comparison.page_slots | 非空且唯一的字符串列表，如 product、pricing；规定全体品牌的比较范围 |
| sites | 一项 role=brand，至少一项 role=competitor；id 唯一，name 为显示名称 |
| sites[].aliases | 可选，明确的品牌别名列表；不要用“我们”等泛称 |
| sites[].pages | slot、url、可选 snapshot。每槽位每方最多一页；缺槽位输出未验证 |
| sites[].robots | 可选，明确 url 和可选 snapshot。只用于与最终页面同源的路径判断 |
| ai_samples | 可选；省略或空数组代表未提供真实 AI 实测样本 |

snapshot 的 `status` 为 `ok`、`failed` 或 `not_run`；`kind` 为 `observed` 或 `simulated`；`captured_at` 必须带时区。`ok` 需要 UTF-8 的 `path` 和 2xx `http_status`，可附 `final_url`。其余状态需要 `reason`；若已知 HTTP 状态可保留 `http_status`，失败不读取正文，也不会因 `--fetch` 自动重试。快照状态表示用户提供的采集记录，不是脚本对网站真实性的认证。文件缺失/无法解码按页面未验证处理；超尺寸、非法路径、无效配置为输入错误。

没有 snapshot 且没用 `--fetch` 时，记录“未运行”；其他已读页面照常交付。已读页面内容仅为壳或无法定位可见正文时也按未验证处理。登录页或软错误页可能有正文，Agent 必须复核再采用，不将 HTTP 200 自动等同业务成功。

## 可选 AI 样本

以下是**字段示意，不是实测结果**。真实使用时必须提供对应原始资料；`status=observed` 不能用来给构造回答贴真实标签。

```json
{
  "id": "demo-answer",
  "status": "simulated",
  "platform": "offline-fixture",
  "query": "哪些工具支持 CSV 导入？",
  "captured_at": "2026-10-19T12:00:00+08:00",
  "answer": "模拟回答：青禾支持 CSV 导入。",
  "evidence": "本次构造回答的记录标识",
  "native_citations": null
}
```

成功回答使用 `observed` 或 `simulated`，需要非空 `answer`、`platform`、`query`、`captured_at`、`evidence`。`evidence` 是用户提供的导出文件/记录定位符，不由脚本打开。`native_citations` 必须显式提供：`null` 表示没有采集，`[]` 表示采集后确认无条目，有条目时为 `[{"url":"https://source.example/","label":"可选原生标签"}]`。不能把回答正文链接补进该数组。

未运行/失败用 `not_run` / `query_failed`，填写 `reason`，不能携带成功回答或非空的引用数据结构。示例见 [failure-input.json](../examples/failure-input.json)。

## 交付文件与退出码

`竞品差距矩阵.csv` 按槽位和信号排列，各品牌值与证据并列；未验证单元格有原因，模拟单元格标明模拟。`evidence.json` 保存 URL、采集时间、HTTP 状态、文件摘要、解析证据、匹配规则、原始 AI 样本、分母和缓存计数。没有用户/Agent 的原创建议写作功能。

`analysis_status=observed` 在页面对象中仅表示可提取的页面证据，是否模拟以同一对象的 `acquisition.kind` 为准；`comparisons[].kind` 同样保留性质。`ai_observations` 的真实分母只纳入 `status=observed` 的回答；引用分母还要求已采集原生来源。模拟回答保留原输入，但 `native_citation_count` 为 `null`，不冒充零条真实引用。真实引用分母为 0 时总数为 `null`，不是 0。不汇总平台排名、不判断索引收录。

退出码 0 表示完成报告，即使包含未验证页面；调用者仍需看 `pages_unverified` 和报告状态。退出码 2 表示配置、输入或输出错误，stderr 说明原因；不要将失败目录中的旧文件当成本次新报告。每次建议使用独立输出目录。
