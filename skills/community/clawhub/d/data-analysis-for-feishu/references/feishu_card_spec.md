# 飞书ECharts卡片规范说明

## 官方规范参考
飞书卡片平台ECharts组件官方文档：https://open.feishu.cn/documentation/uQjNz4jM0EjL70k1VNzc

## 支持的ECharts版本
飞书当前支持ECharts 5.x版本的大部分配置，以下为注意事项：

### 不支持的功能
1. 不支持3D图表
2. 不支持自定义JS函数（如formatter中写JS代码）
3. 不支持graphic组件
4. 不支持dataZoom、brush等交互组件
5. 不支持自定义主题

### 支持的交互
1. hover显示tooltip
2. 图例点击切换显示/隐藏
3. 饼图扇区点击高亮

## 卡片尺寸说明
- 推荐高度：400px - 600px
- 宽度默认使用"100%"，自适应卡片宽度
- 移动端会自动适配屏幕尺寸

## 卡片JSON结构
```json
{
    "config": {
        "wide_screen_mode": true // 开启宽屏模式，推荐开启
    },
    "elements": [
        {
            "tag": "markdown",
            "content": "**图表标题**" // 可选，可添加说明文字
        },
        {
            "tag": "echarts_chart",
            "option": {}, // ECharts配置对象
            "width": "100%",
            "height": "400px"
        }
    ]
}
```

## 注意事项
1. ECharts配置中的formatter字段只能使用字符串模板，不能使用JS函数
2. 所有颜色值必须使用十六进制或RGB格式，不能使用颜色名称
3. 不要使用过于复杂的配置，避免渲染性能问题
4. 生成的卡片JSON必须是合法的JSON格式，不能包含注释
5. 中文需要使用UTF-8编码，确保在飞书端正常显示

## 发送卡片到飞书
使用`message`工具发送卡片示例：
```python
import json
card = json.load(open("card.json", "r", encoding="utf-8"))
# 调用message工具发送
{
    "action": "send",
    "channel": "feishu",
    "card": card
}
```
