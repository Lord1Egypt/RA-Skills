# 🦞 Amber Url to Markdown

> 智能 URL 转 Markdown 工具 - 一键抓取网页内容，生成完整 Markdown 文档

**版本**: V3.0  
**更新时间**: 2026-03-24  
**作者**: 小文  
**许可**: MIT

---

## 🎯 快速开始

### 在飞书中使用

**最简单的方式 - 直接发送链接**：
```
https://mp.weixin.qq.com/s/xxx
```

**或添加说明**：
```
帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
```

### 效果示例

**输入**：
```
https://mp.weixin.qq.com/s/mpf7EidCn_p6vvIOR2om_Q
```

**输出**：
```
✅ 抓取成功（方案一：Playwright）
📄 标题：劲爆！个人微信官方接入龙虾了【喂饭级教程】
📊 字数：1133
🖼️ 图片：11 张
⏱️ 耗时：9.4 秒
📂 目录：/root/openclaw/urltomarkdown
```

---

## ✨ 核心特性

### 1. 智能识别

自动识别链接类型，使用最优策略：

| 网站 | 识别 | 状态 |
|------|------|------|
| 微信公众号 | ✅ 自动 | 完美支持 |
| 知乎 | ✅ 自动 | 支持 |
| 掘金 | ✅ 自动 | 支持 |
| CSDN | ✅ 自动 | 支持 |
| GitHub | ✅ 自动 | 支持 |
| Medium | ✅ 自动 | 支持 |
| 其他网页 | ✅ 自动 | 通用支持 |

### 2. 自动降级

三种抓取方案，确保成功率：

```
方案一：Playwright 无头浏览器（首选 - 支持所有网站）
    ↓ 失败
方案二：Scrapling（备选 - 支持所有网站）
    ↓ 失败
方案三：第三方 API（保底 - 仅微信）
```

### 3. 图片下载

所有图片自动下载到本地：

```
/root/openclaw/urltomarkdown/
├── 文章标题.md          # Markdown 文件
└── images/
    └── knowledge_时间戳/
        ├── img_001.jpg
        ├── img_002.jpg
        ...
```

### 4. 完整格式

保留完整的 Markdown 格式：

```markdown
# 文章标题

> 链接：https://...  
> 抓取时间：2026-03-24 12:34:56  
> 图片数量：11 张  
> 网站类型：微信公众号

---

正文内容...

![图片](images/knowledge_时间戳/img_001.jpg)
```

### 5. 合规性检查

- ✅ robots.txt 协议检查
- ✅ 浏览器 UA 模拟
- ✅ 请求限流与随机延迟

---

## 📋 触发条件

### 自动触发

**条件 1：消息中只有 URL**
```
https://mp.weixin.qq.com/s/xxx
```

**条件 2：URL + 解析意图**
```
帮我解析这个链接
请把这个 URL 转成 Markdown
下载这篇文章
```

### 手动调用

用户明确指定：
```
使用 Amber_Url_to_Markdown 处理
```

---

## 🚀 使用方式

### 飞书聊天（推荐）

```
# 直接发送链接
https://mp.weixin.qq.com/s/xxx

# 或添加说明
帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
```

### 命令行

```bash
python3 scripts/amber_url_to_markdown.py <URL>
```

### Python 调用

```python
from amber_url_to_markdown import fetch_url_to_markdown

result = fetch_url_to_markdown("https://mp.weixin.qq.com/s/xxx")
print(f"文件已保存：{result['file']}")
```

---

## 📊 性能对比

| 方案 | 速度 | 图片 | 格式 | 成功率 | 支持网站 |
|------|------|------|------|--------|----------|
| **Playwright** | 10s | ✅ 本地 | ✅ 完整 | ⭐⭐⭐⭐⭐ | 所有 |
| **Scrapling** | 5s | ✅ 本地 | ✅ 完整 | ⭐⭐⭐⭐ | 所有 |
| **第三方 API** | 5s | ✅ 本地 | ✅ Markdown | ⭐⭐⭐⭐ | 仅微信 |

---

## 🛠️ 安装依赖

### 基础安装

```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 完整安装（包含开发工具）

```bash
# 安装所有依赖（含开发工具）
pip install -r requirements.txt --upgrade

# 安装 Playwright 浏览器
playwright install chromium
```

---

## 🧪 运行测试

```bash
# 方式 1：使用测试脚本
./run_tests.sh

# 方式 2：直接使用 pytest
pytest tests/ -v
```

### 测试覆盖

- ✅ URL 请求测试（正常、404、超时、无效）
- ✅ HTML 解析测试（标题提取、Markdown 转换）
- ✅ 工具函数测试（标题清理、时间戳、目录管理）
- ✅ 链接类型识别测试（微信、知乎、掘金等）

---

## 📁 项目结构

```
amber-url-to-markdown/
├── scripts/
│   ├── amber_url_to_markdown.py    # 主入口
│   ├── fetcher.py                  # URL 请求模块（含 robots.txt 检查）
│   ├── parser.py                   # HTML 解析模块
│   ├── utils.py                    # 工具函数模块
│   └── url_handler.py              # URL 类型识别
├── tests/
│   └── test_amber_url_to_markdown.py  # 单元测试
├── third_party/
│   └── fetch-wx-article/           # 第三方 Scrapling 实现
├── requirements.txt                # 依赖列表
├── pyproject.toml                  # 项目配置
├── run_tests.sh                    # 测试运行脚本
├── README.md                       # 使用文档
├── SKILL.md                        # OpenClaw 技能说明
└── _meta.json                      # ClawHub 元数据
```

---

## 🔧 代码质量

### 代码规范

```bash
# 代码格式化
black scripts/ tests/

# 代码检查
flake8 scripts/ tests/
```

### 模块化设计

- **fetcher.py** - URL 请求（普通/动态/批量）
- **parser.py** - HTML→Markdown 转换
- **utils.py** - 工具函数（标题清理、文件保存、图片下载）
- **url_handler.py** - URL 类型识别与配置

---

## 🔍 故障排查

### 常见问题

**Q: 脚本报错 "playwright not found"**
```bash
pip install playwright
playwright install chromium
```

**Q: 抓取内容为空**
- 检查链接是否有效
- 可能触发反爬（自动降级到其他方案）
- 查看详细日志

**Q: 图片下载失败**
- 检查网络连接
- 查看日志中的具体错误
- 图片链接可能已失效

**Q: 触发 robots.txt 限制**
- 检查目标网站是否允许爬取
- 手动确认是否继续

### 查看详细日志

脚本默认输出详细日志：
```
[17:18:32.157] [BROWSER] 启动浏览器...
[17:18:32.557] [BROWSER] 浏览器启动成功
[17:18:35.230] [NAVIGATE] 页面加载成功，耗时=3.1s
...
```

---

## 📝 使用示例

### 示例 1：微信公众号

**输入**：
```
https://mp.weixin.qq.com/s/mpf7EidCn_p6vvIOR2om_Q
```

**输出**：
```
✅ 抓取成功
📄 标题：劲爆！个人微信官方接入龙虾了【喂饭级教程】
📊 字数：1133
🖼️ 图片：11 张
⏱️ 耗时：9.4 秒
```

### 示例 2：知乎

**输入**：
```
帮我解析这篇知乎文章：https://zhuanlan.zhihu.com/p/xxx
```

**输出**：
```
✅ 抓取成功
📄 标题：如何评价 XXX？
📊 字数：5000
🖼️ 图片：20 张
⏱️ 耗时：12.3 秒
```

### 示例 3：GitHub

**输入**：
```
https://github.com/xxx/xxx/blob/main/README.md
```

**输出**：
```
✅ 抓取成功
📄 标题：Project README
📊 字数：2000
🖼️ 图片：5 张
⏱️ 耗时：8.5 秒
```

---

## ⚠️ 注意事项

### 1. 链接格式

确保链接完整：
```
✅ https://mp.weixin.qq.com/s/xxx
❌ mp.weixin.qq.com/s/xxx
```

### 2. 网络要求

需要稳定的网络连接：
- 访问目标网站
- 下载图片资源

### 3. 图片下载

- 默认启用图片下载
- 图片保存在 `images/` 子目录
- 使用相对路径引用

### 4. 合规性

- 遵循 robots.txt 协议
- 批量请求时自动限流
- 浏览器 UA 模拟

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - OpenClaw 技能详细说明
- [_meta.json](_meta.json) - ClawHub 元数据
- [requirements.txt](requirements.txt) - Python 依赖列表

---

## 🎉 总结

**Amber Url to Markdown V3.0** 是一个专业级的 URL 转 Markdown 工具：

### 核心优势

- ✅ **自动识别** - 识别链接类型
- ✅ **多网站支持** - 微信公众号、知乎、掘金等
- ✅ **图片下载** - 自动下载所有图片
- ✅ **完整格式** - 保留 Markdown 格式
- ✅ **自动降级** - 三种方案确保成功率
- ✅ **详细日志** - 便于排查问题
- ✅ **合规性** - robots.txt 检查、限流
- ✅ **模块化** - 清晰的代码结构
- ✅ **测试覆盖** - 完整的单元测试

### V3.0 新特性

1. **模块化重构** - 代码拆分为 fetcher、parser、utils 三个模块
2. **错误处理增强** - 全量异常捕获和兜底
3. **合规性检查** - robots.txt 协议遵循
4. **单元测试** - pytest 测试覆盖核心功能
5. **代码规范** - black 格式化、flake8 检查
6. **时间戳优化** - 确保图片路径一致性

**使用方式简单**：
```
发送链接 → 自动抓取 → 生成 Markdown
```

---

**版本**: V3.0  
**创建时间**: 2026-03-22  
**更新时间**: 2026-03-24  
**作者**: 小文  
**许可**: MIT
