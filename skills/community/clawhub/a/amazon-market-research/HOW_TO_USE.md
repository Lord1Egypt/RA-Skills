# How to Use

安装或更新 Skill 后：

openclaw gateway restart

检查是否识别成功：

openclaw skills list | grep amazon

如果看到：

amazon-market-research

说明安装成功。

飞书中推荐使用 Slash 命令调用：

/amazon-market-research 调研一下午餐盒在美国Amazon市场值不值得做

本地测试命令：

bash ~/.openclaw/workspace/skills/amazon-market-research/run.sh "调研一下午餐盒在美国Amazon市场值不值得做"

首次使用前，请先配置 .env 中的模型环境变量。