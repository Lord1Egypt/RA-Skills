# Quick Start

安装或更新 Skill 后先执行：

openclaw gateway restart

检查是否已识别：

openclaw skills list | grep amazon

本地首次运行：

bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh

飞书中推荐调用方式：

/amazon_listing_factory 生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图

本地正式测试：

bash ~/.openclaw/workspace/skills/amazon-listing-factory/run.sh "生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图"
