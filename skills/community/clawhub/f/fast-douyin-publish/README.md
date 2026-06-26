# 抖音视频发布助手

> 一键抖音登陆, 上传视频到抖音
> 修正自 auto-publisher skill (之前的不可用)

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 playwright
pip install playwright

# 安装浏览器
playwright install chromium
```

### 2. 配置账号

首次运行会自动创建配置文件：
```
config/accounts.json
```

编辑文件，启用抖音（使用二维码登录，无需填写密码）

### 3. 发布视频

```bash
# 手动指定标题和标签
python scripts/auto_publisher.py "video.mp4" --title "我的视频" --tags "AI,科技,创新"

# 无头模式
python scripts/auto_publisher.py "video.mp4" --title "我的视频" --tags "AI,科技" --headless
```

**注意**：`--title` 和 `--tags` 是必填参数。如果用户未提供标题或标签，skill 应根据视频文件名自动生成标题和标签。

---

## 📱 支持的平台

| 平台 | 登录方式 | 标题限制 | 时长限制 |
|------|---------|---------|---------|
| 抖音 | 二维码 | 30 字 | 15 分钟 |

---

## ⚙️ 配置文件说明

### config/accounts.json

```json
{
  "douyin": {
    "enabled": true,        // 是否启用
    "qr_login": true,       // 使用二维码登录
    "notes": "首次需要扫码"
  }
}
```

---

## 📝 常用命令

### 发布视频
```bash
python scripts/auto_publisher.py "video.mp4" --title "我的视频" --tags "AI,科技" --headless
```
---

## 📊 发布记录

发布记录保存在 `config/publish_log.json`

包含：
- 发布时间
- 视频文件
- 标题和标签
- 发布结果

---

## ⚠️ 注意事项

### 首次使用
1. 首次登录需要扫码
2. 扫码后 Cookie 会保存，下次无需重复登录
3. Cookie 有效期约 7-30 天

### 发布频率
- 抖音：建议日更 1-3 条

### 内容规范
- 不要发布违规内容
- 注意版权问题

---

## 🐛 故障排除

### 问题：Playwright 安装失败
```bash
# 解决方法
pip install --upgrade pip
pip install playwright
playwright install chromium
```

### 问题：登录超时
- 检查网络连接
- 手动打开平台网站，确认可以访问
- 重新运行，重新扫码

### 问题：发布失败
- 检查视频格式是否支持
- 检查视频大小是否超限
- 查看浏览器窗口中的错误信息
