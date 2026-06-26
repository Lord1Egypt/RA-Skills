# Amazon Listing Factory

Amazon Listing Factory 用于快速生成 Amazon Listing 初稿，包括：

- 标题
- 五点
- 图组规划
- 图片 Prompt
- 视频脚本

如果已配置图片环境，还会继续自动生图。

安装或更新 Skill 后，请先执行：

openclaw gateway restart

然后检查是否识别成功：

openclaw skills list | grep amazon

如果看到：

amazon-listing-factory

说明 Skill 已被 OpenClaw 正确识别。

推荐在飞书中使用 Slash 命令调用：

/amazon_listing_factory 生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图

本地测试：

bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh "生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图"
