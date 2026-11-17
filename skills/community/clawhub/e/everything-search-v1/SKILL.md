---
name: everything-search-v1
description: "Windows10/11 & WSL2 本地文件极速检索系统，基于 Everything es.exe CLI 工具。触发条件：当用户或智能体有查找/搜索/定位文件的意图时（非全文内容搜索或网页搜索）。"
description_en: "Windows 10/11 & WSL2 Local File Search System based on Everything es.exe CLI tool. Triggered when user or agent has the intent to find/search/locate files (not full-text content search or web search)."
emoji: 🔎
author: OneToken
version: 1.0.0
update_website: https://github.com/1TOKENer/everything-search-skill
requires:
  os: [windows_10, windows_11,wsl2]
  arch: [win32, win64, win_arm32, win_arm64]
  bins: [python3]
---

# Everything Search v1

🔎 **Windows10/11 & WSL2 本地文件极速检索系统** — 基于 [Everything](https://www.voidtools.com/) es.exe 命令行工具。

## 触发条件

当用户（user）或智能体(Agent)有以下意图时触发此 skill：

- ✅ **适用于**：查找/搜索/定位**文件**（如文件名、路径、大小等）
- ❌ **不适用**：网页搜索、代码/文件**内容搜索**（如文本内容、代码第多少行）

## 功能特性

|    特    性  |         说        明                  |
|-------------|---------------------------------------|
| 极速搜索     | 基于 Everything 的即时索引，毫秒级响应  |
| 词元友好     | 本地工具搜索，降低直接用智能体的词元消耗 |
| 多维索引     | 文件名、后缀扩展名、文件大小、完整路径   |
| 人类可读输出 | 自动转换大小单位（B/KB/MB/GB/TB）       |
| 中文编码支持 | 自动纠正中文路径和文件名的编码问题       |
| 纯搜索模式   | 默认不存储文件索引信息，保护隐私         |
| 自动发现     | 自动检测 Everything 安装位置和 es.exe  |
| 后台启动     | Everything 未运行时自动后台启动        |

## 使用示例
### 1. 在 agents 中触发搜索
```bash
输入：使用everything-search-v1技能搜索文件 "陈绮贞 - 太聪明"
```
### 2. 命令行示例

```bash
输入：python scripts/search_core.py "陈绮贞 - 太聪明"
```

支持的搜索语法（Everything 语法）：
- `*.pdf` — 搜索所有 PDF 文件
- `report` — 搜索文件名包含 "report" 的文件
- `ext:docx;pdf` — 搜索指定扩展名
- `size:>100mb` — 搜索大于 100MB 的文件
- `path:C:\Users` — 在指定路径下搜索



## 搜索全流程解析（表格好看不？是作者一个一个打上去的[哭]）

当用户触发搜索时，搜索系统按以下顺序执行：

```
┌─────────────────────────────────────────────────────────┐
       a. 直接调用 search_core.py 处理用户输入，
          并提取关键词，再调用 es.exe 搜索                                    
└───────────────────────────┬─────────────────────────────┘
                              │
┌───────────────────────────▼─────────────────────────────┐
             b. 调 用  es.exe   是 否 成 功 ？   
└─────────────────────────────────────────────────────────┘
         是 ↓                                 ↓ 否
┌────────────────────────┐        ┌───────────────────────┐
   c.返回search_core.py                
     处理中文乱码                     1. Everything 已启动？            
└────────────────────────┘           → 后台启动 Everything         
            ↓                           → 重新搜索                    
┌────────────────────────┐                                     
 d. 以表格输出优化后的结果          └───────────────────────┘
└────────────────────────┘                 ↓ 
                                           ↓ 否
                                           ↓
┌─────────────────────────────────────────────────────────┐
  2. es.exe 存在？ 
  → 运行 install.py 探测并保存路径到 path.py  → 重新搜索              
└─────────────────────────────────────────────────────────┘
                            ↓ 否
┌──────────────────────────────────────────────────────────┐
  3. es.exe 版本正确？        
  → 指引用户去官网下载 正确版本的 es.exe 
    移动到 Everything文件夹                 
└──────────────────────────────────────────────────────────┘
                            ↓ 否
┌──────────────────────────────────────────────────────────┐
│                      4. 参考官方资料                      │
└──────────────────────────────────────────────────────────┘
```

## 输出格式

搜索结果以表格形式展示：（文件大小优先以TB/GB/MB/KB/B为单位）

```
文件名                    扩展名    大小       路径
───────────────────────────────────────────────────────────────
report_2024                pdf      2.3 MB     C:\Documents\report_2024.pdf
project_backup             zip      156.7 MB   D:\Backups\project_backup.zip
notes                      txt      12.5 KB    C:\Users\Documents\notes.txt
```


## 📚 官方参考资料

- [Everything 命令行界面帮助信息](https://www.voidtools.com/zh-cn/support/everything/command_line_interface/)
- [Everything 命令行选项帮助信息](https://www.voidtools.com/zh-cn/support/everything/command_line_options/)
- [Everything 所以搜索语法查询](https://www.voidtools.com/support/everything/searching/)
- [Everything 下载](https://www.voidtools.com/zh-cn/downloads/)
- [Everything es.exe 下载](https://www.voidtools.com/zh-cn/downloads/#cli)
- [Everything 更多帮助信息](https://www.voidtools.com/zh-cn/support/everything/)