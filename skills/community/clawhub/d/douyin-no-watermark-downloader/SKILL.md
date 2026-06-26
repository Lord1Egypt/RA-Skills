---
name: 无水印抖音视频下载器
description: |
  下载抖音视频到本地（无水印），以mp4格式默认保存在桌面目录。
触发关键字:                   
  - "下载抖音视频"
  - "抖音视频下载"
  - "抖音无水印视频"
  - "去除抖音视频水印"
metadata:
  author: ley
  version: "1.0.8"
  update_time: "2026-04-09" 
---

# 无水印抖音视频下载器

## 使用方式
### 示例命令
下载这个视频：https://v.douyin.com/1A4yExNduOU/ <br>
抖音无水印下载：https://v.douyin.com/8B9xYz789/ <br>
去除这个抖音视频水印：https://v.douyin.com/8B9xYz789/ <br>


### 工具使用说明
- 脚本路径：`scripts/douyin-no-watermark-downloader.py`
- 使用格式：`python douyin-no-watermark-downloader.py "抖音分享链接/分享文本"`

### 示例1：直接输入短链接
```bash
python douyin-no-watermark-downloader.py "https://v.douyin.com/XIkH2hGDnw/"
```

### 示例 2：输入带文案的分享文本
```bash
python douyin-no-watermark-downloader.py "复制打开抖音，看看【任 一的作品】爆竹声声一岁除！这才是王安石笔下的真爆竹！#福建民俗 https://v.douyin.com/1A4yExNduOU/"
```

### 示例 3：去除视频水印（输入原链接）
```bash
python douyin-no-watermark-downloader.py "去除这个抖音视频水印：https://v.douyin.com/1A4yExNduOU/"
```

- 输出 
  - 默认输出目录：./desktop
  - 文件名：<video_timestamp>.mp4
  - 终端会输出每条的成功/失败结果与落盘路径

### 工具说明
#### 安装说明
可通过此命令直接安装
```bash
clawdhub install douyin-no-watermark-downloader
```
#### 解析逻辑
1、不篡改抖音平台数据，不破解、不绕过平台合法限制 <br>
2、不获取视频的非公开信息（如作者隐私、未公开数据等）<br>
3、解析行为严格遵循网络服务规范与抖音平台公开分享规则 <br>

#### 数据安全说明
仅处理用户主动输入的公开分享链接，不收集、不上传任何用户隐私数据（包括但不限于姓名、手机号、设备 ID、浏览记录等）

