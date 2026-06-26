# Python 示例代码
import requests
import json

url = "https://api.bizyair.cn/w/v1/webapp/task/openapi/create"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
data = {
      "web_app_id": 48084,
      "suppress_preview_output": False,
      "input_values": {
        "2:LoadImage.image": "https://bizyair-prod.oss-cn-shanghai.aliyuncs.com/inputs/20260311/tpYGNhvyaCNAjWKmbOW11WxsM78lXvqS.jpg",
        "19:BizyAir_NanoBananaPro.prompt": "参考我提供的插画风格，使用我提供的大学生AI应用与创业创新教材章节内容，重新提炼内容后做成横版的教材配图，要保证生成的“简体中文不能有乱码，必须文字清晰可见”。教材章节内容如下：\n------------------------------------------------------------\n复盘与产业启示——从代码到柯桥供应链的跨越\n1. 为什么大学生能完成这种量级的开发？\n你看完了上述代码，可能会觉得逻辑繁杂。但在实际的开发过程中，这支大学团队并没有手敲所有的代码。他们充分利用了 AI 编程大模型（如 （如 千问Gwen3.5 或 Claude 4.6 Sonnet）。\n团队的技术合伙人只需撰写详尽的 Markdown 格式的 Prompt 命令文档（如文档中的 @宿舍床帘生成器模拟助手-AI 编程命令.md）。\n当发现历史记录的大图导致 Chrome 插件卡顿时，他不是去查阅复杂的网络优化手册，而是对 AI 说：“历史卡片中，将卡片内的缩略图图片加上阿里云 OSS 缩略图的后缀 ?image_process=format... 原始的 URL 太大了，要刷新好久”。AI 瞬间理解意图，生成了 `BizyAirAPI.getThumbnailUrl` 这个静态方法。这正是 2026 年“工程整合者”的威力。\n2. 打通供应链：“可见即所得”的商业闭环\n这段代码跑通后，插件已经具备了极强的视觉冲击力：大学生随意拍一张自己乱糟糟的宿舍床铺，上传一张淘宝上的布料材质截图，几十秒后，一张完美适配 9:16 比例、2K 高清、呈现莫兰迪色系遮光质感的高铺床帘融合图就跃然屏上。\n但团队的行业合伙人深知，这不能停留在“看图玩具”的阶段。\n在上述架构跑通后，团队拿着这套搭载着 《宿舍床帘生成器》的工具，前往了浙江绍兴柯桥窗帘布艺市场。",
        "19:BizyAir_NanoBananaPro.aspect_ratio": "16:9"
      }
    }

response = requests.post(url, headers=headers, json=data)
result = response.json()
print("生成结果:", result)
