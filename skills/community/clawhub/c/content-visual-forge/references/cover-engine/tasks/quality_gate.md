# Task: Quality Gate

## 目标
检查生成结果是否达到封面交付标准。

## 检查维度
- 内容契合度
- 标题可读性
- 留白是否充足
- 画面复杂度
- 小字风险
- 公众号缩略图可读性
- 风格一致性
- 是否有廉价模板感
- 是否有版权/IP 风格风险

## 结果等级
```yaml
pass:
  description: 可用
minor_revision:
  description: 小修可用
regenerate_required:
  description: 必须返工
```

## 直接判定返工的情况
- 主标题错字
- 除主标题外出现中文小字
- 书脊或便签出现伪字
- 画面过满导致缩略图混乱
- 标题无法看清
