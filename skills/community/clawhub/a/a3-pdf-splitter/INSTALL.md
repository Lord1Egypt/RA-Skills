# 安装说明

## 1. 安装Skill
将整个`a3-pdf-splitter`文件夹复制到你的LobsterAI Skill目录：
```
C:/Users/admin/AppData/Roaming/LobsterAI/SKILLs/
```

## 2. 安装依赖
```bash
pip install pypdfium2 pillow
```

## 3. 验证安装
重启LobsterAI后，你可以通过以下方式触发这个Skill：
- "帮我切分这个A3试卷PDF"
- "把A3 PDF转成A4格式方便打印"
- "拆分这个试卷PDF"
- "A3转A4工具"

## 4. 使用示例
当你说："帮我把C:\Downloads\试卷.pdf切分成A4格式"
系统会自动调用这个工具，处理完成后告诉你输出文件位置。

## 5. 手动使用
你也可以直接在命令行使用：
```bash
python C:/Users/admin/AppData/Roaming/LobsterAI/SKILLs/a3-pdf-splitter/scripts/split_a3_smart.py "输入文件.pdf" "输出文件.pdf"
```