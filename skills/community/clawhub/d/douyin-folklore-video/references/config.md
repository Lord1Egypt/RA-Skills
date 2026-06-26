# 配置信息

## API Key

**阿里云百炼 API Key：**
```
YOUR_DASHSCOPE_API_KEY
```

支持的服务：
- 语音合成（qwen3-tts-flash）
- 文生图（wan2.6-t2i）
- 图生视频（wan2.2-kf2v-flash）

## FTP 服务器

用于托管图片供视频生成 API 访问：

```
地址：YOUR_FTP_HOST:21
账号：YOUR_FTP_USER
密码：YOUR_FTP_PASSWORD
```

上传后的 URL 格式：
```
http://YOUR_HTTP_HOST/<文件名>
```

## 浏览器配置

上传抖音时使用：
- profile: openclaw
- 上传目录：`<TEMP_DIR>/openclaw/uploads/`

## 抖音账号

- 账号名：YOUR_DOUYIN_ACCOUNT