# docx-writer Log

| 时间 | 类型 | 描述 | 路径 |
|------|------|------|------|
| 2026-07 | 踩坑 | 封面页垂直居中不能依赖 `sectPr.vAlign=center`（python-docx 不认），必须用单格表格 + 行高固定 + 单元格垂直居中 | `build_handbook.py` |
| 2026-07 | 踩坑 | 封面表格行高用 `trHeight` 设 `hRule=exact`，值≈14000 twips（A4可用高度约24cm） | `build_handbook.py` |
| 2026-07 | 踩坑 | 分节后添加页脚页码：`sectPr` 必须用 `copy.deepcopy(原sectPr)` 而非 `etree.Element()`，否则 python-docx 找不到 `page_width` | `build_handbook.py` |
| 2026-07 | 踩坑 | `footerReference` 的 `r:id` 属性命名空间是 `{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id`，不是 `w:id` | `build_handbook.py` |
| 2026-07 | 踩坑 | 目录页的点线页码：用 `tab_stops.add_tab_stop(Cm(15.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)` 设置右对齐制表位+点线前导符 | `build_handbook.py` |
| 2026-07 | 踩坑 | 页码前两页不显示：分三节，第一节（封面）和第二节（目录）不加 `footerReference`，第三节（正文）加 | `build_handbook.py` |
| 2026-07 | 踩坑 | `B()` 函数不支持 `sz` 参数，需要小字时直接用 `P(text, sz=Pt(9))` | `build_handbook.py` |
| 2026-07 | 踩坑 | 全角括号 `（`（U+FF08）在 Python 源代码中会被误认为函数调用，导致 `SyntaxError`，必须用半角 `(` | `build_handbook.py` |
| 2026-07 | 踩坑 | 调研报告内容不能缩减，用户要求完整还原所有子主题和问题的原始内容 | `build_handbook.py` |
| 2026-07 | 经验 | 用 `page_break()` 实现分页，用 `sectPr` + `type=nextPage` 实现分节 | `build_handbook.py` |
| 2026-07 | 经验 | `H3` 需要单独定义（`build_docx.py` 中已有，但自定义脚本中容易遗漏） | `build_handbook.py` |
| 2026-07 | 经验 | 图片插入用 `run.add_picture(FLAG, width=Cm(10))`，段落对齐用 `p.alignment = 1` | `build_handbook.py` |
| 2026-07 | 经验 | LibreOffice 转 PDF：`soffice.exe --headless --convert-to pdf --outdir DIR FILE.docx` | CLI |
| 2026-07 | 经验 | PDF 转图片用 `pdf2image.convert_from_path(pdf, dpi=150)`，再用 Read 工具看图片做视觉核验 | `build_handbook.py` |
| 2026-07 | 踩坑 | 行程表中 `7.25 浙江大学、讲座、第二次研讨会` 等细节需严格与 PPT 第二次行前会议一致 | `build_handbook.py` |
| 2026-07 | 踩坑 | 酒店地址需用具体名称，不能写"上海酒店"、"杭州酒店" | `hotel.txt` |
| 2026-07 | 踩坑 | 队旗图片应放在标识解读文字的上方，而非下方或封面 | `build_handbook.py` |
| 2026-07 | 踩坑 | 单位标题需另起一页且居中（H1 样式），与调研报告保持统一 | `build_handbook.py` |
| 2026-07-20 | tmp_script | 生成实践支队通勤安排正文与图片附录 | `tmp/scripts/build_commute_docx.py` |
| 2026-07-20 | tmp_script | 校验附录图片居中与同行分页符 | `tmp/scripts/validate_commute_docx.py` |
| 2026-07-20 | task | 生成实践支队通勤安排 | `output/实践支队通勤安排.docx` |
| 2026-08-03 | tmp_script | 公众号A相对B的修改标注版docx排版（红下划线=新增/改写，灰删除线=删除，无图片） | `tmp/scripts/build_wx_diff.py` |
| 2026-08-03 | task | 以B《"穹游沪杭"\|总结回顾》为底稿生成A《解锁AI世界地图》修改标注版 | `output/穹游沪杭_B为基础_A修改标注.docx` |
| 2026-08-03 | tmp_script | 公众号B全文整理排版（docx-writer，**加粗**语法保留原文强调，无图片） | `tmp/scripts/build_wx_B.py` |
| 2026-08-03 | task | 公众号B《"穹游沪杭"\|总结回顾》整理为docx | `output/穹游沪杭_总结回顾.docx` |
| 2026-08-03 | tmp_script | 公众号A全文整理排版（docx-writer，**加粗**语法保留原文强调，无图片） | `tmp/scripts/build_wx_A.py` |
| 2026-08-03 | task | 公众号A《解锁AI世界地图》整理为docx | `output/穹游沪杭_解锁AI世界地图.docx` |
| 2026-08-03 | tmp_script | 基于A/B改写第三人称新闻稿（2000-2500字），docx-writer排版 | `tmp/scripts/build_news.py` |
| 2026-08-03 | task | 新闻稿《在产业一线寻找AI的"生态密码"》 | `output/新闻稿_清华无穹书院穹游沪杭实践侧记.docx` |
| 2026-08-03 | skill更新 | SKILL.md 引号规范改为强制：中文引号必须拆独立run且 `eastAsia/ascii/hAnsi` 设所在段中文字体，禁止TNR；嵌套单引号一并处理；字符串级替换不算完成 | `SKILL.md` |
| 2026-08-03 | skill更新 | `build_docx.py` `fix_quotes()` 升级：支持双引号+嵌套单引号，引号字体跟随所在段中文字体（默认宋体），纯ASCII保留直引号 | `scripts/build_docx.py` |
| 2026-08-03 | 测试 | 验证更新后引号：中文引号宋体/标题黑体，嵌套单引号宋体，纯ASCII"AI"直引号TNR（符合规范） | `tmp/scripts/test_skill_quotes.py` |
| 2026-08-03 | 改稿 | 新闻稿去推送稿化：去掉团队自我引语/调研笔记表述、概念加引号、日期括号行；引号从35组降至5组（仅专名+官方讲话+标题比喻） | `tmp/scripts/build_news.py` |
| 2026-09-13 | 重构 | 引擎化改造：新增配置驱动引擎 `docx_engine.py`（Template+Builder，排版全部来自 YAML），新增 `templates/{academic,push,news}.yaml` 三套模板 + 声明式渲染器 `build_from_content.py`；`build_docx.py` 改为引擎薄封装（保留 B/H1/H2/add_img/add_tbl）；README/SKILL 同步 | `scripts/docx_engine.py`, `templates/*.yaml`, `scripts/build_from_content.py`, `scripts/build_docx.py` |
| 2026-09-13 | 测试 | 用 push 模板（15pt/1.8/灰图注/中文引号/三线表/灰右落款）与 academic 模板（脚注上标+页脚注释）各渲一份，LibreOffice 转 PDF 目视核验通过 | `tmp/test_push.docx`, `tmp/test_academic.docx` |
| 2026-10-01 | 功能 | 新增 **LaTeX 公式支持**（XeLaTeX 真排版，遵循 AGENTS.md「数学公式渲染（转图片）」）：① `scripts/latex_formula.py`（preview/tightpage 紧裁 → PyMuPDF 转 PNG，CLI + 可 import `render_formulas`，xelatex 定位 `--xelatex`>`OPENCODE_XELATEX`>PATH，哈希缓存）；② 引擎新增 `Builder.formula()`（行间）与 `{Xn}` 行内公式占位（`para(..., lx_map=)`）；③ `build_docx.py` 新增 `Fx/Lx`；④ `build_from_content.py` 支持 `formula` 块与 `para.lx`；⑤ 模板新增 `formula` 样式；⑥ SKILL/README 同步（含脚本登记表） | `scripts/latex_formula.py`, `scripts/docx_engine.py`, `scripts/build_docx.py`, `scripts/build_from_content.py`, `templates/*.yaml` |
| 2026-10-01 | 测试 | 渲染含行内公式（α0=arctan(px/py)）与行间公式（bmatrix 矩阵、arccos 分式、定积分）的测试文档，LibreOffice 转 PDF 目视核验通过；回归：原报告脚本重建正常；`xelatex`=MiKTeX 25.12 | 项目文件夹 `tmp/formula_test/` |
| 2026-10-01 | 优化 | 行内公式排版：`_formula_png` 增加 `border` 透传；`_inline_formula` 支持模板 `inline_border`（默认 1pt，收紧裁剪留白）与 `inline_scale`（相对缩放），行内公式行距更均匀 | `scripts/docx_engine.py`, `templates/{academic,script}.yaml` |
| 2026-10-01 | 功能 | 公式新增 **Word 原生可编辑公式（OMML）**：`latex_to_omml()`（pandoc `-f markdown -t docx` → 抽取 `m:oMath`/`m:oMathPara`，并给含空格的 `m:t` 补 `xml:space="preserve"`）；引擎 `formula`/`_inline_formula` 支持 `mode=image\|omml\|auto`（模板 `formula.mode`，默认 auto）；CLI 增 `--omml`/`--pandoc`；SKILL/README 更新 | `scripts/latex_formula.py`, `scripts/docx_engine.py`, `templates/*.yaml` |
| 2026-10-01 | 测试 | 用报告实测：`mode:auto` + pandoc → document.xml 含 `m:oMath`（原生公式，Word 可编辑），`xmlns:m` 在根声明；LibreOffice 转 PDF 目视核验公式与单位空格正常 | 项目文件夹 `MathLab/Robotics/L3_HW_P` |
| 2026-10-01 | 踩坑 | **Word 把公式（OMML）计入「字数」**：正文 340 字、Word 状态栏却 543（行间矩阵/分式占 ~107 个公式元素）；改用"删行间公式 + 单位集中说明"后估算 543→~420。→ 字数受限稿子应优先 `mode: image`（图片不计字数）| SKILL.md「已知问题」 |
| 2026-10-01 | 踩坑 | 段落设 `keep_with_next`/`keep_together` 会在 Word「显示格式标记」时于左边缘出现**黑色小方块**（非打印）；交付稿如在意观感则不设该属性 | SKILL.md「已知问题」 |
| 2026-10-01 | 踩坑 | pandoc 的 OMML 未带 `xml:space="preserve"` 会吞掉公式内空格（`1.2m`）；已在 `latex_to_omml()` 自动补齐 | `scripts/latex_formula.py` |
