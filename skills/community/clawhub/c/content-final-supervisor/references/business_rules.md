# 业务规则 - content-final-supervisor

> 来源: skills/content-final-supervisor/SKILL.md (来源: B3-03修复 R-91/R-86/R20/R72.2)

## 规则列表

### 终检阶段

三阶段终检流程,按顺序执行:

| 阶段 | 代码 | 检查项 |
|:-----|:-----|:-------|
| 剧本终检 | script | 主题一致性 / 角色设定 / 情节逻辑 / 台词规范 / 红线合规 |
| 分镜终检 | storyboard | 分镜与剧本一致性 / 镜头语言 / 画面描述 / 转场设计 |
| 视频终检 | video | 视频与分镜一致性 / 画面质量 / 音频同步 / 时长合规 |

### 终检模式 (stage 参数)

- `script`: 仅剧本终检
- `storyboard`: 仅分镜终检
- `video`: 仅视频终检
- `all`: 全链终检,按 script→storyboard→video 顺序依次执行,每阶段通过后才进入下一阶段

### 红线检查

- 红线违规: 立即标记 verdict=fail,进入返工流程
- check_type: script / storyboard / video
- redline_list: 自定义红线检查项列表

### 跨阶段一致性检查

- 验证三阶段输出是否对齐 (剧本↔分镜↔视频)
- 不一致项: 标记 inconsistency,触发对应阶段返工

### 返工规则

- 返工条件: verdict=fail 且可修复
- 返工后: 重新进入对应阶段终检
- 返工次数上限: 3 次
- 超限处理: 返工次数 > 3 次,触发 final_arbitration 终审

### 终审仲裁

- 触发条件: verdict=fail 且需人工介入或争议,或返工次数超限
- 终审结果: 为最终结论,不可再返工

### 发布门控

- can_publish=true 条件: verdict=pass (所有终检阶段通过 + 红线无违规 + 跨阶段一致)

### MCP 依赖

- 依赖: quality-supervisor-mcp (8个工具)
  - supervise_script / supervise_storyboard / supervise_video
  - check_redlines / cross_stage_consistency
  - get_supervision_history / auto_redo / final_arbitration

### 超时限制

- 终检超时阈值: 120 秒
- 超时处理: 返回 TIMEOUT,建议分阶段终检
