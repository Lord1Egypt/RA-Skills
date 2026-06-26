# Amazon Market Research

Amazon Market Research 用于快速生成 Amazon 市场调研报告。

## 当前输出结构

1. 飞书直接展示完整 18 步市场调研报告
2. 本地自动保存 markdown 报告文件

## 首次安装或更新后

执行：

openclaw gateway restart

然后检查是否识别成功：

openclaw skills list | grep amazon

如果看到：

amazon-market-research

说明 Skill 已被 OpenClaw 正确识别。

## 推荐飞书调用方式

/amazon-market-research 调研一下午餐盒在美国Amazon市场值不值得做

## 本地测试

bash ~/.openclaw/workspace/skills/amazon-market-research/run.sh "调研一下午餐盒在美国Amazon市场值不值得做"

## 说明

本版本已针对飞书长文本展示做优化：
- 优先使用 answer 字段
- 直接输出完整 18 条，不再前置摘要
- 标题采用更稳定的 【1. 模块名】 格式