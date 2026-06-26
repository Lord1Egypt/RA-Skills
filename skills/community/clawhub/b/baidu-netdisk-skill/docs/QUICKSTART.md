# 🚀 快速开始指南

## 第一步：申请百度 API（5 分钟）

### 1. 访问百度网盘开放平台

https://pan.baidu.com/union/apply

### 2. 登录并申请开发者账号

- 使用你的企业百度账号登录
- 填写公司信息（你有营业执照，很快通过）
- 选择应用类型：**工具类**
- 填写应用名称：`百度网盘 Skill`（或你喜欢的名字）
- 应用描述：`OpenClaw 网盘连接工具`

### 3. 创建应用

审核通过后（通常 1-3 个工作日）：

- 进入控制台
- 创建新应用
- 获取 **API Key** 和 **Secret Key**

### 4. 获取 Access Token

方法一：OAuth 授权（推荐）

```
https://openapi.baidu.com/oauth/2.0/authorize?
response_type=code&
client_id=你的 API_KEY&
redirect_uri=oob&
scope=basic,netdisk
```

访问后获得 code，然后用 code 换 token：

```bash
curl "https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code=你的 CODE&client_id=你的 API_KEY&client_secret=你的 SECRET_KEY&redirect_uri=oob"
```

返回的 JSON 里有 `access_token` 和 `refresh_token`。

---

## 第二步：安装 Skill

```bash
# 克隆代码
git clone https://github.com/你的用户名/baidu-netdisk-skill

# 进入目录
cd baidu-netdisk-skill

# 安装依赖
npm install

# 全局链接（可选）
npm link
```

---

## 第三步：配置

```bash
npx baidu-netdisk-skill config \
  -k 你的 API_KEY \
  -s 你的 SECRET_KEY \
  -t 你的 ACCESS_TOKEN \
  -r 你的 REFRESH_TOKEN
```

---

## 第四步：测试

```bash
# 查看用户信息
npx baidu-netdisk-skill whoami

# 列出根目录文件
npx baidu-netdisk-skill list /

# 搜索文件
npx baidu-netdisk-skill search "学习资料"

# 获取下载链接
npx baidu-netdisk-skill download 123456789
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `whoami` | 查看用户信息 |
| `list /` | 列出根目录文件 |
| `list /我的资源` | 列出指定目录 |
| `search "关键词"` | 搜索文件 |
| `download <fsId>` | 获取下载链接 |
| `upload ./文件.pdf /备份/` | 上传文件 |
| `clear-cache` | 清空缓存 |
| `config` | 重新配置 |

---

## 常见问题

### Q: 提示 "Token 过期" 怎么办？

A: 运行 `config` 命令重新配置 Token，或者等自动刷新。

### Q: 文件太多，列表不完整？

A: 使用分页参数：
```bash
npx baidu-netdisk-skill list / -l 200
```

### Q: 如何上传大文件？

A: 代码支持分片上传，最大支持 20GB：
```bash
npx baidu-netdisk-skill upload ./大文件.zip /备份/
```

### Q: 如何节省 Token？

A: 
1. 使用缓存（默认开启）
2. 搜索时用服务端搜索（`search` 命令）
3. 只获取必要的元数据

---

## 下一步

- 阅读 [完整 API 文档](./api.md)
- 查看 [安全说明](../SECURITY.md)
- 订阅付费版本获取更多支持

---

**有问题？** [提交 Issue](https://github.com/你的用户名/baidu-netdisk-skill/issues)
