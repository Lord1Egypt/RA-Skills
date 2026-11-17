# v1.5 全链路示例

## 1. 剧本

先锁定：

- 观众承诺
- 主角欲望
- 阻力
- 代价
- 每集开场问题
- 每集大悬念
- 每集回收
- 评论问题
- 下一集钩子

## 2. 场景和分镜

每场戏必须有：

- 目标
- 阻力
- 策略
- 转折
- 出口

每镜必须有：

- 故事功能
- 覆盖角色
- 运镜动机
- 视线
- 屏幕方向
- 光线方向
- 提示词
- 角色参考
- 时长
- 状态

## 3. 付费前

```powershell
validate_project.py
audit_retention.py
build_seedance_tasks.py
seedance_client.py dry-run
```

只有预演通过、任务数量确认、参考图方案确认后，才允许付费提交。

## 4. 视频生成

```powershell
seedance_client.py submit --execute --confirm-paid --limit 1 --embed-local-refs
seedance_client.py poll --download-dir .\raw_generations
```

## 5. 后期

- 选片
- 配音
- 字幕
- 口型
- 音乐/音效
- 调色
- 后期文字
- 版权水印
- AI标识
- 交付清单

## 6. 关键原则

- 分镜表是唯一生成来源
- 任务状态必须可追溯
- 角色参考图不能丢
- 付费必须显式确认
- 失败只重跑单镜
- 不把中文文字交给视频模型生成
- 不用单条爆款承诺替代发布测试

`© 2026 火焰广告 版权所有。`
