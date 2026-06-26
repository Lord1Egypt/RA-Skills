name
file-uploader
description
将本地文件（图片、文档、视频等）上传至阿里云 OSS 并返回可直接访问的网络 URL。

触发场景：
1、用户说 “上传文件”“上传图片”“上传文档”
2、需要将本地文件转换为网络 URL
3、用户提供文件并要求生成可直接网页引用的链接

配置方式
需要配置 JWT Token 和 Device-ID：
JWT Token：登录 https://www.szmpy.com 获取
Device-ID：由管理员分配

支持文件类型
图片：jpg、jpeg、png、gif、webp、svg、bmp文档：pdf、doc、docx、xls、xlsx、ppt、pptx视频：mp4、avi、mov、mkv、webm音频：mp3、wav、flac、aac压缩包：zip、rar、tar、gz

安全限制
文件大小最大 4MB
仅允许白名单内文件类型
凭证仅保存在本地用户目录，权限 600
所有错误信息脱敏，不暴露服务端细节

实现逻辑（curl）
#!/bin/bash
CONFIG="$HOME/.file-uploader.json"
UPLOAD_URL="https://xcx.szmpy.com/api/image/uploadfile"

if [ "$1" = "config" ]; then
  shift
  jq -n \
    --arg token "$2" \
    --arg device "$4" \
    '{jwt_token: $token, device_id: $device}' > "$CONFIG"
  chmod 600 "$CONFIG"
  echo "配置已保存"
  exit 0
fi

FILE="$1"

if [ ! -f "$CONFIG" ]; then
  echo "未配置，请先执行 file-uploader config --token ... --device-id ..."
  exit 1
fi

JWT=$(jq -r .jwt_token "$CONFIG")
DEVICE=$(jq -r .device_id "$CONFIG")

if [ ! -f "$FILE" ]; then
  echo "文件不存在"
  exit 1
fi

EXT="${FILE##*.}"
EXT=$(echo "$EXT" | tr A-Z a-z)
ALLOWED="jpg,jpeg,png,gif,webp,svg,bmp,pdf,doc,docx,xls,xlsx,ppt,pptx,mp4,avi,mov,mkv,webm,mp3,wav,flac,aac,zip,rar,tar,gz"

if ! echo "$ALLOWED" | grep -qw "$EXT"; then
  echo "不支持的文件类型"
  exit 1
fi

SIZE=$(stat -c%s "$FILE" 2>/dev/null || stat -f%z "$FILE")
if [ "$SIZE" -gt $((100*1024*1024) ]; then
  echo "文件超过大小限制"
  exit 1
fi

RESP=$(curl -s -X POST \
  -H "Authorization: Bearer $JWT" \
  -H "Device-ID: $DEVICE" \
  -F "file=@$FILE" \
  --connect-timeout 10 \
  --max-time 60 \
  "$UPLOAD_URL")

URL=$(echo "$RESP" | grep -Eo 'https?://[^"]+' | head -n 1)

if [ -n "$URL" ]; then
  echo "SUCCESS"
  echo "URL: $URL"
  echo "{\"code\":1,\"url\":\"$URL\"}"
else
  echo "UPLOAD FAILED"
  echo "{\"code\":0,\"url\":null}"
  exit 1
fi

输出格式
成功：code=1,msg=url