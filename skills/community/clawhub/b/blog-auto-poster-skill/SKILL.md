---
name: blog-auto-poster-skill
license: MIT
allowed-tools: Bash
description: >-
  多平台文章统一发布与同步工具。支持 CSDN、51CTO、博客园、掘金四个平台。
  触发场景：用户需要将文章、博客、Markdown 文件的内容分发或群发到指定平台。
  典型指令如：“帮我把这段文字发布到所有平台”、“把这个 MD 文件同步到 CSDN”、“一键群发这篇博客”。
---

# 多平台统一发布 Skill

## 发布流程

### 1. 检查凭证

检查 `.env` 是否存在且包含目标平台的配置项，如有缺失则引导用户配置。

```bash
ls -la .env
grep "CSDN_COOKIES=" .env
grep "51CTO_COOKIES=" .env
grep "CNBLOGS_COOKIES=" .env
grep "JUEJIN_COOKIES=" .env
```

各平台凭证获取方式见 `references/<平台>.md`。

### 2. 明确需求

#### (a) 选择发帖模板

模板文件位于 `templates/` 目录，提供以下模板供用户选择：

| 模板 | 文件 | 适用场景 |
|------|------|----------|
| `default` | `templates/default.md` | 通用技术文章 |
| `tool-review` | `templates/tool-review.md` | 工具/软件推荐测评 |
| `deep-dive` | `templates/deep-dive.md` | 底层原理/源码深度解析 |
| `comparison` | `templates/comparison.md` | 技术选型对比分析 |
| `troubleshooting` | `templates/troubleshooting.md` | 踩坑记录/排错指南 |
| `summary` | `templates/summary.md` | 知识总结/学习笔记 |

引导用户说出文章的大致主题和受众，推荐合适的模板。

#### (b) 确认信息

与用户确认以下内容：
- **标题**
- **标签**
- **正文内容**（基于选定的模板填充）
- **目标平台**（全部四个，或指定子集）

### 3. 写入临时文件

将正文以 **Markdown 格式** 写入临时文件：

```bash
mkdir -p temp
cat > ./temp/publish.md << 'EOF'
<Markdown 正文>
EOF
```

### 4. 按序发布

按以下顺序逐个发布，**失败不中断**。每个平台执行后记录状态。

所有命令在 skill 根目录下执行。

---

#### CSDN

内容格式：Markdown（加 `--format markdown` 让脚本自动转 HTML）

```bash
python scripts/csdn_poster.py post \
  --title "<标题>" \
  --file ./temp/publish.md \
  --format markdown \
  --tags "标签1,标签2" \
  --categories "分类名" \
  --publish
```

可选参数：
- `--desc "摘要"` — 自定义摘要
- `--type original|reprint|translated` — 文章类型
- `--read-type public|private|fans` — 阅读权限
- 不加 `--publish` 则存为草稿

- 成功标志：返回 `发布成功！` + `链接: https://blog.csdn.net/...`
- 失败：查看 `references/csdn.md`

---

#### 51CTO

内容格式：Markdown（脚本自动转 HTML）

```bash
python scripts/51cto_poster.py post \
  --title "<标题>" \
  --file ./temp/publish.md \
  --tags "标签1,标签2"
```

可选参数：
- `--type original|reprint|translated` — 默认 original
- `--draft` — 存草稿

- 成功标志：返回 `发布成功！` + `链接: https://blog.51cto.com/...`
- 失败：查看 `references/51cto.md`

---

#### 博客园

内容格式：**原生 Markdown**（博客园 isMarkdown=true，不需要转 HTML）

```bash
python scripts/cnblogs_poster.py post \
  --title "<标题>" \
  --file ./temp/publish.md \
  --tags "标签1,标签2"
```

可选参数：
- `--category "分类ID"` — 多个用逗号分隔
- `--draft` — 存草稿

- 成功标志：返回 `发布成功！` + `链接: https://www.cnblogs.com/...`
- 失败：查看 `references/cnblogs.md`

---

#### 掘金

内容格式：**原生 Markdown**（掘金的 `mark_content` 字段原生支持 Markdown）
鉴权方式：仅需 Cookie（无需 CSRF 请求头，只需在 `.env` 中配置 `JUEJIN_COOKIES` 即可）

```bash
python scripts/juejin_poster.py post \
  --title "<标题>" \
  --file ./temp/publish.md \
  --brief "摘要（50-100 字）"
```

可选参数：
- `--tags 标签名1 标签名2` — 传入**标签名称**（脚本支持常见标签自动映射）
- `--draft-only` — 仅存草稿，不发布
- `--category <分类ID>` — 分类 ID（默认 `0`）

**常用标签（名称自动映射）：**

| 名称 | ID |
|------|-----|
| Python | `6809640408797167623` |
| TypeScript | `6809640543006490638` |
| JavaScript | `6809640407484334093` |
| Vue.js | `6809640445233070094` |
| React | `6809640407484334100` |
| Node.js | `6809640361531539470` |
| CSS | `6809640394175971342` |
| Go | `6809640408797167624` |
| Java | `6809640445233070094` |
| Rust | `6809640495594078216` |
| C++ | `6809640447497994253` |
| Swift | `6809640463633481741` |
| Kotlin | `6809640615584727053` |
| Docker | `6809640445233070095` |
| Spring Boot | `6809641037787561992` |
| AI | `6809640445233070096` |
| DeepSeek | `7467857238493757466` |
| LLM | `7257794499869573175` |
| AIGC | `7197380506562871333` |
| Agent | `7516396389476401162` |
| 前端 | `6809640407484334093` |
| 后端 | `6809640408797167623` |
| Android | `6809640400832167949` |
| iOS | `6809640399544516616` |
| 架构 | `6809640501776482317` |
| 数据库 | `6809640600502009863` |
| 云计算 | `6809640508441231367` |
| 开源 | `6809640419505209358` |

**常用分类 ID：**

| 名称 | ID |
|------|-----|
| 前端 | `6809637767543259144` |
| 后端 | `6809637769959178254` |
| AI | `6809637773935378440` |
| Android | `6809635626879549454` |
| iOS | `6809635627209637895` |
| 开发工具 | `6809637771511070734` |
| 阅读 | `6809637772874219534` |

> 非常用标签/分类请查阅 `references/juejin.md`。

- 成功标志：返回 `发布成功！` + `链接: https://juejin.cn/post/...`
- 失败：查看 `references/juejin.md`

---

### 5. 汇总结果

所有平台执行完毕后，按此格式汇总给用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  多平台发布结果汇总
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ CSDN     发布成功  https://blog.csdn.net/...
  ✅ 51CTO    发布成功  https://blog.51cto.com/...
  ❌ 博客园   失败     错误信息摘要
  ✅ 掘金     发布成功  https://juejin.cn/post/...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

失败的平台引导用户查看对应的 `references/<平台>.md` 了解原因和解决方法。

## 注意事项

1. **失败不中断**：一个平台失败不影响其他平台继续发布
2. **临时文件**：发布完成后不自动删除 `./temp/publish.md`，保留供用户复查
3. **Cookie 过期**：各平台 Cookie 过期时间不同，发布失败时优先检查 `.env` 中的凭证
4. **CSDN 审核**：部分内容可能触发人工审核，发布后不保证即时可见
5. **掘金频率限制**：发布过于频繁会返回 `err_no: 1002`，需等待 30 秒以上重试
6. **凭证配对**：掘金的 Cookie 和 CSRF Token 必须来自同一次浏览器会话，不可混用
