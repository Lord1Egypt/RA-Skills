# Cooling Circulating Water Expert

提供冷却循环水系统全流程设计、运行优化与阻垢防腐方案

## 类型

Agent 型（单个 AI 专家）

## 功能

系统提供冷却循环水系统设计、药剂配方推荐、运行优化建议及报告生成

## 使用示例

- 请为某工业园区设计冷却循环水系统，要求节能降耗。
- 如何在冷却水中实现无磷处理并防止结垢？
- 请给出大规模循环水系统的阻垢剂配方与投加策略。

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

将专家包目录放到专家目录下：

```
C:\Users\36977\.workbuddy\plugins\marketplaces\my-experts\plugins/cooling-circulating-water-expert/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
zip -r cooling-circulating-water-expert.zip cooling-circulating-water-expert/
```
