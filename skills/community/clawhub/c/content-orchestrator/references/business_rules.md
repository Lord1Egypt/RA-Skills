# content-orchestrator 业务规则参考

> 来源: 02内容矩阵手册§五(工作流) + 05文档§四(DEF-U47管线补全) + SKILL.md

## 11步状态机

```
hotspot → copywrite → marketing_inject → material_gen → seo_optimize_pre
→ geo_optimize → qa → publish → schedule → analytics → seo_optimize
```

- 每步状态: pending / in_progress / completed / failed / skipped
- 只允许redo_step重试failed状态的步骤
- 下游步骤随目标步骤一起重置(R43 output依赖链)

## 管线类型

| 类型 | 模板 | 说明 |
|:-----|:-----|:-----|
| E2E-DAILY | 端到端日常 | 完整11步 |
| PL-VIDEO | 视频管线 | hotspot→copywrite→material_gen→publish |
| PL-IMAGE | 图片管线 | hotspot→copywrite→material_gen→publish |
| PL-COMIC | 漫画管线 | 含角色一致性生成 |
| PL-NOVEL-BATCH | 小说批量 | 批量脚本生成 |

## 存储策略

- PG优先(content_pipelines表), JSON降级(data/content_pipelines/)
- PG写入时同步写JSON(防止RLS租户上下文不一致导致读取失败)
- RLS: SET app.current_tenant = tenant_id

## 质量评分(content_quality_scorer)

- 评分维度: 内容质量/营销注入/SEO优化/受众匹配
- 评分阈值: ≥0.7为合格, <0.7触发qa步骤重试
