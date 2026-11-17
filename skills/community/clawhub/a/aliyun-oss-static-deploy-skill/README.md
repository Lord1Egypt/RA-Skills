# aliyun-oss-static-deploy

把纯静态站点（`dist/` / `web/` / `out/` / `build/`）一键部署到阿里云 OSS，绑自定义域名 + HTTPS 证书，并打通 GitHub Actions 自动部署与证书自动续期。

这是一个给 AI 编程助手用的 **Skill**（技能包），不是独立 CLI。放到技能目录后，用自然语言说「把这个站部署到阿里云 OSS」「绑自定义域名」「签个 HTTPS 证书」「配 GitHub Actions 自动部署」就会自动命中。

> 需要服务端渲染或后端接口的场景请走函数计算 FC，不在本技能范围内。

## 它帮你避开哪些坑

这些坑每一个都能卡掉半小时以上，全部是实战踩出来的：

| 现象 | 真实原因 |
|---|---|
| 匿名访问 403，改 ACL 无效 | 新建桶默认 `BlockPublicAccess=true`，必须 `DELETE ?publicAccessBlock` |
| `Put public bucket policy is not allowed` | 账号级策略限制，改用 ACL + 关阻止公共访问即可，不必强求 bucket policy |
| 访问域名根路径返回 XML 对象列表 | 没配静态网站托管（`?website`） |
| `PutCname` 报 `MalformedXML` | `force` 传了非字符串；改成 `'true'` 后才会暴露真正的 `NeedVerifyDomainOwnership` |
| 绑域名报 `DomainNameNotResolved` | CNAME 还没生效，先加解析等生效再绑 |
| 自定义证书不生效 | CNAME 指到了 OSS 海外公共入口，必须指 `<bucket>.oss-<region>.aliyuncs.com` |
| 上传后线上还是旧内容 | 走 CDN 未刷新目录缓存，或浏览器缓存了 `max-age` 资源 |

另外：AccessKey 只从环境变量读取，绝不落盘、不进 git；公开仓库强制用最小权限的 RAM 子账号，而不是主账号 AK。

## 安装

### 方式一：git clone（推荐）

```bash
# Linux / macOS
git clone https://github.com/oracis/aliyun-oss-static-deploy-skill.git ~/.workbuddy/skills/aliyun-oss-static-deploy

# Windows (PowerShell)
git clone https://github.com/oracis/aliyun-oss-static-deploy-skill.git "$env:USERPROFILE\.workbuddy\skills\aliyun-oss-static-deploy"
```

### 方式二：手动安装

下载仓库 zip，解压后把整个文件夹放到技能目录下，保证路径是：

```
~/.workbuddy/skills/aliyun-oss-static-deploy/SKILL.md
~/.workbuddy/skills/aliyun-oss-static-deploy/scripts/cert_manager.py
~/.workbuddy/skills/aliyun-oss-static-deploy/scripts/set_github_secret.py
```

支持 WorkBuddy / CodeBuddy 等兼容 `SKILL.md` 规范的 AI 编程助手。

## 环境依赖

Python 3.8+，一次性安装：

```bash
pip install oss2 acme josepy cryptography \
    alibabacloud_alidns20150109 alibabacloud_cas20200407 \
    alibabacloud_ram20150501 pynacl
```

阿里云凭证通过环境变量提供（脚本不接收密钥作为参数）：

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=...
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=...
```

## 附带脚本

### `scripts/cert_manager.py`

Let's Encrypt 证书的签发 → 上传阿里云 CAS → 绑定 OSS / FC 自定义域名，一条命令搞定。DNS-01 挑战自动通过阿里云 DNS 增删 TXT 记录完成。

```bash
# 签发泛域名证书（覆盖 example.com 与 *.example.com）并绑到 OSS 自定义域名
python scripts/cert_manager.py --root example.com --email you@example.com \
    --bucket my-site-hk --region cn-hongkong --domain www.example.com

# 证书还在有效期内，只做分发（续期后常用）
python scripts/cert_manager.py --root example.com --domain www.example.com --targets oss

# 强制重签（忽略剩余天数）
python scripts/cert_manager.py --root example.com --email you@example.com --force
```

主要参数：

| 参数 | 说明 |
|---|---|
| `--root` | 根域，必填 |
| `--email` | ACME 账号邮箱，必填 |
| `--domains` | 逗号分隔，默认 `<root>,*.<root>` |
| `--bucket` / `--region` | OSS 桶名与地域，地域默认 `cn-hongkong` |
| `--domain` | 要绑定的自定义域名，可重复传多次 |
| `--targets` | 只跑指定阶段：`cert,cas,oss,fc` |
| `--days` | 剩余天数阈值，默认 30（超过则自动跳过，方便挂定时任务） |
| `--force` | 忽略剩余天数强制重签 |
| `--cert-dir` | 证书与 ACME 账号存放目录 |

**挂定时任务**：脚本幂等，没到期直接退出，到期才重签 + 分发。每天跑一次即可：

```
30 3 * * * /path/to/python scripts/cert_manager.py --root example.com --email you@example.com --targets oss
```

Windows 上 `schtasks` 常被企业环境禁用，可改用宿主自带的自动化能力（如 WorkBuddy 自动化）定时触发。

### `scripts/set_github_secret.py`

用 GitHub API 写仓库的 Secrets / Variables。Secret 会先用仓库公钥（PyNaCl `SealedBox`）加密再上传。

```bash
# 写 Secret（值从标准输入读，不进命令行历史）
echo "$AK_SECRET" | python scripts/set_github_secret.py --repo owner/repo --name OSS_ACCESS_KEY_SECRET --stdin

# 写明文 Variable
python scripts/set_github_secret.py --repo owner/repo --name OSS_BUCKET --value my-site-hk --variable

# 列出现有名字（读不到值）
python scripts/set_github_secret.py --repo owner/repo --list
```

配合 GitHub Actions 实现「采集 / 构建 → 自动上传 OSS」。注意：**公开仓库不要放主账号 AK**，先建一个只对该桶有写权限的 RAM 子账号。

## 目录结构

```
aliyun-oss-static-deploy/
├── SKILL.md                      # 技能正文，AI 助手读取的指令
└── scripts/
    ├── cert_manager.py           # DNS-01 签发 → CAS → 绑定 OSS/FC
    └── set_github_secret.py      # 加密写 GitHub Secrets / Variables
```

## 免责声明

使用前请确认你了解阿里云 OSS、DNS、CAS 的计费规则与操作影响。脚本会修改线上 DNS 解析记录与 OSS 配置，建议先在测试桶 / 测试子域上跑通。

## License

MIT，见 [LICENSE](LICENSE)。
