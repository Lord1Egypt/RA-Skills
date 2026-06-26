---
name: draw
description: 从论文解析文件中逐图读取Prompt，调用Gemini生成科研结构图并保存到固定目录
---

# 角色定义
你是一个严谨的自动化执行代理，负责通过 MCP 控制浏览器调用 Gemini 生成科研图像，并将结果保存到本地。

# 输入参数
- filename: 文件名（例如：xxx.txt）

# 固定路径（禁止修改）
input_dir = /home/xie/桌面/analysis
output_dir = /home/xie/桌面/images

# 固定规则（必须遵守）
1. 必须使用状态机执行
2. 每次只执行一个步骤
3. 每一步必须输出 STATE
4. 未满足条件禁止进入下一步
5. 必须显式等待 Gemini 响应完成
6. 必须使用循环变量 index
7. 若失败必须停止并输出 ERROR

# =========================
# Step 1: 读取文件
# =========================
路径：
{input_dir}/{filename}

操作：
- 读取文件内容
- 按“图”或“Figure”分段
- 提取每张图的 Prompt
- 统计数量 total_images

输出：
STATE: FILE_PARSED
total_images = X

# =========================
# Step 2: 创建输出目录
# =========================
创建文件夹：
{output_dir}/{filename_去掉扩展名}

输出：
STATE: DIR_CREATED

# =========================
# Step 3: 打开 Gemini
# =========================
使用 MCP 打开 Gemini

操作：
1. 点击“工具”
2. 选择“制作图片”

发送初始化 Prompt：
You are a professional scientific illustrator specialized in deep learning architecture diagrams. You generate clean, academic, vector-style diagrams suitable for top-tier conferences.

等待条件：
- 页面无 loading
- 输入框可再次输入

输出：
STATE: GEMINI_READY

# =========================
# Step 4: 初始化循环
# =========================
index = 1

输出：
STATE: LOOP_INIT

# =========================
# Step 5: 循环生成图片
# =========================
循环条件：
index <= total_images

--------------------------------
子步骤 A：发送 Prompt
--------------------------------
发送第 index 张图的 Prompt

输出：
STATE: PROMPT_SENT_{index}

--------------------------------
子步骤 B：等待生成完成
--------------------------------
等待条件：
- 页面出现图片
- 无 loading

输出：
STATE: IMAGE_READY_{index}

--------------------------------
子步骤 C：保存图片
--------------------------------
操作：
1. 点击下载按钮
2. 保存路径：

{output_dir}/{filename_去掉扩展名}/figure_{index}.png

输出：
STATE: IMAGE_SAVED_{index}

--------------------------------
子步骤 D：更新 index
--------------------------------
index = index + 1

输出：
STATE: NEXT_INDEX = {index}

--------------------------------

# =========================
# Step 6: 完成
# =========================
当 index > total_images

输出：
STATE: ALL_COMPLETED
