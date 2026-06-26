# feishu-emoji - 飞书表情包发送技能

**版本**：1.0  
**创建时间**：2026-03-16  
**依赖**：无（仅需 curl 和 message 工具）  
**数据源**：fabiaoqing.com（免费表情包网站）

---

## 🎯 技能目标

让 OpenClaw AI 能够在飞书聊天中发送内联表情包图片，增强对话表达力。

---

## 📋 核心原理

### 关键发现
- ✅ **成功路径**：`/home/admin/.openclaw/media/inbound/` → 飞书显示为内联图片
- ❌ **失败路径**：`/tmp/` → 飞书显示为附件链接（📎）

### 技术要点
1. **图片必须保存到 OpenClaw 媒体目录**才能被飞书识别为内联图片
2. **CDN 防盗链**：fabiaoqing.com 的图片需要 Referer 头才能访问
3. **使用 message 工具**：`media` 参数指向媒体目录中的文件

---

## 🛠️ 使用方式

### 方法一：直接发送（推荐）

当用户请求发送表情包时，执行以下步骤：

```bash
# 1. 下载表情包到媒体目录（带 Referer 头）
curl -sL -H "Referer: https://fabiaoqing.com/" "图片 URL" -o /home/admin/.openclaw/media/inbound/emoji_<关键词>.jpg

# 2. 使用 message 工具发送
message(action="send", message="你的回复文字", media="/home/admin/.openclaw/media/inbound/emoji_<关键词>.jpg")
```

### 方法二：调用 API（需要先启动服务）

如果已部署表情包 API 服务（emoji_server.py）：

```bash
# 1. 获取表情包信息
curl -s "http://localhost:8000/emoji?keyword=大学生"

# 2. 下载 proxy_url 到媒体目录
curl -sL "http://localhost:8000/image?url=<encoded_url>" -o /home/admin/.openclaw/media/inbound/emoji_xxx.jpg

# 3. 发送
message(action="send", message="表情包来了！", media="/home/admin/.openclaw/media/inbound/emoji_xxx.jpg")
```

---

## 📦 表情包来源

### 推荐网站
- **fabiaoqing.com** - 免费表情包，无需登录
- 搜索 URL 格式：`https://fabiaoqing.com/search/bqb/keyword/<关键词>/type/bq/page/1.html`

### 热门关键词
- 日常：好的、收到、谢谢、OK、没问题
- 情绪：开心、难过、生气、惊讶、无语
- 场景：打工人、大学生、摸鱼、加班、开会
- 动物：猫猫、狗狗、熊猫、兔子

### 图片 URL 特征
- 通常来自第三方 CDN（如 `img.soutula.com`）
- 需要 Referer: `https://fabiaoqing.com/` 才能访问
- 格式多为 `.jpg`，大小 10-50KB

---

## 🔧 完整示例

### 示例 1：发送"收到"表情包

```bash
# 下载
curl -sL -H "Referer: https://fabiaoqing.com/" \
  "https://img.soutula.com/bmiddle/006APoFYly1glojj7wfc5j306o06odg1.jpg" \
  -o /home/admin/.openclaw/media/inbound/emoji_shoudao.jpg

# 发送
message(action="send", \
  message="收到！马上处理～", \
  media="/home/admin/.openclaw/media/inbound/emoji_shoudao.jpg")
```

### 示例 2：发送"猫猫"表情包

```bash
# 先获取表情包信息（可选）
curl -s "https://fabiaoqing.com/search/bqb/keyword/猫猫/type/bq/page/1.html" | \
  grep -o 'data-original="[^"]*"' | head -1

# 下载并发送
curl -sL -H "Referer: https://fabiaoqing.com/" \
  "https://img.soutula.com/bmiddle/xxx.jpg" \
  -o /home/admin/.openclaw/media/inbound/emoji_maomao.jpg

message(action="send", \
  message="猫猫表情包来了！🐱", \
  media="/home/admin/.openclaw/media/inbound/emoji_maomao.jpg")
```

---

## ⚠️ 注意事项

### 版权
- 表情包均来自互联网，版权归原作者所有
- **请勿商用**
- 个人聊天使用通常没问题

### 技术限制
- 图片链接可能失效（第三方 CDN）
- 建议控制调用频率（避免被网站封禁）
- 飞书图片发送仅限媒体目录内的文件

### 文件管理
- 建议命名规范：`emoji_<关键词>.jpg`
- 定期清理旧文件（避免占用过多空间）
- 单个文件通常 10-50KB

---

## 🧪 测试清单

安装后测试以下关键词：
- [ ] 好的
- [ ] 收到
- [ ] 谢谢
- [ ] 猫猫
- [ ] 打工人

确保图片能正常显示为内联图片（不是附件链接）。

---

## 📁 文件结构

```
skills/feishu-emoji/
├── SKILL.md          # 本说明文件
└── (可选)
    ├── emoji_sender.py    # Python 发送脚本
    └── emoji_keywords.json # 常用关键词映射表
```

---

## 🚀 进阶功能（可选）

### 1. 关键词映射表
创建 `emoji_keywords.json` 存储常用表情包 URL：
```json
{
  "收到": "https://img.soutula.com/bmiddle/xxx.jpg",
  "好的": "https://img.soutula.com/bmiddle/yyy.jpg",
  "猫猫": "https://img.soutula.com/bmiddle/zzz.jpg"
}
```

### 2. 随机表情包
支持发送随机表情包：
```bash
# 从关键词列表随机选一个
keywords=("好的" "收到" "谢谢" "OK")
random_keyword=${keywords[$RANDOM % ${#keywords[@]}]}
```

### 3. 表情包 API 服务
部署完整 API 服务参考：
- `/home/admin/.openclaw/workspace/emoji_server.py`
- `/home/admin/.openclaw/workspace/README_EMOJI_API.md`

---

## 💡 使用场景

- ✅ 日常聊天增强表达
- ✅ 工作群活跃气氛
- ✅ 回复确认（收到/好的）
- ✅ 情绪表达（开心/无语/震惊）
- ❌ 正式公文/严肃场合
- ❌ 商业用途

---

**Happy Emoji Sending! 🎉**
