# 迁移指南

## 最小系统要求
- Python 3.8+
- 能联网
- 有 SiliconFlow 账号（免费注册：https://siliconflow.cn）

## 一键迁移步骤

### 1. 复制 skill 目录
```bash
cp -r douyin-learning-pipeline /path/to/new/system/
```

### 2. 运行环境自检
```bash
cd douyin-learning-pipeline
bash scripts/check_env.sh
```

### 3. 配置
```bash
python3 scripts/setup_config.py
```

按提示输入：
- SiliconFlow API Key（必需）
- 飞书文档 token（可选）

### 4. 配置抖音 Cookie
```bash
vim assets/douyin-downloader/config.yml
```

按提示填入从浏览器获取的 Cookie。

### 5. 开始使用
发送抖音链接给助手即可。

---

## 手动配置说明

### SiliconFlow API Key
两种方式：
1. 环境变量：`export SILICONFLOW_API_KEY='your-key'`
2. 本地配置：`local/config.json` 中的 `siliconflow_api_key`

### 抖音 Cookie
配置文件：`assets/douyin-downloader/config.yml`

需要填写的字段：
- `msToken`
- `ttwid`
- `odin_tt`
- `passport_csrf_token`
- `sid_guard`

获取方法：
1. 浏览器打开抖音网页版并登录
2. F12 → Application → Cookies
3. 复制对应值

### 飞书文档
可选。如需自动写入飞书：
1. 获取文档 token（从 URL 中提取）
2. 配置到 `local/config.json` 的 `feishu_doc_token`

---

## 常见问题

### Q: ffmpeg 安装失败
A: 手动安装：
- Ubuntu: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: 从官网下载

### Q: douyin-downloader 克隆失败
A: 手动克隆：
```bash
git clone https://github.com/jiji262/douyin-downloader.git assets/douyin-downloader
```

### Q: Cookie 过期
A: 重新获取并更新 `config.yml`

### Q: SiliconFlow API 调用失败
A: 检查：
1. API Key 是否正确
2. 账号是否有余额
3. 网络是否能访问 siliconflow.cn
