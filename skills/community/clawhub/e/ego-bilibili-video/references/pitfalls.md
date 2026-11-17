# 避坑 / Pitfalls

## 会打断自动化的弹窗

- **通知权限弹窗**:打开创作中心可能触发浏览器通知权限提示,ego 会把 space 交给用户并停掉脚本。`post-video.mjs` 在 goto 之前用 `page.cdp("Browser.grantPermissions", { permissions: ["notifications"] })` 预授;该调用不支持 `camera` 等类型,传了会整批报错,只传确认存在的类型。
- 文件选择是原生对话框,必须**先** `waitForFileChooser` **再**触发点击,顺序反了会超时。

## micro-app + shadow DOM

- 创作中心表单在 `<micro-app name="video-up">` 的 shadow 树里:`document.body.innerText` 看不到表单,所有探测都要 shadow-walk(`page.click(css=…)` 同样看不到)。
- 交互方式统一为:walk 定位元素 → `getBoundingClientRect` 中心点 → `page.mouse.click(x, y)`。
- `blob:` URL 会在重渲染时刷新,**不能**当稳定标识;判断槽位用 `.cover-phone-view-home-video-img` / `.cover-phone-view-space-video-img` 包裹层的 `img.naturalWidth/Height`。

## 上传路径

- 不要直接对 `<input type="file">` `setInputFiles`:bilibili 的 micro-app 不响应程序注入的 change,上传不会开始。
- 正确路径:坐标点 `.upload-area`(内部 `.upload-btn` 是 `no-events`,点它会被拦截报错;点区域中心,事件冒泡到挂 handler 的祖先)。
- 上传完成信号是 shadow 文本「上传完成 / 更换视频」;出现「上传失败 / 解析失败」直接失败。

## 表单回读

- **标题不能用原生 setter 写 value**:只改显示、不更新 Vue 模型,投稿会以文件名当标题发出去(实测 2026-11-06 发生过)。execCommand 也可能因 v-model.lazy 不进模型——**首选 CDP `Input.insertText` 真实输入**,再补 `change` 事件 + `blur()`,回读校验。
- 标签要逐个「写值 + 派发 Enter 键事件」并核对 chip(`.label-item-v2-content`)文本;回车没生效会留下一半标签,宁可失败也不要静默。
- 简介是 Quill 编辑器(`.ql-editor`,页面上可见的那个;另一个隐藏的是动态编辑器):focus + selectAll + insertText,回读 `innerText`(Quill 把单换行渲染成 `\n\n`,比较前归一化)。
- 表单会预填上一次投稿的标签(如 爱情/生活/校园),技能先逐个移除;移除失败会保留并记录在 stderr,不会静默当成功。

## 封面

- 「双比例同步改动」默认勾选。控件是 `.sync-checkbox-wrapper` 里可见的 `input[type=checkbox]`，类名不是 `bcc-checkbox`。点文字中心不会稳定改掉 `input.checked`。要读到连续两次未勾选，才选文件。仍勾着就停。
- 右侧「首页推荐 / 个人空间」只改手机预览，不决定上传落点。上传前要点中 `editor_4_3` 或 `editor_16_9`，并确认父级是 `active`。传完 16:9 后手机预览停在「个人空间」，首页那张 `cover-phone-view-home-video-img` 是隐藏的，隐藏时的 500×375 不能当 4:3 结论。先点「首页推荐」，只读当前稿件那一张可见封面。编辑画布和这张可见手机图都要对上原图。16:9 文件进了 4:3 画布，或同步把 4:3 换成 16:9，都要停。收起后的单张 `.cover-img` 不能代替两个槽。
- 4:3 槽 = 弹窗里「首页推荐」视图 + `上传封面`;16:9 槽 = 「个人空间」视图 + `上传封面`。每次上传后以槽位缩略图 natural 比例为准(±8%)。
- 「完成」(`.button.submit`)后回到表单,`.cover-img` 必须出现 `url(...)` 背景;没有就是封面没落位。
- 点「完成」可能弹出二层确认「检测到个人空间封面(16:9)未修改」(`.videoup-confirm-modal`):**必须点「不同步,手动编辑」**,绝不能点「确认同步」(会用 4:3 的居中裁切覆盖我们分开上传的 16:9)。选完后编辑器切到 16:9 手动编辑视图,再点一次「完成」才关闭。当两张封面裁自同一原图时(中心裁切像素相同)该弹窗必现,真实的不同设计稿也可能触发。
- AI 推荐封面(`.img-item-box.img-item-cover`)是干扰项,不要误点。

## 分区与投稿

- **创作声明是必填**。表单经常已经显示「内容无需标注」,这是 bcc-select 的当前值,直接回读可见输入框即可。点输入框正中不会展开列表,未展开的 `.bcc-option` 高度是 0。需要改值时点右侧箭头。选项行在 `scrollIntoView` 之后还会往下走,行还在动时点击会落空,列表勾选仍停在「内容无需标注」。等 `.bcc-option` 的纵坐标连续两次不变,再点这一行的中部。点完输入框和列表勾选必须都是指定项。不要在行还没停时再点第二次。先把分区选定并收起,再改声明。停投前再读一次可见值。
- `--stop-before-submit` 在唯一的「立即投稿」点击之前返回。它和 `--yes` 同时出现时仍然不点。缺了这两个参数时不会打开浏览器。
- **成功文案是「稿件投递成功」**,不是「投稿成功」——成功判定正则必须包含「投递成功」,否则会把实际成功的投稿当成失败(实测 2026-11-06 发生过)。URL 不变,SPA 原地切换成功视图,出现「查看进度 / 再投一个」按钮。
- 分区 chip 是 `.video-human-type` 里的 `select-item-cont-inserted`,input `.value` 是空的;判空和回读都看 chip 文本。`--type` 要点开 `.human-type-list` 再点同名项,点不中就停,不能把旧 chip 当成指定分区。
- 「立即投稿」是 `.submit-add`;「存草稿」是 `.submit-draft`,不要点错。
- 成功信号:页面出现「投稿成功/审核中」。90 秒没确认就截图(`/tmp/bilibili-video-publish-fail.png`)退出 1;此时稿件可能已在审核队列,**不要**盲目重跑,先去「内容管理 → 稿件管理」查重。

## 其它

- 网页投稿没有「仅自己可见」;给用户发测试视频前必须说清楚过审即公开。
- B 站风控会针对高频投稿触发验证码(`geetest`/`risk-captcha`):脚本遇到即失败退出,把截图给用户人工处理,**不要**尝试自动绕过。
- 表单布局会随展开「更多设置」等操作 reflow,任何缓存坐标都要在点击前现取。
