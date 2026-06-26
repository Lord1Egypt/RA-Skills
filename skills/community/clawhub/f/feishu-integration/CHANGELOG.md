# 飞书消息解析功能扩展完成

## 📦 版本历史

### v1.1.0 (2026-03-02)

**新增功能**：
- ✅ 结构化输出支持（`--format json`）
- ✅ 返回 images、mentions、links 列表
- ✅ 支持 `elements` 格式的富文本（新格式）
- ✅ 命令行参数解析（argparse）

**修复**：
- 🐛 修复 `elements` 格式无法解析的问题
- 🐛 修复结构化数据提取

### v1.0.0 (2026-03-02)

**初始版本**：

### 核心模块
1. **scripts/feishu-message-parser.py** - 消息解析器（Python）
   - 支持 text、post、interactive、image 类型
   - 完整的富文本标签支持
   - OCR 图片识别集成

2. **scripts/feishu-ocr.py** - OCR 独立模块
   - 飞书 OCR API 封装
   - 图片文字识别

### 文档
3. **references/message-parsing.md** - 完整使用文档
   - API 参考
   - 示例代码
   - 错误处理

### 示例
4. **examples/parse_text.sh** - 纯文本解析示例
5. **examples/parse_rich_text.sh** - 富文本解析示例
6. **examples/ocr_image.sh** - OCR 识别示例

### 参考代码
7. **reference-feishu-message/** - autogame-17 的实现参考
8. **reference-feishu-common/** - 公共库参考

## ✅ 功能清单

### 消息类型支持
- [x] 纯文本消息（text）
- [x] 富文本消息（post）
- [x] 交互式卡片（interactive）
- [x] 图片消息 + OCR（image）
- [x] 引用回复消息

### 富文本标签支持
- [x] `text` - 纯文本
- [x] `lark_md` - Markdown 内容
- [x] `at` - @提及
- [x] `a` - 链接
- [x] `img` - 图片

## 🚀 快速使用

### 命令行
```bash
# 获取 token
TOKEN=$(bash ~/mo-hub/skills/feishu-integration/scripts/feishu-auth.sh get)

# 解析消息
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-message-parser.py \
  "$TOKEN" \
  '{"msg_type":"text","body":{"content":"{\"text\":\"Hello\"}"}}'

# OCR 识别
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-ocr.py \
  "img_v3_xxx" \
  "$TOKEN"
```

### Python API
```python
from feishu_message_parser import FeishuMessageParser

parser = FeishuMessageParser(tenant_token="your_token")
result = parser.parse(message_data)
print(result)
```

## 📚 学习来源

1. **飞书官方教程**：https://uniquecapital.feishu.cn/docx/BZTvd4SMSo6OzsxodHnckHh8nZb
2. **autogame-17 实现**：/tmp/openclaw-skills/skills/autogame-17/feishu-message/
3. **OpenClaw 源码**：~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/extensions/feishu/src/bot.ts

## 🔧 技术细节

### 解析流程
1. 识别消息类型（msg_type）
2. 提取 body.content（JSON 字符串）
3. 解析 JSON 获取内容块
4. 遍历内容块，处理各种标签
5. 返回纯文本结果

### OCR 流程
1. 提取 image_key
2. 调用飞书 OCR API
3. 解析返回的文字数组
4. 拼接成完整文本

## 📝 测试结果

### 纯文本
```bash
$ bash examples/parse_text.sh
Hello World
```

### 富文本
```bash
$ bash examples/parse_rich_text.sh
# 测试标题

第一行文本@张三
**粗体内容**
```

## 🎯 下一步

### 短期优化
- [ ] 添加更多富文本标签支持（表格、代码块等）
- [ ] 性能优化（批量解析、缓存）
- [ ] 错误处理增强

### 长期规划
- [ ] 提交 PR 到 OpenClaw 官方（修复 bot.ts）
- [ ] 发布到 ClawHub 技能市场
- [ ] 添加单元测试

## 🔗 相关文件

- SKILL.md - 已更新，添加消息解析说明
- references/message-parsing.md - 完整文档
- examples/ - 示例脚本

## 📞 联系

如有问题，请查看：
- 飞书开放平台文档：https://open.feishu.cn/document/
- OpenClaw 文档：https://docs.openclaw.ai/
