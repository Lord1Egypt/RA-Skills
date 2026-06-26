# arxiv-to-zotero

[English version / 英文版](README.md)

这是一个用于 **查找近期 arXiv 论文并把真正的新论文导入 Zotero** 的 OpenClaw skill。它会自动去重、尽量附加 PDF，并把新建父条目统一打上 `arxiv-to-zotero` 标签，放进 `arxiv-to-zotero` 分类中。

## 为什么这个 skill 值得装

它针对的是一个非常常见、但反复做很烦的科研流程：

- 在 arXiv 上找新论文
- 写入 Zotero 前先去重
- 尽量自动附加 PDF
- 统一标签和分类，保持 Zotero 干净
- 不去碰已有的 Zotero 条目

一句话概括：**把“找 arXiv 新论文并整理进 Zotero”这件事，压缩成一次稳定的自动流程。**

## 它会做什么

agent 会：

1. 收集主题关键词或短语，以及时间范围
2. 在内部构造一条合法的 arXiv `search_query`
3. 在 arXiv 上检索近期论文
4. 与 Zotero 现有条目去重
5. 只导入新的论文
6. 给新建父条目统一打上 `arxiv-to-zotero` 标签
7. 将新导入内容放入 `arxiv-to-zotero` 分类；若不存在则自动新建
8. 返回一次最终总结

## 典型请求示例

- 帮我找近三年来用 Mamba 做股票预测的论文，并把新的导入 Zotero。
- 搜索近几年关于多模态用于股票预测的论文，和 Zotero 去重后，只导入新的。
- 帮我查近期关于 test-time adaptation 和 active search 的 arXiv 论文，只保存我 Zotero 里还没有的条目。

## 运行要求

- Python 3.10+
- `curl`
- 通过 `ZOTERO_API_KEY` 访问 Zotero Web API
- OpenClaw skill 运行环境

## 首次运行

如果 setup-state 文件不存在，skill 会：

1. 读取 [`setup.md`](setup.md)
2. 收集所需的 Zotero 配置
3. 将非敏感配置写回 `config.json`
4. 创建 setup-state 文件
5. 精确恢复并继续原始请求一次

## agent 应该如何使用这个 skill

推荐的交互方式是：

1. 收集主题关键词或短语
2. 收集时间范围
3. 如用户给出中文关键词，先翻译成简洁、准确的英文技术短语
4. 在内部构造一条合法的英文 arXiv `search_query`
5. 只调用脚本一次

示例：

```bash
python3 scripts/main.py --config ./config.json --query '(all:"Mamba" OR all:"state space model") AND (all:"stock prediction" OR all:"financial prediction" OR all:"market prediction" OR all:"price forecasting") AND submittedDate:[202304010000 TO 202604092359]'
```

## 关键行为说明

### 论文来源

这个 skill **只使用 arXiv** 作为论文发现来源。

### 去重策略

脚本会从三类范围预热 Zotero 缓存：

- 由查询语句拆出的 Zotero quick-search 词
- 固定技能标签 `arxiv-to-zotero`
- 已存在时的目标分类 `arxiv-to-zotero`

随后基于以下规则判断是否已存在：

- 标准化标题的精确匹配
- 标准化标题前缀的严格匹配
- 在可用时使用 arXiv ID 匹配

已有 Zotero 条目会被跳过，且不会被修改。

### PDF 附件处理

对每个新导入的父条目，脚本会根据论文 URL 推导 PDF 候选链接。

它会优先尝试把 PDF 作为真正的 Zotero 文件附件上传。如果 Zotero 返回 `413 Request Entity Too Large`，脚本会删除未完成上传，改为 `linked_url` 方式附加，并在本轮后续条目中继续使用链接模式。

### 组织规则

默认情况下，脚本会按下面的固定规则整理导入结果：

- 父条目统一打上 `arxiv-to-zotero` 标签
- 子 PDF 附件不打标签
- 父条目放入 `arxiv-to-zotero` 分类
- 如果该分类不存在，脚本会自动创建

### 导入上限

当新建 Zotero 父条目数量达到 `import_policy.max_new_items` 后，脚本会停止继续创建。默认上限是每轮 50 篇。

## 固定运行路径

- 默认非敏感配置：skill 根目录下的 `./config.json`
- setup 状态文件：`~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- 密钥 / 环境变量：`~/.openclaw/.env`

## 仓库结构

- [`SKILL.md`](SKILL.md)：skill 定义与运行说明
- [`setup.md`](setup.md)：首次运行配置说明
- [`SECURITY.md`](SECURITY.md)：安全边界与风险说明
- [`scripts/main.py`](scripts/main.py)：主脚本实现
- [`config.json`](config.json)：默认非敏感配置

## 安全与隐私

这个 skill 会访问：

- arXiv Atom API
- arXiv PDF 链接
- Zotero Web API

这个 skill：

- 创建新的 Zotero 条目和附件
- 不修改已有的 Zotero 条目
- 使用 `ZOTERO_API_KEY` 访问 Zotero API

更多细节请见 [`SECURITY.md`](SECURITY.md)。

## 备注

- 这个脚本只适用于一次直接程序调用。
- 不要使用 `&&`、`;`、管道或串联 `cd` 等 shell 组合方式。
- 查询参数的 URL 编码由脚本自身处理，不要手动预编码空格、引号或括号。
