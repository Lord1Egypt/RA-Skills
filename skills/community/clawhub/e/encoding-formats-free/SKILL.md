---
slug: "encoding-formats-free"
name: "encoding-formats-free"
version: "1.0.0"
displayName: "编码格式工具(免费版)"
summary: "编码解码与数据格式转换，覆盖Base64、URL编码、Hex、Unicode、JWT、哈希、序列化(免费版)"
summary_zh: "编码解码与数据格式转换，覆盖Base64、URL编码、Hex、Unicode、JWT、哈希、序列化(免费版)"
license: "MIT"
description: "|-. 适用于需要encoding formats相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  编码解码与数据格式转换工具，覆盖Base64、URL编码、Hex、Unicode、JWT解码、
  哈希校验和序列化格式转换。支持命令行和代码两种方式，适用于API响应解码、
  HTTP请求参数编码、二进制数据检查、JWT令牌分析、文件完整性校验等场景.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 通用办公
  - encoding
  - formats
  - automation
  - productivity
  - 工具
  - 效率
  - 安全
  - 加密
  - base64
category: "Automation"
pricing_tier: free
---
# 编码格式工具(免费版)

编码、解码和检查常见数据格式。覆盖Base64、URL编码、Hex、Unicode、JWT、哈希校验和序列化格式.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 编码格式工具(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力

### 1. Base64编码解码
支持标准Base64和URL安全Base64（RFC 4648）变体。Base64使数据增大约33%，适用于在文本格式中嵌入二进制数据.
```bash
echo -n "Hello, World!" | base64
# 输出: SGVsbG8sIFdvcmxkIQ==
# ...
echo "SGVsbG8sIFdvcmxkIQ==" | base64 -d
# 输出: Hello, World!
# ...
# URL安全变体
echo -n "Hello" | base64 | tr '+/' '-_' | tr -d '='
```- 验证返回数据的完整性和格式正确性
- 参考`Base64编码解码`的配置文档进行参数调优
### 2. URL编码解码
对HTTP请求参数进行编码，处理特殊字符和空格.
```bash
python3 -c "from urllib.parse import quote; print(quote('hello world & foo=bar'))"
# 输出: hello%20world%20%26%20foo%3Dbar
# ...
parse import unquote; print(unquote('hello%20world%20%26%20foo%3Dbar'))"
# 输出: hello world & foo=bar
```- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `url编码解码` 选项
- 处理流程: 接收输入 -> 执行URL编码解码 -> 返回结果
- 输入: 用户提供URL编码解码所需的参数和指令

### 3. Hex查看与转换
查看二进制文件的十六进制转储，在Hex和文本之间转换.
```bash
xxd -p file.bin          # 纯Hex输出
xxd -l 64 file.bin       # 前64字节
echo "48656c6c6f" | xxd -r -p   # Hex转文本: Hello
```

- 异常时参考错误处理章节进行恢复
- 关键参数: `hex查看与转换` 选项

### 4. JWT解码
解码JWT令牌的header和payload（JWT是签名而非加密，任何人可解码）.
```bash
TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
echo "$TOKEN" | cut -d. -f2 | tr '-_' '+/' | base64 -d 2>/dev/null | jq
# 输出: {"sub": "1234567890", "name": "John Doe"}
```

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| API响应解码 | Base64编码数据 | 解码后的原始数据 |
| HTTP请求编码 | 含特殊字符的参数 | URL编码后的字符串 |
| JWT令牌分析 | JWT token | 解码后的header和payload |

## 使用流程

1. 确定需要编码或解码的数据格式
2. 选择对应的命令行工具(base64/url编码/hex/JWT)
3. 执行编码或解码操作
4. 验证结果正确性

#
## 示例

### 示例:解码API响应中的Base64图片

```bash
base64 -d image.b64 > image.png
# 将Base64编码的图片数据解码并保存为PNG文件
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| Base64解码失败 | 输入包含非Base64字符或padding错误 | 检查输入是否为有效Base64，添加 `=` padding |
| Mojibake（乱码） | 文件编码假设错误 | 用 `file -bi` 检测实际编码，用 `iconv` 转换 |
| JWT解码返回乱码 | Base64url使用 `-` 和 `_` 而非 `+` 和 `/` | 先 `tr '-_' '+/'` 转换再解码，添加padding |
| BOM导致解析错误 | UTF-8 BOM（`EF BB BF`）在文件开头 | 用 `sed -i '1s/^\xEF\xBB\xBF//' file.txt` 移除 |

## 常见问题

### Q1: Base64使数据增大多少？
A: Base64使数据增大约33%（每3字节编码为4字符）。适用于在JSON、XML、邮件等文本格式中嵌入二进制数据，不适用于压缩或加密.
### Q2: Base64url和标准Base64有什么区别？
A: Base64url（RFC 4648）使用 `-` 和 `_` 替代 `+` 和 `/`，并省略padding `=`。JWT和URL参数使用此变体。转换方法：`tr '+/' '-_'` 和 `tr -d '='`.
### Q3: JWT是加密的吗？
A: JWT是签名的，不是加密的。任何人都可以解码header和payload。只有签名用于验证真实性。切勿在JWT claims中放置敏感信息.
## 已知限制

- Base64不提供压缩或加密功能，仅做编码转换
- JWT解码不需要密钥，但验证签名需要密钥
- `xxd -p` 和 `xxd -r -p` 是命令行最快的二进制与Hex互转方式

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
如需调用外部API，请参考环境配置章节设置对应密钥

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 升级提示

本免费版提供基础功能。升级到完整版 encoding-formats 获取全部能力和高级特性.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "编码格式工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "encoding-formats"
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
