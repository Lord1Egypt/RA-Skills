---
slug: "dns-free"
name: "dns-free"
version: "1.0.0"
displayName: "DNS配置基础版"
summary: "提供包含DNS记录配置基础、TTL迁移提示与邮件认证SPF/DMARC入门检查.DNS配置基础版Skill,覆盖TTL迁移提示、SPF/DMARC入门检查与dig基础诊断. 核心能力: - 迁移前的"
summary_zh: "DNS记录配置基础、TTL迁移提示与邮件认证SPF/DMARC入门检查。DNS配置基础版Skill,覆盖TTL迁移提示、SPF/DMARC入门检查与dig基础诊断"
license: "MIT"
description: "|-. 适用于需要dns相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  DNS配置基础版Skill,提供DNS快速诊断与自动检测能力,覆盖TTL迁移提示、SPF/DMARC入门检查与dig基础诊断.
  核心能力:
  - 迁移前的TTL降级提示与基础缓存探测
  - SPF单TXT记录与DMARC基础配置检查
  - dig基础命令(A/TXT/MX查询)
  - www规范化基础建议

  适用场景:
  - 个人域名迁移前的TTL预热
  - 邮件认证SPF/DMARC基础配置
  - DNS记录基础排查
tags:
  - - DNS
  - dns
  - automation
  - productivity
  - developer-tools
  - DMARC
  - TTL
  - SPF
  - 域名迁移
  - 邮件认证
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free
---
# DNS配置基础版

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | DNS配置基础版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

本Skill提供DNS配置的基础检查与提示能力:

- **TTL迁移提示**: 迁移前48小时将TTL降至300秒,迁移稳定24小时后恢复至3600-86400秒
- **SPF基础检查**: 确认SPF为单条TXT记录,结尾为 `-all` 或 `~all`
- **DMARC基础配置**: 配置 `_dmarc.example.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"`
- **dig基础诊断**: 使用 `dig example.com`、`dig TXT example.com`、`dig MX example.com` 查询记录
- **www规范化**: apex与www需同时配置或互转,HTTPS重定向需双域名证书
### TTL迁移提示

针对TTL迁移提示,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供TTL迁移提示相关的配置参数、输入数据和处理选项.
**输出**: 返回TTL迁移提示的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`TTL迁移提示`的配置文档进行参数调优
### SPF基础检查

针对SPF基础,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供SPF基础检查相关的配置参数、输入数据和处理选项.
**输出**: 返回SPF基础检查的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`SPF基础检查`的配置文档进行参数调优
### DMARC基础配置

针对DMARC基础,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供DMARC基础配置相关的配置参数、输入数据和处理选项.
**输出**: 返回DMARC基础配置的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`DMARC基础配置`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. **环境确认**: 确认Agent平台已加载本skill，检查依赖说明中的环境要求
2. **指令输入**: 向Agent描述需要执行的任务，引用`dns-free`的相关能力
3. **执行处理**: Agent按照核心能力章节的指令执行任务
4. **结果验证**: 检查输出结果是否符合预期，参考错误处理章节处理异常

## 适用场景

### 场景一： 个人域名迁移前TTL预热
- **输入**: 待迁移域名 example.com,当前TTL=86400s
- **处理**: 用 `dig +nocmd +noall +answer example.com` 探测当前缓存TTL;将TTL降至300s;等待原TTL过期后再切换
- **输出**: 当前TTL状态 + 降级建议 + 切换时机提示

### 场景二： SPF/DMARC基础配置检查
- **输入**: 域名 example.com,邮件发送后进入垃圾箱
- **处理**: 用 `dig TXT example.com` 检查SPF是否为单条TXT;检查结尾是否为 `-all`/`~all`;配置DMARC基础记录 `_dmarc.example.com"`
- **输出**: SPF配置状态 + DMARC配置建议

### 场景三： www子域访问排查
- **输入**: 用户反馈 www.example.com 无法访问,但 example.com 正常
- **处理**: 用 `dig www.example.com` 检查是否有A记录;确认apex与www是否同时配置;检查HTTPS重定向是否双域名证书
- **输出**: www记录状态 + 修复建议

## 调试命令参考

### dig基础命令
- `dig example.com`: 查询A记录,验证域名解析
- `dig TXT example.com`: 查询TXT记录,验证SPF/DMARC配置
- `dig MX example.com`: 查询MX记录,验证邮件路由
- `dig +nocmd +noall +answer example.com`: 精简输出,快速查看TTL与记录值
- `dig @8.8.8.8 example.com`: 指定Google解析器查询,对比缓存状态

### 诊断基础策略
1. 用 `dig TXT example.com` 确认SPF为单条TXT记录
2. 用 `dig +nocmd +noall +answer example.com` 探测当前缓存TTL
3. 用 `dig @8.8.8.8` 与 `dig @1.1.1.1` 对比,判断缓存传播进度

## 案例展示

### 案例1: 迁移后部分用户访问旧IP
**背景**: 将 example.com 迁移到新DNS商,A记录已更新,但部分用户仍命中旧IP.
**诊断过程**:
1. 用 `dig @8.8.8.8 example.com` 与 `dig @1.1.1.1 example.com` 对比,发现Google解析器仍返回旧IP
2. 检查原TTL,发现迁移前未降TTL(仍为86400s),旧缓存需24小时才过期

**修复**:
- 在旧DNS商保留记录同步至新IP,直到新DNS全球生效
- 下次迁移前48小时将TTL降至300s

### 案例2: SPF配置多条TXT导致邮件被拒
**背景**: 配置了SPF但向Gmail发送邮件仍被拒收.
**诊断过程**:
1. 用 `dig TXT example.com` 发现存在两条SPF TXT记录,这是无效配置
2. 检查SPF结尾,原为 `+all`(允许所有),需改为 `-all`

**修复**:
- 合并为单条TXT: `"v=spf1 include:_spf.google.com -all"`
- SPF结尾强制为 `-all` 或 `~all`,禁止 `+all`/`?all`

## 异常处理

### 1. dig返回SERVFAIL
**原因**: 权威服务器故障或DNSSEC签名问题
**处理**: 用 `dig +dnssec example.com` 查看DNSSEC状态;联系DNS托管商确认权威服务器健康

### 2. SPF记录被截断
**原因**: 单条TXT记录超过255字节或配置了多条SPF TXT
**处理**: 使用 `include:` 引用减少长度;SPF必须为单条TXT记录

### 3. DMARC报告未收到
**原因**: rua邮箱配置错误或目标域未授权接收
**处理**: 确认 `rua=mailto:` 邮箱可接收外部邮件;检查目标域授权配置

### 4. TTL修改后立即生效但随后回退
**原因**: 缓存层TTL未过期,存在中间缓存层独立缓存
**处理**: 用 `dig @ns1.provider.com example.com` 确认权威记录已更新;等待各缓存层TTL自然过期

### 5. www子域无法访问
**原因**: apex与www未同时配置,或HTTPS重定向缺少双域名证书
**处理**: 为apex和www分别配置记录;HTTPS重定向前确保证书覆盖两个域名

## FAQ

### Q1: 迁移前TTL应该提前多久降低?
A: 至少提前48小时将TTL降至300秒,确保旧TTL完全过期后再切换。降TTL前先用 `dig +nocmd +noall +answer example.com` 探测当前缓存TTL.
### Q2: SPF可以配置多条TXT记录吗?
A: 不可以。SPF必须为单条TXT记录,多条SPF TXT无效。多个发送源使用 `include:` 串联,如 `"v=spf1 include:_spf.google.com -all"`.
### Q3: DMARC的p=none/quarantine/reject有什么区别?
A: `p=none` 仅监控;`p=quarantine` 隔离至垃圾箱;`p=reject` 直接拒绝。建议从none开始观察,逐步升级.
### Q4: dig +trace和dig @ns有什么区别?
A: `dig +trace` 从根服务器逐级解析,展示完整解析链;`dig @ns1.provider.com` 直接查询权威服务器,绕过缓存。两者配合可定位缓存与权威不一致问题.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 无法直接修改DNS托管商记录,需配合控制台操作
- 不支持DKIM签名配置与CAA证书锁定(需升级付费版)
- 不支持Cloudflare代理行为分析与CNAME扁平化诊断(需升级付费版)
- DMARC的rua报告解析需额外工具,本版本不提供
- TTL传播时间受全球ISP缓存策略影响,无法精确预测

## 升级提示

以上为基础版能力,如需以下进阶功能,请升级到付费版 `dns`:

- DKIM签名配置与完整三件套(SPF/DKIM/DMARC)链路诊断
- CAA证书锁定与iodef安全事件告警通道
- Cloudflare橙云/灰云代理行为分析与CNAME扁平化迁移诊断
- dig +trace完整解析链路与权威/缓存响应比对
- 通配符记录规则与多级子域配置
- 通配符SSL证书DNS-01挑战签发指导
- 8个领域特定异常处理与6个深度FAQ
- 4个真实案例展示与完整调试命令参考

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "DNS配置基础版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dns"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
