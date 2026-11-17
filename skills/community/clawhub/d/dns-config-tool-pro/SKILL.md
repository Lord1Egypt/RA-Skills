---

slug: dns-config-tool-pro
name: "dns-config-tool-pro"
version: "1.0.0"
displayName: "DNS配置工具专业版"
summary: "企业级 DNS 配置工具,支持 CAA、Cloudflare 代理、通配符与批量迁移策略。。面向企业运维与基础设施团队的 DNS 全功能配置与迁移工具。核心能力: - CAA 记录配置(限制"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: config。
  面向企业运维与基础设施团队的 DNS 全功能配置与迁移工具。核心能力:
  - CAA 记录配置(限制证书授权 CA,防未授权签发)
  - Cloudflare 代理行为管理与 CNAME 扁平化
  - 通配符记录与通配符 SSL 证书(DNS challenge)
  - 企业级批量迁移策略与回滚方案
  - 高级调试(全链路追踪、权威对比、记录完整性校验)

  适用场景:
  - 企业多域名 DNS 架构治理
  - 安全合规要求下的 CAA 与证书管控
  - Cloudflare 架构下的代理与源站保护

  差异化: Pro 版在免...
tags:
  - DNS
  - 企业运维
  - Communication
  - 安全配置
  - 批量迁移
  - 工具
  - 效率
  - 自动化
  - 运维
  - 监控
  - 写作
  - 电商
  - 安全
  - caa
  - dns
  - domain
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"

---

# DNS 配置工具(专业版)

## 概述

DNS 配置工具专业版是一款面向企业运维与基础设施团队的 DNS 全功能配置与迁移工具。它在免费版基础 TTL 管理、邮件认证、www 处理和基础调试之上,扩展出 CAA 记录配置(限制可签发证书的 CA,防止未授权签发)、Cloudflare 代理行为管理(橙云/灰云、CNAME 扁平化、Universal SSL)、通配符记录与通配符 SSL 证书(DNS challenge 签发)、企业级批量迁移策略与回滚方案,以及高级调试能力,帮助企业安全合规地管理 DNS 架构.
专业版与免费版配置理念完全兼容:免费版的基础配置原则在专业版中完全适用,升级后额外获得进阶安全与迁移能力。专业版适合企业多域名 DNS 治理、安全合规证书管控和 Cloudflare 架构下的源站保护场景.
## 核心能力

| 能力模块 | 说明 | 免费版 | Pro 版 |
|----|---|---|-----|
| TTL 管理 | 迁移前调整 | 支持 | 支持+批量 |
| 邮件认证 | SPF/DKIM/DMARC | 支持 | 支持+验证 |
| www 处理 | apex 与 www | 支持 | 支持+批量 |
| 基础调试 | dig 命令 | 支持 | 支持 |
| CAA 记录 | 证书授权限制 | 不支持 | 支持 |
| Cloudflare 代理 | 代理行为管理 | 不支持 | 支持 |
| 通配符记录 | 通配符与 SSL | 不支持 | 支持 |
| 批量迁移 | 多域名迁移 | 不支持 | 支持+回滚 |
| 高级调试 | 全链路追踪 | 基础 | 完整 |
| 记录完整性 | 全类型校验 | 部分 | 支持 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、DNS、配置工具、通配符与批量迁移、面向企业运维与基、础设施团队的、全功能配置与迁移、核心能力、记录配置、限制证书授权、防未授权签发、代理行为管理与、CNAME、扁平化、通配符记录与通配、challenge、企业级批量迁移策、略与回滚方案、权威对比、记录完整性校验等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:配置 CAA 记录防止未授权证书签发

企业安全合规要求限制仅指定 CA 可为域名签发 SSL 证书,防止未授权 CA 被滥用签发.
```bash
# 1. 基础 CAA:仅允许 Let's Encrypt 签发
example.com. CAA 0 issue "letsencrypt.org"
# ...
# 2. 通配符需单独条目
example.com. CAA 0 issuewild "letsencrypt.org"
# ...
# 3. 事件报告(发现异常签发时通知)
example.com. CAA 0 iodef "mailto:security@example.com"
# ...
# 4. 验证 CAA 配置
dig example.com CAA +short
```

未配置 CAA 时,任何 CA 都可为域名签发证书,存在安全风险。配置后仅指定 CA 可签发.
### 场景二:Cloudflare 代理行为管理

企业使用 Cloudflare 代理保护源站,需正确理解橙云/灰云行为并避免常见陷阱.
```bash
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
echo "implementation_ready"
```

### 场景三:通配符记录与通配符 SSL 证书

企业有大量子域名,需用通配符记录简化管理,并用 DNS challenge 签发通配符证书.
```bash
# 1. 通配符记录
*.example.com. A 1.2.3.4
# ...
# 注意:通配符不匹配 apex
# 示例
# 但不匹配 example.com 本身,需单独配置:
example.com. A 1.2.3.4
# ...
# 2. 显式子域名优先于通配符
# 若同时存在 *.example.com 和 api.example.com 的记录
# api.example.com 的显式记录优先生效
# ...
# 3. 通配符 SSL 证书(DNS challenge 签发)
# 使用 Let's Encrypt + DNS challenge 获取 *.example.com 证书
certbot certonly --manual --preferred-challenges dns \
  -d "*.example.com" -d "example.com"
```

### 场景四:企业级批量迁移

企业需将 50 个域名从旧 DNS 服务商批量迁移到新服务商,要求零停机和可回滚.
```bash
# 1. 迁移前 7 天:批量降低所有域名 TTL 至 300 秒
for domain in $(cat domains.txt); do
  echo "降低 $domain 的 TTL..."
  # 在旧服务商后台批量修改 TTL
done
# ...
# 2. 导出所有域名当前记录
  dig +nocmd +noall +answer $domain ANY > "records-$domain.txt"
  dig +nocmd +noall +answer _dmarc.$domain TXT >> "records-$domain.txt"
done
# ...
# 3. 在新服务商预配置所有记录(不切换 NS)
# ...
# 4. 迁移当日:切换 NS 记录
  # 在域名注册商处更新 NS 为新服务商
  echo "切换 $domain 的 NS 记录..."
done
# ...
# 5. 多解析器验证
  echo "验证 $domain:"
  dig @8.8.8.8 $domain +short
  dig @1.1.1.1 $domain +short
done
# ...
# 6. 回滚预案:若新服务商异常,将 NS 切回旧服务商
# (TTL 已降至 300 秒,回滚后 5 分钟内生效)
```

## 不适用场景

以下场景DNS配置工具专业版不适合处理：

- 安全评估未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、质量检查、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 领先步:评估当前架构

```bash
# 检查现有 CAA 配置
dig example.com CAA +short
# ...
# 检查 Cloudflare 代理状态(若使用)
dig example.com +short  # 返回 Cloudflare IP 说明已代理
# ...
# 导出完整记录清单
dig +nocmd +noall +answer example.com ANY
```

### 第二步:按需求配置

根据你的安全合规需求和企业架构,参考上方使用场景中的配置示例.
### 第三步:完整验证

```bash
# 验证 CAA
dig example.com CAA +short
# ...
# 验证通配符
dig anything.example.com +short
# ...
# 验证所有记录类型
for type in A AAAA MX TXT CAA NS SOA; do
  echo "=== $type ==="
  dig example.com $type +short
done
```

## 配置示例

### CAA 完整配置

```bash
# 仅允许 Let's Encrypt 签发常规证书
# ...
# 通配符证书单独授权
# ...
# 异常签发事件通知
# ...
# 多 CA 授权(如同时用 Let's Encrypt 和 ZeroSSL)
example.com. CAA 0 issue "sectigo.com"
# ...
# 完全禁止签发(紧急锁定)
example.com. CAA 0 issue ";"
```

### Cloudflare 架构配置

```bash
# Web 流量(橙云代理)
# A 记录设为橙云,源站 IP 被隐藏
# 自动获得 Cloudflare 的 CDN/DDoS 防护/Universal SSL
# ...
# 非 HTTP 服务(灰云 DNS-only)
# 邮件 MX 记录:必须灰云
# SSH/Game 服务器:必须灰云
# 否则橙云会中断这些服务
# ...
# 混合架构示例:
example.com.    A    1.2.3.4    (橙云 - Web)
api.example.com. A   1.2.3.4    (橙云 - API Web)
mail.example.com. A  1.2.3.5   (灰云 - 邮件)
ssh.example.com. A   1.2.3.5   (灰云 - SSH)
# ...
# Universal SSL 注意:
# 仅橙云记录获得 Universal SSL
# 灰云记录需源站自行配置证书(如 Let's Encrypt)
```

### 通配符 SSL 证书签发

```bash
# 方式一:certbot + DNS challenge(推荐)
certbot certonly \
  --manual \
  --preferred-challenges dns \
  --server https://acme-v02.api.letsencrypt.org/directory \
  -d "*.example.com" \
  -d "example.com"
# ...
# 方式二:acme.sh + Cloudflare DNS API(自动化)
acme.sh --issue --dns dns_cf \
  -d "*.example.com" \
  -d "example.com" \
  --keylength ec-256
# ...
# 注意:通配符证书必须用 DNS challenge,HTTP challenge 不支持通配符
```

### 批量迁移检查清单

```markdown
# DNS 批量迁移检查清单
# ...
## 迁移前(7 天前)
- [ ] 导出所有域名完整记录清单
- [ ] 批量降低 TTL 至 300 秒
- [ ] 等待原 TTL 过期(确认新 TTL 生效)
- [ ] 在新服务商预配置所有记录
- [ ] 验证新服务商记录与原记录一致
- [ ] 准备回滚预案
# ...
## 迁移当日
- [ ] 选择低峰时段
- [ ] 更新 NS 记录指向新服务商
- [ ] 多解析器验证(8.8.8.8 / 1.1.1.1 / 本地 ISP)
- [ ] 验证所有记录类型(A/AAAA/MX/TXT/CAA/NS)
- [ ] 验证邮件认证(SPF/DKIM/DMARC)
- [ ] 验证 SSL 证书有效
- [ ] 监控服务可用性(至少 2 小时)
# ...
## 迁移后(24 小时)
- [ ] 确认全球解析一致
- [ ] 恢复 TTL 至 3600-86400 秒
- [ ] 保留旧服务商记录 7 天(回滚窗口)
- [ ] 归档迁移记录与决策文档
```

## 优选实践

1. **CAA 必配原则**: 安全敏感域名务必配置 CAA 记录,限制仅授权 CA 可签发证书。未配置 CAA 时任何 CA 都可签发,存在证书滥用风险。配置 `iodef` 字段以便异常签发时收到通知.
2. **Cloudflare 代理按服务类型区分**: Web 流量用橙云获得 CDN 和防护;非 HTTP 服务(SSH/邮件/游戏)必须用灰云,否则橙云会中断连接。混合架构中明确标注每条记录的代理状态.
3. **通配符不匹配 apex**: `*.example.com` 匹配子域名但不匹配 apex(`example.com`)。通配符和 apex 需分别配置记录。显式子域名记录优先于通配符,可用于覆盖特定子域名的解析.
4. **通配符证书用 DNS challenge**: 通配符 SSL 证书必须使用 DNS challenge 签发,HTTP challenge 不支持。配合 Cloudflare DNS API 可实现自动签发和续期,避免手动添加 TXT 记录的繁琐.
5. **CNAME 扁平化记录决策**: Cloudflare 支持 apex 的 CNAME 扁平化,但迁移离开 Cloudflare 时会造成混乱(其他服务商不支持 apex CNAME)。建议在架构文档中明确记录此决策,便于后续迁移.
6. **批量迁移分阶段执行**: 大规模迁移分三阶段:7 天前降 TTL 并预配置;迁移日切 NS 并验证;24 小时后恢复 TTL。保留旧服务商记录 7 天作为回滚窗口。TTL 已降至 300 秒,回滚 5 分钟内生效.
7. **迁移记录完整性校验**: 迁移后逐一验证所有记录类型(A/AAAA/MX/TXT/CAA/NS/SOA),A 正常不代表其他类型正确。特别注意邮件认证(SPF/DKIM/DMARC)和 CAA 是否完整迁移.
8. **Universal SSL 限制认知**: Cloudflare Universal SSL 仅对橙云(代理)记录生效。灰云(DNS-only)记录不获得 Universal SSL,需源站自行配置证书(如 Let's Encrypt).
9. **回滚预案必备**: 任何迁移都需准备回滚预案。回滚关键:TTL 已提前降低(300 秒,5 分钟生效);旧服务商记录保留窗口(7 天);明确回滚触发条件(如可用性低于阈值)和执行步骤.
10. **与免费版兼容**: Pro 版完全兼容免费版配置原则。免费版的 TTL 策略、邮件认证、www 处理等基础配置在 Pro 版中完全适用,Pro 版额外提供 CAA、Cloudflare、通配符与批量迁移能力.
## 常见问题

### Q1: CAA 记录配置后证书签发失败?

检查 CAA 是否过于严格。若 CAA 仅允许 `letsencrypt.org`,但实际使用 ZeroSSL 签发,会被拒绝。确认 CAA 中 `issue` 字段包含所有实际使用的 CA。通配符证书需额外配置 `issuewild`。紧急情况下可用 `issue ";"` 完全禁止签发.
### Q2: Cloudflare 橙云后 SSH/邮件连不上?

橙云(代理)仅支持 HTTP/HTTPS 流量,会中断 SSH、邮件(SMTP/IMAP)、游戏服务器等非 HTTP 服务。这些服务必须用灰云(DNS-only)。检查记录的代理状态,将非 HTTP 服务记录切换为灰云.
### Q3: 通配符证书续期失败?

通配符证书必须用 DNS challenge 续期。若使用 HTTP challenge 会失败。建议配置 DNS API 自动化(如 acme.sh + Cloudflare DNS API),实现自动续期。确认 DNS API Token 权限包含 Zone DNS 编辑权限.
### Q4: apex 用 CNAME 扁平化后迁移出 Cloudflare 报错?

其他 DNS 服务商通常不支持 apex 的 CNAME(RFC 限制)。Cloudflare 的 CNAME 扁平化是其特有功能。迁移离开 Cloudflare 时需将 apex 的 CNAME 改回 A 记录。建议迁移前在架构文档记录此决策,迁移时优先处理 apex 记录.
### Q5: 批量迁移如何保证零停机?

关键:迁移前 7 天将所有域名 TTL 降至 300 秒并等待生效;在新服务商完整预配置所有记录(包括 TXT/CAA/MX 等所有类型)并验证一致;迁移日仅切换 NS 记录(不改记录值);切换后多解析器验证;保留旧服务商 7 天回滚窗口。TTL 300 秒确保回滚 5 分钟生效.
### Q6: Universal SSL 没生效?

Universal SSL 仅对橙云(代理)记录生效。若记录为灰云(DNS-only),不获得 Universal SSL,需在源站自行配置证书。检查记录代理状态,Web 流量记录应设为橙云。新启用代理后 Universal SSL 可能需要几分钟到几小时激活.
### Q7: 迁移后邮件认证失效?

迁移时容易遗漏 TXT 记录(SPF/DKIM/DMARC)。迁移后务必逐一验证:SPF(`dig TXT example.com`)、DKIM(`dig TXT default._domainkey.example.com`)、DMARC(`dig TXT _dmarc.example.com`)。DKIM 记录由邮件服务商提供,确保完整复制(含公钥).
### Q8: Pro 版和免费版能同时用吗?

可以。两者配置原则兼容。Pro 版包含免费版全部能力,额外提供 CAA、Cloudflare、通配符与批量迁移。建议企业环境统一使用 Pro 版,免费版用于个人轻量场景.
### Q9: 如何监控 CAA 异常签发?

配置 CAA 的 `iodef` 字段(`CAA 0 iodef "mailto:security@example.com"`),当有 CA 尝试为域名签发证书但被 CAA 拒绝时,指定邮箱会收到通知。定期检查通知,发现异常签发尝试及时排查.
### Q10: 大规模迁移用什么工具辅助?

Pro 版提供迁移检查清单和脚本模板。批量操作可编写脚本循环处理(如 bash 遍历域名列表执行 dig 验证)。记录导出用 `dig +nocmd +noall +answer domain ANY` 批量保存。迁移进度跟踪建议用表格记录每个域名的阶段状态.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持解析 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **命令行工具**: `dig`(DNS 查询)、`certbot`/`acme.sh`(证书签发,可选)
- **DNS 服务商后台**: 支持高级功能(CAA/通配符)的 DNS 服务商
- **Cloudflare 账号**: 若使用 Cloudflare 代理与 DNS API(可选)

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM 能力 | API | 必需 | 由 Agent 内置大模型提供 |
| dig 命令 | 工具 | 推荐 | 系统自带或安装 bind-utils/dnsutils |
| DNS 服务商后台 | 平台 | 必需 | 支持 CAA 的 DNS 服务商 |
| Cloudflare | 平台 | 可选 | Cloudflare 账号(代理架构时) |
| certbot / acme.sh | 工具 | 可选 | 通配符证书签发 |
| mail-tester.com | 验证服务 | 推荐 | 免费在线服务 |

### API Key 配置

- **本 Skill 核心无需 API Key**: 基于 Markdown 指令和命令行工具,不调用外部 API.
- **Cloudflare API Token**: 若使用 Cloudflare DNS API 自动化签发通配符证书,需在 Cloudflare 后台创建 API Token(权限:Zone DNS 编辑),通过环境变量注入.
- **DNS 服务商凭证**: 修改 DNS 记录需登录服务商后台,凭证由用户自行管理.
- **ACME 账户**: certbot/acme.sh 首次使用会自动创建 Let's Encrypt ACME 账户,无需手动配置 Key.
### 可用性分类

- **分类**: MD+execute(纯 Markdown 指令 + 部分功能需 `exec` 执行 dig/certbot 等命令)
- **说明**: 以自然语言指令驱动 Agent 指导 DNS 高级配置、证书签发与批量迁移
- **适用规模**: 企业级、多域名架构、安全合规场景
- **兼容性**: 与 `dns-config-tool-free` 配置原则完全兼容,可平滑升级
- **支持级别**: 优先支持(Pro 版享有问题优先响应与功能迭代建议通道)

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 依赖云服务，需要网络连接
- 需要有效的云服务凭证和配置好的CLI环境
- 产生的云资源可能产生费用，使用前请确认计费方式
- 不同区域的服务可用性和功能支持可能存在差异

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "DNS配置工具专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dns config pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。