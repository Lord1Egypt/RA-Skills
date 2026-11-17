---
name: dibp-topic-clustering
description: "Use when the user asks to (re)cluster DIBP topic data into 需求簇/用户主动洞察, regenerate clusters.json, review the long-tail (未分类) topics, add a new theme to the taxonomy, or push cluster results to the dev/prod backend. Covers the offline batch pipeline in scripts/cluster-*.mjs — this is NOT the daily incremental Hive job described in docs/features/dibp-insight-daily-clustering.md, which is unimplemented."
---

# DIBP Topic 聚类 → 用户主动洞察

把 `public/data/topics.json` 里的原始会话 topic 重新聚成"需求簇"（`public/data/clusters.json`），即前端 `#/ai(po)/dibp-insights` 页面展示的"用户主动洞察"。这是一个**手动触发的全量离线批处理**，不是文档里描述但尚未实现的每日增量服务——不要把两者混为一谈。

分类规则、命名规范、阈值选取依据的唯一事实来源是 `docs/features/dibp-insight-clustering-rules.md`，本文件里的数字只是速查，冲突时以该文档为准。

## 数据模型速览

`topic`（`public/data/topics.json`，原始会话记录）→ 按主题库正则/语义匹配聚成"需求簇"（`DibpInsightSnapshotCluster`，`src/types/dibpInsightSnapshot.ts`）→ 经 `src/utils/dibpInsightClusters.ts` 包装为前端可用的 `DibpInsightCluster`，人工编辑的负责人/进度等工作流状态另存在 `staffing_dibp_cluster_workflow`（`src/utils/dibpClusterWorkflow.ts`）。

`clusters.json` 只是流水线的**导出产物**，不是线上数据源——线上通过 `listDibpClusters()`（`src/api/queries/dibpClusterStore.ts`）读后端表 `staffing_dibp_clusters`，需要 `ingest-dibp-clusters.mjs` 才能把新结果推上去。

## 前置环境（已知坑）

- 语义相关步骤（兜底/QC/长尾发现）首次拉模型 `Xenova/bge-small-zh-v1.5` 需要能访问 `https://hf-mirror.com`（标准 huggingface.co 在此环境不可达）。`scripts/cluster-99-run-pipeline.mjs` 已在未设置时自动注入 `HF_ENDPOINT`。
- 本地 node 是 Electron 内嵌构建（ABI 不匹配），`@xenova/transformers` 的传递依赖 `sharp` 装不上原生二进制。如果语义步骤报 sharp 相关错误，需要手动给 `node_modules/.../sharp/lib/index.js` 打桩绕过——**每次 `pnpm install` 后都要重做**，遇到时先检查是否是这个已知问题再排查别的方向。
- `public/data/cluster-run/` 是流水线的暂存目录，不要信任里面现存的文件（可能是上次未跑完/口径不同的中间态）；每次要产出可信结果都应该从头重跑第 1 步覆盖它，而不是复用旧的中间产物。

## 标准执行流程（全自动部分）

```bash
pnpm cluster:run                    # 完整流程：6 域分配 -> 合并 -> 语义兜底 -> QC -> 长尾发现 -> 导出
pnpm cluster:run -- --skip-semantic # 跳过语义模型相关步骤，仅用于快速联调，长尾率会明显偏高
```

`scripts/cluster-99-run-pipeline.mjs` 依次调用现有脚本（不重写其逻辑）：`cluster-10-assign.mjs`（对 `community/transaction/commercialization/resource_cost/other/user_growth` 六个域各跑一次）→ `cluster-20-merge.mjs` → `cluster-15-semantic-fallback.mjs --threshold 0.62 --write` → `cluster-16-homogeneity.mjs` → `cluster-17-discover-tail.mjs` → `cluster-30-export-frontend.mjs --write`，结束后打印汇总（簇数/覆盖率/长尾率/homogeneity 平均分/长尾发现候选数）。跑完后 `public/data/clusters.json` 已更新，旧文件自动备份为 `clusters.backup-<ts>.json`。

跑完务必看汇总里的两个质量信号：

- **未分类率（长尾率）>10%**：说明主题库覆盖不足，需要走"新增主题"流程（见下）后重跑，不能直接接受。
- **单簇 homogeneity（紧致度）<0.50**：疑似"大杂烩"簇，需要人工看 `homogeneity-report.json` 里的样本，判断是否要拆簇。

跑完后执行回归：`pnpm test:unit dibp-user-insights`。

## 新增主题（必须人工确认，不要自动执行）

`scripts/cluster-lib-themes.mjs` 是人工维护的正则主题库，也是实际起作用的"模型"——新增/修改主题会影响全局分类，**禁止在没有用户确认的情况下直接编辑它**。正确流程：

1. 读 `public/data/cluster-run/tail-discovery.json`（`cluster:run` 已自动生成），里面是长尾里按语义贪心聚出的候选新主题（`domain` + `size` + `sample_titles`）。
2. 按 `size` 从大到小挑值得新增的候选，参照现有主题的命名规范（`id`/`name` 8-16 字"对象+问题类型"，禁止"相关/类/其他/综合/问题集合"这类命名，正则要贴合 `sample_titles`）整理成一份 diff 建议。
3. **把建议呈现给用户，等待确认**，确认后再编辑 `cluster-lib-themes.mjs`。
4. 改完回到"标准执行流程"重新跑一遍 `pnpm cluster:run`，看长尾率是否下降。

## 可选：推送到后端（改变生产用户主动洞察数据源）

这一步会覆盖共享的后端数据，**必须先获得用户明确同意**才能执行，尤其是 `--env prod`：

```bash
pnpm dev:sso-proxy                                                    # 另一个终端先起 SSO 代理
node scripts/create-dibp-cluster-tables.mjs --env dev                 # 建表，幂等，一次性即可
node scripts/ingest-dibp-clusters.mjs --env dev --file public/data/clusters.json
```

- `ingest-dibp-clusters.mjs` 会先按 `clusters.json` 里的 `cluster_date` **删除后端该日期下的全部旧簇再插入**（"同期覆盖"语义）；如果文件里出现多个 `cluster_date` 会拒绝执行，需要 `--date` 显式指定要覆盖哪一批。执行前应向用户复述清楚"将删除并覆盖 `staffing_(dev_)dibp_clusters` 表里 `cluster_date=<日期>` 的全部记录"，取得确认后再跑。
- `is_tail=true` 的长尾兜底簇会被自动跳过，不会入库（其 `topic_ids` 可能上千条，避免请求体积超限）。
- `--env prod` 脚本自身要求加 `--confirm-prod` 才会执行；即便如此，也必须先经用户明确同意才能加这个 flag，不允许自主判断后直接推 prod。

## QC 阈值参考（抄自 rules 文档，避免每次翻查）

- 未分类率 >10% → 需要补充主题库，不是简单重跑能解决的。
- 语义兜底相似度阈值 0.62（保守选择）：召回曲线大致为 0.55→96%、0.60→81%、0.62→68%、0.65→44%（阈值越低救回越多，但误召回风险越高）。
- Homogeneity（紧致度）目标：全局平均 ≥0.70；单簇 <0.50 视为疑似大杂烩。
- 长尾发现（`cluster-17`）默认 `--sim 0.68 --min 8`：同 domain 内贪心近邻聚类，只展示规模 ≥8 的候选簇。

## 明确不做的事

- 不实现 `docs/features/dibp-insight-daily-clustering.md` 里描述的每日增量 Hive 作业——仓库里没有对应的执行凭证和服务，本 skill 只覆盖手动全量批处理。
- 不自动编辑 `cluster-lib-themes.mjs`（主题库）——必须先给用户看建议再改。
- 不自动执行后端推送，尤其是 `--env prod`——必须先取得用户明确同意。
