# ClawHub Skill Monitor

监控并查询 ClawHub 用户发布的 skill 元数据。

## 当前修复后的真实能力

这个 skill 现在基于 **ClawHub 真实公开接口** 工作，而不是模拟数据或猜测接口。

当前可以稳定获取：
- 用户名（ownerHandle）名下的公开 skill 列表
- skill 名称 / display name
- 最新版本
- 发布时间 / 更新时间
- 是否官方
- 是否执行代码
- 简介 summary

当前 **不能保证获取** 的字段（因为 ClawHub 公开 API 目前未暴露）：
- 安装量 installs
- 下载量 downloads
- 用户评分 / stars
- 评论数 / reviews

> 也就是说：该 skill 已修复为“真实可用”，但不会再伪造不存在的公开指标。

## 用法

### 基本查询

```bash
python scripts/clawhub_monitor.py <username>
```

### JSON 输出

```bash
python scripts/clawhub_monitor.py <username> --format json
```

### 文本输出

```bash
python scripts/clawhub_monitor.py <username> --format text
```

### 导出 CSV

```bash
python scripts/clawhub_monitor.py <username> --export skills.csv
```

### 扩大扫描范围

由于当前公开接口没有直接按 ownerHandle 精准过滤的公开端点，本脚本会扫描公开 skill 列表并在本地过滤。
如果目标用户的 skill 较新度不高，可能需要加大扫描范围：

```bash
python scripts/clawhub_monitor.py <username> --max-pages 50 --page-size 50
```

## 输出说明

输出中的这些字段目前会是 `null` 或显示不可用：
- `installs`
- `downloads`
- `stars`
- `reviews`

原因不是脚本 bug，而是 **ClawHub 当前公开 API 未提供这些实时指标**。

## 适用场景

适合：
- 查询某个 ClawHub 用户公开发布了哪些 skill
- 导出该用户 skill 基础信息
- 追踪版本、更新时间和公开元数据

暂不适合：
- 实时精确抓取安装量 / 下载量 / 评分 / 评论数

如果未来 ClawHub 开放这些字段，本 skill 可以直接扩展接入。
