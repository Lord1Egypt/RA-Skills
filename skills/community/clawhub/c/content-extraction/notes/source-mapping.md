# Source Mapping: markdown-proxy → OpenClaw

## 1. SKILL.md

### markdown-proxy 做了什么
- 定义 URL 路由
- 说明代理级联顺序
- 给出使用方法与示例

### OpenClaw 版怎么做
- 用 OpenClaw skill 入口描述路由逻辑
- 直接写明 browser / feishu / web_fetch 的优先级
- 保留 Markdown 输出模板

---

## 2. scripts/fetch_weixin.py

### markdown-proxy 做了什么
- Playwright 打开公众号页
- 等待 `#js_content`
- 提取标题 / 作者 / 发布时间 / 正文 / 图片
- 输出 Markdown frontmatter

### OpenClaw 版怎么做
- 不再硬写 Playwright 依赖
- 改为调用 browser 技能链
- 继续保留：
  - 标题提取
  - 作者提取
  - 发布时间提取
  - 正文清洗
  - 图片链接保留

### 可直接复用的逻辑
- 微信页面的 DOM 选择器思路
- Markdown frontmatter 格式
- 图片转 `![image](url)` 的策略

---

## 3. scripts/fetch_feishu.py

### markdown-proxy 做了什么
- 用飞书 token 拉取文档 blocks
- 支持 docx / doc / wiki
- 将 block 结构映射为 Markdown
- 对多种 block 类型做格式化处理

### OpenClaw 版怎么做
- 不再自己维护 Feishu SDK 调用
- 直接使用 OpenClaw feishu 工具
- 核心保留 block→Markdown 的转换思路

### 可直接复用的逻辑
- URL 类型解析
- wiki → 实际节点解析
- block 类型到 Markdown 的映射规则
- 代码块语言映射表

---

## 4. 通用 URL 降级链

### markdown-proxy 做了什么
- r.jina.ai
- defuddle.md
- agent-fetch
- defuddle CLI

### OpenClaw 版怎么做
- 继续保留前两层代理思想
- 第三层改用 web_fetch / browser fallback
- 可视需要加本地代理工具

---

## 5. 需要重新设计的部分

- Claude Code 路径和安装方式
- 依赖声明方式
- 调用接口格式
- 保存文件策略
- OpenClaw 内部工具调用优先级

---

## 结论

这不是简单移植，而是：

1. 保留 markdown-proxy 的**路由设计**
2. 替换成 OpenClaw 的**工具实现**
3. 用 OpenClaw 的 skill 体系重新封装