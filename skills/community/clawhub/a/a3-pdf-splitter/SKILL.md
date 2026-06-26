---
name: a3-pdf-splitter
description: 智能A3试卷PDF切分工具，自动识别试卷中间的空白位置进行切分，将A3格式的试卷PDF转换为A4格式方便打印。当用户提到"切分A3试卷"、"A3转A4"、"PDF切分"、"试卷打印"、"拆分试卷PDF"等相关需求时必须使用此技能。
---

# A3 PDF智能切分工具

## 功能说明
将A3格式的试卷PDF文件智能切分为A4格式，方便打印。工具会自动识别页面中间的最佳空白位置进行切割，避免切到文字内容。

- 支持横向A3页面：左右切分为两个A4页面
- 支持纵向A3页面：上下切分为两个A4页面
- 400DPI高分辨率输出，保证打印质量
- 自动保留原PDF的所有页面顺序

## 依赖安装
使用前需要安装依赖包：
```bash
pip install pypdfium2 pillow
```

## 使用方法
当用户需要切分A3试卷PDF时，按照以下步骤操作：

1. 获取输入PDF文件路径和输出路径
2. 调用切分脚本进行处理
3. 告知用户处理结果和输出文件位置

### 示例调用
```python
from split_a3_smart import split_a3_to_a4_smart

# 切分A3试卷PDF
split_a3_to_a4_smart("输入文件路径.pdf", "输出文件路径.pdf")
```

## 脚本代码
```python
import pypdfium2 as pdfium
from PIL import Image
import os

def find_best_split_position(img, is_horizontal=True):
    """
    智能寻找最佳切割位置：在中间区域寻找最空白的列/行
    is_horizontal=True：左右切（找最佳列）；False：上下切（找最佳行）
    """
    # 转为灰度图像
    gray_img = img.convert('L')
    pixels = list(gray_img.getdata())
    width, height = gray_img.size
    
    if is_horizontal:
        # 左右切：计算每列的像素和，和越大越空白（255是纯白色）
        middle_start = int(width * 0.45)
        middle_end = int(width * 0.55)
        max_sum = -1
        best_x = middle_start
        
        for x in range(middle_start, middle_end):
            col_sum = 0
            for y in range(height):
                col_sum += pixels[y * width + x]
            if col_sum > max_sum:
                max_sum = col_sum
                best_x = x
        return best_x
    else:
        # 上下切：计算每行的像素和
        middle_start = int(height * 0.45)
        middle_end = int(height * 0.55)
        max_sum = -1
        best_y = middle_start
        
        for y in range(middle_start, middle_end):
            row_sum = 0
            for x in range(width):
                row_sum += pixels[y * width + x]
            if row_sum > max_sum:
                max_sum = row_sum
                best_y = y
        return best_y

def split_a3_to_a4_smart(input_path, output_path):
    # 打开PDF文件
    pdf = pdfium.PdfDocument(input_path)
    output_images = []
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        width, height = page.get_size()
        
        # 渲染页面为高分辨率图像（400 DPI）
        scale = 400 / 72
        bitmap = page.render(scale=scale)
        img = bitmap.to_pil()
        
        # A3横向：左右切
        if width > height:
            split_x = find_best_split_position(img, is_horizontal=True)
            print(f"第{page_num+1}页最佳切割位置：x={split_x} (总宽度{img.width})")
            
            # 左半部分
            left_img = img.crop((0, 0, split_x, img.height))
            output_images.append(left_img)
            
            # 右半部分
            right_img = img.crop((split_x, 0, img.width, img.height))
            output_images.append(right_img)
        else:
            # A3纵向：上下切
            split_y = find_best_split_position(img, is_horizontal=False)
            print(f"第{page_num+1}页最佳切割位置：y={split_y} (总高度{img.height})")
            
            # 上半部分
            top_img = img.crop((0, 0, img.width, split_y))
            output_images.append(top_img)
            
            # 下半部分
            bottom_img = img.crop((0, split_y, img.width, img.height))
            output_images.append(bottom_img)
    
    # 保存为PDF
    if output_images:
        output_images[0].save(
            output_path,
            "PDF",
            resolution=400,
            save_all=True,
            append_images=output_images[1:]
        )
    
    print(f"\n处理完成！输出文件：{output_path}")
    print(f"原始页数：{len(pdf)}，切分后页数：{len(output_images)}")
```

## 返回结果
处理完成后，告知用户：
1. 输出文件的保存路径
2. 原始页数和切分后的页数
3. 每个页面的切割位置（可选）

## 注意事项
- 输入文件必须是PDF格式
- 输出文件路径需要有写入权限
- 大文件处理可能需要较长时间，请耐心等待
- 建议输出文件名包含"_A4切分版"等标识，方便区分