# Run Log Spec

每次正式执行 Skill 时，应输出一份运行记录，便于复盘、质检、调参和后续批量化生产。

## 必填边界

以下路径必须输出 Run Log：

- `production_cover`
- `engineering_rendering`
- 批量输出
- 任何发生重试、降级、升级或拒绝的任务

快速预览和纯 `prompt_package` 可以不写完整 Run Log，但仍需说明 Source Lock、路由和风险。

## 文件命名

```text
_runs/YYYYMMDD-HHMM-<project-slug>/run-log.md
```

## Run Log 字段

```yaml
run_id: ""
created_at: ""
source:
  type: ""
  title: ""
  summary: ""
source_lock:
  core_topic: ""
  key_points: []
  boundaries: []
routing:
  output_mode: ""
  execution_mode: ""
  reason: ""
artifacts:
  - name: ""
    type: ""
    status: ""
    path: ""
asset_sources:
  - asset_id: ""
    role: ""
    source_type: ""
    source_url: ""
    license: ""
    attribution_required: true/false
    commercial_use_allowed: true/false/unknown
    decision: use/replace/request_confirmation/reject
quality:
  content_fidelity: pass/fail/risk
  visual_consistency: pass/fail/risk
  text_legibility: pass/fail/risk
  anti_plagiarism: pass/fail/risk
  asset_source_policy: pass/fail/risk
retry:
  needed: true/false
  reasons: []
  suggested_actions: []
production:
  engineering_rendering_recommended: true/false
  reason: ""
notes: ""
```

## 最小运行记录模板

```md
# Run Log

## 1. 输入源
- 类型：
- 主题：
- 内容边界：

## 2. 路由结果
- 输出模式：
- 执行模式：
- 选择原因：

## 3. 生成物
| 名称 | 类型 | 状态 | 备注 |
|---|---|---|---|

## 4. 质检结果
- 内容忠实度：
- 视觉一致性：
- 中文可读性：
- 反抄袭：
- 素材来源策略：

## 4A. 素材来源
| 素材 | 角色 | 来源 | 许可证 | 署名 | 决策 |
|---|---|---|---|---|---|

## 5. 重试建议
- 是否需要：
- 原因：
- 下一步：
```
