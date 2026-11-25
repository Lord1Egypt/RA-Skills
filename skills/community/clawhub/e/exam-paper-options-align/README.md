# 试卷选项对齐与排版优化

把 Word 试卷的选择题选项用制表位对齐成列（A 对 A、B 对 B、C 对 C、D 对 D），并统一全卷字号、字体、行距，让试卷可直接打印给学生考试使用。

## 为什么需要它

试卷排版最常见的两个问题：

1. **选项参差**：选项之间用空格分隔，打印出来东倒西歪，学生看串行。
2. **字号"看着"不一致**：`w:sz` 明明都是 12pt，但 `w:szCs` 缺失或混乱、theme 字体继承、表格字号不同，导致实际渲染大小不一。

本技能一次解决：制表位对齐 + 全卷版式统一，并做逐段内容校验，保证题目文字零改动。

## 安装

把整个目录放到你的技能目录下即可：

- WorkBuddy：`~/.workbuddy/skills/exam-paper-options-align/`
- 其他兼容 Skill 的工具：按各自的用户级技能目录放置

依赖 Python 库：

```bash
python3 -m pip install python-docx lxml
```

## 用法

```bash
PY=$(command -v python3 || command -v python)
SK="本技能目录/scripts/exam_format.py"

# 先诊断（只读，不改文件）
$PY "$SK" 试卷.docx --inspect

# 对齐选项 + 统一版式（自动备份后原地覆盖）
$PY "$SK" 试卷.docx

# 只对齐选项，不动其它版式
$PY "$SK" 试卷.docx --align-only

# 输出到新文件、四选项、正文 14pt
$PY "$SK" 试卷.docx -o 新卷.docx --letters ABCD --body-size 14
```

常用参数见 `SKILL.md` 的参数表。

## 验证记录

在真实小学英语试卷（译林版 4B Unit 8）上验证：

| 项目 | 结果 |
|---|---|
| 选项对齐 | 12 行全部对齐，列位自适应 [80, 185, 284] pt，每行恰好 3 个制表符 |
| 字号统一 | 正文 12pt（278 处）+ 标题 16pt/14pt，表格同步为 12pt |
| `sz≠szCs` | 修正 318 处，归零 |
| OOXML 顺序 | 重排 249 处 `rPr`/`pPr` |
| 内容校验 | 去空白逐段比对，字词差异为零 |

## 目录结构

```
exam-paper-options-align/
├── SKILL.md                        # 主文档：工作流 + 参数表 + 关键约束
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── scripts/exam_format.py          # 可执行脚本（对齐 + 版式统一 + 校验）
└── references/ooxml-pitfalls.md    # OOXML 坑位参考
```

## 注意事项

- 运行前**关闭 Word 中打开的目标文件**，否则改动可能被 Word 覆盖。
- 脚本默认自动备份为 `原名.bak-时间戳.docx`。
- 改完请在 Word 中**重新打开**文件查看效果。
- 题干与 4 个选项挤在同一行可能放不下，脚本会警告并给出建议字号，建议改为「题干一行、选项一行」。

## 隐私

发布版本已移除所有本地绝对路径、用户名与个人信息，可安全公开分发。
