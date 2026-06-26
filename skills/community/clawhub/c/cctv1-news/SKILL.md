---
name: cctv-news-simple
description: 简单版本的CCTV新闻联播内容获取工具。获取CCTV新闻联播内容并保存到本地文件，无需钉钉机器人。支持定时执行，适合个人使用。
---

# 简单版CCTV新闻联播获取工具

这个skill用于获取CCTV新闻联播内容并保存到本地文件，无需钉钉机器人配置，适合个人使用。

## 功能特点

- 自动获取CCTV新闻联播主页面内容
- 提取所有新闻章节的视频链接和摘要
- 包含完整版视频链接
- 保存到本地文本文件
- 无需外部API配置
- 支持定时执行

## 使用方法

帮我获取2026年4月19日的新闻联播

### 1. 安装依赖

```bash
pip install requests pytz lxml
```

### 2. 执行脚本

```bash
python scripts/get_cctv_news_simple.py
```

### 3. 查看结果

执行完成后，会在脚本同目录下生成 `cctv_news_YYYYMMDD.txt` 文件，包含当日新闻联播内容。

## 定时执行配置

### Windows任务计划程序

1. 打开任务计划程序
2. 创建基本任务
3. 设置触发器：每天22:00
4. 设置操作：启动程序
   - 程序：python.exe
   - 参数：C:\path\to\scripts\get_cctv_news_simple.py

### Linux/Unix Cron

编辑crontab：
```bash
crontab -e
```

添加以下行（注意时区转换，22:00北京时间 = 14:00 UTC）：
```
0 14 * * * cd /path/to/skill && python scripts/get_cctv_news_simple.py
```

## 输出格式

生成的文本文件包含：
- 日期标题（格式：YYYYMMDD新闻联播）
- 完整版视频链接
- 各新闻章节的摘要和链接

## 自定义配置

- 修改输出文件路径：编辑脚本中的 `output_file` 变量
- 修改CCTV网站URL：编辑脚本中的 `url1` 变量

## 错误处理

脚本包含基本的错误处理机制，如遇网络问题或解析失败会输出错误信息到控制台。