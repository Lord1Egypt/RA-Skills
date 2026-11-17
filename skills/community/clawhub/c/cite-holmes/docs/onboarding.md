# 5 分钟上手路径（三级）

> **30 秒导航**：新用户从这里开始——三级路径每级一条命令，跑完即懂五态判定；
> 卡住看 faq.md，误用看 anti-patterns.md。

## 第 1 级（30 秒）：零门槛体验

```bash
python scripts/verify_refs.py --demo
```

内置 8 条引用（3 处预埋伪造）跑完整判定流程。看三样东西：五态判定列、
CiteScore、报告头部结论。**invalid 的那条就是预埋的假 DOI**。

## 第 2 级（3 分钟）：核验你自己的清单

把你的引用整理成 JSON（每条 title/url/doi/pmid 任填其一二）：

```bash
python scripts/verify_refs.py --refs refs.json --out report.md
```

打开 report.md：头部 BLUF + CiteScore，逐条判定与依据。partial 条目按
备注人工过目；unreachable 换网络重跑（≠不存在）。

## 第 3 级（5 分钟）：投稿前导出

```bash
python scripts/verify_refs.py --refs refs.json --preset submission
```

一键：严格退出码 + GB/T 7714 / BibTeX / CSV 三导出（仅收 verified 与
元数据一致的条目，宁缺毋错）。

## 之后按需

- 医学清单：`--easy` 自动识别；本地文献库批量：`--refs-dir ~/Zotero/`；
  上一轮未决条目再生：`--next-round report.json`；过程留痕：`--trace`。
- 概念与判定语义：`references/verification-details.md`；任务路由：
  `references/INDEX.md`。

## 示例请求（怎么说会触发什么）

- 「帮我核验这份参考文献列表」/「这些 DOI 是真的吗」→ 引用核验
- 「找近三年 XX 主题的文献，导出 GB/T」→ --discover + --review-kit
- 「深度研究 XX 的研究现状」→ 五阶段工作流（QUICK/FULL 自适应）
- 「投稿前帮我终检参考文献」→ --preset submission
- 「这份报告经得起审稿人挑刺吗」→ --grill
