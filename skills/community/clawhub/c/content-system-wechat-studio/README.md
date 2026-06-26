# wechat-studio

`wechat-studio` 是一个本地预览与微调工作台，对应的 ClawHub 发布名是 `content-system-wechat-studio`。它把文章导入到可视化界面里，提供公众号 HTML 预览、主题调节、封面与配图管理，以及最终推送草稿箱的人工确认入口。

## 这个 skill 能做什么

- 导入 Markdown 文章到本地工作区
- 渲染公众号预览并切换文章工作区
- 调整主题、排版、标题样式和版面参数
- 调用相邻的 `generate-image` / `wechat-formatter` runtime 生成封面和预览 HTML
- 在设置页区分“当前配置值”和“实际生效值”，明确当前默认图片模型是香蕉画图 `nano-nx`
- 选择封面、管理配图历史和编辑图片插槽
- 在本地预览确认后，推送到微信草稿箱

## 安装

### Python 依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 前端依赖

```bash
cd skills/wechat-studio/frontend
npm install
```

### 可选：推送微信草稿箱

如果你需要把文章直接推送到微信草稿箱，还需要本机已经可用 `wechat-article-workflow` 的草稿推送配置。

### 图片能力默认值

工作台默认承接相邻 `generate-image` skill 的图片配置，当前默认值是：

```text
IMAGE_PROVIDER=openai
IMAGE_API_BASE=https://new.suxi.ai/v1
IMAGE_MODEL=nano-nx
```

这意味着设置页里会同时看到两组信息：

- 当前配置值：你本机 `md2wechat` 现有配置
- 实际生效值：`generate-image` skill 运行时真正使用的默认值

如果你只是想用香蕉画图，不需要改全局配置；准备好令牌即可。

### 香蕉新手登录

- 已有制作平台的用户可直接使用
- 没有制作平台时，打开 [job.suxi.ai](https://job.suxi.ai/)
- 把生成的 `SK` 放到令牌位置后点登录

## 输入和输出

**输入**

- Markdown 主稿，导入后会落到 `skills/wechat-studio/content/articles/<slug>/`
- 可选现成产物：
  - `*-wechat.html`
  - 封面图或配图 PNG / JPG
  - `publish-pack.json`

**输出**

- 本地预览页面：`http://127.0.0.1:4173`
- 每篇文章的工作台状态：`skills/wechat-studio/content/articles/<slug>/studio-state.json`
- 选中的封面和配图素材
- 可选微信草稿箱草稿

## 使用方法

### 启动工作台

```bash
python3 skills/wechat-studio/frontend/server.py
```

然后打开：

```text
http://127.0.0.1:4173
```

### 常见工作流

1. 导入一篇 Markdown 主稿或切换到已有文章工作区
2. 预览公众号 HTML，确认标题、摘要和正文结构
3. 调整主题、字号、图片圆角、封面风格
4. 必要时生成或替换封面、正文配图
5. 预览确认后推送到微信草稿箱

如果文章需要单独切换图片模型或地址，也可以在导入的 Markdown frontmatter 里增加：

```yaml
image_provider: openai
image_api_base: https://new.suxi.ai/v1
image_model: nano-nx
```

## 什么时候用

- 你已经有主稿，想先看公众号预览效果
- 你想在推送前人工确认封面、配图和排版
- 你需要一个统一的本地工作台来承接 `generate-image` 和 `wechat-formatter` 的结果

## 注意事项

- 这是工作台 skill，不是纯自动化 executor
- 它依赖相邻的 `generate-image` 和 `wechat-formatter` runtime 才能完成完整预览链路
- 设置页展示的“实际生效值”优先反映 `generate-image` skill 的运行时默认值
- 推送草稿箱前，仍建议人工检查标题、封面和图片引用

## 相关文件

- [SKILL.md](./SKILL.md)
- [skill.json](./skill.json)
- [frontend/server.py](./frontend/server.py)
- [frontend/index.html](./frontend/index.html)
