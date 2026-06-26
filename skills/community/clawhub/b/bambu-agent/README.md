🚀 Bambu Nebula Console (OpenClaw Skill)
Bambu Nebula Console 是一款专为 OpenClaw 设计的智能 3D 打印农场监控 Skill。它结合了极简的 Gemini 风格 Web 界面、实时 MQTT 数据流以及 AI Agent 自动诊断功能。

✨ 核心特性
农场级监控：支持同时管理多台拓竹 (Bambu Lab) 打印机。

RAG 状态指示灯：红（异常）、黄（工作中）、绿（空闲）三色灯，一眼掌握全场动态。

Gemini 风格 UI：极简深色模式，可视化 AMS 耗材系统与打印时间轴。

Agent 驱动：支持 OpenClaw 语音交互，自动播报进度并实时预警打印故障。

配置向导：无需修改代码，通过命令行轻松添加或删除设备。

🛠️ 快速上手
1. 环境准备
确保你的电脑（建议 RTX 30系列或以上主机）已安装 Python 3.8+。

在项目根目录下运行以下命令安装必要依赖：

Bash
pip install -r requirements.txt
2. 第一次启动（配置向导）
在终端运行主程序：

Bash
python main.py
程序会自动检测到缺失配置文件，并引导你进入 配置向导。请按照提示输入以下信息：

备注名称：如“一号机”

设备型号：如 P1S, X1C

局域网 IP：打印机的内网地址

访问码 (Access Code)：在打印机屏幕设置中查看

序列号 (SN)：打印机的唯一识别码

配置完成后，信息将自动保存在 config.json 中。

3. 访问控制台
启动成功后，打开浏览器访问：
👉 http://localhost:5000

🤖 与 OpenClaw 联动
本 Skill 已深度适配 OpenClaw 的 AI Agent 接口。你可以尝试以下指令：

查询进度：“嘿 OpenClaw，看看农场现在的进度怎么样？”

异常诊断：“为什么二号机亮红灯了？”

任务总结：“今天上午有哪些打印任务完成了？”

📁 文件结构说明
main.py: 后端服务核心，处理 MQTT 集群连接与 Web API。

templates/index.html: 前端界面，负责 Gemini 风格的渲染与状态灯动画。

config.json: 存储你的打印机配置信息（请勿泄露给他人）。

skill.json: OpenClaw 插件定义文件。

⚠️ 注意事项
局域网要求：运行本程序的电脑必须与打印机处于同一局域网。

Bambu Studio 兼容：本 Skill 使用局域网 MQTT 协议，与 Bambu Studio 可同时运行，互不干扰。

安全性：config.json 包含你的打印机访问密钥，请确保该文件在本地安全存放。

🤝 贡献与反馈
如果你在农场管理过程中有更好的 UI 创意或动作逻辑建议，欢迎联系作者。