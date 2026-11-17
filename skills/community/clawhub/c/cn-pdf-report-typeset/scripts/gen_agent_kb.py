# -*- coding: utf-8 -*-
"""AI Agent 核心知识体系学习笔记 → 专业中文PDF，大字手机可读"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether)

FONT_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("MSYH",   f"{FONT_DIR}/msyh.ttc",   subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYHBD", f"{FONT_DIR}/msyhbd.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYHL",  f"{FONT_DIR}/msyhl.ttc",  subfontIndex=0))

C_DARK  = colors.HexColor("#1a1a2e")
C_RED   = colors.HexColor("#c0392b")
C_BLUE  = colors.HexColor("#1f4e79")
C_LGRAY = colors.HexColor("#f2f3f5")
C_MGRAY = colors.HexColor("#d9dce1")
C_WHITE = colors.white

def st(name, **kw):
    base = dict(fontName="MSYH", fontSize=15, leading=24, textColor=C_DARK,
                alignment=TA_JUSTIFY, spaceAfter=8)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_TITLE = st("title", fontName="MSYHBD", fontSize=32, leading=42, alignment=TA_CENTER, textColor=C_DARK, spaceAfter=8)
S_SUB   = st("sub", fontName="MSYHBD", fontSize=19, leading=27, alignment=TA_CENTER, textColor=C_BLUE, spaceAfter=6)
S_META  = st("meta", fontName="MSYH", fontSize=13, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#666666"))
S_H1    = st("h1", fontName="MSYHBD", fontSize=21, leading=30, alignment=TA_LEFT, textColor=C_BLUE, spaceBefore=16, spaceAfter=10)
S_H2    = st("h2", fontName="MSYHBD", fontSize=17, leading=24, alignment=TA_LEFT, textColor=C_DARK, spaceBefore=12, spaceAfter=7)
S_BODY  = st("body", fontSize=15, leading=24)
S_BULLET= st("bullet", fontSize=15, leading=24, leftIndent=18, bulletIndent=6, spaceAfter=4)
S_BOX   = st("box", fontName="MSYHBD", fontSize=15, leading=24, alignment=TA_CENTER, textColor=C_WHITE)

def make_table(data, widths, header_bg=C_BLUE, fontsize=13, align_center_cols=None):
    def cell_style():
        return ParagraphStyle("cell", fontName="MSYH", fontSize=fontsize, leading=fontsize+4,
                              textColor=C_DARK, wordWrap="CJK")
    tdata = []
    for r_i, row in enumerate(data):
        trow = []
        for c_i, cell in enumerate(row):
            if r_i == 0:
                trow.append(Paragraph(str(cell), ParagraphStyle("h", fontName="MSYHBD", fontSize=fontsize,
                                   leading=fontsize+4, textColor=C_WHITE, wordWrap="CJK", alignment=(TA_CENTER if c_i>0 else TA_LEFT))))
            else:
                trow.append(Paragraph(str(cell), cell_style()))
        tdata.append(trow)
    t = Table(tdata, colWidths=widths, repeatRows=1)
    style = [
        ("FONTNAME", (0,0), (-1,-1), "MSYH"),
        ("FONTSIZE", (0,0), (-1,-1), fontsize),
        ("TEXTCOLOR", (0,0), (-1,-1), C_DARK),
        ("BACKGROUND", (0,0), (-1,0), header_bg),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("FONTNAME", (0,0), (-1,0), "MSYHBD"),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.5, C_MGRAY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LGRAY]),
    ]
    if align_center_cols:
        for c in align_center_cols:
            style.append(("ALIGN", (c,1), (c,-1), "CENTER"))
    t.setStyle(TableStyle(style))
    return t

OUT = "output.pdf"   # ← 改成你要输出的路径
DOC_TITLE = "AI Agent 核心知识体系"
DOC_SUB   = "感知 · 思考 · 行动 · 大脑 · 工具"
DOC_META  = "九品锦锂e 出品  |  2026-08-31"
DOC_SRC   = "学习沉淀  |  来源：AI Agent 教学课程资料系统性整合"
FOOTER    = "AI Agent 核心知识体系学习笔记  |  九品锦锂e 出品"

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=20*mm, bottomMargin=18*mm,
                      title=DOC_TITLE, author="九品锦锂e")

def on_page(canvas, doc_):
    canvas.saveState()
    canvas.setFont("MSYH", 8.5)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(22*mm, 10*mm, FOOTER)
    canvas.drawRightString(A4[0]-22*mm, 10*mm, f"第 {canvas.getPageNumber()} 页")
    canvas.restoreState()

frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

E = []
# ---- 封面 ----
E.append(Spacer(1, 20*mm))
E.append(Paragraph(DOC_TITLE, S_TITLE))
E.append(Paragraph(DOC_SUB, S_SUB))
E.append(Spacer(1, 8*mm))
E.append(Paragraph(DOC_META, S_META))
E.append(Paragraph(DOC_SRC, S_META))
E.append(Spacer(1, 18*mm))
E.append(HRFlowable(width="100%", thickness=1.2, color=C_BLUE))
E.append(Spacer(1, 6*mm))
E.append(Paragraph("⚡ 一句话认知", S_H2))
E.append(Paragraph("Agent = <span color='#c0392b'><b>感知（收输入+带历史上下文）→ 大脑（LLM理解/生成）→ 行动（工具/沙箱执行）</b></span>，循环为<span color='#c0392b'><b>想→做→看</b></span>。", S_BODY))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("LLM 是大脑，工具是手脚，沙箱是活动的圈", S_BOX))
E.append(PageBreak())

# ---- 一、Agent 是什么 ----
E.append(Paragraph("一、Agent 是什么（本质认知）", S_H1))
E.append(Paragraph("<b>一句话：Agent（代理）= 会自己动手做事的 AI，不只是回你话。</b>英文原义 <i>one who acts for</i> = 替你做事。是\"编码代理\"，能自己读代码、改文件、跑命令。", S_BODY))
E.append(Paragraph("核心工作循环：想 → 做 → 看（Think → Act → Observe）", S_H2))
E.append(make_table([
    ["动作", "含义"],
    ["想", "读相关文件、看报错、看状态，理解现状"],
    ["做", "改代码、建文件、跑命令"],
    ["看", "看输出/结果，不对就再来一轮"],
], [30*mm, 132*mm]))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("类比：普通聊天机器人 = 你拿教鞭一步步教；Agent = 自动驾驶汽车，你选方向它负责开。", S_BODY))
E.append(Paragraph("Agent vs 传统 Chatbot", S_H2))
E.append(make_table([
    ["类型", "行为"],
    ["传统 Chatbot", "给你一段文字，不操作任何东西"],
    ["Agent", "自己跑命令、读文件、改代码，然后告诉你结果"],
], [50*mm, 112*mm]))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("Agent 能干活的两个必备能力：<b>规划能力</b>（拆解复杂任务） + <b>执行能力</b>（调工具、执行任务）。", S_BODY))

# ---- 二、感知思考行动 ----
E.append(Paragraph("二、核心能力：感知、思考、行动", S_H1))
E.append(Paragraph("感知（Perception）—— Agent 如何接收理解输入", S_H2))
E.append(Paragraph("感知是 Agent 与外部世界交互的第一步，通过\"接口\"接收输入。", S_BODY))
E.append(make_table([
    ["人类感知", "Agent感知", "示例"],
    ["眼睛", "文本输入", "用户对话框输入"],
    ["耳朵", "语音输入", "语音指令"],
    ["皮肤", "传感器数据", "温度/压力/光照"],
    ["鼻子", "嗅觉输入", "气体浓度"],
    ["舌头", "多模态输入", "图片/视频/文件"],
], [36*mm, 46*mm, 80*mm], align_center_cols=None))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("<b>关键点：感知不仅接收当前输入，还感知对话历史（上下文）。</b>例：用户第一句\"帮我查上季度销售数据\"，第二句\"只看华东区\"——若无历史感知，\"华东区\"毫无意义。", S_BODY))
E.append(Paragraph("多模态感知：语音（转文字）、图片（识别表格）、文件（读Excel分析）、系统状态（数据库/网络可用性）。", S_BODY))
E.append(Paragraph("> <b>对感知的判断力决定决策能力。</b>", S_BOX))

# ---- 三、LLM 大脑 ----
E.append(Paragraph("三、Agent 的大脑：LLM（大语言模型）", S_H1))
E.append(Paragraph("LLM 是什么：本质是特殊训练的计算机程序，可想象成\"超级学霸\"——通过互联网上亿本书籍/文章/代码/论坛学习，掌握语言规律、语法、逻辑、知识。它<b>不总是\"搜索\"答案，而是\"生成\"答案</b>。", S_BODY))
E.append(Paragraph("LLM vs 搜索引擎（易混淆，重要）", S_H2))
E.append(make_table([
    ["特性", "搜索引擎（Google）", "LLM（ChatGPT）"],
    ["工作方式", "检索已有网页返回链接", "理解/生成语言"],
    ["交互方式", "关键词匹配", "自然语言对话"],
    ["幻觉", "无", "可以有"],
    ["处理能力", "无法", "可以"],
    ["相关性", "基于关键词匹配", "基于语义理解"],
    ["创造性", "无（只返回已有信息）", "有（能生成新内容）"],
], [33*mm, 62*mm, 67*mm]))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("LLM 两大核心能力", S_H2))
E.append(Paragraph("1. <b>理解能力</b>：理解真实含义，把自然语言翻译成机器可执行指令。例：\"上个月北京房价怎么样\" → 上个月=时间/北京=地点/房价=需求/怎么样=价格走势。", S_BULLET))
E.append(Paragraph("2. <b>生成能力</b>：按指示生成文本/代码/指令/结构化数据。例：\"查询2024年北京地区客户销售数据\" → SELECT month, SUM(amount) FROM sales WHERE city='北京' AND year=2024 GROUP BY month。", S_BULLET))
E.append(Paragraph("> <b>LLM 是大脑负责理解和生成；工具是手脚负责执行。</b>", S_BOX))

# ---- 四、DataAgent ----
E.append(Paragraph("四、真实企业级案例：DataAgent（网易）", S_H1))
E.append(Paragraph("企业级数据分析 Agent，能听懂数据问题、自动写 SQL、画图表、出报告。处理\"近三个月各产品线销售数据如何？\"的 16 步流程：", S_BODY))
E.append(make_table([
    ["步骤", "标签", "说明"],
    ["1", "用户提问", "用户发起问题"],
    ["2", "意图识别", "判断是数据分析，不是闲聊"],
    ["3", "证据推理", "了解\"数据\"对应哪些表和字段"],
    ["4", "意图推理", "把\"近三个月\"转成具体日期范围"],
    ["5", "Schema识别", "找到 sales、product、sales_detail 表"],
    ["6", "SQL生成", "分析表关联"],
    ["7", "可行性评估", "判断能否用现有数据回答"],
    ["8", "规划", "拆分步骤：查数据→图表→报告"],
    ["9", "人员反馈", "询问用户确认信息"],
    ["10", "计划执行", "逐步执行规划步骤"],
    ["11", "查询", "生成SQL查数据库"],
    ["12", "图表生成", "根据结果生成图表"],
    ["13", "代码执行", "生成图表数据并执行"],
    ["14", "PyEcharts生成", "用 PyEcharts 库生成图表"],
    ["15", "报告生成", "整合分析生成报告"],
    ["16", "结果返回", "图表+结论+报告返回用户"],
], [14*mm, 40*mm, 108*mm], fontsize=12))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("<b>入口逻辑：意图识别模式</b>——第2步是第一道闸门，判断输入是\"数据分析请求\"还是\"闲聊\"。数据分析→进入后续引擎；闲聊→直接回答（避免资源浪费）。", S_BODY))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("DataAgent 感知代码示例（Java）", S_H2))
E.append(Paragraph("<font color='#444444'>public String getUserInput(String userInput) {<br/>    String rawInput = userInput;  // 感知：当前输入<br/>    String multiTurn = getHistory(\"user\", MULTI_TURN_CONTEXT, \"[]\");  // 感知：历史上下文<br/>    String prompt = PromptBuilder.build(perceptionPrompt(multiTurn, userInput));<br/>}</font>", S_BODY))

# ---- 五、Hermes 画像 ----
E.append(Paragraph("五、Hermes Agent 能力画像（官方入门）", S_H1))
E.append(Paragraph("Hermes 具备丰富功能，远超基本聊天——持久记忆、文件感知、上下文浏览、深度自动化、语音对话，共同作用成为强大的自主助手。Nous Research 开源端侧智能体。", S_BODY))
E.append(Paragraph("核心能力", S_H2))
E.append(make_table([
    ["能力", "说明"],
    ["工具与工具集", "扩展能力的功能，按逻辑工具集组织（网络搜索/编程/文件操作），如 curl、fetch、浏览器扩展"],
    ["技能集成", "技能是知识/脚本模块，需要时加载，共享函数提效减少命令输入，与 agentSkills 库标准化"],
    ["持久记忆", "会话间持久存在，记住偏好/项目/环境/会话通知（MEMORY.md 等）"],
    ["文件上传", "文件可上传作为项目注释文档（README.md、CLAUDE.md、SOUL.md、curriculum.md）"],
], [40*mm, 122*mm], fontsize=13))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("自动化能力", S_H2))
E.append(make_table([
    ["能力", "说明"],
    ["计划任务（Cron）", "自然语言或 cron 表达式安排任务自动运行，作业可附技能、发送到平台、暂停/恢复/编辑"],
    ["子代理系统", "委派任务给子代理、收集结果（可与 LangChain 等协作）"],
    ["代码执行", "执行 Python 脚本，通过沙盒化 RPC 编程调用 Hermes 工具（execute_code）"],
    ["事件钩子", "关键生命周期（如消息发布）自动触发，执行自动化/提醒/Webhook"],
], [40*mm, 122*mm], fontsize=13))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("媒体/网页集成", S_H2))
E.append(make_table([
    ["能力", "说明"],
    ["语音模式", "CLI 和消息平台全语音交互，实时对话"],
    ["浏览器自动化", "多浏览器自动化（Browserbase云/CDP本地Chrome/Firefox）、截图、表单、抓数据、密码填充"],
    ["视图集成", "一般扩展模块（表单/截图/绘制）"],
], [40*mm, 122*mm], fontsize=13))

# ---- 六、上下文文件 ----
E.append(Paragraph("六、Hermes 上下文文件（官方入门第三章）", S_H1))
E.append(Paragraph("Hermes Agent 自动发现并加载决定行为的上下文文件。分两类：<b>项目本地</b>（从工作目录发现）+ <b>全局</b>（从 $HERMES_HOME 加载）。", S_BODY))
E.append(Paragraph("支持的上下文文件完整表", S_H2))
E.append(make_table([
    ["文件", "目的", "发现", "优先级"],
    [".hermes.md / HERMES.md", "项目说明（最高优先级）", "走到 git 根目录", "1"],
    ["AGENTS.md", "项目说明、约定、框架", "启动时当前工作目录 + 逐层展开子目录", "2"],
    ["CLAUDE.md", "Claude 代码上下文文件", "启动时当前工作目录 + 逐层展开子目录", "3"],
    ["SOUL.md", "描述 Hermes 实例的全局个性/语言定制", "仅从 $HERMES_HOME/SOUL.md", "4"],
    [".cursorrules", "Cursor IDE 编码规范", "仅 CWD", "5"],
    [".cursor/rules/*.md", "Cursor IDE 规则模块", "仅 CWD", "6"],
], [40*mm, 52*mm, 52*mm, 18*mm], fontsize=12.5))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("<b>优先级规则（关键）</b>：每个会话仅加载一种项目上下文类型（首次匹配优先）：<font color='#c0392b'><b>.hermes.md &gt; AGENTS.md &gt; CLAUDE.md &gt; .cursorrules</b></font>。SOUL.md 始终作为代理独立加载（叠加在最上），与项目文件不冲突。", S_BODY))
E.append(Paragraph("渐进式子目录发现机制：会话开始加载工作目录文件；会话中导航到子目录（cd 等）时，合并发现该子目录上下文文件，相关时注入对话。", S_BODY))
E.append(Paragraph("> 渐进式加载两大优点：<b>无系统提示冗余</b>（子目录提示仅需要时出现）+ <b>提示缓存保留</b>（系统提示会话期间保持稳定）。要点：每子目录每会话最多访问一次；所有上下文文件都经安全扫描，恶意文件被拦截（防提示注入）。", S_BODY))

# ---- 七、Codex 画像 ----
E.append(Paragraph("七、Codex 能力画像（OpenAI 编程代理）", S_H1))
E.append(Paragraph("Codex 是 OpenAI 官方推出的 AI 编程代理。你给目标，它读整个项目、写代码、执行命令行、跑测试，把活几乎全包交付——不是像 ChatGPT 那样一问一答聊天。", S_BODY))
E.append(Paragraph("Codex 的四种入口", S_H2))
E.append(make_table([
    ["入口", "说明", "平台"],
    ["桌面 App", "最轻量，原生上手体验", "macOS/Windows"],
    ["CLI 命令行", "终端集成，高效执行/脚本化", "跨平台"],
    ["IDE 扩展", "编辑器内即席操作，边写边用", "VS Code/IntelliJ"],
    ["Cloud Web", "云端网页版，零代码门槛", "chatgpt.com/codex"],
], [40*mm, 80*mm, 42*mm]))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("> 同一账号到底层互通——选哪个入口看当前场景。", S_BODY))
E.append(Paragraph("Codex vs ChatGPT", S_H2))
E.append(make_table([
    ["维度", "ChatGPT", "Codex"],
    ["角色定位", "通用对话助手", "专门写代码的 AI 编程代理"],
    ["交互", "一问一答，你按它教的做", "你给目标，它改项目/跑命令/测代码全包"],
    ["结果", "给你\"菜谱\"你来做", "直接给你\"做好的菜\""],
], [30*mm, 62*mm, 70*mm]))
E.append(Spacer(1, 4*mm))
E.append(Paragraph("Codex 核心能力", S_H2))
E.append(Paragraph("1. <b>代码编写</b>：按需求结合项目已有结构/风格生成，非瞎编孤岛式代码。", S_BULLET))
E.append(Paragraph("2. <b>代码库/依赖分析</b>：接手陌生项目\"体检\"，快速了解结构依赖。", S_BULLET))
E.append(Paragraph("3. <b>查漏补缺</b>：找潜在 bug、漏洞、边界条件、遗留坑。", S_BULLET))
E.append(Paragraph("4. <b>调试修复</b>：丢报错信息，定位问题、修复并生成补丁。", S_BULLET))
E.append(Paragraph("5. <b>自动化测试</b>：跑通测试、补测试、回归测试，一句话委托。", S_BULLET))

# ---- 八、内化结论 ----
E.append(Paragraph("八、核心结论（六个认知）", S_H1))
E.append(Paragraph("1. <b>Agent 统一公式</b>：感知（收输入+带历史上下文）→ 大脑（LLM理解/生成）→ 行动（工具/沙箱执行），循环想→做→看。判断一个 AI 是不是真 Agent 就套这个——能自己调工具动手才算，只回话的不算。", S_BODY))
E.append(Paragraph("2. <b>感知的核心不是\"收\"，是\"带上下文接\"</b>：只接当前输入=玩具，接住历史才值钱。这解释了多轮对话和上下文管理的价值。", S_BODY))
E.append(Paragraph("3. <b>LLM 是大脑，工具是手脚</b>：LLM 负责想和生成，工具负责执行，缺一不可。这正是 Hermes 工具集/技能设计的内在逻辑。", S_BODY))
E.append(Paragraph("4. <b>上下文文件优先级</b>（天天在用）：.hermes.md &gt; AGENTS.md &gt; CLAUDE.md &gt; .cursorrules，SOUL.md 全局独立叠加。这解释了为啥 SOUL.md 定人设、项目文件定项目约定，不冲突。", S_BODY))
E.append(Paragraph("5. <b>沙箱是 Agent 的\"圈\"</b>：只读 → 工作区可写（日常最常用）→ 全权限（能联网改任何文件，风险高需人盯）。做 AI 产品权限边界就按这三档设，从最小权限开始。", S_BODY))
E.append(Paragraph("6. <b>Codex 四种入口对做产品有直接启发</b>：桌面/CLI/IDE/云Web 四入口、账号底层互通——这正是 Hermes 多平台网关（飞书/微信/WhatsApp）和产品形态设计的参照。", S_BODY))

E.append(Spacer(1, 10*mm))
E.append(HRFlowable(width="100%", thickness=0.8, color=C_MGRAY))
E.append(Paragraph("— 九品锦锂e 出品 —", st("sign", fontSize=9.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#999999"))))

doc.build(E)
print("PDF OK:", OUT)
print("size:", os.path.getsize(OUT), "bytes")
