# Qenda AI 封面生成

## 封面优先级

1. item 专属封面：`{uploads_dir}/cover_{item_id}/cover.jpg`
2. Qenda AI 生成（基于标题，9:16 竖版，4K）
3. 通用封面：`{uploads_dir}/*.jpg`

以上路径取自 CONFIG.md。

## Qenda API

- 端点：`https://api.ai6700.com/api/v1/media/generate`
- 模型：`wan2.7-image`
- 同步等待，最长 120s（轮询每 5s 一次，共 24 次）
- 输出尺寸：9:16（竖版抖音封面）

## 生成提示词模板

```
抖音视频封面，标题文字「{clean_title}」，
深色科技感背景配渐变光效，左上角标注「AI量化」，
整体氛围专业权威，适合金融科技主题，9:16竖版，4K高清
```

clean_title = 标题中移除 emoji、截断到 40 字。

## 常见失败

| 状态 | 原因 | 解决 |
|------|------|------|
| submit failed | API Key 无效或余额不足 | 检查 Qenda 账户 |
| poll timeout | 生成耗时 >120s | 手动延长超时或使用已有封面 |
| 无生成权限 | 账户额度用完 | 联系 Qenda 续费 |
