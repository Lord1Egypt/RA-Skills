---
name: content-final-supervisor
description: 内容终检统一入口(CP-01),连接quality-supervisor-mcp,对剧本/分镜/视频三阶段执行质量终检+红线检查+跨阶段一致性+终审仲裁。触发:终检/质量监督/质量终检/supervise/final_check/内容审核终检/漫剧终检
tools:
  - mcp_caller
dependencies: []
metadata:
  requires:
    config:
      - mcp.servers.quality-supervisor-mcp
    bins:
      - python
  priority: "P1"
  version: "1.0"
  phase: "B3-03"
  ep: "CP-01"
  source_rules: "R-91/R-86/R20/R72.2"
---

# 内容终检统一入口 (CP-01)

> 来源: B3-03修复(R-91终检入口统一化/R-86终检缺失/R20赚钱链路完整性/R72.2核心表保护)
> MCP依赖: quality-supervisor-mcp (8工具: supervise_script/supervise_storyboard/supervise_video/check_redlines/cross_stage_consistency/get_supervision_history/auto_redo/final_arbitration)

## 使用场景

- 漫剧/短视频内容生产完成后,发布前必须经过终检
- 三阶段(剧本→分镜→视频)任意阶段需要质量审核
- 发现质量问题后需要自动返工或终审仲裁
- 跨阶段一致性检查(剧本与分镜与视频是否对齐)

## 工作流

### 1. 终检初始化

1. 接收终检请求,包含: episode_id(剧集ID)、stage(终检阶段: script/storyboard/video/all)、content(待检内容)
2. 通过mcp_caller调用quality-supervisor-mcp.get_supervision_history获取历史监督记录
3. 判断是否有未解决的返工项: 如果有,先处理返工再进入终检

### 2. 分阶段终检

根据stage参数执行对应终检:

**剧本终检(stage=script)**:
- 执行: mcp_caller → quality-supervisor-mcp.supervise_script(episode_id, script_content, project_params)
- 检查项: 主题一致性/角色设定/情节逻辑/台词规范/红线合规

**分镜终检(stage=storyboard)**:
- 执行: mcp_caller → quality-supervisor-mcp.supervise_storyboard(episode_id, storyboard_content, script_content)
- 检查项: 分镜与剧本一致性/镜头语言/画面描述/转场设计

**视频终检(stage=video)**:
- 执行: mcp_caller → quality-supervisor-mcp.supervise_video(episode_id, video_url, storyboard_content)
- 检查项: 视频与分镜一致性/画面质量/音频同步/时长合规

**全链终检(stage=all)**:
- 按script→storyboard→video顺序依次执行三阶段终检
- 每阶段终检通过后才进入下一阶段

### 3. 红线检查

- 执行: mcp_caller → quality-supervisor-mcp.check_redlines(content, check_type, redline_list)
- check_type: script/storyboard/video
- 红线违规: 立即标记verdict=fail,进入返工流程

### 4. 跨阶段一致性检查

- 执行: mcp_caller → quality-supervisor-mcp.cross_stage_consistency(episode_id, stage_outputs)
- 验证三阶段输出是否对齐(剧本↔分镜↔视频)
- 不一致项: 标记inconsistency,触发对应阶段返工

### 5. 返工或终审

**返工(verdict=fail且可修复)**:
- 执行: mcp_caller → quality-supervisor-mcp.auto_redo(episode_id, stage, supervision_id, verdict, retry_reason)
- 返工后重新进入步骤2对应阶段终检

**终审仲裁(verdict=fail且需人工介入或争议)**:
- 执行: mcp_caller → quality-supervisor-mcp.final_arbitration(episode_id, supervision_id, final_verdict, arbiter_note)
- 终审结果为最终结论,不可再返工

### 6. 终检报告输出

```json
{
  "success": true,
  "data": {
    "episode_id": 123,
    "stage": "all",
    "verdict": "pass",
    "checks": {
      "script": {"verdict": "pass", "supervision_id": 456},
      "storyboard": {"verdict": "pass", "supervision_id": 457},
      "video": {"verdict": "pass", "supervision_id": 458},
      "redlines": {"verdict": "pass", "violations": []},
      "consistency": {"verdict": "pass", "inconsistencies": []}
    },
    "final_supervision_id": 458,
    "can_publish": true
  },
  "error": null,
  "code": "SUPERVISION_OK"
}
```

## 输入格式

```json
{
  "episode_id": 123,
  "stage": "all",
  "script_content": "剧本文本...",
  "storyboard_content": "分镜JSON...",
  "video_url": "https://...",
  "project_params": "{\"theme\":\"...\"}",
  "redline_list": "[]"
}
```

## 输出格式

```json
{
  "success": true,
  "data": {"episode_id": 123, "verdict": "pass|fail|redo", "supervision_id": 456, "can_publish": true},
  "error": null,
  "code": "SUPERVISION_OK|SUPERVISION_FAIL|SUPERVISION_REDO"
}
```

## 异常处理

| 异常 | 处理 | 错误码 |
|:-----|:-----|:-------|
| quality-supervisor-mcp不可用 | 返回SERVICE_UNAVAILABLE错误,建议稍后重试 | SUPERVISION_SERVICE_DOWN |
| episode_id不存在 | 返回NOT_FOUND错误 | EPISODE_NOT_FOUND |
| 内容为空 | 返回VALIDATION_ERROR | CONTENT_EMPTY |
| 终检超时(>120秒) | 返回TIMEOUT,建议分阶段终检 | SUPERVISION_TIMEOUT |
| 返工次数超限(>3次) | 触发final_arbitration终审 | REDO_LIMIT_EXCEEDED |

## 示例

### 示例1: 全链终检通过

```json
输入: {"episode_id": 123, "stage": "all", "script_content": "...", "storyboard_content": "...", "video_url": "https://..."}
输出: {"success": true, "data": {"verdict": "pass", "can_publish": true}, "code": "SUPERVISION_OK"}
```

### 示例2: 红线违规触发返工

```json
输入: {"episode_id": 124, "stage": "script", "script_content": "...含敏感词..."}
输出: {"success": true, "data": {"verdict": "fail", "redline_violation": "敏感词:<参数>", "redo_recommended": true}, "code": "SUPERVISION_REDO"}
```

## 变更历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-07-17 | B3-03修复: 创建CP-01统一终检入口,连接quality-supervisor-mcp 8工具,覆盖剧本/分镜/视频三阶段终检+红线+一致性+返工+终审(R-91/R-86). 2026-07-19修正:EP-05→CP-01(05文档§6.1 EP-05=竞品分析,内容终检属CP链路) |
