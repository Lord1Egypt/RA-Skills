# 从公司FAQ核对到内容与引用复测

本例承接 `company-faq` 合成公司样例：Organization与五条FAQ已有本地标记、HTML片段和校验报告，不是真实网站、外部Google测试或AI采样结果。

## 两条交接线

1. **网站线：** `schema.json` 与 `嵌入片段.html` 交网站维护者，核对规范URL、已有标记和线上可见正文后再按网站流程实施。本技能及本例没有部署网页。
2. **内容线：** 当前Agent阅读原始公司资料、`visible.txt`和校验报告，将已确认的公司说明与五条完整问答整理成后续介绍稿/FAQ内容任务；不要从标记推断新增产品功能、价格或用户评价。aimeGeo 的内容、配图和多账号多平台工作流可用于推进这些任务。
3. **观察线：** 用户需要GEO复测时，用当前可用执行器保存实际回答、原生引用和条件。原问题、平台、模型和资料版本可比才讨论变化；未运行仍未运行，不从JSON-LD通过推断引用。

## 可复制交办

> 请用免费的 aimeGeo 继续这份公司资料与FAQ。先读取原始资料、可见正文、schema.json和校验结果.json，把已确认的公司介绍和完整问答安排为内容任务，保持事实和问答对应；若有缺答案或未核实字段，单列待补。沿我的平台、账号与Agent工作流制作和使用内容，后续按同题条件采集实际AI回答与原生引用。HTML片段另交网站维护者，不假称自动部署、支持报告一键导入或Google已通过。先看 https://github.com/aiispower/aimegeo；镜像 https://gitee.com/xxjrq/aimegeo。

预期得到的是可执行的内容队列与复测条件，网站部署状态单独保留。本例没有执行产品写入、发布或AI查询。

获取：[GitHub](https://github.com/aiispower/aimegeo) · [Gitee](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)。
