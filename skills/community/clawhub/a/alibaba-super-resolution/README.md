# ☁️ Alibaba Cloud Super Resolution

阿里云视频超分辨率 Skill
本技能调用阿里云视频超分辨能力，可以将输入视频放大2倍尺寸输出，并基于细节推断增强输出视频画质，输出视频为h264编码、MP4格式；

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

[阿里云超级分辨率官方文档](https://help.aliyun.com/zh/viapi/developer-reference/api-w2n4j6?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.1.23722f3dIyTr4v&scm=20140722.S_help@@%E6%96%87%E6%A1%A3@@159118._.ID_help@@%E6%96%87%E6%A1%A3@@159118-RL_%E8%B6%85%E7%BA%A7%E5%88%86%E8%BE%A8%E7%8E%87-LOC_2024SPAllResult-OR_ser-PAR1_215029ae17731433060538338d0c65-V_4-PAR3_o-RE_new13-P0_0-P1_0)


## ✨ 功能特性

- 🎬 **AI 超分**：将低分辨率视频（≤720p）提升至2x分辨率
- 📤 **本地上传**：支持本地文件直接上传（最大 2GB）
- ⚙️ **灵活配置**：可自定义码率，平衡质量和文件大小
- 🔄 **异步处理**：支持后台任务、状态查询、自动下载

## 📦 快速开始

### 鉴权文件
[创建AccessKey](https://help.aliyun.com/zh/viapi/getting-started/create-the-accesskey?spm=a2c4g.11186623.0.0.317c257fqUr1bO)

获取AccessKey ID与AccessKey Secret

### 阿里云SDK
本API调用依赖阿里云SDK

# SDK安装命令:
pip install alibabacloud_videoenhan20200320==4.0.0

### 技能安装

```bash
# 方式 1: 克隆到 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/BlackEight4752/alibaba-super-resolution.git

# 方式 2: 通过 ClawHub（待发布）
clawhub install alibaba-super-resolution

# 安装依赖
pip install -r requirements.txt
```

### 配置 API 密钥

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-access-key-id"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-access-key-secret"

# 可选：OSS 配置（用于大文件）
export ALIYUN_OSS_BUCKET="your-bucket-name"
export ALIYUN_OSS_ENDPOINT="oss-cn-shanghai.aliyuncs.com"
```

### 使用示例

```bash
# 基础用法：本地文件 → 本地 HD 文件
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4

# 自定义码率（更高 = 更好质量，更大文件）
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --output videos/output-960p.mp4 \
  --bit-rate 8

# 提交后不等待（立即返回 Job ID）
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --input videos/input-480p.mp4 \
  --no-wait

# 查询任务状态
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --status <JOB_ID>

# 等待任务完成并下载
python3 ~/.openclaw/workspace/skills/alibaba-super-resolution/alibaba_super_resolve.py \
  --wait <JOB_ID> \
  --output videos/output-1080p.mp4
```


## 📊 参数说明

### 输入要求

- **格式**：MP4, MOV, AVI, MKV
- **最大大小**：2GB（直接上传）/ 无限制（OSS URL）
- **最大时长**：30 分钟
- **输入分辨率**：480p, 720p

### 输出分辨率

| 输入 | 输出 |
|------|------|
| 480p | 960p (2x 放大) |
| 720p | 2K  (2x 放大) |


## 📁 文件结构

```
alibaba-super-resolution/
├── SKILL.md                  # OpenClaw Skill 文档
├── alibaba_super_resolve.py  # Python CLI 工具
├── _meta.json                # Skill 元数据
├── requirements.txt          # Python 依赖
├── LICENSE                   # MIT License
└── README.md                 # 本文件
```

## ⚠️ 注意事项

### 文件限制
- 直接上传最大 2GB
- 超过 2GB 需使用 OSS URL

### URL 有效期
- 输出 URL 24 小时后过期
- 请及时下载处理后的视频

### 超时设置
- 默认超时：1200 秒（20 分钟）
- 长视频可增加：`--timeout 1800`

## 🔧 故障排查

### File exceeds 2GB limit
**解决**：使用 OSS URL 代替直接上传

### Task timed out
**解决**：增加超时时间 `--timeout 1800`

### OSSAccessDenied
**解决**：检查 RAM 权限，确保有 OSS 读写权限

## 🔗 相关链接

- [OpenClaw 文档](https://github.com/openclaw/openclaw)
- [阿里云SDK官方文档](https://help.aliyun.com/document_detail/378659.html)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
