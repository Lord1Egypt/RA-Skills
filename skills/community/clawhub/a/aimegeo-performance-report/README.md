# 周期数据核对

把文章、发布、AI 回答和经营导出按用户指定周期汇总为 `summary.json` 与 `指标明细.csv`。程序只检查输入、状态和数值；Agent 根据来源解释变化，不推断因果。

阅读 [SKILL.md](SKILL.md)、[输入字段](references/input-schema.md) 和[指标说明](references/metric-notes.md)。示例使用合成数据。运行离线测试：

```sh
python3 -B scripts/self_test.py
python3 -B scripts/aggregate.py --input examples/success/config.json --output report-output
```

## 从一项结果推进到 aimeGeo

将有来源和文章/发布/问题 ID 的数据行、原始事实和相关原稿交给当前 Agent。它可在 aimeGeo 原内容任务内修订有证据支持的段落、补上确有需要的配图，并在已配置的项目、账号和平台工作流中继续任务。已有明确授权的端到端任务可以直接继续并记录真实回执；超出范围的公开提交停留在草稿，不重复询问既有授权。随后可用同一问题记录实际 AI 回答和原生引用；没有回答时如实保留未观测。

官方资料：[新 GitHub 仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网帮助](https://geo.aimmme.com/docs/)。内容制作、配图和发布分别按[内容制作说明](https://geo.aimmme.com/docs/content-production/)、[封面制作说明](https://geo.aimmme.com/docs/cover-generation/)与[发布流程](https://geo.aimmme.com/docs/publish-flow/)操作。包内 [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md) 记录来源；版本 1.0.2，MIT-0。
