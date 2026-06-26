# 依赖说明

## 必需组件

### 1. ffmpeg（本地工具）

用途：将图片序列 + 音频合成为 MP4 视频

安装方式：
```bash
# macOS（推荐 Homebrew）
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# CentOS/RHEL
sudo yum install -y ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# 验证安装
ffmpeg -version
```

Windows 用户：
```
1. 访问 https://ffmpeg.org/download.html
2. 点击 Windows 图标，选择 gyan.dev 或 BtbN 提供的构建
3. 下载并解压 zip 文件
4. 将 bin 目录添加到系统 PATH 环境变量
5. 重启命令行后执行 ffmpeg -version 验证
```

### 2. china-image-gen（OpenClaw Skill）

用途：调用硅基流动文生图 API，为每个分镜生成图片

安装方式：
```bash
clawhub install china-image-gen
# 或访问：https://clawhub.ai/ToBeWin/china-image-gen
```

支持的模型：
```
FLUX.1-schnell  速度最快，适合快速预览（推荐首选）
FLUX.1-dev      最高质量，适合最终输出
Kolors          中文 prompt 理解最佳，适合国内场景
```

### 3. china-tts（OpenClaw Skill）

用途：调用硅基流动 TTS API，生成视频解说词

安装方式：
```bash
clawhub install china-tts
# 或访问：https://clawhub.ai/ToBeWin/china-tts
```

### 4. SILICONFLOW_API_KEY（环境变量）

用途：调用硅基流动 API（图片生成 + TTS 共用同一个 Key）

获取方式：
```
1. 访问 cloud.siliconflow.cn（国内直连）
2. 手机号注册，新用户有免费额度
3. 进入「API密钥」→「新建API密钥」
4. 复制 sk- 开头的 Key
```

配置方式：
```bash
export SILICONFLOW_API_KEY="sk-xxxxxxxxxxxxxxxx"
# 或写入 ~/.openclaw/.env（永久生效）
```

---

## 音色列表（china-tts）

| 音色 | 风格 | voice 参数 | 适合视频类型 |
|---|---|---|---|
| alex | 沉稳男声 | CosyVoice2-0.5B:alex | 商务/产品/科技 |
| benjamin | 低沉男声 | CosyVoice2-0.5B:benjamin | 纪录片/严肃 |
| charles | 磁性男声 | CosyVoice2-0.5B:charles | 品牌/高端 |
| david | 欢快男声 | CosyVoice2-0.5B:david | 活泼/促销 |
| anna | 沉稳女声 | CosyVoice2-0.5B:anna | 新闻/教育 |
| bella | 激情女声 | CosyVoice2-0.5B:bella | 广告/发布会 |
| claire | 温柔女声 | CosyVoice2-0.5B:claire | 生活/情感 |
| diana | 欢快女声 | CosyVoice2-0.5B:diana | 小红书/抖音 |

---

## 成本估算

```
图片生成（FLUX.1-schnell）：
  6张图（30秒视频）≈ ¥0.42
  12张图（60秒视频）≈ ¥0.84

图片生成（FLUX.1-dev，高质量）：
  6张图 ≈ ¥0.42
  12张图 ≈ ¥0.84

TTS 配音（按 UTF-8 字节计费）：
  30秒视频约120字中文 = 360字节 ≈ 极低（< ¥0.01）
  60秒视频约240字中文 = 720字节 ≈ 极低

合计：
  30秒产品视频（schnell）≈ ¥0.50
  60秒科普视频（schnell）≈ ¥1.00
  30秒高质量视频（dev）  ≈ ¥0.50
```
