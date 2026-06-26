# 商机热榜指南（opportunities）

> 命令为只读；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py opportunities
```

- 无额外参数；使用 AK 签名调用 `/1688claw/skill/workflow`，body 固定 `{"code": "offer_opportunity"}`。

## 典型触发场景

- “现在的热榜/近1小时趋势商机/爆款榜单/实时榜单”
- “小红书/淘宝/1688 当前热度/排行/榜单”
- 用户已表述要看“榜单/趋势/热度”，AK 已配置。

## 输出理解

- 正常：`bizData` 为嵌套 JSON，含 `1688/taobao/xiaohongshu` 下的 trend/hot。默认摘要仅展示各平台的 `detail` Top 若干条；`graphic` 保存在 `data`，仅在用户追问细节或需要图表概览时再取用。
- 展示时结合用户关注点改写摘要（如只关心淘宝，则突出淘宝 trend/hot Top 条目），避免逐字透传原始结构。
- 无结果：若返回为空或字段缺失，脚本会提示“未返回商机数据”；可建议稍后重试。

## 异常处理

- 通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
