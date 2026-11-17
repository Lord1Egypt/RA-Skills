# feishu-api-cache-fix

> 修复飞书API每分钟调用一次导致额度耗尽的问题

**版本**: 1.0.0
**作者**: @bryan-chx
**标签**: feishu, api, fix, performance

## 问题

Gateway每分钟调用飞书API `/open-apis/bot/v3/info` 检查机器人状态，导致API额度快速耗尽。

## 解决方案

在 `probe.ts` 中添加2小时缓存，避免频繁调用API。

## 修复步骤

```bash
 运行修复脚本
# 1.sudo bash fix_feishu_cache.sh

# 2. 重启OpenClaw
# 点击菜单栏OpenClaw图标 → Restart
```

## 效果

- API调用：从每分钟1次 → 每2小时1次
- 节省：99%的API配额

## 文件

- `fix_feishu_cache.sh` - 自动修复脚本
- `probe.ts.patch` - 补丁文件备份
