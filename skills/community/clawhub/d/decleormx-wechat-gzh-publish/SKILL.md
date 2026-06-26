# 📱 微信公众号 AI 配图自动发布工具

**Skill ID**: `decleormx_wechat_gzh_publish`

自动化微信公众号文章发布流程，支持 AI 动态生成配图（既作为封面，又插入正文），提高内容发布效率。

## 功能特性

✨ **核心功能**
- 🔐 自动登录（首次扫码，后续复用 Cookie）
- ✍️ 自动填写标题、正文
- 🎨 **AI 配图双用**：自动生成图片作为封面 + 插入正文底部
- 📸 失败降级至图片库
- 💾 支持保存草稿或直接发布
- 📋 支持自定义摘要、留言、赞赏设置

🎯 **AI 配图特点**
- 每次生成 4 张不同的 AI 图片
- 生成时间约 14 秒
- 提示词可自定义（默认：AI，萨克斯，猫）
- 自动拍摄选择质量最好的一张
- 失败自动降级到图片库

## 安装

### 方式一：直接使用（推荐）

```bash
# 在 WorkBuddy 中唤起该 Skill 即可使用
```

### 方式二：手动配置

1. **环境要求**
   - Python 3.8+
   - Playwright（自动安装）
   - 微信公众号账号

2. **首次使用 - 登录**
   ```bash
   python3 publish.py --login
   ```
   - 浏览器窗口会打开
   - 用微信扫描二维码
   - 登录后 Cookie 会自动保存到 `~/.wechat_mp/cookies.json`

## 使用方法

### 基础发布

```bash
python3 publish.py \
  --title "我的文章标题" \
  --content "这是文章内容"
```

**输出示例**
```
🖼️  设置封面（AI 配图提示词: AI，萨克斯，猫）
   ✅ AI 配图生成中...
   ✅ AI 配图已生成 4 张
   ✅ 已获取 AI 图 URL（首字 https://...）
   ✅ 已选择 AI 配图，进入裁剪步骤
✅ 封面图设置完成
✅ AI 配图已插入正文底部
✅ 已保存为草稿
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--title` | **必需** - 文章标题 | `--title "AI时代的思考"` |
| `--content` | **必需** - 文章内容（纯文本） | `--content "今天天气不错..."` |
| `--content-file` | 从文件读取正文 | `--content-file ~/article.txt` |
| `--ai-prompt` | AI 配图提示词 | `--ai-prompt "AI,城市,夜景"` |
| `--draft` | 保存为草稿（不发布） | 仅需加这个参数 |
| `--cover` | 本地封面图（作为降级方案） | `--cover ~/cover.jpg` |
| `--abstract` | 文章摘要（最多120字） | `--abstract "简介..."` |
| `--no-comment` | 关闭留言（默认开启） | 仅需加这个参数 |
| `--reward` | 开启赞赏（需先声明原创） | 仅需加这个参数 |

### 使用示例

**1. 保存草稿测试**
```bash
python3 publish.py \
  --title "测试标题" \
  --content "这是测试内容" \
  --draft
```

**2. 自定义 AI 提示词发布**
```bash
python3 publish.py \
  --title "科技前沿" \
  --content "最新 AI 技术分析..." \
  --ai-prompt "AI,机器学习,代码" \
  --abstract "深度分析最新 AI 技术" \
  --reward
```

**3. 从文件读取长文本**
```bash
python3 publish.py \
  --title "长篇文章" \
  --content-file ~/long_article.md \
  --ai-prompt "文章主题相关的关键词" \
  --draft
```

**4. 使用本地图片作为降级方案**
```bash
python3 publish.py \
  --title "标题" \
  --content "内容" \
  --cover ~/my_cover.jpg \
  --draft
```

## 工作流程

### 封面逻辑流程图

```
开始发布
  ↓
1️⃣ 填写标题
  ↓
2️⃣ 填写正文（HTML 富文本）
  ↓
3️⃣ 设置封面
  ├─ 点「AI 配图」
  ├─ 输入提示词（默认：AI，萨克斯，猫）
  ├─ 点「开始创作」
  ├─ 轮询等待生成（最多 90 秒）
  ├─ 拿下第一张图的 URL ⭐
  ├─ 点「使用」
  ├─ 裁剪确认
  └─ ❌ 如果失败
      └─ 自动降级：从图片库选第一张
  ↓
4️⃣ 将 AI 图插入正文底部 ⭐
  ↓
5️⃣ 填写摘要（可选）
  ↓
6️⃣ 设置留言/赞赏（可选）
  ↓
7️⃣ 保存草稿 或 直接发布
  ↓
完成 ✅
```

## Cookie 管理

- **保存位置**：`~/.wechat_mp/cookies.json`
- **有效期**：通常 30 天左右
- **过期处理**：自动跳转登录，用微信重新扫码
- **清除**：`rm ~/.wechat_mp/cookies.json` 后重新 `--login`

## 故障排查

### 常见问题

**Q: 第一次运行总是要登录？**
A: 首次登录后 Cookie 会保存到 `~/.wechat_mp/cookies.json`，后续会自动使用。如果还是提示登录，检查：
- Cookie 文件是否存在：`ls -l ~/.wechat_mp/cookies.json`
- 文件是否可读：`cat ~/.wechat_mp/cookies.json`
- 尝试重新登录：`python3 publish.py --login`

**Q: AI 配图生成超时？**
A: 网络或腾讯云 API 问题。脚本会自动降级使用图片库。也可以：
- 检查网络连接
- 稍后重试
- 手动指定本地图片：`--cover ~/backup.jpg`

**Q: 图片URL提取失败？**
A: 这可能是公众号页面 DOM 结构变化。建议：
- 运行 `python3 inspect_ai_cover.py` 检查最新的 DOM 选择器
- 更新脚本中的 CSS 选择器

**Q: 如何获取调试截图？**
A: 发布失败后会自动保存截图：
- 标题填写失败：`/tmp/mp_debug_title.png`
- 发布失败：`/tmp/mp_debug_publish.png`
- 发布后：`/tmp/mp_after_publish.png`

## 文件结构

```
decleormx_wechat_gzh_publish/
├── SKILL.md              # 本说明文档
├── scripts/
│   ├── publish.py        # 主发布脚本
│   ├── inspect_*.py      # 调试脚本（可选）
│   └── requirements.txt   # Python 依赖
└── README.md             # 快速开始
```

## 技术细节

### HTML 内容转换
- 纯文本行自动转换为 `<p>` 标签
- 检测 ① ② ③ 开头的行作为标题加粗
- 保留行间距和样式

### ProseMirror 编辑器
- 直接操作 DOM：`document.querySelector('.ProseMirror')`
- 注入 HTML 后触发 input 事件
- AI 图片插入到 `.innerHTML` 末尾

### Playwright 自动化
- 使用 Chromium 浏览器
- Headless 模式支持（可改为有界面调试）
- 所有点击通过 JS evaluate() 执行（避免弹窗遮罩）

## 更新日志

**v1.0 (2026-03-18)**
- ✨ 首版发布
- 🎨 AI 配图双用（封面 + 正文）
- 💾 自动 Cookie 管理
- 🔄 失败自动降级

## 许可证

个人使用脚本，仅供学习参考。

## 支持

遇到问题？
1. 检查参数是否正确（`--title` 和 `--content` 必需）
2. 查看控制台输出中的 ⚠️ 警告信息
3. 检查 `/tmp/mp_debug_*.png` 的调试截图
4. 保证网络连接正常
5. 尝试重新登录：`python3 publish.py --login`
