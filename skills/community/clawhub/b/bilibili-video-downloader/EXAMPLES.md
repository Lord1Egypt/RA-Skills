# 使用示例

## 示例 1: 搜索并下载单个视频

```powershell
# 1. 搜索视频
.\search.ps1 -Keyword "Python入门教程" -Limit 5

# 输出:
# Python零基础入门教程 | 程序员小灰 | 125000 views | BV1xx411c7mD | https://www.bilibili.com/video/BV1xx411c7mD

# 2. 下载视频
.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD" -Quality 1080
```

## 示例 2: 批量下载视频

```bash
# 1. 创建 URL 文件
cat > videos.txt << 'EOF'
https://www.bilibili.com/video/BV1xx411c7mD
https://www.bilibili.com/video/BV1yy411c7nE
https://www.bilibili.com/video/BV1zz411c7oF
EOF

# 2. 批量下载
./download-batch.sh videos.txt 1080 ./downloads
```

## 示例 3: 下载 UP 主全部视频

```bash
# 1. 获取 UP 主视频列表（以 UID 208259 为例）
./up-videos.sh 208259 50 > up-videos.txt

# 2. 批量下载
./download-batch.sh up-videos.txt 1080 ./downloads
```

## 示例 4: 获取视频信息

```powershell
.\video-info.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD"

# 输出:
# 标题: Python零基础入门教程
# UP主: 程序员小灰
# 上传时间: 20240101
# 时长: 15分30秒
# 播放量: 125000
# 点赞: 8500
# 简介: 本视频适合零基础学习Python...
# BV号: BV1xx411c7mD
# 链接: https://www.bilibili.com/video/BV1xx411c7mD
# 
# 可用清晰度:
#   - 1080P
#   - 720P
#   - 480P
#   - 360P
```

## 示例 5: 获取评论

```bash
./comments.sh "https://www.bilibili.com/video/BV1xx411c7mD" 20

# 输出:
# 共获取 20 条评论:
# 
# [1] 用户A (👍 125)
#     讲得太好了，终于懂了！
# 
# [2] 用户B (👍 89)
#     收藏了，慢慢看
```

## 示例 6: 下载弹幕

```bash
./danmaku.sh "https://www.bilibili.com/video/BV1xx411c7mD" video-danmaku.xml

# 弹幕文件将保存为 video-danmaku.xml
# 可使用弹幕播放器查看
```

## 示例 7: 使用 OpenClaw 触发

在 OpenClaw 对话中直接说：

```
帮我下载B站上的Python教程视频
```

OpenClaw 会自动：
1. 搜索相关视频
2. 展示搜索结果
3. 下载选定的视频

或指定具体视频：

```
把B站这个视频下载下来 https://www.bilibili.com/video/BV1xx411c7mD
```
