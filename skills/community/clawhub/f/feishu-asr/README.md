# 飞书语音识别 ASR Skill

## 快速开始

### 1. 配置环境变量

在 OpenClaw 配置文件或系统环境中设置：

```bash
# 飞书应用凭证
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxx

# 阿里云ASR凭证（推荐）
ALIYUN_ACCESS_KEY_ID=xxxxx
ALIYUN_ACCESS_KEY_SECRET=xxxxx
```

### 2. 飞书应用权限

飞书应用需要配置以下权限：
- `im:message:readonly_as_app` - 以应用身份读取消息
- `im:message:list` - 获取消息列表

### 3. 使用方式

当用户发送飞书语音消息时：
1. 自动获取消息的 message_id
2. 下载语音文件
3. 调用ASR服务识别
4. 返回文字结果

## ASR服务商

### 阿里云ASR（推荐）

1. 访问 https://d.console.aliyun.com
2. 注册/登录阿里云账号
3. 开通"智能语音交互"服务
4. 获取 AccessKeyId 和 AccessKeySecret
5. 每月100小时免费额度

### 腾讯云ASR

1. 访问 https://cloud.tencent.com
2. 开通"语音识别"服务
3. 获取 SecretId 和 SecretKey

## 注意事项

- 飞书语音消息通常是 .silk 格式，需要转换为 .wav
- 阿里云ASR需要将音频转为16kHz采样率
- 免费额度用完后需要付费
