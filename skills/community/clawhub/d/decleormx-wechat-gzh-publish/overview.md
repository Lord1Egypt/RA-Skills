# 📱 Skill 打包完成：微信公众号自动发布

## 工作总结

✅ **已完成**：将完整的公众号发布流程打包成 Skill 包，支持跨电脑使用

### 📦 Skill 信息

| 字段 | 值 |
|------|-----|
| **Skill ID** | `decleormx_wechat_gzh_publish` |
| **名称** | 微信公众号 AI 配图自动发布工具 |
| **范围** | project rule（项目级别） |
| **注册位置** | `.workbuddy/rules/decleormx_wechat_gzh_publish.mdc` |

### 📂 文件结构

```
/Users/zengxiang/Library/Application Support/WorkBuddy/User/globalStorage/tencent-cloud.coding-copilot/brain/68fb9ee6e6dc4dde97af07e7fcda1c47/
├── SKILL.md                          # 完整文档（核心参考）
├── README.md                         # 快速开始指南
├── scripts/
│   ├── publish.py                    # 主发布脚本（完整实现）
│   └── requirements.txt               # Python 依赖
└── [artifacts registered as rule]
```

### 🎯 功能完整性清单

- ✅ 自动登录（首次扫码，后续自动复用 Cookie）
- ✅ 自动填写标题、正文（支持富文本）
- ✅ **AI 配图双用**（既作为封面，又插入正文底部）
- ✅ AI 配图失败自动降级到图片库
- ✅ 支持自定义 AI 提示词（`--ai-prompt` 参数）
- ✅ 支持草稿保存 / 直接发布
- ✅ 支持自定义摘要、留言、赞赏设置
- ✅ 支持从文件读取长文本
- ✅ 自动保存调试截图

### 🚀 在其他电脑上使用

#### 方法一：直接复制脚本

```bash
# 1. 从 artifacts 目录拷贝 scripts/publish.py 到新电脑
cp /Users/zengxiang/Library/Application\ Support/WorkBuddy/User/globalStorage/tencent-cloud.coding-copilot/brain/68fb9ee6e6dc4dde97af07e7fcda1c47/scripts/publish.py ~/new_location/

# 2. 安装依赖
pip3 install playwright

# 3. 首次登录
python3 publish.py --login

# 4. 发布文章
python3 publish.py --title "标题" --content "内容"
```

#### 方法二：使用 Skill Manager

1. 在 WorkBuddy 中找到 `decleormx_wechat_gzh_publish` Skill
2. 「导出」或「共享」选项
3. 在新电脑上导入

### 📋 快速参考命令

```bash
# 首次登录
python3 publish.py --login

# 保存草稿测试
python3 publish.py --title "标题" --content "内容" --draft

# 直接发布
python3 publish.py --title "标题" --content "内容"

# 自定义 AI 提示词
python3 publish.py --title "标题" --content "内容" --ai-prompt "AI,猫,萨克斯" --draft

# 从文件读取
python3 publish.py --title "标题" --content-file ~/article.txt --draft

# 完整配置
python3 publish.py \
  --title "标题" \
  --content "内容" \
  --ai-prompt "自定义提示词" \
  --abstract "摘要" \
  --reward \
  --draft
```

## 📖 文档位置

| 文档 | 位置 | 用途 |
|------|------|------|
| **SKILL.md** | artifacts 目录 | **核心参考**（完整文档、故障排查、进阶用法） |
| **README.md** | artifacts 目录 | 快速开始（5分钟上手） |
| **publish.py** | scripts/ | 实现代码（可直接使用） |
| **规则文件** | `.workbuddy/rules/` | WorkBuddy 注册 |

## 🔧 核心技术细节

### AI 配图工作流

```
发起 AI 配图
    ↓
输入提示词 → 点「开始创作」
    ↓
轮询等待生成（最多 90 秒）
    ↓
[关键] 在点「使用」之前先 evaluate() 拿到 img src
    ↓
点「使用」进入裁剪
    ↓
裁剪确认
    ↓
将拿到的 URL 插入 ProseMirror 正文底部
    ↓
✅ 完成（图既作为封面，也在正文底部）
```

### 失败降级逻辑

```
AI 配图失败（超时/网络/审核）
    ↓
关闭 AI 配图弹窗
    ↓
重新打开封面菜单
    ↓
选择「从图片库选择」
    ↓
如有 --cover 参数 → 上传本地图
否则 → 选第一张
    ↓
下一步 → 裁剪 → 完成
```

## 💡 关键改进点

1. **URL 截获时机**（行 241-247）
   - 在点「使用」**之前**用 evaluate() 拿 URL
   - 避免弹窗消失后无法获取
   - 关键：`const imgs = last.querySelectorAll('.ai-image-item-wrp img')`

2. **多弹窗修复**（行 262-274）
   - 遍历所有 `.weui-desktop-dialog__ft`
   - 避免单一弹窗选择器冲突
   - 关键：`const fts = document.querySelectorAll('.weui-desktop-dialog__ft')`

3. **自动降级**（行 278-348）
   - 完整的 try-catch-finally 流程
   - 用户无感知降级
   - 确保发布不失败

## 🎁 额外收获

- 📚 完整的 Skill 编写范例
- 🔐 Cookie 管理最佳实践
- 🎨 DOM 选择器稳健性设计
- ⚡ Playwright 实战技巧

## 📝 使用注意事项

1. **首次登录必需** - `python3 publish.py --login`
2. **Cookie 自动过期** - 30 天左右需要重新登录
3. **AI 配图需网络** - 生成过程约 14 秒
4. **提示词定制化** - 可通过 `--ai-prompt` 指定任意主题
5. **降级无缝** - AI 失败自动改用图片库

## 🚀 后续可能的扩展

- [ ] 支持批量发布的配置文件
- [ ] 集成定时发布（cron）
- [ ] 支持 Markdown 自动转 HTML
- [ ] 集成公众号数据分析
- [ ] 支持多个公众号账号切换

---

**总结**：完整的微信公众号自动发布工具已打包完成，包含详细文档和可复用代码，支持在任何有 Python 环境的电脑上直接使用！ 🎉
