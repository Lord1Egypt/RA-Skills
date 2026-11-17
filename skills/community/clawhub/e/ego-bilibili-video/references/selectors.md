# Selectors(2026-11 实测,基于 ego-browser 0.6.x)

投稿页 `https://member.bilibili.com/platform/upload/video/frame`(micro-app `video-up`,表单在 shadow DOM)。

| 目标 | 定位 | 备注 |
|------|------|------|
| 上传区 | `.upload-area` 中心坐标 | 轻量 DOM,不在 shadow 里;`.upload-btn` 是 `no-events` 不可点 |
| 上传完成信号 | shadow 文本 `上传完成` / `更换视频` | `上传失败`/`解析失败` 为失败 |
| 标题 | shadow `INPUT[placeholder*="稿件标题"]` | 上限 80;优先 CDP `Input.insertText`,失败再 execCommand,回读必须一致。原生 setter 不进模型 |
| 标签输入 | shadow `INPUT[placeholder*="创建标签"]` | Enter 创建;chip `.label-item-v2-content` |
| 预填标签 chip | `.label-item-v2-container` | 逐个点内部最后可见子元素移除 |
| 简介 | shadow `.ql-editor` 且可见、高度 >60 | Quill;隐藏的另一个是动态编辑器 |
| 添加封面 | shadow 文本 `添加封面`(span `.add-text`) | 打开 `.bcc-dialog`(1220px 宽) |
| 弹窗头 | `.cover-editor-head` | 可见性判定弹窗开关 |
| 双比例同步 | `.sync-checkbox-wrapper input[type=checkbox]` | 默认勾选。点可见方框并读 `checked`，连续两次为关才上传 |
| 4:3 视图按钮 | shadow 文本 `首页推荐`,`class^="button"` | active 判定 `button active` |
| 16:9 视图按钮 | shadow 文本 `个人空间` | 同上 |
| 上传封面 | shadow 文本 `上传封面`(span `.upload-text`) | 传到当前激活视图的槽 |
| 4:3 槽位缩略图 | `.cover-phone-view-home-video-img img` | 用 naturalWidth/Height 验比例 |
| 16:9 槽位缩略图 | `.cover-phone-view-space-video-img img` | 同上 |
| 弹窗完成 | shadow 文本 `完成` + `class*="submit"` | 取消是纯 `.button` |
| 16:9 未修改确认框 | `.videoup-confirm-modal`,按钮 `不同步，手动编辑` / `确认同步` | 选不同步;选完需再点一次「完成」 |
| 表单封面落位 | `.cover-img` 的 `background-image` | 出现 `url(...)` 即已应用 |
| 分区 | `.video-human-type` 内 `.select-item-cont-inserted` | 点 `.select-controller` 打开 `.human-type-list`;选项是 `.drop-list-v2-item[title]` |
| 创作声明 | `.bcc-select` 里 `INPUT[placeholder*="创作声明"]` | 当前值看 `input.value`。要改时点控件右侧箭头;未展开的 `.bcc-option` 高度为 0 |
| 成功视图 | 文本 `稿件投递成功`,按钮 `查看进度` / `再投一个` | URL 不变,SPA 原地切换;正则要含「投递成功」 |
| 立即投稿 | shadow 文本 `立即投稿` + `class*="submit-add"` | `存草稿` 是 `.submit-draft` |
| 成功信号 | 文本 `投递成功|投稿成功|提交成功|审核中` | 稿件号从页面或稿件管理标题链接读取;没有则 identity=unconfirmed |

文件选择 input 参考(均为 shadow 内 `INPUT[type=file]`):

- 视频:`accept` 含 `.mp4` 且**可见**的那个(还有一个 hidden 兄弟,`setInputFiles` 需区分;技能用 chooser 路径,不走 input)
- 封面:`accept="image/png, image/jpeg"`
