# 快速开始 - 微信公众号自动发布

## 5 分钟快速上手

### 1️⃣ 第一次使用 - 登录

```bash
cd scripts
python3 publish.py --login
```

- 浏览器会自动打开
- **用微信扫描二维码**
- 登录后会自动保存 Cookie（~/.wechat_mp/cookies.json）

### 2️⃣ 发布文章（保存草稿测试）

```bash
python3 publish.py \
  --title "我的第一篇文章" \
  --content "这是文章内容，可以包含多个段落

② 第二点：内容
③ 第三点：内容" \
  --draft
```

**预期输出**
```
✅ AI 配图已生成 4 张
✅ 已获取 AI 图 URL
✅ 已选择 AI 配图，进入裁剪步骤
✅ 封面图设置完成
✅ AI 配图已插入正文底部
✅ 已保存为草稿
```

### 3️⃣ 真正发布（不加 --draft）

```bash
python3 publish.py \
  --title "正式发布标题" \
  --content "正文内容"
```

✅ 完成！文章已发布到微信公众号

## 常见用法

### 使用自定义 AI 提示词

```bash
python3 publish.py \
  --title "科技资讯" \
  --content "AI 最新进展..." \
  --ai-prompt "AI,黑科技,未来" \
  --draft
```

### 从文件读取长文本

```bash
python3 publish.py \
  --title "长篇文章" \
  --content-file ~/article.md \
  --draft
```

### 添加摘要和启用赞赏

```bash
python3 publish.py \
  --title "文章标题" \
  --content "文章内容" \
  --abstract "这是文章摘要，最多120字" \
  --reward \
  --draft
```

### 自动关闭留言

```bash
python3 publish.py \
  --title "标题" \
  --content "内容" \
  --no-comment \
  --draft
```

## 参数速查表

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--title` | ✅ | 文章标题 | `--title "标题"` |
| `--content` | ⚠️* | 文章内容 | `--content "内容"` |
| `--content-file` | ⚠️* | 从文件读取 | `--content-file ~/file.txt` |
| `--ai-prompt` | ❌ | AI 配图提示词 | `--ai-prompt "AI,猫,萨克斯"` |
| `--draft` | ❌ | 保存草稿 | (无需值) |
| `--no-comment` | ❌ | 关闭留言 | (无需值) |
| `--reward` | ❌ | 启用赞赏 | (无需值) |
| `--abstract` | ❌ | 摘要 | `--abstract "简介..."` |
| `--cover` | ❌ | 降级封面 | `--cover ~/img.jpg` |

*\*`--content` 和 `--content-file` 必须二选一*

## 故障排查

### Q: 提示「未登录」？
A: 重新运行登录命令：
```bash
python3 publish.py --login
```

### Q: AI 配图生成超时？
A: 这是网络问题，脚本会自动降级使用图片库。稍后重试或检查网络。

### Q: 如何查看调试截图？
A: 发布失败时会保存截图到 `/tmp/`：
- `mp_debug_title.png` - 标题填写失败
- `mp_debug_publish.png` - 发布失败
- `mp_after_publish.png` - 发布后的状态

### Q: 如何清除登录状态？
A: 删除 Cookie 文件后重新登录：
```bash
rm ~/.wechat_mp/cookies.json
python3 publish.py --login
```

## 文本格式

### 支持的特殊格式

```
① 这是一级标题（加粗）
② 这也是一级标题
③ 还有很多

普通段落文本
多行也可以
会自动换行处理

空行会被保留
```

自动转换为：
- `①②③` 开头的行 → 加粗标题
- 普通文本 → 正常段落
- 空行 → 段落间距

## 工作流程简图

```
python3 publish.py --title "标题" --content "内容"
           ↓
    登录检查（自动使用 Cookie）
           ↓
    填写标题 & 正文
           ↓
    设置 AI 配图封面
    （生成 4 张，选最好的）
           ↓
    将 AI 图插入正文底部
           ↓
    设置摘要/留言/赞赏
           ↓
    [--draft] 保存为草稿
    或 [无参数] 直接发布
           ↓
    ✅ 完成
```

## 进阶技巧

### 批量发布

创建 `batch_publish.sh`：
```bash
#!/bin/bash
python3 publish.py --title "文章1" --content "内容1"
python3 publish.py --title "文章2" --content "内容2"
python3 publish.py --title "文章3" --content "内容3"
```

运行：
```bash
chmod +x batch_publish.sh
./batch_publish.sh
```

### 定时发布（cron）

编辑 crontab：
```bash
crontab -e
```

添加定时任务（每天下午 3 点发布）：
```
0 15 * * * cd /path/to/scripts && python3 publish.py --title "$(date +\%Y-\%m-\%d)" --content "今日内容"
```

## 需要帮助？

查看完整文档：参考根目录的 `SKILL.md`
