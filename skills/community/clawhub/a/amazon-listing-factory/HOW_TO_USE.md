# How to Use

安装或更新 Skill 后：

openclaw gateway restart

检查是否识别成功：

openclaw skills list | grep amazon

如果看到：

amazon-listing-factory

说明安装成功。

飞书中推荐使用 Slash 命令调用：

/amazon_listing_factory 生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图

本地测试命令：

bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh "生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图"

如需自动生图，请先配置 .env 中的图片环境变量，并前往米核获取 KEY：
miheai.com/s/98707
