# Intent Routing

## 文本问答触发

- 问问Gemini xxx
- 去Gemini帮我问 xxx
- 让Gemini总结 xxx

动作：走文本问答链路。

## 生图触发

- 给我画一只小猫
- 生图：未来城市海报
- nano banana 风格来一张

动作：走生图链路，并先反馈“正在绘图中”。

## 混合请求

例如：
- 先问Gemini这个产品定位，再出一张封面图

动作：拆成两步执行，先问答后生图。
