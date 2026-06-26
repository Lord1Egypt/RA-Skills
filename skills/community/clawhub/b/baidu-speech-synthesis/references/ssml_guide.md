# 百度语音合成 SSML 指南

## 什么是 SSML？
SSML（Speech Synthesis Markup Language）是一种基于XML的标记语言，用于控制语音合成的各种参数，如音色、语速、音调、停顿等。

## 百度 SSML 支持
百度智能云语音合成 API 从 V5.5 开始支持 SSML，通过 `per=511` 参数启用多音色模式。

### 基本结构
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <!-- 内容 -->
</speak>
```

## 核心标签

### `<voice>` - 音色控制
```xml
<voice name="度小宇">文本内容</voice>
```
**属性：**
- `name`: 音色名称，如 "度小宇"、"度小美" 等
- `spd`: 语速 (0-15, 默认5)
- `pit`: 音调 (0-15, 默认5)  
- `vol`: 音量 (0-15, 默认5)

**示例：**
```xml
<voice name="度小美" spd="6" pit="5" vol="5">欢迎使用百度语音合成</voice>
```

### `<break>` - 停顿控制
```xml
<break time="500ms"/>
```
**属性：**
- `time`: 停顿时间，如 "300ms"、"1s"、"0.5s"

**示例：**
```xml
<voice name="度小宇">第一句话</voice>
<break time="300ms"/>
<voice name="度小美">第二句话</voice>
```

### `<prosody>` - 韵律控制（百度部分支持）
```xml
<prosody rate="fast" pitch="high">快速高音调文本</prosody>
```

## 完整示例

### 示例1：简单对话
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="度小宇">小明：你好，小红！</voice>
  <break time="300ms"/>
  <voice name="度小美">小红：你好，小明！今天天气真好啊。</voice>
  <break time="500ms"/>
  <voice name="度小宇">是的，我们一起去公园吧。</voice>
</speak>
```

### 示例2：带情感的故事讲述
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="度逍遥" spd="4">从前有座山，山里有座庙。</voice>
  <break time="1s"/>
  <voice name="度丫丫" spd="7" pit="6">庙里有个小和尚！他很快乐！</voice>
  <break time="800ms"/>
  <voice name="度米朵" spd="3" pit="4">可是有一天，他迷路了...</voice>
</speak>
```

### 示例3：新闻播报风格
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="度博文" spd="5" pit="4">北京时间今天上午十点，重要会议在北京召开。</voice>
  <break time="500ms"/>
  <voice name="度小美" spd="5">会议强调了科技创新在经济发展中的关键作用。</voice>
</speak>
```

## 对话文本转 SSML 规则

### 输入格式
```
小明：你好吗？
小红：我很好，谢谢！
老师：同学们，请安静。
```

### 转换规则
1. 每行以 "角色：" 开头
2. 自动匹配音色映射
3. 根据标点自动添加停顿：
   - 句号、感叹号、问号：500ms
   - 逗号、分号：300ms
   - 换行：300ms

### 自动转换示例
**输入文本：**
```
小明：今天我们去哪里？
小红：去公园吧！
小明：好啊，我带上足球。
```

**生成的 SSML：**
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="度小宇">小明：今天我们去哪里？</voice>
  <break time="500ms"/>
  <voice name="度小美">小红：去公园吧！</voice>
  <break time="500ms"/>
  <voice name="度小宇">小明：好啊，我带上足球。</voice>
</speak>
```

## 限制与注意事项

### 长度限制
- SSML 文本最大长度：1024 字节（UTF-8编码）
- 超过限制需要拆分为多个请求

### 标签嵌套限制
```xml
<!-- 正确 -->
<voice name="度小美">
  <break time="300ms"/>
  文本内容
</voice>

<!-- 错误（voice嵌套voice） -->
<voice name="度小美">
  <voice name="度小宇">文本</voice>
</voice>
```

### 特殊字符处理
- XML 特殊字符需要转义：
  - `&` → `&amp;`
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `"` → `&quot;`
  - `'` → `&apos;`

### 性能建议
1. **批量处理**：多个短对话合并为一个SSML请求
2. **缓存结果**：相同内容可缓存音频文件
3. **预验证**：发送前验证SSML格式和长度

## 错误处理

### 常见错误
1. **SSML格式错误**：XML结构不正确
2. **长度超限**：超过1024字节
3. **不支持标签**：使用百度不支持的SSML标签
4. **音色不存在**：指定的音色名称错误

### 调试建议
```python
# 验证SSML格式
from dialogue_formatter import DialogueFormatter

formatter = DialogueFormatter()
is_valid, message = formatter.validate_ssml(ssml_text)
print(f"验证结果: {message}")

# 如果超长，自动拆分
if not is_valid and "超过1024字节" in message:
    segments = formatter.split_long_ssml(ssml_text)
    print(f"拆分为 {len(segments)} 个片段")
```

## 最佳实践

### 1. 对话设计原则
- 每个角色说话不宜过长（建议<20字）
- 合理使用停顿增强自然感
- 根据场景选择合适音色

### 2. 参数调节技巧
- **语速(spd)**: 5为正常，新闻6-7，故事4-5
- **音调(pit)**: 5为正常，儿童6-7，老人3-4
- **音量(vol)**: 5为正常，重要内容6-7

### 3. 性能优化
- 使用SSML模式减少API调用次数
- 本地缓存常用音频片段
- 异步处理批量任务

## 扩展阅读
- [百度SSML官方文档](https://ai.baidu.com/ai-doc/SPEECH/Tk4o0bmio#ssml)
- [W3C SSML标准](https://www.w3.org/TR/speech-synthesis/)
- [语音合成最佳实践](https://cloud.baidu.com/doc/SPEECH/s/zk4o0bixe)