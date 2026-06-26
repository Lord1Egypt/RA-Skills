# 百度网盘 Skill

管理百度网盘文件。

## 触发条件
用户提到：百度网盘、网盘、文件上传、文件下载、文件管理

## 功能

### 列出文件
```
列出根目录文件
列出 /EVA 目录文件
```

### 搜索文件
```
搜索 centos
搜索 电影
```

### 创建目录
```
在网盘创建 /测试 目录
```

## 配置说明

使用前需要配置环境变量：

```bash
# 设置环境变量（Mac/Linux）
export BAIDU_APP_ID="你的AppID"
export BAIDU_NETDISK_TOKEN="你的access_token"
```

### 如何获取 access_token

1. 打开百度网盘开放平台创建应用
2. 获取 AppID、AppKey、SecretKey
3. 按文档获取 OAuth access_token

详细步骤参考：https://pan.baidu.com/union/doc/

## 技术实现
- Python 脚本调用百度网盘 REST API
- 使用 OAuth 授权（更安全）
- 凭证从环境变量读取，不硬编码

## 文件位置
- 脚本: scripts/main.py
- 配置: skill.json

## 版本
- v1.0.0 - 基础功能：列出、搜索、创建目录
