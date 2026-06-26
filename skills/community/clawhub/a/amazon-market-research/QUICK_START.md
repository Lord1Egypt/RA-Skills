# Quick Start

安装或更新 Skill 后先执行：

openclaw gateway restart

检查是否已识别：

openclaw skills list | grep amazon

首次运行：

bash ~/.openclaw/workspace/skills/amazon-market-research/run.sh "调研一下午餐盒在美国Amazon市场值不值得做"

飞书中推荐调用方式：

/amazon-market-research 调研一下午餐盒在美国Amazon市场值不值得做

首次使用前，请先填写 .env 中的模型配置。