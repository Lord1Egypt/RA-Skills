# Step 7: 提交草稿

**目标：** 完成所有检查后，提交到微信公众号草稿箱

## 输出产物清单

所有产物都应该存放在规范目录：

```
工作区/work/output/{YYYYMMDD}-{文章标题}/
├── article.md              # 原始文章（Markdown）
├── article.html            # HTML排版后的文章
├── images/
│   ├── cover.jpg           # 封面图
│   └── article-*.jpg       # 文章配图
└── draft.json             # 微信公众号草稿信息
```

## 提交前检查清单

- [ ] 文章已通过用户审阅
- [ ] 配图已生成并确认
- [ ] AI味检测通过（LOW）
- [ ] HTML排版已完成
- [ ] 封面图已包含在HTML中
- [ ] 文章内配图全部生成
- [ ] 数据来源已标注
- [ ] 作者署名正确

## 脚本使用

直接运行脚本，自动完成：获取access\_token → 上传图片 → 发布草稿 全流程：

```bash
node ${SKILL_DIR}/scripts/submit-draft.js --html 工作区/output/YYYYMMDD-标题/article.html --title "文章标题"
```

**参数说明：**

- `--html`: HTML文件路径（必填，生成好的文章HTML）
- `--title`: 文章标题（必填，和HTML中标题一致）
- `--author`: 作者名称（选填，若为空则默认使用"虾看虾说"）
- `--digest`: 文章摘要（选填，若为空将默认使用正文的前64字）

## 流程说明

1. **获取access\_token**：从微信API获取接口调用凭证
2. **解析HTML**：自动提取HTML中的所有图片
3. **上传图片**：将所有本地图片上传到微信素材库
4. **发布草稿**：将文章内容和封面图发布到微信公众号草稿箱
5. **保存结果**：将草稿信息保存到 `draft.json` 中，包含 `draft_id` 和所有上传图片的 `media_id`

## 结果验证

脚本执行成功后，会输出草稿ID，可以登录微信公众号后台 → 新建草稿 → 查看最新草稿确认发布成功。
