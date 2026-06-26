# 1-Click WOA 常见问题排查

---

## 错误：Token 获取失败

**症状：**
```
Token error: {'errcode': 40013, 'errmsg': 'invalid appid'}
```

**原因：** AppID 格式不正确或与 AppSecret 不匹配

**解决：**
1. 确认 AppID 是否以 `wx` 开头（例：`wx1234567890`）
2. 确认 AppSecret 没有多余的空格或换行
3. 重新从微信公众平台复制

---

## 错误：图片上传失败

**症状：**
```
media_id: FAILED {'errcode': 40007, 'errmsg': 'media_id invalid'}
```

**原因：** 图片格式不被支持或文件损坏

**解决：**
1. 将图片转换为 PNG 或 JPG 格式
2. 确保图片文件未损坏（用图片查看器能正常打开）
3. 封面图尺寸需 ≥ 900×383 px

---

## 错误：草稿提交成功但预览乱码

**症状：** 草稿箱里文章正文显示 `\u4e00\u4e00` 这样的 Unicode 转义序列

**原因：** 微信草稿 API 的中文编码 bug

**解决：**
1. Skill 会自动检测并切换到 **HTML Fallback 模式**
2. 自动生成一个 `article_fallback.html` 文件
3. 下载 HTML 文件，用电脑浏览器打开
4. 全选内容（Ctrl+A）→ 复制（Ctrl+C）
5. 粘贴到微信公众号后台编辑器（注意：用**格式粘帖**或**纯文本粘帖**）

---

## 错误：access_token 过期

**症状：**
```
{'errcode': 42001, 'errmsg': 'access_token expired'}
```

**原因：** Token 有效期2小时，超时未使用

**解决：**
1. 重新运行发布命令，Skill 会自动获取新 Token
2. 若频繁过期，检查系统时间是否正确

---

## 问题：没有永久素材上传权限

**症状：**
```
{'errcode': 41006, 'errmsg': 'api freq out of limit, maybe'}
```

**原因：** 订阅号无法上传永久素材（只有服务号可以）

**解决：**
- 使用服务号
- 或改用临时素材接口（有限制）

---

## 问题：图片数量不足

**症状：**
```
Not all images uploaded, exiting
```

**原因：** 指定的图片文件不存在

**解决：**
1. 至少准备1张封面图（cover.png）
2. 确保文件名完全匹配（区分大小写）
3. 图片放在配置指定的 `image_dir` 目录

---

## 问题：clwbot 上传文件失败

**症状：**
```
lightclaw_upload_file: access denied
```

**原因：** HTML Fallback 文件超过上传限制

**解决：**
1. 将 HTML 文件通过邮件发送
2. 或上传到云盘（腾讯云/阿里云）后分享链接

---

## 调试模式

查看详细执行日志：

```bash
cd ~/.openclaw/agents/gzh-assistant/skills/1-click-woa/scripts
python3 -v publish.py
```

添加 `-v` 参数查看每一步的详细输出。
