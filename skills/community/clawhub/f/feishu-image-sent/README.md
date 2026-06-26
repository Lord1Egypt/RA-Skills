# feishu-image-sender

飞书图片发送工具，支持系统截图和本地图片发送到飞书。

## 核心特性
- **系统截图**：截取整个电脑屏幕
- **区域截图**：支持交互式指定截图区域
- **本地图片发送**：发送本地图片文件到飞书
- **智能压缩**：如果图片过大（>5MB），会自动先压缩上传一次，再原图上传一次；小图片则不压缩直接发送。

## 安装与配置
将本技能放置在 OpenClaw 工作区的 `skills/feishu-image-sender` 目录下。

## 使用方法
可以通过 OpenClaw 发送指令：
- "帮我截个全屏并发到飞书"
- "把桌面的 xxx.png 发给飞书"

脚本层面支持：
- `feishu-image-screenshot`：快速截图并发送
- `feishu-image-send <图片路径>`：智能判断大小并发送指定图片
- `feishu-image-interactive`：交互式选择区域截图

详情请参阅 `SKILL.md`。
